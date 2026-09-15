"""Rebuild artifact_hashes.json over the whole tree.

One entry per archived file, keyed by its path relative to the repo root, so the
manifest describes the layout and not just a pile of names. Build outputs and
the virtualenv are excluded; everything a referee would need to reproduce the
results is included.
"""
import hashlib, json, os, sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from c39.paths import ROOT, rel

SKIP_DIRS = {".venv310", "__pycache__", "dist", ".git", ".idea", ".vscode"}
SKIP_EXT = {".aux", ".log~", ".out", ".bbl", ".blg", ".pdf", ".toc", ".fls",
            ".fdb_latexmk", ".synctex.gz", ".gz", ".zip", ".pyc"}
KEEP_EXT = {".py", ".md", ".json", ".log", ".txt", ".tex", ".bib"}
SELF = "artifact_hashes.json"

out = {}
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
    for f in sorted(filenames):
        p = pathlib.Path(dirpath) / f
        if f == SELF or p.suffix in SKIP_EXT or p.suffix not in KEEP_EXT:
            continue
        # LaTeX build logs are output, not evidence; results/logs/ are
        # evidence and stay. This matches .gitignore exactly -- and it must
        # cover every paper directory, not just paper/, or a new one silently
        # gets its build log hashed and then gitignored, which breaks the
        # archive's own integrity check.
        if p.suffix == ".log" and p.parent.name.startswith("paper"):
            continue
        b = p.read_bytes()
        out[rel(p)] = {"sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}

target = ROOT / SELF
json.dump(out, open(target, "w"), indent=1)
print(f"hashed {len(out)} files -> {rel(target)}")
by_dir = {}
for k in out:
    by_dir[k.split("/")[0] if "/" in k else "(root)"] = \
        by_dir.get(k.split("/")[0] if "/" in k else "(root)", 0) + 1
for d, c in sorted(by_dir.items()):
    print(f"   {d:<20} {c}")
