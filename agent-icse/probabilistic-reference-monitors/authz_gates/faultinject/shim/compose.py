#!/usr/bin/env python3
"""Run a gate that ships as a chain of hooks, the way Claude Code would.

COMPOSE_SPEC (JSON) maps a tool name to its hook chain:
    {"Bash": {"PreToolUse": [[argv...], ...], "PermissionRequest": [[argv...], ...]}}

Claude Code semantics, as documented in the hooks reference:
  * PreToolUse hooks run first. A block (exit 2 or "deny") blocks the call; an "ask"
    forces a prompt; an "allow" skips the prompt. Any other non-zero exit is a
    non-blocking error and the call continues.
  * If nothing blocked or allowed, the call would reach the permission prompt, and the
    PermissionRequest hooks run there: "deny" refuses, "allow" approves without a prompt,
    silence leaves the prompt to the human.
Precedence within an event: deny > ask > allow. The composite answers on stdout in the
PreToolUse shape (or exits 2 to block), so the harness reads it like any single hook.
Each component's outcome goes to stderr as one JSON line for the trial log. Stdlib only.
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from recipes import interpret_pretooluse  # noqa: E402

RANK = {"block": 3, "ask": 2, "allow": 1}


def run_event(chain, payload, event):
    data = json.dumps({**payload, "hook_event_name": event})
    best, trace = None, []
    for argv in chain:
        try:
            p = subprocess.run(argv, input=data, capture_output=True, text=True, timeout=55)
            outcome = interpret_pretooluse(p.returncode, p.stdout, p.stderr)
        except subprocess.TimeoutExpired:
            outcome = "error"
        trace.append({"event": event, "hook": os.path.basename(argv[-1]), "outcome": outcome})
        if outcome in RANK and (best is None or RANK[outcome] > RANK[best]):
            best = outcome
    return best, trace


def answer(decision):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                             "permissionDecision": decision}}))


def main():
    spec = json.loads(os.environ["COMPOSE_SPEC"])
    payload = json.loads(sys.stdin.read() or "{}")
    chains = spec.get(payload.get("tool_name", ""), {})

    pre, trace = run_event(chains.get("PreToolUse", []), payload, "PreToolUse")
    if pre in ("block", "ask", "allow"):
        decision = pre
    else:
        perm, more = run_event(chains.get("PermissionRequest", []), payload, "PermissionRequest")
        trace += more
        decision = perm if perm in ("block", "allow") else None
    print(json.dumps({"compose_trace": trace}), file=sys.stderr)
    if decision == "block":
        sys.exit(2)
    if decision:
        answer(decision)


if __name__ == "__main__":
    main()
