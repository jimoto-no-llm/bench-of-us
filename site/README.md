# site — Bench of Us GitHub Pages website

**English (primary)** · [简体中文](README.zh-CN.md) · [日本語](README.ja.md)

This Astro project generates a static website from `report/*.md` and `report/attachment/`.

**Live site:** https://jimoto-no-llm.github.io/bench-of-us/

The source of truth is `report/`. Reports are not duplicated or manually edited for the website.

## Development

```bash
cd site
npm install
npm run dev      # http://localhost:4321/bench-of-us/
npm run build    # output to dist/
npm run preview  # preview the built site
npm test         # build + report-count and local-link checks
```

`npm run build` and `npm run dev` run `scripts/sync-assets.mjs` first to copy `report/attachment/` into `site/public/report-assets/`. This copy is excluded from Git.

## Project layout

| Path | Purpose |
|------|---------|
| `src/lib/reports.ts` | Read `report/*.md` and extract report metadata |
| `src/lib/parse.ts` | Parse existing Markdown without frontmatter |
| `src/lib/frontmatter.ts` | Minimal optional YAML frontmatter parser |
| `src/lib/markdown.ts` | Render Markdown safely and rewrite relative URLs for the site base |
| `src/pages/` | Home, report index, report details, Performance Explorer, and Contribute |
| `scripts/sync-assets.mjs` | Copy report attachments |
| `scripts/check-build.mjs` | Check generated report count and links in CI |

## Report metadata

Frontmatter takes precedence; otherwise, fields are extracted from headings, author/date bullets, and hardware/benchmark tables.

- Title: the first `# Heading`, unless provided in frontmatter.
- Author / date: English `Author`/`Date`, Japanese `作成者`/`作成日`, or Chinese `作者`/`日期` (and filename date fallback).
- Machine, GPU, CPU, model, and benchmark information: recognized table labels; frontmatter avoids ambiguity.
- Summary: `概要`, `Summary`, `摘要`, or `概述`.

If extraction fails, the website displays its unknown-value placeholder and logs a warning. A single malformed report does not fail the entire build.

All frontmatter fields below are optional:

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

English, Chinese, and Japanese reports can use these keys. The original Markdown remains unchanged.

## Base path

This is a GitHub Pages project site: `astro.config.mjs` configures `base: '/bench-of-us'`. Relative `attachment/…` URLs inside reports are rewritten to `/bench-of-us/report-assets/…` during rendering.

If deploying elsewhere, update the `site` and `base` settings in the Astro configuration.

## Related docs

- [English contributor guide](../CONTRIBUTING.md)
- [简体中文贡献指南](../CONTRIBUTING.zh-CN.md)
- [Main README](../README.md)
