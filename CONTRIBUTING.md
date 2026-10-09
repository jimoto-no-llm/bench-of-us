# Contributing to Bench of Us

**English (primary)** · [简体中文](CONTRIBUTING.zh-CN.md) · [日本語（エージェント用手順）](CLAUDE.md)

Thank you for sharing your local LLM hardware setup or performance measurements. You do **not** need to run a benchmark to contribute.

## Submission workflow

1. Fork and clone [bench-of-us](https://github.com/jimoto-no-llm/bench-of-us).
2. Collect hardware specifications. If you wish to benchmark, follow [llama-split-bench](https://github.com/kuraneko1/llama-split-bench) and record the exact model, quantization, tool, backend, and test conditions.
3. Create `report/yyyy-mm-dd_HHMMSS_<english_slug>.md`. Use the local date/time for the timestamp and a lowercase ASCII/underscore slug.
4. Place figures, `results-*.json`, `run-info.json`, and relevant `argv-*.txt` under `report/attachment/<report_basename>/`.
5. Insert a report row, newest first, into **all three** indexes: `README.md` (English), `README.zh-CN.md` (Simplified Chinese), and `README.ja.md` (Japanese). Preserve the author, machine, GPU, model, date, and link exactly; translate only human-readable descriptions.
6. Open a pull request. Keep it focused on your new report, its attachments, and the indexes.

The original report text can be written in any language. Keep technical identifiers, units, numeric measurements, and file paths unchanged. YAML frontmatter is recommended so the website can extract metadata consistently.

## Minimum report requirements

- Author name or handle (a real name is not required).
- Machine or motherboard model, plus GPU model, count, and ideally VRAM per GPU.
- Either benchmark conditions and results **or** an explicit statement that the benchmark was not run.
- A clear distinction between measured results and estimates or unverified details.

CPU, RAM, OS, driver versions, GPU interconnects, and power limits are helpful when available.

## Suggested report template

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
# A descriptive report title

- **Author**: your-handle
- **Date**: 2026-10-09

## Summary

Describe the machine and the key observations in two to four lines.

## Hardware

| Item | Value |
|------|-------|
| Machine | Example Motherboard |
| GPU | Example GPU × 2 (VRAM 16 GB each) |
| CPU | Example CPU |
| RAM | 64 GB |
| GPU interconnect | PCIe / NVLink information, if known |

## Software environment

| Item | Value |
|------|-------|
| OS | Example distribution / kernel |
| GPU driver | Driver version |
| llama.cpp | Commit / build, CUDA / ROCm / Vulkan / Metal / CPU |

## Benchmark

### Conditions

| Item | Value |
|------|-------|
| Tool | llama-split-bench + commit |
| Model | Full model and quantization |
| Split mode | layer / tensor / single / profile |
| Context and stages | CTX / STAGES |
| KV cache | KV_K / KV_V |

### Results

| depth | prefill layer (t/s) | decode layer (t/s) |
|-------|---------------------|--------------------|
| 4096 | 000.0 | 00.0 |

Replace the example values with actual measured results and link figures.

### Notes

Describe surprising behavior, limitations, and test conditions.

## Attachments

- [run-info.json](attachment/<report_basename>/run-info.json)
```

For **hardware-only submissions**, replace the `## Benchmark` section (including its subsections) with exactly:

```markdown
## Benchmark

Not run
```

The website also recognizes `未実施` (Japanese) and `未运行` (Simplified Chinese).

## Privacy and safety

Do not include serial numbers, UUIDs, MAC addresses, hostnames, IP addresses, or user-identifying absolute paths. Review `run-info.json` and `argv-*.txt` before submitting. Do not commit `.gguf` model files, server logs, raw responses, or private input data. Do not modify other people's reports.

## Website integration

The site reads reports from `report/` and prefers YAML frontmatter when present. Reports merge into the website automatically through GitHub Actions. See [site/README.md](site/README.md) for build and parser details. The report Markdown remains the source of truth.
