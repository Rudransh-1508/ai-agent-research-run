# B13 — Agent Observability Landscape (Adversarial Evidence Map)

**Investigator:** Landscape B13 · **Date:** 2026-09-21
**Mission question:** Map tracing/logging/monitoring for agentic systems (OpenTelemetry GenAI conventions, LangSmith/LangFuse/AgentOps-style tooling, academic agent observability, runtime monitoring, anomaly detection for agent workflows). **Is observability connected to automated containment, or is it passive?** Adversarial goal: test whether this landscape kills or subsumes the seed hypothesis ("organizational blast radius" of failure propagation in LLM MAS + containment/recovery mechanisms).

**Verification method note:** Semantic Scholar API, DBLP, OpenAlex, and the arXiv API/search UI were hard rate-limited or bot-blocked from this environment (shared-IP budgets exhausted). All papers below were verified by fetching the **actual arXiv abstract pages** (arxiv.org/abs/<id>), Crossref records, GitHub repos, or official docs — never from search snippets. Discovery was via the HuggingFace Papers API (`huggingface.co/api/papers/search`), which worked reliably, plus targeted arXiv-ID verification. Every arXiv ID, venue claim, and date below was read off the primary page on 2026-09-21.

---

## 0. Bottom line

**Observability for agentic systems is real, maturing fast, and overwhelmingly PASSIVE.** The stack that exists in September 2026 is: (a) a standardization layer (OTel GenAI conventions, still in "Development" status; OpenInference/OpenLLMetry as vendor-neutral instrumentation), (b) mature commercial/OSS trace platforms (LangSmith, Langfuse, AgentOps.ai, Arize Phoenix, W&B Weave) aimed at *human* debugging and evaluation, and (c) a 2025–2026 academic wave on trace-based failure *attribution*, anomaly *detection*, and root-cause *diagnosis*. The closed loop **detect → localize → contain → recover → verify** for multi-agent workflows is essentially unbuilt: detection/attribution papers stop at diagnosis; containment papers (authorization gates, sandboxing, guardrails, kill switches) are **not observability-driven** — they act pre-action or on policy violation, not in response to observed failure propagation across an organization of agents. Nothing found kills the seed hypothesis; the closest neighbors (MAS-FIRE, AgentDebugX, AgentTether, trace-contamination measurement) each cover one segment of the loop, offline or single-agent, and none touch the *organizational* boundary dimensions (role, authority/delegation, accountability, human-agent) that define the seed.

---

## 1. Standards layer

