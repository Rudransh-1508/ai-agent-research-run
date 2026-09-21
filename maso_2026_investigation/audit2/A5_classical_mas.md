# A5 — Classical MAS Theory Specialist: Actual Predictions, Theorems, and Experimental Conditions

**Investigator:** AGENT 5 (Classical MAS Theory)
**Date:** 2026-09-21
**Mission:** Extract the ACTUAL predictions/theorems/results (not citations) from classical MAS fault-handling and organizational theory that could be experimentally transferred to LLM-MAS; search classical MAS for resource-scarcity × fault-handling interactions beyond Dellarocas & Klein. Adversarial goal: disprove the candidate paper's novelty.
**Started from:** report E5 (`reports/E5_assassin_classical_mas.md`); every load-bearing claim below was independently re-verified against primary sources on 2026-09-21.

---

## 1. Bottom line

**All three surviving hypotheses (H1, H2, H3) have exact classical antecedents with stated predictions, demonstrated experimental conditions, and known parameter dependencies. H3 — the candidate's "most promising" hypothesis — is the most thoroughly anticipated: the sign reversal of containment value under resource scarcity was demonstrated in classical MAS simulation at least twice, with two different mechanisms, in 2000 and 2012, and a third closely related result (verification-communication cost causing mission failure at scale) in 1997.**

What survives is only the substrate transfer: no classical work used LLM agents, natural-language messages, learned memory, or tool execution, and classical detection of faults was effectively perfect (crash faults), so detection quality was never an experimental factor. Even that is narrower than the candidate's current claim, because the classical record *conceptually* anticipated semantic/information faults (Klein & Dellarocas CSCW 2000 "garbled data" provenance-rollback strategy; Carley & Lin 1997 organizational performance under information distortion; the trust/reputation literature).

---

## 2. Verification log

Full texts obtained and read (all local copies in `maso_2026_investigation/raw/r3_review/`):

| Paper | Source used | Status |
|---|---|---|
| Dellarocas & Klein, ICMAS 2000 (10.1109/ICMAS.2000.858440) | MIT CCS WP #212 / SWP #4116 PDF via Wayback of MIT DSpace (handle 1721.1/2770); `dk_icmas2000.txt` | **FULL TEXT VERIFIED** (abstract, CNET model, EH services, experiments, results, related work, future work all read) |
| Klein & Dellarocas, CSCW 2000 (10.1023/A:1008759413689) | MIT CCS WP #203 (April 1998) full text, pre-archived `kd_cscw2000.txt` | **FULL TEXT VERIFIED** (WP version of the journal article) |
| Klein, Rodríguez-Aguilar & Dellarocas, JAAMAS 2003 (10.1023/A:1024145408578) | Crossref metadata; companion framing paper CCS WP #211 / SWP #4115 ("Domain-Independent Exception Handling Services That Increase Robustness in Open MAS", Klein & Dellarocas, May 2000) fetched live from MIT DSpace (handle 1721.1/2769) and read | **PARTIALLY VERIFIED** (journal article itself not retrieved; it is the journal extension of the ICMAS 2000 experiments, whose full text I read; WP #211 read in full) |
| Hägg 1997 (10.1007/BFb0030090) | BTH DiVA full-text PDF (diva2:833731) via Wayback; `hagg1997.txt` | **FULL TEXT VERIFIED** |
| Horling & Lesser, KER 2004 (10.1017/S0269888905000317) | Crossref abstract | **ABSTRACT ONLY** (full text not retrievable: Cambridge blocked, CiteSeerX/ScholarWorks copies dead) |
| Kota, Gibbins & Jennings, ACM TAAS 2012 (10.1145/2168260.2168261) | Southampton ePrints full 36-page PDF; `kota_taas2012.txt` | **FULL TEXT VERIFIED** (abstract, model, utility equations, experimental setup, results read) |
| Tambe, JAIR 1997 (10.1613/jair.433) | arXiv cs/9709101 full PDF (JAIR version has broken font encoding; arXiv copy extracted cleanly); `tambe_arxiv.txt` | **FULL TEXT VERIFIED** |
| Kaminka & Tambe, JAIR 2000 (10.1613/jair.682) | JAIR open-access PDF; `kaminka_jair2000.txt` | **FULL TEXT VERIFIED** (theorems, proofs sketch, ModSAF/RoboCup experiments read) |
| Baldoni et al., JAAMAS 2022/2023 (10.1007/s10458-022-09590-6) | Crossref metadata + S2 TLDR | **TLDR/ABSTRACT-LEVEL ONLY** (Springer blocked; no arXiv preprint found) |

