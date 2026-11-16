#!/usr/bin/env python3
"""Score the corpus with a second model family as a safety judge, for the certified-threshold
recipe. Talks to an OpenAI-compatible chat endpoint (default: Groq) and emits a
benchmark-results JSONL (p_safe per definite-label item) that analysis/threshold_recipe.py
consumes. The question is whether the recipe produces a valid false-allow bound on a model
unrelated to the vendor's (jev/TypeSafe). Stdlib only.

The key variable may hold several comma-separated keys (e.g. GROQ_API_KEYS=k1,k2,k3 in
~/.env). Requests rotate across them, and a key that gets rate-limited is rested until its
Retry-After passes while the others carry on.

  set -a; source ~/.env; set +a
  python3 analysis/model_judge.py --provider groq --model openai/gpt-oss-120b \
      --out artifact/judge_groq.jsonl
"""
import argparse
import json
import os
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
BENCH = os.path.join(HERE, "..", "benchmark")
import sys  # noqa: E402
sys.path.insert(0, HERE)
from ollama_judge import SYS, action_text  # reuse the identical safety prompt + renderer
sys.path.insert(0, os.path.join(HERE, "..", "faultinject"))
from run_gates_live import tool_call  # noqa: E402  the harness's item -> hook tool call


def render(it, mode):
    """Text the judge sees. "action": the benchmark's own rendering. "hook": what the design
    gate sends for this item once the harness turns it into a Claude Code tool call - only
    Bash calls reach the gate's model, so other items return None (not scored)."""
    if mode == "action":
        return action_text(it)
    tool, inp = tool_call(it)
    if tool != "Bash":
        return None
    return action_text({"arguments": {"command": inp["command"]}})

PROVIDERS = {
    "groq": {"base": "https://api.groq.com/openai/v1", "key_env": ("GROQ_API_KEYS", "GROQ_API_KEY")},
    "openai": {"base": "https://api.openai.com/v1", "key_env": ("OPENAI_API_KEY",)},
}


def parse_keys(raw):
    """Comma-separated key list -> unique non-empty keys, order kept."""
    keys = []
    for k in (raw or "").split(","):
        k = k.strip().strip('"').strip("'")
        if k and k not in keys:
            keys.append(k)
    return keys


class KeyPool:
    """Round-robin over keys; a rate-limited key rests until its cooldown ends."""

    def __init__(self, keys, clock=time.monotonic, sleep=time.sleep):
        if not keys:
            raise ValueError("no API keys")
        self.keys = list(keys)
        self.ready_at = [0.0] * len(keys)
        self.i = 0
        self.clock, self.sleep = clock, sleep

    def take(self):
        """Index of the next usable key, waiting if every key is resting."""
        n = len(self.keys)
        now = self.clock()
        for step in range(n):
            j = (self.i + step) % n
            if self.ready_at[j] <= now:
                self.i = (j + 1) % n
                return j
        j = min(range(n), key=lambda k: self.ready_at[k])
        if self.ready_at[j] == float("inf"):
            raise SystemExit("every API key was rejected (401/403)")
        self.sleep(self.ready_at[j] - now)
        self.i = (j + 1) % n
        return j

    def rest(self, j, seconds):
        self.ready_at[j] = self.clock() + max(seconds, 1.0)

    def drop(self, j):
        self.ready_at[j] = float("inf")


def retry_after(err, default):
    try:
        return float(err.headers.get("retry-after"))
    except (TypeError, ValueError, AttributeError):
        return default


def ask(base, key, model, text, timeout_s=60, max_tokens=None):
    req_body = {
        "model": model, "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [{"role": "system", "content": SYS},
                     {"role": "user", "content": "Proposed action:\n" + text}],
    }
    if max_tokens:
        req_body["max_tokens"] = max_tokens  # Groq counts this budget against the TPM cap
    body = json.dumps(req_body).encode()
    # Groq's Cloudflare front rejects urllib's default User-Agent with 403 "error code: 1010".
    req = urllib.request.Request(base + "/chat/completions", data=body, headers={
        "Content-Type": "application/json", "Authorization": "Bearer " + key,
        "User-Agent": "authz-gates-judge/1.0"})
    with urllib.request.urlopen(req, timeout=timeout_s) as r:
        out = json.loads(r.read())
    content = out["choices"][0]["message"]["content"]
    try:
        p = float(json.loads(content).get("p_safe"))
    except Exception:
        return None
    return max(0.0, min(1.0, p))


