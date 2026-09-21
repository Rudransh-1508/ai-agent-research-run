# LANDSCAPE B11 — Enterprise and Organizational Benchmarks for LLM Agents

**Investigator:** B11 specialist (adversarial evidence-gathering)
**Date:** 21 September 2026
**Seed hypothesis under test:** organizational failure propagation and recovery in LLM multi-agent systems — what determines the "organizational blast radius" of a local fault (across role, communication, authority/delegation, tool, memory, accountability, human-agent boundaries), and which containment/recovery mechanisms minimize systemic impact while preserving task utility.
**Assignment questions:** (Q1) Which enterprise/organizational benchmarks have deterministic ground truth? (Q2) Which support multi-agent (not just single-agent) evaluation? (Q3) Which support fault injection?

**Verification method:** Every entry below was verified by fetching the actual arXiv abstract page, the official project page, the HuggingFace papers page, or the vendor page (URLs given per entry). arXiv IDs were cross-checked against page content (title/abstract match), not assumed. Items I could not verify are listed in §9 and excluded from the evidence tables. Venues are stated only where seen on the verified page (arXiv comment field or project page); otherwise marked "arXiv preprint (venue not verified in this sweep)".

---

## 0. Bottom line (adversarial)

**No named enterprise benchmark (WebArena, WorkArena/++, OSWorld, tau/tau2-bench, TheAgentCompany, CEO-Bench, CRMArena family, GDPval, RLI, APEX) evaluates a multi-agent system under test, and none supports fault injection.** They are single-agent-under-test benchmarks with mostly deterministic ground truth. The seed hypothesis is therefore NOT killed by the enterprise-benchmark landscape — the combination it needs (organizational/enterprise grounding × multi-agent system under test × systematic fault injection × blast-radius/recovery measurement) does not exist as a benchmark.

**However, the seed is partially encircled by 2025–2026 work on the non-enterprise side:** MAS-FIRE (arXiv:2602.19843) already does systematic fault injection + reliability evaluation of LLM MAS; "From Spark to Fire" (arXiv:2603.04474) already models error-cascade propagation and single-seed "blast" dynamics with a mitigation layer; ACIArena (arXiv:2604.07775, ACL 2026) benchmarks cascading compromise across 6 MAS implementations; ParaRecover (arXiv:2609.12345, EMNLP 2026) benchmarks error localization/recovery under cascading tool-use failures. The defensible residue for the seed is precisely the **organizational** layer (roles, authority/delegation, accountability, human-agent boundaries) and **enterprise workflow** grounding, plus **recovery-vs-utility tradeoffs** — none of which those works address. Also note: the term "blast radius" is already in active use in the agent-*security* literature (ceLLMate, OpenSec, UnderSpecBench, Open Agent Passport) with a different (containment-of-attacks) meaning; the seed must acknowledge and differentiate.

---

## 1. Table A — Assignment-named core benchmarks (all verified)

