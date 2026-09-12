# python-scala-collections held-out instance: RecordBatch (derived task)

Status: **Derived instance, explicitly modified from the original SkillsBench task, published per the research plan's Section 8 requirement ("If tasks are modified, publish them as derived instances").**

## Why this is a derived task, not a drop-in new instance

The original `python-scala-translation` task's verifier (`verifier/test_outputs.py`) grades against a **fixed** `TokenizerSpec.scala` whose assertions are tied to the exact behavior of the original `Tokenizer.py` (e.g. a specific `WhitespaceTokenizer` call is asserted to return `["hell", "worl"]`, a specific datetime is asserted to format as `"2024-01-15"`). A genuinely different Python source cannot be graded by that fixed spec without either producing identical behavior under different names (not a real held-out instance) or breaking the fixed assertions. This is the same structural issue flagged for `dialogue-graph`'s fixed narrative IDs in the source audit, but more severe here since the assertions are behavior-specific, not just structural.

Consequently, this held-out instance uses a **new Python source** (`RecordBatch.py`, a record-grouping/aggregation module distinct from the original tokenizer), a **new hand-derived-by-execution Scala reference translation** (`RecordBatch.scala`), and a **new ScalaTest spec** (`RecordBatchSpec.scala`) authored specifically for this module — not the original `TokenizerSpec.scala`. The oracle outcome measure is simplified to direct `sbt test` pass/fail, rather than reproducing the original verifier's compound quality-score-plus-tests scoring, since the quality-score component (readability/convention/paradigm checks) is a separate, disclosed non-outcome measure in the original candidate anyway (Section 11.1 of the qualification log already establishes `reward.txt`, not the quality score, is the only field that matters).

## Task statement (for whoever authors an L/G repair or runs an agent against this instance)

`RecordBatch.py` is a Python module for grouping, deduplicating, and aggregating sale records. Translate it into idiomatic Scala 2.13, preserving behavior exactly, saving the translation as `RecordBatch.scala` in package `recordbatch`. Required components: `Record` (case class with fields `id`, `category`, `amount`, `tags`), `dedupeById`, `groupByCategory`, `categoryTotals`, `topCategories`, `findById`, `overallTotal`, `recordsWithTag`. The translation must compile under Scala 2.13.12 and pass all cases in `RecordBatchSpec.scala`.

## Ground truth provenance

Expected values in `RecordBatchSpec.scala` were derived by **actually executing** `RecordBatch.py` against the exact fixture used in the spec (not hand-computed), on 2026-09-13 — see the qualification log for the raw Python interpreter output this was transcribed from.

## Files

- `environment/RecordBatch.py` — the Python source (the task input).
- `environment/RecordBatch.scala` — the reference/oracle Scala translation (used to validate the spec accepts a correct submission).
- `localtest/` — a runnable sbt project: `build.sbt`, `project/build.properties`, `src/main/scala/recordbatch/RecordBatch.scala` (the reference solution, for the passing-case check), `src/test/scala/recordbatch/RecordBatchSpec.scala` (the new spec).

## Single-reviewer caveat

Same as the other 4 held-out instances (Section 3 of the pilot manifest): this was constructed and validated by a single agent in one pass, with actual `sbt test` execution confirming pass on the correct solution and fail on a deliberately corrupted one (see the qualification log). It has **not** received the plan's required second-person review.
