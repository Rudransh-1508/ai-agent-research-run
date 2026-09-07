# Survey D - Governance, Human-AI, Ops, Memory, Context, Environment
Target: AAMAS 2027 main track (abstract 1 Oct 2026, paper 8 Oct 2026). Date of survey: 2026-09-07.

## 0. Method note

The eight corpus files were fetched as **raw markdown via `curl`**, not through WebFetch's summarizer, so
the entry lists below are exhaustive rather than sampled. arXiv abstracts were pulled from the
**arXiv Atom API** (`export.arxiv.org/api/query`) and, where the API rate-limited (HTTP 429), from
`arxiv.org/abs/<id>` with an explicit "reproduce verbatim, do not paraphrase" instruction. Every
load-bearing claim below is backed by an abstract I actually read.

## 1. Coverage: entries enumerated per file

| File | Bullet entries | Unique arXiv links |
|---|---|---|
| [operations/governance.md](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/operations/governance.md) | 21 (2 exact duplicates: 2606.04306, 2607.22611) | 23 |
| [operations/human-ai.md](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/operations/human-ai.md) | 27 | 29 |
| [operations/agentops.md](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/operations/agentops.md) | 46 | 51 |
| [newsletters/aug_2026/governance_trends.md](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/newsletters/aug_2026/governance_trends.md) | prose newsletter, 7 papers covered | 7 |
| [capabilities/knowledge-context/memory.md](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/capabilities/knowledge-context/memory.md) | 128 (4 sections) | 142 |
| [capabilities/knowledge-context/context-engineering.md](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/capabilities/knowledge-context/context-engineering.md) | 38 | 40 |
| [capabilities/other/environment.md](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/capabilities/other/environment.md) | 41 | 45 |
| [applications/system/world-simulation.md](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/applications/system/world-simulation.md) | 57 | 66 |
| **Total** | **358 bullets + 1 newsletter** | **403 link slots** |