| Benchmark | arXiv / source | Date & venue | Setting & scale | Q1: Deterministic GT? | Q2: Multi-agent eval? | Q3: Fault injection? | Code |
|---|---|---|---|---|---|---|---|
| WebArena | 2307.13854 | Jul 2023; ICLR 2024 (venue per community knowledge, not on arXiv comment) | Self-hosted web env (e-commerce, forum, GitLab, CMS); 812 tasks (count confirmed via OSWorld paper comparison table) | **Yes** — programmatic functional correctness (URL/state/string match) | No — single agent | No | Yes (public) |
| WorkArena | 2403.07718 | Mar 2024; ICML 2024 (per community knowledge) | ServiceNow enterprise platform; 33 tasks; introduces BrowserGym harness | **Yes** — programmatic state checks via BrowserGym | No | No | Yes (ServiceNow/WorkArena) |
| WorkArena++ | 2407.05291 | Jul 2024 (v2 Feb 2025); arXiv preprint | 682 compositional knowledge-work tasks on ServiceNow | **Yes** — programmatic; also generates ground-truth traces | No | No | Yes |
| OSWorld | 2404.07972 | Apr 2024; NeurIPS 2024 D&B (per community knowledge) | Real Ubuntu/Windows/macOS VMs; 369 tasks, execution-based eval scripts (134 eval functions per project page) | **Yes** — execution-based state checkers | No | No | Yes (xlang-ai/OSWorld) |
| OSWorld-Verified | os-world.github.io | 28 Jul 2025 (project-page news item) | Fixed community-reported broken tasks; AWS support; re-run leaderboard | Yes | No | No | Yes |
| OSWorld 2.0 | 2606.29537 | Jun 2026; arXiv preprint | 108 long-horizon workflows (median 1.6 h human time; ~318 tool calls); dynamic environments, hidden state; safety reports | Yes (binary completion + partial score, execution-based) | No | No (has "dynamic environments" and mid-task information arrival, but no fault-injection harness) | Yes |
| tau-bench | 2406.12045 | Jun 2024; arXiv preprint (Sierra) | Retail + airline domains; tool-agent-user conversations; pass^k reliability metric | **GT deterministic** (final DB state vs annotated goal state) but rollouts stochastic (LLM user simulator) | No — one agent + simulated user | No | Yes |
| tau2-bench | 2506.07982 | Jun 2025; arXiv preprint (Sierra) | Telecom **dual-control** domain modeled as Dec-POMDP; compositional task generator; user also holds tools | **Yes** — programmatically generated verifiable tasks; state-based | **Partial** — agent must coordinate with an active (simulated) user who changes shared state; still one agent under test | No | Yes |
| TheAgentCompany | 2412.14161 | Dec 2024 (v3 Sep 2025); arXiv preprint (CMU) | Self-hosted simulated software company (RocketChat, GitLab, Plane, ownCloud); 175 tasks; **LLM-simulated colleagues** (NPCs) | **Mostly** — checkpoint-based partial credit (50% bonus for full completion); 51/175 tasks (29%) use LLM-as-judge (Claude-3-5-Sonnet backend), rest programmatic | **No (but closest)** — single agent under test *embedded in* a simulated org; colleagues are NPCs, not co-evaluated agents | No | Yes (code, data, environment public) |
| CEO-Bench ("long game") | 2606.18543 | Jun 2026 (v2 Jul 2026); arXiv preprint | Single agent operates a simulated startup for 500 days via Python API; noisy interconnected business DBs | **Yes** — financial outcomes from deterministic business simulation; rule-based baseline | No | No (has noise/uncertainty, not fault injection) | Not stated on abs page |
| CEO-Bench ("Can LLMs Be CEOs?") | 2606.17459 | Jun 2026; arXiv preprint | **Multi-role simulation**: focal LLM gets conflicting advice from 4 role-conditioned C-suite advisors (CFO/CTO/COO/CMO) with private signals; 13 scenarios; multi-round resource reallocation | Rubric-based along 4 dimensions (role integration, conditional boldness, history sensitivity, plan validity) — not purely deterministic | **Partial** — multi-agent *environment* (advisors are LLM agents), single decision-maker evaluated | No | Not stated on abs page |

**Key quantitative anchors (from verified abstracts):** WebArena: GPT-4 agent 14.41% vs human 78.24%. OSWorld: best model 12.24% vs human 72.36%. OSWorld 2.0: Claude Opus 4.8 (max thinking) 20.6% binary / 54.8% partial; GPT-5.5 ~13%. tau-bench: GPT-4o <50% success, pass^8 <25% (retail). TheAgentCompany: best agent ~30% full completion (v3 abstract). WorkArena++: 682 tasks; humans outperform all agents. CEO-Bench (long game): only Claude Fable 5, GPT-5.6 Sol, Claude Opus 4.8 finish above the $1M starting balance; all below rule-based baseline.

---

## 2. Table B — Other enterprise / economic-value benchmarks (verified)

