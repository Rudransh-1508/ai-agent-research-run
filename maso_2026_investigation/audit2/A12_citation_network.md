# A12 — Citation-Network Audit (Agent 12)

**Date:** 2026-09-21
**Mission:** Backward + forward citation-graph search on 15 anchor papers; flag citers combining {faults/recovery} × {structure/depth} × {resources/budget}; identify same-author follow-ups and workshop→expanded versions; surface papers keyword search plausibly missed.
**Sources:** Semantic Scholar Graph API (metadata, citations, references, batch; heavy shared-IP 429s handled with serialized retry/backoff), OpenCitations COCI (DOI↔DOI citation edges — independent second graph), Crossref (DOI resolution), arXiv abs pages (version history, dates, comments), ar5iv full-text (reference-list extraction for 7 anchors). OpenAlex was exhausted (retry-after 38508s); OpenReview API bot-blocked from this host; arXiv export API 429.
**Raw data:** `maso_2026_investigation/audit2/raw_s2/` (all JSON responses + arXiv/ar5iv snapshots preserved).

---

## 1. Headline results

1. **The triple intersection is empty in the citation graph.** Across ~1,060 unique post-2024 citers of the 15 anchors, **no paper combines faults/recovery × organizational structure/depth × resources/budget**. The closest pairwise combinations are enumerated in §4.
2. **The classical fault-handling canon is citation-disconnected from the LLM-MAS literature — confirmed from BOTH directions.** Forward: Dellarocas & Klein ICMAS 2000 has exactly 2 post-2024 citers (both classical JaCaMo lineage, zero LLM content); Kota TAAS 2012 has 1 (irrelevant). Backward: of ~445 references across the 11 LLM-era anchors, the ONLY classical-MAS organizational citations are in Loop-Back Authority (Horling & Lesser 2004; MOISE+ 2002; Contract Net 1980) — organizational *structure* theory, **not** the fault-handling canon (no Dellarocas & Klein, Kota, or Hägg anywhere). The "first experimental transfer test" framing survives the citation-graph attack.
3. **Citation-graph search found 7+ relevant papers that the 48 keyword-based reports missed** (§5) — the strongest being **Sherlock** (cost-optimal verification placement + rollback, Microsoft) and **ResMAS** (topology × resilience optimization under agent failures).
4. **No scoop signal for the nearest neighbor:** Containing the Cascade has **0 citations** in both S2 and COCI; no expanded version visible in the graph.

## 2. Per-anchor results

### 2.1 Dellarocas & Klein, ICMAS 2000 (DOI:10.1109/ICMAS.2000.858440) — FULL TEXT of citers not needed; citation lists VERIFIED via S2 + COCI
- S2: 57 citations; **post-2024 citers: 1** — Baldoni, Baroglio, Micalizio & Tedeschi, "Exception handling in multi-agent oriented programming," Knowledge Engineering Review 2025 (DOI:10.1017/S0269888925000050). Classical JaCaMo organizational exception handling; no LLM content (confirms W2_assassin_cand2).
- **COCI (independent graph) found a second post-2024 citer that S2 has NOT indexed:** Baldoni, Baroglio, Micalizio & Tedeschi, **"Robust Multi-Agent Systems in JaCaMo: A Practical Guide to the Use of Exception Handling and Accountability,"** Springer LNCS "Agents and Multi-Agent Systems Development," 2026 (DOI:10.1007/978-3-032-01082-7_9 — title/container/authors VERIFIED via Crossref; content not read, ABSTRACT UNAVAILABLE — but JaCaMo is a classical Jason+CArtAgO+Moise platform; LLM content implausible). **Same-author follow-up of the KER 2025 paper.** Significance: the Turin group is actively extending classical organizational exception handling in 2026 — the transfer could be done "from the classical side"; worth monitoring, currently zero LLM content.
- 2015–2021 citers: spectrum-based fault localization for MAS (2015, 2017) and the same Turin JaCaMo line (2021 ×2). Nothing else alive.

