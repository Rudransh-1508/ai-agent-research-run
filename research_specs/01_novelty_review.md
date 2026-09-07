# Novelty / Prior-Art Review: Regret-Grounded Evaluation of LLM Agent Teams

Reviewed 7 September 2026. Adversarial review: the goal below was to falsify the novelty claim, not to support it.

## Verdict

**Gap is open, but narrower than the spec states.**

I could not find any paper that evaluates LLM agent teams against a *computed decentralized* optimum V*_Dec, and I could not find any paper that reports the two-way decomposition (V*_Cent - V*_Dec) vs (V*_Dec - V_LLM). Every close competitor stops at a centralized/full-information oracle or at a solo-agent baseline. However, three things the spec treats as novel are already occupied: (a) the *name and concept* of decentralization loss for LLM teams is claimed by [The Collaboration Tax](https://arxiv.org/abs/2608.22152) (EMNLP 2026) and [The Interaction Tax](https://arxiv.org/abs/2608.23541); (b) *normalized reward against a solver-computed full-information optimum* for LLM teams under partial observability is already published in [arXiv:2607.06157](https://arxiv.org/abs/2607.06157); and (c) the centralized-minus-decentralized gap for LLM architectures is already formalized theoretically in [arXiv:2603.26993](https://arxiv.org/abs/2603.26993). The residual defensible contribution is the *decentralized* half of the reference pair plus Mode B (exact evaluation of LLM-synthesized decentralized controllers) - not "optimum-grounded evaluation" in general.

---

## Evidence table

| Paper | Venue / year | Link | What it actually measures | Overlap with the proposal |
|---|---|---|---|---|
| The Collaboration Tax: How Much LLM Multi-Agent Systems Pay to Coordinate (Sun, Wang, Huang, Nelson, Ma, Ye) | EMNLP 2026; arXiv Aug 2026 | [arXiv:2608.22152](https://arxiv.org/abs/2608.22152) | "Collaboration tax" = **team-decentralisation loss** on 32 *solo-tractable* tasks, 11 models, 7 providers. Comparator is **the same model working alone**, not any computed optimum. Diagnoses a four-stage conversational cascade; prompt intervention recovers part of the gap. Verified by extracting the PDF text directly. | Owns the framing "coordination loss is measurable". Its oracle is solo performance. **No Dec-POMDP, no sequential horizon, no V*_Dec, no V*_Cent, no decomposition.** Directly supports the spec's "different oracle" defense - but also means the motivating slogan is taken. |
| LLM Agents for Deliberative Collaboration: Joint Decision Making Under Partial Observability (Wang, Yang, Du, Lin, Liu - Tsinghua/Fuzhou) | arXiv Jul 2026 | [arXiv:2607.06157](https://arxiv.org/abs/2607.06157) | **The single most dangerous paper.** Menu-Design (numeric + semantic) and Task-Allocation tasks with partial, asymmetric observations. Metric is **Normalized Reward = R_final / R_max**, where R_max is "the maximum possible reward computed by the integer programming solver" given the ground-truth full state. Includes an explicit **Centralized Baseline** (one agent gets all merged observations) and an **Oracle Baseline** (deliberation + full observations). | Already does: solver-computed optimum as denominator; centralized ceiling; normalized regret; LLM-team evaluation under partial observability; centralized-vs-decentralized contrast. Does **not** do: any sequential Dec-POMDP (tasks are one-shot combinatorial optimization), any *decentralized* optimum, or the two-way decomposition. Its R_max **is** V*_Cent, so its "normalized regret" conflates the spec's two terms. |
| The Interaction Tax: When Communication Erases Diversity in Multi-Agent Teams | arXiv Aug 2026 | [arXiv:2608.23541](https://arxiv.org/abs/2608.23541) | Communication causes proposal convergence within one round, erasing ensemble diversity. Measures team vs. information exchanged. | Same "tax" naming space. No formal optimum. Relevant to H3 (dialogue is not free) but not a novelty threat to the measurement instrument. |
| On the Reliability Limits of LLM-Based Multi-Agent Planning | arXiv Mar 2026 | [arXiv:2603.26993](https://arxiv.org/abs/2603.26993) | Decision-theoretic analysis of multi-agent LLM architectures as a **finite acyclic decision network**. Characterizes the loss from communication and information compression as a gap between the **centralized Bayes value** and the value under communication constraints, via conditional mutual information / expected posterior divergence. Theory plus LLM experiments on a controlled problem set. | **Formalizes the price-of-decentralization idea for LLM systems already.** The spec's "intrinsic decentralization cost" is conceptually anticipated here. Differs: no Dec-POMDP, no computed V*_Dec, no benchmark suite, no policy synthesis. The proposal must cite this and cannot claim first formalization of the centralized-vs-decentralized LLM gap. |
| Language Model Teams as Distributed Systems | arXiv Mar 2026 | [arXiv:2603.12229](https://arxiv.org/abs/2603.12229) | Team-vs-single-agent effectiveness, team size, structural configuration; reports decentralized teams achieving 0.88x median speedup vs 1.36x for preassigned teams. | Single-agent baseline only, no formal optimum. Weak threat. |
| The price of decentralization in managing engineering systems through MARL | arXiv Mar 2026 | [arXiv:2603.11884](https://arxiv.org/abs/2603.11884) | Benchmarks MADRL against **centralized (near-)optimal policies** in POMDP maintenance-planning environments deliberately built so centralized optima stay tractable. Studies redundancy vs optimality loss. | **Owns the term "price of decentralization" and the methodology** - but for MARL, not LLMs, and against a centralized optimum only. The spec should either rename the quantity or cite this explicitly. |
| Benchmarking Open-Ended Multi-Agent Coordination in Language Agents (ALEM) | arXiv Jun 2026 | [arXiv:2606.08340](https://arxiv.org/abs/2606.08340) | JAX/Craftax-like open-ended coordination benchmark; 13 LLMs zero-shot; **reference points are MARL agents trained for 1B steps**; LLMs average ~6% normalized return. | Uses "normalized return" but the reference is a trained MARL policy, an empirical not an optimal ceiling. Complementary, not overlapping. |
| LLM-Coordination (Agashe, Fan, Reyna, Wang) | Findings of NAACL 2025, pp. 8053-8072 | [ACL Anthology](https://aclanthology.org/2025.findings-naacl.448/) / [arXiv:2310.03903](https://arxiv.org/abs/2310.03903) | Four pure coordination games, Agentic Coordination + CoordinationQA (198 MCQs) over Environment Comprehension, ToM, Joint Planning. Zero-shot-coordination robustness to unseen partners. | **No formal optimum reported anywhere.** Confirms the spec's characterization. Good motivating citation. |
| DICE: Entropy-Regularized Equilibrium Selection for Stable Multi-Agent LLM Coordination | arXiv Jun 2026 | [arXiv:2606.08068](https://arxiv.org/abs/2606.08068) | Convention selection / oscillation; notes systems saturating at a "single-agent ceiling". | Equilibrium selection method, not optimum-grounded measurement. |
| MAGRPO / Learning to Deliberate (meta-policy Dec-POMDP framing for LLMs) | arXiv 2509.03817 and related | [arXiv:2509.03817](https://arxiv.org/html/2509.03817v2) | Formalizes multi-LLM collaboration as a Dec-POMDP and trains decentralized policies with CTDE on writing/coding benchmarks. | Confirms Dec-POMDP notation is already routine for LLM teams (the spec correctly concedes this). It is a *training* method with no computed optimum on any benchmark with a known V*. |
| Dibangoye, Amato, Buffet, Charpillet - Optimally Solving Dec-POMDPs as Continuous-State MDPs (FB-HSVI) | JAIR 55:443-497, 2016 | [JAIR](https://jair.org/index.php/jair/article/view/10986) | Exact finite-horizon Dec-POMDP solver with published optimal values. | The instrument's source of truth. Classical, no LLM component - the spec is right not to claim novelty here. |
| Inductive Synthesis of FSCs for POMDPs; Search and Explore; Synthesizing POMDP Policies (sampling + model checking) | arXiv 2203.10803, 2305.14149, [2605.14440](https://arxiv.org/html/2605.14440) | links inline | Formal-methods synthesis of finite-state controllers with model-checking oracles and counterexample guidance. | The **counterexample-guided repair loop is a standard formal-methods pattern**. Novelty of Mode B/method version lies only in the LLM being the synthesizer. Searched specifically for "LLM synthesize finite-state controller Dec-POMDP" - **found nothing**; all synthesis work is non-LLM. |

---

## Nearest prior work (narrative)

**1. arXiv:2607.06157 - LLM Agents for Deliberative Collaboration.** This is the closest, and it is close enough to require an explicit rebuttal paragraph in any submission. I read the PDF rather than trusting a summary, because the automatic summarizer falsely claimed the paper had "decentralized optimal baselines" - it does not. What it actually has: tasks whose ground-truth optimum is an integer program solvable to optimality given full state; a Normalized Reward metric `NR = R_final / R_max * 100`; a centralized baseline where a single agent receives perfectly merged observations; and a further oracle baseline with deliberation plus full observations. Results (GPT-5.1, DeepSeek-V3.2, GLM-4.7, GPT-4.1-mini, Qwen3 family) show large decentralized-vs-centralized gaps, e.g. GPT-5.1 Menu-Semantic 55.95 NR deliberative vs 90.67 centralized. **Therefore "LLM teams measured as normalized regret against a solver-computed optimum, with a centralized ceiling" is published prior art.** What survives: their tasks are one-shot joint decisions, not sequential Dec-POMDPs; there is no policy object, no local observation history, no horizon, no V*_Dec, and consequently their NR gap *is* the sum of the spec's two terms with no way to separate them. That inseparability is precisely the spec's stated motivation - which is now a demonstrated, published deficiency rather than a hypothetical one. That is arguably good for the proposal, but the framing must change from "nobody grounds LLM teams in an optimum" to "existing optimum-grounded LLM evaluation uses the wrong optimum."

**2. arXiv:2608.22152 - The Collaboration Tax (EMNLP 2026).** Verified real; arXiv ID resolves; the PDF text confirms authors (Notre Dame / Meta Superintelligence Labs / SFU) and the abstract. It defines the collaboration tax as "the team-decentralisation loss of a two-player cooperative game with private information", with two propositions on its sign and equivalence to a max-superadditivity violation, measured on 32 solo-tractable tasks across 11 models. The comparator is the model acting alone. This is a *capability-relative* baseline, not an *environment-relative* one, so a strong model and a weak model are measured against different yardsticks - the exact defect the spec's V*_Dec fixes. The spec's characterization of this paper is accurate. The cost is that the vocabulary of "coordination loss for LLM teams" is now branded, and reviewers will ask how this differs.

**3. arXiv:2603.26993 - Reliability Limits of LLM-Based Multi-Agent Planning.** The under-appreciated threat. It gives a decision-theoretic characterization of the gap between a centralized Bayes decision maker and a decentralized, communication-limited LLM network, using conditional mutual information and expected posterior divergence, with confirming LLM experiments. In other words, the *theoretical* content of "intrinsic price of decentralization for LLM teams" exists. The proposal's differentiator must be that this paper works on a finite acyclic decision network with an information-theoretic bound, whereas the proposal computes exact V*_Dec on sequential Dec-POMDPs and measures a real LLM against it. That is a real difference, but it is a difference of instrument, not of concept.

**4. arXiv:2603.11884 - The price of decentralization (MARL, engineering systems).** This paper independently invented the spec's headline phrase and its methodology: build environments where centralized optima remain tractable, then measure how far decentralized learners fall. It is not about LLMs and does not compute a decentralized optimum. Using the phrase "price of decentralization" without citing this will look careless.

**5. FB-HSVI (JAIR 2016) and the POMDP-synthesis line (2203.10803, 2305.14149, 2605.14440).** These bound the classical half. FB-HSVI supplies the reference values; the synthesis line already established counterexample-guided, model-checked controller synthesis. The method-paper framing ("solver-verified synthesis with counterexample-guided local repair") is therefore a *transfer* of an established formal-methods loop to an LLM synthesizer. Defensible, but it should be pitched that way rather than as a new algorithmic idea.

---

## Citation audit

| Spec citation | Status | What it actually is |
|---|---|---|
| arXiv:2608.22152 - "The Collaboration Tax (2026)" | **VERIFIED** | "The Collaboration Tax: How Much LLM Multi-Agent Systems Pay to Coordinate", Sun, Wang, Huang, Nelson, Ma, Ye (Notre Dame / Meta Superintelligence Labs / SFU). Submitted 23 Aug 2026, **accepted to EMNLP 2026**. Not a hallucinated ID. Its oracle is the **solo single-model baseline** on solo-tractable tasks, exactly as the spec assumes. |
| arXiv:2310.03903 - "LLM-Coordination (2025)" | **VERIFIED, year needs care** | Agashe, Fan, Reyna, Wang. arXiv v1 Oct 2023; published as [Findings of NAACL 2025, pp. 8053-8072](https://aclanthology.org/2025.findings-naacl.448/). Cite the NAACL Findings version. **Reports no formal optimum** - the spec's claim holds. |
| Oliehoek & Amato, *A Concise Introduction to Dec-POMDPs* | **VERIFIED** | [Springer](https://link.springer.com/book/10.1007/978-3-319-28929-8). |
| Bernstein et al. 2002, complexity of decentralized control | **VERIFIED (not independently re-fetched)** | DOI 10.1287/moor.27.4.819.297, Math. of OR. I did not open the paywalled DOI; the citation is standard and uncontroversial. **Flagged as not directly verified.** |
| Dibangoye et al. 2016, FB-HSVI | **VERIFIED** | "Optimally Solving Dec-POMDPs as Continuous-State MDPs", JAIR 55:443-497, 2016. PDF downloaded and result tables read directly. |
| Wu et al. 2017, IJCAI | **VERIFIED** | [Multi-Agent Planning with Baseline Regret Minimization, IJCAI 2017, p. 0063](https://www.ijcai.org/proceedings/2017/0063.pdf). Title confirms the "regret" usage the spec wants to disambiguate from. |
| AAMAS 2027 CFP page | **VERIFIED** | See below. |
| FAST @ NeurIPS 2026 page | **VERIFIED** | See below. |
| NeurIPS 2026 Resource-Aware Agentic AI (29 Aug 2026 deadline) | **NOT RE-CHECKED** | Not fetched this session; spec already treats it as expired. Flagged. |

---

## Feasibility of the instrument

**Yes - buildable, and the reference values are already published and free.** I downloaded the FB-HSVI JAIR PDF and read Tables 4 and 5 directly. Reported values are epsilon-optimal expected cumulative reward at the initial occupancy state, `L_0,M(xi_0)`:

| Domain | Largest horizon with an exact value in FB-HSVI | Sample values |
|---|---|---|
| Dec-Tiger (multi-agent tiger) | **T = 10** | T2 = -4.00, T3 = 5.1908, T4 = 4.8027, T5 = 7.0264, T6 = 10.381, T10 = 15.184 |
| Recycling Robots | **T = 100** | T2 = 7.000, T3 = 10.660, T4 = 13.380, T5 = 16.486, T10 = 31.863, T100 = 308.78 |
| Meeting in a 3x3 Grid | **T = 30** | T2 = 0.0, T3 = 0.133, T5 = 0.894, T10 = 4.68, T30 = 24.33 |
| Broadcast Channel (mabc) | **T = 100** | T2 = 2, T3 = 2.99, T5 = 4.79, T10 = 9.29, T100 = 90.76 |
| Grid-Small | **T = 10** | T2 = 0.37, T5 = 2.24, T10 = 6.03 |
| Cooperative Box-Pushing | **T = 10** | T2 = 17.600, T3 = 66.081, T5 = 107.72, T10 = 223.74 |
| Mars Rovers | **T = 10** | T2 = 5.80, T3 = 9.38, T5 = 13.26, T10 = 26.31 |

Source: [JAIR 55 (2016) 443-497, Tables 4-5](https://jair.org/index.php/jair/article/download/10986/26136/20480), pp. 483-484.

Model files: the [MADP Toolbox](https://github.com/MADPToolbox/MADP) ships `problems/` with `dectiger.dpomdp`, `dectiger_skewed.dpomdp`, `broadcastChannel.dpomdp`, `recycling.dpomdp`, `boxPushingUAI07.dpomdp.gz`, `Mars.dpomdp.gz`, `fireFighting_2_3_3.dpomdp.gz`, `fireFighting_2_4_3.dpomdp.gz`, plus grid problems. [MASPlan.org problem_domains](http://masplan.org/problem_domains) is the canonical `.dpomdp` repository - **I could not open it: the site returned a self-signed-certificate error.** Use the GitHub mirror instead.

Two caveats.
- **Fire Fighting has no FB-HSVI optimal-value row.** Its model file exists in MADP but the JAIR tables do not list it among the benchmarked domains (Table 3 lists Dec-Tiger, Grid-Small, Recycling-Robots, Box Pushing, Mars Rovers). Fire Fighting values must be sourced from the earlier GMAA*/Oliehoek line or recomputed. Do not list it as "verified" without that.
- **"Meeting on a Grid" vs "Grid-Small"** are distinct rows in FB-HSVI with different values; the spec must name the exact instance.
- **V*_Cent is the cheap half:** the MPOMDP/centralized ceiling is a finite-horizon POMDP over joint observations, solvable exactly at these sizes. No published-table dependency.

Bottom line: falsification gate #5 in the spec ("references cannot be independently verified") is **cleared** for six of seven named families.

---

## Venue / deadline facts (from official pages)

**[AAMAS 2027 Call for Main Track](https://warwick.ac.uk/fac/sci/dcs/aamas2027/calls/call-for-main-track/)** - all AoE:
- Author registration on OpenReview: **17 September 2026** (the spec omits this; it is a hard gate)
- Abstract submission: **1 October 2026** - matches spec
- Full paper submission: **8 October 2026** - matches spec
- Rebuttal: 20-24 November 2026; notification: 21 December 2026; camera-ready: 25 January 2027; conference: 3-7 May 2027
- **Findings track confirmed**: papers not selected for proceedings are automatically considered for Findings of AAMAS 2027 under CC-BY unless authors opt out; identical length and formatting. Matches spec.
- 11 primary research areas, including Learning and Adaptation, Generative and Agentic AI, Planning/Optimization, and Coordination/Organizations/Norms/Ethics.

**[FAST @ NeurIPS 2026](https://fast-workshop.github.io/)** - Foundations of Agentic Systems Theory, NeurIPS 2026, Paris:
- Deadline **5 September 2026 AoE** - confirmed, and **it has passed as of 7 September 2026**. This option is closed.
- Full papers up to 7 pages, short papers up to 4 pages, excluding references and appendices - matches spec.
- **Non-archival confirmed**: "papers are non-archival but will be given the option to appear on OpenReview", and work under review elsewhere is permitted.

---

## Residual novelty - what actually remains

Defensible after this review:

1. **V*_Dec as the comparator.** No LLM-agent paper found computes or uses an exact *decentralized* optimum. This is the load-bearing claim and it survived every search.
2. **The two-term decomposition on instances where both terms are exactly computable.** 2607.06157 has V*_Cent only; 2603.26993 has the concept but no computed V*_Dec; 2603.11884 has centralized optima but no LLMs. Nobody has all three.
3. **Mode B - exact value of an LLM-synthesized decentralized policy object.** Searched "LLM synthesize finite-state controller / policy tree Dec-POMDP", "LLM Dec-POMDP policy synthesis OpenReview 2026": **found nothing**. All FSC-synthesis work uses inductive/model-checking synthesizers. Evaluating an LLM-emitted controller exactly against the model, with an information-legality check, appears genuinely unoccupied.
4. **The structural sweep (coupling / horizon / observation noise / team size) against exact optima.** No competitor can run this because no competitor has V*_Dec.

Should be dropped or heavily rewritten:

- **"No LLM multi-agent evaluation measures team performance against a computed optimum."** False as written - 2607.06157 does, and 2603.11884 does for MARL. Restate as: *against a computed **decentralized** optimum, with the intrinsic decentralization cost reported separately*.
- **Sole credit for "price of decentralization".** Taken by 2603.11884. Cite it or rename.
- **Sole credit for framing LLM coordination loss as a measurable tax.** Taken by 2608.22152 and 2608.23541.
- **Novelty of counterexample-guided repair.** Standard in POMDP controller synthesis; claim only the LLM-synthesizer transfer.
- **FAST as a venue.** Deadline passed. AAMAS 2027 (17 Sep OpenReview registration, 1/8 Oct) is now the only live target in the spec.

---

## Risks to the novelty claim, ranked

1. **A follow-up to 2607.06157 adds a decentralized optimum before 8 Oct 2026.** Highest risk. That group already has the benchmark, the solver, the centralized baseline, and the NR metric; adding V*_Dec on a sequential task is the obvious next paper. Re-run this check in the week before submission.
2. **Reviewers read the contribution as "2607.06157 plus a second baseline".** The decomposition must carry visible scientific weight (H1/H2 structural results), or the paper reads incremental. The spec already anticipates this with the method-paper upgrade; that upgrade is now close to mandatory rather than optional.
3. **The Dec-POMDP benchmarks are too small to be interesting to an LLM audience.** Dec-Tiger has 2 states and 3 actions. Reviewers may argue the regret measured is about parsing tiny puzzles rather than coordination. Falsification gates 1 and 2 in the spec address this and must be reported prominently, not in an appendix.
4. **Concept priority on the centralized-decentralized gap for LLMs goes to 2603.26993.** Manageable via honest citation, but it removes "we are the first to formalize this" from the abstract.
5. **Naming collision fatigue.** Three 2026 papers use "tax"/"price of decentralization". A fourth entrant needs a distinct metric name; "coordination excess loss" is fine, "price of decentralization" is not.
6. **Fire Fighting reference values are unverified.** Minor and fixable by dropping the domain or recomputing.

---

## Searches run that returned nothing relevant

Recording these explicitly, since absence is evidence here.

- `Dec-POMDP` x (`LLM`, `large language model`, `agent team`, `optimal decentralized policy`) - only Dec-POMDP-as-notation training papers (MAGRPO, LangMARL, Learning to Deliberate, 2512.24609). **No optimum-grounded evaluation.**
- `LLM multi-agent normalized regret optimal policy gap Dec-POMDP evaluation 2026` - regret appears only as online-learning regret (ALIGN 2602.00127, 2511.04594) or negotiation optimality gap (TERMS-Bench 2605.13909). **No Dec-POMDP regret.**
- `LLM synthesize finite-state controller / policy tree Dec-POMDP solver verified` - **nothing**; all hits are non-LLM formal synthesis.
- `LLM agents Dec-Tiger benchmark optimal value comparison` - **nothing**. No LLM paper uses Dec-Tiger at all as far as I can find.
- `LLM translate natural language to POMDP / Dec-POMDP model formal planning verified 2026` - the LLM-as-formalizer literature is **entirely PDDL/LTL/MILP** (survey [2503.18971](https://arxiv.org/html/2503.18971), LLM+P, PDDLCoder 2608.16637, 2603.23844). **No LLM-to-Dec-POMDP formalization found** - Mode C is also unoccupied.
- `"large language model" "Dec-POMDP" optimal policy synthesis OpenReview 2026` - **nothing matching**.
- `AAMAS 2026 proceedings LLM Dec-POMDP optimal coordination benchmark` - AAMAS 2026 has Dec-POMDP papers (IMAS2) and LLM-coordination papers, but **no intersection with computed optima**.

Could not open / unverified:
- [masplan.org/problem_domains](http://masplan.org/problem_domains) - self-signed certificate error.
- The Zero-Shot Coordination Among LLM Agents OpenReview PDF (`openreview.net/pdf/bc2a21...`) - blocked by OpenReview's browser-verification page. Its title suggests ZSC evaluation without formal optima, but **I could not confirm this**; worth a manual check before submission.
- Bernstein et al. 2002 DOI - not opened (paywall), citation accepted on standard grounds.
