# Survey C — Learning, Adaptation, Self-Evolution, Planning
Corpus slice traversal for an AAMAS 2027 main-track gap hunt. Compiled 2026-09-07.

Method note: all eight assigned files were fetched as **raw markdown via `curl`**, not via WebFetch's
summarizer, so every entry count below is a direct `grep` over the actual file bytes rather than an
LLM summary. Every paper claim in this document was verified by fetching `arxiv.org/abs/<id>` and
extracting the `<blockquote class="abstract">` element; quotes are literal. Where a corpus title
disagreed with the arXiv title I flag it.

---

## 0. Coverage stats (enumerated, not sampled)

| File | Bullet entries | arXiv links | Unique arXiv IDs |
|---|---|---|---|
| [`capabilities/adaptation/learning.md`](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/capabilities/adaptation/learning.md) | 122 | 121 | 120 |
| [`capabilities/adaptation/self-evolution.md`](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/capabilities/adaptation/self-evolution.md) | 180 | 175 | 175 |
| [`capabilities/adaptation/experience.md`](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/capabilities/adaptation/experience.md) | 27 | 24 | 21 |
| [`capabilities/adaptation/exploration.md`](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/capabilities/adaptation/exploration.md) | 18 | 18 | 18 |
| [`capabilities/core-cognition/planning.md`](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/capabilities/core-cognition/planning.md) | 49 | 48 | 48 |
| [`newsletters/aug_2026/learning_trends.md`](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/newsletters/aug_2026/learning_trends.md) | prose (8 papers reviewed) | 10 | 7 |
| [`newsletters/aug_2026/self_evolution_trends.md`](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/newsletters/aug_2026/self_evolution_trends.md) | prose (14 papers reviewed) | 14 | 11 |
| [`newsletters/jul_2026/self_evolution_trends.md`](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/newsletters/jul_2026/self_evolution_trends.md) | prose (7 papers reviewed) | 11 | 7 |

**Totals: 396 bullet entries, 421 arXiv links, ~382 unique IDs enumerated.** Of the two large
capability files, **76 of 175** self-evolution entries and **40 of 120** learning entries carry a
2026 date — this slice is dominated by the last nine months.

Sections in the two big files (all read): `learning.md` = *Agent Tuning* + *Agentic RL*;
`self-evolution.md` = main list + *Recursive Self-Improvement (RSI) & Gödel Machines* +
*Reflection & Self-Refinement* + *Workflow & Prompt Optimization*.

