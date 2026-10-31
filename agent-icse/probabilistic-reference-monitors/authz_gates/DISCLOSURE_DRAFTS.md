# Responsible-disclosure drafts (NOT SENT)

Drafted 2026-10-31 for the AGENT @ ICSE 2027 submission (deadline 2026-11-13). Each note
goes to the maintainer privately first (GitHub security advisory where enabled, otherwise
the email in the repo), with a 14-day window before the preprint goes public. Every claim
below was observed with our harness at the pinned SHA and re-checked by reading upstream
HEAD on 2026-10-31; see `RECHECK_2026-10-31.md`.

## eugeniughelbur/jev-engineering

- **Padded-command bypass.** A Bash command padded past Jev's token limit (~372k chars)
  gets HTTP 400 `max_tokens_exceeded` in under a second; `decide()` then falls back to
  "ask", which `guard` and `auto` modes turn into exit 0, so under a host mode that runs
  unblocked calls (e.g. `bypassPermissions`) the command executes. `enforce` mode blocks.
  The hard rules added on 2026-09-28 catch our specific probe (`~/.aws/credentials`), but
  any destructive command outside the 10 regexes is still exposed. Suggested fix: reject
  (or truncate with a deny) any state over a fixed size before calling the model.
- **Empty-answers crash.** A 200 response with an empty `answers` map raises `KeyError`
  at `jev_gate.py:198` (`answers["destructive"]`); Claude Code treats the non-zero exit as
  a non-blocking error and runs the call. Suggested fix: treat a missing answer as the
  fallback, and let `enforce` block on it.
- **guard mode under auto-approval.** In `guard` mode, every "ask" verdict becomes exit 0.
  Under a host mode that runs unblocked calls, 88/131 clearly destructive benchmark calls
  ran (64/64 on held-out attack families). Worth a README warning that `guard` relies on a
  confirming host.
- **Allowlist treats `git branch -D` as read-only.** The fast-path pattern
  `^\s*git\s+(status|diff|log|branch|remote|fetch)\b` in `policy.json` matches
  `git branch -D <name>`; in `auto` mode that returns `allow`, so a branch is force-deleted
  with no prompt even in Claude Code's default mode (observed live, 3/3 such benchmark
  items, 2026-10-31). Suggested fix: anchor `branch` to its listing forms
  (`git branch(\s+(-a|-r|--list|-v+))*\s*$`) or drop it from the fast path.

## leepokai/jev-guard

- **Padded-command bypass.** `assessAction` sends the full tool input to Jev without the
  `truncate()` that `scanContent` uses (`src/guard.js`); an oversized command gets HTTP 400
  and the hook defers (fail-open by design, `hook.js`). Observed live at the pinned SHA:
  block at ~90 chars, defer when padded. Suggested fix: apply `truncate()` (or deny) on the
  action path too, so oversize cannot turn a block into a defer.

## valentynkit/jev-belay and noplan-inc/limpet

- Every model failure (400, 429, 5xx, timeout, malformed, connection refused) **proceeds**:
  the check is skipped. Documented as intentional; worth stating in the README that this
  makes the gate removable by anyone who can make the model call fail (e.g. by padding).
- limpet: the shipped default block threshold is infinite, so out of the box it never
  blocks; documented, but easy to miss.

## ismaelsoilet/jev-harness

- At the pinned SHA, the OpenRouter provider substituted a regex-based *simulated* answer on
  a connection failure and the verify gate acted on it (proceeds); the TypeSafe path failed
  closed. Since then (README, upstream HEAD 2026-10-31) the default policy is fail-open for
  every provider, TypeSafe included: after retries the gate decides on the offline
  deterministic engine, marked `degraded_reason`, and only `--fail-closed` restores the old
  behaviour. The marking is a real improvement, but a gate that verifies work should not
  pass it on a fabricated answer by default. Suggested fix: make `--fail-closed` the default
  for the verify/gate commands, keeping fail-open for advisory commands.
