# AUDIT2 — AGENT 6: DISTRIBUTED SYSTEMS / RELIABILITY SPECIALIST

**Date:** 2026-09-21
**Lane question:** Is H3's mechanism — "recovery/containment actions consume scarce resources and thereby worsen failure (sign reversal under scarcity)" — already a well-established phenomenon in distributed systems with a trivial mapping, thereby weakening the candidate paper's conceptual novelty?
**Candidate claim under attack:** "first experimental transfer test of classical MAS fault-handling results (Dellarocas & Klein sentinels, delegation-depth cost inflation, scarcity sign reversal) on tool-executing LLM agent organizations with semantic faults." H3: containment BACKFIRES under resource scarcity (token/tool/latency/reviewer budgets).

---

## 1. BOTTOM LINE

**YES — H3's mechanism is textbook-level established in distributed systems, and the mapping to LLM-MAS is close to trivial.** The exact phenomenon — recovery traffic consuming scarce capacity and thereby sustaining or worsening the failure it was meant to fix, with a sign reversal between abundance and scarcity — is the core of the **metastable-failures** literature (Bronson et al., HotOS 2021; Huang et al., OSDI 2022; Isaacs et al., HotOS 2025), the **retry-storm / congestion-collapse** canon (Jacobson 1988; Google SRE Book ch. 22), and is already demonstrated empirically with an explicit sign reversal (retries *worse* than no-retry under stress) in a 2026 distsys preprint (Mehan, SSRN). The distsys field also already owns the standard mitigations H3's framing implies (retry budgets, backoff+jitter, circuit breakers, load shedding, admission control).

**However, this does not deliver a clean kill of the paper**, for two reasons: (a) the candidate openly frames H3 as a *transfer test* of Dellarocas & Klein ICMAS 2000 (which itself contains the scarcity backfire — verified by E5 from the full text), so the conceptual ancestry is acknowledged, not disguised; (b) no LLM-MAS work found demonstrates the sign reversal in task utility on real executions — the nearest LLM-side budget sweeps (Babu 2606.01416; FTDI SSRN 6387100) found *monotone* dominance of budgeted recovery, i.e., the crossover did NOT appear where it was looked for. The conceptual novelty of H3 is weak; the *empirical* novelty (does the reversal actually occur for semantic-fault containment on token/context budgets?) survives but is fragile.

**What the paper must show to be more than "retry storms / metastable failures applied to agents":** a reversal mechanism with no trivial distsys analogue. The strongest candidate is the **context-window coupling**: in LLM MAS, recovery traffic (retries, verifier debates, re-delegation messages) is appended to the same context window that carries task state, and long-context degradation (Lost in the Middle, TACL 2023, verified) means recovery actions degrade the *medium of computation itself* — a "capacity shrinks as recovery load grows" amplifier that has no clean queueing-theory analogue. If the paper demonstrates the sign reversal *via* context degradation or semantic false-positive quarantine (verifier false positives removing healthy capacity — analogous to false-positive failover, a known metastable trigger), it contributes beyond relabeling. If the reversal is driven purely by token-budget exhaustion, it is metastable-failure theory with tokens substituted for CPU, and a distsys-literate reviewer will say so.

---

## 2. METHOD

Sources queried 2026-09-21: Crossref REST API (primary; worked throughout), Semantic Scholar Graph API (spaced single calls; intermittent 429), OpenReview API v2 search, DataCite API, arXiv abstract pages via direct fetch, USENIX proceedings pages, Google SRE Book online, author blog (charap.co) for the HotOS 2021 mechanism detail. OpenAlex daily budget was exhausted (shared IP); arXiv export API returned empty/429 from this host; ACM DL PDFs 403. Prior reports read first: E4 (distsys assassin), E2 (containment assassin), B16 (cost/reliability), E5 (classical MAS), CtC full-text verification, R1/R3/W2-cand2 for H3 framing. Every load-bearing item below was verified against a primary record (abstract page, Crossref metadata, publisher page, or full text); nothing rests on search snippets.

---

