# Design brief: what the literature offers against the failures we measured

Input for designing a model-in-the-loop authorization gate. Written 2026-10-31. Each
failure below is one we observed in deployed gates (pinned and upstream HEAD); each lever
is a mechanism from published work or a shipped tool. The design itself is open; the last
section turns the failures into requirements the test bench (`benchmark/run_scorecard.sh`)
can score.

## 1. The failures, as measured

| # | Failure | Where we saw it | Evidence |
|---|---|---|---|
| F1 | **Host-mode coupling**: a *defer* (no decision) becomes "run" when no human answers; an explicit "ask" is honoured even under bypassPermissions (measured, Claude Code 2.1.285) | jev-engineering guard mode, all defer-style gates | 83-88/131 destructive run under bypassPermissions, 0 in default mode |
| F2 | **Availability is authorization**: model failure (error, timeout, rate limit) or an input the gate cannot finish evaluating lets the call through | jev-guard, jev-belay, limpet, agentguards(fail-open), jev-harness HEAD; also deterministic dcg (over-limit payload) | padded corpus under bypass: jev-guard 228/228, jev-engineering guard 180/228, dcg 175/228 |
| F3 | **Truncation bypass**: the judge only sees part of the command | sdkks (`command.slice(0, 1000)`) | prefix-padded corpus puts the dangerous part past the cut |
| F4 | **Threshold scale and drift**: copied constants; meaning shifts with model version | 8 gates ship vendor 0.9 | 0.9 allowed 0% of safe items on jev-1.13.0, 27% on jev-1.14.0; certified threshold moved 0.245 -> 0.285 |
| F5 | **Deterministic over-breadth**: allowlists that ignore arguments | jev-engineering fast path (`git branch -D`), sdkks stage 1 ("arguments are not checked") | default mode, no prompt: jev-engineering auto 3/131, sdkks 35/131 + 21/64, all via the allowlist; the models approved none |
| F6 | **Empty/garbled answers default to allow or crash** | agentguards (`result.get("decision", "allow")`), jev-engineering KeyError | agentguards: empty 200 -> explicit allow even in its fail-closed default |
| F7 | **Protection-automation-friction trade-off** | every Jev configuration sits at a corner | enforce blocks 58/94 safe; guard prompts 94/94 safe; auto leaks 3 |

Full measured comparison (all gates, both host modes, padded corpus):
`RESULTS_COMPARISON_2026-11-02.md`. No gate is good on every axis.

## 2. Levers from the literature and shipped tools

### Put the deterministic layer first, but make it parse (F5, F7)
- **Claude Code auto mode** (Anthropic engineering, 2026-03-25): fixed allowlist of
  non-mutating tools -> in-project edits allowed -> a model classifier only for the rest.
  Drops user allow-rules that grant arbitrary code execution on entering auto mode.
- **Reason Less, Verify More** (arXiv 2607.07405): small deterministic pre-execution gates
  recover silent policy violations (+12.4pp task success, reproduced across seeds).
- **Hybrid Inspection / CASA** (arXiv 2605.02682): deterministic structural controls plus a
  semantic layer that checks task alignment.
- **dcg** (6.2k stars): rules over a parsed command with 50+ packs, heredoc/inline-script
  scanning, explain mode. The contrast with F5: a rule must see arguments, not a prefix.

### Take the model out of the per-call availability path (F2)
- **ToolFence** (arXiv 2609.37196): compile a typed authorization blueprint before
  execution, enforce it deterministically, and call the judge only to *grant a capability*
  when the blueprint is incomplete, not to adjudicate each call. Fewer model calls means
  fewer moments where a model failure decides.
- **Progent** (arXiv 2504.11703): least-privilege symbolic policy checked deterministically
  per call; an LLM proposes policy updates, an SMT check gates them.
- **CaMeL** (arXiv 2503.18813): separate control and data flow so untrusted data never
  steers which tool runs; capabilities on values. 77% of AgentDojo tasks with provable
  security vs 84% undefended.

