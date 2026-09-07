# Survey B — Trust, Verification, Failure, Safety
Corpus slice from `masamasa59/ai-agent-papers`. Compiled 2026-09-07 for AAMAS 2027 main track.

## 0. Method and provenance note

All eight assigned files were fetched as **raw markdown via `curl`**, not via WebFetch's summarizer, so
every paper entry below is read from the literal source text rather than a model summary. All
abstracts quoted in this document were fetched from `arxiv.org/abs/<id>` and parsed out of the
`citation_abstract` meta tag, again bypassing summarization.

**Fabrication guard that actually fired.** A WebSearch snippet described
[arXiv 2603.19262](https://arxiv.org/abs/2603.19262) as proving that a belief-revision exponent
"below one [is] necessary and sufficient for asymptotic stability under repeated revision." That
claim is **only in v1**. Fetching
[v1](https://arxiv.org/abs/2603.19262v1) vs. the current version confirms the paper was retitled
from *"The α-Law of Observable Belief Revision in Large Language Model Inference"* to
*"Empirical Characterization of Inference-Time Elicited Probability Transformations in Large
Language Models"*, and the current abstract explicitly retreats: *"The main contribution is not the
algebraic form itself ... but the empirical observation that diverse inference-time prompting
pipelines repeatedly exhibit reproducible log-ratio structure under controlled conditions."* The
stability theorem is gone. This is load-bearing for the STAV verdict in §3.

---

## 1. Coverage stats — every entry enumerated

| File | Unique arXiv IDs | Notes |
|---|---|---|
| [capabilities/trust/evaluation.md](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/capabilities/trust/evaluation.md) | **104** | Aug 2023 – Aug 2026. Includes a 6-entry "Evaluator, Verifier & Judge" subsection. |
| [capabilities/trust/safety.md](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/capabilities/trust/safety.md) | **102** | Three subsections: main (62), Attacks & Red-Teaming (25), Defenses & Guardrails (13). Two entries have no link (Proteus, MonitoringBench). |
| [capabilities/adaptation/self-correction.md](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/capabilities/adaptation/self-correction.md) | **51** | Jun 2022 – Aug 2026. Heavily 2024–2025 weighted; only 2 entries from Jul–Aug 2026. |
| [capabilities/adaptation/verification.md](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/capabilities/adaptation/verification.md) | **14** | **Thinnest file in the slice.** Feb 2024 – Aug 2026, and 2 of the 14 are surveys. |
| [capabilities/adaptation/failure-attribution.md](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/capabilities/adaptation/failure-attribution.md) | **11** | Newest category (created Aug 2026). 13 list lines, 2 duplicated (WHO&WHEN PRO, TRAJDEBUG). |
| [newsletters/aug_2026/evaluation_trends.md](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/newsletters/aug_2026/evaluation_trends.md) | 10 linked (covers 15 Aug papers) | Prose analysis + a numbers table + a 5-item open-problems section. |
| [newsletters/aug_2026/failure_attribution_trends.md](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/newsletters/aug_2026/failure_attribution_trends.md) | 8 linked (covers 8 Aug papers) | First issue of this category. 5-item open-problems section. |
| [newsletters/aug_2026/safety_trends.md](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/newsletters/aug_2026/safety_trends.md) | 11 linked (covers 15 Aug papers) | 5-item open-problems section. |
| **Total distinct IDs across slice** | **278** | |

Newsletters are written in Japanese; all quotations below are my translations, with the original
kept where the wording is load-bearing.

---

## 2. Map of the territory

### 2.1 SATURATED (crowded, many 2026 entries — do not enter)

**(a) Benchmark construction, especially "realistic work" benchmarks.** This is by far the most
crowded band. August 2026 alone contributed
[StartupBench](https://arxiv.org/abs/2608.17800),
[DuMateBench](https://arxiv.org/abs/2608.26546),
[Thinkingbox](https://arxiv.org/abs/2608.19741),
[Business Arena](https://arxiv.org/abs/2608.08621),
[FM-Bench](https://arxiv.org/abs/2608.18423),
[CentaurBench](https://arxiv.org/abs/2608.18554),
[SHIJIANBENCH](https://arxiv.org/abs/2608.01204), and
[AI4AI-Bench](https://arxiv.org/abs/2608.20318). A new benchmark is not a contribution here.

**(b) Self-evolution poisoning / skill-library attacks.** Went from concept to five measured attacks
in one month:
[EvoMal](https://arxiv.org/abs/2608.25776),
[PoisonedEvolution](https://arxiv.org/abs/2608.05563),
[EvoBreak](https://arxiv.org/abs/2608.01759),
[Practice Makes Unsafe](https://arxiv.org/abs/2608.12851),
[RedEvoAgent](https://arxiv.org/abs/2608.27439), plus
[SkillJack](https://arxiv.org/abs/2608.03509),
[BadSkill](https://arxiv.org/abs/2604.09378),
[Supply-Chain Poisoning](https://arxiv.org/abs/2604.03081),
[ZOMBIE AGENTS](https://arxiv.org/abs/2602.15654). *Demonstrating another poisoning channel is
saturated.* The population-level and incentive-level treatment is not (see §5.3).

**(c) Trajectory-level failure attribution as a supervised prediction problem.**
[WHO&WHEN PRO](https://arxiv.org/abs/2607.09996),
[TRAJDEBUG](https://arxiv.org/abs/2608.06346),
[SearchAuditor](https://arxiv.org/abs/2608.05212),
[AgentLocate](https://arxiv.org/abs/2607.07989),
[A2E](https://arxiv.org/abs/2608.07346),
[LEDGER](https://arxiv.org/abs/2608.18398),
[MP-Bench](https://arxiv.org/abs/2603.25001),
[Conformal Agent Error Attribution](https://arxiv.org/abs/2605.06788). Better attribution accuracy
is a crowded target.

**(d) LLM-as-judge reliability auditing.**
[Jagged Judges](https://arxiv.org/abs/2608.12645),
[Nine Judges, Two Effective Votes](https://arxiv.org/abs/2605.29800),
[Blind to the Pivotal Vote](https://arxiv.org/abs/2608.06940),
[Judge Reliability Harness](https://arxiv.org/abs/2603.05399),
[When the Judge Changes](https://arxiv.org/abs/2607.08535). *Measuring* judge fragility is done.

**(e) Guardrails and runtime enforcement.**
[SESG](https://arxiv.org/abs/2608.08471), [SHE](https://arxiv.org/abs/2608.09885),
[PolicyGuide](https://arxiv.org/abs/2608.19861), [SysEvolve](https://arxiv.org/abs/2608.15012),
[SafeHarbor](https://arxiv.org/abs/2605.05704), [SABER](https://arxiv.org/abs/2512.07850).

### 2.2 THIN (few entries, mostly non-2026, or empirical-only)

**(a) Verification as a capability — strikingly thin.** `verification.md` holds **14 papers total**,
two of which are surveys, and the newest non-survey entry is
[The Art of Building Verifiers for Computer Use Agents](https://arxiv.org/abs/2604.06240) (Apr
2026). For a slice whose whole subject is trust, there is *no* formal treatment of verification as a
decision under cost, no equilibrium analysis, and no population-level verification model anywhere in
the file.

**(b) Self-correction has gone quiet.** 51 papers, but only 2 from Jul–Aug 2026
([Critic Experience Bank](https://arxiv.org/abs/2607.12397),
[Corrective Features](https://arxiv.org/abs/2608.05207)). The field moved from "repair" to
"diagnose" (failure-attribution) and "prevent" (guardrails).

**(c) Causal/counterfactual grounding of blame.** Essentially one paper —
[Credit Without Ground Truth](https://arxiv.org/abs/2608.19760) — and it is a negative result.

**(d) Anything mechanism-design shaped.** The whole 278-paper slice contains **three** entries that
an AAMAS reviewer would call mechanism design:
[Insured Agents](https://arxiv.org/abs/2512.08737),
[Paying for Honesty Without Knowing the Truth (CARP)](https://arxiv.org/abs/2607.28330), and
arguably [CoffeeBench](https://arxiv.org/abs/2606.16613). None is in the verification or
failure-attribution files.

### 2.3 The negative space, stated precisely

An AAMAS reviewer values trust/reputation systems, mechanism design, incentives, formal guarantees,
equilibrium and stability analysis, emergent failure in populations, norms and sanctioning, and
coordination. Mapping the slice against that list:

| AAMAS-valued property | Presence in this 278-paper slice |
|---|---|
| Benchmarks / empirical measurement | Overwhelming — ~60% of the slice |
| Reputation systems | **Zero** in the slice's trust files. Exists only *outside* the corpus ([RepuNet](https://arxiv.org/abs/2505.05029), [Ev-Trust](https://arxiv.org/abs/2512.16167), [CARP](https://arxiv.org/abs/2607.28330)) |
| Mechanism design / incentives | 3 of 278 |
| Equilibrium or stability analysis | **Zero in the corpus slice.** All examples ([Itkin](https://arxiv.org/abs/2606.27409), [Ev-Trust](https://arxiv.org/abs/2512.16167), [Reliability-Contagion](https://arxiv.org/abs/2607.21912)) sit outside it |
| Emergent failure in populations | Named but not modeled: [Systemic Risks of Interacting AI](https://arxiv.org/abs/2512.17793), [Emergent Social Intelligence Risks](https://arxiv.org/abs/2603.27771), [Agents of Chaos](https://arxiv.org/abs/2602.20021) — all position/taxonomy papers |
| Norms and sanctioning | **Zero** |
| Formal guarantees | Only [Conformal Agent Error Attribution](https://arxiv.org/abs/2605.06788) (coverage guarantee), used for rollback, not for governance |

**The single sharpest structural observation:** the LLM-agent verification literature has produced,
in 2026, an unusually rich set of *measured failure rates of its own trust instruments* —

- failure attribution tops out at **34.11% macro-average** ([TRAJDEBUG](https://arxiv.org/abs/2608.06346)) and **32.3%** on long search traces ([SearchAuditor](https://arxiv.org/abs/2608.05212));
- step-level credit signals are **indistinguishable from a shuffled control**, with implicit credit correlating with policy *fluency* at rank-correlation +0.75 while partial correlation with causal contribution is **−0.004** ([Credit Without Ground Truth](https://arxiv.org/abs/2608.19760));
- LLM judges flip **25–71%** under static pushback and **62–91%** against an adaptive persuader, and *"the pressure that succeeds in changing a judgment is almost always harmful with respect to the ground truth"* ([Jagged Judges](https://arxiv.org/abs/2608.12645));
- a nine-judge panel carries the information of **about two independent votes** ([Nine Judges](https://arxiv.org/abs/2605.29800));
- failures often admit **multiple plausible attributions**, so a point-valued blame label is the wrong object ([MP-Bench](https://arxiv.org/abs/2603.25001)).

— and has done **nothing** with those numbers downstream. Not one paper in the slice asks what a
population of agents does when its trust signal is known to be 34% accurate. That disconnect is
where all three of my candidates live.

### 2.4 Verbatim stated open problems (highest-yield source)

From [failure_attribution_trends.md](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/newsletters/aug_2026/failure_attribution_trends.md), §「論点・未解決課題」:

> 「**致命的な誤りの正解を誰が作るのか。** TRAJDEBUG は手作業の注釈（486軌跡）、SearchAuditor も専門家の注釈（1,243軌跡）に依存する。一方 Credit Without Ground Truth は実行による反実仮想で正解を作った。注釈は「人間が致命的だと思う手」を、再サンプルは「実際に結果を変える手」を測る——**両者が一致するかは検証されていない**。」
>
> *"Who creates the ground truth for critical errors? ... Annotation measures 'the move a human thinks was fatal'; resampling measures 'the move that actually changed the outcome' — whether the two agree has not been verified."*

> 「**帰属の粒度が揃っていない。** ステップ、致命的な誤り1点、状態、45パターンの工程×根本原因、ハーネスの部品——**同じ「失敗の帰属」という言葉で、5つの異なる単位が使われている**。」
>
> *"The granularity of attribution is not aligned ... five different units are used under the same phrase 'failure attribution'."*

From [safety_trends.md](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/newsletters/aug_2026/safety_trends.md), §「論点・未解決課題」:

> 「**「組み合わせて有害」を検査する方法がない。** EvoBreak と PoisonedEvolution が示したのは、成果物を1つずつ見る検査が原理的に無力だということだ。**集合としての安全性をどう定義し、どう検査するかは未着手に近い**。」
>
> *"There is no method for inspecting 'harmful in combination' ... how to define and inspect safety of a *set* is close to untouched."*

> 「**防御の進化と攻撃の進化の速度差。** SESG は 16〜24時間で新脅威に適応するが、EvoMal のワームは1回のカスケードで増殖する。SysEvolve は両者を同じ土俵に載せたが、**どちらが速いかという問いには答えていない**。」
>
> *"The speed differential between defense evolution and attack evolution ... SysEvolve put both on the same footing but does not answer which is faster."*

From [evaluation_trends.md](https://raw.githubusercontent.com/masamasa59/ai-agent-papers/main/newsletters/aug_2026/evaluation_trends.md):

> 「**判定者の脆さを、判定者を使う全ベンチマークにどう反映するか。** ... CentaurBench は判定者間一致率 71% を限界として明記したが、**圧力下の安定性まで測った例はまだない**。」
>
> *"How should judge fragility be reflected in every benchmark that uses judges? ... there is still no example that measures stability under pressure."*

Author-stated limitations quoted in the newsletters, verified against the arXiv abstracts:

- [Credit Without Ground Truth](https://arxiv.org/abs/2608.19760): single environment (ALFWorld), single scale (7–8B), offline LoRA, and no validated positive control in the training-loop experiment. Also: causal effects are measurable at only **30.5%** of decision points, and the unmeasurable fraction differs **2×** between models (13.1% vs 26.8%) — *"what you can measure is model-dependent."*
- [PoisonedEvolution](https://arxiv.org/abs/2608.05563): evaluation stops at artifact generation; payloads are never actually executed.
- [EvoBreak](https://arxiv.org/abs/2608.01759): 2 frameworks, 2 models; assumes extracted experiences are observable.
- [EvoMal](https://arxiv.org/abs/2608.25776): a branching-process corollary establishes that self-replication needs **both** a high imitation rate **and** re-retrievability of authored skills — one alone is insufficient. This is an R₀-shaped condition stated for a *single* library.
- [Automata from Agent Traces](https://arxiv.org/abs/2608.23670): the learned FSM accepts the closure of observed immediate-successor relations, not the generating language; adversarial traces preserving bigram statistics replay successfully.

---

## 3. STAV occupancy verdict

**STAV's four-part claim:** (1) measure LLM agents' costly-verification behavior as a *fitted trust-update
law*; (2) plug that law into a *delayed error-propagation model*; (3) predict *held-out stability
transitions*; (4) constrain the resulting adaptive verifier with a *robust stability certificate*.

### Nothing in the corpus — or in the wider literature I searched — publishes all four. Verdict: **NOT SOLVED, and not close.** But the parts are individually claimed, and the seam is riskier than it looks.

Part-by-part, from primary text:

**Part 1 — claimed as measurement, not as a law.**
[Trust Between AI Agents](https://arxiv.org/abs/2606.14923) (Chen) does exactly STAV's measurement:
*"We propose a behavioral measure based on costly verification ... Relative to a memoryless version
of the same model, reduced verification provides an observable measure of trust."* It reports
descriptive dynamics — verification reduced **60–85%** for four of six frontier snapshots, *"Recovery
is slower than formation, and clustered failures sustain suspicion far longer than the same number
of failures spread apart"* — and concludes with a governance recommendation
(*"calibration, rather than maximal suspicion, should be the central concern"*). It fits **no
parametric update law** and does no dynamical analysis. STAV's part 1 is therefore a genuine
increment over Chen, but a **modest** one: it is "fit a curve to Chen's Figure."

**Part 2 — fully claimed, with a stronger result than STAV would need.**
[Delayed Verification Destabilizes Multi-Agent LLM Belief](https://arxiv.org/abs/2606.27409) (Itkin)
already has the delayed error-propagation model *and* the closed-form threshold: *"Spectral
decomposition by the grounded Laplacian yields a closed-form stability threshold for the
verification dose ... for delay two, the threshold is the inverse golden ratio."* It also already
supplies the optimization layer — *"a supermodular placement objective and a greedy (1−1/e)-approximation
rule."* STAV does not get to claim the model; it can only claim the *coupling*.

**Part 3 — the coupling is unclaimed, but there is a live cautionary precedent.**
No paper found fits a behavioral trust law and uses it to predict held-out stability transitions.
**However**, [arXiv 2603.19262](https://arxiv.org/abs/2603.19262) attempted precisely this shape —
fit a multiplicative belief-revision exponent, prove a contraction condition — and the stability
theorem **did not survive revision** (v1 → v2 retitle, theorem removed, contribution downgraded to
"empirical observation of reproducible log-ratio structure"). A reviewer who knows this history will
press hard on whether STAV's fitted law is stable enough across prompt configurations to carry a
dynamical prediction. Itkin's own abstract supplies the counter-lever: *"grounded factual answering
makes truth an absorbing boundary and eliminates the effect, suggesting that the instability is
specific to signed-belief tasks"* — so STAV's stability transitions may only exist in a narrow task
class.

**Part 4 — unclaimed in this literature.** No robust stability certificate constraining an adaptive
verifier appears anywhere in the 278 papers or in my external searches. The nearest object is
Ev-Trust's ESS threshold conditions (below), which are equilibrium conditions on a trust mechanism,
not a robustness certificate on a controller.

### Adjacent unclaimed gaps near STAV (offered, not proposed)

1. **Annotation vs. counterfactual blame divergence.** The failure-attribution newsletter states outright that *whether human-annotated "fatal step" agrees with resampled "step that actually changed the outcome" has not been verified*. A study measuring the disagreement between [TRAJDEBUG](https://arxiv.org/abs/2608.06346)/[SearchAuditor](https://arxiv.org/abs/2608.05212) annotation and [Credit Without Ground Truth](https://arxiv.org/abs/2608.19760)-style executed replay is small, decisive, and explicitly flagged as open.
2. **Verification dose under a budget constraint.** Itkin optimizes corrector *placement* at fixed dose; Chen shows *dose is endogenous and model-dependent*. Nobody solves placement and endogenous dose jointly.
3. **Task-class boundary of verification instability.** Itkin's grounded-vs-signed-belief distinction is asserted in one sentence and never mapped.
4. **Over-verification as a coordination failure.** Chen finds *"persistent over-verification is associated with indecision rather than safety"*; [The Verifier Tax](https://arxiv.org/abs/2603.19328) finds safe success rate **below 5%** despite intercepting up to **94%** of non-compliant actions. Nobody models the resulting welfare loss.

---

## 4. Searches that returned nothing (recorded per instructions)

- Every arXiv API query combining `abs:"LLM agents"` with `abs:"equilibrium"`, `abs:"mechanism design"` + `abs:verification`, and `abs:blame` + `abs:"LLM agents"` returned a **confirmed empty feed**. (Separately, a batch of `ti:` queries returned *no HTTP body at all* — throttling, not zero results; those were retried and are not counted as nulls.)
- `abs:"LLM" AND abs:agent AND abs:"mechanism design" AND abs:verification` → 2 results, **both irrelevant** (an aerodynamics MDO agent, a geometry-reasoning paper). There is no LLM-agent verification mechanism-design literature to speak of.
- WebSearch for an adversary allocating a persuasion budget across multiple verifier panel members to flip a minimum number of votes: the search engine itself reported *"none exactly match the specific scenario you described."* Nearest hits are single-judge attacks ([Bandit-Guided Style Manipulation](https://arxiv.org/abs/2605.26156), [Adversarial Persuasion on Fact-Checking](https://arxiv.org/abs/2601.16890)). **This is the cleanest null in the survey** and it underwrites Candidate 2.
- No search surfaced any paper connecting a *measured* failure-attribution error rate to a *sanctioning or reputation* mechanism. Underwrites Candidate 1.

---

## 5. Three candidate gaps

### Candidate 1 — Sanctioning under unreliable blame: the attribution-accuracy threshold for cooperation

**Gap statement.** *No work takes a measured, calibrated failure-attribution signal — with its real
34%-accuracy and its known set-valued ambiguity — and uses it to drive a reputation/sanctioning
mechanism over a population of LLM agents, while also deriving the attribution-accuracy threshold
below which sanctioning destroys more cooperation than it sustains.*

**Why it matters.** Every proposed remedy for multi-agent LLM failure — reputation, retirement of
bad skills, routing away from unreliable agents, [SafeEvolve](https://arxiv.org/abs/2608.12851)'s
"safety-aware retirement," [SHE](https://arxiv.org/abs/2608.09885)'s per-artifact responsibility
assignment — silently assumes blame can be assigned. The 2026 literature has now measured that
assumption and found it wanting: 34.11% macro-average attribution accuracy, credit signals at chance,
and failures that *"often admit multiple plausible attributions."* Under classical
indirect-reciprocity results, misattributed punishment is not merely wasteful; it is actively
destabilizing, because honest agents get sanctioned and the incentive to cooperate inverts. Whether
the deployed 34% sits above or below that inversion point is currently **unknown and unasked**, and
it determines whether the entire reputation-based governance agenda for agent systems is viable.

**Falsifiable hypothesis.** In a repeated multi-agent task population where an attribution module
assigns blame after each failure, there exists a critical attribution accuracy `a*` such that for
`a > a*` sanctioning raises population task success above the no-sanctioning baseline, and for
`a < a*` it lowers it below baseline. `a*` is (i) strictly greater than chance, (ii) *increasing* in
sanction severity, and (iii) **substantially above the ~0.34 accuracy of current attribution
methods** on long-horizon traces — so that naively deployed blame-based reputation is net-harmful at
today's attribution quality. Secondary hypothesis: replacing the point-valued blame label with a
**conformal prediction set** ([Conformal Agent Error Attribution](https://arxiv.org/abs/2605.06788))
and sanctioning proportionally over the set lowers `a*`, restoring net benefit at current accuracy.

**Decisive experiment.** A population of N≈20 LLM agents repeatedly solves multi-step tasks in
teams of 3–5 sampled from the population. Some agents are seeded as genuinely unreliable. After each
team failure, an attribution module names a culprit; reputation updates; low-reputation agents are
sampled less often. The key move is that **attribution accuracy `a` is an experimental knob**: a
synthetic oracle-plus-noise attributor sweeps `a` from 1.0 down to chance, and *real* attributors
(direct-prompt baseline, an AgentLocate-style multi-evaluator, and a conformal set-valued variant)
are dropped in at their measured accuracies to locate where they fall relative to `a*`. Outcome
measures: population success rate, honest-agent sanction rate, and reputation–reliability rank
correlation. The result is falsified if population success is monotone in sanction strength
regardless of `a`, i.e. if no threshold exists.

**AAMAS fit.** Squarely in *Trust, Reputation and Norms* (primary) and *Learning and Adaptation* /
*Coordination* (secondary). It is the canonical AAMAS question — reputation under noisy observation —
asked about a signal whose noise level the LLM-agent community has just finished measuring. The
theory framing (a threshold on observation fidelity for sanctioning to sustain cooperation) is
familiar to AAMAS reviewers, which is an asset, not a liability: the novelty is the coupling and the
empirical location of today's systems relative to the threshold.

**4-week feasibility: HIGH.** The simulation is small-model-friendly: 20 agents × ~150 rounds × a few
attribution sweeps is well inside a modest API budget, and the accuracy sweep — the load-bearing
part — uses a *synthetic* attributor and costs essentially nothing. Existing annotated traces
([Who&When](https://arxiv.org/abs/2607.09996), TrajErrBench, SearchAuditBench) supply ground-truth
culprits so real-attributor accuracy can be calibrated offline rather than re-derived. No training,
no human subjects. Main risk is tuning a task environment where cooperation can visibly collapse;
mitigated by reusing an existing social-dilemma harness such as
[CoopEval](https://arxiv.org/abs/2604.15267).

**Occupancy check (adversarial).**
- [RepuNet — Reputation as a Solution to Cooperation Collapse in LLM-based MASs](https://arxiv.org/abs/2505.05029): builds dual-level reputation from *"direct interactions and indirect gossip."* **Does NOT** take blame from an attribution algorithm, does not model attribution error, and derives no accuracy threshold — its agents observe outcomes directly.
- [CARP — Paying for Honesty Without Knowing the Truth](https://arxiv.org/abs/2607.28330): the strongest threat. It designs a reputation-penalty mechanism explicitly for a noisy signal — *"it observes only a noisy, biased complaint signal, never the ground truth"* — with a deadband. **But** the noisy signal is an exogenous *consumer complaint* about product fabrication in a marketplace; there is no multi-agent collaborative failure, no attribution module, no culprit-identification error, and no characterization of a critical accuracy. CARP tolerates noise; it does not locate the threshold or ask whether today's attributors clear it.
- [Ev-Trust](https://arxiv.org/abs/2512.16167): has the formal machinery I would want — *"replicator dynamics with a noisy best response micro-foundation,"* proofs of asymptotic stability of cooperative ESS, and *"explicit threshold conditions for maintaining cooperative equilibria."* **Does NOT** derive those thresholds with respect to *attribution accuracy*; its trust signal is a semantic cross-validation gate, its noise is "endogenous stochasticity," and its domain is service fraud, not collaborative task failure. This paper is the closest formal neighbor and must be cited as the method template I am extending to a different signal.
- [Conformal Agent Error Attribution](https://arxiv.org/abs/2605.06788): supplies distribution-free coverage guarantees on attribution sets. **Does NOT** use them for governance — *"use prediction sets to rollback MAS to correct their own errors."* Rollback, not sanctioning. This is my proposed mechanism's key ingredient, sitting unused.

**Verdict: OPEN.** The adversarial read is that CARP + Ev-Trust together cover "reputation under noise, formally." My defense is that neither connects to the *attribution* literature, and the paper's punchline — *current attribution is below the threshold at which sanctioning helps* — is a claim neither can make. Risk is moderate and the framing must foreground the attribution coupling, not reputation-under-noise in general.

---

### Candidate 2 — Verifier panels against a strategic persuader: when adding verifiers makes you wronger

**Gap statement.** *No work models the verified agent as a strategic adversary allocating a
persuasion budget across the members of an LLM verifier panel, while also deriving and validating
the condition under which enlarging the panel lowers its accuracy, and designing an aggregation rule
robust to targeted persuasion.*

**Why it matters.** Two 2026 results are on a collision course that nobody has staged.
[Jagged Judges](https://arxiv.org/abs/2608.12645) shows a *single* judge flips **25–71%** under
static pushback and **62–91%** against an adaptive persuader, and — critically — *"the pressure that
succeeds in changing a judgment is almost always harmful with respect to the ground truth."*
[Nine Judges](https://arxiv.org/abs/2605.29800) shows a nine-judge panel carries about **two**
independent votes because errors are correlated. Put them together and a panel is not a robust
aggregator but a small number of *correlated, individually flippable* targets. Meanwhile
[Blind to the Pivotal Vote](https://arxiv.org/abs/2608.06940) proves the entire decision-relevant
action sits on **one-vote-margin queries**. An adversary who knows this does not need to persuade
the panel — it needs to persuade the *pivotal* member on *pivotal* queries. Panel-based verification
is the load-bearing safety mechanism in agentic deployment, debate, and RLAIF reward models, and its
adversarial breaking point is unmeasured.

**Falsifiable hypothesis.** Against a persuasion-budget-constrained adversary that targets pivotal
ballots, LLM verifier-panel accuracy is **non-monotone in panel size**: beyond a critical size `k*`,
adding judges *reduces* accuracy, because correlated persuadability means each added judge
contributes more attackable surface than independent signal. Formally, the attacker's cost to flip a
majority grows sub-linearly in `k` while the panel's effective sample size saturates (Kish `n_eff`
plateaus near 2), so the crossing exists. Corollary: a **margin-aware aggregation rule** that
escalates one-vote-margin queries to an independent-evidence channel — rather than to more judges —
restores monotonicity at a fraction of the cost.

**Decisive experiment.** Panels of k ∈ {1,3,5,7,9} frontier judges evaluate items from an existing
labeled set with known ground truth (a code benchmark plus an NLI set, mirroring the two occupancy
papers so numbers are directly comparable). An attacker LLM, given a fixed budget of B persuasion
messages per item, chooses *which judges to pressure* under three policies: uniform, random-B, and
pivotal-targeted (informed by a first-round ballot read). Measure panel accuracy vs. k under each
policy, plus attacker cost-to-flip. Then swap in the margin-aware escalation rule and re-measure.
The hypothesis is falsified if accuracy is monotone increasing in k under the pivotal-targeted
attack, i.e. if panel expansion is genuinely protective.

**AAMAS fit.** *Coordination, Cooperation and Collective Decision Making* — this is adversarial
information aggregation and a Condorcet-jury failure under a strategic manipulator — with a strong
secondary claim on *Mechanism Design* (the robust aggregation rule) and *Trust*. AAMAS has a deep
tradition in manipulation of voting rules; framing the verifier panel as a manipulable social-choice
mechanism gives reviewers exactly the handle they want, and the LLM instantiation supplies the
novelty.

**4-week feasibility: HIGH.** This is the cheapest of the three. It is pure API inference — no
training, no environment build, no human subjects. Panels of nine judges over a few hundred items
with several attack policies is a few hundred thousand short calls; a pilot at k ≤ 5 on 200 items
across two benchmarks is comfortably a few days of wall-clock. The pivotal-targeting insight also
*reduces* cost, since only margin-1 queries need the expensive attack. Ground truth already exists.
Main risk: frontier judges may be robust enough that flips are rare on easy items — mitigated by
selecting items near the panel's decision boundary, which is precisely the pivotal set.

**Occupancy check (adversarial).**
- [Jagged Judges](https://arxiv.org/abs/2608.12645): measures flip rates including against *"adversarial persuaders"* (62–91%). **Does NOT** aggregate — it studies judges individually, has no panel, no budget allocation, no panel-size analysis, and proposes no aggregation rule. Its single predictive signal is *"the strength of the judge population's initial majority"*, which is suggestive of my mechanism but undeveloped.
- [Nine Judges, Two Effective Votes](https://arxiv.org/abs/2605.29800): establishes correlated-error collapse and that *"neither adding more judges nor using smarter aggregation algorithms helps."* **Does NOT** involve any adversary — its errors are natural, not induced — so its "adding judges doesn't help" is a *saturation* claim, whereas mine is a strictly stronger *non-monotonicity under attack* claim.
- [Blind to the Pivotal Vote](https://arxiv.org/abs/2608.06940): proves gains concentrate on one-vote-margin queries (*"+10.4 to +23.3 percentage points ... and is exactly zero elsewhere"*) and gives a substitution rule. **Does NOT** consider an adversary at all; it uses the pivotal-set insight *defensively for cost reduction*. I use the same arithmetic *offensively*, which is a genuine reframing, and then defend against it. This is the most dangerous neighbor — I must cite it as the source of the pivotal-set characterization and be explicit that the adversarial direction is new.
- [CW-POR](https://arxiv.org/abs/2504.00374): single judge, single turn, one persuader, no panel — *"the same LLM architecture serves as judge."* **Does NOT** address aggregation or budget allocation.
- [Bandit-Guided Style Manipulation Attacks on LLM Judges](https://arxiv.org/abs/2605.26156): optimizes an attack against a judge. **Does NOT** target a panel or exploit pivotality.

**Verdict: OPEN, and the search engine independently confirmed no exact match.** The honest risk is
that this reads as "Blind to the Pivotal Vote, but adversarial" — a reviewer could call it
incremental. The defense is the non-monotonicity result: nobody has shown that panel expansion is
*actively harmful* under attack, and that is a genuinely surprising, decision-relevant claim.

---

### Candidate 3 — Skill reuse as a contagion externality: epidemic thresholds and quarantine mechanism design

**Gap statement.** *No work treats an agent's skill-reuse intensity as a strategic choice that
imposes a poisoning-contagion externality on a shared library population, while also deriving the
epidemic threshold as a function of the population's reuse policy and designing an incentive or
quarantine mechanism that sits on the resulting containment–capability frontier.*

**Why it matters.** [EvoMal](https://arxiv.org/abs/2608.25776) established that agent-authored
malicious skills self-replicate — the library grows to **4.9–9.0×** the planted count, and after
removing *every* planted skill, Qwen3 still shows **68%** self-contamination at cascade round five,
with 3 of 6 models still infected. Its branching-process corollary states that self-replication
requires **both** high imitation rate **and** re-retrievability of authored skills. That is an R₀
condition — but derived for one agent and one library, with no strategic actors. The externality is
obvious once named: reusing others' skills is *individually* rational (it is the entire value
proposition of a skill ecosystem) but raises the population's contagion rate. EvoMal's own proposed
defense makes the tradeoff explicit — *"structural quarantine offers stronger containment at the
cost of limiting self-evolution"* — and nobody has characterized that frontier. The safety
newsletter flags the closest question as *"close to untouched": how to define and inspect safety of
a set.*

**Falsifiable hypothesis.** In a population of agents sharing a skill library, there is a critical
reuse intensity `ρ*` (equivalently a critical retrieval breadth) above which a single poisoned skill
achieves R₀ > 1 and reaches endemic prevalence, and below which it dies out — and the **selfishly
optimal** reuse intensity chosen by each agent maximizing its own task success **exceeds `ρ*`**, so
the population reliably self-organizes into the epidemic regime. Corollary: a provenance-diversity
gate (the mechanism [PoisonedEvolution](https://arxiv.org/abs/2608.05563) proposes but does not
analyze) shifts `ρ*` upward enough to make the selfish optimum safe, at a measurable and bounded
capability cost.

**Decisive experiment.** A population of ~15 coding agents shares a retrievable skill library over
successive task rounds. One skill is seeded with an EvoMal-style benign-but-marked banner (an inert
traceable marker, not a live payload — no functional malware is needed, and the marker is the *only*
thing measured). Sweep retrieval breadth / reuse probability `ρ` and measure marker prevalence over
rounds, fitting the invasion threshold. Then let agents *choose* `ρ` to maximize their own success
and check whether the selected `ρ` lands above the fitted `ρ*`. Finally, impose a provenance-diversity
gate and a quarantine rule and trace the containment–capability frontier. Falsified if prevalence is
monotone-but-thresholdless in `ρ`, or if the selfish optimum already sits below `ρ*` (in which case
the externality is benign and there is no mechanism to design).

**AAMAS fit.** *Emergent Behaviour / Engineering Multiagent Systems* and *Mechanism Design*, with a
clear *Norms and Sanctioning* reading (quarantine as a sanctioning institution). Contagion on a
population with a social-dilemma structure and a designed institution is a very AAMAS-shaped object.

**4-week feasibility: MEDIUM.** Lower than the other two, and I want to be honest about why. The
epidemiological sweep needs many rounds × many agents × real coding tasks, and each agent-round is
an expensive long-horizon rollout — this is the only candidate with a genuine compute concern. The
mitigations are real but each costs fidelity: use a cheap task suite rather than SWE-bench Verified,
use an inert marker so no execution sandbox is required, and fit the threshold from early-invasion
generations rather than running to endemic equilibrium (which is what
[Reliability-Contagion](https://arxiv.org/abs/2607.21912) does — its LLM validation is only
*"36 new closed-world tasks"* with a *"balanced 12-task subset continued to full cascades"*, i.e. a
deliberately small confirmation of analytically-derived directional predictions). A 3-week pilot can
plausibly deliver the analytic threshold + a small confirmatory sweep, but not the full mechanism
evaluation. **Medium, contingent on doing the theory first and the LLM run as confirmation.**

**Occupancy check (adversarial).**
- [Reliability-Contagion Feasibility in LLM Multi-Agent Networks](https://arxiv.org/abs/2607.21912): the most serious threat and I nearly abandoned this candidate over it. It has SEIR compartments, *"early-invasion condition for heterogeneous communication networks,"* a coupling to a majority-vote reliability benchmark, opposing graph constraints, and LLM validation. **Does NOT** involve any persistent artifact — it propagates *erroneous claims over communication edges within a task*, which vanish when the task ends. EvoMal's whole point is the opposite: contamination that *"does not disappear when you stop the exposure."* Critically, it also has **no strategic agents and no mechanism design** — connectivity is chosen by a designer, not by self-interested agents, so there is no externality and no social dilemma. My candidate's two load-bearing elements (persistent artifacts, endogenous reuse choice) are both absent.
- [EvoMal](https://arxiv.org/abs/2608.25776): has the branching-process condition and the persistence measurements. **Does NOT** have a population of distinct agents, any strategic choice, or any threshold as a function of a reuse policy; its counter-prompt defense is a prompt, not a mechanism, and it never characterizes the containment–capability frontier it names.
- [PoisonedEvolution](https://arxiv.org/abs/2608.05563): proposes the provenance-diversity gate I would analyze, and gives the sharp non-linearity (1 poisoned record → 20%, 2 records → 84%). **Does NOT** analyze the gate formally, and *"evaluation stops at artifact generation"* — no population dynamics.
- [Safety in Self-Evolving LLM Agent Systems](https://arxiv.org/abs/2606.23075): names population contagion via shared memory pools. **Does NOT** model it — it is a threats-and-case-studies survey.
- [Socially-Weighted Alignment](https://arxiv.org/abs/2602.14471): treats negative externalities among LLM agents as a social dilemma. **Does NOT** address poisoning, contagion, or skill libraries.

**Verdict: OPEN but the narrowest margin of the three.** [Reliability-Contagion](https://arxiv.org/abs/2607.21912)
occupies "epidemic threshold for LLM multi-agent error spread" outright, and a reviewer who knows it
will need the persistence/strategic distinction made in the abstract, not the related-work section.
Combined with the medium feasibility, I rank this third.

---

## 6. Ranking

1. **Candidate 1 (sanctioning under unreliable blame)** — best combination of a genuine literature seam (two large, active, mutually-ignorant literatures), a surprising falsifiable claim, high feasibility, and dead-center AAMAS fit.
2. **Candidate 2 (verifier panels vs. strategic persuader)** — cheapest and fastest, sharpest single result (non-monotonicity), cleanest null in the search record; slightly higher "incremental" risk against [Blind to the Pivotal Vote](https://arxiv.org/abs/2608.06940).
3. **Candidate 3 (skill-reuse contagion externality)** — most ambitious and most AAMAS-native in shape, but partially shadowed by [Reliability-Contagion](https://arxiv.org/abs/2607.21912) and the only one with real compute risk in a 4-week window.
