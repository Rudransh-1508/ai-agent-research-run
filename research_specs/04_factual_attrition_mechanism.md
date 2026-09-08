# Mechanism-Isolation of Factual Attrition in Multi-Agent LLM Deliberation

## Decision

**Recommended target for AAMAS 2027.** Selected from nine candidates hunted across three
LLM-substrate-specific directions (context/attention mechanics, trained-bias propagation, in-context
peer imitation) after five prior candidates - all "import a classical AAMAS concept into LLM agents"
in shape - were killed by pre-2020 economics, game-theory, and control-theory results. This candidate
is structurally different: it is grounded in a quantity that only exists for transformer-based agents
(attention allocation over a fixed KV-cache), which is precisely why it has no classical antecedent to
be scooped by.

Working title: **Knowing Versus Saying: Disentangling Attentional Loss from Motivated Suppression in
Multi-Agent LLM Deliberation**

Primary area: **GAAI** (agent architectures, reasoning in LLM-based systems). Secondary: **COINE**
(deliberation, collective decision quality), **LEARN**.

## One-paragraph thesis

A June 2026 paper shows multi-agent LLM deliberation erases up to 72% of issue-critical facts while
agents converge on a shared stance - but it measures "erasure" only by whether a fact is spontaneously
re-mentioned, so it cannot tell apart two mechanistically distinct failures: the fact has fallen out of
the model's effective attention-weighted working set (attentional loss, a substrate-level failure), or
the fact is still fully know­able on direct query but the model has stopped volunteering it as the
group converges (motivated suppression, a social/behavioral failure). A second June 2026 paper shows
that context-compaction silently drops *imposed, top-down* safety constraints in *single-agent*
settings - but never touches *peer-established, bottom-up* commitments reached mid-deliberation by a
group. Nobody has added an explicit-recall probe to disambiguate the first pair, nobody has measured
whether compaction adds an attrition increment on top of the already-high no-compaction baseline for
mutually agreed content specifically, and nobody has compared shared-transcript against
separate-context-relay architectures on the same metric. This paper runs all three.

## The gap

### Precise gap statement

> No work disambiguates attentional loss from motivated non-surfacing as the cause of factual attrition
> in multi-agent LLM deliberation, and no work measures whether context compaction compounds attrition
> specifically for peer-agreed (rather than top-down-imposed) commitments.

### Why it is a real gap, and why it survives where five others didn't

The dissociation this paper runs is only a coherent experiment because attention weight over a
fixed-size KV cache is an independently inspectable, computable quantity. For a human subject in a
classical Janis-style groupthink or Asch-conformity setting, there is no way to separately ask "is the
suppressed fact still in your attention-weighted working memory, right now, as a measurable quantity"
from "will you say it out loud" - those are the same undifferentiated black box. For a transformer
agent they are not: one is a behavioral probe (direct-recall accuracy), the other is architecturally
inspectable (attention allocation, and indirectly, degradation with token-distance). That is the
property that makes this candidate resistant to the failure mode that killed the previous five - there
is no 1962-2016 theory of "knowing versus saying" for a system whose knowing and saying can be
independently instrumented, because no such system existed before transformers.

The two anchor papers establish the phenomenon but explicitly do not run this disambiguation:

- **"The Deliberative Illusion" (arXiv:2606.03032, Jun 2026)**, verbatim: *"multi-agent discussion
  erases up to 72% of issue-critical facts... agents can agree more while knowing less."* Confirmed by
  direct methodology check: one continuous full transcript, no compaction, attrition measured purely
  via spontaneous-mention frequency. Never asks agents to directly recall an "erased" fact.
- **"Governance Decay" (arXiv:2606.22528, Jun 2026)**, verbatim: *"violation rises from 0% with the
  policy in full context to 30% after compaction, reaching 59% for some models... when the constraint
  survives the summary, violation remains 0%, but when it is dropped, violation reaches 38%."*
  Confirmed single-agent, confirmed the dropped content is a top-down imposed policy, not a bottom-up
  peer commitment. No multi-agent negotiation tested.

