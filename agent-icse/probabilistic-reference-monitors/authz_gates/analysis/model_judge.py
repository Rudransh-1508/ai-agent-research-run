#!/usr/bin/env python3
"""Score the corpus with a second model family as a safety judge, for the certified-threshold
recipe. Talks to an OpenAI-compatible chat endpoint (default: Mistral's official API) and
emits a benchmark-results JSONL (p_safe per definite-label item) that
analysis/threshold_recipe.py consumes. The question is whether the recipe produces a valid
false-allow bound on a model unrelated to the vendor's (jev/TypeSafe). Stdlib only.

  MISTRAL_API_KEY=... python3 analysis/model_judge.py --provider mistral \
      --model mistral-small-latest --out artifact/judge_mistral.jsonl
"""
import argparse
import json
import os
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
BENCH = os.path.join(HERE, "..", "benchmark")
import sys  # noqa: E402
sys.path.insert(0, HERE)
from ollama_judge import SYS, action_text  # reuse the identical safety prompt + renderer

PROVIDERS = {
    "mistral": {"base": "https://api.mistral.ai/v1", "key_env": "MISTRAL_API_KEY"},
    "openai": {"base": "https://api.openai.com/v1", "key_env": "OPENAI_API_KEY"},
}


def ask(base, key, model, text, timeout_s=60):
    body = json.dumps({
        "model": model, "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [{"role": "system", "content": SYS},
                     {"role": "user", "content": "Proposed action:\n" + text}],
    }).encode()
    req = urllib.request.Request(base + "/chat/completions", data=body, headers={
        "Content-Type": "application/json", "Authorization": "Bearer " + key})
    with urllib.request.urlopen(req, timeout=timeout_s) as r:
        out = json.loads(r.read())
    content = out["choices"][0]["message"]["content"]
    try:
        p = float(json.loads(content).get("p_safe"))
    except Exception:
        return None
    return max(0.0, min(1.0, p))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--provider", default="mistral", choices=sorted(PROVIDERS))
    ap.add_argument("--model", default="mistral-small-latest")
    ap.add_argument("--corpus", default=os.path.join(BENCH, "corpus.jsonl"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-retries", type=int, default=4)
    args = ap.parse_args()

    prov = PROVIDERS[args.provider]
    key = os.environ.get(prov["key_env"], "")
    if not key:
        raise SystemExit(f"set {prov['key_env']}")

    items = [json.loads(l) for l in open(args.corpus)]
    items = [i for i in items if i["label"] in ("safe", "destructive") and not i["disputable"]]
    done = 0
    with open(args.out, "w") as f:
        for it in items:
            p, err = None, None
            for attempt in range(args.max_retries):
                try:
                    p = ask(prov["base"], key, args.model, action_text(it))
                    break
                except Exception as e:
                    err = str(e)[:80]
                    time.sleep(2 ** attempt)  # backoff on 429/5xx
            row = {"item_id": it["id"], "label": it["label"], "tier": it["tier"],
                   "correct_action": it["correct_action"], "disputable": it["disputable"],
                   "model": f"{args.provider}:{args.model}", "p_safe": p,
                   "outcome": "ok" if p is not None else "malformed", "error": err}
            f.write(json.dumps(row) + "\n")
            f.flush()
            done += 1
            if done % 20 == 0:
                print(f"{done}/{len(items)}", flush=True)
    print(f"DONE {done}/{len(items)}")


if __name__ == "__main__":
    main()
