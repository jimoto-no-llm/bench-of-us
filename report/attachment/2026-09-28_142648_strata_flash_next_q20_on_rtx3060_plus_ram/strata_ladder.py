#!/usr/bin/env python3
"""Depth-ladder bench for the Strata server (OpenAI-compatible).
Grows one conversation so the engine re-reads only the new suffix each stage.
Reads exact stats from strata-q2_0.log lines emitted per request.
"""
import json, re, sys, time, urllib.request

URL = "http://127.0.0.1:8080/v1/chat/completions"
LOG = "~/dev/tools/Strata/strata-q2_0.log"
GEN_TOKENS = 220

# filler: numbered pseudo-technical paragraphs; ~1 token per ~3.2 chars JP-ish, use EN text
def chunk(n_paras, start):
    out = []
    topics = ["memory bandwidth", "expert routing", "kv cache layout", "speculative decoding",
              "PCIe transfer", "tensor quantization", "context window", "attention scoring"]
    for i in range(start, start + n_paras):
        t = topics[i % len(topics)]
        out.append(f"Note {i}: The {t} subsystem of the inference engine was measured under steady "
                   f"load. Observation {i} confirms that {t} behaves predictably when the worker "
                   f"pool is saturated, and parameter {i*7%13} remains the dominant factor. "
                   f"Additional detail {i}: measurements were taken at fixed intervals and show "
                   f"consistent behaviour across repeated trials of the same configuration.\n")
    return "\n".join(out)

def count_log_lines():
    try:
        with open(LOG, encoding="utf-8", errors="replace") as f:
            return sum(1 for _ in f)
    except OSError:
        return 0

def read_new_stats(start_line):
    pat = re.compile(r"prompt (\d+) tokens = (\d+) reused \+ (\d+) read in ([\d.]+) ms \(([\d.]+) tok/s\), (\d+) generated in ([\d.]+) ms \(([\d.]+) tok/s\), drafts accepted (\d+) of (\d+)")
    res = []
    with open(LOG, encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f):
            if i < start_line:
                continue
            m = pat.search(line)
            if m:
                res.append(tuple(m.groups()))
    return res

def send(messages, max_tokens):
    body = json.dumps({"model": "qwen3.8-flash-next-q2_0", "messages": messages,
                       "max_tokens": max_tokens, "temperature": 0.6}).encode()
    req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=900) as r:
        d = json.loads(r.read())
    return d, time.time() - t0

def approx_tokens(s):  # rough estimate to size the chunks
    return len(s) // 4

STAGES = [8000, 16000, 24000, 30000]   # target cumulative prompt sizes (tokens, approx)
messages = []
results = []

# warm-up + depth ~500
log_pos = count_log_lines()
d, dt = send([{"role": "user", "content": "Reply with exactly one word: ready"}], 8)
for s in read_new_stats(log_pos):
    print("warmup:", s, flush=True)

cum = 0
para_idx = 0
for target in STAGES:
    # build a filler chunk that lands near the target
    text = ""
    while approx_tokens(text) < target - cum:
        text += chunk(40, para_idx); para_idx += 40
    text += f"\nEnd of section. Now list {3 + target//8000} distinct prime numbers greater than 1000."
    messages.append({"role": "user", "content": text})
    log_pos = count_log_lines()
    t0 = time.time()
    d, dt = send(messages, GEN_TOKENS)
    stats = read_new_stats(log_pos)
    usage = d.get("usage", {})
    cum = usage.get("prompt_tokens", cum + target)
    print(f"stage~{target}: wall={dt:.1f}s usage={usage}", flush=True)
    for s in stats:
        ptok, reused, read, pms, prate, gen, gms, grate, acc, off = s
        print(f"  STATS total={ptok} reused={reused} read={read} prefill={prate}t/s decode={grate}t/s gen={gen} accept={acc}/{off}", flush=True)
        results.append({"stage_target": target, "prompt_tokens": int(ptok), "reused": int(reused),
                        "read": int(read), "prefill_tps": float(prate), "gen_tokens": int(gen),
                        "decode_tps": float(grate), "accept": f"{acc}/{off}", "wall_s": round(dt, 1)})
    messages.append({"role": "assistant", "content": d["choices"][0]["message"]["content"]})

print("===SUMMARY===")
print(json.dumps(results, indent=1))
with open("/tmp/strata_ladder_results.json", "w") as f:
    json.dump(results, f, indent=1)
