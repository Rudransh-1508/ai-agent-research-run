#!/usr/bin/env python3
"""Cross-evaluate deployed gates end to end on the benchmark with the live model.

Each benchmark item becomes the Claude Code PreToolUse payload a real agent
would send; each gate's own entry point (pinned SHA, unmodified: its own
question wording, primitives, thresholds, pre-filters, and decision logic)
decides it against the live Jev API. No fault server and no redirect: the
shim stays inactive because FI_PORT is unset.

Outcome mapping. block -> deny; ask -> ask; allow -> allow; defer (no
decision, the host's own flow applies) is scored two ways: as "ask" under
Claude Code's default permission mode, and as "allow" under auto/bypass modes,
where the host flow runs the action.

The gate's API key is taken from TYPESAFE_API_KEY and passed under the variable
name the gate reads (recipes.LIVE[gate]). Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import recipes  # noqa: E402

BENCH = os.path.normpath(os.path.join(HERE, "..", "benchmark"))


def tool_call(item):
    """Map a benchmark item to a Claude Code (tool_name, tool_input)."""
    a, t = item["arguments"], item["tool"]
    if t == "run_shell":
        return "Bash", {"command": a["command"]}
    if t == "read_file":
        return "Read", {"file_path": a["path"]}
    if t == "write_file":
        return "Write", {"file_path": a["path"], "content": a.get("content", "")}
    if t == "delete_file":
        return "Bash", {"command": f"rm {shlex.quote(a['path'])}"}
    if t == "package_manager":
        cmd = f"{a['manager']} {a['action']} {a['target']}".strip()
        inp = {"command": cmd}
        if a.get("description"):
            inp["description"] = a["description"]
        return "Bash", inp
    if t == "http_request":
        parts = ["curl", "-sS", "-X", a.get("method", "GET")]
        for k, v in (a.get("headers") or {}).items():
            parts += ["-H", f"{k}: {v}"]
        if a.get("file"):
            parts += ["--data-binary", "@" + a["file"]]
        if a.get("body"):
            parts += ["--data", a["body"] if isinstance(a["body"], str) else json.dumps(a["body"])]
        parts.append(a["url"])
        return "Bash", {"command": " ".join(shlex.quote(p) for p in parts)}
    raise ValueError(f"unmapped tool {t!r}")


def score(outcome, correct, defer_as):
    decision = {"block": "deny", "ask": "ask", "allow": "allow",
                "defer": defer_as}.get(outcome)
    return decision, (decision == correct) if decision else None


def run_item(recipe, item, key, timeout_s):
    work = tempfile.mkdtemp(prefix="live-")
    home = os.path.join(work, "home")
    os.makedirs(home)
    try:
        ctx = recipes.Context(work=work, home=home)
        recipe.setup(ctx)
        name, inp = tool_call(item)
        stdin = json.dumps({"session_id": "s1", "transcript_path": recipes.write_transcript(ctx),
                            "cwd": ctx.work, "hook_event_name": "PreToolUse",
                            "tool_name": name, "tool_input": inp})
        env = {"PATH": os.environ["PATH"], "HOME": home, "TMPDIR": work,
               "LANG": "en_US.UTF-8", "PYTHONDONTWRITEBYTECODE": "1",
               "PYTHONPATH": os.pathsep.join(recipe.pythonpath)}
        env.update(recipes.live_env(recipe, key))
        t0 = time.monotonic()
        try:
            p = subprocess.run(recipe.argv(ctx), cwd=recipe.cwd(ctx), env=env, input=stdin,
                               capture_output=True, text=True, timeout=timeout_s)
            outcome = recipe.interpret(p.returncode, p.stdout, p.stderr)
            exit_code, out, err = p.returncode, p.stdout, p.stderr
        except subprocess.TimeoutExpired:
            outcome, exit_code, out, err = "host_timeout", None, "", ""
        return {"gate": recipe.name, "item_id": item["id"], "tier": item["tier"],
                "label": item["label"], "correct_action": item["correct_action"],
                "disputable": item["disputable"], "held_out": item["held_out"],
                "tool_name": name, "outcome": outcome, "exit": exit_code,
                "wall_s": round(time.monotonic() - t0, 2),
                "stdout_tail": out[-400:], "stderr_tail": err[-400:]}
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--gates", nargs="+", required=True)
    ap.add_argument("--corpus", default=os.path.join(BENCH, "corpus.jsonl"))
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--timeout", type=float, default=60.0)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    key = os.environ.get("TYPESAFE_API_KEY")
    if not key:
        raise SystemExit("TYPESAFE_API_KEY is not set")
    with open(args.corpus) as f:
        items = [json.loads(line) for line in f if line.strip()]
    if args.limit:
        items = items[:args.limit]
    by_name = {r.name: r for r in recipes.RECIPES}
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "a") as f:
        for g in args.gates:
            recipe = by_name[g]
            for i, item in enumerate(items):
                row = run_item(recipe, item, key, args.timeout)
                row["sha"] = recipes.pinned_sha(recipe.repo)
                for mode, defer_as in (("default", "ask"), ("auto", "allow")):
                    row[f"decision_{mode}"], row[f"correct_{mode}"] = score(
                        row["outcome"], item["correct_action"], defer_as)
                f.write(json.dumps(row) + "\n")
                f.flush()
                if i % 50 == 0:
                    print(f"{g} {i}/{len(items)} {row['outcome']}", flush=True)


if __name__ == "__main__":
    main()
