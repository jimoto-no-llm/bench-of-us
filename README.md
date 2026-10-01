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
| 2026-09-29 | [Strata を sm_70 対応させ Tesla V100 32GB にエキスパート 2 万個を常駐させる](report/2026-09-29_105132_sm70_port_and_full_v100_residency_for_strata_flash_next.md) | eightman999 | Thirdwave XA7C-R47T / ASRock B760 TW/D4 | RTX 3060 12GB + Tesla V100-PCIE-32GB | Qwen3.8-Flash-Next Q2_0 |
| 2026-09-28 | [RTX 5060 TiでGemma 4 26B A4B QAT-MTPを131Kコンテキストまで計測](report/2026-09-28_210656_profiling_gemma4_26b_a4b_qat_mtp_on_rtx5060ti.md) | RockinWool | ASRock B650 PG Lightning | RTX 5060 Ti + RTX 5070 | Gemma4 26B A4B QAT Q4_K_M + MTP（131K、単一GPU） |
| 2026-09-28 | [RX 7900 XT + RX 7800 XTでQwen3.8 27B IQ4 XSのsplit-modeを比較](report/2026-09-28_040646_qwen3_8_27b_iq4xs_128k_benchmark_on_rx7900xt_and_rx7800xt.md) | ogawara | ASUS ProArt X870E-CREATOR WIFI | RX 7900 XT + RX 7800 XT | Qwen3.8 27B UD-IQ4_XS（128K、各構成3回） |
| 2026-09-27 | [RTX 3090 4 枚で Qwen3.8 27B の split-mode を比較（Windows・コア1395 MHz固定設定）](report/2026-09-27_130914_comparing_qwen3.8_27b_split_modes_on_4x_rtx3090_at_1395mhz_on_windows.md) | 錦幸佳 | ASUS ROG CROSSHAIR VIII DARK HERO | RTX 3090 × 4 | Qwen3.8 27B UD-Q4_K_XL |
| 2026-09-27 | [GTX 1660 SUPER 6GBで Qwen2.5-Coder 7B のGPU/CPUオフロードを計測](report/2026-09-27_124604_measuring_gpu_cpu_offload_of_qwen2_5_coder_7b_on_gtx1660super_6gb.md) | antarashi | ASRock B450 Pro4 | GTX 1660 SUPER × 1 | Qwen2.5-Coder 7B Q4_K_M |
| 2026-09-27 | [RTX 5090 1 枚で Qwen3.8 27B UD-Q5_K_XL を 262k コンテキストまで計測](report/2026-09-27_060846_profiling_qwen3.8_27b_ud_q5_k_xl_up_to_262k_context_on_rtx5090.md) | unco3 | ASRock Z790 Steel Legend WiFi | RTX 5090 × 1 | Qwen3.8 27B UD-Q5_K_XL |
| 2026-09-26 | [RTX 5090 で Qwen3.8 27B を 262k コンテキストで測定](report/2026-09-26_203225_measuring_qwen3_8_27b_at_262k_context_on_rtx_5090.md) | completenovice-eng | Micro-Star International Co., Ltd. PRO B650-S (MS-7E26) | RTX 5090 × 1 | Huihui-Qwen3.8-27B-abliterated-Q4_K |
| 2026-09-26 | [EVO-X2 128GBでQwen3.8-Flash-NextをHalogenで実行](report/2026-09-26_171511_running_qwen3.8_flash_next_with_halogen_on_evo_x2_128gb.md) | A-Uta | GMKtec NucBox EVO-X2 | Radeon 8060S × 1 | Qwen3.8 Flash Next W4B（Halogen） |
| 2026-09-26 | [Tesla T4 4 枚で Qwen3.8 27B の split-mode と量子化を比較](report/2026-09-26_084514_comparing_split_modes_and_quantizations_of_qwen3.8_27b_on_4x_tesla_t4.md) | MG8853 | HPE ProLiant DL380 Gen10 | Tesla T4 × 4 | Qwen3.8 27B UD-Q4_K_XL / UD-Q6_K / Q8_0 |
| 2026-09-26 | [RTX 5070 12GB 1枚で Qwen3.8 27B GSQ IQ2_S を計測（8K短縮プロファイル）](report/2026-09-26_094401_profiling_qwen3.8_27b_gsq_iq2_s_on_rtx5070_12gb.md) | fumimatsu | GIGABYTE X870M AORUS ELITE WIFI7 ICE | RTX 5070 × 1 | Qwen3.8 27B GSQ-RCO IQ2_S |
| 2026-09-26 | [EPYC 7452 × 2 と RTX 5070 Ti × 2 で Qwen3.5-35B-A3B を BF16 のまま CPU/GPU 分担で動かす](report/2026-09-26_093349_running_qwen3.5_35b_a3b_in_bf16_on_2x_epyc_7452_and_2x_rtx_5070_ti_with_cpu_gpu_hybrid.md) | amane.yukishima | HUANANZHI H12D-16D | RTX 5070 Ti × 2 | Qwen3.5-35B-A3B BF16（sglang＋KTransformers、自作計測） |
| 2026-09-26 | [EPYC 7452 × 2 と RTX 5070 Ti × 2 で GLM-5.3-Flash Uncensored を動かし、GPU での prefill と GPU 常駐エキスパートを比較](report/2026-09-26_093348_running_glm_5.3_flash_uncensored_on_2x_epyc_7452_and_2x_rtx_5070_ti_comparing_gpu_prefill_and_hot_experts.md) | amane.yukishima | HUANANZHI H12D-16D | RTX 5070 Ti × 2 | GLM-5.3-Flash Uncensored FP8＋NVFP4 エキスパート（sglang＋KTransformers、自作計測） |
| 2026-09-26 | [EPYC 7452 × 2 と RTX 5070 Ti × 2 で DeepSeek V4.1-Flash（476 GB）をコンテキスト長 1M で動かす](report/2026-09-26_093347_running_deepseek_v4.1_flash_with_1m_context_on_2x_epyc_7452_and_2x_rtx_5070_ti_with_sglang_and_ktransformers.md) | amane.yukishima | HUANANZHI H12D-16D | RTX 5070 Ti × 2 | DeepSeek V4.1-Flash FP8＋FP4 エキスパート（sglang＋KTransformers、自作計測） |
| 2026-09-26 | [EPYC 7452 × 2 と RTX 5070 Ti × 2 で DeepSeek V4-Flash-Vision-Exp（abliterated、MXFP4）を sglang＋KTransformers で動かす](report/2026-09-26_093346_running_deepseek_v4_flash_vision_exp_abliterated_mxfp4_on_2x_epyc_7452_and_2x_rtx_5070_ti_with_sglang_and_ktransformers.md) | amane.yukishima | HUANANZHI H12D-16D | RTX 5070 Ti × 2 | DeepSeek V4-Flash-Vision-Exp abliterated MXFP4（sglang＋KTransformers、自作計測） |
| 2026-09-25 | [DGX互換機 Lenovo Thinkstation PGX 1台で Qwen3.8 Flash Next（MoE）を 262k コンテキストまで計測](report/2026-09-25_171942_qwen3_8_flash_next_single_gpu_on_nvidia_gb10.md) | 0rangaxx | Lenovo 30KLS01900 | NVIDIA GB10（統合メモリ）× 1 | Qwen3.8 Flash Next IQ3E-Q8D-MTP |
| 2026-09-25 | [Tesla P40 4 枚で Qwen3.8 27B の split-mode を比較（単一 GPU ベースライン付き）](report/2026-09-25_222946_comparing_split_modes_of_qwen3.8_27b_on_4x_tesla_p40_with_single_gpu_baseline.md) | 0kqnet | Supermicro X10DRG-Q | Tesla P40 × 4 | Qwen3.8 27B UD-Q4_K_XL |
| 2026-09-24 | [Tesla V100-SXM2-32GB 2 枚で Qwen3.8 Flash Next（MoE）の layer 分割と単一 GPU を比較](report/2026-09-24_144622_comparing_layer_split_and_single_gpu_of_qwen3.8_flash_next_on_2x_tesla_v100_sxm2_32gb.md) | pentacoxian | Inspur NF5468M5 | Tesla V100-SXM2-32GB × 2 | Qwen3.8 Flash Next IQ3E-Q8D-MTP |
| 2026-09-23 | [Tesla V100 2 枚で Qwen3.8 27B の split-mode を比較](report/2026-09-23_060231_comparing_split_modes_of_qwen3.8_27b_on_2x_tesla_v100.md) | miminashi | ASRock X99 Taichi | Tesla V100-SXM2-16GB × 2 | Huihui Qwen3.8 27B abliterated UD-Q4_K_XL |
| 2026-09-22 | [Tesla V100 2枚で Qwen3.8 27B の split-mode を比較（単一GPU ベースライン付き）](report/2026-09-22_210206_comparing_split_modes_of_qwen3.8_27b_on_2x_tesla_v100_with_single_gpu_baseline.md) | kuraneko1 | ASUS Z170-A | Tesla V100-PCIE-32GB + Tesla PG500-216 | Qwen3.8 27B UD-Q4_K_M |
| 2026-09-28 | [RTX 3060 12GB + RAM で Strata により Qwen3.8-Flash-Next（125B MoE）を回す](report/2026-09-28_142648_strata_flash_next_q20_on_rtx3060_plus_ram.md) | eightman999 | Thirdwave XA7C-R47T / ASRock B760 TW/D4 | RTX 3060 12GB | Qwen3.8-Flash-Next Q2_0 |
| 2026-09-21 | [RTX 3060 + Tesla V100 で Qwen3.8 27B の tensor split を NCCL あり／なしで比較](report/2026-09-21_183303_comparing_nccl_vs_no_nccl_tensor_split_on_rtx3060_and_tesla_v100.md) | eightman999 | Thirdwave XA7C-R47T / ASRock B760 TW/D4 | RTX 3060 12GB + Tesla V100-PCIE-32GB | Qwen3.8 27B Q4_K_M NCCL |
| 2026-09-21 | [RTX 3060 + Tesla V100 で Qwen3.8 27B の split-mode を比較](report/2026-09-21_170911_comparing_split_modes_of_qwen3.8_27b_on_rtx3060_and_tesla_v100.md) | eightman999 | Thirdwave XA7C-R47T / ASRock B760 TW/D4 | RTX 3060 12GB + Tesla V100-PCIE-32GB | Qwen3.8 27B Q4_K_M |
| 2026-09-20 | [Tesla P100 7 枚で Qwen3.8 27B の split-mode を比較](report/2026-09-20_072013_comparing_split_modes_of_qwen3.8_27b_on_7x_tesla_p100.md) | miminashi | Supermicro SYS-4028GR-TRT2 | Tesla P100 × 7 | Qwen3.8 27B UD-Q4_K_XL |
| 2026-09-20 | [Tesla P100 4 枚で Qwen3.8 27B の split-mode を比較](report/2026-09-20_033840_comparing_split_modes_of_qwen3.8_27b_on_4x_tesla_p100.md) | miminashi | NEC Express5800/T120h | Tesla P100 × 4 | Qwen3.8 27B UD-Q4_K_XL |

レポートの本体は [report/](report/) にあります。

## 注意

- シリアル番号・MAC アドレス・ホスト名・IP アドレスなど、個人を特定しうる情報は載せないでください。
- モデルファイル（`.gguf`）やベンチマークのサーバログはコミットしないでください。
