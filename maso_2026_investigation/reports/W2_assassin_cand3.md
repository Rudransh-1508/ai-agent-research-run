# W2 ASSASSIN — CAND-3 (AttribContain): Attribution-Informed Containment

**Date:** 2026-09-21
**Mission:** Kill CAND-3: "how accurate must attribution be before attribution-guided containment (targeted quarantine/rollback) beats attribution-free containment (verify-everything, restart-all)? Derive the threshold empirically; provenance+attribution-guided minimal-containment controller."
**Attack vectors assigned:** (a) attribution output → runtime intervention/containment in LLM MAS; (b) attribution quality vs downstream intervention utility; (c) conformal/uncertainty-aware attribution triggering actions (2605.06788); (d) the attribution-guided repair cluster (MARS 2607.29055, DoCtOR 2608.28264, FlowFixer 2607.02882, CUADebug 2608.02643, AgentDebugX 2607.18754) — containment or rerun-repair?; (e) the threshold question anywhere, incl. classical fault-diagnosis literature.
**Method:** Built on wave-1 reports (B3, B14, B18, D1, E2, E4, C5). All load-bearing items below re-verified on primary pages this session: arXiv abs + full HTML (2605.06788, 2608.02643, 2608.28264 read in full), arXiv abs (2607.29055, 2607.18754, 2607.02882, 2511.22924, 2608.02464, 2607.06273), ACL Anthology (2026.acl-long.373), Crossref (classical DOIs). OpenReview API went challenge-walled mid-session; BPD details rely on wave-1 C5's verified record (OpenReview `TphOLCDmKB`, code github.com/ChengcanWu/BPD). DataCite/arXiv-API/S2 searches for "attribution-guided containment", "diagnosis-driven containment", "failure attribution quarantine" returned only Zenodo spam — a verified negative.

---

## VERDICT: WOUNDED — survives only in narrowed form

