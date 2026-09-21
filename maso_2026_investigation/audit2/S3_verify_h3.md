# S3-VERIFY-H3 — Full-text verification of the three papers that decide H3's fate

**Date:** 2026-09-21
**Mission:** Upgrade the three H3-deciding papers from ABSTRACT ONLY to full-text where possible, and fix exactly which cell of the H3 claim each occupies. H3 = "containment/recovery mechanisms help under resource abundance but hurt under scarcity (sign reversal)" in tool-executing LLM multi-agent organizations.
**Prior reports read first:** audit2/A4_scarcity_redteam.md, A6_distsys.md, A9_adversarial_reviewer.md, A2_org_structure.md; reports/CtC_fulltext_verification.md (skimmed for method).

---

## 0. Bottom line

All three papers are now **FULL TEXT VERIFIED** — two via arXiv PDFs, one via the authors' own companion repository (SSRN itself is Cloudflare-walled to all automated access). The verification **changes the H3 threat assessment in both directions**:

- **Xiang (SSRN 7348298) is real and does contain the sign reversal — but its mechanism is degenerate, not economic.** The gate's harm at zero budget is mechanical (empty audited set → forced abstention/guessing), not "containment consumes the scarce resource." The causal direction is *opposite* to H3's: in Xiang, scarcity starves the gate's input; in H3, the containment mechanism spends the scarce resource. The headline pattern ("gate's effect changes sign with the verification budget," on LLM agents, DiD = +0.456) is nonetheless **published and citable**, and a hostile reviewer will not read the mechanism footnote before pattern-matching.
- **Mehan (SSRN 6313332 = arXiv 2608.25403) is NOT what the inventory says in two respects:** it has **two authors** (A6 said single), and its retry result is **not** an abundance→scarcity crossover — standard retry is worse than no-retry in *all three* simulated scenarios (worst under correlated failure), because injected faults are sustained, so retries mostly cannot succeed. It is a congestion/correlated-failure result with no LLM content whatsoever.
- **Self-Healing Orchestrators (2606.01416) is confirmed numerically but its "opposite-sign" status needs reframing:** the budget sweep has **no no-recovery arm**, and the budget is a *recovery-attempt allowance*, decoupled from task resources. It shows a better recovery *policy* dominates more at tighter allowances — it never tests whether recovery itself turns harmful under scarcity. It is anti-H3 only in the weak sense (the crossover was looked for in the adjacent design space and did not appear).

