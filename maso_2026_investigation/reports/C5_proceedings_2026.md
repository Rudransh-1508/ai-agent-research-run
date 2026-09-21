# C5 — Novelty Hunter: 2026 Conference Proceedings Sweep

**Mission:** Sweep AAMAS 2026, ICML 2026, ACL 2026, COLM 2026, AAAI 2026 proceedings for papers on multi-agent failure / reliability / containment / organizational agents, adversarially testing the seed hypothesis ("organizational failure propagation and recovery in LLM multi-agent systems" — what determines the *organizational blast radius* of a local fault, and which containment/recovery mechanisms minimize systemic impact while preserving task utility).

**Date of sweep:** 21 September 2026
**Investigator:** C5 (proceedings track)

---

## 1. Venue coverage and access status

| Venue | Dates / Place | Proceedings status as of 2026-09-21 | Source actually swept |
|---|---|---|---|
| AAAI-26 | Jan 20–27, 2026, Singapore | Published, ojs.aaai.org, 48 track issues (Vol. 40) | Multiagent Systems track (Vol. 40 No. 35 = issue 717, 74 articles) fully listed; Humans and AI track (No. 21 = issue 702, 87 articles) checked — nothing on-target |
| AAMAS 2026 | May 25–29, 2026, Paphos, Cyprus | Published; official TOC at ifaamas.org/Proceedings/aamas2026 (643 entries: 338 full research papers, 207 extended abstracts, plus AAAI/JAAMAS/Blue-Sky/Demo/DC tracks) | Full TOC swept; key PDFs downloaded and abstract-verified |
| ICML 2026 | July 2026, Seoul | PMLR volume **not yet published** (latest PMLR vols: 339 RAISE 2026, 337 UAI 2026, 336 COLT 2026 — no ICML 2026 yet) | Official icml.cc virtual-site data dump (`icml-2026-orals-posters.json`, 6,797 events incl. main conf. + workshops); main-conference accepts confirmed via `decision` field; abstracts verified via OpenReview search API and GitHub repos |
| ACL 2026 | Aug 2026 | Published on ACL Anthology | `2026.acl-long` (2,223 papers) and `2026.findings-acl` (2,164 papers) volume pages downloaded with full abstracts; both swept at title + abstract level |
| COLM 2026 | **Oct 6–9, 2026, San Francisco — NOT YET HELD** | No proceedings exist; 800 accepted papers listed at colm.cc/Conferences/2026/AcceptedPapers | Accepted-paper list swept; key abstracts verified via OpenReview search API |

Access notes: DBLP was unreachable (Anubis anti-bot proof-of-work on both curl and FetchURL). OpenReview forum pages are challenge-walled, but `api2.openreview.net/notes/search` worked with a browser User-Agent. arXiv API and Semantic Scholar API were persistently HTTP 429 (shared-IP contention with other swarm agents); arXiv IDs below come from author repositories' own citation blocks, not from the arXiv API.

---

## 2. Headline result

**The seed hypothesis is NOT killed, but its adjacent territory is heavily occupied in 2026 proceedings.** No 2026 proceedings paper uses the constructs "blast radius", "containment", or "circuit breaker" for LLM multi-agent failure (verified by exhaustive title search across all five venues — see §6). However, four clusters of 2026 papers occupy neighboring ground:

1. **Non-adversarial error propagation + repair in LLM MAS** (closest to the seed): AgentAsk (ACL), MASC (ACL Findings), CORRECT (ICML), R³DAO (ICML), EPC-AW (ICML).
2. **Containment/isolation of spreading faults — but framed adversarially** (malicious agents, injection): TopoSHIELD (ACL Findings), BPD (ICML), AgentRevive (ACL), AcMAS (ICML), ACIArena (ACL), BlindGuard (ACL), XG-Guard (ACL).
3. **Organizational/architectural structure → collective failure**: Diversity Collapse (ACL Findings — authority dynamics, topology density), Architecture Matters for Multi-Agent Security (ICML — roles/authority, topology, memory), HiddenBench (ICML), SILO-BENCH (ACL), MAS-BENCH (ACL Findings).
4. **Failure attribution/localization** (diagnosis, not containment): TraceElephant (ACL), ErrorProbe (ACL Findings), AgentLocate/"Who Broke the System?" (COLM), HiveMind DAG-Shapley (AAAI), Patient-0 contagion graphs in MARL (AAMAS), "Who Gets Credit or Blame?" (ICML).

