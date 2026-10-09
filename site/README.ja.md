# site — Bench of Us の GitHub Pages サイト

[English (primary)](README.md) · [简体中文](README.zh-CN.md) · **日本語**

`report/*.md` と `report/attachment/` を読み取って、静的サイトを生成します。
公開先: https://jimoto-no-llm.github.io/bench-of-us/

レポートの正本は `report/` です。サイトのためにデータを二重管理しません。

## 開発

```bash
cd site
npm install
npm run dev      # http://localhost:4321/bench-of-us/
npm run build    # dist/ に出力
npm run preview  # build 結果を確認
npm test         # build + 生成物チェック（リンク切れ・レポート数）
```

`npm run build` / `npm run dev` は先に `scripts/sync-assets.mjs` を実行し、`report/attachment/` を
`site/public/report-assets/` にコピーします（このコピーは git 管理外）。

## 構成

| パス | 内容 |
|------|------|
| `src/lib/reports.ts` | `report/*.md` の読み込みとメタデータ抽出 |
| `src/lib/parse.ts` | 既存 Markdown（frontmatter なし）からの抽出 |
| `src/lib/frontmatter.ts` | 任意の frontmatter の最小パーサ |
| `src/lib/markdown.ts` | Markdown → HTML（生 HTML は除去、相対 URL を base 付きに変換） |
| `src/pages/` | トップ / レポート一覧 / 個別レポート / Performance Explorer / Contribute |
| `scripts/sync-assets.mjs` | 添付のコピー |
| `scripts/check-build.mjs` | 生成物の検査（CI で実行） |

## メタデータの読み取り

frontmatter があればそれを優先し、無ければ本文から抽出します。

- タイトル: 先頭の `# 見出し`
- 作成者 / 作成日: `- **作成者**: …` / `- **作成日**: …`（無ければファイル名の日付）
- マシン / GPU / CPU など: ハードウェア表の行
- モデル / ツール: ベンチマーク条件表の行

抽出に失敗した項目は「不明」として表示し、ビルドログに warning を出します。
1 本のレポートの解析失敗でサイト全体のビルドは落ちません。

frontmatter を使う場合（すべて任意）:

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

## base path

GitHub Pages の project site なので `astro.config.mjs` で `base: '/bench-of-us'` を設定しています。
レポート内の `attachment/…` への相対リンクは、ビルド時に `/bench-of-us/report-assets/…` へ書き換えます。
別の場所で公開する場合は `site` と `base` を変更してください。
