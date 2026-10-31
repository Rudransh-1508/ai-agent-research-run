#!/usr/bin/env bash
# Freshness re-check: the paper's four gate configurations on a newer pinned model.
# Usage: benchmark/run_recheck.sh jev-1.14.0   (needs TYPESAFE_API_KEY)
set -uo pipefail
cd "$(dirname "$0")/.."

MODEL="$1"
OUT="artifact/$MODEL"
mkdir -p "$OUT"
for corpus in main heldout; do
  file=benchmark/corpus.jsonl
  [ "$corpus" = heldout ] && file=benchmark/corpus_heldout.jsonl
  for g in noul_vendor_0.9 noul_0.5 choice_policy score_risk5; do
    if [ -f "$OUT/results_${corpus}_${g}.summary.json" ]; then echo "--- skip $g $corpus (done)"; continue; fi
    echo "--- $MODEL $g $corpus $(date +%H:%M:%S)"
    python3 benchmark/run_benchmark.py --model "$MODEL" --corpus "$file" --gate "$g" \
      --out "$OUT/results_${corpus}_${g}.jsonl" \
      --artifact-log "$OUT/calls_${corpus}_${g}.jsonl" > "$OUT/log_${corpus}_${g}.txt" 2>&1
  done
done
echo "=== RECHECK COMPLETE $(date +%H:%M:%S) ==="
