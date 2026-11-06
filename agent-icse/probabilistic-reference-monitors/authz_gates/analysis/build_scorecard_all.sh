#!/usr/bin/env bash
# Rebuild artifact/scorecard-all/SCORECARD.md from the committed live results of every gate:
# Jev gates at upstream HEAD on jev-1.14.0, the deterministic baselines, sdkks (CLI judge)
# and agentguards (hosted service).
set -euo pipefail
cd "$(dirname "$0")/.."
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
R=faultinject/results
for c in main heldout oversize; do
  cat "$R/live_${c}_head.jsonl" artifact/scorecard-baselines/live_${c}.jsonl \
      artifact/scorecard-sdkks-cli/live_${c}.jsonl \
      artifact/scorecard-agentguards/live_${c}.jsonl > "$tmp/$c.jsonl"
done
python3 analysis/scorecard.py --main "$tmp/main.jsonl" --heldout "$tmp/heldout.jsonl" \
  --oversize "$tmp/oversize.jsonl" --out artifact/scorecard-all/SCORECARD.md
