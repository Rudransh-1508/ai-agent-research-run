# D5 — Mandatory Papers: Organizational / Evaluation Surveys — Verification & Positioning

**Investigator:** D5 specialist (adversarial evidence-gathering)
**Date:** 2026-09-21
**Seed hypothesis under test:** *Organizational failure propagation and recovery in LLM multi-agent systems* — when a local fault occurs in an organizational multi-agent workflow, what determines its "organizational blast radius" (spread across role, communication, authority/delegation, tool, memory, accountability, and human-agent boundaries), and which containment/recovery mechanisms minimize systemic impact while preserving task utility.

**Scope of this report:** Verify and position five assigned papers; record full structured metadata; extract the open gaps each survey explicitly names; and answer whether any of them kills or subsumes the seed hypothesis.

**Verification method:** Every paper was located and confirmed by inspecting the actual arXiv abstract page (arxiv.org/abs/...), the arXiv full-text HTML, Crossref (`api.crossref.org`), and the Semantic Scholar Graph API. arXiv/SemanticScholar/OpenAlex/DBLP search APIs were heavily rate-limited or bot-walled on this IP during the run; identification therefore relied on Google Scholar result HTML (title↔arXiv-link extraction) plus direct abstract-page fetches. No citation below is asserted without a fetched primary page.

---

## Bottom-line judgment

**None of the five assigned papers kills or subsumes the seed hypothesis.** Four of the five are *evaluation-methodology* or *single-agent long-horizon* works that do not study inter-agent failure propagation, blast-radius determinants, or runtime containment/recovery at all. The one genuinely close work — the **"Beyond Individual Intelligence" survey (Qi et al., arXiv:2605.14892)** — surveys failure propagation, failure attribution, and self-evolution, and it **explicitly names "failure propagation" and "repair mechanisms" as open, under-integrated challenges**. That is evidence the seed territory is *recognized as open*, not solved. However, it substantially crowds the "failure propagation + diagnosis + recovery" neighborhood and raises the positioning bar: the seed's defensible core must be **organizational blast-radius *determinants* and runtime *containment/recovery* mechanisms** (a resilience/fault-tolerance framing), clearly differentiated from the existing **attribution-accuracy** and **self-evolution** framing that Qi et al. survey.

---

## Evidence table (verified identifiers)

