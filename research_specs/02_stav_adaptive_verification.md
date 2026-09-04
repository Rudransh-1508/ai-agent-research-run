# Stability-Constrained Adaptive Verification (STAV)

## Decision

**Rank: #2 overall; high-upside, high-gate project.**

Working title: **When Trust Becomes a Controller: Stability-Constrained Adaptive Verification for LLM-Agent Networks**

This project is worth exploring only in the order stated here: measure behavior first, test whether a realistic unstable region exists second, and develop a controller only after those gates pass. It must not be sold as “delays are bad” or “trust graphs are new.”

## One-paragraph thesis

LLM agents can save resources by verifying collaborators less after a successful history. This creates endogenous verification: past outcomes alter trust; trust changes audit frequency; audit frequency changes which failures become visible; and delayed observations later update trust. We test whether this empirically measured feedback law creates oscillations or cascading failures in a region where a verification-budget-matched fixed verifier remains stable. STAV projects a proposed adaptive audit action onto a robustly safe region, preserving adaptive savings when possible and falling back to a certified fixed policy otherwise.

## Precise gap

> No identified work jointly (i) estimates LLM costly-verification behavior as a trust-update law, (ii) uses that independently fitted law in a delayed error-propagation model, (iii) predicts held-out stability transitions, and (iv) constrains the resulting adaptive verifier with a robust stability guarantee.

This is the only defensible novelty claim. Each individual component is already occupied:

- costly-verification trust measurement;
- delayed verification instability;
- dynamic trust graphs;
- sparse communication with trust;
- verifier-cost trade-offs;
- classical delayed control and consensus.

## Why the gap matters

A producer-reviewer architecture exists in coding agents, research agents, workflow automation, and safety gates. Always checking is expensive; never checking creates unbounded exposure. A practical team will therefore adapt its auditing to perceived reliability. The key scientific risk is that this sensible local rule can form a delayed feedback controller with poor global dynamics.

The relevant distinction is between:

- **under-verification:** past success suppresses audits until errors propagate; and
- **over-verification:** failures leave a persistent scar, causing costly auditing after the system has recovered.

The project is worthwhile only if adaptive verification is demonstrably worse than a matched fixed policy in a plausible region—not merely worse than always verify or better than never verify.

## Formal core

At time \(t\), let:

- \(q_t\): expected actionable-error rate;
- \(\tau_t\): behavioral trust;
- \(a_t\): audit probability/intensity;
- \(d_v\): delay from audit choice to correction;
- \(d_o\): delay from evidence to trust update;
- \(\lambda\): unverified propagation strength;
- \(\rho\): audit effectiveness;
- \(\mu>0\): exogenous error floor.

Use an auditable mean-field model:

\[
q_{t+1}=[1-a_{t-d_v}]F_{\lambda,\mu}(q_t)+a_{t-d_v}G_{\rho,\mu}(q_t)+\xi_t,
\]

with \(G(q)<F(q)\), and a monotone trust-to-audit law:

\[
a_t=a_{\min}+(a_{\max}-a_{\min})\sigma(\beta_0-\beta_1\tau_t), \quad \beta_1>0.
\]

Observed error evidence updates trust only after delay. In the audit-selected case, missing audit outcomes are **missing evidence**, not successes. This avoids the invalid conclusion that a system becomes more trustworthy merely because it stopped observing failures.

Near a nonzero operating point, the reduced delayed system has the form:

\[
\tilde q_{t+1}=A\tilde q_t+B\tilde\tau_{t-d_v},
\qquad
\tilde\tau_{t+1}=C\tilde\tau_t+D\tilde q_{t-d_o},
\]

with characteristic equation:

\[
r^{d_v+d_o}(r-A)(r-C)-BD=0.
\]

The proof target is a nonempty region in which the fixed verifier is stable but the endogenous trust-to-audit loop is not. Do not linearize only around \(q=0\); at a perfect absorbing truth state the trust coupling can vanish to first order.

## Proposed solution: STAV

