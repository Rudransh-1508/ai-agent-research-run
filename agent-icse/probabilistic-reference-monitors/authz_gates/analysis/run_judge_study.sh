#!/usr/bin/env bash
# Multi-judge certification study, end to end (repo-relative; reproduces artifact/judge_* ,
# artifact/validation_*, artifact/JUDGES.md and paper/figures/judge_*).
#
#   set -a; source ~/.env; set +a        # GROQ_API_KEYS=k1,k2,... (and TYPESAFE_API_KEY for jev)
#   bash analysis/run_judge_study.sh [score|validate|figures|all]   (default: all)
#
# Protocol per judge: 3 runs on the main corpus (run 1 = calibration, r2/r3 = repeats) and
# 1 run on the held-out corpus, each followed by a --resume pass that re-asks only failed
# rows (rate limits). Validation freezes the threshold certified on run 1 and the worst case
# over all runs, then applies both to held-out and repeats. Rows already scored ok are kept,
# so re-running is cheap and never double-counts.
set -euo pipefail
cd "$(dirname "$0")/.."
STEP="${1:-all}"
mkdir -p artifact/judge_runs/logs

# tag | Groq model | extra judge flags
JUDGES=(
  "gptoss120b|openai/gpt-oss-120b|"
  "gptoss20b|openai/gpt-oss-20b|--max-tokens 1024"
  "safeguard20b|openai/gpt-oss-safeguard-20b|--max-tokens 1024"
  "qwen3|qwen/qwen3.8-27b|"
  "allam7b|allam-2-7b|--max-tokens 1024"
)
NAMES=(gptoss120b=gpt-oss-120b gptoss20b=gpt-oss-20b safeguard20b=gpt-oss-safeguard-20b
       qwen3=qwen3.8-27b allam7b=allam-2-7b)

score_one() {  # tag model flags suffix corpus [render]
  local out="artifact/judge_groq_$1$4.jsonl" log="artifact/judge_runs/logs/$1$4.log"
  local render="${6:-action}"
  # shellcheck disable=SC2086
  python3 analysis/model_judge.py --model "$2" $3 --render "$render" --corpus "$5" --out "$out" --resume >> "$log" 2>&1
  # shellcheck disable=SC2086
  python3 analysis/model_judge.py --model "$2" $3 --render "$render" --corpus "$5" --out "$out" --resume >> "$log" 2>&1
}

score() {
  for spec in "${JUDGES[@]}"; do
    IFS='|' read -r tag model flags <<<"$spec"
    for s in "" _r2 _r3; do score_one "$tag" "$model" "$flags" "$s" benchmark/corpus.jsonl & done
    score_one "$tag" "$model" "$flags" _heldout benchmark/corpus_heldout.jsonl &
  done
  # The design gate's judge, certified on exactly what the gate sends (hook rendering).
  for s in "" _r2 _r3; do
    score_one gptoss120b_hook openai/gpt-oss-120b "" "$s" benchmark/corpus.jsonl hook &
  done
  score_one gptoss120b_hook openai/gpt-oss-120b "" _heldout benchmark/corpus_heldout.jsonl hook &
  wait
  # jev through the gate's own prompt (TypeSafe), for the jev-backed design's threshold.
  if [ -n "${TYPESAFE_API_KEY:-}" ]; then
    for s in "" _r2 _r3; do
      [ -s "artifact/judge_gate_jev113$s.jsonl" ] ||
        DESIGN_JUDGE=jev JEV_MODEL=jev-1.13.0 python3 design/certify.py --out "artifact/judge_gate_jev113$s.jsonl"
    done
    [ -s artifact/judge_gate_jev113_heldout.jsonl ] ||
      DESIGN_JUDGE=jev JEV_MODEL=jev-1.13.0 python3 design/certify.py \
        --corpus benchmark/corpus_heldout.jsonl --out artifact/judge_gate_jev113_heldout.jsonl
  fi
}

validate_one() {  # prefix tag name
  python3 analysis/judge_validation.py --name "$3" --calib "artifact/$1$2.jsonl" \
    --repeats "artifact/$1${2}_r2.jsonl" "artifact/$1${2}_r3.jsonl" \
    --heldout "artifact/$1${2}_heldout.jsonl" --out-prefix "artifact/validation_${1#judge_}$2"
}

validate() {
  for nm in "${NAMES[@]}"; do validate_one judge_groq_ "${nm%%=*}" "${nm#*=}"; done
  validate_one judge_groq_ gptoss120b_hook "gpt-oss-120b (gate prompt)"
  [ -s artifact/judge_gate_jev113.jsonl ] && validate_one judge_gate_ jev113 "jev-1.13.0 (gate prompt)"
  python3 analysis/judge_table.py \
    $(for nm in "${NAMES[@]}"; do echo "artifact/validation_groq_${nm%%=*}.json"; done) \
    artifact/validation_groq_gptoss120b_hook.json artifact/validation_gate_jev113.json \
    --out artifact/JUDGES.md
}

figures() {
  python3 analysis/judge_figures.py \
    "jev-1.13.0=artifact/threshold_recipe_noul.json" \
    "jev-1.14.0=artifact/jev-1.14.0/threshold_recipe_noul.json" \
    $(for nm in "${NAMES[@]}"; do echo "${nm#*=}=artifact/validation_groq_${nm%%=*}.json"; done)
}

case "$STEP" in
  score) score ;;
  validate) validate ;;
  figures) figures ;;
  all) score; validate; figures ;;
  *) echo "usage: $0 [score|validate|figures|all]" >&2; exit 2 ;;
esac
