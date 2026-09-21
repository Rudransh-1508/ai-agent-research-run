# W2 — Feasibility Review F-A: CAND-1 (OrgBlast) and CAND-2 (ClassicalTransfer)

**Reviewer:** Wave-2 feasibility specialist F-A
**Date:** 21 Sep 2026 (19 days to the 10 Oct 2026 MASO deadline)
**Inputs relied on:** F1_feasibility_scan.md (substrate, effort, cost, stats — all verified 21 Sep), E5_assassin_classical_mas.md (Dellarocas & Klein parameters from full text), B5_fault_injection.md (MAS-FIRE/AgentChaos full-text details), B11_benchmarks.md (tau2-bench), B15_metrics.md, B10_organizational_mas.md, B4_cascading_failures.md, B8_human_escalation.md.
**Independent verification this session:** tau2-bench repo re-inspected via GitHub API (21 Sep 2026): domains = {mock, airline, retail, telecom, banking_knowledge}; retail = **114 tasks**, **25 tools** (incl. `transfer_to_human_agents` — a built-in human-escalation boundary), per-task `evaluation_criteria.actions` (expected action sequences) + DB-state ground truth in `data/tau2/domains/retail/db.json` + `policy.md`. τ³ v1.0.1 current; pin `>= 1.0.1` (grading fix; older results not comparable).

---

## 1. Verdict

**Both candidates are buildable by 10 Oct with 2 engineers, but only as ONE shared testbed with two experiment layers, and only after the cuts in §10.** CAND-1 supplies the metric contribution (organizational blast radius) and the mechanism comparison; CAND-2 reuses ~80% of that infrastructure (the sentinel mechanism, the survivalist retry, the crash fault, the scarcity flag) and adds the classical-prediction hypotheses that make the paper reviewer-proof for a classical-MAS-heavy MASO pool. Attempting both as separate builds fails; attempting CAND-1 at full scope (3 workflows × 15 faults × 7 mechanisms) fails. The descoped joint build below is ~4.5–5.5 person-weeks against ~5.4 pw available (2 people × 19 days, full-time) — **zero slack; the week-1 de-risking gates (§9) are go/no-go, not optional.**

If forced to choose one: **CAND-1 descoped + CAND-2's Experiment 2a/2b as its "classical grounding" section.** CAND-2 standalone is feasible but weaker as a workshop paper (replication framing without the new metric is a harder sell; the metric without classical grounding is a harder defense).

---

## 2. Shared testbed architecture (one build)

