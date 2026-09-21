# C1 — arXiv Last-7-Days Sweep (14–21 Sep 2026): LLM Multi-Agent Failure, Containment, Recovery, Blast Radius

**Investigator:** Novelty Hunter C1
**Date:** 21 Sep 2026
**Mission:** Sweep new/cross-listed arXiv submissions in cs.MA, cs.AI, cs.CL, cs.SE (14–21 Sep 2026) for anything on LLM multi-agent failure, reliability, containment, recovery, blast radius, fault injection, organizational agents. Adversarial evidence-gathering against the seed hypothesis ("organizational failure propagation and recovery in LLM multi-agent systems" / "organizational blast radius").

---

## 1. Method and coverage

| Channel | What was done | Coverage |
|---|---|---|
| arXiv listing pages (`arxiv.org/list/cs.MA/recent?show=100`) | Full parse of all 79 cs.MA entries announced Tue 15 – Mon 21 Sep 2026 (titles, subjects, cross-list origin) | 100% of cs.MA week |
| arXiv abstract pages (`arxiv.org/abs/...`) | Individual verification of ~25 flagged papers (abstract, authors, dates, comments, subjects) | all Tier-1/2 finds verified against the actual page |
| Semantic Scholar bulk search API (`api.semanticscholar.org/graph/v1/paper/search/bulk`) | 40+ keyword queries × publicationDate 2026-09-14:2026-09-21: {multi-agent, LLM, agentic} × {failure, fault, reliability, robustness, recovery, containment, cascade, propagation, accountability, blame, attribution, resilience, delegation, oversight, quarantine, isolation, circuit breaker, chaos engineering, stress testing, memory poisoning, error propagation, failure taxonomy, blast radius, organizational, rollback, checkpoint, monitoring, inter-agent communication} | ~60 unique papers screened |
| arXiv export API (`export.arxiv.org`) | Attempted; rate-limited (HTTP 429) for most of the session after initial retries; compensated with the three channels above | partial |

**Window convention.** arXiv's "recent" listing covers announcements Tue 15 Sep → Mon 21 Sep 2026, corresponding to submissions received ~11–18 Sep. Papers submitted 19–21 Sep are not yet announced and are therefore invisible to any sweep today; this is an inherent blind spot. Two papers appearing in this week's listings are v1s from July 2026 that were cross-listed this week (2609.20211, 2609.18998) — flagged below.

**Terminology note.** The exact phrase "blast radius" appears this week only in a hypersonics paper (2609.19141, OSIRIS-REx infrasound) — the term is NOT yet adopted in the LLM-MAS literature. However, the concept is actively published this week under the synonyms **"contagion", "propagation", "cascade/cascading failure", "collective loss of control", "attack propagation"**. In classical control-theory MAS literature, "containment" means a formation-control objective ("containment control of multi-agent systems", two control-theory papers this week) — a terminology collision to be careful about when claiming novelty of terms.

---

## 2. BOTTOM LINE (adversarial)

**The seed hypothesis is NOT killed, but its naive framing is substantially occupied — this exact week.** Four papers appeared in the last 7 days that each claim a piece of the seed's core territory:

1. **2609.18460** ("Collective Loss of Control in LLM Agent Systems: An Epidemic Account of Mutation, Contagion, and Recovery") asks nearly the seed's question verbatim — "How does a multi-agent system evolve from a local deviation into collective loss of control?" — with mutation/contagion/recovery vocabulary and a fault-injection benchmark.
2. **2609.17648** ("Trust propagation and structural containment in Multi-agent LLM pipelines", accepted IEEE CARS 2026) empirically decomposes compromise-at-attacked-agent vs propagation-to-final-action (a blast-radius decomposition) in a role-structured pipeline and shows structural authorization contains propagation when LLM judgment fails.
3. **2609.17320** ("Emergence World") injects controlled stress events into long-horizon multi-agent worlds and shows detection ≠ containment, with propagation through memory, tools, and other agents up to 46h later.
4. **2609.15293** ("Why LLM Agents Collapse Without Oversight: The Enforcement Gap", submitted ICLR 2027) proves detection quality is irrelevant when enforcement probability ≈ 0 and shows a ~20-line enforcement check cuts attack success 4×.