The unoccupied remainder: a unified, non-adversarial "organizational blast radius" construct measured across role/communication/authority/tool/memory/accountability/human boundaries jointly, plus containment/recovery mechanisms explicitly optimized for systemic-impact-vs-task-utility trade-off. TopoSHIELD's "reduce spread while preserving >90% utility" is the closest existing formulation of that trade-off (adversarial setting only).

---

## 3. Verified papers — evidence tables

### 3.1 ICML 2026 (main conference; verified via icml.cc official data + OpenReview/GitHub)

| Paper | IDs / links | Problem, method, setting, findings | Relation to seed |
|---|---|---|---|
| Securing Multi-Agent Systems Against Corruptions via Node Contribution Backpropagation (BPD). Wu, Zhang, Xu, Wei, Sun | OpenReview `TphOLCDmKB`; code github.com/ChengcanWu/BPD; Accept (regular) | MAS communication modeled as signed DAG; external LLM scores edges {-1,0,1}; backward propagation detects malicious agents (threshold ε=1.5); **repair = isolate detected attacker, clear outgoing edges, re-run**. Flat vs hierarchy structures (5+2+5 hierarchy, 5+5+5 flat) on MMLU with DeepSeek/GPT-4o | Detection + **isolation + recovery** pipeline; hierarchy vs flat comparison = organizational structure matters. Adversarial framing |
| CORRECT: COndensed eRror RECognition via knowledge Transfer in multi-agent systems | OpenReview `ZUDdYZSwr4`; Accept (regular) | "Minor errors can propagate across agents, escalating into task failures." First lightweight training-free framework: online cache of distilled **error schemata** recognizing recurring failure structures; targeted error localization at inference | Non-adversarial error propagation + recognition. Direct neighbor of seed |
| R³DAO: Reactive Recovery and Reconstruction for Long-horizon Data Agent Orchestration | OpenReview `KxOlRNsRDG`; Accept (regular) | Static chain-like execution plans are "prone to error propagation from early stages — causing reasoning chain collapse and task failure." Reactive framework: dynamic hierarchical task network, feedback-driven topology evolution, "iterative recovery" closed loop | Error propagation + **recovery via topology evolution** in agent orchestration. Direct neighbor |
| AutoRAS: Learning Robust Agentic Systems with Primitive Representations | OpenReview `7zTV4dvdGB`; code github.com/guohezuy/AutoRAS; Accept (regular) | Automated design (GFlowNet search over primitive representations) of agentic systems "resilient to **both external adversarial attacks and internal execution failures**"; MMLU, attack/no-attack eval | Architecture search for robustness to internal faults — closest "design for containment" paper |
| MaMa: A Game-Theoretic Approach for Designing Safe Agentic Systems | OpenReview `KR6avDABG8`; project page jnoether.github.io/publication/MaMa; Accept (regular) | Stackelberg security game: Meta-Agent designs system, Meta-Adversary corrupts a subset of agents. **Discovered defenses include role separation (planning/execution/approval), multi-agent agreement, safety-review agents, monitoring.** Travel/personal-assistance/finance/codegen; large safety gains with minimal quality loss; robust to unseen models/attackers | Organizational design (role separation!) as automatic containment. Adversarial threat model but authors argue it covers accidental failures |
| Architecture Matters for Multi-Agent Security | OpenReview `Jk4zLorDUx`; Accept (regular) | Empirical study: how MAS design shapes task-performance vs attack-resistance. **Three design choices: (i) agent roles (authority/responsibility allocation), (ii) communication topology, (iii) memory.** 3 environments (browser, desktop, code), 13 architectures, stagewise eval (planning refusal → execution interception → partial harmful execution → attack completion) | Almost the seed's independent variables — but outcome is attack resistance, not organic-fault blast radius |
| When Planning Fails Despite Correct Execution: On Epistemic Calibration for LLM-Based Multi-Agent Systems (EPC-AW). Wang, Jin, Cao, Wang | OpenReview `9oZh2zQQXi`; code github.com/wzhSteve/EPC-AW; Accept (regular) | Repair framework for **epistemic miscalibration in the planning phase** of LLM MAS; n sampled candidate plans; Bamboogle, 2Wiki, HotpotQA, Musique, GAIA, MedQA | Fault localized to organizational phase (planning vs execution) + repair |
| When Agents Go Rogue: Activation-Based Detection of Malicious Behaviors in MAS (AcMAS) | OpenReview `BnduUW8izq`; Accept (regular) | Activation-space detection of stealthy malicious behavior without explicit interaction graphs; synchronization-robust; activation signals guide **restoring functionality** | Detection + recovery; adversarial |
| Systematic Failures in Collective Reasoning under Distributed Information in Multi-Agent LLMs (HiddenBench). Li, Naito, Shirado | OpenReview `igHBKQaLLP`; code github.com/Yassellee/HiddenBench_ICML; arXiv:2505.11556; Accept (regular) | 65 hidden-profile tasks separating individual reasoning from information pooling. **Frontier LLM groups: 30.1% accuracy under distributed information vs 80.7% single-agent full-information** | Systematic collective failure from information distribution — an organizational property |
| The Value of Variance: Mitigating Debate Collapse in Multi-Agent Systems via Uncertainty-Driven Policy Optimization | OpenReview `Bc6c2OVWRh`; Accept (**spotlight**) | "Debate collapse": final decisions compromised on erroneous reasoning. Hierarchical uncertainty metric (intra-agent, inter-agent, system-level) as failure diagnostic; uncertainty-driven policy optimization penalizes self-contradiction/peer conflict | Failure mode + detection + mitigation in deliberation |
| When Embedding-Based Defenses Fail: Rethinking Safety in LLM-Based Multi-Agent Systems | OpenReview `j5ibZwkwqF` (CoRR version `NkBIBNWnkN`); Accept (regular) | Malicious agents "propagate misinformation and manipulate group decisions"; embedding-based detect-and-prune defenses circumvented by Slow Drift / Benign Wrapper / Chaos Seeding attacks; token-level logit signals proposed | Propagation of misinformation; limits of prune-based containment |
| TRACER: Trajectory Risk Aggregation for Critical Episodes in Agentic Reasoning. Tayebati et al. | OpenReview `oVWRuzgQLU`; arXiv:2602.11409; code github.com/sinatayebati/agent-tracer; Accept (regular) | Trajectory-level uncertainty/tail-risk metric on τ²-bench (airline, retail, telecom); content-aware surprisal, loop/coherence situational metrics | Single-agent risk aggregation; boundary: agent–user stochasticity |
| Emergence of Biased Consensus in Multi-Agent LLM Debates | OpenReview `5EtByXq4bX`; Accept (regular) | Consensus bias emergence in debates (title-verified; abstract not retrievable — OpenReview search miss) | Collective failure mode |
| Learning Robust Multi-Agent Policies via Selective Adversarial Fault Induction | OpenReview `t0kOFRgwR8`; Accept (regular) | Fault induction for robust MARL policies (title-verified) | Fault injection → robustness; MARL not LLM-MAS |
| Who Gets Credit or Blame? Attributing Accountability in Modern AI Systems | OpenReview `wfHCePoAed`; Accept (regular) | Accountability attribution across model **development stages** (pretrain/finetune/align) via counterfactual stage-effect estimators | Accountability boundary — but model-pipeline, not organizational MAS |
| Also accepted (title-verified, lower relevance): TeamTR (trust-region fine-tuning for multi-agent LLM coordination, `IMwLhg52ZY`), MEMO (robust multi-turn multi-agent LLM games, `bYDjZyqKxq`), OpenDeception (deception/trust in human–AI multi-agent simulation, `PW8YVqhI6K`), RedDebate (multi-agent red-teaming debates, `79fSrxFKKx`), FormalJudge (neuro-symbolic agentic oversight, `tnsQ23imeD`), Cycle-of-Science (counterfactual verification for agent decisions, `NvTyyBFICP`), RAGEN-2 (reasoning collapse in agentic RL, spotlight), Anytime Detection of Strategic Deviations (e-value sequential tests vs equilibrium, `hXO2OP0T4w`), "Delegation and Verification under AI", "Adaptive Contracts for Cost-Effective AI Delegation" | | | |

