#!/usr/bin/env python3
"""vllm-split-bench: llama-split-bench と同じプロトコル／同じ出力スキーマを、
既に稼働している vLLM の OpenAI 互換サーバに対して実行する計測ハーネス。

llama-split-bench (kuraneko1) は llama.cpp の llama-server を自前で起動し、
/completion の `timings` を読む。vLLM はその両方を満たさない（サーバは常駐、
timings 無し）ため、本スクリプトは同じ測定内容を vLLM の API で再現する:

  1. 深度ラダー（コンテキスト再利用）     -> results-<mode>.json
  2. 深さ0の prefill（新規プロンプト）    -> results-<mode>-pp0.json
  3. 投機デコード(MTP)採択率              -> 上記に内包（/metrics 差分から算出）
  4. 実プロンプト補正係数                 -> results-real.json
  5. 実行証跡                             -> run-info.json / argv-<mode>.txt

llama.cpp の timings への対応:
  prompt_per_second    = (今回新規に評価されたプロンプトトークン) / TTFT
  predicted_per_second = completion_tokens / (総時間 - TTFT)
  cache_n              = /metrics の prefix_cache_hits_total 差分
  draft_n / accepted   = /metrics の spec_decode_* 差分

出力 JSON は plot_bench.py がそのまま読める形式。
"""
import argparse
import hashlib
import json
import os
import random
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
import datetime

TAIL = ("\n\nContinue the sequence with the next 100 numbered lines, in exactly "
        "the same style. Do not stop and do not summarize.")
STAGE0_PROMPT = "The capital of France is and the capital of Germany is"

REAL_PROMPTS = [
    ("design", "次の設計判断を整理して: 単一のV100 32GBで262kコンテキストの推論を回すとき、"
               "KVキャッシュの型・重みの量子化・投機デコードの3つは互いにどう影響し合うか。"
               "トレードオフを表にまとめ、優先順位と根拠を示して。"),
    ("review", "長文の技術文書をレビューする立場で、次の観点を順に検討して: 主張の根拠が測定に基づいているか、"
               "見落とされている交絡因子はないか、結論を出す前に必要な追加検証は何か。"
               "それぞれ具体的な反例を挙げて説明して。"),
    ("qa",     "以下を自分の言葉で説明して: なぜGPUのGEMVは帯域律速になるのか、"
               "なぜ量子化ブロックのメモリ配置が実効帯域を変えるのか、"
               "そして帯域を測る際に論理バイト数と実DRAM転送量がずれるのはどんな時か。"),
]

METRIC_KEYS = ("vllm:prefix_cache_hits_total", "vllm:prefix_cache_queries_total",
               "vllm:spec_decode_num_draft_tokens_total",
               "vllm:spec_decode_num_accepted_tokens_total",
               "vllm:num_requests_running", "vllm:num_requests_waiting",
               "vllm:kv_cache_usage_perc")


def fill_text(n_chars):
    unit = "Sequence {i}: the quick brown fox jumps over the lazy dog while we measure context tokens. "
    parts, total, i = [], 0, 1
    while total < n_chars:
        p = unit.format(i=i)
        parts.append(p)
        total += len(p)
        i += 1
    return "".join(parts)[:n_chars]


