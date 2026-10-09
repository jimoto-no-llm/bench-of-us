# 为 Bench of Us 贡献报告

[English (primary)](CONTRIBUTING.md) · **简体中文** · [日本語（代理操作说明）](CLAUDE.md)

欢迎分享本地大语言模型的硬件配置与性能实测结果。**不运行基准测试也可以参与。**

## 投稿流程

1. Fork 并克隆 [bench-of-us](https://github.com/jimoto-no-llm/bench-of-us)。
2. 收集硬件规格。如要运行测试，请参考 [llama-split-bench](https://github.com/kuraneko1/llama-split-bench)，记录模型、量化、工具、后端及测试条件。
3. 新建 `report/yyyy-mm-dd_HHMMSS_<english_slug>.md`。时间戳采用本地日期和时间；文件名尾部使用小写 ASCII 字符和下划线。
4. 图片、`results-*.json`、`run-info.json` 和必要的 `argv-*.txt` 放在 `report/attachment/<report_basename>/` 中。
5. 在**全部三个**索引中按从新到旧的顺序插入报告：`README.md`（英文）、`README.zh-CN.md`（简体中文）、`README.ja.md`（日文）。作者、设备、GPU、模型、日期和链接需保持一致；只翻译面向读者的描述。
6. 提交 Pull Request；尽量只包含新报告、附件与索引修改。

报告正文可使用任意语言。技术标识、单位、测量数值和文件路径应保持准确。建议使用 YAML frontmatter，方便网站稳定提取元数据。

## 报告最低要求

- 作者名字或网名（不需要真实姓名）。
- 整机或主板型号、GPU 型号与数量，最好补充每张 GPU 的显存容量。
- 测试条件和结果，**或者明确标记“未运行”**。
- 区分实测数据、估算值与未经验证的信息。

如有条件，也建议说明 CPU、内存、操作系统、驱动版本、GPU 互连方式及功耗限制。

## 推荐报告模板

```markdown
---
author: your-handle
date: 2026-10-09
machine: Example Motherboard
gpu: Example GPU
gpu_count: 2
model: Example Model Q4_K_M
backend: llama.cpp
benchmark: llama-split-bench
tags:
  - multi-gpu
---
# 报告标题

- **作者**: your-handle
- **日期**: 2026-10-09

## 摘要

用两至四行介绍设备配置和主要观察。

## 硬件

| 项目 | 规格 |
|------|------|
| 计算机 / 主板 | Example Motherboard |
| GPU | Example GPU × 2（每张 16 GB 显存） |
| CPU | Example CPU |
| 内存 | 64 GB |
| GPU 互连 | PCIe / NVLink（如已知） |

## 软件环境

| 项目 | 规格 |
|------|------|
| OS | 发行版 / 内核 |
| GPU 驱动 | 版本 |
| llama.cpp | 提交版本 / 构建方式；CUDA / ROCm / Vulkan / Metal / CPU |

## 基准测试

### 测试条件

| 项目 | 规格 |
|------|------|
| 工具 | llama-split-bench + 提交版本 |
| 模型 | 完整模型名及量化方式 |
| 切分模式 | layer / tensor / single / profile |
| 上下文及阶段 | CTX / STAGES |
| KV 缓存 | KV_K / KV_V |

### 测试结果

| depth | prefill layer (t/s) | decode layer (t/s) |
|-------|---------------------|--------------------|
| 4096 | 000.0 | 00.0 |

请以实测数值替换示例，并链接相关图片。

### 备注

说明异常现象、限制因素与测试条件。

## 附件

- [run-info.json](attachment/<report_basename>/run-info.json)
```

如果**仅分享硬件**，请将整个 `## 基准测试` 小节（含其子章节）替换为：

```markdown
## 基准测试

未运行
```

网站也能够识别英文 `Not run` 与日文 `未実施`。

## 隐私与安全

不要公开序列号、UUID、MAC 地址、主机名、IP 地址或包含个人用户名的绝对路径。提交前检查 `run-info.json` 与 `argv-*.txt`。不要提交 `.gguf` 模型文件、服务器日志、模型原始响应或私人输入数据。不要修改其他人的报告。

## 网站集成

网站读取 `report/`，若存在 YAML frontmatter 则优先使用。报告合并到主分支后，GitHub Actions 会自动更新网站。构建与解析详情参见 [site/README.md](site/README.md)。原始 Markdown 报告始终是数据正本。