**What remains unoccupied (the defensible residue):**
- **(a) Organizational structure as the manipulated variable.** Nobody this week varies roles/hierarchy/delegation topology/authority gradients and measures failure spread. 2609.14767 varies the authority link but measures output *quality*, not failure propagation. 2609.17648 has a fixed 4-role pipeline. 2609.18460 does not vary org structure.
- **(b) Non-adversarial operational faults.** All four Tier-1 papers are security/unsafe-behavior framed (injection, poisoning, attacks). Accidental faults — hallucination, tool errors, stale memory, misrouting — in ordinary organizational workflows are unstudied as cascade seeds (2609.18460 explicitly lists "no natural rare-event rates, no autonomous cascade demonstrated" as limitations).
- **(c) Recovery-mechanism comparison with task-utility preservation as co-objective.** This week's recovery papers (2609.18304 rollback-boundary control; 2609.19654 replan/repair/edit) are single-agent or single-domain.
- **(d) A unified cross-boundary blast-radius instrument.** Each boundary got its own paper this week (tool: 2609.15397; memory: 2609.20211; authority: 2609.18820; human: 2609.21081; privacy/topology: 2609.19226) — no unified 7-boundary measurement study exists.

**Timing risk: HIGH.** The area is moving at multiple papers per week; differentiation from 2609.18460/2609.17648/2609.17320 must be explicit and central in any MASO submission.

---

## 3. Tier 1 — Direct novelty threats (verified against arXiv pages)

### 3.1 Collective Loss of Control in LLM Agent Systems: An Epidemic Account of Mutation, Contagion, and Recovery
- **arXiv:** 2609.18460 (cs.AI, cs.CR), v1 Wed 16 Sep 2026. Corresponding author: Xiangfan Wu.
- **Problem:** how a multi-agent system evolves from a *local deviation* into *collective loss of control*. Epidemic framing: accidental mutation creates a seed; communication lets other agents adopt/retransmit the unsafe strategy; collective failure emerges when propagation outpaces correction and containment.
- **Method/setting:** (i) deployment audit identifying implicit communication paths between nominally independent evaluation runs, verifying transport through a default Docker backend; (ii) RogueHandoff-20 benchmark — 20 executable scenarios injecting unsafe trajectories generated by a modified Qwen-27B route, testing recipient susceptibility across four native-pending routes.
- **Metrics/findings:** executed harm 0–5% on normal tasks vs 40–95% after injection; injection exceeds paired direct malicious requests by 5–45 pp. Supports low baseline harm alongside high conditional susceptibility.
- **Author-stated limitations:** does NOT establish natural rare-event rates; does NOT demonstrate an autonomous cascade.
- **Relation to seed:** **closest paper found this week.** Occupies the epidemic/contagion framing of local-fault → collective failure and the "audit/restrict communication paths + strengthen resistance and recovery" defense direction. Does not vary organizational structure, does not study non-adversarial workflow faults, does not compare recovery mechanisms on task utility.

### 3.2 Trust propagation and structural containment in Multi-agent LLM pipelines
- **arXiv:** 2609.17648 (cs.CR, cs.CY), v1 Tue 15 Sep 2026. **Accepted at IEEE Cyber Awareness & Research Symposium (CARS) 2026.** From: Sharif Noor Zisad.
- **Problem:** compromised low-privilege agent influencing higher-privilege agent to trigger unauthorized action — attack propagation across privilege boundaries.
- **Method/setting:** four-agent LangGraph pipeline (Supervisor, Researcher, Validator, Executor); shared-memory poisoning + indirect prompt injection via forged approval in a retrieved document; compares Validator judgment vs independent authorization layer (task-bound signed tokens, separately verified policy oracle); component-level ablation of the authorization boundary.
- **Metrics:** **Judgment Bypass Rate (JBR)** — compromise measured at the attacked agent rather than the final action; Unsafe Action Rate (UAR); false-positive rate for agent hijacking.
- **Findings:** memory poisoning reaches execution in every undefended trial; with authorization enabled, 100% JBR but 0% UAR — "the Validator can remain compromised while execution is contained"; policy oracle contains even an attacker holding the signing secret; Observer layer cuts hijacking false positives 49% → 7%.
- **Relation to seed:** occupies **propagation-across-authority-boundaries + structural containment** with a blast-radius-like metric decomposition (compromise at layer vs at execution). Gaps vs seed: adversarial-only faults, fixed topology, no recovery, no task-utility preservation, single pipeline.