### 3.2 ACL 2026 (main + Findings; abstracts verified from ACL Anthology volume pages)

| Paper | ID | Key content (from verified abstract) | Relation to seed |
|---|---|---|---|
| AgentAsk: Multi-Agent Systems Need to Ask | 2026.acl-long.1294 | MAS "often fail to consistently outperform strong single-agent baselines due to **error propagation at inter-agent message handoffs**." Edge-level error taxonomy: **Data Gap, Signal Corruption, Referential Drift, Capability Gap**. Lightweight clarification module intervenes at edges "to prevent cascading errors"; +4.69% accuracy, <10% cost; 5 benchmarks | **Closest non-adversarial propagation+intervention paper.** Edge-level only; no org-structure variables |
| Seeing the Whole Elephant: A Benchmark for Failure Attribution in LLM-based Multi-Agent Systems (TraceElephant) | 2026.acl-long.912 | Failure attribution (responsible agent + decisive step) under **full execution observability**; full traces improve attribution accuracy up to 76.5% over partial observation | Attribution, not containment; supplies evaluation methodology |
| ACIArena: Toward Unified Evaluation for Agent Cascading Injection | 2026.acl-long.457 | **Agent Cascading Injection**: compromised agent exploits inter-agent trust to propagate malicious instructions, "causing cascading failures across the system." 1,356 test cases, 6 MAS implementations, 3 attack surfaces, 3 objectives. Finding: "evaluating MAS robustness solely through topology is insufficient; **robust MAS require deliberate role design and controlled interaction patterns**"; defenses from simplified settings fail to transfer | Cascading failure benchmark; role design as containment variable. Adversarial |
| TAMAS: Benchmarking Adversarial Risks in Multi-Agent LLM Systems | 2026.acl-long.1442 | 300 adversarial instances, 6 attack types, 211 tools, 10 backbone LLMs, AutoGen/CrewAI configs; **Effective Robustness Score (ERS) trading off safety vs task effectiveness**; MAS "highly vulnerable" | Safety–utility trade-off metric; adversarial |
| BlindGuard: Safeguarding LLM-based Multi-Agent Systems under Unknown Attacks | 2026.acl-long.1819 | Names "**propagation vulnerability**, where malicious agents distort collective decision-making through inter-agent interactions." Unsupervised hierarchical agent encoder + corruption-guided detector (noise injection + contrastive) | Detection of propagating malice without labels |
| Explainable and Fine-Grained Safeguarding of LLM MAS via Bi-Level Graph Anomaly Detection (XG-Guard) | 2026.acl-long.1407 | Bi-level (sentence/token) agent encoder + theme-based anomaly detector across diverse MAS topologies and attack scenarios | Detection; topology-aware |
| Taming "Zombie" Agents: A Markov State-Aware Framework for Resilient Multi-Agent Evolution (AgentRevive) | 2026.acl-long.373 | Hard pruning discards agents that could recover. **Soft state transitions Active/Standby/Terminated**; risk estimator assesses hallucination risk; "minimizing the influence of unreliable nodes while safeguarding valuable ones"; standby nodes retained for later rounds | **Containment + recovery of faulty (non-adversarial) agents**; resilient topology evolution |
| SILO-BENCH: A Scalable Environment for Evaluating Distributed Coordination in Multi-Agent LLM Systems | 2026.acl-long.1354 | Role-free benchmark under information silos; 1,620 experiments; **Communication–Reasoning Gap**; performance collapses at Level-III beyond 50 agents | Coordination failure from information distribution |
| When KV Cache Reuse Fails in Multi-Agent Systems | 2026.acl-long.327 | Efficiency optimization (KV reuse) silently perturbs LLM-judge selection; Judge Consistency Rate metric | Infrastructure-induced failure mode |
| Visual Inception: Compromising Long-term Planning in Agentic Recommenders via Multimodal Memory Poisoning | 2026.acl-long.954 | Poisoned long-term memory hijacks future planning ("sleeper agents" in memory); CognitiveGuard dual-process defense; ~85% Goal-Hit Rate reduced to ~10% | **Memory boundary** propagation + defense |
| MARCH: Multi-Agent Reinforced Check for Hallucination | 2026.acl-long.1828 | Deliberate **information asymmetry** between Solver/Proposer/Checker breaks confirmation bias; MARL-trained | Information partitioning as failure containment |
| Diversity Collapse in Multi-Agent LLM Systems: Structural Coupling and Collective Failure in Open-Ended Idea Generation | 2026.findings-acl.13 | "**Collective failures emerging from structural coupling**": stronger aligned models → diminishing diversity; **authority-driven dynamics suppress semantic diversity** vs junior-dominated groups; **dense communication topologies accelerate premature convergence**. Collapse "arises primarily from the interaction structure rather than inherent model insufficiency" | **The most "organizational" 2026 paper**: authority + topology → collective failure. Non-adversarial. Outcome is diversity, not task fault spread |
| TopoSHIELD: Reshaping the Flow of Malice via Spatio-Temporal Risk-Aware Topological Evolution in MAS | 2026.findings-acl.426 | Interconnectivity as "conduit for rapid spread of malicious injections." Spatio-temporal GNN monitors dynamics; node risk entropy + edge attack conductivity; **structural interventions: prune high-risk edges, isolate compromised communities to block diffusion. Reduces toxicity 58% (GPT-4o) while preserving >90% task success** | **Blast-radius containment with explicit utility preservation** — the seed's objective function, adversarial framing |
| Towards Self-Improving Error Diagnosis in Multi-Agent Systems (ErrorProbe) | 2026.findings-acl.98 | Failure attribution: local anomaly detection via MAS failure taxonomy, symptom-driven backward tracing, Strategist/Investigator/Arbiter validation team, verified episodic memory; evaluated on TracerTraj and Who&When benchmarks | Attribution; references prior Who&When benchmark |
| Metacognitive Self-Correction for Multi-Agent System via Prototype-Guided Next-Execution Reconstruction (MASC) | 2026.findings-acl.1168 | MAS "brittle to **cascading errors: a single faulty step can propagate across agents** and disrupt the trajectory." Real-time unsupervised step-level anomaly scoring (next-execution reconstruction + prototype prior); correction agent revises output **before information flows downstream**; +7.8% AUC-ROC on Who&When (w/o GT), gains on AgentErrorBench | **Non-adversarial cascade interception.** Direct neighbor |
| Topology Matters: Measuring Memory Leakage in Multi-Agent LLMs (MAMA) | 2026.findings-acl.1980 | Topology-conditioned memory leakage: 6 topologies × sizes; **denser connectivity, shorter attacker–target distance, higher target centrality increase leakage**; leakage concentrated in early rounds | **Memory boundary × topology** — quantified spread determinants |
| When 20 Agents Fail to Sort: The Distributed Sorting Benchmark (MAS-BENCH) + CAMOC | 2026.findings-acl.1698 | Fragility under scaling on trivial tasks; failures in shared state, convention alignment, termination; CAMOC mitigation (collaboration-aware sharing, early metadata exchange, single-commit verification) | Scale-induced organizational failure + mitigation |
| From Tasks to Teams: A Risk-First Evaluation Framework for Multi-Agent LLM Systems in Finance (M-SAEA) | 2026.findings-acl.1934 | Audits LLM teams across 4 layers (model, workflow, interaction, system), 10 probes, continuous risk vector | Team-level risk auditing |
| MCP-Guard: Multi-Stage Defense-in-Depth for Securing Model Context Protocol | 2026.findings-acl.240 | 3-stage detection pipeline for MCP tool-layer attacks; MCP-AttackBench (70,448 samples) | Tool/MCP boundary — overlaps the occupied delegation-invariants territory |
| Also relevant (title-verified): Self-Evolving Multi-Agent Systems via Textual Backpropagation (findings-acl.483); FAMA: Failure-Aware Meta-Agentic Framework (findings-acl.1716); MADRA: risk-aware embodied planning via debate (findings-acl.340) | | | |

