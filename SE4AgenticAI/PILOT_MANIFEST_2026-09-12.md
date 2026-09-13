# Pilot manifest: behavioral validity of agent-skill lint repairs

Status: **Draft manifest closing the last open Gate 0 checklist item. Not yet approved, not yet executed. No LLM episode has been run under this manifest.**

Companion documents: [Research plan](SKILL_REPAIR_BEHAVIORAL_VALIDITY_RESEARCH_PLAN_2026-09-12.md) | [Eight-candidate source audit](EIGHT_SKILL_CANDIDATES_SOURCE_AUDIT_2026-09-12.md) | [Gate 0 qualification and second-source log](GATE0_QUALIFICATION_AND_SECOND_SOURCE_2026-09-12.md)

This document is the Gate 0 deliverable called for in the research plan's Section 9 ("Write a pilot manifest, explicit spending ceiling, and predeclared decision rules for approval"). Every factual claim below about the corpus is backed by an executed Docker build and verifier run recorded in the qualification log; nothing here is asserted from static reading alone. Approving this manifest is what would let Gate 0 be declared passed. Approving it is not authorization to run the main study — see Section 9.

## 1. What is frozen by this manifest

- The corpus (Section 2), including each candidate's declared role and narrowed claim.
- The comparison arms and their access restrictions (Section 4).
- The repair-generation protocol (Section 5).
- The outcome measures per candidate (Section 6).
- The predeclared decision rules (Section 8).
- The spending ceiling and calibration gate (Section 7).

Changing any of these after episodes begin invalidates the confirmatory status of the affected results, per the plan's own discipline (Section 6: "Do not select the final hypothesis after seeing which one produces a favorable significance test").

## 2. Corpus: role, status, and narrowed claim per candidate

All 8 are from the single accepted source, SkillsBench, pinned commit `9a1f4dd5f7659f75707435da3ce854b6e48321d1`. Single-source scope is a disclosed limitation, not a defect — see the qualification log Section 10.3 for the source-diversity search that led to this decision.

### 2.1 Primary substantive candidates (R diagnostic: "no mention of error handling or validation")

| Candidate | Task | Status | Narrowed claim / caveat |
|---|---|---|---|
| `fuzzy-match` | `invoice-fraud-detection` | Fully qualified (oracle discriminates correct vs. wrong fraud determinations) | None. Original already allows `None` on no-match — repair scope is ambiguous-candidate handling, not "add error handling from scratch." |
| `d3-visualization` | `data-to-d3` | Fully qualified (15 real Playwright assertions, repeat-run stable) | Do not bundle the D3 v6-vs-v7.9.0 version inconsistency into the R repair — that confound is separate from the diagnostic and must stay out of the frozen edit scope. |
| `dc-power-flow` | `energy-market-pricing` | Fully qualified, **narrowed** | Verifier only checks total cost and internal consistency, never individual LMPs or binding-line sets. Restrict this candidate's measured claim to cost/consistency outcomes only. |
| `mesh-analysis` | `3d-scan-calc` | Fully qualified as a **derived task** | Original task never specifies coordinate units; verifier accepts both cm and cm/1000 conventions. Must ship a modified `task.md` pinning one convention before use, published explicitly as a derived instance per the plan's Section 8. |
| `python-scala-collections` | `python-scala-translation` | **Fully qualified** — confirmed on native x86_64 via a GitHub Actions run (`ubuntu-latest`, 2026-09-13): `sbt` and `scalac` both installed and found (`/root/.local/share/coursier/bin/{sbt,scalac}`); correct submission compiled, all 10/10 unit tests passed, `reward.txt = 1`, `Status: PASSED`; a deliberately corrupted submission (bad Scala syntax appended) correctly failed compilation, tests were correctly skipped as a result, `reward.txt = 0`, `Status: NEEDS IMPROVEMENT` despite an unrelated 25/25 cosmetic quality score — confirming the earlier control-flow trace that a broken compile forces failure regardless of style score. | None remaining. The machine-architecture blocker from the prior pass is resolved; this candidate is on equal footing with the other 7. |

### 2.2 Comparator (C diagnostic: instruction-size / token-efficiency)

