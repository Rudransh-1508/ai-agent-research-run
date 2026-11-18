# Framing evidence: what the gates promise and what the host documents

Answers the expected reviewer objection "bypass/auto mode is the user's choice, so a call that
runs there is not a gate failure". Quotes are verbatim; host docs accessed 2026-11-17
(Claude Code 2.1.325 installed locally; the live measurements ran on 2.1.285). Gate READMEs
are from the snapshots measured (`corpus/repos_head/`, `comparison_nonjev/repos/`,
`baselines/`).

## 1. The gates promise protection, with no carve-out for unattended modes

- **jev-guard** (leepokai/jev-guard README): *"Destructive calls are **denied**; risky ones
  **require the user's approval** ..."*, and it pitches itself as auto mode: *"If you want auto
  mode outside Claude Code, or a second opinion inside it, this is the build."*
- **jev-engineering / jev-gate** (eugeniughelbur/jev-engineering README): *"A strict second
  lock on every command your coding agent runs"*; *"Clearly dangerous, like reading `~/.ssh`
  or `~/.aws/credentials` ...: blocked, with the reason"*; *"Unsure, like `git push --force`:
  your agent's normal prompt, or its own auto mode, takes over."* The last sentence is the
  seam: "unsure" is delegated to whatever the host does next, which in bypass mode is "run".
- **CC Safety Net** (kenryu42/cc-safety-net README): *"blocks destructive commands and access
  to secrets such as SSH keys and `.env` files before the tool call runs"*; dangerous calls
  *"never run"*.
- **dcg** (Dicklesworthstone/destructive_command_guard README): *"intercepts destructive
  commands *before* they execute, blocking them"*; feature *"Bounded Failure Policy: Analysis
  timeouts become explicit review/block outcomes"*.
- **AgentGuards** (alelaguard/agentguards-plugins README): *"Enforcing hooks (input, Bash,
  web-content ...)"*, *"destructive-command"* blocking.
- **sdkks/example-claude-settings** README: PreToolUse hooks *"ARE the security boundary.
  They can block commands with exit code 2."*, so *"we can be aggressive with auto-approval"*.

## 2. The host documents the seams the paper measures

Claude Code, Hooks reference (https://code.claude.com/docs/en/hooks):
- Failure is fail-open by default: *"On most events, when a hook fails or times out, Claude
  Code still carries out the action. A policy hook with a wrong path or a crashing script then
  lets everything through."* and *"Non-blocking error: your hook exits with any other code, or
  fails in some other way, such as not starting or printing invalid JSON. The action goes
  ahead, except for hooks whose failure blocks the action"*.
- The host-side fix is recent and opt-in: *"To block the action instead, set
  `"onFailure": "block"` on a `command` or `http` hook. Requires Claude Code v2.1.295 or
  later."* (after the 2.1.285 measured here; unset means the action goes ahead).
- Timeout: *"`timeout` ... Seconds before canceling ... Defaults: 600 for `command`, `http`,
  and `mcp_tool` ..."*.

Claude Code, Permission modes (https://code.claude.com/docs/en/permission-modes):
- bypassPermissions: *"disables permission prompts and safety checks so tool calls execute
  immediately"*; warnings *"Only use this mode in isolated environments ..."* and
  *"`bypassPermissions` offers no protection against prompt injection or unintended
  actions."*
- auto: *"A separate classifier model reviews actions before they run ... Explicit ask rules
  still force a prompt."*; warning *"Auto mode reduces permission prompts but does not
  guarantee safety."*
- acceptEdits auto-approves `rm`, `mv`, `cp`, `sed` inside the working directory, also when
  wrapped by *"process wrappers such as `timeout`, `nice`, or `nohup`"* - the same
  launcher-wrapping the paper found argument-blind allowlists miss.

## 3. How to use this in the paper

- The objection is answered by the gates' own claims (sec 1): they sell protection exactly
  where the host provides none (bypass) or a classifier (auto). A gate whose "unsure" or
  "failed" verdict becomes "run" in those modes does not deliver what it advertises; the
  measured leak counts are the size of that gap.
- The host documents fail-open hook failure and only recently added an opt-in fix; this is
  vendor confirmation that the failure path is part of the contract a gate must handle itself,
  which the composed design does (total failure function, bounded model budget).

## 4. Correction this forces (RESULTS sec 18, finding 3)

The fault harness kills a hook at 60s (`run_faults.py --host-timeout`, labelled "Claude Code
default: 60"). The documented default for command hooks is 600s. So the design's old jev path
(retries up to ~2 minutes) is killed - and the call proceeds - only where a hook timeout below
its worst-case retry time is configured, not at today's default. The finding stands as a
configuration-dependent seam (any gate whose worst-case latency can exceed its configured
timeout fails open on hosts without `onFailure: "block"`), and the 20s model budget is still
the right fix (it makes the gate's failure path independent of host configuration and keeps
latency bounded), but the paper must not say the default configuration was bypassed.

## 5. A maintainer's stated threat model (cc-safety-net, 2026-11-18)

Closing issue kenryu42/cc-safety-net#368 (6 sandbox-verified bypasses on 2.7.15) as not
planned, the maintainer wrote: *"These were found by probing rather than by an agent doing
real work. CC Safety Net targets the mistakes helpful agents make, not every shape a probe can
construct. Missed-detection reports now need an agent transcript showing the command was run
during a real task (see CONTRIBUTING.md). For adversarial agents, an OS sandbox is the right
layer."*

Use in the paper: this is the clearest statement of the scope gap the study measures. The
gate's README promises that dangerous calls "never run" and that wrapping a command does not
hide it; its maintainer scopes that promise to cooperative agents, and assigns adversarial
inputs (prompt injection, disguised commands) to a different layer. Users who install the
gate to run in bypass/auto mode - exactly where an injected or disguised command would run -
are relying on a guarantee the tool does not make. The paper should (a) report rule-gate
misses on evasion/LOLBin items as outside such gates' stated threat model, not as defects,
and (b) make the point that the advertised protection and the scoped threat model diverge,
which is itself an integration seam: nothing in the host tells the user which threat model
the installed gate assumes.