### 3.3 AAMAS 2026 (verified via official IFAAMAS proceedings TOC + PDF full text where noted)

| Paper | Proceedings ID | Key content | Relation to seed |
|---|---|---|---|
| Interpretable Failure Analysis in Multi-Agent Reinforcement Learning Systems. Shefin, Gupta, Le, Alqahtani | DOI 10.65109/GWFE6009 (Research Track, p.1ff); PDF-verified | Two-stage gradient-based diagnostics: **(1) Patient-0 detection (true initial failure source), (2) explaining "downstream-first" detection anomalies from domino effects, (3) tracing failure propagation through learned coordination pathways as interpretable contagion graphs** (critic derivative sensitivity + curvature over causal windows). 500 episodes Simple Spread (3/5 agents), 100 episodes StarCraft II, MADDPG/HATRPO; 88.2–99.4% Patient-0 accuracy | **Failure propagation + contagion graphs + Patient-0** — the seed's core vocabulary, in MARL (not LLM) setting |
| Reputation as a Solution to Cooperation Collapse in LLM-based MASs (RepuNet). Ren et al. | DOI 10.65109/UEHN4980 (p.245); PDF-verified | Cooperation collapse emerges in LLM MAS; dual-level reputation (agent-level + network evolution via interaction/gossip); agents connect/disconnect peers; avoids collapse in 3 scenarios | Collapse + self-organizing containment via reputation |
| Beyond Vibe Decision Theory: Asymmetric Manipulation Vulnerabilities in LLM Multi-Agent Coordination. Krishna (Harvard), South (Stanford) | p.2482 (Research Track); PDF is image-only (no text layer) — title/author-verified only | Manipulation vulnerabilities in LLM coordination | Influence/manipulation failure modes |
| The Triad of Identity, Trust and Responsibility in Multi-Agent Systems | p. (Research Track); VTZX9616.pdf | Identity/trust/responsibility triad | Accountability boundary (classical MAS framing) |
| On Quantitative Analysis of Responsibility in Multiagent Systems | PVFH7189.pdf | Quantitative responsibility analysis | Accountability boundary |
| Verification of Robust Multi-Agent Systems | DHRR7601.pdf | Formal verification of robust MAS | Classical robustness |
| Developing Guidelines for Human-LLM Agent Teams: A Multi-Stakeholder Lens | JOWO4591.pdf | Guidelines for human-LLM teaming | Human-agent boundary |
| LLM Performance Predictors: Learning When to Escalate in Hybrid Human-AI Moderation Systems | KWGX1235.pdf | Learning when to escalate to humans | Human-agent boundary / escalation as containment |
| IntentGuard: Securing MCP-Enabled LLM Agents via Post-Decision Semantic Plan Verification (ext. abs). Cheng et al. | PJGH6650.pdf; PDF-verified | Post-decision semantic plan verification for MCP-enabled agents | Tool/MCP boundary — overlaps occupied delegation territory |
| Finding the Weakest Link: Adversarial Attack against Multi-Agent Communications (ext. abs). Standen, Kim, Szabo | GION7107.pdf; PDF-verified | Which messages to perturb, when to attack, which agent to target, how to craft perturbation | Communication boundary vulnerability (MARL comms) |
| When LLM Agent Teams Fail at Topological Spatial Reasoning Under Partial Observability (ext. abs). Gama, Diguet, Ranasinghe | RTFT9958.pdf; PDF-verified | LLM agent teams fail at map-topology reasoning under decentralized information | Team failure under partial observability |
| Also in proceedings (title-verified): MA-SafeDiffuser (safe multi-agent planning), Robust Information Design for MAS, ReAcTree (hierarchical LLM agent trees with control flow), Disobedience in Normative MAS, You Can Go First (social law synthesis), Engineering Norm-aware BDI Agents | | | |

