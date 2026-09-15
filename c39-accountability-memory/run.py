"""One entry point, so nobody has to remember which script lives where.

    python run.py verify | audit | score | figures | package | all

Every task runs from the repo root regardless of the working directory, and
stops on the first failure so a broken step cannot be mistaken for a passing
run.
"""
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable

TASKS = {
    "verify":  [("src/check_manifest.py", "archive integrity"),
                ("src/verify_all.py", "solver-free checks")],
    "audit":   [("src/audit_paper_numbers.py", "paper vs artifacts")],
    "score":   [("src/analyse_experiment.py", "pre-registered predictions")],
    "figures": [("src/make_figures.py", "one-bit frontier"),
                ("src/make_figures2.py", "intermediate-K and identity plots")],
    "package": [("src/update_hashes.py", "refresh manifest"),
                ("src/make_artifact.py", "build archive")],
}
TASKS["all"] = TASKS["verify"] + TASKS["audit"] + TASKS["score"] + TASKS["figures"]


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in TASKS:
        print(__doc__.strip())
        print("\ntasks: " + ", ".join(sorted(TASKS)))
        return 2
    failed = 0
    for script, label in TASKS[sys.argv[1]]:
        print(f"\n=== {label}  ({script})")
        r = subprocess.run([PY, str(ROOT / script)], cwd=str(ROOT))
        if r.returncode != 0:
            print(f"FAILED: {script} exited {r.returncode}")
            failed = r.returncode
            break
    if failed:
        return failed
    print(f"\n{sys.argv[1]}: all steps passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
