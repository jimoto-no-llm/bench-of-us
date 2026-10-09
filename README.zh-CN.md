# bench-of-us

[English (primary)](README.md) · **简体中文** · [日本語](README.ja.md)

这是一个由社区共同维护的资料库，用于分享**真实硬件上的本地大语言模型（LLM）配置与基准测试结果**。

特定 GPU 组合运行某个模型究竟有多快？多 GPU 环境下，按层切分与张量切分哪种方式更快？Bench of Us 通过贡献者提交的实测报告，为这些问题积累可供查阅的资料。

## 网站

可通过 [Bench of Us 基准测试数据库](https://jimoto-no-llm.github.io/bench-of-us/) 浏览报告。

网站由 `site/` 中的 Astro 项目根据 `report/` 内的 Markdown 自动生成。报告合并到 `main` 后，GitHub Actions 会自动重新构建网站，无需额外提交网页内容。

## 如何参与

1. Fork 并克隆本仓库。
2. 根据需要，使用 [llama-split-bench](https://github.com/kuraneko1/llama-split-bench) 在本机运行测试（可选）。
3. 在 `report/` 中新增一份 Markdown 报告。
4. 在下方报告索引中加入一行，然后提交 Pull Request。

**欢迎仅分享硬件配置的报告。** 基准测试不是强制要求；未运行时请明确注明。

完整说明及报告模板见 **[CONTRIBUTING.zh-CN.md](CONTRIBUTING.zh-CN.md)**（[English](CONTRIBUTING.md)）。现有报告大多使用日语；下面仅翻译索引标题，不修改投稿者的原始报告。

### 使用 AI 编程代理

在仓库根目录启动 Claude Code、Codex、OpenCode 等工具，请其协助采集硬件信息、执行测试并编写报告。[CLAUDE.md](CLAUDE.md) 提供现行的代理操作规范（内容为日语）。发布前请检查命令、个人信息与 Pull Request 内容。

### 手动编写报告

- 文件命名：`report/yyyy-mm-dd_HHMMSS_<english_slug>.md`，标题部分使用小写 ASCII 和下划线。
- 必填内容：作者、整机或主板型号、GPU 型号与数量，以及测试结果或明确的“未运行”说明。
- 图片与 JSON 放入 `report/attachment/<report_basename>/`。
- 建议使用 YAML frontmatter，尤其是使用中文或英文撰写报告时，便于网站正确提取元数据。
- 向 `README.md`、`README.zh-CN.md` 与 `README.ja.md` 的报告索引同时新增一行。

## 报告索引

大致按提交日期从新到旧排列。这里翻译的是导航标题；链接仍指向投稿者原语言的 Markdown 报告。

<!-- 新增报告时，将条目插入表头分隔行之后，并同步维护三个 README。不要在 Markdown 表格内部插入空行或 HTML 注释。 -->

| 日期 | 报告 | 作者 | 计算机 / 主板 | GPU | 模型 / 基准测试 |
|------|------|------|---------------|-----|-----------------|
| 2026-10-08 | [在单张 Tesla V100-PCIE-32GB 上测试 Qwen3.8 27B UD-Q4_K_M，最大 262k 上下文](report/2026-10-08_105734_profiling_qwen3.8_27b_ud_q4_k_m_up_to_262k_on_tesla_v100_pcie_32gb.md) | sh1ma | Supermicro SYS-1019GP-TT | Tesla V100-PCIE-32GB × 1 | Qwen3.8 27B UD-Q4_K_M(262k、性能剖析) |
| 2026-10-07 | [在两张 V100 上比较 Qwen3.8 27B 的层切分、张量切分、MTP 与 DFlash2](report/2026-10-07_073209_comparing_layer_and_tensor_mtp_and_dflash2_on_2x_v100.md) | pakutoma | ASRock B550M Pro RS | Tesla V100-SXM2-16GB × 2 | Qwen3.8 27B UD-Q4_K_M |
| 2026-10-05 | [在两张通过 NVLink 互连且每张限功耗 150W 的 Tesla V100 16GB 上比较 Qwen3.8 27B 切分模式](report/2026-10-05_203331_comparing_qwen3_8_27b_split_modes_on_2x_v100_nvlink_at_150w.md) | KotaroFurukawa | Supermicro X11SPi-TF | Tesla V100-SXM2-16GB × 2(NVLink、每张 150 W) | Qwen3.8-27B Q4_K_M(64k、层切分/张量切分) |
| 2026-10-04 | [在 TB250-BTC PRO 上测试新旧混合 GPU 的切分性能（Vulkan + 恢复支持的 Kepler CUDA）](report/2026-10-04_195500_multi_gpu_split_bench_on_tb250_btc_pro.md) | eightman999 | BIOSTAR TB250-BTC PRO | RX 6400 + Pro WX 2100 + GT 730 + GT 710(GT 430 和 HD 610 未能完成测试) | Qwen3-1.7B Q4_K_M / TinyLlama-1.1B Q4_0 |
| 2026-10-03 | [在 Tesla V100-PCIE-32GB + PG500-216 上测试 Qwen3.8 Flash Next 的 192k/256k 上下文性能](report/2026-10-03_122722_profiling_qwen3.8_flash_next_at_192k_and_256k_on_tesla_v100_pcie_and_pg500_216.md) | warabii | MSI MPG X570 GAMING EDGE WIFI | Tesla V100-PCIE-32GB + Tesla PG500-216 | Qwen3.8 Flash Next IQ3E-Q8D-MTP |
| 2026-10-01 | [在四张 RTX 3090 上比较 Qwen3.8 27B 的切分模式（Ubuntu + NCCL）](report/2026-10-01_203001_comparing_qwen3.8_27b_split_modes_on_4x_rtx3090_with_nccl_on_ubuntu.md) | 錦幸佳 | ASUS ROG CROSSHAIR VIII DARK HERO | RTX 3090 × 4 | Qwen3.8 27B UD-Q4_K_XL |
| 2026-09-30 | [在四张 Tesla T4 上测试 Nemotron 3 Nano Omni 33B，最大 128k 上下文](report/2026-09-30_111720_profiling_nemotron_3_nano_omni_33b_up_to_128k_on_4x_tesla_t4.md) | MG8853 | HPE ProLiant DL380 Gen10 | Tesla T4 × 4 | Nemotron 3 Nano Omni 33B UD-Q4_K_M(仅层切分) |
| 2026-09-30 | [在四张 Tesla T4 上测试 Nemotron 3.5 Lightning 30B A3B，最大 262k 上下文](report/2026-09-30_110715_profiling_nemotron_3.5_lightning_30b_a3b_up_to_262k_on_4x_tesla_t4.md) | MG8853 | HPE ProLiant DL380 Gen10 | Tesla T4 × 4 | Nemotron 3.5 Lightning 30B A3B UD-Q4_K_M + MTP(仅层切分) |
| 2026-09-30 | [在四张 Tesla T4 上比较 Ornith 1.5 35B A3B 的切分模式](report/2026-09-30_105157_comparing_split_modes_of_ornith_1.5_35b_a3b_on_4x_tesla_t4.md) | MG8853 | HPE ProLiant DL380 Gen10 | Tesla T4 × 4 | Ornith 1.5 35B A3B Q4_K_M + MTP |
| 2026-09-30 | [在四张 Tesla T4 上比较 Gemma 4 26B A4B QAT 的切分模式](report/2026-09-30_041750_comparing_split_modes_of_gemma_4_26b_a4b_qat_on_4x_tesla_t4.md) | MG8853 | HPE ProLiant DL380 Gen10 | Tesla T4 × 4 | Gemma 4 26B A4B QAT UD-Q4_K_XL + MTP |
| 2026-09-30 | [在四张 Tesla T4 上比较 Gemma 4 31B QAT 的切分模式](report/2026-09-30_035231_comparing_split_modes_of_gemma_4_31b_qat_on_4x_tesla_t4.md) | MG8853 | HPE ProLiant DL380 Gen10 | Tesla T4 × 4 | Gemma 4 31B QAT UD-Q4_K_XL + MTP |
| 2026-09-29 | [在两张 TITAN V 上测试 Swift 版 Qwen3.8 27B IQ4_XS，最大 160K 上下文](report/2026-09-29_155502_benchmarking_swift_qwen3_8_27b_iq4_xs_up_to_160k_context_on_2x_titan_v.md) | tomo_9180 | MSI MPG Z490M GAMING EDGE WIFI | TITAN V × 2 | Swift-Qwen3.8-27B IQ4_XS(128K 性能比较；160K 容量验证) |
| 2026-09-29 | [在两张 TITAN V 上比较 Qwen3.8 27B IQ4_XS 的切分模式，最大 64K 上下文](report/2026-09-29_141725_comparing_qwen3_8_27b_iq4_xs_split_modes_on_2x_titan_v_at_64k_context.md) | tomo_9180 | MSI MPG Z490M GAMING EDGE WIFI | TITAN V × 2 | Qwen3.8 27B UD-IQ4_XS(64K、层切分/张量切分) |
| 2026-09-28 | [在单张 RTX 5090 上使用 FreeToken 测试 Qwen3.8 Flash Next NVFP4，输入约 260k](report/2026-09-28_172024_measuring_qwen3.8_flash_next_nvfp4_with_freetoken_on_rtx5090.md) | centra | ASRock Z890 Pro RS WiFi | RTX 5090 × 1 | Qwen3.8-Flash-Next Uncensored NVFP4(FreeToken、每种配置运行 3 次) |
| 2026-09-28 | [在 Radeon AI PRO R9700 上比较 Qwen3.8 27B 的 IQ4_XS 与 MXFP4](report/2026-09-28_152428_comparing_iq4_xs_and_mxfp4_on_r9700.md) | jyohukuchan | ASRock WRX80 Creator | Radeon AI PRO R9700 × 1 | Qwen3.8 27B UD-IQ4_XS / Quark AWQ MXFP4(每种配置运行 3 次) |
| 2026-09-28 | [在 RTX 5060 Ti 上测试 Gemma 4 26B A4B QAT-MTP，最大 131K 上下文](report/2026-09-28_210656_profiling_gemma4_26b_a4b_qat_mtp_on_rtx5060ti.md) | RockinWool | ASRock B650 PG Lightning | RTX 5060 Ti + RTX 5070 | Gemma4 26B A4B QAT Q4_K_M + MTP(131K、单 GPU) |
| 2026-09-28 | [在 RX 7900 XT + RX 7800 XT 上比较 Qwen3.8 27B IQ4_XS 的切分模式](report/2026-09-28_040646_qwen3_8_27b_iq4xs_128k_benchmark_on_rx7900xt_and_rx7800xt.md) | ogawara | ASUS ProArt X870E-CREATOR WIFI | RX 7900 XT + RX 7800 XT | Qwen3.8 27B UD-IQ4_XS(128K、每种配置运行 3 次) |
| 2026-09-27 | [在两张 CMP 170HX 上使用 vLLM TP=2 测试 Qwen3.8 Flash Next（W4A16/MoE），最大 258k 上下文](report/2026-09-27_153558_measuring_qwen3.8_flash_next_w4a16_on_2x_cmp_170hx_with_vllm_tp2.md) | moriyasujapan | GIGABYTE MZ32-AR0-00 | NVIDIA CMP 170HX × 2 | Qwen3.8 Flash Next heretic2 W4A16(vLLM TP=2) |
| 2026-09-27 | [在四张 RTX 3090 上比较 Qwen3.8 27B 的切分模式（Windows、GPU 核心频率固定 1395 MHz）](report/2026-09-27_130914_comparing_qwen3.8_27b_split_modes_on_4x_rtx3090_at_1395mhz_on_windows.md) | 錦幸佳 | ASUS ROG CROSSHAIR VIII DARK HERO | RTX 3090 × 4 | Qwen3.8 27B UD-Q4_K_XL |
| 2026-09-27 | [在 GTX 1660 SUPER 6GB 上测量 Qwen2.5-Coder 7B 的 GPU/CPU 卸载性能](report/2026-09-27_124604_measuring_gpu_cpu_offload_of_qwen2_5_coder_7b_on_gtx1660super_6gb.md) | antarashi | ASRock B450 Pro4 | GTX 1660 SUPER × 1 | Qwen2.5-Coder 7B Q4_K_M |
| 2026-09-27 | [在单张 RTX 5090 上测试 Qwen3.8 27B UD-Q5_K_XL，最大 262k 上下文](report/2026-09-27_060846_profiling_qwen3.8_27b_ud_q5_k_xl_up_to_262k_context_on_rtx5090.md) | unco3 | ASRock Z790 Steel Legend WiFi | RTX 5090 × 1 | Qwen3.8 27B UD-Q5_K_XL |
| 2026-09-26 | [在 RTX 5090 上测量 Qwen3.8 27B 的 262k 上下文性能](report/2026-09-26_203225_measuring_qwen3_8_27b_at_262k_context_on_rtx_5090.md) | completenovice-eng | Micro-Star International Co., Ltd. PRO B650-S (MS-7E26) | RTX 5090 × 1 | Huihui-Qwen3.8-27B-abliterated-Q4_K |
| 2026-09-26 | [在 EVO-X2 128GB 上使用 Halogen 运行 Qwen3.8 Flash Next](report/2026-09-26_171511_running_qwen3.8_flash_next_with_halogen_on_evo_x2_128gb.md) | A-Uta | GMKtec NucBox EVO-X2 | Radeon 8060S × 1 | Qwen3.8 Flash Next W4B(Halogen) |
| 2026-09-26 | [在四张 Tesla T4 上比较 Qwen3.8 27B 的切分模式与量化格式](report/2026-09-26_084514_comparing_split_modes_and_quantizations_of_qwen3.8_27b_on_4x_tesla_t4.md) | MG8853 | HPE ProLiant DL380 Gen10 | Tesla T4 × 4 | Qwen3.8 27B UD-Q4_K_XL / UD-Q6_K / Q8_0 |
| 2026-09-26 | [在单张 RTX 5070 12GB 上测试 Qwen3.8 27B GSQ IQ2_S（精简 8K 配置）](report/2026-09-26_094401_profiling_qwen3.8_27b_gsq_iq2_s_on_rtx5070_12gb.md) | fumimatsu | GIGABYTE X870M AORUS ELITE WIFI7 ICE | RTX 5070 × 1 | Qwen3.8 27B GSQ-RCO IQ2_S |
| 2026-09-26 | [在双路 EPYC 7452 + 两张 RTX 5070 Ti 上通过 SGLang 和 KTransformers 运行 Qwen3.8 Flash Next Uncensored（自制 NVFP4）](report/2026-09-26_204056_running_qwen3.8_flash_next_uncensored_nvfp4_on_2x_epyc_7452_and_2x_rtx_5070_ti_with_sglang_and_ktransformers.md) | amane.yukishima | HUANANZHI H12D-16D | RTX 5070 Ti × 2 | Qwen3.8-Flash-Next Uncensored NVFP4 专家模块(SGLang + KTransformers、自行测量) |
| 2026-09-26 | [在双路 EPYC 7452 + 两张 RTX 5070 Ti 上以 BF16 运行 Qwen3.5-35B-A3B（CPU/GPU 混合推理）](report/2026-09-26_093349_running_qwen3.5_35b_a3b_in_bf16_on_2x_epyc_7452_and_2x_rtx_5070_ti_with_cpu_gpu_hybrid.md) | amane.yukishima | HUANANZHI H12D-16D | RTX 5070 Ti × 2 | Qwen3.5-35B-A3B BF16(SGLang + KTransformers、自行测量) |
| 2026-09-26 | [在双路 EPYC 7452 + 两张 RTX 5070 Ti 上运行 GLM-5.3-Flash Uncensored，比较 GPU 预填充与常驻专家模块](report/2026-09-26_093348_running_glm_5.3_flash_uncensored_on_2x_epyc_7452_and_2x_rtx_5070_ti_comparing_gpu_prefill_and_hot_experts.md) | amane.yukishima | HUANANZHI H12D-16D | RTX 5070 Ti × 2 | GLM-5.3-Flash Uncensored FP8 + NVFP4 专家模块(SGLang + KTransformers、自行测量) |
| 2026-09-26 | [在双路 EPYC 7452 + 两张 RTX 5070 Ti 上以 1M 上下文运行 DeepSeek V4.1-Flash（476 GB）](report/2026-09-26_093347_running_deepseek_v4.1_flash_with_1m_context_on_2x_epyc_7452_and_2x_rtx_5070_ti_with_sglang_and_ktransformers.md) | amane.yukishima | HUANANZHI H12D-16D | RTX 5070 Ti × 2 | DeepSeek V4.1-Flash FP8 + FP4 专家模块(SGLang + KTransformers、自行测量) |
| 2026-09-26 | [在双路 EPYC 7452 + 两张 RTX 5070 Ti 上通过 SGLang 和 KTransformers 运行 DeepSeek V4-Flash-Vision-Exp（abliterated、MXFP4）](report/2026-09-26_093346_running_deepseek_v4_flash_vision_exp_abliterated_mxfp4_on_2x_epyc_7452_and_2x_rtx_5070_ti_with_sglang_and_ktransformers.md) | amane.yukishima | HUANANZHI H12D-16D | RTX 5070 Ti × 2 | DeepSeek V4-Flash-Vision-Exp abliterated MXFP4(SGLang + KTransformers、自行测量) |
| 2026-09-25 | [在 Lenovo ThinkStation PGX（兼容 DGX）上测试 Qwen3.8 Flash Next（MoE），最大 262k 上下文](report/2026-09-25_171942_qwen3_8_flash_next_single_gpu_on_nvidia_gb10.md) | 0rangaxx | Lenovo 30KLS01900 | NVIDIA GB10(统一内存)× 1 | Qwen3.8 Flash Next IQ3E-Q8D-MTP |
| 2026-09-25 | [在四张 Tesla P40 上比较 Qwen3.8 27B 切分模式，并提供单 GPU 基线](report/2026-09-25_222946_comparing_split_modes_of_qwen3.8_27b_on_4x_tesla_p40_with_single_gpu_baseline.md) | 0kqnet | Supermicro X10DRG-Q | Tesla P40 × 4 | Qwen3.8 27B UD-Q4_K_XL |
| 2026-09-24 | [在两张 Tesla V100-SXM2-32GB 上比较 Qwen3.8 Flash Next（MoE）的层切分与单 GPU](report/2026-09-24_144622_comparing_layer_split_and_single_gpu_of_qwen3.8_flash_next_on_2x_tesla_v100_sxm2_32gb.md) | pentacoxian | Inspur NF5468M5 | Tesla V100-SXM2-32GB × 2 | Qwen3.8 Flash Next IQ3E-Q8D-MTP |
| 2026-09-23 | [在两张 Tesla V100 上比较 Qwen3.8 27B 的切分模式](report/2026-09-23_060231_comparing_split_modes_of_qwen3.8_27b_on_2x_tesla_v100.md) | miminashi | ASRock X99 Taichi | Tesla V100-SXM2-16GB × 2 | Huihui Qwen3.8 27B abliterated UD-Q4_K_XL |
| 2026-09-22 | [在两张 Tesla V100 上比较 Qwen3.8 27B 的切分模式，并提供单 GPU 基线](report/2026-09-22_210206_comparing_split_modes_of_qwen3.8_27b_on_2x_tesla_v100_with_single_gpu_baseline.md) | kuraneko1 | ASUS Z170-A | Tesla V100-PCIE-32GB + Tesla PG500-216 | Qwen3.8 27B UD-Q4_K_M |
| 2026-09-21 | [在 RTX 3060 + Tesla V100 上比较 Qwen3.8 27B 张量切分启用与禁用 NCCL 的性能](report/2026-09-21_183303_comparing_nccl_vs_no_nccl_tensor_split_on_rtx3060_and_tesla_v100.md) | eightman999 | Thirdwave XA7C-R47T / ASRock B760 TW/D4 | RTX 3060 12GB + Tesla V100-PCIE-32GB | Qwen3.8 27B Q4_K_M NCCL |
| 2026-09-21 | [在 RTX 3060 + Tesla V100 上比较 Qwen3.8 27B 的切分模式](report/2026-09-21_170911_comparing_split_modes_of_qwen3.8_27b_on_rtx3060_and_tesla_v100.md) | eightman999 | Thirdwave XA7C-R47T / ASRock B760 TW/D4 | RTX 3060 12GB + Tesla V100-PCIE-32GB | Qwen3.8 27B Q4_K_M |
| 2026-09-20 | [在七张 Tesla P100 上比较 Qwen3.8 27B 的切分模式](report/2026-09-20_072013_comparing_split_modes_of_qwen3.8_27b_on_7x_tesla_p100.md) | miminashi | Supermicro SYS-4028GR-TRT2 | Tesla P100 × 7 | Qwen3.8 27B UD-Q4_K_XL |
| 2026-09-20 | [在四张 Tesla P100 上比较 Qwen3.8 27B 的切分模式](report/2026-09-20_033840_comparing_split_modes_of_qwen3.8_27b_on_4x_tesla_p100.md) | miminashi | NEC Express5800/T120h | Tesla P100 × 4 | Qwen3.8 27B UD-Q4_K_XL |

原始报告位于 [report/](report/)。

## 隐私与发布注意事项

- 不要公开序列号、UUID、MAC 地址、主机名、IP 地址或绝对路径中包含的个人用户名。
- 不要提交模型文件（`.gguf`）、基准测试服务器日志、模型原始响应或敏感的本地数据。
- 上传前检查 `run-info.json` 和启动参数文件，去除私人路径与主机名。
- 提交新报告时，不要修改其他贡献者已有的报告。

## 许可证

请参阅本仓库的 [LICENSE](LICENSE)。
