#!/usr/bin/env python3
"""補足計測: 合成ラダーと同じ深さで、生成内容だけを「実運用相当」に替えて decode を測る。
ラダーの TAIL（数列の続きを書け）は MTP 採択率が 0.93 まで上がり decode が楽観側に出る。
同じ前置き（キャッシュ済みの filler）に別の指示を付けて temp 0.7 で生成し、
深さの効果と採択率の効果を分離する。"""
import json, sys, importlib.util, statistics as st
spec = importlib.util.spec_from_file_location("vsb", "vllm-split-bench.py")
vsb = importlib.util.module_from_spec(spec); spec.loader.exec_module(vsb)

srv = vsb.Server("http://127.0.0.1:18024", "flash-next-w4a16")
TAIL2 = ("\n\n上の数列は完全に無視してください。まったく別の話題として、GPU の HBM 帯域幅と "
         "4bit 量子化が推論のスループットに与える影響について、あなた自身の言葉で、"
         "具体例を挙げながら詳しく論じてください。箇条書きではなく文章で書いてください。")
out = []
ratio = 4.3; pcache = {}
for target in [0, 32000, 128000, 258000]:
    if target == 0:
        prompt = TAIL2.strip()
    else:
        body, _, ratio = vsb.sized_prompt(srv, target, ratio, pcache)
        prompt = body[:-len(vsb.TAIL)] + TAIL2
    m0 = srv.metrics()
    r = srv.complete(prompt, 1000, temperature=0.7, top_p=0.9, ignore_eos=True)
    m1 = srv.metrics()
    u = r["usage"]; gen = r["total"] - r["ttft"]
    hits = vsb.delta(m0, m1, "vllm:prefix_cache_hits_total") or 0
    dn = vsb.delta(m0, m1, "vllm:spec_decode_num_draft_tokens_total") or 0
    acc = vsb.delta(m0, m1, "vllm:spec_decode_num_accepted_tokens_total") or 0
    rec = {"target_tokens": target, "effective_depth": u["prompt_tokens"],
           "cache_n": int(hits), "prompt_n": u["prompt_tokens"] - int(hits),
           "prompt_ms": round(r["ttft"]*1000, 1),
           "prompt_per_second": round((u["prompt_tokens"]-int(hits))/r["ttft"], 2) if r["ttft"]>0 else None,
           "predicted_n": u["completion_tokens"],
           "predicted_per_second": round(u["completion_tokens"]/gen, 2),
           "draft_n": int(dn), "draft_n_accepted": int(acc),
           "draft_accept_rate": round(acc/dn, 3) if dn else None,
           "temperature": 0.7, "top_p": 0.9, "wall_s": round(r["total"], 1)}
    out.append(rec); print(json.dumps(rec, ensure_ascii=False), flush=True)
# Output path comes from argv so a re-measurement writes next to its own run
# instead of overwriting the tag this script was first written for.
dest = sys.argv[1] if len(sys.argv) > 1 else "runs/tp2-170hx-262k/results-real-depth.json"
json.dump(out, open(dest, "w"), indent=2, ensure_ascii=False)
print(f"wrote {dest}")
