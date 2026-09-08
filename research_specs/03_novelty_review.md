# Adversarial Prior-Art Review: "Sanctioning Under Unreliable Blame"

Reviewer stance: falsification. Date of review: 2026-09-08.
Target spec: `03_sanctioning_under_unreliable_blame.md`.

---

## Verdict

**Gap is partially closed - and the specific part that is closed is the headline result.**

RQ1/H1 as stated is not new. Two published, primary-source experiments already establish that a sanctioning mechanism driven by a noisy signal of who defected produces *lower* welfare than no sanctioning at all, and they already bracket the threshold: Grechenig, Nicklisch & Thöni (2010, *JELS*) show welfare at signal accuracy 0.9 equals the no-punishment benchmark and welfare at accuracy 0.5 falls *below* it; Ambrus & Greiner (2012, *AER*) independently show a 10% monitoring-noise rate is already enough to make costly punishment welfare-reducing. That is `a* ≈ 0.9`, published fourteen and sixteen years ago, and it is already "substantially above 0.535." Above that, the general theoretical statement - noisy monitoring forces punishment onto the equilibrium path and bounds attainable welfare strictly below the efficient frontier - is *textbook* material with its own chapter (Mailath & Samuelson 2006, Ch. 7-8: "Punishments Happen", "Strongly Symmetric Behavior Implies Inefficiency", "Bounding Perfect Public Equilibrium Payoffs", "Binding Moral Hazard"), tracing to Green-Porter (1984), Radner-Myerson-Maskin (1986) and Abreu-Pearce-Stacchetti (1990). What survives is narrower than the spec claims: H2 (an *estimated, non-uniform* error kernel from real LLM failure attributors) and H3 (blame-based exclusion losing to random exclusion at matched rate under a directional kernel). H3 is the only claim I could not find a direct precedent for, and even it has a strong structural analogue in statistical discrimination and in runaway-feedback-loop results.

If you write this paper as "we derive `a*` and show it is high," a COINE reviewer who knows the public-goods-under-noise literature will reject it as a rediscovery. Reframe or drop that framing.

---

## The classical-literature verdict

### 1. Repeated games with imperfect monitoring - **decisive; this area closes RQ1's general form**

The mapping the spec worries about is real. "Attribution accuracy" is monitoring quality, and the consequences are classical.

- **Mailath & Samuelson, *Repeated Games and Reputations: Long-Run Relationships*, OUP 2006.** I pulled the official table of contents PDF from Mailath's Penn page ([toc PDF](https://web.sas.upenn.edu/gmailath/files/2017/02/toc-twqxyh.pdf), linked from [the book page](https://web.sas.upenn.edu/gmailath/books/repeated-games-and-reputations/)) and read the section headings directly. Verbatim entries:
  - `7.2.1 Punishments Happen` (p. 233)
  - `7.2.3 Strongly Symmetric Behavior Implies Inefficiency` (p. 239)
  - `7.7.1 Symmetric Inefficiency Revisited` (p. 264)
  - `8 Bounding Perfect Public Equilibrium Payoffs` (p. 273)
  - `8.2 The Inefficiency of Strongly Symmetric Equilibria` (p. 278)
  - `8.3.1 The Upper Bound on Payoffs` (p. 280)
  - `8.3.2 Binding Moral Hazard` (p. 281)
  - `8.4.1 Bounds on Efficiency: Pure Actions` (p. 282) / `8.4.2 Bounds on Efficiency: Mixed Actions` (p. 284)
  - `9.4 Enforceability and Identifiability` (p. 305)

  In other words: an entire textbook chapter on "how far below efficient does noisy monitoring push you", plus a named identifiability condition (Fudenberg-Levine-Maskin) governing when you can tell *who* deviated - which is precisely "attribution." **A reviewer can point at Chapter 8 and say the general result is in a textbook.**

