# Does the pattern hold beyond Jev? A non-Jev comparison

The corpus is Jev-only, so a reviewer can ask whether fail-open, threshold-copying and the
ask->allow downgrade are Jev artifacts or properties of putting *any* remote model in the
authorization path. This is a small comparison set of non-Jev gates, classified with the
corpus's rubric (read the error path at a pinned SHA; static, no execution). Cloned
2026-09-29.

## The substrate already fails open (independent of any gate)

Claude Code and Codex both document that a timed-out `command`/`http` hook does **not**
block: the call continues through the normal permission flow (Claude Code hooks reference;
Codex hooks docs, accessed 2026-09-29). The built-in `prompt` hook (a single-turn LLM
judge) has a 30 s timeout. So the availability-to-authorization gap is a property of the
hook mechanism every one of these gates runs on, Jev or not: a model judge that stalls is
overridden into fail-open by the host. This is the strongest generalization and needs no
corpus.

## Sample (4 gates, 2 model-judges + 2 deterministic)

| gate | judge | fail on outage | mechanism / evidence |
|---|---|---|---|
| sdkks/example-claude-settings @162a9e9 | Haiku (Anthropic/Bedrock) | **defer** | auto-approve emits an allow only on a positive judgement; "nothing on skip/error" (scripts/auto-approve.ts:11). Model-discovery errors fall back to a default id (:99-100). Stage-1 structural allowlist **does not check arguments**: "Arguments are not checked - anything after the command word is always allowed" (:291) - the same fast-path weakness the corpus flagged in jev-engineering. |
| alelaguard/agentguards-plugins @64e7e8e | hosted REST classifier | **env-toggled** | command path fails **closed** by default; `AGENTGUARDS_FAIL_OPEN=true` flips it to open (agentguards_hook.py:474-477, 815-816, 867-868). Its URL-scan path fails **open unconditionally**: "ANY failure allows (unreachable, timeout, 404...)" (:722). 429/403 carved out as non-outage (:149-166). A cache once "quietly downgraded" require-approval to allow (:129-135). |
| roboticforce/agent-guardrails @93d315c | none (regex) | fail-closed | pure pattern match, `exit 2` on a hit, `exit 0` otherwise; no network, no model, no availability axis (claude-code/scripts/git-guard.sh). |
| richardsun-voyager/agent_guardrail @4749c96 | none (rules) | fail-closed | allowlist + path-resolution + secret patterns; returns allow/block deterministically, no model call (before-tool-guard-service/tool_guard_service.py). |

## What generalizes

Every pathology the paper reports on Jev gates reappears in a non-Jev model-judge gate:

1. **Fail direction is a config toggle, not a code property.** jev-engineering flips
   fail-closed/defer by `JEV_GATE_MODE`; agentguards flips it by `AGENTGUARDS_FAIL_OPEN`.
   Same design, different vendor.
2. **Split fail direction across paths within one gate.** jev-harness fails closed on its
   TypeSafe path and fabricates/proceeds on its OpenRouter path; agentguards fails closed on
   the command path and open on the URL path. The gate's failure semantics are per-code-path,
   not per-gate.
3. **"ask"/require-approval silently downgraded to "allow."** Observed live in
   jev-engineering (guard mode x host auto-approve: 83/127 destructive allowed); documented
   as a cache bug in agentguards (:129-135). The downgrade is the dominant real-world failure,
   and it is not Jev-specific.
4. **Unchecked command arguments after a fast-path allowlist.** In the corpus (jev-engineering
   fast path) and in sdkks (:291).

**And the contrast that proves the point:** the two deterministic gates (roboticforce,
richardsun) have **no availability axis at all** - no timeout, no fail-open/closed choice,
nothing to switch off with a padded input. That is exactly the security literature's
argument for deterministic, fail-closed authorization. The paper's findings are properties
of the *probabilistic-model-in-the-path* design, which Jev popularised but does not own.

## Scope note

This is a convenience sample for external validity, not a second corpus: 4 gates, static
read, one snapshot. It shows the mechanisms transfer; it does not re-measure prevalence
off-Jev.