**Corpus errors found while cross-checking against arXiv** (worth reporting upstream):
- `2602.04837` appears twice with two different titles — as *"Group-Evolving Agents: Open-Ended
  Self-Improvement via Experience Sharing"* in `exploration.md` and as *"Scaling Small Agents Through
  Strategy Auctions"* in `learning.md`. arXiv confirms the former is correct
  ([2602.04837](https://arxiv.org/abs/2602.04837)).
- `2512.04988` is listed as *"Strategic Self-Improvement for Competitive Agents in AI Labour
  Markets"*; the real title is *"When AI Agents Compete for Jobs: Strategic Capabilities and
  Economic Dynamics of AI Labour Markets"* ([2512.04988](https://arxiv.org/abs/2512.04988)).
- `2605.22148` is listed as *"Ratchet: A Minimal Hygiene Recipe for Self-Evolving LLM Agents"*; the
  real title is *"Ratchet: How Reliable Must an LLM Judge Be to Retire a Skill?"*
  ([2605.22148](https://arxiv.org/abs/2605.22148)).
- `experience.md` has 3 exact duplicate pairs (`2510.16079`, `2512.10696`, `2603.10600`).

---

## 1. Map of the territory

### Saturated (crowded, many 2026 entries, marginal returns)

1. **Prompt / workflow / agentic-system optimization.** 18 entries in the *Workflow & Prompt
   Optimization* section alone, from [AFlow](https://arxiv.org/abs/2410.10762) and
   [GEPA](https://arxiv.org/abs/2507.19457) through
   [CAPO](https://arxiv.org/abs/2608.16068). The Aug-2026 newsletter's own framing
   ([OEO](https://arxiv.org/abs/2608.09629)) is that prescribed pipelines are now merely "a
   capability-dependent scaffold". Nothing left here for a novel AAMAS contribution.
2. **Experience banks / memory-as-the-improvement-substrate for a single agent.** ~21 entries in
   `experience.md` plus a large slice of `self-evolution.md`
   ([ReasoningBank](https://arxiv.org/abs/2509.25140),
   [Tree-of-Experience](https://arxiv.org/abs/2608.09044),
   [CoEvo-Mem](https://arxiv.org/abs/2608.01739),
   [Knowledge-Centric](https://arxiv.org/abs/2607.19592),
   [MemEvolve](https://arxiv.org/abs/2512.18746v1),
   [EVOLVEMEM](https://arxiv.org/abs/2605.13941)). Method-level contributions here are commodity.
3. **Evolutionary program/agent search.** AlphaEvolve lineage,
   [ShinkaEvolve](https://arxiv.org/abs/2509.19349),
   [OpenEvolve/GigaEvo](https://arxiv.org/abs/2511.17592v1),
   [Darwin Gödel Machine](https://arxiv.org/abs/2505.22954),
   [Mendel Gödel Machine](https://arxiv.org/abs/2608.07645),
   [Meta^n](https://arxiv.org/abs/2608.24735). Well-populated and compute-hungry.
4. **Agentic RL infrastructure & environment scaling.** 30+ entries;
   [SPADE](https://arxiv.org/abs/2608.19197),
   [Agent Lightning v1.0](https://arxiv.org/abs/2608.17528),
   [Polar](https://arxiv.org/abs/2605.24220). Infeasible on a 4-week budget anyway.
5. **Self-evolution benchmarks.** [SEA-Eval](https://arxiv.org/abs/2604.08988),
   [SEAGym](https://arxiv.org/abs/2606.17546), [EvoMemBench](https://arxiv.org/abs/2605.18421),
   [AgentStream](https://arxiv.org/abs/2608.00155), [AI4AI-Bench](https://arxiv.org/abs/2608.20318),
   [RSIBench-Data](https://arxiv.org/abs/2607.25886),
   [Frontier-Eng](https://arxiv.org/abs/2604.12290). A "yet another benchmark" paper will not stand out.
6. **Multi-agent credit assignment for LLM teams.** *This was on the brief as an under-explored
   intersection. It is not — it has become crowded in 2026, see §3.2.*

### Thin

- **Populations (n ≫ 4) of self-evolving agents analysed as a population.** Almost every
  "multi-agent self-evolution" paper uses 2–8 agents and reports accuracy.
- **Endogenous non-stationarity** — agents whose environment is other *evolving* agents. Zero papers found.
- **Provenance / staleness / contamination of a shared experience pool by *non-adversarial* error.**
- **Self-evolving agents as strategic contributors** to a shared knowledge commons.
- **Planning under self-evolution.** `planning.md` is small (48 entries) and almost entirely
  single-agent; the newest entries ([Plans Don't Persist](https://arxiv.org/abs/2605.21902),
  [From Plan to Action](https://arxiv.org/abs/2604.12147)) are about plan-following fidelity, not
  multi-agent replanning under drift.

### The single strongest cross-paper finding in this slice

Three independent Aug-2026 papers converge on the same diagnosis: **self-improvement operates at the
execution layer and never reaches the strategy layer.** From the newsletter, verified against the
primary sources:

- [AI4AI-Bench](https://arxiv.org/abs/2608.20318): mean score 0.166 across 6 systems × 29 configs ×
  10 tasks, where 0.1 = the implementation the repo already ships and 1.0 = task optimum; **141 of
  263 submissions never touched the learning procedure at all.**
- [What is Missing from AI Post-Training AI](https://arxiv.org/abs/2608.19072): across 1,338
  trajectories, **strategy changes occur in only 2.1% of adjacent experiment pairs**; 80.7% of Claude
  Code trajectories lock onto full-parameter SFT, 89.6% of Codex CLI onto PEFT. Providing experience,
  human guidance, or extra inference compute each fails to unstick the strategy layer.
- The newsletter's own open-problem #1 states it plainly: *"「戦略を再評価する仕組み」をどう作るのか。…
  処方はまだない"* — "how do we build a mechanism that re-evaluates strategy? … there is still no
  prescription."

This is the field's loudest stated open problem. It is, however, **a single-agent
metacognition problem**, it is being attacked by three well-resourced groups, and the decisive
experiments require training runs. I did not build a candidate on it. It does, however, motivate C3
below: a population is the cheapest known mechanism for escaping a strategy-layer local optimum, and
nobody has framed it that way.

---

## 2. Stated open problems, quoted

Verified verbatim from arXiv abstracts (fetched HTML, `<blockquote class="abstract">`).

**[Credit Without Ground Truth (2608.19760)](https://arxiv.org/abs/2608.19760)** — scope limit is
stated in the first clause:
> "Audited against policy-conditional ground truth from executed replay **in a single-agent tool
> environment (ALFWorld)**, none of the step-level credit signals we audit -- LLM-judge scores,
> outcome-conditioned logprob ratios, or the policy's own confidence -- shows reliable incremental
> fidelity beyond its own marginal-matched shuffled control."

**[DecentMem (2605.22721)](https://arxiv.org/abs/2605.22721)** — asserts the phenomenon C1 targets,
without measuring it:
> "existing designs almost exclusively adopt a centralized repository shared across agents, incurring
> communication and coordination overhead, raising privacy concerns, and **collapsing agent
> diversity**."

**[GLOVE (2601.19249)](https://arxiv.org/abs/2601.19249)** — names the drift problem but scopes it
to exogenous change:
> "Most existing memory-enhanced LLM approaches implicitly assume that memory validity can be
> established either through external evaluators … or through internal model cognition … **these
> assumptions often break down in practical environments with dynamic drifts.**"
Its drifts are "interface updates, rule modifications, or altered configurations" — all exogenous.

**[Safety in Self-Evolving LLM Agent Systems (2606.23075)](https://arxiv.org/abs/2606.23075)** —
names population propagation as the threat but delivers a taxonomy, not dynamics:
> "adversarial influences become permanently encoded, self-amplify across generations, and
> **propagate through populations without sustained attacker access**." … "17 [of 25 cells] face
> critical threats for which no effective partial mitigation."

**[Evolving Deception (2603.05872)](https://arxiv.org/abs/2603.05872)** — the closest thing to
evolutionary-game analysis of self-evolution:
> "under utility-driven competition, unconstrained self-evolution reliably drifts toward deceptive
> behaviors, even when honest strategies remain viable. This drift is explained by a fundamental
> asymmetry in generalization."

**[Evaluating Collective Behaviour of Hundreds of LLM Agents (2602.16662)](https://arxiv.org/abs/2602.16662)**:
> "**cultural evolution converges to low-welfare, Selfish-dominant equilibria in larger groups.**"

**[Ratchet (2605.22148)](https://arxiv.org/abs/2605.22148)** — the sharpest existing theory on skill-pool hygiene:
> "a judge scoring failures as passes at rate $(1-\tau)/2$ or above **retires nothing, at any sample
> size**, for eviction margin $\tau$. … LLM-written skills are worth $+0.0$ percentage points (pp)
> against a no-skill control, human-written ones $+16.2$pp. Unmaintained, a library enters *library
> drift*, growing until injecting a skill scores worse than injecting nothing."

**[Aug-2026 self-evolution newsletter, 論点・未解決課題](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/newsletters/aug_2026/self_evolution_trends.md)**, item 4:
> "本番の数字と研究環境の数字が接続していない … 自己進化の「効果」を横断的に語る共通の尺度がないままだ。"
> ("Production numbers and research numbers are disconnected … there is still no common scale for
> talking about the *effect* of self-evolution across settings.")

**[Aug-2026 learning newsletter](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/newsletters/aug_2026/learning_trends.md)**, item 3:
> "報酬の粒度をどう決めるか。CRISP は「証拠を集めたか」で手を分類し、Credit Without Ground Truth は
> 「実際に結果を変えたか」で分類する。**両者が同じ手を選ぶのかは検証されていない。**"

---

## 3. Negative space against AAMAS-native concerns

I checked each of the five intersections on the brief. Two are genuinely thin, one is thin in a
narrower form than the brief supposed, and **two turned out to be occupied**.

### 3.1 Populations of self-evolving agents — THIN, but partially pre-empted

What exists:
- [Group-Evolving Agents (GEA), 2602.04837](https://arxiv.org/abs/2602.04837) — "treats a group of
  agents as the fundamental evolutionary unit, enabling explicit experience sharing and reuse within
  the group". Reports SWE-bench Verified 71.0% vs 56.7%. Its diversity analysis runs the *opposite*
  direction from the risk: it claims GEA "more effectively converts early-stage exploratory diversity
  into sustained, long-term progress". Diversity is treated as fuel to be consumed, never as
  something whose destruction is a failure mode.
- [Meta-Team, 2605.29790](https://arxiv.org/abs/2605.29790) ("Evolve as a Team") — MAS evolution at
  behaviour / coordination / organization scales; accuracy on six benchmarks.
- [Prism, 2604.19795](https://arxiv.org/abs/2604.19795) — the only paper in the slice with genuine
  population-dynamics machinery: "a *replicator-decay dynamics* framework that interprets memory
  confidence as evolutionary fitness, proving convergence to an **Evolutionary Stable Memory Set
  (ESMS)**", plus "a causal memory graph … with interventional edges and **agent-attributed
  provenance**". But: the replicator dynamics are over *memory items*, not over agents; the
  experiment is 4 agents; and nothing measures whether agent behaviour homogenises.
- [DecentMem, 2605.22721](https://arxiv.org/abs/2605.22721) — **states** that centralized shared
  memory collapses agent diversity, then measures only accuracy and token usage. Its theory is
  $O(\log T)$ bandit regret, not population dynamics.
- [Diversity Collapse in Multi-Agent LLM Systems, 2604.18005](https://arxiv.org/abs/2604.18005) —
  measures diversity collapse properly, including that "dense communication topologies accelerate
  premature convergence". But this is **one-shot ideation with no persistent memory and no evolution
  across episodes**; the coupling channel is live conversation, not a written experience pool.
- [Representational Collapse in Multi-Agent LLM Committees, 2604.03809](https://arxiv.org/abs/2604.03809)
  — single-round committee, embedding-space effective rank 2.17/3.0.
- [Evaluating Collective Behaviour of Hundreds of LLM Agents, 2602.16662](https://arxiv.org/abs/2602.16662)
  — the most AAMAS-native population paper in the slice: hundreds of agents, payoff-biased imitation,
  cultural evolution to "low-welfare, Selfish-dominant equilibria". But agents are *frozen code
  strategies* being imitated; there is no self-evolution loop, no experience memory, and the task is
  a social dilemma, not a capability task.

**Verdict:** nobody measures diversity *as a trajectory across evolution rounds* in a population of
self-evolving agents, as a function of the sharing mechanism, and nobody has a dynamical model that
predicts when it happens. Pre-empted enough that a pure "we measured collapse" paper is risky; the
contribution has to be the control parameter + design rule.

### 3.2 Multi-agent credit assignment — OCCUPIED. Candidate killed.

The brief flagged this as under-explored. It is not. Enumerated from arXiv API search
`abs:"credit assignment" AND abs:"LLM" AND abs:"multi-agent"` and `abs:"Shapley" AND abs:"LLM" AND
abs:"multi-agent"`:

- [SHARP, 2602.08335](https://arxiv.org/abs/2602.08335) — Shapley-based hierarchical attribution.
- [Shapley-Coop, 2506.07388](https://arxiv.org/abs/2506.07388) — Shapley CoT + negotiated pricing for self-interested LLM agents.
- [Agents that Matter, 2605.27621](https://arxiv.org/abs/2605.27621) — formalises attribution as a
  cooperative game parameterised by coalition distribution / removal protocol / target metric; shows
  LOO ≈ combinatorial, and that "introspective LLM judges fail to faithfully approximate this behavior".
- [Unifying Temporal and Structural Credit Assignment, 2605.30227](https://arxiv.org/abs/2605.30227)
- [CANTANTE, 2605.13295](https://arxiv.org/abs/2605.13295); [LEMON, 2605.14483](https://arxiv.org/abs/2605.14483);
  [Tree-based Credit Assignment for Multi-Agent Memory, 2605.04811](https://arxiv.org/abs/2605.04811);
  [Who Gets the Reward & Who Gets the Blame?, 2511.10687](https://arxiv.org/abs/2511.10687);
  [HiveMind, 2512.06432](https://arxiv.org/abs/2512.06432);
  [OrchRM, 2606.13598](https://arxiv.org/abs/2606.13598);
  [Semantic Cooperative Games, 2607.18255](https://arxiv.org/abs/2607.18255);
  [MASkills, 2609.02094](https://arxiv.org/abs/2609.02094).

My fallback idea — *"audit MAS credit attribution against executed-replay counterfactual ground
truth, as [Credit Without Ground Truth](https://arxiv.org/abs/2608.19760) did for the single-agent
case"* — is also occupied:
- [Causal Agent Replay (CAR), 2606.08275](https://arxiv.org/abs/2606.08275) — "models an agent run as
  a structural causal model, applies a do-operation to a step, and **re-executes the trajectory
  forward under the same stochastic policy**", with a Monte-Carlo Shapley estimator and validation
  against planted synthetic ground truth.
- [CCPO/SEPO, 2603.21563](https://arxiv.org/abs/2603.21563) — agent-removal counterfactual credit.
- [COSAC, 2604.17693](https://arxiv.org/pdf/2604.17693) — counterfactual credit in sequential
  cooperative teams.

**I am recording this as a killed candidate, not a gap.**

### 3.3 Shared / collective memory contamination — THIN in the non-adversarial direction only

Adversarial side is well covered:
- [EvoBreak, 2608.01759](https://arxiv.org/abs/2608.01759) — "experiences that are benign in
  isolation may jointly weaken an agent's safety boundary when accumulated and reused across
  sessions"; an *attacker* composes them. Single victim agent.
- [Misevolution, 2509.26354](https://arxiv.org/abs/2509.26354) — "degradation of safety alignment
  after memory accumulation"; single agent, four pathways.
- [Memory poisoning and secure multi-agent systems, 2603.20357](https://arxiv.org/abs/2603.20357);
  [SuperLocalMemory, 2603.02240](https://arxiv.org/abs/2603.02240) (Bayesian trust + per-agent
  provenance, but benchmarked on latency/NDCG/attack separation);
  [The Misattribution Gap, 2605.22842](https://arxiv.org/abs/2605.22842);
  [Safety in Self-Evolving LLM Agent Systems, 2606.23075](https://arxiv.org/abs/2606.23075).

Non-adversarial side is nearly empty. The only rigorous treatment is
[Ratchet](https://arxiv.org/abs/2605.22148), which is **single-agent** and assumes a **stationary**
notion of skill value. Nobody studies a merely *wrong* or *outdated* experience — written in good
faith by a competent agent — propagating through a shared pool to teammates.

### 3.4 Co-adaptation and endogenous non-stationarity — EMPTY

Zero results for `abs:"co-adaptation" AND abs:"LLM agents"`, `abs:"non-stationarity" AND abs:"LLM"
AND abs:"multi-agent"`. [GLOVE](https://arxiv.org/abs/2601.19249) is the only drift paper and its
drift is exogenous and its agent is single. [Memory-Induced Tool-Drift,
2605.24941](https://arxiv.org/abs/2605.24941) is about persona-bias leakage into tool calls, single
agent, no evolution. In every multi-agent self-evolution paper I read (GEA, Meta-Team, CoMAS, Prism,
DecentMem) the possibility that agent *i*'s recorded experience is invalidated by agent *j*'s
subsequent evolution is not mentioned once.

### 3.5 Incentives — PARTIALLY OCCUPIED, one thin slice left

Occupied:
- [When AI Agents Compete for Jobs (AI-Work), 2512.04988](https://arxiv.org/abs/2512.04988) — a
  simulated gig economy; agents "compete for jobs, develop skills, and adapt their strategies under
  uncertainty and competitive pressure"; studies metacognition, competitive awareness, long-horizon
  planning. **Strategy adaptation, not persistent-artifact self-evolution; no shared pool.**
- [Evolving Deception, 2603.05872](https://arxiv.org/abs/2603.05872) — self-evolution under
  competition drifts to deception as an ESS. **Bidding arena; each agent evolves privately.**
- [MAC-SPGG, 2508.02076](https://arxiv.org/abs/2508.02076) — sequential public-goods game redesigned
  so effortful contribution is the unique SPNE. **Contribution is abstract per-round effort, not a
  persistent artifact others reuse.**
- [CoopEval, 2604.15267](https://arxiv.org/pdf/2604.15267);
  [Social Learning and Collective Norm Formation, 2510.14401](https://arxiv.org/pdf/2510.14401).

Left open: contributing to a **persistent shared experience/skill pool** has economics that abstract
effort does not — the contribution is non-rival, permanently reusable, competitively self-harming
(revealing a winning method erodes your relative edge), and *degradable* (you can contribute a
plausible-but-suboptimal entry at no cost). Meanwhile the entire cooperative self-evolution
literature — [Knowledge-Centric](https://arxiv.org/abs/2607.19592),
[GEA](https://arxiv.org/abs/2602.04837), [Meta-Team](https://arxiv.org/abs/2605.29790),
[CoMAS](https://arxiv.org/abs/2510.08529) — assumes truthful, complete, free contribution.

### Searches that returned nothing (recorded per brief)

arXiv API, `sortBy=submittedDate`:
`abs:"difference rewards" AND abs:"language model"` (0) ·
`abs:"counterfactual replay" AND abs:"agent"` (0) ·
`abs:"experience sharing" AND abs:"LLM agents" AND abs:"diversity"` (0) ·
`abs:"stale" AND abs:"memory" AND abs:"LLM agents"` (0) ·
`abs:"evolutionary game" AND abs:"self-evolving" AND abs:"LLM"` (0) ·
`abs:"non-stationarity" AND abs:"LLM" AND abs:"multi-agent"` (0) ·
`abs:"experience sharing" AND abs:"LLM agents"` (0) ·
`abs:"memory" AND abs:"staleness" AND abs:"agent"` (0) ·
`abs:"provenance" AND abs:"agent memory"` (0) ·
`abs:"co-adaptation" AND abs:"LLM agents"` (0) ·
`abs:"population" AND abs:"LLM agents" AND abs:"convergence"` (0).

**Caveat, stated honestly:** a later batch of broader re-runs of these same queries also returned 0,
including a sanity query that should have had hits, which indicates the arXiv API started
rate-limiting me mid-session. I therefore re-ran the decisive kill-checks through independent web
search restricted to `arxiv.org`/`openreview.net`/`aclanthology.org`/`dl.acm.org`, and those
searches **did** surface the occupancy hits recorded in §3.1, §3.2 and §3.3 (DecentMem, CAR, GLOVE,
2604.18005). Every one of those was then confirmed by fetching the arXiv abstract page directly. The
zero-result list above should be read as "no hits under this exact phrasing", not as proof of absence.

---

## 4. Three candidate gaps

All three share one cheap testbed, described in §5, which is why a 4-week pilot is realistic. All
three use **frozen models plus prompting/memory/selection dynamics** — no fine-tuning, no RL runs.

---

### C1 — Endogenous non-stationarity: experience invalidated by teammates' own evolution

> **Gap statement.** No work measures whether experiences written into a shared pool by a
> self-evolving agent remain valid **while its teammates concurrently self-evolve** — i.e. nobody
> treats the classical MARL non-stationarity problem as a *memory-validity* problem in LLM agent
> teams; all existing drift work ([GLOVE](https://arxiv.org/abs/2601.19249)) assumes the drift is
> exogenous and the agent is alone.

**Why it matters.** Every deployed self-evolving MAS
([PILOT](https://arxiv.org/abs/2608.18637), [Agent Gym](https://arxiv.org/abs/2608.15591),
[SESG](https://arxiv.org/abs/2608.08471)) accumulates experience under the implicit assumption that a
lesson learned at round *t* is still true at round *t+k*. In a team where every member is rewriting
its own behaviour, that assumption is false by construction: "when the retrieval agent returns
paginated results, summarise before ranking" stops being true the moment the retrieval agent evolves
pagination away. This is exactly why independent learners are unsound in MARL, and it is the single
best-understood pathology in the AAMAS canon — imported into a literature that has not noticed it.

**Falsifiable hypothesis.** In a self-evolving LLM team, the *hazard rate* of an experience entry —
the probability per round that following it now hurts rather than helps — is a monotonically
increasing function of the number of *teammate* evolution events since the entry was written, and is
**larger than** the hazard from exogenous environment drift of comparable magnitude. Corollary: a
provenance-gated retrieval rule that discounts entries by teammate-churn-since-authorship recovers
most of the lost performance at near-zero cost, and beats both a recency baseline and a
[Ratchet](https://arxiv.org/abs/2605.22148)-style judged-contribution eviction rule (which is
blind to *who* changed).

**Decisive experiment.** A 4-role team (planner / retriever / executor / verifier) on a long-horizon
tool task, each role holding an evolving private playbook plus a shared pool. Three arms:
(a) **frozen teammates** — only the focal agent evolves; (b) **co-evolving teammates**; (c)
**exogenous drift** — teammates frozen but tool APIs mutated on a matched schedule. For every pooled
entry, at every later round, re-run the focal task with and without that entry injected (paired,
same seeds) to get a direct validity measurement. Plot hazard vs. teammate-evolution-count and vs.
exogenous-drift-count. The hypothesis dies if curve (b) is flat or does not exceed (c).

**AAMAS fit.** *Learning and Adaptation* primarily; secondarily *Coordination and Cooperation*.
Non-stationarity under concurrent learning is core AAMAS territory, and the paper's framing —
"independent learners are unsound, and LLM MAS have quietly rebuilt independent learners with a
shared blackboard" — is a message this venue is uniquely positioned to receive.

**4-week feasibility: HIGH.** Frozen API models throughout; "evolution" is playbook rewriting, not
weight updates. The dominant cost is the paired with/without re-runs, which is embarrassingly
parallel and bounded: 4 agents × ~20 rounds × ~30 pooled entries × 2 conditions × 3 arms ≈ 14k short
rollouts, comfortably a few hundred dollars on a mid-tier model with a small frontier-model
replication for the headline table. No human subjects. Weeks 1–2 build the harness and the drift
injector, week 3 runs arms, week 4 the provenance-gating intervention.

**Occupancy check.**
| Nearest paper | What it does NOT do |
|---|---|
| [GLOVE, 2601.19249](https://arxiv.org/abs/2601.19249) | Formalises memory-environment misalignment and probes for it — but drift is exogenous ("interface updates, rule modifications, or altered configurations"), the agent is single, and there is no notion of a teammate as a drift source. |
| [Ratchet, 2605.22148](https://arxiv.org/abs/2605.22148) | Gives the exact judge-reliability condition for retiring a skill, and defines "library drift" — but single-agent, stationary skill value, and the eviction statistic has no provenance dimension. |
| [Meta-Team, 2605.29790](https://arxiv.org/abs/2605.29790) | Evolves behaviours, coordination and organization from MAS experience — but only ever measures end-task accuracy; never asks whether an earlier lesson has been invalidated by a later change. |
| [CoEvo-Mem, 2608.01739](https://arxiv.org/abs/2608.01739) | Co-evolves retrieval policy with memory bank — two coupled components inside one agent, not a team, and no validity-decay measurement. |

**Adversarial self-critique.** The risk is that the effect is small, or that a plain recency
baseline captures most of it (teammate churn and elapsed time are correlated). Mitigation is built
into the design: arm (c) matches drift *rate* while removing the teammate as the source, and the
recency baseline is a required comparator, not an afterthought. If recency wins, that is still a
publishable negative result with a clean mechanism story — but it is a weaker paper.

---

### C2 — Sharing rate as a control parameter for monoculture in self-evolving populations

> **Gap statement.** No work treats the experience-sharing rate/topology in a population of
> self-evolving LLM agents as a **control parameter** and measures the resulting behavioural-diversity
> trajectory across evolution rounds; existing diversity-collapse results are one-shot and
> conversational, and the one paper that asserts shared memory "collapses agent diversity" never
> measures diversity at all.

**Why it matters.** The field is converging on shared-knowledge designs — [Knowledge-Centric
Self-Improvement](https://arxiv.org/abs/2607.19592) ("throw the agent away, grow the shared
knowledge"), [GEA](https://arxiv.org/abs/2602.04837) (group as evolutionary unit) — on the strength
of short-horizon accuracy gains. If the price is that the population's exploration variance decays
geometrically in the sharing rate, then the design that wins at round 10 loses at round 100, and
every reported gain is measured inside the window where the cost has not yet materialised. There
should be a *speed/diversity frontier*, and no one has drawn it.

**Falsifiable hypothesis.** Behavioural diversity (semantic-cluster entropy over proposed solution
mechanisms, plus distinct-mechanism coverage) decays with the per-round sharing probability *p*, and
there exists a critical *p\** above which the population is absorbed into a single mechanism family
before the task's mechanism space is covered — with **short-horizon accuracy rising in *p* while
long-horizon best-of-population falls**, producing a crossover. A diversity-preserving admission rule
(admit an entry to the pool only if it is not within ε of an existing entry's mechanism cluster)
shifts *p\** without sacrificing the early gains.

**Decisive experiment.** N = 24–40 frozen-model agents on an open-ended task with a measurable
mechanism space (algorithm-discovery style, so mechanism clusters are machine-labellable). Sweep
*p* ∈ {0, 0.1, 0.25, 0.5, 1.0} × topology ∈ {none, ring, random-graph, fully-shared} over ~40
evolution rounds. Track per round: mechanism-cluster entropy, effective rank of the embedded
proposal set (following [2604.03809](https://arxiv.org/abs/2604.03809)'s instrument), mean fitness,
best-of-population fitness. Fit a payoff-biased-imitation / replicator model to the observed cluster
frequencies and test whether it predicts held-out *p*. Dies if entropy is flat in *p*, or if
best-of-population is monotone in *p* at every horizon.

**AAMAS fit.** *Learning and Adaptation* and *Engineering Multiagent Systems*; the replicator-model
fit puts it within reach of *Formal Models / Evolutionary Game Theory*. Diversity maintenance in
adapting populations is an AAMAS home topic.

**4-week feasibility: MEDIUM-HIGH.** Frozen models, prompt/memory-only evolution, so no training.
The cost driver is 5 sharing rates × 4 topologies × 30 agents × 40 rounds; the honest plan is to
prune to 5 *p*-values × 2 topologies × 24 agents and run the full cross only if budget allows.
Mechanism-cluster labelling needs a stable embedding + clustering pipeline, and
[2604.03809](https://arxiv.org/abs/2604.03809) shows encoder choice is "a first-order design
decision" — so two encoders must be reported, which is a real but manageable time cost. Medium
rather than high because the sweep is the largest of the three.

**Occupancy check.**
| Nearest paper | What it does NOT do |
|---|---|
| [DecentMem, 2605.22721](https://arxiv.org/abs/2605.22721) | Asserts centralized shared memory is "collapsing agent diversity" as motivation, then measures only accuracy and token count. Its theory is $O(\log T)$ bandit regret over one agent's dual pool — no population state, no diversity metric, no sharing-rate sweep. It hands us our premise and leaves the evidence undone. |
| [Diversity Collapse in MAS, 2604.18005](https://arxiv.org/abs/2604.18005) | Measures diversity collapse properly and finds dense topologies accelerate convergence — but in **one-shot ideation**: no persistent experience pool, no evolution across rounds, coupling is live conversation. No sharing-rate control parameter, no dynamical model. |
| [GEA, 2602.04837](https://arxiv.org/abs/2602.04837) | Group as evolutionary unit with explicit experience sharing — but frames diversity purely as fuel ("converts early-stage exploratory diversity into sustained, long-term progress") and never measures whether sharing destroys it. No *p*, no topology ablation. |
| [Prism, 2604.19795](https://arxiv.org/abs/2604.19795) | Has replicator-decay dynamics and proves convergence to an Evolutionary Stable Memory Set — but over **memory items**, not agent behaviours; 4 agents; no diversity trajectory. |
| [Evaluating Collective Behaviour of Hundreds, 2602.16662](https://arxiv.org/abs/2602.16662) | Hundreds of agents under payoff-biased imitation converging to low-welfare equilibria — but agents are frozen code strategies in social dilemmas, with no self-evolution loop, no experience pool, and no capability task. |

**Adversarial self-critique.** This is the most pre-empted of the three: [2604.18005](https://arxiv.org/abs/2604.18005)
owns the phrase "diversity collapse" and DecentMem owns the claim. The contribution has to be
(i) the *dynamics over rounds*, (ii) *p* as a tunable knob with a predicted critical value, and
(iii) the accuracy/diversity crossover. If a reviewer reads it as "2604.18005 with memory added",
it fails. I rate this the weakest of the three for that reason.

---

### C3 — The experience commons: self-evolving agents as strategic contributors

> **Gap statement.** No work models contribution to a shared experience/skill pool as a **strategic
> choice** — where writing your winning method into the commons is costly to your relative standing
> and where plausible-but-degraded entries are free to produce — while the pool is simultaneously the
> substrate of every agent's self-evolution; all cooperative self-evolution work assumes truthful,
> complete, free contribution, and all LLM public-goods work uses abstract per-round effort rather
> than a persistent reusable artifact.

**Why it matters.** [Knowledge-Centric Self-Improvement](https://arxiv.org/abs/2607.19592)'s thesis —
discard the agent, grow the shared knowledge — is only sound if contributors are cooperative
components. The moment agents are separately evaluated, separately owned, or competing for tasks
(precisely the world [AI-Work](https://arxiv.org/abs/2512.04988) describes), contributing becomes a
public-goods game with an unusual and under-studied twist: the *quality* of a contribution is cheap
to fake and expensive to verify, so the equilibrium failure is not silence but **plausible
mediocrity**. That is a mechanism-design question with a concrete engineering answer (what does the
pool have to pay for, and how does it verify?), and AAMAS is the venue that cares.

**Falsifiable hypothesis.** Under a scoring rule that rewards relative rank, self-evolving LLM agents
sharing a pool will (H1) under-contribute their highest-value experiences relative to a
cooperative-instruction control, and (H2) preferentially contribute entries that are *valid but
sub-optimal* — degradation without detectable falsehood — rather than withhold outright; and (H3) a
usage-based reward (credit the author each time an entry is retrieved and the retrieving agent
succeeds, i.e. a downstream-attribution payment) restores contribution quality closer to the
cooperative ceiling than a flat per-contribution payment, which increases *volume* while lowering
mean entry value.

**Decisive experiment.** Same team testbed, but agents are scored on **relative** performance and
must decide, after each successful episode, whether and what to write to the pool. Conditions:
{cooperative instruction, relative scoring + no payment, relative scoring + flat payment, relative
scoring + usage-based payment}. Instrumentation: (i) *withholding rate* — measured by comparing each
agent's private playbook against the pool for semantically matched entries; (ii) *entry value* —
measured directly by paired inject/no-inject re-runs on held-out tasks, the same primitive as C1;
(iii) pool-level welfare over rounds. H2 is the sharp, easily-falsifiable prediction: it dies if
degraded entries are indistinguishable in measured value from cooperative-condition entries.

**AAMAS fit.** Strongest fit of the three. *Economic Paradigms* (mechanism design, incentives) and
*Coordination and Cooperation*, with *Learning and Adaptation* as the secondary area. This is a
mechanism-design paper wearing an LLM-agent testbed, which is exactly the shape AAMAS rewards.

**4-week feasibility: HIGH.** No training. The instrumentation is the same paired inject/no-inject
primitive as C1, so the two share a harness. Four conditions × ~20 rounds × ~15 agents is a smaller
run than C2. The main design risk is *behavioural*, not computational: frozen LLMs may not act
strategically enough for the effect to appear without heavy-handed prompting, and a prompt that
tells the agent to be competitive risks measuring instruction-following rather than strategy. This
must be handled with a graded competitive-pressure manipulation (payoff structure varied, framing
held constant) so that the effect is shown to track the incentive rather than the wording — that
manipulation check is itself a contribution, and its failure is a clean negative result.

**Occupancy check.**
| Nearest paper | What it does NOT do |
|---|---|
| [MAC-SPGG, 2508.02076](https://arxiv.org/abs/2508.02076) | Redesigns the public-goods reward so effortful contribution is the unique SPNE — but contribution is abstract per-round effort in a sequential ensemble, not a **persistent artifact other agents reuse later**; there is no pool, no retrieval, no self-evolution, and no notion of contribution *quality* being separately manipulable from contribution *volume*. |
| [AI-Work, 2512.04988](https://arxiv.org/abs/2512.04988) | Simulates a competitive gig economy where agents "compete for jobs, develop skills, and adapt their strategies" — but skills are private and there is no shared knowledge commons; the studied capabilities are metacognition / competitive awareness / planning, not contribution strategy. |
| [Evolving Deception, 2603.05872](https://arxiv.org/abs/2603.05872) | Shows self-evolution under competition drifts to deception as an evolutionarily stable strategy — the closest prior in spirit. But deception is directed at *opponents in a bidding arena*; there is no shared artifact pool, so nothing about strategic degradation of a commons other agents learn from. |
| [Knowledge-Centric Self-Improvement, 2607.19592](https://arxiv.org/abs/2607.19592) | Builds exactly the shared-knowledge commons this candidate stress-tests — and assumes every agent writes truthfully and completely. The assumption is never stated as an assumption, let alone tested. |
| [Shapley-Coop, 2506.07388](https://arxiv.org/abs/2506.07388) | Prices contributions among self-interested LLM agents via Shapley CoT and negotiation — but prices *task execution* within an episode, not deposits into a persistent experience pool consumed by future episodes. |

**Adversarial self-critique.** The honest worry is H1/H2 being an artifact of prompt framing.
Secondarily, [Evolving Deception](https://arxiv.org/abs/2603.05872) already established "competition
+ self-evolution → strategic misbehaviour", so the novelty rests entirely on the *commons* structure
and the usage-based-payment mechanism result. If the mechanism comparison (H3) does not separate,
the paper is a phenomenon report in a space where a phenomenon report already exists.

---

## 5. Shared testbed (why 4 weeks is realistic)

All three candidates reduce to one harness plus one measurement primitive:

- **Harness.** A small team of frozen-model agents on a long-horizon tool/search task, each with a
  private playbook it rewrites after each episode, plus a shared append-only experience pool with
  per-entry provenance (author, round, retrieval count).
- **Measurement primitive.** *Paired entry-value estimation*: to value any pooled entry at any round,
  re-run the same episode with and without that entry injected, same seed. This single primitive
  yields C1's hazard rate, C2's fitness curves, and C3's entry-value distributions.
- **Knobs.** C1 varies *who evolves* (focal only / all / none-but-tools-drift). C2 varies *sharing
  rate and topology*. C3 varies *scoring rule and payment mechanism*.

Nothing requires fine-tuning, RL, or human subjects. The build is shared; only the sweeps differ.

## 6. Recommendation

**C1 first.** It sits on a genuinely empty intersection (§3.4 returned nothing under any phrasing,
and GLOVE's single-agent exogenous scope is stated in its own abstract), it re-imports the
best-established result in the AAMAS canon into a literature that has not noticed it needs it, and
it is the cheapest of the three to run convincingly. **C3 second** — best venue fit and a real
mechanism-design contribution, but carries prompt-framing risk. **C2 third** — the phenomenon is
real and DecentMem hands us the premise, but [2604.18005](https://arxiv.org/abs/2604.18005) has
already planted a flag nearby and the contribution has to survive a "so it's that, with memory"
reading.
