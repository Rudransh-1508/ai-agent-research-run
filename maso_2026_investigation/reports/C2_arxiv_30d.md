# C2 — Novelty Hunter: arXiv 30-Day Sweep (22 Aug – 21 Sep 2026)

**Assignment:** NOVELTY HUNTER C2. Sweep arXiv submissions from the last 30 days (mid-Aug to 21 Sep 2026) for multi-agent reliability / failure / containment / recovery / organizational testbeds, adversarially assessed against the seed hypothesis: *organizational failure propagation and recovery in LLM multi-agent systems — what determines the "organizational blast radius" of a local fault (across role, communication, authority/delegation, tool, memory, accountability, human-agent boundaries), and which containment/recovery mechanisms minimize systemic impact while preserving task utility.*

**Date of sweep:** 21 Sep 2026
**Window covered:** submissions dated 2026-08-22 through 2026-09-21 (arXiv IDs 2608.22xxx–2609.21xxx)

---

## 1. Methodology and coverage

- Primary discovery channel: Semantic Scholar Graph API `paper/search/bulk` with `publicationDateOrYear=2026-08-22:2026-09-21`, across **32 query variants** (two sweeps): "multi-agent failure/reliability/robustness/resilience LLM", "error propagation multi-agent", "cascading failures multi-agent", "fault tolerance/injection agent", "agent containment", "blast radius", "failure containment multi-agent system", "organizational blast radius agent", "multi-agent recovery benchmark", "human oversight multi-agent failure", "agent failure taxonomy", "systemic risk AI agents", "inter-agent communication failure", "delegation failure agent", "fault localization", "agent rollback recovery", "self-healing multi-agent LLM", etc.
- Yield: 312 + 70 query-results → **~350 unique papers** screened by title; ~60 inspected at abstract level; **20 verified directly on arxiv.org/abs/ pages** (exact title, authors, date, subjects, venue comments, submission history). Two non-arXiv items verified via Semantic Scholar records (DOI).
- Note: the arXiv export API (`export.arxiv.org`) was intermittently rate-limited (HTTP 429) from this host during the sweep; discovery therefore ran through Semantic Scholar and every load-bearing claim was verified on the actual arXiv abstract page. Raw query dumps are in `maso_2026_investigation/raw/`.
- Caveat on corpus quality: the 2026 arXiv agent-reliability stream contains a visible fraction of low-effort/AI-assisted papers (odd author strings, single-author "framework" papers with no artifacts). Venue acceptance is flagged where stated on the arXiv page; treat unrefereed items accordingly.

## 2. Bottom line

**The 30-day window does NOT kill the seed hypothesis, but it substantially narrows it.** The generic claim "local faults propagate through LLM multi-agent systems and structure/mechanisms shape the spread" is now *crowded and partially published at good venues* (EMNLP 2026 ×3, ECML PKDD 2026, MobiHoc 2026). Failure *attribution* is saturated (5+ new papers in 30 days on the Who&When lineage). Recovery-via-replay/rollback is occupied. **However, no paper in the window studies propagation jointly across heterogeneous *organizational* boundary types (role, communication, authority, tool, memory, accountability, human-agent) as a multi-dimensional blast-radius construct, and none compares containment/recovery mechanisms on systemic-impact-vs-task-utility trade-offs in an organizational workflow.** The term "blast radius" appears in the window only in *adjacent* senses (AIOps remediation collateral damage; credential compromise scope) — not in the seed's organizational-propagation sense. The seed survives if it is sharpened to that multi-boundary, mechanism-comparative, utility-preserving framing; a vaguer "errors spread in MAS" paper would be scooped several times over.

---

## 3. Evidence tables by cluster

### Cluster A — Failure propagation / contagion dynamics (DIRECT overlap with seed core)

