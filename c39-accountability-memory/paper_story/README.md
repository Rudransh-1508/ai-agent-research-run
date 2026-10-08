# C39 for AAMAS 2027 (GTEP), technical draft with a short story-led opening

`main.tex` (body ends on page 8) and `supplement.tex`. Body, all with proofs: model and
settlement game, strategic compaction (Prop 2), payment elimination (Thm 1), linear memory
(Thm 2) and its tightness up to pi ln 2 via one threshold bit per block (Thm 3), budget
balance (Thm 4), cost of implementation and the designer (Props 5-6), repeated tasks:
per-task settlement adds nothing (Prop 7) and deferred settlement with review records
(Thm 5), exact outcomes (Thms 6-7), measured mechanisms. The supplement holds Theorem S1
(every full-support prior) with proofs, the certificate chain and extra figures/tables.
Verification scripts: `experiments/threshold_tightness.py`, `experiments/repeated_review.py`.
Content and numbers come from `revision_2026-09-30/merged_candidate/`, which is not modified.
`archive_storyled/` holds the earlier story-led version.

Build (from this folder):

    tectonic -X compile main.tex
    tectonic -X compile supplement.tex

`figures/g_*.pdf` (main) and the other PDFs (supplement) are vector exports of the
interactive explainer, re-exported with larger labels for print. Layout uses `acmart`
sigconf/anonymous, the class the official AAMAS template builds on; move the body into the
official `aamas` class before submitting.
