# Adversarial prior-art check: "The shared experience pool as a commons with strategic contributors"

Checked 2026-09-08. Brief: falsify, not support. Pre-LLM literature searched first.

## Verdict

**closed** (on the headline and both sharp predictions; at best *partially closed* on a narrow empirical instantiation).

The economics of user-generated content owns this outright, and it owned it by 2011: Ghosh & McAfee, *Incentivizing High-quality User-Generated Content* (WWW 2011) states, verbatim in its abstract, "The model predicts, as observed in practice, that if exposure is independent of quality, there will be a flood of low quality contributions in equilibrium." That single sentence is the candidate's entire "sharp prediction" - contributors do not withhold, they supply valid-but-minimum-quality entries under flat reward - and the paper's positive result (make reward contingent on realized downstream exposure/use) is the candidate's "usage-based beats flat payment," proved fifteen years ago in the same model. This is the same class of trap as the 2010 experimental-economics burn: the result is pre-LLM, in a venue (WWW/EC) that a modern-agents literature search will not surface. Independently, Hess & Ostrom (2007) owns the "knowledge as a commons" framing including the non-rival/subtractable distinction the candidate treats as its own setup; federated-learning incentive design owns the "value each contribution, pay proportionally, detect free riders" mechanism space at industrial scale; peer prediction owns quality elicitation when quality is unverifiable at write time; P2P pollution-attack research owns the pollution dynamics and its reputation-based defenses; and Holmström-style output-contingent-vs-fixed-fee contracting owns "usage-based beats flat" as a textbook result. On the LLM side the candidate is also less clear than assumed: **EquiMem (arXiv 2605.09278, May 2026)** already formulates writing to a shared LLM agent memory as a *zero-trust memory game* with contributor/auditor utilities, an equilibrium, and downstream-task evaluation on real LLM agents.

---

## 1. Public goods provision and the commons

**Hess & Ostrom, *Understanding Knowledge as a Commons: From Theory to Practice* (MIT Press, 2007).** Direct hit on framing. The volume's stated project is exactly the candidate's setup move: treat a shared knowledge resource as a commons subject to social dilemmas, and explicitly separate it from Hardin-style subtractable CPRs. Open-access edition: <https://mitpress.mit.edu/9780262516037/understanding-knowledge-as-a-commons/>; MIT Press Direct: <https://direct.mit.edu/books/edited-volume/3807/>. I read the publisher pages and the eScholarship review (<https://escholarship.org/uc/item/44x8994c>), not the full book - flagging that plainly. The framing paragraph of the candidate is not novel and a reviewer who knows this book will say so in the first line of their review.

**Bergstrom, Blume & Varian, "On the private provision of public goods," *J. Public Economics* 29(1):25-49 (1986).** Full text: <http://www2.ulpgc.es/hege/almacen/download/39/39266/on_the_private_provision_public_goods.pdf>. Unique Nash equilibrium of voluntary contribution, neutrality, crowding-out, comparative statics. This is the baseline any "derive free-riding equilibria" claim is measured against. The candidate's "derive free-riding equilibria" step is a re-derivation in a special case.

**Wasko & Faraj, "Why Should I Share? Examining Social Capital and Knowledge Contribution in Electronic Networks of Practice," *MIS Quarterly* 29(1):35-57 (2005).** <https://aisel.aisnet.org/misq/vol29/iss1/4/>. Frames contribution to an *electronic knowledge repository* explicitly as a collective-action / public-good problem with free riders acquiring the same knowledge. The candidate's premise sentence, twenty-one years early, for human contributors to a persistent retrievable pool.

**Verdict on this area:** framing fully closed.

## 2. Quality vs quantity in voluntary contribution - THE LOAD-BEARING PREDICTION

This is where the candidate dies.

