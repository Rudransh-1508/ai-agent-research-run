# C4 — OpenReview 2026 Novelty Sweep: Failure Propagation / Blast Radius / Containment / Recovery in Multi-Agent & Agentic Systems

**Investigator:** Novelty Hunter C4 (OpenReview 2026)
**Date:** 21 September 2026
**Seed hypothesis under test:** *Organizational failure propagation and recovery in LLM multi-agent systems* — what determines the "organizational blast radius" of a local fault (spread across role, communication, authority/delegation, tool, memory, accountability, human-agent boundaries), and which containment/recovery mechanisms minimize systemic impact while preserving task utility.

---

## 0. CRITICAL META-FINDING (assignment premise falsified)

**NeurIPS 2026 submissions are NOT publicly visible on OpenReview as of 21 Sep 2026.**

Evidence:
- The venue group `NeurIPS.cc/2026/Conference` exists (submission deadline May 2026, conference Dec 06 2026, Sydney), but its domain content sets `public_submissions: false`.
- OpenReview full-text search (`api2.openreview.net/notes/search`, group-scoped) returns **count = 0 for the term "transformer"** in `group=NeurIPS.cc/2026`, versus 10,000 (capped) for `ICLR.cc/2026` and 3,133 for `ICML.cc/2026`. NeurIPS 2026 submissions cannot be mined.
- NeurIPS 2026 **workshop** groups exist (incl. highly relevant `Workshop/Meta-Agents` — "First Workshop on Meta Agents: Managing Agents that Manage Agents", and `Workshop/Verify-Agents` — "Who Verifies the Agents? Toward Reliable Agent Development"), but all have `public_submissions: false` and zero searchable notes (workshop deadlines are ~Sep–Oct 2026; most submissions not yet in or not public). These are **watch-list venues, not minable sources**.
- Workshop proposal texts (`NeurIPS.cc/2026/Workshop_Proposals`) are also not public.

**What IS minable and was mined:** ICLR 2026 (all submissions + workshops public, ~20k notes), ICML 2026 (submissions public, incl. main track + workshops), AAAI 2026 (partially on OpenReview, incl. workshops LaMAS, TrustAgent, WoMAPF, AIGOV). AAMAS 2026 is not on OpenReview (`AAMAS.org/2026` → 0 results).

**Method note:** `api2.openreview.net/notes/search` ORs multi-word terms (Elasticsearch-style), so raw counts are noisy; all reported hits were filtered locally by co-occurrence of agent-context and failure-context keywords in title+abstract, then read in full. The direct `/notes` endpoint was intermittently challenge-blocked (403 ChallengeRequiredError) for anonymous curl; the `/notes/search` endpoint worked throughout and returns full note content (title, authors, abstract, venue, venueid, keywords, TLDR, invitations, cdate) — this API data is itself the primary-source verification for every entry below. Raw JSON dumps: `maso_2026_investigation/raw/`.

**Query log (2 sweeps × 3 venue groups):** multi-agent failure; failure propagation; cascading failure; fault injection; blast radius; agent recovery; fault tolerance multi-agent; multi-agent robustness; error propagation multi-agent; delegation multi-agent; organizational agents; multi-agent reliability; agent fault; failure containment; multi-agent hallucination; agent error recovery; trust propagation; error cascade; fault-tolerant LLM agents; agent rollback; orchestrator failure; hierarchical multi-agent; failure taxonomy agents; resilient multi-agent LLM; checkpoint recovery agent; accountability multi-agent; authority delegation agents; Who and When attribution; agentic workflow robustness; memory poisoning agents; human-agent teaming failure; inter-agent communication failure.

---

## 1. LANDSCAPE SUMMARY