## Research questions and hypotheses

| ID | Question / hypothesis | Decisive evidence |
|---|---|---|
| H1 | A meaningful fraction of "erased" facts (no spontaneous mention) are in fact still fully recoverable via direct query, with no accuracy loss vs. round 1 - attrition is dominated by non-surfacing, not forgetting. | Explicit-recall probe accuracy vs. round-1 baseline. |
| H1-alt | Recall accuracy degrades on the same curve (as a function of token-distance from introduction) as spontaneous-mention attrition - the two are statistically indistinguishable, meaning attrition is attentional, not social. | Regression comparing the two decay curves. This is the falsifying direction and is explicitly the paper's fallback result if H1 fails - see Falsification below. |
| H2 | Compaction adds a statistically significant attrition increment on top of the no-compaction baseline, concentrated on facts introduced earliest in the transcript. | 2x2x2 ablation, compaction-on vs. off, controlling for distance. |
| H3 | Shared-transcript and separate-context-relay architectures produce different attrition *profiles* even at equal total attrition rate - relay attrition is front-loaded at the summarization boundary, shared-transcript attrition is smoothly distance-decaying. | Profile-shape comparison across architecture conditions. |

## Ablation design (3 weeks, API-only, no training, no human subjects)

**Base task.** Replicate or closely reconstruct the Deliberative Illusion setup: N agents, each holding
some subset of issue-critical atomic facts on an ethical/policy scenario, K rounds of open discussion,
a final consensus stance.

**2x2x2 design, each factor independently toggled:**

1. **Recall probe (on/off).** After each round, for a sampled subset of facts not yet spontaneously
   mentioned that round, either do nothing (baseline replication) or inject a direct query to the
   holding agent - "restate what you know about X" - before the next round, scored against ground
   truth. **Must be between-subjects, not within-subjects** - probing is itself an intervention that
   could re-activate the fact and contaminate the very attrition curve being measured. This is the
   single most important design discipline in the whole pilot.
2. **Compaction (on/off).** Full-transcript relay vs. periodic LLM-summarization compaction every M
   rounds, using Governance Decay's deterministic grading logic adapted from tool-call-violation
   grading to fact-survival grading.
3. **Architecture (shared / relay).** Single shared transcript vs. separate per-agent context with an
   explicit relay/summary message passed between agents each round.

**Dependent variables.** Spontaneous-mention attrition (for direct comparability to Deliberative
Illusion), direct-recall accuracy, final-stance factual grounding. Token-distance from fact
introduction to measurement point is a continuous covariate throughout, enabling a regression
decomposition of attrition into distance-explained, compaction-explained, and architecture-explained
components.

**Content-neutrality requirement, built in from the start, not bolted on.** Facts must be
interchangeable, non-narratively-salient, and equally surprising, to allow the design to distinguish
attentional/distance-driven loss (predicted content-neutral) from Bartlett-style
schema/surprisingness-driven distortion (predicted to track narrative salience, not raw distance). A
sharp reviewer will raise Bartlett (1932) immediately; the stimulus design must have already answered
it by construction.

## Nearest work

