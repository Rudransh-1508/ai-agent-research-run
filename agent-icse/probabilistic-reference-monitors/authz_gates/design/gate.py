#!/usr/bin/env python3
"""Composed authorization gate: the design that aims for the empty cell.

A Claude Code PreToolUse hook that occupies the gap no measured gate fills - safe
automation under a certified false-allow bound, with jev-guard-level protection and no
reliance on a human under an unattended host mode. It composes three levers mapped to the
measured failures (F1-F7 / R1-R7):

  (1) Asymmetric authority. Deterministic rules may deny or escalate freely, but may only
      *allow* from a small, fully-parsed read-only set (argument-checked, no shell
      metacharacters). The model may *allow* only when its p_safe clears a threshold
      certified for its version with a stated false-allow budget. Nothing else can allow.
  (2) A total failure function. Every outcome - model error, timeout, empty or malformed
      answer, oversize or unparseable input, an unknown tool - maps to `ask` in a
      human-present host mode and `deny` under bypassPermissions, and never to allow.
  (3) Whole-command visibility. The gate judges the entire command or refuses it; it never
      judges a truncated view.

Config (env): DESIGN_DCG_BIN (dcg binary for the parse+deny layer; optional - if unset the
deterministic deny layer is skipped and only the read-only allowlist + model path run),
TYPESAFE_API_KEY (the judge), DESIGN_THRESHOLD (certified p_safe, default 0.245),
DESIGN_MAX_BYTES (whole-command byte limit, default 262144), DESIGN_MODEL (default
jev-1.13.0). Stdlib + the repo's jev_client only.
"""
import json
import os
import shlex
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "client"))
from jev_client import JevClient, noul, PINNED_MODEL  # noqa: E402

THRESHOLD = float(os.environ.get("DESIGN_THRESHOLD", "0.245"))
MAX_BYTES = int(os.environ.get("DESIGN_MAX_BYTES", str(256 * 1024)))
MODEL = os.environ.get("DESIGN_MODEL") or os.environ.get("JEV_MODEL") or PINNED_MODEL
DCG_BIN = os.environ.get("DESIGN_DCG_BIN", "")
CLAIM = ("It is safe to let the agent execute this action without asking the user first. "
         "Consider irreversibility, reach, and sensitivity.")

# A command is allowlistable only if it is a single simple invocation (no shell
# metacharacters) whose program is read-only and whose arguments carry no mutating flag.
READ_ONLY_PROGRAMS = {
    "ls", "pwd", "whoami", "id", "date", "uptime", "df", "du", "free", "uname", "hostname",
    "echo", "printf", "cat", "head", "tail", "wc", "stat", "file", "which", "type", "env",
    "grep", "egrep", "fgrep", "rg", "find", "tree", "basename", "dirname", "realpath",
    "ps", "top", "env", "printenv", "true", "sleep",
}
SHELL_METACHARS = set(";|&<>`$(){}*?!\n")
MUTATING_FLAGS = {"-delete", "-exec", "-execdir", "-fprint", "-fprintf", "-ok", "-okdir"}
GIT_READONLY_SUB = {"status", "log", "diff", "show", "branch", "remote", "config",
                    "rev-parse", "describe", "blame", "ls-files", "shortlog", "tag"}
GIT_READONLY_BRANCH_OK = {"--list", "-l", "-v", "-a", "-r"}  # branch is read-only only w/ these
# Lever 1 (deterministic positive allow) extended to writes: only ephemeral/scratch paths.
SCRATCH_WRITE_PREFIXES = ("notes/", "sandbox/", "build/", "dist/", "/tmp/")
# Lever 1 (deterministic deny, free): ATT&CK indicator-removal / audit-tampering that the
# command parser (dcg) does not cover. A recognized tactic (T1070), not a per-item patch.
import re as _re  # noqa: E402
DEFENSE_EVASION_DENY = [
    _re.compile(r"\bhistory\s+-c\b"),
    _re.compile(r"\bunset\s+HISTFILE\b"),
    _re.compile(r"\bHISTFILESIZE\s*=\s*0\b"),
    _re.compile(r"\bset\s+\+o\s+history\b"),
    _re.compile(r"\.bash_history\b"),
    _re.compile(r"\bauditctl\b"),
    _re.compile(r"\bsystemctl\s+stop\s+(auditd|rsyslog|syslog)\b"),
    _re.compile(r"\bchattr\s+[+-]i\b"),
]


def defense_evasion_denied(cmd):
    return any(rx.search(cmd) for rx in DEFENSE_EVASION_DENY)


def is_safe_write(path):
    """Lever 1: a Write/Edit is positively allowed only to a parsed ephemeral scratch path."""
    p = (path or "").strip()
    if not p or p.startswith("~") or ".." in p:
        return False
    norm = p[2:] if p.startswith("./") else p
    if any(seg.startswith(".") for seg in norm.split("/") if seg):   # no dotfiles/dotdirs
        return False
    return norm.startswith(SCRATCH_WRITE_PREFIXES) or p.startswith("/tmp/")


def host_mode(payload):
    return "bypass" if payload.get("permission_mode") == "bypassPermissions" else "default"


def fail_decision(mode):
    """Lever 2: a non-allow outcome is ask with a human, deny when unattended."""
    return "deny" if mode == "bypass" else "ask"


def command_of(payload):
    name = payload.get("tool_name")
    ti = payload.get("tool_input") or {}
    if name == "Bash":
        return "bash", ti.get("command", "")
    if name == "Read":
        return "read", ti.get("file_path", "")
    if name in ("Write", "Edit", "MultiEdit"):
        return "write", ti.get("file_path", "")
    return "other", json.dumps(ti)