| # | Short name | Exact title | Authors | Venue | arXiv / DOI | Date | Verified via |
|---|-----------|-------------|---------|-------|-------------|------|--------------|
| 1 | Org-Science / IMACS | Toward an Organizational Science of Multi-Agent LLM Systems: Decoupling Who, How, and Which Algorithm | Huan Chen, Xiang Song, Jian Jin, Pan Ren, Liang-Jie Zhang | arXiv preprint (8 pp, 2 figs) | arXiv:2607.25446 [cs.AI] | v1 2026-07-28 | arXiv abs + full HTML |
| 2 | CEO-Bench | CEO-Bench: Can Agents Play the Long Game? | Haozhe Chen, Karthik Narasimhan, Zhuang Liu | arXiv preprint (Princeton) | arXiv:2606.18543 [cs.AI] | v1 2026-06-16; v2 2026-07-22 | arXiv abs + full HTML |
| 3 | Yehudai eval survey | (A) Survey on Evaluation of LLM-based Agents | Asaf Yehudai, Lilach Eden, Alan Li, Guy Uziel, Yilun Zhao, Roy Bar-Haim, Arman Cohan, Michal Shmueli-Scheuer | **ACL Findings** | arXiv:2503.16416 [cs.AI] | v1 2025-03-20; v2 2026-04-23 | arXiv abs + full HTML |
| 4 | Mohammadi eval survey | Evaluation and Benchmarking of LLM Agents: A Survey | Mahmoud Mohammadi, Yipeng Li, Jean-Pierre Lo, Wendy Yip | **KDD 2025** (SAP Labs) | arXiv:2507.21504 [cs.LG]; DOI 10.1145/3711896.3736570; DBLP conf/kdd/MohammadiLLY25 | arXiv v1 2025-07-29; pub 2025-08-03 | arXiv abs + Crossref + S2 |
| 5 | BII survey (Qi et al.) | Beyond Individual Intelligence: Surveying Collaboration, Failure Attribution, and Self-Evolution in LLM-based Multi-Agent Systems | Shihao Qi, Jie Ma, Rui Xing, Wei Guo, Xiao Huang, Zhitao Gao, Jianhao Deng, Jun Liu, Lingling Zhang, Bifan Wei, Boqian Yang, Pinghui Wang, Jianwen Sun, Jing Tao, Yaqiang Wu, Hui Liu, Yu Yao, Tongliang Liu | arXiv preprint (Xi'an Jiaotong U., Lenovo, U. Sydney, et al.) | arXiv:2605.14892 [cs.AI] | v1 2026-05-14; v2 2026-05-15 | arXiv abs + full HTML |

**Adjacent canonical reference (verified, not one of the 5 but load-bearing for the "subsumption" question):** *Why Do Multi-Agent LLM Systems Fail?* — Mert Cemri, Melissa Z. Pan, Shuyi Yang, Lakshya A. Agrawal, Bhavya Chopra, Rishabh Tiwari, Kurt Keutzer, Aditya Parameswaran, Dan Klein, Kannan Ramchandran, Matei Zaharia, Joseph E. Gonzalez, Ion Stoica — **arXiv:2503.13657**, 2025-03-17, NeurIPS 2025 (the "MAST" multi-agent failure-taxonomy paper). Cited by both #1 and the failure-attribution ecosystem surveyed by #5.

---

## Full structured records

### 1. Toward an Organizational Science of Multi-Agent LLM Systems (IMACS) — arXiv:2607.25446

- **Research problem:** MAS frameworks entangle three logically distinct concerns — *who* is on the team (organization), *how* members align (coordination), and *which algorithm* fuses their work (collaboration protocol). Argues these should be orthogonal, independently swappable layers.
- **Method:** IMACS (Intelligent Multi-Agent Collaboration System), a 7-layer stack on AgentScope 2.0. Formalizes an organization as `O=(R,μ,κ,ρ)` (Belbin roles, model binding, Mintzberg coordination, RACI tags with at-most-one-Accountable constraint) and a protocol as `π:(Task,Team,Blackboard)→Result`; proves an orthogonality property (Prop. 1). Adds **Adaptive Org Routing**, a LinUCB contextual bandit that picks a protocol per task under a quality–cost trade-off (`r = quality − λ·cost`), with Sherman–Morrison online updates.
- **Experimental setting:** Controlled RACI ablations (3 repeats) holding the team fixed and varying only the Accountable tag; real-benchmark cells; a *simulated oracle* for routing/regret.
- **Benchmarks/metrics:** GSM8K (exact-match), HumanEval (pass@1), HotpotQA (token-F1), AgentsNet (formal validity), AlpacaEval (LLM-judge win-rate; judge=GLM-5.2); cost-adjusted reward, routing accuracy, regret, latency. Models: DeepSeek-V4 (pro/flash), Qwen3.7-plus, GLM-5.2, MiniMax-M3.
- **Major findings:** (a) Accountability placement changes outcomes **exactly when the protocol routes the deliverable through the accountable agent** (replicated, sign-consistent for LLM-Blender; null for voting/debate which never read the tag); (b) the winning placement **flips across model families** → organizational design cannot be hard-coded, must be re-validated or learned per model binding; (c) Adaptive Org Routing beats all six fixed protocols (0.708 vs best-fixed MoA 0.669), 82% routing accuracy, recovers ~45% of best-fixed→oracle headroom.
- **Author-stated limitations:** synthetic oracle is a stand-in calibrated to literature trends; LinUCB linearity assumption; tiny samples (N=10/cell, RACI 3 repeats → directional, not leaderboard claims); cost = model-call multiplicity, not billing; **benchmarks "do not cover long-horizon tool use, human approval loops, or failures caused by changing external state"**; AgentsNet run as whole-graph, not partial-visibility; English-centric lightweight features; model-binding dependence.
- **Inferred limitations:** Position/framework paper whose headline router number comes from a *simulated* oracle; accountability studied only as a RACI routing tag, **not** as blame/blast-radius under injected faults; no failure-propagation, containment, or recovery analysis.
- **Code availability:** Claims a "modular, reproducible framework, released with this paper" on AgentScope 2.0, but **no repository URL was found** on the abstract page or in the extracted full text.
- **Relationship to seed:** *Adjacent, supportive of premise.* Establishes that organizational variables (roles, coordination, accountability/authority) are a real, independent, model-dependent lever on outcomes — which the seed's "authority/delegation" and "accountability" boundaries presuppose. But it explicitly scopes out failures from changing state and does not study propagation or containment. **Does not subsume the seed.**

### 2. CEO-Bench: Can Agents Play the Long Game? — arXiv:2606.18543

- **Research problem:** Agents are good at isolated short-horizon tasks; untested are (1) long horizons amid uncertainty, (2) acquiring information in noisy environments, (3) adapting to a changing world, (4) orchestrating many moving parts toward a coherent goal.
- **Method:** Simulate operating a startup for **500 days**. A **single agent** manages pricing, marketing, budgeting, etc. through a programmable Python interface over business databases / company tools / social media. Outcomes driven by a partially observable, noisy, evolving market with delayed, coupled consequences; explicit mechanisms (microeconomics-motivated participation rule) rather than an LLM judge.
- **Experimental setting / metrics:** Final cash on hand vs $1M starting balance; bankruptcy; comparison to a non-LLM rule-based baseline and an estimated attainable-cash upper bound (~$2.2B after a friction adjustment).
- **Models:** Claude Fable 5, GPT-5.6 Sol, Claude Opus 4.8, GPT-5.5, GLM 5.1, DeepSeek V4 Pro, Gemini 3 Flash, Grok 4.20.
- **Major findings:** Most SOTA models struggle and often bankrupt; only Claude Fable 5, GPT-5.6 Sol, Claude Opus 4.8 finish above $1M (best runs); **all evaluated models remain below the rule-based baseline**; benchmark far from saturated. Noted environment mechanic: "reputation propagates across related groups, so a quality failure in one enterprise group can spill into nearby groups" — but this is *environment-side* spillover, not inter-agent propagation.
- **Author-stated limitations:** Approximates reality; products simulated only via a scalar quality measure (no qualitative product changes); limited action scope; **leaves out compliance, security, and fundraising**.
- **Inferred limitations:** **Single-agent**, not multi-agent — no roles, delegation, communication, or accountability boundaries; no inter-agent blast radius; not a containment/recovery testbed.
- **Code availability:** Programmable Python interface described; **no repository URL found** on the abstract page.
- **Relationship to seed:** *Tangential.* A long-horizon **single-agent** strategic-control benchmark. Could serve as a long-horizon harness, but it does not address multi-agent organizational failure propagation, blast radius, or containment/recovery. **Does not subsume the seed.**

### 3. (A) Survey on Evaluation of LLM-based Agents — arXiv:2503.16416 (ACL Findings)

- **Research problem:** First comprehensive survey of evaluation methods for LLM-based agents.
- **Method / taxonomy:** Five perspectives — (1) core LLM capabilities for agentic workflows (planning, tool use); (2) application-specific benchmarks (web, SWE agents); (3) generalist-agent evaluation; (4) analysis of benchmark core dimensions; (5) evaluation frameworks and tools for developers (LangSmith, Langfuse, Vertex AI, Arize, Galileo, Patronus, W&B Weave, AgentEvals, Databricks Mosaic, AutoGen, etc.). Distinguishes final-response / stepwise / trajectory-based assessment; reference-based vs reference-free judging.
- **Experimental setting / datasets / metrics:** N/A (survey); catalogs benchmarks (SWE-bench, WebArena, τ-bench, GAIA, AppWorld, OS-World, BFCL, HAL, etc.) and metrics (task completion, latency, pass@k / pass^k, tool-call correctness, trajectory alignment).
- **Major findings:** Field is shifting toward more realistic, challenging, continuously updated benchmarks; evaluation frameworks are valuable but lack granular behavioral insight and built-in safety/policy-compliance support.
- **Open gaps explicitly named (§7.2 Future Directions):**
  1. **Fine-grained diagnosis** — coarse end-to-end success metrics "fall short in diagnosing specific agent failures"; need standardized step-by-step / trajectory metrics.
  2. **Cost-efficiency** — overlooked; should be a core metric (token usage, API cost, inference time).
  3. **Safety** — lack comprehensive tests for adversarial robustness, bias mitigation, and **organizational and societal policy compliance**; need safety benchmarks "**particularly in multi-agent scenarios where emergent risks may arise**."
  4. **Controlled protocols** — vary each factor (LLM capability, harness, memory, planning) independently.
  5. **Fine-grained, scalable methods** with standardized cost/safety/robustness metrics.
- **Author-stated limitations:** Survey scope/selection bias (mitigated via domain-expert consultation); future-directions section is inherently interpretive.
- **Code availability:** None (survey).
- **Relationship to seed:** Evaluation-methodology survey. It *names* multi-agent emergent risk and organizational policy compliance as open evaluation gaps, but does not study failure propagation, blast-radius determinants, or containment/recovery. **Does not subsume the seed**; useful for framing how a blast-radius benchmark should be evaluated.

### 4. Evaluation and Benchmarking of LLM Agents: A Survey — arXiv:2507.21504 / KDD 2025

- **Research problem:** LLM-agent evaluation is complex and underdeveloped; existing surveys are narrow and ignore enterprise requirements.
- **Method / taxonomy:** Two-dimensional taxonomy — (1) **evaluation objectives** (what: agent behavior, capabilities [tool use, planning/reasoning, memory, multi-agent collaboration], reliability, safety/alignment) × (2) **evaluation process** (how: interaction modes, datasets/benchmarks, metric computation, tooling).
- **Experimental setting / datasets / metrics:** N/A (survey); catalogs benchmarks (WebArena, AppWorld, AssistantBench, AgentHarm, AgentDojo, BFCL, Holistic Agent Leaderboard, TheAgentCompany, IntellAgent, CoSafe, etc.) and metrics (pass@k, pass^k, Step Success Rate, Collaborative Efficiency, Factual Recall / Consistency).
- **Major findings:** Enterprise deployment demands RBAC-aware, reliability-guaranteed, long-horizon, compliance-checked evaluation — rarely addressed.
- **Enterprise-specific challenges named (§5):** Role-Based Access Control (RBAC); reliability guarantees (audit/compliance, determinism); dynamic & long-horizon interaction (performance drift, cumulative effects); domain-specific policy & compliance (GDPR/HIPAA, approval workflows).
- **Future directions explicitly named (§6):** (1) **Holistic** evaluation frameworks across interdependent dimensions; (2) **more realistic** settings (dynamic multi-user, RBAC, domain knowledge); (3) **automated & scalable** evaluation (synthetic data, LLM-as-judge / Agent-as-a-judge); (4) **time- and cost-bounded** evaluation protocols.
- **Author-stated limitations:** Enterprise concerns "usually overlooked during evaluation"; reliability measurement is costly (repeated trials).
- **Code availability:** None (survey); open-access PDF (CC-BY) via ACM.
- **Relationship to seed:** Evaluation-methodology survey with an **enterprise/RBAC/compliance** angle that is *conceptually adjacent* to the seed's "authority/delegation" and "accountability" boundaries (e.g., TheAgentCompany's organizational-policy constraints). But it does not study inter-agent failure propagation, blast radius, or containment/recovery. **Does not subsume the seed.**

