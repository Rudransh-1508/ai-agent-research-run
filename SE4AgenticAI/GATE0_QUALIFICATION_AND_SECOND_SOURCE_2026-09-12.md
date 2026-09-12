# Gate 0 qualification pass 2: container execution and a second source

Date: 12 September 2026

Status: **Corpus-qualification checklist item now complete for all 8 SkillsBench candidates. Seven of eight have executed, reproducible qualification evidence (deliberately-wrong-output rejection confirmed for each); the eighth (python-scala-collections) is qualified by static control-flow analysis but empirically blocked by this machine's CPU architecture, not by a task defect. `github.com/swe-bench/SWE-bench` was investigated and rejected as a direct source (no skill layer; using it would require fabricating skills ourselves). SWE-Skills-Bench was investigated as a second source, pulled and run for real, and found not reconstructible from public artifacts (Section 9). A final bounded second-source search (Section 10) found nothing viable. The corpus is confirmed single-source, accepted as such. Gate 0 still does not pass overall — the corpus-qualification checklist item is done, but the pilot manifest, spending ceiling, and predeclared decision rules (a separate checklist item) have not been started.**

Companion documents: [Research plan](SKILL_REPAIR_BEHAVIORAL_VALIDITY_RESEARCH_PLAN_2026-09-12.md), [Eight-candidate source audit](EIGHT_SKILL_CANDIDATES_SOURCE_AUDIT_2026-09-12.md).

## 1. What this document adds

The prior audit found 8 candidates but explicitly left two Gate 0 checklist items undone: "demonstrate that candidate environments build and reset" and "exercise existing reference solutions... and test the oracles without an LLM." It also flagged reliance on a single source (SkillsBench) as a limitation. This pass closes the first gap for the top 2 candidates with real, executed evidence, and makes progress on the second gap by locating and screening one additional independently verified source.

No LLM repair calls or agent task episodes were run. Everything below is either an actual command execution with captured output, or an explicitly labeled static/document review.

## 2. Task A: container qualification of the top 2 SkillsBench candidates

Environment: local Docker (Docker Desktop, arm64), pinned SkillsBench commit `9a1f4dd5f7659f75707435da3ce854b6e48321d1`, fetched via GitHub codeload tarball (git clone of the full history exceeded a 2-minute timeout at >400MB; the tarball approach was used instead and only the two target task directories were extracted).

### 2.1 fuzzy-match / invoice-fraud-detection

- `docker build` on `environment/Dockerfile` (Ubuntu 24.04, Python 3, pinned `pandas`, `rapidfuzz`, `pdfplumber`, etc.) completed successfully.
- Ran `oracle/solve.sh` inside the built image, then `verifier/test.sh`: both pytest cases (`test_file_exists`, `test_content`) **passed**, `reward.txt` = `1`.
- Ran the verifier again against a deliberately wrong output (`fraud_report.json` replaced with `[]`): `test_file_exists` passed, `test_content` **failed** with an explicit assertion listing all 50 missed-fraud pages, `reward.txt` = `0`.
- Conclusion: the oracle exists, runs, and the verifier discriminates correct from incorrect output. This candidate passes the "exercise oracle without an LLM" checklist item.

### 2.2 d3-visualization / data-to-d3

- `docker build` on `environment/Dockerfile` (Ubuntu 24.04 + Node + Playwright with Chromium, `playwright install --with-deps chromium`) completed successfully (~130s for the Chromium download layer).
- Ran `oracle/solve.sh` (builds `index.html`/CSS/JS/data into `/root/output`, pins `d3@6.7.0` via `npm install`) then `verifier/test.sh`. The verifier launches a real Playwright/Chromium browser against a local HTTP server. All 15 test cases passed (`test_bubble_chart_rendering`, `test_data_table`, `test_tooltips_non_etf_and_etf`, `test_interactive_linking`, `test_market_cap_formatting`, `test_sector_clustering`, `test_legend_completeness`, `test_data_integrity`, plus file-structure checks), `reward.txt` = `1`.
- Repeated the full oracle+verifier run a second time: identical result, 15/15 passed, `reward.txt` = `1`. No flakiness observed across 2 runs.
- Ran the verifier against a deliberately broken output (`index.html` replaced with a 33-byte stub, no JS/CSS/data copied): 2 of 15 passed (file-existence check for the stub `index.html` and a diagnostic test), **13 failed** with real assertion errors (missing files, empty DOM, no bubbles, no table rows), `reward.txt` = `0`.
- Confirms the audit's flagged version confound is real and unaddressed: the oracle explicitly installs `d3@6.7.0`, while the skill body's own default recommendation is v7.9.0 (per the prior audit, Section 4.2). This remains a live risk for any repair that touches version guidance and must stay out of the frozen R-diagnostic repair scope.
- Conclusion: the verifier does genuine DOM/interaction assertions via a real browser, not a trivial exit-code check, and is reproducible across repeated runs. This candidate also passes the checklist item.

### 2.3 What this does and does not establish

This closes the specific "build and exercise oracles" checklist gap for the two highest-priority candidates only. It does not qualify `dc-power-flow`, `python-scala-collections`, or `mesh-analysis` (still blocked per the prior audit), and it does not constitute a pilot run, a repair, or any agent-behavior evidence.

## 3. Task B: a second, independently verified source

### 3.1 Search process

Searched beyond SkillsBench for corpora that pair skill text with a runnable task, execution environment, and independent verifier (not routing/retrieval benchmarks, and not instruction-only skill repositories). Explicitly ruled out during the search:

- **NVIDIA/skills** (`github.com/nvidia/skills`): confirmed via direct repository review to contain only `SKILL.md` + governance metadata + optional benchmark docs, with no bundled tasks, Docker environments, or per-skill verifiers. This is the exact trap the prior audit already warned against ("a skill file alone may omit required supporting resources"). Rejected.
- **darkrishabh/agent-skills-eval**: a CI test-runner tool for the agentskills.io `evals.json` format, ships only one demo skill, no corpus. Rejected as a source.
- **SkillRet, SkillRouter, SkillResolve-Bench**: retrieval/routing benchmarks. Out of scope per the plan's explicit decision to hold routing fixed (Section 5, "Recommended initial scope").
- **MalSkillBench** (arXiv:2606.07131): a malicious-skill detection benchmark with a Docker/syscall-monitoring pipeline and an LLM judge, not a deterministic task-acceptance verifier; its "benign" samples are matched controls for detection scoring, not standalone skill+task+oracle bundles. Reusing it would require building new evaluation scaffolding the plan says to avoid. Rejected.
- Several other benchmark names (SkillCraft, SkillLearnBench, WildClawBench, SkillForge) surfaced only inside a third-party survey's AI-generated summary (arXiv:2606.11435, fetched via a summarizing tool) and could not be independently confirmed to exist via direct search; they are not used below. Do not treat a survey's paraphrase as a verified citation without independent confirmation — this is the same caution the prior audit applied to detector tooling.

### 3.2 SWE-Skills-Bench: a confirmed, independently verifiable second source

