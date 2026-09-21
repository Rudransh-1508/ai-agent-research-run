# W2 — Feasibility Reviewer F-B: CAND-3 (AttribContain), CAND-4 (RecoveryCost), CAND-5 (FaultValidity)

**Investigator:** F-B (wave-2 feasibility)
**Date:** 21 September 2026 (deadline: 10 Oct 2026 — 19 days)
**Mission:** For each of CAND-3/4/5: implementation complexity, required artifacts (verified downloadable or not), compute/API cost, experiment count, evaluation difficulty, baseline availability, 19-day statistical feasibility, reproducibility. Rank by feasibility-adjusted payoff.
**Method:** Built on wave-1 reports (F1 feasibility scan, B3 attribution, B5 fault injection, B11 benchmarks, B15 metrics, B16 cost/reliability, B8 escalation, D1/D2 verification reports). All load-bearing artifacts re-verified today against primary pages: GitHub API (authenticated), HuggingFace dataset pages, arXiv abstract/HTML pages. New verifications specific to this report: Who&When repo structure, MAST-Data HF page, AgentFail paper ID + repo contents, TRAIL HF link, LongRCA/StateMAS/Who&When-Pro data-link inspection.

---

## 0. Shared context (from F1, re-used not re-derived)

- Substrate: tau2-bench (sierra-research/tau2-bench, MIT, active — pushed 19 Sep 2026) + LangGraph (MIT, checkpointing = rollback primitive, interrupts = human boundary). Descoped testbed build: **3.5–5 person-weeks** (2 workflows, 6–8 fault types, 3 containment conditions) = 2 people × 19 days with discipline.
- API cost: ~$50–250 per full factorial (~3,240 runs) on GPT-5-mini/DeepSeek class; batch APIs halve this. **Money is non-binding; engineering time is the constraint.**
- Statistics: n=30/cell detects 25–30pp binary differences; n=50/cell detects 20pp; continuous metrics (blast radius, cost) need n=20–30/cell for d≈0.8. Throughput: 3–5k runs = hours at 20–50 parallel workers.
- **All three candidates inherit this testbed.** Marginal cost per candidate is what differs, and that is what this report scores.

---

## 1. CAND-3 "AttribContain" — attribution-accuracy threshold for attribution-guided containment

### 1.1 The decisive feasibility insight
CAND-3's research question ("how accurate must attribution be before attribution-guided containment beats attribution-free containment?") has a structural property that makes it the most experimentally tractable of the three: **under fault injection, attribution ground truth is known by construction.** The experimenter injects fault f at agent a, step s — so a perfect attributor is free. Attribution accuracy then becomes a **controlled independent variable** via synthetic degradation of the oracle (sample the blamed agent/step from a confusion distribution calibrated to published accuracy levels). No external attribution benchmark is needed for the core threshold sweep.

### 1.2 Required artifacts — does CAND-3 need Who&When's dataset/code?
- **Core experiment: NO.** The Who&When *dataset* (HF Kevin355/Who_and_When — verified live today, 184 annotated logs from CaptainAgent/Magentic-One on GAIA/AssistantBench web tasks) is the wrong distribution for organizational workflows and is not needed: injection provides ground truth.
- **Calibration and credibility: YES, code only.** Verified today: `github.com/mingyin1/Agents_Failure_Attribution` (MIT LICENSE file present, 34★, last push Jan 2026) contains `Automated_FA/` with runnable `inference.py` + `evaluate.py` + `Lib/` (the three method families: all-at-once, step-by-step, binary search) and the `Who&When/` dataset dir (Algorithm-Generated + Hand-Crafted). Use it to (a) measure the *actual* accuracy of a real attributor on our organizational traces, anchoring which synthetic accuracy levels are realistic operating points (published range: 14.2% step / 53.5% agent on Who&When; up to ~76% with full observability per TraceElephant 2604.22708; 24.1% root-step on long traces per LongRCA 2608.15242).
- Optional stronger attributor: AgenTracer-8B code at `github.com/bingreeky/AgenTracer` (103★, **no license**, has data/ + MetaGPT/ dirs — usable with caution, cite-only fallback exists).
- Containment mechanisms (targeted quarantine/rollback vs verify-everything/restart-all): built once on the shared testbed; LangGraph checkpointing gives rollback; agent-level message gating gives quarantine. ~1–1.5 pw marginal.

