#!/bin/bash
# Condition 2: the host runs everything (bypassPermissions), the gate is the only check;
# Bash stays inside the strict sandbox. Same tasks and gates as run_all.sh.
set -e
cd "$(dirname "$0")/.."
python3 agent_trials/run_trials.py --gate dcg --reps 2 --mode bypass
for t in discard branch; do python3 agent_trials/run_trials.py --gate cc-safety-net --task $t --reps 2 --mode bypass; done