def score_item(pool, base, args, it, text):
    """One item -> one result row. Rate limits (429) rest the key and do not spend the
    retry budget, which is for real errors; a sustained 429 storm still ends."""
    p, err, attempt, limited = None, None, 0, 0
    while attempt < args.max_retries and limited < 200:
        j = pool.take()
        try:
            p = ask(base, pool.keys[j], args.model, text, max_tokens=args.max_tokens)
            err = None
            break
        except urllib.error.HTTPError as e:
            detail = e.read()[:120].decode("utf-8", "replace").strip()
            err = f"HTTP {e.code} key#{j}: {detail}"
            if e.code == 429:
                limited += 1
                pool.rest(j, retry_after(e, 2 ** min(limited, 6)))  # other keys keep going
                continue
            attempt += 1
            if e.code == 413:
                pool.rest(j, 60)  # over this key's tokens-per-minute cap; try another key
            elif e.code in (401, 403):
                print(f"dropping key#{j}: {err}", flush=True)
                pool.drop(j)  # bad/revoked key: out for the rest of the run
            elif e.code == 400 and "validate JSON" in detail:
                continue  # Groq rejected one sampled generation; a fresh one may pass
            elif 400 <= e.code < 500:
                break  # bad request/model: retrying cannot help
            else:
                time.sleep(2 ** attempt)
        except Exception as e:
            attempt += 1
            err = str(e)[:80]
            time.sleep(2 ** attempt)
    return {"item_id": it["id"], "label": it["label"], "tier": it["tier"],
            "correct_action": it["correct_action"], "disputable": it["disputable"],
            "model": f"{args.provider}:{args.model}", "render": args.render, "p_safe": p,
            "outcome": "ok" if p is not None else "malformed", "error": err}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--provider", default="groq", choices=sorted(PROVIDERS))
    ap.add_argument("--model", default="openai/gpt-oss-120b")
    ap.add_argument("--corpus", default=os.path.join(BENCH, "corpus.jsonl"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-retries", type=int, default=6)
    ap.add_argument("--render", default="action", choices=("action", "hook"),
                    help="hook = certify on exactly what design/gate.py sends the model")
    ap.add_argument("--max-tokens", type=int, default=None,
                    help="completion budget; set it where a model's per-key TPM cap is small")
    ap.add_argument("--resume", action="store_true",
                    help="keep rows already scored ok in --out; re-ask only failed/missing items")
    args = ap.parse_args()

    prov = PROVIDERS[args.provider]
    keys = []
    for env in prov["key_env"]:
        keys += [k for k in parse_keys(os.environ.get(env)) if k not in keys]
    if not keys:
        raise SystemExit(f"set {' or '.join(prov['key_env'])} (comma-separated keys allowed)")
    pool = KeyPool(keys)
    print(f"{len(keys)} key(s) for {args.provider}", flush=True)

    items = [json.loads(l) for l in open(args.corpus)]
    items = [i for i in items if i["label"] in ("safe", "destructive") and not i["disputable"]]
    items = [(i, render(i, args.render)) for i in items]
    items = [(i, t) for i, t in items if t is not None]
    # --resume keeps every row already scored ok in --out and re-asks only the rest.
    kept = {}
    if args.resume and os.path.exists(args.out):
        for l in open(args.out):
            r = json.loads(l)
            same_run = (r.get("model") == f"{args.provider}:{args.model}"
                        and r.get("render", "action") == args.render)
            if r.get("outcome") == "ok" and same_run:
                kept[r["item_id"]] = r
    done = 0
    with open(args.out, "w") as f:
        for it, text in items:
            row = kept.get(it["id"]) or score_item(pool, prov["base"], args, it, text)
            f.write(json.dumps(row) + "\n")
            f.flush()
            done += 1
            if done % 20 == 0:
                print(f"{done}/{len(items)}", flush=True)
    print(f"DONE {done}/{len(items)}")


if __name__ == "__main__":
    main()
