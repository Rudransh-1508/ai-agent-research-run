# W2 — Assassin Report: CAND-2 "ClassicalTransfer"

**Investigator:** W2 ASSASSIN (CAND-2)
**Date:** 2026-09-21
**Candidate under attack:** Replication/falsification study — do classical MAS organizational fault-handling results (Dellarocas & Klein sentinel services + "unzippering", Horling & Lesser organizational paradigms, Kota et al. decentralized reorganization, containment-backfires-under-scarcity) hold for LLM-based agents with semantic faults? Frame: 25 years of organizational fault-tolerance theory never tested against LLM failure phenomenology; test predictions, find where they break, derive updated design principles.

**Mission:** Kill CAND-2. Search for (a) any existing replication/transfer study of classical MAS fault-tolerance/organizational results to LLM agents; (b) LLM-MAS papers citing the four classical anchors (Semantic Scholar citation APIs); (c) the "do classical results hold for LLM agents" genre (formulaic risk); (d) 2025–2026 papers already framing LLM-MAS robustness as "lessons from classical MAS"; (e) honest assessment of reviewer reception and replication-study precedent at AAMAS/PRIMA.

---

## VERDICT: SURVIVES — wounded on framing novelty and outcome-suspense, but the core kill fails decisively

The direct kill — an existing transfer study — does not exist. Citation analysis proves the classical fault-handling canon is essentially **uncited** by the LLM-MAS literature: Dellarocas & Klein ICMAS 2000 has exactly **one** post-2023 citer (a classical-lineage JaCaMo paper with zero LLM content); Hägg 1997 has **zero** LLM-era citers; Kota TAAS 2012 has four post-2023 citers, none LLM; Horling & Lesser 2004 has four LLM-era citers, none on fault handling. No paper — found via citation APIs, arXiv full-text searches, or the 39 wave-1 reports — tests whether classical organizational fault-handling results hold for LLM agents.

The wounds are real but non-fatal: (1) the "re-test classical X with LLMs" genre is established and partially fatigued in behavioral science; (2) three position papers (NeurIPS 2025, two arXiv 2025–2026) have already staked the "engage classical MAS" framing; (3) the study's value hinges on producing non-obvious middle results rather than confirmatory or obvious-failure outcomes.

---

## 1. Kill attempt 1 — existing transfer/replication study: FAILED (no occupancy)

### 1.1 Citation analysis of the four classical anchors (Semantic Scholar Graph API, 2026-09-21)

| Classical anchor | S2 citation count | Post-2023 citers | LLM-MAS citers | Details |
|---|---|---|---|---|
| Dellarocas & Klein, ICMAS 2000 (DOI 10.1109/ICMAS.2000.858440; S2 CorpusId 6442794) | 57 | **1** | **0** | Sole recent citer: Baldoni, Baroglio, Micalizio & Tedeschi, "Exception handling in multi-agent oriented programming," Knowledge Engineering Review 2025, DOI 10.1017/S0269888925000050. Abstract verified via Crossref: JaCaMo organizational exception handling, exceptions as first-class organizational design elements — **pure classical lineage, no LLM content**. |
| Kota, Gibbins & Jennings, ACM TAAS 2012 (DOI 10.1145/2168260.2168261; CorpusId 15071096) | 105 | 4 | **0** | Citers: "Pick Two: An Adversarial Animal Survival Game" (arXiv:2606.27557 — Unity ABM of animal coalitions, irrelevant, abstract verified); Li et al. TCSS 2023 (DOI 10.1109/TCSS.2022.3204838); Amaral et al. JAAMAS 2023 (DOI 10.1007/s10458-023-09623-8); Hashmi et al. IEEE SSE 2023 (DOI 10.1109/SSE60056.2023.00034). All classical/self-adaptive systems. |
| Hägg, "A Sentinel Approach to Fault Handling in MAS" (DOI 10.1007/BFb0030090; CorpusId 226300991 line) | 137 | 5 since 2020 | **0** | Recent citers all classical: Mahala et al. JAAMAS 2023 (normative resilience, DOI 10.1007/s10458-023-09627-4); Baldoni et al. JAAMAS 2022 accountability (10.1007/s10458-022-09590-6); Baldoni et al. IEEE Internet Computing 2022 (10.1109/MIC.2022.3216272); Baldoni et al. PAAMS 2023 SARL (10.1007/978-3-031-37616-0_33); Benaboud & Mags 2020 (10.3233/MGS-200334). |
| Horling & Lesser, KER 2004 (DOI 10.1017/S0269888905000317) | 752 | 38 since 2024 | 4, **none fault-related** | LLM-era citers: Loop-Back Authority (arXiv:2609.14767); Organizational Control Layer (arXiv:2606.04306); Borghoff et al., Discover Computing 2025 (DOI 10.1007/s10791-025-09667-2); Cognitive Agents for Agile SW PM (Electronics 2024, DOI 10.3390/electronics14010087). All performance/governance framing; zero fault-handling transfer. |