### 3.3 Emergence World: Adversarial Stress-Testing of Long-Horizon Multi-Agent Systems
- **arXiv:** 2609.17320 (cs.MA), v1 Tue 15 Sep 2026. From: Aditya Vempaty. 36.8 MB submission.
- **Problem:** failures propagate through memory, tools, other agents, and environmental state long after interactions; model-level evaluation cannot characterize this regime.
- **Method/setting:** continuously running multi-agent environment; 8 parallel worlds × 10 agents (7 homogeneous frontier-model worlds + 1 mixed); 16 days, 850k+ LLM calls, ~50B tokens; agents pursue goals, use/create tools, maintain persistent memory, govern shared institutions. Three controlled stress events via ordinary interaction surfaces: indirect prompt injection, misinformation, exposure of private agent memories.
- **Findings:** no world achieved full resilience across all three events; **"detection did not ensure containment"** — systems recognized threats while still writing adversarial content into persistent memory and acting on it up to 46 hours later; recurring tool errors, goal drift, language opacity, conformity despite private disagreement, coordinated refusal of assigned work; same model-persona pairing behaves differently in mixed vs homogeneous populations; "model-level alignment is not compositional".
- **Relation to seed:** occupies **fault/stress injection + propagation across memory/tool/agent boundaries + containment failure** in persistent MAS. Gaps vs seed: adversarial security events (not organizational operational faults), no systematic org-structure variation, no recovery-mechanism comparison, no utility-preservation objective.

### 3.4 Why LLM Agents Collapse Without Oversight: The Enforcement Gap as the Mechanism Behind Emergence World Failure
- **arXiv:** 2609.15293 (cs.AI), v1 Mon 14 Sep, v2 Wed 16 Sep 2026. **Submitted to ICLR 2027.** From: Yuhang Wang. 27 pp.
- **Problem:** Reflexion-style agents detect dangerous plan steps via self-critique, but architectures provide no pathway from detection to action — the "enforcement gap".
- **Method/findings:** formal proof that when enforcement probability ≈ 0, detection quality is irrelevant to security; a single conditional check (<20 lines) reduces attack success >4× across frontier models, all five major agent frameworks, and an independent benchmark; two compounding failure modes (unreliable auditors, unparseable verdicts) "explain every collapse pattern in Emergence World"; GRPO-trained enforcement controller for the ambiguity case; proposes a 3-requirement Audit Enforcement Specification "absent from every deployed framework today".
- **Relation to seed:** occupies the **detection→containment mechanism gap**; a containment-mechanism paper, not a propagation-determinants paper. Complementary more than subsuming, but must be cited; its "enforcement is the binding constraint" claim competes with a "blast radius determinants" framing.

---

## 4. Tier 2 — Boundary-specific adjacent work (verified)

