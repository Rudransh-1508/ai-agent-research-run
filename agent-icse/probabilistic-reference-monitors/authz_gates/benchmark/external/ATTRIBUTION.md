# External attack sources

The corpus's `attack_external` and `lolbin` splits are derived from two public catalogs.
Both are used here defensively - to test whether deployed authorization gates stop real
attacker commands - and every included command is label-verified by execution in
`benchmark/sandbox/`.

## Atomic Red Team (`attack_external` split)

- Source: Red Canary, Atomic Red Team, https://github.com/redcanaryco/atomic-red-team
- License: MIT (Copyright (c) 2018 Red Canary, Inc.)
- `atomic_red_team.jsonl` holds the derived commands: every Linux `sh`/`bash` atomic in our
  threat-model techniques (data destruction, defense evasion, exfiltration), rendered with
  its default input arguments by `extract_atomics.py`, then kept only if its destructive or
  exfiltration effect was observed in the offline sandbox (11 of 93 in-scope atomics; the
  rest need network tool-downloads, target `/tmp`, or are credential *collection* that is
  out of our deletion/exfil threat model). Each item keeps its MITRE ATT&CK technique id and
  the atomic's `auto_generated_guid` for traceability.

## GTFOBins (`lolbin` split)

- Source: GTFOBins, https://gtfobins.github.io/
- License: GPLv3. GTFOBins' own text is **not** redistributed here. The `lolbin` split uses
  the *techniques* it documents (legitimate binaries - `awk`, `tar`, `sed`, `env`, `nohup`,
  `perl`, `tee`, `dd`, ...- abused to delete, overwrite or exfiltrate), but the command
  strings in `build_corpus.py` (`LOLBIN_PAIRS`) are our own, written against the sandbox's
  seeded state, each paired with a benign twin using the same binary. GTFOBins is cited as
  the source of the technique, not copied.
