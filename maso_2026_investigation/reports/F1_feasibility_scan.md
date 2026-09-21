# F1 — Feasibility Scan: Code & Infrastructure for Organizational Failure-Propagation Research

**Investigator:** F1 (code/infrastructure feasibility)
**Date:** 21 September 2026
**Mission:** MASO 2026 seed hypothesis — organizational failure propagation / "blast radius" and containment in LLM multi-agent systems. This report assesses what code and infrastructure exists, what is reusable, and whether a controlled experiment is buildable and runnable before the 10 Oct 2026 deadline (19 days).

**Verification method:** every system below was verified by inspecting the actual arXiv abstract page, the actual GitHub repository (via authenticated `gh` API), and/or the Hugging Face dataset page on 21 Sep 2026. Prices were pulled live from the OpenRouter models API. Nothing here is from search snippets alone.

---

## 1. Bottom line

**FEASIBLE, with tight scoping.** A controlled 3-workflow organizational testbed with deterministic tools, fault injection, and logging is buildable in roughly **4–8 person-weeks** (less if reusing tau2-bench as substrate), API cost is **~$15–800 per 1,000 runs** depending on model tier, and a statistically meaningful factorial experiment is **achievable in 19 days** if (a) the team reuses an existing deterministic-tool substrate rather than building from scratch, and (b) the design is scoped to ~2–3 workflows × a small factorial. The two closest prior systems (MAS-FIRE, From Spark to Fire) have **no usable code release**, which is bad for reproducibility but good for novelty: the organizational-boundary framing (role/authority/delegation/accountability blast radius + containment) is not occupied by any available artifact.

---

## 2. Failure-injection / failure-attribution systems (closest to seed)

