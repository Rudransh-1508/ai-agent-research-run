#!/usr/bin/env python3
"""Alternative design B: a deterministic least-privilege capability gate (no model).

The dominant 2026 paradigm (Progent, CaMeL, ToolFence, ChainCaps, LeanGuard, intent-graph
auditing) enforces security outside the model: a deterministic policy mediates every tool
call and the model is consulted at most once per task to set scope, never per call. This is
the per-call, fixed-policy degenerate of that paradigm - a default-deny capability allowlist
with no model call at all - built to contrast with design A (per-call model-in-the-loop with
a certified threshold).

Policy: a call is allowed only if it falls inside a granted capability; everything else fails
closed (ask with a human, deny under bypassPermissions). Granted capabilities:
  - cap:read          any Read tool call (reads do not mutate)
  - cap:readonly_sh   a single simple shell invocation of a read-only program (parsed,
                      argument-checked, no shell metacharacters) - reuses design A's set
  - cap:scratch_write a Write/Edit to an ephemeral scratch path - reuses design A's set
There is deliberately no capability for network, package, git-mutation, or arbitrary shell:
without task context a fixed policy cannot grant those safely, so they fail closed. That is
the point of the comparison - what a pure policy must refuse that a judged gate can allow.

The truest form of this paradigm derives the capability set per task from the user's
objective (one model call per task); our corpus is isolated tool calls with no task context,
so that version is out of scope here and noted as future work. Stdlib + design A helpers.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gate import (host_mode, fail_decision, command_of, is_readonly_command,  # noqa: E402
                  is_safe_write, MAX_BYTES)


def decide(payload, stdin_bytes):
    mode = host_mode(payload)
    kind, target = command_of(payload)
    if len(stdin_bytes) > MAX_BYTES or len(str(target)) > MAX_BYTES:
        return fail_decision(mode), {"rule": "oversize", "mode": mode}
    if kind == "read":
        return "allow", {"cap": "read"}
    if kind == "bash" and is_readonly_command(target):
        return "allow", {"cap": "readonly_sh"}
    if kind == "write" and is_safe_write(target):
        return "allow", {"cap": "scratch_write"}
    # Default-deny: no granted capability covers this call.
    return fail_decision(mode), {"rule": "no-capability", "kind": kind, "mode": mode}


def main():
    raw = sys.stdin.buffer.read()
    try:
        payload = json.loads(raw.decode("utf-8", "replace"))
    except Exception:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse", "permissionDecision": "ask",
            "permissionDecisionReason": "cap-gate: unparseable hook input"}}))
        return
    decision, reason = decide(payload, raw)
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse", "permissionDecision": decision,
        "permissionDecisionReason": "cap-gate: " + json.dumps(reason)}}))


if __name__ == "__main__":
    main()
