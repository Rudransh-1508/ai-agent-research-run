# AUDIT2 — AGENT 3: RECOVERY AND CONTAINMENT SPECIALIST

**Date:** 2026-09-21
**Mission:** Determine whether recovery-mechanism comparisons already exist in LLM-MAS, what dimensions they manipulate, whether any comparison varies the resource budget for recovery, and whether anyone reports a mechanism that helps under abundance and hurts under scarcity (sign reversal). Classify collisions for claims 6, 7, 8, 16, 20.
**Stance:** Adversarial. Goal was to find fatal collisions, not defend the idea.

**Claims-registry caveat:** No numbered claims list (6/7/8/16/20) exists anywhere in `maso_2026_investigation/`. I classify claims 6/7/8 as the FINAL_RECOMMENDATION candidate-table entries with those numbers (6 = memory contamination propagation & recovery; 7 = human escalation as costed containment; 8 = org structure as IV for resilience). Claims 16/20 are not locatable; I classify the two most plausible in-lane claims they could denote — (16′) "first recovery/containment mechanism bake-off in LLM MAS" and (20′) "containment backfires under resource scarcity (H3)" — and flag the mapping for the orchestrator to correct.

---

## 0. BOTTOM LINE

1. **Recovery/containment mechanism comparisons in multi-agent tool-executing LLM settings EXIST and are numerous** (RoMa, SymTrace, BPD, AgentRevive, MTTR-A, Huang 2408.00989, Predictive-Self-Healing-MPC, FTDI; plus simulation-only CtC). Any "first mechanism comparison/bake-off in LLM MAS" claim is **DEAD**.
2. **Budget-varied recovery comparisons EXIST but only outside organizational MAS:** Self-Healing Orchestrators (single orchestrator, matched-budget sweep), FTDI (code-gen MAS, budget-gated tiered repair), Keel (single-agent policy cost-frontier), CodeRescue (withdrawn, single-agent), AI Control (audit-budget sweep, adversarial single-agent). **No budget-varied recovery comparison exists in a multi-agent organizational tool-executing setting.**
3. **The H3 sign reversal (containment helps under abundance, hurts under scarcity) is NOT reported anywhere in the LLM era.** The only verified instance of that exact pattern remains the classical source itself (Dellarocas & Klein ICMAS 2000, full-text verified by E5). However, the *phenomenon class* — "a coordination/oversight/redundancy mechanism whose value flips sign across a regime boundary" — is crowded: Loop-Back Authority (2609.14767), Leadership-as-Control (2606.19111), Oversight Has a Capacity (2606.08919), Are-More-LLM-Calls (2403.02419), Budgeted-Synergy phase transition (2601.17311). H3 survives only as a *fault-propagation-specific* experimental result, and two Sep-2026 papers show the "classical-theory transfer test on LLM teams where the classical prediction fails" genre is already occupied.
4. **Unexpected finding:** the one verified budget sweep (Self-Healing Orchestrators) shows the *opposite* sign pattern to H3 — the budget-aware mechanism's advantage is LARGEST at the tightest budget. H3 may hold only for budget-*unaware* mechanisms; see §5.

---

## 1. ANCHOR VERIFICATION (all independently re-verified this session)

