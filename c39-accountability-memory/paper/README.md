# C39 paper — build and status

**Target:** AAMAS 2027 main track, COINE. 8 pages excluding references, LaTeX
mandatory. Abstract 1 Oct 2026, paper 8 Oct 2026.

## Build

```
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

Builds clean (MiKTeX, 2026-09-15): no errors, no undefined references or
citations, longest remaining overfull box 8 pt. **11 pages total** — the
body (Sections 1–9) ends on page 8, references follow, and the appendix runs
to page 11. The body is therefore exactly at the 8-page limit; swapping in
the official AAMAS class will change the measure, so **re-check the body
length first and trim Section 5 or move proof detail to the appendix if it
spills**.

`main.tex` currently uses `acmart` with `sigconf,nonacm`. **Download the official
AAMAS 2027 class from the conference site and replace that one line** — all
content lives in `sections/`, so nothing else moves. `macros.tex` declares
theorem environments only if the class has not already defined them and does
`\let\Bbbk\relax` before `amssymb`, so the swap should not reintroduce the
`\Bbbk` clash.

Figures are LaTeX source, not images: `figures/frontier.tex` is pgfplots
(regenerate with `python run.py figures`) and Figure 2 is
inline TikZ. No image pipeline, no matplotlib dependency.

## Status

| File | State |
|---|---|
| `sections/00-abstract.tex` | final — 224 words |
| `sections/01-intro.tex` | final — contributions plus roadmap |
| `sections/02-model.tex` | near-final |
| `sections/03-elimination.tex` | near-final — Theorem 1 with full proof |
| `sections/04-onebit.tex` | near-final — the general-$n$ argument now points at Proposition 14 |
| `sections/05-threshold.tex` | near-final — the heart of the paper |
| `sections/05b-priors.tex` | **new** — §5.7: the threshold for a general prior (Thm 11) and the tilted-prior collapse (Cor 12) |
| `sections/06-agent-systems.tex` | drafted — unmeasured claims about summaries now scoped to what the theory supports |
| `sections/065-experiment.tex` | **new** — §7: compaction mechanisms measured against the frontier; two pre-registered predictions falsified and reported |
| `sections/07-related.tex` | drafted, fully cited — now opens with moral hazard in teams |
| `sections/08-limitations.tex` | near-final — limitation 1 rewritten now that the prior question is settled for the threshold |
| `sections/A-proofs.tex` | **complete** — Theorem 1 in full (Steps 1–5), both threshold lemmas with the case analysis, the shell bound, reproduction instructions |
| `refs.bib` | 18 entries, all cited; 7 marked `FIELDS INCOMPLETE` |

## The open technical item — CLOSED 2026-09-15

Appendix A.1 step 5 (minimising over reconstruction pairs for general odd $n$) is
written out and machine-checked. The argument: split the coordinates of a pair
$(a,b)$ into the $p$ positions with $(a_i,b_i) = (0,1)$ and the $m$ with
$(1,0)$; then $\E[\Delta_{a,b}(S)^-] = \tfrac12\E|R_{p+m}|$ for a sum $R_k$ of
$k$ Rademacher variables, $\E|R_k|$ is nondecreasing in $k$ by conditional
Jensen, and $p+m \le n$, so every pair is dominated by the antipodal one. It
needs no permutation averaging — which is what the old proof-order bug was
about — and no orbit enumeration. `verify_all.py` block E checks every step: the
Rademacher identity, its monotonicity, the bound over all $4^n$ pairs at
$n = 3,5$ and all $(p,m)$ orbits at $n = 7,9$, and feasibility of the minimiser.

## What still needs a human

1. **Author block** in `main.tex` (commented out) and author registration.
2. **The AAMAS class** — one line, see above.
3. **Seven `FIELDS INCOMPLETE` bib entries**: the binary-CEO log-loss paper
   (arXiv:1801.00435), multifold packings (arXiv:1902.00023), TRACE, TRACER and
   VICT (arXiv:2606.00611, 2608.29363, 2608.28128), the Chellali et al. survey,
   and the Bittensor free-riding CCS 2024 poster (DOI 10.1145/3658644.3691414).
   Each has its identifier; author lists, full titles and page numbers must come
   from the publisher record rather than be reconstructed.

## Reproducibility

From the repo root, in the pinned environment (`.venv310`: Python 3.10.11,
NumPy 2.2.6, SciPy 1.15.3):

```
python run.py verify          # archive integrity + 145 solver-free checks
python run.py audit           # every printed number vs its artifact
python run.py score           # pre-registered predictions, scored
python run.py figures         # regenerate the figures
python src/make_certificates.py   # once; the only step needing the MILP
```

`verify_all.py` is an independent reimplementation — it shares no code with
`kflat_theory.py` — and all 145 checks pass. The referee-facing description of
the package, including what is deliberately *not* verified, is in
`../ARTIFACT.md`. Build the submission zip with `python make_artifact.py`.
