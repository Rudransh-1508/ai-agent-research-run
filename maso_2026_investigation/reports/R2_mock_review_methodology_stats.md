# MASO 2026 — Mock Review R2 (Methodology/Statistics Skeptic)

**Paper:** "Do Classical Organizational Fault-Handling Results Hold for LLM Multi-Agent Systems? Measuring Organizational Fault Propagation and Containment in Agentic Workflows" (merged candidate "OrgResilience")
**Reviewer mindset:** Methodology/statistics skeptic, classical-MAS-literate.
**Date:** 21 Sep 2026
**Recommendation:** Reject (confidence 4/5)

---

## 1. Summary as I understand it

The authors build a fault-injectable organizational testbed on LangGraph around two workflows (tau2-bench retail refunds; a newly authored 12-tool/30-task IT incident domain), vary organizational structure (flat / 2-level / 3-level, ±sentinel, ±scarcity) as the independent variable, inject 5–7 "organic-style" semantic faults with known ground truth, and measure a new metric — Organizational Blast Radius (OBR), the fraction of seven typed organizational boundaries crossed by provenance-traced corrupted events — plus MTTD/MTTC, utility preservation, and a priced recovery-cost vector. Six containment policies (none, retry, verifier gate, checkpoint-rollback, sentinel quarantine + re-delegation, scripted-oracle human escalation) are compared on a cost–utility Pareto. Pre-registered hypotheses test transfer of Dellarocas & Klein (ICMAS 2000) unzippering and scarcity-backfire results, Hägg (1997) sentinels, and hierarchy-vs-flat resilience (Horling & Lesser 2004), with TOST equivalence testing (SESOI ±10pp) so that "classical prediction fails" is a designed-in outcome. The statistical plan: ~3,400 runs, continuous OBR as co-primary endpoint (d=0.65 at n=37/cell), within-instance pairing with McNemar, Holm/BH multiplicity control, deterministic ground truth primary, LLM-judge secondary (κ≥0.7 gate, 10% human audit), claims scoped to ≥25pp binary / d≥0.5 continuous effects.

## 2. Strengths (grudgingly)

- The statistical plan is more sophisticated than most agent-benchmark papers: exact power computations, instance-level pairing, GLMMs with random intercepts, Newcombe CIs, a pilot with blinded variance re-estimation, and an explicit trigger-verification step learned from AgentChaos. Someone on this team has run experiments before.
- Deterministic DB-state ground truth for primary endpoints (tau2 pattern) is the right call; confining LLM judges to one gated secondary DV is disciplined.
- The TOST/pre-registration instinct — designing "classical prediction fails" as a publishable outcome rather than null-hunting — is methodologically admirable *in intent*. The execution is another matter (W2 below).
- The cost–utility Pareto with priced human-oversight minutes is the right evaluation frame and matches what the classical literature (Kota et al. TAAS 2012) used.

## 3. Weaknesses — the rejection case, ranked

### W1 (fatal): The primary endpoint is not invariant to the primary independent variable

