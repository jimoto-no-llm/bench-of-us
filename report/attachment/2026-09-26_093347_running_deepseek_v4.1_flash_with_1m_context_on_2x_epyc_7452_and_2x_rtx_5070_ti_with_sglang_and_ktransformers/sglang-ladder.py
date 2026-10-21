#!/usr/bin/env python3
"""Depth ladder for an sglang server, the llama-split-bench protocol
(kuraneko1/llama-split-bench measure_ladder.py / measure_pp0.py, 7af72d4) on
sglang's native /generate:

  ladder  each stage sends fill_text(target) + TAIL; the previous stage's prompt
          is its prefix, so the radix cache holds it and only the new chunk is
          computed (the server must run with the radix cache on). Timings are
          the server's own, like llama.cpp's: prefill t/s = (prompt_tokens -
          cached_tokens) / (prefill_finished_time - forward_entry_time), decode
          t/s = meta_info decode_throughput. Streaming was 25-30% low on decode
          (09-28, qwen35: 60 vs 86). Greedy, ignore_eos.
  pp0     fresh prompts (a unique prefix defeats the cache) of 512 / 2048 / 8192
          tokens, 64 new tokens; the figure's depth-0 prefill is pp2048.

Writes results-<tag>.json and results-<tag>-pp0.json with the same keys as the
tool (prompt_per_second, predicted_per_second, ...).

  sglang-ladder.py --tag TAG --out DIR [--stages 0,32000,64000,128000]
                   [--n-predict 1000] [--url http://127.0.0.1:8080]
"""
import argparse
import json
import os

import urllib.request
import uuid

TAIL = ("\n\nContinue the sequence with the next 100 numbered lines, in exactly "
        "the same style. Do not stop and do not summarize.")


def fill_text(n_chars):
    unit = "Sequence {i}: the quick brown fox jumps over the lazy dog while we measure context tokens. "
    parts, total, i = [], 0, 1
    while total < n_chars:
        p = unit.format(i=i)
        parts.append(p)
        total += len(p)
        i += 1
    return "".join(parts)[:n_chars]


CLIENT_TIMING = False


def generate(url, text, n_predict):
    """/generate: returns (prefill seconds, decode t/s, meta) from the server's timings."""
    if CLIENT_TIMING:
        return generate_streamed(url, text, n_predict)
    body = json.dumps({"text": text,
                       "sampling_params": {"max_new_tokens": n_predict, "temperature": 0.0,
                                           "ignore_eos": True}}).encode()
    req = urllib.request.Request(url + "/generate", body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=7200) as r:
        meta = json.loads(r.read().decode())["meta_info"]
    if "prefill_finished_time" in meta and "forward_entry_time" in meta:
        prefill_s = meta["prefill_finished_time"] - meta["forward_entry_time"]
        return prefill_s, meta.get("decode_throughput"), meta
    return generate_streamed(url, text, n_predict)


def generate_streamed(url, text, n_predict):
    """Older trees (the GLM one) report no prefill_finished_time: time to the
    first streamed token for the prefill, and for the decode the server's
    e2e_latency minus that (the client-side stream alone reads 25-30% low)."""
    import time
    body = json.dumps({"text": text, "stream": True,
                       "sampling_params": {"max_new_tokens": n_predict, "temperature": 0.0,
                                           "ignore_eos": True}}).encode()
    req = urllib.request.Request(url + "/generate", body, {"Content-Type": "application/json"})
    t0, first, meta = time.time(), None, {}
    with urllib.request.urlopen(req, timeout=7200) as r:
        for raw in r:
            line = raw.decode().strip()
            if not line.startswith("data:") or line == "data: [DONE]":
                continue
            if first is None:
                first = time.time()
            meta = json.loads(line[5:]).get("meta_info", meta)
    ttft = first - t0
    n = meta.get("completion_tokens", 0)
    e2e = meta.get("e2e_latency") or (time.time() - t0)
    dec = (n - 1) / (e2e - ttft) if n > 1 and e2e > ttft else None
    meta["timing_source"] = "stream-ttft+e2e"
    return ttft, dec, meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--stages", default="0,32000,64000,128000")
    ap.add_argument("--n-predict", type=int, default=1000)
    ap.add_argument("--url", default="http://127.0.0.1:8080")
    ap.add_argument("--ratio", type=float, default=4.3, help="chars per token guess, adapted per stage")
    ap.add_argument("--pp0-only", action="store_true", help="only the fresh-prompt prefill")
    ap.add_argument("--client-timing", action="store_true",
                    help="trees whose chunked prefill reports only the last chunk (the Flash-Next "
                         "v0519 one: cached_tokens counts the request's own earlier chunks and the "
                         "timestamps are the last chunk's). Prefill = time to the first streamed "
                         "token, new tokens = prompt length minus the previous stage's")
    args = ap.parse_args()
    global CLIENT_TIMING
    CLIENT_TIMING = args.client_timing
    os.makedirs(args.out, exist_ok=True)

    # pp0: fresh prompts. The warm-up includes one fresh 8K prompt: the first
    # prompt that goes through the kt streamed prefill after launch pays its
    # one-off set-up (09-28, vision: pp2048 429 s = 4.4 t/s, then 560 t/s).
    generate(args.url, "warmup", 8)
    generate(args.url, f"[{uuid.uuid4()}] " + fill_text(int(8192 * args.ratio)), 8)
    pp0 = []
    for n in (512, 2048, 8192):
        text = f"[{uuid.uuid4()}] " + fill_text(int(n * args.ratio))
        ttft, _, meta = generate(args.url, text, 64)
        new = meta.get("prompt_tokens", 0) - (0 if CLIENT_TIMING else meta.get("cached_tokens", 0))
        pp0.append({"n_prompt_target": n, "prompt_n": new, "cached": meta.get("cached_tokens"),
                    "prompt_ms": ttft * 1000, "prompt_per_second": new / ttft})
        print(f"pp0 {n}: {new} tokens in {ttft:.2f} s = {new / ttft:.1f} t/s", flush=True)
    json.dump(pp0, open(os.path.join(args.out, f"results-{args.tag}-pp0.json"), "w"), indent=2)
    if args.pp0_only:
        return

    ratio, records, prev_pt = args.ratio, [], 0
    for k, target in enumerate(int(x) for x in args.stages.split(",")):
        prompt = ("The capital of France is and the capital of Germany is" if target == 0
                  else fill_text(int(target * ratio)) + TAIL)
        ttft, dec, meta = generate(args.url, prompt, args.n_predict)
        pt, cached = meta.get("prompt_tokens", 0), meta.get("cached_tokens", 0) or 0
        if CLIENT_TIMING:
            # the previous stage's prompt minus its TAIL is this one's prefix
            cached = max(0, prev_pt - 40) if target > 0 else 0
        prev_pt = pt
        new, done = pt - cached, meta.get("completion_tokens", 0)
        if target > 0 and pt:
            ratio = len(prompt) / pt  # adapt the chars-per-token guess
        rec = {"stage": k, "target_tokens": target, "effective_depth": pt, "cache_n": cached,
               "prompt_n": new, "prompt_ms": ttft * 1000, "prompt_per_second": new / ttft if ttft else None,
               "predicted_n": done, "predicted_per_second": dec, "e2e_s": meta.get("e2e_latency")}
        records.append(rec)
        print(f"stage {target}: depth {pt}, new {new} in {ttft:.1f} s = {rec['prompt_per_second']:.1f} t/s, "
              f"decode {done} tok = {rec['predicted_per_second']:.2f} t/s", flush=True)
        json.dump(records, open(os.path.join(args.out, f"results-{args.tag}.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
