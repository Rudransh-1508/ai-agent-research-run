# W2 ASSASSIN — CAND-1 "OrgBlast" (Organizational Blast Radius)

**Investigator:** Wave-2 ASSASSIN for CAND-1
**Date:** 2026-09-21
**Mission:** Kill CAND-1. Beyond wave-1 threats, search for: (a) org structure (roles/hierarchy/RACI/authority config) as independent variable under fault injection; (b) fault spread measured across *typed* boundaries (not just communication topology); (c) containment-mechanism bake-off (quarantine vs rollback vs revocation vs escalation) in LLM MAS; (d) any IMACS-style executable-orgs × MAS-FIRE-style fault-injection combination. Assess whether IMACS + MAS-FIRE trivially yields CAND-1. Verify current status/full text of Containing the Cascade (DOI 10.1109/ICERA72709.2026.11666599) and OrchestraBench (arXiv:2608.05263).

---

## VERDICT: WOUNDED

CAND-1's generic core — "measure blast radius of injected faults in tool-using LLM MAS and compare containment mechanisms under utility preservation" — is **occupied, including the exact metric name, a published containment-mediator ablation, and (newly verified this wave) a real-LLM cascade-radius + recovery measurement over enterprise-framed workflows**. The candidate cannot lead with "blast radius," "first containment comparison," or "first real-LLM cascade measurement."

**The surviving sliver, precisely:** *org structure as the independent variable* (role/RACI/authority/delegation configuration, hierarchy depth, span of control) × *organic/semantic faults* (not adversarial injection) × *real multi-agent LLM executions of stateful organizational workflows* (IT incident / procurement / refund — not QA benchmarks, not arithmetic chains) × *spread measured across typed organizational boundaries* (authority, accountability, memory, human-agent — not pipeline stages) × *bake-off of organizationally-semantic containment mechanisms* (quarantine, rollback, delegation revocation, reroute, human escalation — priced against each other and against task utility). Every clause of that conjunction is verified empty; every clause individually is adjacent to occupied territory. The paper must be framed as **organizational resilience science** and must cite-and-differentiate the full occupant list below, or it dies in review.

---

## 1. Verification of the two assigned threats

### 1.1 Containing the Cascade (Divi, Gullapalli, Brahmandam; IEEE ICERA 2026; DOI 10.1109/ICERA72709.2026.11666599)

Re-verified 2026-09-21 via Crossref + Semantic Scholar + Zenodo API:

- **Status:** Published, ICERA 2026 pp. 604–609, July 2026. **0 citations.** 33 references. Full text remains **inaccessible**: IEEE Xplore bot-walled; the Zenodo OA copy (10.5281/zenodo.21314250) was **deleted 2026-07-22, removal reason "copyright"** (tombstone confirmed via Zenodo API). Unpaywall lists only the dead Zenodo location. No live code repository exists despite the abstract's "we release Cascade-Bench and Sentinel."
- **Boundaries:** message-passing/tool layer only. Its six fault modes include hallucination, malformed tool call, and "role drift" — but role drift is a fault *type*, not an organizational boundary; no authority/delegation, accountability, memory, or human-agent boundaries; no org structure variation.
- **Metrics:** containment rate, cascade depth, **blast radius**, mean time-to-detection — the exact term, in the exact setting.
- **Mechanisms:** Sentinel mediator = typed message contracts + semantic anomaly gate + **circuit breaker** + **checkpoint rollback**; ablation separates fail-safe (circuit breaker → containment) from fail-operational (rollback → completion). Task success 31.3%→83.7%, containment 46.2%→99.4%.
- **Fatal weaknesses (for differentiation):** discrete-event **simulation** "calibrated to reported MAS failure statistics" — zero LLM calls; suspiciously clean numbers (99.4%); low-tier venue; artifact deleted; 0 citations. CAND-1 cannot ignore it (a reviewer may know it) but can legitimately attack its evidence base.

### 1.2 OrchestraBench (Gu, Vidra, Setty, Zheng — Anote; arXiv:2608.05263 v1, 5 Aug 2026)

**Full text read** (arXiv HTML). This paper is **more damaging than wave-1 credited** ("cascade radius + recovery metrics, controlled-chain probes" undersells it):

