# AUDIT2 — AGENT 7: HUMAN OVERSIGHT SPECIALIST

**Date:** 2026-09-21
**Mission:** Determine whether the human-escalation × resource-scarcity interaction is already covered; verify anchors (Oversight Has a Capacity 2606.08919, READY 2609.02095, TAO mPh4B1JoAN, DeCCaF TMLR, AI Control 2312.06942, Multi-Agent Off-Switch Game, Invisible Ink 2608.02018, 2609.02191); go beyond prior reports (B8, E6, W2-cand4); answer whether "reviewer capacity as a resource that containment mechanisms consume" is modeled anywhere in LLM-MAS; classify collisions for claims 17/18.
**Stance:** adversarial — trying to kill novelty, not defend it.

---

## 1. Bottom line

**The human-oversight lane does NOT kill the candidate's core claim, but it strips the novelty of every *concept* behind H3's reviewer-budget dimension.** "Oversight capacity is finite, is spent by escalation/containment policies, and its exhaustion reverses the sign of the safety benefit" exists in at least four verified forms: (i) a modeling result with an explicit inverted-U (Oversight Has a Capacity, 2606.08919); (ii) a governance theory with an oversight *solvency condition* (Kadowaki, SSRN 10.2139/ssrn.7296638); (iii) capacity-constrained deferral frameworks (DeCCaF TMLR; FALCON); (iv) a deployed-systems lesson that review-everything "fails at scale and may paradoxically reduce safety" (Scalable Oversight for AI in Mental Health, 2609.09533). What remains unoccupied — and I could not find any counterexample — is the **experimental demonstration** of that sign reversal *for containment of faults already propagating through a multi-agent LLM organization*, where the containment mechanisms themselves draw down a shared, priced reviewer budget. Every occupant is single-agent, single-decision, prevention/gating, adversarial-security, or theory-only.

**Strongest collision (see §3.1):** Oversight Has a Capacity (2606.08919) — it already owns "more oversight can make the system less safe" as a function of escalation load on a fatiguing reviewer. It is a modeling result in single-agent action gating, so it collides with the *mechanism* of H3's reviewer dimension, not with the *setting* (multi-agent propagation + recovery).

---

## 2. Anchor verification (all eight)

| Anchor | Status | Verification | Notes |
|---|---|---|---|
| Oversight Has a Capacity (arXiv:2606.08919, v1 8 Jun 2026) | CONFIRMED as described in B8 | **ABSTRACT+ VERIFIED** (arXiv abs page re-fetched 21 Sep) | Inverted-U safety vs escalation rate with endogenous fatiguing reviewer; flooding attack; explicitly disclaims mechanism novelty, cites FALCON/DeCCaF; inverted-U is a *modeling* result, human study not yet run |
| READY (arXiv:2609.02095, v1 2 Sep 2026) | CONFIRMED | **ABSTRACT VERIFIED** (re-fetched) | Prices human-oversight burden for deployment qualification; 16 systems, 750 cases; 39.2% vs 29.6% review at equal reliability. Oversight = screening cost, not fault containment |
| TAO (OpenReview mPh4B1JoAN, ICLR 2026, rejected) | CONFIRMED | **ABSTRACT VERIFIED** via OpenReview API (re-fetched) | Hierarchy absorbs ≤24% of agent errors; human physician top tier 40%→60% triage; healthcare-only; no reviewer-capacity model |
| DeCCaF (TMLR, forum TAvGZm2Rqb) | CONFIRMED | **ABSTRACT VERIFIED** via OpenReview API (re-fetched) | L2D under cost + **human work-capacity constraints**; constraint programming over team of synthetic analysts; single-decision classification |
| AI Control (arXiv:2312.06942, ICML 2024) | CONFIRMED | **ABSTRACT VERIFIED** (re-fetched) | Limited trusted (human) labor as budgeted escalation resource traded against automated checking; adversarial, single-agent coding |
| Multi-Agent Off-Switch Game (AAAI 2026 TrustAgent poster, XXW1dIcgik) | CONFIRMED | **ABSTRACT VERIFIED** via OpenReview API (re-fetched) | Corrigibility not compositional; theory only; no capacity/scarcity dimension |
| Invisible Ink Threats (arXiv:2608.02018, v1 3 Aug 2026) | CONFIRMED | **ABSTRACT VERIFIED** (re-fetched) | HITL confirmation gates fail against low-salience injected goals; simulated user review; single-agent CUA security |
| Fault-point human interventions (arXiv:2609.02191, v1 2 Sep 2026) | CONFIRMED | **ABSTRACT VERIFIED** (re-fetched) | Correct human intervention at fault points +40% accuracy, incorrect −6% with drift/uncertainty; medical conversation MAS; **no capacity/scarcity manipulation** — the human is always available and always answered |

