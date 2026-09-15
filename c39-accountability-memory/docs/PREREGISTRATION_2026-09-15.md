# Pre-registration — the agent-record experiment

**Written 2026-09-15, before the harness was written and before any run.**
Hashed into `artifact_hashes.json` at that point, so the predictions below are
on the record ahead of the results. This project has already falsified one of
its own fitted formulas; the point of writing this first is that the experiment
can embarrass us.

---

## 1. What the experiment is for

Everything in the paper so far is a statement about records chosen *optimally*.
The obvious objection — the one three reviewers would raise — is that no real
system chooses its record that way. A coordinator keeps a count, or a paragraph,
or the last thing each sub-agent said, and it keeps it under observation noise.

So the experiment evaluates **named compaction mechanisms that nobody designed
to be optimal**, measures where each lands on the reconstruction/accountability
plane, and asks whether the theory predicts those landings.

The margin of each mechanism is measured *using Theorem 3* — the elimination
theorem turns an otherwise bilinear search over payment rules into one LP per
agent. The experiment therefore also exercises the paper's own main tool.

## 2. Mechanisms to be evaluated

Each maps an effort profile (or its noisy observation) to a record label.

| id | mechanism | labels $K$ |
|---|---|---|
| `full` | retain the whole profile | $2^n$ |
| `count` | retain $\lvert S\rvert$ — "how many agents succeeded" | $n+1$ |
| `threshold` | retain $\mathbf{1}\{\lvert S\rvert \ge \lceil n/2\rceil\}$ | 2 |
| `topk` | retain which $k$ agents contributed, not how much | $\binom{n}{k}$ |
| `prefix` | retain the first $m$ agents' bits, drop the rest | $2^m$ |
| `hash` | hash the profile into $K$ buckets (generic lossy compaction) | $K$ |
| `kmedian` | the reconstruction-optimal $K$-label record | $K$ |
| `flat` | the 2-dominating construction of Lemma 8 | $\gamma_2(Q_n)$ |

Under noise, effort $S_i$ is observed as $X_i$ with $\Pr[X_i \ne S_i] = \eta$,
and the mechanism sees $X$ rather than $S$ while reconstruction and payment are
still judged against the true $S$.

## 3. Predictions

Marked **[D]** if it is a derivation — it *must* hold if the theory and the code
are both right, so failure means a bug or a false theorem — and **[U]** if the
outcome is genuinely unknown to us at the time of writing.

**P1 [D] No mechanism beats the frontier.** For every mechanism, the measured
pair $(D, \gamma)$ satisfies $D \ge \Dopt(K,\gamma)$ for its own $K$. A strict
violation falsifies either Theorem 5/9 or the simulator.

**P2 [D] Nothing below the threshold is flat.** No mechanism with
$K < \gamma_2(Q_n)$ simultaneously achieves $D = D_0(K)$ and $\gamma > 0$.

**P3 [D] The construction is flat and the optimal quantiser is not.** At
$K = \gamma_2(Q_n)$, `flat` achieves $D = D_0(K)$ with $\gamma \ge 1/2$, while
`kmedian` at the same $K$ may achieve $D = D_0(K)$ with $\gamma = 0$ — same
distortion, no accountability. This is the paper's whole point and should be
visible as two points at the same $K$ and the same $D$ with different $\gamma$.

**P4 [U] Where aggregates actually fail.** Section 6 currently says an aggregate
such as "how many agents succeeded" is "far inside the tension regime". We
predict the failure is **not** a loss of margin. `count` changes by exactly one
whenever a single agent deviates, so we expect $\gamma(\texttt{count}) = 1$ in
the noiseless case, and the cost to appear entirely in reconstruction:
$D(\texttt{count}) > D_0(n+1)$, strictly. At $n = 3$ we have computed
$D(\texttt{count}) = 1.0$ against $D_0(4) = 0.5$, so we predict a factor of
about two, and we predict the gap widens with $n$.