class Server:
    def __init__(self, url, model):
        self.url = url.rstrip("/")
        self.model = model

    def _post(self, path, body, timeout=3600):
        req = urllib.request.Request(self.url + path, data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())

    def n_tokens(self, text):
        return self._post("/tokenize", {"model": self.model, "prompt": text}, timeout=300)["count"]

    def metrics(self):
        with urllib.request.urlopen(self.url + "/metrics", timeout=60) as r:
            body = r.read().decode()
        out = {}
        for line in body.splitlines():
            if line.startswith("#"):
                continue
            m = re.match(r'^([a-zA-Z_:][^\s{]*)(\{[^}]*\})?\s+([-+0-9.eE]+)$', line)
            if not m:
                continue
            name, val = m.group(1), m.group(3)
            if name in METRIC_KEYS:
                try:
                    out[name] = out.get(name, 0.0) + float(val)
                except ValueError:
                    pass
        return out

    def complete(self, prompt, max_tokens, temperature=0.0, top_p=None,
                 ignore_eos=True, cache_salt=None, timeout=3600):
        """Streaming completion. Returns ttft / total / usage measured client-side."""
        body = {"model": self.model, "prompt": prompt, "max_tokens": max_tokens,
                "temperature": temperature, "stream": True,
                "stream_options": {"include_usage": True}}
        if ignore_eos:
            body["ignore_eos"] = True
        if top_p is not None:
            body["top_p"] = top_p
        if cache_salt:
            body["cache_salt"] = cache_salt
        req = urllib.request.Request(self.url + "/v1/completions", data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
        t0 = time.perf_counter()
        t_first = None
        usage = None
        text_parts = []
        finish = None
        with urllib.request.urlopen(req, timeout=timeout) as r:
            for raw in r:
                line = raw.decode("utf-8", "replace").strip()
                if not line.startswith("data: "):
                    continue
                payload = line[6:]
                if payload == "[DONE]":
                    break
                obj = json.loads(payload)
                if obj.get("usage"):
                    usage = obj["usage"]
                ch = obj.get("choices") or []
                if ch:
                    if ch[0].get("text"):
                        if t_first is None:
                            t_first = time.perf_counter()
                        text_parts.append(ch[0]["text"])
                    if ch[0].get("finish_reason"):
                        finish = ch[0]["finish_reason"]
        total = time.perf_counter() - t0
        if usage is None or t_first is None:
            raise RuntimeError(f"no usable timing data (usage={usage}, first_token={t_first})")
        return {"ttft": t_first - t0, "total": total, "usage": usage,
                "text": "".join(text_parts), "finish_reason": finish}


def sized_prompt(srv, target_tokens, ratio, cache=None):
    """Build a prompt of ~target_tokens tokens (filler + TAIL), refining the
    chars-per-token ratio with the server's own tokenizer."""
    if target_tokens in (cache or {}):
        return cache[target_tokens]
    tail_n = srv.n_tokens(TAIL)
    body_target = max(1, target_tokens - tail_n)
    chars = int(body_target * ratio)
    for _ in range(6):
        body = fill_text(chars)
        n = srv.n_tokens(body)
        if abs(n - body_target) <= max(4, int(body_target * 0.002)):
            break
        chars = max(1, int(chars * body_target / max(1, n)))
    prompt = body + TAIL
    got = srv.n_tokens(prompt)
    new_ratio = len(body) / max(1, n)
    if cache is not None:
        cache[target_tokens] = (prompt, got, new_ratio)
    return prompt, got, new_ratio


def gpu_state(idx):
    if not idx:
        return None
    q = ("nvidia-smi --query-gpu=index,memory.used,utilization.gpu,temperature.gpu,"
         "power.draw,clocks.sm --format=csv,noheader,nounits")
    try:
        out = subprocess.run(q, shell=True, capture_output=True, text=True, timeout=30).stdout
    except Exception:
        return None
    rows = {}
    for line in out.strip().splitlines():
        f = [x.strip() for x in line.split(",")]
        if len(f) >= 6 and f[0] in idx:
            rows[f[0]] = {"mem_used_mib": f[1], "util_pct": f[2], "temp_c": f[3],
                          "power_w": f[4], "sm_mhz": f[5]}
    return rows


def delta(a, b, key):
    va, vb = a.get(key), b.get(key)
    if va is None or vb is None:
        return None
    return vb - va


def run_ladder(srv, args, outdir, guard_idx):
    stages = [int(x) for x in args.stages.split(",")]
    results_path = os.path.join(outdir, f"results-{args.mode}.json")
    records = []
    ratio = args.ratio_init
    prev_depth = 0
    pcache = {}
    for k, target in enumerate(stages):
        m0 = srv.metrics()
        running = m0.get("vllm:num_requests_running", 0)
        if running > 0:
            print(f"stage {target}: WARNING {running:.0f} other request(s) already running "
                  f"on the shared server - measurement may be contended", flush=True)
        if target == 0:
            prompt, want, _ = STAGE0_PROMPT, srv.n_tokens(STAGE0_PROMPT), ratio
        else:
            prompt, want, ratio = sized_prompt(srv, target, ratio, pcache)
        before = gpu_state(guard_idx)
        t0 = time.time()
        try:
            r = srv.complete(prompt, args.n_predict, temperature=0.0, ignore_eos=True,
                             cache_salt=args.cache_salt or None)
        except urllib.error.HTTPError as e:
            body = e.read()[:300].decode(errors="replace")
            print(f"stage {target}: HTTP {e.code} ({body}) - retrying at 96% fill", flush=True)
            try:
                prompt, want, ratio = sized_prompt(srv, int(target * 0.96), ratio, pcache)
                r = srv.complete(prompt, args.n_predict, temperature=0.0, ignore_eos=True,
                                 cache_salt=args.cache_salt or None)
            except Exception as e2:
                records.append({"aborted": f"stage {target}: {e2}"})
                json.dump(records, open(results_path, "w"), indent=2)
                return records, f"stage {target}: {e2}"
        except Exception as e:
            records.append({"aborted": f"stage {target}: {e}"})
            json.dump(records, open(results_path, "w"), indent=2)
            return records, f"stage {target}: {e}"
        wall = time.time() - t0
        after = gpu_state(guard_idx)
        m1 = srv.metrics()

        u = r["usage"]
        total_prompt = u["prompt_tokens"]
        cache_hits = delta(m0, m1, "vllm:prefix_cache_hits_total")
        cache_n = int(cache_hits) if cache_hits is not None else None
        prompt_n = total_prompt - cache_n if cache_n is not None else total_prompt
        if prompt_n <= 0:
            prompt_n = total_prompt
            cache_n = 0
        pred_n = u["completion_tokens"]
        gen_s = r["total"] - r["ttft"]
        draft_n = delta(m0, m1, "vllm:spec_decode_num_draft_tokens_total")
        acc = delta(m0, m1, "vllm:spec_decode_num_accepted_tokens_total")
        rec = {
            "stage": k,
            "target_tokens": target,
            "shrunk": False,
            "prompt_chars": len(prompt),
            "tokens_evaluated": total_prompt,
            "cache_n": cache_n,
            "prompt_n": prompt_n,
            "effective_depth": total_prompt,
            "prompt_ms": round(r["ttft"] * 1000.0, 3),
            "prompt_per_second": round(prompt_n / r["ttft"], 3) if r["ttft"] > 0 else None,
            "predicted_n": pred_n,
            "predicted_ms": round(gen_s * 1000.0, 3),
            "predicted_per_second": round(pred_n / gen_s, 3) if gen_s > 0 else None,
            "draft_n": int(draft_n) if draft_n is not None else 0,
            "draft_n_accepted": int(acc) if acc is not None else 0,
            "draft_accept_rate": round(acc / draft_n, 3) if draft_n else None,
            "wall_s": round(wall, 1),
            "finish_reason": r["finish_reason"],
            "target_tokens_requested": want,
            "kv_cache_usage_perc_after": m1.get("vllm:kv_cache_usage_perc"),
            "other_requests_running_before": running,
            "gpu_before": before,
            "gpu_after": after,
        }
        records.append(rec)
        json.dump(records, open(results_path, "w"), indent=2)
        print(json.dumps({kk: rec[kk] for kk in
                          ("stage", "target_tokens", "effective_depth", "cache_n", "prompt_n",
                           "prompt_per_second", "predicted_n", "predicted_per_second",
                           "draft_accept_rate", "wall_s")}, ensure_ascii=False), flush=True)
        prev_depth = total_prompt
    return records, None


def run_pp0(srv, args, outdir):
    out = {"tag": args.mode}
    salt_base = "vsb-%d-%d" % (int(time.time()), random.randrange(10 ** 6))
    ratio = args.ratio_init
    pcache = {}
    srv.complete("warmup", 8, temperature=0.0, ignore_eos=False,
                 cache_salt=salt_base + "-warm")
    for size in [int(x) for x in args.pp0_sizes.split(",")]:
        prompt, want, ratio = sized_prompt(srv, size, ratio, pcache)
        m0 = srv.metrics()
        r = srv.complete(prompt, 64, temperature=0.0, ignore_eos=True,
                         cache_salt=f"{salt_base}-pp{size}")
        m1 = srv.metrics()
        u = r["usage"]
        hits = delta(m0, m1, "vllm:prefix_cache_hits_total")
        gen_s = r["total"] - r["ttft"]
        out[f"pp{size}"] = {
            "prompt_n": u["prompt_tokens"],
            "cache_n": int(hits) if hits is not None else None,
            "prompt_ms": round(r["ttft"] * 1000.0, 3),
            "prompt_per_second": round(u["prompt_tokens"] / r["ttft"], 3),
            "predicted_n": u["completion_tokens"],
            "predicted_per_second": round(u["completion_tokens"] / gen_s, 3) if gen_s > 0 else None,
            "wall_s": round(r["total"], 2),
        }
        print(f"{args.mode} pp{size}: prompt_n={u['prompt_tokens']} cache_n={out[f'pp{size}']['cache_n']} "
              f"prefill={out[f'pp{size}']['prompt_per_second']:.1f} t/s", flush=True)
    path = os.path.join(outdir, f"results-{args.mode}-pp0.json")
    json.dump(out, open(path, "w"), indent=2)
    print(f"wrote {path}", flush=True)


def run_real(srv, args, outdir):
    salt_base = "vsb-real-%d" % int(time.time())
    srv.complete("warmup", 8, temperature=0.0, ignore_eos=False, cache_salt=salt_base + "-warm")
    records = []
    for name, prompt in REAL_PROMPTS:
        m0 = srv.metrics()
        r = srv.complete(prompt, 1200, temperature=0.7, top_p=0.9, ignore_eos=False,
                         cache_salt=f"{salt_base}-{name}")
        m1 = srv.metrics()
        u = r["usage"]
        gen_s = r["total"] - r["ttft"]
        dn = delta(m0, m1, "vllm:spec_decode_num_draft_tokens_total") or 0
        acc = delta(m0, m1, "vllm:spec_decode_num_accepted_tokens_total") or 0
        rec = {
            "prompt": name,
            "prompt_chars": len(prompt),
            "n_predict": 1200, "temperature": 0.7, "top_p": 0.9,
            "ttft_ms": round(r["ttft"] * 1000.0, 1),
            "prompt_n": u["prompt_tokens"],
            "prefill_tok_s": round(u["prompt_tokens"] / r["ttft"], 3),
            "predicted_n": u["completion_tokens"],
            "decode_tok_s": round(u["completion_tokens"] / gen_s, 3) if gen_s > 0 else None,
            "draft_n": int(dn), "accepted": int(acc),
            "accept_rate": round(acc / dn, 3) if dn else None,
            "tokens_per_cycle": round(u["completion_tokens"] / dn, 3) if dn else None,
            "wall_s": round(r["total"], 1),
            "finish_reason": r["finish_reason"],
            "text_sha256": hashlib.sha256(r["text"].encode()).hexdigest(),
        }
        open(os.path.join(outdir, f"real-response-{name}.txt"), "w").write(r["text"])
        records.append(rec)
        print(json.dumps({k: rec[k] for k in
                          ("prompt", "prompt_n", "prefill_tok_s", "predicted_n",
                           "decode_tok_s", "accept_rate")}, ensure_ascii=False), flush=True)
    json.dump(records, open(os.path.join(outdir, "results-real.json"), "w"),
              indent=2, ensure_ascii=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--url", default="http://127.0.0.1:18024")
    ap.add_argument("--model", required=True)
    ap.add_argument("--mode", default="tensor", help="series name used in results-<mode>.json")
    ap.add_argument("--devices", default="", help="label only, e.g. CUDA1,CUDA2")
    ap.add_argument("--split", default="tensor")
    ap.add_argument("--guard-devices", default="", help="nvidia-smi indices to sample, e.g. 1,2")
    ap.add_argument("--ctx", type=int, default=262144)
    ap.add_argument("--stages", default="0,32000,64000,128000,196000,258000")
    ap.add_argument("--n-predict", type=int, default=1000)
    ap.add_argument("--pp0-sizes", default="512,2048,8192")
    ap.add_argument("--ratio-init", type=float, default=4.3)
    ap.add_argument("--machine", default="")
    ap.add_argument("--runs-dir", default="runs")
    ap.add_argument("--no-real", action="store_true")
    # The ladder deliberately reuses each stage's prefix in the next one, so the
    # salt is constant within a run -- it only isolates one run from the next,
    # which is what makes a repeat a cold measurement instead of a cache hit.
    ap.add_argument("--cache-salt", default="",
                    help='vLLM cache_salt for the ladder; "auto" generates a per-run one')
    args = ap.parse_args()

    if args.cache_salt == "auto":
        args.cache_salt = "vsb-ladder-%d-%d" % (int(time.time()), random.randrange(10 ** 6))
    outdir = os.path.join(args.runs_dir, args.tag)
    if os.path.exists(os.path.join(outdir, f"results-{args.mode}.json")):
        print(f"BENCH-ABORT: {outdir}/results-{args.mode}.json already exists - use a new tag")
        sys.exit(1)
    os.makedirs(outdir, exist_ok=True)
    guard_idx = [x.strip() for x in args.guard_devices.split(",") if x.strip()]
    srv = Server(args.url, args.model)

    probe = srv.complete("ping", 4, temperature=0.0, ignore_eos=False)
    try:
        fingerprint = srv._post("/v1/completions", {"model": args.model, "prompt": "ping",
                                                    "max_tokens": 1, "temperature": 0},
                                timeout=120).get("system_fingerprint", "")
    except Exception:
        fingerprint = ""
    try:
        with urllib.request.urlopen(args.url.rstrip("/") + "/version", timeout=30) as r:
            ver = json.loads(r.read().decode()).get("version", "")
    except Exception:
        ver = ""
    argv = ""
    for pid in os.listdir("/proc"):
        if not pid.isdigit():
            continue
        try:
            c = open(f"/proc/{pid}/cmdline", "rb").read().replace(b"\0", b" ").decode()
        except OSError:
            continue
        if "vllm" in c and " serve " in c:
            argv = c.strip()
            break
    open(os.path.join(outdir, f"argv-{args.mode}.txt"), "w").write(argv + "\n")

    print(f"server ok (vllm {ver}), tag={args.tag}, mode={args.mode}", flush=True)
    err = None
    records, err = run_ladder(srv, args, outdir, guard_idx)
    if err:
        print(f"BENCH-ABORT: {err}")
        sys.exit(1)
    run_pp0(srv, args, outdir)
    if not args.no_real:
        run_real(srv, args, outdir)

    deepest = max((r.get("effective_depth") or 0) for r in records)
    info = {
        "tag": args.tag,
        "date": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "ctx": args.ctx, "stages": args.stages, "n_predict": args.n_predict,
        "modes": [{"name": args.mode, "device": args.devices, "split": args.split,
                   "argv_file": f"argv-{args.mode}.txt"}],
        "machine": args.machine,
        "bin": "vllm serve (already-running server)",
        "bin_version": f"vllm {ver}",
        "bin_sha256": "",
        "server_fingerprint": fingerprint,
        "cache_k": "auto", "cache_v": "auto",
        "launch_prefix": "", "tensor_split": "",
        "engine_label": (f"vLLM {ver}" if ver else "vLLM") + " (TP=2, expert-parallel, MTP n=4)",
        "harness": "vllm-split-bench.py (llama-split-bench protocol over the vLLM OpenAI API)",
        "deepest_measured": deepest,
    }
    json.dump(info, open(os.path.join(outdir, "run-info.json"), "w"),
              ensure_ascii=False, indent=2)
    print("run-info.json written", flush=True)
    print(f"BENCH-DONE {args.tag} {datetime.datetime.now().strftime('%H:%M:%S')}", flush=True)


if __name__ == "__main__":
    main()
