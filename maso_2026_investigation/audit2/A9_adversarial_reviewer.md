# A9 — ADVERSARIAL NOVELTY REVIEW (Reviewer 2, hostile)

**Date:** 2026-09-21
**Target:** "First experimental transfer test of classical MAS fault-handling results (Dellarocas & Klein sentinels, delegation-depth cost inflation, scarcity sign reversal) on tool-executing LLM agent organizations with semantic faults, with containment-mechanism comparison under resource constraints."
**Stance:** Reject for lack of novelty. No benefit of the doubt given.
**Method:** Read the prior 48-report wave first (E1–E6, B1–B18, C1–C6, D1–D5, R1–R3, W2/W3, CtC full-text note). Then ran an independent sweep weighted to what the earlier waves' vocabulary would miss: Crossref bibliographic queries (SSRN/journal gray literature the arXiv-only sweeps cannot see), DataCite title resolution, OpenReview search, arXiv abstract-page verification via FetchURL. arXiv search UI, Semantic Scholar, and OpenAlex were rate-limited/blocked from this host for most of the session (shared-IP exhaustion by the swarm); every load-bearing item below was verified against its arXiv abs page, ACL Anthology record, or Crossref record — never a search snippet.

---

## 1. THE TEN STRONGEST REJECTION CITATIONS

Ranked by damage to the novelty claim as stated. Verification level marked per item.

