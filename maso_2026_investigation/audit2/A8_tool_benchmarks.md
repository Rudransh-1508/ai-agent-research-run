# AUDIT2 — A8: Tool-Using Agent Benchmark Specialist

**Investigator:** Agent 8 (tool/state-changing MAS vs reasoning-only MAS distinction)
**Date:** 21 September 2026
**Lane:** tau-bench, tau2-bench, retail/transactional agents, API/workflow agents, stateful environments, irreversible actions, AppWorld, ToolSandbox, OSWorld, WorkArena, TheAgentCompany; anchors Atomix, PAE, SagaLLM, Cordon.
**Mission:** DISPROVE novelty of the candidate paper (fault propagation & recovery in tool-executing LLM multi-agent organizations; H1 delegation depth, H2 containment cost, H3 containment-backfires-under-scarcity).

**Verification methods:** arXiv API (export.arxiv.org), arXiv abs pages + HTML search UI via FetchURL, Semantic Scholar Graph API (heavily rate-limited; partial), Crossref API, HuggingFace papers search. DBLP blocked (Anubis). Google Scholar 429. Every HIGH/MEDIUM-threat item below was verified against its arXiv abstract page or API record on 2026-09-21; verification level marked per item. Note: the numbered claims registry ("claims 5, 19") is NOT present anywhere in `maso_2026_investigation/` — I classify the two lane-claims implied by my assignment and flag the mapping explicitly (§7).

---

## 0. Bottom line (adversarial)

**The reasoning-only vs tool/state-changing distinction is load-bearing and it HOLDS, but the tool/state-changing side is far more crowded than the prior 48 reports imply.** A 2026 cluster of *single-agent* work already runs fault/recovery/containment-cost experiments in stateful tool environments — including on tau-bench/tau2-bench itself: Outcome Monitors (injected silent tool failures + recovery on ToolMaze and tau-bench retail), The Verifier Tax (enforcement-vs-success cost on tau-bench), SABER (mutating-step verification gating on tau-bench), ToolMaze (recovery metrics), Atomix/Cordon (transactional recovery of tool effects under injected faults), FinalityBench (irreversibility decisions). **Any claim of the form "no fault/recovery experiments exist where agent actions modify external state" is DEAD.** What survives: every one of these is single-agent; none measures propagation *across agents through shared mutated state*; none manipulates organizational structure or scarcity; and irreversibility is treated as a classification/budget/decision property, never as an experimental IV in a propagation/recovery-cost design.

---

## 1. Anchor verification (assignment-named)

| Anchor | ID / source | Verified | Notes |
|---|---|---|---|
| tau-bench | arXiv:2406.12045 | VERIFIED (B11 abs page; title/ID cross-checked) | Retail+airline, pass^k, deterministic DB-state GT, stochastic user sim |
| tau2-bench | arXiv:2506.07982 | **FULL TEXT of abstract re-verified 21 Sep** (v1 9 Jun 2025) | Dual-control Dec-POMDP telecom; compositional task generator; agent+user both mutate shared state |
| Atomix | arXiv:2602.14849 | **ABSTRACT VERIFIED** (v1 16 Feb 2026) | Progress-aware transactions for tool effects; seal/commit/abort; "improves clean recovery under injected faults"; irreversible effects "leave the gate" only when correctly classified — irreversibility is a *classification*, not an IV |
| AppWorld | arXiv:2407.18901 | VERIFIED (B11; ACL 2024) | State-based unit tests incl. collateral-damage checks; single-agent; no fault injection |
| PAE | arXiv:2603.03116 | **ABSTRACT VERIFIED** (v1 3 Mar 2026) | 27–78% of tau-bench "successes" are corrupt (conceal policy/integrity violations); gating collapses Pass^4, re-ranks models |
| SagaLLM | PVLDB 2025, DOI 10.14778/3750601.3750611 | **VERIFIED via Crossref** (Aug 2025, Chang & Geng) | Saga-pattern compensation/rollback + validation agents for multi-agent LLM *planning*; consistency-focused, no propagation/blast-radius measurement |
| Cordon | arXiv:2606.17573 | **ABSTRACT VERIFIED** (v1 16 Jun 2026) | Semantic transactions: shadow state, effect outbox, commit/rollback/audit, delegated-authority binding; "reduces irreversible-effect failures while preserving benign task completion with modest approval and latency overhead" — a costed containment mechanism for tool effects, single-agent workflows |