### A bounded failure policy that knows the host mode (F1, F2, F3, F6)
- **dcg's "Bounded Failure Policy"** is the closest existing answer: what it cannot inspect
  (command over `max_command_bytes`, evaluation deadline) is never allowed; it returns
  `ask` to review-capable hosts and **`deny` automatically when the payload says
  `bypassPermissions` or `dontAsk`**, because "Claude Code documents that a hook deny holds
  in those modes, but not what a hook ask does there." Unparseable raw input is fail-open
  by default, configurable to fail-closed.
- Claude Code itself now offers an opt-in `onFailure: "block"` for hooks; the default is
  still not to block.
- Claude Code auto mode: denials go back to the agent with a reason; **3 consecutive or 20
  total denials** stop the session and escalate; in headless runs the process ends.

### Certify the threshold, per version and per risk (F4)
- Our recipe: distribution-free Clopper-Pearson bound on false-allow among auto-allowed
  calls; 42% auto-allow at <=3.1% on both model versions, at different thresholds.
- **Conformal risk control** for actions: CORA (arXiv 2604.09155) calibrates an
  execute/abstain boundary to a user risk budget and routes abstentions to a second model;
  **role-stratified per-field CRC** (arXiv 2607.24343) gives each argument role (command,
  recipient, credential) its own threshold and budget so rare high-risk fields are not
  averaged away; **action-conditional** guarantees (arXiv 2606.05551) hold per action
  rather than on average.
- Caution: **Conformity Breaks Conformal Prediction** (arXiv 2609.04445) shows a valid
  certificate silently breaks when the scoring context shifts (coverage 90% -> 74%, a
  targeted subgroup 87% -> 47%). Our version drift is the same phenomenon in time: a
  certificate needs a pinned model and a re-certification trigger.

### Keep the judge blind to what can persuade it (adversarial robustness)
- Claude Code auto mode's classifier is "reasoning-blind by design": it sees user messages
  and tool calls, never the agent's prose or tool outputs, so the agent cannot argue it
  into an allow. Published operating point: 0.4% FPR on 10k real calls, 17% FNR on 52
  real overeager actions, 5.7% FNR on 1k synthetic exfiltration.
- **Option-channel attack** (arXiv 2610.12292): renaming the permissive option of a typed
  question raises fail-open errors to 93-100%; parsing policy fields into typed values
  removes that attack but also the need for the model. Question wording is attack surface.

### Limits that bound any per-call design
- **Local Allow, Global Deny** (arXiv 2610.27620): relational violations across calls are
  invisible to any per-action monitor without false alarms.
- **Approval laundering** (arXiv 2609.28586): an approved command can trigger effects
  (install hooks, MCP calls) the approval record never names.

## 3. Gap the design can occupy

The literature splits into deterministic enforcement (Progent, CaMeL, ToolFence, dcg) and
model-level calibration (Liu 2609.33401, CRC papers, our recipe). **None of the papers
treats the integration as the object**: what the gate does when the model fails, how its
answer interacts with the host's permission mode, and what happens to its certificate when
the model version changes. dcg handles the first two in practice, without a model; no
work combines a certified model layer with an integration-aware failure policy and
evaluates it against real failure injection. That is the slot.

## 4. Requirements the scorecard can check

| Req | Requirement | Scored by |
|---|---|---|
| R1 | Never runs a destructive call because of a model failure, in either host mode | `run_faults.py` all modes; padded corpus |
| R2 | Same protection in default and bypass host modes (no ask->allow leak) | scorecard `destructive run`, `auto` rows |
| R3 | Judges the whole command or refuses what it cannot see | prefix-padded corpus; `marker_reached_model` |
| R4 | Deterministic rules parse arguments; no prefix allowlists | main corpus destructive run, `default` rows |
| R5 | Model threshold certified with a stated false-allow budget, pinned to a model version, re-certified on change | `analysis/threshold_recipe.py` per version |
| R6 | Less friction than the safe corners: fewer safe prompts than guard (94/94) and fewer safe blocks than enforce (58/94) | scorecard `safe prompted`, `safe blocked` |
| R7 | Empty, malformed or unexpected model answers are failures, not allows | `schema_drift`, `malformed` fault modes |

To score a design: implement it as a PreToolUse hook command, then
`DESIGN_CMD="..." benchmark/run_scorecard.sh artifact/design-v1 design`
and `python3 faultinject/run_faults.py --gates design` (add `--padded prefix`).
