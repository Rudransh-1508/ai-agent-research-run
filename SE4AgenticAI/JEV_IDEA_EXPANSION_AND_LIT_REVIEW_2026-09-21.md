# Jev: idea expansion and academic literature review

Date: 2026-09-21. Companion to [JEV_RESEARCH_GAP_AUDIT_2026-09-21.md](JEV_RESEARCH_GAP_AUDIT_2026-09-21.md), which covered the grey literature (232 community projects, 6 independent calibration repos).
This document covers the **peer-reviewed and arXiv literature** and revises the idea ranking in light of it.

## 0. The single most important finding

**There is no academic paper on Jev or on System One models.** Jev entered early access on 2026-09-15, six days ago. Searches across arXiv and the SE venues return only vendor material and blog coverage. Every study that exists is a GitHub repository.

Combined with the grey-literature audit, the position is:

- Writing "we measured Jev's calibration" = scooped by six public repos.
- Writing the **first peer-reviewed study of a System One model as a software component** = wide open, and defensible as a genuine first.

More importantly, the literature review turned up a paper that transforms the recommended idea from "interesting" into "sharp." See Section 2.

---

## 1. Literature map

### 1.1 Agent authorization and runtime enforcement (the key cluster)

| Work | Relevance |
|---|---|
| **Capability Gates Are Not Authorization: Confused-Deputy Failures in LLM Agent Frameworks** ([arXiv 2606.28679](https://arxiv.org/html/2606.28679v1)) | Audits LangChain/LangGraph, LlamaIndex, Stripe Agent Toolkit at pinned commits. Finding: all three provide capability gating but **no deterministic fail-closed per-call argument authorization by default**. Proposes ScopeGate: a five-stage policy decision point (scope, authorization, ceiling, idempotency, **default-deny**). 48-vector static bypass suite, 0 bypasses; 40-iteration adaptive attacker, 0/29 allowed. Crucially: **"No probabilistic or ML-driven authorization mechanisms are evaluated. The authors treat the LLM itself as untrusted and place authorization outside it."** |
| **AgentSpec: Customizable Runtime Enforcement for Safe and Reliable LLM Agents** (ICSE 2026, [PDF](https://cposkitt.github.io/files/publications/agentspec_llm_enforcement_icse26.pdf)) | Deterministic rule language for runtime enforcement on agents. Note: I could not extract this PDF's body text, so treat its details as unread; the venue and premise are confirmed. It is the deterministic-enforcement baseline our work must be positioned against. |
| **TraceSafe** ([arXiv 2604.07223](https://arxiv.org/html/2604.07223v1)) | **Potentially our evaluation substrate.** 1,170+ instances, 90 per risk category, 12 risk types across prompt injection / privacy leakage / hallucination / interface inconsistency. Built by programmatic "benign-to-harmful editing" of 100%-accuracy Berkeley Function Calling Leaderboard trajectories, truncated at the mutation point. Evaluated 13 general LLMs and 7 specialized guardrails. Best coarse-grained result **83.58% (Qwen3-14B)**. Specialized guardrails **underperformed** general LLMs. Released research-only. |
| **AgentTrust** ([arXiv 2605.04785](https://arxiv.org/html/2605.04785v1)), **GuardianAgentBench** ([arXiv 2607.20982](https://arxiv.org/html/2607.20982v1)), ToolEmu, InjecAgent, AgentDojo, AgentHarm, WASP | The established benchmark ecosystem for tool-use safety and injection. Provides baselines and threat taxonomies. |
| **Authorization Propagation in Multi-Agent AI Systems** ([arXiv 2605.05440](https://arxiv.org/html/2605.05440v1)) | Identity governance as infrastructure; multi-agent authority propagation. MASO-adjacent. |

**Classical grounding:** Saltzer and Schroeder's reference monitor requirements - complete mediation, fail-safe defaults, economy of mechanism, verifiability - are the standard against which any authorization component is judged.

### 1.2 Calibration, cascades, deferral

| Work | Relevance |
|---|---|
| **UCCI: Calibrated Uncertainty for Cost-Optimal LLM Cascade Routing** ([arXiv 2605.18796](https://arxiv.org/html/2605.18796)) | The theory we need. Establishes that **calibration gives a threshold an explicit selective-risk interpretation and supports near-optimal decisions under a cost-sensitive objective**. Observes that LLM token-level confidences "require explicit calibration correction." Jev is the first shipped model claiming calibration as a *training objective* (RLCD), so it is a direct empirical test of UCCI's premise. |
| **FrugalGPT**, **RouteLLM**, **RouterBench**, **Dynamic Model Routing and Cascading survey** ([arXiv 2603.04445](https://arxiv.org/html/2603.04445v2)), **Calibration-Aware Uncertainty Cascades** ([arXiv 2609.11446](https://arxiv.org/html/2609.11446)), **CascadeDebate** ([arXiv 2604.12262](https://arxiv.org/html/2604.12262v1)) | FrugalGPT uses learned thresholds without imposing calibration; RouteLLM learns from preference data. Consensus in this line: **poorly calibrated confidence makes static routing thresholds brittle under distribution shift.** That is exactly the claim Jev's product thesis contests. |
| **Learning-to-defer / selective prediction**: Consistent Estimators for Learning to Defer ([arXiv 2006.01862](https://arxiv.org/pdf/2006.01862)), Predictor-Rejector Multi-Class Abstention ([arXiv 2310.14772](https://arxiv.org/pdf/2310.14772)), Budgeted Multiple-Expert Deferral ([arXiv 2510.26706](https://arxiv.org/pdf/2510.26706)), LLM Performance Predictors for escalation ([arXiv 2601.07006](https://arxiv.org/html/2601.07006)) | The formal vocabulary for "act automatically above threshold, escalate below." Jev's documented confidence-routing pattern is an untheorised instance of reject-option classification. Nobody has connected the two. |

### 1.3 Testing probabilistic components (the oracle problem)

| Work | Relevance |
|---|---|
| **Bidirectional Empowerment of Metamorphic Testing and LLMs: A Systematic Survey** ([arXiv 2605.13898](https://arxiv.org/html/2605.13898v1)) | States the open problem verbatim: **how to define stable and statistically meaningful metamorphic relations for probabilistic systems**, since existing studies rely on one-shot executions or few samples. |
| **METAL** ([arXiv 2312.06056](https://arxiv.org/html/2312.06056v1)), **Fault Detection Effectiveness of MRs for Supervised Classifiers** ([arXiv 1904.07348](https://arxiv.org/pdf/1904.07348)), **Systematicity, Compositionality and Transitivity of Deep NLP Models** ([arXiv 2204.12316](https://arxiv.org/pdf/2204.12316)) | MR catalogues for classifiers and LLMs. None targets a typed decision API returning a full probability distribution, and none tests option-order or complement invariance on such an API. |
| **Hidden Technical Debt in Machine Learning Systems** (Sculley et al., NeurIPS 2015) | Names **configuration debt** and manually-set thresholds that go stale as the world shifts. Written before thresholds encoded authorization decisions against a remote vendor model behind a moving alias. |

### 1.4 Governance, delegation, oversight (MASO cluster)

| Work | Relevance |
|---|---|
| **Minimal Oversight: Uncertainty-Aware Governance for Delegated AI Systems** ([arXiv 2606.15563](https://arxiv.org/html/2606.15563)) | Formal variational framework, Fisher information, first-passage analysis. Evaluated on **synthetic simulations** plus one semi-real reconstructed workflow. Explicitly does **not** use calibrated model confidence - it tracks empirical uncorrected success rate instead. Self-declared limits: binary outcomes, conditional independence, "synthetic, not a production study." |
| **Autonomy and Agency in Agentic AI: Architectural Tactics for Regulated Contexts** ([arXiv 2605.12105](https://arxiv.org/html/2605.12105v1)) | Treats **escalation** as the architectural tactic for when "the agent's reliability across inputs is uneven and the need for human involvement cannot be specified in advance." Names the tactic; supplies no measured mechanism for deciding when to fire it. |
| IMDA Model Governance Framework for Agentic AI (Jan 2026), NIST AI Agent Standards Initiative (Feb 2026) | Policy context. NIST names "the practical impossibility of meaningful real-time human oversight for long-running autonomous processes" - which is the problem a confidence gate claims to solve. |

Same shape as the authorization cluster: **the theory exists and is unmeasured; the practice exists and is unexamined.**

### 1.5 Adjacent, weaker

- **Let Me Speak Freely?** (EMNLP 2024 Industry, [PDF](https://arxiv.org/pdf/2408.02442)): format restriction degrades reasoning, *improves* classification. Jev is the limiting case of that continuum. Good one-paragraph related work; not a paper by itself.
- **LLM-as-a-judge reliability**: [Bias in the Loop: Auditing LLM-as-a-Judge for SE](https://arxiv.org/html/2604.16790v1), [Bias and Uncertainty in LLM-as-a-Judge Estimation](https://arxiv.org/pdf/2605.06939), [Calibrating LLM Judges](https://arxiv.org/pdf/2512.22245). Established finding: judges are systematically overconfident. Jev is a cheaper judge that claims calibration.
- **Green AI**: [Watts and Debts of Agentic Frameworks (registered report)](https://arxiv.org/pdf/2606.10702), [Green SARC](https://arxiv.org/html/2606.15954v1). Interesting framing, but joules of a hosted API are not measurable from outside. Demoted.

---

## 2. The revised headline idea

The confused-deputy paper changes everything, because it draws the line our subject crosses.

**The literature says** per-call authorization must be deterministic, fail-closed, default-deny, and placed *outside* the untrusted model (2606.28679, AgentSpec, and the reference monitor requirements behind both).

**The practice says** otherwise. Twenty-two public projects put a *probabilistic, remotely hosted, documented-as-injectable* model into exactly that slot: `jev-axi` scoring shell destructiveness, `pi-verdict` returning allow/ask/deny, `jev-git` screening commits for secrets, Vercel `fx` shipping a builtin `typesafe_permission_reviewer`.

Check the Jev gate against the reference monitor requirements and it fails all of them:

| Requirement | Jev gate |
|---|---|
| Complete mediation | Depends on an HTTPS call under a dynamic 1200 rpm limit. A 429 is an unmediated call unless the gate fails closed. |
| Tamperproof | Vendor concedes the model "does not treat data as hostile by default." The gate's input is attacker-reachable. |
| Verifiable / economy of mechanism | A 255-cardinality probabilistic model with a documented jaggedness page and no published accuracy figures. |
| Fail-safe defaults | An empirical question nobody has asked. |

**Title:** *Probabilistic Reference Monitors: Calibrated Decision Models in the Authorization Path of Coding Agents.*

**Four results:**

1. **Corpus study.** ~22 gates at pinned SHAs: question asked, primitive used, threshold constant, threshold provenance, action set, whether raw attacker-reachable text is passed unsanitised.
2. **Fail-open analysis.** Static read of every gate's error path for timeout / 429 / 5xx / malformed response. Needs no API key, no money, and produces the finding that survives the vendor: *putting a remote probabilistic service on the permission path makes gate availability a security property.* Frame directly against ScopeGate's default-deny stage.
3. **Benchmarked accuracy against published baselines.** Run Jev gates over TraceSafe-Bench and compare to its 13 LLMs and 7 specialized guardrails, best 83.58%. This answers `themsquared/jev-benchmark`'s two self-declared weaknesses (n=60, no baselines) in one move, and TraceSafe's finding that *specialized guardrails underperform general LLMs* sets up a genuinely open question about where a System One gate lands.
4. **Cost-sensitive threshold analysis.** Per UCCI, calibration is what licenses a threshold to carry a selective-risk interpretation. Authorization loss is wildly asymmetric. Derive the loss-optimal threshold and report where the vendor docs' illustrative 0.9 actually sits.

Why this is much stronger than yesterday's version: it has a named theoretical frame, a named deterministic baseline, a published benchmark with published numbers, and a tension between literature and practice that a reviewer can grasp in one sentence.

---

## 3. Ranked ideas

### A. Probabilistic reference monitors (Section 2) - **recommended, best story**
Strongest narrative, strongest citations, highest reviewer interest. Risks: needs API access for results 3-4; may draw a security-minded reviewer who wants a bigger threat model; TraceSafe's research-only licence must be confirmed obtainable in days.

### B. Metamorphic testing for typed decision models - **recommended, best odds**

The oracle problem in its purest form: you cannot assert equality on a returned probability, so what *is* a unit test for a decision dependency? The MT survey names stable MRs for probabilistic systems as an open problem. TypeSafe's own jaggedness page hands us pre-admitted violations to build on: `P(noul) != 1 - P(not_noul)`, option-ordering effects on ambiguous input, context pollution from irrelevant state.

Contribution: (i) an MR catalogue for typed decision APIs - complement, option permutation, irrelevant-context injection, paraphrase, Score monotonicity, composite distributivity, cardinality-split consistency; (ii) a statistical decision procedure for declaring a violation given sampling noise, which is the open problem the survey names; (iii) measured violation rates on a real System One model; (iv) a CI canary design for pinning a probabilistic dependency across a version bump, against Sculley's configuration debt.

Why I rate its *acceptance odds* above A even though its story is smaller: it is 100% inside SE, needs no security reviewer, costs single-digit dollars, generalises past Jev to any typed decision API, is entirely uncovered by the 232-project grey corpus, and degrades gracefully into a short paper if access slips. It is the safe pick.

### C. Threshold provenance and configuration debt
Mine thresholds from the corpus; test cross-task transfer; diff `jev-latest` against `jev-preview` (themsquared already observed a 43 ms latency gap, so they are not the same build). Ground in Sculley et al. **Fold into A or B as a section.** Thin alone.

### D. MASO: calibrated confidence as a delegation boundary
Minimal Oversight is formal and synthetic and explicitly declines to use model confidence; the architectural-tactics paper names escalation without a mechanism. Supply the measured mechanism, plus the governance observation that thresholds encoding organizational authority are undocumented constants copied from vendor sample code. Connects to the existing `maso/policy_preserving_delegation_research_proposal.md`. **Distinct enough from A to be a second submission** - do not send the same PDF.

### E. Native vs post-hoc calibration for cost-optimal routing
Jev-native calibration vs LLM + temperature/isotonic at matched cost, on cost-sensitive selective risk, against UCCI. Genuine, but ML-conference shaped and partly covered by `calibre` and `jev-ood-calibration`. Fallback.

### F. Probabilistic context pruning - **new, underrated**
A second emergent practice nobody has studied: using a typed decision model to decide what stays in an agent's context (`fast-jev-compaction`, `jev-pruner`, `pi-fast-jev-compaction`, `jselect`, `public-browser` claiming ~30% fewer tokens). The SE question is sharp: **pruning errors are silent and unrecoverable.** A wrongly dropped tool result does not raise; the agent just fails later, and the failure is attributed to the agent, not the pruner. Measurable with the existing `SE4AgenticAI/harness/` episode runner. Held back only by cost and wall-clock: full agent episodes in 19 days is tight, and the repo's own calibration-mechanics log shows how fragile that pipeline has been. **Best candidate for the *next* paper, not this one.**

### G. Energy and cost of decision-model substitution - **demoted**
Cannot measure joules of a hosted API from outside. Cost and latency only, which the grey literature already reports.

### H. The format-restriction continuum - **skip**
Good related-work paragraph, wrong venue.

---

## 4. What I would actually do

Write **A** if access is confirmed by day 3 and TraceSafe is obtainable. Write **B** if either gate fails - and note that B's corpus-free, cheap, single-reviewer-profile shape makes it the higher-probability acceptance even though A is the better paper.

The two share infrastructure: both need a pinned `jev-1.13.0` client, a logging wrapper, and a raw-JSONL artifact. Build that first, and the choice between A and B can be deferred to day 5.

Submit **D** to MASO only if it can be written as a genuinely different paper, not a re-skin.

## 5. Citations we must engage with, not just list

A reviewer who knows this area will expect these by name:

- 2606.28679 (authorization must be deterministic and fail-closed) - the tension our paper is about.
- AgentSpec, ICSE 2026 - the deterministic baseline. **Read the actual PDF before writing.**
- TraceSafe 2604.07223 - substrate and baselines.
- UCCI 2605.18796 - why calibration licenses a threshold.
- Sculley et al. 2015 - configuration debt.
- 2605.13898 - MRs for probabilistic systems as an open problem.
- 2606.15563 and 2605.12105 - for the MASO variant.
- Saltzer and Schroeder - reference monitor requirements.