The raw trust policy proposes \(a_t^{\mathrm{raw}}\). STAV changes it only when it cannot certify a stability margin.

\[
\mathcal A_{\mathrm{safe}}(t)=\{a:\sup_{\theta\in\Theta_t}\rho(M(\theta,a))\leq1-\epsilon\},
\]

\[
a_t^{\mathrm{STAV}}=\arg\min_{a\in\mathcal A_{\mathrm{safe}}(t)}(a-a_t^{\mathrm{raw}})^2.
\]

For a one-dimensional audit action, precompute safe intervals under an uncertainty set over fitted behavior and environmental parameters. If the safe set is empty, use a pre-certified fixed policy and mark the episode as outside the certificate scope.

STAV must be compared against clipping, an audit floor, a rate limiter, a fixed safe policy, and an unconstrained trust policy. If a simple rate limiter matches it, simplify the method and say so.

## Required experimental chain

### 1. Behavioral identification (first gate)

Use a scripted adviser and an LLM reviewer. At each round the reviewer chooses **ACCEPT**, **VERIFY**, or **DEFER**; verification costs a controlled resource and returns delayed, imperfect evidence. Compare a memoryful reviewer to a reset-history anchor exposed to the same current evidence.

Manipulate reliability, burstiness, reliability shifts, verification cost, outcome cost, evidence delay, identity persistence, and prompt paraphrase. Fit a compact panel:

- memoryless;
- symmetric EWMA;
- Beta-Bernoulli threshold;
- asymmetric update;
- scar/hysteresis;
- optional identity/generalization extension.

Proceed only if history materially improves held-out verification prediction and the fitted response survives payoff-preserving prompt variants.

### 2. Theory and synthetic phase diagram (second gate)

Fit parameters on designated schedules only. Predict stable/oscillatory/cascade-prone cells held out by delay, topology, and reliability schedule. The theory must classify held-out transitions better than a flexible descriptive baseline.

### 3. Delayed Audit Relay (DAR)

Use a procedural, fully programmatic environment. Producers emit claims; consumers accept, verify, or defer; accepted claims feed downstream tasks; audits return after delay; each team eventually takes consequential actions. Ensure both always-verify and never-verify lose in preregistered regimes for transparent reasons.

Primary outcomes: cascade risk, accepted-error rate, delay failures, verification cost, and safety-cost frontier.

### 4. Patch Relay transfer

After a proposer submits a history of correct patches, a reviewer chooses no test, a cheap test, or a full hidden-suite test. Use seeded candidate patches for exact reliability control; treat naturally generated coding-agent patches as secondary ecological validation. Hidden tests, containers, no network access, and deterministic grading are mandatory.

## Must-beat baselines

- Never verify / always verify.
- Fixed Bernoulli and periodic auditing.
- Random budget-matched auditing.
- Beta-Bernoulli and EWMA/asymmetric-trust threshold policies.
- Raw fitted adaptive policy.
- Rate limiter, clipping, and audit-floor controls.
- Fixed certified safe policy.
- Oracle policy with true state/dynamics.

The primary comparison is **STAV versus raw adaptive and fixed policies under exact realized verification-cost matching**.

## Falsification gates

| Gate | Stop or pivot when |
|---|---|
| Behavioral trust | Memoryful and reset agents do not reliably differ in costly verification. |
| Model adequacy | A compact trust model cannot predict held-out schedules. |
| Practical relevance | Fixed-adaptive separation exists only at implausible, unfitted parameters. |
| Grounding boundary | Independent ground truth eliminates the effect. Narrow claim to partial/delayed validation. |
| Efficiency | STAV’s benefit disappears under exact cost matching. |
| Simplicity | Rate limiting matches STAV. Use the simpler method. |
| Transfer | Patch Relay has no analogous effect. Retain only a strong theory result. |

## Prerequisite reading: understand the gap

