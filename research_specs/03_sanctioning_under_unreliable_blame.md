# Sanctioning Under Unreliable Blame

## Decision

**Recommended target for AAMAS 2027 main track.** Selected over six other surviving candidates after a four-slice traversal of ~1,360 corpus entries (see `_survey/` notes and the occupancy table below).

Working title: **When Blame Is Wrong More Often Than Right: Accuracy Thresholds for Reputation and Sanctioning in LLM Agent Systems**

Primary area: **COINE** (Coordination, Organizations, Institutions, Norms and Ethics - trust, reputation, normative systems). Secondary: **GTEP**, **EMAS**.

## One-paragraph thesis

LLM multi-agent systems are starting to govern themselves: reputation scores, agent exclusion, trust-weighted routing, and rollback are all now driven by automated failure attribution. But attribution is measured to be very weak - the originating benchmark reports the best method at **53.5% accuracy for naming the responsible agent and 14.2% for locating the decisive step, with some methods below random**. No work asks the obvious governance question that follows: *below what attribution accuracy does sanctioning make a system worse than not sanctioning at all?* We define that threshold `a*`, derive it for a repeated team-formation model, show that it sits far above today's attainable accuracy, and show that the failure is not merely noise but *directional* - attribution error correlates with agent role and verbosity, so naive blame-based reputation systematically purges a structural class of agent rather than the incompetent one. We then show that a conformal abstention layer, an ingredient that already exists but is currently spent on rollback, lowers `a*` enough to make sanctioning safe.

## The gap

### Precise gap statement

> No work drives a reputation or sanctioning mechanism from a *measured* failure-attribution signal and characterizes the accuracy threshold below which sanctioning is net-harmful.

Both halves exist independently. Reputation and sanctioning for LLM agent systems exist. Measured attribution accuracy exists. The dependency between them is unexamined: every reputation mechanism for LLM agents assumes it can observe who misbehaved.

### Why it is a real gap

The corpus traversal found, across 278 unique papers in the trust/verification/safety/attribution slice: **zero** reputation systems, **zero** norms or sanctioning work, **zero** equilibrium or stability analysis, and only 3 papers touching mechanism design. Across the multi-agent/architecture slice (326 entries), the same terms returned zero. The formal treatments that do exist sit *outside* the LLM-agent corpus entirely.

Meanwhile 2026 produced an unusually rich set of *measured failure rates of the field's own trust instruments* - attribution ceilings, judges flipping under pushback, credit signals at chance - and nothing downstream consumes those numbers. This gap lives exactly in that disconnect.

## Formal core

A population of `N` agents is repeatedly assigned to teams of size `k` on tasks. Agent `i` has latent competence `theta_i`. A team fails with probability determined by its members' competence.

On failure, an attribution mechanism `A` returns a blamed agent. Define its accuracy

```
a = P(A(trace) = true culprit | team failed)
```

with the residual mass distributed over innocent members according to an error kernel `E`. Reputation `r_i` decays on blame; the sanction is reduced selection probability (soft exclusion) or removal (hard exclusion).

Let `W_s(a)` be steady-state expected task success under sanctioning at attribution accuracy `a`, and `W_0` the same without sanctioning. Define

```
a* = inf { a : W_s(a) >= W_0 }
```

**Claim to prove:** `a*` is bounded below by a quantity increasing in team size `k`, in sanction severity, and in the *bias* of the error kernel `E`. Under a uniform error kernel, sanctioning degrades gracefully. Under a biased kernel - blame concentrating on the most verbose, most active, or last-acting agent, all documented attribution biases - sanctioning can invert the competence signal, making the system strictly worse than random exclusion.

That inversion result, if it holds, is the paper.

## Research questions and hypotheses

