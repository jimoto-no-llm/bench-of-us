#!/usr/bin/env python3
"""Measure ProjectMaya prefill/decode at arbitrary context depths.

Starts the persistent engine (strata --serve) with the pack/config given, sends one
GEN request per depth, and records the DONE timings.  The prompt is a repetition of
the project's docs and source code, so it is representative of coding/repo context.
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path("~/project-maya").expanduser()
sys.path.insert(0, str(ROOT))
import serve.server as SV  # noqa: E402
import strata_tokenizer as ST  # noqa: E402


def corpus_ids(tok, need):
    parts = []
    for pattern in ("README.md", "docs/*.md", "src/**/*.py", "serve/**/*.py", "src/**/*.cu", "src/**/*.cpp", "bench/results/*.md"):
        for p in sorted(ROOT.glob(pattern)):
            try:
                parts.append(p.read_text(encoding="utf-8", errors="replace"))
            except OSError:
                pass
    text = "\n\n".join(parts)
    while len(text) < need * 4:
        text += "\n\n" + text
    ids = tok.encode(text)
    if len(ids) < need:
        raise SystemExit(f"corpus only produced {len(ids)} tokens, need {need}")
    return ids[:need]


def build_prompt(tok, corpus, ctx, max_new):
    target = ctx - max_new - 16
    head0 = tok.encode("[gMASK]<sop><|user|>\n", parse_special=True)
    needle = tok.encode(
        '\n# bench-of-us long-context needle\ndef bench_of_us_secret():\n    return "BENCH-OF-US-7F3A"\n',
        parse_special=True,
    )
    tail = tok.encode(
        "\n\nQuestion: In the code above, what exact string does bench_of_us_secret() return? "
        "Answer with only that string.<|assistant|>\n</think>",
        parse_special=True,
    )
    pre_n = max(64, target // 20)  # needle at ~5% depth
    ids = head0 + corpus[:pre_n] + needle
    middle_n = target - len(ids) - len(tail)
    if middle_n <= 0:
        raise SystemExit(f"ctx {ctx}: prompt does not fit (head {len(ids)}, tail {len(tail)})")
    return ids + corpus[pre_n : pre_n + middle_n] + tail


def stage(cfg, ids, ctx, max_new, out_dir, tok):
    cfg = json.loads(json.dumps(cfg))
    args = list(cfg["args"])
    args[args.index("--max-context") + 1] = str(ctx)
    cfg["args"] = args
    log_path = out_dir / f"engine-{ctx}.log"
    prompt = ids[: max(1, ctx - max_new - 16)]
    t_start = time.time()
    with open(log_path, "w", encoding="utf-8") as log:
        p = subprocess.Popen(
            [cfg["exe"], "--serve"] + SV.engine_args(cfg),
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=log, text=True,
            env=SV.child_env(cfg), cwd=cfg.get("cwd") or str(ROOT), bufsize=1,
        )
        ready = None
        while True:
            line = p.stdout.readline()
            if not line:
                raise RuntimeError(f"engine exited before READY (see {log_path})")
            if line.startswith("READY"):
                ready = line.strip()
                break
        load_s = time.time() - t_start

        def gen(ids_in, n):
            p.stdin.write(f"GEN {n} temperature=0 " + ",".join(map(str, ids_in)) + "\n")
            p.stdin.flush()
            pp = []
            toks = []
            while True:
                line = p.stdout.readline()
                if not line:
                    raise RuntimeError(f"engine exited during GEN (see {log_path})")
                if line.startswith("PP "):
                    pp.append(line.strip())
                elif line.startswith("T "):
                    toks.append(int(line.split()[1]))
                elif line.startswith("DONE"):
                    f = line.split()
                    return f, pp, toks
                elif line.startswith("ERR"):
                    raise RuntimeError(line.strip())

        gen(ids[:64], 8)  # warm-up
        t0 = time.time()
        f, pp, out_toks = gen(prompt, max_new)
        wall = time.time() - t0
        p.stdin.write("QUIT\n")
        p.stdin.flush()
        try:
            p.wait(timeout=120)
        except subprocess.TimeoutExpired:
            p.kill()
    prompt_n = int(f[2])
    prompt_ms = float(f[3])
    decode_ms = float(f[4])
    text = tok.decode(out_toks)
    return {
        "ctx": ctx,
        "prompt_tokens": prompt_n,
        "generated": int(f[1]),
        "finish": f[5],
        "prompt_ms": prompt_ms,
        "decode_ms": decode_ms,
        "prefill_tok_s": prompt_n / prompt_ms * 1000.0 if prompt_ms else None,
        "decode_tok_s": int(f[1]) / decode_ms * 1000.0 if decode_ms else None,
        "load_s": load_s,
        "wall_s": wall,
        "ready": ready,
        "needle_found": "BENCH-OF-US-7F3A" in text,
        "output_head": text[:300],
        "output_tail": text[-300:],
        "pp_lines": pp[-3:],
        "engine_log": str(log_path),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--contexts", default="32768,131072,262144,524288,1048576")
    ap.add_argument("--max-new", type=int, default=128)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out_dir = Path(a.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    cfg = json.loads(Path(a.config).read_text())
    tok = ST.Tokenizer.from_dir(Path(cfg["tokenizer"]))
    contexts = [int(x) for x in a.contexts.split(",")]
    corpus = corpus_ids(tok, max(contexts) + a.max_new + 4096)
    results = []
    for ctx in contexts:
        print(f"=== ctx {ctx}", flush=True)
        try:
            ids = build_prompt(tok, corpus, ctx, a.max_new)
            r = stage(cfg, ids, ctx, a.max_new, out_dir, tok)
            print(json.dumps(r, ensure_ascii=False), flush=True)
        except Exception as e:  # noqa: BLE001 - report and continue with other depths
            r = {"ctx": ctx, "error": str(e)}
            print(json.dumps(r, ensure_ascii=False), flush=True)
        results.append(r)
        (out_dir / "results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
