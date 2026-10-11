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
| 2026-10-11 | [Apple M1 Max 64GB で Qwen3.8 27B UD-Q4_K_M の MTP 投機的デコードを 64k まで比較](report/2026-10-11_125828_comparing_mtp_speculative_decoding_of_qwen3.8_27b_up_to_64k_on_apple_m1_max.md) | Kenya Nara (@penta2himajin) | Apple MacBook Pro 18,4 | Apple M1 Max × 1 | Qwen3.8 27B UD-Q4_K_M（64k、MTP あり/なし） |
| 2026-10-08 | [Tesla V100-PCIE-32GB 1 枚で Qwen3.8 27B UD-Q4_K_M を 262k コンテキストまで計測](report/2026-10-08_105734_profiling_qwen3.8_27b_ud_q4_k_m_up_to_262k_on_tesla_v100_pcie_32gb.md) | sh1ma | Supermicro SYS-1019GP-TT | Tesla V100-PCIE-32GB × 1 | Qwen3.8 27B UD-Q4_K_M（262k、profile） |
| 2026-10-07 | [V100 2枚で Qwen3.8 27B の Layer・Tensor分割と MTP・DFlash2 を比較](report/2026-10-07_073209_comparing_layer_and_tensor_mtp_and_dflash2_on_2x_v100.md) | pakutoma | ASRock B550M Pro RS | Tesla V100-SXM2-16GB × 2 | Qwen3.8 27B UD-Q4_K_M |
| 2026-10-05 | [Tesla V100 16GB ×2・NVLink・各150W制限でQwen3.8 27Bのsplit-modeを比較](report/2026-10-05_203331_comparing_qwen3_8_27b_split_modes_on_2x_v100_nvlink_at_150w.md) | KotaroFurukawa | Supermicro X11SPi-TF | Tesla V100-SXM2-16GB × 2（NVLink・各150W） | Qwen3.8-27B Q4_K_M（64k、layer/tensor） |
| 2026-10-04 | [TB250-BTC PRO で新旧混成GPUの分割ベンチ (Vulkan + Kepler 復活CUDA)](report/2026-10-04_195500_multi_gpu_split_bench_on_tb250_btc_pro.md) | eightman999 | BIOSTAR TB250-BTC PRO | RX 6400 + Pro WX 2100 + GT 730 + GT 710（GT 430・HD 610 は計測不可） | Qwen3-1.7B Q4_K_M / TinyLlama-1.1B Q4_0 |
| 2026-10-03 | [Tesla V100-PCIE-32GB と PG500-216 で Qwen3.8 Flash Next を 192k / 256k で計測](report/2026-10-03_122722_profiling_qwen3.8_flash_next_at_192k_and_256k_on_tesla_v100_pcie_and_pg500_216.md) | warabii | MSI MPG X570 GAMING EDGE WIFI | Tesla V100-PCIE-32GB + Tesla PG500-216 | Qwen3.8 Flash Next IQ3E-Q8D-MTP |
| 2026-10-01 | [RTX 3090 4 枚で Qwen3.8 27B の split-mode を比較（Ubuntu・NCCL）](report/2026-10-01_203001_comparing_qwen3.8_27b_split_modes_on_4x_rtx3090_with_nccl_on_ubuntu.md) | 錦幸佳 | ASUS ROG CROSSHAIR VIII DARK HERO | RTX 3090 × 4 | Qwen3.8 27B UD-Q4_K_XL |
| 2026-09-30 | [Tesla T4 4 枚で Nemotron 3 Nano Omni 33B を 128k コンテキストまで計測](report/2026-09-30_111720_profiling_nemotron_3_nano_omni_33b_up_to_128k_on_4x_tesla_t4.md) | MG8853 | HPE ProLiant DL380 Gen10 | Tesla T4 × 4 | Nemotron 3 Nano Omni 33B UD-Q4_K_M（層分割のみ） |
| 2026-09-30 | [Tesla T4 4 枚で Nemotron 3.5 Lightning 30B A3B を 262k コンテキストまで計測](report/2026-09-30_110715_profiling_nemotron_3.5_lightning_30b_a3b_up_to_262k_on_4x_tesla_t4.md) | MG8853 | HPE ProLiant DL380 Gen10 | Tesla T4 × 4 | Nemotron 3.5 Lightning 30B A3B UD-Q4_K_M + MTP（層分割のみ） |
| 2026-09-30 | [Tesla T4 4 枚で Ornith 1.5 35B A3B の split-mode を比較](report/2026-09-30_105157_comparing_split_modes_of_ornith_1.5_35b_a3b_on_4x_tesla_t4.md) | MG8853 | HPE ProLiant DL380 Gen10 | Tesla T4 × 4 | Ornith 1.5 35B A3B Q4_K_M + MTP |
| 2026-09-30 | [Tesla T4 4 枚で Gemma 4 26B A4B QAT の split-mode を比較](report/2026-09-30_041750_comparing_split_modes_of_gemma_4_26b_a4b_qat_on_4x_tesla_t4.md) | MG8853 | HPE ProLiant DL380 Gen10 | Tesla T4 × 4 | Gemma 4 26B A4B QAT UD-Q4_K_XL + MTP |
| 2026-09-30 | [Tesla T4 4 枚で Gemma 4 31B QAT の split-mode を比較](report/2026-09-30_035231_comparing_split_modes_of_gemma_4_31b_qat_on_4x_tesla_t4.md) | MG8853 | HPE ProLiant DL380 Gen10 | Tesla T4 × 4 | Gemma 4 31B QAT UD-Q4_K_XL + MTP |
| 2026-09-29 | [TITAN V 2枚でSwift版Qwen3.8 27B IQ4_XSを160Kコンテキストまで測定](report/2026-09-29_155502_benchmarking_swift_qwen3_8_27b_iq4_xs_up_to_160k_context_on_2x_titan_v.md) | tomo_9180 | MSI MPG Z490M GAMING EDGE WIFI | TITAN V × 2 | Swift-Qwen3.8-27B IQ4_XS（128K比較、160K容量確認） |
| 2026-09-29 | [TITAN V 2枚でQwen3.8 27B IQ4_XSのsplit-modeを64Kまで比較](report/2026-09-29_141725_comparing_qwen3_8_27b_iq4_xs_split_modes_on_2x_titan_v_at_64k_context.md) | tomo_9180 | MSI MPG Z490M GAMING EDGE WIFI | TITAN V × 2 | Qwen3.8 27B UD-IQ4_XS（64K、layer/tensor） |
| 2026-09-28 | [RTX 5090 1 枚で Qwen3.8-Flash-Next NVFP4 を FreeToken で約 260k 入力まで計測](report/2026-09-28_172024_measuring_qwen3.8_flash_next_nvfp4_with_freetoken_on_rtx5090.md) | centra | ASRock Z890 Pro RS WiFi | RTX 5090 × 1 | Qwen3.8-Flash-Next Uncensored NVFP4（FreeToken、各条件 3 回） |
| 2026-09-28 | [Radeon AI PRO R9700でQwen3.8 27BのIQ4_XSとMXFP4を比較](report/2026-09-28_152428_comparing_iq4_xs_and_mxfp4_on_r9700.md) | jyohukuchan | ASRock WRX80 Creator | Radeon AI PRO R9700 × 1 | Qwen3.8 27B UD-IQ4_XS / Quark AWQ MXFP4（各3回） |
| 2026-09-28 | [RTX 5060 TiでGemma 4 26B A4B QAT-MTPを131Kコンテキストまで計測](report/2026-09-28_210656_profiling_gemma4_26b_a4b_qat_mtp_on_rtx5060ti.md) | RockinWool | ASRock B650 PG Lightning | RTX 5060 Ti + RTX 5070 | Gemma4 26B A4B QAT Q4_K_M + MTP（131K、単一GPU） |
| 2026-09-28 | [RX 7900 XT + RX 7800 XTでQwen3.8 27B IQ4 XSのsplit-modeを比較](report/2026-09-28_040646_qwen3_8_27b_iq4xs_128k_benchmark_on_rx7900xt_and_rx7800xt.md) | ogawara | ASUS ProArt X870E-CREATOR WIFI | RX 7900 XT + RX 7800 XT | Qwen3.8 27B UD-IQ4_XS（128K、各構成3回） |
| 2026-09-27 | [CMP 170HX 2 枚で Qwen3.8 Flash Next（W4A16・MoE）を vLLM TP=2 で 258k コンテキストまで計測](report/2026-09-27_153558_measuring_qwen3.8_flash_next_w4a16_on_2x_cmp_170hx_with_vllm_tp2.md) | moriyasujapan | GIGABYTE MZ32-AR0-00 | NVIDIA CMP 170HX × 2 | Qwen3.8 Flash Next heretic2 W4A16（vLLM TP=2） |
| 2026-09-27 | [RTX 3090 4 枚で Qwen3.8 27B の split-mode を比較（Windows・コア1395 MHz固定設定）](report/2026-09-27_130914_comparing_qwen3.8_27b_split_modes_on_4x_rtx3090_at_1395mhz_on_windows.md) | 錦幸佳 | ASUS ROG CROSSHAIR VIII DARK HERO | RTX 3090 × 4 | Qwen3.8 27B UD-Q4_K_XL |
| 2026-09-27 | [GTX 1660 SUPER 6GBで Qwen2.5-Coder 7B のGPU/CPUオフロードを計測](report/2026-09-27_124604_measuring_gpu_cpu_offload_of_qwen2_5_coder_7b_on_gtx1660super_6gb.md) | antarashi | ASRock B450 Pro4 | GTX 1660 SUPER × 1 | Qwen2.5-Coder 7B Q4_K_M |
| 2026-09-27 | [RTX 5090 1 枚で Qwen3.8 27B UD-Q5_K_XL を 262k コンテキストまで計測](report/2026-09-27_060846_profiling_qwen3.8_27b_ud_q5_k_xl_up_to_262k_context_on_rtx5090.md) | unco3 | ASRock Z790 Steel Legend WiFi | RTX 5090 × 1 | Qwen3.8 27B UD-Q5_K_XL |
| 2026-09-26 | [RTX 5090 で Qwen3.8 27B を 262k コンテキストで測定](report/2026-09-26_203225_measuring_qwen3_8_27b_at_262k_context_on_rtx_5090.md) | completenovice-eng | Micro-Star International Co., Ltd. PRO B650-S (MS-7E26) | RTX 5090 × 1 | Huihui-Qwen3.8-27B-abliterated-Q4_K |
| 2026-09-26 | [EVO-X2 128GBでQwen3.8-Flash-NextをHalogenで実行](report/2026-09-26_171511_running_qwen3.8_flash_next_with_halogen_on_evo_x2_128gb.md) | A-Uta | GMKtec NucBox EVO-X2 | Radeon 8060S × 1 | Qwen3.8 Flash Next W4B（Halogen） |
| 2026-09-26 | [Tesla T4 4 枚で Qwen3.8 27B の split-mode と量子化を比較](report/2026-09-26_084514_comparing_split_modes_and_quantizations_of_qwen3.8_27b_on_4x_tesla_t4.md) | MG8853 | HPE ProLiant DL380 Gen10 | Tesla T4 × 4 | Qwen3.8 27B UD-Q4_K_XL / UD-Q6_K / Q8_0 |
| 2026-09-26 | [RTX 5070 12GB 1枚で Qwen3.8 27B GSQ IQ2_S を計測（8K短縮プロファイル）](report/2026-09-26_094401_profiling_qwen3.8_27b_gsq_iq2_s_on_rtx5070_12gb.md) | fumimatsu | GIGABYTE X870M AORUS ELITE WIFI7 ICE | RTX 5070 × 1 | Qwen3.8 27B GSQ-RCO IQ2_S |
| 2026-09-26 | [EPYC 7452 × 2 と RTX 5070 Ti × 2 で Qwen3.8-Flash-Next Uncensored（自前 NVFP4）を sglang＋KTransformers で動かす](report/2026-09-26_204056_running_qwen3.8_flash_next_uncensored_nvfp4_on_2x_epyc_7452_and_2x_rtx_5070_ti_with_sglang_and_ktransformers.md) | amane.yukishima | HUANANZHI H12D-16D | RTX 5070 Ti × 2 | Qwen3.8-Flash-Next Uncensored NVFP4 エキスパート（sglang＋KTransformers、自作計測） |
| 2026-09-26 | [EPYC 7452 × 2 と RTX 5070 Ti × 2 で Qwen3.5-35B-A3B を BF16 のまま CPU/GPU 分担で動かす](report/2026-09-26_093349_running_qwen3.5_35b_a3b_in_bf16_on_2x_epyc_7452_and_2x_rtx_5070_ti_with_cpu_gpu_hybrid.md) | amane.yukishima | HUANANZHI H12D-16D | RTX 5070 Ti × 2 | Qwen3.5-35B-A3B BF16（sglang＋KTransformers、自作計測） |
| 2026-09-26 | [EPYC 7452 × 2 と RTX 5070 Ti × 2 で GLM-5.3-Flash Uncensored を動かし、GPU での prefill と GPU 常駐エキスパートを比較](report/2026-09-26_093348_running_glm_5.3_flash_uncensored_on_2x_epyc_7452_and_2x_rtx_5070_ti_comparing_gpu_prefill_and_hot_experts.md) | amane.yukishima | HUANANZHI H12D-16D | RTX 5070 Ti × 2 | GLM-5.3-Flash Uncensored FP8＋NVFP4 エキスパート（sglang＋KTransformers、自作計測） |
| 2026-09-26 | [EPYC 7452 × 2 と RTX 5070 Ti × 2 で DeepSeek V4.1-Flash（476 GB）をコンテキスト長 1M で動かす](report/2026-09-26_093347_running_deepseek_v4.1_flash_with_1m_context_on_2x_epyc_7452_and_2x_rtx_5070_ti_with_sglang_and_ktransformers.md) | amane.yukishima | HUANANZHI H12D-16D | RTX 5070 Ti × 2 | DeepSeek V4.1-Flash FP8＋FP4 エキスパート（sglang＋KTransformers、自作計測） |
| 2026-09-26 | [EPYC 7452 × 2 と RTX 5070 Ti × 2 で DeepSeek V4-Flash-Vision-Exp（abliterated、MXFP4）を sglang＋KTransformers で動かす](report/2026-09-26_093346_running_deepseek_v4_flash_vision_exp_abliterated_mxfp4_on_2x_epyc_7452_and_2x_rtx_5070_ti_with_sglang_and_ktransformers.md) | amane.yukishima | HUANANZHI H12D-16D | RTX 5070 Ti × 2 | DeepSeek V4-Flash-Vision-Exp abliterated MXFP4（sglang＋KTransformers、自作計測） |
| 2026-09-25 | [DGX互換機 Lenovo Thinkstation PGX 1台で Qwen3.8 Flash Next（MoE）を 262k コンテキストまで計測](report/2026-09-25_171942_qwen3_8_flash_next_single_gpu_on_nvidia_gb10.md) | 0rangaxx | Lenovo 30KLS01900 | NVIDIA GB10（統合メモリ）× 1 | Qwen3.8 Flash Next IQ3E-Q8D-MTP |
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
