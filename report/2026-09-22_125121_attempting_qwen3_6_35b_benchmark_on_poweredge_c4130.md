# PowerEdge C4130 で Qwen3.6 35B の測定を試行（CUDA 初期化エラーで未計測）

- **作成者**: jin
- **作成日**: 2026-09-22

## 概要

Dell PowerEdge C4130 上で Qwen3.6-35B-A3B-UD-Q4_K_M のベンチマークを試行した。
Tesla P100-PCIE-12GB は PCIe 上に3枚存在し、`nvidia-smi` はうち2枚を認識したが、CUDA 初期化が失敗した。
llama-split-bench の layer モードのスモークテストはサーバ起動中に終了し、速度は未計測。本レポートは実行失敗の記録であり、性能比較結果ではない。

## ハードウェア

| 項目 | 内容 |
|------|------|
| コンピュータ / マザーボード | Dell PowerEdge C4130 / Dell 0VCHW8 |
| GPU | Tesla P100-PCIE-12GB × 3（VRAM 公称12GB / 枚）。nvidia-smi で認識された2枚を測定対象に指定 |
| GPU 接続 | PCIe。今回の測定試行時のリンク世代・幅、NVLink の有無は未確認 |
| CPU | Intel Xeon E5-2637 v3 @ 3.50GHz × 2（合計8コア / 16スレッド） |
| メモリ | OS 認識約15.04 GiB（16,147,992,576 bytes）、種類は不明 |

## ソフトウェア環境

| 項目 | 内容 |
|------|------|
| OS | Ubuntu 26.04.1 LTS / Linux 7.0.0-31-generic |
| GPU ドライバ | NVIDIA 580.173.02 |
| llama.cpp | 0.4.0-dev、build 1、commit 6a1a922d269908a29cbd4b49c27e6a8e7fd10fae、既存 CUDA ビルド |
| CUDA ビルド設定 | CMakeCache の CMAKE_CUDA_ARCHITECTURES=60、GGML_CUDA=ON |

## ベンチマーク

### 条件

以下は実際に試行したスモークテストの条件。本番測定は実施していない。

| 項目 | 内容 |
|------|------|
| ツール | llama-split-bench commit 7af72d4085aa5073677d41389144112dd94fcb74 |
| モデル | Qwen3.6-35B-A3B-UD-Q4_K_M.gguf、22,134,528,992 bytes（約20.61 GiB） |
| 測定モード | layer、デバイス CUDA0,CUDA1 |
| ctx / stages | 8192 / 0,4000 |
| 各段の生成長 | 100 tokens（スモークテスト） |
| 新規プロンプト長 | 512,2048 tokens |
| KV キャッシュ | K=q8_0 / V=q8_0 |
| 投機的デコード | なし |
| GPU オフロード / Flash Attention | 全レイヤー指定 / on |
| CPU スレッド / batch / ubatch | 8 / 256 / 128 |
| 実プロンプト補正 | 無効（--no-real） |
| 実行日時 | 2026-09-22 12:51 UTC |

### 結果

**未計測（スモークテストがサーバ起動段階で失敗）。** prefill / decode の速度、比較図、results JSON は生成されていない。

測定ツールは次の完了状態を返した（プロセス終了コード1）。

```text
BENCH-ABORT: layer server process exited during startup
```

サーバのエラーは以下のとおり。

```text
ggml_cuda_init: failed to initialize CUDA: invalid device ordinal
error while handling argument "--device": invalid device: CUDA0
```

CUDA ドライバ API を直接呼び出した確認でも、`cuInit(0)` はエラー101（`invalid device ordinal`）を返した。
正常に認識された2枚を `CUDA_VISIBLE_DEVICES` に GPU UUID で指定しても、デバイス一覧は空だった。
UUID 自体は本レポートに記載していない。

### 所感・再測定に必要な対応

同じ起動セッションのカーネルログには、PCIe `0000:83:00.0` の GPU について次のエラーが記録されている。

```text
GPU does not have the necessary power cables connected.
RmInitAdapter failed! (0x24:0x1c:1603)
```

GPU の電源接続エラーと CUDA 初期化失敗を確認した。ただし、両者の因果関係は復旧後の再確認が必要であり、モデルや split-mode の性能については判断できない。
電源を切った状態で該当 GPU の補助電源接続を確認し、CUDA のデバイス一覧が正常に取得できる状態でスモークテストを再実行する必要がある。
また、作図用の matplotlib が未導入のため、本番測定前に準備する必要がある。今回のサーバ起動失敗とは別の問題である。

ローカルの `src/llama-split-bench/bench.local.conf` に再実行用設定を保存した。
生のサーバログやユーザ名を含む絶対パスは公開用添付に含めていない。
