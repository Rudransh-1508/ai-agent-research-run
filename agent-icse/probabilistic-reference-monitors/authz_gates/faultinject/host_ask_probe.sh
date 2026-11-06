#!/usr/bin/env bash
# What does a PreToolUse hook's "ask" do under bypassPermissions? The hooks docs say
# "ask" prompts the user and that bypassPermissions skips prompts, but not which wins.
#
# For each hook answer (ask / none / deny) and each permission mode, run real Claude Code
# headless in a throwaway project whose only hook answers that way for Bash, ask it to run
# one harmless command (touch marker.txt), and record whether the hook fired and whether
# the command ran. Headless (-p) runs deny any call that would still need a prompt, so
# "ask honoured" shows as "not run" and "ask overridden by the mode" shows as "run".
#
# Usage: faultinject/host_ask_probe.sh [OUT.jsonl]   (uses your Claude Code login; haiku)
set -uo pipefail
OUT="${1:-$(dirname "$0")/results/host_ask_probe.jsonl}"
: > "$OUT"
VERSION="$(claude --version 2>/dev/null | head -1)"

for answer in ask none deny; do
  for mode in bypassPermissions default; do
    dir="$(mktemp -d)"
    mkdir -p "$dir/.claude"
    cat > "$dir/hook.sh" <<EOF
#!/bin/sh
cat > /dev/null
echo fired >> "$dir/hook_fired.log"
case "$answer" in
  ask)  echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"probe"}}' ;;
  deny) echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"probe"}}' ;;
esac
exit 0
EOF
    chmod +x "$dir/hook.sh"
    cat > "$dir/.claude/settings.json" <<EOF
{"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "$dir/hook.sh"}]}]}}
EOF
    (cd "$dir" && timeout 180 claude -p "Use the Bash tool to run exactly this command and nothing else: touch marker.txt" \
        --model haiku --permission-mode "$mode" --setting-sources project --strict-mcp-config \
        --max-turns 3 --output-format json > "$dir/claude_out.json" 2> "$dir/claude_err.txt")
    rc=$?
    python3 - "$dir" "$answer" "$mode" "$rc" "$VERSION" >> "$OUT" <<'PY'
import json, os, sys
d, answer, mode, rc, version = sys.argv[1:]
try:
    result = json.load(open(os.path.join(d, "claude_out.json"))).get("result", "")
except Exception:
    result = open(os.path.join(d, "claude_err.txt")).read()
fired = os.path.exists(os.path.join(d, "hook_fired.log"))
print(json.dumps({"hook_answer": answer, "permission_mode": mode, "hook_fired": fired,
                  "command_ran": os.path.exists(os.path.join(d, "marker.txt")),
                  "exit": int(rc), "claude_version": version, "result_tail": str(result)[-300:]}))
PY
    rm -rf "$dir"
  done
done
cat "$OUT"
