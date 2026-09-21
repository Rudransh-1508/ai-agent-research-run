# OrgResilience — Pilot Study Plan

**Date:** 22 Sep 2026 · **Deadline:** 10 Oct 2026 (18 days) · **Parent document:** `FINAL_RECOMMENDATION.md` (v3, post-audit)
**Purpose of the pilot:** the pilot is NOT a mini-version of the paper. It is a measurement-instrument validation and variance-estimation exercise whose only job is to decide — with pre-committed rules — whether the main study runs, and in what descoped form. Pilot data are NOT pooled into the confirmatory analysis if any design element changes afterward (internal-pilot discipline, per `audit2/../reports/W2_statistics.md`).

---

## 1. What the pilot must establish (six estimands)

| # | Estimand | Why it gates the main study | Pass criterion |
|---|---|---|---|
| E1 | **Baseline fidelity** — no-fault pass rate of the org-wrapped tau2-retail vs published single-agent numbers | All effects are relative to baseline; a broken baseline invalidates every cell (F-A risk R1) | Within ~10pp of single-agent retail reference |
| E2 | **Fault trigger rates** — fraction of injections that actually manifest, per fault type (agent death; corrupted handoff; [memory staleness if built]) | Untriggered faults silently bias effects toward zero (AgentChaos lesson) | ≥70% per fault type, else redesign or drop the fault |
| E3 | **Boundary-tracer labeling agreement** — automated corrupted-event/boundary-crossing labels vs human labels | The propagation metric is attackable if labeling is unreliable (F-A risk R3) | Cohen's κ ≥ 0.7 on structured channels; else restrict metric to tool/DB/memory boundaries + handoff entity-matching and disclose |
| E4 | **Rollback determinism** — joint LangGraph-checkpoint + tau2-DB snapshot restore | The rollback containment arm is meaningless without it (F-A risk R4) | Deterministic joint restore in a forced-fault test; else rollback arm degrades to "restart-subtask" (honest, weaker) |
| E5 | **Variance components** — instance-level variance, seed ICC, within-instance correlation ρ under pairing; per-cell effect-size estimates | Determines final instance count and whether binary endpoints survive the tau2 noise floor (audit: paired noise up to +18pp at n=100; binary contrasts need n≥250/cell — 2606.20695, FULL TEXT) | Blinded variance re-estimation completed; final I fixed before main runs |
| E6 | **Throughput & unit cost** — runs/hour at target parallelism, rate-limit behavior, actual tokens/run vs the 150k-in/20k-out assumption | Wall-clock, not money, is the binding constraint | ≥ target throughput to finish main matrix in days 12–16; else descope ladder engages |

**Secondary pilot measurement (cheap, high value):** the **natural-attenuation / committedness base rate** (A10-H9) — with no containment mechanism, what fraction of injected faults self-mask vs propagate? This is both a main-study control arm and a sanity check on whether containment effects can be measured at all above the attenuation floor.

## 2. Pilot design

### 2.1 Cells (deliberate subset of the main matrix, extremes only)

depth {2, 4} × handling {none, sentinel quarantine+re-delegation} × scarcity {abundant, scarce} × detector {oracle, LLM-semantic} = **16 cells**
- 10 task instances × 2 seeds per cell = **320 runs**
- No-fault baselines: depth {2,4} × scarcity {2} × 10 instances = **40 runs**
- Natural-attenuation probes (no mechanism, both faults, depth 3): **20 runs**
- Reliability sub-study (seed variance / pass^k): 10 instances × 8 seeds in 2 key cells = **160 runs**
- **Total ≈ 540 runs** (~15–20% of the minimum main matrix; cost ≈ $30–55 at GPT-5-mini/DeepSeek class — non-binding)

Rationale for extremes-only: the pilot needs variance and trigger estimates at the corners of the design space (where failure is most likely), not coverage of the middle.

### 2.2 Faults in pilot
- F5 agent death (API-layer abort; required for H1/D&K-comparability) — trigger check: no response within timeout.
- F2 corrupted handoff (semantic; required for the detector dial) — trigger check: downstream agent acts on mutated value (entity match against fault payload).
- F6 memory staleness only if the shared-scratchpad arm is built by day 8; otherwise deferred.

### 2.3 Human labeling
20 pilot traces sampled stratified by fault type × depth; 2 annotators; adjudicate disagreements; compute κ for the automated boundary tracer (E3). Annotators blind to condition.

### 2.4 What the pilot does NOT include
No human-escalation arm (load-dependent reviewer model is built days 8–10, piloted only if ahead of schedule). No verifier-gate arm (added to main study only if Gate 1 passes cleanly). No LLM-judge secondary DV (rubric validation is a day 16 task if used at all).

## 3. Timeline (days 1–11)

