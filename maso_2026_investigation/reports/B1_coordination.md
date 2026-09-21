# LANDSCAPE B1 — LLM Multi-Agent Coordination (2023 – Sep 2026)

**Investigator:** B1 specialist (adversarial evidence-gathering for MASO 2026 seed-hypothesis selection)
**Date:** 21 September 2026
**Assignment:** Map 2023–Sep 2026 work on coordination of LLM-based multi-agent systems (coordination protocols, planning, role assignment, debate/discussion, theory-of-mind). What is solved, active-but-open, underexplored? Explicitly: does any coordination work model FAILURE propagation or containment?

**Verification method:** Every paper below was verified by fetching the actual arXiv abstract page (arxiv.org/abs/…) or, where noted, the arXiv listing page. Two candidate IDs from prior notes turned out to be WRONG on inspection (2410.06106 = tomography paper, not AgentPrune; 2502.11139 = exoplanet paper, not G-Safeguard; 2402.02455 = DID survey, not a ToM paper) — a reminder that unverified IDs are dangerous. Semantic Scholar API and OpenReview were rate-limited/bot-blocked during this run; arXiv abstract pages were the primary verification channel.

---

## 1. Bottom line

**Coordination of LLM MAS is a crowded, maturing landscape; failure propagation/containment specifically has gone from "one 2024 paper" to an active 2026 subfield with its own workshop (FAGEN — Failure Modes in Agentic AI, at ICML 2026). The seed hypothesis is NOT killed, but the naive framing ("does anyone study failure spread in LLM MAS?") IS dead. What remains open — and defensible for MASO — is the *organizational* cut: propagation across authority/delegation, memory, accountability, and human-agent boundaries; containment *and recovery* mechanisms that preserve task utility; and non-adversarial local faults in organizational workflows. Existing propagation work is (a) adversarial-security framed, (b) single-fault-type in linear pipelines, or (c) post-hoc attribution. The term "blast radius" is already in use in the agentic-security literature (arXiv:2507.21146, tied to OWASP AIVSS) and must be cited and differentiated.**

---

## 2. Landscape map: solved / active-but-open / underexplored

### 2.1 Largely solved (or saturated as "architecture demonstration")

| Capability | Status | Evidence |
|---|---|---|
| Role-playing / role assignment via prompts | Solved as demo; gains over strong baselines unclear | CAMEL (2303.17760), ChatDev (2307.07924), MetaGPT (2308.00352), AgentVerse (2308.10848) |
| Programmable conversation graphs / orchestration frameworks | Solved as engineering | AutoGen (2308.08155), AgentScope (2402.14034), Internet of Agents (2407.07061) |
| SOP/workflow-encoded coordination | Solved as demo (software eng.) | MetaGPT (2308.00352) |
| Debate improves factuality/reasoning (vs. single call) | Established, but compute-matched value contested | Du et al. (2305.14325), Liang et al. MAD (2305.19118), Corex (2310.00280) vs. Huang et al. self-correction limits (2310.01798) |
| Sampling/voting scaling ("more agents") | Established; it is population sampling, not coordination | More Agents Is All You Need (2402.05120, TMLR) |
| Topology optimization / communication pruning | Active, several strong methods | GPTSwarm (2402.16823, ICML 2024), MacNet (2406.07155, ICLR 2025), AgentPrune (2410.02506) |

### 2.2 Active-but-open

| Capability | Status | Evidence |
|---|---|---|
| Coordination *measurement* (not just task score) | Active 2025–2026 | MultiAgentBench (2503.01935), When Agents Coordinate (2608.16801: 1,902 coding runs as temporal networks; naming a coordinator creates no hub and no reliable success gain), Info-Sharing/orchestrator ablations (2508.12981) |
| Heterogeneous-model collaboration | Active; "collaboration gap" documented | The Collaboration Gap (2511.02687, COLM 2026): strong solo models degrade in pairs; relay inference mitigates |
| Theory-of-mind / partner modelling for coordination | Active, fragmented | Street et al. higher-order ToM (2405.18870); BayesBeliefAgent (2608.18490): Bayesian partner tracking + contradiction-triggered replanning in Overcooked; ToMAS (2609.16986): converts MAST FC2 misalignment traces into ToM items (pilot, no training effect shown) |
| Protocol-level coordination (A2A/MCP) | Active, engineering-led | MCP-vs-A2A comparative study (2607.23884): A2A = richer native task/lifecycle; MCP = lighter but app-layer coordination burden |
| Organizational structure as experimental variable | Emerging 2026 | Loop-Back Authority (2609.14767): paired flat-vs-hierarchical experiment; hierarchy *hurts* utility when the supervisor can only opine, not verify; revision loops degrade clarity; +51.5% tokens for no gain. Leadership as Coordination Control (2606.19111): recovery-advantage boundary — controllers help only where round-0 majority is unreliable and task is recoverable |
| Failure attribution / localization | Active and crowded 2025–2026 | MAST (2503.13657), Who&When (2505.00212), AgentLocate (2607.07989, COLM 2026), DUOTRACE (2608.29646), ASCon (2605.29874, listed not fetched), Who&When Pro (2607.09996, listed not fetched) |

