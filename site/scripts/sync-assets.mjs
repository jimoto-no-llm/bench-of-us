// report/attachment/ を site/public/report-assets/ へコピーする。
// 正本は report/ 側。ここで生成したコピーは git 管理外（site/.gitignore）。
import { cp, mkdir, readdir, rm, stat } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const siteRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = path.resolve(siteRoot, '..');
const src = path.join(repoRoot, 'report', 'attachment');
const dest = path.join(siteRoot, 'public', 'report-assets');
// csv / diff も許可する: ベンチの生データ（サンプル列）やパッチ差分をそのまま証跡として
// 添付するレポートがある（例: report/2026-09-26_171511_..._128gb, report/2026-09-26_203225_..._rtx_5090）。
// いずれも静的テキストで、サイトからは report-assets/ としてそのまま配信される。
// py も許可する: 計測・集計に使った補助スクリプトを再現手順の証跡として添付できるようにする。
// サイトのビルドでは実行も import もせず、テキストとしてコピーするだけ。
// patch も許可する: git format-patch 形式のパッチを diff と同様に証跡として添付できるようにする。
const allowedExtensions = new Set(['.png', '.json', '.txt', '.csv', '.diff', '.py', '.patch']);

async function exists(p) {
  try {
    await stat(p);
    return true;
  } catch {
    return false;
  }
}

async function validateAttachments(dir) {
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);

    if (entry.isDirectory()) {
      await validateAttachments(full);
      continue;
    }

    const relative = path.relative(repoRoot, full);
    if (!entry.isFile()) {
      throw new Error(`[sync-assets] 許可されていない添付形式です: ${relative}`);
    }

    if (!allowedExtensions.has(path.extname(entry.name).toLowerCase())) {
      throw new Error(`[sync-assets] 許可されていない添付形式です: ${relative}`);
    }
  }
}

if (!(await exists(src))) {
  console.warn(`[sync-assets] ${path.relative(repoRoot, src)} が無いのでスキップします`);
  await mkdir(dest, { recursive: true });
} else {
  await validateAttachments(src);
  await rm(dest, { recursive: true, force: true });
  await mkdir(path.dirname(dest), { recursive: true });
  await cp(src, dest, { recursive: true });
  console.log(`[sync-assets] copied ${path.relative(repoRoot, src)} -> ${path.relative(repoRoot, dest)}`);
}