### 5. Beyond Individual Intelligence (LIFE survey) — arXiv:2605.14892  ⚠ closest to the seed

- **Research problem:** Tighter multi-agent coordination amplifies a less-explored risk — **errors propagate across agents and interaction rounds, producing failures that are hard to diagnose and rarely translate into structural self-improvement**. Existing surveys treat capability, collaboration, and self-evolution in isolation, leaving causal dependencies unexamined.
- **Method / taxonomy:** Unified survey organized around the causally linked **LIFE progression** — **L**ay the capability foundation → **I**ntegrate agents through collaboration → **F**ind faults through attribution → **E**volve through autonomous self-improvement. Provides per-stage taxonomies, formalizes dependencies between adjacent stages, identifies open challenges at stage boundaries, and proposes a cross-stage research agenda for closed-loop, self-organizing MAS. Claims a "publicly maintained repository" of structured literature (no URL extracted).
- **Experimental setting / datasets / metrics:** N/A (survey), but it catalogs the failure-attribution ecosystem: **AgentFail, FailCycle, AGENTSCOPE/AgentErrata, GraphTracer, CORRECT / CORRECT-Error, AgentAsk, Trajectory Guard, Trajectory Graph Copilot, DiLLS, A2P, DoVer, Role-Trace, AgentRx, XAgen, AgentTrace, AGENTRACER, AEGIS**, plus causal-attribution theory (Agent-Specific Effects, Triantafyllou et al., Shapley/causal-discovery methods).
- **Major findings (synthesis):** Errors often do not manifest where introduced — they "propagate, accumulate, or even evolve through subsequent interactions before surfacing as system-level failures," so the observable point ≠ the true origin; sequential pipelines risk error propagation while parallel pipelines improve robustness but create aggregation problems.
- **Open challenges explicitly named (failure-attribution discussion + future work):**
  1. The central difficulty is **integrating five elements studied in isolation: attribution semantics, failure propagation, diagnostic granularity, data realism, and repair mechanisms**.
  2. Current formulations reduce attribution to a responsible agent / critical step / single cause, with **limited treatment of *how* anomalies propagate across agents, modules, and execution stages** → methods mistake downstream symptoms for root causes.
  3. **Fine-grained attribution** lacks robust methods for long-horizon, multi-role, multi-level dependency structures.
  4. Attribution evaluation is **weakly connected to downstream verification, intervention, and repair** — no robust closed loop from failure identification → root-cause confirmation → repair feedback.
  5. Need a **unified, extensible failure-classification/attribution framework** capturing multi-cause, multi-effect, and failure propagation.
  6. Dataset bottlenecks: scarce high-quality open datasets; annotation fidelity vs scalability; no unified standards for attribution granularity or evaluation protocols.
