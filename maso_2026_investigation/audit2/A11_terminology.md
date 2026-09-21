# A11 — TERMINOLOGY EXPANSION AGENT: Cross-Community Ontology + Combinatorial Search Audit

**Investigator:** AGENT 11 (Terminology Expansion)
**Date:** 2026-09-21
**Assignment:** Construct a systematic ontology of the research problem (fault propagation / containment / recovery / scarcity / structure / organization) across 10 communities, then use it to launch searches the previous swarm's cascade/blast-radius vocabulary missed. Special target: any paper matching "intervention helps at high resources, hurts at low resources."

---

## 0. BOTTOM LINE

The previous swarm's zero-hit claims were indeed vocabulary-limited. Using resilience/oversight/audit/budget/degradation/contagion vocabulary, I found **12 verified papers absent from all 48 prior reports**, including one that materially changes the audit:

1. **BRA-Audit (arXiv:2608.14668, Aug 2026)** — budget-constrained runtime auditing for LLM MAS on **real AutoGen executions**: audit-point placement under a fixed audit-call budget, localized rollback/recovery, defense-vs-token-cost Pareto, and a false-positive analysis showing **"excessive auditing can introduce unnecessary errors on benign trajectories"** (FP 0% → 12–16% as audit ratio ρ goes 0.2 → 1.0). This **occupies H2 outright** (containment reduces propagation but imposes cost — measured, on real LLM MAS, with a budget ablation) and **wounds H3** (containment actively harming benign work is demonstrated, though framed as over-auditing rather than scarcity sign reversal). FULL TEXT VERIFIED.
2. **Audit-capacity triage study (arXiv:2608.06949, Aug 2026)** — independent audit layer in a 9-agent LLM pipeline under **explicitly varied audit capacity**: undetected-bias rate 18.4% → 43.8% when the auditor is overloaded; coverage collapses 100% → 65.6%; risk-ordered queueing recovers coverage to 91.7% under the same capacity. This is "oversight effectiveness is a function of resource scarcity" in an LLM multi-agent pipeline — the closest existing experiment to H3's moderator variable. ABSTRACT VERIFIED. **Same first author (Arslan) as "Audit Without Verification" (2609.07680), which the prior swarm DID catch** — the swarm found the September paper and missed the August one, a within-author validation of the vocabulary-miss hypothesis.
3. **Memory Poisoning Propagation and Repair Mechanism in Multi-Agent Collaborative Environments (DOI 10.20944/preprints202602.1188.v1, Feb 2026)** — detection + **isolation/rewriting/conflict-resolution repair** of poisoned shared memory in collaborative MAS; cross-agent propagation reduced 78.1%, misbehavior 15.6%→2.3%, "minimal impact on overall task efficiency." This **directly contradicts prior reports' claim (B6, E5) that the memory boundary is the seed's strongest unoccupied wedge** — memory-boundary propagation + repair + utility impact is now occupied (preprint, low-tier). ABSTRACT VERIFIED via Crossref (full abstract incl. method/numbers).

**H3's exact claim survives but is surrounded.** No paper found demonstrates the full sign reversal — *the same containment mechanism flipping from net-positive under budget abundance to net-negative under scarcity* — in tool-executing LLM MAS. But the phenomenon-space is occupied in five adjacent senses (§5), and four canonical adjacent-community results (epidemiology contact-tracing capacity, human-factors alarm fatigue, queueing admission control, Hollnagel's ETTO) establish the pattern as *known* — a reviewer can call H3 "ETTO rebranded" unless the paper explicitly imports and tests that literature.

---

## 1. METHOD AND TOOLING LOG

Sources queried 2026-09-21: arXiv API (export.arxiv.org — worked in windows, throttled ~50% of session), arXiv search UI via fetch (worked, then 429), Crossref REST (worked throughout — primary channel for non-arXiv), DataCite (worked; relevance ranking swamped by Zenodo spam — low yield), OpenReview API v2 search (worked; mostly DBLP/review records — low yield), Semantic Scholar Graph API (single-paper endpoints worked; search endpoint 429 all session), OpenAlex (daily budget exhausted, shared IP).

