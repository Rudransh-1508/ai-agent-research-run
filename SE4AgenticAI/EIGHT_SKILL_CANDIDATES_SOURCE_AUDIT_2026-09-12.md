# Eight candidate skills for the lint-repair behavioral study

Date: 12 September 2026

Status: **Source-screened shortlist, not an approved experimental corpus. No behavioral pilot or container qualification has passed in this audit.**

Companion proposal: [Research plan](SKILL_REPAIR_BEHAVIORAL_VALIDITY_RESEARCH_PLAN_2026-09-12.md).

## 1. Decision

The best first candidate to qualify is **fuzzy-match**, followed by **d3-visualization**. The table below identifies eight distinct packages worth considering, with different experimental roles. It does not claim that eight runtime-ready, substantively defective skills have been found.

Five are candidates for execution-facing reliability-guidance repairs. One is a compression comparator. Two are boundary controls, useful precisely because their warnings may not identify missing operational guidance.

**Do not freeze these eight as the entire main study yet.** Three substantive candidates have specific verifier or environment problems. All eight come from one benchmark distribution, and six share one keyword-based diagnostic. This is a useful starting shortlist, but not evidence of broad coverage across linters, warning families, or production skill authors.

| Priority | Target skill | Paired SkillsBench task | Intended role | Main qualification issue |
|---|---|---|---|---|
| 1 | `fuzzy-match` | `invoice-fraud-detection` | Matching reliability guidance | Establish a legitimate repair beyond existing no-match handling; audit independent labels |
| 2 | `d3-visualization` | `data-to-d3` | Data-loading and rendering validation guidance | Stabilize browser tests; keep version-conflict repair separate |
| 3 | `dc-power-flow` | `energy-market-pricing` | Numerical input and solver-validation guidance | Existing verifier does not validate all claimed physical/economic outputs |
| 4 | `python-scala-collections` | `python-scala-translation` | Behavioral-equivalence and edge-case guidance | Compiler fallback and grading logic need qualification |
| 5 | `mesh-analysis` | `3d-scan-calc` | Binary-input and output-validation guidance | Resolve a factor-of-1,000 unit ambiguity before use |
| 6 | `pymatgen` | `crystallographic-wyckoff-position-analysis` | One compression/progressive-disclosure comparator | Exact-answer conventions, task-specific references, and score handling |
| 7 | `dialogue-graph` | `dialogue-parser` | Documentation-format boundary control | Do not pretend a missing table means the API is undocumented |
| 8 | `reflow-profile-compliance-toolkit` | `manufacturing-equipment-maintenance` | Suspected false-positive reliability control | Existing failure guidance; permissive parts of the task verifier |

Priority means order for qualification, not estimated effect size or probability of producing publishable results. A control is not a substitute for another substantive repair family.

## 2. What was actually checked

### Pinned sources