**Net for H3:** the "first sign reversal of a containment/verification mechanism under budget scarcity on LLM agents" headline is **occupied by Xiang** (single-agent, accuracy DV, degenerate mechanism). What survives for the candidate is narrower than Stage 1 thought in one way (the phenomenon on LLM substrate is published) and stronger in another (Xiang's mechanism is distinguishable and its authors themselves flag the effect size as probably overestimated; nobody — including Xiang — has propagation, organization, tool execution, or a containment-spends-resource mechanism).

---

## 1. Xiang, "When Do Audited Action Gates Help? The Cost and Failure Conditions of Epistemic Strictness in LLM Agents" (SSRN 2026, DOI 10.2139/ssrn.7348298)

### Verification status: FULL TEXT VERIFIED (via companion repository)

- SSRN abstract page and PDF delivery are behind a Cloudflare challenge ("Just a moment...") for curl, FetchURL, and the r.jina.ai proxy — **SSRN itself is inaccessible to automated retrieval** (raw: `raw_s3/ssrn_7348298_abs.html`, `raw_s3/jina_xiang.txt`).
- Crossref metadata confirms: title, single author **Rong Xiang** ("Independent researcher"), type `posted-content`, publisher Elsevier BV, created 2026-08-27; full 2,051-char abstract retrieved (raw: `raw_s3/cr_xiang.json`). No PDF link in Crossref; no arXiv mirror (arXiv full-text search for "epistemic strictness" and "Audited Action Gates": zero results, 21 Sep 2026); no OpenReview mirror; no DataCite record; Semantic Scholar has no record of the DOI at all.
- **Full text obtained from the authors' companion repository** `github.com/aiegisafety/fault-world` (found via DuckDuckGo): `paper/main.tex` (530 lines, complete LaTeX source) and `paper/main.pdf` (compiled, 10 pp., matching the SSRN "10 Pages Posted: 27 Aug 2026" record), plus per-experiment lab notes (`notes/E0–E7`, `PLAN-REVISIONS.md`) and all per-run data. Raw copies: `raw_s3/xiang_main.tex`, `raw_s3/xiang_main.pdf`, `raw_s3/xiang_E5.md`, `raw_s3/xiang_planrev.md`. This is the paper itself, not a summary — verification level FULL TEXT.

### Answers to the assigned questions (all from the full text)

| Question | Answer |
|---|---|
| Single-agent or multi-agent? | **Single-agent, explicitly.** "These lines concern propagation across steps and agents; the present paper concerns the genesis of spurious belief within a *single agent*" (Related work). Each run = one model instance interacting with the environment over 3 episodes. |
| What is the "verification budget"? | **A count of interventions (experiments) per run**: S2 swept over 0/3/6/12/21. Each intervention forces one component active/inactive and runs the synthetic machine 20 times, returning symptom counts. NOT tokens, NOT API calls-as-currency, NOT wall-clock time. It is a per-run allowance of epistemic actions. |
| Sign reversal measured on accuracy or propagation? | **Task accuracy.** DV is downstream diagnostic accuracy ("which component to repair"; 30-case protocol for the main effect, older 8-case protocol for the interaction). There is no propagation measurement anywhere in the paper — no inter-agent spread, no cascade, no blast radius. |
| Tool-executing? | **No, in the MASO sense.** The agent executes *interventions* in a synthetic causal-discovery environment ("Fault World": 6 components, 8 symptoms, K=3 true rules, M=4 confounded spurious pairs). These are environment actions, not external tool calls; no tool-use benchmark, no API tools, no tau-bench-style execution. |
| Pre-registered? | **Partially — and the sign reversal is NOT one of the three pre-registered hypotheses.** Pre-registered: T1 (strictness trade-off), T2 (gate mechanism), T3 (exploration collapse — refuted). The budget×gate reversal was however a **pre-committed falsification prediction** of T2's mechanism, tested in dedicated experiment E5 (lab note dated 2026-08-25: "if the gate's benefit really comes from the audited set, then at budget 0 the audited set is necessarily empty and the gate should conversely harm performance — a prediction that can falsify T2's mechanistic explanation"). So: not post-hoc fishing, but also not among the registered three. Holm correction applied within a 5-contrast family. |
| The 9 models and 1,330 runs? | Models: `qwen3.8-27b`, `glm-4.5-air`, `glm-5.2`, `kimi-k3`, `qwen3.7-flash-2026-07-15`, `qwen3.7-max-2026-06-08`, `qwen3.7-plus`, `qwen3.7-plus-2026-05-26`, `deepseek-v4-flash-0731` — **all mid-sized/inexpensive; no frontier models; chain-of-thought disabled throughout** (`enable_thinking=false`, "an untested simplification"). 1,330 completed runs across 18 experiment cells; model set differs between experiments due to free-quota availability; results not pooled across experiments. |
| Organizational structure? | **None.** No roles, no delegation, no hierarchy, no communication topology. |

### The sign reversal itself — exact numbers and mechanism (Table in §5.4 / E5 note)

Measured with **two models** (deepseek-v4-flash-0731, qwen3.7-plus), 20 reps/cell, budget {0, 6, 21} × gate {OFF, AUDIT}, strictness fixed L1, shared world seeds, **8-case protocol** (the older, smaller one):

- Gate effect at budget 0: **−0.315 [−0.452, −0.178]**, Holm p = .0017
- Gate effect at budget 6: **+0.140 [+0.054, +0.227]**, p = .0080
- Gate effect at budget 21: +0.081 [+0.002, +0.163], p = .063 (marginal; OFF side near ceiling)
- DiD 0→6: **+0.456 [+0.297, +0.625]**, p = .0017; DiD 0→21: +0.320, p = .0017

**Mechanism (verbatim from the paper):** "With zero budget the audited set is necessarily empty, so the gate strips the agent of every usable rule; one model falls to 0.28 accuracy." The E5 lab note is blunter: at budget 0 the AUDIT arm "can only guess" (qwen3.7-plus: 0.82 OFF → 0.28 AUDIT). **The gate does not consume the scarce resource; the scarce resource provisions the gate.** The harm is forced abstention on an empty whitelist — a design corner — not containment traffic starving the task. Also note the gate's benefit is non-monotone at the top (budget 21 < budget 6) and the authors' own Limitation 5: "the budget-by-gate interaction was measured under the earlier 8-case protocol and … its magnitude is probably overestimated."

### Cell of H3 occupied

**Occupied:** "a verification/containment-style gate on an LLM agent flips from harmful to helpful as a verification-resource budget increases" — measured, published (27 Aug 2026), with paired seeds, Holm correction, and full data release.
**NOT occupied:** multi-agent, organization, propagation, tool execution, containment-*spends*-the-resource mechanism, task-level token/tool/reviewer budgets, any scarcity operationalization where the mechanism itself competes for the resource.
**Corrections to Stage-1 records:** A9's "pre-registered hypotheses with Holm correction" overstates the registration status of finding (iv) (see above). A9/A4's implicit reading that the reversal is an economic scarcity crossover is wrong — it is a vacuity corner. Everything else in A9's R3 (numbers, moderations) checks out against the full text.

---

## 2. Mehan & Saluja, "Retry Amplification in Distributed Systems" (SSRN 2026, DOI 10.2139/ssrn.6313332)

### Verification status: FULL TEXT VERIFIED (arXiv mirror)

- Semantic Scholar's single-paper endpoint reveals an **arXiv mirror: arXiv:2608.25403v1 [cs.SE], 26 Aug 2026** (externalIds link the SSRN DOI and the arXiv ID; CorpusId 291367907). Full PDF fetched and read (raw: `raw_s3/mehan_2608.25403.pdf/.txt`).
- **Correction to A6: two authors — Rishabh Mehan ("Software Engineering Research") and Jasmit Kaur Saluja ("Independent Researcher")** — not "single author." SSRN record + arXiv record agree.

### Setting, method, LLM content

- **Setting: distributed systems / microservices. Zero LLM or agent content** — no LLM appears anywhere in the paper; references are Metcalfe-Boggs, Kleinrock, Nygard, Newman, Burns, Gunawi, Welsh-Culler, Zhou (WeChat overload), Envoy, Linkerd.
- **Method, three parts:** (i) analytical model — Retry Amplification Factor RAF = (1−p^{n+1})/(1−p) per tier, compounding multiplicatively down a call chain (bound 6.59× at depth 3, p=0.5, n=3); (ii) empirical static analysis of 200 GitHub Python microservice repos (explicit retry logic detected in 11.5%, true prevalence est. ~41% after a 33.3% false-negative audit; 60.9% of detected projects have ≥1 no-backoff config; exactly 1 of 113 production configurations uses jitter); (iii) discrete-event simulation: 5-tier linear chain (API→Auth→Catalog→Inventory→Database), 1000 RPS capacity, 500 RPS base load (50% utilization), n=100 trials per strategy per scenario.

### The "25% worse" claim — precise form

Table III (mean success rate, n=100): **Standard Retry ranks last in every scenario, below No Retry** — S1 (single-tier 50% failure): 61.0% vs 71.7%; S2 (cascading slowdown): 55.1% vs 65.4%; S3 (correlated 60% failure across tiers 3–5): **41.5% vs 55.4%** ("a relative degradation of 25%"). Mechanism (§VII.C): queue slots are the scarce resource; retries compete with fresh traffic; each attempt burns processing time; at S3 failure rates "a large share of retries could not have succeeded, so the capacity they consumed yielded nothing."

**Two mismatches with the H3 cell that Stage 1 did not record:**
1. **There is no abundance condition in which retry helps.** SR is worse than NR in all three scenarios — because the injected faults are sustained/correlated, not transient. This is "naive retry is counterproductive under sustained failure," not "recovery helps under abundance and hurts under scarcity." The sign-reversal-along-a-scarcity-axis pattern is NOT what this paper measures; there is no budget/utilization sweep of the reversal at all (utilization is fixed at 50%; what varies is the failure scenario).
2. **Budgeted recovery does NOT backfire.** Adaptive Retry Budgeting (ARB) and Circuit Breaker both hold RAF ≈ 1.01 and finish within ~1pp of the No-Retry baseline in every scenario. The paper's own containment mechanism is safe under stress — if anything this is weakly anti-H3 within distsys.

### Cell of H3 occupied

Classical distsys congestion backfire (retry traffic consumes queue capacity under correlated failure). NOT occupied: LLM, agents, organization, propagation of semantic faults, a true abundance→scarcity crossover, any containment mechanism that itself turns harmful along a budget axis. Usable by a reviewer as "the pattern is textbook in distsys" ammunition; NOT usable as "already demonstrated for LLM agents."

---

## 3. Babu & Agrawal, "Self-Healing Agentic Orchestrators for Reliable Tool-Augmented Large Language Model Systems" (arXiv:2606.01416v1, 31 May 2026)

### Verification status: FULL TEXT VERIFIED (arXiv PDF, 11 pp.)

Raw: `raw_s3/sho_2606.01416.pdf/.txt`. Authors: Rahul Suresh Babu (Independent Researcher; rahulsb@bu.edu), Adarsh Agrawal (Senior Member, IEEE; adagrawal@cs.stonybrook.edu). arXiv preprint; no peer-reviewed venue indicated.

### The budget sweep — exact confirmation

- **Table 9 confirmed verbatim:** task success under matched recovery budgets — budget 1: self-healing **94.0%**, retry-only **85.3%**, full replanning **88.2%**; budget 2: 97.8/93.8/94.3; budget 3: 99.2/96.7/97.8; budget 5: 100.0/99.2/99.3. At λ=0.4, budget 1: 90.3 vs 79.0/81.7. Design: 100 tasks × 3 methods × 4 budgets {1,2,3,5} × 2 fault intensities λ∈{0.2,0.4} × 3 seeds = 7,200 executions, paired fault schedules.
- **Exact budget definition (§3.3, §5.2):** the recovery budget is a tuple of counters — remaining retry budget, replanning budget, tool-substitution budget, model-escalation budget, latency budget, cost budget. In the sweep, "budget" operationalizes as **the number of recovery attempts/opportunities allowed per task**, matched across methods. It is a recovery-allowance cap, **not** a task-level token/time/compute budget shared with the work itself.
- **Is the comparison budget-aware vs budget-unaware recovery? NO.** All three arms are capped at the same allowance; what differs is the recovery *policy* (failure-class-targeted + verifier-guided vs blind retry vs discard-and-replan). "Budget-aware" in this paper means "respects the cap and spends attempts selectively," not an arm contrast. The ablation's "relaxed recovery budget" variant (100.0% success) is the only budget-size contrast within self-healing, and it is monotone: more attempts → more success.

### Why this is NOT an H3 test (three decouplings)

1. **No no-recovery arm in the sweep.** Static workflow (the no-recovery baseline: 70.1% overall, 0.0% on the faulted subset) is excluded from the budget experiment. So the sweep cannot show a sign reversal of *recovery itself*; it only ranks recovery policies. The "largest gap at the tightest budget" is a policy-efficiency gap (94.0 vs 85.3), not "recovery helps most vs nothing when scarce."
2. **Recovery does not consume the task's resource.** The recovery allowance is decoupled from task execution resources; there is no channel by which recovery spending starves the task (H3's mechanism). Cost is reported as a call-count proxy, and self-healing's cost (3.13 at budget 1) sits between retry-only (2.15) and replanning (3.45) — no runaway.
3. **No organization, no propagation.** Single orchestrator over a single tool-augmented pipeline; faults are per-tool-step injected runtime faults plus a separate semantic silent-failure setting; the controlled benchmark "abstracts model behavior" (deterministic tools), and the live-model validation is compact (90+60+180 executions) and saturates at 100% success.