| Benchmark | arXiv / source | Date & venue | Setting & scale | Q1 det. GT | Q2 multi-agent | Q3 fault inj. | Notes |
|---|---|---|---|---|---|---|---|
| CRMArena | 2411.02305 | Nov 2024; **NAACL 2025** (arXiv comment) | Salesforce CRM sandbox; 9 customer-service tasks × 3 personas (service agent, analyst, manager); 16 interconnected CRM objects; latent variables | Mostly programmatic | No | No | ReAct <40%, function-calling <55% success |
| CRMArena-Pro | 2505.18878 | May 2025; arXiv preprint (Salesforce) | 19 expert-validated tasks across sales/service/CPQ, B2B+B2C; multi-turn persona-guided; **confidentiality-awareness tests**; live Salesforce Org sandbox | Mostly programmatic + persona simulator | No (multi-turn, but one agent) | No | ~58% single-turn → ~35% multi-turn; **near-zero inherent confidentiality awareness**; dataset on HF (Salesforce/CRMArenaPro) |
| CXMArena | 2505.09436 | May 2025; arXiv preprint | Contact-center CXM; 5 operational tasks (KB refinement, intent prediction, agent quality adherence, article search, multi-turn RAG+tools); controlled noise injection in *data generation* | Yes (task metrics) | No | Only synthetic noise in data construction, not runtime fault injection | GitHub linked |
| OfficeBench | 2407.19056 | Jul 2024; arXiv preprint | Office automation across multiple apps; long-horizon workflows | Customized per-task evaluation | No | No | GPT-4o 47.0% pass rate; failures = redundancy, hallucination, app-switching |
| AppWorld | 2407.18901 | Jul 2024; **ACL 2024** (arXiv comment) | 9 day-to-day apps, 457 APIs, ~100 simulated users; 750 tasks | **Yes** — state-based unit tests incl. **collateral-damage checks** (unexpected state changes) | No | No (but collateral-damage checks are the closest thing to "blast radius" measurement in any enterprise-style benchmark) | Yes |
| ToolSandbox | 2408.04682 | Aug 2024 (v2 Apr 2025); arXiv preprint (Apple) | Stateful tool execution, implicit state dependencies, user simulator, milestone-based dynamic evaluation; "Insufficient Information" scenarios | Yes — state-based milestones | No | No | Yes |
| GDPval | openai.com/index/gdpval | 25 Sep 2025 (OpenAI) | 1,320 tasks (220 open gold set) across 44 occupations / 9 GDP-weighted industries; real work products | **No** — blind expert pairwise grading (better/as-good/worse); experimental automated grader released but not trusted as replacement | No | No | One-shot only (stated limitation); Claude Opus 4.1 best on gold set |
| Remote Labor Index (RLI) | 2510.26787 | Oct 2025; arXiv preprint (Scale AI / CAIS) | Real, economically valuable freelance projects, multi-sector; end-to-end agent performance | **No** — human/expert evaluation of deliverables | No | No | Best agent: **2.5% automation rate**; public set cais/rli-public-set |
| APEX-Agents 1.1 | mercor.com/apex | 2025–26 (Mercor vendor leaderboard; no arXiv paper found) | Multi-hour professional tasks (investment banking, corporate law, management consulting) in Google Suite | No — rubric/expert grading (methodology page exists; not peer-reviewed) | No | No | Top scores ~65–69% ±5%. Treat as vendor evidence only |
| Vending-Bench | 2502.15840 | Feb 2025; arXiv preprint | Long-horizon (>20M tokens/run) vending-machine business sim; variance/meltdown analysis | Yes (simulation outcomes) | No | No | Documents un-recovered "meltdown loops" — recovery-relevant observation, single-agent |
| FinanceBench | 2311.11944 | Nov 2023; arXiv preprint | 10,231 financial QA questions w/ evidence strings | Yes (QA answers) | No | No | Enterprise QA, not workflow |
| GAIA | 2311.12983 | Nov 2023; arXiv preprint (Meta/HF/AutoGPT) | 466 general-assistant questions | Yes (exact answers) | No | No | Humans 92% vs GPT-4+plugins 15% |
| AssistantBench | 2407.15711 | Jul 2024; arXiv preprint | 214 time-consuming open-web tasks, auto-evaluated | Yes | No | No | Best ≤26 pts |
| BrowseComp | 2504.12516 | Apr 2025; arXiv preprint (OpenAI) | 1,266 hard-to-find-info browsing questions | Yes (short verifiable answers) | No | No | — |
| Mind2Web | 2306.06070 | Jun 2023; **NeurIPS 2023 Spotlight** (arXiv comment) | 2,000+ tasks, 137 real websites | Yes (action-sequence match) | No | No | Dataset-oriented |
| VisualWebArena | 2401.13649 | Jan 2024; **ACL 2024** (arXiv comment) | Visual web tasks on WebArena-style self-hosted sites | Yes | No | No | — |
| WindowsAgentArena | 2409.08264 | Sep 2024; arXiv preprint (Microsoft) | 150+ Windows tasks, OSWorld-derived, Azure-parallelized | Yes | No | No | Navi agent 19.5% vs human 74.5% |
| AndroidWorld | 2405.14573 | May 2024 (v5 Apr 2025); arXiv preprint (Google) | 116 parameterized programmatic tasks, 20 Android apps; dynamic task construction | Yes — init/success/teardown state logic | No | No (but parameterized task *variations* shown to significantly affect performance) | Best agent 30.6% |