### 2.3 Underexplored (gaps relevant to the seed hypothesis)

1. **Propagation across *organizational* boundaries** (authority/delegation, accountability, human-agent decision rights) — existing propagation work covers communication/message boundaries and tool/injection boundaries, not organizational ones.
2. **Recovery, not just detection/attribution/prevention** — only MRFR/GCJR (2608.29228, counterfactual replay for minimal repair families) and Leadership-as-Control (2606.19111, recovery-advantage boundary) touch recovery; neither studies containment+recovery under a task-utility budget in organizational workflows.
3. **Correlated/non-adversarial faults** — most injection studies use one faulty/malicious agent or injected misinformation; shared-base-model correlated faults and mundane organizational faults (stale memory, revoked authority, ambiguous policy) are unstudied.
4. **Blast-radius *metrics* with utility trade-off** — no work quantifies "organizational blast radius" as a measurable quantity trading systemic impact against task utility.

---

## 3. Evidence table A — coordination architectures, role assignment, planning

| Paper | ID / Venue | Problem & method | Setting / metrics | Findings | Limitations (stated + inferred) | Relation to seed |
|---|---|---|---|---|---|---|
| CAMEL: Communicative Agents for "Mind" Exploration | arXiv:2303.17760 (2023) | Role-playing inception-prompting for autonomous cooperation | AI society sim, code, math | Role-play enables autonomous task dialogue | Single-model pairings; no fault model | Baseline role-assignment paradigm |
| MetaGPT | arXiv:2308.00352 (ICLR 2024) | SOPs encoded into role-specialized assembly line | Software eng. benchmarks | SOPs reduce "cascading hallucinations" vs naive chaining | Notes cascading hallucination as motivation but does not *model* propagation | Motivates seed: SOPs as implicit containment |
| AutoGen | arXiv:2308.08155 (2023) | Programmable multi-agent conversation framework | Math, coding, QA, decision-making | Flexible conversation patterns | Framework paper; no failure analysis | Infrastructure layer |
| ChatDev | arXiv:2307.07924 (ACL 2024) | Chat-chain guided software company | Software dev phases | Language as unifying bridge; communicative dehallucination | Fixed roles/chain | Role + communication boundary baseline |
| AgentVerse | arXiv:2308.10848 (2023) | Dynamic group composition; emergent social behaviors | Multi-task | Dynamic adjustment helps; emergent behaviors discussed | "Under review" note; qualitative emergence | Group dynamics baseline |
| DyLAN | arXiv:2310.02170 (COLM 2024) | Agent Importance Score team selection + dynamic comms | Code, reasoning, MMLU | +25% on MMLU subjects via team optimization | Selection assumes a preliminary trial; no faults | Dynamic role assignment |
| AgentScope | arXiv:2402.14034 (2024) | Developer platform, message-exchange core, fault tolerance hooks | Platform | Built-in/customizable fault-tolerance mechanisms | Fault tolerance = engineering hooks, not studied scientifically | Infrastructure; fault hooks unexploited |
| Internet of Agents | arXiv:2407.07061 (2024) | Internet-like heterogeneous agent integration protocol | Assistant, embodied, RAG tasks | Beats baselines; dynamic teaming | Work-in-progress note | Heterogeneous teaming protocol |

## 4. Evidence table B — debate, discussion, scaling, communication topology