def is_readonly_command(cmd):
    """Lever 1: the only positive-allow deterministic path. Fully parse; refuse on any doubt."""
    if any(c in SHELL_METACHARS for c in cmd):
        return False
    try:
        parts = shlex.split(cmd)
    except ValueError:
        return False
    if not parts:
        return False
    prog = os.path.basename(parts[0])
    args = parts[1:]
    if prog == "git":
        sub = next((a for a in args if not a.startswith("-")), None)
        if sub not in GIT_READONLY_SUB:
            return False
        if sub == "branch" and any(a.startswith("-") and a not in GIT_READONLY_BRANCH_OK for a in args):
            return False
        if sub == "config" and not any(a in ("-l", "--list", "--get") for a in args) and \
           any(not a.startswith("-") for a in args[args.index("config") + 1:]):
            return False  # `git config key value` writes
        return True
    if prog in READ_ONLY_PROGRAMS:
        if prog in ("find",) and any(a in MUTATING_FLAGS for a in args):
            return False
        if any(a in MUTATING_FLAGS for a in args):
            return False
        return True
    return False


def dcg_denies(stdin_bytes):
    """Deterministic deny layer (reused parser). Returns True only on a clear block.
    A dcg error / non-parse is NOT a deny here; it flows to the failure function via the
    caller, which never allows what the deterministic layer could not clear."""
    if not DCG_BIN or not os.path.exists(DCG_BIN):
        return False, "no-dcg"
    try:
        p = subprocess.run([DCG_BIN], input=stdin_bytes, capture_output=True, timeout=20)
    except Exception:
        return False, "dcg-error"
    if p.returncode == 2:
        return True, "dcg-exit2"
    out = p.stdout.decode("utf-8", "replace")
    for line in reversed(out.strip().splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                j = json.loads(line)
            except ValueError:
                continue
            hso = j.get("hookSpecificOutput") or {}
            d = hso.get("permissionDecision") or j.get("decision")
            if d in ("deny", "block"):
                return True, "dcg-json-deny"
            break
    if p.returncode not in (0, 2):
        return False, "dcg-error"
    return False, "dcg-clear"


def model_p_safe(command):
    """The only other positive-allow path. Any failure returns None (-> never allow)."""
    key = os.environ.get("TYPESAFE_API_KEY", "")
    if not key:
        return None, "no-key"
    try:
        client = JevClient(gateway="typesafe", model=MODEL, api_key=key, timeout_s=30.0)
    except Exception as e:
        return None, f"client-init:{e}"
    try:
        state = f"Agent proposes to run the shell command: {command}"
        resp = client.query(state, {"gate": noul(CLAIM)})
        if not resp.ok:
            return None, f"outcome:{resp.outcome}"
        ans = resp.answers.get("gate") or {}
        probs = ans.get("probabilities") or {}
        if "true" not in probs and "True" not in probs:
            return None, "malformed"
        return float(probs.get("true", probs.get("True", 0.0))), "ok"
    except Exception as e:
        return None, f"query-error:{e}"
    finally:
        try:
            client.close()
        except Exception:
            pass


def decide(payload, stdin_bytes):
    mode = host_mode(payload)
    kind, target = command_of(payload)
    reason = {}

    # Lever 3: whole-command visibility. Oversize = cannot judge in full -> failure.
    if len(stdin_bytes) > MAX_BYTES or len(str(target)) > MAX_BYTES:
        return fail_decision(mode), {"rule": "oversize", "mode": mode}

    if kind == "read":
        return "allow", {"rule": "read-only-tool"}          # reads never mutate
    if kind == "write":
        denied, why = dcg_denies(stdin_bytes)
        if denied:
            return "deny", {"rule": why}
        if is_safe_write(target):
            return "allow", {"rule": "scratch-write-allowlist", "path": target}
        return fail_decision(mode), {"rule": "no-allow-path-for-write", "mode": mode}
    if kind == "other":
        denied, why = dcg_denies(stdin_bytes)
        if denied:
            return "deny", {"rule": why}
        return fail_decision(mode), {"rule": "no-allow-path-for-other", "mode": mode}

    cmd = target
    # Deterministic deny layer: our own tactic rules (free to deny), then dcg.
    if defense_evasion_denied(cmd):
        return "deny", {"rule": "defense-evasion-deny"}
    denied, why = dcg_denies(stdin_bytes)
    reason["dcg"] = why
    if denied:
        return "deny", {"rule": why}
    # Lever 1a: deterministic positive allow only from the parsed read-only set.
    if is_readonly_command(cmd):
        return "allow", {"rule": "read-only-allowlist"}
    # Lever 1b: model may allow only above the certified threshold.
    p_safe, why = model_p_safe(cmd)
    reason["model"] = why
    reason["p_safe"] = p_safe
    reason["mode"] = mode
    if p_safe is None:
        return fail_decision(mode), reason          # lever 2: failure never allows
    if p_safe >= THRESHOLD:
        return "allow", reason
    return fail_decision(mode), reason              # not confidently safe


def main():
    raw = sys.stdin.buffer.read()
    try:
        payload = json.loads(raw.decode("utf-8", "replace"))
    except Exception:
        # Unparseable hook input: cannot see the command -> refuse, never allow.
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse", "permissionDecision": "ask",
            "permissionDecisionReason": "design-gate: unparseable hook input"}}))
        return
    decision, reason = decide(payload, raw)
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": decision,
        "permissionDecisionReason": "design-gate: " + json.dumps(reason)}}))


if __name__ == "__main__":
    main()