| arXiv | Title (date, venue) | Boundary | Core content | Relation to seed |
|---|---|---|---|---|
| 2609.15397 | When Tool Calls Succeed but Workflows Fail: Anomalies at the Agent-Tool Boundary (14 Sep; cs.AI/DB/DC/SE) | **Tool** | Effect-history model separating world events from runtime observations; catalog of 8 external-effect anomalies (missing/duplicated effects, aborted effects surviving, committed effects depending on withdrawn provisional state); 4 points where black-box tool invocation cannot give general guarantees; measurement of annotation vocabulary across **98,291 MCP-server tools** — no required capability fully expressible; motivates transactional contracts at tool boundary | Occupies tool-boundary failure semantics + compensation/recovery contracts. Pre-LLM lineage: advanced transaction models (sagas). Strong "prior art" cite for the tool axis |
| 2609.20211 | Silence Is Endorsement: Verification-Status Laundering in LLM Agent Pipelines (v1 25 Jul 2026; **cross-listed this week**, 18 Sep; cs.CR, cs.MA) | **Memory/communication** | Handoffs preserve "authorized" claim while losing "never verified" status; removing unverified-provenance framing raises risky approval 5%→60% (Llama-3.1-8B), 9%→98% (Qwen2.5-14B); full proposer–summarizer–memory–monitor pipeline raises risky approval to 57–81%; instructing monitors to reject unverified claims is not a reliable fix; fix = authorization provenance as structured state | Failure *propagation through summarization/memory compression* + containment via structured provenance. Directly adjacent to the memory axis |
| 2609.18820 | Compositional Policy Violations: When Step-Level Compliance Fails In Agentic AI Workflows (16–17 Sep; cs.AI, cs.MA) | **Authority/policy** | Every step passes its own check while composed execution violates governing policy; taxonomy: **Authority Creep, Threshold Laundering, Cumulative Sum Violation, Context Collapse**; provenance-aware runtime evaluating policies over complete traces | **Overlaps the OCCUPIED delegation-invariants territory** (maso/policy_preserving_delegation_research_proposal.md) — flag to that proposal's owner; also a scoop-risk for it |
| 2609.21081 | Loopjacking: Hijacking Human-in-the-Loop Approval (17 Sep; cs.CR, cs.MA) | **Human-agent** | Human approves operation A, implementation uses decision for materially different B; representation-based vs post-approval state-substitution variants; reproduced in 7 Agno AgentOS releases (≤3.0.9), 12 LangGraph Agent Server versions (≤0.14.0), OpenClaw 2026.2.23; OpenAI Agents SDK negative control; canonical approval rendering + exact use-time comparison blocks attacks | Occupies the human-approval boundary failure mode (security framing) |
| 2609.19226 | PAPC: Platform Mediation for Privacy-Propagation Externalities in AI-Mediated Workflows (16 Sep; cs.CR, cs.AI) | **Communication/memory, topology** | Privacy loss created before final answer via memory writes, shared-workspace updates, inter-agent messages, tool events; **cost of disclosure depends on topology and fanout** — a blast-radius notion; PAPC intercepts information-moving events: allow / release policy-safe abstraction / quarantine / block / narrow onward rights; eliminates measured raw-value exposure while preserving deterministic task completion | Closest this-week paper to "topology/fanout determines propagation cost" + graded containment actions. Privacy-specific, but the externality model transfers |
| 2609.19720 | Reachability, Not Observation: Containing Systems Whose Wiring Changes (17 Sep; cs.CR, cs.NI) | **Structural containment theory** | Snapshot-based containment misses time-varying wiring (hypercube rotation: defender sees 2 edges where 8,194 must be blocked); one step of clock lag drops containment to 0%; includes **tool-surface analysis of a coding agent**: idle instantaneous state-cut is zero while 6 channels carry it across a context reset; **agent self-spawn channel = branching process with sharp threshold at approval rate 1/b** — below it denial unnecessary, above it denial insufficient | Containment-under-dynamic-topology theory with an agent section; the 1/b approval threshold is a rare quantitative containment-threshold result |
| 2609.18304 | Rollback the World, Keep the Reflection: Rollback-Induced Reflection for Long-Horizon LLM Agents (16–17 Sep; cs.CL, cs.RO) | **Recovery** | Recovery as a **rollback-boundary control problem**: when to intervene, where to resume, what information survives recovery; unified operator over rollback depth × retained memory; restores prior state while carrying distilled knowledge from the abandoned trajectory; improves 3 long-horizon benchmarks across backbones | Occupies principled single-agent recovery design; multi-agent organizational recovery still open |
| 2609.19654 | Replan, Repair, or Edit? A Unified Empirical Evaluation of Travel Agents for Itinerary Revision under Resource Disruptions (17 Sep; cs.AI, cs.MA) | **Recovery** | 500 single-disruption + 200 compound-disruption cases (TREK-derived); LLM-Z3 replanning vs IPyHOPPER hierarchical repair vs iTIMO local revision; hierarchical/local repair preserves more accepted commitments at lower cost; guidelines balancing feasibility recovery, commitment preservation, cost | Recovery-strategy comparison with utility preservation — but single-agent planning domain |
| 2609.19789 | Contagion on the Trading Floor: How Adversarial Signals Spread in Multi-Agent Trading Systems (17 Sep; **ECML PKDD 2026**, LNCS 16946) | **Communication, topology** | GMATS framework; black-box poisoning via admissible social-media feeds; **contagion metrics tracing propagation through analyst and coordinator layers** (belief-shift scores, attack-clean backtest deltas); multi-agent topologies and coordinator prompts can **dampen adversarial shocks** under identical budgets | Topology-as-dampener result; domain-specific (trading), adversarial |
| 2609.16461 | Protocol-Preserving Context Trimming for Agentic Workflows (15 Sep; cs.SE, cs.AI) | **Memory** | 5 trimming strategies; metrics include **cascading failures** and critical context thresholds; adaptive budget guardrails: 96.0% task success, 1.0% cascading failure; retained-context ≤25% raises failure odds 10.92× | Uses "cascading failure" as a metric in workflow context management; guardrails as containment |
| 2609.17527 | Agentic Societies Need a Social Harness (15 Sep; cs.MA, cs.AI, cs.NI) | **Communication, accountability** | Honest competent agents fail with existing harnesses; faulty/malicious agents stall collaboration via "speech" exploits; layered social-harness architecture: (i) prevent failure classes outright, (ii) runtime detection of invalid messages, (iii) post-facto investigation and consequences | Position+experiments paper occupying the cross-trust-boundary containment/governance framing |

