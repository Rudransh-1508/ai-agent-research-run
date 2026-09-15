"""Verify artifact_hashes.json against the tree it claims to describe.

    python src/check_manifest.py

Reports files missing from the manifest, manifest entries whose file is gone,
and files whose sha256 has drifted. Exit code 0 iff the manifest is exact.
Rebuild with src/update_hashes.py, which uses the same selection rules.
"""
import hashlib, json, os, sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from c39.paths import ROOT, rel

SKIP_DIRS = {".venv310", "__pycache__", "dist", ".git", ".idea", ".vscode"}
SKIP_EXT = {".aux", ".log~", ".out", ".bbl", ".blg", ".pdf", ".toc", ".fls",
            ".fdb_latexmk", ".synctex.gz", ".gz", ".zip", ".pyc"}
KEEP_EXT = {".py", ".md", ".json", ".log", ".txt", ".tex", ".bib"}
SELF = "artifact_hashes.json"


def current():
    out = {}
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for f in sorted(filenames):
            p = pathlib.Path(dirpath) / f
            if f == SELF or p.suffix in SKIP_EXT or p.suffix not in KEEP_EXT:
                continue
            # LaTeX build logs are output, not evidence; results/logs/ are
            # evidence and stay. This matches .gitignore exactly.
            if p.suffix == ".log" and p.parent.name == "paper":
                continue
            out[rel(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


man = {k: v["sha256"] for k, v in json.load(open(ROOT / SELF)).items()}
cur = current()

missing = sorted(set(cur) - set(man))     # on disk, not in the manifest
vanished = sorted(set(man) - set(cur))    # in the manifest, not on disk
changed = sorted(k for k in set(man) & set(cur) if man[k] != cur[k])

print(f"manifest: {len(man)} entries   tree: {len(cur)} files")
for label, group in (("NOT IN MANIFEST", missing),
                     ("MISSING FROM TREE", vanished),
                     ("HASH CHANGED", changed)):
    for k in group:
        print(f"  [{label}] {k}")

if missing or vanished or changed:
    print(f"\nMANIFEST STALE -- {len(missing)+len(vanished)+len(changed)} "
          f"discrepancies.\nRerun: python src/update_hashes.py")
    sys.exit(1)
print("\nMANIFEST EXACT -- every recorded file present and unchanged.")