| System | Paper (verified) | Venue | Code | License | Reusability verdict |
|---|---|---|---|---|---|
| **Who&When** | "Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems", Zhang et al., [arXiv:2505.00212](https://arxiv.org/abs/2505.00212) (v3, Jun 2025) | ICML 2025 Spotlight | [github.com/mingyin1/Agents_Failure_Attribution](https://github.com/mingyin1/Agents_Failure_Attribution) — 34★, last push Jan 2026; dataset at [HF Kevin355/Who_and_When](https://huggingface.co/datasets/Kevin355/Who_and_When) (verified live) | MIT (badge; LICENSE file present) | **Reusable as dataset + attribution baselines.** 184 annotated failure logs (algorithm-generated via CaptainAgent + hand-crafted Magentic-One), tasks from GAIA/AssistantBench. Best attribution method: 53.5% agent accuracy, 14.2% step accuracy. NOT a fault-injection or propagation testbed; logs are from web-task MAS, not organizational workflows. |
| **MAS-FIRE** | "MAS-FIRE: Fault Injection and Reliability Evaluation for LLM-Based Multi-Agent Systems", Jia, Deng, Chen, Wang, Zheng, [arXiv:2602.19843](https://arxiv.org/abs/2602.19843) (Feb 2026) | arXiv (cs.SE) | [github.com/wxhhxn/MASFIRE](https://github.com/wxhhxn/MASFIRE) — 3★, **data only** (result CSVs for CAMEL/MetaGPT/Table-Critic × DeepSeek-v3/GPT-5, baseline vs injection). Root contains only README/data/images — **no injection framework code released** | None | **Taxonomy reusable, code NOT.** 15 fault types (intra-agent cognitive + inter-agent coordination), 3 non-invasive injection mechanisms (prompt modification, response rewriting, message-routing manipulation), 4-tier fault-tolerance model. Key finding: iterative closed-loop topologies neutralize >40% of faults that collapse linear workflows. Directly adjacent to seed — must be cited and differentiated (they do not model organizational boundaries, authority, or containment policies). |
| **AgentChaos** | "AgentChaos: Chaos Engineering for Agent Systems via Programmatic Fault Injection", Tan et al., [arXiv:2608.06790](https://arxiv.org/abs/2608.06790) (Aug 2026), DOI 10.1145/3832783.3837437 | **ASE 2026** (accepted) | [github.com/IntelligentDDS/AgentChaos](https://github.com/IntelligentDDS/AgentChaos) — 3★, real code (scripts/, datasets/, pyproject.toml), Python 3.12 | MIT (README badge) | **Most reusable injection machinery.** Runtime, non-intrusive fault injection at the LLM HTTP API layer — works on any agent system without source modification. 65 fault configurations (6 fault types × 2 target fields × 4 strategies + position/compound), crash/omission/value faults on content and tool-call fields, trigger verification. Evaluated on AutoGen, MAD, MapCoder, EvoMAC, Mini-SE over HumanEval/MBPP/MATH/MMLU-Pro/SWE-bench-Pro. Finding: pass@1 drops up to 50pp; robustness depends on system implementation, not model. Limitation for seed: injects *infrastructure/API* faults, not semantic/organizational faults; no org roles or containment mechanisms. |
| **From Spark to Fire** | "From Spark to Fire: Modeling and Mitigating Error Cascades in LLM-Based Multi-Agent Collaboration", Xie, Zhu, Zhang, Zhu, Ye, Qi, Chen, Zhou, [arXiv:2603.04474](https://arxiv.org/abs/2603.04474) (v2, May 2026) | arXiv (cs.MA) | **None found.** No GitHub link in arXiv HTML; GitHub search for title/genealogy-graph terms returns nothing | — | **Conceptually closest to seed; not reusable.** Propagation-dynamics model over directed dependency graphs, early-stage amplification-risk criterion, 3 vulnerability classes (cascade amplification, topological sensitivity, consensus inertia), single atomic error seed → widespread failure, genealogy-graph governance plugin raises defense success 0.32→≥0.89 across six frameworks. This is the paper the seed must most clearly differentiate from: it models error *cascades* but through message dependencies, not organizational boundaries (authority, delegation, accountability), and its mitigation is a message-layer plugin, not containment/recovery policies. No code = cannot build on it, must reimplement any comparison. |

**Adversarial note for the swarm:** these four together mean "fault injection in LLM-MAS" and "error cascade modeling" are *occupied territory as of Feb–Aug 2026*. The seed survives only in its **organizational** framing: blast radius measured across role/communication/authority/tool/memory/accountability/human boundaries, and containment/recovery *mechanisms* as the independent variable. None of the four has organizational workflows, authority structure, or containment-policy comparison. MAS-FIRE and AgentChaos being SE-venue papers (and Who&When ICML) also means MASO reviewers may not know them — but we must cite all four or risk a novelty kill.

---

## 3. Benchmark environments (candidate substrates)

| Benchmark | Paper (verified) | Code (verified 21 Sep 2026) | Setup cost | Fit for organizational fault-injection testbed |
|---|---|---|---|---|
| **tau-bench / tau2-bench** | τ-bench [arXiv:2406.12045](https://arxiv.org/abs/2406.12045) (Jun 2024); τ²-bench [arXiv:2506.07982](https://arxiv.org/abs/2506.07982) (Jun 2025) | [sierra-research/tau-bench](https://github.com/sierra-research/tau-bench) 1.4k★ MIT (quiet since Mar 2026); [sierra-research/tau2-bench](https://github.com/sierra-research/tau2-bench) 2.1k★ MIT, **very active** (pushed 19 Sep 2026), now τ³-bench v1.0.1 with domains: mock, airline, retail, telecom, banking_knowledge | **Low** — pure Python (`uv` install, Py3.12), no servers | **Best substrate.** Deterministic tools + database-state-based evaluation (compare end DB state to annotated goal state) = exactly the "deterministic tools + verifiable outcomes" the seed needs. Policy documents per domain ≈ organizational policy. Retail domain ≈ customer-service refund workflow out of the box. Compositional task generator (τ²) enables controlled task families. pass^k metric suits reliability statistics. Single-agent + simulated user by default — multi-agent org structure must be added on top. |
| **TheAgentCompany** | [arXiv:2412.14161](https://arxiv.org/abs/2412.14161) (Dec 2024, v3 Sep 2025) | [TheAgentCompany/TheAgentCompany](https://github.com/TheAgentCompany/TheAgentCompany) 781★ MIT, last push Nov 2025 | **High** — Docker + docker-compose, 30+ GB disk, self-hosted GitLab/Plane/ownCloud/RocketChat with pre-baked data; per-task Docker images | Richest *organizational* environment (simulated software company, coworker communication via RocketChat). But heavy infra, single-agent-against-environment design, and checkpoint-based task graders. Reusable for an "IT incident" style workflow only with real engineering effort; risky under a 19-day deadline. |
| **WorkArena / WorkArena++** | WorkArena [arXiv:2403.07718](https://arxiv.org/abs/2403.07718) (Mar 2024); WorkArena++ [arXiv:2407.05291](https://arxiv.org/abs/2407.05291) (Jul 2024, NeurIPS 2024) | [ServiceNow/WorkArena](https://github.com/ServiceNow/WorkArena) 274★, Apache-2.0 (LICENSE verified; API says NOASSERTION due to rider files), active (Apr 2026); BrowserGym ecosystem [arXiv:2412.05467], AgentLab runner | **High** — requires ServiceNow developer instance access, browser automation stack | 33 + 682 enterprise knowledge-work tasks on real ServiceNow — genuinely organizational (ITSM: incidents, requests, approvals). But browser-GUI agents are the wrong abstraction layer for controlled fault injection; non-deterministic web UI fights the "deterministic tools" requirement. Not recommended for this deadline. |
| **OSWorld** | [arXiv:2404.07972](https://arxiv.org/abs/2404.07972) (Apr 2024, NeurIPS 2024) | [xlang-ai/OSWorld](https://github.com/xlang-ai/OSWorld) 3.2k★ Apache-2.0, active (Sep 2026) | **Very high** — VM provisioning (Ubuntu/Windows/macOS), execution-based evaluators | Real OS control, 369 tasks. Wrong layer entirely (GUI grounding, single agent). Not relevant except as a citation for execution-based evaluation design. |

**Substrate recommendation:** build the testbed on **tau2-bench's deterministic-tool + DB-state-eval pattern** (reuse retail domain for the refund workflow; author IT-incident and procurement domains in the same style), and drive the multi-agent organization from **LangGraph** (see §4). Reserve TheAgentCompany as a "validation on a realistic environment" stretch goal only.

---

## 4. Frameworks for building the organizational workflow testbed

| Framework | Repo (verified) | License | Status (21 Sep 2026) | Fault-injection / determinism fit |
|---|---|---|---|---|
| **LangGraph** | [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) 42k★ | MIT | Very active (pushed 20 Sep 2026) | **Recommended.** Explicit graph topology = org chart is directly expressible (roles as nodes, authority as edge-level policy). Durable execution/checkpointing (persist through failures, resume from exact state) = built-in recovery mechanism to ablate. Interrupts = human-in-the-loop boundary. Deterministic tools = plain Python functions. Fault injection via middleware/wrapping LLM calls or adopting AgentChaos's HTTP-layer approach. |
| **AutoGen** | [microsoft/autogen](https://github.com/microsoft/autogen) 61k★ | MIT code / CC-BY docs | **MAINTENANCE MODE** (verified in README): "will not receive new features… community managed"; Microsoft points new users to **Microsoft Agent Framework** (github.com/microsoft/agent-framework, production 1.0, A2A+MCP support). Last push Apr 2026 | Do not build new work on AutoGen. Note: Who&When and AgentChaos both evaluate AutoGen-based systems, so it may still be needed as a *comparison target*, not as the testbed base. |
| **CrewAI** | [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) 59k★ | MIT | Very active (pushed 21 Sep 2026) | Role/crew metaphor matches organizational framing (roles, delegation flags, hierarchical process with manager agent). Weaker state/checkpoint model than LangGraph; fine for rapid prototyping of role-based crews, less control for fine-grained fault injection. |
| **OpenAI Agents SDK** | [openai/openai-agents-python](https://github.com/openai/openai-agents-python) 30k★ | MIT | Very active (pushed 21 Sep 2026) | Handoffs (delegation), guardrails (containment hooks!), sessions, built-in tracing (logging for free). Guardrails are directly reusable as a containment-mechanism condition. Lightweight; less topology control than LangGraph. Provider-agnostic via LiteLLM-style adapters but OpenAI-first. |
| **AgentScope** | [agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope) 32k★ | Apache-2.0 | Very active (pushed 21 Sep 2026); paper: AgentScope 1.0, [arXiv:2508.16279](https://arxiv.org/abs/2508.16279) (Aug 2025, Alibaba) | ReAct-based, async, realtime interruption & resume, runtime sandbox, evaluation module with tracing studio. Strong engineering; message-hub model suits communication-boundary studies. Larger API surface to learn under deadline. |

**Framework recommendation:** **LangGraph** as the primary testbed (topology control + checkpointing-as-recovery + interrupts-as-human-boundary), with **OpenAI Agents SDK guardrails** as the model for one containment condition, and AgentChaos-style HTTP interception as the injection layer so the same faults can be applied framework-agnostically.

---

## 5. Engineering effort estimate — 3 workflows + fault injection + logging

Assumes 1–2 competent engineers, Python, reuse of tau2-bench patterns and LangGraph.

| Work package | Estimate (person-weeks) | Notes |
|---|---|---|
| Workflow 1: customer-service refund | 0.5–1 | Adapt tau2-bench retail domain (tools, policy, DB already exist); wrap in multi-agent org (frontline agent → supervisor → finance approver) |
| Workflow 2: IT incident response | 1–1.5 | New domain: deterministic mock tools (ticket system, monitoring API, runbook lookup, restart-service with state), policy doc, ~30–50 tasks |
| Workflow 3: procurement approval | 1–1.5 | New domain: vendor DB, budget tools, PO creation, multi-level approval chain; ~30–50 tasks |
| Fault injection layer | 1–1.5 | Reimplement MAS-FIRE-style semantic faults (prompt modification, response rewriting, message routing) + AgentChaos-style API faults; injection scheduling + trigger logging |
| Blast-radius instrumentation & logging | 0.5–1 | Per-run JSONL traces: which roles/tools/memories/authority boundaries touched by fault; DB-state divergence metrics; LangSmith or custom |
| Containment/recovery mechanisms | 1–2 | 3–4 conditions: none, checkpoint-rollback (LangGraph), guardrail/validation gate (Agents-SDK-style), human escalation (interrupt) |
| **Total** | **5–9 pw** (realistic midpoint ~6) | With 2 people = ~3–4.5 calendar weeks — **exceeds the 19-day window unless descoped** |

**Descoping options that preserve the contribution:** (a) 2 workflows instead of 3 (refund + IT incident) → saves ~1–1.5 pw; (b) fault taxonomy cut to 6–8 types spanning the boundary categories rather than 15; (c) containment conditions cut to 3 (none / rollback / validation-gate). Descoped: **~3.5–5 pw**, i.e. 2 people × 19 days is feasible with discipline, 1 person is not.

---

## 6. API cost per 1,000 runs (prices verified live via OpenRouter API, 21 Sep 2026)

Assumptions per run: 5–8 agents, 30–60 LLM calls, history accumulation → ~150k input + ~20k output tokens per run (mid estimate for a 15–25 step organizational workflow).

| Model | $/M in | $/M out | Cost per run | **Cost per 1,000 runs** |
|---|---|---|---|---|
| GPT-5-nano | 0.05 | 0.40 | ~$0.016 | **~$16** |
| Gemini 2.5 Flash-Lite | 0.10 | 0.40 | ~$0.023 | **~$23** |
| DeepSeek v3.2 | 0.269 | 0.40 | ~$0.048 | **~$48** |
| GPT-5-mini | 0.25 | 2.00 | ~$0.078 | **~$78** |
| GPT-4.1-mini | 0.40 | 1.60 | ~$0.092 | **~$92** |
| GPT-5 / GPT-5.1 | 1.25 | 10.00 | ~$0.39 | **~$390** |
| Claude Haiku 4.5 | 1.00 | 5.00 | ~$0.25 | **~$250** |
| Claude Sonnet 4.5 | 3.00 | 15.00 | ~$0.75 | **~$750** |

A full factorial (e.g., 2 workflows × 3 topologies × 6 fault types × 3 containment conditions × 30 reps = 3,240 runs) costs **~$50–250 on GPT-5-mini/DeepSeek class models, ~$1,300 on GPT-5**. Batch APIs halve input/output prices (verified batch tiers exist for GPT-5-mini, GPT-5.1, Claude, Gemini). Budget is not a binding constraint; engineering time is.

---

## 7. Statistical feasibility by 10 Oct 2026 (19 days)

- **Sample size:** binary containment outcome, n=30/cell detects ~25–30pp differences (two-proportion test, α=.05, power .8); n=50/cell detects ~20pp. Continuous blast-radius metric (fraction of downstream roles/tools/records corrupted, DB-state divergence) is more powered — n=20–30/cell suffices for large effects (d≈0.8). tau2-bench's pass^k convention supports reliability claims.
- **Throughput:** at ~1–2 min/run and 20–50 parallel workers, 3–5k runs = a few hours per model. Rate limits, not money, set the pace; use 2 providers or batch API.
- **Timeline:** days 1–8 build (2 engineers, descoped), days 9–11 pilot + injection-trigger verification (AgentChaos's lesson: filter untriggered faults or you underestimate impact), days 12–16 main runs, days 17–19 analysis + writing. **Feasible for a short/workshop paper; zero slack for infra surprises.** Biggest schedule risks: (1) multi-agent org wrapper around tau2-bench domains taking longer than estimated; (2) fault-trigger rates lower than expected requiring injection redesign; (3) LLM nondeterminism forcing higher rep counts.

---

## 8. Does any of this kill or subsume the seed hypothesis?

**No kill, but the flanks are crowded.** Verified, adjacent 2025–2026 work: Who&When (failure *attribution*, ICML 2025, code+data available), MAS-FIRE (fault injection + reliability tiers, Feb 2026, **no code**), From Spark to Fire (error-cascade modeling + message-layer mitigation, Mar 2026, **no code**), AgentChaos (API-layer chaos engineering, ASE 2026, code available). None studies **organizational boundaries** (role, authority/delegation, accountability, human-agent) as the unit of blast radius, none compares **containment/recovery mechanisms**, and none uses **organizational workflows with deterministic tools**. The seed is feasible and differentiable — but the paper must cite all four and position explicitly against them, and "blast radius" framing should be checked against MAS-FIRE's propagation findings and Spark-to-Fire's cascade model (both predate us in 2026).

---

## Appendix: verification log (all checked 21 Sep 2026)

- arXiv abstract pages fetched directly: 2505.00212 (v3), 2412.14161 (v3), 2406.12045, 2506.07982, 2403.07718 (v5), 2407.05291 (v2), 2404.07972 (v2), 2602.19843, 2603.04474 (v2), 2608.06790, 2508.16279.
- GitHub repos inspected via authenticated API (stars/license/last-push/contents): mingyin1/Agents_Failure_Attribution, wxhhxn/MASFIRE (data-only confirmed), IntelligentDDS/AgentChaos (code confirmed), TheAgentCompany/TheAgentCompany, ServiceNow/WorkArena (+LICENSE file read: Apache-2.0), sierra-research/tau-bench, sierra-research/tau2-bench (README read: τ³ v1.0.1, domains list), xlang-ai/OSWorld, langchain-ai/langgraph, microsoft/autogen (maintenance-mode notice read), crewAIInc/crewAI, openai/openai-agents-python, agentscope-ai/agentscope.
- HF dataset Kevin355/Who_and_When fetched and contents eyeballed (failure logs with responsible-agent + step annotations).
- Prices: OpenRouter `/api/v1/models` live pull, 21 Sep 2026.
- From Spark to Fire code: searched GitHub (title + "genealogy graph governance" queries) — no repository found; arXiv HTML contains no code link.