Combinatorial query matrix executed (arXiv unless noted): graceful degradation × LLM agent; error amplification × LLM; compounding errors × LLM; faulty agent × LLM; error cascade × LLM; resilient × multi-agent × LLM × fault; oversight × LLM × agents × cost; verifier × multi-agent × budget; sycophancy/misinformation × propagation × multi-agent; verification × budget × multi-agent; overload × multi-agent × LLM; resource constraints × multi-agent × LLM; containment × multi-agent × LLM (recheck); circuit breaker × LLM agent (recheck); quarantine × LLM agent (recheck); rollback × multi-agent × LLM; fault tolerance × multi-agent × LLM; hierarchy × robustness × multi-agent × LLM; budget × recovery × multi-agent × LLM; organizational × multi-agent × LLM × failure; sentinel × LLM agent; exception handling × LLM agent; escalation × multi-agent × LLM; redundancy × cost × multi-agent × LLM × fault; self-healing × multi-agent × LLM; contagion × multi-agent × LLM; immune × multi-agent × LLM; congestion × multi-agent × LLM; critic × cost × multi-agent × LLM. Crossref: contact tracing × capacity; alert fatigue × automation; admission control × overload; self-correction × degrade; verification × multi-agent × cost; delegation depth × failure; misinformation × propagation × multi-agent LLM; memory poisoning × multi-agent; organizational resilience × LLM agents; multi-agent collaboration × counterproductive × budget; Cvach alarm fatigue; SEDA; Motter cascade control; test-time verification granularity; ETTO; graceful extensibility; error management culture; defense × degrades × multi-agent LLM; excessive verification; oversight × workload. OpenReview: fault propagation × LLM agents; oversight × budget × agent; containment × recovery × LLM agents; cascading failure × LLM; error propagation × multi-agent.

**Reliability caveats:** (a) queries run during arXiv throttling windows that returned 0 results are marked UNRELIABLE NEGATIVE (delegation chain × LLM; compensation/saga × LLM workflow; decentralized × failure × robust; judge × budget); (b) S2 search and OpenAlex were unavailable — recall on non-arXiv 2026 preprints (SSRN/TechRxiv/preprints.org) relies on Crossref bibliographic search, which is noisy; (c) all positive finds below were individually verified on arXiv abstract pages, arXiv HTML full text, or Crossref metadata with full abstracts.

---

## 2. THE CROSS-COMMUNITY ONTOLOGY

The research problem decomposes into six concept clusters. For each: the vocabulary each community actually uses (the search surface), and the canonical anchors (verified this session or in prior waves).

### 2.1 FAULT (the thing that propagates)