### 1.3 Experiment matrix, cost, statistics
- Main sweep: 2 workflows × 5 accuracy levels (e.g., 15/30/50/70/100%, spanning published 14.2–53.5% and oracle) × 4 containment strategies (targeted-quarantine, targeted-rollback, verify-everything, restart-all) × 30–50 reps ≈ **1,200–2,000 runs** → ~$30–150 mid-tier. Real-attributor validation arm: ~200–400 runs (~$10–30).
- The threshold is the accuracy level where the targeted-containment utility/cost curve crosses the attribution-free curve — a crossing-point estimate with bootstrap CIs. n=30–50/cell is ample because the dependent variables (blast radius fraction, task success, tokens) are continuous or high-base-rate binary.
- **19-day verdict: FEASIBLE** if the testbed is the shared CAND-1 build (days 1–8 shared build; CAND-3-specific mechanism + degradation-sampler work is ~3–4 days, parallelizable; runs fit in days 12–16).

### 1.4 Evaluation difficulty, baselines, reproducibility
- Evaluation: **low difficulty.** Outcomes are instrumented (DB-state divergence for utility, boundary-crossing count for blast radius, tokens for cost). No human judgment, no LLM-judge needed for the primary metrics.
- Baselines: trivially implementable and unambiguous (verify-everything = verifier call per step; restart-all = full checkpoint reset; random-target containment as a sanity floor). The oracle-attribution ceiling is free.
- Reproducibility: **high.** Synthetic degradation is seed-deterministic; all external artifacts MIT or public; the accuracy sweep is exactly reproducible. This is the most reproducible design of the three.
- Risks: (a) reviewers may ask whether the threshold is stable across fault types — mitigate by stratifying the sweep over 2–3 fault classes rather than pooling; (b) the synthetic-confusion model must be shown to match a real attributor's error *structure* (not just marginal accuracy) in the validation arm.

---

## 2. CAND-4 "RecoveryCost" — cost-utility Pareto of containment/recovery mechanisms

### 2.1 Implementation complexity — lowest marginal build of the three
CAND-4 is essentially "the shared testbed's containment-mechanism arm + cost accounting." Marginal work over the CAND-1 build:
- Cost instrumentation: per-mechanism token/tool-call/wall-clock logging (~2–3 days; LangGraph callbacks or LangSmith; token counting is mechanical).
- Metric definitions: cost-of-recovery = E[$ to restore correct execution | fault injected], a direct extension of cost-of-pass (arXiv:2504.13359, verified by B16 — metric machinery is definitional, no code needed); MTTD/MTTR imported from ITBench (2502.05352) definitions.
- Pareto analysis: standard dominance + scatter; no new stats.

### 2.2 The human-escalation arm — the one hard spot
- **A real human study is INFEASIBLE in 19 days** (recruitment, per-cell n≥30, session logistics, payment ethics). Do not plan it.
- Feasible design: **simulated human supervisor** (LLM-based overseer invoked on escalation, with priced latency + an explicit wage assumption per oversight minute), plus a **sensitivity analysis over wage/latency assumptions** (e.g., $0.5–2/min, 30s–5min response). Frame as "priced oversight model," cite GDPval's explicit exclusion of oversight cost (verified by B16) and Oversight-Has-a-Capacity (arXiv:2606.08919, fatigue/flooding) as the model of human limits. This is defensible for a workshop paper and is the honest scoping; a real-human arm is the obvious journal extension.
- tau2-bench's user simulator and LangGraph interrupts provide the technical hook; B8 confirms no prior work prices human escalation against automated containment for propagating faults, so even the simulated version is a verified-gap contribution.