Two entries have no link at all ("Position: Agentic AI System Is a Foreseeable Pathway to AGI",
"DynamicMem", "Interactive Evaluation Requires a Design Science", "Evaluating Memory Condensation
Strategies for Coding Agents") - these are unresolvable from the corpus alone.

## 2. Territory map: saturated vs thin

### Saturated (heavily crowded with 2026 work - do not enter)

- **Agentic memory architectures and self-evolving memory.** memory.md alone carries 128 entries with
  ~65 from 2026 and **eight** surveys/taxonomies ([2602.06052](https://arxiv.org/abs/2602.06052),
  [2604.01707](https://arxiv.org/abs/2604.01707), [2602.05665](https://arxiv.org/abs/2602.05665),
  [2512.13564](https://arxiv.org/abs/2512.13564v1), [2606.30306](https://arxiv.org/abs/2606.30306), ...)
  plus a dense benchmark layer (EvoMemBench, MEMGYM, STALE, HaluMem, Harness-the-Memory). Any new
  "MemX: a better memory architecture" paper is DOA.
- **Context compression / long-horizon context management.** 38 entries, 2026-heavy (ACON, Context-Folding,
  AgentFold, PEEK, HyMem, Compaction Cliff). Engineering-saturated.
- **World models and environment synthesis.** 41 entries, of which ~28 are 2026; includes a survey
  ([2606.12191](https://arxiv.org/abs/2606.12191)) and multiple benchmark environments.
- **Governance frameworks / permissions / policy enforcement engineering.** Governance.md is dominated
  by 2026 architecture papers: Organizational Control Layer ([2606.04306](https://arxiv.org/abs/2606.04306)),
  Deontic Policies / AgenticRei ([2606.19464](https://arxiv.org/abs/2606.19464)), Dynamic Capability Scoping
  ([2607.22445](https://arxiv.org/abs/2607.22445)), Decentralized Granular Access Control
  ([2607.22611](https://arxiv.org/abs/2607.22611)), PolicyGuide ([2608.19861](https://arxiv.org/abs/2608.19861)),
  Governance by Construction ([2605.20874](https://arxiv.org/abs/2605.20874)).
  **All of it is centralized, top-down, non-strategic** - see §3.2.
- **Position papers on LLM social-simulation validity.** Already three: "LLM-Based Social Simulations
  Require a Boundary" ([2506.19806](https://arxiv.org/abs/2506.19806)), "Position: AI Agents Are Not (Yet)
  a Panacea for Social Simulation" ([2603.00113](https://arxiv.org/abs/2603.00113)), "We Need Strong
  Preconditions For Using Simulations In Policy" ([2604.07838](https://arxiv.org/abs/2604.07838)).
  A fourth position paper adds nothing; a *calibration method* would, but see §4 for feasibility.
- **Human-AI collaboration UX / empirical studies.** human-ai.md is HCI-dominant and most entries need
  human subjects (ViviDoc, MUSE, InterDeepResearch, TUX, interaction smells). IRB-infeasible for us.
- **Agentic markets and negotiation - filling fast in 2026.** Magentic Marketplace
  ([2510.25779](https://arxiv.org/abs/2510.25779)), Business Arena ([2608.08621](https://arxiv.org/abs/2608.08621)),
  FM-Bench ([2608.18423](https://arxiv.org/abs/2608.18423)), supply-chain bargaining with private
  information ([2608.07538](https://arxiv.org/abs/2608.07538)), CARP reputation-penalty mechanism
  ([2607.28330](https://arxiv.org/abs/2607.28330)).

### Thin (real negative space)

- Strategic / incentive treatment of **shared agent memory** (see §3.5) - **thinnest**.
- **Norms with sanctioning as an alternative enforcement regime** for operational agent policy (§3.2).
- **Incentive compatibility of oversight escalation** - theory exists without LLMs, empirics exist without
  incentives, nobody has joined them (§3.4).
- **Calibration methods** (not position papers) for LLM social simulation (§3.6).

## 3. AAMAS-native negative-space checks

### 3.1 Agent economies / agent-to-agent markets - **NOT empty; substantially occupied**

I expected this to be a gap. It is not. Verbatim evidence:

- [Virtual Agent Economies, 2509.10147](https://arxiv.org/abs/2509.10147) is still framework-level
  ("we consider auction mechanisms for fair resource allocation and preference resolution"), i.e. described,
  not analyzed. But:
- [When LLM Agents Negotiate, 2608.07538](https://arxiv.org/abs/2608.07538) does the real thing:
  "We benchmark nine LLMs ... against a validated Perfect Bayesian Equilibrium across 9,840 LLM-to-LLM
  negotiations" with a buyer holding **private demand information**, and finds "Delegation separates the
  principal's economic patience from the agent's prompted strategic patience". That is strategic
  misreporting + delegation contracts, done.
- [CARP, 2607.28330](https://arxiv.org/abs/2607.28330) is genuine mechanism design under unverifiable
  outcomes: "We design CARP, a reputation-penalty mechanism with a deadband ... CARP requires no
  product-level ground truth and is robust to strategic gaming", and critically establishes that the
  incentive is *behaviorally* binding for LLMs: "LLM merchants fabricate when lying is free but restrain
  themselves when fabrication costs them sales, a self-interested response rather than compliance."
- [LLM Economist, 2507.15815](https://arxiv.org/abs/2507.15815) already does mechanism design (Stackelberg
  tax-schedule design) over persona-conditioned LLM populations.

**Verdict: closed.** CARP's methodological template (design a mechanism, then show the incentive is
behaviorally binding on LLMs) is however the right *method* to import elsewhere.

### 3.2 Norms and institutions - **partially open, the interesting half**

Two literatures exist and **do not touch each other**:

(a) *Governance-as-static-guardrail* - the entire operations/governance.md list. Enforcement is always
centralized, exogenous, and applied to a single agent's action stream. AgenticRei
([2606.19464](https://arxiv.org/abs/2606.19464)) is the most expressive: obligations, dispensations,
meta-policy conflict resolution - but "evaluated at runtime by a high-performance logic engine entirely
outside the LLM". No sanctioning, no compliance dynamics, no population.

(b) *Emergent norms in LLM populations* - exists but on abstract social dilemmas:
[Emergence of Reputation-Based Cooperation in LLM Agents, 2608.04507](https://arxiv.org/abs/2608.04507)
(indirect-reciprocity donation game), [Emergent social conventions and collective bias in LLM populations,
Science Advances](https://www.science.org/doi/10.1126/sciadv.adu9368) (naming game),
[Adaptive Accountability in Networked MAS, 2512.18561](https://arxiv.org/abs/2512.18561),
[Democracy-in-Silico, 2508.19562](https://arxiv.org/abs/2508.19562) (institutional design as alignment,
with the Power-Preservation Index).

**Nobody runs a decentralized peer-sanctioning regime against a centralized guardrail on the same
operational policy-compliance task.** Search run: *"compare centralized guardrail enforcement versus
decentralized peer sanctioning LLM agents policy compliance enforcement cost utility tradeoff"* -
**returned nothing matching**; the results were all guardrail-architecture papers (SafeHarbor
[2605.05704](https://arxiv.org/abs/2605.05704), Provably Secure Agent Guardrail
[2605.29251](https://arxiv.org/abs/2605.29251)).

### 3.3 Interoperability protocols (MCP / A2A) - **closed as of Aug 2026**

I expected only engineering description (and the corpus supports that: "A Survey of AI Agent Protocols"
[2504.16736](https://arxiv.org/abs/2504.16736), Authenticated Delegation
[2501.09674](https://www.arxiv.org/abs/2501.09674), Autogenesis [2604.15034](https://arxiv.org/abs/2604.15034)).
But outside the corpus:
[Do LLM Agents Negotiate Rationally? A Mechanism-Design Framework for Verifiable Multi-Agent Interaction
over A2A/MCP, 2608.14613](https://arxiv.org/abs/2608.14613) encodes alternating-offers bargaining and
VCG-style auctions as constraints over A2A message schemas with a runtime verification layer.
**This candidate is dead.** Recorded as a killed candidate.

### 3.4 Human-agent teaming as a formal problem - **mostly closed in the last 3 months**

This was my strongest prior. It has been taken, twice, very recently:

- [Oversight Has a Capacity, 2606.08919](https://arxiv.org/abs/2606.08919): "Agent oversight, framed this
  way, is not only a classification problem but a resource-allocation one: human attention is finite, and
  the guard's escalation policy spends it." Models an endogenous fatiguing reviewer, finds "realized safety
  becomes an inverted-U in the escalation rate: more human oversight can make a system less safe". The
  authors explicitly disclaim mechanism novelty: "fatigue-aware learning-to-defer (FALCON), cost-sensitive
  deferral under workload constraints (DeCCaF) ... are all prior art we cite."
- [One Human, N Agents: Audit-Budget Allocation for LLM Agent Fleets, 2607.28317](https://arxiv.org/abs/2607.28317):
  "A single human must audit $N$ LLM agents under a budget of $B \ll N$ audits per round, guided by
  self-reported confidence that may be adversarially miscalibrated and by correlated errors. We model
  this as budgeted noisy inspection over a two-level Gaussian copula and locate the miscalibration
  threshold $\delta^*$..."

The corpus's own contribution here is weaker than these: "Intelligent AI Delegation"
([2602.11865](https://arxiv.org/abs/2602.11865)) is a **framework/position** paper ("we propose an adaptive
framework ... aiming to inform the development of protocols"), no formal model. "Observability for Delegated
Execution" ([2606.09692](https://arxiv.org/abs/2606.09692)) is a systems/forensics paper.

**What survives:** in 2607.28317 miscalibration is an *exogenous parameter* $\delta$; the agents are not
strategic players choosing a report in response to the audit rule. Making the audit-allocation rule
**incentive-compatible** is untouched empirically. The relevant theory is pure GT with no LLMs:
[The Endogeneity of Miscalibration: Impossibility and Escape in Scored Reporting, 2605.07671](https://arxiv.org/abs/2605.07671)
(cs.GT/cs.MA/econ.TH; confirmed **no LLM experiments**) and
[Honest Reporting in Scored Oversight, 2605.03793](https://arxiv.org/abs/2605.03793).

### 3.5 Shared memory as a commons - **genuinely open. Best gap found.**

Everything in the corpus and its neighbourhood treats contributors to a shared memory pool as
**cooperative by assumption**:

- [INMS / Memory Sharing, 2404.09982](https://arxiv.org/abs/2404.09982): "establishes a shared conversational
  memory pool ... promoting collective self-enhancement". Benevolent contributors.
- [Prism, 2604.19795](https://arxiv.org/abs/2604.19795): decision-theoretic, "replicator-decay dynamics
  ... proving convergence to an Evolutionary Stable Memory Set (ESMS)" - evolutionary *language*, but the
  fitness is memory confidence, not an agent's payoff; no strategic contributor.
- [TreeMem, 2605.04811](https://arxiv.org/abs/2605.04811): credit assignment across a builder-summarizer-
  retriever pipeline; cooperative-team credit, not incentive design.
- [Governed Shared Memory / MemClaw, 2606.24535](https://arxiv.org/abs/2606.24535): four failure modes
  "unauthorized leakage, stale propagation, contradiction persistence, and provenance collapse" - pure
  systems primitives, cs.AI, no incentives.
- [Governed Collaborative Memory as Artificial Selection, 2605.04264](https://arxiv.org/abs/2605.04264):
  cs.MA **Viewpoint** asking exactly "which candidate memories should become shared institutional state?"
  and framing governance as a *selection regime* - and it explicitly does **not** model strategic or
  self-interested agents. This is a standing invitation.
- [GateMem, 2606.18829](https://arxiv.org/abs/2606.18829): the closest thing - "multiple principals write
  to a common memory pool and query it under different roles, scopes, and relationships, so memory quality
  requires governance as well as recall". But its multi-principal-ness is about **access control, leakage,
  and deletion compliance**, not about principals having *conflicting incentives over what to contribute*.
- Degradation is studied only as *accident or attack*: [Useful Memories Become Faulty When Continuously
  Updated by LLMs, 2605.12978](https://arxiv.org/abs/2605.12978) (consolidation-induced regression -
  "GPT-5.4 fails on 54% of a set of ARC-AGI problems it had previously solved without memory"),
  [Memory Injection Attack, 2503.03704](https://arxiv.org/abs/2503.03704),
  [SSGM, 2603.11768](https://arxiv.org/abs/2603.11768), [Memory Worth, 2604.12007](https://arxiv.org/abs/2604.12007)
  (single-principal quality metric).
- Nearest incentive work is about *effort in a reasoning ensemble*, not a persistent pool:
  [MAC-SPGG, 2508.02076](https://arxiv.org/abs/2508.02076) - sequential public-goods game making effortful
  contribution the unique SPNE. No persistence, no pollution dynamics, no downstream retrieval harm.

Search run: *`all:"shared memory" AND all:"LLM agents" AND (free-riding OR incentive OR commons)`* -
**4 results, none on point** (only GateMem was relevant).

### 3.6 LLM agent-based social simulation validity - **discussed, not solved**

The corpus is honest about this. [Insurance as AI Risk Infrastructure, 2608.15181](https://arxiv.org/abs/2608.15181)
is used as governance evidence but rests on one LLM-driven ABM; the newsletter itself flags this as
"要追試" (needs replication) and notes the AI-Governance-in-Finance drawdown figure 39.2%->79.3% is a
"calibrated synthetic illustration". [Validating Generative ABMs for Logistics, 2508.20234](https://www.arxiv.org/abs/2508.20234)
and [On the limits of agency in agent-based models, 2409.10568](https://arxiv.org/abs/2409.10568) are the
only validation-oriented entries against 57 simulation papers. Three position papers say "we need
preconditions"; nobody supplies an operational calibration protocol. Real gap, but it is a
statistics/methodology contribution more than an AAMAS-mechanism contribution, and validating against real
human data is human-subjects-adjacent. Not carried forward as a top-3 candidate.

## 4. Candidate gaps

---

### Candidate D1 - The shared experience pool is a commons and nobody has priced it

**Gap statement.** No work models a persistent shared agent-memory / experience pool as a **common-pool
resource with strategic contributors** - deriving the free-riding and pollution equilibria and designing a
contribution mechanism - while also **measuring downstream task utility** of the resulting pool on real
LLM agents; existing work either builds cooperative shared-memory systems (INMS, Prism, MemClaw) or
governs a shared pool for *access control and deletion* (GateMem) with contributors assumed non-strategic.

**Why it matters.** Agent fleets are converging on exactly this architecture - ReasoningBank, AgentKB,
MemClaw, MATM, and every "self-evolving agent" paper writes distilled experience into a pool that other
agents read. The moment those agents belong to different principals (different teams, vendors, or
customers on a multi-tenant service - GateMem's own motivating deployments: "hospitals, workplaces,
campuses, and households"), contribution becomes a public good: writing a high-quality, honestly-labelled
memory is costly (tokens, exposure of proprietary method, risk of being blamed for a bad entry) while
reading is free. The predicted failure is not leakage but **quiet pool collapse**: everyone reads,
contributions become cheap/self-serving/uncurated, and 2605.12978 already shows a pool of low-quality
consolidations can drive agents *below the no-memory baseline*. Governance today has no lever for this -
access control does not make anyone contribute well.

**Falsifiable hypothesis.**
H1 (pollution): Under a neutral pool (unlimited read, uncredited write) with agents facing a per-token
cost for curation, LLM agents' contribution quality declines monotonically over rounds and the pool's
downstream utility crosses below a no-sharing baseline within a bounded number of rounds.
H2 (mechanism): A contribution mechanism that conditions *read access* on a retrieval-outcome-based
contribution score (a "memory worth"-style two-counter signal, cf. 2604.12007, used as a *currency*
rather than a filter) restores pool utility to within X% of the fully-cooperative oracle pool, and the
incentive is **behaviorally binding** on LLM agents in CARP's sense - agents curate when curation is
rewarded, not merely when instructed to.
H3 (the sharp, killable one): honest-effort contribution is *not* a Nash equilibrium of the neutral pool
but *is* under the mechanism, and LLM agents' observed behaviour tracks the equilibrium prediction rather
than their prompted instruction.

**Decisive experiment.** N agents (N = 8-24), heterogeneous task streams drawn from a shared distribution
(so memories are cross-usefully transferable), a persistent pool, T = 30-60 rounds. Each round an agent
solves a task, chooses a costly curation effort level for the memory it writes, and retrieves k memories.
Conditions: (i) no pool, (ii) neutral pool, (iii) neutral pool + honesty instruction, (iv) access-priced
pool (mechanism), (v) oracle pool (human/LLM-curated, upper bound). Primary outcome: task success over
rounds; secondary: measured contribution quality, Gini of read/write ratio, and the *pollution rate*
(fraction of retrieved memories that lower success in a counterfactual ablation). The falsifier for H3:
if condition (iii) alone matches (iv), the incentive story is unnecessary and the paper dies.

**AAMAS fit.** Excellent, and multi-area: *Economic paradigms / mechanism design*, *Norms, institutions
and social dilemmas*, *Learning and adaptation*, *Engineering multiagent systems*. It reads as a public
goods problem, which is AAMAS's home turf, applied to the object the LLM-agent field currently cares most
about.

**4-week feasibility: HIGH.** No human subjects, no IRB. Pure LLM API calls plus a small memory store.
Cost estimate: 20 agents x 50 rounds x 5 conditions x ~4 calls = ~20k calls; with a mid-tier model this
is low-hundreds of dollars. The theory half (a public-goods game with a quality-degrading pool and an
access-pricing mechanism) is a whiteboard-and-simulation exercise, and can be checked against a cheap
numerical agent-based simulation before any LLM is called - so weeks 1-2 are theory + simulated agents,
week 3 is the LLM instantiation, week 4 is ablations. Main risk: making the pool's utility *measurably*
degrade requires a task family where memory actually helps; use a domain with known memory lift
(ALFWorld/WebArena-style, or the ARC-AGI Stream setup from 2605.12978, which is already published as a
controlled environment exposing Retain/Delete/Consolidate).

**Occupancy check (adversarial).**
1. [GateMem, 2606.18829](https://arxiv.org/abs/2606.18829) - multi-principal shared memory benchmark.
   **Does NOT**: model contributors as strategic, have any notion of contribution cost or free-riding,
   or design a mechanism. Its axes are utility / access control / forgetting compliance.
2. [Governed Shared Memory (MemClaw), 2606.24535](https://arxiv.org/abs/2606.24535) - production
   fleet-memory service. **Does NOT**: contain agents with payoffs; its failure modes are engineering
   (leakage, staleness, contradiction, provenance collapse), and it explicitly runs "rather than a
   baseline comparison ... a live production service".
3. [Governed Collaborative Memory as Artificial Selection, 2605.04264](https://arxiv.org/abs/2605.04264) -
   cs.MA Viewpoint framing memory governance as a selection regime. **Does NOT**: model self-interested
   agents or incentive mechanisms (confirmed), run experiments, or give a formal game. It poses the
   question this candidate answers.
4. [MAC-SPGG, 2508.02076](https://arxiv.org/abs/2508.02076) - sequential public-goods game for multi-LLM
   cooperation. **Does NOT**: involve any persistent artifact; contribution is per-task reasoning effort
   in a one-shot ensemble, so there is no pool quality that degrades, no retrieval, no cross-round
   externality, and no read/write asymmetry.
5. [Useful Memories Become Faulty, 2605.12978](https://arxiv.org/abs/2605.12978) - pool degradation.
   **Does NOT**: have multiple agents or any incentive; degradation is attributed to the LLM consolidation
   step in a single-agent loop.

**Residual risk.** Someone at NeurIPS/ICLR 2026 may be running the same public-goods framing right now;
the 2605.04264 viewpoint (May 2026) shows the idea is in the air. Mitigation: lead with the *mechanism*
and the equilibrium result, not with the observation that pools degrade (which is already published).

---

### Candidate D2 - Sanctioning as an enforcement regime for operational agent policy

**Gap statement.** No work evaluates **decentralized peer sanctioning with emergent compliance** as an
enforcement regime for a *concrete operational agent policy* (the kind PolicyGuide/AgenticRei compile
into guardrails) while also **measuring the enforcement-cost / task-utility frontier** against a
centralized verifier baseline; the governance literature only builds centralized enforcers and the
norm-emergence literature only studies abstract social dilemmas.

**Why it matters.** The corpus's own August-2026 newsletter names the problem: the "verifier tax" -
blocking 94% of unsafe actions can drop safe task completion below 5%, because the agent routes around
the guard - and states outright that whether workflow-level enforcement escapes this trap
"は検証されていない" (has not been verified). Centralized enforcement also scales badly: every action
crosses a policy engine, and 2606.08919 shows the human end of that pipeline has finite capacity.
Normative MAS has a 25-year answer to exactly this - distribute enforcement into the population via
sanctions - and it has never been tried on LLM agents doing real policy-bound work. The interesting
possibility is a *hybrid*: a cheap centralized floor plus peer sanctioning that adapts to policy the
designer never wrote down.

**Falsifiable hypothesis.**
H1: On a policy-bound task suite, a peer-sanctioning regime (agents observe peers' action traces, may
pay a cost to sanction, sanctions affect a reputation that gates future collaboration) achieves a
compliance/utility point **not dominated** by any operating point of a centralized verifier with a tunable
strictness knob - i.e. it is on a different Pareto frontier, not a worse point on the same one.
H2: Compliance under sanctioning **generalizes to policy clauses not present at design time** (held-out
clauses), where the compiled centralized verifier is by construction blind.
H3 (killable): sanctioning's advantage disappears when enforcement cost is charged at parity - if peer
sanctioning costs more LLM calls than it saves, it is an academic curiosity.

**Decisive experiment.** Use an existing policy-compliance environment with a real policy document -
tau^2-bench domains (airline/retail/telecom) as used by PolicyGuide, or ReguSim's financial compliance
setting ([2608.19974](https://arxiv.org/abs/2608.19974), which already separates stated reasoning,
attempted action, enforcement, and monitoring evidence). Populate it with a population of agents that
repeatedly interact and can observe one another. Regimes: (a) no enforcement, (b) centralized action-level
guard at several strictness levels, (c) centralized workflow-level guard (PolicyGuide-style), (d) peer
sanctioning only, (e) hybrid. Measure: policy violation rate, task success (Pass^k), *enforcement cost in
LLM calls/tokens*, and held-out-clause compliance. Falsifier: if (d)/(e) sit strictly inside the (b)/(c)
frontier on both violation rate and success at equal cost, the hypothesis is refuted.

**AAMAS fit.** Very strong and squarely AAMAS-native: *Norms, institutions, sanctioning and social
dilemmas*; secondary *Engineering multiagent systems* and *Trust and reputation*.

**4-week feasibility: MEDIUM-HIGH.** No human subjects. The cost driver is that sanctioning requires a
*population* and *repeated interaction*, so the call count is population x rounds x regimes and grows fast;
and tau^2-bench-style environments are episodic and single-agent by construction, so a real chunk of week
1-2 goes into making a repeated multi-agent wrapper where agents actually see each other's traces. That
engineering risk is the reason this is not HIGH. Mitigation: run the pilot in one domain (telecom, the
most structured, where PolicyGuide showed the largest effect 0.19->0.61) with a small population (6-10),
and treat the second and third domains as stretch.

**Occupancy check (adversarial).**
1. [PolicyGuide, 2608.19861](https://arxiv.org/abs/2608.19861) - compiles policy into a workflow graph
   with a proactive verifier at user-turn boundaries. **Does NOT**: have a population, peers, sanctions,
   emergent compliance, or any enforcement-cost accounting; enforcement is fully centralized and the
   policy must be known and compilable in advance.
2. [Deontic Policies / AgenticRei, 2606.19464](https://arxiv.org/abs/2606.19464) - obligations,
   dispensations, conflict resolution in OWL. **Does NOT**: study whether agents comply, or how compliance
   emerges; the logic engine runs "entirely outside the LLM" and compliance is enforced, not learned.
3. [Emergence of Reputation-Based Cooperation in LLM Agents, 2608.04507](https://arxiv.org/abs/2608.04507)
   and [Emergent social conventions in LLM populations, Sci. Adv.](https://www.science.org/doi/10.1126/sciadv.adu9368)
   - norm/convention emergence in LLM populations. **Do NOT**: involve any externally specified operational
   policy, task utility, or enforcement cost; the environments are donation games and naming games with no
   notion of a policy document to comply with.
4. [Democracy-in-Silico, 2508.19562](https://arxiv.org/abs/2508.19562) - institutional design as alignment,
   with a Power-Preservation Index. **Does NOT**: compare against a centralized runtime guardrail, measure
   task utility on a compliance benchmark, or account for enforcement cost; institutions are deliberation
   and voting protocols, not sanctioning of policy violations.
5. [Adaptive Accountability in Networked MAS, 2512.18561](https://arxiv.org/abs/2512.18561) - tracing and
   mitigating *emergent* norms. **Does NOT** (from title/scope): treat emergent norms as an enforcement
   instrument for designer-specified policy; it treats them as something to trace and mitigate.

**Negative search recorded:** no paper found comparing centralized guardrails to decentralized peer
sanctioning for LLM agent policy compliance with a cost-utility tradeoff.

---

### Candidate D3 - Incentive-compatible escalation when human oversight is the scarce common resource

**Gap statement.** No work makes the **allocation of a scarce human-audit budget across a fleet of LLM
agents incentive-compatible** - designing a scoring/pricing rule under which an agent's best response is
to truthfully reveal its own risk, and testing whether that incentive is behaviorally binding on real LLM
agents - while also **modeling the agents as competing for the same congested reviewer**; existing fleet
work treats miscalibration as an exogenous parameter, and the matching scored-elicitation theory contains
no LLMs.

**Why it matters.** Escalation is about to become a strategic action. An agent that escalates gets a free
correctness check and offloads blame; an agent that escalates less finishes faster. With one reviewer and
N agents, escalation is a congestion externality, and 2606.08919 shows the pathology empirically -
"realized safety becomes an inverted-U in the escalation rate: more human oversight can make a system
less safe" - plus a flooding attack that exploits exactly this. 2607.28317 then shows the ranking signal
is already broken: "Five open-weight LLMs show operationally useless (near-constant) confidence". Fixing
this by better estimating confidence is a losing race; making truthful reporting the agent's best response
is the mechanism-design answer, and it has never been instantiated on LLM agents.

**Falsifiable hypothesis.**
H1: Under a fixed audit budget with confidence-ranked auditing, self-interested LLM agents (rewarded for
task throughput, penalized for caught violations) learn/adopt strategic under-reporting of risk, degrading
fleet safety below the random-audit baseline - i.e. 2607.28317's exogenous $\delta$ arises **endogenously**
from ordinary deployment incentives without any adversary.
H2: A reserve-report / kinked-approval mechanism in the family characterized by
[2605.07671](https://arxiv.org/abs/2605.07671) ("A Lipschitz rule with one kink achieves optimal outcomes,
though no smooth rule can under strict feasibility") restores separation between high- and low-risk agents
and lifts realized safety at fixed budget.
H3 (killable, and the paper's real content): the *kink* matters behaviorally for LLM agents - a smooth
proper-scoring rule fails where the kinked rule succeeds, as theory predicts. If LLMs respond identically
to both, the theory does not transfer and the result is a negative one worth reporting.

**Decisive experiment.** Fleet of N = 30-100 LLM agents on a task suite with objectively checkable
violations (unsafe shell/file/API actions; reuse 2606.08919's public agent-oversight system and its 125
hand-labeled adversarially-weighted actions as a seed). Each round: agents act, self-report a risk score,
a budget B << N of audits is allocated by the rule under test, audited violations are penalized, unaudited
violations land. Rules compared: random, confidence-ranked (2607.28317 baseline), smooth strictly-proper
scoring, kinked reserve-report mechanism. Payoffs made explicit in the agent's prompt and made real
through repeated-round accounting (CARP's "byte-clean code-gated reflection" is the template for making
the penalty felt rather than instructed). Primary: realized violation rate at fixed B. Secondary:
report-truthfulness (correlation of report with realized risk) and separation between agent types.

**AAMAS fit.** Strong: *Economic paradigms - mechanism design, incentive compatibility*; secondary
*Human-agent interaction* and *Trust, safety and assurance*. Note the theory anchor 2605.07671 is already
cross-listed cs.MA.

**4-week feasibility: MEDIUM.** No human subjects - crucially, the human reviewer is **simulated**, exactly
as 2606.08919 does ("The inverted-U and the flooding attack are modeling results that motivate a human
study"), which keeps us out of IRB territory but is also the honest limitation to state. Feasible because
the mechanism is one scoring function and the fleet is cheap (a round is one action + one scalar report
per agent). The medium rating is about *scientific* risk, not compute: H3 requires LLM agents to be
sensitive enough to a numeric penalty structure to distinguish a smooth from a kinked rule, and they may
simply not be - in which case the paper becomes a negative result. Budget week 1 to a pure-simulation
replication of the theory, week 2 to a pilot on a small fleet checking whether *any* incentive response
is detectable (go/no-go gate), weeks 3-4 to the full comparison.

**Occupancy check (adversarial).**
1. [One Human, N Agents, 2607.28317](https://arxiv.org/abs/2607.28317) - budgeted noisy inspection over a
   Gaussian copula, miscalibration threshold $\delta^*$. **Does NOT**: design a mechanism, model agents as
   players with payoffs, or let the reporting policy respond to the audit rule; $\delta$ is a dial the
   experimenter turns, and the contribution is a *criterion for vacuous oversight*, not a fix.
2. [Oversight Has a Capacity, 2606.08919](https://arxiv.org/abs/2606.08919) - oversight as resource
   allocation with a fatiguing reviewer. **Does NOT**: have multiple agents competing for the reviewer,
   any incentive-compatibility notion, or a strategic agent - the action stream is exogenous and the
   authors explicitly disclaim mechanism novelty relative to FALCON/DeCCaF.
3. [The Endogeneity of Miscalibration, 2605.07671](https://arxiv.org/abs/2605.07671) - the exact theory
   (reserve report, kinked Lipschitz rule, closed-form critical slope for Brier/log/power scores).
   **Does NOT**: involve LLMs at all (confirmed), have any audit-budget/congestion structure, or test
   whether the mechanism binds behaviorally on a language model. It names "AI oversight" only as an
   application.
4. [CARP, 2607.28330](https://arxiv.org/abs/2607.28330) - mechanism design under unverifiable outcomes
   with LLM agents, and the source of the "behaviorally binding" method. **Does NOT**: concern oversight,
   audits, human attention, or a scarce shared reviewer; its setting is a consumer marketplace with
   complaint signals, and its scarce quantity is sales, not audit capacity.

**Residual risk (state honestly).** This is the most derivative of the three - it is 2607.28317's setting
plus 2605.07671's mechanism plus CARP's validation method. Its defensibility rests entirely on H3 being a
real, surprising empirical question. Rank it third.

---

## 5. Killed candidates (recorded)

- **"Interoperability protocols have no game-theoretic analysis"** - killed by
  [2608.14613](https://arxiv.org/abs/2608.14613) (Aug 2026, VCG/alternating-offers encoded over A2A schemas).
- **"Agent-to-agent markets are described, not analyzed with mechanism design"** - killed by
  [CARP 2607.28330](https://arxiv.org/abs/2607.28330), [2608.07538](https://arxiv.org/abs/2608.07538)
  (PBE-referenced, private information), [LLM Economist 2507.15815](https://arxiv.org/abs/2507.15815).
- **"Human oversight allocation is not modeled as a decision/control problem"** - killed by
  [2606.08919](https://arxiv.org/abs/2606.08919) and [2607.28317](https://arxiv.org/abs/2607.28317).
  Survives only in the incentive-compatible form (D3).
- **"A fourth position paper on social-simulation validity"** - saturated; see §3.6.

## 6. Searches that returned nothing useful (recorded)

- arXiv API `all:"shared memory" AND all:"LLM agents" AND (all:"free-riding" OR all:"incentive" OR all:"commons")` - 4 hits, only GateMem relevant.
- arXiv API `abs:"experience pool" AND abs:agent` - 15 hits, all cooperative RL/self-evolution, none on incentives.
- Web: "compare centralized guardrail enforcement versus decentralized peer sanctioning LLM agents policy compliance enforcement cost utility tradeoff" - no matching paper.
- arXiv API `abs:"learning to defer" AND abs:"LLM"` and `abs:"escalation policy" AND abs:agent AND abs:human` - both blocked by HTTP 429 rate limiting; substituted with web search over arxiv.org, which surfaced 2606.08919 and 2607.28317.

## 7. Recommendation

**D1 (shared memory as a commons)** is the pick: thinnest negative space, an explicit standing invitation
in a cs.MA viewpoint ([2605.04264](https://arxiv.org/abs/2605.04264)), the highest 4-week feasibility, and
it converts the field's most saturated topic (agent memory) into an AAMAS-native mechanism-design question
rather than competing inside it. **D2** is the best pure-AAMAS fit if the multi-agent wrapper engineering
can be absorbed. **D3** is a fallback with real occupancy pressure on three sides.