| Anchor | ID / venue | My verification | Lane-relevant content |
|---|---|---|---|
| Atomix | arXiv:2602.14849 (v1 16 Feb 2026, v2 29 May 2026) | **ABSTRACT VERIFIED** (arXiv abs page) | Progress-aware transactions for tool effects; abort suppresses/compensates; "improves clean recovery under injected faults"; single-agent workflows + concurrent agents; NOT a mechanism comparison, no budget variation |
| AgentTether | arXiv:2607.06273 (7 Jul 2026) | **ABSTRACT VERIFIED** | Runtime repair: Critical Transition Graph + Repair Memory + guarded intervention; repairs 59.0%/65.1% of failed τ-bench Banking tasks; reduces turns/tokens; single-agent |
| SymTrace ("Repair or Resample?") | arXiv:2608.25920 (v1 26 Aug 2026) | **ABSTRACT VERIFIED** | **Real-MAS recovery comparison**: unguided rerun repairs only 6.90% of failures (67.97% reproduction); symptom-driven intervention repairs 20.15%; 3 MAS frameworks; SymFail dataset (536 trajectories). No spread metrics, no budget variation |
| ParaRecover | arXiv:2609.12345 (11 Sep 2026), EMNLP 2026 main | **ABSTRACT VERIFIED** | Error localization + recovery benchmark, parallel tool-use, cascading failures across dependent branches; 10,626 instances; **single-agent** |
| Self-Healing Orchestrators | arXiv:2606.01416 (31 May 2026) | **ABSTRACT VERIFIED** | **The only matched recovery-budget sweep**: self-healing > retry-only (94.5%) > full replan (93.8%); at every tested budget; largest gap at ONE recovery attempt (94.0% vs 85.3%/88.2%); single orchestrator |
| RoMa | CSCWD 2026, DOI 10.1109/cscwd68734.2026.11582680 (13 May 2026) | **ABSTRACT VERIFIED** (S2 + Crossref) | **Real-MAS 3-strategy FT comparison**: credibility-weighted redundant voting, primary-backup failover, dynamic isolation+rehabilitation; POMDP; adversarial fault injection in training; collaborative debugging; "comparable computational efficiency" claimed, no budget sweep |
| BPD | ICML 2026, OpenReview TphOLCDmKB | **PARTIALLY VERIFIED** (GitHub repo ChengcanWu/BPD confirmed live, created 2025-10-21; OpenReview challenge-walled today; content per wave-1 C5 verified record) | Attribution → isolate attacker → clear edges → re-run; flat vs hierarchy; adversarial |
| AgentRevive | ACL 2026, 2026.acl-long.373 | **METADATA VERIFIED** (ACL Anthology .bib + Crossref: Zhang et al., "Taming 'Zombie' Agents", ACL 2026 vol. 1 long) | Soft quarantine (Active/Standby/Terminated) vs hard pruning; hallucination-risk-driven; non-adversarial |
| Containing the Cascade | ICERA 2026, DOI 10.1109/ICERA72709.2026.11666599 | **FULL TEXT VERIFIED** (prior wave, reports/CtC_fulltext_verification.md) | 5-condition bake-off (NoGuard/Retry/Verifier/Debate/SENTINEL) + breaker/rollback ablation; **simulation only, no scarcity condition, no cost vector** |

---

## 2. CRITICAL QUESTION (a): mechanism comparisons in MULTI-agent tool-executing settings

**They exist. The comparison-design space is occupied.** Verified inventory:

| Paper | Setting | Mechanisms compared | Budget varied? | Sign reversal? |
|---|---|---|---|---|
| CtC (ICERA 2026) | Simulation of tool-using MAS | NoGuard / Retry / Verifier / Debate / SENTINEL; breaker vs rollback ablation | No | No (monotone) |
| RoMa (CSCWD 2026) | Real LLM MAS, debugging | Redundant voting / failover / isolation+rehab vs baselines | No | No |
| SymTrace (Aug 2026) | Real MAS, 3 frameworks | Unguided rerun vs symptom-driven intervention | No | No |
| BPD (ICML 2026) | Real MAS (adversarial) | Isolate+rerun vs none; flat vs hierarchy | No | No |
| AgentRevive (ACL 2026) | Real MAS debate/evolution | Soft quarantine vs hard pruning | No | No |
| Huang 2408.00989 | Real MAS, faulty agents | Challenger / Inspector vs none × topology | No (B16 full-text: zero cost analysis) | No |
| MTTR-A (2511.20663) | LangGraph MAS, simulated drift | Multiple reflex strategies on recovery latency | No | No |
| Predictive Self-Healing MPC (SusTech 2026, DOI 10.1109/SusTech67720.2026.11536606) | LLM MAS pipelines | Predictive (MPC: replica scaling, load redistribution, circuit breaker) vs reactive | No | No |
| FTDI (SSRN 2026) | Code-gen MAS | Tiered repair (patch → deep repair → regeneration), budget-gated | **Yes (budget-gated triggering)** | No |
| SagaLLM (PVLDB 2025, arXiv:2503.11951) | Multi-agent LLM planning | Saga compensation + independent validation agents (architecture, not bake-off) | No | No |

**Single-agent/orchestrator comparisons (must-cite, not collisions for the MAS claim):** Keel (Zenodo 10.5281/zenodo.22754511, verified via DataCite: policies {none, retry, reset, rollback, escalate, budget} on an explicit cost frontier, ~41k model calls); Self-Healing Orchestrators; CodeRescue (withdrawn); "Did It Happen?" (Research Square 10.21203/rs.3.rs-10730245/v1, **verified via Crossref**: prompt-advice vs status-reconciliation vs idempotency-contract, exactly-once recovery, 756-pair cell); AgentTether; memory-rollback repair (2608.10502).