No anchor was found to be misdescribed by the prior reports. B8/E6/W2-cand4 characterizations hold.

---

## 3. New finds beyond the 48 prior reports

### 3.1 Tier 1 — strongest new/direct collisions

**Control Tax: The Price of Keeping AI in Check** (Terekhov et al., arXiv:2506.05296, v1 Jun 2025, v3 Mar 2026) — **ABSTRACT VERIFIED** (fetched 21 Sep). Formalizes the "control tax": operational/financial cost of integrating control measures into AI pipelines; optimized monitoring strategies balancing safety vs cost "while accounting for practical constraints like auditing budgets." This is the AI-control literature explicitly pricing containment/oversight and treating audit capacity as a binding budget — the adversarial-single-agent analog of H2/H3's cost vector. Not in any of the 48 reports. **Threat: moderate.** It occupies "containment cost must be budgeted" in the AI-control frame; it does not touch multi-agent propagation, non-adversarial faults, or scarcity sign reversal.

**Human-on-the-Loop: A Theory of Oversight Capacity, Its Failure Modes, and the Non-Delegable Residual** (Kadowaki, SSRN 2026, DOI 10.2139/ssrn.7296638) — **ABSTRACT VERIFIED** via Crossref (fetched 21 Sep). States verbatim-level the concept the candidate needs: "oversight is not a role but a **consumable resource** with a measurable capacity — uncommitted attention, interaction time, context re-acquisition cost, neglect time — and therefore with a **solvency condition**. Insolvent oversight fails not by refusing work but by accepting it, and its symptom is a rising override and non-response rate." (E6 listed it; I re-verified and quote it here because it is the single most direct statement of "reviewer capacity as a resource that gets consumed," and it is 2026.) **Threat: moderate-high for framing, low for results** — pure theory, no experiments, no LLM-MAS, no fault propagation. The candidate MUST cite it or reviewers who know it will call the oversight-solvency framing unattributed.

**Scalable Oversight for AI in Mental Health: Lessons from 350,000 AI Coaching Conversations** (Havlik et al., arXiv:2609.09533, v1 8 Sep 2026) — **ABSTRACT VERIFIED** (fetched 21 Sep; not in prior reports). "Clinician review of every AI output is often proposed as a safeguard… but vigilance research suggests this approach **fails at scale and may paradoxically reduce safety**." A deployed-systems lessons paper asserting the oversight-backfires-at-scale sign reversal in a real (mental-health) human-on-the-loop deployment. **Threat: low-moderate** — no controlled experiment, no MAS, no fault injection; but it is a September-2026 public statement of the sign-reversal intuition for human oversight, which weakens any "first to suggest oversight can backfire under load" phrasing.

### 3.2 Tier 2 — reviewer/analyst capacity under load (empirical, adjacent communities)