| Paper | What it does | What it does not do |
|---|---|---|
| [Deliberative Illusion, arXiv:2606.03032](https://arxiv.org/abs/2606.03032) (Jun 2026) | Establishes the 72% attrition phenomenon and the spontaneous-mention metric, full-shared-transcript, no compaction. | No recall probe, no attentional/suppression disambiguation, no compaction condition, no architecture comparison. |
| [Governance Decay, arXiv:2606.22528](https://arxiv.org/abs/2606.22528) (Jun 2026) | Establishes compaction as a mechanism for silent content loss, clean causal ablation (swap summarizers), a working mitigation (Constraint Pinning). | Confirmed single-agent only; top-down imposed policy only, not peer-established commitments; no recall-vs-in-situ dissociation. |
| [PINE, arXiv:2407.01100](https://arxiv.org/abs/2407.01100) (NeurIPS 2024) | Mechanistically attributes position bias to causal attention + RoPE; training-free fix for pairwise/listwise judge and RAG-QA. | Single-shot document comparison, not iterative multi-agent deliberation with evolving group commitments over rounds. |

## Falsification gates

1. If H1-alt holds (recall degrades on the same curve as spontaneous mention), the "motivated
   suppression" half collapses. **This is not fatal** - the paper narrows to a smaller but still clean,
   still falsifiable, still publishable finding: "attrition in multi-agent deliberation is attentional,
   not social." State this fallback in the paper design from the start, not as a post-hoc rescue.
2. If the recall probe itself measurably perturbs downstream deliberation dynamics (detectable by
   comparing probed vs. unprobed condition's stance trajectories), the between-subjects design must be
   tightened further before H1/H1-alt can be trusted.
3. If compaction shows no attrition increment over the no-compaction baseline (H2 fails), report it as
   a negative result - Governance Decay's single-agent effect not transferring to peer commitments is
   itself informative.

## Risks, ranked

1. **Recency of both anchor papers.** Both are June 2026. A second, independent literature check
   should run again in the week before submission to confirm nothing newer has closed this specific
   dissociation in the interim - this is standard hygiene given how fast this exact sub-area is moving,
   not a special weakness of this candidate.
2. **Bartlett (1932) serial reproduction / Janis (1972) groupthink** are real classical antecedents for
   the general phenomenon of group-discussion distorting recall. They are dissociable in principle
   (Bartlett predicts schema-driven, surprisingness-dependent distortion; this candidate predicts
   distance-driven, content-neutral loss) but the dissociation must be built into the stimulus design
   from day one, per the content-neutrality requirement above.
3. **The probe-contamination risk** (point 2 under Falsification) adds real design and compute cost
   within the 3-week window and needs to be budgeted for explicitly, not discovered late.
4. **This hunt ran a single self-check pass**, not the two-round adversarial process that killed the
   previous five candidates. It is the strongest survivor of a genuinely LLM-native search, but has not
   yet been independently red-teamed the way spec 01 and the four "classical import" candidates were.
   Recommended: one more targeted adversarial pass specifically on this candidate (Bartlett/Janis
   exposure, and a fresh search for anything published between the anchor papers' June 2026 date and
   now) before committing the full 3 weeks.

## AAMAS contribution package

1. A mechanistic decomposition of "attrition" into attentional and social components, using a
   quantity (recall-vs-mention dissociation) that is only measurable because of the transformer
   substrate.
2. A compaction ablation isolating the peer-commitment case, extending Governance Decay's single-agent
   result.
3. An architecture comparison (shared transcript vs. relay) showing attrition *shape*, not just rate,
   depends on design choices that are currently made ad hoc by system builders with no formal
   treatment.
4. A concrete, actionable implication for multi-agent system design: if attrition is attentional
   (H1-alt), the fix is architectural (e.g., periodic re-injection); if social (H1), the fix is
   procedural (e.g., mandatory recall checkpoints) - the paper's result determines which of two very
   different engineering responses is correct, which is a genuinely useful finding either way.

## Immediate pilot (week 1)

Before the full 2x2x2 sweep: reconstruct the Deliberative Illusion baseline (no compaction, shared
transcript, no probe) on a small scenario set and confirm attrition rates in the same range as
reported (up to 72%). Then add the recall probe alone (still no compaction, still shared transcript)
on the same scenarios and get a first read on H1 vs. H1-alt before committing to the full ablation
matrix. If the probe shows near-zero recall degradation (fully supporting H1), proceed to full scope.
If recall degrades in lockstep with spontaneous mention (H1-alt), pivot immediately to the narrower
"attrition is attentional" framing and simplify the remaining two weeks accordingly - do not run the
full matrix hoping the picture changes.
