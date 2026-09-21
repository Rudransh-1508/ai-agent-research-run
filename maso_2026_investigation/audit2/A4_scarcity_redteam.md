# AGENT 4 — RESOURCE SCARCITY SPECIALIST: H3 RED-TEAM

**Date:** 2026-09-21
**Mission:** Kill H3 — "containment/recovery mechanisms help under resource abundance but hurt under scarcity (sign reversal)" — by finding prior demonstrations of the pattern "intervention improves reliability at high budget, reduces it at low budget" in LLM agents, classical MAS, or distributed systems. Answer the "isn't this just retry storms?" reviewer question.
**Stance:** Adversarial. H3 treated as disposable.

---

## 0. Bottom line

**H3 is NOT killed as an LLM-MAS experimental result — no work demonstrates the containment×scarcity sign reversal for propagating faults in executing LLM agent organizations. But H3 is badly exposed on three sides:**

1. **The phenomenon is textbook classical.** The sign reversal "recovery/containment backfires when the resource it consumes is scarce" is established in at least four independent literatures: (a) Dellarocas & Klein ICMAS 2000 itself (the candidate's own anchor — containment slightly *worse* than survivalist under subcontractor scarcity; FULL TEXT VERIFIED by E5); (b) distributed-systems retry storms / metastable failures (Google SRE Book ch. 22; Bronson et al. HotOS 2021; MSF-Model SRDS 2024; Isaacs et al. HotOS 2025; Mehan SSRN 2026 — retries 25% *worse* than no-retry under correlated failure); (c) bounded rationality / metareasoning (Russell & Wefald, AI Journal 1991 — value of computation can be negative under time pressure); (d) human-oversight capacity (Oversight Has a Capacity 2606.08919 — inverted-U safety vs escalation rate under reviewer fatigue; FALCON/DeCCaF capacity-constrained deferral). A claim that the *phenomenon* is novel is DEAD.
2. **The closest LLM-era budget×recovery evidence points the OTHER way.** Self-Healing Orchestrators (arXiv:2606.01416) ran a matched recovery-budget sweep and found targeted recovery helps **most** at the **tightest** budget (94.0% vs 85.3%/88.2% at one attempt) — an anti-backfire result in a tool-augmented LLM system. FTDI (SSRN 2026) built budget-gated recovery for LLM MAS code-gen precisely because naive retries are "low-yield" under constraint — and reports no reversal either. H3 is therefore not merely untested; the nearest adjacent experiment is unfavorable to it. This makes H3 a genuinely risky headline (and, symmetrically, a genuinely non-foreordained transfer test).
3. **The "just retry storms" dismissal is partially valid against the current design.** The current scarcity operationalization (W2_feasibility_A: "one specialist role + rate-limited approval tool") is exactly the congestion regime where the backfire is textbook SRE knowledge. What blocks the dismissal is only what the paper has not yet committed to: demonstrating backfire through non-congestion channels (token-budget partition, false-positive quarantine of healthy work, reviewer fatigue) and showing the crossover *threshold/magnitude* shifts under semantic faults — things no classical model predicts.

**Classification of H3:** WOUNDED-BUT-STANDING as "first experimental transfer test on tool-executing LLM organizations"; DEAD if framed as a novel phenomenon; AT RISK empirically (nearest evidence is opposite-sign, and D&K's own backfire was "slight" — vs W2_statistics' requirement of a ≥40pp DiD for adequate power at n≈34/cell).

---

## 1. Search channels and their failures (method honesty)

| Channel | Status | Used for |
|---|---|---|
| arXiv abs pages (curl) | WORKED | Verification of all arXiv items below |
| arXiv export API | 429 (shared-IP budget exhausted by swarm) | — |
| arXiv search UI / listing pages | "no longer served from CIT web nodes" / empty | — |
| OpenReview search API (`api2/notes/search`) | WORKED | ~55 combinatorial queries (budget×verification, retry, metastable, congestion, containment×scarcity, oversight capacity, backfire, quarantine, degradation, anytime, metareasoning, …) |
| OpenReview note-detail/PDF | 403 challenge | blocked — abstracts via search endpoint only |
| Crossref API | WORKED (intermittent hiccups) | Classical + SSRN verification, bibliographic discovery |
| Semantic Scholar API | 429 except single-paper endpoint (worked twice, slow) | "Analyzing Metastable Failures" abstract |
| FetchURL | WORKED for sre.google | Google SRE Book ch. 22 full text |
| Zenodo API | rate-limited | Keel not re-verified this session (relies on W2_assassin_cand4's same-day verification) |

Raw query dumps: `audit2/raw_a4/` (or_*.json, q_*.xml, abs_*.html, cr_metastable.json, s2_*.json).

Prior reports read first: B16 (cost/reliability), B8 (human escalation), E4 (distsys assassin), E5 (classical MAS assassin), E6 (escalation assassin), W2_assassin_cand4 (recovery-cost), CtC full-text verification, FINAL_RECOMMENDATION, R1–R3, W3_reviewer4/5. Everything load-bearing below was independently re-verified against primary sources this session.

---

## 2. The sign-reversal pattern across communities — occupation map

### 2A. Classical MAS (the candidate's own anchor)

| Work | ID | The sign-reversal content | Verification |
|---|---|---|---|
| Dellarocas & Klein, "An Experimental Evaluation of Domain-Independent Fault Handling Services in Open Multi-Agent Systems" | ICMAS 2000, DOI 10.1109/ICMAS.2000.858440 | Citizen (sentinel EH) vs survivalist (timeout/retry) × {abundant, scarce subcontractors}: with short tasks + scarce subcontractors, **EH slightly worse than survivalist** — early detection increased competition for the bottleneck redeployment resource. Also the unzippering propagation result (600–700% completion-time inflation). | FULL TEXT VERIFIED (E5 read the MIT WP PDF via Wayback; S2 metadata re-verified this session: citationCount 57, CorpusId 6442794) |
| Kota, Gibbins & Jennings, ACM TAAS 2012 | DOI 10.1145/2168260.2168261 | Decentralized org self-adaptation with explicit reorganization-cost-vs-utility model | FULL TEXT VERIFIED (E5) — tradeoff frame, no scarcity sign reversal |
| Horling & Lesser JAAMAS 2007 | DOI 10.1007/s10458-007-9020-y | Queueing-model-based organizational design search | Metadata-verified (E5) |

**Assessment:** the candidate's H3 is explicitly a transfer test of D&K, so D&K is not a "collision" by construction — but it caps H3's novelty at *substrate transfer*, and R1's critique stands: the qualitative answer (backfire happens) is 26 years old; only magnitude/threshold/mechanism on LLM substrates can be news.

### 2B. Distributed systems / SRE — the pattern is textbook

| Work | ID | Sign-reversal content | Verification |
|---|---|---|---|
| Google SRE Book, ch. 22 "Addressing Cascading Failures" (Ulrich) | sre.google/sre-book/addressing-cascading-failures | Retries under overload reduce useful-work fraction, can melt down backends; "retry budgets" as containment; "system changes meant to reduce background errors … Retrying on failures, shifting load, killing unhealthy servers … might be implemented to improve the normal case, but can improve the chance of causing a large-scale failure." Footnote 110 literally assigns the reader: "write a simple simulator and see how the amount of useful work the backend can do varies with how much it's overloaded and how many retries are permitted." | FULL TEXT VERIFIED this session (fetched and quoted) |
| Bronson, Aghayev, Charapko, Zhu, "Metastable Failures in Distributed Systems" | HotOS 2021, DOI 10.1145/3458336.3465286 | Recovery mechanisms (retries, failover, autoscaling) as *sustaining* mechanisms that keep a system in degraded state after the trigger is removed — recovery consumes the scarce capacity | Crossref-verified metadata; concept well-established |
| Isaacs, Alvaro, Majumdar, Muniswamy-Reddy, Salamati, Soudjani, "Analyzing Metastable Failures" | HotOS 2025, DOI 10.1145/3713082.3730380 | "A metastable failure is a self-sustaining congestive collapse…"; queueing + simulation + emulation toolchain to predict vulnerability conditions | ABSTRACT VERIFIED (S2, this session) |
| MSF-Model (queueing analysis of metastable failures in replicated storage) | SRDS 2024, DOI 10.1109/SRDS64841.2024.00013 | Formal queueing model of the recovery-induced congestion | Crossref-verified metadata |
| **Mehan, "Retry Amplification in Distributed Systems: A Systematic Analysis of Retry Policies and Their Role in Cascading Failures"** | SSRN 2026, DOI 10.2139/ssrn.6313332 | **The most on-the-nose demonstrated sign reversal found:** "under correlated failure conditions, standard retry policies achieve 25% lower success rates than no-retry baselines (41.5% vs 55.4%), empirically demonstrating that naive retries can be counterproductive"; proposes Adaptive Retry Budgeting. 200-project analysis + simulation (n=100). | ABSTRACT ONLY (Crossref). Caveats: SSRN, single author, not peer-reviewed, simulation |
| Jacobson, "Congestion Avoidance and Control" | SIGCOMM 1988, DOI 10.1145/52325.52356 | Congestion collapse from retransmission — the original "recovery traffic destroys capacity" result | Crossref-verified metadata |
| Young 1974 / Daly 2006 checkpoint interval theory | DOI 10.1145/361147.361115 / 10.1016/j.future.2004.11.016 | Checkpointing (recovery prep) trades overhead vs lost rework — recovery cost as first-class optimization | Verified by B16 |
| Candea et al., "Microreboot — A Technique for Cheap Recovery" | OSDI 2004 | Cheap recovery enables recover-at-slightest-hint — the inverse design response to recovery cost | Verified by B16/E4 |

**Assessment:** in distributed systems, "recovery/containment helps under abundance, hurts under scarcity (overload)" is not a hypothesis — it is a named, taught, modeled phenomenon (retry storm, metastable failure, congestion collapse). This is the strongest *conceptual* collision with H3 and the fuel for the "just retry storms" review.

### 2C. Bounded rationality / metareasoning — the decision-theoretic root

| Work | ID | Content | Verification |
|---|---|---|---|
| Russell & Wefald, "Principles of metareasoning" | Artificial Intelligence 1991, DOI 10.1016/0004-3702(91)90015-C | Value of computation can be negative; deliberation must be traded against the cost of delay — the formal root of "verification/deliberation backfires under time scarcity" | Crossref-verified |
| Russell & Wefald, "Deliberation scheduling for problem solving in time-constrained environments" | AI Journal 1994, DOI 10.1016/0004-3702(94)90054-X | Deliberation scheduling under time constraints | Crossref-verified (title/venue) |
| Anytime algorithms line (Dean & Boddy 1988; Zilberstein) | — | Quality vs time profiles; interruptible computation | Found in Crossref search; not individually re-verified |

### 2D. Human-oversight capacity (LLM-agent era)

| Work | ID | Sign-reversal content | Verification |
|---|---|---|---|
| **"Oversight Has a Capacity: Calibrating Agent Guards to a Subjective, Fatiguing Human"** | arXiv:2606.08919, submitted 8 Jun 2026 | **The closest LLM-agent-era "more containment → less safety" result:** with an endogenous fatiguing reviewer, realized safety is an **inverted-U in escalation rate**; safety-optimal guard escalates *below* full escalation; flooding attack exploits the fatigued reviewer. Explicitly: "human attention is finite, and the guard's escalation policy spends it." | ABSTRACT VERIFIED (arXiv abs page, this session). Critical caveats from the abstract itself: (i) the inverted-U is a **modeling result** ("motivate a human study" — not run); (ii) single-agent action *gating* (prevention), not post-fault recovery; (iii) adversarial framing; (iv) authors disclaim mechanism novelty (cite FALCON, DeCCaF) |
| FALCON (fatigue-aware L2D as CMDP) | ICLR 2026 withdrawn (OpenReview) | Deferral under fatigue/budget constraints | Verified by B8 via OpenReview |
| DeCCaF (cost-sensitive L2D with workload constraints) | TMLR | Capacity-constrained deferral | Verified by B8 via OpenReview |
| READY or Not (Chatrath et al.) | arXiv:2609.02095, submitted 2 Sep 2026 | Minimum-cost oversight policy meeting a reliability target; 16 agent systems, 750 cases; oversight burden as deployment operating point. **Monotone framing: more review → more reliability at more cost; NO sign reversal** | ABSTRACT VERIFIED (arXiv abs page, this session) |
| AI Control (Greenblatt et al.) | arXiv:2312.06942, ICML 2024 | Audit budget traded against usefulness; safety monotone in audit budget | Verified by E6 |

### 2E. LLM(-MAS) budget×recovery experiments — the nearest neighbors point the other way

| Work | ID | What it shows about budget×recovery | Verification |
|---|---|---|---|
| **Self-Healing Agentic Orchestrators (Babu & Agrawal)** | arXiv:2606.01416, submitted 31 May 2026 | 100-task fault-injection benchmark; **matched recovery-budget sweep: targeted self-healing beats retry-only and full replanning AT EVERY TESTED BUDGET, with the LARGEST GAP AT THE TIGHTEST BUDGET** (one attempt: 94.0% vs 85.3%/88.2%). Verifier-guided recovery eliminates silent failures. | ABSTRACT VERIFIED (arXiv abs page, this session). **This is anti-H3 evidence in a tool-augmented LLM system: recovery helps most when budget is scarcest.** Single orchestrator, not organizational MAS |
| **FTDI: Budget-Aware Self-Healing for Resilient LLM Multi-Agent Code Generation (Men et al.)** | SSRN 2026, DOI 10.2139/ssrn.6387100 | **LLM MAS** fault injection; motivation: defenses "lack a budget-aware recovery loop, which results in many low-yield retries when interaction rounds and costs are constrained"; budget-gated triggering + tiered repair (cheap patch → deep repair → regeneration); "reducing the cost per unit recovery." Budget-awareness as *design response*; no sign reversal reported | ABSTRACT VERIFIED (Crossref, this session) |
| Keel, "The Economics of Recovery" | Zenodo 10.5281/zenodo.22754511 (2026-09-14) | Policy cost-frontier over {none, retry, reset, rollback, escalate, budget}; single-agent; no reversal reported | UNVERIFIED this session (Zenodo rate-limited); per W2_assassin_cand4 same-day verification |
| Anytime Verified Agents (AVA) | TMLR (OpenReview JMDCMf7mlF) | Dynamic allocation across search/sampling/verification under a user budget; "reduces cost at matched reliability thresholds" vs always-verify baselines. Monotone framing; abstract does not report always-verify dropping below no-verify | ABSTRACT VERIFIED (OpenReview search, this session) |
| Cost-of-Pass (Erol et al.) | arXiv:2504.13359 | "Performance-oriented methods with marginal performance gains [majority voting, self-refinement] rarely justify the costs" — recovery-flavored compute has measurable, sometimes-negative ROI; no fault dimension, no sign reversal | ABSTRACT VERIFIED (arXiv abs page, this session) |
| Should we be going MAD? | ICML 2024 Poster (OpenReview CrUmgUaAQp) | Multi-agent debate does not reliably beat self-consistency/ensembling at matched cost — collaboration overhead often not worth it | ABSTRACT VERIFIED (OpenReview, this session) |
| When More Thinking Hurts | ACL Findings 2026 (OpenReview 150bHJ0Vma) | Overthinking: extended reasoning abandons correct answers; optimal thinking length varies by difficulty — non-monotone in compute, but task-mediated not scarcity-mediated | ABSTRACT VERIFIED (OpenReview, this session) |
| LLMs Cannot Self-Correct Reasoning Yet | ICLR 2024 (OpenReview IkmD3fKBPQ) | Intrinsic self-correction can degrade performance | ABSTRACT VERIFIED (OpenReview, this session) |
| Cost-Aware Protocol Routing | arXiv:2608.14927, 14 Aug 2026 | When is extra collaboration worth its cost; routers over/under-escalate; no faults | ABSTRACT VERIFIED (arXiv abs page, this session) |
| VP-CONTROL (commit gates) | arXiv:2609.10969, 10 Sep 2026 | Cost-aware verification portfolios; matched-budget portfolios beat fixed verification policies; no reversal | ABSTRACT VERIFIED (arXiv abs page, this session) |
| Protocol-Preserving Context Trimming | arXiv:2609.16461, 15 Sep 2026 | Adaptive budget guardrails achieve 96.0% success with 56% token savings; context budgets ≤25% raise failure odds 10.92×. **Guardrails help under scarcity — opposite sign to H3** | ABSTRACT VERIFIED (arXiv abs page, this session) |
| Control Under Compression | arXiv:2608.01056, 2 Aug 2026 | Nonlinear reliability frontier as context budget shrinks (93.8% → 19.9% at 35% retained) — substrate scarcity degrades reliability, but no containment interaction | ABSTRACT VERIFIED (arXiv abs page, this session) |

### 2F. Negative results (searched, nothing found)

- OpenReview (~55 queries): no LLM(-MAS) paper demonstrating a containment/verification/recovery × budget sign reversal; no "retry storm" × LLM agent; no "metastable" × LLM agent; no "congestion" × LLM agent; no "containment backfires under scarcity" anything (only control-theory "containment control" and DB "query containment" homonyms).
- Crossref bibliographic search: "containment backfire scarcity", "recovery counterproductive" — nothing beyond §2B.
- The 48-report corpus (B16, W2_cand4, C1–C3 sweeps through 17 Sep 2026): no budget×containment interaction study in LLM-MAS.
- Channel caveat: arXiv full-text search and S2 search were down/429 this session; residual risk for very recent (Sep 2026) items is partially covered by C1's 7-day sweep (through ~17 Sep) and my OpenReview/Crossref queries, but a re-sweep before submission is mandatory.

---

## 3. The assigned question: "isn't this just retry storms applied to LLM agents?"

**Partially yes — and the paper's current design invites it. Here is the precise anatomy.**

### 3.1 Where the dismissal lands

The current scarcity operationalization (per W2_feasibility_A: "scarcity = one specialist role + rate-limited approval tool") is a **congestible-resource** regime. In that regime, the backfire mechanism — containment traffic (retries, re-delegation requests, approval requests) consuming the same scarce capacity as task progress, with positive feedback — *is* the retry-storm/metastable-failure mechanism, taught in the Google SRE Book with a simulator exercise as a footnote. If H3's demonstration reduces to "sentinel-triggered re-delegation storms a rate-limited tool," a systems-literate reviewer correctly says: known since Jacobson 1988, named since Netflix/SRE circa 2016, modeled since HotOS 2021, demonstrated counterproductive under correlated failure in SSRN 2026.

### 3.2 Where the dismissal fails — the four distinct backfire mechanisms

"Retry storms" names only ONE of at least four mechanisms by which containment can backfire under scarcity in LLM-MAS:

1. **Congestion feedback** (the retry-storm mechanism): containment actions consume a congestible shared resource (API rate limit, tool throughput, reviewer queue), delaying/throttling useful work, feeding back into more failures. Classical. Requires queueing coupling.
2. **Static budget partition** (no distsys analogue in this form): a per-run token/tool-call budget is *not* congestible — there is no feedback loop. Containment consuming c tokens simply leaves B−c for the task; the backfire is arithmetic, not dynamic. Whether the sign flips depends on the marginal utility of the last tokens vs the marginal fault-containment value — a *different* (and open) question than congestion. No classical result answers it for LLM workloads.
3. **Redeployment competition** (D&K's actual mechanism): early detection triggers re-bidding/re-delegation that competes for scarce *replacement capacity* (specialist agents). Organizational, not congestion.
4. **Detection-error interaction** (NO classical analogue at all): in distsys, fault signals are error codes/timeouts — detection is ~free and ~perfect. With semantic faults, detection itself spends budget (verifier LLM calls) and errs: false positives quarantine *healthy* work (destroying correct output under scarcity), false negatives admit propagation. The crossover point of the sign reversal depends on detector quality — a parameter no classical model has. CtC assigns semantic-fault detectability by construction; nobody has measured how detection error moves the backfire threshold.
5. (Human channel) **Reviewer fatigue/flooding**: escalation spends finite attention; inverted-U (2606.08919, modeling-only) — adjacent to alert-fatigue literature, not to retry storms.

A paper that demonstrates the backfire through mechanisms 2–5 (not just 1), and shows the crossover *threshold* shifts with detector quality and fault semantics, is not "retry storms applied to LLM agents." A paper that only demonstrates mechanism 1 is exactly that.

### 3.3 Why the adjacent literature has not made H3 obvious

Each adjacent community owns exactly one leg of the conjunction, and the legs currently *disagree*:

- Cost-of-pass / MAD / overthinking: recovery-flavored compute has poor marginal ROI (steady-state, no faults, no propagation).
- AVA / Self-Healing Orchestrators / FTDI / context-trimming guardrails: budget-aware recovery/verification **helps at all tested budgets, most at the tightest** (faults present, but single-orchestrator or code-gen, no organizational propagation, no shared congestible resource).
- Oversight-Has-a-Capacity / FALCON / DeCCaF: oversight backfires past a capacity threshold (human resource, single decision, modeling or classification only).
- D&K / retry storms / metastable failures: backfire under scarcity (crash faults / congestion, no semantics, no LLMs).

The conjunction — containment mechanism × scarcity × *propagating semantic faults* × *executing organizational LLM-MAS* — is empty on every channel searched. And because the nearest LLM-era evidence (2E) is opposite-sign, a reviewer cannot claim the LLM-MAS result is obvious from adjacent literature; they can only claim the *mechanism* is classical. That is a positioning problem, not a novelty kill.

---

## 4. Collision classification for claims in this lane

| Claim | Classification | Basis |
|---|---|---|
| "Containment can backfire under resource scarcity" as a phenomenon | **DEAD (classical, multiply occupied)** | D&K ICMAS 2000 (FULL TEXT); Google SRE Book ch.22 (FULL TEXT); metastable-failure line HotOS 2021/2025, SRDS 2024; Retry Amplification SSRN 2026 (ABSTRACT); Russell & Wefald 1991; Oversight-Has-a-Capacity inverted-U (ABSTRACT, modeling) |
| "First demonstration of the sign reversal in LLM agents" | **SURVIVES** (as of 21 Sep 2026) | §2E nearest items are opposite-sign (2606.01416), design-level (FTDI), monotone (READY, AVA), or modeling-only/single-agent/adversarial (2606.08919). No LLM-MAS fault-recovery × scarcity interaction found |
| "First experimental transfer test of D&K scarcity-backfire on tool-executing LLM orgs" | **SURVIVES but fragile** | The qualitative answer is 26 years old and textbook in distsys; contribution must be magnitude/threshold/mechanism shifts under semantic faults (§3.2), not the existence of the backfire |
| H3 as the paper's *most promising* hypothesis | **AT RISK** | (i) nearest adjacent experiment is opposite-sign; (ii) D&K's own backfire was "slightly worse" — a small effect vs W2_statistics' ≥40pp DiD power requirement at feasible n; (iii) if scarcity is operationalized as a rate-limited tool only, the result is congestion folklore re-measured |
| H2 (containment reduces propagation but imposes cost) | **OCCUPIED in pieces, unoccupied in conjunction** | Cost axis: Keel/ToolMaze/FTDI/MTTR-A/READY (W2_cand4). Propagation-reduction: CtC (simulation), TAO (rejected), 2408.00989 (no cost). No work joins cost × propagation × mechanism comparison in org LLM-MAS |

---

## 5. Recommendations to the orchestrator (adversarial, actionable)

1. **Do not let H3 be the headline as a "discovery."** Frame it strictly as a pre-registered transfer test whose interest is the *crossover location and mechanism*, with the opposite-sign LLM-era evidence (2606.01416) cited as the reason the outcome is genuinely uncertain. This converts the biggest threat into the motivation.
2. **Force the non-congestion channels into the design.** If scarcity = rate-limited tool only, the "retry storms" review lands. Add at least one non-congestible scarcity channel (hard per-run token budget) and report the false-positive-quarantine effect (mechanism 4) — the one backfire channel with no classical analogue and no occupied prior art.
3. **Cite the distsys line head-on** (SRE Book ch.22, Bronson 2021, Isaacs 2025, Mehan SSRN 2026, Jacobson 1988) and state explicitly which mechanisms are and aren't congestion. Reviewers with systems backgrounds *will* know this literature; silence reads as ignorance.
4. **Power check against the classical effect size.** D&K's backfire was "slight." If the pre-registration requires ≥40pp DiD (W2_statistics), state what a small-but-real crossover means for the claim — otherwise H3 risks a null that looks like a failed replication rather than a boundary condition.
5. **Re-sweep before submission.** arXiv search/API and S2 were degraded this session; Sep-2026 items (VP-CONTROL, context-trimming guardrails, READY) show this lane is being actively colonized.

## 6. Verification ledger (this session)

- FULL TEXT: Google SRE Book ch. 22 (fetched, quoted); D&K ICMAS 2000 (E5's full-text read, metadata re-verified via S2: CorpusId 6442794).
- ABSTRACT VERIFIED (primary source fetched this session): arXiv:2606.08919 (8 Jun 2026), 2609.02095 (2 Sep 2026), 2606.01416 (31 May 2026), 2504.13359, 2609.10969 (10 Sep 2026), 2608.14927 (14 Aug 2026), 2608.01056 (2 Aug 2026), 2609.16461 (15 Sep 2026); Crossref abstracts: FTDI (10.2139/ssrn.6387100), Retry Amplification (10.2139/ssrn.6313332); S2 abstract: Analyzing Metastable Failures (10.1145/3713082.3730380); OpenReview abstracts: AVA (TMLR), Should-we-be-going-MAD (ICML 2024), When-More-Thinking-Hurts (ACL Findings 2026), LLMs-Cannot-Self-Correct (ICLR 2024), AgentBalance (ARR 2026), AGENT* (ICLR 2026 sub), Rational Metareasoning (NeurIPS 2024 WS).
- METADATA VERIFIED (Crossref): 10.1145/3458336.3465286, 10.1145/52325.52356, 10.1109/SRDS64841.2024.00013, 10.1016/0004-3702(91)90015-C, 10.1016/0004-3702(94)90054-X.
- UNVERIFIED this session (relies on same-day swarm verification): Keel (Zenodo rate-limited); FALCON/DeCCaF (B8's OpenReview records).
- FAILED CHANNELS: arXiv export API (429), arXiv search UI (not served), S2 search endpoint (429), OpenAlex (budget exhausted), Zenodo API (rate-limited), OpenReview note-detail (403 challenge).