1. **Chen (2026), “Trust Between AI Agents.”** Defines behavioral trust through reduced costly verification; this is the direct behavioral foundation. [arXiv](https://arxiv.org/abs/2606.14923)
2. **Itkin (2026), “Delayed Verification Destabilizes Multi-Agent LLM Belief.”** Directly establishes exogenous delayed-verification instability and its grounded-truth boundary. [arXiv](https://arxiv.org/abs/2606.27409)
3. **Gou & Liu (2026), DySCo.** Dynamic trust-aware sparse communication; distinguishes communication selection from verification-control stability. [arXiv](https://arxiv.org/abs/2606.01828)
4. **Sun et al. (2026), “The Collaboration Tax.”** Empirical coordination-loss mechanisms, including acceptance without re-derivation. [arXiv](https://arxiv.org/abs/2608.22152)
5. **Sah et al. (2026), “The Verifier Tax.”** Establishes cost/safety trade-offs for verification on long horizons. [arXiv](https://arxiv.org/abs/2603.19328)
6. **Li et al. (2026), DynaTrust.** Dynamic trust graphs and adversarial/sleeper-agent context. [arXiv](https://arxiv.org/abs/2603.15661)
7. **Olfati-Saber, Fax & Murray (2007), consensus and cooperation in networked multi-agent systems.** Classical grounding for graph modes, delayed feedback, and stability terminology. [DOI](https://doi.org/10.1109/JPROC.2007.904725)
8. **Åström & Murray, _Feedback Systems_.** Control-theoretic stability, delays, robustness, and system-identification vocabulary. [Open text](https://fbswiki.org/wiki/index.php/Main_Page)

## Novelty-defense reading list

Before submission, rerun searches across arXiv, Semantic Scholar, OpenReview, and AAMAS 2026/2027 submissions for:

- `endogenous verification` / `adaptive verification` / `verifier scheduling` + agents;
- `trust dynamics`, `trust hysteresis`, `costly verification` + LLM;
- `delayed consensus`, `adaptive pinning`, `gain scheduling`, `switched systems` + multi-agent;
- `LLM cascade`, `agent failure propagation`, `collaboration tax`;
- `coding agent review`, `test scheduling`, `CI verifier`.

For every close paper, write one sentence answering: *Does it independently measure a trust update law, use it to predict held-out stability boundaries, and derive a cost-matched constrained verifier?* If the answer is yes, the claim must be narrowed or the project stopped.

## Why this is still a gap despite close papers

| Existing thread | What it does not establish |
|---|---|
| Trust measurement | Whether the measured behavior creates a dangerous delayed closed loop. |
| Delayed verification theory | Whether real LLM trust behavior yields parameters inside the unstable region. |
| Dynamic trust graphs | A cost-matched fixed-versus-adaptive stability separation. |
| Verifier-cost work | A robust controller with an interpretable, fitted stability certificate. |
| Coding review systems | Controlled reliability shifts, hidden ground truth, and a causal stability test. |

## AAMAS contribution package

1. An operational, behaviorally measured trust-to-verification law.
2. A fixed-versus-adaptive delayed-control separation theorem.
3. Held-out prediction of phase transitions, not retrospective explanation.
4. A minimally invasive stability-constrained controller.
5. Programmatically evaluated relay and coding-review tasks with exact cost matching.

This has main-track potential only if the independent-fit and held-out-prediction claims hold. Otherwise, a narrower behavioral-trust or delayed-control paper may still be publishable, but it is not the same project.

## Suggested eight-page outline

1. Endogenous verification as a delayed feedback loop.
2. Behavioral identification and operational trust measure.
3. Delayed dynamical model and separation theorem.
4. STAV algorithm and robust certificate.
5. DAR environment and preregistered protocol.
6. Held-out boundary prediction and cost-matched controller results.
7. Patch Relay transfer, limitations, and related work.

## Immediate pilot

Do not build DAR first. Implement the scripted adviser-reviewer identification task, run memoryful versus reset conditions under matched dispersed/clustered failure schedules, and fit memoryless, Beta, and asymmetric-history models. In parallel, sweep the reduced analytic model to see whether a stable-fixed/unstable-adaptive region intersects plausible behavioral parameters. If either check fails, do not proceed to STAV implementation.