| ID | Question / hypothesis | Decisive evidence |
|---|---|---|
| RQ1 | Where is `a*` for realistic team sizes and sanction severities? | Closed form or numerically solved threshold, validated against simulation. |
| H1 | `a*` lies substantially above the ~0.535 agent-level accuracy currently attainable. | Threshold curve vs. measured attributor accuracy, with CIs. |
| H2 | Attribution error is **biased**, not uniform, w.r.t. agent role, verbosity, and turn position. | Error kernel estimated from real attributor outputs on real failure traces. |
| H3 | Under a biased kernel, blame-based sanctioning underperforms *random* exclusion at matched exclusion rate. | The strongest falsifiable claim; matched-rate comparison. |
| H4 | Conformal abstention (sanction only on singleton or small prediction sets) lowers `a*` below attainable accuracy. | Threshold with and without the abstention layer. |
| RQ2 | Does the effect survive when the attributor is the same model family as the agents? | Self-attribution ablation. |

## Experimental design

The load-bearing sweep is **synthetic and nearly free**, which is what makes this viable in four weeks.

**Stage 1 - Synthetic attributor (week 1-2).** Attribution accuracy `a` and error-kernel bias become *experimental knobs*. Simulate the population model directly, sweep `a`, `k`, sanction severity, and kernel bias. Locate `a*` and test H1/H3 at scale with no API cost. This stage alone produces the headline threshold result.

**Stage 2 - Real attributors dropped in (week 2-3).** Take published failure traces with ground-truth annotations, run real attribution methods, measure their actual accuracy *and estimate the error kernel* (H2). Insert each real attributor into the population model at its measured operating point and confirm the simulation's prediction.

**Stage 3 - Conformal layer (week 3).** Add the abstention layer, recompute `a*`, test H4.

**Stage 4 - Live confirmation (week 4, optional).** A small live multi-agent run with reputation-driven routing, to confirm the effect is not an artifact of the simulator. Explicitly scoped as confirmation, not as the main evidence.

## Baselines

- No sanctioning.
- Random exclusion at matched exclusion rate (**the critical baseline** - this is what H3 is measured against).
- Oracle attribution (`a = 1`) as ceiling.
- Blame-based reputation with each real attributor.
- Conformal-gated sanctioning.
- Direct behavior observation, the RepuNet assumption, as an upper reference showing what is lost when blame must be inferred.

## Metrics

- `a*` under each configuration, with confidence intervals.
- Steady-state task success and welfare vs. `a`.
- Exclusion precision and recall against latent competence.
- Competence-signal correlation: does reputation track `theta_i`, and does it *invert*?
- Error-kernel bias coefficients by role, verbosity, turn position.
- Coverage/abstention rate and cost of the conformal layer.

## Falsification gates

Stop or narrow if:

1. `a*` turns out to be below 0.3, meaning current attribution is already good enough and the concern is moot.
2. The estimated error kernel is close to uniform, killing the inversion result and reducing the paper to a graceful-degradation curve.
3. Blame-based sanctioning beats random exclusion at every measured accuracy, killing H3.
4. The result is entirely driven by the simulator's team-formation assumptions and does not survive Stage 4.
5. The conformal layer's abstention rate is so high that sanctioning never fires.

Gates 1-3 are checkable in week 2 on synthetic data alone. That is the main reason this candidate was ranked first for a four-week runway.

## Occupancy table

