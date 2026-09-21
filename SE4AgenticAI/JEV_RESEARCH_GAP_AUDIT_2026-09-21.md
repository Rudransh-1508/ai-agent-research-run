# Jev / System One models: research gap audit for SE4AgenticAI 2026 and MASO 2026

Date: 2026-09-21. Deadline for both venues: **2026-10-10** (19 days).
Sources inspected: TypeSafe launch post, `docs.typesafe.ai` (full page index via `llms.txt`), `evals.typesafe.ai`, and the public community corpus (232 catalogued projects in `yibie/awesome-jev`, plus five independent evaluation repos read directly).

## 0. Bottom line

Jev is a strong paper subject, but **not for the paper everyone is writing.** Within ~10 days of launch, the grey literature already contains at least six independent calibration/ECE studies. A "we measured Jev's calibration" submission is scooped by GitHub repos a reviewer can find in one search, even though none of them is peer reviewed.

The gap that is real, large, and squarely inside both venues' topic lists is this:

> Practitioners have already wired a probabilistic, remote, vendor-hosted decision model into the **authorization path of coding agents** - as PreToolUse hooks, permission gates, pre-commit gates, and stop-hooks. At least 22 such gates are public. No one has evaluated this as a software-engineering construct: not its failure modes, not its fail-open behaviour, not its threshold provenance, not its behaviour under adversarial tool-call inputs, not what happens when the gate's HTTP call fails.

That is an empirical SE paper with a mineable corpus, a cheap experiment, and an asymmetric-risk framing nobody in the grey literature has used. Recommended target: **SE4AgenticAI regular paper (8-10 pages)**, with MASO as the second submission of a different angle, not the same paper.

---

## 1. What Jev actually is (verified)

| Property | Verified detail |
|---|---|
| Category | "System One model" - TypeSafe's own coinage, not an established category. Named for Jevons, not an acronym. |
| Interface | `POST /v1/systemone`. Send *state* + a batch of *typed questions*, evaluated in parallel in one call. |
| Primitives | **Choice** (one of N options, cardinality <= 255), **Score** (ordered levels), **Noul** (probability that a yes/no claim is true). |
| Output | The typed answer, a full `probabilities` distribution, and a scalar `confidence`. No free text - the model cannot generate strings. |
| Confidence | *Not* an independent signal. It is "a statistic computed from the probability distribution the answer already gives you". For 3 options the doc gives `(3 * p_max - 1) / 2` - i.e. a rescaled max-probability. |
| Training | RLCD - "Reinforcement Learning for Calibrated Decisions", optimising epistemically honest probabilities rather than preference or verifiable reward. |
| Claims | Cannot hallucinate; never a type error; always reports confidence; consistent on similar inputs; 70-500 ms end to end; $42/Btok input, output free. |
| Limits | 64k tokens/request (32k state + longest question), English best, text only, 1200 rpm, "rate limits adjusting dynamically". |
| Version | `jev-1.13.0`, aliases `jev-latest` and `jev-preview`. |
| Access | Early access, plus third-party routes already used by independent evaluators: OpenRouter, Vercel AI Gateway, Cloudflare AI Gateway. |

### 1.1 The two admissions that create the research space

**(a) No calibration guarantee in the docs.** The confidence page ends with: "The correct threshold values depend on your domain and the performance of the model for your use case. Start with conservative thresholds, test with your own data, and adjust." The entire product thesis is calibration; the documentation devolves validation of it onto the integrator and supplies no method.

**(b) A published jaggedness page** (`model-jaggedness/jev-1.13`) admits nine failure modes with no numbers attached, including three that matter enormously for gate use:
- *Adversarial content*: "does not treat data as hostile by default" - injected instructions can influence output.
- *Structural invariants*: not guaranteed, explicitly `P(noul) != 1 - P(not_noul)`.
- *Context pollution*: large state with irrelevant detail degrades accuracy.

Meanwhile the documented architectural patterns - `composite-scoring`, `fan-out`, `hierarchical-classification`, `confidence-routing` - all combine several independent question results in code, and composite-scoring explicitly assumes dimensions are independent and that a score of 4 means the same thing across dimensions. **The vendor recommends composition patterns while disclaiming the invariants those patterns need.** That is an unmeasured architectural contract.

