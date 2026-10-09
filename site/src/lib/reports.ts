import { readdir, readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

import { fmList, fmNumber, fmString, splitFrontmatter } from './frontmatter';
import {
  extractBenchTable,
  extractBullet,
  extractSection,
  extractSummary,
  extractTables,
  extractTitle,
  parseGpu,
  parseModel,
  stripMarkdown,
  type BenchTable,
} from './parse';

const thisDir = path.dirname(fileURLToPath(import.meta.url)); // site/src/lib
const siteRoot = path.resolve(thisDir, '..', '..');
const repoRoot = path.resolve(siteRoot, '..');
export const REPORT_DIR = path.join(repoRoot, 'report');

export const GITHUB_REPO = 'https://github.com/jimoto-no-llm/bench-of-us';
export const GITHUB_BLOB = `${GITHUB_REPO}/blob/main`;

export const UNKNOWN = '不明';

export type Report = {
  slug: string;
  file: string;
  title: string;
  author: string;
  date: string;
  summary?: string;
  machine: string;
  gpu: string;
  gpuCount?: number;
  model: string;
  backend: string;
  benchmark: string;
  os?: string;
  tags: string[];
  hasBenchmark: boolean;
  benchTable?: BenchTable;
  githubUrl: string;
  body: string;
  warnings: string[];
};

function dateFromFilename(file: string): string | undefined {
  const match = file.match(/^(\d{4}-\d{2}-\d{2})/);
  return match?.[1];
}

function titleFromFilename(file: string): string {
  return file.replace(/\.md$/, '').replace(/^\d{4}-\d{2}-\d{2}_\d{6}_/, '').replace(/_/g, ' ');
}

function parseReport(file: string, raw: string): Report {
  const warnings: string[] = [];
  const slug = file.replace(/\.md$/, '');

  const { data, body, warning } = splitFrontmatter(raw);
  if (warning) warnings.push(warning);

  const tables = extractTables(body);

  const title = fmString(data, 'title') ?? extractTitle(body) ?? titleFromFilename(file);
  const author = fmString(data, 'author') ?? extractBullet(body, ['作成者', 'author', '作者']) ?? UNKNOWN;
  const date =
    fmString(data, 'date') ??
    extractBullet(body, ['作成日', 'date', '日期', '创建日期']) ??
    dateFromFilename(file) ??
    UNKNOWN;

  const machine =
    fmString(data, 'machine') ??
    lookup(['コンピュータ / マザーボード', 'コンピュータ', 'マザーボード', 'machine', 'computer', 'motherboard', 'computer / motherboard', '计算机 / 主板', '计算机', '主板', '机器 / 主板']) ??
    UNKNOWN;

  const gpuRaw = lookup(['GPU']);
  const parsedGpu = parseGpu(gpuRaw);
  const gpu = fmString(data, 'gpu') ?? parsedGpu?.gpu ?? UNKNOWN;
  const gpuCount = fmNumber(data, 'gpu_count') ?? parsedGpu?.gpuCount;

  const benchSection = extractSection(body, 'ベンチマーク') ?? extractSection(body, 'Benchmark') ?? extractSection(body, '基准测试');
  const notRun = /^(?:未実施|未运行|未执行|未测试|not\s+(?:run|performed|measured))[.。]?$/i;
  const hasBenchmark = benchSection !== undefined && !notRun.test(benchSection.trim());

  const model =
    fmString(data, 'model') ?? parseModel(lookup(['モデル', 'model', '模型'])) ?? (hasBenchmark ? UNKNOWN : '未実施');

  const toolRaw = lookup(['ツール', 'tool', 'benchmark', '工具', '基准测试工具']);
  const benchmark =
    fmString(data, 'benchmark') ?? (toolRaw ? toolRaw.split(/\s+/)[0] : hasBenchmark ? UNKNOWN : '未実施');

  const backend = fmString(data, 'backend') ?? lookup(['llama.cpp', 'backend', 'バックエンド', '后端']) ?? UNKNOWN;
  const os = fmString(data, 'os') ?? lookup(['OS', '操作系统']);

  const benchTable = hasBenchmark ? extractBenchTable(tables) : undefined;
  if (hasBenchmark && !benchTable) {
    warnings.push('depth 別の結果表を認識できませんでした（レポート本文はそのまま表示します）');
  }
  if (author === UNKNOWN) warnings.push('作成者を抽出できませんでした');
  if (gpu === UNKNOWN) warnings.push('GPU を抽出できませんでした');

  return {
    slug,
    file,
    title,
    author,
    date,
    summary: fmString(data, 'summary') ?? extractSummary(body),
    machine,
    gpu,
    gpuCount,
    model,
    backend,
    benchmark,
    os,
    tags: fmList(data, 'tags'),
    hasBenchmark,
    benchTable,
    githubUrl: `${GITHUB_BLOB}/report/${file}`,
    body,
    warnings,
  };

  function lookup(labels: string[]): string | undefined {
    for (const table of tables) {
      for (const row of table.rows) {
        if (row.length < 2) continue;
        const key = row[0].replace(/\s+/g, '').toLowerCase();
        if (labels.some((l) => l.replace(/\s+/g, '').toLowerCase() === key)) {
          const value = stripMarkdown(row[1]);
          if (value) return value;
        }
      }
    }
    return undefined;
  }
}

let cache: Report[] | undefined;

/** report/*.md をすべて読み込み、日付の新しい順に返す。 */
export async function getReports(): Promise<Report[]> {
  if (cache) return cache;

  let files: string[] = [];
  try {
    files = (await readdir(REPORT_DIR)).filter((f) => f.endsWith('.md')).sort();
  } catch (error) {
    console.warn(`[reports] ${REPORT_DIR} を読めませんでした: ${String(error)}`);
    return [];
  }

  const reports: Report[] = [];
  for (const file of files) {
    try {
      const raw = await readFile(path.join(REPORT_DIR, file), 'utf8');
      const report = parseReport(file, raw);
      for (const warning of report.warnings) {
        console.warn(`[reports] ${file}: ${warning}`);
      }
      reports.push(report);
    } catch (error) {
      // 1 本の解析失敗でサイト全体を落とさない
      console.warn(`[reports] ${file} の解析に失敗したのでスキップします: ${String(error)}`);
    }
  }

  reports.sort((a, b) => (a.date === b.date ? b.file.localeCompare(a.file) : b.date.localeCompare(a.date)));
  cache = reports;
  return reports;
}

export type Stats = {
  reports: number;
  gpuSetups: number;
  models: number;
  contributors: number;
};

export function summarize(reports: Report[]): Stats {
  const setups = new Set<string>();
  const models = new Set<string>();
  const authors = new Set<string>();

  for (const report of reports) {
    if (report.gpu !== UNKNOWN) setups.add(`${report.gpu} x${report.gpuCount ?? '?'}`);
    if (report.model !== UNKNOWN && report.model !== '未実施') models.add(report.model);
    if (report.author !== UNKNOWN) authors.add(report.author);
  }

  return {
    reports: reports.length,
    gpuSetups: setups.size,
    models: models.size,
    contributors: authors.size,
  };
}

export function gpuLabel(report: Report): string {
  if (report.gpu === UNKNOWN) return UNKNOWN;
  return report.gpuCount ? `${report.gpu} × ${report.gpuCount}` : report.gpu;
}

/** 検索用の 1 本のテキスト。 */
export function searchIndex(report: Report): string {
  return [
    report.title,
    report.author,
    report.machine,
    report.gpu,
    report.gpuCount ? `x${report.gpuCount}` : '',
    report.model,
    report.backend,
    report.benchmark,
    report.os ?? '',
    report.tags.join(' '),
    report.summary ?? '',
  ]
    .join(' ')
    .toLowerCase();
}