### 3.4 AAAI-26 (Multiagent Systems track, Vol. 40 No. 35; abstracts verified from ojs.aaai.org article pages)

| Paper | Article ID | Key content | Relation to seed |
|---|---|---|---|
| Attack the Messages, Not the Agents: Multi-round Adaptive Stealthy Tampering Framework for LLM-MAS (MAST) | 40224 | MCTS+DPO-trained attack policy tampers with **inter-agent messages** multi-round with semantic/embedding stealth constraints; high ASR across tasks/architectures/LLMs; "underscores the need for robust communication safeguards" | Communication boundary as propagation channel |
| A Graph-Theoretical Perspective on Law Design for Multiagent Systems | 40211 | **Laws = constraints avoiding undesirable outcomes; "useful laws" eliminate outcomes, "gap-free laws" guarantee ���1 responsible agent per outcome; minimization NP-hard; hypergraph vertex-cover approximation** | Classical-MAS institutional containment + guaranteed accountability — direct classical grounding for the seed |
| HiveMind: Contribution-Guided Online Prompt Optimization of LLM MAS | 40222 | **DAG-Shapley** contribution attribution identifies underperforming agents; online prompt refinement | Attribution + targeted repair |
| Key Decision-Makers in Multi-Agent Debates: Who Holds the Power? | 40235 | Role allocation ("Truth Last") swings MAD performance up to 22%; MADC consistency strategy | Authority/position determines influence — org variable |
| MPAS: Individual-Epistemic Message Propagation | 40231 | Sequential DAG execution "exhibits vulnerabilities to potential backdoor threats"; node-wise message-passing parallelization | Topology × vulnerability |
| SafeSieve: Progressive Pruning for LLM-based Multi-Agent Communication | 40236 | 0-extension clustering prunes ineffective links; 94.01% accuracy with reduced tokens | Communication pruning (efficiency-motivated, containment-adjacent) |
| Not on-target: 68 remaining track papers (MAPF, DCOP, MARL, debate, applications). Humans and AI track (No. 21, 87 articles): nothing on organizational failure propagation | | | |

