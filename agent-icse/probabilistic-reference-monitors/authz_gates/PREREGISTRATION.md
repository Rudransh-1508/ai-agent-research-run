# Pre-registration: Probabilistic Reference Monitors study

Date: 2026-09-21. Written BEFORE corpus extraction and BEFORE any benchmark measurement.
Paper target: SE4AgenticAI 2026 (deadline 2026-10-10 AoE).

## Prior knowledge disclosure

A literature-sweep subagent read 16 gate repos on 2026-09-21 as part of gap verification
(documented in `../PROBABILISTIC_REFERENCE_MONITORS_LIT_REVIEW_2026-09-21.md` Section 3.2).
Those 16 are treated as a **pilot set**; predictions P1-P4 are registered for the **full
corpus** and will additionally be reported for the **held-out remainder** (gates not in the
pilot set) separately. Benchmark predictions P5-P8 concern measurements nobody has made.

## Inclusion criteria (corpus)

A project counts as a gate iff: (a) it calls a typed decision model (Jev or a replica) to
decide whether an agent action proceeds (allow/ask/deny, block, hold, escalate, or stop);
(b) it is runnable code, not a README-only scaffold; (c) it was public before 2026-10-01;
(d) it is listed in yibie/awesome-jev or reachable from a listed project. Commit SHAs are
pinned at clone time and recorded with access dates.

## Extraction fields (per gate)

question(s) asked; primitive(s) used (Choice/Score/Noul); threshold constant(s); threshold
provenance (documented-derivation / swept-on-data / copied-from-vendor-docs / undocumented);
action set; whether attacker-reachable text is passed unsanitised; error path on timeout,
HTTP 429, HTTP 5xx, malformed response; fail classification (fail-open / fail-closed /
partial / undocumented); evidence as file:line quotes.

## Registered predictions

- **P1 (fail-open).** >= 50% of gates with a determinable error path fail open on at least
  one of timeout / 429 / 5xx / malformed response.
- **P2 (threshold provenance).** >= 60% of threshold constants have no documented derivation
  (undocumented or copied from vendor docs).
- **P3 (vendor constants).** >= 1 gate ships the vendor docs' illustrative threshold
  (0.9 or 0.5) verbatim.
- **P4 (no cross-evaluation).** No gate cites a published evaluation against another gate
  or against a public benchmark with baselines.
- **P5 (ambiguity gap).** On the benchmark, accuracy on ambiguous items is >= 15 points
  below accuracy on clear items. (Prior: themsquared 100% clear vs 71.4% ambiguous, n=60.)
- **P6 (vendor threshold suboptimal).** Under asymmetric loss with C(false allow) >= 10 x
  C(false deny), the vendor docs' illustrative 0.9 threshold is not loss-optimal; the
  Chow-optimal threshold differs by >= 0.1.
- **P7 (confidence blindness).** Mean confidence on successful-injection items is not
  significantly lower than on matched clean items (prior: priorbench observed ~0.97
  confidence on pure noise).
- **P8 (baselines).** No directional prediction: where a calibrated typed gate lands
  against TraceSafe's 13 LLM + 7 guardrail baselines is exploratory.

## Analysis plan (fixed in advance)

- Fail-open classification rubric: a gate fails open on failure mode F iff the action
  proceeds (or is treated as allowed) when F occurs; fail-closed iff the action is
  denied/held/escalated; partial iff behaviour differs across failure modes. Undocumented
  paths are classified by reading the code; unclassifiable gates are reported as such,
  not dropped.
- Asymmetric loss model: C(false allow on destructive action) = L, C(false deny) = 1,
  C(ask/escalate) = c in (0,1). Report the loss-optimal operating point via Chow's rule
  instantiated for three actions, sweeping L in {5, 10, 25, 100} and c in {0.05, 0.2, 0.5}.
- Selective-risk curves: risk vs coverage per gate; report AURC; bootstrap CIs (10k
  resamples); Holm correction across gates and predictions.
- All raw calls logged as JSONL with model id, gateway, timestamp; recount script shipped.