---

## 2. Scoop map: what the grey literature already covers

This section exists so we do not write a scooped paper. All of the following are public and datable before our submission.

| Work | What it measured | Why it constrains us |
|---|---|---|
| `priorbench/jev` | Pre-registered, 5,721 calls, 21 experiments, 50 predictions registered in advance (26 confirmed, 21 falsified). 95.9% zero-shot on a 400-item set; ~430 ms fixed cost; accuracy-above-threshold flat 0.50-0.95 then jumps at 0.99; model **always answers** - cake recipes scored 0.94 confidence as technical issues, random text 0.97. | Kills any generic "does confidence detect nonsense" claim, and sets a methodological bar (pre-registration) we should match. |
| `scienthoon/jev-ood-calibration` | 900 rule-generated tickets + 3 public benchmarks. ECE 0.107 vs a 0.024 noise floor. Per-primitive sign of miscalibration: **Choice overconfident, Score badly overconfident (44.7% acc), Boolean underconfident.** The `confidence` field performed *worse* than raw probabilities. Cost ~$0.06. | Kills "we compute Jev's ECE". Also gives us a citable per-primitive prior we can build on. |
| `keduseworku/Jev-Calibration` | Platt scaling and isotonic regression; raw ECE 0.064-0.160 -> 0.006-0.018 post-isotonic. | Kills "recalibration helps" as a contribution. |
| `FirasSX914/calibre` | Banking77 confidence routing; 80.2% at $0.103/500 decisions. | Kills generic confidence-routing-on-a-public-benchmark. |
| `themsquared/jev-benchmark` | **Closest competitor.** Tool-call risk classification, n=60 hand-labelled (34 clear / 14 ambiguous / 12 adversarial). 91.7% overall, 100% clear, **71.4% ambiguous**, 91.7% adversarial. p50 421.6 ms. Wrong answers never at confidence 1.0. Author's own stated limits: n too small, no frontier-LLM baseline. | This is our nearest neighbour. We must be visibly beyond it: larger and differently constructed corpus, asymmetric cost metrics, baselines, and the systems questions it never asks. |
| `eugeniughelbur/jev-gate` + `jev-engineering` | Ships a 300-injection test against **its own** gate, results dated 2026-09-20. | Establishes injection-of-gates as a live concern - and that it has been done once, unsystematically, against a single implementation. Cite it; do not repeat it. |
| ~22 further public gate implementations | `jev-axi` (shell destructiveness, 44/44 on own tests), `pi-verdict` (allow/ask/deny), `jev-guard`, `jev-git` (secret screening pre-commit), `harshwasan/jev-sentinel`, `hermes-jev-approvals`, Vercel `fx`'s builtin `typesafe_permission_reviewer`, `jev-belay`, `limpet`, `wakegate`, `Abide` (10/39 flags confirmed correct). | **This is the corpus.** Each reports at best its own smoke tests. None is compared to any other. No one has looked across them. |

**Pattern across all of it:** every study is a single-call classification benchmark with symmetric accuracy. Nothing studies Jev *as a component inside a running agent's control flow*, which is exactly what SE4AgenticAI and MASO are about.

---

## 3. Ranked gaps

### Gap 1 - Confidence-gated tool-call authorization (RECOMMENDED)

**Claim to test:** a calibrated decision model has become a de-facto authorization mechanism for coding agents, and the engineering discipline around it is absent.

Four distinct sub-results, none of which exists anywhere:

1. **Corpus study of deployed gates.** Mine the ~22 public gate repos: what typed question is asked, which primitive, what threshold constant, where the threshold came from (documented? derived? copied from the docs' 0.5/0.9 example?), what the action set is, what state is passed to the model, whether the raw command is passed unsanitised. Expect the finding: thresholds are undocumented magic constants copied from the vendor's illustrative example, and the docs explicitly say those must be domain-tuned.
2. **Fail-open analysis - the strongest systems result.** These gates put a remote HTTPS call on the agent's permission path under a dynamic 1200 rpm limit. Read every gate's error path: on timeout, 429, 5xx, or malformed response, does the agent proceed? A gate that fails open turns a vendor rate-limit into a silent authorization bypass; a gate that fails closed turns it into an agent-wide halt. This is checkable statically, costs nothing, and is a genuine, novel, reportable engineering finding.
3. **Asymmetric-cost evaluation.** Every existing study reports symmetric accuracy/ECE. Authorization is not symmetric: a false *allow* on `kubectl delete namespace prod` is unbounded, a false *deny* costs one human interrupt. Re-score on a cost-sensitive selective-prediction framing and derive the threshold that actually minimises expected loss. `themsquared`'s 71.4% on ambiguous cases is precisely the region gates operate in. Report where the docs' 0.9 threshold lands against the loss-optimal one.
4. **Injection through gate state.** The gate's input is attacker-reachable (a diff, a tool argument, a file the agent just read). The vendor concedes the model "does not treat data as hostile by default". Test whether confidence *falls* on successful injections - `priorbench` already showed confidence stays ~0.97 on pure noise, so the prior is that it will not, which breaks the entire confidence-routing premise for adversarial inputs. Generalise `jev-gate`'s single-implementation 300-call test across several gate designs.

**Why it survives review:** it is an empirical engineering study of agent software with a public artifact - the same contribution shape as the accepted 2025 SE4AgenticAI empirical mining paper - but on a subject that did not exist a month ago. The mining half needs no API key at all, which de-risks the deadline.

**Provisional title:** *Confidence as an Authorization Boundary: How Coding Agents Delegate Permission Decisions to a Calibrated Decision Model.*

### Gap 2 - Compositional calibration of the vendor's own patterns

Per-question calibration has now been measured several times. **Pipeline-level calibration has not.** Real agents chain gates: `fan-out` then `composite-scoring`, or `hierarchical-classification` by parallel beam search. Composite-scoring assumes cross-dimension independence and cross-dimension score comparability; the jaggedness page disclaims structural invariants and gives `P(noul) != 1 - P(not_noul)` as a documented violation.

Measure: ECE of a composed decision versus ECE of its parts; the magnitude of the invariant violation on complement pairs; error growth down a hierarchical classification chain. Clean, cheap, theoretically motivated, and directly falsifies or validates a shipped architectural pattern. Strong second paper; weaker than Gap 1 only because it has no corpus and no security stakes.

### Gap 3 - The threshold as an unversioned dependency (SE maintenance framing)

`jev-latest` is a moving alias. A threshold constant tuned against `jev-1.13.0` is a magic number coupled to a remote model that can change underneath it, and the vendor already ships `jev-preview` alongside. The question is a testing question with no current answer: **how do you write a regression test for a dependency that returns a probability?** You cannot assert equality; you need distributional assertions and a calibration canary in CI. Mine the corpus for whether anyone pins a version (early evidence: `themsquared` benchmarks both aliases and finds a 43 ms latency gap, suggesting they are not identical in practice). Best folded into Gap 1 as a section rather than run alone - it risks being a position paper without a version bump to observe.

### Gap 4 - Replacing LLM-as-judge with typed gates: a refactoring experience report

Take an existing open-source agent in our own harness, refactor its judge/routing calls to Jev, and report measured accuracy/latency/cost/token deltas plus the refactoring cost. LangChain and Vercel have already published directionally similar walkthroughs, so the novelty is thin unless the finding is negative or conditional. The one genuinely interesting variant is negative-result-shaped: `jev-reranker` results in the wild already include "Jev reranking is not a free win" (33,047 entries, did not beat vector retrieval). **Demote** unless Gap 1 collapses.

### Gap 5 - MASO angle: typed calibrated decisions as an organizational delegation boundary

MASO's call is about theoretical, operational, and **governance** gaps of deploying heterogeneous agents in organizations. Reframe the same substrate: a confidence threshold is a machine-readable statement of *how much authority an agent holds before a human must be consulted*. That connects directly to the existing `maso/policy_preserving_delegation_research_proposal.md` in this repo. The contribution is a delegation model where escalation is governed by calibrated uncertainty, plus the empirical observation that the thresholds encoding organizational authority are currently undocumented constants copied from vendor sample code. Positioning matters: MASO wants governance and organizational framing, SE4AgenticAI wants engineering evidence. **Do not submit the same PDF to both.**

---

## 4. Venue fit

| | SE4AgenticAI 2026 | MASO 2026 |
|---|---|---|
| Co-located | IEEE Big Data 2026, Phoenix, Dec 14-17 | PRIMA 2026, Kumamoto, Dec 14 |
| Deadline | Oct 10, 2026 | Oct 10, 2026 (23:59 AoE) |
| Notification | Oct 31 | Nov 12 |
| Format | IEEE 2-column; short 3-4 pp, regular 8-10 pp, refs included | Not published on the CFP page - **must be confirmed with organizers** |
| Edition | 2nd (2025 program had 3 papers) | 1st |
| Fit of Gap 1 | Very strong - matches "testing and verification", "human-in-the-loop", "standardized agent-tool protocols", "observability and audit trails", "empirical studies of frameworks" | Moderate |
| Fit of Gap 5 | Moderate | Very strong |

Both are first/second-edition workshops with no published acceptance rates. Per the existing `PAST_PAPERS_AND_SUBMISSION_STRATEGY_2026-09-09.md` analysis, the 2025 SE4AgenticAI program accepted a repository-mining empirical study and a bounded architectural feasibility case - Gap 1 is the same contribution shape as the former, on a fresher subject. That is a reason for confidence in *fit*, not a predicted acceptance probability.

---

## 5. 19-day plan with kill gates

**Day 1-2 - Access gate.** Get a working key by any of: TypeSafe early access, OpenRouter, Vercel AI Gateway, Cloudflare AI Gateway. Independent evaluators have used all three. Confirm `jev-1.13.0` echoes back in the response, and pin it. *Kill condition: no route to the model by day 3 -> drop the measurement half and ship the corpus + fail-open study as a short paper, which needs no key.*

**Day 2-4 - Corpus freeze.** Enumerate public gates, apply written inclusion criteria (must gate a real action, must be runnable, must be dated before Oct 1), pin commit SHAs, extract question/primitive/threshold/action/error-path per gate. This half is deterministic and is the paper's floor.

**Day 4-5 - Pre-registration.** Write down the predictions before collecting. `priorbench` did this and it is the single cheapest credibility multiplier available; a reviewer who finds the grey literature will find that repo too.

**Day 5-11 - Measurement.** Build the tool-call corpus substantially beyond n=60 and with a *documented* construction procedure, since `themsquared`'s ambiguous-case labels are self-declared as disputable. Include held-out adversarial items authored after threshold selection. Run the asymmetric-loss analysis and the injection battery. Budget: the OOD study cost $0.06; assume single-digit dollars.

**Day 11-15 - Write.** Use `research-paper-writing`. IEEE 2-column, target regular paper; fall back to short if a gate fails.

**Day 15-18 - Artifact + internal review.** Public repo with raw JSONL, recount script, exact model id, dates and gateway used.

**Day 18-19 - Submit**, SE4AgenticAI workshop 59 on the Big Data CyberChair.

Run MASO only if Gap 5 can be written as a genuinely different paper. Two rushed submissions are worse than one good one.

## 6. Threats to validity to state in the paper, not discover in review

- Single vendor, single model version, a model days old and actively changing.
- Rate limits are explicitly "adjusting dynamically", so latency and throughput numbers are dated observations, not model properties. Record date, region, and gateway - `priorbench` could not separate gateway from model latency and said so.
- Public gate repos are a convenience sample of early adopters, not a population. Do not report a "percentage of gates that fail open" as if it generalises to industry.
- Ground truth for allow/ask/deny is a policy judgement. Publish the labelling rubric and inter-rater agreement, or the 71.4%-ambiguous problem recurs as a reviewer objection.
- `confidence` is a deterministic function of `probabilities`, so treat it as one signal, not two, and report both as `scienthoon` found the derived field performs worse.

## 7. What would make me abandon Gap 1

If the corpus survey shows gates are overwhelmingly toys with no real action wired up, or if every gate already fails closed and documents its threshold, the interesting findings evaporate. That is checkable in about two days for zero dollars, which is why the corpus work runs first.
