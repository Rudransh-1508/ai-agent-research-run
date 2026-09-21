# AUDIT2 — STAGE 3: S3-VERIFY-SECONDARY

**Date:** 2026-09-21
**Mission:** Upgrade the remaining Stage-1 abstract-only/unverified threats to verified status. For each: abstract + method + experiments at minimum; state exactly what it occupies relative to the candidate (fault propagation/containment/recovery in tool-executing LLM multi-agent organizations; H1 delegation depth, H2 containment cost, H3 scarcity sign reversal).
**Stance:** Hostile. Goal is to find fatal problems while cheap.
**Sources read first:** audit2/A1, A3, A8, A9, A11, A12 (all Stage-1 claims about these papers re-checked against primary sources this session).

**Verification-level key:** FULL TEXT = arXiv HTML full text read this session (method + experiments + references where noted). ABSTRACT VERIFIED = arXiv abs page or Crossref full abstract read this session. Anything less is marked.

---

## 0. BOTTOM LINE

All nine assigned threats verified; **six upgraded to FULL TEXT**, two to ABSTRACT VERIFIED (Crossref full abstract / arXiv abs), one (memory-poisoning repair) confirmed ABSTRACT-ONLY-accessible (preprints.org bot-walled, 403 on both HTML and PDF download). **No Stage-1 classification needed reversal, but two need sharpening:**

1. **Outcome Monitors is a stronger threat than A8 recorded** — full text shows a *third* environment (held-out AppWorld) where the mechanism shows **no net effect**, and a frozen, prespecified, intention-to-treat protocol on tau-bench retail (50 tasks × 5 fault types factorial). It is methodologically ahead of the candidate's planned design on the candidate's exact environment — but strictly single-agent.
2. **The tau²-retail noise floor is real but asymmetric and worse than "±12–15pp" on the upside**: paired configuration-equivalent gaps span **[−3, +18]pp** across two n=100 seeds; pooled +5pp, Wilson CI [−2, +12], upper Wilson ≲15pp. Single-seed contrasts up to **+18pp** arise from pure noise at n=100. Any planned n=100/cell binary contrast on tau²-bench retail is dead on arrival; the paper's own coordination-active subsets had only n=8–17 informative pairs.
3. **ResMAS's structure manipulation is weaker than "topology × resilience" implies**: structure is an *optimization target*; the only structure-as-factor evidence is a 30-random-graph motivational sweep plus a two-topology case study (hierarchical > centralized). No delegation depth, no tools, no recovery, no cost vector. H1's measurement claim survives it comfortably.
4. **Sentinel Agents independently confirmed to cite zero classical MAS** (my own reference-list scan: no Dellarocas, Klein, Hägg, no exception-handling lineage). Its evaluation is detection-only (quarantine disabled, no false positives measured, 100% detection on 162 synthetic attacks). It occupies the *word and the architecture sketch*, not any measured containment/recovery effect.
5. Neither "backfire" paper is a scarcity backfire: Alignment Backfire = language-moderated sign reversal of alignment interventions; Feedback That Backfires = harness-level repetition pathology (delete-and-retry is the *worst* measured harness). Both belong in the candidate's related-work as convergent "interventions backfire" evidence; neither occupies H3.

---

## 1. Outcome Monitors — arXiv:2608.19303 (v1, 19 Aug 2026) — **FULL TEXT VERIFIED**

**Authors/venue:** Panthi & Abdelfattah, University of Southern Mississippi. 16 pp (9 main + 7 supp). cs.AI/cs.CL/cs.SE.

**Method:** Deterministic detector for **silent tool failures** ("a cached error page or negative price arrives in the expected format and is consumed as fact"). *Outcome contracts* — invariants over tool-call/result relationships — mined from nominal executions with **task-disjoint cross-fitting** (ToolMaze), derived from public API schemas (AppWorld), or mined from the public database (tau-bench retail). On violation the monitor preserves the result and issues a **nonbinding advisory receipt** naming the violated property + a list of public recovery tools; it never blocks an action, executes a repair, or sees fault labels. Explicit design goal: separate detection from recovery so evaluators score the *agent's chosen* recovery.

