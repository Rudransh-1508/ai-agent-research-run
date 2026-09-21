# MASO 2026 — Final Research Direction Recommendation (v3, post-audit)

**Date:** 21 September 2026
**Process:** 3 waves / 52 agents (`reports/`, 48 files) → external critique round → full-text verification of the nearest neighbor (`reports/CtC_fulltext_verification.md`) → second adversarial novelty audit (`audit2/`, 18 agents in 2 stages, 11 previously-missed papers found, all load-bearing threats full-text verified). This document reflects the audit outcome and supersedes earlier framings. Audit details: `audit2/FINAL_AUDIT.md`.

---

## 1. The recommendation (one paragraph)

**Build "OrgResilience" as a classical-transfer measurement paper: the first experimental transfer test of the classical MAS fault-handling canon (Dellarocas & Klein ICMAS 2000; Kota et al. TAAS 2012; Hägg 1997) on tool-executing LLM agent organizations — where detection is imperfect and costly, faults are semantic, and containment spends the task's own resource budget.** The headline is NOT "containment backfires under scarcity" (Kota published that contrast in 2012); the headline is **mapping WHEN containment pays**: the containment×scarcity crossover located parametrically across budget currencies (tokens, tool calls, latency, reviewer minutes), with a detection-quality dial as the de-confounding instrument and a natural-attenuation control arm. Substrate: tau2-bench retail + LangGraph. Submit as a 16-page full paper, pre-registered.

## 2. Novelty sentences (three registers — use the defensible one)

1. **Aggressive (do NOT use):** "First demonstration that fault containment backfires under resource scarcity in LLM agent organizations." — Collides with Kota 2012 (FULL TEXT: maximal recovery drives organizational profit below zero), D&K 2000, and weakly with Xiang (SSRN 7348298).
2. **Defensible (USE):** "We present the first experimental transfer test of the classical MAS fault-handling canon (Dellarocas & Klein; Kota et al.) on tool-executing LLM agent organizations — where detection is imperfect and costly, faults are semantic, and containment spends the task's own resource budget — and parametrically map the containment×scarcity crossover that classical work demonstrated only qualitatively."
3. **Conservative (fallback):** "A pre-registered replication-and-extension of classical organizational fault-handling results in LLM-based agent organizations, with two measurement contributions: the detection-quality × containment-benefit frontier, and the containment×scarcity crossover location across four budget currencies."

Every clause of the defensible sentence was checked in the audit: the conjunction (organizational × tool-executing × propagating semantic faults × containment-spends-task-budget × detection-quality instrument × parametric crossover map) is empty with HIGH confidence (three independent search processes + citation-network sweep of ~1,060 citers). Every *pair* is occupied — the paper must be written as a conjunction claim, never as any single-factor claim.

## 3. Venue intelligence (unchanged, verified wave 1)

- MASO 2026 CFP verbatim lists "Detection and mitigation of cascading, and systemic failures" plus organizational testbeds, decision rights, accountability, organizational memory. Deadline 10 Oct 2026 AoE; LNCS; full 16pp / short 8pp; double-blind; workshop 14 Dec 2026, Kumamoto, colocated with PRIMA 2026.
- **Reviewer pool is classical-MAS/XAI/norms-heavy** (van der Torre, Najjar, Galland, Calvaresi). PRIMA 2024 was ~97% classical MAS. This pool rewards engaging the classical canon and punishes unpositioned LLM-benchmark framing — the transfer-test spine is the right call.
- Generic "first classical transfer test" framing is occupied (Resilient Consensus 2606.15024; Loop-Back Authority 2609.14767; Leadership-as-Control 2606.19111). Only the **fault-handling** instantiation survives — scope every framing claim accordingly.

## 4. Hypothesis verdicts after the full audit

| Hypothesis | Verdict | Disposition in the paper |
|---|---|---|
| **H1** — delegation depth changes propagation/recovery cost | SURVIVES WITH NARROWING | Transfer hypothesis, framed as conflict-resolution: D&K amplification vs Hallucination Cascade's measured attenuation (0.644). Not a first-observation claim. |
| **H2** — containment reduces propagation at a cost | COLLIDED as headline | Background/motivation only. Cost premise triple-occupied (Sherlock 2511.00330; Verifier Tax 2603.19328; BRA-Audit 2608.14668). |
| **H3** — containment backfires under scarcity | SURVIVES, RE-AIMED | From "demonstrate the backfire" (occupied: Kota, D&K, metastable failures) to "map when the crossover occurs" via non-classical mechanisms (§6.5). Genuine suspense: SHO's budget sweep is H3-silent, so the LLM-MAS sign pattern is empirically open. |

## 5. Prior-art matrix — top threats (all verification levels in `audit2/FINAL_AUDIT.md` §B)