| Paper | ID / venue | Verification | Relevance |
|---|---|---|---|
| PACT: Reducing Alert Fatigue in Low-Prevalence SOC Streams | arXiv:2605.22324 (May 2026, sub. ACSAC 2026) | ABSTRACT VERIFIED | SOC analyst queries as an explicit budget ("3.8–5.2× fewer analyst queries"); alert fatigue from investigation load in low-prevalence streams — the queue/burden math the candidate's reviewer-budget arm needs |
| Can Risk-Based Alerting Mitigate Cybersecurity Alert Fatigue? | arXiv:2609.02465 (2 Sep 2026, sub. USENIX Sec '27) | ABSTRACT VERIFIED | First systematic RBA evaluation; models "SOCs of varying sizes and alert volumes" — analyst capacity as the constrained resource; Sep-2026 |
| Evaluating Algorithm-Assisted Human Decision-Making Over Repeated Algorithm Exposure | arXiv:2607.27701 (Jul 2026, stat.ME) | ABSTRACT VERIFIED | Experimental design + estimands for behavior adaptation under repeated exposure: **automation bias, alert fatigue, calibrated reliance** — the measurement methodology for exactly the reviewer-degradation effects the candidate's noisy-oracle arm idealizes away |
| AI-Driven Security Alert Screening and Alert Fatigue Mitigation in SOCs: A Survey | arXiv:2605.08316 (May 2026) | TITLE/ABSTRACT via arXiv search listing | SOC alert-fatigue mitigation is a surveyed, mature area |
| Towards Human-AI Teaming to Mitigate Alert Fatigue in Security Operations Centres | ACM TOIT (OpenReview forum Komjfrb9lS) | TITLE/VENUE VERIFIED via OpenReview search | Human-AI teaming explicitly *for* alert-fatigue mitigation |

**Assessment:** "Reviewer capacity is finite, degrades under load, and must be budgeted" is one of the most empirically established facts in applied human factors — clinical CDS alert fatigue (override rates; van der Sijs et al., JAMIA 2008, DOI 10.1197/jamia.m2311, **Crossref-verified**), SOC analyst fatigue (above), automation bias (Parasuraman & Riley, Human Factors 1997, DOI 10.1518/001872097778543886, **Crossref-verified**), out-of-the-loop performance (Endsley & Kiris, Human Factors 1995, DOI 10.1518/001872095779064555, **Crossref-verified**), ironies of automation (Bainbridge, Automatica 1983, DOI 10.1016/0005-1098(83)90046-8, **Crossref-verified**), levels of automation (Parasuraman/Sheridan/Wickens, IEEE TSMC 2000, DOI 10.1109/3468.844354, **Crossref-verified**), and one-human-many-robots supervisory capacity / fan-out / neglect tolerance (Crandall et al., HRI 2010, DOI 10.1109/HRI.2010.5453223, **Crossref-verified**). None of this is LLM-MAS, but a reviewer with any HF background will treat H3's reviewer dimension as a *transfer* of known results — which is fine, since the candidate's whole spine is transfer-testing, but the paper must frame it that way and cite this lineage.

### 3.3 Tier 3 — fresh (last-two-weeks) items in the lane

| Paper | ID | Verification | Relevance |
|---|---|---|---|
| When Should a Failing Robot Ask? Initiating Corrective Human-Robot Dialogue from Audited Sensor Evidence | arXiv:2609.21942 (18 Sep 2026, IROS 2026 H-R Dialogue ws) | ABSTRACT VERIFIED | Failure-triggered ask-human decision with **explicit question cost**; finds VLMs' ask rates "ignore a fourfold change in question cost." Single robot, but it is the freshest "escalation priced against cost" result — and its finding (agents don't track ask-cost) is directly usable motivation |
| TeamCAMS: platform for studying human behaviour in human-AI teams | arXiv:2609.20490 (17 Sep 2026) | ABSTRACT VERIFIED | Process-control simulation for human-AI team studies incl. automation reliability and stress — evidence the "human supervises automated team under load" paradigm is actively studied in HCI, not in LLM-MAS |
| From Task Success to Productive Success: Evaluating Human-AI Collaboration by Quality and Cost | arXiv:2609.21117 (Sep 2026) | TITLE VERIFIED (cs.HC listing) | Prices human collaboration — costed-HITL evaluation trend continues |
| Loopjacking (2609.21081), Enforcement Gap (2609.15293, sub. ICLR 2027) | — | ABSTRACT VERIFIED (2609.15293 re-fetched) | Already in C1; human-approval boundary as attack surface; machine-side enforcement, no capacity model |