**Stack:** LangGraph (org graph as explicit state graph; checkpointer = rollback substrate; `interrupt` = human boundary) wrapped around tau2-bench domains (deterministic tools, DB-state ground truth, policy docs). Injection at two layers: (a) semantic — MAS-FIRE-style prompt modification / response rewriting / message-routing manipulation, implemented as LangGraph middleware on agent nodes and edges; (b) API — AgentChaos-style crash/omission faults on the LLM HTTP layer (needed for the agent-death fault that CAND-2's unzippering replication requires).

**Key structural decision:** tau2 is single-agent-vs-simulated-user. The org wrapper splits the *agent side* only: the frontline role owns the user dialogue; supervisor/approver roles are internal and communicate through typed handoff messages and gated tool subsets. Every handoff, tool call, DB write, and memory write is logged as an event tagged with the boundary it crosses (role, communication, authority, tool, memory, accountability, human) and with a **provenance pointer** to its causal parents — this is what makes blast radius measurable rather than anecdotal.

**DB snapshotting:** tau2's DB is a JSON document; snapshot it at every supervisor checkpoint (trivial) so that rollback = LangGraph checkpoint restore + DB snapshot restore. This is the single most important cheap engineering decision — it makes checkpoint-rollback a near-free containment condition.

---

## 3. Workflows (2, not 3)

| # | Workflow | Source | Org wrapper | Effort (pw) |
|---|---|---|---|---|
| W1 | **Customer-service refund/exchange** | tau2-bench **retail**, 114 tasks, 25 tools, policy.md — zero new domain authoring | Frontline agent → supervisor (verify/approve) → finance approver (refunds above threshold). Authority boundary = spending limit; human boundary = existing `transfer_to_human_agents` tool | 0.5–1 |
| W2 | **IT incident response** | New domain in tau2 style: ~12 deterministic mock tools (ticket create/update, monitoring query, runbook lookup, service restart with state, paging), policy doc, **30 tasks** with DB-state goal annotations | L1 responder → L2 specialist → on-call engineer; natural 3-level escalation/delegation tree for the unzippering replication | 1–1.5 |
| ~~W3~~ | ~~Procurement approval~~ | **CUT** (§10). Best authority-boundary domain but third-domain authoring (~1–1.5 pw) is what breaks the schedule | — | — |

W1 gives scale (114 tasks → clean task sampling) and a pre-verified harness; W2 gives a structurally different org (ops escalation tree vs service approval chain) and is the natural home of CAND-2. Two workflows suffice for the "organizational workflows" plural in the claim; three is a luxury.

---

## 4. Independent variables

### 4.1 CAND-1: org structure (3 levels, fixed agent roster of 5 roles)

- **S1 Flat/peer:** all roles coordinate directly, no verification authority. (Baseline structure.)
- **S2 Two-level hierarchy:** frontline → supervisor with verify-and-approve authority over boundary-crossing actions.
- **S3 Three-level delegation chain:** frontline → supervisor → finance/on-call approver. Depth is the classical unzippering variable.

**Memory config** is NOT a crossed factor (would double the matrix). Default = private per-agent memory; a focused sub-study (§7.3) adds shared scratchpad ON/OFF for the two memory-relevant faults. Shared memory is one LangGraph state key — cheap to build, expensive to cross.

### 4.2 CAND-2: classical mechanisms re-implemented (on W2 + W1 approval chain)

| Classical mechanism | Source (verified, E5) | LLM-era implementation | Cost |
|---|---|---|---|
| **Survivalist** (timeout/retry, no coordination) | Dellarocas & Klein ICMAS 2000, DOI 10.1109/ICMAS.2000.858440 | Local retry with backoff on detected failure; no cross-agent signaling | trivial |
| **Sentinel services** (citizen condition) | D&K 2000; Hägg 1997 (DOI 10.1007/BFb0030090) | Monitor node watching the message bus + tool stream; on detection: cancel orphaned subtasks, re-delegate, quarantine faulty agent, escalate. Detection rules: (a) syntactic/structural (schema, DB invariants) — the classical assumption; (b) semantic LLM-check — the ablation that shows where classical breaks | ~1 pw, shared with CAND-1's C4 |
| **Hierarchy vs flat** (organizational paradigms) | Horling & Lesser 2004 survey, DOI 10.1017/S0269888905000317 | = CAND-1's S1 vs S2/S3. Do NOT build market/contract-net or matrix paradigms — cite as design space only | free (shared) |
| **Reorganization** (link adaptation) | Kota, Gibbins & Jennings TAAS 2012, DOI 10.1145/2168260.2168261 | After k verification failures of agent X's outputs, supervisor reassigns X's pending subtasks and rewrites the routing table; measure recovery toward an oracle-routing upper bound | ~0.5 pw — **stretch goal only** |
| **Scarcity condition** (containment backfires) | D&K's key non-obvious finding | Scarcity = one specialist role + rate-limited approval tool; short tasks = low-step W1 tasks. Config flag, not new code | trivial |

**Classical predictions under test (the paper's hypotheses):**
- H1 (unzippering): cost of an agent-death fault grows with delegation depth; survivalist handling at depth 3–4 multiplies completion cost severalfold vs failure-free baseline (D&K: 600–700% of baseline time).
- H2 (sentinel containment): citizen+sentinel keeps utility within a few % of baseline under abundant capacity.
- H3 (backfire under scarcity): with scarce specialists and short tasks, sentinel-based early re-delegation is *worse* than survivalist (D&K's inversion).
- H4 (LLM breakdown): sentinels with syntactic detection — the only kind classical MAS had — fail against semantic faults (corrupted handoff content, hallucinated arguments); semantic detection recovers only part of the gap. **H4 is the novel result; H1–H3 are the replication that earns the classical reviewers.**

---

## 5. Fault library (7 types; 5 in the main matrix)

Selection criteria: each fault maps to a distinct organizational boundary, is injectable via a verified mechanism (MAS-FIRE's three + AgentChaos's API layer), and has an automated trigger check (AgentChaos's lesson: log and filter untriggered injections).

| # | Fault | Boundary | Injection mechanism | Trigger check | Matrix |
|---|---|---|---|---|---|
| F1 | **Hallucinated tool arguments** (plausible-but-wrong values) | Tool | Response rewriting on `tool_calls` field | Tool invoked with mutated args | Main |
| F2 | **Corrupted handoff content** (semantic drift: mutated ID/amount/status in inter-agent message) | Communication | Response rewriting on handoff message | Downstream agent acts on mutated value | Main |
| F3 | **Instruction conflict / role ambiguity** (conflicting policy injected into one role's prompt) | Role | Prompt modification | Behavior consistent with injected instruction | Main |
| F4 | **Verification omission / blind trust** (supervisor passes output without checking) | Authority | Prompt modification + routing manipulation (bypass check edge) | Check edge not exercised | Main |
| F5 | **Agent death** (crash mid-delegation) | (classical; delegation) | API-layer abort (AgentChaos-style) | No response within timeout | Main — required by CAND-2 H1 |
| F6 | **Memory poisoning** (corrupted fact written to shared scratchpad, e.g. wrong refund cap) | Memory | Direct memory-write injection | Fact retrieved and used downstream | Sub-study only (needs shared memory) |
| F7 | **Unauthorized action attempt** (frontline attempts action above its privilege) | Authority/accountability | Prompt modification | Gated tool called by unauthorized role | Sub-study only (pairs with verifier gate) |

Dropped from consideration: MAS-FIRE's message cycle/storm/broadcast (infrastructure noise, not organizational), wrong-tool-selection (redundant with F1), context-length violations (not organizational).

---

## 6. Containment mechanisms (6 conditions)

| # | Mechanism | Implementation | Shared with |
|---|---|---|---|
| C0 | **None** | baseline | both |
| C1 | **Retry (survivalist)** | local timeout/retry | CAND-2 |
| C2 | **Verifier gate** | supervisor validates outputs before boundary crossing: rule-based on DB invariants + LLM semantic check; Agents-SDK-guardrail style | both (H4 ablation) |
| C3 | **Checkpoint-rollback** | LangGraph checkpointer + tau2 DB snapshot; on detection, restore last clean joint state and re-execute | CAND-1 |
| C4 | **Quarantine + re-delegation (sentinel)** | isolate faulty agent, reassign its subtasks, purge its downstream writes | CAND-2 (citizen) |
| C5 | **Human escalation** | LangGraph `interrupt` → **scripted oracle human**: policy-compliant decisions, fixed latency of k steps, bounded daily capacity, sees only what the escalator surfaces. W1 reuses `transfer_to_human_agents` | both |

Cut from CAND-1's original list: **revocation** (needs authority-token machinery; partially covered by C4) and **reroute** as a separate mechanism (folded into C4). Human escalation stays because "human vs automated containment for propagating organizational faults has never been compared" is a verified gap (B8) and a headline result — but with a scripted oracle, not a user study, and with its cost priced in oversight-minutes (§7).

---

## 7. Metrics (formal definitions)

Episode e = (workflow w, task i, structure s, fault f injected at agent a₀ at step t₀, containment c). Trace T = tagged event stream. G = annotated goal DB state (tau2). Fault-free reference trace T* and final state DB* obtained by running the same cell with f disabled.

**Primary:**
1. **Organizational Blast Radius.** OBR(e) = |{b ∈ B : ∃ corrupted event in T crossing b}| / |B|, B = {role, communication, authority, tool, memory, accountability, human}. An event is *corrupted* iff (a) it is a provenance descendant of the injected fault and (b) it deviates from T* or violates a domain invariant. Corruption detection is automated on structured channels only (tool args, DB writes, IDs/amounts in handoffs via entity match against the fault payload); LLM-judge used only as a secondary rater with a human spot-check on a 5% sample (target κ ≥ 0.7 — see risk R3). Report per-boundary OBR_b ∈ {0,1} as the main table.
2. **Task utility.** U(e) = fraction of `evaluation_criteria.actions` correctly completed with final DB state matching G (partial credit; tau2-native), plus binary pass = 1[U = 1 ∧ no policy violation]. 
3. **Utility preservation.** UP(c) = E[U | f, c] / E[U | no fault, c] per cell.
4. **Recovery cost.** RC(e) = tokens_containment + tokens_re-execution + λ_t·(extra tool calls) + λ_h·(human oversight minutes), λ published. Report the **(UP, RC) Pareto frontier per mechanism** — this is the figure that also serves CAND-4's territory defensively.

**Secondary:** cascade depth (max org-graph distance from a₀ to any corrupted agent); corrupted-agent fraction; MTTD (steps t₀ → first detection); MTTC (steps t₀ → first containment action that stops further boundary crossings, ∞ if none); collateral damage |DB_final Δ DB*| over records outside G (AppWorld-style, B11-verified pattern); RS_f = pass(f)/pass(baseline) (MAS-FIRE-comparable); pass^k on a 10% subsample.

**CAND-2 metrics (D&K-analogous):** relative completion cost = tokens+steps vs failure-free baseline (the analog of D&K's "600–700% of baseline completion time"); wasted effort = tokens spent on orphaned/dead-end subtasks; utility as above. H4 adds detection-rate-by-detector-type (syntactic vs semantic sentinel).

### 7.1 Main matrix (CAND-1)
2 workflows × 3 structures × 5 faults × 6 containment × **n=30** = **5,400 runs**, plus matched no-fault baselines 2×3×6×30 = 1,080. n=30/cell detects 25–30pp binary differences (F1's power analysis); the continuous OBR/RC metrics are powered for d≈0.8 at n=20–30. Expected effect sizes from prior work (MAS-FIRE, AgentChaos: 40–80pp swings) are well above threshold.

### 7.2 CAND-2 matrices
- **Exp 2a (unzippering replication):** depth {1,2,3,4} × {survivalist, citizen} × scarcity {abundant, scarce} × 30 = **480 runs** (fault = F5, on W2's escalation tree + W1's approval chain).
- **Exp 2b (semantic breakdown):** same design with F2 (semantic handoff corruption) instead of F5, sentinel detection {syntactic, semantic} = **480 runs**. H4 lives here.
- **Exp 2c (reorganization, stretch):** static vs adaptive routing × 3 faults × 30 = 180 runs — only if day-11 gate passes.

### 7.3 Memory sub-study
1 workflow (W1) × memory {private, shared} × {F6, F2} × {C0, C2, C3} × 30 = **360 runs**. Covers the memory boundary — E5's identified strongest residual-novelty boundary — without crossing it into the main matrix.

**Total: ≈ 8,500 runs** (incl. ~500 pilot). 

### 7.4 API cost (prices from F1's live OpenRouter pull, 21 Sep)
Per run ≈ 150k input + 20k output tokens; containment cells +~30% for verification/re-execution.

| Primary model | $/run | 8,500 runs |
|---|---|---|
| DeepSeek v3.2 | ~$0.05–0.065 | **~$450–550** |
| GPT-5-mini | ~$0.08–0.10 | **~$700–850** |
| GPT-5-nano (robustness subsample, ~800 runs) | ~$0.016 | ~$13 |

**Budget ≈ $500–900 all-in** (batch API halves it). Non-binding, as F1 concluded. One primary model + one cheap robustness check on a 10% stratified subsample; **no model sweep** — model generality is explicitly future work.

---

## 8. Timeline (19 days, 2 engineers)

| Days | Work | Gate |
|---|---|---|
| 1–4 | **Week-1 de-risk spikes (§9):** org wrapper on retail (R1), injection harness + trigger logging (R2), lineage/OBR tracer (R3), DB-snapshot rollback (R4) | **Go/no-go on day 4** |
| 5–8 | W2 domain (12 tools, 30 tasks); fault library F1–F7; containment C1–C5 | all 7 faults trigger ≥70% in smoke tests |
| 9–11 | Pilot ~5% of cells; fix trigger rates; freeze config; human spot-check of OBR labels (κ gate) | pilot pass-rates sane; κ ≥ 0.7 |
| 12–16 | Main runs (~8k; ~6–8 h/model-day at 30–50 parallel workers — rate limits, not money, set pace; use 2 providers or batch API) | — |
| 17–19 | Analysis (OBR table, Pareto figure, D&K replication figure), writing | submit 10 Oct |

Effort: wrapper 1 + W2 1.25 + injection 1.25 + instrumentation 0.75 + containment 1.25 ≈ **5.5 pw** against 5.4 available — the cut list (§10) is what makes this close; any slippage takes from Exp 2c, then W2 task count (30→20), then the memory sub-study.

---

## 9. Riskiest engineering assumptions + week-1 de-risking

| # | Risk | Why it can kill the paper | Week-1 de-risk (go/no-go) |
|---|---|---|---|
| R1 | **Org wrapper degrades baseline.** Splitting tau2's single agent into a role hierarchy may tank no-fault pass rates for coordination reasons, compressing all fault effects into noise | All effects are relative to baseline; a broken baseline invalidates every cell | Days 1–3: 2-level refund org, 30 no-fault episodes. **Gate: baseline pass within ~10pp of published single-agent retail numbers.** Fail → fall back to shallower split (frontline + supervisor only) |
| R2 | **Fault trigger rates too low.** Strong models ignore prompt-modified faults (cf. MAS-FIRE's blind-trust variance); AgentChaos showed untriggered faults silently bias impact estimates downward | Faults that don't fire = empty cells | Days 2–4: every fault gets an automated trigger check (§5); smoke-test 20 runs/fault. **Gate: ≥70% trigger per fault; redesign or drop any that fail** (dropping F3/F4 first is acceptable) |
| R3 | **OBR corruption-labeling is unreliable.** "Corrupted event" requires provenance through free-text LLM messages; if automated labeling disagrees with humans, the headline metric is attackable | The OBR metric IS the contribution | Days 2–4: build lineage tracer, hand-label 20 pilot traces, compute agreement. **Gate: κ ≥ 0.7 on structured channels; else restrict OBR to tool/DB/memory boundaries + handoff entity-matching and say so** |
| R4 | **Rollback semantics across agents.** LangGraph checkpoints the graph, but tau2's DB lives in the environment; uncoordinated restore = phantom state | C3 (rollback) is a headline containment condition | Day 3–4: forced-fault test — inject F1, roll back, verify DB + graph state jointly restored. **Gate: deterministic restore in the test; else C3 becomes "restart-subtask" (weaker but honest)** |
| R5 | **Oracle human too strong.** A scripted human with perfect policy knowledge makes C5 look artificially dominant | Reviewers reject the human-escalation comparison | Mitigate by construction: fixed latency, bounded capacity, sees only escalated context; sensitivity analysis over latency/capacity; stated as limitation |
| R6 | **Throughput/rate limits.** ~8k runs in 5 days | Schedule slips into writing days | Day 4: 100-run batch test through tau2's runner with async + provider fallover; batch API as backup |

---

## 10. Cut list (what does NOT make 10 Oct — be honest)

1. **Workflow 3 (procurement)** — cut entirely; named as future work. It is the single biggest schedule saver (~1–1.5 pw).
2. **Fault taxonomy 15 → 5 main + 2 sub-study.** MAS-FIRE's full 15 is uncitable-and-unbuildable in 19 days; our 7 span all seven boundaries, which is the actual claim.
3. **Org paradigms: hierarchy/flat only.** Contract-net/market and matrix (Horling & Lesser) are cited as design space, not built.
4. **Kota-style reorganization (Exp 2c)** — stretch goal, first thing cut on slippage.
5. **Revocation as a separate containment mechanism** — folded into quarantine.
6. **Model sweep** — 1 primary + 1 cheap robustness subsample.
7. **Human escalation = scripted oracle, not a user study.** The comparison "human vs automated containment" survives; human-factors realism does not.
8. **TheAgentCompany validation run** (F1's stretch goal) — cut; heavy infra, wrong deadline.
9. **Memory as crossed factor** — reduced to a 360-run sub-study.

What survives intact: the OBR metric + per-boundary table; the 6-mechanism comparison incl. human escalation with priced oversight; the cost-utility Pareto; the D&K replication incl. the scarcity-backfire test (H3) and the semantic-breakdown result (H4). That is a full workshop paper.

---

## 11. Candidate-level verdicts

- **CAND-1 (OrgBlast): FEASIBLE, descoped as above.** Its binding constraint is engineering time, specifically R1/R3 (wrapper baseline fidelity and OBR labeling validity). Both are gated in week 1 with explicit fallbacks, so the failure mode is graceful degradation of scope, not a blown deadline.
- **CAND-2 (ClassicalTransfer): FEASIBLE — and nearly free once CAND-1's testbed exists.** Sentinel = C4, survivalist = C1, agent-death = F5, scarcity = a config flag. Its standalone risk is framing, not engineering: a pure replication needs the H4 semantic-breakdown result to be more than a replication, and H4 needs CAND-1's semantic fault library. **Recommendation: merge — one testbed, one paper, CAND-1's metrics as the contribution and CAND-2's hypotheses as the evaluation frame.** This also directly answers E5's kill shot: the classical literature becomes the paper's theoretical foundation and its replication target, not its rebuttal.

---

## Appendix: verification log (this session, 21 Sep 2026)

- tau2-bench GitHub repo via API: domain list, retail domain file layout, `data/tau2/domains/retail/tasks.json` parsed (114 tasks; task schema = id/description/user_scenario/initial_state/evaluation_criteria.actions), `src/tau2/domains/retail/tools.py` parsed (25 tool functions incl. `transfer_to_human_agents`, `return_delivered_order_items`, `exchange_delivered_order_items`, `modify_pending_order_*`), README (τ³ v1.0.1 grading note; install via `uv`, Python ≥3.12).
- All other factual inputs (D&K parameters, MAS-FIRE taxonomy/mechanisms, AgentChaos trigger-verification lesson, tau2 dual-control telecom, LangGraph checkpoint/interrupt primitives, model prices, power analysis) are taken from wave-1 reports F1/E5/B5/B11/B15, all verified against primary sources on 21 Sep 2026 by those investigators; no new external citations are introduced in this report.
