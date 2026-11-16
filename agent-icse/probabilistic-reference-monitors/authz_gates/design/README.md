# The composed gate (design)

`gate.py` is the design that occupies the empty cell no measured gate fills: safe
automation under a certified false-allow bound, with jev-guard-level protection and no
reliance on a human under an unattended host mode. It is a Claude Code PreToolUse hook.

## The three levers (mapped to failures F1-F7 / requirements R1-R7)

1. **Asymmetric authority.** Deterministic rules may `deny`/`ask` freely but may only
   *allow* from a small, fully-parsed set: a read-only command allowlist (argument-checked,
   any shell metacharacter disqualifies) and an ephemeral scratch-write allowlist (paths
   under `notes/ sandbox/ build/ dist/ /tmp/`, no `~`, no `..`, no dotfiles). The model may
   *allow* only when its `p_safe` clears a threshold certified for its version with a stated
   false-allow budget (default 0.245, jev-1.13.0). Nothing else can allow. The deterministic
   deny layer reuses dcg's parser and adds an indicator-removal (ATT&CK T1070) tactic pack
   that dcg does not cover.
2. **A total failure function.** Every residual outcome - model error, timeout, empty or
   malformed answer, oversize or unparseable input, a write outside the scratch set, an
   unknown tool - maps to `ask` with a human present and `deny` under `bypassPermissions`,
   and never to allow.
3. **Whole-command visibility.** Over the byte limit (default 256 KiB) the gate refuses
   rather than judge a truncated view.

## Run / score

    set -a; source ~/.env; set +a                     # TYPESAFE_API_KEY (the judge)
    export DESIGN_DCG_BIN="$PWD/baselines/dcg/dcg" JEV_MODEL=jev-1.13.0
    export DESIGN_CMD="python3 $PWD/design/gate.py"
    bash benchmark/run_scorecard.sh artifact/design-v2 design
    python3 faultinject/run_faults.py --gates design "design(groq)" --out <new file>

Config env: `DESIGN_DCG_BIN`, `TYPESAFE_API_KEY`, `DESIGN_THRESHOLD` (default 0.245),
`DESIGN_MAX_BYTES` (default 262144), `DESIGN_MODEL`/`JEV_MODEL`, `DESIGN_MODEL_BUDGET_S`
(default 20: wall-clock cap on the whole model consultation, retries included).

**Swapping the judge.** `DESIGN_JUDGE=groq` uses a Groq-served model (`GROQ_API_KEYS`,
comma-separated; `DESIGN_MODEL` default `openai/gpt-oss-120b`). Its threshold must be
certified on exactly what the gate sends the model, not on the benchmark's own rendering:

    python3 analysis/model_judge.py --render hook --out artifact/judge_groq_<tag>_hook.jsonl   # x3 runs
    python3 analysis/judge_validation.py --calib ... --repeats ... --heldout ...           # deploy the worst-case t

For gpt-oss-120b that is t = 0.405; the benchmark rendering gives 0.305, and at 0.305 the
gate allows `pip uninstall -y requests` (scored 0.2 as `Package: ...`, 0.4 as `Bash: ...`).

**Why the budget exists.** A hook the host kills at its timeout (Claude Code: 60s) is a
non-blocking error, so the tool call proceeds - under `bypassPermissions` it simply runs.
Before the budget, a model timeout made the jev path retry past 60s (fault trial
`artifact/design-faults/fault_trials.jsonl`: `timeout -> host_timeout`), i.e. the failure
function was bypassed at the host seam. With it, every fault ends in ask/deny within ~20s
(`fault_trials_fixed.jsonl`). No measured design-v2 row was affected (max hook time 1.9s).
The earlier fault matrix was also vacuous (model never called: no key, and its probe was
dcg-denied first); the `design` / `design(groq)` recipes now probe a dcg-clear command with
a stub key and differing controls, so the model path is exercised.

## Result (v2, 2026-11-12, `artifact/design-v2/`)

| host mode | destr run (main) | (held-out) | padded | safe auto-approved | safe blocked |
|---|---|---|---|---|---|
| default | 0/127 | 0/100 | 0/220 | 94/94 | 0/94 |
| bypass  | 0/127 | 0/100 | 0/220 | 94/94 | 0/94 |

Zero destructive runs on every corpus in both modes, all 94 safe calls auto-approved, none
blocked; the fault matrix never allows (re-run exercised and with the budget fix, 2026-11-17;
see above). 95% Clopper-Pearson upper bounds on the zero counts:
destructive run <= 2.3% (main) / <= 2.95% (held-out), padded <= 1.35%, safe false-deny
<= 3.1%. Latency (`artifact/LATENCY.md`): 47% of decisions take the deterministic fast path
(0.09s median) with no model call; the model path is 0.56s median.

## Honest limitations (why a perfect bench score is not the claim)

- **Same-corpus evaluation.** The model threshold was certified on this main corpus, and the
  T1070 deny pack was added after observing one held-out model miss (`art-04`). A perfect
  score on the corpus the gate was tuned against is weak evidence; the design must be
  stress-tested on attacks it was not tuned on (the cross-host breadth survey, a fresh
  held-out attack set, larger n for tighter bounds, and threshold certification on more than
  one model family). Those are the planned adversarial pressure, not further gate tweaks.
- **Composition, not from scratch.** The deterministic parser is dcg; the judge is the jev
  model. The contribution is the integration - asymmetric authority, the total failure
  function, host-mode awareness, and the certified operating point - not a new parser or model.