ICLR 2027 submissions are not yet visible through OpenReview's public search API (searches for "human oversight", "escalation policy agents", "oversight fatigue", "containment failure agents" returned no ICLR-2027-tagged notes on 21 Sep). The Enforcement Gap paper's comments field confirms ICLR 2027 submission is underway — **the highest-risk window for a scoop is the next ~2 weeks**; a re-sweep after the ICLR 2027 deadline is mandatory.

---

## 4. The assigned question: is "reviewer capacity as a resource that containment mechanisms consume" modeled anywhere in LLM-MAS?

**No — not in LLM multi-agent systems, and not for fault containment/recovery anywhere.** The complete verified inventory of "reviewer/oversight capacity as consumable resource":

| Work | Setting | Capacity modeled? | Containment consumes it? | LLM-MAS? |
|---|---|---|---|---|
| Oversight Has a Capacity (2606.08919) | single-agent action gating | Yes (fatigue curve) | Yes — escalation policy "spends" attention; inverted-U; flooding attack | No (single agent; prevention not recovery) |
| Kadowaki SSRN 2026 | governance theory | Yes (solvency condition) | Conceptually | No (theory) |
| DeCCaF (TMLR) / FALCON (withdrawn) | L2D classification | Yes (work-capacity constraints, fatigue CMDP) | Deferral consumes capacity | No (single-decision) |
| AI Control (ICML 2024) / Control Tax (2506.05296) | adversarial code gen | Yes (trusted-labor/audit budget) | Auditing consumes budget | No (single-agent, adversarial) |
| READY (2609.02095) | deployment qualification | Review fraction measured | Oversight = screening cost | No (no faults, no propagation) |
| Nonuniformity Principle (2607.16530) | single-workflow oversight placement | Yes (time/resource constraints) | Oversight stages reduce rework/tokens | No (single workflow, no faults) |
| SOC/clinical alert-fatigue literature | human triage | Yes (empirically) | Alerts consume analyst capacity | No |
| HRI fan-out/neglect tolerance | human–robot teams | Yes | Supervision consumes attention | No (robots) |
| **Anything in LLM-MAS fault propagation/recovery** | — | **Not found** | **Not found** | — |

TAO (the closest MAS work) has a human as top tier but no capacity model; 2609.02191 manipulates intervention *correctness*, never intervention *availability/capacity*. The candidate's specific construction — containment arms (verifier gate, sentinel quarantine, human escalation) drawing down a shared priced budget of reviewer-minutes, with the scarcity sign reversal measured on propagating semantic faults — remains unoccupied.

---

## 5. Is the human-escalation × resource-scarcity interaction already covered?

**Covered as a concept; not covered as an experiment in the candidate's setting.**

- The *direction* of the interaction (oversight helps when capacity is abundant, hurts when scarce) is already asserted or modeled in: Oversight Has a Capacity (inverted-U, modeling), Kadowaki (solvency, theory), Scalable Oversight for AI in Mental Health (deployment lesson, "paradoxically reduce safety"), and is the foundational empirical fact of the alert-fatigue literature (clinical + SOC).
- **Not found anywhere:** a controlled experiment varying reviewer/oversight capacity (or queue latency) while measuring containment efficacy against *propagating* faults in a multi-agent LLM system; any LLM-MAS paper where human escalation is one arm in a containment bake-off priced in oversight-minutes; any measurement of how escalation load from one fault degrades oversight of concurrent faults (the queue-interference effect, which is the natural mechanism for backfire in MAS and which even Oversight Has a Capacity does not test — its flooding attack is adversarial, single-agent).

---

## 6. Collision classification for claims 17 and 18

