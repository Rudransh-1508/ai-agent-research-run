# W2 ASSASSIN — CAND-5 "FaultValidity": Do injected faults predict organic failure?

**Date:** 2026-09-21
**Mission:** Kill CAND-5: a measurement-validity study comparing naturally-occurring LLM-MAS failures (MAST traces, AgentFail logs) against injected fault taxonomies (MAS-FIRE's 15), testing whether containment-mechanism rankings transfer between injected and organic fault regimes.
**Wave-1 basis:** B5_fault_injection.md, D2_fault_injection_papers.md, E4_assassin_distsys.md, B4_cascading_failures.md, B3_failure_attribution.md read in full before searching. Wave 1 mapped injection and observational-failure literatures separately but never ran the injected-vs-organic validity search; that cross-comparison is this report's contribution.

---

## 1. VERDICT: SURVIVES (with two real wounds)

No work — in LLM-MAS, in chaos engineering, or in LLM evaluation — empirically compares organic failure distributions against injected fault taxonomies for agent systems, and no work tests whether containment/recovery-mechanism rankings transfer between injected and organic fault regimes. The core of CAND-5 is unoccupied. Two wounds: (W1) the *question* "what gaps exist between simulated faults and real-world failures" is already a named RQ of a TOSEM-accepted survey (arXiv:2407.00125), so framing novelty is limited to the LLM-MAS empirical execution; (W2) AgentChaos (ASE 2026) makes a qualitative realism-by-construction claim for its API-layer taxonomy that reviewers may mistake for having addressed the issue. Both are differentiation obligations, not kills.

---

## 2. Kill searches executed (all negative for occupation)

| Search target | Channels | Result |
|---|---|---|
| Endogenous vs injected LLM-MAS failure comparison | arXiv API + arXiv search UI (12+ query variants: "injected faults"×"naturally occurring", "fault injection"×"organic failures", "fault injection"×"distribution shift"×agents, "simulated faults"×"real faults", "ecological validity"×"fault injection", …) | Zero relevant hits. Only MAS-FIRE itself matches "representative"+"fault injection"+agents |
| Distribution-shift analysis MAST (2503.13657) vs MAS-FIRE (2602.19843) taxonomies | Semantic Scholar citation neighborhoods: MAS-FIRE 11 citers (enumerated), MAST 300 citers scanned by title, AgentFail 7 citers (enumerated) | No citer performs any validation of injection taxonomies against organic failure data |
| "Do fault-injection benchmarks predict real failure behavior" | arXiv UI, S2, OpenReview full-text search (api2 notes/search, 4 query variants) | Nothing for agents or LLM systems |
| Chaos-engineering analogue: does injected-fault response predict real-incident response? | S2 search, arXiv API, DDG (bot-blocked) | No empirical validity study found. CE literature *asserts* the link via principles (Basiri 2016, DOI 10.1109/MS.2016.60); empirical CE work is adoption/tooling studies (Owotogbe, "Chaos Engineering in the Wild", arXiv:2505.13654 — 971 GitHub repos, fault-type usage stats; multi-vocal review arXiv:2412.01416). The validity question is open even in mature CE |
| LLM-evaluation analogue: synthetic vs natural errors | arXiv UI ("induced hallucination"×"natural", "synthetic faults"×"natural failures", "synthetic"×"naturally occurring"×errors×LLM) | No benchmark-validity transfer study; hallucination work uses induced/natural distinctions descriptively, never as a ranking-transfer test |
| AgentFail / MAST-Data used to validate injection taxonomies | AgentFail verified (arXiv:2509.23735v2, 307 real Dify/Coze failure cases — abstract has no injection content); MAST full text grepped — **zero occurrences of "inject"** | Neither organic dataset has been used to validate any injection taxonomy |

---

## 3. Most damaging papers found (differentiation obligations, with identifiers)

1. **Tan, Huang, Zhang, Chen, Natella, Zheng, Lyu — "A Survey on Failure Analysis and Fault Injection in AI Systems," TOSEM-accepted (arXiv:2407.00125v2, Jan 2026).** RQ3 is literally "what gaps exist between the simulated faults and real-world failures"; does qualitative FA↔FI capability mapping across six AI-system layers (service/model/framework/toolkit/platform/infrastructure). **Most damaging to CAND-5's framing novelty.** Limitations that keep CAND-5 alive: (a) survey-level capability mapping, not empirical distribution measurement; (b) six layers exclude the agentic/MAS layer — no LLM-MAS fault injection covered (v2 predates MAS-FIRE); (c) no mechanism-ranking transfer test. Note shared authorship with AgentChaos (Tan, Chen) and with the classical representativeness line (Natella) — this group owns the FA↔FI-gap framing and may well be executing the agentic version now (collision risk, see §5).
2. **AgentChaos (arXiv:2608.06790, ASE 2026).** §3: "Faults in our taxonomy are not hypothetical" — taxonomy qualitatively grounded in production bug empirics (Zhu et al. 2602.21806 "An empirical study of bugs in modern LLM agent frameworks"; Shao et al. 2025/2026; Zhang et al. 2026; Microsoft vendor docs); 8 compound scenarios each "reproduce a real deployment failure." This is realism-by-*construction* at the API-transport layer. It never measures a distribution shift, never runs an organic-fault arm, and covers none of MAS-FIRE's semantic/coordination faults (hallucination, role ambiguity, blind trust, message storms) — precisely the fault classes CAND-5 targets. CAND-5 must argue: qualitative grounding ≠ measured representativeness; and the semantic/coordination faults that matter for organizational containment are exactly the ungrounded ones.
3. **MAS-FIRE (arXiv:2602.19843).** Full-text re-read: taxonomy "derive[d]… based on systematic literature review" of prior benchmarks/failure studies; §3 claims injection "simulate[s] realistic and representative anomalies" — an assertion with zero validation against organic failure distributions (its Grounded-Theory methodology applies to the fault-*tolerant behavior* taxonomy, not the fault taxonomy). CAND-5's primary target is intact: the field's standard injection taxonomy has never been validated against observed failures.
4. **From Spark to Fire (arXiv:2603.04474v2).** Closest user of the endogenous/exogenous distinction: governance layer "suppresses both endogenous and exogenous error amplification." Uses the distinction rhetorically; never measures whether endogenous and exogenous errors differ in distribution or respond differently to containment.
5. **TRAIL (arXiv:2505.08638v3).** Already claims "ecological validity" for agentic trace curation (148 annotated traces) — terminology CAND-5 should adopt with citation; but TRAIL is a trace-debugging benchmark, not an injection-validity study.
6. **AgentChaosBench (arXiv:2608.14680).** 250 injected-fault traces + 25 no-fault controls over A2A/MCP — purely injected, no organic arm; confirms even the newest diagnosis benchmarks don't validate against organic failures.

## 4. Classical precedent (importable methodology, not occupation)

- **Natella, Cotroneo, Duraes, Madeira, "On Fault Representativeness of Software Fault Injection," IEEE TSE 39(1), 2013 — DOI 10.1109/TSE.2011.124** (Crossref-verified). The representativeness question for injected software faults, answered via field-data comparison.
- **Duraes & Madeira, "Emulation of Software Faults: A Field Data Study and a Practical Approach," IEEE TSE 32(11), 2006 — DOI 10.1109/TSE.2006.113** (Crossref-verified). Field-data-driven fault model construction (G-SWFIT lineage).
- These prove the question is respected and publishable when executed with real field data — a 20-year-old methodological template CAND-5 can import for LLM MAS, where it has never been instantiated.

## 5. Wounds and risks (honest assessment)

- **W1 (framing):** the simulated-vs-real gap question is already a named survey RQ (2407.00125). CAND-5 cannot claim "first to ask"; it can claim "first to *measure* for LLM MAS + first mechanism-ranking transfer test."
- **W2 (reviewer reflex):** AgentChaos's realism-by-construction and MAS-FIRE's "representative" claim give reviewers an easy "already addressed" misreading; the paper must burn a section on why qualitative grounding is not validation.
- **W3 (internal validity):** organic corpora (MAST-Data: 7 frameworks, coding/math/general tasks; AgentFail: Dify/Coze low-code workflows) come from *different systems and tasks* than any injection testbed — distribution-shift measurement across substrates is confounded by task and harness, not just fault origin. CAND-5 needs a design that holds substrate fixed (e.g., replay organic failure modes into the same org testbed used for injection).
- **W4 (dependency):** the "containment-ranking transfer" half is parasitic on a containment-mechanism testbed (CAND-1 machinery). Standalone, CAND-5 collapses to a taxonomy-alignment measurement — publishable but thinner.
- **W5 (venue fit):** a measurement-validity meta-study is methodology, not organizational science; MASO's classical-MAS/norms-heavy pool may find it less native than CAND-1/CAND-2. Counter: the CFP's "detection and mitigation of cascading and systemic failures" line makes "our mitigation evidence may be measuring the wrong faults" a legitimate and provocative workshop contribution.
- **W6 (collision risk):** the Sun Yat-sen/SMU dependability group (Zheng/Chen/Lo/Natella network) owns both injection pillars (MAS-FIRE, AgentChaos) and the FA↔FI-gap survey — they are the most likely team to execute exactly this study before Oct 2026. Timing risk is real.

## 6. What survives (precise statement)

CAND-5 survives as: **the first empirical distribution-shift measurement between organic LLM-MAS failure corpora (MAST-Data's 1,642 traces, AgentFail's 307 platform-workflow cases, Who&When's hand-crafted real-failure set) and the injected fault taxonomies now in production use (MAS-FIRE's 15 types, AgentChaos's 65 configs, AgentChaosBench's 10 types), plus the first test of whether containment/recovery-mechanism rankings transfer across the two regimes.** No paper does any part of this; the strongest neighbors only assert realism (MAS-FIRE), ground qualitatively at the wrong layer (AgentChaos), or map the gap qualitatively for pre-agentic AI systems (TOSEM survey). Classical software-FI representativeness work (Natella TSE 2013; Duraes & Madeira TSE 2006) supplies the method template and legitimacy. Recommended hardening: (a) frame as "field-data-driven fault models for LLM MAS" à la Duraes & Madeira, not as a critique paper; (b) hold substrate fixed when comparing regimes; (c) couple with CAND-1's testbed so the transfer test has mechanisms to rank; (d) cite TRAIL for ecological-validity vocabulary and the TOSEM survey for the gap framing.

## 7. Verification log

- arXiv abstract pages fetched and read: 2509.23735 (AgentFail), 2407.00125 (TOSEM FA/FI survey), 2606.02430 (LLMFI soft errors — discarded, hardware-level), 2505.13654 (Chaos Engineering in the Wild), 2505.08638 (TRAIL), 2509.25370 (AgentErrorBench — organic single-agent failures, debugging, no injection link), 2608.14680 (AgentChaosBench), 2603.04474 (From Spark to Fire).
- Full texts read/grepped: MAS-FIRE html v1 (taxonomy derivation §3.1 — literature synthesis, no organic validation); AgentChaos html v1 (§3 realism grounding, §4.2 compound scenarios from production studies); MAST html v3 (zero "inject" occurrences); TOSEM survey html v2 (RQ3 scope: six layers, qualitative gap tables).
- Citation neighborhoods via S2 API: MAS-FIRE (11 citers), MAST (300 scanned), AgentFail (7 citers).
- Crossref-verified DOIs: 10.1109/TSE.2011.124 (Natella 2013), 10.1109/TSE.2006.113 (Duraes & Madeira 2006).
- OpenReview api2 notes/search: 4 validity-flavored queries, no relevant 2026 hits.
- Blocked channels: arXiv export API intermittent 429 (worked around via arxiv.org/search UI), S2 intermittent 429, DDG/Bing bot-challenged, DBLP Anubis (per wave-1).