| Candidate | Task | Status | Role |
|---|---|---|---|
| `pymatgen` | `crystallographic-wyckoff-position-analysis` | Fully qualified (per-file fractional scoring confirmed via `reward.txt`, exit code always 0 and must not be used) | Anchors the study against the already-published compression/progressive-disclosure literature (SkillReducer). Its result alone cannot carry the paper's novelty claim — see plan Section 5, P4. |

### 2.3 Boundary controls

| Candidate | Task | Status | Role / caveat |
|---|---|---|---|
| `dialogue-graph` | `dialogue-parser` | Fully qualified | T diagnostic (documentation-format), not R — original already documents error handling. Tests whether a purely cosmetic repair changes behavior at all. **Reward-granularity caveat**: `reward.txt` collapses 35 fine-grained pytest assertions into 6 test-group buckets and is far more punitive than the raw pass rate (confirmed: 30/35 assertions passing produced `reward.txt` = 0.333, not 0.857). Capture pytest's own per-assertion output as a supplementary measure, not just `reward.txt`. |
| `reflow-profile-compliance-toolkit` | `manufacturing-equipment-maintenance` | Fully qualified, **narrowed** | R diagnostic firing is a suspected semantic false positive — the skill already documents null-output, missing-data, and sanity-check guidance the keyword detector doesn't recognize. Verifier confirmed empirically toothless on the Q05 "best run" field (a demonstrably wrong best-run pick still passes); do not credit any repair with improving best-run accuracy. Q01-Q04 and schema checks remain valid. **Environment gap**: the Docker image installs no PDF-reading library even though the skill instructs reading `handbook.pdf` — install one (e.g. `pdfplumber`) before any agent episode runs on this candidate. |

### 2.4 What this corpus supports and does not

7 of 8 candidates carry real, executed pass/fail discrimination. This satisfies the plan's "bounded runnable corpus" requirement. It does not support a claim broader than: the behavioral consequences of these specific, frozen repairs on these specific tasks. Six of eight instances share one lexical diagnostic (R) — conclusions about "static checking in general" are not licensed by this corpus, consistent with the original audit's Section 6.

## 3. Task instances

Every candidate above has been qualified only against its **original** SkillsBench task instance. The plan's target is 2 instances per candidate (original + held-out) to distinguish a genuine repair effect from overfitting to one dataset's quirks.

**Update:** held-out instances for all 5 primary candidates have now been constructed and validated by execution — real command output in [GATE0_QUALIFICATION_AND_SECOND_SOURCE_2026-09-12.md](GATE0_QUALIFICATION_AND_SECOND_SOURCE_2026-09-12.md) Sections 12 and 14, artifacts persisted at `SE4AgenticAI/held_out_instances/<task>/`. This was **single-reviewer** construction only — the two-person validation this section still requires has not happened yet.