- ~430 unique notes retrieved; ~130 topically relevant after local filtering; 27 first/second-tier works analyzed in full below.
- **There is an entire ICML 2026 workshop devoted to this territory: FAGEN — "Workshop on Failure Modes of Agentic AI at ICML 2026"** (`ICML.cc/2026/Workshop/FAGEN`). At least 10 of the relevant hits are FAGEN posters. The failure-modes-of-agents area is *crowded* in 2026.
- AAAI 2026 workshop **LaMAS** = "LLM-based Multi-Agent Systems: Towards Responsible, Reliable, and Scalable Agentic Systems" — also populated with reliability/security works.
- ICML 2026 workshop **AIWILD** ("Agents in the Wild: Safety, Security, and Beyond", 2nd edition) carries many blast-radius/containment-flavored papers.
- The dominant 2026 framing is **adversarial security** (prompt injection, memory poisoning, sabotage, infiltration) and **hallucination/error propagation in pipelines**. **Benign/organizational fault propagation is largely unoccupied** (see §4).

---

## 2. TIER 1 — DIRECT OVERLAP WITH THE SEED (must cite; differentiation required)

| # | Paper | Venue (verified) | OpenReview ID | Authors | Date | What it does | Overlap with seed |
|---|-------|------------------|---------------|---------|------|--------------|-------------------|
| T1.1 | **What Can One Bad Tool Call Destroy? Measuring and Minimizing Blast Radius in Agentic Tool Use** (DamageFlow benchmark + BlastGuard runtime) | ICML 2026 Workshop AIWILD (poster; camera-ready revision invitation present) | `MYvsxnxbCf` | Muhammet Anil Yagiz (single author) | cdate 2026-05-08 | Benchmark + eval framework for **"blast radius"** of tool-using agents under indirect prompt injection, MCP tool poisoning, tool shadowing, **multi-agent relay attacks**. Sandboxed email/docs-RAG/repo/MCP-registry environments; deterministic state-diff oracles score *committed tool effects*. Metric **Blast Radius Score (BRS)** decomposes unauthorized tool effects by **resource sensitivity, action impact, propagation, and recovery cost**. BlastGuard: provenance-aware runtime compiling trusted intent into least-privilege capability graphs; dry-run, policy checks, scoped tokens, rollback logs. 80-scenario pilot: equal 20% attack-success rates can differ 89× in BRS; BlastGuard retains 87.5% benign task utility. | **Highest collision. Takes the term "blast radius" and the propagation + recovery-cost metric decomposition, and the "minimize damage while preserving utility" objective.** Framing is adversarial-security at the tool/resource boundary, NOT organizational/benign-fault. Seed MUST cite and differentiate (or rebrand). |
| T1.2 | **The Hallucination Snowball: Modeling Error Propagation as State Transitions in Multi-Agent LLM Pipelines** | FAGEN @ ICML 2026 (poster) | `YOPVjUoijs` | Prabhjot Singh, Bhushan Pawar | cdate 2026-04-26 | Formalizes error propagation across a 4-agent sequential pipeline as a first-order Markov chain over 4 states (Raw Fact → Derived → Narrative → Invisible); per-boundary escape probabilities 24.6%/48.3%/89.3%. 346 injected hallucinations, FinanceBench, financial-analysis pipeline. Detection decays 72.0%→50.9% (gpt-4o) across stages; **boundary gates at handoffs cut survival 58.4%→16.2% vs end-of-pipeline checking**; prescribes optimal verification-resource allocation ("when you verify matters more than whether"). | Occupies **error-propagation-across-agent-boundaries + containment-placement optimization** for linear pipelines, communication/handoff boundary only, hallucination faults only. Directly adjacent to the seed's communication boundary and containment questions. |
| T1.3 | **The Containment Gap: How Deployed Agentic AI Frameworks Fail Public-Facing Safety Requirements** | AI4GOOD Workshop 2026 (regular; NeurIPS-family AI4GOOD) | `QDJkugAU53` | Md Jafrin Hossain, Mohammad Arif Hossain, Weiqi Liu, Nirwan Ansari | cdate 2026-05-08 | Audits LangChain, AutoGPT, OpenAI Agents SDK against **six containment principles** from a compositional model of agentic architectures; finds no native compliance. Empirical: single memory-poisoning write → persistent targeted corruption (88.9% wrongful-denial rate in simulated government benefits agent); introduces two **containment mechanisms** (memory integrity validator, policy gate) with <0.2 ms overhead. | Takes "**containment**" branding and the memory boundary; adversarial (poisoning) framing, single-agent frameworks, not organizational MAS. |
| T1.4 | **Auditing Cascading Risks in Multi-Agent Systems via Semantic–Geometric Co-evolution** | ICLR 2026 Workshop Trustworthy AI | `jaj403z6XW` | Zixun Luo, Yuhang Fan, Hengyu Lin, Youzhi Zhang | cdate 2026-02-02 | Models MAS interactions as dynamic graphs; Ollivier–Ricci curvature anomalies in communication topology **precede semantic violations by several turns** (early-warning); local curvature gives root-cause attribution of which agent/link precipitated collapse. | Occupies **cascading-risk detection + root-cause attribution** on the communication-topology axis. Detection/auditing only — no containment or recovery mechanisms. |
| T1.5 | **CORRECT: COndensed eRror RECognition via knowledge Transfer in multi-agent systems** | **ICML 2026 main track (regular)** | `ZUDdYZSwr4` | Yifan Yu, Moyan Li, Shaoyuan Xu, Jinmiao Fu, et al. | cdate 2026-01-22 | Training-free error recognition for LLM MAS via online cache of distilled "error schemata"; **CORRECT-Error dataset: 2,000+ annotated trajectories from an error-injection pipeline** guided by real-world failure distributions; +19.8% step-level error localization across 7 MAS applications. Abstract: "Minor errors can propagate across agents, escalating into task failures." | Main-track proof that **MAS error propagation + fault injection + localization** is a recognized 2026 problem. Occupies recognition/attribution, not containment/recovery. Its error-injection pipeline + dataset could be reused or cited as infrastructure. |
| T1.6 | **Conformal Agent Error Attribution** | ICML 2026 Workshop AgenticUQ (poster) | `B6WCheiViX` | Naihe Feng, Yi Sui, Shiyi Hou, Ga Wu, et al. | cdate 2026-04-15 | Conformal-prediction error attribution over MAS trajectories with finite-sample coverage; contiguous-segment prediction sets; **uses prediction sets to roll back MAS to correct their own errors** ("first step for automated recovery to an earlier state"). | Occupies attribution + **rollback-as-recovery** with guarantees. Single mechanism (rollback), not a comparative study of containment options. |
| T1.7 | **Architecture Matters for Multi-Agent Security** | FAGEN @ ICML 2026 poster (`d4NytwJ6ne`); same title also appears as ICML 2026 AIWILD (`DNWFP9HlBa`), AI4GOOD 2026 (`DhVMDR9lrI`), ICML 2026 regular (`Jk4zLorDUx`) — same work multi-submitted | `d4NytwJ6ne` | Ben Hagag, William L. Anderson, Christian Schroeder de Witt, Sarah Scheffler | cdate 2026-04-24 | Empirical study of how MAS design choices shape the performance/attack-resistance tradeoff: **(i) agent roles (authority/responsibility allocation), (ii) communication topology, (iii) memory/state visibility**; 3 environments (browser, desktop, code), 13 architectural configurations, stagewise attack evaluation. | **Occupies the role/authority + topology + memory design axes** — but strictly under adversarial attack resistance, not benign fault propagation or recovery. Closest occupant of the seed's "organizational structure determines systemic impact" claim. |

