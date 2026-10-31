#!/usr/bin/env bash
# Score gates end to end: main + held-out + padded (oversize) corpora, each call run once per
# host mode with permission_mode in the payload, then one scorecard table.
#
# Usage:
#   benchmark/run_scorecard.sh OUT_DIR GATE [GATE...]
#   DESIGN_CMD="python3 /path/to/my_gate.py" benchmark/run_scorecard.sh OUT_DIR design
#
# Gate names are recipe names in faultinject/recipes.py (dcg, cc-safety-net, jev-guard,
# jev-engineering, "jev-engineering(guard)", "jev-engineering(auto)", design, ...).
# Model-backed gates need TYPESAFE_API_KEY; GATE_REPOS / LIVE_JEV_MODEL select the gate
# snapshot and the pinned model as in run_gates_live.py.
set -euo pipefail
cd "$(dirname "$0")/.."

OUT="$1"; shift
mkdir -p "$OUT"
[ -f benchmark/corpus_oversize.jsonl ] || python3 benchmark/build_oversize.py

for corpus in main heldout oversize; do
  file=benchmark/corpus.jsonl
  [ "$corpus" = heldout ] && file=benchmark/corpus_heldout.jsonl
  [ "$corpus" = oversize ] && file=benchmark/corpus_oversize.jsonl
  echo "--- $corpus $(date +%H:%M:%S)"
  python3 faultinject/run_gates_live.py --per-mode --gates "$@" --corpus "$file" \
    --out "$OUT/live_${corpus}.jsonl"
done

python3 analysis/scorecard.py --main "$OUT/live_main.jsonl" --heldout "$OUT/live_heldout.jsonl" \
  --oversize "$OUT/live_oversize.jsonl" --out "$OUT/SCORECARD.md"
echo "=== SCORECARD COMPLETE $(date +%H:%M:%S) ==="