### 1.2 arXiv full-text searches (all 2026-09-21, export.arxiv.org API)

- `"unzippering"` → **0 hits, ever**. The Dellarocas-Klein key phenomenon term is absent from the entire arXiv corpus.
- `"contract net protocol" AND "LLM"` → 0 hits. Nobody has re-implemented the classical substrate with LLMs.
- `"sentinel" AND "LLM agents" AND fault` → 0 hits.
- `"classical multi-agent" AND "large language model"` → 2 hits: LangMARL (arXiv:2604.00722, MARL credit assignment in language space — not fault tolerance) and Bădică et al. (arXiv:2509.02515, see §3).
- `"fault handling" AND "LLM-based multi-agent"`, `"reorganization" AND "LLM-based multi-agent"`, `"self-adaptation" AND "LLM" AND "agent organization"` → 0 relevant hits (only the LIFE survey 2605.14892, already mapped in wave 1).

**Conclusion:** No existing replication, transfer, or falsification study of classical MAS fault-tolerance results on LLM agents. The specific study is unoccupied. Kill fails.

---

## 2. Kill attempt 2 — the "do classical results hold for LLMs" genre: EXISTS, prestigious, partially fatigued (WOUND)

The genre is real and has top-venue precedent — which both legitimizes CAND-2's approach and makes its *framing template* feel familiar:

| Paper | Venue | What it re-tests | Verified via |
|---|---|---|---|
| Aher, Arriaga & Kalai, "Using Large Language Models to Simulate Multiple Humans and Replicate Human Subject Studies" (Turing Experiments) | **ICML 2023, oral** (arXiv:2208.10264) | Ultimatum Game, Milgram, Garden Path, Wisdom of Crowds | arXiv abs page |
| Akata et al., "Playing repeated games with large language models" | **Nature Human Behaviour 2025**, DOI 10.1038/s41562-025-02172-y | Classical repeated-game theory | Crossref |
| "LLM Agents Do Not Replicate Human Market Traders: Evidence From Experimental Finance" | arXiv:2502.15800 (2025) | Experimental-finance results — a *falsification* outcome | arXiv API |
| "Spiral of Silence in Large Language Model Agents" | arXiv:2510.02360 (2025) | Noelle-Neumann opinion theory | arXiv API |
| "Can Lessons From Human Teams Be Applied to Multi-Agent Systems?" | arXiv:2510.07488 (Oct 2025, under ARR) | Human team science (structure/diversity/interaction) → LLM MAS; flat > hierarchical | arXiv abs page |
| Critique of the genre: "The threat of analytic flexibility in using large language models to simulate human data" | under review 2025–26 (Crossref review DOIs 10.1177/25152459261461505/v1/review1 etc.) | — | Crossref |

**Assessment:** All of these replicate *human-subject / experimental-economics* results. None transfers *computational MAS engineering* results (sentinels, reorganization, containment). CAND-2 is closer to a systems-replication study than to the fatigued "LLMs simulate humans" template — but a reviewer pattern-matching to the template is a real risk. The Nature Human Behaviour / ICML-oral precedent also means the approach is *respected*, not just tolerated. Net: WOUND on framing freshness, not on legitimacy.

---

## 3. Kill attempt 3 — "lessons from classical MAS" framing already staked: PARTIALLY (WOUND)

Four 2025–2026 papers publicly stake the framing that LLM-MAS must engage classical foundations:

1. **La Malfa et al., "Large Language Models Miss the Multi-Agent Mark," NeurIPS 2025 position track, arXiv:2505.21298** (abstract verified). Argues LLM-"MAS" appropriates MAS terminology without engaging foundational principles (social agency, environment design, coordination protocols, emergence); warns the field "may slow down and lose traction by revisiting problems the MAS literature has already addressed." **This is the most damaging framing paper**: a top-venue position piece explicitly calling for what CAND-2 does — but it is a *position* paper with no experiments. CAND-2 can position as the experimental answer to a named, NeurIPS-published call.
2. **Bădică et al., "Contemporary Agent Technology: LLM-Driven Advancements vs Classic Multi-Agent Systems," arXiv:2509.02515** (Sep 2025, 33 pp, cs.MA; abstract verified). Reflection on LLM advances vs foundational MAS literature; identifies challenges/directions. No experiments.
3. **Mieczkowski et al., "Language Model Teams as Distributed Systems," arXiv:2603.12229** (Mar 2026, cs.MA; abstract verified). Proposes distributed-systems theory as the principled foundation for LLM teams — the same transfer move, one field over. No fault-tolerance experiments.
4. **Terrarium, arXiv:2510.14312** (Oct 2025; abstract verified). Revives the classical **blackboard architecture** as a testbed for LLM-MAS safety/security — a classical-concept revival with an implementation, but attack-focused, not fault-handling transfer.

Adjacent mechanism occupancy: **SHIELDA, arXiv:2508.07935** (Aug 2025, cs.SE; abstract verified) — runtime exception-handling framework for LLM agentic workflows (36-exception taxonomy over 12 agent artifacts, handling-pattern registry, phase-aware recovery; single AutoPR case study). Occupies "exception handling for LLM agents" as *engineering*, but is single-workflow, non-organizational, and not a replication/falsification of classical results. Must-cite, not a killer.

**Assessment:** The framing is pre-staked; the *experimental content* is not. CAND-2's abstract must not claim "first to connect classical MAS to LLM agents" (false — La Malfa et al., Bădică et al., Mieczkowski et al.) but "first to *experimentally test* classical organizational fault-tolerance predictions on LLM agents" (true per §1).

---

## 4. Reviewer reception and replication precedent at AAMAS/PRIMA (honest assessment)

**Venue fit is unusually good.** PRIMA 2026's theme is verbatim "Beyond Traditional MAS: fusing rigorous MAS foundations with Generative and Agentic AI" (A2 report, verified prima2026.org). The PRIMA 2026 board includes Dignum, van der Torre, Dastani, Ito, Yokoo — the community that *wrote* the classical organizational-MAS literature. A faithful transfer study speaks the reviewers' native language and flatters their heritage; the "old wine" reaction is far more likely at an ML venue than at MASO/PRIMA. MASO's CFP additionally names "detection and mitigation of cascading, and systemic failures" and "organizational testbeds."

**Replication precedent:** thin at AAMAS main track (no replication track; PRIMA 2024/2025 TOCs contain no replication studies — A2 report), but the adjacent agent-based-modeling community has an established replication culture (e.g., "Replication of an agent-based model using the Replication Standard," Environmental Modelling & Software 2021, DOI 10.1016/j.envsoft.2021.105016 — verified), and the LLM-era genre precedent (§2) is at ICML/Nature HB/PNAS level. A MASO reviewer is more likely to ask "is this a *workshop-sized* contribution?" than "is replication science?"

**The genuine reviewer risks for CAND-2:**
1. **Outcome-suspense risk (biggest).** If sentinels/verifiers handle semantic faults fine → "confirmatory, no surprise." If they fail → "of course; they were built for crash faults." The paper lives or dies on landing *non-obvious middle results*: e.g., does the unzippering effect's magnitude shrink or explode with semantic faults (retry can amplify cost without amplifying error)? Does containment-backfires-under-scarcity replicate when the scarce resource is *tokens/context* rather than subcontractors? Does Kota-style reorganization help when agent "capabilities" are model-prompt bindings rather than fixed skills? These are genuinely uncertain — the paper must be designed around them, not around re-running the classical experiments.
2. **Fidelity-of-replication risk.** Faithfully reproducing Dellarocas-Klein conditions (4-level contracting trees, abundant/scarce subcontractor regimes, Swarm-style discrete-event dynamics) on tau2-bench + LangGraph is a heavier build than wave 1's 3.5–5 person-week descoped estimate (which was scoped for CAND-1). An "inspired-by" loose adaptation weakens the falsification claim; a faithful one may exceed workshop scope. Tension to resolve in scoping.
3. **Genre-template fatigue (moderate).** §2's template is recognizable; mitigate by framing as *engineering-science transfer with design-principle output*, not "we simulated classical study X with LLMs."
4. **Framing pre-claimed (moderate).** §3's position papers must be cited as motivation; CAND-2 is derivative of their call — spin as answering it.