## 2. NEW collisions found in this sweep (not in the 48 prior reports)

### 2.1 HIGH — Outcome Monitors (arXiv:2608.19303, v1 19 Aug 2026) — ABSTRACT VERIFIED
Panthi & Abdelfattah. **Silent tool failures** ("a cached error page or negative price arrives in the expected format and is consumed as fact" — exactly the candidate's *semantic fault* concept) with **injected-failure evaluations on ToolMaze AND tau-bench retail**. Outcome contracts mined from task-disjoint traces; on violation, issues a receipt naming the violated property + public recovery tools. ToolMaze completion 10.9%→28.1% (4 models, 2 provider families, replicated in a third); **tau-bench retail completion +14.0/+12.0 points on two tiers**. Ablation: removing the recovery-tool list eliminates the gain. Detection outside mined vocabulary drops to 46%.
- **Why it collides:** it is a containment/detection + recovery mechanism evaluated under injected semantic faults in stateful tool benchmarks — the candidate's H2 territory, on the candidate's exact planned environment (tau-bench retail).
- **Why the candidate survives it:** single-agent; no propagation across agents; no organizational structure; no scarcity arm; mechanism is per-call monitoring, not organizational containment. Must be cited and differentiated.

### 2.2 HIGH (for H2's cost clause) — The Verifier Tax (arXiv:2603.19328, v1 18 Mar 2026) — ABSTRACT VERIFIED
Sah, Srivastava, Sah, Jordan. Runtime enforcement vs end-to-end task performance on **tau-bench Airline + Retail**; baseline vs planning-integrated (TRIAD) vs policy-mediated (TRIAD-SAFETY). Safety mediation intercepts up to 94% of non-compliant actions but SSR <5% in most settings; **"runtime enforcement imposes a significant verifier tax on conversational length and compute cost without guaranteeing safe completion"**; recovery after blocked actions 21% (GPT-OSS-20B, simple tasks) → ~0% (complex Retail). cs.CR.
- **Why it collides:** "verification/containment imposes cost on tool-executing agents" is already demonstrated, quantified, and named on tau-bench. H2's cost clause is not new in this lane.
- **Survives as:** safety-policy enforcement (compliance), single-agent, no fault propagation, no scarcity sign-reversal (cost does not flip benefit sign under a budget manipulation — it is a fixed tax measurement).

### 2.3 MEDIUM-HIGH — SABER (arXiv:2512.07850, v1 25 Nov 2025) — ABSTRACT VERIFIED (via HF + arXiv search; authors Cuadron, Yu, Liu, Gupta)
Decomposes tau-bench (Airline/Retail) and SWE-Bench Verified trajectories into **mutating (environment-changing) vs non-mutating steps**; formalizes "decisive deviations" (earliest action-level divergence flipping success→failure); each mutating-step deviation cuts odds of success up to 92–96%; safeguard = mutation-gated verification + targeted reflection before mutating steps (+28% relative on Airline for Qwen3-Thinking). Releases tau-Bench Verified.
- **Why it matters:** the state-changing/read-only action distinction — the candidate's load-bearing environment property — is already operationalized as an analysis axis and gating trigger on tau-bench. Single-agent; no propagation; no org structure.

### 2.4 MEDIUM-HIGH — TMAS: A Trace-Based Assurance Framework for Agentic AI Orchestration (arXiv:2603.18096, v1 18 Mar 2026, Stefanescu) — ABSTRACT VERIFIED
Multi-agent orchestration assurance: Message-Action Traces with step/trace contracts, deterministic replay, budgeted counterexample stress testing, **structured fault injection at service, retrieval, and memory boundaries to assess containment**, runtime governance (per-agent capability limits, allow/rewrite/block mediation), and metrics including **containment rate**. Code: github.com/george-QF/TMAS-code.
- **Why it collides:** boundary-typed fault injection + containment-rate metric for LLM orchestration — vocabulary and instrumentation overlap with the candidate's testbed claims.
- **Survives as:** framework/capability paper; abstract reports no systematic experiment varying organizational structure, depth, or scarcity; boundaries are service/retrieval/memory, not authority/delegation/accountability/human.

### 2.5 MEDIUM — AgentProp-Bench (arXiv:2604.16706, v1 17 Apr 2026, v2 10 Aug 2026) — ABSTRACT VERIFIED
14,750 execution traces, 13 LLM agents, 4 domains. Under validated judging, **a parameter-level error propagates to a wrong final answer with probability ≈0.62**, replicated across model families; ability to reject corrupted inputs and to recover from them are statistically independent; agents fabricate tool executions; a lightweight runtime interceptor reduces hallucinated-tool-execution claims (up to 24pp) at a tunable, net-positive operating point. cs.MA listed.
- **Why it collides:** this IS "fault propagation measured in tool-using agents" with a human-calibrated probability — the closest thing to question (c). But: single-agent trajectories, propagation = error→wrong-answer (not error→corrupted-shared-state→downstream-agent), no organizations.

### 2.6 MEDIUM — FinalityBench (arXiv:2609.04706, v1 4 Sep 2026) — ABSTRACT VERIFIED
Executable benchmark: merchant payment processor/ledger/ERP/bank-feed hold contradictory beliefs from delayed/duplicated/dropped/reordered messages; agent must ship/re-submit/refund/wait **"knowing some of those cannot be undone."** Hidden canonical event log; faulted delivery streams (fault semantics specified, not authored); grading on executed monetary effects; 321 tasks incl. 45 snapshot-indistinguishable twin pairs; 14,445 graded episodes; a runtime gate on irreversible actions reaches 85.4% with zero pass^5 loss; LLMs match the gate's accuracy but lose ~2× the money.
- **Why it matters for (b):** irreversibility is decision-central and economically priced here — but it is a *task property*, not a manipulated IV in a propagation/recovery-cost design; single-agent; no MAS.

### 2.7 MEDIUM — Safety Invariants for Agents Orchestrating Irreversible State Transitions (arXiv:2608.00783, v1 1 Aug 2026) — ABSTRACT VERIFIED
Formalizes irreversible ledger state transitions; fault model admits planner mis-mapping, ambiguous outcomes, retries, at-least-once delivery, and **delegated non-human callers**; proves "execution fidelity" (effect = nothing or exactly the rendered transition, exactly once); +74pp over naive ReAct on write-aggressive models, ~+3pp on write-cautious ones ("single-model evaluations of agent safety stacks are close to unfalsifiable"). Deployed; 108 production writes.

### 2.8 MEDIUM — The Irreversibility Budget (arXiv:2609.00275, v1 31 Aug 2026; AgenticOS @ SOSP) — ABSTRACT VERIFIED
Fleet-level cumulative account of residual value-at-risk; irreversibility as a first-class *resource*; per-effect gates admit fleet overdraws up to 48× tenant risk limit while the budget holds every correctly charged run within limit. Admission control, not fault propagation/recovery.

### 2.9 MEDIUM — Spawn Freely, Act Sparingly: Progressive Risk Vesting (arXiv:2609.01035, v1 1 Sep 2026) — ABSTRACT VERIFIED
Recursive agent trees crossing an "irreversible-action boundary"; trajectory-level risk budget in escrow; anytime harm bound; authority reproduction number R_A phase transition. Theory + synthetic only.

### 2.10 MEDIUM — Thinkingbox / Thinkingbox-bench (arXiv:2608.19741, v1 20 Aug 2026) — ABSTRACT VERIFIED
Stateful business-workflow sandbox (retail, hospitality, auto insurance, neobank IT, consulting IT/HR); 507 policy-conditioned workflows; executable checks **reject wrong, missing, or extra (collateral) effects**; Claude Opus 5: 66.50% pass@1 but 47.53% pass^20. The newest enterprise-stateful benchmark — and it has NO fault injection, confirming B11's Q3 answer.

### 2.11 LOW-MEDIUM — From Confident Closing to Silent Failure (arXiv:2606.09863, FAGEN@ICML 2026) — ABSTRACT VERIFIED
False-success characterization: 9,876 tau2-bench + 1,879 AppWorld trajectories; 45–48% of failures in single-control tau2-bench domains are false successes; LLM judges ≤0.65 AUROC; TF-IDF detectors 0.83/0.95 AUROC at 3,300× lower latency. Detection-of-silent-failure in stateful benchmarks; single-agent.

### 2.12 LOW-MEDIUM — DARC: Diagnosis Before Recovery (arXiv:2608.11772, v1 12 Aug 2026) — ABSTRACT VERIFIED
Diagnosis-guided selective recovery harness on ALFWorld, **AppWorld**, XBRL Finance; verifier-selected success-cost policy; recovery-interface design instead of context broadening. Single-agent recovery-cost awareness in stateful envs.

### 2.13 CONTEXT / METHODOLOGY WARNING — How Much Coordination Gain Is Real? (arXiv:2606.20695, v1 15 Jun 2026) — ABSTRACT VERIFIED
Paired noise-floor protocol run **on tau²-bench retail** with multi-agent coordination configurations (no_coord vs intercept vs pull): paired trial-0 gaps span [−3,+18]pp; pooled +5pp Wilson CI [−2,+12]; 7/10 recent coordination papers report headline effects below this floor. Two implications: (i) others are already running multi-agent protocol experiments on the candidate's planned Workflow-1 environment (colonization signal, though not fault work); (ii) n=100/cell binary contrasts on tau²-bench retail carry a ~±12–15pp noise floor — directly relevant to the candidate's R2 statistics debate.

### 2.14 CONTEXT — PolicyGuide (HF papers, τ²-bench airline/retail/telecom, GPT-5.4) — ABSTRACT ONLY (HF listing; arXiv ID not resolved)
Compiles domain policy into a workflow graph; proactive verifier at user-turn boundaries; mean Pass^4 0.42→0.62. Another verification-mechanism-on-tau2-bench data point.

## 3. Answers to the three critical assignment questions

**(a) What fault/recovery experiments exist specifically where agent actions modify external state?**
A substantial 2026 single-agent cluster: Outcome Monitors (ToolMaze + tau-bench retail, injected silent failures, recovery receipts), Verifier Tax (tau-bench, enforcement cost, post-block recovery rates), SABER (mutating-step deviations + gating, tau-bench/SWE-Bench), ToolMaze (PRR/RC recovery metrics; prior reports), Atomix + Cordon (transactional recovery of tool effects under injected faults), ReliabilityBench (chaos-style tool/API failures; prior reports), DARC (AppWorld recovery), AgentTether (tau-bench repair; prior reports), FinalityBench (irreversible-effect decisions under faulted delivery). **Every one is single-agent.** In multi-agent: MAS-FIRE's WebShop arm is the only stateful-ish benchmark, and faults there propagate via messages, not shared state; TMAS offers boundary fault injection as framework capability without published org-structure experiments.

**(b) Is irreversibility manipulated as a variable anywhere?**
**No — not as an experimental IV.** Irreversibility appears as: effect *classification* in transaction runtimes (Atomix, Cordon), a *task property* whose information is priced (FinalityBench), a *budgeted resource* (Irreversibility Budget), a *boundary* in theory (PRV), and a *formal-guarantee domain* (Safety Invariants). No work runs reversible-vs-irreversible regime arms and measures differential fault propagation or recovery cost. The candidate's two-regime irreversibility flag (R5 fix) is genuinely unoccupied — but the broad claim "irreversibility is ignored" is now false five times over and must not be written.

**(c) Does anything measure fault propagation in stateful tool environments (not reasoning chains)?**
Closest: AgentProp-Bench's ~0.62 error→wrong-answer propagation probability (single-agent, answer-level). CtC measures propagation but in discrete-event simulation with zero LLM calls (per CtC_fulltext_verification.md). **Propagation of a fault through shared mutated environment state across multiple executing agents is measured nowhere.** This is the lane's surviving gap.

## 4. Reasoning-only vs tool/state-changing separation check

The separation holds in the fault literature: MAS-FIRE (HumanEval/WikiTableQuestions/WebShop), AgentChaos (HumanEval/MBPP/MMLU-Pro/MATH/SWE-bench Pro), Spark-to-Fire, ACIArena are reasoning/code/message benchmarks — faults propagate through *messages and answers*. The stateful-tool fault cluster (§2) is entirely single-agent. The conjunction the candidate needs — **multi-agent × stateful tool execution × fault injection × propagation/recovery measurement** — remains empty after this sweep.

## 5. H1/H2/H3 threat assessment from this lane

- **H1 (delegation depth changes propagation/recovery cost):** no tool-environment work manipulates delegation depth under faults. DecisionBench (2605.19099, ABSTRACT VERIFIED) benchmarks emergent delegation on tau-bench (call_model routing, 23,375 instances) but has no faults and no depth manipulation. Safety Invariants includes "delegated non-human callers" in its fault model but varies nothing organizational. **No collision found in this lane.**
- **H2 (containment reduces propagation but imposes cost):** the *cost* clause is occupied in-lane by Verifier Tax (named "verifier tax", tau-bench) and Cordon ("modest approval and latency overhead"); the *propagation-reduction* clause is occupied only for single-agent (Outcome Monitors, SABER). **Partial collision; the MAS + propagation version survives.**
- **H3 (containment backfires under scarcity):** nothing in the tool-benchmark lane manipulates resource scarcity against containment. Verifier Tax's cost is fixed, not budget-scaled; FinalityBench prices finality information but not containment-under-scarcity. (B8's "Oversight Has a Capacity" inverted-U is the nearest scarcity result but single-agent gating.) **No collision found in this lane.**

