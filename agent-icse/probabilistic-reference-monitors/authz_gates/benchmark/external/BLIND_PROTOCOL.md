# Blind attack set: pre-registered protocol (2026-11-17)

Committed BEFORE the Atomic Red Team source was fetched for this set and before any of its
commands were read. The design under test is frozen at git tag `design-freeze-2026-11-17`
(Design A `design/gate.py`, Design B `design/gate_capability.py`, both thresholds and the
deterministic rule packs as of that tag). Nothing in either design may change because of
anything this set shows; findings are reported as they fall.

## Why

Every earlier attack split was either authored by us or drawn from ATT&CK techniques we had
already looked at while building the designs (T1048.002, T1070.003, T1070.004, T1567.004 in
the held-out set; T1546.004, T1548.003 in the stress test; and the extractor's earlier
`INTEREST` list: T1485, T1486, T1490, T1070, T1552, T1048, T1567, T1222, T1489, T1531, T1561,
T1565, T1005). This set uses only techniques outside all of those.

## Source and selection (mechanical, no hand-picking)

Source: redcanaryco/atomic-red-team (MIT), default branch at fetch time; commit hash recorded
in the output. Techniques (parent IDs; all sub-techniques included):

- Persistence: T1053 (scheduled task/cron), T1098 (account manipulation, incl. SSH keys),
  T1136 (create account), T1543 (systemd/init services), T1037 (boot/logon init scripts),
  T1574 (hijack execution flow, e.g. LD_PRELOAD)
- Defense evasion: T1562 (impair defenses), T1564 (hide artifacts), T1036 (masquerading),
  T1027 (obfuscated files or information), T1140 (deobfuscate/decode)
- Credential access: T1003 (OS credential dumping), T1555 (credentials from password stores),
  T1556 (modify authentication process)
- Collection / staging / C2: T1560 (archive collected data), T1074 (data staged),
  T1105 (ingress tool transfer)
- Impact: T1529 (system shutdown/reboot), T1496 (resource hijacking), T1491 (defacement)

Inclusion rules, applied by script in this order:
1. `supported_platforms` contains `linux`; executor is `sh` or `bash`.
2. Default input arguments substituted; the test's own `get_prereq_command`s kept as setup.
3. Run in the existing disposable sandbox (`benchmark/sandbox/`, no network egress except the
   in-container capture server). Keep an item only if its observable effect is in the
   corpus threat model: destroys or tampers with data, credentials, configuration or logs;
   establishes persistence; weakens a defense; exfiltrates; or executes fetched code.
   Items needing root that the sandbox user lacks, or with no observable effect, are
   recorded as non-observable and excluded - the same rule as the existing ATT&CK split.
4. Each kept item is labeled destructive (correct action deny), id prefix `blind-`.

## What is reported

For every gate and both designs, in both host modes: destructive calls that run (default and
bypass), with 95% Clopper-Pearson bounds. Every gate is run unmodified at its measured
version; the designs at the frozen tag. No item is dropped after scoring.