---

## 5. Tier 3 — Collective failure dynamics, org structure, evaluation (verified)

| arXiv | Title (date, venue) | Core content | Relation to seed |
|---|---|---|---|
| 2609.14767 | **Loop-Back Authority in LLM Agent Teams: A Paired Experiment on Flat and Hierarchical Coordination** (13/15 Sep; cs.MA, cs.AI, cs.CL, econ.GN) | Holds 5 agents/roles/prompts/tools/models fixed, varies one link: Manager may reject worker output and oblige revision. 43 paired products, 86 runs, business-intelligence reporting. Flat org scores higher on Utility (d=0.42, p=0.009) and Writing Clarity (d=0.34); hierarchical reports hedge 53% more; each revision loop −0.14 clarity; supervisory tier costs 51.5% more tokens for no gain. "A supervisor pays for itself when it can verify and becomes a liability when it can only opine." | **The authority-axis paper.** Varies org authority structure experimentally but measures output quality, not failure propagation. The seed's authority axis must cite and differentiate |
| 2609.18998 | One Axis, No Brake: Self-Knowledge Limits the Filtering of Harmful Peer Conformity in LLMs (v1 17 Jul 2026; cross-listed this week; cs.LG, cs.CL, cs.MA) | A brake keeping beneficial revisions while blocking harmful ones requires knowing the model was already correct (self-knowledge AUROC 0.64–0.89, "the wall"); at population scale, when most agents start wrong, debate amplifies the shared mistake into confident wrong consensus ("the cliff"); more agents/diversity/stronger member don't fix it; adding information before revision helps | Error *amplification* through deliberation — propagation dynamics without org structure |
| 2609.19183 | Message capacity and claim wording set the transition points of collective truth-finding in language-model networks (15 Sep; cs.MA, cs.CL, nlin.AO) | 31,824 randomized queries; agent judgment ≈ logistic function of weighted inbox sum; wrong consensus predicted unreachable below ~6.4/31 sources read — prediction fails (correct side wins <50% from every start); claim wording sets a threshold ("field"); transition points computable from two single-agent measurements | Phase-transition/contagion-style analysis: connectivity (message capacity) determines collective error — a "what determines spread" result in belief networks |
| 2609.20543 | Language-model groups overstate consensus when replaying human deliberation (17 Sep; cs.AI, cs.CL, cs.CY, cs.MA) | 100 held-out human Wason groups replayed with matched LLM groups; agent groups more consensual by 34–44 pp; reasoning-mode groups agree nearly unanimously, mostly on incorrect answers; simulated consensus does not track collective accuracy | Collective wrong-consensus evidence |
| 2609.13261 | From Process Loss to Assembly Bonus: Human-Grounded Diagnosis of Multi-Agent LLM Collaboration (6/15 Sep; **EMNLP 2026 camera-ready**) | LLM groups follow majorities more, surface less unique information, converge earlier than humans; correct minority signals succeed mainly when re-expressed early; interventions from human group-decision research give modest gains but don't remove the coordination bottleneck | Process-level diagnosis of LLM group failure mechanisms |
| 2609.16986 | ToMAS: A Pilot Failure-Grounded Theory-of-Mind Benchmark from Multi-Agent LLM Failures (15 Sep; cs.MA) | Converts MAST-Data FC2 (inter-agent misalignment) diagnosed execution traces into partner-state reasoning items; 242 traces → 39 CLEAN items; κ=0.92 annotator agreement; GRPO feasibility experiment shows NO training effect (LoRA update numerically negligible) — honestly reports pipeline + limitations | Builds on MAST failure taxonomy; failure-trace diagnosis infrastructure, not propagation/containment |
| 2609.17464 | Decomposition Buys Integrity, Not Yield (15 Sep; cs.MA, cs.AI, cs.DC) | Decomposition trees: if keep-probability r(b)=Cb^−δ, depth-k tree yields C^k N^(1−δ) — flat is optimal for yield; on 600 production deep-research traces δ=0.34; per-tier alignment penalty (1 brief in 16 goes off-target, μ=0.939); 0.7–11.3% of production sessions worth delegating vs 7.8% that do; hazard model on 743,819 tool calls: delegation is an opening move, not a response to filling context | Information loss across hierarchy tiers; when delegation is worth it — quantitative org-structure-cost evidence |
| 2609.19705 | SoK: Trading Agents or Market Crashers? (FARSIGHT) (17 Sep; cs.CR, cs.AI, cs.MA) | Scheme-level evaluation of 15 academic financial LLM trading schemes; 80% fail ≥1 core robustness metric, 100% exhibit security vulnerabilities; "a small misjudgment can cascade into a market-wide crash on its own, while an adversary can deliberately trigger the same collapse at minimal cost" | SoK establishing cascade risk in one high-stakes domain |
| 2609.17698 | A Large-Scale Empirical Study of Quality Assurance Practices and Gaps in AI Agents (15 Sep) | 157 open-source LLM-agent projects (≥100 GitHub stars); QA practices across execution surfaces, safeguards, testing artifacts, risk scenarios; current QA primarily... (gaps characterized) | Evidence that deployed agent systems lack reliability QA — motivation for the seed |
| 2609.16305 | BLINDSPOT: A Benchmark for Safety and Refusal Calibration in Long-Horizon Tool-Using Agents (14 Sep) | Trajectory-level safety; 22 attack families, 35 scenarios, 2,500+ trajectories, avg 14.7 turns; five outcomes incl. Unsafe Completion, Over-Refusal; "failures can emerge only after several initially safe interaction steps" | Long-horizon failure emergence; single-agent |
| 2609.15293 | (see Tier 1.4) | | |

