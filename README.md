# bench-of-us

**English (primary)** · [简体中文](README.zh-CN.md) · [日本語](README.ja.md)

A community-maintained collection of **real-world local LLM hardware configurations and benchmark results**.

How fast can a model run on a particular GPU combination? Is layer splitting faster than tensor splitting on a multi-GPU machine? Bench of Us collects reproducible, contributor-submitted reports so others can explore these questions.

## Website

Explore the reports in the [Bench of Us benchmark database](https://jimoto-no-llm.github.io/bench-of-us/).

The website is generated from the Markdown reports in `report/` via the Astro project in `site/`. When a report is merged into `main`, GitHub Actions rebuilds the website automatically. No additional website submission is required.

## How to contribute

1. Fork and clone this repository.
2. Optionally benchmark your system using [llama-split-bench](https://github.com/kuraneko1/llama-split-bench).
3. Add one Markdown report to `report/`.
4. Add your report to the index below, then open a pull request.

**Hardware-only reports are welcome.** Running a benchmark is optional; explicitly mark the benchmark as not run.

For complete instructions and a reusable report template, see **[CONTRIBUTING.md](CONTRIBUTING.md)** ([简体中文](CONTRIBUTING.zh-CN.md)). Existing reports are largely written in Japanese; translations of index titles below do not modify the original submissions.

### Using an AI coding agent

Start Claude Code, Codex, OpenCode, or another coding agent in the repository root and ask it to help collect hardware details and prepare a benchmark report. [CLAUDE.md](CLAUDE.md) contains the current agent workflow (written in Japanese); review commands and any information that may be published before approving a PR.

### Writing a report manually

- File name: `report/yyyy-mm-dd_HHMMSS_<english_slug>.md` (lowercase ASCII slug with underscores).
- Required: author, machine or motherboard model, GPU model(s) and count, and benchmark results or an explicit “not run” statement.
- Put figures and JSON under `report/attachment/<report_basename>/`.
- Use YAML frontmatter for reliable metadata extraction, especially for reports written in English or Chinese.
- Add a row to the report indexes in `README.md`, `README.zh-CN.md` and `README.ja.md`.

## Report index

Newest reports first. Titles are translated for navigation; the linked Markdown reports remain in their original language.

<!-- When adding a report, insert a row immediately after the header separator. Keep all three README indexes synchronized. Do not put blank lines or HTML comments inside the Markdown table. -->

| Date | Report | Author | Computer / motherboard | GPU | Model / benchmark |
|------|--------|--------|------------------------|-----|-------------------|
| 2026-10-08 | [Profiling Qwen3.8 27B UD-Q4_K_M up to 262k context on 1× Tesla V100-PCIE-32GB](report/2026-10-08_105734_profiling_qwen3.8_27b_ud_q4_k_m_up_to_262k_on_tesla_v100_pcie_32gb.md) | sh1ma | Supermicro SYS-1019GP-TT | Tesla V100-PCIE-32GB × 1 | Qwen3.8 27B UD-Q4_K_M(262k, profile) |
| 2026-10-07 | [Comparing layer/tensor split, MTP, and DFlash2 for Qwen3.8 27B on 2× V100](report/2026-10-07_073209_comparing_layer_and_tensor_mtp_and_dflash2_on_2x_v100.md) | pakutoma | ASRock B550M Pro RS | Tesla V100-SXM2-16GB × 2 | Qwen3.8 27B UD-Q4_K_M |
| 2026-10-05 | [Comparing Qwen3.8 27B split modes on 2× Tesla V100 16GB with NVLink (150 W per GPU)](report/2026-10-05_203331_comparing_qwen3_8_27b_split_modes_on_2x_v100_nvlink_at_150w.md) | KotaroFurukawa | Supermicro X11SPi-TF | Tesla V100-SXM2-16GB × 2(NVLink, 150 W per GPU) | Qwen3.8-27B Q4_K_M(64k, layer/tensor) |
| 2026-10-04 | [Benchmarking mixed-generation GPU splits on TB250-BTC PRO (Vulkan + restored Kepler CUDA)](report/2026-10-04_195500_multi_gpu_split_bench_on_tb250_btc_pro.md) | eightman999 | BIOSTAR TB250-BTC PRO | RX 6400 + Pro WX 2100 + GT 730 + GT 710(GT 430 and HD 610 could not be benchmarked) | Qwen3-1.7B Q4_K_M / TinyLlama-1.1B Q4_0 |
| 2026-10-03 | [Profiling Qwen3.8 Flash Next at 192k/256k on Tesla V100-PCIE-32GB + PG500-216](report/2026-10-03_122722_profiling_qwen3.8_flash_next_at_192k_and_256k_on_tesla_v100_pcie_and_pg500_216.md) | warabii | MSI MPG X570 GAMING EDGE WIFI | Tesla V100-PCIE-32GB + Tesla PG500-216 | Qwen3.8 Flash Next IQ3E-Q8D-MTP |
| 2026-10-01 | [Comparing Qwen3.8 27B split modes on 4× RTX 3090 (Ubuntu + NCCL)](report/2026-10-01_203001_comparing_qwen3.8_27b_split_modes_on_4x_rtx3090_with_nccl_on_ubuntu.md) | 錦幸佳 | ASUS ROG CROSSHAIR VIII DARK HERO | RTX 3090 × 4 | Qwen3.8 27B UD-Q4_K_XL |
| 2026-09-30 | [Profiling Nemotron 3 Nano Omni 33B up to 128k context on 4× Tesla T4](report/2026-09-30_111720_profiling_nemotron_3_nano_omni_33b_up_to_128k_on_4x_tesla_t4.md) | MG8853 | HPE ProLiant DL380 Gen10 | Tesla T4 × 4 | Nemotron 3 Nano Omni 33B UD-Q4_K_M(layer split only) |
| 2026-09-30 | [Profiling Nemotron 3.5 Lightning 30B A3B up to 262k context on 4× Tesla T4](report/2026-09-30_110715_profiling_nemotron_3.5_lightning_30b_a3b_up_to_262k_on_4x_tesla_t4.md) | MG8853 | HPE ProLiant DL380 Gen10 | Tesla T4 × 4 | Nemotron 3.5 Lightning 30B A3B UD-Q4_K_M + MTP(layer split only) |
| 2026-09-30 | [Comparing Ornith 1.5 35B A3B split modes on 4× Tesla T4](report/2026-09-30_105157_comparing_split_modes_of_ornith_1.5_35b_a3b_on_4x_tesla_t4.md) | MG8853 | HPE ProLiant DL380 Gen10 | Tesla T4 × 4 | Ornith 1.5 35B A3B Q4_K_M + MTP |
| 2026-09-30 | [Comparing Gemma 4 26B A4B QAT split modes on 4× Tesla T4](report/2026-09-30_041750_comparing_split_modes_of_gemma_4_26b_a4b_qat_on_4x_tesla_t4.md) | MG8853 | HPE ProLiant DL380 Gen10 | Tesla T4 × 4 | Gemma 4 26B A4B QAT UD-Q4_K_XL + MTP |
| 2026-09-30 | [Comparing Gemma 4 31B QAT split modes on 4× Tesla T4](report/2026-09-30_035231_comparing_split_modes_of_gemma_4_31b_qat_on_4x_tesla_t4.md) | MG8853 | HPE ProLiant DL380 Gen10 | Tesla T4 × 4 | Gemma 4 31B QAT UD-Q4_K_XL + MTP |
| 2026-09-29 | [Benchmarking Swift Qwen3.8 27B IQ4_XS up to 160K context on 2× TITAN V](report/2026-09-29_155502_benchmarking_swift_qwen3_8_27b_iq4_xs_up_to_160k_context_on_2x_titan_v.md) | tomo_9180 | MSI MPG Z490M GAMING EDGE WIFI | TITAN V × 2 | Swift-Qwen3.8-27B IQ4_XS(128K comparison; 160K capacity check) |
| 2026-09-29 | [Comparing Qwen3.8 27B IQ4_XS split modes up to 64K context on 2× TITAN V](report/2026-09-29_141725_comparing_qwen3_8_27b_iq4_xs_split_modes_on_2x_titan_v_at_64k_context.md) | tomo_9180 | MSI MPG Z490M GAMING EDGE WIFI | TITAN V × 2 | Qwen3.8 27B UD-IQ4_XS(64K, layer/tensor) |
| 2026-09-28 | [Profiling Qwen3.8 Flash Next NVFP4 with FreeToken up to ~260k input on 1× RTX 5090](report/2026-09-28_172024_measuring_qwen3.8_flash_next_nvfp4_with_freetoken_on_rtx5090.md) | centra | ASRock Z890 Pro RS WiFi | RTX 5090 × 1 | Qwen3.8-Flash-Next Uncensored NVFP4(FreeToken, 3 runs per configuration) |
| 2026-09-28 | [Comparing Qwen3.8 27B IQ4_XS and MXFP4 on Radeon AI PRO R9700](report/2026-09-28_152428_comparing_iq4_xs_and_mxfp4_on_r9700.md) | jyohukuchan | ASRock WRX80 Creator | Radeon AI PRO R9700 × 1 | Qwen3.8 27B UD-IQ4_XS / Quark AWQ MXFP4(3 runs per configuration) |
| 2026-09-28 | [Profiling Gemma 4 26B A4B QAT-MTP up to 131K context on RTX 5060 Ti](report/2026-09-28_210656_profiling_gemma4_26b_a4b_qat_mtp_on_rtx5060ti.md) | RockinWool | ASRock B650 PG Lightning | RTX 5060 Ti + RTX 5070 | Gemma4 26B A4B QAT Q4_K_M + MTP(131K, single GPU) |
| 2026-09-28 | [Comparing Qwen3.8 27B IQ4_XS split modes on RX 7900 XT + RX 7800 XT](report/2026-09-28_040646_qwen3_8_27b_iq4xs_128k_benchmark_on_rx7900xt_and_rx7800xt.md) | ogawara | ASUS ProArt X870E-CREATOR WIFI | RX 7900 XT + RX 7800 XT | Qwen3.8 27B UD-IQ4_XS(128K, 3 runs per configuration) |
| 2026-09-27 | [Profiling Qwen3.8 Flash Next (W4A16/MoE) up to 258k context on 2× CMP 170HX (vLLM TP=2)](report/2026-09-27_153558_measuring_qwen3.8_flash_next_w4a16_on_2x_cmp_170hx_with_vllm_tp2.md) | moriyasujapan | GIGABYTE MZ32-AR0-00 | NVIDIA CMP 170HX × 2 | Qwen3.8 Flash Next heretic2 W4A16(vLLM TP=2) |
| 2026-09-27 | [Comparing Qwen3.8 27B split modes on 4× RTX 3090 (Windows, GPU clock fixed at 1395 MHz)](report/2026-09-27_130914_comparing_qwen3.8_27b_split_modes_on_4x_rtx3090_at_1395mhz_on_windows.md) | 錦幸佳 | ASUS ROG CROSSHAIR VIII DARK HERO | RTX 3090 × 4 | Qwen3.8 27B UD-Q4_K_XL |
| 2026-09-27 | [Measuring GPU/CPU offload of Qwen2.5-Coder 7B on GTX 1660 SUPER 6GB](report/2026-09-27_124604_measuring_gpu_cpu_offload_of_qwen2_5_coder_7b_on_gtx1660super_6gb.md) | antarashi | ASRock B450 Pro4 | GTX 1660 SUPER × 1 | Qwen2.5-Coder 7B Q4_K_M |
| 2026-09-27 | [Profiling Qwen3.8 27B UD-Q5_K_XL up to 262k context on 1× RTX 5090](report/2026-09-27_060846_profiling_qwen3.8_27b_ud_q5_k_xl_up_to_262k_context_on_rtx5090.md) | unco3 | ASRock Z790 Steel Legend WiFi | RTX 5090 × 1 | Qwen3.8 27B UD-Q5_K_XL |
| 2026-09-26 | [Measuring Qwen3.8 27B at 262k context on RTX 5090](report/2026-09-26_203225_measuring_qwen3_8_27b_at_262k_context_on_rtx_5090.md) | completenovice-eng | Micro-Star International Co., Ltd. PRO B650-S (MS-7E26) | RTX 5090 × 1 | Huihui-Qwen3.8-27B-abliterated-Q4_K |
| 2026-09-26 | [Running Qwen3.8 Flash Next with Halogen on EVO-X2 128GB](report/2026-09-26_171511_running_qwen3.8_flash_next_with_halogen_on_evo_x2_128gb.md) | A-Uta | GMKtec NucBox EVO-X2 | Radeon 8060S × 1 | Qwen3.8 Flash Next W4B(Halogen) |
| 2026-09-26 | [Comparing Qwen3.8 27B split modes and quantizations on 4× Tesla T4](report/2026-09-26_084514_comparing_split_modes_and_quantizations_of_qwen3.8_27b_on_4x_tesla_t4.md) | MG8853 | HPE ProLiant DL380 Gen10 | Tesla T4 × 4 | Qwen3.8 27B UD-Q4_K_XL / UD-Q6_K / Q8_0 |
| 2026-09-26 | [Profiling Qwen3.8 27B GSQ IQ2_S on 1× RTX 5070 12GB (short 8K profile)](report/2026-09-26_094401_profiling_qwen3.8_27b_gsq_iq2_s_on_rtx5070_12gb.md) | fumimatsu | GIGABYTE X870M AORUS ELITE WIFI7 ICE | RTX 5070 × 1 | Qwen3.8 27B GSQ-RCO IQ2_S |
| 2026-09-26 | [Running Qwen3.8 Flash Next Uncensored (custom NVFP4) on 2× EPYC 7452 + 2× RTX 5070 Ti with SGLang and KTransformers](report/2026-09-26_204056_running_qwen3.8_flash_next_uncensored_nvfp4_on_2x_epyc_7452_and_2x_rtx_5070_ti_with_sglang_and_ktransformers.md) | amane.yukishima | HUANANZHI H12D-16D | RTX 5070 Ti × 2 | Qwen3.8-Flash-Next Uncensored NVFP4 experts(SGLang + KTransformers, custom measurements) |
| 2026-09-26 | [Running Qwen3.5-35B-A3B in BF16 with CPU/GPU hybrid inference on 2× EPYC 7452 + 2× RTX 5070 Ti](report/2026-09-26_093349_running_qwen3.5_35b_a3b_in_bf16_on_2x_epyc_7452_and_2x_rtx_5070_ti_with_cpu_gpu_hybrid.md) | amane.yukishima | HUANANZHI H12D-16D | RTX 5070 Ti × 2 | Qwen3.5-35B-A3B BF16(SGLang + KTransformers, custom measurements) |
| 2026-09-26 | [Running GLM-5.3-Flash Uncensored and comparing GPU prefill vs. resident experts on 2× EPYC 7452 + 2× RTX 5070 Ti](report/2026-09-26_093348_running_glm_5.3_flash_uncensored_on_2x_epyc_7452_and_2x_rtx_5070_ti_comparing_gpu_prefill_and_hot_experts.md) | amane.yukishima | HUANANZHI H12D-16D | RTX 5070 Ti × 2 | GLM-5.3-Flash Uncensored FP8 + NVFP4 experts(SGLang + KTransformers, custom measurements) |
| 2026-09-26 | [Running DeepSeek V4.1-Flash (476 GB) at 1M context on 2× EPYC 7452 + 2× RTX 5070 Ti](report/2026-09-26_093347_running_deepseek_v4.1_flash_with_1m_context_on_2x_epyc_7452_and_2x_rtx_5070_ti_with_sglang_and_ktransformers.md) | amane.yukishima | HUANANZHI H12D-16D | RTX 5070 Ti × 2 | DeepSeek V4.1-Flash FP8 + FP4 experts(SGLang + KTransformers, custom measurements) |
| 2026-09-26 | [Running DeepSeek V4-Flash-Vision-Exp (abliterated, MXFP4) with SGLang and KTransformers on 2× EPYC 7452 + 2× RTX 5070 Ti](report/2026-09-26_093346_running_deepseek_v4_flash_vision_exp_abliterated_mxfp4_on_2x_epyc_7452_and_2x_rtx_5070_ti_with_sglang_and_ktransformers.md) | amane.yukishima | HUANANZHI H12D-16D | RTX 5070 Ti × 2 | DeepSeek V4-Flash-Vision-Exp abliterated MXFP4(SGLang + KTransformers, custom measurements) |
| 2026-09-25 | [Profiling Qwen3.8 Flash Next (MoE) up to 262k context on Lenovo ThinkStation PGX (DGX-compatible)](report/2026-09-25_171942_qwen3_8_flash_next_single_gpu_on_nvidia_gb10.md) | 0rangaxx | Lenovo 30KLS01900 | NVIDIA GB10(unified memory)× 1 | Qwen3.8 Flash Next IQ3E-Q8D-MTP |
| 2026-09-25 | [Comparing Qwen3.8 27B split modes on 4× Tesla P40 with a single-GPU baseline](report/2026-09-25_222946_comparing_split_modes_of_qwen3.8_27b_on_4x_tesla_p40_with_single_gpu_baseline.md) | 0kqnet | Supermicro X10DRG-Q | Tesla P40 × 4 | Qwen3.8 27B UD-Q4_K_XL |
| 2026-09-24 | [Comparing layer split and single-GPU Qwen3.8 Flash Next (MoE) on 2× Tesla V100-SXM2-32GB](report/2026-09-24_144622_comparing_layer_split_and_single_gpu_of_qwen3.8_flash_next_on_2x_tesla_v100_sxm2_32gb.md) | pentacoxian | Inspur NF5468M5 | Tesla V100-SXM2-32GB × 2 | Qwen3.8 Flash Next IQ3E-Q8D-MTP |
| 2026-09-23 | [Comparing Qwen3.8 27B split modes on 2× Tesla V100](report/2026-09-23_060231_comparing_split_modes_of_qwen3.8_27b_on_2x_tesla_v100.md) | miminashi | ASRock X99 Taichi | Tesla V100-SXM2-16GB × 2 | Huihui Qwen3.8 27B abliterated UD-Q4_K_XL |
| 2026-09-22 | [Comparing Qwen3.8 27B split modes on 2× Tesla V100 with a single-GPU baseline](report/2026-09-22_210206_comparing_split_modes_of_qwen3.8_27b_on_2x_tesla_v100_with_single_gpu_baseline.md) | kuraneko1 | ASUS Z170-A | Tesla V100-PCIE-32GB + Tesla PG500-216 | Qwen3.8 27B UD-Q4_K_M |
| 2026-09-21 | [Comparing NCCL vs. non-NCCL tensor split of Qwen3.8 27B on RTX 3060 + Tesla V100](report/2026-09-21_183303_comparing_nccl_vs_no_nccl_tensor_split_on_rtx3060_and_tesla_v100.md) | eightman999 | Thirdwave XA7C-R47T / ASRock B760 TW/D4 | RTX 3060 12GB + Tesla V100-PCIE-32GB | Qwen3.8 27B Q4_K_M NCCL |
| 2026-09-21 | [Comparing Qwen3.8 27B split modes on RTX 3060 + Tesla V100](report/2026-09-21_170911_comparing_split_modes_of_qwen3.8_27b_on_rtx3060_and_tesla_v100.md) | eightman999 | Thirdwave XA7C-R47T / ASRock B760 TW/D4 | RTX 3060 12GB + Tesla V100-PCIE-32GB | Qwen3.8 27B Q4_K_M |
| 2026-09-20 | [Comparing Qwen3.8 27B split modes on 7× Tesla P100](report/2026-09-20_072013_comparing_split_modes_of_qwen3.8_27b_on_7x_tesla_p100.md) | miminashi | Supermicro SYS-4028GR-TRT2 | Tesla P100 × 7 | Qwen3.8 27B UD-Q4_K_XL |
| 2026-09-20 | [Comparing Qwen3.8 27B split modes on 4× Tesla P100](report/2026-09-20_033840_comparing_split_modes_of_qwen3.8_27b_on_4x_tesla_p100.md) | miminashi | NEC Express5800/T120h | Tesla P100 × 4 | Qwen3.8 27B UD-Q4_K_XL |

The report files are in [report/](report/).

## Privacy and publication

- Never include serial numbers, UUIDs, MAC addresses, hostnames, IP addresses, or personal usernames embedded in absolute file paths.
- Do not commit model files (`.gguf`), benchmark server logs, raw model responses, or sensitive local data.
- Review `run-info.json` and argument files for private paths or hostnames before uploading.
- Do not edit other contributors' existing reports as part of a new report submission.

## License

See [LICENSE](LICENSE) for this repository's license.