- **What it actually has:** (i) seed-reproducible **failure-injection harness over templated enterprise workflows** (finance approval 4-stage, HR onboarding 5-stage, DevOps deployment 5-stage); (ii) **cascade radius** (downstream stages corrupted) and **per-failure-mode recovery rate** as primary metrics, plus time-to-detection, recovery completeness, delegation fidelity; (iii) **real LLM execution** — Claude Sonnet 4.6 / Opus 4.8 / Haiku 4.5, N=150–750 per experiment; (iv) five MAST failure modes injected at prompt level (ambiguous delegation, tool-invocation error, context pollution, conflicting sub-agent outputs, premature action); (v) a **domain-grounded variant framed as a four-role loan-approval pipeline** (Intake Officer, Risk Analyst, Compliance Officer, Approval Manager); (vi) a **policy-conditioned containment probe** (LLM router cuts cascade radius ~5.5× at depth 7) with an honest ablation showing the gain is mostly the trusted-state signal, not autonomous detection; (vii) the finding that **blind retry does not repair latent/semantic faults** — "detection and attribution, not blind retry, is the necessary containment mechanism."
- **What it lacks (why CAND-1 is not killed by it):** **single LLM over a staged chain, explicitly "not a literal multi-agent system"** (its own Limitations §7: "a real multi-agent harness is future work"); roles are prompt framing of one agent, not organizational structure; no org-structure independent variable; no typed organizational boundaries (no authority/memory/accountability/human-agent); no mechanism bake-off (only retry vs trusted-state repair); no utility-vs-containment trade-off; tiny cost (~$4 total); arXiv-only company preprint, no venue.
- **Damage assessment:** It occupies "real-LLM cascade radius + per-mode recovery + failure injection over enterprise-workflow framing" and pre-empts the finding "retry is not containment for semantic faults." CAND-1's wedge "Containing the Cascade is simulation-only; we use real LLMs" is **weakened** — a reviewer can now say "OrchestraBench already did real-LLM cascade measurement on enterprise workflows." The accurate residual claim is: real **multi-agent** executions with **organizational structure as the varied factor**.

---

## 2. Fresh searches this wave (beyond wave-1 coverage)

Channels: Semantic Scholar bulk search API (worked; standard search 429), OpenReview search API, arXiv abstract pages, Crossref, Zenodo API, Unpaywall. arXiv export API blocked from this host (429, consistent with wave-1). Raw dumps in `maso_2026_investigation/raw/w2_cand1/`.

### 2.1 Org structure as IV under fault injection — searched, not found (with three partial exceptions)

