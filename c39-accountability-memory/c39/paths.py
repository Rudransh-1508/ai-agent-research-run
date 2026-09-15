"""Where things live, resolved from the repo root rather than the shell's cwd.

Before this module every script opened bare filenames, so each one only worked
when run from the repo root and the layout could never change. Everything now
goes through `data()` for reads and `out()` for writes, both anchored to
`ROOT`, which is derived from this file's own location. Scripts work from any
working directory and the tree can be rearranged again without touching them.

    from c39.paths import data, out
    cert = json.load(open(data("certified_codes.json")))
    json.dump(obj, open(out("my_results.json"), "w"))
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SRC = ROOT / "src"
EXPERIMENTS = ROOT / "experiments"
RESULTS = ROOT / "results"
LOGS = RESULTS / "logs"
DOCS = ROOT / "docs"
PAPER = ROOT / "paper"
ARCHIVE = ROOT / "archive"
PREPINNED = ROOT / "prepinned_backup"

# Read order: a bare filename is looked for in each of these, first hit wins.
# Root is first so environment.json and artifact_hashes.json resolve there.
SEARCH = [ROOT, RESULTS, LOGS, DOCS, DOCS / "archive", PAPER, ARCHIVE, PREPINNED]

for _d in (SRC, EXPERIMENTS, RESULTS, LOGS, DOCS, DOCS / "archive", ARCHIVE):
    _d.mkdir(parents=True, exist_ok=True)


def data(name):
    """Resolve a file for reading. Accepts a bare name or a path under ROOT."""
    p = Path(name)
    if p.is_absolute():
        return p
    direct = ROOT / p
    if direct.exists() or len(p.parts) > 1:
        return direct
    for d in SEARCH:
        cand = d / p
        if cand.exists():
            return cand
    return direct                      # let the caller raise a normal error


def out(name):
    """Resolve a file for writing, routed by extension unless a path is given."""
    p = Path(name)
    if p.is_absolute() or len(p.parts) > 1:
        return ROOT / p if not p.is_absolute() else p
    if p.suffix == ".log":
        return LOGS / p
    if p.suffix in (".json",) and p.name not in ("environment.json",
                                                 "artifact_hashes.json"):
        return RESULTS / p
    if p.suffix in (".md", ".txt"):
        return DOCS / p
    return ROOT / p


def rel(path):
    """A path relative to ROOT, with forward slashes, for manifests."""
    return str(Path(path).resolve().relative_to(ROOT)).replace("\\", "/")