### 2.2 Huang et al., "On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents" (arXiv:2408.00989, ICML 2025) — citation list VERIFIED via S2 (115 citations, all retrieved)
- 111 post-2024 citers. **Same-author follow-ups:** none on fault tolerance (PIMMUR principles; IP-leakage attacks; JARVIS-or-Ultron CUA safety survey — all different topics).
- Fault×structure citers: **ResMAS** (see §5.2); RoMa (credibility-aware fault tolerance — known); "From Thinker to Society: Security in Hierarchical Autonomy Evolution"; "Hierarchical Attacks for Multi-Modal Multi-Agent Reasoning" (adversarial).
- Fault×resources citers: **DART** (§5.1); "Heterogeneous LLM Debate Under Adversarial Peers: Honest Gains, Replacement Costs, and Resilience" (2606.19826 — debate-panel replacement costs, adversarial); "Safe and Efficient Resource Allocation in Multi-AI-Agent LLM Systems" (IEEE CloudSummit 2026, DOI:10.1109/CloudSummit68932.2026.00053 — resource allocation, no fault-propagation content visible; TITLE/venue VERIFIED, abstract not obtained).
- Notable: MAS-FIRE, AgentChaos, Who&When Pro, Collective Loss of Control (2609.18460) all cite Huang — the anchor is central to the cluster.

### 2.3 MAS-FIRE (arXiv:2602.19843, 2026-02-23) — VERIFIED via S2 (11 citations, all retrieved)
- Citers: H-RePlan "Beyond Global Replanning: Hierarchical Recovery for Cross-Device Agent Systems" (2606.20487 — hierarchical = device-local vs orchestrator replanning granularity, NOT org depth as IV; abstract VERIFIED); CASPIAN (adversarial cascade detection — known); three attribution papers; on-device MAS survey (IEEE ICWS 2026); PARA enterprise readiness. **No same-author follow-up. No faults×structure×resources citer.**
- References (62): zero classical-MAS lineage (S2 refs + ar5iv full-text scan agree).

### 2.4 Who&When (arXiv:2505.00212, ICML 2025) — VERIFIED via S2 (159 citations, all retrieved)
- **Same-author expanded follow-up confirmed: "Who&When Pro: Can LLMs Really Attribute Failures in AI Agents?" (arXiv:2607.09996, 2026-07-10, 5 citations; Liu, Xi, S. Zhang, Zeng, Yue, C. Wang, Kang, Wu, H. Wang)** — the workshop→expanded pattern exists here but stays in the attribution lane (already known to wave-1 reports).
- 157 post-2024 citers, overwhelmingly attribution/diagnosis. New-to-audit finds: "Multi-Agent-based Failure Recovery Planning for a Connected Vehicle Platform" (IEEE DSN-W 2026, DOI:10.1109/DSN-W70714.2026.00022… actually 00021 — classical planning, connected vehicles, LOW relevance; metadata VERIFIED); "Human oversight of agentic systems in practice" (FAccT 2026, arXiv:2606.05391 — qualitative study of developer oversight work; relevant context for the human-escalation arm; metadata VERIFIED).
- CtC and From Spark to Fire both cite Who&When (graph-confirmed).

### 2.5 MAST "Why Do Multi-Agent LLM Systems Fail?" (arXiv:2503.13657, NeurIPS 2025) — VERIFIED via S2 (610 citations; all 7 pages retrieved)
- 590 post-2024 citers. **Same-author follow-ups:** "Fantastic Adaptive Taxonomies and How to Use Them" (arXiv:2607.16387, Pan/Zaharia/Stoica — taxonomy methodology, NOT in prior reports; low threat); "Measuring Agents in Production" (arXiv:2512.04123, 43 cites — known); others (AstraFlow, Barbarians) off-topic.
- **Strongest citer find: Sherlock (arXiv:2511.00330)** — see §5.1.
- CtC cites MAST (graph-confirmed). No faults×structure×resources citer.