Additional items verified during the scarcity sweep: Stanković, Štula & Maras JAAMAS 2015 (10.1007/s10458-015-9320-6, TLDR via S2); Baldoni, Baroglio, Micalizio & Tedeschi KER 2025 (10.1017/S0269888925000050, abstract via Crossref); Carley & Lin Management Science 1997 (10.1287/mnsc.43.7.976, metadata); Lin & Carley "Designing Stress Resistant Organizations" 2003 (10.1007/978-1-4757-3703-5, metadata); Muthitacharoen MIT thesis 2000 (DSpace 1721.1/86529, metadata); Aryananda MIT thesis (DSpace 1721.1/9437, metadata). All DOIs resolved via Crossref on 2026-09-21.

API constraints encountered: OpenAlex daily budget exhausted (shared IP); S2 intermittent 429; Springer/Cambridge bot-walled. All critical claims routed around via Crossref, MIT DSpace REST API, BTH DiVA, JAIR, arXiv, and Wayback.

---

## 3. Paper-by-paper: exact predictions, conditions, parameter dependencies

### 3.1 Dellarocas & Klein, ICMAS 2000 — the central exhibit (FULL TEXT VERIFIED)

**Exact predictions (stated in §4, "The Experiments"):**
- Central hypothesis: "citizen" agents supported by domain-independent exception-handling (EH) services will have significantly lower mean contract completion time under failures than "survivalist" (timeout/retry) agents, and lower overall system effort (less wasted work on orphaned tasks).
- Sub-hypothesis 1 (depth): "tasks that have deep task decompositions should benefit more because in those cases the unzippering effect will be more severe with survivalist agents."
- Sub-hypothesis 2 (task length): "Task decompositions with long duration tasks should benefit more because the quicker agent death detection offered by polling saves more time in absolute terms."

**The "unzippering effect" (defined §2):** death of an agent performing a subtask causes cascading timeouts and retries for its customers, the customers of its customers, "all the way up to the CNET agent at the top of the task decomposition tree." This is the delegation-depth amplification prediction underlying H1 — stated, named, and measured in 2000.

**Experimental conditions:** discrete-event MAS simulator on Swarm; Contract Net (Smith & Davis 1978 variant: binding bids, RFB timeout 100 cycles, award to fastest claimed completion); dozens of agents, one per emulated host with controllable failure frequency; reliable network. Every top-level task requires a **depth-4 contracting tree, branching factor 2 → up to 15 agents per task**. Agent lifespans uniform with mean = 100× short task duration = 10× long task duration (i.e., short=1000 cycles, long=10000 cycles; the OCR of Figure 3 scrambles the duration row but the failure-rate formula fixes the reading). Dead agents are replaced with same-skill new-ID agents to keep the pool constant. Four configurations: {short, long} × {abundant=50 subcontractors, scarce=16 subcontractors}, 3 top-level contractors. Three runs per config: failure-free baseline, survivalist, citizen+EH. Sentinel polling interval ≈ half the short task length ("task length − 2 times the sentinel polling interval").