**Ghosh & McAfee, "Incentivizing High-quality User-Generated Content," WWW 2011.** PDF read in full (author-hosted version, <https://www.mcafee.cc/Papers/PDF/UGC.pdf>; ACM DOI <https://dl.acm.org/doi/10.1145/1963405.1963428>). Verbatim from the abstract of the version I read:

> "We provide a game-theoretic model within which to study the problem of incentivizing high quality UGC, in which contributors are strategic and motivated by exposure. Our model has the feature that both the quality of contributions as well as the extent of participation is determined endogenously in a free-entry Nash equilibrium. The model predicts, as observed in practice, that if exposure is independent of quality, there will be a flood of low quality contributions in equilibrium."

And, verbatim from the body (p. ~8 of the same PDF, discussing a weakened mechanism):

> "remains independent of quality, which means equilibrium qualities remain 0 exactly as in the baseline mechanism."

Map it onto the candidate one-for-one:
- "strategic and motivated by exposure" = agents rewarded when their entry is retrieved and used.
- "quality *and* extent of participation endogenous in free-entry equilibrium" = the candidate's joint withhold/pollute choice.
- "exposure independent of quality → flood of low quality" = **the candidate's sharp prediction, verbatim, with the equilibrium quality pinned at the corner (zero effort), not merely "suboptimal."**
- The elimination mechanism (rate each contribution, drop anything not uniformly rated positive) = the candidate's "contribution mechanism," and it provably drives quality to optimal with diverging participation.

**Ghosh, "Social Computing and User-generated Content: A Game-Theoretic Approach," *ACM SIGecom Exchanges* 11(2):16-21 (2012).** Read in full: <https://www.sigecom.org/exchanges/volume_11/2/GHOSH.pdf>. Verbatim:

> "Without some connection between quality and exposure, exposure-motivated contributors will flood a site with low quality contributions, as is indeed observed in practice."

This six-page survey is, effectively, the candidate's related-work section written in 2012. It also names the flat-payment comparison directly - verbatim:

> "A number of these forums (Y! Answers, MSN QnA, and Rediff Q&A, to name a few) are structured so that the 'best' contribution for each task receives some high reward, while all remaining contributions receive an identical, lower reward irrespective of their actual qualities."

That "identical, lower reward irrespective of their actual qualities" *is* flat payment, and Ghosh & Hummel (2012) analyze exactly when it can and cannot implement the designer's optimum.

**Ghosh & Hummel (2011), rank-order mechanism.** Per the survey above: the rank-order (usage/rating-ordered) allocation elicits *strictly higher* equilibrium quality than the proportional mechanism, with the lowest quality over all mixed equilibria tending to optimal. This is the "usage-based beats flat" comparison, decided, in the ranked-retrieval setting closest to a top-k memory retriever.

**Jain, Chen & Parkes, "Designing Incentives for Online Question and Answer Forums," EC'09** (journal version *Games and Economic Behavior*, 2014). <https://yiling.seas.harvard.edu/publications/designing-incentives-online-question-and-answer-forums>. Best-answer scoring rules; unique efficient equilibrium under substitutes valuations, least-efficient equilibrium under complements. I read the abstract/summary pages, not the full journal text - paywalled at ScienceDirect.

**Xia, Qin, Yu & Liu, AAAI 2014, "Incentivizing High-Quality Content from Heterogeneous Users."** Full text read: <https://arxiv.org/pdf/1404.5155>. Extends the above to heterogeneous contributor ability with private types (agents differ in the best quality they *can* produce), fixed reward budget, top-K vs proportional allocation, existence/non-existence of pure NE. If the candidate's agents are heterogeneous LLMs, this paper already has the type model.

**Hu, Jagadeesan, Jordan & Steinhardt, "Incentivizing High-Quality Content in Online Recommender Systems" (arXiv 2306.07479, v3 2024).** Full text read. Verbatim from the abstract:

> "We show that standard online learning algorithms, such as Hedge and EXP3, unfortunately incentivize producers to create low-quality content, where producers' effort approaches zero in the long run for typical learning rate schedules. Motivated by this negative result, we design learning algorithms that incentivize producers to invest high effort and achieve high user welfare."

This kills the one seam I thought might survive - that in an experience pool the *retriever*, not a designer, allocates attention, so the mechanism is coupled to a learned ranker. That coupling is precisely this paper's subject, and its answer is already negative-then-constructive.

**Verdict on this area:** closed. The prediction is a fifteen-year-old theorem, and its restatement in the recommender setting is two years old.

## 3. Data/knowledge sharing incentive mechanisms

**Federated learning incentive design owns the mechanism half.** Survey: Zhan et al., "A Comprehensive Survey of Incentive Mechanism for Federated Learning" (<https://arxiv.org/pdf/2106.15406>). The FL literature has, at scale: Shapley-based contribution valuation (IJCAI 2024, <https://www.ijcai.org/proceedings/2024/0554.pdf>; DPVS-Shapley, <https://arxiv.org/pdf/2410.15093>), a survey of contribution-evaluation approaches specifically (<https://arxiv.org/pdf/2311.09856>), known instability of those metrics (<https://arxiv.org/html/2405.08044v3>), explicit free-rider detection, and the "model-as-reward" paradigm where the quality of what you receive scales with what you contributed. Critically, this literature already handles the exact hard case the candidate claims: *a contributor who participates but submits a low-value update*, because low-quality data does not improve the global model. Any "usage-based contribution valuation" the candidate proposes will be read as Shapley-lite, and reviewers from this community will ask why Shapley or leave-one-out contribution valuation is not the baseline.

**Verdict:** mechanism-design half largely closed; FL owns the valuation machinery.

## 4. Peer prediction / elicitation without verification

If entry quality is unverifiable at write time, peer prediction is the canonical answer and has been since 2005. Miller, Resnick & Zeckhauser (2005), "Eliciting Informative Feedback: The Peer-Prediction Method"; Prelec's Bayesian Truth Serum; Witkowski & Parkes (2012), peer prediction without a common prior (<https://dl.acm.org/doi/10.1145/2229012.2229085>); Dasgupta & Ghosh (2013), multi-task mechanisms that eliminate uninformative equilibria; Shnayder, Agarwal, Frongillo & Parkes (2016), *informed truthfulness* in multi-task peer prediction. Overview I read: <https://arxiv.org/pdf/1605.01021>.

Important structural point against the candidate: peer prediction exists precisely because you cannot verify at write time. But an experience pool *can* verify - eventually, noisily - via downstream task outcome. That puts the candidate in the *easier* verified-with-delay regime, which is standard contract theory with a delayed noisy signal, not a new elicitation problem. Either way the candidate does not get to claim the elicitation problem as open.

**Verdict:** closed as the default mechanism answer.

## 5. Information pollution / lemons

**P2P pollution attacks are structurally identical and are a named, mature literature.** Liang, Kumar, Xi & Ross, "Pollution in P2P File Sharing Systems" (INFOCOM 2005); Christin, Weigend & Chuang, "Content availability, pollution and poisoning in file sharing peer-to-peer networks" (ACM EC 2005, <https://dl.acm.org/doi/10.1145/1064009.1064017>); Green (<https://arxiv.org/pdf/1108.1343>). The known taxonomy - decoy insertion vs identifier corruption, random vs replicated decoy attacks - and the known defense - reputation systems plus publish-verification at index nodes - is the candidate's "pollution equilibrium" and "contribution mechanism," in a shared retrievable pool, twenty-one years early. Note KaZaA saw 8,000-50,000 polluted versions of a single file: pollution of a shared retrieval pool is not a hypothetical.

**Lemons.** Akerlof (1970) applied to a reuse repository is well-trodden; the current instance is "The Software Supply Chain as a Market for Lemons: A Multivocal Review of Trust Signal Collapse" (<https://arxiv.org/abs/2608.20678>, Aug 2026), which explicitly analyzes separating-to-pooling collapse when cheap trust signals stop separating low- from high-quality contributors, including *non-adversarial AI-driven inflation*. That last clause is the candidate's "valid-but-suboptimal, not malicious" case, already named.

**Verdict:** closed.

## 6. Usage-based vs flat payment

Textbook. Output-contingent pay dominates fixed pay when effort is unobservable and output is an informative signal of effort (Holmström's informativeness principle, 1979); royalty-vs-fixed-fee licensing is the applied version, where royalties are used specifically to address moral hazard over non-contractible know-how transfer, and royalty licensing induces a more efficient outcome than fixed-fee licensing in standard settings (see e.g. Savva & Taneri, *Management Science* 61(6), 2015, <https://pubsonline.informs.org/doi/10.1287/mnsc.2014.2000>; NBER w14226 on inventor moral hazard in university licensing, <https://www.nber.org/system/files/working_papers/w14226/w14226.pdf>). Within UGC specifically, exposure-based reward *is* usage-based reward and Ghosh & McAfee/Ghosh & Hummel already prove it dominates quality-independent reward.

A reviewer will not accept "usage-based beats flat" as a finding. They will accept it as a sanity check that the simulation is not broken.

**Verdict:** closed, and stating it as a headline prediction is a credibility risk.

---

## 7. LLM side - re-verified from full texts

**MAC-SPGG (arXiv 2508.02076, NeurIPS 2025) - verified, and the parent's suspicion is confirmed.** I read the full PDF. The contributed good is *per-episode, not persistent*. From §3 of the PDF: each agent i produces "one contribution τi toward the final collective outcome"; agents observe either the immediate predecessor (partial observation, hᵢᴾᴼ) or the full history hᵢᶠᴼ = {τ₁,…,τᵢ₋₁} *within the same task*; the final score C is "defined as the last agent's contribution." Grep for persistence terms across the whole 2,195-line extraction returns only two hits, both RL bookkeeping - "Store (bᵢ, ς⃗ᵢ, τᵢ) in D" and "Store (Rᵢ, Aᵢ) in D" - i.e. a training replay buffer, not a retrievable knowledge artifact consumed by future tasks. **MAC-SPGG has no persistent artifact, no retrieval, and no cross-task reuse.** That adjacency is genuinely weaker than it looks, and this is the one place the candidate's instinct was right.

**EquiMem: Calibrating Shared Memory in Multi-Agent Debate via Game-Theoretic Equilibrium (arXiv 2605.09278, 10 May 2026) - NEW, and the closest LLM-side work.** Read in full. Verbatim from the abstract:

> "We address this gap by formulating memory updating in MAD as a zero-trust memory game, in which no agent is assumed honest and the game's equilibrium serves as an indicator of optimal memory trust."

From §3 of the same PDF: "no agent's contribution to memory M is assumed honest. Agents iterate between two roles: a contributor who writes reasoning traces with factual claims into M, and auditors who inspect those contributions"; "The contributor a_c may craft Δt to advance a private objective u_c misaligned with…"; and "at equilibrium, a contributor cannot raise an…". It is a two-stage game with explicit contributor/auditor utility functions, an equilibrium result, evaluation across benchmarks, MAD frameworks and both embedding- and graph-based memory, and robustness under adversarial agents. Differences from the candidate: memory persists across *debate rounds*, not across tasks as a reusable skill library; and the mechanism is inference-time *filtering/calibration*, not a *payment* scheme. But "strategic contributors writing to a shared LLM memory, equilibrium analysis, downstream task evaluation" is already published.

**SkillOps (arXiv 2605.13716, 13 May 2026) - read in full; owns the *non-strategic* pollution result.** It names "skill technical debt": "persistent defects in a skill library, such as redundancy, missing validation, interface drift, or stale implementations, that may not break a single skill locally but can reduce future retrieval, composition, and execution reliability." Grep for `incentiv|strateg|game|equilibri|free.rid|mechanism design` across the full extraction returned **zero hits**. So the degradation phenomenon in a persistent skill pool is established engineering; only the strategic reading is missing. Related: library drift below the no-skill baseline absent outcome-driven retirement (GRASP, arXiv 2605.29668); "Regulating experience quality within the memory bank… future task evaluations can serve as free quality labels for stored memory" is already the stated design principle in the experience-memory line (Skill-Pro 2602.01869, Experience Compression Spectrum 2604.15877, RoMeRL 2608.02508) - which is *usage-based quality attribution*, already implemented, just not called a payment.

**Also relevant, previously unlisted:** "State Contamination in Memory-Augmented LLM Agents" (arXiv 2605.16746); "Governed Shared Memory for Multi-Agent LLM Systems" (arXiv 2606.24535, four named failure modes incl. provenance collapse); "Corrupted by Reasoning: Reasoning Language Models Become Free-Riders in Public Goods Games" (arXiv 2506.23276) - LLMs *do* free-ride in PGGs, which cuts against the candidate's prediction that they won't withhold.

**Memory-R2 (arXiv 2605.21768) - checked and dismissed.** Despite "Fair Credit Assignment" in the title, it is single-agent training-time credit assignment for memory writes under group-relative policy optimization. No game theory, no free-riding, no mechanism design. Not an adjacency.

---

## Evidence table: nearest work

| Work | Year | What it owns | Overlap with candidate | Access |
|---|---|---|---|---|
| Ghosh & McAfee, WWW 2011 | 2011 | Free-entry NE over *both* quality and participation; "flood of low quality" under quality-independent exposure; elimination mechanism → optimal quality | **Headline prediction + mechanism claim, entire** | Full PDF read |
| Ghosh, SIGecom Exchanges 11(2) | 2012 | Survey; rank-order > proportional; flat "best-contribution" reward analysis | Candidate's related-work section, pre-written | Full PDF read |
| Hu, Jagadeesan, Jordan & Steinhardt, 2306.07479 | 2023/24 | Learned *ranker* shapes producer effort; Hedge/EXP3 drive effort → 0; corrective algorithms | The retrieval-mediated seam | Full PDF read |
| Hess & Ostrom (eds.), MIT Press | 2007 | Knowledge-as-commons framing; non-rival vs subtractable | Candidate's framing | Publisher + review pages only |
| Xia, Qin, Yu & Liu, AAAI'14 | 2014 | Heterogeneous private contributor types; top-K vs proportional; PNE existence | Heterogeneous-agent version | Full PDF read |
| Jain, Chen & Parkes, EC'09 / GEB | 2009/14 | Best-answer scoring rules; substitutes vs complements | Q&A mechanism design | Abstract only (paywalled) |
| FL incentive survey, 2106.15406 + Shapley line | 2021-24 | Contribution valuation, free-rider detection, model-as-reward | Mechanism + valuation | Survey PDF + abstracts |
| Peer prediction line (MRZ'05 → Shnayder'16) | 2005-16 | Elicitation without verification, informed truthfulness | Default mechanism answer | Secondary + 1605.01021 |
| P2P pollution (Liang'05; Christin EC'05) | 2005 | Decoy insertion, pollution dynamics, reputation defenses in a shared retrievable pool | Pollution equilibrium, structurally identical | Abstracts + 1108.1343 |
| Royalty vs fixed fee / Holmström | 1979- | Output-contingent > fixed pay under moral hazard | "Usage-based beats flat" | Secondary + MnSc/NBER pages |
| **EquiMem, 2605.09278** | 2026 | **Zero-trust memory game; contributor/auditor utilities; equilibrium; LLM downstream eval** | **Closest LLM-side work; not previously found** | Full PDF read |
| SkillOps, 2605.13716 | 2026 | Skill technical debt; library-time maintenance | Pollution phenomenon, non-strategic | Full PDF read |
| MAC-SPGG, 2508.02076 | 2025 | Sequential PGG over per-episode contributions | **No persistence, no retrieval — weaker than feared** | Full PDF read |

---

## What specifically survives

Phrased as a claim a reviewer would accept:

> *Nothing survives at the level of model or prediction.* The one defensible residual is narrowly empirical and must be pitched as a measurement paper, not a theory paper: **"We instantiate the Ghosh-McAfee free-entry quality/participation equilibrium in a persistent, retrieval-mediated LLM experience pool and measure whether real LLM contributor agents reproduce the predicted corner solution (effort → minimum under quality-independent reward), given that here the attention allocator is a learned embedding retriever rather than a designer-controlled display rule, and quality is revealed only through delayed, noisy, endogenously-selected downstream task outcomes."**

Even that is thin, because (a) Hu et al. 2306.07479 already analyzes the learned-allocator case theoretically, (b) EquiMem already runs the strategic-contributor-to-shared-memory experiment with real LLM agents, and (c) a negative empirical result ("LLM agents do not reproduce the equilibrium") is more publishable here than a positive one, which would just be a simulation confirming a 2011 theorem.

The single genuinely uncovered structural feature, if you want one thing to build on: **retrieval-induced selection on the harm.** In UGC the designer chooses exposure; in an experience pool a *k*-NN retriever chooses it, and a low-quality entry only causes damage when it wins retrieval - so pollution cost is endogenous to embedding-space crowding, and an entry can be harmful precisely because it is *semantically well-placed but procedurally wrong*. That is a different externality from "junk floods the front page," and it is not what Ghosh-McAfee or Hu et al. model. It is a small paper, not a headline.

## Ranked risks

1. **(Fatal) Headline is a 2011 theorem.** A reviewer who knows the UGC-economics literature will cite one abstract sentence and desk-reject. The 2010-experimental-economics trap has recurred exactly, one venue over.
2. **(Fatal) "Usage-based beats flat" is textbook contract theory.** Presenting it as a finding signals the authors did not read outside their subfield.
3. **(Severe) EquiMem (May 2026) already did the LLM-side version.** Strategic writers, shared memory, explicit game, equilibrium, LLM downstream eval. This must be the primary baseline, and the delta ("payment mechanism, cross-task reuse" vs "inference-time filtering, within-debate") is narrower than a headline needs.
4. **(Severe) FL incentive design will be the reviewer pool's baseline.** Shapley/leave-one-out contribution valuation with free-rider detection is a mature, deployed answer. Any usage-count reward must beat it, and usage count is a strictly weaker signal than marginal contribution.
5. **(Moderate) Peer prediction pre-empts the unverifiable-quality escape hatch.** If you argue quality cannot be checked at write time, MRZ/Dasgupta-Ghosh/Shnayder is the answer and you must implement it as a baseline. If you argue it *can* be checked downstream, you are in ordinary delayed-signal contract theory.
6. **(Moderate) P2P pollution literature makes the "pollution equilibrium" contribution look like a rediscovery** with a reputation-system defense already characterized.

## Modeling flaws in the candidate

1. **The commons metaphor is the wrong one, and Hess & Ostrom already said why.** An experience pool is non-rival in *storage* but sharply rival in *retrieval slots* (top-k). It is a congestion/attention commons, not a subtractable CPR. Ostrom's eight design principles are for appropriation from a depletable stock and transfer poorly. Leading with "commons" invites the reviewer to correct you using the very book you cite.
2. **"Valid-but-suboptimal" is not a sharp prediction; it is the generic corner solution, and the classical model is sharper.** Ghosh-McAfee gets equilibrium quality pinned at exactly 0 (minimum admissible effort) under quality-independent reward, not "suboptimal." Predicting something weaker than a 2011 paper predicted is not a contribution.
3. **Where do the agents' preferences come from? The strategic premise may be vacuous.** Free-riding requires (a) a private effort cost the contributor bears and (b) a payoff the contributor values and can trade off. In almost every deployed agent system a single principal owns every agent and pays every token bill, so there is no strategic conflict - only a misspecified objective, which is an alignment/credit-assignment problem, not mechanism design. The candidate needs to commit up front to a genuine multi-principal setting (agents from different vendors/tenants sharing a pool) or the entire game collapses to SkillOps-style library maintenance, which is already solved and already published.
4. **Usage-based payment is gameable in exactly the way the candidate's own framing predicts.** Retrieval count is manipulable by embedding-space SEO - keyword/paraphrase stuffing to win *k*-NN without being useful. Hu et al. show the learned allocator itself drives effort to zero; the lemons-signal-collapse review shows cheap signals collapse the separating equilibrium. So "usage-based" is not only unoriginal, it is the *attackable* option, and a reviewer will ask for the manipulation analysis.
5. **The verification timing is unstated and it determines which whole literature applies.** Write-time unverifiable → peer prediction. Downstream-verifiable-with-delay → contract theory with a noisy signal, plus a credit-assignment problem when several retrieved entries jointly produce one outcome (that joint-attribution problem is Shapley, i.e. FL again). Pick one explicitly; the candidate currently straddles both and therefore inherits both literatures' priors.
6. **Empirical direction risk.** "Corrupted by Reasoning" (2506.23276) finds reasoning LLMs *do* free-ride in public goods games, directly contradicting the candidate's "agents don't withhold." The prediction may be empirically wrong as well as unoriginal.

---

## Verbatim queries that returned nothing usable

These are the exact strings issued; each returned only generic memory-architecture or unrelated results, with no strategic/mechanism-design work on a persistent LLM experience pool:

- `"shared memory" OR "experience pool" multi-agent LLM "mechanism design" contribution incentive commons tragedy write access strategic` - returned memory-architecture surveys only (AI Hippocampus 2601.09113, Always-On Agents 2606.30306, MaaS 2506.22815); no mechanism design. Search-summary conclusion, quoted: "focus more on technical architectures rather than mechanism design approaches to address tragedy of the commons scenarios or strategic contribution incentives."
- `"experience pool" LLM agents "free-riding" contribution mechanism "usage-based" reward retrieval count` - returned experience-replay papers (ExpeL, Memex(RL), Skill-Pro) with reward-*ranked* retrieval but no contributor incentives; only free-riding hit was the unrelated PGG paper 2506.23276.
- `agentic memory commons "strategic contributors" pollution equilibrium mechanism downstream task utility LLM benchmark` - no work under this framing; surfaced EquiMem incidentally.
- `"peer prediction" mechanism for LLM agent memory contribution quality shared knowledge base agents mechanism design 2026` - **no paper applies peer prediction to LLM agent memory contributions.** This is the one genuinely empty cell found.
- `LLM agent skill library experience pool degradation low quality memory accumulation retrieval harms performance non-adversarial` - all hits (SkillOps, GRASP, SkillLens, Skill-Pro) are engineering/maintenance; zero strategic framing (confirmed by zero-hit grep on SkillOps full text for `incentiv|strateg|game|equilibri|free.rid|mechanism design`).
- `software reuse repository incentives contributors "market for lemons" knowledge repository adverse selection quality signal` - no classical software-reuse-repository incentive paper surfaced; only the 2026 software-supply-chain review. The 1990s reuse-library incentive literature, if it exists, was not reachable by this query.

Access failures to record honestly:
- `http://www.arpitaghosh.com/papers/nberfr320-ghosh.pdf` - TLS handshake failure (`SSL routines:TLSV1_ALERT_INTERNAL_ERROR`); obtained the same paper from `https://www.mcafee.cc/Papers/PDF/UGC.pdf` instead and read that version.
- Hess & Ostrom (2007) full book - not accessed; publisher and review pages only.
- Jain-Chen-Parkes journal version (GEB 2014) - paywalled at ScienceDirect; abstract only.