### 2.3 Experiment matrix, cost, statistics
- **Key feasibility advantage: CAND-4 needs zero additional runs beyond the shared containment campaign** — cost is an additional *dependent variable* logged on the same runs, not an additional factor. If run standalone: 2 workflows × 4–5 mechanisms (retry, verifier-gate, quarantine, rollback, human-escalation-sim) × 4–6 fault types × 30 reps ≈ 1,440–1,800 runs ≈ $35–140 mid-tier.
- Statistics: cost differences between mechanisms are typically large (verify-everything vs targeted will differ by multiples, not percent) — n=30/cell is overpowered; Pareto membership is robust.
- **19-day verdict: MOST FEASIBLE of the three.** Marginal effort ~1–1.5 pw on top of the shared build.

### 2.4 Evaluation difficulty, baselines, reproducibility
- Evaluation: **lowest difficulty** — all metrics objective (tokens, $, wall-clock, simulated-minutes, DB-state utility). No judges.
- Baselines: no-containment, retry (both free); cost-of-pass as the metric parent; AIOpsLab/ITBench as domain-adjacent comparators to cite (B16 verified they measure episode cost/MTTR but not mechanism-comparative containment cost).
- Reproducibility: high for automated arms; the simulated-human arm is reproducible given the overseer prompt + pricing constants, which must be released. Wage assumptions are the soft spot — report the sensitivity sweep, not a point estimate.
- Risks: (a) standalone thinness — "add a cost axis" reads incremental unless the human-vs-automated pricing result leads; (b) cost numbers are model-price-dependent — mitigate by reporting tokens/tool-calls alongside $ and fixing a dated price sheet.

---

## 3. CAND-5 "FaultValidity" — do injected faults predict organic failure?

### 3.1 Required artifacts — organic corpora, verified today
| Corpus | Status (verified 21 Sep 2026) | Fit |
|---|---|---|
| **MAST-Data** | **Downloadable.** HF `mcemri/MAD` page live: 1,642 traces, 7 frameworks (AG2, MetaGPT, ChatDev, Magentic, AppWorld, HyperAgent, OpenManus), 8 benchmarks, 5 LLMs, binary annotations for the 14 MAST modes; `MAD_full_dataset.json` + `MAD_human_labelled_dataset.json` (only 19 traces). Code repo `multi-agent-systems-failure-taxonomy/MAST` (415★). | The organic-failure backbone. **Caveats: annotations are LLM-judge-produced, not human; tasks are coding/math/GAIA — not organizational workflows.** |
| **AgentFail** | Paper verified: **arXiv:2509.23735** (v1 Sep 2025, v2 Feb 2026; Ma, Xie, Wang, Wang, Wu, Li, Wang), 307 real failure cases from Dify/Coze low-code platforms. Dataset repo `github.com/Jenna-Ma/JaWs-AgentFail` (8★, **NO LICENSE**) — README says "dataset coming soon," but the `coze/dataset`, `dify/output_fail` (JSON + labels), and `n8n/*_traces` directories **do contain trace JSONs and label files** (directory listings verified). | Closest to organizational-ish workflows. **Yellow flag: ambiguous release status + no license — usable for internal analysis, risky to redistribute or lean on as sole organic source.** |
| **TRAIL** | HF `PatronusAI/TRAIL` link verified in arXiv:2505.08638 HTML. 148 human-annotated traces (single+multi-agent). | Small but human-annotated; good validation subsample. |
| **LongRCA** (2608.15242) | Abstract verified: 1,140 failed trajectories, 5 domains, **no injected errors**, human labels, median 145 steps. **No public data link found in HTML v3 — availability UNCONFIRMED.** | Ideal organic corpus if released; do not plan on it. |
| **StateMAS** (2607.29055) | Abstract verified: 1,310 **replayable** MAS failure trajectories, 4 architectures, 4 LLMs. **No own-repo link found in HTML v1 — availability UNCONFIRMED.** | The only corpus that would solve the executability problem (below); do not plan on it. |
| MAS-FIRE injected regime | Taxonomy (15 types) public in paper; repo `wxhhxn/MASFIRE` confirmed **data-only** (result CSVs: camel.csv, metagpt.csv, tablecritic.csv — no injection code). | Injected-regime reference distributions exist as CSVs; live injection must be reimplemented. |

