#!/bin/bash
# The trial matrix: dcg denies the natural command for all four tasks; cc-safety-net only for
# the git tasks (it allows project-local rm -rf by design), so it runs those two.
set -e
cd "$(dirname "$0")/.."
python3 agent_trials/run_trials.py --gate dcg --reps 2
for t in discard branch; do python3 agent_trials/run_trials.py --gate cc-safety-net --task $t --reps 2; done