---

## 5. What survives — precise statement

**Survives intact:** The experimental core. No work — classical-citing, arXiv-indexed, or in the 39 wave-1 reports — tests whether classical MAS organizational fault-handling results (sentinel containment, unzippering propagation magnitude, reorganization-under-faults, containment-backfires-under-scarcity) hold when agents are LLMs with semantic failure modes. The four anchors' LLM-era citation counts are 0–4 with zero fault-transfer content. The specific predictions (600–700% unzippering blowup; EH-services ≤1–216% containment; scarcity backfire; Kota's 70–90%-of-centralized reorganization utility) have never been re-measured on an LLM substrate.

**Must be amputated:** Any claim of framing novelty ("first to bridge classical MAS and LLM agents" — killed by arXiv:2505.21298, 2509.02515, 2603.12229, 2510.14312). Any claim that exception handling for LLM agents is new (killed by SHIELDA arXiv:2508.07935).

**Strongest surviving formulation:** "La Malfa et al. (NeurIPS 2025) and Bădică et al. (2025) argue LLM-MAS must re-engage classical MAS foundations; we provide the first experimental test of that engagement's central empirical question — do classical organizational fault-tolerance results survive the move from crash faults to semantic faults? We replicate Dellarocas-Klein/Kota conditions on LLM agents, identify exactly which predictions break (and why), and derive updated design principles." Positioned this way, CAND-2 is *native* to PRIMA 2026's "Beyond Traditional MAS" theme and to MASO's reviewer pool.

---

## 6. Most damaging papers (for the record, with identifiers)

None kills; ranked by damage to CAND-2's framing:
1. La Malfa et al., "Large Language Models Miss the Multi-Agent Mark," **NeurIPS 2025 position, arXiv:2505.21298** — pre-stakes the framing at a top venue.
2. Bădică et al., "Contemporary Agent Technology: LLM-Driven Advancements vs Classic Multi-Agent Systems," **arXiv:2509.02515** — 33-page reflection occupying the "classical vs LLM MAS" survey space.
3. Mieczkowski et al., "Language Model Teams as Distributed Systems," **arXiv:2603.12229** — same transfer move from distributed systems.
4. SHIELDA, **arXiv:2508.07935** — occupies exception-handling mechanism engineering for LLM workflows.
5. Baldoni et al., "Exception handling in multi-agent oriented programming," **KER 2025, DOI 10.1017/S0269888925000050** — the sole recent citer of Dellarocas & Klein; shows the classical line is alive and could beat CAND-2 to the transfer from the other side.
6. Akata et al., **Nature Human Behaviour 2025, DOI 10.1038/s41562-025-02172-y** + Aher et al., **ICML 2023 oral, arXiv:2208.10264** — genre precedent: legitimizes the method, dates the template.

## 7. Verification log

- Semantic Scholar Graph API: metadata + full citation lists pulled for all four classical anchors (2026-09-21); post-2023 citers enumerated above. S2 search endpoint rate-limited (429) later in the run; citation endpoints worked.
- arXiv API: queries listed in §1.2 (several returned empty under rate limiting; zero-hit claims rest on queries that returned well-formed empty result feeds).
- Crossref: KER 2025 abstract (10.1017/S0269888925000050), Akata et al. (10.1038/s41562-025-02172-y), ABM replication precedent (10.1016/j.envsoft.2021.105016), genre-critique review DOIs.
- arXiv abstract pages fetched and read: 2509.02515, 2510.07488, 2505.21298, 2510.14312, 2508.07935, 2603.12229, 2606.27557, 2208.10264.
- Wave-1 reports read before searching: E5 (classical MAS assassin), B10 (organizational MAS), D5 (org/eval surveys), A2 (PRIMA/MASO positioning), B14 (self-healing, grep).
- Not verified: DBLP (bot-blocked); OpenAlex (daily budget exhausted); DuckDuckGo HTML (returned no parseable results). No claim above rests solely on an unverified snippet.