*If P4 holds, Section 6's wording is wrong and must change* — aggregates are
reconstruction-poor at their label budget, not accountability-poor. We would
rather find that here than in a review.

**P5 [U] Noise degrades margin continuously, and faster than distortion.** As
$\eta$ rises from 0, we predict $\gamma$ of every mechanism falls continuously
(no cliff), and that the relative loss in $\gamma$ exceeds the relative loss in
reconstruction quality at the same $\eta$. We do not know the shape.

**P6 [U] Noise raises the effective threshold.** We predict that under noise the
smallest $K$ at which any mechanism is flat is strictly larger than
$\gamma_2(Q_n)$, i.e. observation noise costs labels. We have not computed this
and it may be false — noise could instead make flatness impossible at every $K$,
which would be a cleaner and more interesting outcome.

**P7 [U] The tilted-prior collapse shows up in mechanisms.** Under a product
Bernoulli$(q)$ prior with $q \ne 1/2$, we predict no mechanism with
$K < 2^n - (n-1)$ is flat, matching Corollary 12, and in particular that
`flat` — built for the uniform case — stops being flat once the prior tilts.

**P8 [U] The design rule survives contact.** Retaining one bit per agent should
dominate every other mechanism at comparable $K$ on the margin axis. We predict
`prefix` with $m < n$ has $\gamma = 0$ exactly (the dropped agents are invisible),
which would make the rule "a per-agent witness for *every* agent, or none".

## 4. What would count as a failure

* Any **[D]** prediction failing — that is a bug or a broken theorem, and the
  paper does not go out until it is resolved.
* P4 failing in the direction that `count` has $\gamma = 0$ — that would mean
  Section 6's current wording is right and this pre-registration is wrong. We
  record it either way.
* Every mechanism landing exactly on the frontier would be suspicious rather
  than reassuring: it would suggest the mechanisms are being fitted rather than
  evaluated.

## 5. Analysis rules, fixed in advance

* $n \in \{3, 5\}$ evaluated **exactly** by enumerating all $2^n$ profiles — no
  sampling, so no sampling error and no seed to choose. $n = 7$ where it runs.
* Noise levels $\eta \in \{0, 0.05, 0.1, 0.2\}$, fixed now.
* $\gamma$ is computed by the Theorem 3 LP, not by searching payment rules.
* Every number reported in the paper from this experiment comes from the JSON
  the harness writes, and is checked by `audit_paper_numbers.py` like every
  other number.
* No mechanism will be added after seeing results in order to improve the
  picture. If one is added, it is listed here as a post-hoc addition.

---

# Addendum — the episode-level experiment

**Written 2026-09-15, after the mechanism experiment of §3–§5 was run and
scored, and before the episode harness was written.** Section 5 above forbids
adding mechanisms after seeing results without declaring them; this is that
declaration. It is a *second, separate* experiment, not an extension of the
first, and the first one's results stand as scored.

## Why a second experiment

The first experiment compresses the effort profile itself. That concedes the
very abstraction most open to attack: that an agent's execution trace can be
summarised by one effort bit. It tests the theory against its own model.

This one puts an episode in between. A coordinator fans out to $n$ sub-agents;
each has a controlled ground-truth effort bit; each returns an artifact whose
content depends stochastically on that effort; the coordinator emits a final
output. Records then compress **the trace**, not the effort profile, and the
induced encoder $\enc(\text{label} \mid S)$ is something we measure rather than
define.

## Record schemes

| id | what survives |
|---|---|
| `full_trace` | every agent's artifact, in full, attributed |
| `per_agent_bit` | one success bit per agent, attributed |
| `per_agent_coarse` | one bit per agent, but only for agents above median quality |
| `global_summary` | the multiset of artifacts — content kept, **identity destroyed** |
| `aggregate` | how many sub-tasks succeeded |
| `final_output` | only the coordinator's output |

## Predictions

**E1 [D]** Every scheme lands on or above the frontier for its own $K$; no
episode-level record beats Theorem 5 or Theorem 9.