| Paper | arXiv | Date | Venue/status | What it does | Relation to seed |
|---|---|---|---|---|---|
| Collective Loss of Control in LLM Agent Systems: An Epidemic Account of Mutation, Contagion, and Recovery (Wu et al.) | [2609.18460](https://arxiv.org/abs/2609.18460) | 16 Sep | cs.AI/cs.CR, v1 | Epidemic model of local deviation → contagion via communication → collective failure; deployment audit of implicit comm paths; RogueHandoff-20 injection benchmark (20 scenarios); harm 0–5% baseline vs 40–95% post-injection | **Closest to seed's propagation core.** Authors explicitly state they do NOT establish natural rare-event rates or demonstrate an autonomous cascade — the "what determines spread" question is left open. Communication boundary only; no authority/memory/accountability dimensions; no containment-mechanism comparison. |
| Contagion on the Trading Floor: How Adversarial Signals Spread in Multi-Agent Trading Systems (Qi et al.) | [2609.19789](https://arxiv.org/abs/2609.19789) | 17 Sep | **ECML PKDD 2026** (LNCS 16946) | GMATS framework; black-box input-only poisoning via social-media feeds; defines *contagion metrics* (belief-shift at analyst/coordinator layers); finds topology + coordinator prompts dampen shocks | Strong evidence that "topology shapes propagation" is published. Domain-specific (trading); adversarial input only, not endogenous organizational faults. |
| PropUQ-MAS: Propagation-Aware Uncertainty Quantification for LLM Multi-Agent Systems (Liu et al.) | [2608.22130](https://arxiv.org/abs/2608.22130) | 22 Aug | **EMNLP 2026 main** | Models MAS execution as communication graph; per-step reliability = local uncertainty + inherited upstream uncertainty; +6.1% AUROC, +47.6% PRR | Occupies "quantify error inheritance/amplification along comm graph." Detection/UQ only — no containment or recovery. |
| Skynet: Workflow-Level Anomaly Detection for Agentic AI (Zhang et al.) | [2609.06835](https://arxiv.org/abs/2609.06835) | 6 Sep | **ACM MobiHoc 2026** | Workflow-level anomaly detection over delegation/tool/data-flow dependency graphs; trained on benign only; sub-1% FPR | Occupies workflow-level *detection* of propagating corruption. Explicitly detection, not containment/recovery. |
| Building Trustworthy Graph-Agentic RAG … Failure Propagation, and Assurance by Construction (Bommireddy & Bommireddy) | [2609.06391](https://arxiv.org/abs/2609.06391) | 6 Sep | cs.* v1 | Synthesizes "evidence-to-action failure chain" in graph-agentic RAG; proposes 5 interface contracts | Conceptual/synthesis; "failure propagation" in title but RAG-specific, no organizational boundaries, no experiments on spread. |

### Cluster B — Failure attribution (SATURATED — avoid as primary contribution)

| Paper | arXiv | Date | Venue | One-liner |
|---|---|---|---|---|
| Detect Before You Attribute / DUOTRACE (Zhang et al.) | [2608.29646](https://arxiv.org/abs/2608.29646) | 30 Aug | cs.AI+cs.MA | VAE anomaly-detection filter before LLM attribution; +8.7% agent-level, +7.0% step-level accuracy |
| EDGE: Error Dependency Graph-Guided Multi-Error Attribution (Hou et al.) | [2609.01360](https://arxiv.org/abs/2609.01360) | 1 Sep | **EMNLP 2026** | Error dependency graphs + counterfactual rollout; multi-error attribution on TRAIL/MAST |
| DCFA: Dual-view Causal-inspired Attribution (Wang et al.) | [2609.04749](https://arxiv.org/abs/2609.04749) | 4 Sep | cs.AI | Causal dependency graphs + local counterfactual reasoning; Who&When SOTA (+8.27% step-level) |
| Adaptive Influence Graphs (Bakish et al.) | [2608.24361](https://arxiv.org/abs/2608.24361) | 25 Aug | cs.AI | Trace→graph→agentic navigation; Who&When SOTA |
| Localizing Emergent Failures: Minimal Repair Families via Counterfactual Replay (Li et al.) | [2608.29228](https://arxiv.org/abs/2608.29228) | 29 Aug | conf. paper | MRFR problem: all inclusion-minimal repair sets; GCJR exact on 120-DAG benchmark + 4-agent pilot |
| One Reflex, Two Answers: Model Judges Weakly Discriminate Localized from Distributed Causes (Scavotto) | DOI 10.3390/make8090275 | 8 Sep | *Mach. Learn. Knowl. Extr.* (journal) | Controlled fault injection; LLM judges barely separate localized vs distributed causes |

**Implication:** "which agent/step caused the failure" is a crowded, benchmarked (Who&When, TRAIL, MAST, SymFail) subfield. The seed must NOT be framed as attribution.

### Cluster C — Recovery, rollback, repair (OCCUPIED as standalone topic)

| Paper | arXiv | Date | Venue | One-liner |
|---|---|---|---|---|
| Repair or Resample? Rethinking Failure Debugging in LLM MAS / SymTrace + SymFail (Luan et al.) | [2608.25920](https://arxiv.org/abs/2608.25920) | 26 Aug | cs.AI+cs.SE | Controlled replay framework; 536 annotated failure trajectories; unguided rerun repairs only 6.9%; symptom-driven intervention 20.15% |
| ParaRecover: Process-Level Benchmark for Error Localization and Recovery in Parallel Tool-Use Agents (Guan et al.) | [2609.12345](https://arxiv.org/abs/2609.12345) | 11 Sep | **EMNLP 2026 main** | 10,626 instances, 14 error types; errors propagate across dependent branches → cascading failures; SDE rubric |
| Rollback the World, Keep the Reflection / RIR (Yu et al.) | [2609.18304](https://arxiv.org/abs/2609.18304) | 16 Sep | cs.AI | Recovery as "rollback-boundary control": when to intervene, where to resume, what knowledge survives |
| Safe to Resume? Breaking Execution Continuity via Rollback (Wu et al.) | [2608.29381](https://arxiv.org/abs/2608.29381) | 29 Aug | cs.CR | First security study of checkpoint/rollback in agent systems; 5 failure modes; attacks on Hermes, Cline, LangGraph |
| EvoUndo: Recoverability-Constrained Self-Evolution (Sah et al.) | [2608.28363](https://arxiv.org/abs/2608.28363) | 28 Aug | cs.* | 197/600 self-modifications fail recoverability verification; extended recovery calculus |
| What Drives Recovery in Agentic Text-to-Cypher / LAST-CQ (Prokopiou et al.) | [2609.12746](https://arxiv.org/abs/2609.12746) | 11 Sep | cs.* | Counterfactual ablations: detection+routing drives recovery, not feedback quality |

**Implication:** single-/multi-agent recovery mechanisms (replay, rollback, reflection, resampling) are actively published. The seed's recovery component must be *organizational* (cross-boundary containment) and *comparative* (mechanism vs mechanism on systemic impact + utility), not a new rollback method.

### Cluster D — "Blast radius" terminology in the window (adjacent senses only)

| Paper | arXiv | Date | Sense of "blast radius" |
|---|---|---|---|
| Can AI Remediate Backend Failures Safely? GuardedAct with Blast-Radius-Aware Sandboxing (Cai et al.) | [2609.11264](https://arxiv.org/abs/2609.11264) | 10 Sep | Collateral damage of an LLM-generated *remediation action* on production microservices; digital-twin sandbox estimates it; 87.4% recovery, collateral damage 25.6%→5.2%. **LLM is the repairer; the failing system is not an agent organization.** |
| Optimizing Credential Blast Radius Through Trust Boundaries and Delegation (Taipale & Lainio) | [2609.04566](https://arxiv.org/abs/2609.04566) | 3 Sep | Credential-compromise scope under post-quantum auth costs; optimization over trust domains. Security/credentials, no LLM agents. |
| Can AI Agents Deliver Verifiable Network-Wide Outcomes Across Authority Boundaries? (Zhang et al.) | [2609.10181](https://arxiv.org/abs/2609.10181) | 9 Sep | Notes authority scopes "limit the blast radius of an erroneous action" in network automation; problem is fragmented *evidence* of outcomes. |

**Implication:** the seed's use of "organizational blast radius" as a propagation-scope construct across boundary types is terminologically distinctive in this window, but the GuardedAct paper means reviewers will expect explicit differentiation from AIOps-remediation usage.

### Cluster E — Organizational / cross-boundary governance and testbeds (seed's home turf — partially occupied)

| Paper | arXiv | Date | What it does | Gap left for seed |
|---|---|---|---|---|
| Risks and Controls for Multi-Agent Systems: deployment across organisational boundaries (Reid, O'Callaghan, … Caetano — Australian AI Safety Institute) | [2608.26626](https://arxiv.org/abs/2608.26626) | 27 Aug | Analytical framework: 3 governance tiers (singular/federated/open), risk factors, failure modes, controls, control-gap analysis | **Qualitative policy framework, zero experiments.** Validates the problem's importance; does not touch blast-radius measurement or mechanism comparison. |
| Emergence World: Adversarial Stress-Testing of Long-Horizon Multi-Agent Systems (Akkil et al.) | [2609.17320](https://arxiv.org/abs/2609.17320) | 15 Sep | 8 worlds × 10 agents, 16 days, 850k LLM calls; 3 stress events (prompt injection, misinformation, memory exposure) via ordinary surfaces; **detection did not ensure containment**; threats written to persistent memory, acted on up to 46h later; model-level alignment "not compositional" | Closest *testbed* to the seed. But: adversarial-security framing, no fault-injection taxonomy across boundary types, no controlled comparison of containment mechanisms, no utility-preservation metric. |
| Why LLM Agents Collapse Without Oversight: The Enforcement Gap (Wang) | [2609.15293](https://arxiv.org/abs/2609.15293) | 14 Sep | Mechanism analysis of Emergence World: detection→action pathway missing; ~20-line fix cuts attack success >4×; formal proof that detection is irrelevant when enforcement ≈ 0 | Single mechanism (audit enforcement), not a comparative containment study. |
| Agentic Societies Need a Social Harness (Chugh et al.) | [2609.17527](https://arxiv.org/abs/2609.17527) | 15 Sep | Cross-trust-boundary agent societies; honest agents fail with current harnesses; layered "social harness" architecture (prevention, runtime detection, post-facto investigation) | Position+architecture paper; no propagation measurement. |
| Audit Without Verification: When LLM Accountability Layers Relay Rather Than Check (Arslan) | [2609.07680](https://arxiv.org/abs/2609.07680) | 7 Sep | Pre-registered, institutionally partitioned 6-agent pipeline, balanced defect injection, 345,600 requests/model; accountability layers relay conclusions instead of verifying; auditor below chance at origin recovery | Occupies the **accountability boundary** experimentally. Strong overlap with one seed dimension. |
| HANSARD: Forensic Readiness, Runtime Witnessing, Graded Attribution (Sardianos et al.) | [2608.22512](https://arxiv.org/abs/2608.22512) | 23 Aug | Reference architecture for accountability as lifecycle property; "attribution laundering"; Halpern–Pearl replay; synergy residual | Architecture proposal; accountability/attribution focus (also brushes the occupied delegation-accountability proposal territory). |
| ORCH: Organizational Principles Enable Collective Intelligence in Embodied AI (Ji et al.) | [2609.11737](https://arxiv.org/abs/2609.11737) | 10 Sep | Organization-theory principles (pooled/sequential interdependence) for embodied collectives; 25 wildfire missions incl. containment | Organizational *design* for performance, not failure propagation. |
| The Agentic Company OS (Larsen & Moghaddam) | [2609.13334](https://arxiv.org/abs/2609.13334) | 11 Sep | Position: enterprise agents stall due to cognitive-substrate mismatch | Position only. |

### Cluster F — Boundary-specific fault studies (each occupies ONE seed dimension)

| Boundary | Paper | arXiv | Date | Finding |
|---|---|---|---|---|
| Communication (handoff) | Facts Without Rules: Boundary Metadata Collapse in Multi-Agent LLM Handoffs (Wang et al.) | [2608.29028](https://arxiv.org/abs/2608.29028) | 29 Aug | "Summary collapse": handoffs preserve facts, lose boundary metadata; σ_b 0.80→0.57 under 25-word budget; explicit constraints cut leakage <15% |
| Communication (handoff) | When "Must" Becomes "Maybe": Constraint Weakening in LLM Agent Workflows (Sun et al.) | [2608.24569](https://arxiv.org/abs/2608.24569) | 25 Aug | Action-binding constraints degrade to advisory info across artifact transformations |
| Communication | Translating the Translator (Agrawal et al.) | [2609.15079](https://arxiv.org/abs/2609.15079) | 14 Sep | "English-Forcing Tax": 13–30.6 pp EM loss from English-routed inter-agent comms |
| Tool | Agents Trust Tools Too Much (Yang et al.) | [2609.05587](https://arxiv.org/abs/2609.05587) | 4 Sep | 14 LLMs; >1/3 mean adoption of corrupted tool returns, up to 68% (web search); agents notice conflict yet present corrupted answer |
| Tool | Robustness Analysis of Agentic AI to Inconsistent and Incomplete Tool Responses (Xu et al.) | [2608.22676](https://arxiv.org/abs/2608.22676) | 24 Aug | Likelihood + next-action signals to type tool failures at return time |
| Tool | Callability Is Not Operability / AFT-Bench (Wang) | [2608.23628](https://arxiv.org/abs/2608.23628) | 23 Aug | Valid tool calls can still leave agents unable to continue safely; interface interventions |
| Memory | MemRiskBench (Jiang et al.) | [2609.14976](https://arxiv.org/abs/2609.14976) | 14 Sep | 5-category memory risk taxonomy (stale, conflicting, cross-user leakage, revoked-memory reuse, constraint decay); 120-episode trace-grounded benchmark |
| Memory | MemGuard (Wang et al.) | [2608.21867](https://arxiv.org/abs/2608.21867) | 22 Aug | Verifier signals as persistent memory lifecycle metadata vs unreliable admission + drift |
| Memory | Invalidation Contracts for Cross-Episode Agent Memory (Wu & Canedo) | [2609.00243](https://arxiv.org/abs/2609.00243) | 31 Aug | Version-stamped cacheability for cached recovery suggestions under server drift |
| Memory | CAPTURE (Hossain et al.) | [2609.02265](https://arxiv.org/abs/2609.02265) | 2 Sep | Preference drift vs memory poisoning disambiguation |
| Authority/delegation | VERA: Authority-Preserving Edge Revocation (Liu et al.) | [2608.30091](https://arxiv.org/abs/2608.30091) | 30 Aug | Revocation semantics for delegation graphs; tree cascades over-revoke, deployer-scoped under-revoke. **Overlaps occupied delegation-invariants territory.** |
| Authority/delegation | Agent Mesh: Reliability Primitives for Non-Idempotent Agent Delegation (Shaikh et al.) | [2608.26225](https://arxiv.org/abs/2608.26225) | 26 Aug | Production failure study: 147 incidents/81 runs; retry/timeout/circuit-breaker assumptions violated; **"a misrouted failure woke five components for a two-component fault"** — empirical blast-radius evidence; 7 delegation-scoped reliability primitives |
| Authority/delegation | CONTINUITY: Security-Context Contracts (Zheng & Geng) | [2609.05269](https://arxiv.org/abs/2609.05269) | 4 Sep | Assume-guarantee contracts so security context survives component composition |
| Human-agent | PACT: Can Enterprise AI Assistants Be Trusted Under Pressure? (Okamoto & Erol) | [2609.18605](https://arxiv.org/abs/2609.18605) | 16 Sep | Compliance-rule following under social pressure; 12 enterprise domains, 48 scenarios |
| Context/harness | What's in Your Agent's Context? CPE attacks (Li et al.) | [2609.01222](https://arxiv.org/abs/2609.01222) | 1 Sep | Context privilege escalation via role confusion and cross-scope persistence; 12 real harnesses |

### Cluster G — Correlated failure / fault domains (theoretical overlap with "blast radius" determinants)

| Paper | arXiv | Date | Contribution |
|---|---|---|---|
| The Illusion of Independent Quorums: Epistemic Fault Domains and Correlated Cognitive Failures (He & Yu) | [2609.02925](https://arxiv.org/abs/2609.02925) | 24 Aug | EFD + Structural Epistemic Cut κ_E; proves arbitrarily large quorums can have κ_E=1 (shared upstream inputs collapse votes); DAQC runtime controller; frozen 120-task benchmark + code |
| Wavering Oracles: Selective Updating and Correlated Failures in LLMs (Nee et al.) | [2609.11428](https://arxiv.org/abs/2609.11428) | 10 Sep | 10 models, 17,055 trajectories; selectivity spans 13.4–71.6 pp; correlated error contribution undermines multi-model selectors |
| AI agents in clinical medicine: delegation, supervision, and the problem of correlated failure | DOI via SS (journal, no arXiv) | 29 Aug | Clinical-domain discussion of correlated failure under delegation |

### Cluster H — SoK / surveys that frame the field

| Paper | arXiv | Date | Scope |
|---|---|---|---|
| SoK: When Safe Agents Fail Together: The Security of Multi Agent LLM Systems (Yang et al.) | [2609.00595](https://arxiv.org/abs/2609.00595) | 1 Sep | 197 works; A-I-R framework (adversary position × interaction interface × system risk); defense contract incl. **recovery**; identifies "path closure and recovery as key challenges"; audits 44 benchmarks |
| Trustworthy Agentic AI: Cybersecurity and Systems Survey | [2609.13731](https://arxiv.org/abs/2609.13731) | 12 Sep | Threat landscapes, defense architectures |
| A Large-Scale Empirical Study of QA Practices and Gaps in AI Agents (Dai et al.) | [2609.17698](https://arxiv.org/abs/2609.17698) | 15 Sep | 157 OSS agent projects; safeguards inconsistent across equivalent routes; boundary/adversarial tests rare |
| How Fast Do Agents Rot? (Mittal) | [2609.01660](https://arxiv.org/abs/2609.01660) | 31 Aug | Geometric per-step reliability decay law; 9 models × 4 task families × 5 horizons |

---

## 4. Adversarial assessment against the seed hypothesis

### 4.1 What would be SCOOPED (do not claim as novel)

1. **"Errors/failures propagate through LLM MAS communication structure"** — published multiple times in-window, incl. EMNLP 2026 (PropUQ-MAS), ECML PKDD 2026 (Contagion/GMATS, with contagion metrics and topology-damping result), MobiHoc 2026 (Skynet).
2. **Failure attribution / root-causing in MAS** — saturated (Cluster B; Who&When/TRAIL/MAST/SymFail benchmarks).
3. **Replay/rollback-based recovery** — occupied (SymTrace, RIR, Safe to Resume, ParaRecover at EMNLP 2026).
4. **"Detection ≠ containment"** as a bare observation — Emergence World's headline finding (15 Sep), plus Enforcement-Gap mechanistic follow-up.
5. **Epidemic/contagion modeling of agent failure spread** — 2609.18460 explicitly frames mutation–contagion–recovery; a second "epidemic model of MAS failure" paper would be derivative.
6. **Delegation/revocation/authority-contract enforcement** — VERA, CONTINUITY, Agent Mesh, HANSARD, plus the existing MASO proposal at `maso/policy_preserving_delegation_research_proposal.md`. Occupied twice over.

### 4.2 What survives (residual novelty space for the seed)

1. **Multi-dimensional organizational blast radius as a measured construct.** No in-window paper quantifies how far a *single injected local fault* spreads simultaneously across *typed* organizational boundaries (role, communication, authority, tool, memory, accountability, human-agent) in an organizational workflow. Closest items each cover one dimension (Cluster F) or one untyped channel (Cluster A).
2. **Comparative evaluation of containment/recovery mechanisms on systemic-impact-vs-task-utility.** Emergence World delivers stress events but no mechanism comparison; GuardedAct compares mechanisms but for microservice remediation, not agent organizations; SymTrace compares repair strategies but on task success only, not containment of spread.
3. **Endogenous organizational faults (not adversarial injection).** Nearly all propagation work in-window is adversarial (poisoning, prompt injection). Non-adversarial local faults (a wrong summary, a stale memory, an over-broad delegation) propagating through an organization remain unstudied at system scale.
4. **Determinants of spread.** 2609.18460 explicitly disclaims establishing cascade conditions; 2609.02925 analyzes quorum authorization only. "What determines blast radius" (topology × boundary type × mechanism) is open.
5. **Terminology:** "organizational blast radius" as used in the seed does not appear in-window (verified: the only "blast radius" hits are AIOps-remediation, credential-scope, and one network-automation usage).

### 4.3 Kill/subsumption verdict

**Nothing in the window kills the seed.** The strongest subsumption threats, ranked:

1. **2609.18460 (Collective Loss of Control)** — shares the propagation+recovery framing and a benchmark; if the seed were "epidemic-style spread of unsafe behavior," it would be subsumed. Its self-declared limitations (no natural rates, no autonomous cascade, comm-path only) leave the organizational-determinants question open.
2. **2609.17320 + 2609.15293 (Emergence World pair)** — occupies "long-horizon organizational testbed with stress events and containment observations." The seed must differentiate: controlled fault injection with typed boundaries, mechanism comparison, utility preservation — not another emergent-behavior zoo.
3. **2609.19789 (Contagion/GMATS, ECML PKDD)** — occupies "contagion metrics + topology dampens spread" in one domain.
4. **2608.26626 (Australian AISI report)** — occupies the cross-organizational risk-framework *narrative*; being qualitative, it is a citation obligation, not a scoop.
5. **2609.07680 (Audit Without Verification)** — occupies the accountability-boundary experiment; the seed's accountability dimension must cite and go beyond it.

### 4.4 Repositioning advice (for the orchestrator)

- Frame as: **"organizational blast radius" = typed, multi-boundary propagation scope of endogenous local faults; contribution = measurement instrument + mechanism comparison under a utility-preservation budget.** This exact configuration is absent in the 30-day window.
- Mandatory differentiation section citing: 2609.18460, 2609.17320, 2609.19789, 2608.22130, 2609.06835 (propagation); 2609.11264, 2609.04566 (blast-radius term); 2608.26626, 2609.17527 (cross-org framing); 2609.07680 (accountability boundary); 2608.25920, 2609.12345 (recovery).
- Avoid: attribution-as-contribution (Cluster B saturated); delegation-invariant enforcement (occupied by existing MASO proposal + VERA/CONTINUITY); epidemic modeling per se (2609.18460).
- Note for feasibility: SymFail (536 trajectories), ParaRecover (10,626 instances), Who&When, TRAIL, MAST, RogueHandoff-20 are all in-window or recent artifacts that a MASO paper could build on rather than build from scratch.

## 5. Threats to validity of this sweep

- arXiv API rate-limiting forced discovery via Semantic Scholar; SS indexing lag could hide papers submitted ~19–21 Sep. A direct arXiv listing check (cs.MA/cs.AI recent) is recommended as a C2 follow-up for the final 3 days.
- SS relevance matching may miss papers that use neither "multi-agent" nor the queried synonyms; mitigated with 32 query variants including "agentic", "harness", "delegation", "rollback".
- Venue claims (EMNLP/ECML/MobiHoc 2026) are taken from arXiv page comments, not independently confirmed with the venues.
- Some in-window papers show hallmarks of low-quality or AI-generated content (e.g., RACER in *Int. J. Adv. Multidiscip. Res. Stud.*); they are reported for completeness but weighted low.