### 3.5 COLM 2026 (accepted, conference Oct 6–9, 2026; abstracts verified via OpenReview search API)

| Paper | OpenReview ID | Key content | Relation to seed |
|---|---|---|---|
| Who Broke the System? Failure Localization in LLM-Based Multi-Agent Systems (AgentLocate) | `5RmOQVmCRO` | Attributes failure to specific agent + **earliest decisive step where trajectory first becomes irreversibly misdirected**; LLM judge + multi-perspective independent verifiers + confidence-aware aggregation; judge adapts from feedback | Failure localization; "point of no return" concept is blast-radius-adjacent |
| Misalignment Contagion: Can a Misaligned Minority Shift Aligned Agents in Multi-Agent LLM Deliberation? | `tj2fLGyWC9` | **A single emergently-misaligned agent (narrow fine-tuning, no adversarial intent) shifts aligned majority's privately-elicited post-deliberation stances** through ordinary debate; 35,290 trials, 5 datasets, **4 communication topologies**; persists under private re-elicitation | **Non-adversarial contagion through deliberation** — propagation without an attacker; topology-dependent |
| Talk is Cheap, Communication is Hard: Dynamic Grounding Failures and Repair in Multi-Agent Negotiation | `heL1Vjbtis` | Iterated negotiation with verifiable joint optima; dyads consistently miss optima; **four failure modes: loss of shared history, anchoring, equal-split shortcuts, abandonment of public agreements at execution**; transparency helps but doesn't fix | Communication failure taxonomy + repair |
| LLMs Corrupt Your Documents When You Delegate (DELEGATE-52) | `DazQybEvgz` | 52 professional domains, 20 LLMs; **frontier models corrupt avg 22% of document content by end of long delegated workflows** | **Delegation boundary** failure measurement |
| Benchmarking the Robustness of Agentic Systems to Adversarially-Induced Harmful Behaviors | (title-verified) | Robustness benchmark | Adversarial |
| Also accepted (title-verified): Learning to Interrupt in Language-based Multi-agent Communication; Cooperative Profiles Predict Multi-Agent LLM Team Performance in AI-for-Science Workflows; The Collaboration Gap (open-world agentic cooperation benchmark); AgentWorld (long-horizon collaboration benchmark); AMAT (automated multi-agent topology design via RL); Failure-Aware Penetration Testing via Typed Failure Tokens | | | |

