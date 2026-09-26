# EPYC 7452 × 2 と RTX 5070 Ti × 2 で DeepSeek V4-Flash-Vision-Exp（abliterated、MXFP4）を sglang＋KTransformers で動かす

- **作成者**: amane.yukishima
- **作成日**: 2026-09-26

## 概要

RTX 5070 Ti 2 枚（VRAM 計 32 GB、GPU 間 P2P なし）と RAM 512 GB で、147 GB の DeepSeek V4-Flash-Vision-Exp（Huihui による abliterated 版、エキスパートは MXFP4）を sglang＋KTransformers で動かしています。エキスパートの大半は CPU で計算し、使用頻度の高いものだけ GPU に置いています。
約 38K トークンの prefill が 615 t/s（62 秒）、decode が 43〜44 t/s でした。コンテキスト長は 1M に設定し、KV キャッシュは 262K トークン分を確保しています。
長いプロンプトでは、エキスパートの重みを層ごとに PCIe で GPU へ転送しながら計算し、その間に CPU も一部のエキスパートを並行して計算します。

## ハードウェア

| 項目 | 内容 |
|------|------|
| コンピュータ / マザーボード | HUANANZHI H12D-16D（デュアル SP3） |
| GPU | GeForce RTX 5070 Ti × 2（VRAM 16 GB / 枚） |
| GPU 接続 | 両 GPU とも PCIe Gen4 x16。GPU0 は CPU0 側、GPU1 は CPU1 側に接続されていて、`nvidia-smi topo -m` は SYS（GPU 間の P2P なし）。ピン留めしたホストメモリから GPU への転送は 1 枚あたり 25〜26 GB/s（自作ベンチ、同じ NUMA ノード）、ソケットをまたぐと 23 GB/s |
| CPU | AMD EPYC 7452 × 2（32 コア / 64 スレッド × 2、Zen 2、AVX2 まで・AVX-512 なし、NUMA 2 ノード、L3 256 MiB） |
| メモリ | 約 512 GiB（`free -h` で 499 GiB）。種類は不明 |
| ストレージ | モデルは NVMe SSD に配置 |
| 電源 | 不明 |

## ソフトウェア環境

| 項目 | 内容 |
|------|------|
| OS | Ubuntu 26.04 LTS / Linux 7.0.0-34-generic |
| GPU ドライバ | 595.91.07（CUDA 13） |
| 推論エンジン | sglang（kvcache-ai/sglang をベースに独自パッチ）＋ KTransformers の kt-kernel（AVX2 ビルド＋独自パッチ）。llama.cpp は使っていません |
| 並列化 | テンソル並列 2（TP=2）。CPU 側のエキスパートは kt-kernel が 2 ソケットに分けて計算 |

## 独自の変更

どれも、GPU 間 P2P のない GeForce 2 枚と、AVX-512 のない Zen 2 で大きな MoE を動かすために入れたものです。一部は本家に PR を出しています。

全モデル共通:

