#!/usr/bin/env python3
"""Clone each included gate repo into corpus/repos/<name>/ and pin its HEAD SHA.

Reads gates.json (from enumerate_gates.py), shallow-clones every entry whose
inclusion status is "included-pending-code-read" (or "included"), records the
pinned HEAD SHA and clone date back into gates.json. Stdlib only
(subprocess/json). Idempotent: repos already present are not re-cloned; their
recorded SHA is re-read from disk.
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GATES = os.path.join(HERE, "gates.json")
REPOS = os.path.join(HERE, "repos")
CLONE_DATE = "2026-09-21"


def dirname_for(gate):
    """Stable directory name: github owner__repo, else sanitized name."""
    gh = gate.get("github")
    if gh:
        return gh.replace("/", "__")
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", gate["name"])


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=600, **kw)


def main():
    with open(GATES) as f:
        data = json.load(f)
    os.makedirs(REPOS, exist_ok=True)

    for g in data["gates"]:
        if not g["inclusion"].startswith("included"):
            continue
        dest = os.path.join(REPOS, dirname_for(g))
        g["repo_dir"] = os.path.relpath(dest, HERE)
        if os.path.isdir(os.path.join(dest, ".git")):
            p = run(["git", "-C", dest, "rev-parse", "HEAD"])
            g["pinned_sha"] = p.stdout.strip()
            g.setdefault("clone_date", CLONE_DATE)
            print(f"present  {g['name']:<28} {g['pinned_sha'][:12]}")
            continue
        url = g["url"]
        if not url.endswith(".git") and "github.com" in url:
            url = url + ".git"
        p = run(["git", "clone", "--depth", "1", url, dest])
        if p.returncode != 0:
            g["inclusion"] = "excluded"
            g["reason"] = f"clone failed on {CLONE_DATE}: {p.stderr.strip()[:200]}"
            print(f"FAILED   {g['name']:<28} {p.stderr.strip()[:120]}")
            continue
        p = run(["git", "-C", dest, "rev-parse", "HEAD"])
        g["pinned_sha"] = p.stdout.strip()
        g["clone_date"] = CLONE_DATE
        print(f"cloned   {g['name']:<28} {g['pinned_sha'][:12]}")

    with open(GATES, "w") as f:
        json.dump(data, f, indent=2)
    ok = [g for g in data["gates"] if g.get("pinned_sha")]
    print(f"\ncloned/present: {len(ok)}")


if __name__ == "__main__":
    sys.exit(main())
