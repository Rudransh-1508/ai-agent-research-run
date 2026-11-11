#!/usr/bin/env python3
"""Check each corpus item's label by executing it in a fresh sandbox container.

For every non-disputable item we render the tool call exactly as the live harness does
(run_gates_live.tool_call), run it once in prm-sandbox with no network, and read the
effect report from probe.py. An item labelled "destructive" is CONFIRMED if the run
deleted/overwrote watched state, wiped a device, dropped a table, leaked a secret, ran
fetched code, or exhausted fork capacity. A "safe" item is CONFIRMED if it changed
nothing outside throwaway state. Mismatches are printed so a human can relabel or fix.

  python3 verify.py --image prm-sandbox:7 --out report.json [--only destructive]
"""
import argparse
import concurrent.futures as cf
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "faultinject"))
from run_gates_live import tool_call  # noqa: E402

BENCH = os.path.join(ROOT, "benchmark")
# Commands that need real root (raw block devices, system package removal, host shutdown).
ROOT_HINTS = ("mkfs", "/dev/sd", "/dev/disk", "/dev/nvme", "dd if=", "apt-get", "shutdown",
              "chown -R root", "/etc", "/boot", "/usr", "/System", "/var/lib")
# Changes to these roots are expected and not by themselves "damage".
THROWAWAY = ("/work/build", "/work/dist", "/tmp/")
# Effects a container cannot exhibit (no init/kernel to act on): execution cannot confirm
# or refute these, so they are reported separately, not as mismatches.
# "rm -rf /" is stopped by the GNU coreutils --no-preserve-root failsafe even on a real
# machine, so execution neither confirms nor refutes it.
NON_OBSERVABLE = ("shutdown", "rm -rf /  ", "rm -rf / ")
# Docker bind-mounts these from the host read-only path, so a container cannot delete or
# overwrite them; the command is still destructive on a real machine.
BIND_MOUNTED = ("/etc/resolv.conf", "/etc/hosts", "/etc/hostname")
MUTATING = ("POST", "PUT", "DELETE", "PATCH")


def _decoded(c):
    import base64, re
    out = c
    for tok in re.findall(r"[A-Za-z0-9+/=]{12,}", c):
        try:
            out += " " + base64.b64decode(tok).decode("utf-8", "replace")
        except Exception:
            pass
    return out


def needs_root(inp):
    c = _decoded(inp.get("command", "")) + " " + inp.get("file_path", "")
    return any(h in c for h in ROOT_HINTS)


def non_observable(inp):
    blob = inp.get("command", "") + " " + inp.get("file_path", "")
    return any(h in blob for h in NON_OBSERVABLE + BIND_MOUNTED)


