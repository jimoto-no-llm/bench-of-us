# site — Bench of Us GitHub Pages 网站

[English (primary)](README.md) · **简体中文** · [日本語](README.ja.md)

本 Astro 项目根据 `report/*.md` 和 `report/attachment/` 自动生成静态网站。

**线上地址：** https://jimoto-no-llm.github.io/bench-of-us/

`report/` 是唯一的数据正本；不会为了展示而另外复制维护一套报告正文。

## 本地开发

```bash
cd site
npm install
npm run dev      # http://localhost:4321/bench-of-us/
npm run build    # 输出到 dist/
npm run preview  # 预览构建结果
npm test         # 构建并检查报告数量和站内链接
```

执行 `npm run build` 或 `npm run dev` 时，会先运行 `scripts/sync-assets.mjs`，将 `report/attachment/` 复制到 `site/public/report-assets/`。该复制目录不纳入 Git 版本管理。

## 项目结构

| 路径 | 用途 |
|------|------|
| `src/lib/reports.ts` | 读取 `report/*.md` 并提取报告元数据 |
| `src/lib/parse.ts` | 解析不含 frontmatter 的现有 Markdown |
| `src/lib/frontmatter.ts` | 解析可选的 YAML frontmatter |
| `src/lib/markdown.ts` | 安全渲染 Markdown 并重写相对 URL |
| `src/pages/` | 首页、报告列表、报告详情、性能浏览器与投稿页面 |
| `scripts/sync-assets.mjs` | 复制报告附件 |
| `scripts/check-build.mjs` | 在 CI 中检查生成的报告数及链接 |

## 报告元数据

如果报告包含 frontmatter，就优先使用其中的字段；否则从标题、作者/日期列表及硬件/测试表格中提取。

- 标题：首个 `# 标题`，除非 frontmatter 另有指定。
- 作者与日期：识别英文 `Author`/`Date`、日文 `作成者`/`作成日` 或中文 `作者`/`日期`，日期还可以从文件名获取。
- 设备、GPU、模型及基准测试：根据已识别的表格字段提取；建议使用 frontmatter 避免歧义。
- 摘要：识别 `概要`、`Summary`、`摘要` 与 `概述`。

提取失败时，网站会显示“未知”占位符并输出 warning。单份报告解析失败不会导致整个网站构建失败。

以下 frontmatter 字段均为可选项：

```yaml
---
author: miminashi
date: 2026-09-20
machine: Supermicro SYS-4028GR-TRT2
gpu: Tesla P100-PCIE-16GB
gpu_count: 7
model: Qwen3.8-27B-UD-Q4_K_XL
backend: llama.cpp
benchmark: llama-split-bench
tags:
  - p100
  - qwen3.8
  - multi-gpu
---
```

英文、中文和日文报告均可使用这些字段；原始 Markdown 保持不变。

## 基础路径

这是 GitHub Pages 项目网站，因此 `astro.config.mjs` 配置了 `base: '/bench-of-us'`。报告内的相对路径 `attachment/…` 会在渲染时重写为 `/bench-of-us/report-assets/…`。

如果部署在其他位置，需要修改 Astro 配置中的 `site` 和 `base`。

## 相关文档

- [英文投稿指南](../CONTRIBUTING.md)
- [简体中文投稿指南](../CONTRIBUTING.zh-CN.md)
- [主 README](../README.md)