- Paper: "SWE-Skills-Bench: Do Agent Skills Actually Help in Real-World Software Engineering?", arXiv:2603.15401. Abstract independently fetched and quoted in full; confirms 49 public SWE skills paired with authentic GitHub repositories at pinned commits, ~565 task instances across six SWE subdomains, and "a deterministic verification framework that maps each task's acceptance criteria to execution-based tests."
- Dataset: `huggingface.co/datasets/GeniusHTX/SWE-Skills-Bench`, confirmed live via the HF API (HTTP 200, MIT license, 329 downloads, `arxiv:2603.15401` tag). Downloaded the actual parquet file (`train/0.parquet`, 49 rows) and inspected it directly with pandas — this is real data, not a description.
- **The linked GitHub repository (`github.com/GeniusHTX/SWE-Skills-Bench`) returns HTTP 404** — confirmed via both `curl` and the GitHub API. The paper's stated code-availability link is currently dead. The dataset itself is still usable independently of that repo, but this is a real provenance gap: no confirmed source for the harness/runner code that executes `docker_image` + `test_code` end to end, only the raw data.
- Schema (confirmed from the actual parquet): `skill_id, name, description, type, task_prompt, skill_document, test_code, repo_url, repo_commit, docker_image`. Unlike SkillsBench, skills are not packaged directories with bundled scripts — `skill_document` is a single Markdown text field. This is a real structural difference from the study's O/L/G/N design, which edits package artifacts including bundled scripts; repairs to this corpus would be repairs to a single markdown blob only. Record this as a scope difference, not a defect.
- Domains (from the dataset card): Deployment & DevOps, Analytics & Monitoring, API Development, Data Science & ML, Security & Testing, Developer Tools — genuinely distinct from SkillsBench's domain mix (invoices, energy markets, materials science, dialogue graphs, manufacturing, etc.), which strengthens the "more than one source" case beyond just a different hostname.
- **Verified blocker**: `repo_commit` is empty for 48 of 49 rows in the distributed parquet. The paper's claim of repositories "pinned at fixed commits" is not reproducible from this artifact as downloaded — either the commit pin lives inside the `docker_image` (unverified — no image was pulled or inspected in this pass) or the field was dropped from this HF snapshot. This must be resolved before any repair-qualification work on this source, exactly analogous to `dc-power-flow`'s incomplete oracle in the prior audit.
- `repo_url` is populated for 48/49 rows; one row (`add-uint-support`) has an empty `repo_url` and should be dropped or investigated before use.

### 3.3 Ran the same reliability diagnostic against this corpus

Reused the prior audit's exact lexical test (regex for error/exception/invalid/failure/validation terms) against the `skill_document` field of all 49 rows, as a stand-in for the NVIDIA SkillEvaluator's `quality_reliability` check (that checker targets `SKILL.md` frontmatter specifically, which this corpus does not have — the same regex logic was applied directly to the text field instead, and this substitution is flagged, not hidden).

**8 of 49 skill documents have no reliability-language hits**, a natural warning rate consistent with SkillsBench's occurrence pattern:

| skill_id | name | repo_url | docker_image |
|---|---|---|---|
| add-uint-support | Add UInt Support | *(empty — reject)* | — |
| add-admin-api-endpoint | Ghost Admin API Endpoint Creator | github.com/TryGhost/Ghost | zhangyiiiiii/swe-skills-bench-python |
| vector-index-tuning | Vector Index Tuning | github.com/facebookresearch/faiss | zhangyiiiiii/swe-skills-bench-python |
| rag-implementation | RAG Implementation Framework | github.com/langchain-ai/langchain | zhangyiiiiii/swe-skills-bench-python |
| similarity-search-patterns | Similarity Search Patterns | github.com/milvus-io/milvus | zhangyiiiiii/swe-skills-bench-python |
| linkerd-patterns | Linkerd Service Mesh Patterns | github.com/linkerd/linkerd2 | zhangyiiiiii/swe-skills-bench-golang |
| gitlab-ci-patterns | GitLab CI Security Templates | github.com/gitlabhq/gitlabhq | zhangyiiiiii/swe-skills-bench-ruby |
| python-performance-optimization | Python Performance Optimizer | github.com/benfred/py-spy | zhangyiiiiii/swe-skills-bench-python |

For the four most promising rows (`add-admin-api-endpoint`, `vector-index-tuning`, `gitlab-ci-patterns`, `linkerd-patterns`) the `test_code` field was read directly: each contains real, non-trivial pytest classes with named test methods asserting on concrete repo-specific artifacts (e.g. `gitlab-ci-patterns` checks for specific SAST/DAST/Dependency-Scanning template file paths under `lib/gitlab/ci/templates/`; `linkerd-patterns` checks for mTLS `Server`/`ServerAuthorization` CRD files). This is consistent with genuine execution-based verification, not placeholder tests — but **no container was built or run for this source in this pass**; only static inspection of the downloaded parquet was performed. That is the specific gap remaining before this source can be treated as qualified.

### 3.4 Candidate roles for the paper if adopted

- `add-admin-api-endpoint` and `linkerd-patterns` are the strongest immediate candidates to qualify next: real repos, real docker images, concrete file-existence + content assertions in `test_code`, and they extend the corpus into infra/backend domains the SkillsBench shortlist does not cover.
- The paper's own finding — "three [skills] degrade performance... due to version-mismatched guidance conflicting with project context" — is a second independent, published instance of exactly the mechanism this study's L-vs-O contrast is designed to detect (a lint-style advisory fix producing behavioral harm). That is a genuine point of resonance with the research question, not just a source of raw materials, and is worth citing directly in the paper's motivation regardless of whether this corpus becomes part of the executed pilot.

## 4. Updated Gate 0 status

Checklist items from the plan (Section 9), status after this pass:

| Item | Status |
|---|---|
| Recheck closest papers for newer versions/artifacts | Not done in this pass |
| Inspect detector definitions and candidate linter implementations | Done (prior audit) |
| Map promising rules to pinned spec/authoring sources | Done (prior audit) |
| Find complete original packages with natural warnings and existing tasks | Done — now across **two** sources |
| Demonstrate candidate environments build and reset | **Done for 2 of 8 SkillsBench candidates** (fuzzy-match, d3-visualization). Not done for the other 6, and not done for any SWE-Skills-Bench row. |
| Exercise reference solutions/oracles without an LLM | **Done for the same 2 candidates**, including known-good and known-bad discrimination and (for d3) repeat-run stability. Not done elsewhere. |
| Establish sampling frame, document inclusion/exclusion | Done (prior audit), extended here with SWE-Skills-Bench screening |
| Determine baseline feasibility beyond compression alone | Unchanged from prior audit |
| Write pilot manifest, spending ceiling, decision rules | Not done |

**Gate 0 does not pass yet.** Two of eight-plus-candidates now have real, executed, reproducible qualification evidence — a meaningful and concrete advance over the prior audit's zero — but the plan's own pass condition requires a bounded runnable corpus, not two data points, and the "more than one source" target is only partially met: SWE-Skills-Bench is confirmed to exist and to contain genuine execution-based verifiers, but **no container from it has actually been built or run**, and its commit-pin field is verifiably broken in the distributed data and must be resolved first.

## 5. Smallest next step (superseded by Sections 6-8 below)

Two options were identified here in the previous pass; both were acted on. See Sections 6-8 for what was actually run and the resulting verdicts.

## 6. SWE-bench (github.com/swe-bench/SWE-bench): investigated, rejected as a direct source

The user pointed at this repository specifically. Checked directly, not inferred:

- Fetched `swe-bench/SWE-bench`'s live README. It is a benchmark of **(codebase, GitHub issue) -> patch** tasks with Docker-based, test-based evaluation. There is no SKILL.md-equivalent packaged-instruction layer anywhere in the repository or its documented task format. A task instance is a repo, a commit, an issue description, and a set of tests — not a skill.
- Searched for any published work pairing SWE-bench instances with agent-skill packages ("SWE-bench skill", "SWE-bench agent skill"). No such artifact was found. The only skill-flavored SWE benchmark located, in this pass or the last, is SWE-Skills-Bench (arXiv:2603.15401), already identified as the second source.
- Fetched the SWE-Skills-Bench paper's abstract and full HTML text directly to check whether it reuses SWE-bench's actual task instances or harness (this would have made SWE-bench a redundant, not independent, third source). It does not: SWE-Skills-Bench's construction is authored from scratch per repository/skill pair (custom requirement documents with Background/Requirement/File-Operations/Acceptance-Criteria sections, and pytest verifiers generated from those requirements via a "professional test engineer" prompt). The paper cites "SWE-Bench Verified" only as related work ("a human-validated subset of 500 instances from SWE-Bench"), not as an input to its own pipeline. SWE-Skills-Bench and SWE-bench are confirmed independent artifacts.

