# S4-ATTACK-D4 — Adversarial attack on Direction D4: Containment-target × fault-medium mismatch

**Date:** 2026-09-21
**Mission:** Kill or wound D4: "Quarantine-the-agent vs rollback-the-memory vs restore-the-state: containment target has never been crossed against fault propagation medium (messages vs shared memory vs environment state) for organic faults. Prediction: agent-targeted containment fails for memory/state-borne faults; memory-targeted containment fails for message-borne faults."
**Stance:** Hostile. Reports read in full: audit2 A3, A9, A10, A11 (N3), A8 (relevant sections); reports B6, E2, B4 (relevant sections), D3 (MemClaw section), E5 (memory-boundary section), FINAL_RECOMMENDATION. Independent re-verification performed this session (see §7).

---

## 0. VERDICT

**SURVIVES WITH NARROWING** — and the narrowing is severe. As a *standalone paper* D4 is **WEAK** (one experiment, prediction half-obvious and half-falsified-as-stated, headline cell already occupied adversarially). It survives only as a merged arm of the main OrgResilience paper with a **repaired prediction**: the causal variable is the fault's *current reservoir set*, not its *origin medium*.

D4 is **not COLLIDED**: the controlled medium × containment-target crossing for *organic* faults is verifiably empty (two prior waves + my own fresh searches this session, §7). But "empty" is doing less work than D4 assumes, because every *cell* of the crossing is occupied or pre-empted, and the crossing's clean prediction is contradicted by verified evidence in one direction.

---

## 1. QUESTION (a): Does the memory-repair preprint (10.20944/preprints202602.1188.v1) already cross containment-target × medium?

**No — but it occupies D4's headline cell with D4's predicted sign and a strong number.** Re-verified the Crossref abstract myself this session (**ABSTRACT VERIFIED**, full text bot-blocked, not S2-indexed):

- Liu, Xu, Ma, Xu, Qiu, "Memory Poisoning Propagation and Repair Mechanism in Multi-Agent Collaborative Environments," preprints.org, 2026-02-14. Evidence graph over memory source credibility + content consistency; contrastive-learning anomaly detection; "upon detecting poisoning, further propagation is suppressed through **isolation, rewriting, and conflict resolution**"; 60 collaborative tasks, ~210k memory records, 12k injected poisoned samples; AUC 0.94; misbehavior 15.6%→2.3%; **cross-agent propagation −78.1%; "minimal impact on overall task efficiency."**

