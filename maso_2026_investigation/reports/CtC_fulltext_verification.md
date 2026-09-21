# Containing the Cascade — Full-Text Verification (resolves FINAL_RECOMMENDATION §10 gap a)

**Paper:** Divi, Gullapalli, Brahmandam, "Containing the Cascade: A Benchmark and Reference Mediator for Failure Propagation in Tool-Using LLM Multi-Agent Systems," ICERA 2026, pp. 604–609, DOI 10.1109/ICERA72709.2026.11666599.
**Source:** full PDF via IEEE Xplore institutional access, 21 Sep 2026. Prior wave-1/2 assessments were based on abstract + Crossref + Zenodo tombstone only; this note supersedes them where they differ.

## The three gating questions

**1. Does it contain a boundary typology (role/authority/memory/accountability/human)? NO.**
What it has instead is a *fault-mode* taxonomy (Table I) organized by "contract coverage" (structural detectability): SCHEMA_VIOLATION (0.95), STALE_STATE (0.80), TOOL_ERROR_MISHANDLED (0.78), INFINITE_DEFERRAL (0.55), ROLE_DRIFT (0.30), HALLUCINATED_FACT (0.22). Two modes touch organizational concepts (STALE_STATE ≈ shared-state/memory; ROLE_DRIFT ≈ role), but propagation is never *measured across typed boundaries* — their blast radius (BR) is "the fraction (or count) of agents that processed a corrupted message." Agent-count only; no boundary typing; no authority/delegation/accountability/human constructs anywhere in the paper.

**2. Does it vary organizational structure? NO — it varies communication topology.**
Four topologies (Pipeline, Star, Hierarchical, Mesh) × size K ∈ {3,5,8,12} × 3 competence regimes (p_e = 0.075/0.155/0.275). "Hierarchical" is tree delegation in the routing sense only — no decision rights, no authority asymmetries beyond topology, no scarcity condition, no approval/human boundary. Our org-structure-as-IV (decision rights, scarcity, sentinel authority, priced human escalation) is untouched.

**3. Real-LLM execution? NO — confirmed simulation-only, by design.**
Discrete-event testbed; per-hop origination/propagation/absorption sampled from probabilities; p_e calibrated so unguarded success lands in the 40–60% band from MAST/τ-bench. §IX: "Instantiating CASCADE-BENCH's scenario suite on AutoGen and MetaGPT with real fault injectors is the primary line of future work." Zero LLM calls.

## What is CLOSER to us than the abstract suggested (must differentiate head-on)

- **The fail-safe/fail-operational ablation (Table V)** is the paper's best result and overlaps our planned mechanism analysis: removing the circuit breaker collapses containment (99.5→51.1%) while preserving success; removing checkpoint rollback preserves containment but collapses success (83.3→2.6%). "Safety and liveness are governed by different mechanisms" is their stated central finding. Our containment-vs-utility framing must cite this as the simulation-only antecedent and show whether it holds on real LLM executions.
- **Five-condition comparison** (No Guard / Retry / Verifier / Debate / SENTINEL) is a mechanism bake-off in miniature — but no quarantine/re-delegation, no revocation, no human arm, no cost vector (overhead in steps only), no priced trade-off.
- **Table VI (per-fault containment)** pre-figures our H4: semantic faults (hallucinated fact, role drift) are "hardest" — but this is *by construction* (coverage parameters are set, not measured). H4's real-LLM measurement of syntactic-vs-semantic detection quality is the empirical test of their assumption. This is a clean differentiation sentence: "CtC assigns semantic-fault detectability; we measure it."
- **Metric names taken:** containment rate, cascade depth, blast radius, MTTD — all confirmed in Table II. Our OBR must be defined against their BR explicitly (theirs: agent fraction; ours: typed boundary crossings on an arm-invariant inventory).

## Other notable facts

- Venue is low-tier (5th ICERA — "Electronics Representation and Algorithm"); authors are independent researchers; refs [32]–[33] are self-citations to the same group's IJEDR/ICAISET papers (the ICAISET one is the "OpsAgent" paper flagged by the W2 cand-1 assassin — same group, confirming they are actively working this lane).
- 590k simulated executions; 30 seeds × 60 Monte-Carlo instances per cell; 95% CIs reported (contrary to our wave-3 R2 note that they report no CIs — they do report CIs across seeds; still no power analysis or multiplicity control).
- Artifact: claimed open release; Zenodo tombstone (deleted 2026-07-22, "copyright") confirmed by wave-1 — the "open baseline" is currently not obtainable, which weakens their reproducibility claim and is worth a careful sentence in related work.

## Impact on OrgResilience framing

**No framing change required.** The three properties our novelty sentence rests on are all confirmed absent: typed organizational boundaries, organizational structure as IV, real LLM execution. Adjustments to make in the paper draft:

1. Cite CtC as the nearest neighbor with the metric vocabulary; differentiate on all three axes + cost vector + human arm + classical transfer.
2. Treat their fail-safe/fail-operational ablation as a *prediction to test on real LLMs* (does the breaker/rollback division of labor survive stochastic semantic reasoners?) — a cheap additional pre-registered hypothesis (H5) that converts a threat into a replication target.
3. Use "CtC assigns detectability; we measure it" for H4 positioning.
4. One explicit terminology paragraph disambiguating OBR from their BR (and from DamageFlow's BRS and Bounded Agents' monotonicity).
5. Note their stated future work (live-LLM instantiation on AutoGen/MetaGPT) as confirmed scoop-risk evidence — strengthens the case for early pre-registration.