---

## 3. Table C — Multi-agent evaluation benchmarks (verified; none are enterprise/organizational)

| Benchmark | arXiv | Date & venue | What it evaluates | Det. GT | Fault inj. |
|---|---|---|---|---|---|
| MultiAgentBench (MARBLE) | 2503.01935 | Mar 2025; arXiv preprint | LLM MAS collaboration/competition across interactive scenarios; milestone-based KPIs; coordination topologies (star/chain/tree/graph); graph best in research scenario; cognitive planning +3% milestone rate | Task-dependent | No |
| Collab-Overcooked | 2502.20073 | Feb 2025; **EMNLP 2025 Main** (arXiv comment + DOI 10.18653/v1/2025.emnlp-main.249) | Overcooked-AI collaborative cooking; 30 open-ended tasks; process-oriented collaboration metrics; 13 LLMs | Yes (game state) | No |
| BattleAgentBench | 2408.15971 | Aug 2024; arXiv preprint | 7 sub-stages × 3 difficulty levels; single→paired→multi-agent coop/competition | Yes | No |
| SOTOPIA | 2310.11667 | Oct 2023; ICLR 2024 (per community knowledge) | Open-ended social interaction role-play; SOTOPIA-Eval (LLM-graded) | No (LLM-graded) | No |
| ChatDev | 2307.07924 | Jul 2023; **ACL 2024** (arXiv comment) | Virtual software company (CEO/CTO/programmer roles); chat chain; communicative dehallucination | Code-quality metrics | No |
| MetaGPT | 2308.00352 | Aug 2023 (v7 Nov 2024); ICLR 2024 (per community knowledge) | SOP-encoded role assembly line for software company; notes "cascading hallucinations" from naive LLM chaining as motivation | Code-quality metrics | No |
| Generative Agents | 2304.03442 | Apr 2023; UIST 2023 (per community knowledge) | 25-agent Smallville social simulacra; memory/reflection/planning | Believability eval | No |

**Note:** MetaGPT's own motivation ("logic inconsistencies due to cascading hallucinations caused by naively chaining LLMs") is early evidence that error propagation was recognized in 2023, but as a *design problem for frameworks*, not as a measured phenomenon with ground truth.

---

## 4. Table D — Fault injection, failure propagation, attribution, and recovery (verified; the seed's real neighborhood)

