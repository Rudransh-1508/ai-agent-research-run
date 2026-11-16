# Reproducibility and versions

Every number in `RESULTS_COMPARISON_2026-11-02.md` comes from a committed raw file. Hosted
models drift and are retired (Groq retired `llama-3.3-70b-versatile` before this study used
it; TypeSafe moved `jev-latest` from 1.13.0 to 1.14.0 mid-study), so the study is built to
replay from recorded scores and to say exactly which parts need a live service.

## Replays offline (no keys, no network)

| what | command | input |
|---|---|---|
| all unit tests (80) | `python3 -m unittest discover` | fixtures |
| corpus, byte-identical | `cd benchmark && python3 build_corpus.py` | seeds 20260921 / 20260922 |
| threshold certificates, alpha sweep | `analysis/threshold_recipe.py`, `analysis/alpha_sweep.py` | `artifact/judge_*.jsonl`, `artifact/results_main_noul_vendor_0.9.jsonl` |
| frozen-threshold validation, judge table | `bash analysis/run_judge_study.sh validate` | `artifact/judge_*.jsonl` |
| paper figures (pgfplots + CSV) | `bash analysis/run_judge_study.sh figures` | `artifact/validation_*.json` |
| gate scorecards and CIs | `analysis/scorecard.py`, `analysis/ci.py`, `analysis/build_scorecard_all.sh` | `artifact/scorecard-*/live_*.jsonl`, `artifact/design-*/live_*.jsonl` |
| automated rater panel report | `python3 analysis/llm_raters.py report` | `artifact/llm_raters/*.jsonl` |
| deterministic gates (dcg, cc-safety-net, design B) | `benchmark/run_scorecard.sh` | release binaries in `baselines/` |
| fault matrix for model-backed gates | `faultinject/run_faults.py` | local fault server, stub keys |

## Needs a live service (re-running measures the service as it is that day)

| what | service | pinned to |
|---|---|---|
| jev-backed gates, jev judge | TypeSafe API (`TYPESAFE_API_KEY`) | `jev-1.13.0` (main measurements; echoed in every row), `jev-1.14.0` (drift re-check) |
| Groq judges, design A with Groq judge, rater panel | Groq (`GROQ_API_KEYS`) | `openai/gpt-oss-120b`, `openai/gpt-oss-20b`, `openai/gpt-oss-safeguard-20b`, `qwen/qwen3.8-27b`, `allam-2-7b`, as served 2026-11-17; temperature 0, JSON mode |
| AgentGuards hosted classifier | agentguards.co (`AGENTGUARDS_API_KEY`) | plugin 0.2.35 at 64e7e8e |
| sdkks LLM fallback | the user's Claude Code login (Haiku) | as served at measurement |
| sandbox label verification | Docker, local only (no network at probe time) | images `prm-sandbox:7` (corpus), `:8`/`:9` (blind set) |

Temperature 0 is not determinism on hosted serving: run-to-run spread is measured and
reported per judge (RESULTS sec 17), and the deployed thresholds are certified on the worst
case over three runs for that reason.

## Versions measured

| component | version |
|---|---|
| Claude Code (host, live measurements) | 2.1.285; docs re-checked on 2.1.325 (2026-11-17) |
| jev-guard | snapshot cda06c4 (2026-10-02); recipe SHA 94996ea |
| jev-engineering | snapshot 412adce (2026-10-25); recipe SHA 3161dbf |
| jev-harness / jev-belay / limpet | 506cdca / 467968e / 7a841b0 |
| sdkks example-claude-settings | 162a9e9 (2026-05-27) |
| agentguards-plugins | 64e7e8e (2026-09-28) |
| dcg (destructive_command_guard) | v0.15.3 release binary, sha256 50a1a507...98d7 |
| CC Safety Net | 2.7.1 prebuilt dist |
| Design A / Design B | frozen at git tag `design-freeze-2026-11-17` |
| Atomic Red Team | original split as extracted 2026-11-11; blind set from commit a0e3f9b |

## Known non-reproducible inputs

- Hosted model weights and serving behaviour change without notice; the recorded scores are
  the evidence, a re-run is a new measurement.
- Atomic Red Team's default branch moves; the blind set records its commit, and the
  extractor plus `blind_candidates.jsonl` fix the candidate list.
- Run logs keep absolute paths of the machine they ran on (`artifact/judge_runs/`).