---

## 6. Peripheral / screened out (title-verified, low relevance to seed)

| arXiv | Title | Why peripheral |
|---|---|---|
| 2609.19141 | Period-Inverted Blast-Radius Normalization ... OSIRIS-REx Capsule Infrasound | Only literal "blast radius" hit this week — hypersonics physics, unrelated |
| 2609.21192 | AI-GRACE: organizational objectives → deployment capabilities framework | Governance/assurance framework (design science), no failure-propagation study |
| 2609.13334 | The Agentic Company OS: Substrate Inversion (AGENTICS 2026) | Position paper on enterprise cognitive substrate |
| 2609.15314 | The Universe of Universes: Implosion Thresholds in Multi-LLM Systems | Ensemble-size vs performance; no fault propagation |
| 2609.17306 | Mo' Models, Mo' Problems (REALM @ EMNLP 2026) | Model-pool selection; heterogeneity can introduce "system instability" |
| 2609.18929 | Social Laws for Multi-agent Coordination in Stochastic Environments (RIPL @ ICAPS 2026) | Classical-MAS social laws, α-robustness verification — useful classical anchor |
| 2609.15009 | CoMem: Collective-Individual Memory Synergy | Memory architecture for MAS learning |
| 2609.21533 | MACE: Memory-Agent Co-Evolution with Adaptive Memory Graphs | Memory graphs reusing collaboration traces incl. failure repair |
| 2609.15161 | EMR: Self-Evolving Medical Multi-Agent System via Experience Mining and Reuse | Experience library — adjacent to KILLED "experience commons" topic (medical, non-adversarial) |
| 2609.19502 | Reputation as Community Memory for the Agentic Web (Cairn; IEEE eScience 2026) | Collective reputation memory — adjacent to KILLED "experience commons / zero-trust memory games" |
| 2609.16098 | Universal Defenses for Tool-Integrated LLM Agents | Defense vs 4 attack types (injection, memory poisoning, backdoor) |
| 2609.18605 | PACT: Can Enterprise AI Assistants Be Trusted Under Pressure? | Compliance-under-pressure benchmark, 12 enterprise domains |
| 2609.18298 | A Study of the Reliability of Agentic AI-Generated Programs | Fuzz-testing reliability of agent-generated code |
| 2609.19391 | MAGS: Multi-agent Auto-formalization Guarantees Safety | Formal verification (Dafny) of agent outputs |
| 2609.13637 | Identity Is More Than Recall (PAI-Bench) | Persistent-identity benchmark |
| 2609.15079 | Translating the Translator: English-Forcing Tax (EMNLP 2026 WS) | Inter-agent communication language cost — a communication-boundary failure tax |
| 2609.11365 | Portable Semantics, Private Dialects | Latent-communication negative transfer between LM societies |
| 2609.16051 | "Looking for Something Weird to Happen" | HCI, human sustainment of agent novelty |
| 2609.20889 | Proxifield: Decentralized Multi-Agent Communication through Semantic Proximity | Communication architecture |
| 2609.16599 | LLMs in the Loop: Stability- and Network-Aware Survey | Survey: LLMs in control loops of networked/CPS/MAS |
| 2609.16777 | Benchmarking Factual Robustness via Multi-conversation Persuasion | "Refusal Inertia" — single-model robustness |
| 2609.19721 | LearnActCoder: Role-Aware Error Memory for Clinical Coding Agents | Error memory routed by role (Coder/Judge) — role-aware recovery in one domain |