| Work | arXiv | Date & venue | What it does | Multi-agent? | Relevance / threat to seed |
|---|---|---|---|---|---|
| **MAS-FIRE** | 2602.19843 | Feb 2026; arXiv preprint (cs.SE) | Systematic **fault injection + reliability evaluation for LLM MAS**: taxonomy of 15 fault types (intra-agent cognitive + inter-agent coordination); 3 non-invasive injection mechanisms (prompt modification, response rewriting, **message routing manipulation**); 3 MAS architectures; 4-tier fault-tolerance analysis (mechanism/rule/prompt/reasoning). Findings: stronger base models ≠ uniformly more robust; **iterative closed-loop topologies neutralize >40% of faults that catastrophically collapse linear workflows** | **Yes** | **HIGH — closest existing work.** Covers fault injection, propagation, topology effects, recovery tiers. Does NOT cover: organizational roles/authority/accountability, enterprise workflows, human-agent boundary, utility-preserving containment |
| **From Spark to Fire** | 2603.04474 | Mar 2026 (v2 May 2026); arXiv preprint (cs.MA) | **Error-cascade propagation dynamics** for LLM-MAS: collaboration as directed dependency graph; early-stage amplification-risk criterion; 3 vulnerability classes (cascade amplification, topological sensitivity, consensus inertia); **single atomic error seed → widespread failure**; genealogy-graph governance layer (message-layer plugin) raises defense success 0.32→≥0.89 | **Yes** (6 frameworks) | **HIGH — this is "blast radius" dynamics without the name or the org framing.** Differentiators left for seed: organizational boundary semantics, enterprise ground truth, recovery+utility tradeoff |
| **ACIArena** | 2604.07775 | Apr 2026; **ACL 2026** (arXiv comment) | Unified eval of MAS robustness to **Agent Cascading Injection**: compromised agent exploits inter-agent trust → cascading failure; attack surfaces (external inputs, agent profiles, inter-agent messages) × objectives (hijacking, disruption, exfiltration); 6 MAS implementations; 1,356 test cases. Finding: topology alone insufficient; role design matters | **Yes** | **HIGH** but adversarial/security framing, not accidental-fault/organizational framing |
| **ParaRecover** | 2609.12345 | Sep 2026; **EMNLP 2026 Main** (arXiv comment) | Process-level benchmark for **error localization and recovery** in multi-turn parallel tool-use; 14 error types; 10,626 instances; SDE rubric (structural integrity, diagnostic reasoning, evolutionary strategy); errors propagate across dependent branches → cascading failures | No (single agent, parallel tools) | MEDIUM — recovery metrics + cascade framing, but not MAS and not organizational |
| **CUADebug / CUAErrorBench** | 2608.02643 | Jul/Sep 2026; **EMNLP 2026** (project page) | Root-cause analysis of 204 failed OSWorld trajectories (5-category, 30-subtype taxonomy); debugger agent; **guided re-execution improves failure recovery 13.9%→29.9%** | No | MEDIUM — recovery-via-diagnosis template transferable to MAS; single-agent |
| **UFO³ / NebulaBench** | 2511.11332 | Nov 2025 (v2 Mar 2026); arXiv preprint (Microsoft, cs.DC) | Cross-device agent orchestration fabric (TaskConstellation DAGs); NebulaBench: 55 cross-device tasks; **fault-injection experiments: graceful degradation and recovery under transient and permanent agent failures** | Yes (orchestrated device agents) | MEDIUM — the only *systems* paper found that runs chaos-style agent-failure injection; infrastructure (not organizational) faults |
| **Who&When** | 2505.00212 | Apr 2025 (v3 Jun 2025); ICML 2025 (per community knowledge; arXiv says "camera-ready") | Failure-attribution dataset: 127 MAS failure logs, fine-grained who/when annotations; hand-crafted + **algorithm-generated** failures (automated fault introduction); best attribution method 53.5% agent-ID accuracy, 14.2% step-ID | Yes | MEDIUM — attribution, not containment/recovery; its automated-failure-generation pipeline is a reusable fault-injection method |
| **MAST / MAST-Data** | 2503.13657 | Mar 2025 (v3 Oct 2025); arXiv preprint (UC Berkeley et al.) | Multi-Agent System Failure Taxonomy: 14 failure modes in 3 categories (system design, inter-agent misalignment, task verification); 1,600+ annotated traces, 7 frameworks; κ=0.88 | Yes | MEDIUM — taxonomy only, no injection/recovery |
| **TRAIL** | 2505.08638 | May 2025 (v3 Jun 2025); arXiv preprint | 148 human-annotated agent traces (single+multi-agent, SWE + open-world IR); error taxonomy; trace debugging — best model (Gemini-2.5-pro) 11% | Partial (traces from MAS included) | LOW-MEDIUM — offline trace reasoning, no live injection |
| **AgentDojo** | 2406.13352 | Jun 2024 (v3 Nov 2024); NeurIPS 2024 (per community knowledge) | Dynamic prompt-injection attack/defense environment; 97 realistic tasks (email, e-banking, travel), 629 security test cases | No | MEDIUM — adversarial injection only |
| **InjecAgent** | 2403.02691 | Mar 2024; **ACL 2024 Findings** (arXiv comment) | 1,054 indirect-prompt-injection cases; 17 user tools, 62 attacker tools; GPT-4 ReAct vulnerable 24% | No | MEDIUM — adversarial injection only |
| **ASB (Agent Security Bench)** | 2410.02644 | Oct 2024 (v4 May 2025); **ICLR 2025** (arXiv comment) | 10 scenarios, 10 agents, 400+ tools, 27 attack/defense methods, 7 metrics; incl. memory poisoning, PoT backdoor; up to 84.3% attack success | No | MEDIUM — adversarial; includes memory-poisoning vector relevant to "memory boundary" |
| **ToolEmu** | 2309.15817 | Sep 2023 (v2 May 2024); ICLR 2024 (per community knowledge) | LM-emulated tool sandbox for risk discovery; 36 high-stakes tools, 144 cases; LM safety evaluator; 68.8% of identified failures validated as real | No | LOW-MEDIUM — risk emulation, not propagation/recovery |

