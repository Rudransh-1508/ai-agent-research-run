#!/usr/bin/env python3
"""Fault-injection runner: execute real gate code against injected model faults.

For each gate recipe (recipes.py) and each fault mode, this starts a local
fault server (fault_server.py), runs the gate's own entry point unmodified with
its model traffic rerouted to that server (shim/), and records what the gate
did: exit code, stdout, stderr tail, wall time, and every request the server
received.

Each trial runs with HOME pointed at a fresh temporary directory, so gates that
write logs or sessions under ~ never touch the real home directory.

Two control modes ("yes", "no": valid answers at opposite poles) come first.
A gate counts as EXERCISED only if its model was called in the controls and the
two controls produce different outcomes: then the harness is observing the
gate's real decision path, and a fault outcome can be compared against it.

The Claude Code hook contract fixes what an outcome means (hooks docs, accessed
2026-09-28): exit 2 blocks; exit 0 with a JSON permissionDecision of
deny/ask/allow applies it; exit 0 with no decision defers to the host's normal
permission flow. A process still running at the host's hook timeout is killed
by the host; that is recorded as host_timeout, not interpreted here.

Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import recipes  # noqa: E402

CONTROL_MODES = ["yes", "no"]
FAULT_MODES = ["http_400_max_tokens", "http_429", "http_500", "http_503", "timeout", "malformed", "schema_drift",
               "conn_refused"]


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def start_server(mode, log_path, spec=None):
    port = free_port()
    if mode == "conn_refused":
        return None, port  # nothing listens on this port
    argv = [sys.executable, os.path.join(HERE, "fault_server.py"), "--mode", mode,
            "--port", str(port), "--log", log_path]
    if spec is not None:
        spec_path = log_path + ".spec.json"
        with open(spec_path, "w") as f:
            json.dump(spec, f)
        argv += ["--spec", spec_path]
    proc = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    proc.stdout.readline()  # "ready"
    return proc, port


def read_calls(log_path):
    if not os.path.exists(log_path):
        return []
    with open(log_path) as f:
        return [json.loads(line) for line in f if line.strip()]


def run_trial(recipe, mode, host_timeout_s):
    work = tempfile.mkdtemp(prefix="fi-")
    home = os.path.join(work, "home")
    os.makedirs(home)
    log_path = os.path.join(work, "server.jsonl")
    server, port = start_server(mode, log_path, recipe.controls.get(mode))
    try:
        ctx = recipes.Context(work=work, home=home)
        recipe.setup(ctx)
        env = {
            "PATH": os.environ["PATH"],
            "HOME": home,
            "TMPDIR": work,
            "LANG": "en_US.UTF-8",
            "FI_PORT": str(port),
            "NODE_OPTIONS": f"--require {os.path.join(HERE, 'shim', 'node', 'redirect.cjs')}",
            "PYTHONPATH": os.pathsep.join(
                [os.path.join(HERE, "shim", "python")] + recipe.pythonpath),
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        env.update(recipe.env(ctx, port))
        t0 = time.monotonic()
        try:
            p = subprocess.run(recipe.argv(ctx), cwd=recipe.cwd(ctx), env=env,
                               input=recipe.stdin(ctx), capture_output=True, text=True,
                               timeout=host_timeout_s)
            exit_code, out, err, killed = p.returncode, p.stdout, p.stderr, False
        except subprocess.TimeoutExpired as e:
            exit_code = None
            out = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
            err = e.stderr.decode() if isinstance(e.stderr, bytes) else (e.stderr or "")
            killed = True
        wall = time.monotonic() - t0
    finally:
        if server:
            server.kill()
            server.wait()
    calls = read_calls(log_path)
    stub_log = os.path.join(work, "stub_claude_calls.log")
    stub_calls = sum(1 for _ in open(stub_log)) if os.path.exists(stub_log) else 0
    outcome = "host_timeout" if killed else recipe.interpret(exit_code, out, err)
    shutil.rmtree(work, ignore_errors=True)
    return {"gate": recipe.name, "mode": mode, "outcome": outcome, "exit": exit_code,
            "wall_s": round(wall, 2), "model_calls": len(calls),
            "cli_fallback_calls": stub_calls,
            "marker_reached_model": (any(c.get("has_marker") for c in calls)
                                     if calls and calls[0].get("has_marker") is not None else None),
            "stdout_tail": out[-600:], "stderr_tail": err[-600:],
            "calls": calls[:5]}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--gates", nargs="*", help="recipe names (default: all)")
    ap.add_argument("--modes", nargs="*", default=CONTROL_MODES + FAULT_MODES)
    ap.add_argument("--host-timeout", type=float, default=60.0,
                    help="seconds before the host kills the hook (Claude Code default: 60)")
    ap.add_argument("--out", default=os.path.join(HERE, "results", "fault_trials.jsonl"))
    ap.add_argument("--padded", choices=("suffix", "prefix"),
                    help="pad each gate's probe command to ~372k chars (benchmark/build_oversize.py)"
                         " and record whether its dangerous part reached the model")
    args = ap.parse_args()

    # The design slot runs only when named (it needs DESIGN_CMD).
    selected = [r for r in recipes.RECIPES
                if (r.name in args.gates if args.gates else r.runtime != "design")]
    if args.padded:
        sys.path.insert(0, os.path.join(HERE, "..", "benchmark"))
        from build_oversize import padded
        os.environ["FI_MARKER"] = "rm -rf ./build"
        for r in selected:
            if r.probe == "pretooluse":
                r.command = padded(r.command, args.padded)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    stamp = datetime.now(timezone.utc).isoformat()
    with open(args.out, "a") as f:
        for recipe in selected:
            for mode in args.modes:
                row = run_trial(recipe, mode, args.host_timeout)
                row["ts"] = stamp
                row["sha"] = recipes.gate_version(recipe)
                row["padded"] = args.padded
                f.write(json.dumps(row) + "\n")
                f.flush()
                print(f"{recipe.name:28s} {mode:13s} -> {row['outcome']:14s} "
                      f"exit={row['exit']} calls={row['model_calls']} t={row['wall_s']}s",
                      flush=True)


if __name__ == "__main__":
    main()