---

## 4. Terminology / novelty cross-check

Exhaustive title search across all five venues (ICML 6,797; COLM 800; AAMAS 643; ACL long 2,223; ACL findings 2,164; AAAI-26 MAS track 74 + Humans&AI 87):

| Seed term | Hits in 2026 proceedings |
|---|---|
| "blast radius" | **0** anywhere |
| "containment" (of failures/agents) | **0** (only ML-unrelated "container sandbox" hits) |
| "circuit breaker" | **0** |
| "quarantine" | **0** |
| "organizational" (MAS context) | **0** |
| "failure propagation" / "error propagation" in LLM-MAS | Present in abstracts (AgentAsk, MASC, CORRECT, R³DAO) — concept occupied, phrase not titular |
| "cascading failure/error" in LLM-MAS | ACIArena (cascading injection), MASC (cascading errors) |
| "contagion" | Misalignment Contagion (COLM); contagion graphs (AAMAS MARL) |
| "recovery" in agent orchestration | R³DAO (ICML), AgentRevive (ACL) |
| "failure attribution/localization" | TraceElephant, ErrorProbe (ACL), AgentLocate (COLM), HiveMind (AAAI) — crowded |

Prior benchmarks repeatedly cited by 2026 papers (pre-2026, for context): **Who&When** (failure attribution), **AgentErrorBench**, **TracerTraj**.