---

## 3. TIER 2 — ADJACENT (propagation, attribution, recovery, resilience — partial overlap)

| # | Paper | Venue | OpenReview ID | Authors | Relevance / boundary |
|---|-------|-------|---------------|---------|----------------------|
| T2.1 | SAFARI: Scaling Long Horizon Agentic Fault Attribution via Active Investigation | ICML 2026 AIWILD | `tXVNXhps8B` | Chenyang Zhu, Jiayu Yao, Kushal Chawla, Youbing Yin, et al. | Tool-augmented diagnostic loop for fault attribution beyond context limits; +20% on Who&When, +19% on TRAIL-GAIA. Attribution only. |
| T2.2 | FAIR-Swarm: Fault-Tolerant Multi-Agent LLM Systems for Scientific Hypothesis Discovery | LaMAS @ AAAI 2026 (poster) | `6WyG2iZHes` | Mahule Roy, Subhas Roy | **Redundancy + consensus-based fault tolerance** against "failure cascades caused by unreliable agents" in LLM MAS. One containment mechanism (consensus), one domain. |
| T2.3 | Smarter Saboteurs, Better Fixers: Scaling & Security in Linear Multi-Agent Workflows | ICML 2026 AIWILD | `lVREKwl6Fm` | (in raw dump) | Model scale vs system-level resilience in linear MAS; terminal "Fixer" stage collapses 53.7pp compliance drop to 0.6pp. Adversarial; recovery-by-fixer-stage. |
| T2.4 | Beyond Single-Model Injection: A Threat Model and Defense Architecture for Prompt Injection in Multi-Agent Systems | ICML 2026 AIWILD | `2YLC2ciEar` | Rudrendu Kumar Paul, Sourav Nandy | 14 attack vectors across 4 categories incl. **inter-agent injection and cascading injection through orchestrator manipulation**; message signing/provenance cuts inter-agent injection 91%. Adversarial cascade containment. |
| T2.5 | OMNI-LEAK: Orchestrator Multi-Agent Network Induced Data Leakage | ICLR 2026 Conference (desk rejected) | `eQ0bqlU7Zi` | (in raw dump) | Red-teams the **orchestrator–delegate pattern**; single indirect injection compromises several agents and leaks data **despite access control**. Authority/delegation boundary — adversarial. |
| T2.6 | ChainCaps: Composition-Safe Tool-Using Agents via Monotonic Capability Attenuation | ICML 2026 AIWILD | `KtrAm71ER9` | (in raw dump) | "Permission laundering" across tool chains; capability budgets propagate by intersection (authority cannot grow through composition); MCP proxy; ASR 25–68%→0–4.8%, 96–100% benign completion. Tool/authority containment, adversarial. |
| T2.7 | Sabotage from Within: Analyzing the Vulnerability of LLM Multi-Agent Systems to Infiltration | LaMAS @ AAAI 2026 (poster) | `2W8r54OfvP` | Loan Gia | Infiltrated agent sabotage; **managerial roles pose greatest threat when compromised; larger teams more vulnerable**; defenses mitigate 78% at 84% overhead. Role-axis fragility — adversarial. |
| T2.8 | The Best-Laid SCHEMEs: Coordinated Sabotage and Monitoring in Multi-Agent Systems | AI4GOOD Workshop 2026 | `4xbK4rM2EJ` | Nikolay Radev, Lennart J. Haas, Benjamin Arnav, Pablo Bernabeu-Pérez | Coordinated covert sabotage across agents under different communication topologies; recovery from communication failures drives model gap. Adversarial coordination. |
| T2.9 | Introspecter: Diagnosing Multi-Agent LLM Debate Failures | FAGEN @ ICML 2026 | `PMd8wkf8sr` | Vikas Reddy, Harsh Satija, Gillian K. Hadfield | **Counterfactual replay**: intervene on intermediate agent states, resimulate downstream to test causal hypotheses about failure propagation in debate. Methodology reusable for the seed. |
| T2.10 | Error Trace Regression: Localizing Root Causes in Long-Horizon LLM Agent Trajectories | FAGEN @ ICML 2026 | `1miRNSRShD` | Poojak Patel | Statistical root-cause-step localization; sensitivity 0.81 vs 0.23 final-outcome. Diagnosis. |
| T2.11 | Before the Fall: Δ-Minimal Failing Prefixes for Local Tool-Use Agent Failures | FAGEN @ ICML 2026 | `KAA8FR6fEq` | Daoyuan Li | Counterfactual-replay diagnostic separating capability failures from "failure basins"; uses **soft fault injection perturbing evidence, memory, or arguments**. Single-agent. |
| T2.12 | Efficient Forecasting of Task Failures in LLM Agents through Adaptive Fault Injection | Forecast @ ICML 2026 | `d3Qq4weuwz` | Vartika Sengar, Parth Thakkar, Pranoy Panda, Shrey Satapara, et al. | Predicts failure from partial trace to enable runtime intervention "while recovery is still possible"; adaptive fault injection for training data. Single-agent forecasting. |
| T2.13 | ContinuityBench: A Framework and Taxonomy for Evaluating Agent Recovery from Interrupted State | CTB @ ICML 2026 | `3N3BzvoLbG` | Aryan Gulati | Controlled interruption/resumption on τ-bench, AppWorld, TerminalBench; handoff-fidelity levels h0/h1/h2; interruption drops success 41.7%→28.0%; **more handoff context is not automatically better**. Recovery axis — single-agent, human/handoff flavored. |
| T2.14 | Within-Episode Failure Recovery in LLM Agents via Progress-Gated Dual-Process Routing (DPR) | ICML 2026 AIWILD | `u3I4CRwe6D` | Ankush Kadu, Aswanth Krishnan | In-episode recovery routing (fast refinement + slow causal diagnosis); +40pp on ALFWorld. Single-agent recovery. |
| T2.15 | PALADIN: Self-Correcting Language Model Agents to Cure Tool-Failure Cases | ICLR 2026 Conference (**desk rejected**); also LaMAS 2026 Oral (`NVTtoO297p`) | `M2AXTAKXbz` | Sri Vatsa Vuddanti, Aarav Shah, Satwik Kumar Chittiprolu, Tony Song, et al. | Trains recovery from **tool malfunctions (timeouts, API exceptions) "triggering cascading reasoning errors"**; 50k recovery-annotated trajectories via failure injection. Benign-fault recovery — but single-agent tool use. |
| T2.16 | Structural Write-Path Control for Non-Formation in Agent Persistent Memory | FAGEN @ ICML 2026 | `h2KYjLhzv5` | (in raw dump) | Commit-gate before store-visible write; "rollback is not non-formation". Memory-boundary containment. |
| T2.17 | MemShield: Three-Tier Retrieval-Time Defense Against Coordinated Memory Poisoning | FAGEN @ ICML 2026 | `yUbDGcrVBX` | (in raw dump) | Memory-boundary defense; adversarial. |
| T2.18 | From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents | FAGEN @ ICML 2026 | `cPxxSqUFYj` | Laksh Advani | False-success failure mode on 9,876 τ2-bench trajectories; LLM judges miss it (AUROC ≤ 0.65). Detection of silent failures — relevant to "fault occurs but is unnoticed". |
| T2.19 | AutoRAS: Learning Robust Agentic Systems with Primitive Representations | **ICML 2026 main track** | `7zTV4dvdGB` | (in raw dump) | Automated design of robust agentic systems; robustness "to external adversaries **and internal failures**" via execution-derived safety signals. Mentions internal faults but optimizes design, not runtime containment/recovery. |
| T2.20 | Failure-Driven Workflow Refinement (CE-Graph) | **ICML 2026 spotlight** | `GbYHY1RVUa` | Jusheng Zhang, Kaitong Cai, Jing Yang, Ziliang Chen, et al. | "Failure Signature Space", Expected Failure Mass, counterexample-pool-driven workflow graph edits. Offline workflow refinement from failure structure. |
| T2.21 | Provably Reliable Tool-Using LLM Agents: Formal Guarantees on Error Accumulation in MCP | TrustAgent @ AAAI 2026 | `8wlgtUBSK4` | (authors not exposed in dump) | Martingale concentration bounds: error accumulation across sequential tool calls is linear + O(√T); periodic re-grounding every ~8 steps. Theory of error growth — tool boundary. |
| T2.22 | Beyond Success Rate: Benchmarking Robustness in Tool-Using Language Agents | TrustAgent @ AAAI 2026 | `3Snm5cHdRu` | (authors not exposed) | Fault-injection taxonomy in ToolBench/WebArena; Recovery Rate / Unrecoverable Failure Rate metrics; GPT-4 Turbo recovery <60%. Single-agent robustness metrics. |
| T2.23 | Diagnosing Failure Modes of Shared-State Collaboration in Resource-Constrained Visual Agents (CoSee) | FAGEN @ ICML 2026 | `LvvVx0RieJ` | Yunpeng Zhou | Shared working memory **amplifies** hallucinations (Noise Reinforcement, Policy Collapse). Memory/shared-state boundary failure modes. |
| T2.24 | VisualLeakBench: Action-Boundary Propagation Failures in Vision-Language Agents | FAGEN @ ICML 2026 | `bzyceCagak` | (in raw dump) | Measures visual→tool propagation of sensitive text; defensive prompts suppress utility. Propagation metric at tool boundary. |
| T2.25 | Automata from Agent Traces: Failure and Next-Step Prediction | ICML 2026 AIWILD | `1cprFkvFT0` | Seonglae Cho, Franklin Cardenoso Fernandez, Umar Mohammed, Zekun Wu, et al. | Minimal FSM over trace corpora; failure prediction AUROC up to 0.94 from partial traces. Monitoring. |