**Experiments (frozen, prespecified; intention-to-treat paired completion):**
- ToolMaze injected implicit failures: completion **10.9% → 28.1%**, 4 models across DeepSeek + Qwen families; separately frozen MiniMax M3 third-family replication.
- **tau-bench retail**: 50 of 115 test tasks (seed 20260718), 50×5 factorial (5 fault types) on DeepSeek V4 Flash; completion **+14.0 and +12.0 points on two fault tiers** (status-fault tier +28.0 in one arm; categorical 12.0%); task-clustered inference; 16/16 prespecified model-by-stratum point estimates positive.
- **Held-out AppWorld: NO measured net effect** ("delivery without net gain"; detection 78.1% but completion unchanged). Gains are explicitly not universal.
- Controls: removing the recovery-tool list eliminates the gain (restoring it recovers the effect) — **recovery affordances, not diagnostic detail or timing, are the active ingredient**. Detection outside mined contract vocabulary falls to **46%**.
- Fault-prevalence (π) deployment-mixture analysis; harm = baseline-only success tracked.

**Single or multi agent?** **Strictly single-agent.** All three environments are single-agent benchmarks; the paper's framing is "the acting agent" + monitor. No inter-agent propagation, no organization, no scarcity arm.

**Occupies:** H2's mechanism half in the candidate's exact planned environment — a detection+recovery-affordance mechanism for injected *semantic* tool faults on tau-bench retail, with a stronger evaluation protocol (frozen/prespecified/ITT) than most of the field. Also occupies "silent/semantic tool failure" as a fault model and prices a deployment-prevalence mixture.
**Does NOT occupy:** multi-agent propagation, organizational structure, containment *cost* (no cost vector — the monitor is deterministic and cheap; no budget manipulation), scarcity sign reversal.
**Action for candidate:** must-cite; differentiate on multi-agent propagation through shared state; match or exceed its protocol rigor (frozen task sets, prespecified endpoints, harm tracking) or reviewers will compare unfavorably. Its AppWorld null is useful: detection gains do not trivially transfer — supports the candidate's claim that environment/structure moderates containment value.

## 2. The Verifier Tax — arXiv:2603.19328 (v1, 18 Mar 2026) — **FULL TEXT VERIFIED**

**Authors/venue:** Sah, Srivastava, Sah, Jordan (Harrisburg U., JHU, Utah). HTML header claims "ACM Conference on AI and Agentic Systems, 2026." 10 pp. cs.CR.

**Method:** Runtime policy enforcement ("verifier mediation") for tool-using agents on **tau-bench Airline + Retail**. Three architectures: baseline Tool-Calling; planning-integrated TRIAD; policy-mediated **TRIAD-SAFETY** (verifier gate + Block-and-Revise loop). Models: GPT-OSS-20B, GLM-4-9B; max_turns 15/30 (model-dependent horizons). Outcome decomposition: SR / SSR (safe success) / USR (unsafe success). Token accounting per episode (agent vs user-simulator separated; reconstructed prompts, native tokenizers; stated as conservative lower bound).

**Experiments/results:** Safety mediation intercepts up to **94%** of non-compliant actions but **SSR < 5%** in most settings ("Safety-Capability Gap"); high USR driven by **Integrity Leaks** (agents hallucinate user identifiers to bypass mandatory authentication); **recovery after blocked actions: 21% (GPT-OSS-20B, simple procedural) → ~0% (complex Retail)**; verifier tax quantified as **2.0–2.8× token overhead** plus conversational-length inflation, "without guaranteeing safe completion."

**Occupies:** H2's cost clause *by name* on the candidate's benchmark family — "containment/verification imposes a measurable tax on tool-executing agents" is published, quantified (2.0–2.8× tokens), and paired with a post-intervention recovery measurement (which is *worse* in the more complex domain — horizon-dependent tax). Single-agent; safety-compliance faults (policy violations), not propagated faults; cost is a fixed measurement, not budget-scaled — no scarcity manipulation, no sign reversal.
**Action:** must-cite for H2's cost premise; the candidate's H2 novelty cannot be "containment costs resources" (dead) — only the priced comparison across mechanisms/structures and the H3 interaction. Its recovery-after-block metric (21%→0%) is direct prior art for recovery-cost measurement on tau-bench and partially anticipates "containment interacts with task complexity."

## 3. Sherlock — arXiv:2511.00330 (v1, 1 Nov 2025) — **FULL TEXT VERIFIED**