| Paper | ID / Venue | Problem & method | Setting / metrics | Findings | Limitations | Relation to seed |
|---|---|---|---|---|---|---|
| Du et al., Multiagent Debate | arXiv:2305.14325 (ICML 2024) | Multi-round debate to consensus | Math, strategy, factuality | Debate improves factuality/reasoning | No compute-matched baseline | Debate as implicit error-correction |
| Liang et al., MAD | arXiv:2305.19118 (EMNLP 2024) | Tit-for-tat debate vs Degeneration-of-Thought | Commonsense MT, arithmetic | Divergent thinking helps; judge bias if agents differ | Judge fairness | Debate failure mode (DoT) |
| Corex | arXiv:2310.00280 (COLM 2024) | Debate/Review/Retrieve multi-model collaboration | 4 reasoning task types | Task-agnostic gains, cost-effective | No fault injection | Collaboration-mode suite |
| Huang et al., LLMs Cannot Self-Correct Yet | arXiv:2310.01798 (ICLR 2024) | Intrinsic self-correction limits | Reasoning benchmarks | Self-correction w/o external feedback degrades | Intrinsic only | Key null result: interaction needs external info |
| More Agents Is All You Need | arXiv:2402.05120 (TMLR) | Sampling-and-voting scaling | Wide benchmarks | Performance scales with agent count | Population sampling ≠ coordination | Threat to naive "more agents = robustness" claims |
| GPTSwarm (Language Agents as Optimizable Graphs) | arXiv:2402.16823 (ICML 2024) | Agents as computational graphs; edge/node optimization | Various | Automatic orchestration improvement | Optimization cost | Topology as design variable |
| MacNet (Scaling LLM-based Multi-Agent Collaboration) | arXiv:2406.07155 (ICLR 2025) | DAG collaboration networks, 1000+ agents | Reasoning tasks | Logistic collaborative scaling law; irregular > regular topologies | Scale ≠ robustness | Topology affects propagation surface (unstudied) |
| AgentPrune (Cut the Crap) | arXiv:2410.02506 (ICLR 2025) | One-shot spatial-temporal communication-graph pruning | 6 benchmarks + 2 adversarial attacks | $5.6 vs $43.7 cost; 28–73% token cut; +3.5–10.8% under attack | Pruning is static per-task | Partial containment via topology sparsification |
| Exploring Collaboration Mechanisms (social psych view) | arXiv:2310.02124 (ACL 2024) | Traits × thinking patterns in agent societies | 3 benchmarks | Conformity/consensus emerge; some strategies cheaper+better | Small societies | Conformity = propagation channel for errors |

## 5. Evidence table C — coordination measurement, protocols, ToM, organizational structure (2025–2026)

| Paper | ID / Venue | Problem & method | Setting / metrics | Findings | Limitations | Relation to seed |
|---|---|---|---|---|---|---|
| MultiAgentBench | arXiv:2503.01935 (2025) | Benchmark collaboration+competition; milestone KPIs; star/chain/tree/graph | Diverse interactive scenarios | Graph topology best in research scenario; cognitive planning +3% milestones | Topology assigned, not learned | Topology–performance link |
| Analyzing Information Sharing and Coordination in Multi-Agent Planning | arXiv:2508.12981 (2025) | Notebook + orchestrator ablations | TravelPlanner | Notebook −18% hallucinated-detail errors; orchestrator −13.5% in focused subareas; combined 25% pass vs 7.5% single | Single domain; still low absolute pass | Shared memory as error-reduction (containment-adjacent) |
| When Agents Coordinate | arXiv:2608.16801 (2026) | Temporal agent-file/message networks as coordination instrument | 1,902 coding runs + 244 sealed reruns | Messaging ~quadratic then broadcast; shared files cut output tokens ~42% @8 agents; named coordinator = no hub, no reliable gain; agents seek hidden grading material | Coding domain | Empirical coordination measurement; null on naive hierarchy |
| The Collaboration Gap | arXiv:2511.02687 (COLM 2026) | Open-world heterogeneous pair collaboration benchmark | Maze-solving, 32 models, solo/homogeneous/heterogeneous | Strong solo models degrade in pairs; relay inference closes much of gap | 2-agent maze setting | Compatibility ≠ capability |
| MCP vs A2A comparative study | arXiv:2607.23884 (2026) | Implementation-grounded protocol comparison | Same SWE task in both protocols | A2A: native task/lifecycle, more complexity; MCP: lighter, app-layer coordination burden | Experience report, narrow pattern | Protocol layer where boundaries are defined |
| Loop-Back Authority | arXiv:2609.14767 (2026) | Paired experiment: vary only manager reject/revise link | 43 paired products, 86 runs, BI reporting, judge panel + spec check | Flat > hierarchical on Utility (d=0.42) and Clarity (d=0.34); hierarchy hedges 53% more; each revision loop −0.14 clarity; +51.5% tokens no gain; "supervisor pays when it can verify, liability when it can only opine" | One task family | **Directly organizational: authority link as failure/cost amplifier** |
| Leadership as Coordination Control | arXiv:2606.19111 (2026) | Leadership styles as controllers; behavioral signatures incl. recovery from wrong round-0 consensus | 4 task regimes × 3 model families | Contingency view confirmed: control helps only where round-0 majority unreliable + task recoverable; matched arbitrary rule ≈ voting | Null-heavy by design | **Recovery-advantage boundary — closest to "when does coordination contain error"** |
| BayesBeliefAgent | arXiv:2608.18490 (2026) | Bayesian partner-skill tracking + contradiction-triggered replanning | Overcooked | Belief-action gap narrowed; 10× fewer replans | 2-player embodied | ToM/partner model for coordination repair |
| ToMAS | arXiv:2609.16986 (2026) | Convert MAST FC2 misalignment traces into ToM items; GRPO pilot | 242 traces → 39 items; 28-item diagnostic | Pipeline works; no training effect (LoRA ΔW negligible); honest negative | Pilot; provenance gap | ToM grounded in *diagnosed coordination failures* |
| Street et al., higher-order ToM | arXiv:2405.18870 (2024) | Multi-order ToM Q&A vs human benchmark | 5 LLMs vs adults | GPT-4 at/above adult level up to 6th order | Static Q&A, not collaboration | ToM capability exists; coordination use lags |