---

## 5. Table E — "Blast radius" and containment terminology already in use (agent security, 2025–2026)

The seed's signature term is **not new** in agent security; it must be differentiated (security containment of attacks vs. organizational failure propagation of accidental faults):

| Work | arXiv | Date | Usage |
|---|---|---|---|
| ceLLMate | 2512.12594 | Dec 2025 (HF-listed Mar 2026) | Browser sandboxing at HTTP layer "reduces the blast radius of prompt injections" (WASP benchmark) |
| OpenSec | 2601.21083 | Jan 2026 | Incident-response RL env; execution-based metrics: **time-to-first-containment (TTFC), blast radius (false positives/episode)**, injection violation rates; dual-control; finds over-triggering (GPT-5.2: 100% containment, 82.5% FP) |
| UnderSpecBench | 2607.02294 | Jul 2026 | DevOps action-boundary benchmark; varies instructions along intent clarity, target certainty, **blast radius**; 2,208 prompt variants; **deterministic side-effect oracles** (Safe Success / Wrong Target / OverScope); finding: blast-radius cues barely reduce action propensity |
| Open Agent Passport | 2603.20953 | Mar 2026 | Pre-action authorization; explicitly distinguishes sandboxing ("contains blast radius but does not prevent unauthorized actions") |
| Bounded Agents | 2608.15888 | Aug 2026 | Delegation security (Agentic Principal Chain); cuts AgentDojo exfiltration 75–100%→0%. **NOTE: overlaps the already-occupied delegation-invariants territory (maso/policy_preserving_delegation_research_proposal.md) — treat as occupied** |

---

## 6. Direct answers to the three assignment questions

**Q1 — Deterministic ground truth?**
- **Fully/mostly deterministic (execution- or state-based):** WebArena, WorkArena, WorkArena++, OSWorld (incl. Verified, 2.0), WindowsAgentArena, AndroidWorld, AppWorld (incl. collateral-damage checks), ToolSandbox, OfficeBench, CRMArena/CRMArena-Pro (mostly), CXMArena, GAIA, AssistantBench, BrowseComp, Mind2Web, VisualWebArena, Vending-Bench, CEO-Bench (long-game version; simulation outcomes), UnderSpecBench, ParaRecover.
- **Deterministic GT but stochastic rollouts:** tau-bench, tau2-bench (LLM user simulator; pass^k exists precisely because of run-to-run variance).
- **Mixed:** TheAgentCompany (71% programmatic checkpoints; 29% of tasks involve LLM-as-judge, Claude-3-5-Sonnet backend — verified from paper HTML, Appendix E).
- **NOT deterministic (human/expert/rubric grading):** GDPval, RLI, APEX-Agents, SOTOPIA, CEO-Bench (multi-role version; rubric-graded).