The headline premise "nobody feeds attribution into containment decisions" is **false as stated** (§1). The repair cluster closes the loop only with rerun-repair, not containment (§2). The specific empirical question — an attribution-accuracy dial vs attribution-free containment, with a derived crossover threshold, for organic faults — is **genuinely unanswered** and is explicitly flagged as open by the closest neighbor (CUADebug's own future-work section). The question's *conceptual template* is 46 years old in medicine and has classical SE analogs (§4), and the strongest intellectual counter-thesis (cheap blind recovery beats expensive diagnosis — ROC/microreboot) is published classical work CAND-3 must engage, not ignore.

---

## 1. Attribution/risk output → containment decisions: OCCUPIED in the adversarial wing, partially occupied for organic faults

| Work | ID / venue (verified) | What it does | Why it wounds CAND-3 | Why it doesn't kill |
|---|---|---|---|---|
| **BPD — Securing MAS Against Corruptions via Node Contribution Backpropagation** | OpenReview `TphOLCDmKB`, **ICML 2026** (Accept, regular); code released (wave-1 C5-verified) | Blame assignment via node-contribution backpropagation over signed communication DAG (LLM scores edges, threshold ε=1.5); **repair = isolate the detected agent, clear its outgoing edges, re-run**; flat vs hierarchy comparison | This *is* an attribution→isolation→re-run closed loop at a top venue. "Attribution-informed containment" as a mechanism class exists | Adversarial (malicious-agent) framing; attribution = attacker detection, not organic-fault who/when; no accuracy dial, no comparison vs attribution-free containment, no threshold |
| **AgentRevive — Taming "Zombie" Agents** | ACL 2026, 2026.acl-long.373, DOI 10.18653/v1/2026.acl-long.373 (verified on Anthology) | Hallucination-**risk estimator** drives soft state transitions Active/Standby/Terminated; standby nodes quarantined but retained; edge pruning by learned state | Non-adversarial, risk-score-driven **quarantine of unreliable agents** — a diagnosis-signal→containment loop | Risk score ≠ failure attribution (no localization of a specific fault); debate/topology-evolution setting; no attribution-quality analysis |
| **RoMa** | CSCWD 2026, DOI 10.1109/cscwd68734.2026.11582680 (wave-1 E2-verified) | Bayesian credibility → **dynamic agent isolation with rehabilitation**, vs failover and redundancy | Credibility-driven quarantine of faulty agents, non-adversarial | Credibility is a running reputation score, not per-failure attribution; metrics are task success, no threshold |
| **MAS-Shield** | arXiv:2511.22924, **EMNLP Findings 2026** (abs verified) | "Rather than applying uniform scrutiny, dynamically allocates defense resources": Critical Agent Selection → light auditing → committee escalation | Occupies **targeted vs uniform (verify-everything) scrutiny** — CAND-3's exact baseline contrast | Targeting is by structural influence, not attribution output; adversarial; no accuracy threshold |
| **Conformal Agent Error Attribution** | arXiv:2605.06788 (abs + full text read) | Conformal prediction sets (contiguous, coverage-guaranteed) over the decisive-error step; **set start = rollback point**; evaluates rollback Success/Coverage/**Cost** vs Top-1 restart baseline | The closest existing work to "uncertainty-aware attribution triggers action": attribution uncertainty (set size) directly sizes the intervention. Occupies conformal-attribution→rollback | **Key null result:** LF conformal rollback beats Top-1 "by a small margin, within one standard deviation" — uncertainty-aware attribution did NOT significantly improve rollback. Rollback is whole-trajectory restart, not selective containment of spread; no blind-containment (restart-all/verify-everything) arm; no accuracy dial |

**Assessment:** CAND-3 cannot claim "first to connect attribution to containment." It can claim: first to do it for **organic faults**, first to treat attribution accuracy as an **independent variable**, first to **compare against attribution-free containment arms**, first to **derive the crossover threshold**. The conformal paper's null (CP ≈ Top-1) is actually supporting evidence that the threshold question is non-trivial and unanswered.

## 2. The attribution-guided repair cluster: all rerun-repair, NONE do containment

All five verified on primary pages:

| Work | ID / venue | Loop closed | Containment? | Attribution-quality analysis? |
|---|---|---|---|---|
| **MARS / StateMAS** | 2607.29055 (under review) | MCTS repair w/ **diagnosis-guided expansion**; ablation: diagnosis guidance "critical" | No — search over repairs of the failed run | Ablation only (with/without diagnosis); no accuracy variation |
| **DoCtOR** | 2608.28264, **EMNLP 2026 main** (full text read) | Attribution → counterfactual correction → **only the decisive-error agent reflects**; +22–27% over Reflexion/Retroformer/COPPER | No — targeted *reflection*, but the framing is containment-flavored: all-agent reflection "contaminates their memory with wrong insights" | Ablation: removing diagnosis causes largest drop. **No oracle-attribution arm, no accuracy dial.** But it IS a published targeted-vs-blanket intervention comparison where targeted wins |
| **FlowFixer** | 2607.02882 | Symbolic RCA → targeted repair patches; 71.3% repair success | No — workflow patch repair | No |
| **CUADebug** | 2608.02643 (full text read) | RCA → guided re-rollout; **Machine RCA (19–29% exact) ≈ human-oracle guidance in recovery (28.5% vs 29.9% re-rollout Acc)** | No — re-execution | **Closest existing evidence on attribution quality → intervention utility** — and the authors explicitly defer it: "Matched re-rollout ablations should test how subtype prediction, exact root-step localization, and evidence quality affect behavioral repair" (future work). Single-agent CUA |
| **AgentDebugX** | 2607.18754 | Detect–Attribute–Recover–**Rerun**; 13/73 GAIA repairs vs 4–6 for decoupled baselines | No — diagnose-and-rerun toolkit | No |

Plus (wave-1, re-confirmed): RESKILL (2609.15684, EMNLP 2026 main, abs verified): "explicit attribution alone is insufficient; durable improvement emerges when attribution is integrated with repair selection" — attribution→repair *selection*, single-agent. AgentTether (2607.06273, abs verified): diagnosis→guarded runtime intervention, explicitly vs "blind retry"; single-agent tau-bench. Real-Time Detection & Repair (2608.02464, abs verified): detection-triggered rollback+rerun recovers 45% vs 16% resampling control (p=0.0005) — a targeted-vs-blind recovery comparison, but detection-driven (anomaly flag), not attribution-driven, single-agent.

**Assessment:** the cluster wounds the *framing* ("attribution stops at localization" is no longer true — it feeds repair and reflection-targeting) but not the *core*: none of these contain propagation, none quarantine/rollback selectively across agents, none vary attribution accuracy, none derive a threshold. DoCtOR is the most dangerous: a reviewer can say "targeted-beats-blanket intervention via attribution is already shown." Rebuttal: DoCtOR targets *who reflects* (repair), not *what to isolate* (containment), and never asks how much attribution error erases the benefit.

## 3. Attribution quality vs downstream intervention utility: embryonic, unanswered

- **CUADebug**: imperfect machine RCA nearly matches human-oracle recovery — suggests the threshold may be *low* for re-rollout repair; explicitly unfollowed-up.
- **Conformal attribution**: better-calibrated attribution (coverage-guaranteed sets) does NOT significantly beat Top-1 for rollback success — suggests the threshold may be *high or irrelevant* for whole-trajectory rollback. These two findings pull in opposite directions: direct motivation for CAND-3's study.
- **MARS / DoCtOR / RESKILL ablations**: qualitative with/without-diagnosis contrasts only.
- **AgenticRAG-FP** (2608.20627, wave-1): post-hoc diagnosis accuracy decays 0.91→0.00 by propagation hop 2–3 — implies attribution quality is *itself* a function of containment timing; nobody closes that loop.
- No found work anywhere varies attribution accuracy as a controlled dial and measures downstream intervention utility. Verified negative across DataCite/OpenReview/arXiv-channel searches.

## 4. The threshold question in classical literature: the QUESTION is old, the MAS answer is absent

| Work | ID (verified) | Content | Threat to CAND-3 |
|---|---|---|---|
| Pauker & Kassirer, "The Threshold Approach to Clinical Decision Making" | NEJM 1980, DOI 10.1056/nejm198005153022003 | Test/treatment thresholds: when diagnostic quality justifies test-guided vs empirical treatment | The *question form* — "how good must diagnosis be before guided action beats blind action" — is 46-year-old decision theory. CAND-3 must cite this as template, not claim the question is new |
| Pauker & Kassirer, "Therapeutic Decision Making: A Cost-Benefit Analysis" | NEJM 1975, DOI 10.1056/nejm197507312930505 | Precursor cost-benefit threshold model | Same |
| Assiri & Bieman, "Fault localization for automated program repair: effectiveness, performance, repair correctness" | Software Quality Journal 2016, DOI 10.1007/s11219-016-9312-z | FL quality ↔ APR outcomes (effectiveness, correctness) | Classical SE analog: localization quality → repair benefit studied for APR |
| Liu et al., "You Cannot Fix What You Cannot Find!" | ICST 2019, DOI 10.1109/icst.2019.00020 | FL bias in APR benchmarking; repair systems inherit FL error | Same; supplies the "garbage-in" caution |
| Parnin & Orso, "Are automated debugging techniques actually helping programmers?" | ISSTA 2011, DOI 10.1145/2001420.2001445 | Localization tools help less than assumed | Counter-evidence template: better attribution may not help containment as much as expected |
| Candea et al., Microreboot (OSDI 2004) + ROC (10.1109/mc.2004.219) | USENIX/Crossref verified (wave-1 E4/B14) | **Cheap blind recovery can dominate expensive diagnosis** — "recover at the slightest hint of failure" | The strongest intellectual counter-thesis: if restart-all/quarantine-all is cheap, the threshold may never be crossed. CAND-3 must measure exactly this, and a null/high-threshold result is still publishable if framed as "when does attribution pay?" |
| Model-based diagnosis (Reiter 1987; de Kleer & Williams) | established | Minimal diagnoses → repair; diagnosis quality assumed, not dialed | Background; no threshold analysis |

No classical or AIOps work found that *empirically derives* a diagnosis-accuracy crossover threshold for guided-vs-blind repair/containment. The medical literature derives it analytically from utilities; the SE literature documents FL→repair coupling without a crossover. The empirical threshold study in LLM MAS is unoccupied.

## 5. What survives (precise statement)

SURVIVES, if reframed as: **"The attribution-accuracy threshold for containment: an empirical study of when attribution-guided containment (targeted quarantine/rollback of the attributed agent/span) beats attribution-free containment (verify-everything, restart-all) for organic faults in LLM multi-agent organizational workflows."** Mandatory conditions:

1. **Drop** any "first to feed attribution into containment/intervention" claim — cite and differentiate BPD (ICML 2026), AgentRevive (ACL 2026), RoMa (CSCWD 2026), MAS-Shield (EMNLP-F 2026), Conformal rollback (2605.06788), DoCtOR (EMNLP 2026).
2. **Organic faults + containment-proper** is the defensible intersection: adversarial blame→isolation exists (BPD); organic-fault attribution→*containment* (not repair) does not.
3. **The accuracy dial is the contribution** — nobody varies it; CUADebug explicitly punts; the conformal null result shows the answer is non-obvious.
4. **Engage the counter-thesis**: microreboot/ROC and Pauker-Kassirer thresholds as the classical frame; report the threshold wherever it lands, including "never crossed" (that would still be a result: blind containment dominates → attribution field's downstream value questioned).
5. **Note the W2_statistics.md finding** (same repo): the regression-over-accuracy-dial design is statistically powered (240 obs/arm, threshold CI ±0.10–0.20) — feasibility is fine; the binding risk is curve separation at a=1.0.

## 6. Most damaging papers (ranked)

1. **BPD** (ICML 2026, OpenReview `TphOLCDmKB`) — attribution→isolation→re-run closed loop at top venue.
2. **Conformal Agent Error Attribution** (arXiv:2605.06788) — uncertainty-aware attribution sizes the rollback intervention; null vs Top-1.
3. **DoCtOR** (arXiv:2608.28264, EMNLP 2026) — targeted-vs-blanket intervention via attribution, targeted wins; memory-contamination framing.
4. **AgentRevive** (ACL 2026, 2026.acl-long.373) — risk-driven soft quarantine of faulty agents, non-adversarial.
5. **CUADebug** (arXiv:2608.02643) — machine-RCA ≈ oracle recovery; explicitly names CAND-3's question as open future work (both a threat and the strongest openness evidence).
6. **MAS-Shield** (arXiv:2511.22924) — targeted vs uniform scrutiny resource allocation.
7. Classical: Pauker & Kassirer NEJM 1980 (10.1056/nejm198005153022003); Candea microreboot/ROC; Assiri & Bieman SQJ 2016 (10.1007/s11219-016-9312-z).

*Verification log: arXiv abs pages + full HTML for 2605.06788, 2608.02643, 2608.28264; arXiv abs for 2607.29055, 2607.18754, 2607.02882, 2609.15684, 2511.22924, 2608.02464, 2607.06273; ACL Anthology 2026.acl-long.373; Crossref for all classical DOIs; DataCite/OpenReview negative searches (queries: "attribution-guided containment", "diagnosis-driven containment", "attribution-driven remediation LLM", "failure attribution quarantine agent"). OpenReview API challenge-walled mid-session; BPD record inherited from wave-1 C5 (verified there via OpenReview API + GitHub).*