**Caveat:** no numbered claims registry exists anywhere in `maso_2026_investigation/` (checked FINAL_RECOMMENDATION.md, all 53 reports, raw/). I classify the two lane-relevant claims as inferred from the final design (§6.3 of FINAL_RECOMMENDATION: "noisy-oracle human escalation (80% accuracy, priced in oversight minutes, queue-latency sweep)" as a containment arm). If the orchestrator's claim texts differ, re-map accordingly.

**Claim 17 (inferred): "Human escalation as a costed containment/recovery mechanism for propagating faults in LLM-MAS is unstudied."**
Classification: **SURVIVES, WOUNDED.** No located work compares human escalation vs automated containment for propagating organizational faults (E6's conclusion, re-confirmed by my sweep). But the wound is real: the *components* are all occupied — escalation-as-containment classically (adjustable autonomy, JAIR 2002), escalation-with-cost in L2D (DeCCaF/FALCON), human-as-top-tier in LLM MAS (TAO), human intervention at fault points with measured ±effects (2609.02191), priced human oversight (READY), human-vs-automated containment comparison template (AI Control). The claim must be phrased as the *conjunction* (propagating faults × org structure × priced human arm × comparison), never as "first to study human escalation in LLM MAS" — that phrasing is dead (TAO, 2609.02191).

**Claim 18 (inferred): "Reviewer/oversight capacity as a resource consumed by containment mechanisms, producing a scarcity sign reversal, is novel."**
Classification: **PARTIAL COLLISION — demote to transfer-test framing.** The concept is multiply occupied (Oversight Has a Capacity's inverted-U and "the guard's escalation policy spends it"; Kadowaki's oversight solvency; DeCCaF/FALCON capacity constraints; Control Tax audit budgets; alert-fatigue empirics). What survives is narrower: "first *experimental* demonstration that containment mechanisms consuming a shared reviewer budget reverse sign under scarcity *for faults propagating through an LLM multi-agent organization*" — and even that must cite Oversight Has a Capacity as the single-agent gating analog and Kadowaki for the solvency framing. Any phrasing like "we introduce the idea that oversight capacity is finite/consumable" would be **FALSE**.

---

## 7. Unexpected finding

**The freshest paper in the lane (2609.21942, 18 Sep 2026) hands the candidate its motivating result for free:** six open VLMs, given an explicit act/consult/ask-a-human decision with a stated question cost, have ask rates that "ignore a fourfold change in question cost" — i.e., current LLM agents do not track escalation cost at all. That is direct evidence that the scarcity-aware escalation policy the candidate wants to study is not just unstudied but *currently absent from model behavior*. Also unexpected: the SOC alert-fatigue literature (PACT, RBA/CATS, both 2026) has already built the exact queue/burden mathematics (analyst queries as budget, low-prevalence streams) that a reviewer-capacity arm needs — importable rather than novel.

## 8. Search log and coverage limits

- Channels: arXiv abs-page fetches (worked throughout); arXiv HTML search (worked, then 429 from ~mid-session); arXiv export API (worked briefly, then 429); OpenReview api2 notes/search (worked; note-detail endpoints challenge-blocked); Crossref API (worked); Semantic Scholar API and DBLP (429/blocked throughout — residual discovery risk for non-arXiv venues).
- Queries run (beyond prior reports' vocabulary): "oversight capacity", "alert fatigue" (±agent), "scalable oversight", "human oversight"×"multi-agent"×LLM, "reviewer fatigue", "audit budget" AI control, "human intervention"×fault×MAS, "when to escalate", "human-in-the-loop" workload, "defer to human" MAS, "human takeover", "cost of human" intervention, oversight "sign reversal"/backfire, "containment backfire", "resource scarcity containment", "human-AI team" failure recovery, SOC analyst fatigue, plus cs.MA/cs.HC recent-listing scans (through 18–21 Sep 2026) and OpenReview term searches.
- Known gaps: Semantic Scholar/DBLP unavailability means non-arXiv 2026 venues (some ACM/IEEE) are under-covered; ICLR 2027 submissions not yet publicly searchable — re-sweep after the deadline.