## 3. PHENOMENON-BY-PHENOMENON: IS EACH CONCEPTUALLY IDENTICAL TO H3?

### 3.1 Metastable failures — the strongest collision. CONCEPTUALLY IDENTICAL, including the sign reversal.

| Item | Identifier | Verification |
|---|---|---|
| Bronson, Aghayev, Charapko, Zhu, "Metastable Failures in Distributed Systems," HotOS 2021, pp. 221–227 | DOI 10.1145/3458336.3465286 | **PARTIALLY VERIFIED** — abstract via Semantic Scholar; Crossref metadata (venue, pages, June 2021); full mechanism detail via lead-author's technical blog post (charap.co, May 2021), which walks through the paper's framework and canonical example. ACM PDF itself 403 from this network. |
| Huang, Magnusson, Muralikrishna, Estyak, Isaacs, Aghayev, Zhu, Charapko, "Metastable Failures in the Wild," OSDI 2022, pp. 73–90 | usenix.org/conference/osdi22/presentation/huang-lexiang | **FULL TEXT VERIFIED** (abstract + full bibtex from USENIX page; findings quoted below). |
| Isaacs, Alvaro, Majumdar, et al., "Analyzing Metastable Failures," HotOS 2025 | DOI 10.1145/3713082.3730380 | **ABSTRACT ONLY** (Semantic Scholar; Crossref metadata confirms venue/date 2025-05-14). |
| MSF-Model: Queuing-Based Analysis and Prediction of Metastable Failures in Replicated Storage Systems, SRDS 2024 | DOI 10.1109/srds64841.2024.00013 | **METADATA VERIFIED** (Crossref; 7 citations). |

