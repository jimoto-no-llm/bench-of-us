# CLAUDE.md

このファイルは、Claude Code (claude.ai/code) がこのリポジトリで作業する際のガイダンスです。

**応答言語**: 日本語で応答してください。レポート本文も日本語で書きます。

---

## プロジェクト概要

**bench-of-us** は、ローカル LLM ユーザが**自分のハードウェア構成とベンチマーク結果を共有する**ためのリポジトリです。

参加の流れ:

1. 参加者がこのリポジトリを fork / clone する
2. 手元でベンチマーク（[llama-split-bench](https://github.com/kuraneko1/llama-split-bench)）を実行する（**任意**）
3. `report/` にレポートを 1 本書く
4. pull request を作成してレポートを共有する

**ベンチマークを実行せず、ハードウェア情報だけを共有するレポートも歓迎**します。その場合もベンチマーク結果の節は省略せず「未実施」と明記します。

---

## ディレクトリ構成

| パス | 内容 | git 管理 |
|------|------|----------|
| `report/` | レポート本体（`.md`）。**レポートは必ずここに作成する** | する |
| `report/attachment/<レポートのbasename>/` | レポートの添付（図・JSON） | する |
| `src/` | ベンチマークツールの clone 先（`src/llama-split-bench/`） | しない |
| `.author` | レポート作成者名（1 行） | しない |

---

## レポート作成の手順

ユーザから「ベンチマークを実行して」「レポートを作って」「ベンチを取って共有したい」などと頼まれたら、以下の順に進めます。

### 1. 作成者名を決める

- `.author` があれば、その内容を作成者名として使う。
- 無ければ**ユーザに聞く**（`git config user.name` の値を候補として示してよい）。回答を `.author` に 1 行で保存し、次回以降はそれを使う。
- 本名である必要はない。ハンドルネームでよい。

### 2. ハードウェアを調査する

sudo 不要のコマンドを優先します。**Claude は sudo を直接実行しません**。sudo が必要な場合（`dmidecode` など）はコマンドをユーザに提示して実行を依頼してください。

| 項目 | 調べ方 |
|------|--------|
| コンピュータ / マザーボード型番 | `cat /sys/class/dmi/id/{sys_vendor,product_name,board_vendor,board_name}` |
| GPU（NVIDIA） | `nvidia-smi --query-gpu=name,memory.total,driver_version,pcie.link.gen.current,pcie.link.width.current --format=csv` |
| GPU（AMD） | `rocm-smi --showproductname --showmeminfo vram` |
| GPU（共通） | `lspci \| grep -iE 'vga\|3d\|display'`、`vulkaninfo --summary` |
| CPU | `lscpu` |
| メモリ | `free -h` |
| OS | `cat /etc/os-release`、`uname -r` |

- 型番が取得できない、または `To be filled by O.E.M.` / `Default string` / `System Product Name` のような無意味な値の場合は、**ユーザに聞く**。自作 PC ならマザーボード型番、メーカー製 PC ならその機種名を書く。
- 必須はコンピュータ（またはマザーボード）型番と GPU 型番。CPU・メモリ・OS などは分かる範囲で書く。
- **シリアル番号・UUID・MAC アドレス・ホスト名・IP アドレスなどの個人を特定しうる情報はレポートに書かない**。

### 3. ベンチマークを実行する（ユーザが希望する場合のみ）

ベンチマークには [kuraneko1/llama-split-bench](https://github.com/kuraneko1/llama-split-bench) を使います。llama.cpp の `llama-server` で `--split-mode layer` / `tensor` / 単一 GPU を比較し、prefill / decode の速度を context 深さごとに測るツールです。

1. **`src/llama-split-bench/` が無ければ、まず clone する**:
   ```bash
   git clone https://github.com/kuraneko1/llama-split-bench src/llama-split-bench
   ```
2. 以降の使い方は同リポジトリの `README.ja.md` に従う。要点:
   - `bench.conf` を `bench.local.conf` にコピーし、`MODEL`（必須）・`BIN`・`DEVICES`・`CTX`・`SPEC_ARGS` などを設定する。使うモデルと llama.cpp のビルドはユーザに確認する。
   - `./list-devices.sh` でデバイス名を確認する。
   - **まず smoke test（約 4 分）** で動作を確かめてから本番を回す。
   - 本番は `setsid nohup bash run-bench.sh <tag> > runs/<tag>.log 2>&1 &` でデタッチ起動し、ログに `BENCH-DONE`（完了）/ `BENCH-ABORT: …`（失敗）/ `BENCH-FIGFAIL`（図の生成のみ失敗）が出るまでポーリングする。**`tail -f` は終了しないので使わない**。
   - GPU が 1 枚だけなら `--profile` で単一構成の prefill / decode を測れる。
3. 公開前提なので、**`MACHINE` を中立な文字列に設定してホスト名を出さない**（例: `MACHINE="ASUS Pro WS WRX80E-SAGE — 2x RTX 3090"`）。既定の `auto` はホスト名を図のタイトルと `run-info.json` に埋め込む。
4. 結果は `src/llama-split-bench/runs/<tag>/` に出力される。

### 4. レポートを書く

下記「レポートの形式」に従って `report/` にレポートを作り、「添付ファイル」の規則に従ってベンチ結果をコピーします。

### 5. 各言語の README にレポートを追加する

`README.md`（英語の正本）・`README.zh-CN.md`（簡体字中国語）・`README.ja.md`（日本語）のレポート一覧に、それぞれ同じレポートを 1 行追加します。**新しいものが上**なので、表の区切り行（`|------|...`）の直後に挿入します。リンク、日付、作成者、型番とモデル名は一致させ、タイトルや説明部分のみ各言語へ翻訳します。

| 列 | 書く内容 |
|----|----------|
| 日付 | `yyyy-mm-dd`（ファイル名の日付） |
| タイトル | レポートへの相対リンク。`[<タイトル>](report/<ファイル名>.md)` |
| 作成者 | `.author` の名前 |
| コンピュータ / マザーボード | 型番 |
| GPU | `<型番> × <枚数>`（例: `RTX 3090 × 2`）。異なる GPU の混在は `+` でつなぐ |
| ベンチ | 実施なら測定したモデル名（例: `Qwen3 27B Q4_K_M`）、未実施なら `未実施` |

- 表のセル内に `|` を書くと列が崩れるので、使う場合は `\|` とエスケープする。
- 表の中（行と行の間）に HTML コメントや空行を入れない。表が途切れる。
- 既存の行は編集しない。
- 他の人の PR と同時に同じ位置へ行を追加すると衝突することがある。衝突したら upstream の最新を取り込み、両方の行を日付順に残して解消する。

### 6. pull request を作成する

1. ブランチを切る（例: `report/<レポートのbasename>`）。
2. **追加したレポート・添付・README.md / README.zh-CN.md / README.ja.md の一覧変更だけ**を commit する（`src/`・`.author`・モデルファイルは含めない）。
3. fork へ push し、`gh pr create` で PR を作る。PR タイトルはレポートのタイトルと同じにする。
4. **push と PR 作成は外部に公開される操作なので、実行前に必ずユーザに確認する**。

---

## レポートの形式

### ファイル名

```
report/yyyy-mm-dd_HHMMSS_<レポートのタイトルの英訳>.md
```

- 日時はローカル時刻で、`date +%Y-%m-%d_%H%M%S` で取得する。
- タイトル部分は日本語タイトルを**英訳**し、小文字・ASCII・単語区切りは `_` にする。
- 例: タイトル「RTX 3090 2 枚で Qwen3 27B の split-mode を比較」→ `report/2026-09-20_013000_comparing_split_modes_of_qwen3_27b_on_2x_rtx3090.md`

### 必須項目

| 項目 | 内容 |
|------|------|
| 作成者 | `.author` の名前 |
| コンピュータ（またはマザーボード）の型番 | 手順 2 で調査、分からなければユーザに聞く |
| GPU の型番 | 型番・枚数・VRAM 容量 |
| ベンチマーク結果 | 実施した場合は結果表と図。**未実施なら「未実施」と明記する** |

### テンプレート

````markdown
# <タイトル>

- **作成者**: <名前>
- **作成日**: yyyy-mm-dd

## 概要

<構成と結果を 2〜4 行で要約。ハードウェア情報のみの場合はその旨>

## ハードウェア

| 項目 | 内容 |
|------|------|
| コンピュータ / マザーボード | <型番> |
| GPU | <型番> × <枚数>（VRAM <容量> / 枚） |
| GPU 接続 | <PCIe 世代・レーン幅、NVLink の有無など。分かる範囲で> |
| CPU | <型番> |
| メモリ | <容量・種類> |
| 電源 | <任意> |

## ソフトウェア環境

| 項目 | 内容 |
|------|------|
| OS | <ディストリビューション / カーネル> |
| GPU ドライバ | <バージョン> |
| llama.cpp | <バージョン / コミット、バックエンド（CUDA / ROCm / Vulkan / Metal / CPU）> |

## ベンチマーク

### 条件

| 項目 | 内容 |
|------|------|
| ツール | llama-split-bench <コミット> |
| モデル | <モデル名・量子化・ファイルサイズ> |
| 測定モード | <layer / tensor / single / profile など> |
| ctx / stages | <CTX> / <STAGES> |
| KV キャッシュ | <KV_K> / <KV_V> |
| 投機的デコード | <SPEC_ARGS、無しなら「なし」> |

### 結果

![結果](attachment/<レポートのbasename>/split-bench-ja.png)

<depth ごとの prefill / decode（t/s）をモード別に並べた表>

### 所感

<どのモードが速かったか、気づいたこと>

## 添付

- [run-info.json](attachment/<レポートのbasename>/run-info.json)
- <その他の添付>
````

- ベンチ未実施の場合は「ベンチマーク」節を `未実施` の 1 行にし、「添付」節は省く。
- 結果表の数値は `results-<mode>.json`（depth ごとの `prompt_per_second` = prefill、`predicted_per_second` = decode）と `results-<mode>-pp0.json`（depth 0 の prefill）から転記する。ladder の最初の stage の prefill 値は 11 トークンのプロンプトによる計測上の artifact なので**表に載せない**。
- 推測や未確認の情報を事実として書かない。分からない項目は「不明」とする。

---

## 添付ファイル

ベンチを実施した場合、`src/llama-split-bench/runs/<tag>/` から `report/attachment/<レポートのbasename>/` へ次のファイルをコピーします。

| コピーする | コピーしない |
|------------|--------------|
| `*.png`（図、ja / en） | `server-*.log`（バックエンドのログ） |
| `run-info.json` | `real-response-*.txt`、`responses-*/`（プロンプト・出力） |
| `results-*.json` | `sampler-*.log` |
| `argv-*.txt`（サーバの起動引数） | `runs/<tag>.log` |

- コピー前に `run-info.json` と `argv-*.txt` を確認し、**ホームディレクトリのパス（ユーザ名）やホスト名が含まれていれば、ユーザに確認のうえ伏せる**（例: `/home/alice/models/` → `~/models/`）。
- **モデルファイル（`.gguf`）は絶対にコミットしない**。

---

## 注意事項

| 項目 | ルール |
|------|--------|
| 他人のレポート | 既存のレポートは編集しない。自分のレポートを新規に追加する |
| レポート一覧 | レポートを追加したら必ず `README.md` / `README.zh-CN.md` / `README.ja.md` の一覧表に 1 行ずつ追加する（新しいものが上） |
| sudo | Claude は直接実行しない。コマンドを提示してユーザに依頼する |
| 外部公開 | push・PR 作成の前にユーザに確認する |
| 個人情報 | シリアル番号・MAC アドレス・ホスト名・IP アドレス・ユーザ名入りのパスを載せない |
| `src/` | ベンチマークツールの clone 先。git 管理外なので中身を commit しない |