### R1. Dellarocas & Klein, "An Experimental Evaluation of Domain-Independent Fault Handling Services in Open Multi-Agent Systems," ICMAS 2000, DOI 10.1109/ICMAS.2000.858440
**FULL TEXT VERIFIED** (E5 read the MIT WP PDF; I re-checked the Crossref record and E5's dissection).
The candidate's three hypotheses are this paper's three experiments: delegation-tree depth → completion-cost inflation ("unzippering," 600–700% of baseline at depth 4); sentinel/EH services → containment (≤1%–216% vs 600–700%); **containment backfires under subcontractor scarcity** (EH slightly worse than survivalist with short tasks + scarce subcontractors). The candidate's H1/H2/H3 are, by its own framing, a substrate swap of a 26-year-old paper. A MASO/PRIMA reviewer pool (van der Torre, Najjar, Calvaresi lineage) will know this paper. The novelty claim survives only on the word "transfer" — i.e., the contribution is *replication*, and the paper must be written as one.

### R2. Divi, Gullapalli & Brahmandam, "Containing the Cascade," IEEE ICERA 2026, DOI 10.1109/ICERA72709.2026.11666599
**FULL TEXT VERIFIED** (reports/CtC_fulltext_verification.md, IEEE Xplore PDF, 21 Sep 2026).
Occupies: the metric vocabulary (containment rate, cascade depth, blast radius, MTTD), a five-condition mechanism comparison (No Guard / Retry / Verifier / Debate / SENTINEL), and a fail-safe/fail-operational ablation (circuit breaker → containment; checkpoint rollback → task completion) in tool-using LLM MAS fault injection. Simulation-only, no org-structure IV, no boundary typology — but a reviewer who reads the candidate's "containment-mechanism comparison" and "utility preservation under containment" will pattern-match here first. The differentiation ("real LLM executions, organizational IV") is one substrate swap + one new independent variable.

### R3. Xiang, "When Do Audited Action Gates Help? The Cost and Failure Conditions of Epistemic Strictness in LLM Agents," SSRN 2026, DOI 10.2139/ssrn.7348298 — **NEW FIND; missed by both waves**
**ABSTRACT VERIFIED** (full Crossref abstract retrieved and read 21 Sep 2026; paper itself not yet read — flagged).
This is the most dangerous paper for H3 found anywhere in this investigation. Synthetic fault-diagnosis environment; 1,330 completed agent runs on nine models; pre-registered hypotheses with Holm correction. Finding (iv), verbatim: **"The gate's effect changes sign with the verification budget: with no budget it reduces accuracy by 0.315, and the budget-by-gate interaction (DiD = +0.456 [+0.297, +0.625]) is the largest effect we measure."** Closing sentence: an audited gate prevents a contaminated belief set from degrading action "**and only when the system can afford to verify**." That is H3's scarcity-induced sign reversal — a containment/verification mechanism that helps under abundance and hurts under scarcity — already measured experimentally on LLM agents, with better statistics than the candidate's own plan. Also: finding (iii) shows gate benefit concentrated in already-poorly-performing systems (+0.31 vs +0.01) — a second, capability moderator the candidate does not consider; finding (ii) shows self-reported verification is worthless and only harness-audited gates help — which *predicts the outcome* of the candidate's oracle-vs-learned-detector arm. Mitigations: single-agent (no organization, no propagation), SSRN preprint, scarce resource = per-agent verification budget rather than org-level token/tool/reviewer budgets. But the *headline phenomenon* of H3 is published. H3 is now squeezed from both sides: D&K owns it classically, Xiang owns it on the LLM substrate.

### R4. Kim et al., "Towards a Science of Scaling Agent Systems," arXiv:2512.08296 (v3 Apr 2026)
**ABSTRACT VERIFIED** (arXiv abs page read 21 Sep 2026).
260 controlled configurations, five architectures (single-agent, independent, centralized, decentralized, hybrid), three LLM families, standardized tools/prompts/compute. Key finding: "**architectures without centralized verification tend to propagate errors more** than those with centralized coordination"; multi-agent overhead on tool-heavy tasks; architecture–task alignment determines success (−70.0% to +80.8% vs single-agent). This is org/architecture structure as IV × verification as moderator × error propagation as DV — the candidate's claims 1, 2, and 12 in one controlled study. Not framed as fault injection or organizational theory, and no recovery/cost vector — but the structure→propagation→verification triangle is occupied at 260-config scale.

### R5. Huang et al., "On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents," ICML 2025, arXiv:2408.00989
**ABSTRACT VERIFIED** (arXiv abs page read 21 Sep 2026; prior waves read more).
Structure (chain/flat/hierarchical) × injected faulty agents (AutoTransform/AutoInject) × containment mechanisms (Challenger, Inspector recovering up to 96.4% of errors). Hierarchical most resilient (5.5% vs 10.5%/23.7% drops). Occupies claims 1, 4 (clumsy = non-adversarial faults), 7 (inspector agents), 12 (structure × containment). Toy 3-agent structures and no cost measurement — but it is the peer-reviewed, code-available anchor a reviewer will cite against "first to vary structure and measure fault impact in LLM MAS."

### R6. Turan, "Oversight Has a Capacity: Calibrating Agent Guards to a Subjective, Fatiguing Human," arXiv:2606.08919 (Jun 2026)
**ABSTRACT VERIFIED** (arXiv abs page read 21 Sep 2026; also in wave-1 B8).
Human reviewer modeled as endogenous and fatiguing: **realized safety is an inverted-U in escalation rate — more human oversight can make the system less safe**; a flooding attack slips malicious actions past the fatigued reviewer. Occupies claims 11 (containment backfire), 17 (human oversight under load), 18 (reviewer-capacity constraints) — including the *sign-reversal-under-load* shape of H3 for the human arm. Single-agent action gating, modeling results (no human study yet) — but the candidate's "priced human escalation with queue-latency sweep" is this paper's framing extended.

### R7. Yagiz, "DamageFlow/BlastGuard: What Can One Bad Tool Call Destroy?", OpenReview MYvsxnxbCf (May 2026)
**PARTIALLY VERIFIED** (wave-1 B8/B9/E3 read the OpenReview page; I re-confirmed the record exists).
Blast Radius Score decomposes into propagation **and recovery cost**; containment runtime retains 87.5% benign utility. Occupies claims 6, 8, 20 and the metric philosophy (provenance-traced damage with utility preservation). Adversarial frame, 80-scenario pilot — but "OBR with a different denominator" is a fair hostile read.

### R8. Babu & Agrawal, "Self-Healing Agentic Orchestrators for Reliable Tool-Augmented LLM Systems," arXiv:2606.01416 (May 2026)
**ABSTRACT VERIFIED** (arXiv abs page read 21 Sep 2026; also in wave-1 E4/W2-cand4).
Controlled 100-task fault-injection benchmark on tool-augmented LLM systems; **four recovery strategies compared (static / retry-only / ReAct / full-replanning vs targeted self-healing) under a matched recovery-budget sweep** — self-healing wins at *every* budget, largest gap at one recovery attempt (94.0% vs 85.3%/88.2%); verifier-guided recovery eliminates silent failures. This is the candidate's H2 experimental template (mechanism comparison × resource budget × utility) already executed — with the *opposite* of H3's prediction (no backfire at low budget), which is itself a useful hostile exhibit: where backfire was sought with a budget sweep, none appeared. Single orchestrator, not MAS.

### R9. Chen et al., "OrchestraBench," arXiv:2608.05263 (Aug 2026)
**PARTIALLY VERIFIED** (wave-2 W2-cand1 read full text; E6 flagged it).
Failure-injection harness over templated enterprise workflows; "cascade radius" + per-failure-mode recovery as primary metrics; routing-policy comparison with bootstrap CIs and paired tests. Occupies claims 5, 6, 8 at the orchestration level. Single-LLM chains, no org boundaries.

### R10. La Malfa et al., "Large Language Models Miss the Multi-Agent Mark," NeurIPS 2025 position, arXiv:2505.21298 — plus the transfer-genre anchors
**ABSTRACT VERIFIED** (wave-2 W2-cand2; record re-confirmed).
Pre-stakes the framing at a top venue: LLM-"MAS" must engage classical MAS or "revisit problems the MAS literature has already addressed." Combined with the established re-test-classical-X-with-LLMs genre (Aher et al. ICML 2023 oral, arXiv:2208.10264; Akata et al. Nat. Hum. Behav. 2025, DOI 10.1038/s41562-025-02172-y; "Can Lessons From Human Teams Be Applied to MAS?", arXiv:2510.07488 — **ABSTRACT VERIFIED** by me: flat > hierarchical structure transfer), the hostile read is: the candidate is an instance of a four-year-old genre answering a named, published call — valuable, not novel in framing.

**Bench (also citable):** Alignment Backfire, arXiv:2603.04904 (NEW; safety-intervention *directional reversal* in LLM MAS, 1,584 preregistered simulations — ABSTRACT VERIFIED); Feedback That Backfires, arXiv:2608.23651 (NEW; the standard "delete-and-retry-from-clean-context" recovery prescription is the *worst* harness measured — ABSTRACT VERIFIED); Tran & Kiela, arXiv:2604.02460 (NEW; MAS advantage over single-agent vanishes under equal token budgets — structure × scarcity — ABSTRACT VERIFIED); FTDI, now journal-published in *Expert Systems with Applications* (DOI 10.1016/j.eswa.2026.134164 — budget-aware self-healing LLM MAS; METADATA VERIFIED); AgentRevive, ACL 2026 (2026.acl-long.373 — soft-quarantine state machine Active/Standby/Terminated for hallucination-prone agents with token-consumption reduction; ABSTRACT VERIFIED via ACL Anthology); RoMa, CSCWD 2026 (isolation+rehabilitation quarantine; wave-1 verified); AIR, ICML 2026 (incident containment/recovery lifecycle; wave-1 verified).

---

## 2. THE 20-CLAIM COLLISION TABLE

Severity scale: EXACT (same claim, same substrate, published) / NEAR (same claim, adjacent substrate or missing one conjunct) / PARTIAL (core mechanism occupied, setting differs materially) / ADJACENT (same neighborhood, different question) / NONE (nothing found). Hostile ratings: I round *up* in severity wherever defensible.

| # | Claim | Closest prior paper | Severity |
|---|---|---|---|
| 1 | Org structure as IV | Kim et al. 2512.08296 (5 architectures × 260 configs, error propagation readout); Huang 2408.00989; "When Do Institutions Beat Intelligence?" 2608.11357 (institutional structure as IV around 4 collective-failure loci — ABSTRACT VERIFIED) | **NEAR** (communication/architecture structure, not decision-rights org constructs) |
| 2 | Depth → propagation | Dellarocas & Klein ICMAS 2000 (unzippering up 4-level contracting trees) — classical EXACT; CTHA 2601.10738 (hierarchical unbounded error propagation, 47% cascade reduction) | **NEAR** |
| 3 | Depth → recovery cost | D&K ICMAS 2000 (600–700% completion-time inflation growing with depth) — classical EXACT; no LLM-era depth-vs-recovery-cost measurement found | **PARTIAL** |
| 4 | Non-adversarial semantic fault propagation | Hallucination Cascade 2606.07937 (500 cascades, amplification factor 0.644); Woozle/DIGRA TASLP 2026; **Emergent Misinformation Genesis, DOI 10.22541/au.177499233.37732392/v1 (NEW — 4,800 trials, zero adversarial input, multi-agent clinical pipelines spontaneously generate dangerous assertions; ABSTRACT VERIFIED)** | **NEAR** |
| 5 | Tool-executing MAS fault propagation | Containing the Cascade ICERA 2026 (simulation); AgentChaos 2608.06790 (real execution, API layer); "When Tool Calls Succeed but Workflows Fail" 2609.15397 | **NEAR** |
| 6 | Containment mechanism comparison | CtC 5-condition bake-off + fail-safe/fail-operational ablation; Self-Healing Orchestrators 2606.01416 (4 strategies × budget sweep); RoMa (3 strategies); DamageFlow | **NEAR** |
| 7 | Verifier/inspector agents | Huang 2408.00989 Inspector (96.4% error recovery, peer-reviewed, code public); CtC Verifier arm; TAO tiered oversight; LLM-as-a-Verifier 2607.05391 | **EXACT** (as a mechanism evaluated in LLM-MAS fault settings; only the org-propagation framing is new) |
| 8 | Recovery cost measurement | Self-Healing Orchestrators (budget sweep); AIOpsLab 2501.06706 (token cost/incident); ITBench (MTTR); Who&When (attribution hours); classical checkpoint-overhead line (Young 1974, Daly 2006) | **PARTIAL** (cost measured in pockets; no priced recovery-cost vector for org faults) |
| 9 | Resource scarcity × recovery | D&K (abundant/scarce × EH) classical EXACT; **Xiang SSRN 7348298 (verification budget × gate)**; FTDI ESWA 2027 (budget-aware self-healing); 2606.01416 (recovery-budget sweep) | **NEAR** |
| 10 | Scarcity-induced sign reversal | **Xiang SSRN 7348298 — gate effect changes sign with verification budget, DiD +0.456, largest effect measured, on LLM agents**; D&K classical (EH worse under scarcity) | **NEAR** (hostile: arguably EXACT for the phenomenon; only the multi-agent org setting differentiates) |
| 11 | Containment backfire | Xiang 7348298; Alignment Backfire 2603.04904 (intervention reversal in LLM MAS); Turan 2606.08919 (inverted-U oversight); Feedback That Backfires 2608.23651 (retry prescription backfires); D&K classical | **NEAR** |
| 12 | Structure × containment | Kim 2512.08296 (architecture × centralized verification → propagation); Huang 2408.00989 (structure × Inspector/Challenger); TPSC 2609.17648 (structural containment) | **NEAR** |
| 13 | Structure × scarcity | D&K 4-cell design (depth × abundance) classical EXACT; **Tran & Kiela 2604.02460 (SAS vs MAS architectures under matched token budgets — NEW)** | **NEAR** |
| 14 | Structure × containment × scarcity | D&K has all three axes classically; LLM-era: nothing found in two waves + this sweep | **PARTIAL** (the candidate's strongest cell; classical-only occupancy) |
| 15 | Classical MAS fault-handling transfer | No experimental transfer test exists (W2-cand2 citation analysis: D&K 1 post-2023 citer, 0 LLM; Hägg 0 LLM citers). Framing pre-staked: La Malfa 2505.21298, Bădică 2509.02515, Mieczkowski 2603.12229, Terrarium 2510.14312, SHIELDA 2508.07935. Genre: Aher/Akata/2510.07488 | **ADJACENT** (literal claim unoccupied; framing and genre occupied) |
| 16 | Sentinel/quarantine | Hägg 1997 + D&K 2000 (classical EXACT); AgentRevive ACL 2026 (soft quarantine, token reduction); RoMa (isolation+rehabilitation); CtC SENTINEL | **NEAR** |
| 17 | Human oversight under load | Turan 2606.08919 (fatigue, inverted-U, flooding attack); FALCON 2604.00904 (fatigue-aware CMDP deferral — ABSTRACT VERIFIED); Kadowaki SSRN (oversight solvency); READY 2609.02095 | **NEAR** |
| 18 | Reviewer-capacity constraints | DeCCaF (TMLR; deferral under human work-capacity constraints); FALCON (cooperation budgets); AI Control ICML 2024 (audit budget on safety-usefulness Pareto); Turan 2606.08919 | **NEAR** |
| 19 | Fault handling in irreversible environments | **Irreversibility Budget 2609.00275 (NEW — fleet-level irreversibility as first-class budgeted resource, admission control, AgenticOS@SOSP; ABSTRACT VERIFIED)**; **Spawn Freely, Act Sparingly 2609.01035 (NEW — irreversible-action boundary, trajectory risk escrow, authority reproduction number R_A; ABSTRACT VERIFIED)**; Cordon 2606.17573; SagaLLM PVLDB 2025; EvoUndo 2608.28363 | **PARTIAL** (prevention/accounting occupied; post-commit recovery dynamics under irreversibility less so) |
| 20 | Utility-preserving recovery | DamageFlow (87.5% benign utility retained); CtC (success under containment); 2606.01416 (success under budget); AIR ICML 2026; classical graceful degradation (Hystrix) | **NEAR** |

**Hostile summary:** 1 EXACT, 13 NEAR, 5 PARTIAL, 1 ADJACENT, 0 NONE. No claim is wholly unoccupied; the candidate's novelty lives entirely in *conjunctions* and in the classical-transfer framing (claim 15).

---

## 3. WHAT THE PRIOR WAVES MISSED (new finds this sweep)

All verified this session; none appear in the 48 prior reports (grepped) or in the concurrently-written audit2 reports (checked A1/A3/A6/A7/A10):

1. **Xiang, SSRN 7348298** — the H3 sign reversal measured on LLM agents (see R3). Highest-threat new find.
2. **Alignment Backfire, arXiv:2603.04904** (5 Mar 2026) — preregistered directional reversal of alignment interventions in LLM MAS across 16 languages; iatrogenesis of countermeasures. "Interventions backfire" is published *in LLM MAS*, moderated by language rather than scarcity.
3. **Feedback That Backfires, arXiv:2608.23651** (24 Aug 2026) — failure records in the transcript make agents *repeat* the failed call (corrective gain negative on 6 checkpoints); "delete the failed attempt and retry from a clean context — the standard prescription for context contamination — is the worst harness we measured." A standard recovery prescription experimentally backfiring.
4. **Tran & Kiela, arXiv:2604.02460** (2 Apr 2026) — under equal thinking-token budgets, single-agent matches/beats MAS on multi-hop reasoning across three model families. Structure × scarcity with an information-theoretic (Data Processing Inequality) argument.
5. **The Irreversibility Budget, arXiv:2609.00275** (31 Aug 2026, AgenticOS @ SOSP) — fleet-level irreversibility accounting; per-effect gates overdraw tenant risk 48×; budget holds every correctly charged run. Irreversibility as a *budgeted resource* for agent fleets.
6. **Spawn Freely, Act Sparingly, arXiv:2609.01035** (1 Sep 2026) — recursive LLM-agent trees with trajectory-level risk escrow; authority reproduction number R_A crossing 1 changes trajectory-harm scaling (p below criticality, √p at criticality). A branching-process treatment of authority propagation depth.
7. **Emergent Misinformation Genesis, DOI 10.22541/au.177499233.37732392/v1** (31 Mar 2026) — 4,800 trials, ~97k API calls: multi-agent clinical pipelines generate dangerous assertions no individual agent produces, zero adversarial input; EMR metric + Clinical Escalation Index.
8. **Token Budgets catalog, arXiv:2606.04056** (2 Jun 2026) — 63 production budget-overrun incidents across 21 orchestration frameworks; retry loops spending thousands of dollars; delegation-fanout race in 11 incidents. (Concurrently found by audit2/A1.)
9. **FTDI journal version** — budget-aware self-healing for LLM MAS now in *Expert Systems with Applications* (10.1016/j.eswa.2026.134164, Jan 2027 issue), upgrading it from SSRN preprint to peer-reviewed occupancy.
10. **Sah & Stiglitz, "The Architecture of Economic Systems: Hierarchies and Polyarchies"** (NBER WP 1334, 1984; AER 76(4), 1986) and "Committees, Hierarchies and Polyarchies" (Economic Journal 1988, DOI 10.2307/2233377 — METADATA VERIFIED via Crossref) — the org-*economics* fallibility literature: hierarchies vs polyarchies as error-filtering structures for fallible decision-makers. The candidate's "classical transfer" engages only the MAS-engineering lineage (D&K, Hägg, Horling & Lesser) and ignores the org-econ lineage that *also* makes structure×fallibility predictions — a scholarship gap a hostile reviewer can weaponize, and a source of alternative predictions (hierarchies reject bad projects but also good ones; polyarchies are error-tolerant but wasteful) that map onto containment-vs-utility.

---

## 4. STRONGEST SURVIVING GAP (stated against my own interest)

The quadruple conjunction remains verifiably empty: **organizational decision-rights structure as the manipulated variable × non-adversarial semantic faults × real tool-executing multi-agent LLM workflows × priced containment/recovery bake-off including a human arm.** Within it, the two most defensible cells:
- **Claim 14 (structure × containment × scarcity on LLM substrate)** — occupied only classically (D&K). But note: each *pair* is now occupied on LLM substrates (12 by Kim/Huang, 13 by Tran & Kiela, 9/10 by Xiang/FTDI/2606.01416), so the triple is one experiment away for three different groups.
- **Claim 15 (experimental classical transfer)** — literally unoccupied, but it is a *framing* novelty over a substrate swap; its suspense problem is now worse than R1 thought, because Xiang (R3) already produced the LLM-substrate sign reversal without any classical framing.

## 5. ONE UNEXPECTED FINDING

Xiang (SSRN 7348298) found the gate's benefit is concentrated almost entirely in systems that were *already performing poorly* (+0.31 when baseline < 0.60 vs +0.01 at 0.80–0.95; permutation p = 0.0007). If that heterogeneity generalizes, the candidate's H3 sign reversal may be confounded with a **capability × containment interaction** — containment helps weak organizations and taxes strong ones — which the candidate's design (fixed model tier per arm) cannot separate from scarcity. Also found: 2606.01416 ran the mechanism × budget sweep and found *no* backfire at any budget — the backfire is mechanism- and setting-dependent, not a robust law, which cuts both ways for H3's pre-registration.

## 6. VERIFICATION LOG

- **FULL TEXT VERIFIED (relied on from prior waves):** D&K ICMAS 2000 (E5); CtC (CtC_fulltext_verification.md); Kota TAAS 2012 (E5).
- **ABSTRACT VERIFIED this session** (arXiv abs page / Crossref full abstract / ACL Anthology record read by me, 21 Sep 2026): SSRN 7348298 (Crossref abstract in full); arXiv 2512.08296, 2408.00989, 2510.07488, 2608.11357, 2606.01416, 2606.08919, 2609.00275, 2609.01035, 2607.16530, 2604.00904, 2603.04904, 2608.23651, 2606.04056, 2604.02460; ACL 2026.acl-long.373 (AgentRevive); Crossref abstracts/metadata: 10.22541/au.177499233.37732392/v1, 10.1016/j.eswa.2026.134164, 10.2307/2233377, 10.3386/w1334, 10.48550/arxiv.2403.06906 (DeCCaF).
- **PARTIALLY VERIFIED (prior-wave full/partial reads, records re-confirmed):** DamageFlow MYvsxnxbCf, OrchestraBench 2608.05263, RoMa, AIR, La Malfa 2505.21298.
- **Not independently re-verified (prior-wave abstract-level, marked):** CTHA 2601.10738, Hallucination Cascade 2606.07937, Woozle TASLP 2026, AgentChaos 2608.06790, TPSC 2609.17648, TAO, AIOpsLab, ITBench, Who&When, AI Control 2312.06942, Kadowaki SSRN, READY 2609.02095, Hägg 1997, SagaLLM, Cordon, EvoUndo, 2609.15397.
- **Channel failures:** arXiv search UI + export API (429 all session), Semantic Scholar (429), OpenAlex (daily budget exhausted), DBLP (bot wall). Compensated with Crossref, DataCite, OpenReview, arXiv abs pages, ACL Anthology. Recall risk: papers without Crossref/DataCite presence and not yet on arXiv abs pages I sampled could be missed; 19–21 Sep arXiv submissions are unannounced and invisible to everyone.
