# Gap Sweep: Outcome and Decision

Sweep run 7-8 Sep 2026. Corpus: `masamasa59/ai-agent-papers`, ~1,360 entries across 30 files,
traversed in four slices as raw markdown (no summarizer in the enumeration path).
Full slice reports in `_survey/`. Per-candidate adversarial reviews in `*_check.md` / `*_novelty_review.md`.

## Scoreboard: four candidates proposed, four headlines closed

| Candidate | Killed by | Verdict |
|---|---|---|
| Sanctioning under unreliable blame (spec 03) | Grechenig, Nicklisch & Thöni, *J. Empirical Legal Studies* 7(4), **2010** - swept signal accuracy directly, found welfare under noisy punishment = no-punishment at ~0.9 and *below* it at 0.5. Replicated Ambrus & Greiner, *AER* 2012. Closed-form error-rate thresholds already in Glynatsi, Hilbe & Murase, *PLoS Comp Bio* 2025. H3's mechanism owned by Ensign et al., FAT* 2018. | **Retracted** |
| Acceptance-gate manipulation-resistance | PACE (arXiv:2606.08106, Jun 2026) names the acceptor as "the loop's silent weak point", diagnoses it as "a textbook case of adaptive data analysis", ships an e-process gate. Classical: Hardt et al. 2016 strategic classification (NP-hardness), Kleinberg & Kleinberg 2018 delegated search, Manheim & Garrabrant "Adversarial Misalignment Goodhart". | **Closed** |
| The experience commons | Ghosh & McAfee, WWW **2011**: "if exposure is independent of quality, there will be a flood of low quality contributions in equilibrium" - the exact prediction, with equilibrium quality pinned at 0. Usage-contingent reward is their positive result. LLM-side: EquiMem (arXiv:2605.09278) already does the zero-trust memory game. | **Closed** |
| Verifier panels vs. strategic persuader | Kaniovski 2008, Corollary 1.4: non-monotonicity of panel competence in size from *correlation alone*, closed form, no adversary. Feddersen & Pesendorfer, *APSR* 1998: "the probability of convicting an innocent defendant may actually increase with the size of the jury." Heese & Lauermann 2021 already stages a Bayesian persuader against a voting body. | **Headline closed** |

## The pattern, which is the real finding

Every dead candidate had the same shape: **import an AAMAS-native concept (reputation, sanctioning,
mechanism design, jury aggregation, commons governance) into LLM agents.** That shape is maximally
exposed, because the concept carries 30-50 years of prior results that an LLM-agent paper corpus
structurally cannot surface. A 2010 economics experiment was never going to appear in a curated list
of 2024-2026 arXiv agent papers.

Three compounding failure modes observed:

1. **Corpus-shaped blindness.** Searching the LLM-agent literature to establish novelty of an
   LLM-agent paper is circular. The classical check must run *before* the recommendation, not after.
2. **Agent convergence is not evidence.** Two independent agents converged on the experience commons.
   Both were searching the same corpus, so convergence measured a shared blind spot.
3. **Unverified quotes.** Two probable fabrications surfaced during this sweep, one load-bearing for a
   candidate. Every quote used in a novelty argument must be extracted from the source document.

## A structural critique that kills a whole class of ideas

Free-riding, misreporting, and strategic contribution all require a private cost and a payoff the
contributor values. **In nearly every deployed LLM agent system, one principal owns every agent and
pays every token bill.** There is no conflict of interest, only a misspecified objective - that is
credit assignment, not mechanism design. Any incentive-theoretic proposal must commit up front to a
genuine multi-principal setting (agents from different vendors, or a real open marketplace) or it is
vacuous. This alone disqualifies a large fraction of "apply game theory to LLM agents" ideas.

## Decision: return to spec 01, method version

`01_regret_grounded_llm_teams.md` is the only proposal in this repo that has **survived** an
adversarial novelty review (`01_novelty_review.md`: gap open but narrower than claimed).

It is also structurally resistant to the failure mode that killed everything else. Its shape is not
"import a classical concept" but **"use a classical solver as a measuring instrument for LLM agents."**
The classical half is explicitly acknowledged as classical - the spec already instructs that no novelty
be claimed in the solver component - so there is far less surface for a 1998 theorem to land on.

What survived its review:
- **V\*_Dec as comparator.** No LLM-agent paper computes or uses an exact *decentralized* optimum.
- **The two-term decomposition** on instances where both terms are exactly computable.
- **Mode B**: exact evaluation of an LLM-synthesized decentralized controller. Searched hard, found nothing.
- **Mode C**: LLM-to-Dec-POMDP formalization. The LLM-as-formalizer literature is entirely PDDL/LTL/MILP.

What must be dropped: the claim that no LLM evaluation is optimum-grounded (arXiv:2607.06157 does it
with a *centralized* optimum), sole credit for "price of decentralization" (arXiv:2603.11884), and
sole credit for framing coordination loss as a measurable tax (arXiv:2608.22152).

Instrument confirmed buildable: exact optimal values transcribed from the FB-HSVI JAIR tables
(Dec-Tiger to h=10, Recycling Robots and Broadcast Channel to h=100, Meeting-in-3x3-Grid to h=30,
Box Pushing / Mars Rovers / Grid-Small to h=10); model files in the MADP GitHub repo. Drop Fire
Fighting (no FB-HSVI optimal-value row).

## Timeline reality

- **17 Sep 2026** - OpenReview author registration. Hard gate, independent of everything else.
- **1 Oct** abstract, **8 Oct** paper. Three weeks. Tight but feasible *because* the reference values
  are published and the pilot (Dec-Tiger + Recycling Robots, two prose renderings, machine-checked
  parsing) needs no training compute.
- **Fallback: Blue Sky Ideas track**, 4 pages, no experimental results required, abstract 5 Nov /
  paper 12 Nov 2026.
- Before submitting, re-run the check on arXiv:2607.06157's group. They hold the benchmark, solver,
  centralized baseline and NR metric; adding V\*_Dec is their obvious next paper.