## 6. Evidence table D — FAILURE propagation / containment / recovery (the assignment's explicit question)

**Yes — coordination-adjacent work now models failure propagation and containment, and 2026 shows a marked acceleration. Details:**

| Paper | ID / Venue | What it does | Fault model | Propagation modeled? | Containment/recovery? | Gaps vs seed hypothesis |
|---|---|---|---|---|---|---|
| On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents | arXiv:2408.00989 (2024; v4 May 2025) | AutoTransform/AutoInject fault injection; 3 structures × 4 tasks × 6 systems | Clumsy/malicious agents | Implicitly (performance drop per structure: hierarchical 5.5% vs 23.7%) | Challenger + Inspector recover up to 96.4% of injected errors | Single injected agent; no organizational boundaries; no utility-preservation trade-off |
| Why Do Multi-Agent LLM Systems Fail? (MAST) | arXiv:2503.13657 (2025, v3 Oct 2025) | 14-mode failure taxonomy; 1,600+ annotated traces; 7 frameworks; LLM judge | Naturalistic failures | Taxonomizes inter-agent misalignment (incl. FC2) but does not model spread dynamics | No — diagnosis only | Taxonomy, not propagation model |
| Who&When (Which Agent Causes Task Failures and When?) | arXiv:2505.00212 (2025, camera-ready) | Automated failure attribution; dataset of 127 MAS failure logs | Naturalistic failures | Post-hoc attribution to agent+step (best 53.5% agent / 14.2% step accuracy) | No | Attribution ≠ containment |
| Towards Unifying Quantitative Security Benchmarking (ACI) | arXiv:2507.21146 (Jul 2025) | **Defines Agent Cascading Injection "analogous to Agent Impact Chain and Blast Radius"**; adversarial goal equation; propagation chains, amplification factors; OWASP AIVSS alignment; A2A/MCP stress-test methodology | Malicious injection | **Yes — formally, but adversarial** | Proposes benchmarking, no evaluated defense | **Occupies "blast radius" terminology — must cite/differentiate.** Position paper, 9pp, no experiments |
| Misinformation Propagation in Benign Multi-Agent Systems | arXiv:2606.16710 (Jun 2026) | Intent-based misinformation injection; single vs multi-agent; debate/voting/consensus protocols | Injected misinformation (benign system) | Yes — persistence across debate rounds; retention of misinformed peers' answers | Debate reduces degradation; consensus more stable than voting under peer pressure | Reasoning/QA tasks; no organizational structure; "containment" = aggregation protocol only |
| Channel Fracture | arXiv:2606.04896 (Jun 2026) | 3 production cases of silent cross-boundary delivery failure; CADVP 13-dimension verification protocol | Infrastructure/delivery faults | Cross-boundary silent blocking (memory injection, skill routing, WebSocket ACK) | Verification protocol: 0% failure under protocol vs 69–98% without (30k trials) | Case-report style; delivery reliability, not semantic/task faults |
| The Hallucination Snowball | arXiv:2608.14588 (FAGEN Workshop @ ICML 2026) | **Markov state-transition model of error propagation** (Raw→Derived→Narrative→Invisible); 346 injected hallucinations; 4-agent FinanceBench pipeline | Injected hallucinations | **Yes — explicit per-boundary escape probabilities (24.6/48.3/89.3%); detection decays 72%→51%** | Boundary gates cut survival 58.4%→16.2% vs end-checking; optimal verification allocation | **Linear pipeline, one fault type, one domain; no authority/memory/accountability boundaries; no recovery** |
| PropUQ-MAS | arXiv:2608.22130 (EMNLP 2026) | Propagation-aware UQ on communication graph; local + inherited uncertainty | Natural errors | Yes — uncertainty inheritance upstream→downstream; +6.1% AUROC, +47.6% PRR | No — quantification only | UQ, not containment |
| CatchBench | arXiv:2608.22808 (2026) | When can a failure be caught: PRE/LIVE/POST audit states; 72 entrants, 1,162 runs | Recorded runs | Detection timing, not spread | Auditability benchmark | Detection-oriented |
| DUOTRACE (Detect Before You Attribute) | arXiv:2608.29646 (2026) | VAE anomaly detection filter before LLM attribution | Trajectory anomalies | Cascade attribution framing | No | Attribution pipeline |
| AgentLocate (Who Broke the System?) | arXiv:2607.07989 (COLM 2026) | Failure localization to agent + earliest decisive step; multi-perspective verification | Naturalistic failures | "Earliest point trajectory becomes irreversibly misdirected" | No | Localization, not containment |
| SafeFlow | arXiv:2607.25255 (Jul 2026) | Semantic taints propagated through collaboration graph; workflow-level validation before irreversible actions | Malicious objective fragmentation | **Yes — malicious cross-agent propagation as semantic info-flow** | **Yes — blocks propagation across delegation boundaries; retains benign completion** | Adversarial only; security framing |
| MRFR / GCJR (Localizing Emergent Failures) | arXiv:2608.29228 (2026) | Minimal Repair Family Recovery via graph-constrained counterfactual replay | Interaction failures | Jointly-necessary failure event sets | **Yes — recovery via replay; 1.000 Family Exact Match; −55% replay calls** | Small pilot (24 cases, 4 agents); repair identification, not runtime containment |
| AI Agents Do Not Fail Alone | arXiv:2607.14275 (2026) | Context-quality as leading indicator; 7 criteria; controlled study | Weak context | No | Prevention via context measurement | Preflight, not runtime |
| Trust Between AI Agents (listed, not fetched) | arXiv:2606.14923 (2026) | Trust formation/breakage/recovery measurement | — | — | Recovery framing | Unverified beyond title/abstract listing |
| Contagion Networks (listed, not fetched) | arXiv:2606.20493 (2026) | Evaluator preference propagation | — | Yes (title) | — | Unverified beyond listing |