## 3b. TIER 3 — CLASSICAL/MARL FAULT TOLERANCE (not LLM-organizational)

| Paper | Venue | OpenReview ID | Note |
|-------|-------|---------------|------|
| Learning Robust Multi-Agent Policies via Selective Adversarial Fault Induction (MARTA) | **ICML 2026 main track** | `t0kOFRgwR8` | Fault-switching (N+2)-player Markov game; Switcher picks when/which agent fails; contraction + minimax value; TJ/LBF/MPE/SMAC. MARL, no LLM, no organizational boundaries. |
| Fault Tolerance in Multi Agent Systems | WoMAPF (7th Int. Workshop on Multi-Agent Path Finding) @ AAAI 2026, Oral | `gLg7bHryTU` | Behavior masking + reward shaping + attention for faulty MARL agents; +22–28% over RNN baseline. MARL/swarm-robotics framing. |

---

## 4. BOUNDARY-BY-BOUNDARY COVERAGE MAP vs THE SEED'S SEVEN BOUNDARIES

| Seed boundary | 2026 OpenReview coverage | Occupied? |
|---|---|---|
| Role | T1.7 (roles/authority vs attacks), T2.7 (managerial compromise) | Adversarial only |
| Communication / handoff | T1.2 (snowball gates), T1.4 (curvature auditing), T2.4, T2.8 | **Heavily occupied** (propagation + detection) |
| Authority / delegation | T2.5 (orchestrator leakage), T2.6 (capability attenuation), T1.7 | Adversarial only; also occupied by existing MASO delegation proposal |
| Tool | T1.1 (DamageFlow/BRS), T2.6, T2.11, T2.21, T2.22, T2.24 | **Heavily occupied** (incl. "blast radius" term) |
| Memory | T1.3 (containment gap), T2.16, T2.17, T2.23 | Occupied — adversarial poisoning angle |
| Accountability | Only attribution-diagnosis works (T1.5, T1.6, T2.1, T2.10); no post-failure accountability assignment under propagation | **Thin** (but adjacent to occupied delegation/accountability proposal) |
| Human–agent | T2.13 (handoff fidelity, interruption) — single-agent; nothing on propagation into/out of human nodes in MAS | **Essentially unoccupied** |
| **Benign/organizational faults** (timeouts, stale state, mis-specified instructions, misrouted delegation) | T2.15 (tool malfunctions, single-agent), T2.19 (internal failures mentioned) | **Essentially unoccupied for organizational MAS** |
| **Comparative containment/recovery mechanism study** (isolation vs quarantine vs redundancy vs rollback vs human escalation; systemic impact vs task utility) | Single mechanisms only: gates (T1.2), rollback (T1.6), consensus (T2.2), fixer stage (T2.3), capability attenuation (T2.6) | **Unoccupied as a systematic comparison** |

