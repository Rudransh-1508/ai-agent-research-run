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

## Dicklesworthstone/destructive_command_guard (dcg v0.15.3, release binary, default config)

- **Oversized hook input is allowed.** A Bash command padded to ~372k characters makes the
  hook payload exceed the 262,144-byte stdin limit; dcg logs `stdin input (372310 bytes)
  exceeds limit (262144 bytes); allowing command (fail-open)`. The README's bounded failure
  policy says an oversized payload "is not allowed blind" because dcg scans the raw text;
  in our runs the window scan caught the dangerous part when it came first (48/114 blocked)
  but almost never when the padding came first (3/114). Because the payload is not parsed,
  the `permission_mode: bypassPermissions` downgrade to deny does not apply either: 175/228
  padded destructive calls would run under bypassPermissions (observed 2026-11-02).
  Suggested fix: treat an over-limit payload as unverified (ask, or deny under
  bypassPermissions/dontAsk), or make `fail_closed` the default for over-limit input.

## alelaguard/agentguards-plugins (@64e7e8e, Claude Code hook)

- **An empty 200 response allows.** `result.get("decision", "allow")` turns a valid but empty
  authorize response (`{}`) into an explicit allow, which skips Claude Code's prompt, in the
  shipped fail-closed configuration that blocks every other failure (400/429/500/503,
  timeout, malformed body, connection refused). Suggested fix: a missing decision is a
  failure and follows the fail-closed path.
- **No API key means allow.** With no key configured, PreToolUse returns an explicit
  `permissionDecision: allow` for Bash, which also skips the host's prompt; the in-code
  comment says a missing key "is a setup gap, not a security event". Suggested fix: emit
  nothing (defer to the host prompt) rather than allow.

## sdkks/example-claude-settings (@162a9e9)

- **The judge sees only the first 1,000 characters.** `stage2` sends `command.slice(0, 1000)`
  to the model. With benign padding first, the dangerous command never reaches the model
  (verified: the request body did not contain it), and a "safe" verdict on the filler
  auto-approves the whole command at the PermissionRequest prompt. Suggested fix: refuse
  (stay silent) when the command is longer than the window, rather than judging a prefix.
- **API failures spawn the Claude CLI as a fallback judge** (`claude -p --model haiku`):
  every failed model call in our fault matrix fell through to it (200 invocations across
  trials, stubbed in our harness). Worth documenting: a permission hook that starts
  another agent process on failure.
- The structural allowlist accepts `kubectl`, `rm`, `curl`, `bash` and others with
  unchecked arguments; this is documented as relying on the paired block hook, which
  covers some but not all misuse (e.g. `terraform destroy -auto-approve` passes the block
  hook and reaches the model).