**Verdict: rejected as a direct source, correctly.** Using SWE-bench for this study would require authoring the skill package ourselves for each repository, since none exists. That is a stronger violation of the plan's natural-warning requirement than anything considered so far: it would mean fabricating not just a repair candidate but the entire skill artifact and whatever "natural" warning it happens to carry, which is indistinguishable from injecting an artificial defect to make the corpus work — exactly what Section 4/8 of the research plan prohibits. SWE-bench remains useful only as background context (it is the well-known bug-fix benchmark genre that SWE-Skills-Bench's authors built their skill layer on top of, independently), not as a corpus source for this study.

## 7. Resolving the 3 blocked SkillsBench candidates: real Docker builds and verifier runs

All three were re-checked against the actual pinned commit (`9a1f4dd5f7659f75707435da3ce854b6e48321d1`), widening the earlier sparse-checkout to pull the complete task directories (the previous pass's checkout was missing supporting files like `scala_tokenizer/build.sbt`, which had to be added before any of this was possible). No LLM calls were made in this section; only Docker builds, direct script execution, and direct verifier execution.

### 7.1 dc-power-flow / energy-market-pricing: RESOLVED, with a narrowed claim

- Read the full verifier (`verifier/test_outputs.py`) directly. It independently re-solves the DC-OPF problem with `cvxpy` (`TestOptimality`) and checks report-internal arithmetic consistency (`TestFeasibility`) and schema (`TestSchema`). Its own docstring states the design choice explicitly: "We do NOT compare individual LMP values or binding line sets, as these may differ between equally-valid optimal solutions."
- Built the Docker image from `environment/Dockerfile` (numerical stack installs at verify-time via `pip3`, deliberately not baked into the image "to avoid hinting the agent" per a comment in `test.sh`) and ran it on a real network (2,869 buses, 510 generators, 4,582 branches).
- Ran `oracle/solve.sh`: produced a real `report.json`; all 4 verifier tests passed (`test_report_schema`, `test_internal_consistency`, `test_costs_near_optimal`, `test_cost_reduction_non_negative`).
- Ran the verifier again after deliberately inflating `base_case.total_cost_dollars_per_hour` by 50%: 2 of 4 tests correctly **failed**, with real assertion output (`Cost reduction 3878.53 != computed 1486697.49`, `base_case cost 4448456.87 exceeds optimal 2965637.91 by more than 0.0100%`).
- **Conclusion**: the verifier genuinely discriminates correct from incorrect total-cost and internal-consistency claims, confirming the prior audit's read. The scope limit is real and must be carried into the study design as the audit already suggested: **restrict this candidate's measured claim to total cost (base and counterfactual) and internal consistency of reported deltas.** Do not claim the study measures whether a repair improves the correctness of individual LMP values or the identified binding-line set — the oracle does not check either against ground truth, so any apparent L-vs-O effect on those fields would be an artifact of the check, not evidence. This is a legitimate, usable candidate under that explicit narrowing, not a dropped one.

### 7.2 python-scala-collections / python-scala-translation: CONDITIONALLY RESOLVED, empirical confirmation blocked by this machine's architecture

- Read the full verifier (`verifier/test_outputs.py`) directly, specifically the `run_full_evaluation` control flow the prior audit flagged. The flagged behavior is real: `check_compilation()` does set `success=True` with a warning when neither `sbt` nor `scalac` is found ("Compilation check skipped - no Scala compiler available"). However, tracing the full gate: `results["tests"]` is only populated (not left as `{"skipped": True}`) when `compilation_result.success and shutil.which("sbt")`; final `results["passed"]` requires, in order, `total_score >= 15`, then `"skipped" not in results["tests"]`, then `test_result.passed == test_result.total and test_result.total == 10`. If `sbt` is absent, tests are always marked skipped regardless of the scalac fallback, and `passed` is forced `False` before the final `test_result` reference is ever reached (so there is also no risk of a `NameError` from referencing an unset `test_result`). **The specific "fake pass" mechanism flagged by the prior audit does not exist in the actual grading computation** — the scalac fallback only affects an informational sub-field, not the reward.
- Attempted to build `environment/Dockerfile` to confirm empirically that `sbt` (not just `scala`/`scalac`) actually installs and that a broken submission fails closed with exactly this logic exercised. This is where a genuine, different blocker was found: the Dockerfile's `RUN curl ... coursier ... ./cs setup --yes && ./cs install scala:2.13.12 scalac:2.13.12` step **fails on this machine (Apple Silicon Mac, Docker Desktop)** — natively (`rosetta error: failed to open elf`, exit 133) and under explicit `--platform linux/amd64` emulation via `docker buildx build --platform linux/amd64 --load` (two separate attempts: `SIGILL`-style abort on first try, then a clean but final QEMU rejection: `The current machine does not support all of the following CPU features that are required by the image: [CX8, CMOV, FXSR, MMX, SSE, SSE2, SSE3, SSSE3, SSE4_1, SSE4_2, POPCNT, LZCNT, AVX, AVX2, BMI1, BMI2, FMA]. Please rebuild the executable with an appropriate setting of the -march option.`). This is coursier's GraalVM-native-image binary hitting a real limitation of QEMU user-mode CPU emulation on ARM hosts, not a bug in the task itself.
- **Conclusion**: the specific concern raised in the prior audit (silent fake-pass) is resolved by static analysis of the actual control flow and does not block use of this candidate. But full empirical confirmation — verifying `sbt` actually installs at verify-time and that a deliberately broken `Tokenizer.scala` fails closed end-to-end — could not be completed on this development machine due to a genuine, unrelated Docker/CPU-emulation incompatibility. This must be re-attempted on native x86_64 Linux infrastructure (e.g. a cloud CI runner or an x86_64 host) before this candidate is marked fully qualified. Record this as an infrastructure requirement for whoever runs the actual pilot, not as a property of the task itself.

### 7.3 mesh-analysis / 3d-scan-calc: RESOLVED as a derived task

- Read `task.md` in full: it specifies the STL file, the material-ID-in-attribute-byte convention, the output schema, and a 0.1% tolerance — **it never specifies the coordinate units** (no mention of mm, cm, or any unit anywhere in the prompt). The `mesh-analysis` SKILL.md itself says: "Do not assume millimeters or inches. Check your task instructions for the coordinate system units" — instructions that do not exist. The task's own contract is genuinely incomplete, independent of the verifier.
- Read `verifier/test_outputs.py` in full and confirmed the exact dual-accept logic the prior audit described: it independently recomputes volume from the ground-truth STL via signed-tetrahedron summation and connected-component analysis, then accepts a submitted mass matching either `volume * density` (cm³ convention) or `volume/1000 * density` (mm³ convention), each within 0.1% relative tolerance.
- Built the Docker image (`environment/Dockerfile`, plain Python 3, no architecture issues) and ran it end to end:
  - Oracle output (`main_part_mass = 34648.04`, material ID 42): verifier **passed** (both tests).
  - Same volume scaled by 1/1000 (`main_part_mass = 34.65`, the mm-convention value): verifier **also passed** — confirms the dual-accept is real and live, not just present in source.
  - The mm-scaled value further multiplied by 10 (a genuinely wrong answer, `346.48`): verifier **correctly failed**, with an explicit assertion (`Mass mismatch. Expected ~34648.04 (cm) or ~34.65 (mm), got 346.48`).
- **Conclusion**: the unit ambiguity is real, confirmed by direct execution, and would make any L-vs-O behavioral contrast on this task uninterpretable as originally distributed (a repair that clarifies units couldn't be credited even if it changed agent behavior, since both conventions already pass). This is resolvable exactly as the plan allows for derived tasks (Section 8: "If tasks are modified, publish them as derived instances"): pin one unit convention explicitly in a modified `task.md`, and narrow the verifier to accept only that convention's tolerance band, before this candidate is used. The underlying computation, oracle, and pass/fail discrimination are otherwise sound (confirmed above), so this is a legitimate derived-task fix, not a fatal flaw.

## 8. Updated Gate 0 status (superseded by Section 9's finding on SWE-Skills-Bench; table below reflects the final state after Section 9)

| Item | Status |
|---|---|
| Recheck closest papers for newer versions/artifacts | Not done in any pass |
| Inspect detector definitions and candidate linter implementations | Done |
| Map promising rules to pinned spec/authoring sources | Done |
| Find complete original packages with natural warnings and existing tasks | Done for SkillsBench (one source, confirmed runnable). SWE-Skills-Bench discovered but **found not independently reconstructible from public artifacts** (Section 9) — see revised source status below. |
| Demonstrate candidate environments build and reset | **4 of 8 SkillsBench candidates confirmed** (fuzzy-match, d3-visualization, dc-power-flow, mesh-analysis). 1 blocked by this machine's architecture only (python-scala-collections). 3 not attempted (pymatgen, dialogue-graph, reflow-profile-compliance-toolkit — declared comparator/control roles, lower priority). SWE-Skills-Bench: containers pull and run, but the required repo state is **absent from the image and unrecoverable from public data** (Section 9) — not qualifiable as distributed. |
| Exercise reference solutions/oracles without an LLM, including deliberately-wrong-output rejection | **Done for the same 4 SkillsBench candidates**, each with a real passing run and a real rejected deliberately-broken run. Not reachable for SWE-Skills-Bench — there is no repo checkout to run `test_code` against. |
| Establish sampling frame, document inclusion/exclusion | Done, including SWE-bench's explicit rejection as a direct source (Section 6) and SWE-Skills-Bench's explicit rejection as a runnable second source (Section 9) |
| Determine baseline feasibility beyond compression alone | Unchanged: `pymatgen` remains the one explicit compression comparator; the other qualified candidates (fuzzy-match, d3-visualization, dc-power-flow, mesh-analysis) are not compression interventions |
| Write pilot manifest, spending ceiling, decision rules | Not done |

**Gate 0 still does not pass**, and the corpus is now confirmed **single-source** (SkillsBench only) rather than "second source pending." The remaining concrete items:

1. **Infrastructure, not corpus**: re-run the `python-scala-collections` empirical check on native x86_64 Linux to close the one candidate left conditional.
2. **Source diversity is now a decision point, not a to-do item.** Section 9 shows SWE-Skills-Bench cannot be qualified from what's publicly distributed without building a clone/setup harness the plan's own stop conditions prohibit ("packages cannot be reconstructed... without extensive new infrastructure"). The team must explicitly choose: (a) proceed with a single, well-qualified SkillsBench corpus and state single-source reliance as a disclosed limitation — defensible, since the plan's literal Section 9 pass condition does not hard-require multiple sources, only its non-binding "suggested feasibility target" does — or (b) spend one more bounded search pass on a genuinely different second source before writing the pilot manifest. This is a scope call for the researchers, not something a further audit can resolve by itself.
3. Write the pilot manifest, spending ceiling, and decision rules once (2) is decided — this is the one checklist item with zero progress across all three passes.

No further undirected corpus search is warranted — three passes have already covered SkillsBench, SWE-bench, and SWE-Skills-Bench thoroughly. What remains is either accepting single-source scope or making one more deliberate, targeted attempt at a second source, followed by the pilot manifest.

## 9. SWE-Skills-Bench container qualification: attempted and found infeasible as distributed

Both candidate images were pulled and run for real; both show the same disqualifying pattern.

### 9.1 add-admin-api-endpoint / zhangyiiiiii/swe-skills-bench-python

- Read the full parquet row directly: `task_prompt` asks the agent to add an `audit_logs` Admin API endpoint to Ghost CMS. `test_code` hardcodes `REPO_DIR = "/workspace/Ghost"` and asserts on files under that path (e.g. `ghost/core/core/server/models/audit-log.js`).
- `docker pull zhangyiiiiii/swe-skills-bench-python` succeeded (digest `sha256:51d40310cdf44d00b3e383af1c4467bc460e6a3a25fedb1f9fab6a8d7b77b974`).
- Ran the image and inspected `/workspace` directly: it contains only a 61-byte `.claudignore` file (a generic build/`.git`/`node_modules` ignore list). **`/workspace/Ghost` does not exist.** `find / -iname "*audit-log*"` returns nothing. There is no git repository anywhere reachable in the container (`git log` at `/workspace/Ghost` fails with "not a git repository").
- Searched the image filesystem for any setup/clone/bootstrap script that might check out the repo at container start (`find / -iname "*setup*"`, `*entrypoint*"`): none reference Ghost, `repo_url`, or any clone step. The image environment is a bare Python 3.12 / Node 20 base with no task-specific content.
- **Conclusion: the image is a generic, task-agnostic execution environment shared across all Python-language SWE-Skills-Bench rows, not a per-task pre-built environment.** The actual repo checkout is expected to happen through a harness that is not present in either the HuggingFace dataset or the dead GitHub repository (Section 3.2 of this document already confirmed the repo 404s).

### 9.2 linkerd-patterns / zhangyiiiiii/swe-skills-bench-golang (fallback attempt)

- `docker pull zhangyiiiiii/swe-skills-bench-golang` succeeded (digest `sha256:08a709af3502f43282367befe0ae3ba641efe7300cf9d2295c01eb12564c6180`).
- Same inspection: `/workspace` contains only a `.claudignore` file. No `linkerd2` directory, no `.git` directory anywhere under `/`, confirmed via `find / -maxdepth 5 -iname ".git" -type d`.
- Identical pattern to the Python image: a generic language-runtime base image, not a task-specific one.

### 9.3 Is the repo_commit gap fatal? Yes, empirically confirmed.

This directly answers the open question from Section 3.2. The missing `repo_commit` field is not merely inconvenient metadata — it is fatal as distributed, for a concrete, checkable reason: **there is no repo checkout anywhere in the publicly available artifacts for this to pin.** The Docker images are bare runtime bases; the dataset provides only `repo_url` (no commit) and `test_code`; the harness that would clone `repo_url`, check out some commit, and run `test_code` against it lives in the paper's GitHub repository, which returns HTTP 404 (confirmed independently in the prior pass via both `curl` and the GitHub API). Reconstructing this would require writing a new clone-and-setup harness from scratch, guessing at which commit produces a fair (neither trivially passing nor unsatisfiable) task state — exactly the "extensive new infrastructure" the plan's Section 9 stop conditions say disqualifies a candidate.

### 9.4 Verdict on SWE-Skills-Bench as a corpus source

**Reject as a second source for this study, given only the currently public artifacts.** This is not a failure of this qualification pass — it is a correct, evidence-based exclusion, exactly analogous to how the prior audit correctly excluded `obspy-datacenter-client` for a dead link or `mesh-analysis` for unit ambiguity before this pass resolved it. If the authors later publish working harness code (the 404 could be resolved, e.g. a renamed or re-published repo), this source should be re-examined at that time. Until then, treat SkillsBench as the sole qualified corpus source and route the "the paper's own finding about version-mismatched guidance harming performance" citation (Section 3.4) into the paper's motivation/related-work only, not into the executed corpus.

### 9.5 Gate 0 bottom line after this pass

**Gate 0 does not pass.** What changed: SWE-Skills-Bench moved from "unqualified, second source pending" to "investigated and excluded, source diversity target not met from public data." The corpus that *can* be honestly claimed today is: 4 fully container-qualified SkillsBench candidates with real pass/fail discrimination (fuzzy-match, d3-visualization, dc-power-flow with a narrowed claim, mesh-analysis as a derived task), 1 conditionally-resolved candidate pending x86_64 re-verification (python-scala-collections), and 3 declared comparator/control-role candidates not yet container-tested (pymatgen, dialogue-graph, reflow-profile-compliance-toolkit) — all from one source.

**Smallest next step:** this is now a decision, not a task. Either (a) declare single-source SkillsBench sufficient, disclose it explicitly as a limitation, container-qualify the remaining 3 comparator/control candidates the same way as the top 4, and move to writing the pilot manifest — or (b) run one more, tightly timeboxed search for a genuinely reconstructible second source before doing so. Recommend (a): three qualification passes have already spent real effort chasing source diversity, two candidate second sources (SWE-bench, SWE-Skills-Bench) have been correctly ruled out with hard evidence, and the plan's literal pass condition does not require multiple sources — only its non-binding suggested target does. Further open-ended searching risks becoming the "open-ended corpus-building project" the plan explicitly warns against.

## 10. One final, bounded second-source search: no viable candidate found

This section applies the exact lesson from Section 9: a dataset or repo is only a real second source if the skill text, the task environment, and the verifier/oracle are *all* actually present and runnable at a live, checkable location right now — not described in a paper abstract or dataset card. Two leads were checked against that bar; both fail it, for different reasons than SWE-Skills-Bench's.

### 10.1 SkillsBench's own `tasks-extra` directory: real, but not independent

- Confirmed live via the GitHub API at the pinned commit (`9a1f4dd5f7659f75707435da3ce854b6e48321d1`): `tasks-extra/` contains 14 additional task directories (`cobol-gl-batch-reconcile`, `gh-repo-analytics`, `nda-playbook-review`, `taxonomy-tree-merge`, `speaker-diarization-subtitles`, and 9 others), each with its own `environment/skills/*/SKILL.md` subdirectories — same structure as the main `tasks/` tree the original audit screened.
- Fetched one sample directly (`gnucobol-mainframe-batch/SKILL.md`, a GnuCOBOL mainframe-batch skill under `cobol-gl-batch-reconcile`): it is a real, substantive, domain-specific skill (PIC clauses, signed-magnitude decimal handling, GnuCOBOL build flags) — genuinely different subject matter from the original 8 (invoices, D3, power flow, etc.).
- **Verdict: this extends domain diversity within SkillsBench but does not count as a second source.** It is the same repository, same authors, same generation/benchmark pipeline, and (based on the original audit's finding that six of eight shortlisted skills already shared one lexical diagnostic) very likely the same authoring conventions and defect distribution as the already-screened `tasks/` tree. The plan's concern in Section 6.1 of the prior audit ("not evidence of broad coverage... not a representative sample of all deployed skills") is about independence of authorship and pipeline, not directory location within one repo. Using `tasks-extra` would not address that concern; it would just be more SkillsBench.
- Useful as a **fallback replacement pool** within the existing single-source scope if any of the 3 remaining comparator/control candidates fail container qualification, since it offers unscreened, natural-warning candidates in new domains without needing new infrastructure. Not evaluated further in this pass — that would be corpus expansion, not second-source qualification, and is out of scope for this bounded search.

### 10.2 TiesPetersen/SkillBenchmark: fails the self-containment/verifier bar

- Live GitHub repo, confirmed via WebFetch. Contains `skills/`, `tasks/` (YAML task definitions), and a Python orchestration/scoring harness (`run.py`, `src/`).
- **Disqualifying findings, both independent of each other:**
  1. **No deterministic verifier.** It uses a blind LLM-judge scoring system (a second LLM scores skill-on vs. skill-off outputs against a rubric, blind to which is which) rather than an execution-based oracle. This is a fundamentally different evaluation paradigm than the plan requires (Section 8 of the research plan: "Write or adopt oracles before seeing arm outcomes... check that a valid reference artifact passes and relevant invalid artifacts fail" — a judge-based rubric cannot be pre-validated against a known-good/known-bad pair the way an execution oracle can, and introduces a second LLM's judgment as a confound directly into the primary outcome measure).
  2. **No task execution environment at all** — "single-turn prompt-in, response-out" against the raw Anthropic API, no Docker, no sandbox, no file-system or tool-use task. This does not match the plan's unit of study (Section 8: "a complete, pinned skill package; its intended environment... independently specified task instances").
  3. **Trivially small even if the paradigm were acceptable**: 1 example skill x 3 example tasks = 3 pairs, explicitly labeled as example content, not a corpus.
- **Verdict: rejected.** This is a different (and for other purposes possibly interesting) research tool, not a candidate corpus source for this study.

### 10.3 Final recommendation on source diversity: accept single-source SkillsBench

Four qualification passes (the original audit plus this document's Sections 2-3, 6-9, and this section) have now made a genuine, evidenced effort at source diversity: one source extended in depth (`tasks-extra` found but correctly excluded as non-independent), and three external candidates evaluated and rejected with concrete, checkable reasons (NVIDIA/skills has no tasks; MalSkillBench needs new eval scaffolding; SWE-bench has no skill layer; SWE-Skills-Bench's harness is a 404 with no self-contained repo checkout; SkillBenchmark has no deterministic oracle and is a 3-pair toy set). No further search is warranted — this was explicitly the last bounded attempt, and continuing would be exactly the open-ended corpus project Section 9 of the research plan prohibits.

**Recommendation: proceed with single-source SkillsBench, disclosed explicitly as a threat-to-validity / limitation in the eventual paper.** This is consistent with the plan's literal Gate 0 pass condition, which requires "a bounded runnable corpus" and does not hard-require multiple sources (only the non-binding Section 9 suggested target mentioned it). The next concrete step is container-qualifying the 3 remaining comparator/control candidates (`pymatgen`, `dialogue-graph`, `reflow-profile-compliance-toolkit`) the same way as the 4 already done, after which — modulo the still-open `python-scala-collections` x86_64 re-verification — Gate 0's corpus requirement would be fully satisfied and the remaining work becomes writing the pilot manifest and spending ceiling (the one Gate 0 checklist item not yet started at all).

## 12. Held-out task instances for the 4 primary candidates: constructed and validated

This section closes [PILOT_MANIFEST_2026-09-12.md](PILOT_MANIFEST_2026-09-12.md) Section 3's held-out-instance gap for the 4 fully-qualified primary candidates prioritized there. No LLM calls were used anywhere in this section — all ground truth was either hand-derived at construction time (and independently cross-checked by running the actual reference oracle) or computed directly from the constructed geometry/network. All artifacts are persisted at `SE4AgenticAI/held_out_instances/<task>/`, not left in ephemeral job scratch space.

**Validation caveat, stated plainly per the plan's Section 8 requirement:** these instances were built and checked by a single agent in one continuous pass. This is **not** the two-person validation the plan calls for ("have two team members validate their requirements and oracles before running agents"). A second reviewer must independently check each instance's construction and expected outcomes before it is used in any executed pilot episode. Nothing below should be read as satisfying that requirement — only as making the single-reviewer construction work available for that review.

### 12.1 fuzzy-match / invoice-fraud-detection: constructed and validated

Built a new instance with 10 distinct vendors, 10 POs, and 12 synthetic invoice pages (`generate.py`, `vendors.xlsx`, `purchase_orders.csv`, `invoices.pdf`), covering all 5 fraud categories plus two rule-priority edge cases (a case where Unknown Vendor coexists with bad IBAN/PO and must still win by rule order; a case where IBAN Mismatch coexists with Invalid PO and must win) and a legitimate fuzzy-match case (a vendor name with a real typo, "Bluewater Logistics Ltd" vs. registered "Bluewater Logistics", must NOT be flagged).

- Ground truth was hand-derived at construction time (`expected_ground_truth.json`), before running anything.
- Ran the actual oracle (`oracle/solve.sh`, unmodified) against the new PDF/xlsx/csv inputs in the existing `invoice-fraud-test` Docker image: its independent fraud determination **exactly matched** the hand-derived expectations for all 7 intended fraud cases and all 5 clean cases, including the fuzzy-match and both priority-order edge cases.
- Built the full `ground_truth.json` (fraud + "Clean" entries) matching the verifier's expected schema, ran the actual pytest verifier (`test_outputs.py`, unmodified): **2/2 tests passed** on the oracle's correct output.
- Ran the verifier again against a deliberately wrong output (`fraud_report.json` replaced with `[]`): `test_content` **correctly failed**, reporting all 7 missed fraud pages by number.
- **Conclusion:** genuine, non-trivial held-out instance (12 invoices vs. the original's count, entirely new entities/amounts, includes cases the original didn't specifically test — a real typo-tolerant fuzzy match and two priority-order conflicts). Not at floor or ceiling. Ready for pilot use pending second-reviewer check.

### 12.2 d3-visualization / data-to-d3: constructed and validated

Rather than substitute entirely different companies (which would require rewriting the verifier's hardcoded exact counts — 50 tickers, a specific 10-ticker ETF list, 5 sector names — a larger derived-verifier change than justified for this pass), constructed a held-out variant that keeps the original 50 tickers/10 ETFs/5 sectors (required by the verifier's hardcoded assertions) but **multiplicatively perturbs every market cap, employee count, and daily price/volume series by an independent random factor per ticker** (seeded, reproducible). This is genuinely different data under the same schema and contract, not a copy — every numeric value in the dataset changed — but is a narrower notion of "held-out" than a fully new company set; recorded here as a scope limitation, not concealed.

- Ran the actual oracle (`oracle/solve.sh`, unmodified, installs D3 v6.7.0 and builds the visualization from whatever CSVs are supplied) against the perturbed data: built cleanly.
- Ran the real Playwright verifier (`test_outputs.py`, unmodified) against the built output: **all 15 tests passed**, including bubble rendering, sector clustering, legend completeness, tooltips, and data integrity — confirming the oracle's HTML/JS generation is genuinely data-driven, not hardcoded to the original numbers.
- Ran the verifier against a deliberately broken output (`index.html` replaced with a stub, `visualization.js` deleted): **8 of 15 tests correctly failed** (missing legend, no bubble chart, no data table, broken tooltips, etc.).
- **Conclusion:** held-out instance validated, with the documented scope limitation (same tickers, perturbed values, not new companies) carried forward as a caveat for whoever runs the pilot. Ready for pilot use pending second-reviewer check.

### 12.3 dc-power-flow / energy-market-pricing: constructed and validated, with a required oracle-compatibility fix documented

The oracle's `solve.sh` **hardcodes** the scenario line as bus 64 -> bus 1501 (`SCENARIO_FROM_BUS = 64`, `SCENARIO_TO_BUS = 1501`) and raises `ValueError` if that exact bus pair is not found as a branch — this is a real constraint on any held-out network, not something this pass introduced. Constructed a minimal 3-bus network (`network.json`) using bus numbers 1 (slack), 64, and 1501 specifically so the oracle's hardcoded scenario applies: a cheap generator at bus 1 (marginal cost $20/MWh) reaches load at bus 1501 only through bus 64, and the 64->1501 line is deliberately capacity-constrained (80 MW) below what the cheap generator would otherwise supply, forcing a more expensive local generator at bus 1501 (marginal cost $60/MWh) to cover the shortfall — engineered so the scenario (raising that line's limit 20%) produces a genuine, non-trivial cost reduction, not a no-op.

- Hand-computed the expected dispatch before running anything: base case cost $5,800/hr (80 MW cheap + 70 MW expensive), counterfactual cost $5,160/hr (96 MW cheap + 54 MW expensive), cost reduction $640/hr.
- Ran the actual oracle (`oracle/solve.sh`, unmodified, independently solves via `cvxpy`) against the new network: **reproduced the hand-computed costs exactly** ($5,800.00 and $5,160.00, cost reduction $640.00), and its own binding-line detection correctly identified the 64->1501 line as binding at exactly its rated limit in both cases — independent confirmation the topology was constructed as intended.
- Ran the real verifier (`test_outputs.py`, unmodified) against the oracle's `report.json`: **all 4 tests passed** (schema, internal consistency, near-optimal cost, non-negative cost reduction).
- Ran the verifier against a deliberately corrupted report (base-case cost inflated 50%): **2 of 4 tests correctly failed** (internal consistency: "Cost reduction 640.0 != computed 3540.0"; near-optimal: "base_case cost 8700.0 exceeds optimal 5799.99... by more than 0.0100%").
- **Conclusion:** held-out instance validated under the manifest's narrowed claim (total cost and internal consistency only, not individual LMPs or binding-line identification — this instance's LMP values are themselves numerically degenerate, in the tens/hundreds of thousands of dollars per MWh, an artifact of the network's small scale, reinforcing why LMPs are correctly excluded from the measured claim). Ready for pilot use pending second-reviewer check.

### 12.4 mesh-analysis / 3d-scan-calc: constructed and validated as a derived task with a derived verifier

Per the manifest's requirement to pin one unit convention, constructed a binary STL (`scan_data.stl`, hand-written via `struct`, not copied from the original) containing a 10 x 10 x 5 cm steel box (material ID 10, density 7.85 g/cm^3, volume 500 cm^3 by construction) as the main part, plus a tiny geometrically separate debris tetrahedron (material ID 1, volume ~0.00017 cm^3) to give the largest-connected-component filter something real to discard. Coordinates are written directly in centimeters (the pinned convention), and a derived `task.md` explicitly states this ("All coordinates in the STL file are in centimeters").

- Independently computed the expected volume (500 cm^3, via the same signed-tetrahedron formula the oracle uses) before running anything; confirmed the debris tetrahedron's volume is negligible by comparison.
- Ran the actual oracle (unmodified, `oracle/solve.sh`) against the new STL: correctly identified the box as the largest component (not the debris), material ID 10, volume 500.0, mass 3925.0 — **exact match** to the independent hand computation.
- Wrote a **derived verifier** (`verifier/test_outputs.py`, based on the original but with the dual cm/mm accept logic removed, replaced with a cm-only check and an explanatory comment pointing at this document) — this is the concrete fix the manifest called for, published explicitly as a derived artifact rather than silently patched.
- Ran the derived verifier against the oracle's correct output: **both tests passed.**
- Ran the derived verifier against the exact value the *original, unpatched* verifier would have accepted under its mm-convention branch (3925.0 / 1000 = 3.925): **correctly failed** — `"Mass mismatch. Expected ~3925.00 (cm convention, pinned by task.md), got 3.92"` — direct, empirical proof that the derived verifier closes the ambiguity the original one could not.
- **Conclusion:** held-out instance and its derived verifier both validated. This is the strongest evidence in this pass that a documented derived-task modification actually fixes the flagged problem, not just papers over it. Ready for pilot use pending second-reviewer check.

### 12.5 Remaining candidates: not attempted in this pass

`pymatgen`, `dialogue-graph`, and `reflow-profile-compliance-toolkit` (comparator/control roles) do not yet have held-out instances. This was scoped out of this pass to prioritize the 4 primary candidates per the manifest; each has a documented construction requirement in `PILOT_MANIFEST_2026-09-12.md` Section 3 (held-out CIF structures by family for `pymatgen`; a held-out dialogue satisfying the verifier's fixed narrative-ID expectations for `dialogue-graph`; pre-specified numerical outputs restricted to Q01-Q04 for `reflow-profile-compliance-toolkit`). `python-scala-collections` remains out of scope, gated on the x86_64 re-verification.

### 12.6 Updated Gate 0 / manifest status

All 4 fully-qualified primary candidates (`fuzzy-match`, `d3-visualization`, `dc-power-flow`, `mesh-analysis`) now have a validated held-out instance with real, executed pass/fail discrimination — the single largest open item in the pilot manifest's Section 10 remaining-gate list. What is still open before Gate 0 can be declared passed and Phase 3 can begin: second-reviewer validation of these 4 instances (single-reviewer only so far), held-out instances for the remaining 3 candidates, repair generation (L/G) with its own second-review step, the calibration run, model selection, and the practical-significance margin — items 1-6 of the manifest's Section 10, now partially addressed rather than fully open.

## 11. Container-qualifying the final 3 candidates: all resolved, two new findings

Using the same pinned SkillsBench commit (`9a1f4dd5f7659f75707435da3ce854b6e48321d1`, already checked out; task directories for these 3 were extracted fresh from the retained tarball since only the top-4 directories had been kept from earlier passes). Real Docker builds, real oracle runs, real deliberate corruption, no LLM calls, for all three.

### 11.1 pymatgen / crystallographic-wyckoff-position-analysis: RESOLVED

- Read `verifier/test_outputs.py` (131 lines) in full: `main()` unconditionally `return`s 0, and `verifier/test.sh` unconditionally `exit 0` regardless of `TEST_EXIT_CODE`. Confirms the prior audit's static read exactly: **exit code carries no information; only `/logs/verifier/reward.txt` does.**
- Built `environment/Dockerfile` (`python:3.12-slim` + pinned `pymatgen==2025.10.7`, `sympy==1.14.0`): succeeded.
- Ran `oracle/solve.sh` then the verifier against all 11 CIF files: **11/11 passed, `reward.txt` = 1.00, exit code 0.**
- Deliberately corrupted 2 of 11 results (wrong multiplicity for `FeS2_mp-226.cif`, wrong coordinate for `C_mp-169.cif`) by monkey-patching the solution function's output for those two files only, then re-ran the verifier: **9/11 passed, `reward.txt` = 0.82, exit code 0**, with real per-file diff output (`Expected: {...} / Got: {...}`) for each of the two corrupted cases. The other 9 files, untouched, correctly still passed — confirming scoring is genuinely per-file, not an aggregate trap.
- **Conclusion:** the verifier discriminates real correctness per file and reports it faithfully in `reward.txt`. The only operational requirement (already flagged in the original dossier) is that the study's scoring pipeline must read `reward.txt`, never the process exit code.

### 11.2 dialogue-graph / dialogue-parser: RESOLVED, with a new reward-granularity finding

- Read `verifier/test.sh`: same unconditional-`exit 0` pattern, with `reward.txt` populated from a CTRF-parsed pytest summary (`passed / total` test-group counts).
- Built `environment/Dockerfile` (`python:3.12.8-slim` + `graphviz`): succeeded.
- Ran `oracle/solve.sh` (the reference implementation falls back to an inline `Node`/`Edge`/`Graph` implementation when the bundled skill module isn't importable — confirmed self-contained, not dependent on skill presence) then the verifier: **all 35 individual pytest assertions passed** (6 parametrized test functions: system basics, narrative content incl. the fixed IDs the audit flagged — `Start`, `TavernChoice`, `Kira`, etc. — graph logic/reachability, DOT visualization validity, content integrity, structural integrity), `reward.txt` = 1.0.
- Deliberately corrupted the oracle's `dialogue.json` (removed all nodes with speaker `Kira`, dropped the required `TavernChoice`→`StrangerApproach` edge) and re-ran the verifier: **5 of 35 individual assertions correctly failed** (missing speaker, invalid edge reference, broken branching, a dependent content-integrity check, the specific structural-integrity pair) with real assertion messages, 30/35 still passed.
- **New finding, not in the prior static audit:** the CTRF-derived `reward.txt` score does not reflect the 35 fine-grained assertions — it collapses to the **6 parametrized test-function groups**, and `reward.txt` reported **0.333** (2/6 groups fully clean) despite the raw assertion pass rate being 30/35 = 0.857. A single failing case inside a parametrize group zeros out that entire group's contribution to the reward. **This means the reward signal, as computed by the task's own `test.sh`, is much coarser and more punitive than the underlying checks, and a repair that only partially fixes a failing group is invisible to `reward.txt`.** If the study relies on `reward.txt` as its outcome measure for this candidate, it should be aware the resolution is 6 buckets, not 35 assertions; capturing pytest's own pass/fail detail directly (rather than only the CTRF summary) would give a finer-grained supplementary signal.
- **Conclusion:** oracle and verifier are real and functional, correctly reject a genuinely broken dialogue graph. Usable as-is, with the granularity caveat recorded above.

### 11.3 reflow-profile-compliance-toolkit / manufacturing-equipment-maintenance: RESOLVED WITH A NARROWED CLAIM, plus a confirmed environment gap

- Confirmed the flagged PDF-dependency concern is real: `environment/data/handbook.pdf` exists and the skill's own SKILL.md explicitly instructs, "Extract numeric limits / temperature regions / timing windows / margins / feasibility rules from handbook.pdf" — but `environment/Dockerfile` installs only `pandas==2.2.3` and `pytest==8.4.1`, no PDF-reading library (no `pdfplumber`, `PyPDF2`, `pymupdf`) and no `pdftotext` binary. The oracle itself (`oracle/solve.sh`, 265 lines, no mention of "pdf" anywhere) never actually parses the PDF — the reference solution hardcodes handbook-derived thresholds directly. **This is a real environment-completeness gap that would only surface when an actual agent (not the oracle) is asked to read the handbook**: the task environment as distributed does not equip an agent to do what its own skill instructs. Record this as a pilot-environment requirement (install a PDF-reading tool before running any agent episode on this candidate), not a blocker to oracle qualification itself.
- Built `environment/Dockerfile`: succeeded.
- `verifier/test.sh` uses a **binary** reward (unlike pymatgen/dialogue-graph's fractional scores): `echo 1 > reward.txt` only if the full pytest run exits 0, else `echo 0`.
- Ran the oracle, then the verifier on the unmodified reference output: **7/7 pytest tests passed** (`test_L0_required_outputs_exist_and_parse`, `test_Q01_preheat_ramp_rate_loose`, `test_Q02_tal_loose`, `test_Q03_peak_loose`, `test_Q04_conveyor_loose`, `test_Q05_best_run_per_board_family_loose`, `test_minimal_schema_guards_loose`), `reward.txt` = 1.
- **Confirmed the prior audit's Q05 looseness concern empirically, not just by reading source.** Read `test_Q05_best_run_per_board_family_loose` in full: it only checks that `best_run_id` is present, is a member of the correct `board_family`'s run list, and is excluded from the runner-up list — it never checks that the selected run is actually numerically best by any of the task's own criteria (ramp rate, TAL, peak deviation). Empirically swapped the oracle's genuinely-best `Compute_IO` run (`R0002`) for one of its own listed runner-ups (`R0011`, moved into the runner-up list in `R0002`'s place) and re-ran the verifier: **all 7 tests still passed, `reward.txt` = 1** — a demonstrably wrong "best run" selection is invisible to this oracle.
- To confirm the verifier isn't simply toothless everywhere, separately corrupted Q01's `violating_runs` list (removed a genuinely ramp-violating run, `R0018`) and re-ran: **`test_Q01_preheat_ramp_rate_loose` correctly failed** with real assertion output, and because the reward is binary, the overall `reward.txt` dropped to 0. So the verifier does catch genuine content errors in Q01-Q04 and schema — the looseness is specific to Q05's best-run selection, not systemic.
- **Conclusion:** usable, but with an explicit narrowed claim, the same pattern as `dc-power-flow`: **do not credit any repair with improving "best run" identification accuracy** — Q05 cannot discriminate a correct best-run pick from an incorrect one as long as it's schema-valid, so any observed L-vs-O effect isolated to that field would be a verifier artifact. Q01-Q04 and schema checks remain valid, discriminating outcome measures. Also carry forward the PDF-tooling gap as a required environment fix before any agent episode is run on this candidate.

### 11.4 Updated Gate 0 status (supersedes Section 8)

| Item | Status |
|---|---|
| Recheck closest papers for newer versions/artifacts | Not done in any pass |
| Inspect detector definitions and candidate linter implementations | Done |
| Map promising rules to pinned spec/authoring sources | Done |
| Find complete original packages with natural warnings and existing tasks | Done, single source, accepted (Sections 6, 9, 10) |
| Demonstrate candidate environments build and reset | **All 8 of 8 SkillsBench candidates now attempted. 7 of 8 fully confirmed by execution** (fuzzy-match, d3-visualization, dc-power-flow, mesh-analysis, pymatgen, dialogue-graph, reflow-profile-compliance-toolkit). **1 of 8 (python-scala-collections) qualified by static control-flow analysis only, blocked empirically by this machine's CPU architecture** — needs re-verification on native x86_64 infrastructure. |
| Exercise reference solutions/oracles without an LLM, including deliberately-wrong-output rejection | **Done for the same 7 candidates**, each with a real passing run and at least one real rejected deliberately-broken run. `dc-power-flow` and `reflow-profile-compliance-toolkit` carry an explicit narrowed claim (specific fields the oracle cannot discriminate); `dialogue-graph` carries a noted reward-granularity caveat. Not done for `python-scala-collections`. |
| Establish sampling frame, document inclusion/exclusion | Done |
| Determine baseline feasibility beyond compression alone | Done — `pymatgen` remains the one compression comparator; the other 6 qualified candidates are distinct mechanisms |
| Write pilot manifest, spending ceiling, decision rules | **Not done — this is now the only unstarted Gate 0 checklist item.** |

### 11.5 Does Gate 0 pass now?

**Not yet, but the corpus-qualification portion of Gate 0 is now functionally complete.** Re-reading the plan's Section 9 pass condition literally — "a distinct question, a bounded runnable corpus, meaningful natural repairs, independent evaluation, and feasible comparisons" — every element except the manifest is now backed by real, executed evidence:

- **Distinct question:** unchanged from the outset, backed by the P2 future-work gap.
- **Bounded runnable corpus:** yes — 7 of 8 candidates fully container-qualified with proven pass/fail discrimination; the 8th is conditionally qualified pending hardware, not corpus-blocked.
- **Meaningful natural repairs:** yes — R/T/C diagnostics fire on real, unmodified skill text across all 8 candidates, mapped to pinned specification/authoring sources.
- **Independent evaluation:** yes — every qualified candidate's oracle has been shown, by actual execution, to accept correct output and reject at least one deliberately incorrect output, with three explicit, evidence-based scope narrowings recorded (`dc-power-flow`, `reflow-profile-compliance-toolkit` Q05, `dialogue-graph` granularity) rather than concealed.
- **Feasible comparisons:** yes — O/L/G/N arms are structurally feasible for all 7 fully-qualified candidates; nothing found in this pass suggests otherwise.

**What remains is not corpus work — it is writing the pilot manifest itself**: the frozen editing/execution protocol, exact model(s) and episode/dollar budget, the O/L/G/N repair-generation procedure with its access restrictions, and the predeclared decision rules for benefit/harm/null outcomes (the three paths in the research plan's Section 10). Once that document exists and is reviewed, Gate 0 as defined by the plan can be formally declared passed. `python-scala-collections`'s x86_64 re-verification can proceed in parallel or be scheduled as a pilot-day prerequisite; it does not block manifest-writing.

## 13. python-scala-collections: x86_64 re-verification closed out (2026-09-13)

The pilot manifest ([PILOT_MANIFEST_2026-09-12.md](PILOT_MANIFEST_2026-09-12.md)) called for empirical confirmation of `sbt`/`scalac` installation and fail-closed behavior on native x86_64, since this development machine's Apple Silicon + QEMU emulation could not run coursier's Scala toolchain installer. The user set up a GitHub Actions workflow (`.github/workflows/qualify-python-scala.yml`, `ubuntu-latest` runner, genuinely x86_64) that: sparse-checks out the pinned SkillsBench commit's `tasks/python-scala-translation` directory, builds `environment/Dockerfile` with `environment/` as build context (the first workflow draft used the task root as context and failed — the Dockerfile's `COPY` sources all live under `environment/`, confirmed via the GitHub tree API before fixing), copies `oracle/solve.sh` and `verifier/{test.sh,test_outputs.py}` into a running container the same way the real SkillsBench harness does (these are not baked into the image), and runs the verifier against both the correct and a deliberately corrupted submission.

**Correct submission**: coursier's `cs setup --yes` step (already present in the Dockerfile) confirmed to install `sbt`, `sbtn`, `scala`, `scalac`, `scalafmt`, `scala-cli`, and `ammonite` as its default toolset — resolving the open question from Section 7.2 about whether `sbt` is ever actually present. `which sbt` and `which scalac` both resolved to `/root/.local/share/coursier/bin/`. Compilation succeeded, `sbt test` ran all 10 `TokenizerSpec` cases, all 10 passed, `reward.txt = 1`, harness status `PASSED`.

**Deliberately corrupted submission**: appended invalid Scala syntax to the generated `Tokenizer.scala`. Compilation failed with a real compiler error at the injected line, tests were correctly skipped as a consequence ("Skipping tests (sbt not available or compilation failed)" — here specifically because compilation failed, not because `sbt` was missing, confirmed by the correct-submission run immediately above), `reward.txt = 0`, harness status `NEEDS IMPROVEMENT` — despite an unrelated 25/25 (100%) cosmetic code-quality score on the same broken file. This is real, executed confirmation of the control-flow trace in Section 7.2: `results["passed"]` is forced `False` whenever tests are skipped, regardless of the quality-criteria score.

**Conclusion: `python-scala-collections` is now fully qualified**, on the same footing as the other 7 candidates. The machine-architecture blocker is resolved. This closes item 1 of the pilot manifest's Section 10 remaining-gate list. `python-scala-collections` still lacks a constructed held-out instance (Section 3 of the manifest) — that remains open, same as it does for `pymatgen`, `dialogue-graph`, and `reflow-profile-compliance-toolkit`.