## 6. Verification log

- arXiv abstract pages/API verified 2026-09-21: 2506.07982, 2602.14849, 2603.03116, 2606.17573, 2608.19303, 2603.19328, 2512.07850, 2603.18096, 2604.16706, 2609.04706, 2608.00783, 2609.00275, 2609.01035, 2608.19741, 2606.09863, 2608.11772, 2606.20695, 2605.19099, 2604.23581 (AgentEval, ACL 2026 Industry — DAG error-propagation *attribution* on tau-bench/SWE-bench traces, offline diagnosis not live injection), 2607.14166 (Stop Means Stop — approval-gate/cancellation side-effect leaks across 6 frameworks + SOUNDGATE repair; containment-integrity evidence).
- Crossref: SagaLLM DOI 10.14778/3750601.3750611.
- ABSTRACT ONLY (unresolved ID): PolicyGuide.
- Blocked/throttled during sweep: Semantic Scholar (429, intermittent), DBLP (Anubis), Google Scholar (429), arXiv API (intermittent empty responses — retried with backoff; all table entries confirmed).
- Prior reports read first: B11, D2, E4, E3 (SagaLLM row), B15 (PAE row), W2_assassin_cand4 (ToolMaze/AgentTether rows), B8 (oversight capacity), CtC_fulltext_verification.