### 2.6 From Spark to Fire (arXiv:2603.04474, 2026-03-04) — VERIFIED via S2 (12 citations, all retrieved)
- Citers include: **"Delayed Verification Destabilizes Multi-Agent LLM Belief: Instability Thresholds and Optimal Corrector Placement"** (arXiv:2606.27409, Itkin — see §4.2; already in B15/B3 reports); SoK "When Safe Agents Fail Together" (2609.00595); CASPIAN; QUIVER; **"Mitigating Fabrication in Multi-Stage LLM Pipelines for Hiring"** (2608.26171 — prompt guardrails vs HITL checkpoints, 180-run controlled comparison with a human arm; NEW to this audit; abstract VERIFIED — single pipeline, hiring domain, no org structure); "Evidence-State Reliability Under Controlled Degradation" (2608.21559 — NEW; degradation conditions in a 3-stage pipeline; abstract VERIFIED).
- References (61, ar5iv full-text): zero classical fault-handling lineage. Only "sentinel" hit is **SentinelAgent (arXiv:2505.24201)** — graph-based anomaly *detection* for LLM MAS (abstract VERIFIED via arXiv) — the word "sentinel" has been re-occupied in the LLM era in the detection sense, NOT the Dellarocas-Klein exception-handling sense. Worth one disambiguation sentence in the paper.

### 2.7 AgentChaos (arXiv:2608.06790, ASE 2026) — VERIFIED via S2
- **0 citations** (too recent, 2026-08-07). References (56): zero classical lineage; cites Huang, MAS-FIRE, and a TOSEM survey on failure analysis/fault injection in AI systems.

### 2.8 Containing the Cascade (DOI:10.1109/ICERA72709.2026.11666599) — VERIFIED via S2 + COCI
- **0 citations in both graphs.** References elided by publisher in S2; 0 reference edges in COCI (IEEE does not deposit). Full text already verified separately (reports/CtC_fulltext_verification.md). **No expanded version and no citers visible — no scoop signal as of 2026-09-21.**
- **CORRECTION to a prior report:** CtC_fulltext_verification.md (§"Other notable facts") claims CtC refs [32]–[33] are self-citations to "the same group's IJEDR/ICAISET papers," identifying the ICAISET one as OpsAgent. I pulled OpsAgent (ICAISET 2026, DOI:10.1109/ICAISET66439.2026.11541300) via the S2 graph endpoint: its authors are **Muppuri, Madugundi & Singh — zero overlap with the CtC group (Divi, Gullapalli, Brahmandam)** (VERIFIED via S2 metadata). The "OpsAgent = CtC same group" claim is therefore **wrong**; CtC's actual self-citations (if any) could not be re-verified because its reference list is publisher-elided in both graphs. Practical impact is minor (the "CtC group is actively working this lane" inference weakens; the scoop-risk argument from their stated future work stands on the full text alone).

### 2.9 DamageFlow / BlastGuard (OpenReview MYvsxnxbCf, ICML 2026 AIWILD)
- OpenReview API bot-blocked from this host; S2 search endpoint rate-limited through 16+ retry attempts across the session — **S2 indexing/citation status UNVERIFIED from this lane**. Paper itself already fully characterized via OpenReview in C4_openreview.md (single-author Yagiz; adversarial tool-boundary blast radius; BRS metric). Given workshop-poster status (cdate 2026-05-08), near-zero citation visibility expected; treat as UNVERIFIED rather than 0.