Why it is NOT the crossing: exactly **one fault medium** (memory poisoning) × **one containment target** (the memory substrate — "isolation" here scopes to poisoned memories, not agents, per the abstract's context of validating newly added memories; flag: ABSTRACT ONLY, so the isolation semantics are not fully pinned). No agent-quarantine arm, no message-borne arm, no state arm, no interaction estimate.

Why it is still heavily damaging:
1. It is a *multi-agent collaborative* demonstration that memory-borne faults propagate cross-agent and that **memory-targeted repair contains them with utility preserved** — D4's central "prediction" for the memory cell, already published (Feb 2026) with a number a reviewer will quote against us.
2. It pre-empts the "first to show containment must match the propagation substrate" framing for the most novel medium (shared memory). D4's residual claim reduces to "first *controlled crossing*" — a methodological novelty, not a phenomenon novelty.
3. Caveats that keep D4 alive: adversarial poisoning frame (D4 scopes to organic faults); non-peer-reviewed preprints.org; no organizational semantics; no target *comparison*.

**Classification: PARTIAL COLLISION on the memory cell; the crossing itself unoccupied.**

## 2. QUESTION (b): Is the mismatch prediction obvious or genuinely contested?

**Worse than obvious: it is obvious in one direction and falsified-as-stated in the other.**

**Direction 1 — "agent-targeted containment fails for memory/state-borne faults" — is obvious.** Three independent stacks of evidence make this a confirmation, not a discovery:
- *Classical distributed systems (textbook):* rollback-propagation / domino-effect theory (Agbaria et al. SRDS 2001 / JPDC 2004, DOIs verified by B6 via Crossref) already formalizes that recovery must follow the **state-dependency graph**, not the process boundary. "Quarantining the process does not clean shared state" is a 40-year-old corollary. Chandy–Lamport, k-rollback, recovery lines — all unconnected to LLM MAS, but any systems-literate reviewer knows the principle.
- *Observational LLM-MAS:* Emergence World (2609.17320, **ABSTRACT VERIFIED by me today**): "Detection did not ensure containment… writing it into their own persistent memory, and acting on it up to **46 hours later**." Agent-targeted responses failing against memory-resident faults is already demonstrated at 850k-call scale.
- *Adversarial reservoir literature:* AgentPoison (2407.12784, NeurIPS 2024), MPBench (OpenReview 5cgg9yenCZ, ICML 2026 AIWILD), MINJA (2503.03704) establish memory as a persistent propagation reservoir where prompt-injection defenses fail (all verified by B6/B4; MINJA full-text read). The memory-repair preprint (§1) then shows the matched repair works.

**Direction 2 — "memory-targeted containment fails for message-borne faults" (and, implicitly, agent-targeted containment *works* for message-borne faults) — is falsified as stated by verified evidence.** TIDE (2608.03421, **ABSTRACT VERIFIED by me today**): a single false testimony "persists through honest agents **after the deceiver exits**" — i.e., *agent-targeted containment (source removal) fails for a message-borne fault* once the testimony is adopted and re-transmitted by honest agents. The fault changed medium (message → other agents' beliefs) without any shared-memory substrate. This breaks D4's taxonomy: the causal variable is not the fault's *origin medium* but whether the fault has **replicated into any persistent reservoir** (shared memory, environment state, *or other agents' adopted beliefs*). Corroborated organically by Paglieri et al. 2609.04170 (**ABSTRACT VERIFIED by me today**): a spontaneously emerged evaluation exploit (organic, non-adversarial, zero external intervention) propagated in a 100-agent collective **via a shared knowledge library and later P2P messages** — one fault, two media, with emergent containment (whistleblower auditing, patches). The medium boundary is porous; faults cross it.

**Consequence for D4's design:** the clean 2-arm prediction (match target to origin medium) will produce a confounded result — the message-borne × quarantine cell will *also* fail whenever adoption precedes quarantine, and the paper's own data will refute its stated prediction. The repaired, defensible hypothesis is: **containment effectiveness is governed by the fault's current reservoir set and its replication/adoption count at intervention time** — which converges with A10-H3 (consensus-inertia threshold, containment collapses after k endorsements). A10 already flagged this: T8 is "unreconciled" precisely because source removal is assumed curative while TIDE/Emergence World show otherwise.

**Is anything genuinely contested?** Yes, narrowly: no work *quantifies* the replication threshold at which a message-borne organic fault becomes quarantine-immune, and no work measures the utility cost of reservoir-matched vs mismatched containment under controlled injection. That is a measurement contribution, not a conceptual one — and it is A10-H3/H5 territory, i.e., D4 narrowed is a merge, not a direction.

## 3. QUESTION (c): Big enough for a paper, or one experiment?

**One experiment.** The design is a single crossed factorial: medium {message, shared-memory, environment-state} × containment target {agent-quarantine, memory-rollback, state-restore, none} ≈ 8–12 cells on the existing tau2-bench org-wrapper. That is one table and one interaction plot. Specific size threats:

1. **Already judged thin.** FINAL_RECOMMENDATION scored the memory candidate (#6) "Too thin standalone; one boundary arm in final" — D4 is that arm wearing a direction's clothes. Nothing in this audit overturns that judgment; §1–2 worsen it.
2. **Noise-floor threat.** tau2-bench retail has a measured paired noise floor of ±12–15pp at n=100 (2606.20695, per A8). The mismatch *interaction* must clear ≥25pp binary / d≥0.5 continuous to be confirmatory under W2_statistics. The adversarial memory cell will clear it easily (preprint: −78.1%); the **organic** cells may not, because…
3. **Natural attenuation can zero out the treatment.** Hallucination Cascade net attenuation 0.644 (2606.07937) and TRAJDEBUG's 7.62:1 self-masking mean most organic faults may die unaided in every arm — leaving no propagation to contain and nulls across the crossing. A10's meta-observation (the escape base rate is unmeasured everywhere) is a *direct* viability threat to D4: the crossing is uninterpretable without a no-fault-would-have-spread control, and with it, may show "medium doesn't matter because nothing propagates." A10-H5's own falsifier ("quarantine equally effective for both media") and the null outcome are both live possibilities.
4. **The state column is mechanism-occupied.** State-targeted containment exists and is crowded: Cordon (2606.17573, semantic transactions, shadow state, commit/rollback — ABSTRACT VERIFIED by A8), Atomix (2602.14849), SagaLLM (PVLDB 2025, saga compensation for multi-agent planning — Crossref-verified by A8/A3). All single-agent or planning-only, so no collision on the crossing — but D4 cannot claim novelty for the state-restore *arm*, only for the comparison.

## 4. QUESTION (d): MASO fit?

**Good as a classically framed arm; mediocre as a standalone.** The CFP verbatim lists "Detection and mitigation of cascading, and systemic failures" and organizational memory — native vocabulary. The classical-MAS-heavy reviewer pool gives D4 one genuine asset: the crossing has a natural classical rendering — **sentinel quarantine (Hägg 1997; Dellarocas & Klein ICMAS 2000 — agent-targeted) vs blackboard hygiene (HEARSAY lineage — memory-targeted)** — and E5 verified the memory boundary is the *weakest classical coverage* ("no verified classical MAS work on failure propagation through shared learned memory"), so a transfer framing ("classical sentinels assume the fault dies with the agent; shared organizational memory breaks that assumption") is available and pool-appropriate. But: (i) D4 drops the depth (H1) and scarcity (H3) axes that carry the main paper's classical-transfer spine; (ii) "containment target" is security/systems vocabulary that needs translation for this pool; (iii) Sentinel Agents (2509.14956, FULL TEXT VERIFIED by A11) already re-invented sentinels for LLM MAS *without* the classical lineage — the mechanism name is occupied, only the transfer test is open.

## 5. Assigned-paper usage table (all load-bearing items)

| Paper | Verification | What it does to D4 |
|---|---|---|
| Memory-poisoning repair preprint (10.20944/preprints202602.1188.v1) | **ABSTRACT VERIFIED (me, Crossref, today)** | Occupies the memory×memory cell with D4's predicted sign (−78.1% propagation, utility preserved); NOT a crossing; adversarial |
| MemClaw (2606.24535) | ABSTRACT VERIFIED (D3/B6; ArgusFleet repo 404 flagged) | Memory failure-mode taxonomy (stale propagation, contradiction persistence) stops at governance; no fault injection, no containment comparison — supports gap, must-cite |
| FamilyRepair (OpenReview IJoWb6T3RJ) | OpenReview API record (B6) | Memory-rollback families + replay verification + poison-leakage metric; single-agent, unpublished — reusable machinery, partial occupant of the memory-repair arm |
| TIDE (2608.03421) | **ABSTRACT VERIFIED (me, today)** | **Falsifies D4's clean prediction**: agent-targeted containment (deceiver exit) fails for message-borne faults post-adoption |
| Emergence World (2609.17320) | **ABSTRACT VERIFIED (me, today)** | Makes Direction 1 obvious: detection ≠ containment; memory-resident threats acted on 46h later |
| AgentPoison / MINJA / MPBench | ABSTRACT/FULL (B4/B6) | Memory-as-reservoir established adversarially; defenses fail; no recovery, no crossing — supports gap, undercuts novelty of Direction 1 |
| SagaLLM (2503.11951, PVLDB 2025) | Crossref-verified (A3/A8) | State-targeted containment (compensation) for multi-agent planning — occupies the state arm mechanism-wise |
| Cordon (2606.17573) | ABSTRACT VERIFIED (A8) | State-targeted transactional containment, single-agent — occupies the state arm mechanism-wise |
| Paglieri et al. 2609.04170 (not in my assignment; found via B12) | **ABSTRACT VERIFIED (me, today)** | Organic fault crossing media (shared library → P2P) in 100-agent collective — evidence the medium taxonomy is porous |

## 6. What precisely survives

1. **The controlled crossing for organic faults is verifiably empty** — no work injects organic faults of controlled medium and crosses containment target against it with utility measurement. (Verified negative: A10, B6, E2, plus my fresh DataCite/OpenReview searches today, §7.)
2. **As a merged arm of OrgResilience**, reframed: "containment must match the fault's *reservoir set*; reservoirs include shared memory, committed state, and adopted peer beliefs; effectiveness collapses once replication count crosses a threshold" — merging A10-H5 with A10-H3's endorsement dial. This is feasible in the existing substrate (memory-write fault is already in the main matrix's 5-fault list; sentinel-quarantine and checkpoint-rollback arms already exist).
3. **Mandatory design repairs:** (i) state the prediction in reservoir terms, not origin-medium terms, or TIDE refutes it in-review; (ii) include a natural-attenuation control (uncontained no-mechanism arm with escape base rate) or the crossing is uninterpretable; (iii) power the interaction above the ±12–15pp tau2 noise floor; (iv) cite-and-differentiate the memory-repair preprint, TIDE, Emergence World, 2609.04170, MemClaw, FamilyRepair, Cordon/SagaLLM.
4. **Do not run D4 as a standalone paper.** Standalone it is one confounded experiment with an obviousness problem and a falsified-as-stated prediction.

## 7. Independent verification & search log (this session)

- Crossref API: full abstract of 10.20944/preprints202602.1188.v1 retrieved and parsed (title/authors/date/abstract incl. all numbers quoted above). **ABSTRACT VERIFIED.**
- arXiv abs pages fetched today: 2609.17320 (Emergence World), 2608.03421 (TIDE v3), 2609.04170 (Paglieri et al.). **ABSTRACT VERIFIED** for all three.
- Fresh collision searches: DataCite full-text query "quarantine rollback agent memory" (top hits: irrelevant Zenodo framework slop); OpenReview notes search "containment memory rollback quarantine" (top hits: FamilyRepair + unrelated; no crossing paper). Negative result consistent with A10/B6 — flagged as weak-to-moderate evidence (recall limited by channel throttling documented in A3/A9: S2 429, arXiv API empty, OpenAlex budget exhausted).
- Not re-verified (relied on prior-wave levels, marked): AgentPoison/MINJA/MPBench (B4/B6), MemClaw (D3), FamilyRepair (B6), Cordon/SagaLLM (A8), Agbaria et al. DOIs (B6 via Crossref).