## 5. Gaps the seed could still claim (and what it must differentiate from)

Unoccupied in 2026 proceedings:
1. The **unified "organizational blast radius" construct** — fault spread measured jointly across role, communication, authority/delegation, tool, memory, accountability, and human-agent boundaries — no paper operationalizes this.
2. **Non-adversarial, organic local faults** (hallucination, tool error, stale memory, misunderstanding) as the fault source with containment/recovery optimized for systemic-impact-vs-utility. Existing non-adversarial work (AgentAsk, MASC, CORRECT) does edge/step-level detection+repair, not org-level containment design; existing org-level work (TopoSHIELD, BPD, MaMa, Architecture Matters) is adversarial.
3. **Recovery** (post-containment restoration of function) is nearly untouched — only AgentRevive (standby/revival), AcMAS (functionality restoration), R³DAO (reactive reconstruction).
4. Human-agent boundary escalation as a *containment* mechanism (only "LLM Performance Predictors: Learning When to Escalate" at AAMAS, moderation domain).

Must differentiate from: AgentAsk & MASC & CORRECT (error propagation + repair), TopoSHIELD & BPD (topology containment with utility preservation), Diversity Collapse & Architecture Matters (structure→failure), TraceElephant/ErrorProbe/AgentLocate (attribution), MaMa/AutoRAS (design-for-robustness).

## 6. Limitations of this sweep

- DBLP unreachable (Anubis); ICML 2026 PMLR volume not yet published — ICML coverage relies on official icml.cc data, which is authoritative for acceptances.
- arXiv/Semantic Scholar APIs rate-limited throughout; a few papers are title-verified only (flagged in tables).
- AAAI-26 tracks other than Multiagent Systems and Humans & AI (e.g., NLP I–VI, Application Domains) were not exhaustively listed; LLM-MAS failure papers could hide there.
- COLM 2026 not yet held; analysis based on accepted-titles + OpenReview abstracts for key papers only.
- AAMAS "Beyond Vibe Decision Theory" PDF lacks a text layer; title/author-verified only.
