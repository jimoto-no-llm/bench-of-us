/**
 * 既存レポート（frontmatter 無し）の Markdown からメタデータを抽出する。
 * どの抽出も失敗したら undefined を返し、呼び出し側で「不明」に落とす。
 */

export type MarkdownTable = { header: string[]; rows: string[][] };

const SEPARATOR_CELL = /^:?-{2,}:?$/;

function splitRow(line: string): string[] {
  return line
    .trim()
    .replace(/^\|/, '')
    .replace(/\|$/, '')
    .split(/(?<!\\)\|/)
    .map((cell) => cell.replace(/\\\|/g, '|').trim());
}

/** 本文中のすべての Markdown 表を取り出す。 */
export function extractTables(body: string): MarkdownTable[] {
  const tables: MarkdownTable[] = [];
  const lines = body.split(/\r?\n/);
  let buffer: string[] = [];

  const flush = () => {
    if (buffer.length >= 2) {
      const header = splitRow(buffer[0]);
      const separator = splitRow(buffer[1]);
      if (separator.length === header.length && separator.every((cell) => SEPARATOR_CELL.test(cell))) {
        tables.push({ header, rows: buffer.slice(2).map(splitRow) });
      }
    }
    buffer = [];
  };

  for (const line of lines) {
    if (line.trim().startsWith('|')) buffer.push(line);
    else flush();
  }
  flush();

  return tables;
}

const normalize = (s: string) => s.replace(/\s+/g, '').toLowerCase();

/** 「| ラベル | 値 |」形式の 2 列表から、ラベルに一致する行の値を返す。 */
export function lookupTableValue(tables: MarkdownTable[], labels: string[]): string | undefined {
  const wanted = labels.map(normalize);
  for (const table of tables) {
    for (const row of table.rows) {
      if (row.length < 2) continue;
      if (wanted.includes(normalize(row[0]))) {
        const value = stripMarkdown(row[1]);
        if (value) return value;
      }
    }
  }
  return undefined;
}

/** 表示用に軽く Markdown 記法を落とす（メタデータ表示用。本文には使わない）。 */
export function stripMarkdown(text: string): string {
  return text
    .replace(/!\[[^\]]*\]\([^)]*\)/g, '')
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/`/g, '')
    .replace(/\*\*(.+?)\*\*/g, '$1')
    .replace(/__(.+?)__/g, '$1')
    .replace(/\*(.+?)\*/g, '$1')
    .trim();
}

export function extractTitle(body: string): string | undefined {
  const match = body.match(/^#\s+(.+?)\s*$/m);
  return match ? stripMarkdown(match[1]) : undefined;
}

/** 「- **作成者**: miminashi」形式の箇条書きを読む。 */
export function extractBullet(body: string, labels: string[]): string | undefined {
  const wanted = labels.map(normalize);
  const re = /^[-*]\s+\*\*(.+?)\*\*\s*[:：]\s*(.+?)\s*$/gm;
  for (const match of body.matchAll(re)) {
    if (wanted.includes(normalize(match[1]))) return stripMarkdown(match[2]);
  }
  return undefined;
}

/** 見出し名で節の本文を取り出す。 */
export function extractSection(body: string, heading: string): string | undefined {
  const lines = body.split(/\r?\n/);
  const target = normalize(heading);
  let collecting = false;
  let level = 0;
  const collected: string[] = [];

  for (const line of lines) {
    const h = line.match(/^(#{1,6})\s+(.*)$/);
    if (h) {
      if (collecting && h[1].length <= level) break;
      if (!collecting && normalize(h[2]) === target) {
        collecting = true;
        level = h[1].length;
        continue;
      }
    }
    if (collecting) collected.push(line);
  }

  const text = collected.join('\n').trim();
  return text === '' ? undefined : text;
}

/** 概要節を 1 段落の平文にする。 */
export function extractSummary(body: string): string | undefined {
  const section = extractSection(body, '概要') ?? extractSection(body, 'Summary') ?? extractSection(body, '摘要') ?? extractSection(body, '概述');
  if (!section) return undefined;
  const paragraph = section.split(/\r?\n\s*\r?\n/)[0];
  return stripMarkdown(paragraph.replace(/\r?\n/g, ' ')) || undefined;
}

export type GpuInfo = { gpu: string; gpuCount?: number };

/** 「Tesla P100-PCIE-16GB × 7（VRAM 16 GB / 枚）」から型番と枚数を取り出す。 */
export function parseGpu(raw: string | undefined): GpuInfo | undefined {
  if (!raw) return undefined;
  const cleaned = raw.replace(/[（(][^）)]*[）)]/g, ' ').replace(/\s+/g, ' ').trim();
  const match = cleaned.match(/^(.+?)\s*[×xX*]\s*(\d+)/);
  if (match) return { gpu: match[1].trim(), gpuCount: Number(match[2]) };
  return { gpu: cleaned };
}

/** 「Qwen3.8-27B-UD-Q4_K_XL（17.6 GB）＋ MTP ヘッド …」からモデル名を取り出す。 */
export function parseModel(raw: string | undefined): string | undefined {
  if (!raw) return undefined;
  const head = raw.split(/[＋+]/)[0];
  const cleaned = head.replace(/[（(][^）)]*[）)]/g, ' ').replace(/\s+/g, ' ').trim();
  return cleaned || undefined;
}

export type BenchRow = { depth: string; values: Record<string, number> };
export type BenchTable = { columns: string[]; rows: BenchRow[] };

/** 「| depth | prefill layer | …」形式の結果表を構造化する。見つからなければ undefined。 */
export function extractBenchTable(tables: MarkdownTable[]): BenchTable | undefined {
  for (const table of tables) {
    if (table.header.length < 2) continue;
    if (normalize(table.header[0]) !== 'depth') continue;
    const columns = table.header.slice(1).map((c) => stripMarkdown(c));
    const rows: BenchRow[] = [];
    for (const row of table.rows) {
      if (row.length !== table.header.length) continue;
      const values: Record<string, number> = {};
      columns.forEach((column, i) => {
        const n = Number(row[i + 1]);
        if (Number.isFinite(n)) values[column] = n;
      });
      if (Object.keys(values).length > 0) rows.push({ depth: stripMarkdown(row[0]), values });
    }
    if (rows.length > 0) return { columns, rows };
  }
  return undefined;
}
