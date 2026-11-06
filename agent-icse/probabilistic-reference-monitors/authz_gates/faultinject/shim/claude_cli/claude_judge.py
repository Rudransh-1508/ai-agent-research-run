"""Run the real Claude Code CLI as a gate's `claude -p` fallback judge (see ./claude)."""
import json
import os
import shutil
import subprocess
import sys

log, args = sys.argv[1], sys.argv[2:]
env = json.loads(os.environ["REAL_ENV_JSON"])
exe = shutil.which("claude", path=env.get("PATH")) or "/opt/homebrew/bin/claude"
# stdin is empty, as with the gate's own execFileSync call: `claude -p` would otherwise
# append whatever it reads there to the prompt.
p = subprocess.run([exe, "--setting-sources", "project", "--strict-mcp-config",
                    "--no-session-persistence", "--tools", ""] + args,
                   env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True)
with open(log, "a") as f:
    f.write(json.dumps({"exit": p.returncode, "answer": (p.stdout or p.stderr)[-200:]}) + "\n")
sys.stdout.write(p.stdout)
sys.exit(p.returncode)