| Community | Vocabulary | Canonical anchors |
|---|---|---|
| LLM agents | hallucination, semantic fault, drift, sycophancy, false belief, instruction decay, factual attrition, stance homogenization, poisoning, corruption, bias, faulty/malicious agent, governance decay, behavioral drift, collapse | MAST (2503.13657); AgentCollabBench (2605.08647, NEW); Deliberative Illusion (2606.03032, NEW); Governance Decay (2606.22528, NEW) |
| Classical MAS | exception, agent death, non-compliance, norm violation, Byzantine | Klein & Dellarocas (Agents'99); Hägg 1997 |
| Distributed systems | crash, omission, timing, Byzantine, gray failure, metastable failure, soft error | Avizienis et al. TDSC 2004 (fault→error→failure chain); Bronson et al. HotOS 2021 (metastable) |
| Reliability/safety eng. | latent failure, active failure, drift into failure, initiating event | Reason 1997; Dekker; Leveson STAMP |
| Software eng. | bug, defect, fault, regression, fault localization | Voas COMPSAC 1997 (error propagation probability) |
| Network science | node failure, overload, attack, removal | Motter & Lai PRE 2002 (10.1103/physreve.66.065102, VERIFIED) |
| Epidemiology | infection, exposure, index case, importation | standard SIR/SEIR |
| Org science | error, incident, accident, near-miss, violation | Perrow 1984; Reason 1997; van Dyck et al. JAP 2005 (10.1037/0021-9010.90.6.1228, VERIFIED) |
| Human factors | slip, lapse, mistake, violation | Reason; Parasuraman & Riley 1997 |
| OR/queueing | demand shock, arrival, abandonment | standard |

### 2.2 PROPAGATION

| Community | Vocabulary | Canonical anchors |
|---|---|---|
| LLM agents | cascade, error cascade, **error amplification**, **error accumulation**, compounding error, hallucination propagation/snowball, **contagion** (preference/emotional/adversarial/reliability), infection, spread, diffusion, downstream corruption, **evidence-root lineage propagation**, **coupling** (Contagion Tensor), inheritance, percolation | From Spark to Fire (2603.04474); Hallucination Snowball (2608.14588); Hallucination Cascade (2606.07937); Contagion Networks (2606.20493); TIDE (2608.03421); Sycophancy Propagation (2604.02668, NEW); Contagion Tensor (2606.28839, NEW) |
| Classical MAS | **unzippering effect**, exception propagation | Dellarocas & Klein ICMAS 2000; Platon et al. |
| Distributed systems | cascading failure, domino effect, retry storm, load amplification, cross-layer propagation | Buldyrev et al. Nature 2010; metastable failures |
| Network science | cascade size, branching factor σ, percolation threshold, spectral radius, k-core | Dobson et al. HICSS 2004; Kempe et al. KDD 2003 |
| Epidemiology | transmission, R0, superspreading, generations | standard |
| Org science | organizational accident trajectory, latent failure pathways, normalization of deviance | Reason 1997; Vaughan |
| SE | defect propagation, ripple effect, change propagation, error permeability | Voas 1997; Hiller et al. |
| Human factors | error chain, incident cascade | Reason's Swiss cheese |

### 2.3 CONTAINMENT

| Community | Vocabulary | Canonical anchors |
|---|---|---|
| LLM agents | guardrail, tripwire, **auditor/auditing**, monitor, **sentinel**, guardian, gate/gating, verification, oversight, moderation, isolation, quarantine, blocking, pruning, circuit breaker, sandbox, capability attenuation, **audit-point placement**, interposition, mediation, firewall, link enforcement | GuardAgent; PeerGuard; TrinityGuard; G-Safeguard; **BRA-Audit (2608.14668, NEW)**; **Sentinel Agents (2509.14956, NEW)**; **MAPLE-Guard (2608.00426, NEW)**; ScopeJudge (2607.07774, NEW) |
| Classical MAS | sentinel, exception handling, norm enforcement, sanction, exclusion/exile | Hägg 1997; Klein & Dellarocas; MOISE+ norms |
| Distributed systems | circuit breaker, **bulkhead**, fault containment region, fencing, fail-safe/fail-operational, **graceful degradation**, **load shedding**, **admission control**, backpressure | Nygard; Hystrix; SEDA (10.1145/502034.502057, VERIFIED); AWS fault-isolation boundaries |
| Safety eng. | defense-in-depth, barriers, layers of protection (LOPA), safety instrumented systems, interlocks | IEC 61511 lineage |
| Epidemiology | isolation, quarantine, **contact tracing**, ring vaccination, cordon sanitaire, NPIs | Kretzschmar et al. Lancet Public Health 2020 (10.1016/s2468-2667(20)30157-2, VERIFIED) |
| Org science | error management (vs error prevention), buffering, redundancy, loose coupling, slack | van Dyck et al. 2005; Weick |
| Human factors | alarm/alert, escalation, supervision, cross-checking | Cvach 2012 (10.2345/0899-8205-46.4.268, VERIFIED) |

**Terminological traps found:** "containment" in control theory = confining followers within a convex hull of leaders (containment control — OpenReview/DBLP hits, irrelevant). "Sentinel" in LLM-MAS security = monitoring agent (Gosmar & Dahl) — same word as Hägg 1997, **no citation link** (verified: zero classical MAS citations in 2509.14956 full text). "Blast radius" = security/authorization sense (Anthropic, Bounded Agents) vs chaos-engineering sense vs CtC's propagation metric — three senses occupied.

### 2.4 RECOVERY

| Community | Vocabulary | Canonical anchors |
|---|---|---|
| LLM agents | retry, rollback, checkpoint, re-execution, repair, regeneration, replanning, self-healing, self-correction, refinement, restoration, **rehabilitation**, resumption, **tiered recovery**, localized recovery | RoMa; Self-Healing Orchestrators (2606.01416); Real-Time Detection & Repair (2608.02464); **GSAR (2604.23366, NEW — tiered recovery under explicit compute budget)**; **Memory Poisoning Propagation & Repair (NEW)** |
| Classical MAS | reorganization, reallocation, replication, re-bidding, proxy agents | Kota et al. TAAS 2012; Horling et al. 2001; DARX |
| Distributed systems | checkpoint/rollback, replay, **saga / compensating transaction**, failover, microreboot, crash-only, ROC | Chandy-Lamport 1985; Garcia-Molina & Salem 1987; Candea & Fox |
| SE | automated program repair (APR), hotfix, revert | TRAIL; SHERLOC (2606.24820) |
| Epidemiology | recovery/removal (SIR), treatment | standard |
| Org science | resilience, restoration, learning from failure, high-reliability organizing | Hollnagel; Weick & Sutcliffe |

### 2.5 SCARCITY (the H3 moderator variable)

| Community | Vocabulary | Canonical anchors |
|---|---|---|
| LLM agents | token/compute/API **budget**, cost, latency, context window, rate limits, **capability tier** (local/weak models), **audit capacity**, **oversight capacity**, attention budget | **BRA-Audit (audit ratio ρ)**; **audit-capacity triage (2608.06949)**; Oversight Has a Capacity (2606.08919); **Two Calls Beat Five Agents (2607.26922, NEW — capability scarcity)** |
| Distributed systems | **overload**, **congestion**, **saturation**, starvation, capacity, resource exhaustion | SEDA; Hystrix |
| OR/queueing | utilization, offered load, admission control, congestion collapse | standard |
| Human factors | **workload**, **fatigue**, vigilance decrement, **alert fatigue**, attentional capacity, out-of-the-loop | Cvach 2012; Bainbridge 1983; Endsley & Kiris 1995 |
| Epidemiology | **tracing capacity**, testing capacity, hospital capacity, resource-limited settings | Kretzschmar 2020 |
| Org science | **resource scarcity**, **organizational slack**, austerity, **ETTO (efficiency–thoroughness trade-off)** | Hollnagel, The ETTO Principle (10.1201/9781315616247, VERIFIED); Woods, graceful extensibility (10.1007/s10669-018-9708-3, VERIFIED) |
| Classical MAS | **scarce subcontractors** | Dellarocas & Klein ICMAS 2000 (citizen < survivalist under scarcity — the seed's own anchor) |

### 2.6 STRUCTURE

| Community | Vocabulary | Canonical anchors |
|---|---|---|
| LLM agents | topology, hierarchy, chain, flat, star, DAG, layered, **tiered**, depth, **width**, span, architecture, pipeline | Zhou et al. 2408.00989; Kim et al. 2512.08296; TAO (2506.12482); **Width, Memory, and Delay (2608.00028, NEW)**; AgentCollabBench (topology explains 7–40% of variance in multi-hop information survival, NEW) |
| Classical MAS | organizational paradigms, roles/groups/links, authority relations | Horling & Lesser 2004; MOISE+; AGR |
| Org science | centralization, formalization, hierarchy depth, **span of control**, tight/loose coupling | Perrow; Weick |
| Network science | degree distribution, clustering, modularity, core-periphery | standard |

### 2.7 ORGANIZATION / GOVERNANCE

institutional, governance, accountability, audit, compliance, norms, decision rights, authority, **delegation**, escalation, reporting structure, bureaucracy. LLM-era anchors: Audit Without Verification (2609.07680); **DARC — Delegation-Aware Runtime Contracts (10.21203/rs.3.rs-10533072/v1, Aug 2026, NEW: budget/capability attenuation along delegation handoffs + state recovery)**; **JAAMAS 2026 task-delegation model on sub-delegations and delegation chains (10.1007/s10458-026-09741-z, NEW, classical side)**; Delegation Without Trust (2609.00267).

---

## 3. NEW PAPERS FOUND (absent from all 48 prior reports), WITH VERIFICATION LEVELS

### TIER 1 — Load-bearing for the audit

**N1. BRA-Audit: Budgeted Runtime Auditing for LLM Multi-Agent Systems via Cumulative-Exposure Audit-Point Placement** — Wang et al., arXiv:2608.14668, v1 2026-08-02. **FULL TEXT VERIFIED** (arXiv HTML, incl. Algorithm 1, threat model, Tables 1–6).
- What it is: models MAS execution as a dynamic dependency DAG; formulates auditing as **audit-point placement under a fixed audit-call budget** minimizing cumulative unchecked exposure (AuditGap × topological impact); trusted audit points bound regions for **localized rollback + re-execution**; blocks unsafe downstream flow.
- Experiments: **real LLM MAS** (AutoGen; Qwen3-235B main; GPT-5/Gemini-3/GLM-5.1/DeepSeek-V4/MiniMax-2.7 ablations) on AgentsNet, BBH, MultiAgentBench-Research; 20% malicious agents (unified abstraction incl. hallucination); attack drops AgentsNet score 0.8162→0.4407; BRA-Audit restores 0.8208 at 54.5K tokens; 17.2–40.6% fewer tokens than PeerGuard/MAD.
- **H3-relevant results:** audit-budget ablation ρ ∈ {0.2,0.4,0.6,1.0}: score rises monotonically (0.760→0.893 on BBH) while token cost rises; "as ρ increases, audit cost grows while rollback cost decreases." **False-positive analysis: 0% FP at ρ=0.2 → 12%/16% FP at full auditing — "excessive auditing can introduce unnecessary errors on benign trajectories."**
- Threat: **occupies H2** (containment-vs-cost, measured, real LLM MAS, budget ablation, Pareto framing) and **partially occupies H3's mechanism** (containment actively harming benign trajectories). Does NOT vary scarcity as an independent variable of the *environment*; does not show sign reversal; no organizational boundaries (dependency graph only); adversarial-leaning threat model.

**N2. Does Splitting a Triage Decision Across Agents Hide Bias or Help Catch It? A Multi-Agent Simulation Study of LLM-Based Resource Allocation Under Audit Capacity Constraints** — Arslan, arXiv:2608.06949, v1 2026-08-07 (6pp, code+data released). **ABSTRACT VERIFIED** (arXiv abs page).
- 9-agent role-differentiated pipeline (assessment, allocation, independent audit) vs single-agent control; 192 episodes / 2,304 case pairs; **three independently varied pressure dimensions incl. audit capacity**.
- Findings: multi-agent vs single-agent bias rates indistinguishable (6.9% vs 6.1%, p=0.498); **audit capacity is the large significant effect**: undetected biased outcomes 18.4% → 43.8% under auditor overload; driven by coverage collapse (100%→65.6%), not judgment degradation; **risk-ordered audit queue recovers coverage to 91.7% under the same capacity constraint**.
- Threat: the closest existing experiment to H3's moderator — **oversight/containment effectiveness as a function of resource scarcity in an LLM multi-agent pipeline**, with a mechanism-design mitigation under fixed capacity. It shows degradation-under-scarcity, not backfire (oversight never hurts; it just covers less). Bias-catching frame, not fault propagation.

**N3. Memory Poisoning Propagation and Repair Mechanism in Multi-Agent Collaborative Environments** — Liu, Xu, Ma, Xu, Qiu; preprints.org 2026-02-14, DOI 10.20944/preprints202602.1188.v1. **ABSTRACT VERIFIED** (Crossref full abstract incl. method+numbers; preprints.org page bot-blocked; not indexed by S2).
- Evidence graph over memory source credibility + content consistency; contrastive-learning anomaly detection; **on detection, "further propagation is suppressed through isolation, rewriting, and conflict resolution"**; 60 collaborative tasks, ~210k memory records, 12k injected poisoned samples; AUC 0.94; misbehavior 15.6%→2.3%; **cross-agent propagation −78.1%; "minimal impact on overall task efficiency"** (utility preservation claimed).
- Threat: **directly occupies the memory-boundary propagation + containment + repair + utility wedge** that B6/E5 called the seed's strongest residual gap. Caveats: non-peer-reviewed preprint; adversarial (poisoning) frame; no organizational semantics.

**N4. Sentinel Agents for Secure and Trustworthy Agentic AI in Multi-Agent Systems** — Gosmar & Dahl, arXiv:2509.14956, v1 2025-09-18 (doc dated 2026-08-24). **FULL TEXT VERIFIED** (arXiv HTML; references section searched).
- Sentinel-agent network + Coordinator: monitoring, anomaly detection, **isolation/quarantine of misbehaving agents, containment**; deployment patterns (sidecar/proxy/continuous-listener); simulation with 162 synthetic attacks (prompt injection, hallucination, exfiltration) — detection feasibility only.
- Threat to the transfer framing: **the classical "sentinel" mechanism (Hägg 1997) is already re-invented by name for LLM MAS — with zero citations to the classical lineage** (verified: no Hägg/Dellarocas/Klein references). So the *mechanism* is occupied in LLM-MAS vocabulary while the *explicit transfer test* remains unclaimed — the candidate's exact positioning, but the gap is now "known mechanism, untested predictions," which is thinner.

### TIER 2 — New occupants of adjacent territory

**N5. Too Polite to Disagree: Understanding Sycophancy Propagation in Multi-Agent Systems** — Parulekar et al., arXiv:2604.02668, v1 2026-04-03; **SIGDIAL 2026 (peer-reviewed), pp. 795–814**. ABSTRACT VERIFIED. Peer-sycophancy rankings (static + online) reduce influence of sycophancy-prone peers, **mitigate error cascades**, +10.5% final accuracy across six open LLMs. Non-adversarial semantic-fault propagation + lightweight mitigation in deliberative MAS. Adds a peer-reviewed brick to the propagation cluster.

**N6. AgentCollabBench: Diagnosing When Good Agents Make Bad Collaborators** — Mazumder et al., arXiv:2605.08647, v1 2026-05-09. ABSTRACT VERIFIED. 900 human-validated tasks; four behavioral risks: **instruction decay, false-belief contagion, context leakage, tracer durability**; four LLMs; **communication topology explains 7–40% of variance in multi-hop information survival**; converging-DAG synthesis bottleneck discards minority-branch constraints. Organic process-failure propagation with topology as IV — overlaps H1's generic claim ("structure determines propagation") from the diagnostics side.

**N7. Two Calls Beat Five Agents: Evaluating Multi-Agent Pipelines Against Self-Refinement for Local Language Models** — Mohite, arXiv:2607.26922, v1 2026-07-29. ABSTRACT VERIFIED. 5-role pipeline on Qwen2.5-7B: GSM8K 75.0%→45.0% (JSON format, **error accumulation**); two-call self-refinement 86.2% at 7.4× lower tokens; **the same refinement on HumanEval actively destroys performance (96.3%→66.5%)**; task-aware gating restores 95.1%. **H3-adjacent: under capability scarcity (weak local model), both multi-agent structure and self-verification can actively hurt; mechanism value is task/resource-conditioned.** Single-workflow, small scale.

**N8. Governance Decay: How Context Compaction Silently Erases Safety Constraints in Long-Horizon LLM Agents** — Chen et al., arXiv:2606.22528, v2 2026-06-27. ABSTRACT VERIFIED. **Token-budget pressure (scarcity) causes context compaction to silently strip in-context governance constraints** — violation 0%→30% (up to 59%) post-compaction across 7 model families, 1,323 episodes; Constraint Pinning (quarantining constraints from compaction) restores 0%. Single-agent, but a distinct H3 mechanism: **scarcity doesn't just starve containment — it dismantles it.**

**N9. The Interaction Tax: When Communication Erases Diversity in Multi-Agent Teams** — Ann et al., arXiv:2608.23541, v1 2026-08-24; **ICML 2026 (PMLR 306)**. ABSTRACT VERIFIED. Full-solution interaction collapses diversity within one round; under matched budgets interaction is a weak default; critique helps only when the violated rule is easy to find/fix. Peer-reviewed evidence that **a coordination/verification mechanism's value is conditional, not monotonic** — supports the plausibility of H3's sign reversal while occupying "interaction helps/hurts under budget" for reasoning quality (not fault containment).

**N10. Multi-Agent Teams Hold Experts Back** — Pappu et al., arXiv:2602.01011, v1 2026-02-01; **ICML 2026**. ABSTRACT VERIFIED. Self-organizing LLM teams fail to match their expert member (up to −41.1%); integrative compromise grows with team size; **consensus-seeking improves robustness to adversarial agents — an explicit alignment-vs-performance trade-off**. Occupies the *genre* "experimental transfer test of organizational/team-science theory onto LLM agent teams" (org-psych strong-synergy hypothesis), which the candidate's framing echoes for classical MAS.

**N11. GSAR: Typed Grounding for Hallucination Detection and Recovery in Multi-Agent LLMs** — Kamelhar, arXiv:2604.23366, v1 2026-04-25. ABSTRACT VERIFIED. Evidence-typed groundedness scoring + **three-tier recovery (proceed/regenerate/replan) under an explicit compute budget**; claims "first published groundedness framework coupling evidence-typed scoring with tiered recovery under an explicit compute budget." FEVER-only, claim-level; occupies budgeted verification+recovery vocabulary.

**N12. Width, Memory, and Delay: A Resource Accounting for the Limits of Flat Multi-Agent Systems** — Kuznetsov, arXiv:2608.00028, v1 2026-07-14. ABSTRACT VERIFIED. Controlled disturbance-rejection testbed; flat swarms with matched internal models match/beat designed hierarchies at equal per-agent memory; **width × memory × delay exchange rates with hard non-exchange boundaries under equal total-state budget**. Control-theoretic, no LLM faults, but directly engages "is hierarchy necessary or is it a resource trade?" — H1's depth question reframed as resource accounting.

### TIER 3 — Contextual / weaker

- **Look Before You Leap: Pre-Action Verification for LLM Agents** (arXiv:2609.11957, 2026-08-09). ABSTRACT VERIFIED. Cheap deterministic pre-action checks; silent-failure taxonomy; refuse-when-unsure at tunable applicability cost. Single-agent; occupies "verification cost–coverage trade-off" vocabulary.
- **ScopeJudge: Cost-Aware Pre-Execution Gating for Offensive Security Agents** (arXiv:2607.07774, v2 2026-07-30). ABSTRACT VERIFIED. Cost–accuracy Pareto of gating judges; cost-sensitive vs recall-first operating points. Single-agent security gating.
- **The Deliberative Illusion** (arXiv:2606.03032, 2026-06-02). ABSTRACT VERIFIED. Factual attrition (up to 72% of issue-critical facts erased) + stance homogenization in deliberation; a propagation-of-loss phenomenon in non-adversarial MAS discussion.
- **The Contagion Tensor** (arXiv:2606.28839, 2026-06-27). ABSTRACT VERIFIED. Coupling Amplification Factor measurement instrument; honest simulation/real-API split (5/11 conditions real).
- **DARC: Delegation-Aware Runtime Contracts for Open LLM Multi-Agent Systems** (DOI 10.21203/rs.3.rs-10533072/v1, 2026-08-13). ABSTRACT VERIFIED via Crossref. Budget/capability/scope attenuation along delegation handoffs + revocation + state recovery — further occupies the delegation boundary (already flagged as crowded).
- **A task delegation model based on trustworthiness in sub-delegations and delegation chain formation** (Baqueta & Tacla, **JAAMAS 2026**, DOI 10.1007/s10458-026-09741-z). METADATA VERIFIED (Crossref; no abstract available). Classical-MAS-side delegation-chain work, current year.
- **Adaptive AI Delegation under Uncertainty** (arXiv:2606.29406, 2026-06-28). ABSTRACT VERIFIED. Governance-POMDP for allocating decision authority to AI; graceful-degradation stress tests. Org-governance framing, no faults.

---

## 4. THE H3 SIGN-REVERSAL HUNT ("intervention helps at high resources, hurts at low resources")

### 4.1 Direct hits in LLM-MAS: the exact pattern NOT found

No located paper varies resource scarcity as an independent variable and demonstrates a containment/verification mechanism flipping from net-positive to net-negative in tool-executing LLM MAS. The exact H3 claim survives this sweep.

### 4.2 Adjacent-sense occupants (each kills a broader framing of H3)

| # | Paper | What it shows | Which H3 framing it kills | Verification |
|---|---|---|---|---|
| A | **BRA-Audit** (2608.14668) | More auditing → monotonic score gain but rising token cost AND rising false-positive harm on benign trajectories (0%→16%); audit cost ↑ while rollback cost ↓ | "First to show containment has costs that can dominate in LLM MAS" | FULL TEXT |
| B | **Audit-capacity triage** (2608.06949) | Oversight value collapses under capacity scarcity (coverage-driven); queue redesign recovers it | "First to study oversight under resource scarcity in LLM MAS" | ABSTRACT |
| C | **Oversight Has a Capacity** (2606.08919; prior swarm B8) | Inverted-U: safety vs escalation rate with fatiguing human; flooding attack | "First to model oversight as a depletable resource" | ABSTRACT (prior wave) |
| D | **Two Calls Beat Five Agents** (2607.26922) | Under capability scarcity, multi-agent pipelines and self-refinement actively hurt | "First to show agentic mechanisms backfire when resources are weak" | ABSTRACT |
| E | **Governance Decay** (2606.22528) | Token-budget scarcity silently dismantles in-context containment | "Scarcity only starves containment" (it also destroys it) | ABSTRACT |
| F | **Huang et al., ICLR 2024** (2310.01798) | Intrinsic self-correction degrades reasoning without external feedback | "Verification backfires" in single-LLM sense | ABSTRACT |
| G | **Rethinking Optimal Verification Granularity** (NeurIPS 2025, 10.52202/085713-2964) | Verification granularity should scale with compute budget | "Verification dose vs budget" in test-time scaling | METADATA (Crossref; no abstract) |
| H | **Interaction Tax** (2608.23541, ICML 2026) | Interaction/critique value is conditional under matched budgets | "More coordination/verification is monotonically good" | ABSTRACT |

### 4.3 Adjacent-community canonical results (the "known phenomenon" risk)

| Community | Anchor (verified) | The sign-reversal/conditionality result |
|---|---|---|
| Epidemiology | Kretzschmar et al., Lancet Public Health 2020 (10.1016/s2468-2667(20)30157-2) | Contact-tracing containment effectiveness collapses with delay/capacity; containment feasible only while caseload < tracing capacity |
| Human factors | Cvach, Biomed Instrum Technol 2012 (10.2345/0899-8205-46.4.268); Bainbridge Automatica 1983; Parasuraman & Riley 1997 | Alarm/alert systems help at low rates, harm at high rates (alarm fatigue, cry-wolf); automation degrades the operator asked to rescue it |
| Queueing/distsys | Welsh et al., SEDA, SOSP 2001 (10.1145/502034.502057) | Admission control/load shedding: pure overhead at low load, system-saving under overload |
| Org science | Hollnagel, The ETTO Principle (10.1201/9781315616247); Woods, graceful extensibility (10.1007/s10669-018-9708-3) | Under time/resource pressure, thoroughness (verification, checking) is systematically traded for efficiency — the organizational-science statement of H3's mechanism |
| Network science | Motter, PRL 2004 (10.1103/physrevlett.93.098701) | Cascade control/defense strategies whose value depends on where/when applied |
| Classical MAS | Dellarocas & Klein ICMAS 2000 (E5, full text) | Citizen (EH services) slightly worse than survivalist with short tasks + scarce subcontractors — the seed's own anchor |

**Implication:** H3's survival depends on claiming the *LLM-MAS-specific, mechanism-level, sign-reversal* demonstration — not the phenomenon, which is multiply occupied. The paper should import ETTO/alarm-fatigue/contact-tracing-capacity as prior theory and position itself as their first experimental instantiation for semantic-fault containment in agent organizations. Failure to cite these = desk-reject risk from any reviewer with safety-engineering or human-factors background (MASO's classical-MAS pool plausibly has them).

---

## 5. COLLISION CLASSIFICATION PER CLAIM IN MY LANE

| Claim | Classification | Basis |
|---|---|---|
| **H1** (delegation/org depth changes fault propagation & recovery cost; amplify-vs-attenuate conflict) | **SUBSTANTIALLY OCCUPIED (generic level); conflict is real and open** | Structure→spread: Zhou 2408.00989, Kim 2512.08296, AgentCollabBench (NEW, topology 7–40% variance), CTHA, Width/Memory/Delay (NEW), classical unzippering. Amplify-vs-attenuate conflict confirmed: Hallucination Cascade (attenuation 0.644) vs From Spark to Fire (amplification) — unresolved scientific question the seed could own. Surviving wedge: organizational (authority/accountability/human) boundary-typed depth effects in real executions |
| **H2** (containment reduces propagation but imposes cost) | **OCCUPIED — cannot be claimed even as secondary** | BRA-Audit (NEW, full text: budget ablation + defense-cost Pareto + audit-vs-rollback cost trade-off, real LLM MAS); CtC (simulation); DamageFlow; ScopeJudge; GSAR; cost-aware protocol routing (2608.14927) |
| **H3** (containment backfires under scarcity — sign reversal) | **WOUNDED BUT ALIVE (narrow form only)** | Exact sign reversal in tool-executing LLM MAS: not found (§4.1). But five adjacent-sense occupants (§4.2) + six canonical adjacent-community results (§4.3) surround it. Defensible form: "first demonstration that containment mechanisms flip sign under token/tool/latency/reviewer budget scarcity in tool-executing LLM agent organizations, as predicted by ETTO/alarm-fatigue/contact-tracing-capacity theory and by Dellarocas & Klein's scarcity arm" |
| **Framing** ("first experimental transfer test of classical MAS fault-handling on LLM orgs") | **WOUNDED** | Sentinel mechanism already re-invented for LLM MAS without classical citations (Sentinel Agents 2509.14956, NEW, full text); org-theory transfer-test genre exists (Multi-Agent Teams Hold Experts Back, ICML 2026, NEW; Can Lessons From Human Teams 2510.07488); exception handling for LLM agents exists (SHIELDA). Verified via S2 citation APIs this session: Dellarocas & Klein ICMAS 2000 (57 citations; post-2020 citers = 3 classical JaCaMo/MOOP papers, zero LLM content); Hägg 1997 (137 citations; post-2023 citers = 2 classical papers, zero LLM content). **The specific transfer test remains unclaimed** — but it is now "testing predictions of a mechanism others have already re-invented," a thinner claim |
| **Memory boundary as strongest residual wedge** (B6/E5 claim) | **DEAD** | Memory Poisoning Propagation & Repair (N3) + MAPLE-Guard (N-new, 2608.00426: memory-lifecycle gates at write/retrieval/promotion/reuse, ASR 38.2%→0.9%, cross-agent contamination framing) occupy memory-boundary propagation + containment + repair |

---

## 6. UNEXPECTED FINDINGS

1. **Within-author vocabulary miss (validates the assignment's premise).** The prior swarm caught Arslan's *September* 2026 paper ("Audit Without Verification", accountability vocabulary) but missed his *August* 2026 paper ("audit capacity constraints", oversight-scarcity vocabulary) — the one that matters more for H3. Same author, same program, different vocabulary → different discoverability.
2. **Governance Decay (2606.22528) reveals a fourth H3 mechanism** beyond budget competition: scarcity (token pressure → context compaction) doesn't just starve containment mechanisms, it *silently removes them from the system state*. No prior report mentions compaction-driven containment loss.
3. **BRA-Audit's false-positive result is the closest existing empirical brick to "containment hurts"** — over-auditing introduces errors on benign trajectories (0%→16% FP) — yet its own framing is "efficiency dilemma," not scarcity. The H3 sign-reversal may be one ablation away from being scooped: BRA-Audit already has the budget knob (ρ), the cost accounting, and the benign-trajectory harm measurement. **Flag as acute scoop risk before October 2026.**

## 7. NEGATIVE RESULTS (reliability-marked)

Reliable negatives (API healthy, 0 relevant hits): "immune" × multi-agent × LLM; "congestion" × multi-agent × LLM; "critic" × cost × multi-agent × LLM; "circuit breaker" × LLM agent → only 2 security-side hits; "quarantine" × LLM agent → only security/trust-boundary hits (MAPLE-Guard, WebMCP-Phalanx, Sentinel Agents); "redundancy" × cost × fault × multi-agent × LLM → 0.
**Unreliable negatives (returned 0 during arXiv throttle windows — do not rely):** "delegation chain" × LLM; "compensation"/"saga" × LLM agent workflow; "decentralized" × failure × robust × multi-agent LLM; "judge" × budget × multi-agent; "saturation"/"starvation" × multi-agent LLM.

## 8. VERIFICATION LOG

- FULL TEXT VERIFIED: BRA-Audit 2608.14668 (arXiv HTML: abstract, intro, system/threat model, method, Algorithm 1, experiments RQ1–RQ3, Tables 1–6, FP analysis, references); Sentinel Agents 2509.14956 (arXiv HTML incl. references — zero classical MAS citations confirmed).
- ABSTRACT VERIFIED (arXiv abs pages fetched this session): 2608.06949, 2604.02668, 2605.08647, 2607.26922, 2606.22528, 2608.23541, 2602.01011, 2604.23366, 2608.00028, 2609.11957, 2607.07774, 2606.03032, 2606.28839, 2606.29406, 2310.01798, 2608.00426.
- CROSSREF METADATA/ABSTRACT VERIFIED: 10.20944/preprints202602.1188.v1 (full abstract); 10.21203/rs.3.rs-10533072/v1 (full abstract); 10.1007/s10458-026-09741-z (metadata only); 10.52202/085713-2964 (metadata only); 10.1016/s2468-2667(20)30157-2; 10.2345/0899-8205-46.4.268; 10.1145/502034.502057; 10.1103/physreve.66.065102; 10.1103/physrevlett.93.098701; 10.1201/9781315616247; 10.1007/s10669-018-9708-3; 10.1037/0021-9010.90.6.1228.
- S2 CITATION APIS (single-paper endpoints, this session): Dellarocas & Klein ICMAS 2000 = CorpusId 6442794, 57 citations, post-2020 citers {10.1017/S0269888925000050, 10.5555/3463952.3464226, one 2021 JaCaMo paper} — no LLM content; Hägg 1997 = 137 citations, post-2023 citers {normative resilient MAS 2023, SARL exception handling 2023} — no LLM content.
- Tooling failures: S2 search endpoint (429 all session), OpenAlex (budget exhausted), arXiv API/UI (intermittent 429), DBLP (unreachable), preprints.org (bot wall), DataCite (functional but spam-flooded relevance).
