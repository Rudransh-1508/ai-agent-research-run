# S4-ATTACK-D1 — Adversarial Attack on Direction D1

**Date:** 2026-09-21
**Target (as assigned):** "Scarcity-induced containment backfire in organizational LLM-MAS, refined as: budget-unaware containment backfires under scarcity while budget-aware containment does not; we map the sign-reversal crossover parametrically (token/tool/latency/reviewer budgets) in tool-executing multi-agent organizations with semantic faults."
**Stance:** hostile. Goal is to find fatal problems while cheap.
**Inputs:** audit2 A1–A12 read (A3, A4, A5, A6, A7, A9, A11, A12 in full); FINAL_RECOMMENDATION; wave-1 E4/E5/R1/W2 reports as cited therein.
**Independent verification this session (not delegated):** Xiang SSRN 7348298 full abstract re-pulled from Crossref (finding (iv) quoted verbatim below); SHO arXiv:2606.01416 abstract re-pulled from arXiv; Kota TAAS 2012 all-Adapt/k-Adapt passage re-quoted from the local full-text artifact (`raw/r3_review/kota_taas2012.txt`, lines 1485–1487, 1827–1830). Everything else marked with the verification level of the audit lane that established it.

---

## 0. VERDICT

**WEAK as stated — one notch above COLLIDED.** The stated headline ("budget-unaware backfires, budget-aware does not, crossover mapped parametrically") is not a refinement of the literature; it is a *citation* of it: Kota et al. TAAS 2012 published exactly this contrast with a parametric sweep, and Xiang (SSRN 7348298) published the sign reversal on the LLM substrate. The full quadruple conjunction (organizational decision-rights structure × propagating semantic faults × real tool-executing LLM MAS × priced budget-aware-vs-unaware contrast) remains verifiably empty, so the direction is not strictly collided — but what survives is a measurement/boundary-mapping contribution plus one non-classical mechanism (detection error), not the stated claim. D1 survives only after amputating its own headline.

---

## 1. The collision stack against D1 (all load-bearing items, verification marked)

