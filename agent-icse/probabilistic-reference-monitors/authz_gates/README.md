# authz_gates — Probabilistic Reference Monitors study

Implementation for the AGENT @ ICSE 2027 paper (2nd International Workshop on Agentic
Engineering; short paper, <=5 pp incl. references, IEEE template, single-anonymous;
deadline 2026-11-13 AoE, https://icse2027-agent.hotcrp.com/): an empirical study of
probabilistic decision-model gates in the authorization path of coding agents.
Originally prepared for SE4AgenticAI 2026; `PREREGISTRATION.md` keeps that original target.

## Layout

- `PREREGISTRATION.md` — predictions and analysis plan, registered 2026-09-21 before data collection.
- `corpus/` — gate enumeration from yibie/awesome-jev, pinned-SHA cloning, feature
  extraction (thresholds, provenance, error paths), fail-open classification.
  Output: `corpus/gates.json`, `corpus/CORPUS_TABLE.md`.
- `client/` — pinned Jev client (`jev-1.13.0`) with gateway support, retry instrumentation
  that records 429/5xx/timeout as first-class outcomes, raw JSONL logging, mock mode.
- `benchmark/` — programmatic tool-call risk corpus builder (clear / ambiguous /
  adversarial tiers, documented rubric) and the benchmark runner.
- `analysis/` — fail-open tabulation, cost-sensitive (Chow) threshold analysis,
  selective-risk curves, bootstrap CIs, Holm correction.
- `artifact/` — raw JSONL of every API call + recount script inputs (generated; dated).

## What needs a human

- **API access**: set one of `TYPESAFE_API_KEY`, `OPENROUTER_API_KEY`,
  `VERCEL_AI_GATEWAY_KEY`, `CLOUDFLARE_AI_GATEWAY_KEY`. Everything in `corpus/` runs
  without a key; `benchmark/` and the measurement half of `analysis/` need one.
  Until a key is available, everything runs in `--mock` mode (heuristic scripted
  provider — produces NO behavioral evidence, mechanics only).
- Budget: single-digit dollars (comparable study cost $0.06-$0.18).

## How to run

```sh
# tests (offline, mock provider)
python3 -m unittest discover            # from this directory

# build the corpus (deterministic; writes corpus.jsonl, corpus_heldout.jsonl, RUBRIC.md)
python3 benchmark/build_corpus.py

# run a gate over the corpus — mock mode (offline):
python3 benchmark/run_benchmark.py --mock --gate noul_vendor_0.9 \
    --out benchmark/results_noul09.jsonl
# real API (needs a key):
python3 benchmark/run_benchmark.py --gateway typesafe --gate noul_vendor_0.9 \
    --out benchmark/results_noul09.jsonl
# re-run deterministically from a previous artifact log:
python3 benchmark/run_benchmark.py --replay artifact/benchmark_noul_vendor_0.9.jsonl \
    --gate noul_vendor_0.9 --out benchmark/results_noul09.jsonl

# gate presets: noul_vendor_0.9, noul_0.5, choice_3way, score_5
# (or pass a JSON file: {"name","primitive","claim"/"options"/"levels","threshold"})

# pre-registered analyses (work on mock or real results)
python3 analysis/threshold_analysis.py --results benchmark/results_noul09.jsonl \
    --out-prefix analysis/out/threshold_noul09
python3 analysis/fail_open.py --gates corpus/gates.json \
    --out-prefix analysis/out/fail_open
```

## Rules

- No git mutations from tooling. Corpus repos are cloned into `corpus/repos/` (gitignored).
- Every number in the paper must be reproducible by a script in this directory.
- The model id is pinned to `jev-1.13.0`; the client refuses the `jev-latest` /
  `jev-preview` aliases for measurements.
- Mock-mode outputs are mechanics checks, never paper numbers.