| Nearest work | What it does | What it does not do |
|---|---|---|
| [RepuNet, AAMAS 2026](https://arxiv.org/abs/2505.05029) | Reputation dynamics + network rewiring for LLM MAS; agents form assessments via direct interaction and gossip. | Agents **observe behavior directly**. No inferred blame, no attribution error, no accuracy threshold. This is the paper to distinguish from first - the AAMAS PC knows it. |
| [Who&When / automated failure attribution](https://arxiv.org/abs/2505.00212) | Establishes the task and the benchmark; reports 53.5% agent-level, 14.2% step-level, some methods below random. | Purely a measurement paper. Never asks what the number implies for governance. Supplies our key constant. |
| [Conformal Agent Error Attribution](https://arxiv.org/abs/2605.06788) | Filtration-based conformal prediction over agent trajectories with distribution-free coverage; contiguous prediction sets. | Uses the sets for **rollback and debugging** - "use prediction sets to rollback MAS to correct their own errors." Never for reputation or sanctioning. Our key ingredient, sitting unused. |
| [Blind to the Pivotal Vote](https://arxiv.org/abs/2608.06940) | Pivotal-set arithmetic for judge panels. | Defensive, no adversary, no reputation, different object. |
| [GateMem](https://arxiv.org/abs/2606.18829) | Multi-principal shared-memory governance. | Access control and authorization, not incentives or blame. |
| [Governed Collaborative Memory](https://arxiv.org/abs/2605.04264) | Memory governance as a selection regime; provenance and version lineage. | A design-agenda Viewpoint. No incentives, no strategic agents, no thresholds. |
| Classical trust/reputation theory (Sabater-Sierra, Jøsang, Hendrikx et al.) | Robustness of reputation to noisy and unfair ratings. | Pre-LLM, assumes rating noise is exogenous and typically unbiased. Does not model attribution over long agent traces, nor role-correlated error. **Must be cited; this is where a reviewer will look for prior art.** |

## Risks, ranked

1. **The classical trust-and-reputation literature already contains a version of this threshold.** Highest risk by far. Reputation robustness to unfair or noisy ratings is a mature pre-LLM field. The defensible increment must be that attribution error here is *structured by agent role and trace position* and is measured, not assumed. **Do this literature check before writing a line of code** - it is the one that can kill the project.
2. **The inversion result (H3) fails and the kernel is near-uniform.** Then the paper degrades to a threshold curve, which is a Findings paper rather than a main-track one.
3. **Reviewers read it as simulation-only.** Stage 2 with real attributors and a real estimated kernel is what prevents this. It is not optional.
4. **RepuNet adjacency.** Manageable and arguably helpful - building on the venue's own recent paper - provided the distinction (observed behavior vs. inferred blame) is made in the abstract.
5. **Attribution accuracy improves fast enough to moot the concern.** Partially self-defending: the threshold framework remains the contribution even as `a` rises, and gate 1 catches this early.

## Four-week plan against the 8 October deadline

- **By 17 Sep:** register authors on OpenReview. This is a hard gate and is easy to miss.
- **Week 1 (8-14 Sep):** classical trust/reputation prior-art check (risk 1, kill-or-proceed). Build the population simulator. First `a*` curve.
- **Week 2 (15-21 Sep):** full synthetic sweep, kernel-bias conditions, H1/H3 resolved. Gates 1-3 evaluated. Go/no-go decision point.
- **Week 3 (22-28 Sep):** real attributors, kernel estimation, conformal layer. H2/H4.
- **Week 4 (29 Sep-8 Oct):** abstract in by **1 Oct**, writing, optional Stage 4, submission by **8 Oct**.

## Fallback

If the week-2 gate fails or the timeline slips, the same idea fits the **AAMAS 2027 Blue Sky Ideas track**: 4 pages, explicitly no experimental results required, abstract **5 Nov** and paper **12 Nov 2026**. That is a five-week extension and a genuinely appropriate venue for a threshold-and-agenda argument.

## Venue facts (verified from official pages, 7 Sep 2026)

- Main track: 8 pages + unlimited references, LaTeX template, **double-blind**.
- Author registration **17 Sep 2026**; abstract **1 Oct**; paper **8 Oct**; rebuttal 20-24 Nov; notification 21 Dec 2026.
- Findings of AAMAS 2027: automatic consideration for non-selected papers unless authors opt out; same length and format.
- Dual submission to archival venues prohibited; **arXiv preprints and non-archival workshops are explicitly exempt**.
- Supplementary material: single zip, max 25MB; reviewers not obliged to read it.