- **エキスパートの CPU/GPU 分担**: 実際のルーティング頻度から選んだ使用頻度の高いエキスパートを GPU に置き、残りを CPU で計算。GPU に置いたエキスパートの重みが別のエキスパートのものとして読み込まれるバグを見つけて修正（[kvcache-ai/sglang#97](https://github.com/kvcache-ai/sglang/pull/97)）
- **P2P なし 2 枚向けの all-reduce**: decode 時の小さな all-reduce を、両 GPU からマップしたピン留めホストメモリ経由の 1 カーネルにまとめ、NCCL（SHM 経路）の 22〜25 µs を 5 µs に短縮（[sgl-project/sglang#39605](https://github.com/sgl-project/sglang/pull/39605)）。prefill 時の大きな all-reduce は、ホストメモリを経由してコピーエンジンで転送
- **CPU の計算結果の受け渡し**: kt-kernel と GPU の間の受け渡しを、ホスト関数のコールバックから GPU のストリーム上でフラグを書いて待ち合わせる方式（`cuStreamWriteValue32` / `cuStreamWaitValue32`）に置き換え、decode の 1 トークンごとの待ち時間を削減
- **AVX2 のエキスパートカーネル**: Zen 2 向けの MXFP4 / NVFP4 カーネル。本家にも複数マージ済み（kvcache-ai/ktransformers #2175, #2176, #2205, #2209, #2210）
- **ホスト経由の all-reduce の競合を修正**: 1 MiB 以上の all-reduce で、自分の入力をホストへ送り終える前にその場で加算していたため、長いプロンプトでまれに誤った和になっていました。修正後は同じ入力に対する出力がビット単位で一致します（速度は変わりません）

このモデル向け:

- **エキスパートを GPU へ転送しながらの prefill**: 1 層あたり約 2 GB のエキスパートを 78 ms で転送して GPU で計算。PCIe Gen4 x16 の帯域（実測 25.8 GB/s）をほぼ使い切っています
- **転送中の CPU 並行計算**: GPU が転送を待つ間に CPU が一部のエキスパートを計算して加算。prefill が 8% 向上
- **AVX2 の MXFP4 カーネル（グループサイズ 32）**: ループ順の入れ替えと K 方向のブロッキングで、CPU 側の prefill の行列積を 1.33 倍に（出力はビット単位で一致）
- **decode**: CPU と GPU の計算を重ねる deferred 実行をやめ、上記の受け渡しの改善と all-reduce を入れて 33.5 → 44 t/s
- **思考モードの既定値**: サーバ側で思考あり・reasoning effort max を既定にするパッチ（今回の計測は思考なし）

## ベンチマーク

llama.cpp を使っていないため、llama-split-bench では計測していません。sglang の OpenAI 互換 API に自作スクリプトでリクエストを送り、経過時間と usage から t/s を計算しています。llama-split-bench のレポートとは条件が異なるため、直接は比較できません。

### 条件

| 項目 | 内容 |
|------|------|
| ツール | 自作スクリプト。サーバを起動し、prefill 2 種類と decode を各 2 回計測して停止する。全モデルを同じスクリプトで計測 |
| prefill | 実際に使っている約 38K トークンのプロンプト（日本語の執筆指示）と、その先頭 11,000 文字（約 6K トークン）を max_tokens 1 で送信。表は 2 回目の値（1 回目は起動直後のウォームアップを含む）。プロンプトの先頭に毎回異なる文字列を付けてプレフィックスキャッシュを無効化 |
| decode | 短いプロンプトから 512 トークンを生成（`ignore_eos`、思考なし）。2 回の範囲 |
| サンプリング | temperature 1.0 / top_p 0.95 |
| 投機的デコード | なし |
| 同時リクエスト | 1 |
| 測定日 | 2026-09-26 |

### モデルと構成

| 項目 | 内容 |
|------|------|
| モデル | DeepSeek V4-Flash-Vision-Exp の abliterated 版。[huihui-ai/Huihui-DeepSeek-V4-Flash-Vision-Exp-abliterated-GGUF](https://huggingface.co/huihui-ai/Huihui-DeepSeek-V4-Flash-Vision-Exp-abliterated-GGUF) を sglang で読める形式に自前で変換 |
| 量子化・サイズ | エキスパートは GGUF の MXFP4 をそのまま使用、エキスパート以外の重みは FP8。147 GB |
| 構造 | 43 層、ルーティングされるエキスパート 256 個中 6 個がアクティブ |
| GPU に置くもの | エキスパート以外のすべてと、各層で使用頻度の高いエキスパート 10 個 |
| prefill | 一定以上の長さでは、エキスパートを層ごとに GPU へ転送して計算。同時に CPU がエキスパート 3 グループ分を並行して計算 |
| コンテキスト長 | 1M（KV キャッシュの確保は 262K トークン）、KV キャッシュは FP8（e4m3） |

### 結果

| 構成 | prefill 38K（t/s） | prefill 6K（t/s） | decode（t/s） |
|---|---:|---:|---:|
| 高頻度エキスパート 10 個 / 層を GPU、prefill は GPU へ転送＋CPU 並行 | 615（38,073 トークン / 61.9 秒） | 627（6,053 トークン / 9.6 秒） | 42.9〜43.7 |

- 1 回目の 38K prefill はウォームアップを含めて 558 t/s でした。

### 所感

- prefill は PCIe の帯域で頭打ちです。これ以上速くするには、転送するエキスパートのバイト数を減らすか、CPU の分担を増やす必要があり、CPU 側のカーネルの高速化を続けています。
- VRAM 16 GB × 2 枚では 147 GB のモデルの 1 割も GPU に載りませんが、decode は GPU に置いたエキスパートと CPU のメモリ帯域で 40 t/s 台に届きました。
- GPU 間 P2P のない 2 枚では、NCCL の SHM 経路が decode の all-reduce で重く、ホストメモリ経由の all-reduce に替えるだけで decode が 4〜6% 伸びました。
- 別のモデルを読み込んだ直後にサーバを起動すると、片方の NUMA ノードがページキャッシュで埋まり、CPU 側のエキスパートの一部が反対側のノードに配置されて decode が 43 → 36 t/s に落ちました。起動前にモデルファイルのページキャッシュを破棄して回避しています（root 権限は不要）。

## 添付

なし（計測スクリプトは自作。数値は 2026-09-26 の計測ログから）。