---

## 5. DOES ANYTHING HERE KILL OR SUBSUME THE SEED HYPOTHESIS?

**No single work kills it. Three partial collisions constrain it:**

1. **Terminology collision (serious):** "Blast radius" for agentic systems is taken by DamageFlow/BRS (T1.1, ICML 2026 AIWILD, May 2026), including the propagation + recovery-cost metric decomposition and the damage-vs-utility objective. The seed must either (a) explicitly define *organizational* blast radius as distinct from DamageFlow's tool-effect BRS and cite it, or (b) rebrand (e.g., "organizational failure footprint", "systemic failure span"). Submitting to MASO 2026 with unmarked "blast radius" framing invites a "this exists" review.

2. **Framing collision (moderate):** The propagation-and-containment question is crowded under the **adversarial-security** framing (T1.1, T1.3, T1.7, T2.4–T2.8, T2.16–T2.17) and the **hallucination-propagation** framing (T1.2, T1.4, T1.5). The seed survives only if it is explicitly about **benign/organizational faults** and **organizational structure** (roles, authority, accountability, human-agent handoffs) as the independent variables — a cell that is demonstrably empty in the 2026 OpenReview corpus.

3. **Methodology prior art (minor):** Fault injection (T1.5's CORRECT-Error pipeline, T2.11, T2.12, T2.22), counterfactual replay (T2.9, T2.11), and state-diff oracles (T1.1) are established 2026 techniques — reusable, must be cited, not claimable as contributions.

**Residual defensible core for MASO 2026:** *Benign local faults in organizational LLM MAS; how organizational structure (role hierarchy, delegation authority, accountability assignment, human-in-the-loop placement) modulates cross-boundary spread; and a controlled comparison of containment/recovery mechanisms on systemic-impact-vs-utility.* Avoid: security/attack framing (crowded), pure pipeline hallucination propagation (T1.2), pure attribution (T1.5/T1.6/T2.1), MARL fault tolerance (Tier 3), and the occupied delegation-invariants territory.

---

## 6. WATCH LIST (not minable as of 21 Sep 2026)

- `NeurIPS.cc/2026/Conference` — submissions private (`public_submissions: false`); accepted papers appear ~late Sep/Oct 2026. Re-check before 10 Oct 2026 submission.
- `NeurIPS.cc/2026/Workshop/Meta-Agents` ("Managing Agents that Manage Agents") — https://meta-agents-workshop.github.io/ — directly on-topic venue; submissions not public.
- `NeurIPS.cc/2026/Workshop/Verify-Agents` ("Who Verifies the Agents? Toward Reliable Agent Development") — https://verify-agents-workshop.github.io/ — submissions not public.
- FAGEN @ ICML 2026 and LaMAS @ AAAI 2026 — monitor for proceedings/camera-ready versions; several posters above may appear on arXiv.

## 7. LIMITATIONS OF THIS SWEEP

- OpenReview search ORs query terms; recall was boosted by 32 query variants × 3 venue groups, but phrase-level false negatives are possible.
- The anonymous `/notes` endpoint was challenge-blocked; all metadata comes from `/notes/search` payloads (full content, verified against venue group listings). Author lists for two AAAI TrustAgent posters (T2.21, T2.22) were not exposed in the search payload.
- AAAI 2026 coverage on OpenReview is partial (main track largely elsewhere); AAMAS 2026 absent. NeurIPS 2026 invisible (§0).
- Counts of 10,000 are API caps, not true totals.