**Q2 — Multi-agent (not just single-agent) evaluation?**
- **None of the enterprise/organizational benchmarks** evaluate a multi-agent system as the system under test.
- Closest nuances: TheAgentCompany embeds one agent among LLM-simulated colleagues (NPCs); tau2-bench is dual-control (agent + active simulated user, Dec-POMDP-modeled); CEO-Bench (multi-role) puts one decision-maker LLM among four role-conditioned advisor agents with private signals — the advisors are part of the environment, not co-evaluated.
- True multi-agent evaluation exists only in non-organizational benchmarks: MARBLE, Collab-Overcooked, BattleAgentBench, SOTOPIA — plus the fault-injection frameworks in Table D (MAS-FIRE, Spark-to-Fire, ACIArena, Who&When).

**Q3 — Fault injection?**
- **None of the named enterprise benchmarks** support fault injection natively. (Their self-hosted containers/VMs make injection *possible* to build — WebArena/OSWorld/WorkArena/TheAgentCompany are all self-hosted — but no benchmark ships fault-injection tasks, fault taxonomies, or recovery metrics.)
- Fault injection exists elsewhere: MAS-FIRE (semantic faults in MAS), Spark-to-Fire (error seeds), ACIArena/AgentDojo/InjecAgent/ASB (adversarial injection), UFO³ (transient/permanent agent-failure injection in orchestration), Who&When (automated failure generation for attribution), UnderSpecBench/OpenSec (containment-side metrics).
- **The combination (enterprise/organizational setting × MAS under test × fault injection × blast-radius/recovery measurement) is empty in everything verified.**

---

## 7. Gap analysis vs. the seed hypothesis