### 2.10 Loop-Back Authority (arXiv:2609.14767, 2026-09-13) — VERIFIED via S2
- **0 citations.** References (60, S2): **the only LLM-era anchor engaging classical organizational MAS** — Horling & Lesser 2004 (organizational paradigms), Hübner et al. MOISE+ 2002, Smith Contract Net 1980. Crucially it does NOT cite the fault-handling canon (no Dellarocas & Klein / Kota / Hägg) and studies performance, not faults (consistent with W2_assassin_cand2's finding).

### 2.11 IMACS (arXiv:2607.25446, 2026-07-28) — VERIFIED via S2 (2 citations)
- Citers: "Testing Interchangeability in LLM Agent Teams" (2609.05279 — role-swap coordination costs, no faults) and "When Do Institutions Beat Intelligence?" (2608.11357 — institutional structure vs model capability as IVs around four collective-failure loci with mechanism-breaking controls; already assessed in W2_assassin_cand1 as closest institutions-as-IV work; no injected faults, no spread metrics). References (29): zero classical lineage.

### 2.12 Atomix (arXiv:2602.14849, 2026-02-16) — VERIFIED via S2 (24 citations, all retrieved)
- **Same-author follow-ups (Mohammadi/Bindschaedler group):** **"The Irreversibility Budget: Fleet-Level Risk Accounting and Admission Control for Agent Operating Systems" (arXiv:2609.00275, 2026-08-31 — NEW to this audit; abstract VERIFIED)** — treats irreversibility as a first-class *resource* with per-principal budgets and admission control; per-effect gates overdraw fleet risk up to 48×. Budget-as-resource framing, but for risk admission of effects, NOT containment-mechanism economics; no org structure, no scarcity sign reversal of containment. Also "Ghost Tool Calls" (2606.02483) and "Don't Trust the Code, Check Its Effects" (2609.00430).
- Recovery-cluster citers (all NEW to this audit, abstracts VERIFIED): **REVISE** (2609.00643 — validity-guided fine-grained recovery; correctness–efficiency trade-off of recovery granularity); **"Safe to Resume?"** (2608.29381 — first security study of checkpoint/rollback in agent systems; five C/R failure modes; in C2 report); **"When Can Agents Safely Checkpoint, Fork, Restore, and Merge?"** (2608.22928 — exact safety checking for execution edits); "Agentic Transaction" (2608.13900 — ACID for agents). This cluster occupies the *mechanisms* of recovery; none varies org structure or budgets adversarially.
- References (57): zero classical lineage.

### 2.13 Oversight Has a Capacity (arXiv:2606.08919, 2026-06-08) — VERIFIED via S2 (4 citations)
- Citers: ERPBench (2609.17885); "Managerial altitude: Where should humans stand when AI agents manage AI agents?" (Business Horizons 2026, DOI:10.1016/j.bushor.2026.09.001 — human-oversight placement, practitioner journal); "Do User-Authored Permission Policies Improve Protection…" (2608.27443); "What Can Be Enforced? Certified Runtime Safety" (2607.22868). None touches fault propagation × structure × budget. References (16): zero classical lineage.

### 2.14 Hallucination Cascade (arXiv:2606.07937, 2026-06-06) — VERIFIED via S2 (7 citations)
- Citers: "Decomposition Buys Integrity, Not Yield" (2609.17464 — known via C1; depth-k trees lose yield C^k N^(1−δ), flat optimal for yield, 600 production traces — structure×information-integrity, not faults); Delayed Verification (2606.27409); Evidence-State Reliability (2608.21559, NEW); hiring-fabrication (2608.26171, NEW); "First-Order Recoverability Collapse in Self-Referential Information Decoders" (2606.24861, NEW, title-only relevance); ATLAS (2608.30685); World Model Science (2609.17419). References (25): zero classical lineage.

### 2.15 Kota, Gibbins & Jennings, ACM TAAS 2012 (DOI:10.1145/2168260.2168261) — VERIFIED via S2 + COCI
- S2: 105 citations; post-2024 citers: 1 — "Pick Two: An Adversarial Animal Survival Game" (2606.27557 — Unity ABM, irrelevant; already verified in W2). COCI: 44 edges, zero post-2024. Confirms W2: no LLM-era engagement with decentralized reorganization.

## 3. Same-author follow-ups and workshop→expanded versions (summary)

| Anchor | Follow-up | Status |
|---|---|---|
| Who&When (2505.00212) | Who&When Pro (2607.09996, Jul 2026) | Known to wave 1; stays in attribution lane |
| Atomix (2602.14849) | The Irreversibility Budget (2609.00275); Ghost Tool Calls (2606.02483); Don't Trust the Code (2609.00430) | **NEW**; risk-budget/privacy/effects lanes, not containment economics |
| MAST (2503.13657) | Fantastic Adaptive Taxonomies (2607.16387); Measuring Agents in Production (2512.04123) | **Former NEW**; taxonomy/production-measurement lanes |
| Huang (2408.00989) | None on faults | — |
| MAS-FIRE, Spark-to-Fire, AgentChaos, CtC, Loop-Back, IMACS, Oversight, HallucCascade | None detected in graph | CtC group check incomplete (§7) |
| Dellarocas & Klein 2000 | Baldoni et al. KER 2025 → Springer LNCS chapter 2026 | **Latter NEW (COCI only)**; classical lineage alive |

## 4. Closest approaches to the triple intersection {faults} × {structure} × {resources}

**4.1 faults × structure (no resources):** ResMAS (§5.2); When Do Institutions Beat Intelligence? (known); Decomposition Buys Integrity (known); Trust Propagation & Structural Containment (known, C2); Huang et al. itself.
**4.2 faults × resources (no org structure):** Sherlock (§5.1); Delayed Verification Destabilizes (Itkin 2606.27409 — verification *backfires* when delayed/overdosed: dose-delay oscillation thresholds + limited-corrector-budget placement via supermodular greedy; the nearest "containment can hurt" result, but the mechanism is consensus instability, not budget scarcity; known to B15/B3); Agent Mesh (2608.26225 — production evidence of circuit-breaker/retry primitives backfiring: false trip "driving one run from six of six components to three"; known via C2); REVISE; DART.
**4.3 structure × resources (no faults):** The Irreversibility Budget (§2.12); Complete Cyclic Subtask Graphs (2604.22820, TMLR 2026 — flexibility/cost/bottlenecks of workflow graphs; NEW, low threat).
**Triple:** empty.

**H3 status (containment backfires under resource scarcity — sign reversal): NO occupant found in the citation graph.** The nearest results are backfire-via-delay (Itkin), backfire-via-wrong-assumptions (Agent Mesh), and cost-aware placement without backfire (Sherlock). None studies scarcity as the independent variable with a sign reversal. H3 survives the citation-network attack.

## 5. Papers keyword search plausibly missed (found only via citation graph)

**5.1 Sherlock: Reliable and Efficient Agentic Workflow Execution (arXiv:2511.00330, 2025-11-01; Ro, Qiu, Goiri, Fonseca, Bianchini, Akella — Microsoft; 11 citations) — ABSTRACT + arXiv page VERIFIED; full text not read.**
Found as MAST citer; absent from all 48 prior reports. Counterfactual analysis identifies error-prone workflow nodes; attaches **cost-optimal verifiers selectively**; speculative downstream execution with rollback to last verified output on failure; +18.3% accuracy, −48.7% latency vs non-speculative, −26% verification cost vs Monte-Carlo placement. **Collision assessment: occupies H2's cost premise** — "verifying every step introduces significant latency and cost overheads" is its motivation, and verifier-cost optimization under a budget is its contribution. Any H2 claim that verification-cost trade-offs are unstudied is DEAD. Does NOT occupy: organizational structure as IV, typed boundaries, scarcity sign reversal (it optimizes within a budget; it never shows containment hurting under scarcity). Classification: **H2 WOUND (cost side), H1/H3 untouched.** Must-cite.

**5.2 ResMAS: Resilience Optimization in LLM-based Multi-agent Systems (arXiv:2601.04694, 2026-01-08; Zhou et al., Tsinghua; 5 citations) — ABSTRACT + arXiv page VERIFIED.**
Found as Huang citer; absent from all prior reports. Studies MAS resilience under agent-failure perturbations; finds **communication topology and prompt design significantly influence resilience**; RL-trained topology generator designs resilient topology per task + topology-aware prompt optimization. **Collision assessment: the closest occupant of H1's structure×faults cell found anywhere in this audit** — but it is *design-time topology optimization* (structure as output), not structure-as-IV measurement of propagation/recovery cost; no delegation depth, no recovery mechanisms, no cost vector, no scarcity. Classification: **H1 WOUND (must cite and differentiate design-time vs measurement), core claim intact.**

**5.3 Other citation-graph-only finds (all abstracts VERIFIED via S2/arXiv):** DART (2605.23311 — semantic recoverability; certifies whether local rollback stays valid after downstream commitment; 9 cites); The Irreversibility Budget (2609.00275); REVISE (2609.00643); Checkpoint/Fork/Restore/Merge exact checking (2608.22928); Evidence-State Reliability (2608.21559); hiring-pipeline HITL checkpoint comparison (2608.26171); Baldoni et al. Springer 2026 chapter (COCI-only Dellarocas citer); Fantastic Adaptive Taxonomies (2607.16387); FAccT developer-oversight study (2606.05391); DSN-W connected-vehicle recovery planning; SentinelAgent (2505.24201 — name collision to disambiguate).

## 6. Collision classification for claims in my lane

| Claim | Classification | Basis |
|---|---|---|
| "First experimental transfer test of classical MAS fault-handling results on tool-executing LLM agent organizations" | **SURVIVES (strengthened)** | Two-direction citation disconnection (§1.2); classical canon uncited by ~1,060 LLM-era citers; LLM-era anchors cite zero classical fault-handling work |
| H1: depth/structure changes fault propagation & recovery cost | **SURVIVES, wounded** | ResMAS + Institutions Beat Intelligence + Decomposition Buys Integrity occupy adjacent cells; none measures propagation/recovery-cost with org structure as IV |
| H2: containment reduces propagation but imposes cost | **WOUNDED on the cost premise** | Sherlock occupies verification-cost optimization; Itkin occupies verification-dose/delay trade-offs; reframe H2 as *priced comparison across 6 mechanisms incl. human*, not "cost observation" |
| H3: containment backfires under scarcity (sign reversal) | **SURVIVES intact** | No occupant; nearest backfire results (Itkin, Agent Mesh) have different mechanisms |
| "Sentinel" terminology | **WOUNDED (minor)** | SentinelAgent (2025) re-occupies the word for LLM-MAS anomaly detection; CtC uses SENTINEL for its mediator; disambiguate from Dellarocas-Klein sentinel services |

## 7. Verification log and limitations

- S2 Graph API: metadata for 14/15 anchors; complete forward-citation lists for Dellarocas&Klein (57), Kota (105), Huang (115), MAS-FIRE (11), Who&When (159), MAST (610), Spark-to-Fire (12), AgentChaos (0), CtC (0), Loop-Back (0), IMACS (2), Atomix (24), Oversight (4), HallucCascade (7); backward references for 10 LLM-era anchors. All raw JSON in `audit2/raw_s2/`.
- COCI: independent confirmation for the two DOI anchors + CtC; found one S2-unindexed citer (Baldoni 2026 chapter).
- arXiv abs pages: all 11 arXiv anchors + Sherlock, DART, ResMAS, SentinelAgent verified (titles, dates, version histories). ar5iv full-text reference scans: 7 anchors.
- **Limitations:** (1) DamageFlow S2 status UNVERIFIED — the S2 `/paper/search` endpoint returned 429 on every attempt all session (20+ retries across ~2h) and OpenReview is bot-blocked from this host; its citer list is unchecked, though workshop-poster age makes citers unlikely. (2) CtC author-group (Divi/Gullapalli/Brahmandam) same-author search likewise blocked (search endpoint down); partially compensated by direct DOI lookup of OpsAgent (see §2.8 correction). (3) S2 citation edges lag very recent (Sep 2026) papers; 0-citation results for Aug–Sep 2026 anchors are lower bounds. (4) Abstract-level verification for most citers; full texts read only where flagged (CtC via prior report; none others needed full text for the classifications above — Sherlock/ResMAS/Itkin classifications rest on detailed abstracts and could shift one notch on full-text reading).
