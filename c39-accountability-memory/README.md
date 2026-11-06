# C39 — reconstruction–accountability frontiers for compressed multi-agent records

Companion repository to *How Much Memory Does Accountability Cost?*, submitted
to AAMAS 2027, GTEP track (see `docs/track_decision_2026-09-23.md`). The paper
asks what a compressed execution record must retain so that individual agents
can still be paid, credited or blamed for their own work, and answers it
exactly.

## Run it

Everything below assumes the pinned environment (`.venv310`: Python 3.10.11,
NumPy 2.2.6, SciPy 1.15.3 — see `environment.json`) and can be run from anywhere;
paths resolve from the repo root, not the shell's working directory.

```powershell
.\.venv310\Scripts\python.exe run.py verify      # script faults + archive integrity + 99 solver-free checks
.\.venv310\Scripts\python.exe run.py audit       # every number in the paper vs its artifact
.\.venv310\Scripts\python.exe run.py score       # pre-registered predictions, scored
.\.venv310\Scripts\python.exe run.py figures     # regenerate the paper's figures
.\.venv310\Scripts\python.exe run.py package     # rebuild the submission archive
```

On macOS or Linux the same tasks run under any Python 3.10+, with the same
commands:

```bash
python3 run.py verify    # and audit / score / figures / package / all
```

`verify`, `audit`, `score` and `figures` need no third-party package at all —
NumPy and SciPy are needed only by the harnesses in `experiments/`, which
regenerate the artifacts rather than check them. Generated files are written
with LF endings on every platform, so re-running `figures` or `package` off
Windows leaves the archive hashes intact.

`run.py all` does the first four in order. None of them needs a solver, a network
connection, or more than a few seconds.

## Layout

| path | what is in it |
|---|---|
| `src/` | the method and everything that checks it — `kflat_theory.py`, `verify_all.py`, the paper-vs-artifact audit, `check_scripts.py` (static faults the numeric checks cannot see), the prediction scorer, figure and manifest tools |
| `experiments/` | the harnesses that produce results: the mechanism sweep, the episode simulator, the intermediate-$K$ frontier, the prior-threshold MILPs |
| `results/` | every JSON an experiment wrote, with `results/logs/` for the console output that produced it |
| `docs/` | the research record: `research_state.md` (what is claimable), `experiment_log.md` (chronological, including what failed), the pre-registration, the literature review, the paper plan. `docs/archive/` holds superseded session documents |
| `paper/` | LaTeX source; see `paper/README.md` for build and status |
| `archive/` | one-off scripts from earlier sessions, kept for provenance. Their outputs are frozen in `results/` |
| `prepinned_backup/` | outputs from before the environment was pinned, kept as evidence that the re-run reproduces them |
| `c39/` | `paths.py`, which resolves every file from the repo root |
| `dist/` | the built submission archive |

`artifact_hashes.json` and `environment.json` stay at the root: they describe the
whole tree, so they do not belong inside any part of it.

## What is checked, and how

* **`verify_all.py`** is an independent reimplementation that shares no code with
  the one that produced the results. 99 checks, no solver, no search.
* **`audit_paper_numbers.py`** parses the LaTeX and compares every printed number
  against the JSON it came from, so the paper cannot drift from the experiments.
* **`analyse_experiment.py`** scores predictions that were written down and
  hashed *before* each harness existed. Four were wrong and are reported as
  wrong.
* Both verifiers have been mutation-tested: deliberately corrupted witnesses,
  tables and constants are caught 8/8 and 8/8.

`docs/ARTIFACT.md` is the referee-facing description, including what is
deliberately *not* verified.