### 3.2 The executability problem (the real blocker for full CAND-5)
CAND-5 has two sub-studies with very different feasibility:
- **Study A (distribution shift):** map organic traces onto the injected taxonomy and compare failure-mode distributions (e.g., per-mode frequency tables, JS divergence, coverage analysis: which MAST modes have no MAS-FIRE counterpart and vice versa). **Pure corpus analysis — no live runs needed.** MAST's 14 modes vs MAS-FIRE's 15 types are different vocabularies; the mapping requires an LLM-judge pass over ~1,642 traces plus human validation of a ~100-trace subsample (~3–4 days, ~$20–50 judge cost). MAS-FIRE's published CSVs supply the injected-regime distribution for free. **Feasible in ~1 week.**
- **Study B (ranking transfer of containment mechanisms):** requires applying containment mechanisms under the *organic* fault regime. **Organic traces are recorded logs — you cannot apply a containment mechanism to a log.** Options: (a) re-instantiate organic failure modes as live injection scenarios in the testbed — but then the validity question recurses (you are testing transfer between injected faults and organically-*inspired* injected faults); (b) use a replayable corpus (StateMAS — availability unconfirmed; Who&When Pro's replay-then-inject pipeline, 2607.09996 — verified abstract, **no data/code link found in HTML v1**). Either way, Study B is a second full experimental campaign on top of the shared build, plus a mapping layer, plus a validity defense.

### 3.3 Experiment matrix, cost, statistics, 19-day verdict
- Study A: no agent runs; judge cost trivial. Statistics = distributional tests over ~1,642 + 307 + 148 traces — adequate for frequency comparisons of common modes, underpowered for rare modes (report as such).
- Study B (if attempted): 2 fault regimes × 3 mechanisms × 1 workflow × 30 reps ≈ 180–360 runs — small, but the *build* (organic-mode re-instantiation + mapping) is 2–3 pw on top of the shared testbed.
- **19-day verdict: Study A alone — FEASIBLE. A+B — NOT FEASIBLE** without descoping B to a demonstration (2–3 mechanisms, 1 workflow, organically-inspired re-instantiation with the recursion caveat stated).

### 3.4 Evaluation difficulty, baselines, reproducibility
- Evaluation: **highest difficulty of the three.** "Distribution shift" needs a defensible metric and the taxonomy mapping will be attacked (MAST modes are behavioral; MAS-FIRE types are causal-injectable — the mapping is many-to-many). Ranking transfer needs Kendall-τ between mechanism rankings with very few mechanisms (τ over 3 items is weak evidence).
- Baselines: none needed for Study A (it is a measurement study); Study B inherits CAND-3/4 mechanisms.
- Reproducibility: MAST-Data/TRAIL public; **AgentFail no-license + "coming soon" README is a reproducibility and citation risk**; LongRCA/StateMAS unconfirmed; the injected regime is reproducible only through our own reimplementation (MAS-FIRE has no code).
- Payoff note: a well-executed Study A ("MAS-FIRE's 15 types cover X% of organic MAST failures; modes a,b,c are missing from every injected taxonomy") is a genuinely useful field-level measurement and cheap. But it is a benchmark-critique paper — the framing least native to MASO's organizational CFP — and its payoff depends on a finding existing (if coverage turns out high, the paper is a shrug).

---

## 4. Ranking by feasibility-adjusted payoff

| Rank | Candidate | Completion prob. in 19 days | Payoff if completed | Feasibility-adjusted verdict |
|---|---|---|---|---|
| **1** | **CAND-3 AttribContain** | High (~0.8 with shared testbed) | High — unoccupied attribution→containment link (B3-verified), crisp threshold deliverable, native to MASO's "detection and mitigation of cascading failures" CFP language | **Best product of feasibility × payoff.** Ground truth is free under injection; artifacts verified (Who&When MIT code runnable; AgenTracer available); modest factorial; deterministic reproducibility. |
| **2** | **CAND-4 RecoveryCost** | Highest (~0.85; rides shared campaign, near-zero extra runs) | Moderate-high — verified gap (recovery cost unmeasured anywhere, B16), but standalone-thin; strongest when merged with CAND-1/3 as their cost axis + the priced-human-escalation result | **Most feasible, thinnest alone.** Recommend: not a standalone paper — fold into whichever of CAND-1/CAND-3 survives, where it adds a verified-gap contribution for ~1 pw. |
| **3** | **CAND-5 FaultValidity** | Low for full (~0.35); high for Study-A-only descope (~0.8) | High if full (field-level validity claim); moderate descoped (benchmark critique) | **Highest risk.** Study B blocked by the executability problem (organic logs are non-executable; StateMAS/LongRCA/Who&When-Pro artifacts unconfirmed) and AgentFail's no-license/ambiguous release. Study A alone is cheap and safe but off-CFP framing and payoff is finding-dependent. |

**Recommended allocation:** CAND-3 as the lead candidate among these three; CAND-4 merged into the shared build as a cost-instrumentation layer (it upgrades any sibling candidate); CAND-5 only as Study-A-only if a spare person-week exists, or deferred.

---

## 5. Verification log (all 21 Sep 2026)

- GitHub API (authenticated `gh`): `mingyin1/Agents_Failure_Attribution` (MIT, 34★, pushed Jan 2026; contents: Automated_FA/{Lib,inference.py,evaluate.py}, Who&When/{Algorithm-Generated,Hand-Crafted}, LICENSE); `wxhhxn/MASFIRE` (data-only: Camel/Metagpt/Table-Critic dirs + CSVs, no code); `multi-agent-systems-failure-taxonomy/MAST` (415★); `Jenna-Ma/JaWs-AgentFail` (8★, **no license**, README "dataset coming soon", but coze/dify/n8n dirs contain trace JSONs + labels — listings inspected); `bingreeky/AgenTracer` (103★, no license).
- HuggingFace pages fetched live: `Kevin355/Who_and_When` (annotated failure logs confirmed); `mcemri/MAD` = MAST-Data (1,642 traces, schema + taxonomy + "annotations are LLM-judge" note read in full).
- arXiv abstract/HTML pages fetched: 2503.13657 (MAST v3), 2509.23735 (AgentFail — ID resolved via arXiv title search; v1 Sep 2025, v2 Feb 2026), 2607.09996 (Who&When Pro — no data link in HTML v1), 2608.15242 (LongRCA v3 — no data link found), 2607.29055 (StateMAS/MARS — no own-repo link found), 2506.07982 (tau2-bench), 2505.08638 HTML (TRAIL → HF PatronusAI/TRAIL).
- Blocked/rate-limited channels: arXiv export API (empty responses), Semantic Scholar API (429), Google Scholar (429), Google web search (JS challenge). All load-bearing claims were nonetheless verified on the primary pages above.
- Wave-1 reports relied on (not re-derived): F1 (substrate, cost table, statistics, build estimates), B3 (attribution accuracy ranges, attribution→containment gap), B5/B16/B8 (recovery-cost gap, human-escalation gap, MAS-FIRE/AgentChaos records), B11/B15 (benchmark + metric landscape), D1/D2 (prior verification of MAS-FIRE/AgentChaos/Who&When).
