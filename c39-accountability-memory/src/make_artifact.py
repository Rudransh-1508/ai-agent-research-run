"""Build the reproducibility archive for the AAMAS submission.

    python src/make_artifact.py

The archive is exactly the set of files recorded in artifact_hashes.json, each
at its path relative to the repo root, plus the manifest itself. Unzipping it
reproduces the layout, so

    python src/check_manifest.py
    python src/verify_all.py

give MANIFEST EXACT and ALL CHECKS PASSED on a clean machine, with no solver and
no network.

Refuses to build if the manifest is stale -- run src/update_hashes.py first.
"""
import hashlib, json, os, sys, zipfile, pathlib
from datetime import date

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from c39.paths import ROOT

MANIFEST = "artifact_hashes.json"
OUT = ROOT / "dist" / f"c39_artifact_{date.today():%Y%m%d}.zip"

man = json.load(open(ROOT / MANIFEST))

bad = []
for rel_path, rec in man.items():
    p = ROOT / rel_path
    if not p.is_file():
        bad.append(f"missing: {rel_path}")
    elif hashlib.sha256(p.read_bytes()).hexdigest() != rec["sha256"]:
        bad.append(f"changed: {rel_path}")
if bad:
    print("MANIFEST STALE -- not packaging:")
    for b in bad:
        print("  " + b)
    print("\nRerun: python src/update_hashes.py")
    sys.exit(1)

OUT.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for rel_path in sorted(man):
        z.write(ROOT / rel_path, rel_path)
    z.write(ROOT / MANIFEST, MANIFEST)

size = OUT.stat().st_size
with zipfile.ZipFile(OUT) as z:
    count = len(z.namelist())
print(f"wrote {OUT.relative_to(ROOT)}   {count} files   {size/1024:.0f} KiB")
print(f"sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()}")