| # | Work | What it occupies of D1 | Verification |
|---|---|---|---|
| 1 | **Kota, Gibbins & Jennings, ACM TAAS 2012** (10.1145/2168260.2168261) | **The refinement itself.** R (reorganisation load = recovery's consumption of task capacity) swept 0→0.9 (Fig. 4c). Verbatim from full text: "the fall in the performance of k-Adapt is gradual and minimal, while it is drastic in all-Adapt. In fact, for higher values of R, the profit of all-Adapt goes below 0, meaning the cost is more than the reward obtained… meta-reasoning is a crucial aspect in an adaptation process and cannot be ignored… k-Adapt is always close to free-Adapt." all-Adapt = budget-unaware maximal recovery → net-negative under scarcity; k-Adapt = cost-aware selective recovery → tracks the zero-cost upper bound. Contrast + parametric sweep + design prescription, in an agent organization, 2012. | FULL TEXT (A5/E5; passage re-verified this session from local PDF text) |
| 2 | **Dellarocas & Klein, ICMAS 2000** (10.1109/ICMAS.2000.858440) | Budget-unaware containment (sentinel/EH) slightly worse than survivalist under subcontractor scarcity, with mechanism (early detection → re-announcement storms the bottleneck). The candidate's own anchor. | FULL TEXT (E5/A5) |
| 3 | **Xiang, SSRN 7348298** (2026-08-27) | The sign reversal **on LLM agents**, pre-registered, 1,330 runs, 9 models, Holm-corrected. Verbatim from abstract: "The gate's effect changes sign with the verification budget: with no budget it reduces accuracy by 0.315, and the budget-by-gate interaction (DiD = +0.456 [+0.297, +0.625]) is the largest effect we measure… only when the system can afford to verify." Single-agent, synthetic fault-diagnosis, verification budget only; no budget-aware gate variant. | ABSTRACT ONLY (re-verified this session via Crossref; full text unread — residual risk, §7) |
| 4 | **Self-Healing Orchestrators** (arXiv:2606.01416) | Matched recovery-budget sweep on tool-augmented LLM system: budget-aware targeted recovery beats retry-only and full replanning **at every tested budget, largest gap at the tightest** (94.0% vs 85.3%/88.2% at one attempt). Opposite-sign to the backfire; pre-answers D1's budget-aware arm. | ABSTRACT ONLY (re-verified this session via arXiv) |
| 5 | **Metastable-failure canon**: Bronson et al. HotOS 2021 (10.1145/3458336.3465286); Huang et al. OSDI 2022; Isaacs et al. HotOS 2025; MSF-Model SRDS 2024 | H3's exact mechanism in distsys: recovery traffic sustains overload; same policy harmless at low utilization, catastrophic at high. Stable vs metastable-vulnerable boundary *is* a parametric crossover map. | PARTIAL (HotOS 2021: abstract + author blog) / FULL TEXT (OSDI 2022 USENIX page) / ABSTRACT (HotOS 2025) — per A6 |
| 6 | **Google SRE Book ch. 22** (Ulrich 2016) | Textbook: retries under overload melt backends; **retry budgets = budget-aware containment as standing doctrine**; footnote 110 assigns the crossover simulator as a reader exercise. | FULL TEXT (A4/A6, quoted) |
| 7 | **Mehan, Retry Amplification** (SSRN 2026, 10.2139/ssrn.6313332) | Explicit empirical sign reversal of a recovery mechanism under stress: retries 25% *worse* than no-retry under correlated failure (41.5% vs 55.4%); proposes Adaptive Retry Budgeting. Weak venue, single author, simulation. | ABSTRACT ONLY (A4/A6 via Crossref) |
| 8 | **BRA-Audit** (arXiv:2608.14668) | Real LLM MAS (AutoGen), audit-point placement under fixed audit-call budget + localized rollback; monotone gains with audit ratio ρ, but **false positives 0%→12–16% harm benign trajectories** — containment hurting healthy work, measured, on real LLM MAS. One scarcity ablation away from D1. | FULL TEXT (A11) |
| 9 | **Arslan, audit-capacity triage** (arXiv:2608.06949) | 9-agent LLM pipeline, audit capacity explicitly varied: coverage collapses 100%→65.6% under overload; **risk-ordered queueing (= budget-aware containment policy) recovers coverage to 91.7% under the same capacity**. Degradation, not backfire — but the "budget-aware rescue under scarcity" pattern demonstrated in multi-agent LLM. | ABSTRACT ONLY (A11) |
| 10 | **Oversight Has a Capacity** (arXiv:2606.08919) | Inverted-U: more escalation can reduce safety with a fatiguing reviewer; "the guard's escalation policy spends it." Owns the reviewer-budget sign-reversal *shape*; modeling-only, single-agent gating. | ABSTRACT ONLY (A4/A7) |
| 11 | **Halverson pair** (SSRN 7270819 + 7265602, 2026) | LLM-native retry-amplification accounting (IAF = LLM-pipeline RAF; ECI); pre-registered budget×retry ablation; recovery at ~2× hidden cost. Occupies "recovery consumes LLM budget, measured per-attempt." | ABSTRACT ONLY (A6) |
| 12 | **FTDI** (SSRN 6387100; now ESWA 10.1016/j.eswa.2026.134164) | Budget-gated tiered recovery for LLM MAS code-gen, motivated by "low-yield retries when interaction rounds and costs are constrained." The budget-aware design response, in MAS, now journal-published. | ABSTRACT / METADATA (A3/A6/A9) |
| 13 | **Tambe JAIR 1997; Kaminka & Tambe JAIR 2000** | Cautious (maximal containment) team: 10–20× messages, infeasible beyond 6–7 agents under fixed compute; balanced dominates. Monitoring-selectivity theorems. Classical cost-containment curve with feasibility cliff. | FULL TEXT (A5) |

---

## 2. Question (a): After Xiang + D&K + Kota, what EXACTLY is left?

Decompose D1 into its four constituent claims and classify each:

**C1 — "Budget-unaware containment backfires under scarcity" (mechanism drops below no-mechanism).**
Occupied on BOTH sides of the substrate boundary. Classical: D&K config 2 (FULL TEXT), Kota all-Adapt net-negative (FULL TEXT, stronger than D&K), Tambe feasibility cliff (FULL TEXT). Distsys: metastable failures, SRE ch. 22, Mehan's 25%-worse-than-no-retry. LLM substrate: Xiang finding (iv). **Left: nothing, as a phenomenon.** Only the specific cell "in an organizational LLM-MAS with propagating semantic faults" is unmeasured.

**C2 — "Budget-aware containment does not backfire."**
Occupied classically AND on the LLM substrate AND partially in LLM MAS. Kota's k-Adapt ≈ free-Adapt across the whole R sweep *is* this claim with its design prescription. SRE retry budgets are this as doctrine. SHO shows the stronger result (budget-aware recovery helps *most* at the tightest budget). FTDI (MAS, journal-published), Arslan's risk-ordered queue (9-agent pipeline), AVA, BRA-Audit all instantiate budget-aware containment under constraint. **Left: nothing, as a design finding.** "Make containment budget-aware" is 2026 consensus, not a result.

**C3 — "We map the sign-reversal crossover parametrically."**
Partially occupied everywhere it has been tried: Kota swept R ∈ [0, 0.9]; Xiang swept verification budget; SHO swept recovery attempts; the metastable literature characterizes the vulnerable-region boundary formally (HotOS 2021/2025, OSDI 2022). **Left:** a *multi-currency* map (token/tool/latency/reviewer in one design) and — the only scientifically interesting residue — the crossover *location* as a function of **detection quality** under semantic faults. No classical model has a detection-quality parameter (classical detection was free and perfect — crash faults; distsys detection is error codes). A4's mechanism inventory (§3.2) is the map: congestion (classical), static budget partition (arithmetic, open for LLM workloads), redeployment competition (D&K's, organizational), detection-error interaction (no classical analogue), reviewer fatigue (human-factors classical).