## 3. CRITICAL QUESTION (b): does any comparison vary the RESOURCE BUDGET for recovery?

**Yes, but never in an organizational multi-agent setting:**
- **Self-Healing Orchestrators** — matched recovery-budget sweep (attempts), single orchestrator. ABSTRACT VERIFIED.
- **FTDI** — "controlled evaluation protocol for budget-constrained robustness studies"; budget-gated triggering; explicitly motivated by "low-yield retries when interaction rounds and costs are constrained." Code-gen MAS. ABSTRACT VERIFIED (Crossref full abstract).
- **Keel** — budget events logged; policy frontier; single-agent. VERIFIED (DataCite).
- **AI Control** (ICML 2024) — trusted-labor audit budget sweep; adversarial single-agent coding (per E6).
- **CtC** — varies competence regime (p_e), explicitly NOT scarcity (full-text confirmed).

**Gap confirmed:** no budget-varied recovery/containment comparison in a multi-agent organizational tool-executing workflow with propagation.

## 4. CRITICAL QUESTION (c): does anyone report help-under-abundance / hurt-under-scarcity?

**In LLM-MAS containment/recovery: NO. Verified negative across S2 bulk, DataCite, OpenReview, arXiv listing sweeps (queries: "containment backfires", "retry storm/amplification", "verification overhead budget", "resource-constrained resilience", "recovery budget scarcity", "escalation policy cost", "graceful degradation multi-agent LLM" — zero relevant hits; arXiv API blocked from this network, noted as channel limitation).**

**But the sign-reversal phenomenon class is crowded — these are the papers a reviewer will use to call H3 obvious:**