**E2 [U]** `global_summary` keeps *more content* than `per_agent_bit` but has a
**strictly smaller** margin. If identity rather than volume is what accountability
needs, this is where it shows. We do not know whether its margin is zero or
merely small; we predict small and decaying in $n$, by the same mixture
cancellation that gave the aggregate $1/n$.

**E3 [U]** The ordering of schemes by margin follows *per-agent identity
retained*, not total bits retained. Concretely we predict
$\gamma(\texttt{full\_trace}) \ge \gamma(\texttt{per\_agent\_bit}) >
\gamma(\texttt{global\_summary}) \ge \gamma(\texttt{aggregate}) \ge
\gamma(\texttt{final\_output})$, even though `global_summary` carries far more
bits than `per_agent_bit`.

**E4 [U]** `final_output` has margin $0$ or indistinguishable from it.

**E5 [U]** `per_agent_coarse` — a per-agent witness for *some* agents — has
margin $0$, extending the first experiment's `prefix` finding from a synthetic
truncation to a plausible retention policy.

**E6 [D]** The exact enumeration and a Monte-Carlo run over episodes agree to
sampling error, which is what licenses reporting the exact numbers as the
result of "running many episodes".

## Rules

* Agents are conditionally independent given $S$, so the induced encoder is
  computed **exactly** by enumerating outcome tuples; a sampled run is also
  reported as a cross-check (E6), with its seed fixed at 20260915.
* Margin is again computed via Theorem 3, not by searching payment rules.
* If E3 fails, the design rule in Section 6 is wrong and must be rewritten.

---

# Addendum 2 — the identity-vs-volume hypothesis

**Written 2026-09-15, after the episode experiment was scored, before the
mechanisms and the sweep below were written.** Third declared addition; the two
earlier experiments stand as already scored.

## The hypothesis, made quantitative

**H1.** *Compression that removes agent identity causes a disproportionate loss
in accountability relative to its reduction in storage.*