**C4 — The setting: tool-executing multi-agent organizations with semantic faults.**
Verified empty in full conjunction: A3/A4 negative sweeps; A9's 20-claim table (best cell = claim 14, PARTIAL, classical-only occupancy); A11 §4.1; A12's citation graph (~1,060 post-2024 citers of 15 anchors; the {faults}×{structure}×{resources} triple is empty). But every *relaxation* is occupied: single-agent LLM (Xiang, SHO, Halverson), non-organizational LLM MAS (FTDI, BRA-Audit, Arslan), classical organization (D&K, Kota, Tambe). The conjunction is one experiment away for at least three groups (A9 §4).

**Net answer to (a):** what is left is exactly (i) the within-one-experiment conjunction (which no single paper has run), (ii) the detection-error/false-positive-quarantine mechanism and its effect on crossover location (no classical analogue anywhere), (iii) the reviewer-budget arm as a post-fault containment race in a propagation setting (A7: experimentally unoccupied), and (iv) genuine outcome suspense created by SHO's opposite sign. Everything else in the stated direction is occupied.

## 3. Question (b): Is "multi-agent organizational setting" enough?

**No — as the sole differentiator it is a trivial-extension reject.** The hostile read writes itself: "Xiang plus more agents" (the sign reversal is already on the LLM substrate), or equivalently "Kota with LLMs substituted for simulated agents" (the refined contrast is already published with a parametric sweep). The generic "first classical transfer test" framing is separately occupied (Resilient Consensus 2606.15024, Loop-Back Authority 2609.14767, Leadership-as-Control 2606.19111), and La Malfa et al. pre-staked the call. Note also that "multi-agent" *alone* is eroded even on the LLM substrate: FTDI, BRA-Audit, and Arslan are all multi-agent LLM systems with budget×containment manipulations. The differentiator cannot be agent count; it must be **organizational decision-rights structure + propagation**.

The organizational setting is load-bearing — not decorative — in exactly three places, and D1 should be rebuilt around them:
1. **False-positive quarantine collateral under propagation.** With semantic faults, detection is costly and errs; a false-positive quarantine at one node strands healthy downstream dependents — organizational collateral that single-agent Xiang cannot express and classical crash-fault work never faced (detection was perfect). This is the one backfire mechanism with no classical analogue (A4 mechanism 4).
2. **Redeployment competition.** D&K's actual backfire mechanism (re-announcement competing for scarce replacement capacity) is inherently organizational; whether it reappears when "replacement capacity" = LLM agent instances with warm context (not fungible fresh agents) is a real, classical-theory-straining question.
3. **Shared oversight queue.** A reviewer budget is an organizational resource; queue-interference across concurrent faults (one fault's escalation delaying another's containment) is untestable in single-agent settings and unmeasured anywhere (A7 §5).

Where the org setting changes no mechanism (e.g., token-budget partition on a single chain), it is decorative and Reviewer 2 will say so.

## 4. Question (c): Does the budget-aware/budget-unaware refinement survive SHO?

**It survives SHO logically but is deflated by it — and its deeper problem is Kota, not SHO.**