### Cell of H3 occupied

"Recovery-policy quality matters most when recovery allowances are tight, in a single-orchestrator tool-augmented LLM system." It is the nearest *adjacent* experiment and it is opposite-signed only against the strong reading of H3; against the precise H3 (containment spending the task's scarce resource flips its sign) it is **silent** — the design cannot express the crossover. Stage-1's use of it as "anti-H3 evidence" stands, but the correct citation is "looked-for-and-not-found in the adjacent design space," not "demonstrated the opposite under scarcity."

---

## 4. Consolidated H3 occupation map after full-text verification

| Sub-claim | Status | Deciding evidence (verification level) |
|---|---|---|
| Sign reversal of a containment/verification mechanism along a resource budget, **on LLM agents**, measured | **OCCUPIED** | Xiang SSRN 7348298 (FULL TEXT): gate × intervention-budget, −0.315 → +0.140, DiD +0.456, on diagnostic accuracy |
| …with the mechanism "containment consumes the scarce task resource" | **UNOCCUPIED everywhere** | Xiang's mechanism is empty-whitelist vacuity (opposite causal direction); Mehan is congestion in non-LLM distsys with no abundance arm; SHO decouples recovery allowance from task resources |
| …on propagation / organizational multi-agent structure | **UNOCCUPIED** | All three papers are single-agent/single-orchestrator or non-LLM; Xiang explicitly disclaims propagation |
| …on tool-executing agents | **UNOCCUPIED** | Xiang: synthetic intervention environment; SHO: deterministic local tools, model abstracted; Mehan: microservices |
| "Recovery helps most at the tightest budget" (anti-H3 adjacent) | **OCCUPIED (weak form only)** | SHO Table 9 (FULL TEXT): policy-efficiency gap widest at budget 1; no no-recovery arm |

## 5. Corrections to Stage-1 records (for the orchestrator)

1. **A6:** Mehan is **two authors** (Mehan & Saluja), and the "25% worse" is not a scarcity crossover — SR < NR in all scenarios; ARB/CB match NR. Downgrade Mehan from "most on-the-nose demonstrated sign reversal" to "congestion backfire under sustained correlated failure, no abundance arm."
2. **A9 (R3):** Xiang's finding (iv) was **not one of the three pre-registered hypotheses** (T1–T3); it was a pre-committed falsification test of T2's mechanism (E5, 2026-08-25). Also: interaction measured on 2 models, 8-case protocol, authors flag probable magnitude overestimation; CoT disabled; mid-sized models only. The claim "pre-registered, 1,330 runs, 9 models" is true of the paper but not of the reversal cell specifically (234 runs, 2 models).
3. **A4/A9:** SHO's sweep has **no no-recovery arm** and its budget is a recovery-attempt allowance — reframe from "opposite-sign budget sweep" to "policy-efficiency gap, H3-silent."
4. **A9 §5 (unexpected finding) stands and strengthens:** Xiang's capability moderation (+0.31 below baseline 0.60 vs +0.01 at 0.80–0.95) is confirmed in full text with the split-half design — the capability×containment confound warning for the candidate's design is real.

## 6. Implications for the candidate (hostile)

- **H3's headline must not be "first sign reversal of containment under scarcity on LLM agents"** — Xiang published exactly that sentence's shape on 27 Aug 2026, with open data. The defensible claim is the conjunction: *organizational* (multi-agent, propagating faults) × *tool-executing* × *containment-spends-the-resource mechanism* × sign reversal. Every element is currently unoccupied; the headline pattern is not.
- **The candidate can and should distinguish Xiang's mechanism explicitly**: Xiang's gate harms because scarcity makes its whitelist empty (vacuity); H3's claim is that containment's *operation* spends the resource (partition/congestion/redeployment/false-positive quarantine). These make different predictions (e.g., H3 predicts harm at *nonzero but tight* budgets with a smooth crossover; Xiang's harm is at exactly zero and disappears once anything is verified). Citing Xiang and drawing this distinction pre-empts the pattern-match review; ignoring it invites a "scooped" review.
- **Xiang's own limitations hand the candidate rhetorical room**: 2 models, 8-case protocol, self-flagged overestimated magnitude, CoT disabled, mid-sized models, synthetic single-agent environment. A reviewer citing Xiang as decisive must reckon with those.
- **Mehan should be cited as textbook-distsys context, not feared** — but cited accurately (it has no abundance arm; its budgeted retry does not backfire).

## 7. Verification ledger (this session)

- **FULL TEXT:** Xiang SSRN 7348298 via `github.com/aiegisafety/fault-world` `paper/main.tex` + `main.pdf` + lab notes E5/PLAN-REVISIONS (SSRN Cloudflare-blocked; no arXiv/OpenReview/DataCite/S2 mirror exists); Mehan & Saluja via arXiv:2608.25403 PDF (SSRN↔arXiv identity via S2 externalIds, CorpusId 291367907); SHO via arXiv:2606.01416 PDF (11 pp.).
- **METADATA:** Crossref 10.2139/ssrn.7348298 (full abstract, author, date); S2 single-paper endpoint for 10.2139/ssrn.6313332.
- **FAILED CHANNELS:** SSRN (Cloudflare, all routes incl. r.jina.ai), S2 search (429), OpenAlex search (paused), arXiv export API (empty responses), Google Scholar (429).
- Raw artifacts: `audit2/raw_s3/` (sho_2606.01416.pdf/.txt, mehan_2608.25403.pdf/.txt, xiang_main.tex/.pdf, xiang_E5.md, xiang_planrev.md, cr_xiang.json, s2_mehan.json, s2_xiang.json, gh_fw_tree.json, ssrn/jina/arxiv-search failure captures).
