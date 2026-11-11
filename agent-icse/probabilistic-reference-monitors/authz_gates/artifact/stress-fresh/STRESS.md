# Generalization stress test: tactics the gate was never tuned on

The design's deny layer covers indicator-removal (T1070) plus dcg's packs, and its threshold
was certified on the main corpus. To test for overfitting we ran both designs against ATT&CK
tactics they were **not** tuned on: persistence and privilege escalation, drawn fresh from
Atomic Red Team (MIT; `benchmark/external/atomic_red_team_persist_privesc.jsonl`), sandbox-
verified (6 of 46 in-scope Linux atomics produced an observable effect offline - shell-profile
injection T1546.004 and sudoers tampering T1548.003; the rest need systemd / network / a cron
daemon we cannot give).

Result (`items.jsonl`, `design_A.jsonl`, `design_B.jsonl`): **both designs block all 6, 0
leaks, in both host modes.**

| design | leaks (any mode) of 6 | default | bypass |
|---|---|---|---|
| A (model-in-the-loop) | 0 | 3 deny + 3 ask | 6 deny |
| B (pure capability)   | 0 | 6 ask | 6 deny |

The asymmetric/deterministic layers generalize to unseen tactics: persistence via
`echo ... >> ~/.bashrc` / `/etc/profile` and privesc via `sudo sed -i ... /etc/sudoers` are
refused because they are writes or redirects to sensitive paths, or run through a command
launcher (`sudo`) - none of which any positive-allow capability covers - regardless of the
specific technique. The gate did not need a rule per tactic; "only allow a small parsed safe
set, refuse the rest" is what makes it generalize. This is the evidence against the
same-corpus-overfitting objection, within the limits of what an offline sandbox can exhibit.