- *Consistency:* SHO is evidence *for* D1's budget-aware half (helps most at tightest budget). No contradiction.
- *Wound 1 — suspense removed:* the budget-aware arm is now confirmatory of SHO (single orchestrator), FTDI (MAS), and Arslan (MAS pipeline). Running it again in an org setting is replication.
- *Wound 2 — the backfire was sought and not found:* SHO ran the matched budget sweep and no mechanism dipped below baseline. D1's budget-unaware arm must therefore explain what its design contains that SHO's retry-only arm lacked. The candidate answers are precisely the three organizational mechanisms of §3 (congestible shared resource, false-positive quarantine, redeployment competition) — none present in SHO's single-orchestrator setting. If D1's design operationalizes scarcity as a plain per-run token cap on a non-congestible pipeline, the likely outcome is SHO's (no backfire), and the paper reports a null that reads as a failed replication of Kota.
- *Wound 3 — the refinement is a citation:* A3 (§5) proposed "budget-unaware backfires, budget-aware doesn't" as the defensible sharpening of H3. Kota 2012 published that exact contrast (all-Adapt vs k-Adapt across R), with the meta-reasoning prescription, 14 years ago. The refinement converts H3 from a false-as-stated hypothesis into a transfer test of a known classical contrast — fine for MASO's classical-MAS pool *if framed as such*, fatal to any framing as a discovery.
- *The asymmetry that actually decides D1's fate:* if D1 finds the backfire, reviewers say "Kota and Xiang already showed this"; if it doesn't, reviewers say "SHO already showed this." **The paper wins only if it explains WHEN** — crossover location as a function of mechanism, budget currency, and detection quality. That is a boundary-mapping/measurement contribution. It is real, it is unoccupied, and it is much smaller than the stated headline.
- *Confound warning (from A9 §5):* Xiang's gate benefit concentrated in weak systems (+0.31 below 0.60 baseline vs +0.01 at 0.80–0.95). Scarcity backfire may be entangled with a capability×containment interaction (cf. Two Calls Beat Five Agents, 2607.26922: under capability scarcity, verification actively hurts). D1's design must separate budget scarcity from capability scarcity or the crossover is uninterpretable.

## 5. Question (d): What Reviewer 2 writes (mock, classical-MAS pool, hostile)

> **Summary.** The authors inject semantic faults into tool-executing LLM multi-agent organizations and measure when containment mechanisms (verifier gates, sentinel quarantine, rollback, human escalation) help or hurt as token/tool/latency/reviewer budgets tighten. Headline: budget-unaware containment reverses sign under scarcity while budget-aware containment does not; the crossover is mapped parametrically.
>
> **Weaknesses.**
> 1. **The headline is 26 and 14 years old.** Dellarocas & Klein (ICMAS 2000) showed sentinel EH services *worse* than survivalist timeout/retry under subcontractor scarcity, with mechanism. Kota, Gibbins & Jennings (TAAS 2012) then showed the paper's exact refined claim: budget-unaware maximal recovery (all-Adapt) drives organizational profit **below zero** as recovery load R rises, while meta-reasoned cost-aware recovery (k-Adapt) tracks the zero-cost upper bound — with R swept parametrically from 0 to 0.9. The authors' "refinement" is Kota's Fig. 4c. This is a substrate swap, and the paper should be written and evaluated as a replication.
> 2. **On the LLM substrate the sign reversal is also published.** Xiang (SSRN 7348298; pre-registered, 1,330 runs, 9 models) measured an audited gate's effect changing sign with the verification budget (DiD = +0.456, the largest effect reported). The delta offered here is "more agents."
> 3. **The budget-aware arm is pre-answered.** Self-Healing Orchestrators (2606.01416) ran the matched budget sweep and found budget-aware recovery helps *most* at the tightest budget; FTDI (now in ESWA) built budget-gated recovery for LLM MAS; Arslan (2608.06949) showed risk-ordered audit queueing recovers coverage under fixed audit capacity in a 9-agent LLM pipeline. "Make containment budget-aware" is 2026 design consensus.
> 4. **Mechanism ambiguity.** If scarcity is a rate-limited tool or shared token pool, the backfire is congestion — retry storms/metastable failures (Bronson et al. HotOS 2021; the SRE Book assigns the simulator as a footnote exercise). Which of the demonstrated backfire channels is *not* congestion? If none, this is metastable-failure theory with tokens for CPU.
> 5. **Detectability and power.** D&K's own backfire was "slight." On tau2-bench retail the paired noise floor at n≈100 is ±12–15pp (2606.20695); a small crossover is unmeasurable at the planned n, and a null reads as failed replication rather than boundary condition.
> 6. **Confound.** Xiang's benefit concentrated in weak baselines; without a capability control, "scarcity backfire" and "capability×containment interaction" are indistinguishable.
>
> **Strengths.** Pre-registration and power analysis are welcome and rare in this lane. The false-positive-quarantine mechanism (containment destroying healthy work under propagation) is genuinely non-classical and the paper's best idea — it should be the headline, not an arm. The reviewer-capacity arm with concurrent faults is unoccupied. The explicit engagement with the classical fault-handling canon is exactly what this workshop asks for.
>
> **Recommendation: weak reject / borderline.** Resubmit with the contribution re-centered on what classical theory cannot predict: how detection quality under semantic faults moves the crossover, and the organizational collateral of erroneous containment.