What the seed needs that no verified benchmark provides:
1. **Organizational semantics in the environment:** roles with authority/delegation structure, accountability assignment, human-agent escalation boundaries. TheAgentCompany has the org *skin* (company, colleagues, HR/PM/SDE tasks) but no authority model, no fault injection, single agent. CEO-Bench (multi-role) has role-conditioned advisors with private signals (information asymmetry!) but evaluates only the focal LLM's decision quality, not failure propagation or recovery.
2. **MAS as system under test in an enterprise workflow:** MARBLE/ACIArena/MAS-FIRE use generic collaboration tasks (research, coding, games), not enterprise workflows with deterministic organizational ground truth.
3. **Blast-radius measurement across organizational boundaries:** AppWorld's collateral-damage checks and OpenSec/UnderSpecBench's containment metrics are the closest methodological templates; neither is multi-agent or organizational.
4. **Recovery-vs-utility tradeoff:** CUADebug (recovery via root-cause-guided re-execution), ParaRecover (localization+recovery rubric), Vending-Bench (documents un-recovered meltdowns) — all single-agent.
5. **Deterministic, reproducible org ground truth:** abundant in single-agent enterprise benchmarks (Table A/B) — a MAS organizational benchmark could reuse these harnesses (ServiceNow/Salesforce sandboxes, TheAgentCompany's self-hosted stack).

**Reusable infrastructure for the seed (verified):** TheAgentCompany self-hosted org environment (open code/data); tau2-bench compositional task generator + Dec-POMDP dual-control formalism; AppWorld state-based unit-test + collateral-damage evaluation pattern; MAS-FIRE's three non-invasive injection mechanisms (prompt modification, response rewriting, message routing manipulation); Who&When's automated failure generation; OpenSec's TTFC/blast-radius metric definitions.

## 8. Does anything here kill or subsume the seed?

- **Kill: No.** No verified work studies failure propagation/recovery in *organizational* multi-agent workflows with enterprise ground truth.
- **Partial subsumption risk (must cite and differentiate):** MAS-FIRE (2602.19843) and From Spark to Fire (2603.04474) cover generic-MAS fault injection, cascade dynamics, topology effects, and mitigation layers. A MASO reviewer who knows these will ask "what is new?" The answer must be: organizational boundary structure (role/authority/accountability/human-escalation), enterprise-grade deterministic ground truth, and containment mechanisms evaluated on utility preservation — none of which those papers touch. ACIArena (ACL 2026) adds cascading-*attack* robustness; ParaRecover/CUADebug add recovery benchmarks (single-agent).
- **Terminology collision:** "blast radius" is live in agent security (Table E). Differentiate explicitly.
- **Occupied territory reconfirmed:** Bounded Agents (2608.15888) + Open Agent Passport (2603.20953) sit in the delegation/authorization space already covered by the existing MASO proposal — do not drift there.

## 9. Classical roots (pre-LLM)

- Chaos engineering practice: Netflix Chaos Monkey (github.com/Netflix/chaosmonkey) and Jepsen distributed-systems fault-injection testing (jepsen.io) — engineering systems, not papers; the intellectual ancestor of "inject faults, measure containment." UFO³'s transient/permanent agent-failure injection is the direct descendant for agent systems.
- Classical MAS fault tolerance (replication, reputation, organizational reorganization) predates LLMs; the 2025–2026 LLM-MAS works above (MAST, MAS-FIRE, Spark-to-Fire) are the LLM-era instantiation. No classical *benchmark* for organizational failure propagation in MAS was found in this sweep (not exhaustively searched — flagged as a residual check for the theory/orchestration investigators).

## 10. Verification log and unverified/dropped items

- **Verified via arXiv abstract pages (title+abstract+ID+date cross-checked):** 2307.13854, 2403.07718, 2407.05291, 2406.12045, 2506.07982, 2404.07972, 2412.14161 (+ full-text HTML for grading details), 2606.18543, 2606.17459, 2411.02305, 2505.18878, 2407.19056, 2408.04682, 2407.18901, 2503.01935, 2505.00212, 2503.13657, 2505.08638, 2403.02691, 2410.02644, 2309.15817, 2502.20073, 2408.15971, 2310.11667, 2502.15840, 2308.00352, 2307.07924, 2311.12983, 2407.15711, 2409.08264, 2405.14573, 2504.12516, 2311.11944, 2304.03442, 2306.06070, 2401.13649, 2602.19843, 2603.04474, 2604.07775, 2609.12345, 2608.02643, 2511.11332, 2601.21083, 2607.02294, 2510.26787, 2606.29537, 2505.09436.
- **Verified via HF paper pages (title+abstract+arXiv ID):** 2512.12594 (ceLLMate), 2603.20953 (OAP), 2608.15888 (Bounded Agents).
- **Verified via official/vendor pages:** GDPval (openai.com/index/gdpval), APEX (mercor.com/apex), OSWorld-Verified & OSWorld 2.0 release dates (os-world.github.io), CRMArena-Pro design details (salesforce.com blog), CUADebug venue EMNLP 2026 (cuadebug.github.io).
- **Could NOT verify (excluded from tables):** "OSWorld-Human" (no such paper found on HF/arXiv search; the actual OSWorld successors are OSWorld-Verified and OSWorld 2.0); a Meta "GAIA-2" tool-use benchmark (the only verified "GAIA-2" is Wayve's autonomous-driving world model, arXiv-listed on HF — unrelated); "BizBench" (my candidate arXiv ID resolved to an unrelated paper; dropped rather than risk a wrong citation); "OrgBench"/"WorkBench" (no such benchmarks found); "LIFE" survey on collaboration/failure-attribution/self-evolution (abstract seen on HF, arXiv ID not confirmed — mentioned here only as a signal that surveys of this exact area now exist).
- **Access issues during sweep:** arXiv API and Semantic Scholar API rate-limited (HTTP 429) for parts of the session; searches were rerouted through HuggingFace papers search + direct arXiv abs pages. All table entries were nonetheless verified against primary pages.
