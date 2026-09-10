# Case Record: {{short case id, e.g. langgraph-checkpointer-01}}

Researcher: {{name}}
Framework: {{...}}
Sample type: {{historical issue/fix | outcome-blind official workflow}}
Date: {{...}}

## 1. Provenance

- Source: {{issue/PR link, or "outcome-blind sample #N"}}
- If historical: defective revision pin / corrected revision pin: {{...}}
- If outcome-blind: selection rule applied (do not select based on expected outcome): {{...}}

## 2. Property contract (freeze before running)

- Property family (from research plan §2.2 table): {{request context | approval behavior | state
  continuity | error propagation | streaming behavior | observability metadata}}
- Documented or independently justified contract: {{what the application is contractually supposed
  to do — cite the doc or justify}}
- Evidence to inspect: {{e.g., synthetic identity marker + tool-side record}}
- Oracle (how pass/fail is decided, defined before running): {{...}}

## 3. Configuration pairing

- Application code: {{identical across conditions? confirm}}
- Framework/dependency versions: {{pinned, identical}}
- Initial state: {{identical, isolated}}
- Caller identity/permissions: {{equivalent}}
- Tool fixtures: {{deterministic double / live}}
- Model configuration: {{deterministic double / live, and which model if live}}

## 4. Embedded execution

- Command/harness: {{...}}
- Result: {{pass/fail + raw evidence excerpt}}

## 5. Served execution

- Serving mode (name precisely): {{...}}
- Command/harness: {{...}}
- Result: {{pass/fail + raw evidence excerpt}}
- State reset confirmed before this run: {{yes/no}}

## 6. Outcome classification (plan §9.5)

- [ ] Embedded pass / served pass
- [ ] Embedded pass / served fail
- [ ] Embedded fail / served pass
- [ ] Embedded fail / served fail
- [ ] Unsupported / setup-blocked / oracle-indeterminate — reason: {{...}}

## 7. Causal note (only if embedded/served diverge)

- Divergence localized to: {{reconstruction | context handling | dispatch | state integration |
  output conversion | other}}
- Supporting evidence: {{...}}

## 8. Adjudication (filled by a second researcher, not the case author)

- Adjudicator: {{name, must differ from Researcher above}}
- Cause classification: {{confirmed implementation defect | intended difference | configuration
  mistake | model-dependent variation | unresolved}}
- Adjudicator notes: {{...}}

## 9. Test-configuration comparison (if this case is part of the Hours 36-60 sample)

| Configuration | Detected this outcome? | Notes |
|---|---|---|
| Local baseline | {{yes/no/n.a.}} | {{...}} |
| Boundary-focused tests | {{yes/no/n.a.}} | {{...}} |
| Fuller E2E reference | {{yes/no/n.a.}} | {{...}} |