OBR = |boundaries crossed| / |B|. But the boundary inventory B is a *function of the treatment arm*. A flat structure has no delegation-hierarchy boundary to cross; adding a sentinel adds a monitor boundary; the human-escalation arm is the only arm where the human-agent boundary is exercised as designed. Comparing OBR across flat/2-level/3-level compares fractions with different denominators and different boundary composition — part of any "structure effect" on OBR is definitional, not empirical. This is a construct-validity failure at the core of the paper: the headline metric changes meaning under the headline IV. Additionally, OBR is an 8-level discrete fraction (k/7) that will be U-shaped in practice (faults either die at the origin boundary or propagate): the "continuous co-primary endpoint" power math (Cohen's d, beta regression) is mis-specified for a U-shaped ordinal outcome, and d is not interpretable on it. The entire power story rests on treating this variable as Gaussian-continuous.

### W2 (fatal): The advertised "designed-in falsification outcome" is statistically unreachable at the planned n

The paper promises TOST equivalence with SESOI ±10pp so that "classical prediction fails to transfer" is a publishable verdict. Arithmetic: for a paired binary difference at p≈0.5 with within-instance correlation ρ=0.5, the 95% CI half-width is 0.98/√n — i.e., **±15.5pp at I=40 pairs and ±13.5pp even at I=53 pairs**. The equivalence bound (±10pp) is *narrower than the confidence interval the design can produce*. Even if the true difference is exactly zero, the test cannot declare equivalence; reaching a ±10pp CI requires ≥96 pairs at ρ=0.5 and ≥134 at ρ=0.3 — 2–3× the planned instance budget. Every no-difference result therefore lands in the authors' own "inconclusive" bucket, and the outcome taxonomy (replicated / falsified / inconclusive) is unfalsifiable in the falsification direction. The paper's most novel advertised contribution — a *rigorous negative* transfer result — cannot be produced by this design. (All numbers recomputed from the standard paired-proportion variance formula; the plan's own power tables imply the same.)

### W3: Triggered-only primary analysis conditions on a post-treatment variable

The plan filters to runs where the injected fault actually manifested ("triggered-only, per-protocol on trigger"), with ITT as sensitivity. But manifestation is plausibly *caused by the containment arm*: a verifier gate suppresses hallucinated-argument manifestation; a sentinel detects earlier and changes downstream behavior. Conditioning on a post-randomization, arm-dependent event induces selection bias of unknown sign and size; the ITT analysis answers a different, diluted question and does not rescue it. The pilot gate "drop any fault with <70% trigger rate" makes it worse: reported effects become conditional on an arm-dependent event *and* on a fault-selection rule applied after seeing pilot data. Per-arm trigger rates must be reported and the estimand stated as a complainer/principal-stratum effect, or the primary analysis should be ITT.

### W4: Structure is confounded with mechanism and with scaffold budget

In the 2- and 3-level hierarchy arms, the supervisor role performs verification *even in the "no containment" arm* — that is what supervisors in the org wrapper do. So the "none" baseline is not mechanism-free across structures, and any structure main effect is partly a built-in-verification effect. Separately, flat vs 3-level arms differ in agent count, total prompt tokens, message count, and per-agent context length; there is no budget-matched scaffold control (e.g., a flat arm with equal agents/messages). "Organizational structure" effects are inseparable from scaffold complexity. τ-bench evidence (arXiv:2406.12045: pass@1 <50%, pass^8 <25% on retail) shows run-to-run and instance variance on this substrate is enormous — exactly the regime where uncontrolled scaffold differences masquerade as structure effects.

### W5: 100% fault prevalence makes detection operating characteristics unmeasurable

Every fault-cell run contains a fault. Sentinel and verifier mechanisms are therefore evaluated only at 100% prevalence: false-positive quarantine rates, precision, and collateral damage *at realistic fault rates* are never measured (no-fault cells measure overhead, not false positives under rare-fault regimes). MTTD/MTTC and the Pareto positions of detection-based mechanisms are base-rate-dependent quantities reported from a world where the base rate is 1.0. A sentinel that looks dominant here may be a false-positive catastrophe at 2% prevalence; the design cannot see this, and the paper's containment recommendations to practitioners rest on it.

### W6: Two workflows, one backbone, one framework cannot support the title's question

The title asks whether classical results hold "for LLM multi-agent systems." The evidence base is: one adapted single-agent benchmark (tau2-retail, where the "organization" is a wrapper splitting one agent into ~5 roles), one newly authored unvalidated 30-task domain, one primary model, one framework. Workflow is a 2-level fixed effect — workflow variance is unestimable, and the IT domain has no published baseline pass rates to anchor sanity. MAS-FIRE (arXiv:2602.19843) showed robustness rankings *flip across models* (RS 6.3% vs 70.6%); the plan concedes single-model scoping but the title and abstract do not. The honest title is "...in two workflows with one model on LangGraph," and at that scope the contribution is a benchmark paper, not a transfer test of classical theory.

### W7: The scripted-oracle "human" is an assumption, not a measurement

The human-escalation arm is a deterministic oracle with perfect policy knowledge, fixed latency, and bounded capacity, and it "sees only what the escalator surfaces" — so its performance is driven by an unstudied surfacing policy confound, and its Pareto position is set by an *assumed* price λ_h on oversight minutes. The project's own feasibility review flags this (R5: "oracle human too strong... makes C5 look artificially dominant"). The 80%-correct noisy variant is arbitrary: real human oversight errors are correlated, attention-dependent, and systematically biased toward accepting agent outputs (the automation-bias literature). As designed, the arm measures "an upper-bound automated checker we chose to price like a human." The headline human-vs-automated containment comparison — advertised as a first — is the paper's weakest evidentiary link.

### W8: The attribution-accuracy dial (CAND-3 axis) is circular

Degrading oracle attribution by mixing in *uniform-random* attribution assumes accuracy is a scalar and errors are unstructured. Real attributors err systematically — Who&When (arXiv:2505.00212) reports best-method 53.5% agent / 14.2% step accuracy with structured biases, some methods *below random*. Containment collateral damage depends on *which* agent is falsely blamed (a hub vs a leaf), not merely how often. The validation sub-study then places two real attributors on the synthetic curve by measuring their accuracy and reading off the predicted containment utility — i.e., it assumes the conclusion (accuracy alone determines downstream utility) in order to validate it. The derived threshold τ̂ is an artifact of the degradation model until re-derived under structured error models.

### W9: Multiplicity and the quietly pruned factorial

The merged claim set carries ~10 named hypotheses, 6 mechanism arms, 7 per-boundary OBR readouts, a 4-component cost vector, latency metrics, across 2 workflows — but the multiplicity families were designed for three *separate* candidate papers and were never re-consolidated for the merged claim list; "co-primary" endpoints are asserted without an alpha-allocation rule; and pre-registration is an "internal doc or OSF" gesture. Meanwhile the advertised factor cross (2W × 3S × ±sentinel × ±scarcity × 5–7F × 6M) is >1,000 cells; at ~3,400 runs that is ~3 runs/cell, so most advertised cells are silently dropped or estimable only through the mixed model — and which cells exist determines which claims survive. Provide the cell×run table or the claim list is not checkable.

### W10: The power chain rests on unestimated assumptions

Pairing power assumes ρ=0.3–0.5, to be estimated from a 10-instance pilot (ICC confidence intervals at n=10 are uselessly wide); the d≥0.5 scoping is justified from non-analogous effects (a simulation-only containment result, 46.2%→99.4%; adversarial-fault robustness swings). If ρ=0.2 or the true continuous effect is d=0.35, the headline contrasts sit at power 0.3–0.6 and the paper's interesting claims — H4, where classical predictions *break*, plausibly a modest effect — are exactly the ones this design cannot see. The reliability sub-study (10 instances × 8 seeds) cannot estimate seed-level variance components with usable precision. Finally, multi-day runs against provider-side model drift with no stated time-randomization of arm assignment invite temporal confounding.

### W11: "Organic" faults that are injected are not organic

The organic-vs-adversarial distinction is about intent framing, not distribution: fault type, site, timing, and magnitude are experimenter-chosen, independent, and uniformly placed, whereas real organic faults cluster on hard instances and co-occur. This is fine for conditional-propagation claims but the paper's ecological-validity framing ("distinct from adversarial/attack framings") oversells it — and combined with W5, the design says nothing about how these mechanisms behave under the natural fault distribution they are nominally about.

## 4. Questions to authors

1. Define B per arm. If the boundary inventory differs across structure arms, in what sense is OBR comparable across your primary IV? Will you report absolute corrupted cross-boundary event counts and per-boundary indicators on a fixed, arm-independent inventory?
2. Show the TOST power calculation: at I=40 and ρ=0.3, what is the probability of declaring equivalence when the true difference is zero? If it is ~0, which planned verdict does H4's "prediction fails" claim actually rest on?
3. Report per-arm fault trigger rates from the pilot. If trigger depends on arm, how do you justify triggered-only primary analysis against selection bias, and what is the principal-stratum estimand?
4. In the 3-level "no containment" arm, does the supervisor verify? If yes, what exactly distinguishes "structure" from "mechanism" in your design?
5. What fault prevalence do you assume in deployment, and what are your sentinel/verifier false-positive quarantine rates at that prevalence?
6. Provide the actual cell×run matrix. Which advertised cells were dropped, and which claims die with them?
7. Why should a deterministic oracle with perfect policy knowledge be interpreted as "human escalation" rather than as a priced upper-bound automated mechanism — and how does the Pareto move under λ_h ±50%?
8. Re-derive τ̂ under a structured attribution-error model (recency-biased, hub-biased false blame). Does the threshold move?

## 5. Score

**Reject.** Confidence 4/5. The engineering and statistical *ambition* are real, but the primary endpoint is not invariant to the primary IV (W1), the flagship falsification outcome is underpowered by construction (W2), and the human and attribution-dial arms measure assumptions (W7/W8). These are design-level, not polish-level, problems.

## 6. Single change that would most improve my score

Fix the estimand layer before running anything: redefine OBR on a fixed, arm-independent boundary inventory (absolute corrupted-event counts + per-boundary indicators), and re-power the confirmatory tests to match — either ≥100 paired instances for the binary/equivalence claims or an honest demotion of all binary and TOST claims to exploratory with the continuous endpoint as sole confirmatory outcome. One sentence version: **make the metric invariant to the treatment and the sample size adequate to the SESOI.**

---

## ORCHESTRATOR NOTE

**Survive — wounded, fixable in the design doc before any runs.** None of W1–W8 touches the testbed, the fault library, or the differentiation obligations; all are repairable at the pre-registration stage. The precise saving revision: (1) redefine OBR as absolute corrupted cross-boundary event counts plus per-boundary crossing indicators on a boundary inventory present in every arm (kills W1); (2) make the continuous endpoint sole confirmatory outcome, demote binary containment and all TOST claims to exploratory with CIs — or raise the instance budget to ≥100 pairs for the classical-transfer hypotheses (kills W2, W10); (3) ITT primary, triggered-only secondary, per-arm trigger rates reported (kills W3); (4) add one budget-matched flat-scaffold control arm and strip verification from the hierarchy "none" arm (kills W4); (5) add a low-prevalence evaluation block (e.g., 5% fault rate) for sentinel/verifier false positives (kills W5); (6) retitle to scope ("two organizational workflows, one backbone") and rename the human arm "priced oracle escalation upper bound" (defuses W6, W7); (7) add a structured-error sensitivity analysis for the attribution dial or drop the CAND-3 axis (defuses W8). With (1)–(4) done, this reviewer moves to weak accept; the candidate remains the strongest of the merged set.