## 6. What precisely survives (the narrowed residue)

1. **Detection-quality × scarcity crossover interaction** — the crossover location as a function of detector accuracy/cost under semantic faults. No classical analogue (classical detection free+perfect; distsys detection = error codes), no LLM-era occupant. This is the scientifically defensible core.
2. **False-positive quarantine collateral under organizational propagation** — containment destroying healthy downstream work; BRA-Audit has the benign-harm measurement but no propagation, no org structure, no scarcity IV. Open.
3. **Reviewer-budget arm as a post-fault velocity race with queue interference across concurrent faults** — A7 confirms experimentally unoccupied; Oversight-Has-a-Capacity owns only the single-agent gating analog (modeling).
4. **Multi-currency parametric map** (token/tool/latency/reviewer in one design) — a measurement contribution; publishable at a workshop if framed as such.
5. **The genuine suspense:** nearest LLM-era evidence is opposite-sign (SHO) while the nearest LLM sign-reversal (Xiang) is single-agent — the transfer outcome is not foreordained. This is D1's best defense against "expected result," and should be stated in the introduction as the motivation.

What does NOT survive: the stated headline (Kota's result), the phenomenon claim (multiply occupied on both substrates), the budget-aware design prescription (2026 consensus), and any "first to study containment under scarcity in LLM MAS" phrasing (BRA-Audit, Arslan, FTDI).

## 7. Kill conditions / residual risks (what would move this verdict)

- **To COLLIDED:** Xiang's full text (unread — ABSTRACT ONLY) contains a budget-aware gate variant or a multi-agent extension; BRA-Audit or the Arslan group adds a scarcity×mechanism ablation before 10 Oct (A11 flags BRA-Audit as one ablation away); ICLR 2027 submissions (invisible until after deadline) contain the org-level crossover.
- **To STRONG(er):** the design centers detection-quality × crossover and false-positive collateral (§6.1–6.2), demonstrates at least one non-congestion backfire channel, and frames the whole paper as a pre-registered transfer test of D&K+Kota with SHO cited as the reason the outcome is uncertain.
- **Empirical kill:** D&K's backfire was "slight"; if the true LLM-substrate effect is similarly small, the planned n (~40 instances, ±12–15pp paired noise floor on tau2-bench) cannot detect it — a null is uninterpretable as designed. Power against a *small* crossover, not W2_statistics' ≥40pp DiD, or drop the confirmatory claim.

## 8. Verification ledger (this session)

- **FULL TEXT:** Kota TAAS 2012 (local artifact `raw/r3_review/kota_taas2012.txt`, key passage re-quoted lines 1485–1487, 1827–1830; original read by A5/E5); D&K ICMAS 2000 (E5/A5); Google SRE ch. 22 (A4/A6); BRA-Audit (A11); OSDI 2022 (A6); Tambe JAIR 1997, Kaminka & Tambe JAIR 2000 (A5).
- **ABSTRACT ONLY (re-pulled from primary source by me this session):** Xiang SSRN 7348298 (Crossref full abstract, finding (iv) verbatim); SHO arXiv:2606.01416 (arXiv abs page, budget-sweep numbers verbatim).
- **ABSTRACT ONLY (per audit lanes, not re-pulled by me):** Oversight Has a Capacity 2606.08919 (A4/A7); Arslan 2608.06949 (A11); Mehan SSRN 6313332 (A4/A6); Halverson pair (A6); FTDI (A3/A6); HotOS 2025 (A4/A6); Two Calls Beat Five Agents (A11).
- **PARTIAL:** HotOS 2021 (A6: abstract + author blog; ACM PDF 403).
- **UNVERIFIED:** none load-bearing.
- **Channel note:** I did not run new discovery searches; this attack consumes the Stage-1 collision inventory plus targeted primary-source re-verification of the two most load-bearing items. A pre-submission re-sweep (post-ICLR-2027 deadline) remains mandatory per A4/A7.
