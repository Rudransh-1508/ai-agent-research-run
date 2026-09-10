# Pilot Go/No-Go Decision

Filled jointly by A, B, and C at Hours 60-72. Source: research plan §11.1 (substantive pilot pass
requirements) and §11.2 (stop or reassess triggers). Answer every line honestly — this document
exists to prevent motivated reasoning under deadline pressure, not to produce a "yes."

Date: {{...}}
Participants: {{A, B, C}}

## 1. Substantive pilot pass checklist (plan §11.1) — ALL must be true

- [ ] Relevant serving access confirmed in at least 2 frameworks. (Reference access logs.)
- [ ] At least 2 consequential, faithfully reproduced mode-dependent differences exist across at
  least 2 frameworks (may include clearly labelled historical cases). List them: {{case ids}}
- [ ] More than one root-cause mechanism is represented, with substantive evidence beyond
  already-studied persistence/resume behavior. List mechanisms found: {{...}}
- [ ] Contracts are valid and trivial version/configuration/oracle errors have been credibly
  excluded for each causal case.
- [ ] A concrete incremental testing decision exists (not merely "a network endpoint can be
  tested"). State it: {{...}}
- [ ] A feasible path to held-out evaluation exists within the remaining schedule.

## 2. Stop-or-reassess triggers (plan §11.2) — NONE should be true

- [ ] Access required waiting on external approvals or inaccessible managed services for 2+
  frameworks.
- [ ] All apparent failures disappeared under correct supported configuration.
- [ ] All results concern previously-studied persistence semantics with no new test-transfer
  insight.
- [ ] Existing upstream tests already cover the entire phenomenon found, with no useful comparison
  left to make.
- [ ] The only evidence is a few selected old bugs plus generic integration-testing advice.
- [ ] Any comparison required bypassing official wiring, incompatible model replay, or silently
  changing the application contract.
- [ ] Too few independent workflows remain to support the intended testing recommendation.

If any box in this section is checked, explain why below and whether it invalidates the pilot:

{{...}}

## 3. Prior-art recheck

Does anything found change an engineering decision that the closest prior work (plan §5) does not
already answer? {{yes/no + justification}}

Any newly discovered paper that changes this assessment? {{...}}

## 4. Accounting summary (pull from outcome_tracker.csv)

- Attempted cases: {{n}}
- Eligible: {{n}}
- Excluded (with reasons on file): {{n}}
- Interpretable: {{n}}
- Frameworks contributing substantive evidence: {{n and names}}

## 5. Decision

- [ ] **GO** — proceed to main-study planning (plan §12).
- [ ] **NO-GO** — stop this cross-framework pilot. Escalate to MCP-study fallback feasibility gate
  (plan §18), outside this folder's scope.
- [ ] **BOUNDED** — pilot found a narrow but solid result; consider scoping to a short paper rather
  than the full main study (plan §13.3).

## 6. Signatures

- A: {{name, date}}
- B: {{name, date}}
- C: {{name, date}}