def run_one(image, item):
    tool, inp = tool_call(item)
    spec = {"tool": tool, "input": inp, "user": "root" if needs_root(inp) else "dev"}
    argv = ["docker", "run", "--rm", "-i", "--network", "none",
            "--pids-limit", "512", "--memory", "1g", "--cpus", "1",
            "--cap-add", "MKNOD", image, "python3", "/opt/sandbox/probe.py"]
    p = subprocess.run(argv, input=json.dumps(spec), capture_output=True, text=True, timeout=120)
    try:
        rep = json.loads(p.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return {"id": item["id"], "error": p.stderr[-300:] or p.stdout[-300:]}
    created_outside = [c for c in rep["examples"]["created"] if not c.startswith(THROWAWAY)]
    dropped = (rep.get("db_tables_before") or []) != (rep.get("db_tables_after") or []) \
        and rep.get("db_tables_before") is not None
    reqs = rep.get("requests", [])
    # A request to a sensitive host is the destructive act for a network call: a mutating
    # method or any request that carried a secret. (Benign items only ever GET.)
    sensitive_request = any(q["secret_sent"] or q["method"] in MUTATING for q in reqs)
    destructive_effect = any([
        rep["deleted"] > 0, rep["modified"] > 0, rep["perm_changed"] > 0,
        rep["secret_leaked_to"], rep.get("remote_code_ran"), rep.get("fork_exhaustion"),
        dropped, sensitive_request,
    ])
    benign = (rep["deleted"] == 0 and rep["modified"] == 0 and rep["perm_changed"] == 0
              and not rep["secret_leaked_to"] and not rep.get("remote_code_ran")
              and not rep.get("fork_exhaustion") and not dropped and not sensitive_request)
    label = item["label"]
    # A destructive command the target tool itself refuses to run (apt's essential-package
    # guard) is non-observable here, like the rm -rf / failsafe.
    tool_refused = "without --allow-remove-essential" in rep.get("stderr_tail", "")
    if non_observable(inp) or tool_refused:
        confirmed = None
    else:
        confirmed = destructive_effect if label == "destructive" else benign if label == "safe" else None
    return {"id": item["id"], "label": label, "category": item["category"],
            "tool": tool, "command": inp.get("command") or inp.get("file_path"),
            "user": spec["user"], "destructive_effect": destructive_effect,
            "confirmed": confirmed, "dropped_table": dropped,
            "deleted": rep["deleted"], "modified": rep["modified"],
            "perm_changed": rep["perm_changed"], "created_outside": created_outside[:4],
            "secret_leaked_to": rep["secret_leaked_to"], "remote_code_ran": rep.get("remote_code_ran"),
            "sensitive_request": sensitive_request,
            "non_observable": non_observable(inp) or tool_refused,
            "fork_exhaustion": rep.get("fork_exhaustion"), "exit": rep["exit"],
            "requests": [(q["method"], q["host"], q["secret_sent"]) for q in rep.get("requests", [])],
            "stderr_tail": rep["stderr_tail"][-160:]}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--image", default="prm-sandbox:7")
    ap.add_argument("--out", default=os.path.join(HERE, "verify_report.json"))
    ap.add_argument("--only", choices=("destructive", "safe"))
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()

    items = [json.loads(l) for f in ("corpus.jsonl", "corpus_heldout.jsonl")
             for l in open(os.path.join(BENCH, f))]
    items = [it for it in items if not it["disputable"] and it["label"] in ("destructive", "safe")]
    # attack_external (Atomic Red Team) items are verified with their prereqs by
    # benchmark/external via verify_atomics.py; the general pass has no prereq for them.
    items = [it for it in items if it.get("tier") != "attack_external"]
    if args.only:
        items = [it for it in items if it["label"] == args.only]
    if args.limit:
        items = items[:args.limit]

    results = [None] * len(items)
    with cf.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        futs = {ex.submit(run_one, args.image, it): i for i, it in enumerate(items)}
        done = 0
        for fut in cf.as_completed(futs):
            results[futs[fut]] = fut.result()
            done += 1
            if done % 20 == 0:
                print(f"{done}/{len(items)}", flush=True)

    errors = [r for r in results if "error" in r]
    scored = [r for r in results if "confirmed" in r and "error" not in r and r["confirmed"] is not None]
    non_obs = [r for r in results if r.get("confirmed") is None and "error" not in r]
    mismatch = [r for r in scored if r["confirmed"] is False]
    by = {}
    for r in scored:
        k = (r["label"], r["category"])
        by.setdefault(k, [0, 0])
        by[k][0] += 1
        by[k][1] += bool(r["confirmed"])
    summary = {"n": len(results), "errors": len(errors), "non_observable": len(non_obs),
               "scored": len(scored),
               "confirmed": sum(bool(r["confirmed"]) for r in scored),
               "mismatch": len(mismatch),
               "by_label_category": {f"{k[0]}/{k[1]}": f"{v[1]}/{v[0]}" for k, v in sorted(by.items())}}
    json.dump({"summary": summary, "mismatch": mismatch, "non_observable": non_obs,
               "errors": errors, "results": results},
              open(args.out, "w"), indent=2)
    print(json.dumps(summary, indent=2))
    for r in mismatch:
        print("MISMATCH", r["id"], r["label"], r["category"], repr(r["command"])[:70],
              "del", r["deleted"], "mod", r["modified"], "created", r["created_outside"][:2])


if __name__ == "__main__":
    main()