- **Radner, Myerson & Maskin (1986), "An Example of a Repeated Partnership Game with Discounting and with Uniformly Inefficient Equilibria," *Review of Economic Studies* 53(1) - [Maskin's page](https://scholar.harvard.edu/maskin/publications/example-repeated-partnership-game-discounting-and-uniformly-inefficient-equilibr).** The canonical "noisy team monitoring caps welfare away from efficient" result. Note the setting: a *partnership with a common output signal and no individual attribution*. That is structurally your team-failure model.

- **Ely & Välimäki (2003), "Bad Reputation," *QJE* 118(3):785-814 - [author PDF](https://faculty.wcas.northwestern.edu/jel292/badrep6.pdf), [QJE](https://academic.oup.com/qje/article/118/3/785/1943003).** I extracted and read the author-hosted PDF. Verbatim abstract: *"We construct a model where the reputational concern of the long-run player to look good in the current period results in the loss of all surplus. This is in contrast to the bulk of literature on reputations where such considerations mitigate myopic incentive problems. We also show that in models where all parties have long-run objectives, such losses can be avoided."* **This is a "reputation is worse than no reputation" theorem, published 2003.** But the mechanism is *not* yours: surplus is destroyed by the long-run player distorting behavior to separate from a bad type, and the market unravels. It is not noisy blame misallocating sanctions. Cite it as precedent for the *shape* of the claim; it does not scoop the mechanism.

**Does this area answer RQ1?** It answers the qualitative form of RQ1 (yes, monitoring noise bounds welfare and forces costly punishment on path) and it owns the vocabulary. It does *not* hand you a closed-form `a*` for your specific team-formation-with-exclusion model, because the classical setting is deterrence of strategic effort, not screening of fixed latent competence. That distinction is your only defensible line here, and it is thinner than it looks - see "Risks."

### 2. Trust and reputation robust to unfair/noisy ratings - **partially relevant, does not own the threshold**

- **Dellarocas (2000), "Immunizing Online Reputation Reporting Systems Against Unfair Ratings and Discriminatory Behavior," ACM EC'00, pp. 150-157 - [ACM DL](https://dl.acm.org/doi/10.1145/352871.352889), [author PDF](http://ccs.mit.edu/dell/ec00reputation.pdf).** Note the title contains *discriminatory behavior*, so a reviewer will check it. It gives a *robustness range* (mechanisms hold up while unfair raters are roughly ≤20-30% of the population), not a welfare-crossover threshold vs. no-reputation.
- **Teacy, Patel, Jennings & Luck (2006), "TRAVOS: Trust and Reputation in the Context of Inaccurate Information Sources," *JAAMAS* 12(2):183-198 - [Springer](https://link.springer.com/article/10.1007/s10458-006-5952-x), [dblp](https://dblp.org/rec/journals/aamas/TeacyPJL06.html).** Robustness demonstrated up to 50% intentionally misleading sources. Again a robustness range, not a threshold at which reputation becomes net-harmful.
- **Whitby, Jøsang & Indulska (2004), "Filtering Out Unfair Ratings in Bayesian Reputation Systems," Trust in Agent Societies workshop @ AAMAS 2004.** Majority-rule iterative filtering. Assumes the honest majority; no crossover threshold.

**Does this area answer RQ1/H3?** No. I found **no** trust/reputation paper deriving an accuracy below which the reputation system degrades performance *relative to having no reputation system*, and **no** paper in this line showing that non-uniform rating error systematically excludes a *structural class* of agent (as opposed to a strategically-targeted victim). This is the weakest of the six threats. But note the framing trap: the classical robustness numbers (20-30%, 50%) are the numbers a reviewer will compare your `a*` against, and they read as "already known to be around here."

### 3. Peer prediction / elicitation without verification - **not a threat**

Miller-Resnick-Zeckhauser (2005), Prelec BTS (2004), Dasgupta-Ghosh (2013), Shnayder et al. ([EC'16 PDF](https://parkes.seas.harvard.edu/sites/g/files/omnuum8711/files/2025-05/shnayder_ec16.pdf)) are about making truthful *reporting* an equilibrium when there is no ground truth. Your attributor is a mechanical classifier, not a strategic reporter, and your problem is that it is *wrong*, not that it *lies*. Different failure mode. Cite in one sentence; no threat. (Adjacent: Liu & Guo's peer-loss functions carry the peer-prediction idea into noisy-label learning, which is area 5, not area 3.)

### 4. Multiagent credit assignment under noisy credit - **not a threat as prior art, but a gap in your citation plan**

Difference rewards (Wolpert & Tumer; Agogino & Tumer) and COMA (Foerster et al., AAAI'18) are about *constructing* a well-shaped counterfactual credit signal, and their analyses concern learning speed and signal-to-noise in the shaped reward. I found no result of the form "credit-assignment error above rate ρ makes the shaped signal worse than the global team reward baseline." Searches returned nothing on that specific claim. Low risk. You should still cite this line, because "attribution = structural credit assignment" is the obvious reviewer analogy.

### 5. Noisy-label / algorithmic-fairness analogues - **the real threat to H3's mechanism**

This is where I would attack if I were reviewing.

- **Ensign, Friedler, Neville, Scheidegger & Venkatasubramanian (2018), "Runaway Feedback Loops in Predictive Policing," PMLR 81 (FAT* 2018) - [proceedings](https://proceedings.mlr.press/v81/ensign18a.html), [arXiv](https://arxiv.org/abs/1706.09847).** A mathematical model proving that when the detection signal is discovery-biased, enforcement is repeatedly directed back to the same subpopulation *regardless of the true underlying rate*, and a fix that changes the inputs to break the loop. **This is the "biased error kernel causes systematic purging, and here is the correction" result, published 2018, with a proof.** Your H3 differs in that its object is exclusion from a team-formation pool rather than patrol allocation, and in that you compare against *random exclusion at matched rate*. That comparison is the survivable increment - but the causal story is not new.
- **Wang, Liu & Levy (2021), "Fair Classification with Group-Dependent Label Noise," ACM FAccT 2021 - [ACM DL](https://dl.acm.org/doi/10.1145/3442188.3445915), [arXiv](https://arxiv.org/abs/2011.00379).** Corruption rates depending jointly on class and protected-group membership; shows naive parity constraints under heterogeneous error rates *decrease both accuracy and fairness*. This is the disparate-impact-under-a-biased-noise-kernel result in its cleanest form.
- **Statistical discrimination: Phelps (1972); Aigner & Cain (1977), "Statistical Theories of Discrimination in Labor Markets," *ILR Review* 30(2):175-187 - [SAGE](https://journals.sagepub.com/doi/10.1177/001979397703000204), [Wisconsin PDF](https://users.ssc.wisc.edu/~gwallace/Papers/Aigner%20and%20Cain%20(1977).pdf).** The canonical result that a signal whose *noise* differs across groups produces systematically differential treatment even with identical true distributions. If your "structural class of agent" is defined by verbosity or turn position, a reviewer will call H3 "statistical discrimination against verbose agents" and ask what is new.

**Does this area own H3?** It owns the *mechanism*. It does not own the *comparison* (blame-based exclusion vs. random exclusion at matched rate, in a repeated team-formation loop with endogenous competence signal) and it does not own the *inversion* claim (reputation ends up anti-correlated with latent competence). Keep the inversion; drop any language implying the bias-causes-purging insight is new.

### 6. Blockchain / P2P / e-commerce reputation and slashing - **not a threat**

Slashing in proof-of-stake is built on *cryptographic accountability*: the design target is "no honest validator is identified except with negligible probability" (accountable safety with resilience f). Because false accusation is engineered to be negligible, there is no literature on welfare thresholds in false-accusation rates - the question is assumed away. Whitewashing/Sybil analyses concern identity churn, not attribution error. Searched and found nothing usable. Low risk; you can cite this as motivation ("existing sanctioning systems that work assume cryptographic attributability, which LLM traces do not provide").

### 6b. The area the spec does not list, and which is the actual killer: **experimental economics of punishment under noisy monitoring**

This is the section the spec is missing entirely, and it is where the paper dies.

- **Grechenig, Nicklisch & Thöni (2010), "Punishment Despite Reasonable Doubt - A Public Goods Experiment with Sanctions Under Uncertainty," *Journal of Empirical Legal Studies* 7(4):847-867, [doi:10.1111/j.1740-1461.2010.01197.x](https://doi.org/10.1111/j.1740-1461.2010.01197.x).** Wiley returned HTTP 403, so I retrieved the authors' MPI Collective Goods preprint (Bonn 2010/11) and read it directly: [homepage.coll.mpg.de/pdf_dat/2010_11online.pdf](https://homepage.coll.mpg.de/pdf_dat/2010_11online.pdf). Verbatim abstract text:

  > "Interestingly, people reveal a high willingness to punish even if their information about cooperation rates is inaccurate, or noisy. If there is some non-trivial degree of noise, punishment (1) cannot maintain high contributions and (2) reduces welfare even below the level of a setting without punishment. Our findings suggest that sufficient information accuracy about others' behavior is crucial for the efficiency of sanction mechanisms. If a situation is characterized by low information accuracy, precluding sanctions can be optimal."

  Their design, quoted verbatim from the preprint, is *literally your parameter `a`*:

  > "In the P/1 treatment, subjects receive accurate signals about the other group [members' contributions]."
  > "In the P/.9 treatment, the signal is accurate in 90 percent of the cases."
  > "In the P/.5 treatment, the signal is accurate in only 50 percent of the cases (λ=.5)."

  And their welfare result, verbatim:

  > "Compared to the punishment regime under accurate information, the introduction of a minor degree of noise already decreases welfare substantially; welfare is equivalent to that obtained in a game without a punishment mechanism. Introducing a major degree of noise, finally, yields welfare below that obtained in the game without punishment."

  **Read that against the spec's own definitions.** `a* = inf{a : W_s(a) >= W_0}`. GNT locate it empirically: at `a = 0.9`, `W_s ≈ W_0`; at `a = 0.5`, `W_s < W_0`. So `a* ≈ 0.9`. **H1 - "`a*` lies substantially above 0.535" - is already established, in 2010, with human subjects, in a paper whose stated policy conclusion is "precluding sanctions can be optimal" under low information accuracy.** This is the single most damaging citation in this review and the spec does not mention it.

- **Ambrus & Greiner (2012), "Imperfect Public Monitoring with Costly Punishment: An Experimental Study," *AER* 102(7):3317-3332 - [AEA](https://www.aeaweb.org/articles?id=10.1257%2Faer.102.7.3317).** Verbatim abstract, retrieved from the AEA page: *"In a perfect monitoring environment, increasing the severity of the potential punishment monotonically increases average net payoffs. In a more realistic imperfect monitoring environment, we find a U-shaped relationship. Access to a standard punishment technology in this setting significantly decreases net payoffs, even in the long run."* Independent replication of the same qualitative crossover at a 10% misreport rate.

- **Markussen, Putterman & Tyran (2016), "Judicial error and cooperation," *European Economic Review* 89:372-388 - [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0014292116301349).** Type-I and type-II error in formal sanctions against free riders; finds judicial error undermines cooperation and the effects of the two error types are symmetric. (Abstract accessed via search-result rendering; the ScienceDirect full text is paywalled and I did **not** open it. Treat the "symmetric" finding as unverified at primary-source level.)

- **Nicklisch, Putterman & Thöni, "Trigger-Happy or Precisionist? On Demand for Monitoring in a Noisy Social Dilemma Game" (working paper May 2019; published as "Trigger-happy or precisionist? On demand for monitoring in peer-based public goods provision," *Journal of Public Economics*, 2021) - [Brown PDF](https://economics.brown.edu/sites/default/files/papers/Trigger-Happy%20or%20Precisionist.pdf).** I read this PDF directly. Verbatim from their introduction:

  > "Grechenig, Nicklisch, and Thöni (2010) and Ambrus and Greiner (2012) find large increases in 'misdirected' punishment that result in less or even negative effects of punishment opportunities on cooperation, when similar interactions occur under imperfect observability."

  and from their conclusion:

  > "In the absence of affordable remedies, noise sharply increases 'misdirected' punishment and eliminates or even reverses the effects on cooperation of peer punishment opportunities that, with perfect information, often successfully promote it."

  Their contribution - *endogenous, costly improvement of monitoring accuracy* - is also structurally close to your conformal abstention layer (H4): both are "buy or gate on accuracy before you sanction."

- Also in this line: Nicklisch, Grechenig & Thöni (2016), "Information-sensitive Leviathans," *JPubE* 144:1-13; Markussen, Putterman & Wang (2023), "Algorithmic Leviathan or Individual Choice: Choosing Sanctioning Regimes in the Face of Observational Error," *Economica* 90(357):315-338 - [Wiley](https://onlinelibrary.wiley.com/doi/10.1111/ecca.12443). Both study *institutional choice* under observational error, i.e. "given noisy blame, which enforcement regime should we adopt" - which is the governance question the spec claims nobody asks.

### 6c. Indirect reciprocity under noise - **owns the analytic-threshold machinery**

- **Glynatsi, Hilbe & Murase (2025), "Exact conditions for evolutionary stability in indirect reciprocity under noise," *PLoS Computational Biology* 21(10):e1013584 - [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12558610/).** Derives necessary-and-sufficient ESS conditions at *arbitrary* error rates, jointly in assessment error μ, perception error ε, and implementation error μ_e. Representative condition for Stern Judging: `b/c > 1/[(1−ε_DC)(1−μ_e)(1−2μ)]`. **This is a closed-form accuracy threshold for reputation-based cooperation.** It is not your model (donation game, not team formation with exclusion; error is symmetric flip noise, not a structured kernel over co-agents), but it is exactly the object RQ1 promises, in closed form, in a top-tier venue, one year ago. Also: Hilbe, Schmid, Tkadlec, Chatterjee & Nowak (2018), "Indirect reciprocity with private, noisy, and incomplete information," *PNAS* - [PNAS](https://www.pnas.org/doi/10.1073/pnas.1810565115); Fujimoto & Ohtsuki (2023), *PNAS* - [PNAS](https://www.pnas.org/doi/10.1073/pnas.2300544120).

---

## Evidence table

| Citation | Year | Venue | Link | What it proves / measures | What it does NOT cover |
|---|---|---|---|---|---|
| Grechenig, Nicklisch & Thöni, "Punishment Despite Reasonable Doubt" | 2010 | *J. Empirical Legal Studies* 7(4):847-867 | [preprint PDF](https://homepage.coll.mpg.de/pdf_dat/2010_11online.pdf) | Signal accuracy λ ∈ {1, .9, .5}. At λ=.9 welfare ≈ no-punishment; at λ=.5 welfare **below** no-punishment. Concludes low accuracy ⇒ precluding sanctions can be optimal. | Human subjects, not agents. Noise is *uniform* (signal replaced by a uniformly random contribution). Punishment is peer-inflicted cost, not exclusion from team formation. No closed-form `a*`, no error-kernel structure, no conformal gate. |
| Ambrus & Greiner, "Imperfect Public Monitoring with Costly Punishment" | 2012 | *AER* 102(7):3317-32 | [AEA](https://www.aeaweb.org/articles?id=10.1257%2Faer.102.7.3317) | U-shaped severity-welfare relation under noise; standard punishment technology **significantly decreases net payoffs** at 10% misreport probability. | Same limits as above. Symmetric noise. No threshold characterization as a function of accuracy. |
| Nicklisch, Putterman & Thöni, "Trigger-Happy or Precisionist?" | 2019/2021 | *J. Public Economics* | [Brown PDF](https://economics.brown.edu/sites/default/files/papers/Trigger-Happy%20or%20Precisionist.pdf) | Endogenises monitoring accuracy: agents pay to improve information before punishing; restores efficiency. | Not a threshold derivation; no distribution-free guarantee; no biased kernel; humans. |
| Markussen, Putterman & Tyran, "Judicial error and cooperation" | 2016 | *European Economic Review* 89:372-388 | [SD](https://www.sciencedirect.com/science/article/abs/pii/S0014292116301349) | Type-I and type-II sanctioning error undermine cooperation; elicits preference over which error to prevent. | **Paywalled - abstract only, not verified at primary source.** No accuracy threshold; no structured error. |
| Markussen, Putterman & Wang, "Algorithmic Leviathan or Individual Choice" | 2023 | *Economica* 90(357):315-338 | [Wiley](https://onlinelibrary.wiley.com/doi/10.1111/ecca.12443) | Institutional choice between peer / formal / algorithmic sanctioning under observational error. | Human institutional choice; no threshold; no LLM attribution. |
| Mailath & Samuelson, *Repeated Games and Reputations* | 2006 | OUP monograph | [book](https://global.oup.com/academic/product/repeated-games-and-reputations-9780195300796), [TOC PDF](https://web.sas.upenn.edu/gmailath/files/2017/02/toc-twqxyh.pdf) | Ch. 7-9: punishments occur on path under imperfect public monitoring; strongly symmetric behavior implies inefficiency; explicit upper bounds on PPE payoffs; binding moral hazard; enforceability & identifiability conditions. | No welfare comparison to a *no-sanctioning* regime with exogenous types; deterrence of strategic effort, not screening of latent competence; no biased error kernel. |
| Radner, Myerson & Maskin | 1986 | *RES* 53(1) | [Maskin](https://scholar.harvard.edu/maskin/publications/example-repeated-partnership-game-discounting-and-uniformly-inefficient-equilibr) | Repeated partnership with noisy common output has uniformly inefficient equilibria. | Existence/bound result, not a policy comparison; no attribution kernel. |
| Ely & Välimäki, "Bad Reputation" | 2003 | *QJE* 118(3):785-814 | [PDF](https://faculty.wcas.northwestern.edu/jel292/badrep6.pdf) | Reputational concern destroys **all** surplus; market unravels. Precedent for "reputation worse than none." | Mechanism is separating-from-a-bad-type, not noisy blame. Short-run players, no sanctioning kernel, no accuracy parameter. |
| Glynatsi, Hilbe & Murase | 2025 | *PLoS Comput. Biol.* 21(10):e1013584 | [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12558610/) | Exact ESS conditions for reputation norms at arbitrary assessment/perception/implementation error rates; closed-form inequalities in error rates. | Donation game, symmetric flip noise, evolutionary dynamics; no exclusion, no team formation, no biased kernel, no LLM. |
| Ensign et al., "Runaway Feedback Loops in Predictive Policing" | 2018 | PMLR 81 (FAT*) | [PMLR](https://proceedings.mlr.press/v81/ensign18a.html) | **Proves** discovery-biased detection sends enforcement back to the same subpopulation regardless of true rate; gives an input correction. | Resource allocation, not agent exclusion; no matched-rate random baseline; no repeated multi-agent equilibrium. |
| Wang, Liu & Levy, "Fair Classification with Group-Dependent Label Noise" | 2021 | ACM FAccT | [ACM](https://dl.acm.org/doi/10.1145/3442188.3445915) | Group-dependent corruption rates; naive constraints under heterogeneous noise reduce both accuracy and fairness. | Static classification, no sanctioning dynamics, no welfare-vs-no-mechanism crossover. |
| Aigner & Cain | 1977 | *ILR Review* 30(2):175-187 | [SAGE](https://journals.sagepub.com/doi/10.1177/001979397703000204) | Signals with group-dependent noise produce systematic differential treatment. | Labor markets; no dynamics; no mechanism design. |
| Dellarocas | 2000 | ACM EC'00, 150-157 | [ACM](https://dl.acm.org/doi/10.1145/352871.352889) | Immunization against unfair ratings *and discriminatory behavior*; robust to ~20-30% unfair raters. | No welfare crossover vs. no-reputation; adversarial raters, not a biased classifier. |
| Teacy, Patel, Jennings & Luck, TRAVOS | 2006 | *JAAMAS* 12(2):183-198 | [Springer](https://link.springer.com/article/10.1007/s10458-006-5952-x) | Probabilistic trust robust to 50% misleading sources. | Same. |
| Zhang et al., "Which Agent Causes Task Failures and When?" (Who&When) | 2025 | arXiv:2505.00212 | [arXiv](https://arxiv.org/abs/2505.00212) | Verbatim: *"The best method achieves 53.5% accuracy in identifying failure-responsible agents but only 14.2% in pinpointing failure steps, with some methods performing below random."* | Measurement only; no governance consumer. Spec's constant is confirmed at source. |
| Ren et al., RepuNet | 2025/26 | arXiv:2505.05029, AAMAS | [arXiv](https://arxiv.org/abs/2505.05029) | Verbatim: *"driven by direct interactions and indirect gossip, agents form reputations for both themselves and their peers, and decide whether to connect or disconnect other agents for future interactions."* | **Spec's claim is confirmed but only weakly**: the abstract says "direct interactions and indirect gossip", which implies observed outcomes, but the abstract does not state an attribution-error model either way. You must verify against the paper body before asserting "assumes directly observed behavior" in your own text. |
| "Conformal Agent Error Attribution" | 2026 | arXiv:2605.06788 | [arXiv](https://arxiv.org/abs/2605.06788) | Conformal prediction sets over agent trajectories, 80% target coverage, used for automated rollback. | Confirmed: rollback/debugging, not reputation or sanctioning. Your ingredient is genuinely unused for governance. |
| Horibe, Itao & Toyokawa, "Emergence of Reputation-Based Cooperation in LLM Agents" | Aug 2026 | arXiv:2608.04507 | [arXiv](https://arxiv.org/abs/2608.04507) | Indirect reciprocity donation game with LLM agents; robustness driven by defector-exclusion sensitivity. | **Directly observed behavioral traces.** No attribution noise, no threshold. This is a second RepuNet-class adjacency the spec does not list. |
| "Institutional AI: Governing LLM Collusion in Multi-Agent Cournot Markets" | 2026 | arXiv:2601.11369 | [arXiv](https://arxiv.org/abs/2601.11369) | Governance graph with declared sanctions; taxonomy of anti-collusion mechanisms; **explicitly names "the attribution problem" as an open challenge.** | Names the problem, does not solve or quantify it. Useful as a "the field has flagged this" citation - and as evidence someone else is circling it. |
| He et al., "Credibility Governance ... under Weak Truth Signals" | Mar 2026 | arXiv:2603.02640 | [arXiv](https://arxiv.org/abs/2603.02640) | Dynamic credibility scores for agents and opinions; reallocates influence under weak signals. | Reallocation, not sanctioning/exclusion; no accuracy threshold. Nearest LLM-side neighbour on "governance under unreliable signal." |
| Khullar, Hopkins, Wang & Roger, "Self-Attribution Bias" | Mar 2026 | arXiv:2603.04582 | [arXiv](https://arxiv.org/abs/2603.04582) | Monitors underreport risk on actions framed as their own. | **Pre-empts part of RQ2.** Measures the bias; no governance consequence. |

---

## Residual novelty

What a reviewer would accept, stated as one sentence:

> *We estimate the empirical error kernel of state-of-the-art automated failure attributors on annotated LLM multi-agent failure traces, show it is directionally biased with respect to agent role, output verbosity, and turn position, and prove that under such a biased kernel - unlike the uniform noise assumed throughout the existing sanctioning-under-noise literature - blame-driven exclusion is strictly worse than random exclusion at a matched exclusion rate, inverting rather than merely attenuating the competence signal.*

That is H2 + H3 only. It survives because:
1. Every prior noisy-sanctioning result I found (GNT, Ambrus-Greiner, indirect-reciprocity ESS conditions, TRAVOS, BRS) uses **symmetric or uniform** error. Your kernel `E` is the new object.
2. **Nobody has measured the error kernel of an LLM failure attributor.** Who&When reports scalar accuracy; nobody has decomposed *whom* the attributor blames when it is wrong. That measurement is genuinely unpublished and cheap.
3. The **random-exclusion-at-matched-rate** baseline is not standard in either the classical or the LLM literature, and "worse than random" is a sharper, more falsifiable claim than "worse than nothing."

What does **not** survive:
- RQ1 as a novel question. It is the question Grechenig et al. asked in 2010 and answered `a* ≈ 0.9`.
- H1 as a finding. "The threshold is far above attainable accuracy" is a 2010 result plus arithmetic on a 2025 benchmark number.
- "No work asks the obvious governance question that follows" - false as written. Markussen-Putterman-Wang (2023) is literally *institutional choice of sanctioning regime under observational error*.
- The spec's occupancy-table line that classical trust/reputation work "assumes rating noise is exogenous and typically unbiased" is true, but it lets you off too easily: the fatal precedent is not in the trust/reputation literature at all, it is in experimental public-goods economics, which the spec never searched.

---

## What must be dropped or reframed

1. **Drop the thesis sentence "No work asks the obvious governance question that follows."** It is falsifiable in one citation and a reviewer will find it.
2. **Reframe RQ1 from "we define `a*`" to "we transport a known threshold into a setting where the error is structured."** The honest positioning: the *existence* and rough *location* of `a*` is known for symmetric noise; the contribution is what happens when the kernel is directional, and the fact that real attributors have directional kernels.
3. **Demote H1 to a calibration step, not a hypothesis.** Present it as "our model reproduces the known GNT/Ambrus-Greiner crossover near a ≈ 0.9, and we then extend it," which is a *validation asset*, not a claim.
4. **Promote H2/H3 to the headline.** The paper is "attribution error is directional, and directionality is what makes blame worse than a coin flip." Title should be about the *inversion*, not the threshold.
5. **Add a dedicated related-work paragraph on sanctioning under imperfect monitoring in experimental economics** - GNT 2010, Ambrus-Greiner 2012, Markussen et al. 2016/2023, Nicklisch-Putterman-Thöni 2021 - and on Mailath & Samuelson Ch. 8. Omitting these reads as ignorance; citing them and drawing the line reads as command of the field.
6. **Re-examine the model's own construction.** With latent fixed competence `theta_i` and no strategic effort choice, sanctioning is *screening*, not *deterrence*, and the `W_s ≥ W_0` condition may reduce to a classical noisy-test precision-vs-base-rate inequality with a one-line derivation. If it does, the "closed form threshold" contribution is close to trivial and only the biased-kernel extension carries weight. **Check this before week 2, not in week 2.** Consider adding a strategic effort choice so the deterrence channel is present and the model is not a screening problem in disguise.
7. **Verify RepuNet's observation model in the body, not the abstract.** The spec asserts "agents observe behavior directly"; the abstract says "direct interactions and indirect gossip," which is consistent with, but does not establish, that claim.
8. **Add Horibe, Itao & Toyokawa (arXiv:2608.04507) to the occupancy table.** It is a month-old LLM-agent indirect-reciprocity/exclusion paper and the second obvious adjacency after RepuNet.
9. **Cite Khullar et al. (arXiv:2603.04582) under RQ2.** Self-attribution bias in monitors is already measured; your RQ2 must build on it rather than re-derive it.

---

## Risks, ranked

1. **A COINE/GTEP reviewer knows Grechenig et al. 2010 or Ambrus & Greiner 2012 and rejects the paper as rediscovery.** This is now the top risk, and it is higher than the spec's own risk 1 (which pointed at the *wrong* literature - trust/reputation - and would have missed this). The only defense is to cite them explicitly and position against them from the abstract onward.
2. **The `a*` derivation is trivial because the model has no strategic channel.** Fixed `theta_i` + exclusion = noisy screening. If the closed form is "precision exceeds base rate," the formal core is a homework exercise. Test this in the first two days.
3. **H3 fails and the kernel is near-uniform.** Unchanged from the spec, but now load-bearing for the *entire* paper rather than for its strength, because H1 no longer carries anything.
4. **Even if H3 holds, it is read as a known mechanism (statistical discrimination / runaway feedback loops) in a new costume.** Mitigation: the matched-rate random-exclusion comparison and the *inversion* of the competence signal are the parts with no precedent I could find. Lead with those, quantitatively.
5. **Scoop risk on the LLM side is real and rising.** arXiv:2601.11369 explicitly names the attribution problem as an open challenge in governance; arXiv:2603.02640 does credibility governance under weak truth signals; arXiv:2608.04507 does LLM reputation with exclusion. Someone connects attribution accuracy to a governance decision within months.
6. **Conformal abstention (H4) is a straightforward application.** Conformal Agent Error Attribution already produces the sets; gating a decision on set size is standard selective prediction. It is a good engineering contribution and a bad novelty claim. Keep it, do not lean on it.
7. **Attribution accuracy improves and moots the concern.** Unchanged; lowest risk.

---

## Searches run that found nothing

Verbatim queries that returned no usable prior art:

- `"critical accuracy" OR "threshold accuracy" detection mechanism sanctioning welfare improving analytical derivation cooperation monitoring precision recall` - returned engineering/hardware threshold material only; nothing on sanctioning welfare.
- `reputation system threshold rating accuracy below which reputation performs worse than no reputation system analysis` - no paper derives a crossover accuracy vs. a no-reputation baseline.
- `reputation-based exclusion versus random exclusion matched rate comparison noisy trust worse than random selection agents` - no matched-rate random-exclusion baseline found anywhere.
- `difference rewards Wolpert Tumer Agogino noisy credit assignment degrades team performance below baseline multiagent` - no "credit error above ρ is worse than the team baseline" result.
- `slashing mechanism false accusation rate threshold analysis proof-of-stake honest validator wrongly slashed welfare` - no threshold literature; false accusation is engineered to be negligible.
- `peer prediction without verification mechanism noisy signal Dasgupta Ghosh Shnayder Miller Resnick Zeckhauser detection threshold` - peer prediction has no detection-threshold result of this kind.
- `"normative multi-agent systems" norm enforcement imperfect detection monitoring accuracy threshold sanction ineffective AAMAS` - norm-monitoring work covers *cost* of monitoring and detection probability, not a welfare crossover.
- `"failure attribution" LLM multi-agent downstream use reputation trust-weighted routing agent exclusion accuracy insufficient` - **confirms the LLM-side gap**: many new attribution methods (VerifyMAS, StepFinder, DuoTrace, Causal Agent Replay, "Seeing the Whole Elephant"), zero consuming the accuracy number for a governance decision.
- `correlated biased monitoring error sanctioning systematically punishes one type of agent verbosity position bias blame attribution LLM` - LLM-as-judge position/verbosity bias is well documented, but nothing links it to sanctioning or exclusion.

## Access limitations (stated, not guessed)

- **Wiley** returned HTTP 403 for the *JELS* version of Grechenig et al.; I used the authors' MPI Collective Goods preprint (Bonn 2010/11) instead, and all quotes above are from that PDF, extracted locally. The published version may differ in wording.
- **SSRN** blocked direct PDF download (returned HTML).
- **ScienceDirect** full text of Markussen, Putterman & Tyran (2016) is paywalled. I did **not** read it; its characterization above is from search-result rendering and is flagged as unverified.
- **Mailath & Samuelson (2006)** is a print monograph. I read the official table of contents PDF and quote section titles and page numbers verbatim; I did **not** read Chapter 8's theorem statements. Before writing related work, get the book and read §8.3.2 and §8.4 - if a bound there is close to your `a*`, that is a further problem.
- **Ambrus & Greiner (2012)** full text is behind AEA; I quote only the abstract, retrieved from the AEA article page.