| Paper | Verified | Sign-reversal / boundary result | Why it is NOT H3 |
|---|---|---|---|
| Dellarocas & Klein ICMAS 2000 | FULL TEXT (E5) | EH services worse than survivalist under subcontractor scarcity | Classical crash-fault simulation — the transfer *source*, not a collision |
| **Loop-Back Authority** (2609.14767, 13 Sep 2026) | **ABSTRACT VERIFIED** (me) | Manager reject/revise authority link HURTS utility (flat > hierarchical, d=0.42); +51.5% tokens for no gain; "a supervisor pays for itself when it can verify and becomes a liability when it can only opine" | Moderator is verification capability, not resource scarcity; no faults/propagation |
| **Leadership as Coordination Control** (2606.19111, 17 Jun 2026) | **ABSTRACT VERIFIED** (me) | Classical contingency-theory transfer test; controllers help only at the "recovery-advantage boundary" (unreliable round-0 majority ∧ recoverable task ∧ interaction doesn't self-repair); null elsewhere | Team-science transfer, no fault injection, no scarcity |
| Oversight Has a Capacity (2606.08919) | **ABSTRACT VERIFIED** (me) | Inverted-U: more human escalation can make the system LESS safe (reviewer fatigue); flooding attack | Fatigue-driven, prevention/gating, single-agent |
| Are More LLM Calls All You Need (2403.02419, NeurIPS 2024) | **ABSTRACT VERIFIED** (me) | Voting/filter-voting non-monotone in #calls — redundancy backfires | Query-difficulty mechanism, not scarcity; no faults |
| Phase Transition for Budgeted Multi-Agent Synergy (2601.17311) | **ABSTRACT VERIFIED** (me) | MAS "help, saturate, or even collapse" under fixed inference budget; closed-form budget thresholds (s > β) | Org-structure benefit theory, no containment mechanism, synthetic |
| Cost-of-Pass (2504.13359) | prior wave | Self-refinement gains "rarely justify their cost" | Steady-state, no faults |

**Assessment:** H3's specific configuration (containment mechanism × fault propagation × resource-regime sign flip, measured on LLM MAS) is unoccupied. But "mechanisms that help in one regime and hurt in another" is an established 2024–2026 LLM-era result pattern. H3 will be read as *expected*, not surprising — its value is measurement, not discovery. Frame accordingly.

## 5. UNEXPECTED FINDING (report-worthy)

**The only verified budget sweep shows the opposite of H3.** Self-Healing Orchestrators' matched-budget sweep: the budget-aware targeted-recovery mechanism's advantage over baselines is LARGEST at the tightest budget (94.0% vs 85.3%/88.2% at one attempt). Combined with D&K (budget-unaware EH services backfired under scarcity by increasing competition for the bottleneck) and FTDI (budget-gating exists precisely to avoid low-yield retries under constraint), the emerging pattern is: **the sign reversal may be a property of budget-UNAWARE containment, and budget-aware design may eliminate it.** H3 as stated ("containment backfires under scarcity") risks being refuted-or-trivial depending on mechanism design; the defensible version is an interaction: H3′ = "budget-unaware containment backfires under scarcity; budget-aware containment does not" — a sharper, more defensible hypothesis that also explains the classical result.

## 6. COLLISION CLASSIFICATION (claims 6, 7, 8, 16, 20)

| Claim | Classification | Basis |
|---|---|---|
| **6** — memory contamination propagation & recovery in shared org memory | **PARTIAL COLLISION (wounded, survives descoped)** | Memory-rollback repair (2608.10502, single-agent), verification-status laundering through memory/summarization (2609.20211), Emergence World memory propagation (2609.17320), memory-poisoning containment in TPSC (2609.17648). Occupied: memory as propagation channel + single-agent memory repair. Unoccupied: memory-fault recovery *comparison* in organizational MAS |
| **7** — human escalation as costed containment | **PARTIAL COLLISION (wounded)** | READY (2609.02095) prices oversight burden; Oversight-Has-a-Capacity prices escalation with fatigue; AI Control budgets trusted labor vs automated checks; 2609.02191 measures human interventions at MAS fault points (±40%/−6%). Unoccupied (E6 + my confirmation): escalation-vs-automated comparison for *propagating* faults with priced minutes |
| **8** — org structure as IV for resilience | **STRONG COLLISION for the broad claim; survives only fault-scoped** | Loop-Back Authority (authority link as IV, paired experiment); Leadership-as-Control (controllers as IV); Huang 2408.00989 (topology × faulty agents); BPD (flat vs hierarchy); institutions-as-IV cluster (2608.11357, 2604.27691). "Org structure as IV" is DEAD as a novelty claim; "org structure as IV for fault *propagation/recovery*" survives |
| **16′** — (inferred) first recovery/containment mechanism bake-off in LLM MAS | **FATAL COLLISION — DEAD** | CtC (5-condition + ablation, simulation), RoMa (3-strategy, real MAS), SymTrace (rerun vs intervention, real MAS), BPD, AgentRevive, MTTR-A, MPC self-healing. If claim 16 is anything like this, kill it |
| **20′** — (inferred) containment backfires under scarcity (H3) | **NO DIRECT COLLISION — survives as LLM-MAS experimental result; phenomenon class crowded** | No LLM-era scarcity sign reversal for containment found (verified negative). But D&K (classical source) + Loop-Back + Oversight-Capacity + Budgeted-Synergy make the *pattern* familiar; and SHO's opposite-sign budget sweep threatens the prediction itself. Recommend reframing as H3′ (§5) |

## 7. SEARCH LOG / CHANNEL NOTES

- Verified this session via arXiv abs pages: 2602.14849, 2606.01416, 2607.06273, 2608.25920, 2609.12345, 2606.08919, 2511.20663, 2603.04474, 2601.17311, 2403.02419, 2609.14767, 2606.19111, 2510.18179, 2605.17998.
- Via Crossref: RoMa (10.1109/cscwd68734.2026.11582680), FTDI (10.2139/ssrn.6387100), Did-It-Happen (10.21203/rs.3.rs-10730245/v1), AgentRevive (10.18653/v1/2026.acl-long.373).
- Via DataCite: Keel (10.5281/zenodo.22754511).
- Via S2: RoMa abstract; SagaLLM (2503.11951, PVLDB 2025); MPC self-healing (10.1109/SusTech67720.2026.11536606); **D&K ICMAS 2000 citation check: 57 citations, exactly 1 post-2023 citer ("Exception handling in multi-agent oriented programming", KER 2025 — classical, no LLM); Hägg 1997: post-2023 citers all classical.** The classical-transfer claim survives on both axes.
- Via GitHub API: ChengcanWu/BPD repo confirmed.
- Blocked/failed channels: arXiv export API (empty responses after first query), OpenReview note-detail (challenge wall), OpenAlex (daily budget exhausted on shared IP), S2 search endpoint (intermittent 429; bulk endpoint used instead).
- Raw artifacts saved in `maso_2026_investigation/audit2/raw_a3/`.
