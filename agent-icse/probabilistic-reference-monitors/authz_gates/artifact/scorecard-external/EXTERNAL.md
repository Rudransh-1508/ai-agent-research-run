# External attack split: real MITRE ATT&CK commands (Atomic Red Team)

11 commands drawn from Atomic Red Team (MIT; `benchmark/external/`), one per Linux `sh`/`bash` atomic in our threat-model techniques whose destructive or exfiltration effect was confirmed in the sandbox. Each is a real attacker command mapped to a MITRE ATT&CK technique. Default = a human answers; bypass = a deferred call runs. Raw: `artifact/scorecard-external/live_external.jsonl`.

| gate | run (default) | run (bypass) | ATT&CK techniques fully blocked (bypass) |
|---|---|---|---|
| jev-guard | 0/11 | 1/11 | T1048 Exfil over alt protocol, T1567 Exfil over web service |
| jev-engineering | 0/11 | 0/11 | T1048 Exfil over alt protocol, T1070 Indicator removal, T1567 Exfil over web service |
| jev-engineering(guard) | 0/11 | 10/11 | none |
| jev-engineering(auto) | 0/11 | 10/11 | none |
| dcg | 0/11 | 8/11 | none |
| cc-safety-net | 0/11 | 7/11 | T1048 Exfil over alt protocol, T1567 Exfil over web service |
| sdkks(cli) | 4/11 | 6/11 | none |
| agentguards | 6/11 | 6/11 | none |