"Disproportionate" needs a number, so we fix one now. Storage is $\log_2 K$ bits,
not $K$. For an identity-preserving record $R$ and an identity-destroying record
$R'$, define

    relative margin loss    = (gamma(R) - gamma(R')) / gamma(R)
    relative storage saving = (log2 K(R) - log2 K(R')) / log2 K(R)

and let their ratio be the **identity price**. H1 says the identity price is
$> 1$, and we predict it is $\gg 1$ --- at least $3$ at every $n$ tested.

From the numbers already in hand at $n=5$ (per-agent bit against the artifact
multiset) the ratio is about $5.9$. That case is therefore **not** evidence for
H1; it is where H1 came from. The test is whether it holds across $n$ and across
mechanism pairs we have not looked at.

**H1a [U]** The identity price exceeds $3$ for every identity-preserving /
identity-destroying pair at every $n$ in $\{3,4,5,6,7\}$.

**H1b [U]** The identity price grows with $n$. We are unsure: the margin of an
identity-destroying record decays roughly like $1/n$, while its storage saving is
roughly constant in relative terms, which would make it grow --- but the
identity-preserving margin is capped at $1/2$ by the construction, so it could
flatten instead.

## New mechanisms, declared before running

Chosen because a real coordinator would plausibly implement them, not because we
expect a particular answer.

| id | what survives | why it is realistic |
|---|---|---|
| `recency_k` | full artifacts for the last $k$ agents only | context-window eviction is recency-ordered |
| `role_rollup` | per-role completion counts, agents split into two roles | team-level rollups are standard reporting |
| `quality_only` | the best quality seen and how many completed | the archetypal summary-statistics record |

**H2 [U]** `recency_k` has margin exactly $0$, like `prefix`, because the dropped
agents are fixed in advance. **H3 [U]** `role_rollup` has margin about $1/|role|$
rather than $1/n$ --- coarser identity is still identity, so splitting the team
into two named halves should recover roughly a factor of two over a global count.

## Rules

* Mechanisms above are fixed now; no further additions after seeing results.
* $n \in \{3,4,5,6,7\}$, exact enumeration, no sampling.
* Storage is always reported as $\log_2 K$ bits alongside $K$.
* If H1a fails at any $n$, the identity-vs-volume claim is downgraded from a
  headline contribution to an observation at $n = 3,5$, and Section 8's rule R1
  is rewritten.

---

# Addendum 3 — the LLM-agent experiment

**Written 2026-09-15, before the harness was written and before any model was
called.** Fourth declared addition. The three earlier experiments stand as
already scored.

## Why this one exists

Every result so far is synthetic. The episode experiment put a coordinator and
artifacts between the effort profile and the record, but the artifacts were
draws from a two-point distribution we chose. The obvious objection is that
nothing about real agent output has been tested, and that the ordering of record
types might be an artifact of the generative model rather than of what the
records retain. This runs the same comparison on artifacts produced by an actual
language model.

## Design

Three agents, so the effort profile ranges over all $2^3 = 8$ values and every
teammate profile is visited. Each agent is assigned a distinct sub-question over
supplied source material and produces a **real artifact**:

* $S_i = 1$ — the agent is given the material and asked to answer properly.
* $S_i = 0$ — the agent is asked to produce a confident, plausible answer
  **without** consulting the material. This is shirking in the sense the paper
  means: the artifact still looks like work.

A coordinator reads the artifacts and emits a final output with a ship/no-ship
decision. The record types are the ones under test:

| record | keeps identity? |
|---|---|
| `full_trace` — every artifact, attributed | yes |
| `per_agent_summary` — a model-written summary per agent, attributed | yes |
| `global_summary` — one model-written summary of the whole episode | no |
| `artifact_multiset` — every artifact, shuffled, attribution stripped | no |
| `final_output` — the coordinator's output alone | no |

`artifact_multiset` is the decisive one: it contains **exactly the same text** as
`full_trace` and differs only in whether you can tell who wrote what.

## Measurement

A judge model reads a record and predicts each agent's effort bit, giving
$\hat S$. Compaction and judge together induce a channel on the cube, estimated
from episodes, and then the paper's own instruments apply unchanged:
$D = \E[\dH(S,\hat S)]$, and $\gamma$ from the Theorem 3 LP on the estimated
channel. Storage is the record's actual size in bytes, not a label count.

## Predictions

**L1 [U]** The margin ordering matches the synthetic episode experiment:
`full_trace` $\ge$ `per_agent_summary` $>$ `artifact_multiset` $\ge$
`global_summary` $\ge$ `final_output`.

**L2 [U]** `artifact_multiset` has a strictly smaller margin than `full_trace`
despite containing the same text. This is the cleanest possible test of the
identity claim: same bytes, same content, attribution removed. We predict the
margin drops by at least a third.

**L3 [U]** `final_output` has a margin near zero but not exactly zero, as in the
synthetic case.

**L4 [U]** Reconstruction error $D$ is *not* ordered the same way as $\gamma$.
We expect `artifact_multiset` to reconstruct the *number* of shirkers about as
well as `full_trace` while failing to say *which*, so its $D$ should be much
closer to `full_trace`'s than its margin is.

**L5 [U]** The judge is imperfect even on `full_trace`, so $\gamma$ there will be
well below the $0.5$ of the synthetic construction. We are not predicting a
value. If it is near zero the experiment has failed to produce a usable signal
and we will say so rather than reporting the ordering of noise.

## Rules fixed in advance

* Model, temperature and seed pinned and recorded in the output JSON.
* Every episode's raw artifacts are saved, so the judging can be re-run or
  re-scored without re-generating.
* 8 profiles, equal episodes per profile; the count is set by budget and
  recorded. Any episode that errors is retried once, then recorded as failed.
* If L5's failure condition triggers, the experiment is reported as
  inconclusive. It will not be quietly dropped.

## Addendum 3a — declared amendment, before any episode was run

The key available is Codestral-issued: it authenticates only against
`codestral.mistral.ai` and returns 429 on `api.mistral.ai`. Codestral is a
code-specialised model, and the task registered above is prose incident
analysis whose judge must distinguish generic writing from writing that cites
specifics. That is the weakest possible match, and the judge is the measurement
instrument, so a poor judge would trigger L5's failure condition for a reason
that says nothing about the paper.

**The task therefore changes to multi-agent code review, and this is recorded
before a single episode was generated.** Three agents each review a distinct
aspect of one code change:

* $S_i = 1$ — the agent is given the diff and must cite specific identifiers or
  line numbers.
* $S_i = 0$ — the agent is given only the aspect to review, and produces
  confident generic review advice without the code, not admitting it.

Everything else is unchanged: the same five records, the same judge-induced
channel, the same instruments, and predictions **L1 through L5 stand exactly as
written**. The decisive comparison is still `full_trace` against
`artifact_multiset` -- identical text, attribution removed.

One prediction is added, specific to the new task:

**L6 [U]** Shirking is *easier to detect* here than in the prose task, because a
review that never names a symbol from the diff is conspicuous. We therefore
expect a larger $\gamma$ on `full_trace` than the prose design would have given,
and we flag that this makes the experiment a more favourable setting for
attribution than a typical deployment -- an upper bound on what a record buys,
not a typical value.

---

## Addendum 4 (2026-09-15, post-hoc — a retraction, not a prediction)

This addendum records a **correction to the theory**, not a new prediction. It
is appended rather than edited into the text above, so the original registration
stays readable as written.

**Theorem 11 and Corollary 12 were false and are withdrawn.** They claimed that
for every tilted product prior $K_{\text{flat}} = 2^n - (n-1)$, hence that the
free compression ratio collapses to $1 + O(n2^{-n})$. Counterexamples:

| | claimed | true |
|---|---|---|
| $n=3$, $q=0.7$ | 6 | **4** (witness $C=\{011,101,110,111\}$, $D=D_0(4)=0.2430$, $\gamma=1/3$) |
| $n=4$, $q=0.7$ | 13 | **5** (witness $C=\{0111,1011,1101,1110,1111\}$, $D=D_0(5)=0.4401$, $\gamma=1/4$) |

A tilted prior can require **fewer** labels than the uniform one. The withdrawn
claim pointed the wrong way.

**P7 is unaffected as a scored prediction.** P7 predicted that no mechanism at
$K=\gamma_2(Q_n)$ is flat under a tilt; that observation stands and was
confirmed. What is withdrawn is the *explanation* the paper attached to it. The
mechanisms in Table 4 were all designed against the uniform prior, so their
failure under a tilt is a statement about those mechanisms, not about where the
tilted threshold lies. §7.1 now says so.

**How it was missed, which is the part worth registering.** The error was a
single step of reading: Lemma 3' gives "$\ge 2$ centres at the vertex's *own
nearest distance*", and we read it as "$\ge 2$ centres at distance 1", i.e.
2-dominating. Those coincide only when the optimal code is dominating — true
for the uniform prior above $\gamma(Q_n)$ (so Theorem 9 survives), false for a
tilt, where the optimal code concentrates on heavy profiles and leaves light
ones at distance 2.

Both verification routes — the `prior_threshold.py` MILP and `verify_all.py`
block G, which share no code — encoded that same wrong condition. **They agreed,
and their agreement was worthless.** Independent implementation buys
independence of *implementation*, not of *specification*. The error surfaced
only when a test asked a structurally different question: relax $\gamma$ and ask
an LP directly whether $D_0(K)$ is attainable, rather than re-testing the proxy.

The withdrawn scripts and artifacts are kept unmodified under
`experiments/withdrawn/` and `results/withdrawn/` as the evidence for that
methodological point. `verify_all.py` block G now constructs the
counterexamples instead, and the check count drops from 145 to 99.