**The mechanism, as stated by the authors (HotOS 2021, via author's blog):** a trigger (transient) pushes a high-utilization system into overload; a **sustaining effect** — canonically *retries*, the recovery mechanism — creates a positive feedback loop that generates more load than the trigger did; when the trigger is removed, the system does not recover. Their worked example: web app at 280 QPS against a 300 QPS database; a seconds-long network glitch causes retries, doubling effective load to 560 QPS; the system stays failed indefinitely until offered load drops below 150 QPS **or the retry policy is changed/suspended**. Crucially: *the same retry policy is harmless at low utilization and catastrophic at high utilization* — the paper's "stable" vs "metastable vulnerable" state distinction is exactly H3's abundance/scarcity sign reversal, with utilization = resource scarcity.

**OSDI 2022 (in the wild):** 22 in-depth metastable failures from 11 organizations; **at least 4 of 15 major AWS outages of the last decade were metastable failures**; two trigger types and two amplification mechanisms taxonomized; reproduced in controlled environments. This is not a curiosity — it is a named, measured, industrially dominant failure class.

**Mapping to H3:** token/tool/latency budget ↔ serving capacity; containment mechanism (retry, verifier gate, re-delegation, sentinel polling) ↔ retry/failover/health-check traffic; scarcity ↔ high utilization; "containment backfires under scarcity" ↔ "sustaining effect activates in the metastable-vulnerable state." The mapping is one-to-one at the mechanism level. **What differs:** the *resource* semantics (tokens/context/attention vs CPU/queue), the *fault* semantics (semantic vs crash/timeout), and the *organization* (delegation structure vs service graph). Those differences are real but are substrate swaps, not new mechanisms — unless the paper shows the substrate changes the qualitative behavior (see §5).

### 3.2 Retry storms / retry amplification — CONCEPTUALLY IDENTICAL (the named, operationalized version).

| Item | Identifier | Verification |
|---|---|---|
| Google SRE Book, ch. 22 "Addressing Cascading Failures" (Mike Ulrich), O'Reilly 2016 | sre.google/sre-book/addressing-cascading-failures | **FULL TEXT VERIFIED** (fetched complete chapter). Cascading failure defined as "failure that grows over time as a result of positive feedback"; overload named the most common cause; retry amplification explicit, incl. the exercise "write a simple simulator and see how the amount of useful work the backend can do varies with how much it's overloaded and how many retries are permitted." |
| Mehan, "Retry Amplification in Distributed Systems: A Systematic Analysis of Retry Policies and Their Role in Cascading Failures," SSRN 2026 | DOI 10.2139/ssrn.6313332 | **ABSTRACT VERIFIED** (Crossref). Single author, 0 citations, simulation n=100 — weak venue, but the finding is the point: defines a Retry Amplification Factor; analyzes 200 open-source microservice projects (60.9% of retry implementations lack backoff, 4.9% have jitter); **under correlated failure, standard retries achieve 25% LOWER success than no-retry (41.5% vs 55.4%)** — an explicit empirical sign reversal of a recovery mechanism under stress; proposes Adaptive Retry Budgeting. |

**Assessment:** "recovery actions consume scarce resources and worsen failure" is not just known — it has a named metric (RAF), design guidelines, and a demonstrated crossover against a no-recovery baseline. H3's token-budget version is this with a different currency.

### 3.3 Congestion collapse — CONCEPTUALLY IDENTICAL at the mechanism level (network-layer ancestor).

Jacobson, "Congestion Avoidance and Control," SIGCOMM 1988, DOI 10.1145/52324.52356 — **METADATA VERIFIED** (Crossref; 2,320 citations). Congestion collapse = goodput crashes under load because the network spends capacity retransmitting (recovery traffic) instead of delivering; the fix (backing off under scarcity) is the original "recovery must consume less when resources are scarce" result. H3 is a descendant idea.

### 3.4 Checkpoint overhead (Young 1974, Daly 2006) — RELATED BUT NOT IDENTICAL (cost trade-off, no backfire).

Young, CACM 1974, DOI 10.1145/361147.361115 (491 cites); Daly, FGCS 2006, DOI 10.1016/j.future.2004.11.016 (359 cites) — both **METADATA VERIFIED** (Crossref). These establish that a recovery mechanism (checkpointing) consumes resources and must be optimized against expected lost work. But the trade-off is a monotone optimization — checkpointing never makes things *worse than not checkpointing* in these models; there is no sign reversal. Relevant as recovery-cost theory the paper should cite; not a collision with H3's backfire claim.

### 3.5 Microreboot / recovery-oriented computing / crash-only — INVERSE DIRECTION (making recovery cheap), not a collision.

Candea et al., "Microreboot — A Technique for Cheap Recovery," OSDI 2004; Patterson et al., ROC tech report UCB/CSD-02-1175, 2002; Candea & Fox, "Crash-Only Software," HotOS 2003 — all verified by E4 (USENIX pages, TR PDF). ROC's program is precisely "make recovery cheap enough to do early and often" — i.e., the field recognized recovery cost as the binding constraint 24 years ago and engineered it down. Supports the paper's framing (recovery cost is first-class) while also showing the *question* is old.

### 3.6 Circuit breakers, bulkheads, retry budgets, load shedding — the MITIGATION side is also occupied.

Nygard, "Release It!" (circuit breaker); Hystrix (Netflix 2012, verified by E4); SRE-book retry budgets and client-side throttling. A distsys reviewer will note that H3's implied design conclusion ("under scarcity, contain less / gate recovery on budget") is the standard operating doctrine: retry budgets exist precisely because recovery consumes scarce capacity. FTDI (below) has already imported "budget-gated recovery" into LLM MAS.

### 3.7 LDFI (Lineage-Driven Fault Injection) — orthogonal method, verified by E4 (Alvaro et al., SIGMOD 2015, DOI 10.1145/2723372.2723711). Not about recovery cost; no H3 collision.

### 3.8 Alert/intervention fatigue (the "reviewer budget" component of H3) — ESTABLISHED in security operations.

H3's "reviewer budgets" arm maps onto alert fatigue in SOCs: verification/escalation consumes finite analyst attention, and under alarm floods the oversight mechanism itself degrades. Verified anchors: "Combating Alert Fatigue in the Security Operations Centre" (SSRN 2023, DOI 10.2139/ssrn.4633965, 6 cites); "Cognitive Alert Triage: A Fuzzy-Logic SOAR Framework for Reducing Analyst Fatigue" (SSRN 2026, DOI 10.2139/ssrn.6703558); "Reducing Alert Fatigue in Cloud Operations" (TechRxiv 2025, DOI 10.36227/techrxiv.176765375.53124342/v1) — all **METADATA VERIFIED** via Crossref. The human-oversight-scarcity backfire is its own established literature; the paper's "priced human escalation" arm should cite it.

### 3.9 Watchdog/monitoring overhead — established practitioner knowledge; no single canonical paper needed. (Observer overhead in profiling/tracing; health-check traffic as load. Not load-bearing for H3.)

---

## 4. LLM-SIDE OCCUPANTS: HOW CLOSE IS THE TRANSFER ALREADY?

| Paper | ID / venue | Verification | Relation to H3 |
|---|---|---|---|
| **Halverson, "Economic Integrity in Production LLM Pipelines: Measuring Attempt Amplification, Discarded Reasoning, and Retry Cost," SSRN 2026** | DOI 10.2139/ssrn.7270819 | **ABSTRACT VERIFIED** (Crossref) | **Closest LLM-side occupant of H3's cost mechanism.** Defines Inference Amplification Factor (physical attempts per logical job — the LLM-pipeline RAF) and Economic Contamination Index; budget×retry ablation (n=10/cell): retry-based recovery reaches an *equivalent scoreboard* at IAF up to 1.70 and ECI up to 1.96 — i.e., recovery works but consumes up to ~2× budget, with 48.9% of one layer's spend buying discarded output. Proactive budget headroom prevents starvation with zero amplification. Single-author SSRN, one provider, one night — weak empirics, but the *conceptual occupation* (recovery consumes LLM budget; measure it per-attempt) is real and 2026. |
| **Halverson, "When the Model Isn't the Problem: Degradation Accounting in Fallback-Enabled Production LLM Pipelines," SSRN 2026** | DOI 10.2139/ssrn.7265602 | **ABSTRACT VERIFIED** (Crossref) | Companion study: reasoning-budget exhaustion and "adversarial-layer starvation" as named failure classes; pre-registered budget-and-retry bundle raised agent-clean rate 4/10→10/10; reactive retry recovered 95/96 starvation events "at the cost of 96 additional retry attempts." Directly prices recovery in attempts. |
| **Babu, "Self-Healing Agentic Orchestrators…," May 2026** | arXiv 2606.01416 (v1 2026-05-31) | **ABSTRACT VERIFIED** (arXiv page) | Bounded-budget recovery control; **matched recovery-budget sweep**: self-healing beats retry-only and full-replanning *at every tested budget* (largest gap at a single recovery attempt: 94.0% vs 85.3%/88.2%). **No sign reversal found where one was directly looked for** — evidence that the crossover is not automatic in LLM systems; the candidate must explain why its setting differs. |
| **FTDI: Budget-Aware Self-Healing Framework for Resilient LLM Multi-Agent Code Generation, SSRN 2026** | DOI 10.2139/ssrn.6387100 | **ABSTRACT VERIFIED** (Crossref) | Explicitly motivated by H3's problem: defenses "lack a budget-aware recovery loop, which results in many low-yield retries when interaction rounds and costs are constrained." Budget-gated triggering + tiered repair (cheap patch → deep repair → regeneration). MAS setting, fault injection, but demonstrates *efficient* recovery, not a backfire crossover. |
| **FlowGuard: Slack-Aware Overload Control for Multi-Agent LLM Serving, ICCCN 2026** | DOI 10.1109/icccn69946.2026.11662939 | **ABSTRACT VERIFIED** (Semantic Scholar; Crossref metadata) | Overload control for *multi-agent LLM serving* (shared GPU backends, BurstGPT load): under sustained overload, GPU cycles on already-violated-SLO requests are wasted; slack-aware prioritization cuts miss rates 14–38pp. Proof that overload/scarcity dynamics of multi-agent LLM systems are being studied at the serving layer in 2026 — different layer (infrastructure, not organizational fault recovery), but the paper must not claim "first to study resource scarcity in multi-agent LLM systems" simpliciter. |
| Smit et al., "Should we be going MAD?," Nov 2023 | arXiv 2311.17371 | **ABSTRACT VERIFIED** | Multi-agent debate (a verification/redundancy mechanism) benchmarked on cost-time-accuracy; does not reliably beat cheaper prompting. Steady-state cost-benefit, not fault recovery. |
| Huang et al., "Large Language Models Cannot Self-Correct Reasoning Yet," ICLR 2024 | arXiv 2310.01798 | **ABSTRACT VERIFIED** | Self-correction (a recovery mechanism) can *degrade* performance — a backfire, but capability-driven, not scarcity-driven. |
| CtC (ICERA 2026) | DOI 10.1109/ICERA72709.2026.11666599 | **FULL TEXT VERIFIED** (by prior wave) | **No scarcity condition anywhere** (confirmed by CtC_fulltext_verification.md). The nearest neighbor does not touch H3. |
| Resilience of LLM-MAS w/ Faulty Agents | arXiv 2408.00989 | full-text checked by B16 | Recovery mechanisms evaluated on effectiveness only; zero cost/budget analysis. |

**Net:** no LLM-MAS paper demonstrates the scarcity sign reversal in task utility. The cost side of H3 (recovery consumes budget) is now occupied in LLM pipelines (Halverson ×2, FTDI, Babu); the *reversal* side is open but was looked for and not found by Babu.

---

## 5. WHAT AN LLM-MAS PAPER MUST SHOW TO BE MORE THAN "RETRY STORMS / METASTABLE FAILURES APPLIED TO AGENTS"

1. **A non-trivial mechanism for the reversal.** If scarcity = token budget and the reversal is "verifier tokens crowd out task tokens," that is resource competition — the trivial mapping. Non-trivial versions: (a) **context-window coupling** — recovery traffic lengthens contexts, and long-context degradation (Lost in the Middle, arXiv 2307.03172, TACL 2023, ABSTRACT VERIFIED) means recovery *reduces the system's effective capacity*, a load-dependent service-rate amplifier with no clean queueing analogue; (b) **semantic false-positive quarantine** — verifier false positives remove healthy agents/capacity, the analogue of false-positive failover (a documented metastable trigger), but with *semantic* error rates that classical theory doesn't model; (c) **correlated recovery failure** — verifier and primary share a foundation model, so recovery fails exactly when needed (correlation breaks the independence assumption of redundancy, per E4 §6.2).
2. **The reversal in task utility, not just cost.** Babu's monotone result (budgeted self-healing dominates at every budget) is the standing contrary evidence; the paper must produce the crossover on real LLM executions and characterize the boundary (which resource, which mechanism, which utilization).
3. **A mapping justification, not assertion.** R1 (W3) already flagged that "scarcity of subcontractors → scarcity of tokens" is asserted, not justified. The distsys literature supplies the correct formal frame (stable vs metastable-vulnerable states; sustaining-effect taxonomy from OSDI 2022); using it explicitly converts "relabeling" into "transfer test with theory."
4. **Differentiation from the serving-layer scarcity literature** (FlowGuard) and the pipeline-economics literature (Halverson) — different layers, but a reviewer will conflate them if the paper's scarcity claim is unscoped.

---

## 6. COLLISION CLASSIFICATION FOR CLAIMS IN MY LANE

- **H3 mechanism ("recovery consumes scarce resources and can worsen failure"): CONCEPTUALLY OCCUPIED — trivial mapping from distsys.** Metastable failures (HotOS 2021 / OSDI 2022 / HotOS 2025), retry storms (SRE canon; RAF metric + empirical sign reversal, SSRN 2026), congestion collapse (1988). Also occupied in classical MAS by the candidate's own anchor (Dellarocas & Klein ICMAS 2000, scarcity backfire — full-text verified by E5). Classification: **fatal to any "we discover/introduce this phenomenon" framing; non-fatal to an honestly-scoped transfer test.**
- **H3 as an empirical LLM-MAS result (sign reversal in task utility under token/context/tool/reviewer scarcity, real executions): NOT OCCUPIED, but fragile.** CtC has no scarcity arm; Babu found no reversal; FTDI/Halverson occupy the cost-measurement side. Classification: **surviving gap, moderate strength.**
- **H2 (containment reduces propagation at a cost): OCCUPIED at the mechanism level** (CtC fail-safe/fail-operational ablation; circuit breakers; checkpoint cost theory Young/Daly; Babu/FTDI budget sweeps). The cost-*priced* comparison in organizational LLM MAS remains open (B16's verdict stands).
- **H1 (delegation depth changes propagation/recovery cost): outside my lane's core, but note** the distsys analogue (hop-count amplification of retries through layered load balancers; SRE-book cascading-failure depth) makes the *qualitative* claim unsurprising to a distsys reviewer; novelty must rest on magnitude/semantic-fault interaction.
- **Overall framing ("first experimental transfer test … with semantic faults"): survives my lane** — no distsys or LLM paper found that transfers metastable-failure/retry-storm theory onto semantic-fault containment in LLM organizations. But the transfer must be *to the theory* (metastability, sustaining effects), not just to Dellarocas & Klein, or the paper misses the closest scientific frame and invites the relabeling verdict.

## 7. UNEXPECTED FINDING

The **Halverson pair** (SSRN 7270819 + 7265602, 2026): a single-author production-pipeline study that has already built the LLM-native version of retry-amplification measurement (IAF = physical attempts per logical job; ECI = spend on discarded outputs; per-attempt economic ledger at the HTTP boundary), with a pre-registered budget×retry ablation showing recovery at ~2× hidden cost and "reasoning-budget exhaustion" as a named starvation mode. It is empirically weak (n=10, one provider, one night) and will likely be ignored — but it occupies the "recovery consumes LLM budget, measured per-attempt" territory in 2026, and its IAF is literally the distsys Retry Amplification Factor re-derived for LLM pipelines. The candidate paper should cite it (or be prepared for a reviewer who does) and must go beyond it: organizational structure, propagation, and the utility crossover are all absent from it.

## 8. VERIFICATION LOG

- Verified via Crossref metadata: 10.1145/3458336.3465286 (HotOS 2021); 10.1145/3713082.3730380 (HotOS 2025); 10.1109/srds64841.2024.00013 (MSF-Model); 10.2139/ssrn.6313332 (Retry Amplification 2026); 10.1145/361147.361115 (Young 1974); 10.1016/j.future.2004.11.016 (Daly 2006); 10.1145/52324.52356 (Jacobson 1988); 10.2139/ssrn.7270819 and 10.2139/ssrn.7265602 (Halverson pair); 10.2139/ssrn.6387100 (FTDI); 10.1109/icccn69946.2026.11662939 (FlowGuard); 10.2139/ssrn.4633965, 10.2139/ssrn.6703558, 10.36227/techrxiv.176765375.53124342/v1 (alert fatigue).
- Verified via Semantic Scholar abstract: HotOS 2021 (CorpusId 235310364); HotOS 2025 "Analyzing Metastable Failures"; FlowGuard.
- Verified via USENIX page (full abstract + bibtex): OSDI 2022 "Metastable Failures in the Wild" (pp. 73–90).
- Verified via arXiv abstract pages: 2606.01416 (Babu), 2311.17371 (MAD), 2310.01798 (self-correction), 2307.03172 (Lost in the Middle).
- Verified via full text: Google SRE Book ch. 22 (sre.google); charap.co author blog detailing the HotOS 2021 framework and canonical retry example.
- Blocked/unavailable from this network: ACM DL PDFs (403), OpenAlex (budget exhausted), arXiv export API (empty/429), DBLP (Anubis). OpenReview note-fetch for "Formal Analysis of Metastable Failures in Software Systems" (search hit uT2ujQ7vaU) returned no content — **UNVERIFIED, not cited as evidence**.
- Prior reports relied upon (independently spot-checked where load-bearing): E4 (distsys classics), E5 (D&K 2000 scarcity backfire, full-text), B16 (2408.00989 no-cost-analysis, full-text), CtC full-text verification (no scarcity condition).
