#!/usr/bin/env bash
# Full benchmark suite for the Probabilistic Reference Monitors study.
# Requires TYPESAFE_API_KEY in the environment. ~2,200 calls, ~$0.05.
set -uo pipefail
cd "$(dirname "$0")/.."

GATES="noul_vendor_0.9 noul_0.5 choice_3way score_5"

echo "=== main corpus (346 items x 4 gates) ==="
for g in $GATES; do
  echo "--- $g main $(date +%H:%M:%S)"
  python3 benchmark/run_benchmark.py --corpus benchmark/corpus.jsonl --gate "$g" \
    --out "artifact/results_main_${g}.jsonl" \
    --artifact-log "artifact/calls_main_${g}.jsonl" > "artifact/log_main_${g}.txt" 2>&1
done

echo "=== held-out adversarial (80 items x 4 gates) ==="
for g in $GATES; do
  echo "--- $g heldout $(date +%H:%M:%S)"
  python3 benchmark/run_benchmark.py --corpus benchmark/corpus_heldout.jsonl --gate "$g" \
    --out "artifact/results_heldout_${g}.jsonl" \
    --artifact-log "artifact/calls_heldout_${g}.jsonl" > "artifact/log_heldout_${g}.txt" 2>&1
done

echo "=== noise floor (50 items x 10 repeats, noul_vendor_0.9) ==="
for i in $(seq 1 10); do
  echo "--- noise repeat $i $(date +%H:%M:%S)"
  python3 benchmark/run_benchmark.py --corpus benchmark/corpus_noise50.jsonl --gate noul_vendor_0.9 \
    --out "artifact/results_noise_r${i}.jsonl" \
    --artifact-log "artifact/calls_noise_r${i}.jsonl" > "artifact/log_noise_r${i}.txt" 2>&1
done

echo "=== ALL RUNS COMPLETE $(date +%H:%M:%S) ==="