- S2 bulk: "fault injection organizational structure agents" → **2 total hits, both irrelevant** (software-testing glossary; oilfield study). "role hierarchy error propagation multi-agent" → 2 hits, irrelevant. "hierarchy fault injection LLM multi-agent" → 1 hit (OpsAgent, below).
- **Partial exception 1 — Cascading Instruction Influence** (DOI 10.19139/soic-2310-5070-3574, *Statistics, Optimization & Information Computing* 2026): indirect prompt injection propagation through three-tier command chains; **hierarchical vs centralized topology compared** (compromise rate Cohen's d = 2.34). Structure-as-IV under injection exists — but **adversarial** (prompt injection), **simulation-based**, dubious venue.
- **Partial exception 2 — OpsAgent** (ICAISET 2026, DOI 10.1109/ICAISET66439.2026.11541300): governance-aware 4-layer agentic framework; Hierarchical Policy Graph (approval levels, change windows) encoded in OPA/Rego; **1,074 fault-injection scenarios**; metrics = availability, MTTR, policy compliance. Governance hierarchy + fault injection co-occur — but simulated trace-grounded environments, AIOps framing, no spread metrics, low-tier venue.
- **Partial exception 3 — Topology Linearization for MAS Security** (IEEE Trans. Network Science & Engineering 2026, DOI 10.1109/TNSE.2026.3680460): C-SPRM transforms arbitrary interaction graphs into linearized execution chains to minimize a Spatio-Temporal Attack Surface — **topology modification as containment of propagation** (prompt injection + hallucination), peer-reviewed. Adversarial framing; structure is the *defense*, not the IV; no org semantics.
- Known from wave-1 and re-confirmed as the cluster CAND-1 must differentiate from: Zhou et al. (arXiv:2408.00989, ICML 2025 — linear/flat/hierarchical × faulty agents × Challenger/Inspector); Kim et al. (arXiv:2512.08296 — 5 architectures × error amplification); Loop-Back Authority (arXiv:2609.14767 — authority link as IV, performance only); When Agents Evolve, Institutions Follow (arXiv:2604.27691 — 7 governance topologies as IV, error-correction as design dimension, performance only); **When Do Institutions Beat Intelligence?** (arXiv:2608.11357 — institutional structure vs model capability varied around four collective-failure loci with mechanism-breaking controls; closest "institutions-as-IV-around-failure" work, but collective-reasoning/public-state frame, no injected faults, no spread metrics).

### 2.2 Typed-boundary spread measurement — searched, not found for organizational boundaries

- Typed per-boundary spread metrics exist only for **pipeline stages** (Hallucination Snowball, arXiv:2608.14588: per-stage escape probabilities 24.6%/48.3%/89.3%) and **knowledge-graph hubs** (SCHEMA, arXiv:2608.00711). No work types boundaries as role/authority/memory/accountability/human and measures cross-boundary spread.
- **New this wave — Trust Propagation & Structural Containment** (arXiv:2609.17648, IEEE CARS 2026): 4-agent **role-typed LangGraph pipeline** (Supervisor, Researcher, Validator, Executor); shared-memory poisoning + forged-approval indirect injection; ablates the **authorization boundary** (task-bound signed tokens + policy oracle); Judgment Bypass Rate vs Unsafe Action Rate — memory poisoning reaches execution in 100% of undefended trials; structural authorization contains execution (0% UAR) even when the Validator stays compromised (100% JBR). **Real multi-agent LangGraph execution crossing memory + authority boundaries with a containment ablation** — the closest thing to CAND-1's boundary story found anywhere. Limitations that save CAND-1: adversarial framing, one fixed structure (no org variation), no spread-extent metric across boundary types, no mechanism bake-off (one mechanism vs none), no utility cost, 60 tasks × 3 seeds, minor venue.

### 2.3 Containment-mechanism bake-off (quarantine vs rollback vs revocation vs escalation) — searched, not found

- S2 bulk: "containment mechanism comparison LLM agents" → **0 hits**. "quarantine rollback agent recovery" → 2 hits, both incoherent low-quality venue papers. "delegation revocation LLM agents" → **0 hits**. OpenReview "containment multi-agent" → only control-theory "containment control" (unrelated meaning).
- What exists instead (all wave-1 verified, re-confirmed): CtC's 2-mechanism ablation (simulation); RoMa (CSCWD 2026: isolation/failover/redundancy, success-rate metrics); Self-Healing Agentic Orchestrators (arXiv:2606.01416: retry vs replan vs targeted recovery, single orchestrator); OrchestraBench (retry vs trusted-state repair, single agent); H-RePlan (arXiv:2606.20487: device-local vs global replanning — scope-aware recovery, cross-device not organizational); AIR (ICML 2026: single-agent incident response). **No multi-agent, organizationally-semantic mechanism bake-off exists.**

### 2.4 IMACS × MAS-FIRE combination — does not exist

- Citation check via S2 (2026-09-21): IMACS (2607.25446) has exactly **2 citers** — Testing Interchangeability in LLM Agent Teams (arXiv:2609.05279; role-swap coordination costs, no faults) and When Do Institutions Beat Intelligence? (2608.11357, above). MAS-FIRE (2602.19843) has **11 citers** (incl. CASPIAN 2605.19240 — adversarial cascade detection/attribution; H-RePlan; three attribution papers; surveys). **The citer sets are disjoint — no paper combines executable org science with fault injection.**

### 2.5 "Blast Radius" (arXiv:2608.07440) — checked and dismissed

Literally titled "Blast Radius" but it is a **withdrawn** token-management/context-eviction layer for agentic coding ("NECROPHORESIS", "Algosophy") — unrelated to failure propagation. No threat. Also checked: EvidenceNet (arXiv:2609.10181, authority-scoped network automation, "blast radius" used in passing); Collective Loss of Control (arXiv:2609.18460, epidemic account + RogueHandoff-20 susceptibility benchmark, no org structure, no containment comparison).

---

## 3. Is CAND-1 "just IMACS with faults injected"? — Triviality assessment

**The conceptual combination is obvious; the execution is not. Evidence:**

*For the triviality charge (what a hostile reviewer says):*
- IMACS makes org structure a config knob (Belbin/Mintzberg/RACI in YAML on AgentScope 2.0); MAS-FIRE defines 15 fault types + 3 non-invasive injection mechanisms; OrchestraBench shows a seed-reproducible injection harness with cascade metrics costs ~$4 and 8 pages. "Bolt MAS-FIRE onto IMACS, measure spread" is a one-sentence research plan.

*Against triviality (verifiable facts):*
1. **Neither artifact exists.** MAS-FIRE's repo is data-only (no injection code — F1 verified). IMACS claims release but no repository URL exists anywhere in the paper (D5 verified). CtC's artifact is deleted. The combination is a **build-from-scratch**, not an integration.
2. **Neither substrate has what CAND-1 measures.** IMACS runs stateless QA benchmarks (GSM8K/HumanEval/HotpotQA) and explicitly scopes out "long-horizon tool use, human approval loops, or failures caused by changing external state." CAND-1 needs stateful workflows with deterministic tools and verifiable end-state (tau2-bench style) — new build. IMACS's "organization" is static role/RACI tags — no hierarchy depth, span of control, delegation chains, or authority config as structural variables.
3. **The fault model doesn't exist.** MAS-FIRE has exactly 2 org-flavored faults (role ambiguity, blind trust); nothing for authority/delegation/accountability/memory/human boundaries. A boundary-typed organizational fault taxonomy is a design contribution, not a config.
4. **The metrics don't exist.** MAS-FIRE measures recovery at the fault site (O_f/L_f/S_f); IMACS measures performance; neither measures cross-boundary spread. Boundary-typed blast-radius instrumentation (which roles/tools/memories/authority links a fault touched) is new machinery.
5. **The mechanisms don't exist.** Quarantine, delegation revocation, reroute, human escalation with organizational semantics appear in neither tool (nor anywhere — §2.3).
6. **The empirical risk is real.** OrchestraBench's trusted-state ablation (apparent containment gains were an artifact of the hint) and CtC's simulation-only 99.4% containment show that naive versions of this experiment produce misleading results. The scientific content is precisely in doing it for real.

**Conclusion:** a reviewer can plausibly *say* "IMACS + MAS-FIRE," and CAND-1 must pre-empt this in one paragraph; but the claim of triviality is factually wrong on artifacts, fault model, metrics, and mechanisms. The honest framing: "the cross product is empty and non-trivial to instantiate; here is the instrumentation, the fault model, and the first measurements."

---

## 4. Damage ledger — what is occupied vs what survives

| CAND-1 component | Status | Most damaging occupant |
|---|---|---|
| Term "blast radius" for agent fault spread | **DEAD** (5 senses) | CtC (ICERA 2026); DamageFlow/BRS (ICML 2026 AIWILD); Bounded Agents (2608.15888); ACI (2507.21146); OrchestraBench's "cascade radius" |
| Fault injection + reliability metrics for LLM MAS | **DEAD** | MAS-FIRE (2602.19843); AgentChaos (ASE 2026, code available) |
| Containment metric suite + mediator ablation | **DEAD (in simulation)** | CtC: circuit-breaker-vs-rollback ablation, 46.2%→99.4% containment |
| Real-LLM cascade radius + per-mode recovery on enterprise-framed workflows | **DEAD (single-agent)** | **OrchestraBench (2608.05263) — newly assessed this wave** |
| "Retry is not containment for semantic faults" | **DEAD** | OrchestraBench (retry reproduces latent faults, lengthens TTD) |
| Structure determines fault spread | **DEAD (generic)** | Zhou et al. 2408.00989 (ICML 2025); Kim et al. 2512.08296; Topology Linearization (IEEE TNSE 2026, adversarial) |
| Memory + authority boundary containment, real LangGraph MAS | **OCCUPIED (adversarial)** | Trust Propagation & Structural Containment (2609.17648, IEEE CARS 2026) — newly assessed this wave |
| The research question itself | **DEAD (classical)** | Dellarocas & Klein ICMAS 2000 (unzippering; citizen-vs-survivalist; containment backfires under scarcity) |
| **Org structure (RACI/authority/hierarchy config) as IV under organic fault injection** | **EMPTY** | nearest: OpsAgent (simulated, low-tier); Cascading Instruction Influence (adversarial, simulated, low-tier) |
| **Spread across typed organizational boundaries (authority/accountability/memory/human)** | **EMPTY** | nearest: Hallucination Snowball (pipeline stages); TPSC (adversarial, no spread metric) |
| **Org-semantic containment bake-off (quarantine/rollback/revocation/reroute/human escalation) under utility preservation** | **EMPTY** | nearest: RoMa (3 FT strategies, no org semantics); 2606.01416 (single orchestrator) |
| **Human escalation priced against automated containment for propagating faults** | **EMPTY** | nearest: TAO (rejected ICLR 2026, healthcare); Oversight Has a Capacity (single-agent gating) |
| **Real multi-agent organizational workflows with verifiable state** | **EMPTY** | nearest: OrchestraBench (single-agent chain); AgentFail (observational) |

---

## 5. Required repositioning if CAND-1 advances

1. **Rename.** Do not headline "blast radius." Use "organizational failure propagation" / "boundary-typed spread" and cite all five term occupants.
2. **Frame as organizational resilience science** — the failure/recovery half IMACS explicitly scopes out; cite IMACS as substrate inspiration, MAS-FIRE/AgentChaos as injection lineage, CtC + OrchestraBench + DamageFlow as metric prior art, Dellarocas & Klein as the classical theory being operationalized.
3. **Pre-empt the triviality paragraph** (§3): artifacts absent, fault model absent, metrics absent, mechanisms absent.
4. **The headline findings must be things prior art cannot say**: which boundary type dominates spread; where containment backfires (the Dellarocas-Klein scarcity prediction tested on LLM orgs — a bridge to CAND-2's framing); the escalation-vs-automated cost crossover.
5. **Collision warning:** Emergence World (2609.17320), TPSC (2609.17648), and the institutions-as-IV cluster (2608.11357, 2604.27691, 2609.14767) are all one experiment away from CAND-1's sliver. The window is weeks-to-months, not years.

## 6. Verification log (this wave)

- Crossref: 10.1109/ICERA72709.2026.11666599 (metadata, 0 citations); 10.1109/TNSE.2026.3680460; 10.1109/ICAISET66439.2026.11541300.
- Zenodo API: record 21314250 tombstone (deleted 2026-07-22, "copyright").
- Unpaywall: CtC OA locations = dead Zenodo only.
- arXiv abs + full HTML read: 2608.05263 (OrchestraBench, full text), 2609.17648, 2609.18460, 2608.07440, 2609.10181, 2609.05279, 2608.11357, 2604.27691, 2606.20487, 2605.19240, 2606.26356.
- S2 bulk searches (raw JSON in `raw/w2_cand1/`): "blast radius agent" (51 total), "cascade containment multi-agent LLM" (5), "fault injection organizational structure agents" (2), "quarantine rollback agent recovery" (2), "containment mechanism comparison LLM agents" (0), "role hierarchy error propagation multi-agent" (2), "hierarchy fault injection LLM multi-agent" (1), "delegation revocation LLM agents" (0), "memory contamination multi-agent recovery" (2), "organizational resilience LLM agents fault" (3), "human escalation containment agents cost" (1), "cascade radius orchestration failure" (2).
- S2 citation lists: IMACS (2 citers), MAS-FIRE (11 citers) — disjoint.
- OpenReview search: "blast radius", "organizational fault", "containment multi-agent", "fault injection organization" — nothing beyond known items.
- Blocked: arXiv export API (429), IEEE Xplore full text, DBLP (consistent with wave-1).