- [SkillsBench](https://github.com/benchflow-ai/skillsbench/tree/9a1f4dd5f7659f75707435da3ce854b6e48321d1), commit `9a1f4dd5f7659f75707435da3ce854b6e48321d1`.
- [NVIDIA SkillEvaluator](https://github.com/NVIDIA/SkillEvaluator/tree/7e189c6bdada8910dfa1684f25feedca87f2db85), commit `7e189c6bdada8910dfa1684f25feedca87f2db85`.
- [Agent Skills specification](https://agentskills.io/specification), consulted to distinguish format requirements from recommendations and intended-environment requirements.

The SkillsBench checkout was sparse, but **all tracked files under the task skill directories were fetched**, not just SKILL.md files. Task definitions, Dockerfiles, and selected verifier sources were also fetched. Most task input datasets were not downloaded. A complete tracked skill directory is not proof that every referenced external resource or runtime dependency is available.

### Completed

1. Inventoried 232 `tasks/*/environment/skills/*/SKILL.md` copies, representing 202 distinct instruction-file contents by SHA-256. These are not 202 independent authors or 202 independently validated packages.
2. Ran the actual SkillEvaluator quality validator across those 232 copies.
3. Ran its actual dead-link check across the complete downloaded package directories.
4. Read the eight shortlisted SKILL.md files, their task definitions and Dockerfiles, and relevant verifier code. This was not a line-by-line audit of every bundled script and every test dependency.
5. Re-ran the relevant diagnostics on the shortlisted packages and recorded their names and severities.
6. Checked local Docker availability, but did not build or run these task containers.
7. Recorded package fingerprints below.

No LLM repair calls, agent task episodes, or task-script executions were performed. The static checker was run in an isolated `uv` environment with `--no-project --no-env-file`. No project credentials were loaded.

### Important limitations of the screen

- This was a broad screen within one runnable benchmark source, not an exhaustive search of every public skill repository.
- The 232-file inventory excludes `tasks-extra` and does not establish prevalence in the wider skill ecosystem.
- Repeated copies were not treated as distinct main-study subjects.
- No claim of a true defect follows merely from a diagnostic firing.
- No claim that a repair helps follows from the existence of a plausible failure mechanism.

## 3. Exact diagnostic families

Source: [quality_score.py](https://github.com/NVIDIA/SkillEvaluator/blob/7e189c6bdada8910dfa1684f25feedca87f2db85/src/skillevaluator/validators/quality_score.py).

### R: Reliability-language diagnostic

- `check_name`: `quality_reliability`
- Message: `No mention of error handling or validation`
- Emitted severity: **low**
- Recommendation: document expected errors and their handling.
- Fires on shortlist entries 1-5 and 8.

This is a lexical heuristic. The implementation searches for terms such as error, exception, invalid, failure, and validation in the document. It does not infer whether the instructions already describe robust behavior. Statistical uses of "error" can suppress it, while substantive instructions phrased as "sanity checks" or "missing data" may not.

Consequently, the six occurrences are **six package instances of one advisory rule**, not six independent kinds of authoring defect. A repair could remove the warning merely by adding a word. That possibility is central to qualification, not something to conceal.

### T: Script-documentation format diagnostic

- `check_name`: `quality_correctness`
- Message: `No documented scripts in table format`
- Emitted severity: **medium**
- Suggested representation: an Available Scripts table with script, purpose, and arguments.
- Selected as the intervention for `dialogue-graph` only.

The name of the checker dimension does not establish that a package is functionally incorrect. A Python library can already have adequate prose and API examples without this table.

### C: Instruction-size diagnostic

- `check_name`: `quality_efficiency`
- Emitted severity: **high**
- `pymatgen` is estimated by this checker at **5,271 tokens**, above its recommended 5,000-token threshold.
- Recommendation: keep the body concise and move detailed examples or documentation into references.

This is the checker's approximate token estimate, not a measurement from the execution model's tokenizer. This candidate overlaps directly with compression and progressive-disclosure prior art and must not carry the novelty claim.

### Findings deliberately not used as primary interventions

- Missing `version`, `metadata.author`, tags, or Purpose headings.
- Missing prerequisites headings when dependencies are already documented elsewhere.
- The checker's suggestion to add `run_script()` examples when that API is not available in the intended host.
- Removing installation instructions from a skill whose job includes setup.
- Treating every platform-specific path as wrong in its intended platform.

In particular, agnix's inspected CC-SK-021 user-home rule does not match `/root/.claude/skills/...`. I did not execute agnix, and do not attribute that finding to it.

## 4. Candidate dossiers

### 1. fuzzy-match: first qualification priority

[Package](https://github.com/benchflow-ai/skillsbench/tree/9a1f4dd5f7659f75707435da3ce854b6e48321d1/tasks/invoice-fraud-detection/environment/skills/fuzzy-match) | [Task and verifier](https://github.com/benchflow-ai/skillsbench/tree/9a1f4dd5f7659f75707435da3ce854b6e48321d1/tasks/invoice-fraud-detection)

**What it does:** normalizes entity names and uses containment, difflib, or RapidFuzz to reconcile records. The task combines invoices, a vendor spreadsheet, and purchase orders to identify fraudulent invoices.

**Verified finding:** R, low severity. This is a one-file package with an MIT declaration.

**Why promising:** matching decisions feed a concrete output with both false-positive and false-negative consequences. The verifier checks fraudulent versus clean pages, reasons, account identifiers, purchase orders, and amounts against a separate ground-truth file. It is more informative than checking whether the agent wrote a plausible narrative.

**Repair boundary:** the original already allows `None` when no fuzzy match is found. Do not claim it completely lacks no-match handling. A legitimate reliability repair could explain how to handle ambiguous candidates or unusable inputs without silently selecting a wrong entity. It must not insert vendor-specific answers, invent a fraud policy, or tune thresholds against the held-out labels.

**Qualification tasks:** first use the original invoice task. A second, independently constructed invoice/vendor instance should preserve the same explicit business rules while changing entities, amounts, and matching cases. Do not create only adversarial cases selected to reward the repair.

**Controls and risks:** retain the supporting `pdf` and `xlsx` packages unchanged. Independently audit the fraud labels and reason precedence. Keep the matching library and version identical across arms. Check that any benefit is not simply extra task-specific policy added by the editor.

**Verdict:** strongest starting candidate, not yet a passed pilot subject.

### 2. d3-visualization: strongest interactive-output candidate

[Package](https://github.com/benchflow-ai/skillsbench/tree/9a1f4dd5f7659f75707435da3ce854b6e48321d1/tasks/data-to-d3/environment/skills/d3-visualization) | [Task and verifier](https://github.com/benchflow-ai/skillsbench/tree/9a1f4dd5f7659f75707435da3ce854b6e48321d1/tasks/data-to-d3)

**What it does:** guides offline D3 visualizations with deterministic data handling, tooltips, and linked selections. The package includes four JavaScript resources alongside its instructions.

**Verified finding:** R, low severity.

**Why promising:** the verifier uses a real Playwright browser rather than only searching generated source. The task has checkable output behavior: stock bubbles, a table, sector grouping, tooltips, and linked selection. This permits studying whether extra validation guidance changes actual execution, unnecessary work, or correctness.

**Repair boundary:** document appropriate checks and responses for data-loading or rendering failures. Do not redesign the visualization, change the requested features, or add the verifier's selector expectations to the skill.

**Important confound:** the task and description specify D3 v6, while the body recommends v7.9.0 by default. That is a real textual inconsistency, but **the selected reliability diagnostic does not identify it**. Do not quietly bundle a version correction into the lint repair and attribute its effects to R.

**Qualification tasks:** original supplied stock dataset, then a held-out dataset with the same schema and interaction contract. Pin D3, Playwright, Chromium, and viewport. Test browser repeatability and ensure actual interactions, not just artifact existence, determine success. Preserve the relevant data-license notices.

**Verdict:** good candidate, subject to browser stability and scope checks.

### 3. dc-power-flow: strong numerical mechanism, incomplete existing oracle

[Package](https://github.com/benchflow-ai/skillsbench/tree/9a1f4dd5f7659f75707435da3ce854b6e48321d1/tasks/energy-market-pricing/environment/skills/dc-power-flow) | [Task and verifier](https://github.com/benchflow-ai/skillsbench/tree/9a1f4dd5f7659f75707435da3ce854b6e48321d1/tasks/energy-market-pricing)

**What it does:** constructs susceptance matrices and computes DC power flows using bus mappings, slack buses, and per-unit conversions. A Python matrix-building script is bundled.

**Verified finding:** R, low severity. Other script-related findings exist, but should not be combined into the same intervention.

**Why promising:** the procedure has explicit numerical assumptions and verifiable consequences. Input and solver checks could prevent silent misuse, but overly broad checks could also reject legitimate cases or add unnecessary work.

**Repair boundary:** clarify existing model assumptions and how to detect/report unusable inputs or unsuccessful calculations. Preserve executable scripts and mathematical semantics. Do not create an islanded or infeasible network solely because a proposed repair handles it; the task contract must define what should happen first.

**Oracle concern:** the verifier independently solves for optimal costs, which is useful. However, its output checks do not establish all physical-feasibility or price claims. It explicitly avoids comparing individual LMPs and binding-line sets, and its feasibility section checks reported internal consistency. A passing report is not proof that every requested economic result is correct.

**Qualification tasks:** original network plus a pre-specified second network/scenario. Decide before runs whether to restrict the measured claim to the independently verified quantities or strengthen the oracle using valid optimality/feasibility conditions. Do not require one unique dispatch or price vector when multiple valid optima exist.

**Environment:** the Dockerfile installs Python but not the full numerical stack. Freeze agent and verifier dependencies, including the solver, before comparison. Keep `economic-dispatch`, `locational-marginal-prices`, and `power-flow-data` fixed.

**Verdict:** conditional. Do not approve on the basis of the current aggregate pass signal alone.

### 4. python-scala-collections: useful semantics candidate with a grading blocker

[Package](https://github.com/benchflow-ai/skillsbench/tree/9a1f4dd5f7659f75707435da3ce854b6e48321d1/tasks/python-scala-translation/environment/skills/python-scala-collections) | [Task and verifier](https://github.com/benchflow-ai/skillsbench/tree/9a1f4dd5f7659f75707435da3ce854b6e48321d1/tasks/python-scala-translation)

**What it does:** translates Python collection operations into Scala. The paired task translates a tokenizer while preserving behavior and following Scala conventions.

**Verified finding:** R, low severity.

**Why promising:** behavior preservation has concrete edge cases involving absent values, empty collections, reduction, mutation, and types. The skill already mentions missing map keys and Option, so "no error handling anywhere" would be an inaccurate interpretation of the warning.

**Repair boundary:** provide general validation and edge-case guidance without adding answers from the tokenizer tests or changing the requested behavior. Preserve examples unless their modification is explicitly within the selected warning's scope.

**Grading blocker:** the inspected verifier can mark compilation successful when no Scala compiler is available. Its `scalac` fallback also reuses a path variable that has been changed to `build.sbt`. Other scoring uses source-pattern checks. These code paths were inspected, not reproduced. Do not equate the aggregate grading score with tested semantic equivalence.

**Qualification tasks:** require an actual pinned Scala toolchain and successful executed tests, with fail-closed behavior if tools are missing. Test outputs should be compared against Python behavior on held-out inputs. The Dockerfile downloads an x86-64 coursier binary, so architecture compatibility must be checked on the intended machine. Supporting translation skills stay fixed.

**Verdict:** promising subject, but held pending compiler/test qualification. Drop it if adopting it requires rebuilding a substantial evaluation system.

### 5. mesh-analysis: compact package, blocked by unit ambiguity

[Package](https://github.com/benchflow-ai/skillsbench/tree/9a1f4dd5f7659f75707435da3ce854b6e48321d1/tasks/3d-scan-calc/environment/skills/mesh-analysis) | [Task and verifier](https://github.com/benchflow-ai/skillsbench/tree/9a1f4dd5f7659f75707435da3ce854b6e48321d1/tasks/3d-scan-calc)

**What it does:** parses binary STL, selects the largest connected component, reads its material ID, and calculates mass using a supplied density table. It bundles `mesh_tool.py`.

**Verified finding:** R, low severity. The script-table finding also fires but is not the proposed primary intervention.

**Why promising:** a small package and deterministic geometric outputs make attribution and independent checking relatively tractable. Different meshes can provide a held-out instance without requiring a live service.

**Critical blocker:** the current verifier accepts both a mass calculated from cubic centimeters and one divided by 1,000 for cubic millimeters. The instruction text does not settle that convention. The skill itself explicitly says not to assume units. Therefore, an apparent repair gain or loss could be an oracle artifact.

**Repair boundary:** explain checks for binary input completeness, a usable component, and a valid material lookup within the declared input contract. Do not expand the skill into a universal mesh-repair system. Do not count fixing the experiment's unit ambiguity as a treatment effect.

**Qualification tasks:** specify units in the task equally for all arms, independently compute the expected mass, and reject the wrong-scale answer. Use a second valid mesh with known volume and material. If tasks are modified, publish them as derived instances rather than unchanged SkillsBench results.

**Controls:** make the identical helper script available in all conditions, including no-guidance. Resolve its installation path before randomization, without silently repairing only the original or only the revised condition.

**Verdict:** do not run until the unit convention is settled.

### 6. pymatgen: one explicit compression comparator

[Package](https://github.com/benchflow-ai/skillsbench/tree/9a1f4dd5f7659f75707435da3ce854b6e48321d1/tasks/crystallographic-wyckoff-position-analysis/environment/skills/pymatgen) | [Task and verifier](https://github.com/benchflow-ai/skillsbench/tree/9a1f4dd5f7659f75707435da3ce854b6e48321d1/tasks/crystallographic-wyckoff-position-analysis)

**What it does:** documents materials-science workflows and bundles scripts and references. The benchmark task asks for a callable function deriving Wyckoff multiplicities and representative coordinates from CIF files.

**Verified finding:** C, high severity, approximately 5,271 tokens under this checker's estimator. The package contains ten files and declares MIT licensing and K-Dense authorship.

**Why include:** it anchors the study against an already-studied intervention class: making a long skill shorter or moving detail into references. It should help distinguish new repair-specific evidence from a repetition of compression results.

**Repair boundary:** preserve general capabilities and references, with no task-answer-driven pruning. The package already contains a task-relevant `wyckoff-positions-from-cif.md` reference and a direct instruction to use a particular API. Record this benchmark adaptation; do not portray it as a pristine, unmodified production skill.

**Qualification tasks:** the existing task tests 11 CIF files. Split held-out evaluation by pre-specified structures or structure families, not by repeated calls to the same file. Freeze coordinate conventions and library versions. Audit exact dictionary/string expectations for scientifically equivalent outputs.

**Score handling:** the verifier returns process exit code zero even when individual cases fail, and records a fractional score in `reward.txt`. Read the score; do not interpret exit zero as task success.

**Controls:** retain `sympy` and bundled scripts unchanged. Local CIF analysis does not require a Materials Project account, even though other documented capabilities do. Do not remove legitimate API instructions merely because the selected task does not need them.

**Verdict:** include at most one such comparator in this initial shortlist. Its result alone would not establish the proposed paper's novelty.

### 7. dialogue-graph: documentation-format boundary control

[Package](https://github.com/benchflow-ai/skillsbench/tree/9a1f4dd5f7659f75707435da3ce854b6e48321d1/tasks/dialogue-parser/environment/skills/dialogue-graph) | [Task and verifier](https://github.com/benchflow-ai/skillsbench/tree/9a1f4dd5f7659f75707435da3ce854b6e48321d1/tasks/dialogue-parser)

**What it does:** exposes a Python graph library with nodes, edges, serialization, validation, and visualization. The task parses a branching dialogue into JSON and DOT.

**Verified finding:** T, medium severity. **R does not fire.** The original explicitly documents validation and returned errors.

**Why include:** it is a useful check against cherry-picking only apparently severe defects. The diagnostic asks for a table even though the package already documents the API. A representation change might help, have no effect, or add distraction; none of those outcomes should be assumed.

**Repair boundary:** reorganize existing library documentation into the recommended format. Do not invent a command-line interface, add unavailable `run_script()` calls, change library code, or add a new parsing algorithm under the label of documentation repair.

**Qualification tasks:** original dialogue plus a held-out dialogue satisfying the same explicit grammar. The original verifier contains fixed narrative IDs and minimum graph-size checks, so it cannot simply be pointed at arbitrary new dialogue data. Retain independent structural and parsing checks; verify DOT parsing rather than relying only on text fragments.

**Controls:** keep the Python library and Graphviz available in all arms. This is one package, not one subject per library method.

**Verdict:** useful control, weak evidence for a new substantive repair mechanism by itself.

### 8. reflow-profile-compliance-toolkit: suspected false-positive control

[Package](https://github.com/benchflow-ai/skillsbench/tree/9a1f4dd5f7659f75707435da3ce854b6e48321d1/tasks/manufacturing-equipment-maintenance/environment/skills/reflow-profile-compliance-toolkit) | [Task and verifier](https://github.com/benchflow-ai/skillsbench/tree/9a1f4dd5f7659f75707435da3ce854b6e48321d1/tasks/manufacturing-equipment-maintenance)

**What it does:** combines handbook instructions with thermocouple and manufacturing data to calculate ramp, time-above-liquidus, peak, and feasibility outputs.

**Verified finding:** R, low severity.

**Why it is a boundary control:** the body already explains non-increasing timestamps, absent thermocouple data, missing parameters, null outputs, and avoiding NaN/Inf. It also has a sanity-check list. The diagnostic is a suspected semantic false positive because those instructions do not satisfy its keyword test.

**Repair boundary:** do not fabricate a missing safety procedure. Permit a legitimate minimal clarification or no-op if the frozen repair policy allows one, and report that outcome. The editor must not be encouraged to rewrite the thermal model just to make the intervention substantial.

**Oracle concern:** the existing tests are deliberately loose in places. In particular, the best-run check establishes family membership and list consistency, not that the selected run is actually best. Conveyor checks also leave some values underconstrained. Do not report full maintenance-task correctness from these tests alone.

**Qualification tasks:** use pre-specified numerical outputs with audited handbook-derived expectations, including naturally occurring missing-data cases. Any restriction to a subset of questions must be made before treatments and reported as a derived task. Confirm PDF-reading dependencies, which are not fully supplied by the minimal Dockerfile.

**Verdict:** useful boundary case, not a substantive new repair category and not the centerpiece of the paper.

## 5. Attractive candidates rejected or deferred

| Candidate | Evidence behind the decision |
|---|---|
| `obspy-datacenter-client` | Actual dead link: `obspy-client-fdsn.md`; the package instead contains `obspy-clients-fdsn.md`. But the paired seismic task supplies local traces and does not require downloading them. Genuine typo, weak task-intervention match. |
| `lean4-theorem-proving` | Actual missing links to plugin-level commands/scripts, plus nested-reference finding. The distributed benchmark package does not include all the advertised plugin facilities. Requires careful intended-host and package-boundary adjudication before claiming a fair repair. |
| `fuzzing-python` | Four actual dead-link targets. Restoring upstream resources and reproducing the OSS-Fuzz-based build adds qualification work; missing-link task relevance has not been established. Keep as a resource-repair reserve, not a ready substitute. |
| `senior-data-engineer` | Dead links are in a secondary HOW_TO_USE document and point to other team skills. Do not assume they affect the Flink task. |
| `uv-package-manager` | Real reliability-language finding and a relevant build task, but an external BugSwarm image and build-script path require access/reproduction checks. It would reintroduce an infrastructure dependency early. |
| `timeseries-detrending` | Reliability finding fires despite existing missing-data and log-domain guidance. The task already supplies much of the procedure. Weaker substantive candidate than the shortlist's core subjects. |
| `scipy-curve-fit` | Already documents fitting failures and common issues. Do not describe it as an error-handling repair candidate when that diagnostic does not fire. |
| Repeated `pdf`, `xlsx`, or `dc-power-flow` copies | Copies do not provide independent package diversity. |

The actual dead-link scan found affected packages in four task families: Flink, Lean, seismic picking, and Python fuzzing. Apparent broken references from a preliminary regex screen were not accepted without checking the Markdown parser and tracked file tree.

## 6. Why these eight are not yet enough for the broad main-study claim

1. **One distribution source.** SkillsBench is practical because it co-locates skills, task specifications, environments, and verifiers. It is not a representative sample of all deployed skills. A second independently sourced package-task collection would strengthen external validity, but should not be added without executable task checks.
2. **One dominant heuristic.** Six subjects use R. The other two are a format rule and a compression rule. This cannot support broad conclusions about static checking in general.
3. **Controls do not create novelty.** Discovering that a word-based detector can be cleared without changing behavior is not, by itself, a strong new research result. The core subjects must establish something beyond that triviality.
4. **Eight is a planning number, not a power analysis.** Eight packages with two task instances each do not become hundreds of independent subjects merely because many episodes are run. Account for clustering by package/task and model. Determine main-study size after estimating variability, not by preserving the original number at all costs.
5. **No observed repair effect.** The shortlist was selected without behavioral outcomes. Keep it that way: do not retain only skills on which the preferred method wins.

The focused question this source screen can plausibly support is: **What are the behavioral consequences of applying these specified advisory repairs, compared with unchanged instructions and a matched generic rewrite?** It does not yet justify a claim that lint-guided repair broadly improves or harms agent skills.

## 7. Next step: qualify, do not immediately spend pilot budget

Start with `fuzzy-match` and `d3-visualization`. Use the existing task execution path and the simplest direct local Docker workflow. Do not build a new harness or repair platform.

For each candidate, require:

1. A complete pinned package, data fixture, environment, and attributable source; retain applicable upstream licenses and notices. The repository-level license does not replace third-party license review.
2. Reproduction of the selected diagnostic in the frozen checker version.
3. Independent human adjudication of whether it is a genuine omission, an advisory representation preference, or a false positive.
4. A clean environment build and successful reference-solution execution.
5. A verifier that rejects a deliberately incorrect output, handles missing tooling as infrastructure failure, and measures the claimed task property.
6. One primary instance and one held-out instance with frozen expectations. Publish derived-task changes explicitly.
7. A legitimate, warning-scoped repair opportunity without hidden answers or execution feedback. If the only defensible repair is a cosmetic word insertion, label it as such rather than forcing a larger edit.
8. Identical non-target skills, libraries, executable helpers, metadata, and available tools across O/L/G/N conditions. Disable automatic routing as the treatment variable; explicitly provide the assigned target instructions in O/L/G. N omits target guidance while retaining matched executable capabilities.

Here O is the original package guidance, L is a warning-directed revision, G is an equally budgeted generic revision, and N is the no-target-guidance reference. Decide explicitly which reference documents count as guidance in N; merely removing SKILL.md while leaving its full instructional content automatically injected would not be a clean no-guidance condition.

The person or model generating repairs should receive the original package, selected warning, and declared environment, **not this dossier's task answers, verifier source, ground-truth labels, or observed outcomes**. This audit inspected some oracle details for qualification; keep that role separate from repair generation.

Freeze the permitted edit surface before generating L and G. Give them the same editor, candidate count, and budget. A warning-scoped no-op can be a valid outcome when a finding is inapplicable. Log it; do not silently exclude it.

**Stop condition:** if the substantive candidates cannot produce legitimate repairs beyond generic added validation language, or if sound evaluation requires rebuilding multiple task environments and oracles, do not declare Gate 0 passed just because eight names are available. Reassess the corpus or the narrower research question before paying for hundreds of episodes.

## 8. Provenance fingerprints

All packages below are from the pinned SkillsBench commit. Paths are `tasks/<task>/environment/skills/<skill>/` using the table in Section 1.

Package SHA-256 was computed over files sorted by relative path, concatenating each UTF-8 relative path, a NUL byte, its raw file contents, and a NUL byte. This fingerprint records file names and contents, not permissions. It is not a substitute for pinning the task data and container image.

| Skill | Tracked package files fetched | Package SHA-256 |
|---|---:|---|
| fuzzy-match | 1 | `7ea9bb124a8dbf796ae97d192745c87f63fbc9e6c62cb49c4af89a20db7094c4` |
| d3-visualization | 5 | `11645c768a9636beecd5ab0f440a788c7aae7e06605ce0ac6d4810299da4d115` |
| dc-power-flow | 2 | `4c84bb3ad525db3aeb8680a6d66ae9adeacb3a8a48462358bf946f306bfd13c4` |
| python-scala-collections | 1 | `13f06cc0607a4d93cb498cf70d761685d61611d18c0106596a8baee94b5bf3d5` |
| mesh-analysis | 2 | `24015b9572db49e4bb2f79912c80ebfe4337cb08d2f5dc1ade7b6bbcc153000c` |
| pymatgen | 10 | `efed29315f3a1e6cc2ed88e61c2ab47c55f90d352982d57be65bb716f08520dc` |
| dialogue-graph | 2 | `56e58c57fd21dbb02cdaf1989c2e0afad7df884ee05e052533d36ef94c7ae773` |
| reflow-profile-compliance-toolkit | 1 | `788047e5f336b6dd323a0d2f99a752c65bf8ef6850e5ce29f38ec61c85b9554d` |

## 9. Bottom line

These are the best eight **candidates from the audited source**, with their shortcomings exposed. They are not eight approved main-study subjects. The first concrete decision is to qualify the first two, while resolving or rejecting the known blockers in the next three. Keep the final three in their declared comparator/control roles, and do not use them to inflate the apparent breadth of the contribution.

This audit improves the plan by identifying authentic diagnostics, complete tracked packages, and real oracle limitations before API spending. It does not demonstrate that the pilot will pass or that the paper will be accepted.