| Candidate | Held-out instance requirement | Status |
|---|---|---|
| `fuzzy-match` | New invoice/vendor/PO instance, same explicit business rules, different entities/amounts/matching cases | **Constructed, execution-validated** (12 invoices, 7 fraud cases across all 5 categories + 2 priority-order edge cases + 1 genuine fuzzy-match case). Pending second-reviewer check. |
| `d3-visualization` | New stock dataset, same schema and interaction contract | **Constructed, execution-validated**, with a scope caveat: same 50 tickers/10 ETFs (verifier hardcodes these counts), values multiplicatively perturbed per-ticker rather than new companies. Pending second-reviewer check. |
| `dc-power-flow` | Second network/scenario, restricted to the narrowed claim's measured quantities | **Constructed, execution-validated** (3-bus network engineered so the oracle's hardcoded 64->1501 scenario line is genuinely binding, cost reduction confirmed by independent hand computation before execution). Pending second-reviewer check. |
| `mesh-analysis` | Second mesh with known volume/material, unit convention pinned identically to the primary instance | **Constructed, execution-validated**, with a derived verifier (cm-only, dual cm/mm accept removed) empirically confirmed to reject the mm-scale value the original verifier would have wrongly accepted. Pending second-reviewer check. |
| `python-scala-collections` | Held-out inputs for behavior comparison | **Constructed as a derived task** (`RecordBatch.py`/`.scala` — record grouping/dedup/aggregation, new module since the original's fixed `TokenizerSpec.scala` asserts exact behaviors of the specific `Tokenizer.py` and cannot grade a different source; 10-case spec, expected values derived by actually running the Python source, x86_64-validated via GitHub Actions: 10/10 pass on correct solution, correctly fails closed on a corrupted one). Pending second-reviewer check. |
| `pymatgen` | Held-out CIF structures, split by pre-specified structure family, not repeated calls to the same file | Not started, deprioritized behind the 4 primary candidates. |
| `dialogue-graph` | Held-out dialogue satisfying the same explicit grammar; note the existing verifier has fixed narrative IDs and cannot simply be pointed at new data unmodified | Not started, deprioritized behind the 4 primary candidates. |
| `reflow-profile-compliance-toolkit` | Pre-specified numerical outputs with audited handbook-derived expectations, restricted to Q01-Q04/schema per the narrowed claim | Not started, deprioritized behind the 4 primary candidates. |

**Gate:** a second team member must validate each held-out instance's requirements and expected oracle outcome before it is used, per the plan's Section 8 ("If new task instances are required, have two team members validate their requirements and oracles before running agents"). This gate is **still open for all 8 candidates**, including the 4 constructed above — single-reviewer construction is not a substitute. Do not begin Phase 2 (calibration) until this second-reviewer check clears for at least the 4 primary candidates.

## 4. Comparison arms

| Arm | Content | Restriction |
|---|---|---|
| **O** — Original | Unmodified SKILL.md and supporting files, exactly as qualified in Section 2 | — |
| **L** — Lint-directed | O revised using the specific fired diagnostic (R, T, or C) and its stated repair guidance only | Editor sees: original package, the fired diagnostic's exact message/rule ID, the declared environment. Editor does NOT see: task prompt, verifier source, ground-truth labels, held-out instance, or any outcome. |
| **G** — Generic revision | O revised using general "improve this skill's quality" guidance, withholding the targeted diagnostic list | Same editor, same model, same one-candidate revision budget as L. Same access restrictions as L. |
| **N** — No skill | Same task environment and tool capabilities, target skill guidance omitted | Non-target skills, executable helpers, and metadata stay identical to O/L/G. If a task requires skill-bundled scripts to be solvable (e.g. `mesh_tool.py` in `mesh-analysis`), those remain available in N — only the natural-language instructions are withheld. |

Freeze the edit surface before generating L and G for each candidate. A warning-scoped no-op is a valid, loggable L/G outcome (e.g. if `reflow-profile-compliance-toolkit`'s R finding is confirmed a true false positive, the correct L output may be "no defensible repair exists" — record this, do not force an edit to make the arm non-trivial).

**Second-reviewer check:** for every L and G pair, a team member who has not seen behavioral outcomes checks that the edit stays within the declared warning's scope, before any task episode runs (plan Section 8, repair preparation step 5).

## 5. Repair-generation protocol

- **Editor model:** one fixed model, same for L and G within a candidate, different from (or same as — decide once, freeze it) the execution model(s) in Section 6. Recommend using the same model family as one of the two execution models to avoid conflating "editor capability" with "execution model" as a third uncontrolled variable, but this is a team decision to make explicitly before Phase 2, not implicitly.
- **Budget:** one candidate revision per arm per skill. No regeneration after seeing a draft's plausibility, no iteration against task outcomes.
- **Inputs the editor receives:** original package contents, the declared quality-checker finding (rule ID, message, severity, source clause), the applicable specification/authoring citation from Section 3 of the source audit.
- **Inputs the editor must never receive:** task prompt, verifier/oracle source, ground-truth labels, prior arm's output, any execution trace.
- **Logging:** every diff (L and G), the exact prompt given to the editor, and the second-reviewer's scope determination, preserved as artifacts regardless of downstream outcome.

## 6. Outcome measures

Primary: task success per the qualified oracle (Section 2), read from the score file the qualification log identified as authoritative for each candidate — **never process exit code**, which pymatgen and dialogue-graph confirmed is always 0 regardless of correctness. Where `reward.txt` is coarser than the underlying checks (`dialogue-graph`), also capture the raw test-framework pass count as a supplementary measure.

Secondary, recorded for every episode regardless of arm: model requests, input/output/cache tokens, tool calls, elapsed time, environment failures (distinguished from task failures).

Every outcome is read against the **narrowed claim** recorded in Section 2 for that candidate. An observed L-vs-O difference on a field the oracle is known not to discriminate (`dc-power-flow`'s individual LMPs, `reflow-profile-compliance-toolkit`'s Q05 best-run pick) is not reportable as a finding — it would be a verifier artifact, not evidence, per the qualification log's explicit empirical demonstration of those gaps.

## 7. Spending ceiling and calibration gate

**No dollar or episode cap is set by this manifest yet — one cannot be set honestly, because zero LLM episodes have been run against this corpus.** The research plan explicitly prohibits inferring cost from an unrelated prior pilot (AgentDojo) given these are different environments. Locking a budget now would repeat exactly that mistake.

**Required calibration step before Phase 3 (full matrix):**

1. All 5 primary candidates now have validated held-out instances (Section 3): `fuzzy-match`, `d3-visualization`, `dc-power-flow`, `mesh-analysis`, `python-scala-collections`.
2. Run a small calibration batch: 5 candidates x 1 task instance (original only) x 2 arms (O, N — cheapest pair, no repair generation needed yet) x 1 model x 1 repetition = 10 episodes.
3. Measure real per-episode: wall-clock time, token cost, tool-call count, infra failure rate.
4. From measured per-episode cost, compute the dollar cap for the full matrix (Section 8's illustrative 256-episode figure, or a reduced version — see below) and get explicit approval before Phase 3 begins.
5. Calibration episodes are **not** confirmatory evidence. Do not fold them into the main analysis, per the plan's explicit warning (Section 10).

**Do not run any L or G episode during calibration** — those require the repair-generation and second-review steps in Section 5 to already be complete, which is out of scope for a cost-measurement pass.

## 8. Illustrative full matrix (subject to the calibration gate)

Scoped to the 4-5 primary substantive candidates only (Section 2.1) for the confirmatory analysis; `pymatgen`, `dialogue-graph`, and `reflow-profile-compliance-toolkit` run a reduced matrix (O/L/N only, no G, since their role is comparator/control rather than primary hypothesis-bearing):

- **Primary (5 — `python-scala-collections` now fully qualified, held-out instance pending):** candidates x 2 task instances x 4 arms x 2 models x 2 repetitions = 5 x 2 x 4 x 2 x 2 = **160 episodes**.
- **Comparator + controls (3):** candidates x 2 task instances x 3 arms (O/L/N) x 2 models x 2 repetitions = 3 x 2 x 3 x 2 x 2 = **72 episodes**.
- **Total: up to 232 episodes**, excluding repair-generation calls, the 8-episode calibration batch, and infrastructure retries.

This is a planning number, not a locked commitment — it is explicitly subordinate to the calibration gate in Section 7 and may be reduced if measured cost makes the full figure infeasible within the deadline (Section 10).

Two models: not yet selected. Decide and freeze before Phase 2, choosing models that differ enough to avoid over-generalizing a single-model artifact (plan Section 10: "do not generalize a single-model artifact to agents as a whole"), while staying within whatever the approved dollar cap allows for 232 episodes at two models' pricing.

Two repetitions is a screening budget, not enough for precise per-candidate reliability claims (plan Section 10) — treat any single-candidate result as a lead for the main study, not a standalone finding, unless cluster-aware analysis across the full corpus shows an effect that survives.

## 9. Predeclared decision rules

Evaluate the pilot's outcome against the three paths in the plan's Section 10, decided **before** running Phase 3:

1. **Benefit:** L shows a practically interesting advantage over G that is not explained by generic rewriting, changed capabilities, or cost omissions, on at least one primary candidate, replicated in direction (not necessarily magnitude) across both models.
2. **Harm or conditional benefit:** a reproducible L-vs-O or L-vs-G difference identifies a nontrivial repair risk or operating condition, with a plausible mechanism traceable to the actual diff (Section 5's logged artifacts), on at least one candidate.
3. **Potentially informative negligible effect:** the pooled, cluster-aware (by candidate and model) confidence interval on the primary L-vs-G contrast excludes the predeclared practical-significance margin — to be set numerically by the team before Phase 3, informed by Phase-2 calibration variance, not chosen after seeing results.

**Pilot stop conditions** (from the plan's Section 10, reproduced here so they are checked against this specific corpus, not abstractly):
- Warning removal is the only demonstrated change, and this corpus cannot resolve a useful effect at feasible scale.
- The apparent effect disappears under the fair-capability/budget/state-reset controls already built into Section 4-5 of this manifest.
- Findings are dominated by one candidate (e.g. `dc-power-flow`'s narrowed claim, or `reflow-profile-compliance-toolkit`'s Q05 exclusion) rather than the corpus as a whole.
- Nearly all tasks are at floor or ceiling with no prejustified independent test population — a real risk given `d3-visualization` and `pymatgen` both passed cleanly at 1.0/1.00 on their qualification runs; held-out instances (Section 3) must be selected to avoid ceiling effects, not just for novelty.
- L and G are operationally indistinguishable for a given candidate — log this per-candidate rather than treating it as a whole-pilot failure, since it is informative on its own (plan Section 4: "the same warning has different consequences...").
- The contribution becomes only "static lint does not guarantee correctness" — none of the corpus's narrowed claims or the `dialogue-graph`/`reflow-profile-compliance-toolkit` control results should be over-read into this trivial framing.

## 10. Remaining gate before Phase 3 can start

1. ~~`python-scala-collections` x86_64 re-verification~~ **DONE (2026-09-13)** — confirmed on native x86_64 via GitHub Actions (`ubuntu-latest`): correct submission compiled, 10/10 tests passed, `reward.txt=1`; corrupted submission correctly failed closed, `reward.txt=0`. This candidate is now fully qualified alongside the other 7 — see Section 2.1. **No longer a Gate 0 blocker.**
2. Held-out task instance construction and second-reviewer validation for the primary candidates (Section 3). **Construction done and execution-validated for all 5** (fuzzy-match, d3-visualization, dc-power-flow, mesh-analysis, python-scala-collections) — see Section 3 and the qualification log Sections 12 and 14. **Second-reviewer validation is still open** for all constructed instances; single-reviewer construction does not satisfy this item.
3. Repair generation (L, G) for those same candidates, with second-reviewer scope checks (Section 4-5). **Still open** — requires LLM API spend, explicitly held pending separate authorization.
4. Calibration batch executed and dollar cap approved (Section 7). **Still open** — requires LLM API spend, explicitly held pending separate authorization.
5. Two execution models selected and frozen (Section 8). **Still open.**
6. Practical-significance margin for the negligible-effect path set numerically (Section 9). **Still open.**

Once items 1-6 are complete, Gate 0 as defined by the research plan's Section 9 pass condition is satisfied by this manifest plus the qualification log it depends on, and Phase 3 (the actual pilot matrix) can begin under the frozen protocol above. Nothing in this manifest authorizes spending yet — items 1-6 are the actual remaining work.

## 11. Team allocation for the items in Section 10

Per the plan's Section 13 roles, adapted to the current state:

| Role | Immediate task from Section 10 |
|---|---|
| Literature/rule lead | Item 6 (margin-setting needs the literature's typical effect sizes as a reference point); also still owes the plan's never-completed "recheck closest papers for newer artifacts" checklist item |
| Corpus/evaluation lead | Items 1-2 (x86_64 re-verification, held-out instances), continuing the same qualification discipline used in the Gate 0 passes |
| Repair/execution lead | Item 3 (frozen L/G generation), item 4 (calibration run) |
| Analysis/reviewer lead | Item 5 (model selection rationale), second-reviewer duties threaded through items 2-3 |

Given the 10 October 2026 deadline, items 1-6 should be timeboxed to roughly 3-4 days, leaving the remainder of the month for Phase 3 execution, analysis, and writing — consistent with the plan's own Section 13 schedule, which allocated "days 3-5" to the approved pilot.