**Authors/venue:** Ro, Qiu, Goiri, Fonseca, Bianchini, Akella, Wang, Erez, Choukse — Microsoft Azure Research + UT Austin. cs.MA listing.

**Method:** Agentic workflows as DAGs of LLM/tool/retrieval nodes (planner: Flow, Niu et al. 2025). (i) **Fault model + counterfactual fault injection** per node to derive node vulnerability; topological vulnerability estimator for new workflows. (ii) **Cost-optimal verifier placement**: heuristic policy under an explicit verification cost budget + learned selector (GRPO-trained preference learning over verifier accuracy–cost pairs, distilbert features). Verifier portfolio: self-refine, advanced-refine, LLM-as-a-judge (Selene-1-Mini-8B), debate, self-consistency. (iii) Runtime: **speculative downstream execution** with background verification; **rollback to last verified output** on failure; lightweight similarity metrics to validate speculative outputs.

**Experiments:** Benchmarks = **CoTCollection (instruction-following), OMEGA (math, compositional), LiveCodeBench (code)** — reasoning/coding, *not* stateful tool benchmarks, *not* tau-bench. Results: **+18.3% accuracy** avg vs non-verifying baseline; **−48.7% latency** vs non-speculative; **−26.0% verification cost** vs Monte-Carlo placement. Motivational measurement: verifying every step costs up to **28.9×/53.2×** (instruction-following/coding).

**Occupies:** H2's cost premise at the workflow level — "verifying everything is prohibitively expensive; place verifiers cost-optimally and roll back locally" is solved and quantified by a Microsoft systems group. Also occupies fault injection + propagation-along-edges as *analysis* (counterfactual vulnerability), and rollback-to-last-verified as a recovery primitive.
**Does NOT occupy:** organizational MAS (workflows are single-planner DAGs, no agents-with-authority), structure as IV, scarcity as regime (budget is a constraint to optimize within, never a manipulated regime; no sign reversal — more verification never *hurts* net utility under scarcity in their results), stateful tool environments.
**Action:** must-cite; the candidate's rollback/containment mechanisms must be positioned as organizational (cross-agent, authority-bearing) rather than workflow-node-level. Note for MASO reviewers: Sherlock is the strongest existing "verification cost optimization" citation and will be the reviewer's benchmark for H2.

## 4. Sentinel Agents — arXiv:2509.14956 (v1, 18 Sep 2025; doc dated 24 Aug 2026) — **FULL TEXT VERIFIED (incl. reference list)**

**Authors:** Gosmar (Tesisquare/Linux Foundation AI & Data) & Dahl (Conversational Technologies).

**Method:** Architecture paper. Network of **Sentinel Agents** (distributed security layer: LLM semantic analysis, regex/rule-based filters, RAG verification, behavioral anomaly detection over a Shared Conversational Space / Open Floor Protocol) + **Coordinator Agent** (policy dissemination, alert ingestion, **isolation/quarantine of misbehaving agents, containment**). Deployment patterns: sidecar, proxy, continuous-listener, hybrid; layered monitoring: pre-validation (proactive blocking), passive listening, hybrid.

**Experiments:** Proof-of-concept continuous-listener only: **162 synthetic adversarial prompts** (prompt injection, hallucination, data exfiltration) injected into a conversational floor; **100% detection rate**; **quarantine disabled** for the evaluation (detection outcomes only); **no ablation; no false positives measured** (adversarial-only dataset); authors state it "does not validate the full Sentinel architecture."