| Item | Verified facts | Status re: containment |
|---|---|---|
| **OpenTelemetry GenAI semantic conventions** | Moved (2026) to dedicated repo `open-telemetry/semantic-conventions-genai` (created 2026-05-05, actively pushed through 2026-09-21, ~384 stars). Docs define span types: `create_agent`, `invoke_agent` (client + internal), `invoke_workflow`, `plan`, `execute_tool`, plus memory ops (`search_memory`, `update_memory`, `upsert_memory`) and MCP conventions. **Every agent-span definition is marked "Status: Development"** — not stable. Workflow-span examples cite ADK `Runner.run`, Microsoft Agent Framework. [repo](https://github.com/open-telemetry/semantic-conventions-genai), [agent spans doc](https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-agent-spans.md) | Purely descriptive schema. No semantics for failure severity, propagation, quarantine, or recovery actions. |
| **OpenInference (Arize)** | OTel-complementary instrumentation spec + ~35 Python/JS/Java/Go instrumentations (LangChain, AutoGen/AG2, CrewAI, OpenAI Agents, MCP, ADK…); feeds Phoenix/Arize AX or any OTel backend. [repo](https://github.com/Arize-ai/openinference) | Passive tracing only. |
| **OpenLLMetry (Traceloop)** | OTel extensions for LLM/vector-DB/framework calls; its semantic conventions were upstreamed into OTel GenAI ("Our semantic conventions are now part of OpenTelemetry!"). [repo](https://github.com/traceloop/openllmetry) | Passive tracing only. |

**Reading:** the industry has converged on *what to record* (spans for agent creation/invocation, tool execution, planning, memory) but the standard is explicitly unfinished and contains **no vocabulary for blast radius, containment, or recovery** — an opportunity and a risk (a MASO paper could propose exactly this vocabulary; it could also be absorbed by the OTel SIG at any time).

## 2. Commercial / OSS tooling (no academic papers exist for these — verified via official sites/repos)

| Tool | What it is (verified 2026-09-21) | Containment? |
|---|---|---|
| **LangSmith** (LangChain) | "Full visibility into your LLM application: from individual traces to production-wide performance metrics… debug failures, monitor quality, build datasets." [docs](https://docs.smith.langchain.com/) | No — human debugging/eval loop. |
| **Langfuse** | OSS LLM engineering platform (tracing, prompt mgmt, evals, datasets); **acquired by/part of ClickHouse since Jan 2026**; MIT-licensed; 16k+ stars. [repo](https://github.com/langfuse/langfuse) | No. |
| **AgentOps.ai** | Commercial "agent observability" SaaS: session traces, time-travel debugging, cost/token tracking, prompt-injection *logging*. [site](https://www.agentops.ai/) | Logs attacks; does not stop them. |
| **W&B Weave** | Tracing + evaluations toolkit (`@weave.op` decorators). [repo](https://github.com/wandb/weave) | No. |
| **Arize Phoenix** | Trace collector/viewer for OpenInference (see §1). | No. |

Note: the name "AgentOps" is overloaded — the startup above vs. the academic taxonomy paper below (§3), which are unrelated.

## 3. Academic observability frameworks (verified)

| Paper | ID / venue | What it does | Passive or active? |
|---|---|---|---|
| **AgentOps: Enabling Observability of LLM Agents** (Dong et al.) | [arXiv:2411.05285](https://arxiv.org/abs/2411.05285) (Nov 2024, cs.AI/cs.SE) | Taxonomy of AgentOps artifacts/data to trace across the agent lifecycle, from a systematic mapping study of existing AgentOps tools; frames observability as prerequisite for "detect anomalies, prevent failures" but delivers the taxonomy only. | Passive (framework/taxonomy). |
| **AgentTrace: A Structured Logging Framework for Agent System Observability** (AlSayyad et al.) | [arXiv:2602.10133](https://arxiv.org/abs/2602.10133) (Feb 2026; AAAI 2026 LaMAS Workshop) | Runtime structured logging across operational/cognitive/contextual surfaces; positions logs as foundation for security, accountability, real-time monitoring. | Passive capture layer. |
| **AgentTrace: Causal Graph Tracing for Root Cause Analysis in Deployed Multi-Agent Systems** (Wang) | [arXiv:2603.14688](https://arxiv.org/abs/2603.14688) (Mar 2026; ICLR 2026 Agents-in-the-Wild Workshop) | Reconstructs causal graphs from execution logs, backward-traces from error manifestations, ranks root causes *without LLM inference at debug time*; sub-second latency. (Name collision with the above — distinct papers.) | Passive post-hoc diagnosis. |
| **AgentSight: System-Level Observability for AI Agents Using eBPF** (Hu et al.) | [arXiv:2508.02736](https://arxiv.org/abs/2508.02736) (Aug 2025; PACMI 2025, DOI 10.1145/3766882.3767169) | "Boundary tracing": intercepts TLS LLM traffic + kernel events via eBPF, causally correlates intent with system effects, <3% overhead; detects prompt injection, resource-wasting loops, multi-agent coordination bottlenecks. | Detection/alerting; no automated response. |
| **The Log is the Agent (ActiveGraph)** | [arXiv:2605.21997](https://arxiv.org/abs/2605.21997) (May 2026) | Event-sourced runtime: append-only log as source of truth, deterministic replay, cheap forking, end-to-end lineage. | Passive substrate enabling audit/replay (recovery-adjacent but no containment logic). |
| **AgentLogs** | [arXiv:2608.29204](https://arxiv.org/abs/2608.29204) (Aug 2026) | 307k GitHub Copilot cloud-agent tasks, 549k sessions, 64M log entries — dataset for studying agent behavior/failure modes in the wild. | Passive (dataset). |
| **Do AI Coding Agents Log Like Humans?** | [arXiv:2604.09409](https://arxiv.org/abs/2604.09409) (Apr 2026) | Empirical study of 4,550 agentic PRs: agents under-log, ignore logging instructions 67% of the time; humans silently repair logs. | Evidence that agent-generated telemetry is unreliable. |
| **Agentic CLEAR** (Yehudai et al.) | [arXiv:2605.22608](https://arxiv.org/abs/2605.22608) (May 2026, ACL) | Evaluation framework "above the observability layer"; explicitly criticizes current tools as "limited, focusing on observability with basic evaluation capabilities." | Passive eval. |
| **Agentic Harness Engineering (AHE)** (Lin et al.) | [arXiv:2604.25850](https://arxiv.org/abs/2604.25850) (Apr 2026) | "Observability-driven" closed loop that evolves coding-agent harnesses (Terminal-Bench 2 pass@1 69.7→77.0%). | Active but *offline* self-improvement, not runtime containment. |

## 4. Trace-based failure analysis & attribution (the "diagnosis" cluster)

| Paper | ID / venue | Key verified numbers | Relation to seed |
|---|---|---|---|
| **Why Do Multi-Agent LLM Systems Fail? (MAST)** (Cemri et al.) | [arXiv:2503.13657](https://arxiv.org/abs/2503.13657) (Mar 2025; v3 Oct 2025) | 1,600+ annotated traces, 7 frameworks, 14 failure modes in 3 categories, κ=0.88. | Foundational failure taxonomy; post-hoc. |
| **TRAIL: Trace Reasoning and Agentic Issue Localization** (Deshpande et al.) | [arXiv:2505.08638](https://arxiv.org/abs/2505.08638) (May 2025) | 148 human-annotated traces; best model (Gemini-2.5-pro) scores **11%** at trace debugging. | Shows LLM judges are bad at trace debugging → automated containment can't yet rely on them. |
| **Who&When: Automated Failure Attribution** (Zhang et al.) | [arXiv:2505.00212](https://arxiv.org/abs/2505.00212) (Apr 2025, cs.MA; camera-ready) | 127 MAS failure logs; best method 53.5% agent-level, **14.2% step-level** attribution; o1/R1 below usability. | Attribution is a hard, unsolved prerequisite for targeted containment. |
| **TraceElephant ("Seeing the Whole Elephant")** | [arXiv:2604.22708](https://arxiv.org/abs/2604.22708) (Apr 2026; **ACL 2026**) | Full-execution-trace attribution benchmark; full traces improve attribution **up to 76%** over partial observation. | Argues observability depth determines diagnosability. |
| **AgentLocate ("Who Broke the System?")** (Fang et al.) | [arXiv:2607.07989](https://arxiv.org/abs/2607.07989) (Jul 2026; **COLM 2026**) | LLM judge + multi-perspective verification + confidence-aware aggregation + judge fine-tuning; SOTA attribution. | Diagnosis only. |
| **GraphTracer** | [arXiv:2510.10581](https://arxiv.org/abs/2510.10581) (Oct 2025) | **WITHDRAWN** (Dec 2025) "due to a fundamental error in the methodology." | Cautionary: do not cite as evidence. |
| **AgentDebugX** (Zhu et al.) | [arXiv:2607.18754](https://arxiv.org/abs/2607.18754) (Jul 2026) | Closed loop **Detect→Attribute→Recover→Rerun**; DeepDebug 28.8% strict agent+step attribution on Who&When (vs 21.7% baseline); on GAIA repairs 13/73 failed tasks in one rerun (55.8→63.6% accuracy). | **Closest existing detect→recover loop — but post-hoc, single-workflow rerun, no propagation containment.** |
| **ParaRecover** | [arXiv:2609.12345](https://arxiv.org/abs/2609.12345) (Sep 2026; **EMNLP 2026 main**) | Process-level benchmark, error localization + recovery in parallel tool-use agents; 14 error types, 10,626 instances; SOTA models struggle with multi-turn error propagation and cascading failures across dependent branches. | Studies cascading failure + recovery, but single-agent tool DAGs, not organizational MAS. |

## 5. Anomaly detection & runtime monitoring (verified)

| Paper | ID / venue | What it does | Containment link |
|---|---|---|---|
| **LumiMAS** (Solomon et al.; BGU — Shabtai/Elovici group) | [arXiv:2508.12412](https://arxiv.org/abs/2508.12412) (Aug 2025; v2 Feb 2026) | MAS observability framework: monitoring/logging layer → **real-time anomaly detection across the MAS workflow** → anomaly explanation/RCA layer; evaluated on 7 MAS apps, 2 platforms. | Detects + explains; **no automated response**. |
| **TrajAD: Trajectory Anomaly Detection for Trustworthy LLM Agents** | [arXiv:2602.06443](https://arxiv.org/abs/2602.06443) (Feb 2026) | Formulates runtime trajectory anomaly detection + precise error localization; TrajBench dataset; specialized verifier beats zero-shot LLMs. Motivated explicitly by "enabling efficient rollback-and-retry." | Detection designed to feed rollback-retry, but the recovery mechanism itself is not built/evaluated; single-agent. |
| **Automata from Agent Traces** (Cho et al.) | [arXiv:2608.23670](https://arxiv.org/abs/2608.23670) (Aug 2026) | Collapses trace corpora into compact FSMs (7–43 states, ≥0.997 replay fitness, 12 datasets); failure prediction AUROC up to 0.94; **online monitor ranks failing runs from partial traces and triggers early stopping**. | The strongest verified observability→action link: **early stopping only** (abort, not contain-and-continue). |
| **Agent Drift** | [arXiv:2601.04170](https://arxiv.org/abs/2601.04170) (Jan 2026) | Defines semantic/coordination/behavioral drift in MAS; Agent Stability Index (12 dimensions); proposes mitigations. Single-author, simulation/theory only — weak evidence. | Monitoring metric proposal. |
| **Temporal Attack Pattern Detection in Multi-Agent AI Workflows** | [arXiv:2601.00848](https://arxiv.org/abs/2601.00848) (Dec 2025) | QLoRA fine-tunes LMs to detect attack patterns in **OpenTelemetry traces** of multi-agent workflows; 80,851 examples + 35,026 synthetic OTel traces; 42.86→74.29% benchmark accuracy. | Security detection on standard traces; acknowledges human oversight needed (false positives). |
| **R-Judge** (Yuan et al.) | [arXiv:2401.10019](https://arxiv.org/abs/2401.10019) (Jan 2024; EMNLP Findings 2024) | Benchmark for judging safety risks from agent interaction records (569 records); best model 74.42%, most near random. | LLM-as-monitor is weak — same lesson as TRAIL. |

## 6. Containment / enforcement mechanisms — and whether observability drives them

**Verified pattern: containment mechanisms act on policy/authorization, pre-action, or on adversarial input — NOT on observed failure propagation.** None consume anomaly/observability signals to decide containment scope.

| Paper | ID / venue | Mechanism | Trigger |
|---|---|---|---|
| **AgentSpec** (Poskitt et al.) | [arXiv:2503.18666](https://arxiv.org/abs/2503.18666) (Mar 2025; **ICSE 2026**, DOI 10.1145/3744916.3764546) | DSL for runtime rule enforcement (triggers, predicates, enforcement); >90% unsafe executions prevented; ms overhead. | Rule trigger, not anomaly detection. |
| **GuardAgent** (Xiang et al.) | [arXiv:2406.09187](https://arxiv.org/abs/2406.09187) (Jun 2024; **ICML 2025**) | Guardrail agent generates guardrail code from safety requests; 98%/83% guardrail accuracy (EICU-AC, Mind2Web-SC). | Guard request, static. |
| **Progent** (Shi et al.) | [arXiv:2504.11703](https://arxiv.org/abs/2504.11703) (Apr 2025; v3 May 2026) | Least-privilege policy over tool calls; SMT-checked updates; **monotonic confinement** (privileges only shrink without approval). | Policy, not observation. |
| **CaMeL** (Debenedetti et al., Google DeepMind) | [arXiv:2503.18813](https://arxiv.org/abs/2503.18813) (Mar 2025) | Control/data-flow separation + capabilities; 77% AgentDojo tasks with provable security. | Structural prevention. |
| **VeriGuard** | [arXiv:2510.05156](https://arxiv.org/abs/2510.05156) (Oct 2025) | Offline-verified policy + online action monitor validating each action pre-execution. | Pre-action gate. |
| **Safety Sentry** | [arXiv:2607.13594](https://arxiv.org/abs/2607.13594) (Jul 2026) | Per-instance EXECUTE/ASK/REFUSE routing, single decoding call. | Pre-action gate. |
| **Faramesh** | [arXiv:2601.17744](https://arxiv.org/abs/2601.17744) (Jan 2026) | Execution control plane; PERMIT/DEFER/DENY artifacts; **explicitly contrasts itself with "observability-only approaches"**. | Pre-action authorization. |
| **Open Agent Passport ("Before the Tool Call")** | [arXiv:2603.20953](https://arxiv.org/abs/2603.20953) (Mar 2026) | Pre-action authorization, signed audit records; distinguishes itself from sandboxing ("contains blast radius") and model screening. | Pre-action; uses "blast radius" in the *security* sense. |
| **Bounded Agents / APC** | [arXiv:2608.15888](https://arxiv.org/abs/2608.15888) (Aug 2026) | Delegation-chain authorization; proves **"Blast Radius Monotonicity"** and Composition Soundness; AgentDojo exfiltration 75–100%→0%. | **Terminology alert: "blast radius" is already in use for authorization scope, not failure propagation.** |
| **ceLLMate** | [arXiv:2512.12594](https://arxiv.org/abs/2512.12594) (Dec 2025) | HTTP-layer sandbox for browser agents; "reduces the blast radius of prompt injections." | Sandbox; security sense of blast radius. |
| **ScopeGate ("Capability Gates Are Not Authorization")** | [arXiv:2606.28679](https://arxiv.org/abs/2606.28679) (Jun 2026) | Audits LangChain/LangGraph, LlamaIndex, Stripe Agent Toolkit: none fail-closed per-call by default; 5-stage PDP/PEP. | Pre-action gate. |
| **SAGA** | [arXiv:2504.21034](https://arxiv.org/abs/2504.21034) (Apr 2025) | Governance architecture: agent registration, cryptographic access-control tokens for inter-agent communication. | Access control. |
| **Escalation channels** ("From surveillance to signalling") | [arXiv:2510.05192](https://arxiv.org/abs/2510.05192) (Oct 2025; v2 Apr 2026) | Environmental controls (Situational Crime Prevention): credible escalation channel cuts harmful-action rate 38.73%→1.21% across 10 frontier LLMs, 24k samples. | Environmental design, not monitoring-driven. |
| **NeMo Guardrails** (Rebedea et al.) | [arXiv:2310.10501](https://arxiv.org/abs/2310.10501) (Oct 2023; EMNLP 2023 demo) | Programmable rails for conversational LLMs. | Dialogue-level, pre-agentic. |

## 7. AI control & kill switches (adversarial-misuse branch of monitoring)

| Paper | ID / venue | Verified content |
|---|---|---|
| **Async Control** (Cooper Stickland et al.) | [arXiv:2512.13526](https://arxiv.org/abs/2512.13526) (Dec 2025) | Asynchronous (after-the-fact) monitoring as a control measure; adversarial blue/red game; ensemble monitor 6% FNR @ 1% FPR; risk extrapolation model. Monitoring *is* connected to disruption here — but for sabotage, not accidental fault propagation. |
| **Multi-Agent AI Control** (Makins et al.) | [arXiv:2607.07368](https://arxiv.org/abs/2607.07368) (Jul 2026; submitted NeurIPS) | **Fragmentation effect: as more agents coordinate an attack, per-agent monitors get worse**; explicit planner amplifies attacks up to 7×; strong trusted monitor cuts undetected success >10× but stays imperfect. Directly relevant warning: per-instance observability does not scale to coordinated multi-agent failure. |
| **KillBench** | [arXiv:2511.13725](https://arxiv.org/abs/2511.13725) (Sep 2025; **EMNLP 2026 Findings**) | External kill switch (prompt-style payloads, no internal access) for malicious web agents; 4 defense methods, 5 models. |
| **The Off-Switch Game** (Hadfield-Menell et al.) | [arXiv:1611.08219](https://arxiv.org/abs/1611.08219) (Nov 2016; IJCAI 2017) | Classical corrigibility: agents need objective uncertainty to preserve their off-switch. |
| **ResearchArena** | [arXiv:2607.19321](https://arxiv.org/abs/2607.19321) (Jul 2026; found via HF search, abstract not separately fetched) | Sabotage + monitoring in automated AI R&D. Listed for completeness. |

## 8. Classical anchors (pre-LLM)

| Work | Verified via | Relevance |
|---|---|---|
| **Dapper** (Barroso et al., Google, 2010) | [research.google](https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/) | Distributed tracing infra; the ancestor of everything in §1–2. Passive. |
| **Kaminka & Tambe, "Robust Agent Teams via Socially-Attentive Monitoring"** | Crossref DOI 10.1613/jair.682, **JAIR vol. 12, 2000** | Classical MAS: agents monitor teammates' behavior to detect failures and reallocate roles — *team-level observability linked to recovery* exists in classical MAS but as model-based plan recognition, not trace analytics. |
| **TraceAnomaly** (Liu et al.) | Crossref DOI 10.1109/issre5003.2020.00014, **ISSRE 2020** | AIOps: unsupervised anomaly detection on microservice traces (deep Bayesian networks). The microservices-RCA field (also e.g. graph-VAE trace anomaly detection, WWW 2023, DOI 10.1145/3543507.3583215) is the methodological ancestor of §5. |
| Circuit breaker / bulkhead patterns | Nygard, *Release It!* (2007); Fowler's CircuitBreaker post (2014) — well-known engineering patterns; **no verified transfer to LLM-agent failure semantics found** (searched "circuit breaker LLM agent": only unrelated circuit-design papers + Progent). | A named gap: nobody has formally adapted circuit-breaker semantics to agent-message propagation. |

## 9. Industry practice anchor

**MAP — Measuring Agents in Production** (Pan, Arabzadeh, … Zaharia, Ellis; [arXiv:2512.04123](https://arxiv.org/abs/2512.04123); **ICML 2026 Oral**): 20 case studies + survey of 86 deployed-system practitioners across 26 domains. Verified findings: **68% of production agents execute ≤10 steps before human intervention; 70% use prompting of off-the-shelf models; 74% depend primarily on human evaluation; reliability is the top challenge, addressed via systems-level design.** Interpretation: real deployments contain failures by *limiting autonomy and inserting humans*, not by observability-driven automated containment. This is the strongest field evidence that the seed's containment question is open in practice.

## 10. Synthesis: is observability connected to automated containment?

**Mostly no.** The verified landscape decomposes into four disconnected clusters:

1. **Capture** (§1–3): standards + platforms record traces. Passive by design; OTel GenAI conventions are still "Development"-status and have no failure/containment vocabulary.
2. **Diagnosis** (§4–5): attribution, anomaly detection, RCA — strong 2025–2026 academic wave, but outputs are *explanations for humans* or, at best, early stopping (Automata-from-Traces) and rollback-retry hooks (TrajAD). Attribution accuracy is still poor (Who&When: 14.2% step-level; TRAIL: 11% for LLM judges), which adversarially implies **automated containment triggered by current attributors would misfire**.
3. **Containment** (§6–7): authorization gates, sandboxing, guardrails, kill switches, AI-control monitors — active, but triggered by policy/permission rules or adversarial-attack signatures, **not by observed fault propagation**; all single-agent or security-focused; none reason about organizational boundaries (role, delegation chain, memory, accountability).
4. **Recovery** (§4): AgentDebugX (detect→attribute→recover→rerun, post-hoc, 13/73 GAIA repairs), AgentTether ([arXiv:2607.06273](https://arxiv.org/abs/2607.06273), Jul 2026: graph-guided diagnosis + guarded runtime intervention, repairs 59–65% of failed τ-bench tasks — single-agent), DARC ([arXiv:2608.11772](https://arxiv.org/abs/2608.11772), diagnosis-guided selective self-correction). Recovery exists as *rerun-with-guidance*, not as *containing an in-flight organizational cascade*.

**The missing connective tissue** (i.e., the seed's opportunity): runtime propagation measurement across organizational boundaries + containment actions graded between "do nothing / retry / quarantine agent / revoke delegation / escalate to human" + utility-preservation metrics. Verified absent as of 2026-09-21.

## 11. Does anything here kill or subsume the seed hypothesis?

**No kill.** Closest partial overlaps, adversarially stated:

- **MAS-FIRE** ([arXiv:2602.19843](https://arxiv.org/abs/2602.19843), Feb 2026): fault injection (15 fault types, 3 non-invasive mechanisms) + reliability evaluation of MAS; finds iterative/closed-loop topologies neutralize >40% of faults that collapse linear workflows. *This is the nearest neighbor to "failure propagation + recovery in MAS."* Differentiators that keep the seed alive: MAS-FIRE is an offline evaluation framework; faults are synthetic cognitive/coordination errors, not mapped to organizational boundary types (authority, memory, accountability, human-agent); no containment mechanisms are compared; no blast-radius metric.
- **AgentDebugX** (2607.18754): owns "detect→attribute→recover→rerun" as a debugging loop. Post-hoc, single workflow, no propagation containment, no organizational semantics.
- **Trace-level information contamination** ([arXiv:2604.27586](https://arxiv.org/abs/2604.27586), Apr 2026): measures propagation as trace divergence under injected perturbations (614 paired runs, GAIA); shows divergence↔correctness decoupling and that verification guardrails fail to intercept contamination. Closest *measurement* work; still single-workflow, no containment.
- **ParaRecover** (2609.12345, EMNLP 2026): cascading failures in parallel tool-use; single-agent.
- **Bounded Agents / OAP / ceLLMate**: already use "blast radius" — but strictly in the *authorization-scope* sense. **Terminology collision risk: the seed must explicitly disambiguate "organizational blast radius" (failure propagation across org boundaries) from "security blast radius" (attacker's reachable action scope).**
- **Multi-Agent AI Control** (2607.07368): warns per-instance monitoring fails under coordination — supports the seed's premise that system-level observability/containment is needed, but in the adversarial-misuse frame.
- **LIFE survey** ([arXiv:2605.14892](https://arxiv.org/abs/2605.14892), May 2026): surveys collaboration→attribution→self-evolution as causally linked stages and calls for closed-loop self-organizing MAS — a survey-level argument that the loop is open, corroborating the gap.

**Subsume risk: LOW-MODERATE.** A MASO paper must position against MAS-FIRE (evaluation vs. runtime containment), AgentDebugX/AgentTether (post-hoc/single-agent recovery), and the authorization cluster (pre-action vs. propagation-triggered). The distinctive, unoccupied claim is: **organizational boundary-aware blast-radius metrics + observability-triggered graded containment in multi-agent organizational workflows.**

## 12. Additional verified items worth knowing

- **ITBench** (IBM/UIUC, [arXiv:2502.05352](https://arxiv.org/abs/2502.05352), Feb 2025): agents that *consume* observability (SRE/CISO/FinOps incidents); SOTA resolves 13.8% of SRE scenarios. Inverse direction (agents as observability consumers) — potential source of testbeds/telemetry formats.
- **Agent Lightning** ([arXiv:2508.03680](https://arxiv.org/abs/2508.03680), Aug 2025, Microsoft): RL training for any agent; "brings agent observability frameworks into agent runtime" as training-data interface. Observability as RL substrate, not containment.
- **ToolEmu** ([arXiv:2309.15817](https://arxiv.org/abs/2309.15817), ICLR 2024): LM-emulated sandbox for finding agent risks pre-deployment.
- **AgentDojo** ([arXiv:2406.13352](https://arxiv.org/abs/2406.13352), NeurIPS 2024 D&B): standard attack/defense benchmark used by containment papers.
- **AgentHarm** ([arXiv:2410.09024](https://arxiv.org/abs/2410.09024), ICLR 2025): misuse benchmark.
- **AgentDoG + ATBench** ([arXiv:2601.18491](https://arxiv.org/abs/2601.18491), Jan 2026): diagnostic guardrail with 3D risk taxonomy (source/failure-mode/consequence), trajectory monitoring, root-cause diagnosis of unsafe actions; 4B/7B/8B models released.
- **Securing MCP** ([arXiv:2511.20920](https://arxiv.org/abs/2511.20920), Nov 2025; via HF search): MCP risks/controls/governance — relevant to tool-boundary containment.

## Appendix — search log (2026-09-21)

- arXiv API + arXiv search UI: HTTP 429 throughout (shared-IP limit); abs pages fetchable individually.
- Semantic Scholar Graph API: 429 throughout. DBLP: Anubis bot-wall. OpenAlex: shared daily budget exhausted. DuckDuckGo: captcha. Bing: poisoned/irrelevant results.
- Working channels: HuggingFace Papers API (`/api/papers/search?q=`), arXiv abs pages, Crossref API, GitHub API, official docs sites.
- Queries run (HF): agent observability; AgentTrace; MAS-FIRE; TraceElephant; Faramesh; Agentic CLEAR; Agent Lightning; ActiveGraph; ATBench; AgentLogs; AI Coding Agents Log; circuit breaker LLM agent; kill switch AI agent; anomaly detection agent workflow; runtime monitoring LLM agent; observability survey; failure propagation multi-agent LLM; cascading failure LLM agents; blast radius agent; containment LLM agents; recovery multi-agent LLM failure; guardrail multi-agent systems; self-healing LLM agents; agent recovery rollback; organizational multi-agent LLM; agent telemetry survey; monitoring agentic AI survey; agentic observability; OpenTelemetry agent; LLM observability survey; production monitoring AI agents.
