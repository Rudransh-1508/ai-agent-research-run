#!/usr/bin/env python3
"""Render in-threat-model Linux-shell Atomic Red Team tests into candidate corpus items.

Each candidate keeps the atomic's prereq_command (to set up the target) and command, with
default input arguments substituted, so the sandbox can run prereq-then-command the way
Atomic Red Team itself does and we can observe the real effect. MIT-licensed source
(redcanaryco/atomic-red-team); attribution kept per item.
"""
import glob
import json
import re
import sys

ART = sys.argv[1] if len(sys.argv) > 1 else "atomic-red-team"
INTEREST = {"T1485", "T1486", "T1490", "T1070", "T1552", "T1048", "T1567",
            "T1222", "T1489", "T1531", "T1561", "T1565", "T1005"}
import yaml  # noqa: E402


def subst(text, args):
    def repl(m):
        k = m.group(1)
        v = (args.get(k) or {}).get("default", "")
        return str(v) if v is not None else ""
    return re.sub(r"#\{([^}]+)\}", repl, text or "")


def main():
    out = []
    for f in sorted(glob.glob(f"{ART}/atomics/T*/T*.yaml")):
        try:
            d = yaml.safe_load(open(f))
        except Exception:
            continue
        if not d:
            continue
        tid = d.get("attack_technique", "")
        if tid.split(".")[0] not in INTEREST:
            continue
        for i, t in enumerate(d.get("atomic_tests", [])):
            ex = t.get("executor") or {}
            if "linux" not in t.get("supported_platforms", []) or ex.get("name") not in ("sh", "bash", "command"):
                continue
            args = t.get("input_arguments") or {}
            cmd = subst(ex.get("command", ""), args).strip()
            if not cmd:
                continue
            prereqs = []
            for dep in (t.get("dependencies") or []):
                gp = subst(dep.get("get_prereq_command", ""), args).strip()
                if gp:
                    prereqs.append(gp)
            prereq = subst(ex.get("prereq_command", ""), args).strip()
            if prereq:
                prereqs.append(prereq)
            out.append({
                "source": "atomic-red-team",
                "attack_technique": tid,
                "guid": t.get("auto_generated_guid", f"{tid}-{i}"),
                "name": t.get("name", ""),
                "executor": ex.get("name"),
                "elevation_required": bool(ex.get("elevation_required")),
                "prereq": "\n".join(prereqs),
                "command": cmd,
            })
    for r in out:
        print(json.dumps(r))


if __name__ == "__main__":
    main()