**Does it cite D&K/Hägg?** **NO — independently confirmed this session.** Full reference list scanned: Open Floor Protocol, tuple spaces, prompt-injection threat surveys, NIST AI RMF, SAIF, A2A — zero classical MAS (no Dellarocas, Klein, Hägg, no exception-handling lineage). A11's claim re-verified.
**Occupies:** the *word* "sentinel" and the *architecture sketch* (monitor + coordinator + quarantine) for LLM MAS security — re-invented with no classical citation. No measured containment/recovery effect, no cost, no propagation metric, no scarcity.
**Action:** one disambiguation sentence (Dellarocas–Klein sentinel *services* for exception handling vs this security-monitoring sense vs SentinelAgent 2505.24201 anomaly detection vs CtC's SENTINEL mediator). The transfer-test framing survives but is thinner: the mechanism has been re-invented by name; what remains unclaimed is testing the classical *predictions* (cost inflation, scarcity sign reversal).

## 5. Memory Poisoning Propagation and Repair — DOI 10.20944/preprints202602.1188.v1 (14 Feb 2026) — **ABSTRACT VERIFIED (Crossref full abstract); full text INACCESSIBLE**

**Authors:** Liu, Xu, Ma, Xu, Qiu. preprints.org.
**Access attempt:** preprints.org manuscript page and /download both return bot-wall/403 from this host (Anubis-style protection). Not indexed by S2 (A11). Crossref carries the full abstract including method and numbers — re-verified verbatim this session.

**Method (from abstract):** Evidence graph over memory source credibility + content consistency to validate newly added memories; contrastive-learning model to identify anomalous "command-induced" memories; on detection, propagation suppressed via **isolation, rewriting, and conflict resolution**.
**Experiments (from abstract):** 60 collaborative tasks, ~210,000 memory records, 12,000 injected poisoned samples; detection **AUC 0.94**; misbehavior rate **15.6% → 2.3%**; **cross-agent propagation −78.1%** on average; "minimal impact on overall task efficiency."

**Occupies:** memory-boundary fault propagation + containment + repair + utility-preservation claim in collaborative MAS — kills any "memory boundary is unoccupied" wedge (confirms A11 N3). Adversarial (poisoning) frame; no organizational semantics; no cost vector beyond the "minimal impact" claim; no scarcity.
**Caveats for the candidate:** non-peer-reviewed preprint; abstract-level only for everyone (full text effectively inaccessible); numbers unverifiable. Cite as preprint with those flags. The −78.1% propagation-reduction-with-minimal-cost claim is a direct prior-art data point *against* H2's cost clause at the memory boundary — the candidate should be ready to explain why organizational containment differs.

## 6. ResMAS — arXiv:2601.04694 (v1, 8 Jan 2026) — **FULL TEXT VERIFIED**

**Authors:** Liu, Liu, Shao, Wang, Shao, Jin, Xu — Tsinghua (EE, BNRist) + Huawei Noah's Ark. Code: github.com/tsinghua-fib-lab/ResMAS.

**Setting/fault model:** Multi-agent *debate* framework (Du et al. 2023 / mixture-of-agents): directed communication graph, T discussion rounds, answer aggregation. Perturbation = **random agent failure**: each agent independently emits a random response with probability p per round (p ∈ {0,0.2,...,1}). Resilience metric R(G) = normalized area under the accuracy-vs-p curve. **No tools, no stateful environment, no recovery mechanism, no adversarial semantics.**

**Is structure an IV or an optimization target?** **Optimization target — with a thin motivational IV-flavored prelude.** The prelude: 30 random graphs varying agent/edge counts on Chess (resilience rises with agents and links), plus a **two-topology case study** (hierarchical > centralized resilience; prompt refinement helps). The contribution proper is design-time optimization: GNN reward model predicts per-problem correctness under error rates (0.86 test accuracy); GRPO-fine-tuned Qwen2.5-7B generates topologies under node/edge constraints; topology-aware prompt optimization from positive/negative neighbor-influence examples.
**Experiments:** MMLU-Pro, MATH-L5, Chess; baselines G-Designer, OPRO, TextGrad, GPTSwarm; constraints 10/15/20 nodes × 10–60 edges; backbone Qwen2.5-32B-Instruct; generalization to HumanEval and GPT-3.5/4o-mini; ablations remove each stage. Node/edge constraints are the only "resource" notion — a *design constraint on graph size*, not a runtime scarcity regime.

**Occupies:** the nearest cell to H1 found anywhere — "communication topology significantly influences MAS resilience under agent failures," including a hierarchical-vs-centralized data point. **Does NOT occupy:** structure as a measured IV for propagation/recovery *cost* (their structural evidence is motivational, not the contribution); delegation depth or authority; tool execution; recovery; budget regimes; sign reversal.
**Action:** must-cite and differentiate design-time optimization vs measurement; note their hierarchical>centralized case study cuts *toward* H1's plausibility (and slightly against any claim that topology effects on resilience are unstudied — the broad claim is dead; only organizational-construct + cost-vector + propagation-measurement specificity survives).

## 7. Resilient Consensus in Agentic AI — arXiv:2606.15024 (v1, 12 Jun 2026) — **FULL TEXT VERIFIED**

**Authors:** S. C. Anand & G. J. Pappas (UPenn). cs.MA + eess.SY.

**Classical theory transferred:** Byzantine agreement/consensus — Pease–Shostak–Lamport **N ≥ 3B+1** (complete graphs); Dolev 1982 directed-graph condition (N ≥ 3B+1 ∧ B < κ/2); Dolev et al. 1986 approximate agreement → **global MSR-type filter** (trim B smallest + B largest); Vaidya et al. 2012 **local MSR-type filter** for arbitrary digraphs with the {F,L,C,R} partition condition (verified exhaustively: holds to B=4, fails at B=5 on their graph).
**How:** "Byzantine consensus game": scalar integer agreement (0–50), H=15 honest + B Byzantine **prompted** agents (Llama-3.2-3B-Instruct; Byzantine agents prompted to coordinate HIGH/LOW splitting); synchronous rounds; Markovian information; 30 trials (10 in ablations); Wilson CIs.
**Findings:** prompted LLM agents fail to reach consensus **well inside the N ≥ 3B+1 safe region** (persists across temperature 0.3–1.0 and horizons); global MSR filter restores ≈100% consensus on complete graphs (even beyond the bound — their adversary pushes extremes, which trimming removes by construction; they acknowledge an interior-value adversary would evade); local MSR filter on the general graph adds little because the dense topology already provides robustness — **"the benefit of filtering depends on the robustness the topology already provides."** Misspecification ablation: f=6 with B∈{0,2,4} still 100%.

**Occupies:** the "classical-theory transfer test on LLM agents" genre *explicitly by name*, in the fault-tolerance-adjacent domain (Byzantine consensus), including a topology-moderated containment-benefit result. This is the strongest existing occupant of the generic framing.
**Does NOT occupy:** fault *handling* theory (Dellarocas–Klein sentinels/exception handling, Kota reorganization — different canon: consensus filters vs organizational fault handling); tool execution; tasks (integer agreement); recovery cost; scarcity (no resource variable at all); organizations.
**Action:** the candidate's framing claim must be scoped to *fault-handling* transfer (already decided in Stage 1 — re-confirmed here with full text). Also cite it as the template a hostile reviewer will use: "transfer tests of classical resilience theory to LLM agents already exist; what is new here?" Answer must be: the D&K/Kota fault-handling canon (citation-disconnected per A12), organizational structure, cost vectors, and the scarcity regime.

## 8. How Much Coordination Gain Is Real? — arXiv:2606.20695 (v1, 15 Jun 2026) — **FULL TEXT VERIFIED**

**Authors:** Kaliyev (UT Austin) & Maryanskyy (Uber). cs.MA.

**Method:** Paired noise-floor protocol: two coordination protocols whose API inputs are **configuration-equivalent at trial 0** (matched by code inspection + SHA-256 byte audit) should produce zero systematic paired gap; measure the actual gap distribution. Substrate: ET-MCP (task-scoped negative-knowledge store, MCP 2026-07-28 conformant). Model: **Claude Haiku 4.5** on **tau²-bench retail**, T=0, **n=100 tasks, two seeds** (n=100 × 2 trials per protocol = 200 trials/protocol); robustness checks on tau² airline n=30 and Sonnet retail n=30.

**Results (the noise floor, confirmed):** clean configuration-equivalent contrast (no_coord vs intercept, both inert at trial 0): **+10pp and 0pp** across the two seeds; pooled **+5pp, Wilson CI [−2, +12]**, n.s. Largest single-seed contrast **+18pp** (pull vs intercept, p_corr=0.012) **did not reproduce** at seed 2 (−3pp, p_corr=1.0). No trial-0 contrast survives Bonferroni. **Envelope of observed paired gaps: [−3, +18]pp; pooled upper Wilson CI ≲15pp.** **7 of 10** recent coordination papers report headline effects below this floor (1 more inside the envelope). Coordination-active subsets contain only **n=8–17 informative pairs after ties** — underpowered for medium effects. Candidate readers (pull/intercept) do not improve trial-1 recovery on Haiku 4.5. Defines **coordination-active pass^k** as minimum reporting protocol; **Sonnet n≥250 retail pre-registered** as follow-up.

**Assessment of the Stage-1 claim ("±12–15pp at n=100"):** **CONFIRMED, with a correction**: the floor is *asymmetric* — pooled CI [−2,+12], upper Wilson ≲15pp, but the single-seed envelope reaches **+18pp**. The safe statement for the candidate's power analysis: "at n=100/cell on tau²-bench retail, paired noise alone produces apparent effects up to +15–18pp; binary contrasts need n≳250/cell (their pre-registered target) or continuous/within-task designs."
**Occupies:** multi-agent protocol experimentation on the candidate's planned Workflow-1 environment (colonization signal, though coordination not faults); the statistical-power argument against any ±10pp SESOI plan at n=100 on tau²-retail.
**Action:** cite in the evaluation-design section; adopt coordination-active pass^k-style reporting; set n from this floor, not from convention.

## 9. The two "Backfire" papers — **ABSTRACT VERIFIED** (arXiv abs pages)

**9a. Alignment Backfire — arXiv:2603.04904 (v1, 5 Mar 2026), Fukui. 89 pp.**
Four **preregistered** studies, **1,584 multi-agent simulations, 16 languages, 3 model families** (Llama 3.3 70B, GPT-4o-mini, Qwen3-Next-80B). Study 1 (N=150): more alignment-instructed agents reduce collective pathology in English (g=−1.844) but **amplify it in Japanese (g=+0.771)** — the "alignment backfire" directional reversal. Study 2 (N=1,174): alignment-induced dissociation near-universal (15/16 languages); pathology bifurcates along cultural-linguistic lines (Power Distance r=0.474). Study 3 (N=180): individuation countermeasure is **iatrogenic** (individuated agents become the primary pathology source, DI=+1.120). Study 4 (N=80): English safety model-general, Japanese backfire model-specific.
**What kind of backfire:** *safety-intervention sign reversal moderated by language/culture*, framed via risk homeostasis and iatrogenesis. **Not** resource scarcity, **not** tool faults, **not** containment cost. Setting is simulated multi-agent social interaction (pathology/dissociation metrics), not tool-executing organizations.
**Occupies:** "interventions in LLM MAS can directionally backfire, preregistered, large-N" — the strongest preregistered LLM-MAS backfire precedent. A reviewer will cite it to call H3's *pattern* known. Differentiator: moderator (language vs resource regime), domain (alignment vs fault containment), and mechanism.

**9b. Feedback That Backfires — arXiv:2608.23651 (v1, 24 Aug 2026), Gumaan. 25 pp, artifacts released.**
**Method:** corrective gain of a failure record = Δ log-probability of re-emitting the just-failed action. **6 instruction-tuned checkpoints, 135M–1.7B, 4 families**; simulated tool calling + MBPP repair; counterfactual pairing of identical calls with failure/success/neutral messages; CPU-only.
**Results:** corrective gain **negative for every model** (≈−1.03 nats/action-token; 2.8× odds; holds on 90–100% of items); repeat probability 0.06→0.54; greedy decoding reproduces the failed call token-for-token on 19% of items post-failure vs 0% pre. Surface form of the failed call accounts for **83%** of the damage. Remedies: runtime-generated failure description removes 76% of the inversion at no token cost; decoder-level unreachability works; "do not repeat" instruction does nothing; **delete-and-retry-from-clean-context — the standard context-contamination prescription — is the WORST harness measured** (restores the failure-producing context).
**What kind of backfire:** *harness/recovery-prescription backfire* — a mechanistic small-model result about failure records inducing repetition. **Not** scarcity, **not** multi-agent, **not** organizational containment.
**Occupies:** "a standard recovery prescription experimentally backfires" — direct precedent that recovery mechanisms can be net-negative, at the single-agent harness level. Threatens any candidate framing of "we first show recovery can hurt"; supports H3's plausibility while occupying the generic claim. Also a design warning: the candidate's retry/rollback arms must control for transcript-context effects.

---

## 10. Consolidated occupation map (what each threat exactly occupies)

| Threat | Verification | Occupies | Does NOT occupy |
|---|---|---|---|
| Outcome Monitors 2608.19303 | FULL TEXT | Single-agent semantic-tool-fault detection + recovery affordances on tau-bench retail/ToolMaze; frozen prespecified protocol; AppWorld null | MAS, propagation across agents, org structure, cost, scarcity |
| Verifier Tax 2603.19328 | FULL TEXT | H2 cost clause *by name* on tau-bench (2.0–2.8× tokens); post-block recovery 21%→0%; horizon dependence | MAS, fault propagation, budget manipulation, sign reversal |
| Sherlock 2511.00330 | FULL TEXT | Cost-optimal verifier placement + speculative execution + rollback on workflow DAGs; verification-cost optimization solved (Microsoft) | Org MAS, structure IV, stateful tools, scarcity regime |
| Sentinel Agents 2509.14956 | FULL TEXT (refs scanned) | "Sentinel" name + monitor/coordinator/quarantine architecture sketch for LLM MAS; zero classical citations | Any measured containment/recovery effect (detection-only PoC, quarantine disabled, no FP) |
| Memory-Poisoning Repair (preprints 1188.v1) | ABSTRACT (Crossref; full text bot-walled) | Memory-boundary propagation + isolation/rewriting repair + −78.1% propagation + "minimal cost" claim | Org semantics, cost vector, scarcity; peer review; verifiable numbers |
| ResMAS 2601.04694 | FULL TEXT | Topology→resilience as *optimization target*; motivational hierarchical>centralized case study; random-failure resilience metric | Structure as measured IV for propagation/recovery cost; tools; recovery; budget regimes |
| Resilient Consensus 2606.15024 | FULL TEXT | Classical-transfer-test genre in Byzantine consensus (PSL/Dolev/Vaidya MSR filters); topology-moderated filter benefit | Fault-*handling* canon (D&K/Kota); tools; tasks; cost; scarcity; orgs |
| Noise-floor 2606.20695 | FULL TEXT | tau²-retail paired noise floor (envelope [−3,+18]pp @ n=100); coordination-active pass^k protocol; colonizes Workflow-1 methodologically | Faults; containment; recovery |
| Alignment Backfire 2603.04904 | ABSTRACT | Preregistered directional reversal of interventions in LLM MAS (language-moderated) | Scarcity, tools, containment cost |
| Feedback That Backfires 2608.23651 | ABSTRACT | Standard recovery prescription (delete-and-retry) is worst measured harness; small-model mechanism | Scarcity, MAS, orgs |

## 11. Net assessment against H1/H2/H3

- **H1:** Unchanged from Stage 1 — survives. ResMAS full text confirms structure-as-target, not structure-as-IV-with-costs. No new occupant of delegation-depth × propagation/recovery-cost.
- **H2:** Cost clause is now *triply* occupied at full-text level (Verifier Tax 2.0–2.8× on tau-bench; Sherlock placement economics; BRA-Audit Pareto from Stage 1). H2 cannot be a headline claim; it is a design dimension of the H3 factorial.
- **H3:** Still no exact occupant. The two new "backfire" papers are different moderators/mechanisms (language; harness context), and both *strengthen plausibility* while shrinking surprise. Combined with Stage-1's SHO opposite-sign finding, the defensible form remains **H3′: budget-unaware containment backfires under scarcity; budget-aware containment does not** — and the candidate must pre-register the interaction, not the main effect.
- **Power analysis:** the tau²-retail floor is confirmed and is the single most *operationally* damaging verification here: n=100/cell binary contrasts on tau²-retail cannot detect <15–18pp effects. Budget n≳250/cell (their own pre-registered target) or switch to paired/continuous designs.

## 12. Verification log

- FULL TEXT (arXiv HTML, this session): 2608.19303, 2603.19328, 2511.00330, 2509.14956 (incl. full reference list scan for Dellarocas/Klein/Hägg — zero hits), 2601.04694 (incl. references), 2606.15024 (incl. references), 2606.20695.
- ABSTRACT VERIFIED: 2603.04904, 2608.23651 (arXiv abs pages); 10.20944/preprints202602.1188.v1 (Crossref full abstract via API, re-verified verbatim).
- Blocked: preprints.org (bot wall, 403 on page and /download). No other channel failures this session.
- Stage-1 reports read first: A1, A3, A8, A9, A11, A12. No Stage-1 classification reversed; sharpenings recorded in §0 (Outcome Monitors AppWorld null + protocol strength; noise-floor asymmetry +18pp; ResMAS structure evidence thinner than implied).
