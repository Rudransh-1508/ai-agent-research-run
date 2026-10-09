# GTEP assessment and revision notes

## Assessment

GTEP is the appropriate AAMAS area: the primary contribution is an economic model of strategic agents, bounded contracts, and endogenous retained information. The official 2027 call explicitly includes information design and economic models of AI agents. Source: https://warwick.ac.uk/fac/sci/dcs/aamas2027/calls/call-for-main-track/ (checked 9 October 2026).

My subjective assessment of the revised draft is **6/10 overall: borderline, with a plausible weak-accept case**, and **8/10 for GTEP fit**. These are editorial judgments, not official review scores. A defensible acceptance probability cannot be inferred from the paper alone; reviewer expertise, novelty judgments, proof scrutiny, and competition remain unknown. No calibrated percentage is available.

The strongest case is the combination of a retained-alphabet constraint, a constructive noisy-outcome memory bound, a deviator-attribution bound under fixed-total payments, and reconstruction-optimal incentive geometry. The main reviewer risk is whether this combination constitutes enough new theory beyond standard minimax/TV duality, information inequalities, and covering-code facts. The revision makes that distinction explicit instead of presenting every supporting tool as novel.

## Changes implemented

- Reframed the introduction around independently operated strategic agents and an explicit settlement evidence constraint.
- Separated exact outcomes, noisy outcomes, dominant-strategy implementation, Nash implementation, fixed-total payments, and deferred settlement.
- Qualified the threshold-block constant as a small-cost asymptotic comparison; retained finite-size rounding.
- Restricted the flatness equivalence to the dominating-code regime. Unrestricted small-dimensional claims remain tied to their certificate chain.
- Clarified that strict cost inequalities are required for unique implementation, and fixed-T repeated memory remains linear in team size.
- Corrected the empirical comparison: both names and order change; Hamming error counts wrong agent labels, not information-theoretic bits; estimated margins describe the judge-induced channel.
- Removed the claim that finite-sample margin errors must be downward. The scoring script now states the limitation accurately.
- Corrected the authorship of Jewitt, Kadan and Swinkels and removed the inaccurate claim that related research always fixes monitoring.
- Moved cube illustrations to the supplement, preserved the official class, and used its intended Libertine/Biolinum/Libertinus fonts.
- Removed the literal placeholder submission ID. The real ID must be entered if the submission instructions require it.

## Validation

Executed successfully:

```sh
python src/verify_all.py
python experiments/threshold_tightness.py
python experiments/repeated_review.py
```

All three scripts reported passing checks. Logs are in `validation/`. These are numerical and construction checks, not an independent proof certification. The revision did not rerun model API experiments or every integer-program infeasibility run. Saved empirical results are reported with their limitations. Historical preregistration and solver claims are retained from the supplied materials rather than newly independently authenticated.

The compiled main paper has eight body pages and one reference page; the supplement has four pages. Both were rendered and visually inspected. Compilation has no undefined references/citations or overflowing text lines. The official class emits an existing incomplete-conditional warning. Neither prevents generation or produces visible clipping. Some supplied figures contain embedded Type 3 fonts; they were retained rather than redrawn with unverified data.

## Highest-value further work

1. Have a specialist independently check Theorem S1 and the certificate exclusions, and verify that the key results are not subsumed by bounded-contract/monitoring-design literature. This is the largest remaining soundness/novelty risk.
2. For a stronger empirical contribution, run a factorial comparison separating name removal and order shuffling, randomise reviewer roles across multiple tasks, and use a distinct judge plus held-out estimates. Measure incentive response only if an actual strategic effort-choice experiment is implemented. None of those new results is claimed here.
3. Strengthen the theory with a tighter memory constant, heterogeneous/correlated outcomes, or an online-memory analysis. These are new research problems, not changes that prose editing can honestly supply.

## Author action before submission

Review the mathematical changes and approve the final claims. Enter the actual submission ID where appropriate and check the submission form. Reconcile the full project's AI-use disclosure with the conference policy: this revision used an AI assistant for critical review, rewriting, source edits, and execution of supplied verification scripts. No new LLM experiment was run in this revision. This note does not establish how AI was used in the original research. Keep this author-facing note and validation logs out of the anonymous paper PDF.

## Building

Use the supplied official `aamas.cls` without changes. With a complete TeX installation:

```sh
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex
xelatex supplement.tex
xelatex supplement.tex
```

The original `tectonic -X compile main.tex` workflow is also documented in README.md but was not available for this verification. Required font packages include libertine, inconsolata, newtx and Libertinus math. Do not accept a build that silently substitutes fallback fonts.
