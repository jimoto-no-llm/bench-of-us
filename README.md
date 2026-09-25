# bench-of-us

ローカル LLM ユーザが、**自分のハードウェア構成とベンチマーク結果を持ち寄って共有する**ためのリポジトリです。

「この GPU の組み合わせでこのモデルはどれくらい出るのか」「マルチ GPU は layer 分割と tensor 分割のどちらが速いのか」を、実機の記録として集めます。

## Website

Bench of Us は、ブラウズできるベンチマークデータベースとしても公開しています。

https://jimoto-no-llm.github.io/bench-of-us/

サイトは `report/` の Markdown から自動生成されます（`site/`）。レポートを追加する手順は今までどおりで、
main にマージされると GitHub Actions がサイトを再生成します。サイト向けの追加作業は不要です。

## 参加方法

1. このリポジトリを fork して clone します。
2. （任意）手元でベンチマークを実行します。ベンチマークには [llama-split-bench](https://github.com/kuraneko1/llama-split-bench) を使います。
3. `report/` にレポートを 1 本追加します。
4. pull request を作成します。

**ベンチマークを取らず、ハードウェア情報だけを共有するのも歓迎**です。

### Claude Code 等のコーディングエージェントを使う場合

Claude Code、Codex、OpenCodeなどのコーディングエージェントを使用する場合は、リポジトリのルートでコーディングエージェントを起動し、「ベンチマークを実行して」と頼んでください。
[CLAUDE.md](CLAUDE.md) の手順に従って、作成者名の確認・ハードウェアの調査・ベンチマークの実行・レポートの作成・PR の作成までを進めます。

### 手で書く場合

[CLAUDE.md](CLAUDE.md) の「レポートの形式」にあるテンプレートを使ってください。

- ファイル名: `report/yyyy-mm-dd_HHMMSS_<タイトルの英訳>.md`
- 必須項目: 作成者、コンピュータ（またはマザーボード）の型番、GPU の型番、ベンチマーク結果（未実施なら「未実施」）
- 図や JSON は `report/attachment/<レポートのbasename>/` に置きます
- 下の「レポート一覧」の表に 1 行追加します

## レポート一覧

新しいものが上です。

<!-- レポートを追加したら、表の区切り行（|------|...）の直後に 1 行追加する。表の中にコメントを入れると表が壊れるので、この注記は表の外に置く -->

| 日付 | タイトル | 作成者 | コンピュータ / マザーボード | GPU | ベンチ |
|------|----------|--------|-----------------------------|-----|--------|
| 2026-09-25 | [Tesla P40 4 枚で Qwen3.8 27B の split-mode を比較（単一 GPU ベースライン付き）](report/2026-09-25_222946_comparing_split_modes_of_qwen3.8_27b_on_4x_tesla_p40_with_single_gpu_baseline.md) | 0kqnet | Supermicro X10DRG-Q | Tesla P40 × 4 | Qwen3.8 27B UD-Q4_K_XL |
| 2026-09-24 | [Tesla V100-SXM2-32GB 2 枚で Qwen3.8 Flash Next（MoE）の layer 分割と単一 GPU を比較](report/2026-09-24_144622_comparing_layer_split_and_single_gpu_of_qwen3.8_flash_next_on_2x_tesla_v100_sxm2_32gb.md) | pentacoxian | Inspur NF5468M5 | Tesla V100-SXM2-32GB × 2 | Qwen3.8 Flash Next IQ3E-Q8D-MTP |
| 2026-09-23 | [Tesla V100 2 枚で Qwen3.8 27B の split-mode を比較](report/2026-09-23_060231_comparing_split_modes_of_qwen3.8_27b_on_2x_tesla_v100.md) | miminashi | ASRock X99 Taichi | Tesla V100-SXM2-16GB × 2 | Huihui Qwen3.8 27B abliterated UD-Q4_K_XL |
| 2026-09-22 | [Tesla V100 2枚で Qwen3.8 27B の split-mode を比較（単一GPU ベースライン付き）](report/2026-09-22_210206_comparing_split_modes_of_qwen3.8_27b_on_2x_tesla_v100_with_single_gpu_baseline.md) | kuraneko1 | ASUS Z170-A | Tesla V100-PCIE-32GB + Tesla PG500-216 | Qwen3.8 27B UD-Q4_K_M |
| 2026-09-21 | [RTX 3060 + Tesla V100 で Qwen3.8 27B の tensor split を NCCL あり／なしで比較](report/2026-09-21_183303_comparing_nccl_vs_no_nccl_tensor_split_on_rtx3060_and_tesla_v100.md) | eightman999 | Thirdwave XA7C-R47T / ASRock B760 TW/D4 | RTX 3060 12GB + Tesla V100-PCIE-32GB | Qwen3.8 27B Q4_K_M NCCL |
| 2026-09-21 | [RTX 3060 + Tesla V100 で Qwen3.8 27B の split-mode を比較](report/2026-09-21_170911_comparing_split_modes_of_qwen3.8_27b_on_rtx3060_and_tesla_v100.md) | eightman999 | Thirdwave XA7C-R47T / ASRock B760 TW/D4 | RTX 3060 12GB + Tesla V100-PCIE-32GB | Qwen3.8 27B Q4_K_M |
| 2026-09-20 | [Tesla P100 7 枚で Qwen3.8 27B の split-mode を比較](report/2026-09-20_072013_comparing_split_modes_of_qwen3.8_27b_on_7x_tesla_p100.md) | miminashi | Supermicro SYS-4028GR-TRT2 | Tesla P100 × 7 | Qwen3.8 27B UD-Q4_K_XL |
| 2026-09-20 | [Tesla P100 4 枚で Qwen3.8 27B の split-mode を比較](report/2026-09-20_033840_comparing_split_modes_of_qwen3.8_27b_on_4x_tesla_p100.md) | miminashi | NEC Express5800/T120h | Tesla P100 × 4 | Qwen3.8 27B UD-Q4_K_XL |

レポートの本体は [report/](report/) にあります。

## 注意

- シリアル番号・MAC アドレス・ホスト名・IP アドレスなど、個人を特定しうる情報は載せないでください。
- モデルファイル（`.gguf`）やベンチマークのサーバログはコミットしないでください。
