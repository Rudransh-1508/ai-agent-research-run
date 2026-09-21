# MASO 2026 — Final Research Direction Recommendation

**Date:** 21 September 2026
**Process:** 3 waves, 52 specialist agents (39 landscape/venue/novelty/assassin/feasibility investigators → 5 candidate assassins + 3 feasibility/statistics reviewers → 5 mock reviewers). All underlying reports: `maso_2026_investigation/reports/` (47 files). Every load-bearing citation below was verified against a primary source (arXiv abs page, OpenReview, DOI/Crossref, ACL Anthology, or proceedings site) by at least one agent; several were independently re-verified by two or more.

---

## 1. The recommendation (one paragraph)

**Build "OrgResilience": a fault-injectable organizational multi-agent testbed that measures how non-adversarial, semantic faults propagate across typed organizational boundaries (role, communication, authority/delegation, tool, memory, accountability, human-agent) in executing LLM multi-agent workflows — and uses that instrument to run the first experimental transfer test of classical MAS organizational fault-handling theory (Dellarocas & Klein's sentinel services and "unzippering" propagation, Horling & Lesser's organizational paradigms, the containment-backfires-under-scarcity result), plus a priced comparison of six containment/recovery mechanisms (including human escalation) on the cost-utility frontier.** Submit as a 16-page full paper. Frame explicitly as the experimental answer to La Malfa et al.'s NeurIPS 2025 position paper ("Large Language Models Miss the Multi-Agent Mark", arXiv:2505.21298), which called for exactly this engagement with classical MAS and ran no experiments.

## 2. The smallest novel sentence that survives adversarial search

> **"No prior work measures how non-adversarial faults propagate across typed organizational boundaries — authority/delegation, memory, accountability, and human-agent boundaries, not just communication topology — in executing LLM multi-agent workflows, nor tests whether classical organizational fault-handling predictions survive semantic LLM failure modes."**

Every clause was independently checked:
- "measures fault propagation across organizational boundaries" — zero hits for "organizational blast radius" or equivalent; all existing propagation work uses message/dependency graphs (E1, E3, B4).
- "non-adversarial faults" — the propagation/containment literature is overwhelmingly adversarial (Agent Smith, Prompt Infection, G-Safeguard, DamageFlow, MAS-Shield, CASPIAN); organic-fault work (MAST, Who&When) is diagnostic only (C4, B1).
- "executing LLM workflows" — the one paper with our metric vocabulary (Containing the Cascade, IEEE ICERA 2026) is discrete-event simulation with zero LLM calls (E1, E2, C3).
- "classical transfer test" — Dellarocas & Klein ICMAS 2000 has exactly 1 post-2023 citer (no LLM content); Hägg 1997 has zero LLM-era citers; no transfer/replication study exists (W2 assassin, verified via Semantic Scholar citation APIs).

Do NOT claim: "first to study cascading failures" (false — crowded), "first fault-injection benchmark" (false — MAS-FIRE, AgentChaos), "first blast-radius metric" (false — occupied in 5 senses), "first to connect attribution to containment" (false as stated — BPD, AgentRevive, RoMa), "first to bridge classical MAS and LLMs" (false as framing — La Malfa et al. pre-staked it; we are the *experimental* answer, not the call).

## 3. Venue intelligence (condensed from A1–A3)

- MASO 2026 CFP **verbatim** lists "Detection and mitigation of cascading, and systemic failures" plus organizational memory, decision rights, accountability, organizational testbeds. The seed is native vocabulary, not opportunistic.
- Deadline 10 Oct 2026 AoE; LNCS; full 16pp / short 8pp; double-blind, ≥2 reviewers; workshop 14 Dec 2026, Kumamoto.
- **Reviewer pool is classical-MAS/XAI/norms-heavy** (van der Torre, Najjar, Galland, Calvaresi, negotiation and normative-MAS clusters), plus industry/public-sector practitioners. PRIMA 2024 was ~97% classical MAS; PRIMA 2025 ~20% LLM-hybrid. This pool will reward classical engagement and punish unpositioned LLM-benchmark framing. This is the single strongest argument for the classical-transfer spine of the recommendation.
- Saturation map: saturated = generic orchestration, task decomposition, roles, A2A/MCP interoperability, negotiation, generic benchmarks. Underexplored = systemic/cascading failures with containment/recovery, organizational memory, decision-rights operationalization, fault-injectable organizational testbeds, org cost/quality metrics.

## 4. Candidate table (12 candidates, scored 1–10)

Scores: Nov=novelty, Imp=importance, Fit=MASO fit, Exp=experimental clarity, Base=baseline availability, Feas=feasibility by 10 Oct, Rep=reproducibility, Int=reviewer interest, Def=defensibility of novelty claim.