**Also noted in listings (Jun–Sep 2026 cs.MA), not individually fetched:** "Distributed Agent System: Fault-Tolerant Collaboration Among Embodied Agents" (2607.10811), "Self-Healing Coordination in Cognitive Swarm Agents" (2607.11960), "The Honest Quorum Problem: Epistemic Byzantine Fault Tolerance for Agentic Infrastructure" (2607.16109), "Beyond Byzantine: An Organizational Consensus Algorithm" (2607.28957), "Resilient Consensus in Agentic AI" (2606.15024), "Silent Failure in LLM Agent Systems: The Entropy Principle" (2606.08162), "Fluid Structure, Rigid Record: Layered Organizational Design for Agent-Native Organizations" (2608.08516), "Organizational Memory for Agentic Business Process Execution" (2607.03228), "The Organizational Behavior of Agentic AI" (2606.30986). These signal a 2026 surge at the org × failure intersection; each would need verification before citation.

---

## 7. Explicit answer: does coordination work model failure propagation or containment?

**Yes, and increasingly so — but along three narrow axes, none of which is the seed hypothesis's organizational axis:**

1. **Adversarial cascade/blast-radius (security):** ACI (2507.21146) formalizes cascading injection with explicit "Blast Radius" language tied to OWASP; SafeFlow (2607.25255) contains malicious propagation via semantic taints; AgentPrune (2410.02506) prunes malicious messages. → The *terminology* is occupied; the *non-adversarial organizational* problem is not.
2. **Error/hallucination propagation in pipelines:** Hallucination Snowball (2608.14588) gives the first explicit stochastic propagation model (Markov over transformation states) with containment via verification-gate placement; PropUQ-MAS (2608.22130) models inherited uncertainty; Misinformation Propagation (2606.16710) studies persistence through debate. → Propagation *modeling* exists for message/content faults in linear or debate structures.
3. **Post-hoc attribution/localization:** MAST, Who&When, AgentLocate, DUOTRACE, CatchBench, MRFR/GCJR. → Diagnosis is crowded; runtime containment + recovery with utility preservation is not.