- **Author-stated limitations:** (implied) fragmentation of the threads it bridges; the attribution/self-correction deficits are "deeply intertwined" and unresolved.
- **Inferred limitations:** As a survey it proposes no new mechanism; its recovery treatment is framed as **self-evolution** (long-horizon structural improvement), not **runtime containment** that limits blast radius while preserving task utility.
- **Code availability:** Claims a curated public repository; **no URL extracted** from the fetched text.
- **Relationship to seed:** **Closest prior work.** It directly covers failure propagation and attribution and names "failure propagation" and "repair mechanisms" as open. This *validates the gap* the seed targets. But its center of gravity is **attribution accuracy** (post-hoc diagnosis) and **self-evolution** (long-term improvement) — **not** the seed's distinct focus on **what determines organizational blast radius** across role/communication/authority/tool/memory/accountability/human boundaries, and **which runtime containment/recovery mechanisms** minimize systemic impact while preserving task utility. **Partially crowds the neighborhood; does not kill the seed, but forces sharp differentiation.**

---

## Does anything here kill or subsume the seed hypothesis?

**No — nothing here kills the seed.** Specifically:

- **Not killed:** No assigned paper studies organizational blast-radius *determinants* or runtime *containment/recovery* under injected local faults. CEO-Bench is single-agent; the two evaluation surveys are methodology; the IMACS paper studies org-design-for-quality, not failure containment.
- **Closest / partially crowding (must cite & differentiate):** **Qi et al. arXiv:2605.14892** (failure propagation + attribution + self-evolution) and the canonical taxonomy **Cemri et al. arXiv:2503.13657** ("Why Do Multi-Agent LLM Systems Fail?", NeurIPS 2025). Qi et al. explicitly list "failure propagation" and "repair mechanisms" as **open and under-integrated**, and note attribution is "weakly connected to downstream verification, intervention, and repair." This is direct evidence the seed's territory is *unsolved*.
- **Differentiation required (adversarial note):** The seed must not be framed as "failure attribution" (heavily surveyed: AgentFail, GraphTracer, A2P, DoVer, AgentTrace, AGENTRACER, AEGIS, …) or as "self-evolution." Its defensible novelty is the **organizational blast-radius** construct — *which structural boundaries (role, communication, authority/delegation, tool, memory, accountability, human-agent) modulate spread* — and **runtime containment/recovery mechanisms** that trade systemic impact against task utility. That is a **resilience / fault-tolerance** framing, distinct from the diagnosis framing that dominates the surveyed literature.
- **Watch-out (occupied territory):** The repo's existing MASO proposal already occupies *policy-preserving delegation + causal accountability across A2A/MCP chains*. The IMACS paper (accountability-as-routing) and the Mohammadi survey (RBAC/compliance) touch adjacent accountability/authority themes — the seed should stake out **blast-radius containment/recovery**, not delegation-invariants or attribution, to avoid overlap.

**Most important verified papers for the orchestrator (identifiers):**
1. Qi et al., *Beyond Individual Intelligence* (LIFE survey) — **arXiv:2605.14892** (closest; names propagation + repair as open).
2. Cemri et al., *Why Do Multi-Agent LLM Systems Fail?* — **arXiv:2503.13657** (NeurIPS 2025; canonical MAS failure taxonomy).
3. Chen et al., *Toward an Organizational Science of MAS* (IMACS) — **arXiv:2607.25446** (org/accountability as model-dependent lever).
4. Chen, Narasimhan, Liu, *CEO-Bench* — **arXiv:2606.18543** (single-agent long-horizon; not multi-agent).
5. Yehudai et al., *Survey on Evaluation of LLM-based Agents* — **arXiv:2503.16416** (ACL Findings; names multi-agent emergent-risk + org-policy-compliance eval gaps).
6. Mohammadi et al., *Evaluation and Benchmarking of LLM Agents* — **arXiv:2507.21504** / **DOI 10.1145/3711896.3736570** (KDD 2025; enterprise RBAC/compliance eval gaps).