| Paper | Real LLM MAS | Org structure as IV | Tool-executing/stateful | Non-adversarial faults | Containment bake-off | Recovery cost | Scarcity arm | Detection-quality factor | Human arm |
|---|---|---|---|---|---|---|---|---|---|
| Kota et al. TAAS 2012 | ✗ classical | ✓ (reorganization) | ✗ | ✓ | ✓ (adaptation strategies) | ✓ (recovery priced in capacity) | ✓ (R swept 0→0.9) | ✗ (perfect free detection) | ✗ |
| Dellarocas & Klein ICMAS 2000 | ✗ classical | ✓ (delegation depth) | ✗ | ✓ | ✓ (sentinels vs survivalist) | ✓ (time inflation) | ✓ (scarce subcontractors) | ✗ | ✗ |
| Xiang SSRN 7348298 | ✗ single-agent | ✗ | partial | ✓ | ✗ (one gate) | ✓ (verification budget) | ✓ (sign reversal, degenerate mechanism) | partial | ✗ |
| Containing the Cascade (ICERA 2026) | ✗ simulation | ✗ (topology only) | ✗ | ✓ | ✓ (breaker/rollback ablation) | ✗ (steps only) | ✗ | ✗ (coverage assigned, not measured) | ✗ |
| BRA-Audit 2608.14668 | ✓ | ✗ | ✓ | ✓ | ✓ (audit placement) | ✓ (tokens) | partial (audit budget additive, monotone) | partial | ✗ |
| Huang et al. 2408.00989 | ✓ | ✓ (3-agent patterns) | ✗ (reasoning tasks) | ✓ | ✓ (Challenger/Inspector) | ✗ | ✗ | ✗ | ✗ |
| OrchestraBench 2608.05263 | ✓ (single-LLM chains) | ✗ (chain depth) | ✓ | ✓ | partial | ✓ (rates, not cost) | ✗ | ✗ | ✗ |
| Outcome Monitors 2608.19303 | ✗ single-agent | ✗ | ✓ (tau-bench retail!) | ✓ (silent tool faults) | ✗ | ✓ | ✗ | ✗ | ✗ |
| Sherlock 2511.00330 | ✓ | ✗ | ✓ | ✓ | ✗ (placement optimization) | ✓ | ✗ | partial | ✗ |
| Oversight Has a Capacity 2606.08919 | ✗ modeling | ✗ | ✗ | ✗ adversarial | ✗ | ✓ (reviewer capacity) | ✓ (inverted-U) | ✗ | ✓ (modeled) |
| **OrgResilience (ours)** | ✓ | ✓ (authority depth) | ✓ (tau2 DB state) | ✓ | ✓ | ✓ (4 currencies) | ✓ (crossover mapped) | ✓ (oracle→syntactic→LLM dial) | ✓ (priced, load-dependent) |

Terminology note: "blast radius" remains occupied in 5 senses (CtC, DamageFlow, Bounded Agents, OrchestraBench, ACI) — do not headline it; "sentinel" is re-occupied for LLM MAS by Sentinel Agents (2509.14956, zero classical citations) — cite and differentiate.

## 6. Final design (minimal, audit-corrected)

### 6.1 Testbed
- **One workflow:** tau2-bench retail (114 tasks, 25 tools, deterministic DB-state ground truth, built-in `transfer_to_human_agents`). LangGraph wrapper (checkpoints = rollback arm; interrupts = human arm). Pin τ³ ≥ v1.0.1.
- Workflow 2 (IT incident) is a conditional extension only, after both gates pass.

### 6.2 Core matrix (the whole confirmatory design)
depth {2,3,4} × handling {none, survivalist-retry, sentinel quarantine+re-delegation} × scarcity {abundant, scarce} × detector {oracle, syntactic, LLM-semantic} — with a **natural-attenuation control arm** (no mechanism, measure would-have-died-anyway base rates) and no-fault baselines.
- Faults: agent death (crash, for H1/D&K-comparability) + corrupted handoff (semantic, for the detection dial). Memory-staleness arm only as extension.
- Scarcity currencies: token budget primary; tool-call budget and reviewer-minutes secondary.

### 6.3 Hypotheses (pre-registered)
- **H1-transfer:** recovery-cost inflation grows with delegation depth (D&K: 600–700% at depth 4) — tested against the attenuation alternative (Hallucination Cascade). TOST on the inflation ratio; "fails to transfer" is a designed-in publishable outcome.
- **H3′ (headline):** the containment×scarcity crossover exists on LLM substrates, and its location **shifts with detection quality** (no classical analogue — classical detection was free and perfect; note Kaminka & Tambe JAIR 2000 had monitoring-selectivity theorems, so claim "never an experimental factor," never "classical assumed perfect detection").
- **H2′ (secondary):** sentinel quarantine+re-delegation vs Inspector-style verifier, on the cost-utility Pareto, under both scarcity regimes.
- **H5 (cheap, from CtC full text):** does CtC's fail-safe/fail-operational division of labor (breaker governs containment, rollback governs completion) survive real stochastic semantic reasoners? CtC demonstrated it in simulation only.

### 6.4 Mechanisms and the human arm
Containment arms: none / survivalist-retry / verifier gate / sentinel quarantine+re-delegation / checkpoint-rollback / human escalation. The human arm is a **load-dependent reviewer** (capacity + fatigue, per Oversight Has a Capacity 2606.08919), priced in minutes — a static 80% oracle is behind prior art.

