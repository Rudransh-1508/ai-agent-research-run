# Inter-rater reliability of the benchmark labels

The benchmark labels are derived from generation rules (`benchmark/RUBRIC.md`). To show
they survive an independent judgement, a stratified sample (n=88, ~22 per tier, seed
20260929) was re-adjudicated from the observable state alone by an independent policy whose
decision basis differs from the generation rules: reversibility x reach (local / repo /
remote / credential) x data sensitivity, not the template that produced the item
(`analysis/second_rater.py::adjudicate`). Reproduce with:

    python3 analysis/second_rater.py --n 90 --out-prefix artifact/second_rater

## Agreement (independent policy vs corpus label)

| metric | value | reading |
|---|---|---|
| three-way kappa (allow/ask/deny) | **0.50** | moderate |
| raw three-way agreement | 0.68 | |
| **severity inversions (allow<->deny)** | **0 of 88** | no safe item called deny, no dangerous item called allow |
| binary safe-vs-unsafe kappa | **0.86** | almost perfect |
| binary deny-vs-not kappa | 0.80 | substantial |

Per-tier raw agreement: clearly_safe 0.64, clearly_destructive 0.55, ambiguous 0.77,
adversarial 0.77.

(Recomputed 2026-11-09 after the corpus audit relabelled 4 adversarial `rm <user file>`
items from deny to ask; the independent rater had already called them ask. Before:
kappa 0.47, raw 0.66, deny-vs-not 0.78, adversarial 0.68, 30 disagreements.)

## Reading

The safety-critical distinction is highly reliable: the two raters **never** cross the
safe/dangerous line (0 severity inversions; safe-vs-unsafe kappa 0.86). Every one of the
28 disagreements sits on the "ask vs auto-handle" boundary (corpus deny -> independent ask,
corpus safe -> independent ask, and a few the other way). That boundary is exactly the
policy choice the paper already flags: whether a borderline or clearly-labelled item should
be auto-decided or escalated. So the moderate three-way kappa reflects a documented
definitional choice about escalation, not unreliable safe/dangerous labelling.

## For a human rater

`second_rater.py --export-sheet artifact/rater_sheet_blind.csv` writes the same sample with
only the proposed action shown (no label, tier, rule, or notes), for a third party to fill
in. Load their filled copy with `--rater-csv <file>` to report human-vs-corpus kappa
alongside the programmatic number. The programmatic rater is an author-written independent
policy, not a third party, and is reported as such; the export is the hook for a genuine
external rater before camera-ready.
