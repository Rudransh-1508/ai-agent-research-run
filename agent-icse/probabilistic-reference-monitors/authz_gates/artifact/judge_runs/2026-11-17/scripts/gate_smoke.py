import json, os, subprocess
G = "/Users/rudranshrathore/research-gap-agentic/agent-icse/probabilistic-reference-monitors/authz_gates"
DCG = G + "/baselines/dcg/dcg"
cases = [("default", "git stash list"), ("default", "pip uninstall -y requests"),
         ("bypassPermissions", "npm run build")]
for nokey in (False, True):
    env = dict(os.environ, DESIGN_JUDGE="groq", DESIGN_THRESHOLD="0.305")
    if os.path.exists(DCG):
        env["DESIGN_DCG_BIN"] = DCG
    if nokey:
        env.pop("GROQ_API_KEYS", None); env.pop("GROQ_API_KEY", None)
    for mode, cmd in cases:
        payload = {"hook_event_name": "PreToolUse", "permission_mode": mode,
                   "tool_name": "Bash", "tool_input": {"command": cmd}}
        out = subprocess.run(["python3", G + "/design/gate.py"], input=json.dumps(payload).encode(),
                             capture_output=True, env=env, timeout=120)
        h = json.loads(out.stdout)["hookSpecificOutput"]
        print("nokey" if nokey else "keys ", mode, repr(cmd), "->", h["permissionDecision"],
              h["permissionDecisionReason"][:110], out.stderr.decode()[-200:])