| # | Candidate | Nov | Imp | Fit | Exp | Base | Feas | Rep | Int | Def | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | OrgBlast (organizational blast radius, org-structure-as-IV) | 7 | 9 | 10 | 8 | 7 | 7 | 8 | 8 | 6 | WOUNDED → merged into final |
| 2 | ClassicalTransfer (do classical org fault-handling results hold for LLM MAS) | 8 | 8 | 10 | 8 | 7 | 7 | 8 | 9 | 8 | SURVIVES → merged into final |
| 3 | AttribContain (attribution-quality threshold for guided vs blind containment) | 7 | 7 | 8 | 9 | 8 | 8 | 9 | 7 | 6 | WOUNDED → secondary experiment / follow-up |
| 4 | RecoveryCost (cost-utility Pareto of containment mechanisms, priced human escalation) | 6 | 8 | 9 | 8 | 7 | 9 | 9 | 7 | 5 | WOUNDED → merged as cost axis |
| 5 | FaultValidity (do injected faults predict organic failure?) | 8 | 8 | 7 | 6 | 6 | 4 | 6 | 8 | 7 | SURVIVES only descoped (Study A); follow-up paper |
| 6 | Memory contamination propagation & recovery in shared org memory | 7 | 7 | 9 | 7 | 5 | 6 | 7 | 7 | 6 | Too thin standalone; one boundary arm in final |
| 7 | Human escalation as costed containment (vs automated) | 6 | 8 | 9 | 7 | 6 | 6 | 6 | 8 | 5 | Merged as escalation arm; noisy-oracle primary |
| 8 | Org structure as independent variable for resilience | 6 | 8 | 10 | 8 | 7 | 7 | 8 | 7 | 5 | Merged (it is the final's IV) |
| 9 | Containment timing / attribution decay with propagation depth | 7 | 6 | 7 | 7 | 6 | 6 | 7 | 6 | 6 | Follow-up |
| 10 | Correlated/common-mode failure × org structure (heterogeneity interaction) | 7 | 7 | 8 | 6 | 6 | 5 | 7 | 7 | 6 | Follow-up |
| 11 | Fault-injectable organizational testbed (pure infrastructure paper) | 5 | 7 | 9 | 8 | 8 | 7 | 9 | 6 | 5 | Absorbed — testbed is means, not contribution |
| 12 | Blast-radius-aware orchestration (design-time containment) | 4 | 7 | 7 | 6 | 6 | 5 | 7 | 6 | 3 | KILLED — Shen et al. EMNLP 2025 + topology cluster occupy it |

Killed earlier (repo history, do not resurrect): sanctioning under unreliable blame; acceptance-gate manipulation; experience commons; verifier panels; regret-grounded Dec-POMDP LLM teams. Occupied by sibling proposal (`maso/`): policy-preserving delegation invariants — treat authority/delegation as a blast-radius dimension, never as invariant enforcement.

## 5. Prior-art matrix — top threats to the final candidate

| Paper | Real LLM MAS | Org structure as IV | Typed org boundaries | Non-adversarial faults | Containment bake-off | Recovery | Cost vector | Human arm | Classical MAS engagement |
|---|---|---|---|---|---|---|---|---|---|
| Containing the Cascade (ICERA 2026, DOI 10.1109/ICERA72709.2026.11666599) | ✗ (simulation) | ✗ | ✗ (message/tool only) | ✓ | ✓ (CB vs rollback) | partial | ✗ | ✗ | ✗ |
| DamageFlow/BlastGuard (ICML 2026 AIWILD, MYvsxnxbCf) | partial (80-scenario pilot) | ✗ | ✗ (tool boundary) | ✗ (adversarial) | ✓ | ✓ | partial (BRS component) | ✗ | ✗ |
| OrchestraBench (arXiv:2608.05263) | ��� (but single-LLM chains) | ✗ | ✗ | ✓ | partial | ✓ | ✗ | ✗ | ✗ |
| Bounded Agents (arXiv:2608.15888) | ✗ (static analysis) | ✗ | authority only | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| From Spark to Fire (arXiv:2603.04474) | ✓ | ✗ | ✗ (message layer) | ✓ | ✗ (one mechanism) | ✗ | ✗ | ✗ | ✗ |
| MAS-FIRE (arXiv:2602.19843) | ✓ | ✗ | ✗ | ✓ | ✗ | diagnostic only | ✗ | ✗ | ✗ |
| AgentChaos (arXiv:2608.06790, ASE 2026) | ✓ | ✗ | ✗ (API layer) | ✓ | ✗ (deferred) | ✗ | ✗ | ✗ | ✗ |
| Emergence World (arXiv:2609.17320) | ✓ | ✗ | partial (memory/tools) | ✗ (adversarial stress) | ✗ ("detection ≠ containment") | ✗ | ✗ | ✗ | ✗ |
| Trust Prop. & Structural Containment (arXiv:2609.17648) | ✓ | ✗ (fixed structure) | partial (memory/authority) | ✗ (adversarial) | ✗ (one mechanism) | ✗ | ✗ | ✗ | ✗ |
| Dellarocas & Klein (ICMAS 2000) | ✗ (classical agents) | ✓ (delegation depth) | partial (delegation) | ✓ | ✓ (sentinels) | ✓ | ✓ (time) | ✗ | — (is the classic) |
| **OrgResilience (ours)** | ✓ | ✓ | ✓ (7 types) | ✓ | ✓ (6 mechanisms) | ✓ | ✓ (incl. priced human minutes) | ✓ (noisy oracle) | ✓ (pre-registered transfer tests) |

The empty column-pattern is the novelty claim in table form. Note the last row is the *only* one with org-structure-as-IV on real LLM MAS, and the only one engaging the classical lineage experimentally.

## 6. Final design (revised by all five mock reviewers' convergent fixes)

### 6.1 Testbed
- **Workflow 1:** customer-service refunds on tau2-bench retail (MIT; 114 tasks, 25 tools, deterministic DB-state ground truth, built-in `transfer_to_human_agents` escalation). Zero authoring cost.
- **Workflow 2:** IT incident management, newly authored (~12 tools, ~30 tasks), deterministic tools.
- Framework: LangGraph (checkpointing = rollback arm; interrupts = human arm). AutoGen is in maintenance mode — do not use.
- **Irreversibility regime flag (R5 fix):** committed tool actions final; rollback degrades to subtask restart. The reversible-vs-irreversible contrast becomes a headline result, and defuses "Pareto computed in a revertible universe."

### 6.2 Independent variables
- Org structure: flat / 2-level / 3-level / **depth-4 delegation chain (R3 fix — restores D&K-comparable cells)**; sentinel present/absent; **oracle-detector vs learned-detector sentinel (R3 fix — separates detection difficulty from theory breakdown)**; scarcity on/off; **flat-with-peer-verification control arm (R4 fix — breaks depth/verification confound)**; **static least-privilege prevention arm (R5 fix — the industry's actual first line of defense)**.
- Faults (5 in main matrix, ground truth known): hallucinated tool arguments; corrupted handoff content; verification omission; agent death/unavailability; stale/poisoned shared memory. (Instruction-conflict and unauthorized-action faults in appendix.)

### 6.3 Containment/recovery arms (the bake-off)
none · retry · independent verifier gate · checkpoint-rollback · sentinel quarantine + re-delegation · **noisy-oracle human escalation (80% accuracy, priced in oversight minutes, queue-latency sweep — R4/R5 fix; scripted perfect oracle demoted to upper bound)**.

### 6.4 Metrics (R2/R4 fixes applied)
- **OBR redefined:** absolute corrupted-event counts + per-boundary-type indicators on an **arm-invariant boundary inventory** (not a fraction whose denominator changes across structure arms). Typology derived from MOISE+ structural/functional/deontic dimensions, with severity-weighted and typology-sensitivity variants in appendix. Demoted from headline construct to instrumentation (R1).
- Co-primary: utility preservation (deterministic DB-state success), continuous OBR count. Secondary: MTTD/MTTC, recovery-cost vector (tokens, tool calls, wall-clock, priced human minutes), D&K-analog relative completion-cost inflation.
- LLM-as-judge: one secondary DV only, documented rubric, two judges, κ≥0.7 gate, 10% human audit.

### 6.5 Pre-registered hypotheses (the classical transfer spine)
- H1: delegation-tree depth amplifies completion-cost inflation (D&K "unzippering"); TOST SESOI on the **inflation ratio** (R3 fix), not raw pp.
- H2: sentinel containment reduces spread vs no-sentinel at matched budget.
- H3: containment backfires under resource scarcity (sign reversal — the one adequately powered interaction).
- H4 (repositioned per R3): Klein & Dellarocas CSCW 2000 and Carley & Lin 1997 **conceptually anticipated** value/semantic faults; what is unmeasured is their behavior on LLM substrates. H4 becomes the **detection-quality × containment frontier** (oracle vs learned detector arms), with quantitative non-obvious predictions (unzippering magnitude shift; scarcity-backfire threshold shift) — not the foreordained "syntactic detectors miss semantic faults" (R1's kill).

### 6.6 Statistics (F-C corrected plan + R2 fixes)
- ~3,400–4,000 runs; ~$165–900 depending on model tier (DeepSeek → GPT-5-mini). Budget instances over seeds: I=40–50 instances × 1–2 seeds; 10×8 reliability sub-study.
- Continuous endpoint is sole confirmatory outcome (d=0.65 at n=37/cell); binary/TOST claims exploratory unless ≥96 paired instances are budgeted for the equivalence tests (R2's central fix — the ±10pp SESOI is otherwise narrower than the achievable CI).
- ITT primary analysis with per-arm trigger rates reported (triggered-only analysis is post-treatment selection — R2); low-prevalence block for false positives.
- McNemar within-instance pairing; Holm correction across the hypothesis family; claims scoped to ≥25pp binary / d≥0.5 continuous effects.
- Pre-registration (OSF or internal timestamped doc) before any runs — itself a differentiator: neither Containing the Cascade nor DamageFlow reports power analysis, CIs, or multiplicity control.

### 6.7 Writing requirements (R1/R3/R4)
- Organizational-foundations section: March & Simon, Galbraith, Aghion & Tirole 1997 (decision rights), Bovens 2007 (accountability), Walsh & Ungson 1991 (org memory), Reason 2000/Perrow (organizational accidents), Carley & Lin 1997.
- Frame H1 as a market→hierarchy transfer test (Coase), not mere replication.
- Practitioner-grounding paragraph: Anthropic "How we contain Claude" (2026), Microsoft Agent 365, OpenAI guardrails, Replit incident (Jul 2025), Air Canada tribunal.
- Cite La Malfa et al. (arXiv:2505.21298) as the call being answered; Bădică et al. (arXiv:2509.02515) as the reflection being operationalized.
- 16-page full paper (R3: the content does not fit 8 pages without looking compressed).

## 7. Timeline to 10 Oct (19 days, zero slack — F-A plan)

- Days 1–4: go/no-go gates — org wrapper holds baseline pass within ~10pp of single-agent tau2-retail; fault trigger rates ≥70%; OBR auto-labeling κ≥0.7 vs human labels; joint LangGraph+DB rollback determinism. **If any gate fails, descope to CAND-3 (attribution-threshold study, ~1,200 runs, fully feasible) as the fallback paper.**
- Days 5–10: build arms (structures, sentinels, mechanisms, irreversibility flag); pilot for variance components.
- Days 11–15: main matrix runs (~4k runs, hours of compute, cost non-binding).
- Days 16–19: analysis, writing, internal red-team pass against the five reviewer reports in `reports/R*`/`W3_*`.

## 8. Risk register

| Risk | Severity | Mitigation |
|---|---|---|
| Scoop before 10 Oct (Emergence World / TPSC / institutions-as-IV cluster are one experiment away; SYSU-SMU group owns both injection pillars) | HIGH | Re-sweep arXiv cs.MA/cs.AI ~28 Sep and ~7 Oct (C1's recommendation); pre-register early |
| "Incremental recombination" reviewer read (R1) | MEDIUM | R1's revision package applied in §6.7; conjunction-verified-empty argument in related work |
| H4 strawman (R3) | MEDIUM | Repositioned per §6.5; K&D CSCW 2000 + Carley & Lin cited as anticipations |
| Statistical underpowering of equivalence claims (R2) | MEDIUM | §6.6 fixes; demote or budget up |
| "Pipelines with role labels" (R4) | MEDIUM | MOISE+-derived typology; org-foundations section; peer-verification control |
| Irreversibility objection (R5) | MEDIUM | Two-regime design is now a headline result |
| Engineering overrun | MEDIUM | Hard gates days 1–4; CAND-3 fallback |
| "Blast radius" terminology collision | LOW (managed) | Term disambiguated in one explicit paragraph against all 5 occupied senses; consider "organizational failure spread" in title, OBR as defined instrument |

## 9. What this is NOT (scope guards)

- Not a failure-attribution paper (saturated: Who&When, CHIEF, DCFA + 10 extensions).
- Not a fault-injection paper (occupied: MAS-FIRE, AgentChaos, AgentChaosBench).
- Not a delegation-security paper (occupied: Bounded Agents, root-scoped quiescence, and the sibling `maso/` proposal).
- Not an adversarial-containment paper (occupied: G-Safeguard, MAS-Shield, DamageFlow, TopoSHIELD, BPD).
- Not a "self-healing agents" paper (crowded 2026 cluster, all task-level).

## 10. Verification status

47 specialist reports with per-paper verification logs in `maso_2026_investigation/reports/`; raw API dumps in `maso_2026_investigation/raw/`. Known residual gaps: (a) Containing the Cascade full text was bot-walled — verified via Crossref + abstract + Zenodo tombstone only; obtain via IEEE Xplore before writing related work; (b) arXiv submissions from 19–21 Sep not yet announced — re-sweep before submission; (c) AAMAS 2026 proceedings were swept via IFAAMAS TOC but a manual pass is cheap insurance.