**Measured results (Figures 5–6, text):**
- Config 1 (short/abundant): citizen ≈ **<1% above failure-free baseline**; survivalist worse (figure values ≈ 106–140%).
- Config 2 (short/**scarce**): **survivalist OUTPERFORMED citizen**, especially at chain length 2. Authors' explanation: for short tasks the benefit of early death detection is small, while "early detection causes more agents to re-announce their tasks and thus increases the number of agents who compete for the, already overloaded, scarce subcontractors... The net effect is that the EH mechanism slightly worsens the bottleneck created by the scarce subcontractors." At longer chains the proxy-bidding mechanism compensates and the two converge. **This is H3's sign reversal, demonstrated and mechanistically explained, in 2000.**
- Configs 3–4 (long tasks): citizen dramatically better; survivalist mean completion **600–700% of baseline** at depth 4 (multiple deaths re-trigger unzippering, "multiplying the mean completion time"); citizen held to **160–216%**.
- Max completion time: citizen lower in **all four** configurations (consistency benefit even where mean is worse).

**Parameter dependencies explicitly demonstrated:** chain depth (2/3/4), task duration (1000/10000), subcontractor abundance (50/16), failure rate (tied to task duration), polling interval, RFB timeout.

**Author-stated limitations:** only agent-death exception evaluated; one protocol; "there are situations where a survivalist approach will be superior" (refused-award example); EH service itself can fail ("dealing with exceptions in the EH service itself" = future work).

### 3.2 Klein & Dellarocas, CSCW 2000 (FULL TEXT VERIFIED, WP #203 version)

Not an experiment paper — a knowledge-based framework — but it contains the transferable *content*:
- Exception = "any departure from a process that achieves the process goals completely and with maximum efficiency," including "changes in resources, organizational structure, company policy, task requirements or task priority... **incorrectly or tardily performed tasks, resource contentions** between two or more distinct processes... conflicts between actions taken in different process steps." Undetected exceptions "can cause **cascading exceptions** as normal work is shoved aside."
- Failure-mode inheritance down a process taxonomy (specialization ≠ decomposition); detection via interleaved "sentinel" process templates; diagnosis by heuristic classification ("diagnoses represent **hypotheses rather than guaranteed deductions**" — fallible, type-specific detection is explicit); resolution via a taxonomy of ~200 strategies with preconditions; ~100 exception types; 4000+ process templates.
- **Semantic-fault anticipation (verbatim):** "IF an agent receives garbled data, THEN trace back to the original source of the faulty data, eliminate all decisions that were corrupted by this error, and start again" — provenance-traced rollback of corrupted downstream state, 2000.
- **Scarcity-relevant content:** "resource poaching" is a named failure mode of pull-based sharing (low-priority tasks reserve resources first); detection template compares average priority of served vs all tasks; resolution strategies include changing resource-sharing policy under wasteful contention and reallocating tasks when better resources appear.

### 3.3 Klein, Rodríguez-Aguilar & Dellarocas, JAAMAS 2003 (PARTIALLY VERIFIED)

Crossref-verified: "Using Domain-Independent Exception Handling Services to Enable Robust Open Multi-Agent Systems: The Case of Agent Death," JAAMAS 2003. It is the journal extension of the ICMAS 2000 study (same subtitle subject, same group). The group's framing paper CCS WP #211 (read in full) adds: **300+ exception types** with handlers for CNET, multi-level (Durfee & Montgomery), and team-based (Tambe) protocols; the **Role Commitment Violation (RCV) analysis** methodology (enumerate roles → commitments → failure modes per commitment); three interlinked taxonomies (protocols, exceptions, handlers); sentinel-as-"commitment guardian" architecture with registrar, notary, matchmaker-cleaning, orphan-task cancellation, and bid-annotation handlers. Prediction content is the ICMAS 2000 set (§3.1).

### 3.4 Hägg 1997 (FULL TEXT VERIFIED)

- **The H1 "prior work disagrees" framing is stated verbatim in 1997:** "there are two opposite positions to fault handling in MAS, one saying that a MAS is inherently fault tolerant [modularity → faults can be isolated, 'firewalling'] and the other saying that it is difficult to make a MAS fault tolerant [non-determinism → behaviour hard to guarantee, especially in fault situations]." The candidate's H1-as-conflict-resolution is a restatement of Hägg's §1/§3.
- Degrees of fault tolerance defined: full / graceful degradation / fail-safe.
- Sentinel concept: agents that guard functions/states, monitor communication (semantic addressing), build models of other agents incl. internal-state "checkpoints," intervene by selecting alternative problem-solving methods, **excluding faulty agents**, altering parameters, or **escalating to human operators**.
- **Containment-as-control-cost claim:** "the technique we choose actually **decreases the freedom for agents** where it is necessary for preserving the system's integrity" (with a footnote acknowledging controversy). Containment trades autonomy for integrity — a qualitative H2.
- Domain: power-distribution automation (DA-SoC/Sydkraft, Test Site Ronneby); worked examples (negotiation sentinel detecting underbidding customer agents; inconsistency detection). **No quantitative experiments** — architecture + examples only.

### 3.5 Horling & Lesser, KER 2004 (ABSTRACT ONLY)

Crossref abstract: "Many researchers have demonstrated that the **organizational design employed by an agent system can have a significant, quantitative effect on its performance characteristics**... survey of the major organizational paradigms... hierarchies, holarchies, coalitions, teams, congregations, societies, federations, markets, and matrix organizations... advantages and disadvantages... how they may be instantiated and maintained." Transferable content: the taxonomy of organizational structures (the IV space for H1) and the documented claim that structure quantitatively modulates performance. (The quantitative depth-versus-load results of this lineage live in Horling & Lesser JAAMAS 2007 and Horling's 2006 thesis — metadata-verified by E5, not re-read here.)

### 3.6 Kota, Gibbins & Jennings, ACM TAAS 2012 (FULL TEXT VERIFIED) — the strongest H3 antecedent beyond D&K

**Exact result:** decentralized structural self-adaptation (k-Adapt) reaches **70–90% of an idealized centralized allocator** and beats decentralized SOTA (Glinton et al. 2008 token variants) by **10–60%**, across closed/open × static/dynamic scenarios.

**The scarcity × recovery interaction (directly load-bearing for H3):**
- The adaptation (recovery) mechanism **consumes the same computational capacity as task work**: reorganisation load coefficient R; "the computation required for these utility calculations and reasoning depends on R... it need not be negligible and **might exhaust the computational capacities of the agent that, otherwise, would have been spent on task related actions**."
- Utility of every reorganisation action explicitly includes a **reorganisation cost term (−D)** and load deltas: V = Δload_x + Δload_y + Δload_OA + Δcost_comm + Δcost_reorg (Eq. 5).
- **Sign-reversal demonstration:** varying R from 0 to 0.9 (Fig. 4c), k-Adapt (meta-reasoned, selective adaptation) degrades "gradual[ly] and minimal[ly]," but all-Adapt (adapt with all acquaintances every step = maximal recovery activity) degrades "drastic[ally]"; "**for higher values of R, the profit of all-Adapt goes below 0, meaning the cost is more than the reward obtained.**" I.e., beyond a resource-cost threshold, more recovery mechanism ⇒ net-negative organizational utility — a stronger form of H3 than D&K's (net harmful, not merely slightly worse).
- Corollary design prediction: meta-reasoning about *when* to run recovery is essential when recovery is costly ("meta-reasoning is a crucial aspect in an adaptation process and cannot be ignored"); free-Adapt (R=0, resource-free recovery) is the theoretical upper bound — recovery works best exactly when it consumes no scarce resource.
- Conditions: 25 agents (up to 100 checked), 1000 runs/data point, 95% CIs; static: 1500 tasks/2000 steps; dynamic: 3000/4000; service probability SP ∈ [0,0.5] (heterogeneity); task similarity via pattern count NoP ∈ {5, ∞}; C=0.25, M=0.5, R=0.25, D=1 defaults. Structure matters most when agents are heterogeneous (SP low); at high SP "the significance of the structure itself diminishes" — an organizational-depth/structure × environment interaction relevant to H1's boundary conditions.

### 3.7 Tambe, JAIR 1997 (STEAM) (FULL TEXT VERIFIED)

- Teamwork model on joint intentions; team members **monitor team and individual performance and reorganize the team as necessary**; role-monitoring and team re-formation on member failure.
- **Decision-theoretic communication selectivity** — the transferable prediction for H2's cost side: agents weigh communication costs (Cc) against incoherence risks (Cmt, Cme); communication is the containment/coherence mechanism and it is *priced*.
- Experiments (Attack/Transport helicopter domains, RoboCup; Soar-based, ~300 domain-independent rules): "balanced" (decision-theoretic) vs "cautious" (always communicate) vs "reckless" (minimal communication) teams under 6 uncertainty conditions and team sizes 2–8.
- **Measured containment-cost result:** cautious team exchanges **10–20× more messages** than balanced for identical missions, and "**beyond six agents, the simulation with cautious team could not be run in real time**" (Attack; beyond seven in Transport) — i.e., maximal verification/communication is infeasible at scale under fixed computational resources. Reckless team **fails the mission** under uncertainty (gets stuck; strands members). Balanced adapts message count to conditions and succeeds throughout. This is the classical cost–benefit curve of containment, with an explicit feasibility cliff.
- Note the fixed-resource design: "the total computational resources available to each team were kept constant (a single SUN Ultra1)" — scarcity is the experimental frame.

### 3.8 Kaminka & Tambe, JAIR 2000 (FULL TEXT VERIFIED)

- Problem: **Monitoring Selectivity** — "how much monitoring of other agents' states is required to be effective" for failure detection. Socially-Attentive Monitoring: monitor for failures in *social relationships* between agents.
- **Theorems (proved in Appendix A):**
  - Thm 1: complete team-modeling + maximally team-coherent hypothesis ⇒ **sound** detection (no false positives).
  - Thm 2: maximally team-incoherent hypothesis ⇒ **complete** detection (no false negatives).
  - Thm 3: sound *and* complete detection in a centralized scheme requires **monitoring all teammates** (verification coverage ↔ correctness trade-off).
  - Thm 4: with an **observably-partitioned** set of team plans, **distributed** monitoring of only **key agents** achieves sound and complete detection — the classical answer to "how much verification is enough," conditioned on a structural property of the organization.
  - Thms 5–6: analogous results for monitoring mutual-exclusion relationships in groups.
- Empirics: ModSAF helicopter teams (broken radio-link and undetected-waypoint scenarios; all failure permutations tabulated; coherence heuristic gives no false positives but false negatives in cases 4–5; incoherence heuristic the reverse) and RoboCup (ISIS'97/'98 vs Andhill'97; ~15 and ~30 games per condition; ATA = average-time-to-agreement metric).
- **Capability × containment interaction (H2/H3-adjacent):** communication cuts ATA dramatically (e.g., '97 goalies 32.80→5.79 ticks, p≈7e-13), but ISIS'98 — with better local environment monitoring — is **3–4× less sensitive to communication loss**, and its score difference with/without communication is **not statistically significant**. The value of the containment mechanism (communication) depends on agents' independent sensing capability — a classical demonstration that containment value is conditional, not absolute.

### 3.9 Baldoni et al., JAAMAS 2022/2023 (TLDR-LEVEL VERIFIED)

TLDR (S2): "a formalization of accountability, including the **accountability lifecycle**, for the design of **robust agent organizations**, by describing typical patterns in which accountability affects the state of an agent's goals and vice versa." Accountability as a first-class organizational construct for robustness — pre-LLM. Companion 2025 KER vision paper (abstract verified): exceptions as first-class elements of organizational design in JaCaMo, with explicit **responsibilities for managing exceptions**. The classical community is actively consolidating this space *now*.

---

## 4. Resource-scarcity × fault-handling interactions in classical MAS beyond D&K

Ranked by strength of evidence:

1. **Kota et al. TAAS 2012 (FULL TEXT):** recovery activity priced by R and D; maximal recovery (all-Adapt) goes **net-negative** at high R; selective meta-reasoned recovery (k-Adapt) degrades gracefully; resource-free recovery (free-Adapt) is the upper bound. The cleanest classical statement that containment value reverses sign as the mechanism's resource consumption rises.
2. **Tambe JAIR 1997 (FULL TEXT):** maximal containment communication (cautious) is 10–20× costlier and **infeasible in real time beyond 6–7 agents** under fixed compute; minimal containment (reckless) fails missions; priced selectivity (balanced) dominates. Scarcity (fixed CPU, hostile-environment comms risk) is the frame.
3. **Kaminka & Tambe JAIR 2000 (FULL TEXT):** monitoring selectivity theorems — full coverage required for sound+complete centralized detection (Thm 3), but structural properties (observable partitioning) let you monitor only key agents (Thm 4); containment value conditional on agent capability (ISIS'97 vs '98).
4. **D&K ICMAS 2000 config 2 (FULL TEXT):** EH services slightly *worse* than timeout/retry with short tasks + scarce subcontractors; mechanism: early detection → more re-announcements → worse bottleneck competition.
5. **Klein & Dellarocas CSCW 2000 (FULL TEXT):** resource poaching as named failure mode; scarcity-specific detection templates and resolution strategies.
6. **Chia, Neiman et al., "Poaching and distraction in asynchronous agent activities," ICMAS'98** (cited in ICMAS 2000 as the source of the resource-poaching dysfunction; metadata not re-verified here — flagged UNVERIFIED).
7. **Stanković, Štula & Maras, JAAMAS 2015 (TLDR):** an evaluation methodology with metrics for comparing fault-tolerance approaches in MAS — the classical community's own mechanism bake-off frame.
8. **Carley & Lin, Management Science 1997; Lin & Carley 2003 (metadata verified):** computational organization theory — organizational performance under **information distortion** (semantic corruption) across org designs; "designing stress-resistant organizations" is org-design-for-fault-resistance. Not MAS-agent-based but directly on the H1/H4 lane.
9. **Replication-cost trade-offs** in the DARX line (Guessoum et al. 2005/2006; Fedoruk & Deters 2002; Kumar/Cohen/Levesque ICMAS 2000) — adaptive replication explicitly trades replication cost against fault coverage (via E5's verified Arfat & Eassa 2016 survey; individual papers metadata-level).

---

## 5. Collision classification for the candidate's claims (my lane)

- **H1 (delegation/org depth changes fault propagation and recovery cost):** **FATAL COLLISION on the phenomenon and its direction-conditions.** D&K ICMAS 2000 demonstrated depth-dependent amplification (unzippering; 600–700% at depth 4, long tasks) and its containment (160–216% with sentinels), with depth, branching, task length, and failure rate as controlled parameters. The "prior work disagrees (amplify vs attenuate)" framing is itself classical — Hägg 1997 states both positions in §1. Horling & Lesser 2004 document that org design quantitatively modulates performance. Only the LLM substrate is new.
- **H2 (containment reduces propagation but imposes cost):** **FATAL COLLISION.** D&K citizen-vs-survivalist; Tambe's cautious/balanced/reckless with a measured 10–20× cost multiple and a feasibility cliff; Kaminka & Tambe's coverage↔correctness theorems; Kota's explicit reorganization cost in the utility function. "Containment has a price" is a 1997–2012 commonplace with theorems and measurements.
- **H3 (containment backfires under scarcity — sign reversal):** **FATAL COLLISION on the qualitative claim; the candidate's experiment would be a replication, not a discovery.** D&K 2000 demonstrated the reversal (scarce subcontractors ⇒ EH worse) with a mechanism; Kota 2012 demonstrated a stronger reversal (net-negative profit at high recovery cost); Tambe 1997 demonstrated the feasibility cliff. The candidate's remaining space: (a) does the reversal replicate with *semantic* faults and *token/latency/reviewer* budgets (classical budgets were compute/communication/subcontractor count)? (b) the crossover *location* as a function of budget tightness — classical work never mapped the phase boundary parametrically.
- **Novelty claim as stated ("first experimental transfer test of classical MAS fault-handling results ... on tool-executing LLM agent organizations with semantic faults"):** **SURVIVES only in narrowed form.** No classical or (per the other lanes' reports) LLM-era paper has run this transfer. But the claim as worded invites the W1-style objection (R3 mock review): the classical record did not assume crash-only faults conceptually — CSCW 2000's taxonomy includes incorrectly performed tasks, wrong-type inputs, garbled data with provenance rollback; Carley & Lin studied information distortion; the trust/reputation literature is about semantically unreliable information. The defensible claim is substrate + detection-quality: classical detection was perfect and free (polling for crash faults); for semantic faults detection is imperfect and costly, and **detection quality is an uncontrolled confound in any naive transfer** — that is the genuinely open experimental question.

---

## 6. Unexpected findings

1. **Hägg 1997 pre-empts the H1 framing itself**, not just its answer: the "two opposite positions" (inherent fault tolerance via modularity vs. non-determinism making guarantees hard) is the amplify-vs-attenuate disagreement, in print, 29 years early.
2. **Kota et al. 2012's all-Adapt result is a stronger H3 than D&K's** — recovery activity can drive organizational profit *below zero* ("the cost is more than the reward obtained") — and it comes with the design prescription the candidate will need: meta-reasoning about when to invoke recovery. Any H3 experiment must cite this or be scooped conceptually.
3. **The classical lineage is alive in 2025**: Baldoni, Baroglio, Micalizio & Tedeschi, "Exception handling in multi-agent oriented programming," KER 2025 (10.1017/S0269888925000050) — exceptions as first-class organizational design elements in JaCaMo. The scoop risk on the classical side is not just old papers; the JAAMAS/KER community is actively re-consolidating exception handling in agent organizations right now, and they are exactly the MASO/PRIMA reviewer pool.
4. **Two MIT theses extend the D&K experimental line** (Muthitacharoen 2000, DSpace 1721.1/86529; Aryananda, DSpace 1721.1/9437, "exception handling service for the contract net protocol family") — the D&K experiments were part of a small experimental program, not a one-off (metadata verified; contents not read).

## 7. What I could not verify

- JAAMAS 2003 full text (journal version proper) — treated via ICMAS 2000 full text + WP #211; risk: LOW (same study).
- Horling & Lesser KER 2004 full text — ABSTRACT ONLY; it is a survey, so no unique predictions are attributed to it here.
- Baldoni et al. JAAMAS 2022 full text — TLDR-level only.
- Chia, Neiman et al. ICMAS'98 — UNVERIFIED (cited within verified full texts only).
- Figure 3 of ICMAS 2000 has an OCR column-alignment ambiguity in the task-duration row; resolved logically via the failure-rate formula (short=1000, long=10000 cycles) but flagged for anyone quoting the table directly.