## 7. Collision classification for claims 5 and 19 (lane mapping — registry absent)

The numbered claims registry does not exist in `maso_2026_investigation/`; mapping below is my inference and must be confirmed by the orchestrator.

- **Claim 5 (interpreted as: "no fault/recovery experiments exist in stateful, tool-executing environments" — the reasoning-vs-tool distinction claim):** **FATAL COLLISION if stated without the multi-agent qualifier** — Outcome Monitors (2608.19303), Verifier Tax (2603.19328), SABER (2512.07850), ToolMaze, Atomix, Cordon, FinalityBench occupy exactly this, several on tau-bench itself. **SURVIVES** as: "no fault-propagation/recovery experiments in *multi-agent* stateful tool environments, and none with organizational structure or scarcity as IVs."
- **Claim 19 (interpreted as: "irreversibility of tool actions has not been studied/manipulated"):** **FATAL COLLISION for the broad form** — Cordon, Atomix, FinalityBench, Safety Invariants, Irreversibility Budget, PRV all treat irreversibility as first-class in 2026. **SURVIVES** only as the narrow experimental claim: "irreversibility has never been manipulated as an independent variable in a fault-propagation/recovery-cost experiment (reversible vs irreversible regime arms)."

## 8. Unexpected finding

The candidate's planned Workflow-1 environment (tau²-bench retail) is already being used for multi-agent coordination methodology (2606.20695) with a measured paired noise floor of ±12–15pp at n=100 — both a colonization warning and a statistical-power constraint that directly undercuts any ±10pp SESOI equivalence-test plan on that environment.