| Days | Work | Output |
|---|---|---|
| 1–2 | Org wrapper on tau2-retail (2-level first); event/boundary tracer with provenance pointers; DB snapshotting | E1, E3 instrumentation |
| 2–3 | Injection harness for F5/F2 with automated trigger checks; forced-fault rollback test | E2 instrumentation, E4 |
| 3–4 | 30 no-fault baseline episodes (E1); 20-run smoke per fault (E2); 100-run throughput test (E6) | **GATE 1 inputs** |
| **4** | **GATE 1 (go/no-go on build)** — criteria in §4 | go / descope / stop |
| 5–8 | Full pilot matrix (540 runs); sentinel mechanism; scarcity flag; detector dial (oracle + LLM-semantic) | E2, E5, E6 data |
| 8–10 | Human labeling of 20 traces (E3); load-dependent reviewer model (stretch) | κ estimate |
| 9–11 | Pilot analysis: variance components, trigger-rate CIs, effect-size estimates, attenuation base rate | **GATE 2 inputs** |
| **12** | **GATE 2 (post-pilot descope decision)** — pre-committed ladder in §4 | frozen main-study config |
| 12 | Finalize pre-registration (OSF timestamp) with pilot-informed power analysis | pre-registration locked before main runs |

## 4. Decision rules (pre-committed)

### Gate 1 — day 4 (build viability)
- E1 fails (baseline >10pp below reference) → fall back to shallower split (frontline + supervisor only); if still failing, **stop the OrgResilience build and switch to the fallback paper** (attribution-threshold study, ~1,200 runs, per `W2_feasibility_B.md`).
- E2 fails for a fault → redesign injection once; still <70% → drop the fault (drop order: F6, then F2 — F5 is non-negotiable, H1 needs it).
- E4 fails → rollback arm becomes restart-subtask; disclose.
- E6 fails (throughput) → engage descope ladder one level immediately.

### Gate 2 — day 12 (post-pilot scope)
Pre-committed descope ladder (cut in this order, per the audit-corrected plan):
1. Workflow 2 (IT incident) — already conditional; confirm cut.
2. Memory-staleness arm (F6).
3. Human-escalation arm (if reviewer model unbuilt or κ/throughput marginal).
4. Reviewer-minutes currency (keep token + tool-call budgets).
5. Detector levels 3 → 2 (drop syntactic, keep oracle + LLM-semantic).
6. Depth levels {2,3,4} → {2,4} (H1 becomes a two-point contrast; weaker but powered).

**Never cut:** instances below the pilot-derived power floor; the natural-attenuation control arm; within-instance pairing.

### Power re-estimation rule
Using pilot ρ and variance: if binary containment contrasts require >250/cell and the budget cannot reach them, binary endpoints are demoted to exploratory and the continuous endpoints (recovery-cost inflation ratio; boundary-crossing counts) become sole confirmatory outcomes. This is decided on day 12 with pilot numbers, not during analysis.

## 5. Pilot analysis plan

- Trigger rates: Wilson 95% CIs per fault type; primary main-study analysis will be ITT with per-arm trigger rates reported (triggered-only analysis is post-treatment selection — R2 reviewer correction).
- Variance: random-effects decomposition (instance, seed, cell); ICC; ρ for paired design; blinded re-estimation of required I.
- Attenuation: proportion of injected faults with zero boundary crossings beyond origin under no-mechanism arm, with CI; if attenuation is very high (>80%), expect small treatment effects and re-power accordingly.
- Labeling: Cohen's κ + per-boundary-type agreement breakdown.
- No hypothesis tests on treatment effects in the pilot — estimation only.

## 6. Pilot deliverables (day 12)

1. Frozen main-study configuration (post-ladder).
2. Final power analysis with pilot-derived variance (replaces all F1/F-C estimates).
3. Pre-registration (OSF timestamp): hypotheses H1-transfer, H3′, H2′, H5; endpoints; analysis plan; descope record.
4. Instrumentation validation note (E1–E6 results) — appendix material for the paper.
5. Go/no-go record for the fallback paper.

## 7. Pilot-specific risks

| Risk | Mitigation |
|---|---|
| Pilot eats build time (540 runs while arms still under construction) | Pilot matrix uses only arms built by day 5; anything later is main-study-only |
| Rate limits during pilot distort E6 | Run throughput test at 2× target parallelism briefly; measure provider limits directly; batch API fallback |
| Annotator disagreement on semantic corruption | Restrict metric to structured channels per E3 fallback; disclose restriction in paper |
| Pilot looks "good enough" and temptation to skip Gate 2 descope | The ladder is pre-committed; this document is the commitment device |
| tau2 version drift | Pin τ³ ≥ v1.0.1; record exact version in pre-registration |

## 8. Relationship to the main study

The pilot validates the instrument; the main study (days 12–16, ~2,500–4,000 runs) tests the hypotheses. Everything the pilot establishes is reported in the paper's appendix as instrumentation validation — which is itself a differentiator against CtC (simulation-only) and DamageFlow (no power analysis, no multiplicity control).