### 6.5 The three non-classical mechanisms (what stops the "just retry storms" review)
1. **Detection-quality × scarcity:** the backfire threshold shifts as detection degrades (no queueing/classical analogue).
2. **False-positive quarantine collateral:** wrongly quarantining a healthy agent strands its subtasks organizationally (BRA-Audit's FP→unnecessary-rollback channel, unquantified).
3. **Reviewer-budget race:** escalation consumes a shared queuing reviewer budget — congestion dynamics, not just congestion of compute.

### 6.6 Statistics (audit-corrected)
- **HARD CONSTRAINT: tau2-retail paired noise floor is up to +18pp at n=100 (2606.20695, FULL TEXT). Binary contrasts need n≥250/cell; the earlier ±10pp TOST plan is dead.** Primary endpoints: continuous (recovery-cost inflation ratio; arm-invariant boundary-crossing counts) with full within-instance pairing; binary containment claims only at n≥250 or demoted to exploratory.
- GLMM with random intercept per instance; Newcombe CIs for proportions; Holm within confirmatory family (H1-transfer, H3′, H5); BH-FDR for exploratory.
- Pre-register (OSF timestamp) before main runs — the real scoop mitigation, and a differentiator: neither CtC nor DamageFlow has power analysis/multiplicity control.
- Budget: ~2,500–4,000 runs; cost non-binding (DeepSeek/GPT-5-mini class, hundreds of USD); wall-clock is the binding constraint — build the parallel harness during days 5–10, budget days 12–16 for runs.

### 6.7 Writing requirements
- Organizational-foundations section (March & Simon, Galbraith, Aghion & Tirole, Bovens, Walsh & Ungson, Reason, Carley & Lin).
- Frame as answering La Malfa et al. (2505.21298) — but scoped: Loop-Back Authority and Leadership-as-Control already answered the generic call; we answer it for fault handling.
- Practitioner paragraph: Anthropic containment post, Agent 365, Replit/Air Canada incidents.
- 16-page full paper.

## 7. Timeline (19 days, two gates)

- **Days 1–4, GATE 1 (build):** org wrapper holds baseline within ~10pp of single-agent retail; fault trigger rates ≥70%; boundary tracer κ≥0.7 vs human labels; joint LangGraph+DB rollback determinism; 100-run throughput test.
- **Days 5–10:** arms + parallel harness + detector dial.
- **Days 9–11:** pilot (~5% of cells) for variance components and trigger rates.
- **Day 12, GATE 2 (post-pilot, pre-committed descope ladder):** cut in order — W2 → memory arm → human arm → reviewer-currency → detector levels 3→2. Never cut instances below the power floor.
- **Days 12–16:** main runs. **Days 17–19:** analysis + writing. Submit early if possible.

## 8. Risk register (post-audit)

| Risk | Severity | Mitigation |
|---|---|---|
| "Kota did this in 2012" | HIGH | Headline is crossover-mapping + transfer, never backfire-discovery; non-classical mechanisms §6.5 |
| "Just metastable failures for LLM agents" | HIGH | Same; cite Bronson/OSDI 2022 explicitly and differentiate on mechanism |
| BRA-Audit adds a scarcity ablation (one experiment away) | HIGH | Pre-register early; submit early; cite as closest neighbor |
| Flat detection-quality frontier (CUADebug: machine RCA ≈ oracle) | MEDIUM | Pre-register flat as publishable; detector dial is the de-confounding instrument regardless |
| tau2 noise floor swallows effects | MEDIUM | n≥250 binary / continuous+paired primary; §6.6 |
| Xiang full text shows a budget-aware arm (would tighten the squeeze) | LOW-MED | Full text already read (audit S3): single-agent, degenerate mechanism, not pre-registered — differentiate |
| Scoop 19–21 Sep + ICLR 2027 invisible | MEDIUM | Re-sweep ~28 Sep for framing; pre-registration is the only real mitigation |

## 9. What this is NOT (scope guards)

Not failure attribution (saturated). Not fault injection per se (MAS-FIRE/AgentChaos). Not delegation security (Bounded Agents + sibling `maso/` proposal). Not adversarial containment (G-Safeguard/DamageFlow/TopoSHIELD). Not "self-healing agents." Not a backfire-discovery claim (Kota/D&K). Not a generic classical-transfer claim (Resilient Consensus/Loop-Back/Leadership-as-Control).

## 10. Verification status

- 48 wave-1–3 reports (`reports/`) + 18 audit reports (`audit2/`), all with per-paper verification levels; raw API dumps in `raw/`, `audit2/raw_*/`.
- Containing the Cascade: FULL TEXT verified (`reports/CtC_fulltext_verification.md`) — no boundary typology, no org-structure IV, simulation-only; fail-safe/fail-operational ablation converted into hypothesis H5.
- H3-deciding papers (Xiang, Mehan, SHO): FULL TEXT verified (`audit2/S3_verify_h3.md`).
- D&K citation claim re-verified 3× (57 citations, exactly 1 post-2023 citer, non-LLM).
- Residual: 19–21 Sep arXiv submissions unannounced (re-sweep ~28 Sep); memory-repair preprint abstract-only (preprints.org bot-walled); ICLR 2027 submissions invisible.