**Not found anywhere in the verified set:** a model of how a *local, non-adversarial* fault spreads across **organizational boundaries** (role, authority/delegation, memory, accountability, human-agent decision rights) with **containment AND recovery** mechanisms evaluated on **systemic impact vs task utility**. The closest neighbors each miss at least two of: {non-adversarial, organizational boundaries, recovery, utility trade-off}.

## 8. Threats to the seed hypothesis (adversarial assessment)

1. **Terminology collision:** "blast radius" + "cascading" already used by ACI/OWASP line (2507.21146). Reviewers may ask "how is this different from agentic-security cascading risk?" — answer must be: organizational fault semantics, non-adversarial faults, recovery, utility preservation.
2. **FAGEN workshop (Failure Modes in Agentic AI, ICML 2026)** exists — the failure-modes community is organizing fast; by Oct 2026 more propagation papers will exist. Window is open but narrowing.
3. **Hallucination Snowball + PropUQ-MAS** could be extended to organizational settings by their authors; a MASO paper must go beyond "errors propagate downstream" (now established) to *what determines the radius* and *what contains it*.
4. **Loop-Back Authority and Leadership-as-Control** already import organizational theory (contingency, substitutes) into LLM-teams experiments — the "organizational theory × LLM MAS" move is no longer novel per se; the failure-propagation instantiation of it still is.
5. **Prior repo kills remain avoided:** nothing here resurrects sanctioning/blame games, acceptance gates, experience commons, verifier panels, or regret-optimal teams; and the delegation-invariants territory (existing MASO proposal) is complementary, not overlapping — that proposal covers *authority preservation across delegation chains*; the seed covers *fault spread and containment across organizational boundaries*.

## 9. What is genuinely underexplored (defensible residual for the seed)

- A formal, measurable notion of **organizational blast radius** spanning ≥3 boundary types (e.g., communication × authority × memory), with fault injection that is **non-adversarial** (stale memory, ambiguous instruction, revoked permission, tool timeout).
- **Containment mechanisms beyond detection**: quarantine of memory/context, authority rollback, delegation revocation, human escalation — evaluated on **utility preserved per unit containment**.
- **Recovery**: re-planning, state repair, trust re-establishment after containment (only MRFR/GCJR and Leadership-as-Control touch recovery, neither in organizational workflows).
- Classical MAS/distributed-systems prior art to check next: Byzantine fault tolerance semantics, epidemic/gossip propagation models (SIR on networks), organizational reliability theory (Weick), cascade models in interdependent infrastructures — these predate LLMs and a reviewer from classical MAS will expect them cited.

---

## Appendix: verification log

- All arXiv IDs in tables verified by fetching arxiv.org/abs/<id> on 2026-09-21; titles, authors, dates, venue comments, and abstracts quoted from those pages.
- Wrong IDs caught and corrected during verification: AgentPrune is 2410.02506 (not 2410.06106, which is a tomography paper); G-Safeguard could not be verified (2502.11139 is an exoplanet paper) and is therefore excluded; "Mutual ToM" candidate 2402.02455 is a decentralized-identity survey — excluded.
- Discovery of 2026 work via arXiv cs.MA monthly listing pages (2026-06, 2026-07, 2026-08, 2026-09), keyword-filtered on fail/fault/propagat/cascad/resilien/recover/contain/blast/ToM/coordinat/organiz.
- Semantic Scholar API: rate-limited (429) throughout. OpenReview: bot-check wall. DBLP: Anubis bot wall. Google/DDG: bot walls. arXiv API (export.arxiv.org): began returning empty responses after initial queries — likely IP throttling; abstract pages remained accessible.