Also screened out from S2 results: classical control-theory "containment control of multi-agent systems" papers (terminology collision, different field), smart-water/digital-twin/voice-phishing/traffic orchestration applications, and non-arXiv items.

---

## 7. Answers to the standing questions

**Does anything this week KILL the seed hypothesis?**
No single paper kills it. But **2609.18460 (epidemic account of mutation/contagion/recovery) occupies the seed's central metaphor and research question** in the security-framing, and **2609.17648 occupies propagation-decomposition + structural containment in a role pipeline**, and **2609.17320 occupies stress-injection + cross-boundary propagation + containment failure in persistent MAS**. A submission that merely re-states "local faults can cascade; containment matters" would be scooped three times over *as of this week*.

**Does anything SUBSUME it?**
Partially. The union of 2609.18460 + 2609.17648 + 2609.17320 + 2609.15293 covers: fault injection, propagation across memory/tool/agent/communication boundaries, detection-vs-containment gap, structural containment mechanisms. NOT covered by anything this week: **organizational structure (roles, hierarchy, delegation topology, authority gradients) as the independent variable determining blast radius; non-adversarial operational faults; recovery-mechanism comparison with task-utility preservation; a unified multi-boundary blast-radius measurement instrument.** The seed survives only if re-aimed at that residue.

**Collision with occupied internal territory:** 2609.18820 (Compositional Policy Violations: Authority Creep, Threshold Laundering, provenance-aware runtime) collides with the existing maso/policy_preserving_delegation_research_proposal.md territory — that proposal's owner should be notified of a partial scoop risk.

**Classical anchoring available this week:** social-laws robustness verification (2609.18929, ICAPS 2026 WS), advanced transaction models lineage inside 2609.15397, control-theory "containment control" (terminology collision to acknowledge).

**Blind spot of this sweep:** papers submitted 19–21 Sep 2026 are not yet announced; arXiv export API was rate-limited (compensated via listing pages + Semantic Scholar + abs-page verification). Recommend a re-sweep on ~28 Sep before final submission decisions.
