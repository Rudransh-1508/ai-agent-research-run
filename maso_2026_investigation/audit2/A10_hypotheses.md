# A10 — HYPOTHESIS GENERATOR: Alternative Hypotheses from Verified Contradictions

**Investigator:** Agent 10 (audit wave 2)
**Date:** 21 September 2026
**Mission:** Do NOT defend H1/H2/H3. Mine the verified literature for contradictions, untested interactions, and threshold effects; generate ≥10 causal, falsifiable, cheap-to-test (~19 days, tau2-bench substrate) alternative hypotheses, preferring the form "Mechanism X improves outcome Y when Z is high but reverses when Z falls below threshold T."

**Reports read in full:** B4 (cascading failures), B10 (organizational MAS), B12 (heterogeneity), B14 (self-healing), E5 (classical MAS assassin), CtC_fulltext_verification, W2_statistics, FINAL_RECOMMENDATION; B8 (human escalation) and B16 (cost/reliability) read selectively for collision checks.

**Independent verification performed today (not delegated to prior waves):**
- arXiv:2606.07937 (Hallucination Cascade) — abs page fetched: attenuation confirmed verbatim (0.422→0.272, amplification factor 0.644; factual accuracy 0.789→0.769). **ABSTRACT VERIFIED.**
- arXiv:2609.04373 (Why Better Models Can Create Riskier Systems) — abs page fetched: capability→correlation→non-diversifiable risk floor confirmed; v1 posted **3 Sep 2026**. **ABSTRACT VERIFIED.**
- arXiv:2603.03116 (PAE, corrupt success) — abs page fetched: 27–78% corrupt successes on τ-bench confirmed; v1 posted 3 Mar 2026. **ABSTRACT VERIFIED.**
- arXiv:2609.14767 (Loop-Back Authority) — abs page fetched: flat > hierarchical (Utility d=0.42, p=0.009); "supervisor pays for itself when it can verify and becomes a liability when it can only opine" confirmed verbatim; v1 posted **13 Sep 2026**. **ABSTRACT VERIFIED.**
- arXiv:2606.19111 (Leadership as Coordination Control) — abs page fetched: "recovery-advantage boundary" confirmed (controller helps only where round-0 majority unreliable ∧ task recoverable ∧ undirected interaction doesn't already repair). **ABSTRACT VERIFIED.**
- Dellarocas & Klein ICMAS 2000 and CtC ICERA 2026 relied on at **FULL TEXT VERIFIED** level via E5 and CtC_fulltext_verification (both read primary PDFs; I read their dissections, not the PDFs — treated as FULL TEXT VERIFIED by proxy).
- Fresh collision searches: Semantic Scholar API 429-blocked; arXiv export API returned empty; OpenReview full-text search returned no relevant hits for "quarantine/rollback containment" and "verifier failure monitor" beyond items already in prior reports. Absence-of-hit claims below are therefore **weak evidence**, flagged as such.

---

## 1. The verified tension map (ground truth for the hypotheses)

| # | Tension | Side A (verified) | Side B (verified) | Status |
|---|---|---|---|---|
| T1 | Effect of chain/delegation **depth** on fault spread | Amplifies: D&K unzippering 600–700% inflation at depth 4 (FULL TEXT); CtC unguarded cascade depth ~doubles with scale (FULL TEXT) | Attenuates: Hallucination Cascade factor 0.644 over 3-agent chains (ABSTRACT) | **Unreconciled.** Nobody has varied fault *class* to explain the sign |
| T2 | **Hierarchy** vs flat under faults | Hierarchy most resilient: 5.5% vs 23.7% drop (2408.00989, ABSTRACT via 4 prior reports) | Flat beats hierarchy on utility; supervisor a liability when it can only opine (2609.14767, ABSTRACT today) | Partially reconciled by Loop-Back's own boundary condition — but never tested **under injected faults** |
| T3 | **Verification gates** | Help: boundary gates cut survival 58.4%→16.2% (Hallucination Snowball 2608.14588); CHARM 82.1% vs 18.5% (both ABSTRACT via B4) | Corrupt successes pass outcome checks: 27–78% (PAE, ABSTRACT today); amplification main effect n.s. after controls, p=0.658 (Kim et al. 2512.08296, via B10) | **Unreconciled** at the mechanism level: *which* faults survive *which* gates |
| T4 | **Capability/heterogeneity** | Heterogeneity "universal antidote" (2502.08788, via B12) | Capability ↑ → correlation ↑ → non-diversifiable risk floor (2609.04373, ABSTRACT today); diversity saturates <10 agents (2607.09197, via B12) | **Unreconciled:** no experiment crosses model mix with *containment* design |
| T5 | **Containment** net effect | Helps: CtC containment 46.2→99.4% (FULL TEXT) | Strands: CtC no-rollback ablation success 83.3→2.6% (FULL TEXT); backfires under scarcity (D&K, FULL TEXT) | CtC's own ablation proves mechanism-ranking fragility — in simulation only |
| T6 | **Cross-agent correction** | Challenger/Inspector recover ≤96.4% (2408.00989) | Correction is a role-labeling artifact, +23–93pp when relabeled external (Self-Correction Illusion 2606.05976, via B12) | **Unreconciled:** is "independent verification" independence or framing? |
| T7 | **Natural containment** | One atomic seed → widespread failure (From Spark to Fire 2603.04474, via B4) | 7.62 local errors per failed trajectory, only 1 critical (TRAJDEBUG 2608.06346, via B14); net attenuation (T1-B) | **Unreconciled and consequential:** the escape base rate is unmeasured everywhere |
| T8 | **Source removal** | Quarantine/isolation assumed curative (CtC, Isolation 2607.12406) | False testimony persists after deceiver exits (TIDE 2608.03421); threats in persistent memory acted on 46h later (Emergence World 2609.17320, 15 Sep 2026) | **Unreconciled:** containment-target × fault-medium interaction untested |
| T9 | **Escalation** | Human top tier improves triage 40→60% (TAO, via B10) | Inverted-U: more oversight can reduce safety (Oversight Has a Capacity 2606.08919, via B8); corrigibility not compositional (Multi-Agent Off-Switch, via B8) | Escalation studied as *gating*, never as post-fault containment with a velocity race |
| T10 | **Recovery across boundaries** | Retry/replan/targeted compared under matched budgets (2606.01416, via B14) | Handoff across model switch recovers <50% of quality gap (Handoff Tax 2608.24358, via B14); each revision loop −0.14 clarity (2609.14767) | Boundary-crossing recovery loss never measured organizationally |

---

## 2. The hypotheses (12)

All are designed for the existing substrate: tau2-bench retail org-wrapper (LangGraph), deterministic DB-state ground truth, injected faults with known ground truth, ~40 instances × paired arms, per W2_statistics power constraints (continuous co-primary endpoint; only ≥25pp binary / d≥0.5 continuous / crossover interactions are confirmatory).

### A10-H1 — Verification theater: the endorsement-laundering reversal
**Statement:** An independent verifier gate reduces organizational blast radius when verifier accuracy on the injected fault class exceeds threshold T, but *increases* blast radius below T, because a passed gate launders the corrupt artifact with authority and raises downstream adoption. BR(weak verifier) > BR(no verifier) > BR(strong verifier) — non-monotone.
**Resolves:** T2 × T3 × T6 (Loop-Back's "verify vs opine" + PAE's corrupt successes + Self-Correction Illusion's framing artifact).
**IVs:** verifier accuracy dial (oracle/noise mixture, CAND-3 style: a ∈ {0,.2,.4,.6,.8,1}) × endorsement framing (verdict attached as authoritative stamp vs silent flag). **DVs:** continuous OBR count; downstream adoption rate of the faulty artifact (provenance graph); corrupt-success rate (PAE-style gated). **Moderators:** fault subtlety (syntactic vs semantic); depth of remaining chain after the gate.
**Mechanism:** downstream agents condition trust on the gate's verdict; a false-pass raises consumption probability above the no-gate baseline. **Competing explanation:** weak verifiers merely fail to *subtract*; the excess over no-verifier baseline is the discriminating observation. **Falsifier:** BR monotone non-increasing in a under both framings. **Null publishable:** yes — "verification never backfires at any accuracy" would kill the theater concern and strengthen gate-everywhere prescriptions; either sign resolves T3.
**Collision status:** OPEN for fault propagation. PARTIALLY OCCUPIED at the output-quality level by Loop-Back (its boundary condition is exactly verify-vs-opine, but no faults, no propagation) — must cite as the quality-level antecedent.

### A10-H2 — Depth sign is fault-class-dependent: refinement attenuates, commitment amplifies
**Statement:** Chain depth attenuates *content* faults (hallucinated facts — re-generation washes them out, per 2606.07937) but amplifies *commitment* faults (wrong tool arguments, policy-violating actions — committed state cannot be washed out, per D&K/PAE/SABER). The depth-effect sign flips at the fault's "committedness" threshold.
**Resolves:** T1 head-on — the field's loudest contradiction.
**IVs:** depth {1,2,4} × fault class {semantic-content, procedural-commitment} (crossed, same injection sites). **DVs:** per-stage escape probability (Snowball-style Markov transitions); committed-effect count (DB-state diff); amplification factor per class. **Moderators:** whether intermediate agents transform vs relay; tool reversibility flag.
**Mechanism:** stochastic re-generation is a low-pass filter on content; state commitment is a write-once channel. **Competing explanation:** detection difficulty confound — commitment faults may simply be harder to detect; control by holding oracle-detector rate equal across classes in one arm. **Falsifier:** same sign and similar magnitude for both classes. **Null publishable:** yes — "depth is irrelevant to both classes" falsifies both D&K-transfer and Hallucination Cascade in one shot.
**Collision status:** OPEN. Both poles verified; the reconciling experiment exists nowhere.

### A10-H3 — Consensus inertia: containment collapses after k endorsements
**Statement:** A sentinel/verifier intervention succeeds at rate r when the fault has been endorsed by <k agents, and collapses toward 0 once pre-intervention endorsements cross k≈2–3, *independent of sentinel accuracy* — social proof overrides correction.
**Resolves:** T8-adjacent; ties From Spark to Fire's "consensus inertia" class + pluralistic ignorance (2608.02758: single dissenter breaks consensus <26%) + TIDE (observers suppress but don't recover).
**IVs:** controlled pre-containment endorsement count (inject fault, let it propagate exactly j ∈ {0,1,2,3} hops via scripted timing) × sentinel accuracy {oracle, learned}. **DVs:** containment success; post-intervention re-adoption of the fault; correction persistence. **Moderators:** hierarchy (does a supervisor's endorsement count double?); endorsement visibility.
**Mechanism:** LLM agents weight concordant peer context over a lone corrective signal (conformity). **Competing explanation:** longer propagation = more state committed = mechanically harder recovery; control with a memory-fault arm where nothing is committed at intervention time. **Falsifier:** containment flat in j. **Null publishable:** yes — "sentinels are immune to consensus inertia" would be a reassuring, cited-null result.
**Collision status:** OPEN. Consensus inertia is named as a vulnerability class but never parameterized as a containment threshold.

### A10-H4 — Rollback's healthy-work collateral: the checkpoint-spacing × detection-latency race
**Statement:** Checkpoint-rollback preserves utility when detection latency < checkpoint spacing, but destroys it when detection latency exceeds spacing — because rollback discards healthy committed work along with the fault (the CtC 83.3→2.6% stranding). Optimal checkpoint frequency *decreases* with fault subtlety (subtle faults have long MTTD → wider spacing), inverting the naive "checkpoint more" prescription.
**Resolves:** T5's CtC ablation paradox; imports classical domino-effect theory (Elnozahy 2002, via B14).
**IVs:** checkpoint spacing {every step, every 3, every 5, episode-only} × fault subtlety {syntactic, semantic}. **DVs:** utility preservation; healthy-steps-discarded count (deterministic from logs); cost vector. **Moderators:** irreversibility regime; depth.
**Mechanism:** rollback granularity vs detection delay race. **Competing explanation:** stranding is caused by lost external side-effects, not discarded work — the irreversibility flag separates them. **Falsifier:** utility monotone in spacing for both subtlety classes. **Null publishable:** moderate.
**Collision status:** PARTIALLY OCCUPIED — Nonuniformity Principle (2607.16530) owns oversight-checkpoint placement under time constraints (human oversight, no faults); Young 1974/Daly 2006 own optimal checkpoint intervals classically. The LLM-specific residue (semantic MTTD is stochastic and long; collateral is *healthy LLM work*) is open but the framing must cite both.

### A10-H5 — Memory residue: quarantine fails when the fault lives in shared memory
**Statement:** Agent-quarantine contains message-borne faults but fails for memory-borne faults: once the fault is written to shared organizational memory, removing the source agent leaves propagation statistically unchanged; only memory-targeted rollback/redaction contains it. Containment effectiveness is determined by *match between mechanism target and fault medium*, not mechanism strength.
**Resolves:** T8; exploits E5's finding that the memory boundary is the classical literature's weakest coverage.
**IVs:** fault medium {message-only, shared-memory write} × containment {agent quarantine, memory rollback, both, none}. **DVs:** post-containment propagation count; time-to-reinfection (fault re-enters from memory after containment declared); utility. **Moderators:** memory read rate; number of memory subscribers.
**Mechanism:** memory is a persistent reservoir (AgentPoison/MPBench show this adversarially; TIDE/Emergence World show persistence observationally) — the *organic-fault* version is untested. **Competing explanation:** reinfection is just delayed detection of pre-quarantine spread; timestamped provenance separates the two. **Falsifier:** quarantine equally effective for both media. **Null publishable:** yes — "medium doesn't matter" would validate target-agnostic containment design.
**Collision status:** OPEN — my strongest surviving gap. All adjacent evidence is adversarial (AgentPoison, MPBench) or observational (TIDE, Emergence World); no controlled medium×mechanism crossing exists for non-adversarial faults.

### A10-H6 — The correlation floor caps verifier redundancy
**Statement:** Adding verifier agents reduces residual escape rate while team correlation ρ < ρ*, but escape plateaus above ρ* regardless of verifier count — the correlation floor (2609.04373) makes N-version verification non-diversifiable. Heterogeneous verifier panels break the plateau; homogeneous ones don't.
**Resolves:** T4; imports Littlewood–Strigini diversity limits (classical, via B12).
**IVs:** verifier count {0,1,2,4} × panel composition {same-model, mixed-family} × injected-fault class. **DVs:** residual escape rate; marginal escape reduction per added verifier; cost. **Moderators:** base model capability (does ρ* move with capability, per 2609.04373's capability-correlation link?).
**Mechanism:** shared training → shared blind spots → correlated false-passes. **Competing explanation:** plateau is a budget/attention artifact; cost-matched arms control it. **Falsifier:** escape keeps declining with verifier count for same-model panels. **Null publishable:** yes — "correlation floor not binding at n≤4 verifiers" scopes 2609.04373's threat.
**Collision status:** OPEN for containment. 2609.04373 is finance-market ABM; Huot's robustness collapse is routing; nobody crosses correlation with verification redundancy.

### A10-H7 — Recovery-path asymmetry: escalation re-delegation is lossier than peer rerouting
**Statement:** After containment, recovery through a peer reroute preserves more utility than recovery through escalate-and-redelegate across an authority boundary, even when the recovering agent is identical — the boundary crossing itself destroys context (Handoff Tax <50%; Loop-Back's −0.14 clarity per loop). The loss grows with the number of authority boundaries crossed.
**Resolves:** T10; gives the authority boundary a measurable recovery cost, which no verified paper does.
**IVs:** recovery path {peer reroute, supervisor re-delegation, restart-at-origin} × boundary count {0,1,2}. **DVs:** utility preservation ratio; semantic quality of recovered output (judged secondary DV); tokens-to-recovery. **Moderators:** handoff-context completeness (full trace passed vs summary).
**Mechanism:** context truncation/lossy summarization at authority handoffs. **Competing explanation:** supervisor re-delegation adds a quality-improving review step that offsets the loss — net effect is the empirical question; the review-only arm (no boundary crossing) isolates it. **Falsifier:** path-invariant utility. **Null publishable:** moderate.
**Collision status:** OPEN organizationally; Handoff Tax is single-agent lineage, Loop-Back is fault-free. Fresh-search confirmation weak (S2/arXiv blocked) — flagged.

### A10-H8 — Scarcity moves the optimal verification point downstream
**Statement:** Under budget abundance, per-stage boundary gates dominate end-of-pipeline verification (Snowball's prescription); under scarcity, gate overhead consumes the budget recovery needs, and the optimal verification placement shifts downstream — a placement-level sign reversal distinct from H3's presence-level reversal.
**Resolves:** T3 × T5; connects Snowball's "when you verify matters more than whether" to D&K's scarcity backfire and 2606.01416's budget sweep.
**IVs:** verification placement {every stage, mid-only, end-only} × token/tool budget {abundant, 0.5×, 0.25×}. **DVs:** success; survival rate of injected faults; budget exhaustion rate. **Moderators:** fault position in chain; mechanism cost per gate.
**Mechanism:** gates have fixed cost per stage; under scarcity the opportunity cost is unrecovered faults elsewhere. **Competing explanation:** scarcity simply reduces total verification everywhere (a level effect, not a placement effect) — the budget-matched end-only arm discriminates. **Falsifier:** per-stage dominates at all budgets. **Null publishable:** yes — placement-invariance would simplify deployment guidance.
**Collision status:** OPEN as an interaction; both poles verified separately. Note: adjacent to candidate H3 — keep only if H3 is framed as presence/absence, not placement.

### A10-H9 — The committedness threshold: which faults escape natural containment
**Statement:** Fault escape probability is a threshold function of *time-to-first-state-commitment*, not of fault severity: faults that commit shared state within k steps escape; faults that remain conversational self-mask (TRAJDEBUG's 7.62:1). Severity predicts escape only through committedness.
**Resolves:** T7 — reconciles From Spark to Fire (one seed → systemic failure) with TRAJDEBUG (most local errors die) and Hallucination Cascade (net attenuation).
**IVs:** injected-fault committedness dial (steps-to-first-write: {immediate, delayed, never}) × severity {low, high} (crossed). **DVs:** escape probability; OBR; natural-attenuation rate. **Moderators:** topology; presence of gates.
**Mechanism:** conversational faults face re-generation washout each hop; committed faults bypass it (same mechanism as A10-H2, different IV — H2 varies fault class, H9 varies timing of commitment). **Competing explanation:** early-committing faults are also earlier-detected (detection races commitment); MTTD measurement discriminates. **Falsifier:** smooth severity-graded escape with no commitment effect. **Null publishable:** HIGH — a null here (escape is severity-graded, commitment irrelevant) undermines the mechanism basis of every gate-placement prescription.
**Collision status:** OPEN. SABER (mutating steps cut success 92–96%) is the nearest evidence but is single-agent and doesn't model escape.

### A10-H10 — Irreversibility flips the mechanism ranking
**Statement:** With reversible tools, rollback dominates the containment bake-off; with irreversible (committed) tools, rollback degrades to subtask restart and *prevention* (least-privilege gating) dominates — CtC's fail-safe/fail-operational division of labor is an artifact of its simulated reversibility, not a general law.
**Resolves:** T5; operationalizes mock-reviewer R5's objection as a hypothesis.
**IVs:** irreversibility regime {reversible, irreversible tool subset} × mechanism {none, verifier gate, rollback, quarantine+reroute, least-privilege prevention}. **DVs:** utility preservation; OBR; cost vector. **Moderators:** fraction of irreversible tools in the workflow.
**Mechanism:** rollback requires restorable state; committed effects (sent emails, executed refunds) make rollback cosmetic. **Competing explanation:** prevention wins everywhere because it's cheaper — the reversible arm discriminates. **Falsifier:** identical ranking in both regimes. **Null publishable:** yes — ranking-invariance would be a strong robustness result for CtC's law.
**Collision status:** OPEN. GoEX (undo/damage confinement) is a design paper; DeltaBox is infrastructure; nobody crosses regime × mechanism ranking on real LLM executions.

### A10-H11 — The sentinel is a hub: containment-layer faults out-propagate worker faults
**Statement:** A faulty sentinel/verifier corrupts more of the organization than a faulty worker at equal fault rate, because every worker's output transits the sentinel (hub centrality); net sentinel benefit reverses when sentinel fault rate exceeds worker fault rate by a topology-dependent factor. "Who watches the watcher" is a measurable crossover, not a slogan.
**Resolves:** D&K's own stated future work ("the EH service itself can fail") + From Spark to Fire's topological sensitivity.
**IVs:** fault injection site {worker, sentinel} × sentinel fault rate {0, p, 2p} × topology {star, chain, hierarchy}. **DVs:** system-level OBR; success; false-quarantine collateral (healthy workers isolated). **Moderators:** sentinel redundancy (paired sentinels arm).
**Mechanism:** centrality converts local faults into global ones; sentinels are maximally central by design. **Competing explanation:** sentinel faults are more *detectable* (privileged logging) — detection-matched arms discriminate. **Falsifier:** per-fault system damage equal across injection sites. **Null publishable:** yes — hub-immunity would justify trusted-mediator architectures.
**Collision status:** OPEN. No verified LLM-MAS work injects faults into the containment layer itself. (Weak-evidence caveat: fresh searches blocked; classical self-* literature discusses EH-service failure only rhetorically.)

### A10-H12 — The escalation velocity race: human containment only works on slow faults
**Statement:** Human escalation reduces blast radius only when fault propagation velocity (boundary crossings per minute) is below the human queue's drain rate; when faults outrun the queue, escalation is pure cost — and *raises* BR by delaying automated containment that was displaced. Containment benefit is a race between two rates, with a crossover at v*.
**Resolves:** T9; extends Oversight Has a Capacity's inverted-U from gating to post-fault recovery.
**IVs:** propagation velocity (via fanout/depth manipulation) × simulated human latency {fast, realistic, backlogged} × fallback policy {automated containment continues vs suspended during escalation}. **DVs:** BR at containment; utility; priced human minutes. **Moderators:** human accuracy (noisy oracle 80%); queue discipline.
**Mechanism:** escalation latency lets the fault traverse more boundaries before the verdict arrives. **Competing explanation:** the harm is the suspension policy, not the latency — the continue-during-escalation arm isolates it. **Falsifier:** escalation benefit flat in velocity. **Null publishable:** moderate.
**Collision status:** PARTIALLY OCCUPIED conceptually (2606.08919's fatigue/flooding; FALCON/DeCCaF capacity-constrained deferral — all single-decision gating, no propagation). The velocity-race form in MAS fault recovery is open.

---

## 3. Collision classification summary (my lane)

| Hypothesis | Classification | Basis |
|---|---|---|
| A10-H1 verification theater | OPEN (quality-level antecedent occupied) | 2609.14767 ABSTRACT today; PAE ABSTRACT today |
| A10-H2 depth-sign-by-fault-class | OPEN | both poles verified; reconciliation absent |
| A10-H3 consensus-inertia threshold | OPEN | vulnerability class named, threshold never parameterized |
| A10-H4 checkpoint race | PARTIALLY OCCUPIED | 2607.16530 + Young/Daly classical; LLM-semantic residue open |
| A10-H5 memory residue | OPEN (strongest gap) | adjacent evidence adversarial/observational only |
| A10-H6 correlation floor | OPEN | 2609.04373 ABSTRACT today (finance ABM, not containment) |
| A10-H7 recovery-path asymmetry | OPEN (weak fresh-search confirmation) | Handoff Tax single-agent; Loop-Back fault-free |
| A10-H8 placement×scarcity | OPEN | poles verified; interaction absent; adjacent to candidate H3 |
| A10-H9 committedness threshold | OPEN | TRAJDEBUG/SABER adjacent, neither models escape |
| A10-H10 irreversibility flip | OPEN | CtC law simulation-only; regime never varied on real LLMs |
| A10-H11 sentinel-as-hub | OPEN | classical rhetoric only; zero LLM-MAS injection into containment layer |
| A10-H12 escalation velocity race | PARTIALLY OCCUPIED conceptually | 2606.08919/FALCON/DeCCaF own costed gating, not post-fault races |

## 4. Meta-observation for the orchestrator

The single most consequential verified fact for *any* containment hypothesis (including the candidate's H1–H3): **the natural escape base rate is unmeasured everywhere.** TRAJDEBUG's 7.62:1 self-masking ratio (B14) plus Hallucination Cascade's net attenuation (verified today) imply the default dynamics may be self-containment. Every verified containment paper (CtC, DamageFlow, 2408.00989) compares mechanism vs no-mechanism on *injected-and-triggered* faults, none reports what fraction would have died unaided per fault class. A10-H9 is therefore not just another hypothesis — it is the control condition without which all other containment effects (including H2/H3) are uninterpretable. Recommend it be promoted from alternative hypothesis to mandatory measurement in the pilot.
