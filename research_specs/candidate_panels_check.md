# Adversarial prior-art check: "Verifier panels against a strategic persuader"

**Date of check:** 2026-09-08. Checker: adversarial (goal = falsify).

---

## Verdict

**partially closed — and the headline is closed.**

Non-monotonicity of majority-vote accuracy in jury size is a known theorem in two separate pre-LLM literatures: Kaniovski's **Corollary 1.4 (2008 working paper; Theory and Decision, 2010)** proves that under positive inter-juror correlation "the effect of larger size on competence is ambiguous, but becomes positive for a sufficiently large size," with an explicit closed form and threshold; and **Feddersen & Pesendorfer, APSR 1998** proved that under strategic voting "the probability of convicting an innocent defendant may actually increase with the size of the jury." So the exact shape you propose to discover — accuracy falls then rises (or just falls) in n — has been on the books since 1998/2008, derived from *both* of your two 2026 ingredients (correlation, and strategic behavior) independently, without needing each other. Worse for the framing: a budgeted attacker who targets pivotal voters is a named, characterized problem in computational social choice since **Bartholdi–Tovey–Trick 1992** (control by adding voters) and **Faliszewski–Hemaspaandra–Hemaspaandra, JAIR 2009** (bribery under a budget), and an information-designing sender who defeats the Condorcet Jury Theorem in a voting body of *any* size is **Heese & Lauermann (2021)**, who prove a persuader "can implement any state-contingent outcome in some equilibrium" and note it works "in small committees with as few as 15 members." On the LLM side the news is no better: **arXiv 2605.29800** already reports, *with no adversary at all*, that the best single judge matches or beats the 9-judge panel on every dataset — i.e. adding verifiers already makes the panel wronger, empirically, today. What survives is one narrow empirical slice, described at the end; the theoretical claim as written is not novel.

---

## 1. Condorcet Jury Theorem and its failures

### 1a. Correlated votes → non-monotonicity in n. **This is the direct hit.**

**Kaniovski, "Aggregation of Correlated Votes and Condorcet's Jury Theorem"** (working paper dated 11 September 2008; published version: *Theory and Decision*). I read the author's PDF at <https://serguei.kaniovski.wifo.ac.at/fileadmin/pdf/condorcet.pdf> (24 pp.).

Verbatim, from the abstract:

> "In the first theorem, negative correlation increases the competence of the jury, while positive correlation has the opposite effect. **An enlargement of the jury with positive correlation can be detrimental up to a certain size, beyond which it becomes beneficial.**"

Verbatim, Corollary 1.4 (p. 15 of that PDF):

> "**Corollary 1.4.** For positive correlation, the effect of larger size on competence is ambiguous, but becomes positive for a sufficiently large size."

And Theorem 1 gives the closed form:

> "M_n^B(p, c) = M_n(p, 0) + c·n(n−1)(0.5 − p)·C_{n−2}^{(n−1)/2} · p^{(n−1)/2} q^{(n−1)/2}"

with the accompanying text: "For c > 0, the term involving c is negative if F(n) > 0, or when n < 3/(1−4pq)." That inequality **is** your non-monotonicity: below the threshold, adding jurors hurts; above it, it helps. This is the theorem you would be re-deriving.

- **Berend & Sapir, "Monotonicity in Condorcet's Jury Theorem with dependent voters," *Social Choice and Welfare* 28(3): 507–528, 2007** — <https://link.springer.com/article/10.1007/s00355-006-0179-y>, RePEc listing <https://ideas.repec.org/a/spr/sochwe/v28y2007i3p507-528.html>. Paywalled; **I could not read the full text** (Springer redirected to an IdP login and I have no institutional access). The abstract as indexed states the paper "provides necessary and sufficient conditions for beneficial augmentation (reduction) of the size of a random subcommittee" of dependent heterogeneous experts. A paper whose title is literally "Monotonicity in Condorcet's Jury Theorem" and whose result is a necessary-and-sufficient condition for when *shrinking* the committee is beneficial is, by construction, the characterization of your claimed phenomenon. Treat as a blocking citation you must read before writing anything. There is an earlier companion, Berend & Sapir (2005), "Monotonicity in Condorcet Jury Theorems," *Social Choice and Welfare*.
- Antecedents on correlation generally: **Ladha (1992)**, *AJPS*, "The Condorcet jury theorem, free speech, and correlated votes"; **Boland (1989)**, *The Statistician*, common-leader model; **Berg (1993)**, *Social Choice and Welfare*, dependency among jurors; **Berend & Paroush (1998)**, "When is Condorcet's jury theorem valid?", *SCW*.

### 1b. Strategic voting → accuracy worsens in n. **Second direct hit, 1998.**

**Feddersen & Pesendorfer, "Convicting the Innocent: The Inferiority of Unanimous Jury Verdicts under Strategic Voting," *APSR* 92(1), March 1998.** I could not get a clean PDF (econdse.org refused the connection; Kellogg/Princeton/Stanford mirrors 404'd), so I pulled the Wayback copy of the econdse PDF and decoded its content streams directly. Verbatim from the abstract as printed on p. 1:

> "It is often suggested that requiring juries to reach a unanimous verdict reduces the probability of convicting an innocent defendant while increasing the probability of acquitting a guilty defendant. We construct a model that demonstrates how strategic voting by jurors undermines this basic intuition. We show that the unanimity rule may lead to a high probability of both kinds of error and that **the probability of convicting an innocent defendant may actually increase with the size of the jury.** Finally, we demonstrate that a wide variety of voting rules, including simple majority rule, lead to much lower probabilities of both kinds of error."

Note also their pivotality mechanism, verbatim from the body: "under the unanimity rule, a vote is pivotal only if all the other jurors have voted to convict. The fact that all other jurors have voted to convict reveals additional [information]" — i.e. pivotal-event conditioning as the engine of the perverse size effect. That is exactly the machinery arXiv 2608.06940 rediscovers, minus the adversary.

- **Austen-Smith & Banks, "Information Aggregation, Rationality, and the Condorcet Jury Theorem," *APSR* 90(1): 34–45, 1996** (<https://econpapers.repec.org/RePEc:cup:apsrev:v:90:y:1996:i:01:p:34-45_20>): sincere voting is not a Nash equilibrium, so the CJT has no rational-choice foundation. This is the standard citation for "independence is necessary, not sufficient" — and notably it is already cited in the LLM paper 2605.29800.
- **Feddersen & Pesendorfer (1996)**, "The Swing Voter's Curse," *AER* — the pivotal-conditioning result that underwrites all of the above.
- **Mukhopadhaya, "Jury Size and the Free Rider Problem," *JLEO* 19(1): 24–44, 2003** (<https://academic.oup.com/jleo/article/19/1/24/795116>): larger juries make *worse* decisions because each juror's incentive to acquire information falls with n. A third, independent route to the same non-monotonicity, with no adversary needed. **Gradstein & Nitzan (1987)** has the same flavour.
- The Nitzan/Paroush survey "Collective Decision Making and Jury Theorems" (<https://econ.biu.ac.il/sites/econ/files/shared/students/teach/898/collective_decision_making_and_jury_theorems.pdf>, 51 pp., read directly) states it flatly: "Gradstein and Nitzan (1987) and Mukhopadhaya (2003) find, for instance, that in contrast to Condorcet's second statement, **a larger jury may reach worse decisions.**"

**Bottom line for §1:** your headline is a known theorem, twice over, from 1998 and 2008, plus a characterization paper (Berend & Sapir 2007) whose title is the claim.

---

## 2. Adversarial / Byzantine aggregation and robust voting

- **Control by adding voters is a named, formally studied problem since Bartholdi, Tovey & Trick, "How hard is it to control an election?", *Mathematical and Computer Modelling*, 1992.** Constructive Control by Adding Voters (CCAV) asks exactly whether a chair can make a preferred alternative win by adding at most k voters. Complexity is fully mapped for most standard rules. Your "adding verifiers can make the panel wronger" is CCAV with a truth-tracking objective bolted on. Survey entry points: <https://www.jair.org/index.php/jair/article/download/10936/26062/20406> (Weighted Electoral Control), <https://arxiv.org/pdf/cs/0507027v5>.
- **Bribery under a budget: Faliszewski, Hemaspaandra & Hemaspaandra, "How Hard Is Bribery in Elections?", *JAIR* 35, 2009** (<https://arxiv.org/abs/cs/0608081>). "Bribery ... modeling situations where an external agent influences voters' preferences within a fixed budget." Your "persuasion budget" is the bribery budget, renamed. The whole $-bribery / swap-bribery / shift-bribery family follows.
- **Byzantine fault tolerance**: the n ≥ 3f+1 bound is not a non-monotonicity result — accuracy is monotone in n *for fixed f*. The non-monotonicity only appears if f scales with n, which is exactly the assumption you would need to state explicitly and defend (see Risk 4).
- **Adversarial crowdsourcing**: Steinhardt, Valiant & Charikar, "Avoiding Imposters and Delinquents: Adversarial Crowdsourcing and Peer Prediction," NeurIPS 2016 (<https://cs.stanford.edu/~jsteinhardt/publications/crowdsourcing/paper.pdf>) — αn reliable workers, (1−α)n arbitrary/adversarial; recovery guarantees depend on α, not n, so adding workers of unknown type does not help. **Guo et al., "Robust Aggregation with Adversarial Experts," WWW 2025** (<https://arxiv.org/pdf/2403.08222>) is the closest modern formalization of "aggregating a panel containing adversaries."
- No result I found in this literature is phrased as "accuracy is non-monotone in n," but the substance — more voters helps the manipulator when the manipulator's budget scales or the adversarial fraction is fixed — is standard.

---

## 3. Boosting / ensemble theory with correlated errors

- **Kuncheva & Whitaker, "Limits on the majority vote accuracy in classifier fusion," *Pattern Analysis and Applications* 6: 22–31, 2003** (author copy: <https://www.lucykuncheva.co.uk/papers/lkpaa.pdf>). Derives upper and lower limits on majority-vote accuracy as a function of individual accuracy p, ensemble size L, and pairwise dependence (Yule's Q). The dependence-conditioned limits are exactly the envelope inside which non-monotonicity in L lives.
- Kuncheva & Whitaker (2003), "Measures of diversity in classifier ensembles"; Dietterich (2000). The saturation-with-correlation result is folklore-plus-formalized in ML and predates the LLM literature by two decades.
- This area gives you *bounds*, not a named non-monotonicity theorem, so it is the weakest of the six for a novelty attack — but it is enough for a reviewer to say "this is the classifier-fusion diversity result."

---

## 4. Information aggregation with a strategic sender. **This is the second-worst news.**

- **Heese & Lauermann, "Persuasion and Information Aggregation in Elections," ECONtribute DP 112, August 2021** (81 pp. PDF read directly: <https://www.econtribute.de/RePEc/ajk/ajkdps/ECONtribute_112_2021.pdf>; subsequently published, check the *Econometrica* version). Verbatim abstract:

  > "This paper studies a large majority election with voters who have heterogeneous, private preferences and exogenous private signals. We show that **a Bayesian persuader can implement any state-contingent outcome in some equilibrium by providing additional information.** In this setting, without the persuader's information, a version of the Condorcet Jury Theorem holds (Feddersen and Pesendorfer, 1997). Persuasion does not require detailed knowledge of the voters' private information and preferences: the same additional information is effective across environments. The results require almost no commitment power by the persuader. Finally, **the persuasion mechanism is effective also in small committees with as few as 15 members.**"

  This is your candidate's exact setup — CJT holds absent an adversary, collapses under a strategic sender — proved five years ago, at both large-n and n=15, with a pivotal-inference engine (their Claim 2: the likelihood ratio of the pivotal event "diverges exponentially fast"). It is strictly stronger than your claim: they don't get non-monotone accuracy, they get *arbitrary* accuracy, chosen by the adversary.
- **Alonso & Câmara, "Persuading Voters," *AER* 106(11): 3590–3605, 2016** (accepted version: <https://eprints.lse.ac.uk/67953/7/Persuading%20voters_2016.pdf>). A politician designs a public experiment; under a non-unanimous rule he "exploits voters' heterogeneity by designing an experiment with realizations targeting different winning coalitions," and a majority of voters can be made strictly worse off. Targeting the winning coalition = targeting the pivotal set.
- **Chan, Gupta, Li & Wang, "Pivotal Persuasion," *JET* 180: 178–202, 2019** (working version: <https://econpub.xmu.edu.cn/research/repec/upload/201811031731464791.pdf>). The name alone is a problem for you. Sender's information design against a majority-voting body, exploiting heterogeneity in voting costs.
- **Bardhi & Guo, "Modes of persuasion toward unanimous consent," *Theoretical Economics*, 2018** (<https://yingniguo.com/wp-content/uploads/2020/08/Bardhi-Guo-2018-Theoretical-Economics.pdf>). Sender-optimal policy under unanimity; distinguishes general (state-of-all-voters) persuasion from individual (per-voter) persuasion, and designates "rubber-stampers" vs. fully-informed vs. partially-informed subgroups. This is the closest thing to a formal "persuasion budget allocated across panel members."
- **Kamenica & Gentzkow (2011)** *AER* is the root; **Schnakenberg (2015)**, "Expert advice to a voting body," *JET*, is the cheap-talk analogue.
- CS-side: **Castiglioni, Celli & Gatti, "Persuading Voters: It's Easy to Whisper, It's Hard to Speak Loud"** (<https://arxiv.org/pdf/1908.10620>) — computational separation between private and public persuasion of voters, which is the algorithmic version of the attack-channel distinction you have not made.

---

## 5. Experimental economics / psychology of group judgment

The trap you were told to look for is here, and it is the 2011 one.

- **Lorenz, Rauhut, Schweitzer & Helbing, "How social influence can undermine the wisdom of crowd effect," *PNAS* 108(22): 9020–9025, 2011** (<https://www.pnas.org/doi/10.1073/pnas.1008636108>). N=144 lab experiment: even mild social influence narrows the diversity of estimates without improving accuracy — the "range reduction," "confidence," and "social influence" effects. Mechanism: influence induces error correlation, which destroys the aggregation benefit. This is the psychology-lab version of your entire causal story, from 2011, and it is precisely the class of finding that burned you last time. Note the published dissent (Farrell's letter, <https://www.pnas.org/doi/pdf/10.1073/pnas.1109947108>) and the authors' reply, "Improved individual estimation success can imply collective tunnel vision" (<https://www.pnas.org/doi/10.1073/pnas.1111007108>) — read both before citing.
- Adjacent and older: Asch conformity (1951/1956); Bikhchandani, Hirshleifer & Welch (1992) information cascades — in a cascade, *later* agents add no information and can lock in the wrong answer, so accuracy is flat-to-worse in n. **Cascades are already a non-monotonicity-in-n result with a natural "influence" channel and no adversary.**
- Counterweight worth citing honestly: Becker, Brackbill & Centola, *PNAS* 2017, "Network dynamics of social influence in the wisdom of crowds" — decentralized influence networks *improve* crowd accuracy. The sign of the effect depends on network structure, which is a modeling degree of freedom your candidate currently leaves unspecified.

---

## 6. Sybil / collusion in reputation and review systems

- **Lam & Riedl, "Shilling recommender systems for fun and profit," WWW 2004** — coined "shilling"; random and average attack models; injecting fake profiles to push or nuke items. Adding voters (profiles) under an attacker's control is the literal attack.
- **Douceur, "The Sybil Attack," IPTPS 2002** — the foundational statement that without a trusted identity authority, an adversary can manufacture arbitrarily many voters, so "more voters" is not a defense.
- Modern survey: "Poisoning Attacks and Defenses in Recommender Systems: A Survey" (<https://arxiv.org/pdf/2406.01022>).
- This area supplies the strongest *intuitive* framing for a practitioner audience, but no theorem you'd cite for non-monotonicity.

---

## LLM side

- **arXiv 2605.29800, "Nine Judges, Two Effective Votes: Correlated Errors Undermine LLM Evaluation Panels"** (HTML read directly). This is the source of your "~two independent votes" premise, and it already contains your headline finding empirically, **with no adversary**. Verbatim from the abstract: "the panel's actual accuracy falls 8–22 percentage points short of what independent voting would achieve, and **the best single judge matches or outperforms the full panel across all conditions.** Neither adding more judges nor using smarter aggregation algorithms helps." Their Table 5: majority vote 72.0 / 77.7 / 88.7 / 92.7 vs. best individual 71.8 / 84.2 / 91.2 / 95.5 — the panel loses on three of four. In its own words, "**correlated voters can perform worse than individuals**" (crediting Austen-Smith & Banks 1996). If accuracy at n=9 is below accuracy at n=1, accuracy is already non-monotone in n *today, in the LLM judge setting, without an attacker*. Your adversary is therefore not necessary to produce the phenomenon you propose to demonstrate.
- **arXiv 2608.06940, "Blind to the Pivotal Vote"** (abstract read from arXiv). Confirmed as you described: pivotal-set arithmetic ("only decisions with a one-vote margin can change"), used defensively for single-ballot substitution, +10.4 to +23.3 pp concentrated on pivotal queries, "four panel sizes (a 9-judge extension and 56 dependent subsampling checks)." **No adversary.** Your "nearest LLM-side work" characterization is accurate.
- **arXiv 2504.18333, "Adversarial Attacks on LLM-as-a-Judge Systems: Insights from Prompt Injections"** (PDF read directly). This is the paper that most directly threatens your *empirical* contribution: §"Multi-Model Committee" evaluates "Committee sizes: 3, 5, and 7 models" against four injection attack families, and reports "**Increasing committee size substantially improved robustness, with 7-model committees reducing attack success**" (19.3% success against the 7-model committee). So a panel-size sweep under adversarial attack **already exists** — and it found *monotone improvement*, the opposite of your prediction. You either replicate this (and your claim dies) or you must explain precisely what your attacker does that theirs does not: theirs is a static injection with no pivotal targeting and no budget reallocation across judges.
- **"When collaboration fails: persuasion-driven adversarial influence in multi-agent LLM debate," *Scientific Reports*, 2026** (<https://www.nature.com/articles/s41598-026-42705-7>) — a single strategically designed persuasive adversary lowers system accuracy by 10–40% and raises consensus on wrong answers by >30%. Reported figures include 58.9% of final outputs carrying injected misinformation under full connectivity.
- **arXiv 2606.19826, "Heterogeneous LLM Debate Under Adversarial Peers"** (abstract read from arXiv) — matched panels: homogeneous / honest-mixed / adversarial-mixed / contaminated. "An honest heterogeneous peer sharply lowers harmful revision, and an adversarial one reverses it"; Llama-3.1-70B harmful-revision 89% → 35% with an honest peer, back to 90% with an adversarial one. **This is panel-composition-vs-outcome under an adversary, measured.** It varies composition rather than size, which is the one crack left.
- **arXiv 2509.05396, "Talk Isn't Always Cheap: Understanding Failure Modes in Multi-Agent Debate"** — adding a weaker agent to a debate produces results worse than no debate; longer debate degrades accuracy.
- Also in the neighbourhood and worth reading before you write: arXiv 2606.01034 (finite-calibration regime map for judge panels — how many judges to deploy), arXiv 2608.19802 (stopping and routing judge panels, explicitly "drop copies, add complements, ... stop when validation gain falls below a threshold"), arXiv 2603.06594 ("A Coin Flip for Safety"), arXiv 2607.23931 (state-dependent error correlations set voting thresholds for AI-agent committees, 28 models, no adversary), Huang et al., ICML 2025, "Exploring and Mitigating Adversarial Manipulation of Voting-Based Leaderboards."

---

## Evidence table: nearest work

| # | Work | Year | Has adversary? | Varies n? | Non-monotone in n? | Kills what |
|---|------|------|----------------|-----------|--------------------|------------|
| 1 | Kaniovski, *Aggregation of Correlated Votes and CJT*, Cor. 1.4 | 2008/2010 | no (correlation only) | yes, analytic in n | **yes, proved, with threshold n < 3/(1−4pq)** | the entire headline theorem |
| 2 | Feddersen & Pesendorfer, *Convicting the Innocent*, APSR | 1998 | no (strategic voters) | yes | **yes — P(convict innocent) increases in jury size** | the headline, via strategic behavior |
| 3 | Berend & Sapir, *Monotonicity in CJT with dependent voters*, SCW | 2007 | no | yes | necessary & sufficient conditions for beneficial augmentation/reduction | the characterization you'd claim; **unread, paywalled** |
| 4 | Heese & Lauermann, *Persuasion and Information Aggregation in Elections* | 2021 | **yes, Bayesian persuader** | yes (large n, and n=15) | stronger: adversary implements *any* outcome | the "strategic persuader vs. voting panel" framing |
| 5 | Alonso & Câmara, *Persuading Voters*, AER | 2016 | yes | no | no | "targets the winning/pivotal coalition" as a novel idea |
| 6 | Chan, Gupta, Li & Wang, *Pivotal Persuasion*, JET | 2019 | yes | no | no | the name and the pivotal-targeting mechanism |
| 7 | Bardhi & Guo, *Modes of persuasion toward unanimous consent*, TE | 2018 | yes | group-size dependent | no | "persuasion budget allocated across panel members" |
| 8 | Bartholdi, Tovey & Trick, *How hard is it to control an election?* | 1992 | yes (chair) | **yes — adding voters is the action** | n/a (winner, not accuracy) | "adding voters can help the manipulator" as novel |
| 9 | Faliszewski et al., *How Hard Is Bribery in Elections?*, JAIR | 2009 | yes, **budgeted** | no | no | "persuasion budget" as a novel primitive |
| 10 | Mukhopadhaya, *Jury Size and the Free Rider Problem*, JLEO | 2003 | no | yes | **yes — larger jury decides worse** | a third independent route to your result |
| 11 | Kuncheva & Whitaker, *Limits on the majority vote accuracy* | 2003 | no | yes (L) | bounds admitting it | the ML-side framing |
| 12 | Lorenz et al., PNAS | 2011 | no (mild social influence) | no (fixed group) | accuracy fails to improve under influence | the empirical/psych framing; **this is your 2010-style trap** |
| 13 | Bikhchandani, Hirshleifer & Welch, cascades | 1992 | no | yes | yes — later agents add nothing, wrong answer locks in | novelty of "more voters ≠ more information" |
| 14 | Lam & Riedl, *Shilling recommender systems*, WWW | 2004 | yes | yes (# fake profiles) | n/a | "adding voters as an attack" |
| 15 | arXiv 2605.29800, *Nine Judges, Two Effective Votes* | 2026 | **no** | yes (n_eff(k) curve) | **yes, empirically: best single judge ≥ 9-judge panel** | your empirical headline, without needing an adversary |
| 16 | arXiv 2504.18333, *Adversarial Attacks on LLM-as-a-Judge* | 2025 | **yes (prompt injection)** | **yes: committees of 3, 5, 7** | **no — monotone improvement** | your empirical contribution, *and* contradicts your prediction |
| 17 | arXiv 2606.19826, *Heterogeneous LLM Debate Under Adversarial Peers* | 2026 | yes | composition, not size | sign flips with composition | "panels under an adversary" as unexplored |
| 18 | Sci. Reports, *When collaboration fails* | 2026 | yes, persuasive | no | no | "strategic persuader vs. LLM panel" as unexplored |
| 19 | arXiv 2608.06940, *Blind to the Pivotal Vote* | 2026 | no | 4 panel sizes | no | (your stated nearest neighbour — confirmed accurate) |

---

## What specifically survives

Almost nothing of the theory. Concretely:

**Dead.** "Panel accuracy is non-monotone in panel size under an adversary" — a reviewer will cite Kaniovski Cor. 1.4 (correlation route), Feddersen–Pesendorfer 1998 (strategic route), Mukhopadhaya 2003 (endogenous-effort route), and Berend–Sapir 2007 (the characterization), and reject. "An attacker with a budget who targets the pivotal voter" — bribery, JAIR 2009. "Adding voters helps the attacker" — CCAV, 1992. "A strategic sender defeats the CJT in a committee" — Heese & Lauermann 2021, in a strictly stronger form.

**Survives, phrased as a claim a reviewer would accept:**

> *In deployed LLM-as-judge panels, the classical correlation-induced non-monotonicity of majority accuracy in panel size (Kaniovski 2008, Cor. 1.4) binds at the panel sizes actually used in practice (n ≤ 9), because measured effective independence is n_eff ≈ 2.2; and the existing empirical evidence that larger judge committees are more robust to adversarial input (arXiv 2504.18333, committees of 3/5/7) does not survive an attacker who allocates a fixed persuasion budget conditional on the observed vote margin rather than injecting a static payload uniformly.*

That is: **an empirical falsification of one prior positive result, under a stronger and better-specified threat model, with the classical theory cited as the explanation rather than claimed as the contribution.** It is a workshop-to-mid-conference paper, not a headline theorem. To even hold that, you must (a) obtain and read Berend & Sapir 2007 in full, (b) reproduce 2504.18333's committee sweep as your baseline, (c) show your margin-conditional attacker beats their static one at matched budget, and (d) show the crossover point sits inside the n ≤ 9 range practitioners use. If (d) fails, there is no paper.

A second, thinner survivor: nobody has combined *size* sweep with *adversary* on judge panels — 2606.19826 varies composition under an adversary; 2504.18333 varies size under a weak adversary; 2605.29800 varies size with no adversary. The 2×2 cell "size × strong adaptive adversary" is empty. That is a gap, but it is a gap in a table, not a gap in knowledge.

---

## Ranked risks

1. **The headline is a 1998/2008 theorem.** (Highest.) Kaniovski Cor. 1.4 and Feddersen–Pesendorfer 1998 are each individually fatal to the claim as stated. A reviewer in political economy or social choice will recognize both within one page.
2. **Heese & Lauermann 2021 already did the adversarial version, stronger.** "Any state-contingent outcome, in committees as small as 15, with almost no commitment power" dominates "accuracy is non-monotone." You cannot claim to be first to stage a persuader against a voting panel.
3. **Your prediction is contradicted by the only existing LLM panel-size sweep under attack.** arXiv 2504.18333 found committees of 7 *more* robust than 3. If you run the experiment and get the same monotone result, you have a negative paper against your own thesis.
4. **The phenomenon already occurs without your adversary.** 2605.29800 shows the 9-judge panel losing to the best single judge on 3 of 4 datasets, no attacker present. This makes the adversary look like decoration: any non-monotonicity you measure has an adversary-free confound you must control for.
5. **Berend & Sapir 2007 is unread and may contain your exact characterization theorem.** Unquantified risk until you read it. Do this first — it is cheap and it may end the project.
6. **The psych/experimental trap is live.** Lorenz et al. PNAS 2011 is the same causal story (influence → correlation → aggregation fails) in a 2011 lab experiment. This is structurally identical to the burn you described.
7. **Bribery/control complexity results may make your attacker either trivial or NP-hard**, and either outcome is awkward: if the pivotal-targeting attack is polynomial-time, it is a known bribery instance; if it is NP-hard, your attacker is not realizable and the threat model is vacuous.

---

## Modeling flaws in the candidate itself

1. **The two 2026 findings do not compose the way the pitch assumes — they fight each other.** If n_eff ≈ 2 for a nominal panel of 9, then the "pivotal voter" is not an individual model; it is a latent shared factor. An attacker targeting *one judge* moves ~1/9 of a nominal vote but ~0 effective votes; an attacker moving the *shared* factor moves all judges at once. Those are two different attacks (private vs. public persuasion — Castiglioni et al. 2019 separate them computationally) and the candidate conflates them. As written, the mechanism is under-specified at exactly the point where the claim lives.
2. **Non-monotonicity in n is partly a trivial parity artifact.** Majority-vote accuracy is already non-monotone from odd n to even n under any tie-breaking rule, even with fully independent voters. If you report accuracy at n = 3,4,5,6,7,8,9 and point at a dip, a reviewer will ask whether you have merely rediscovered the odd/even effect. You must either restrict to odd n or explicitly decompose parity from correlation from adversary.
3. **"Persuasion budget" is not defined as an object.** Is it (a) a bribery budget (k voters flipped at cost c — Faliszewski et al.), (b) a Bayesian-persuasion information structure with commitment (Kamenica–Gentzkow), or (c) a token/compute budget for adversarial text? These have different solution concepts and different prior art. (a) and (b) are both closed. Only (c) is arguably open, and (c) is an engineering measurement, not a theorem.
4. **The attacker's information is unstated and load-bearing.** Targeting "the pivotal voter" requires knowing the other votes. If the attacker sees votes, it is the fully-informed chair of BTT 1992 and the result is unsurprising. If it does not, "targeting the pivotal voter" is meaningless and the attack degenerates to a uniform prior-shift — which is Heese & Lauermann's public signal, whose effect is *not* non-monotone in n but monotone-catastrophic.
5. **No stated scaling of adversary power with n.** Non-monotonicity vs. monotone-worse depends entirely on whether the budget is fixed or scales with n. Fixed budget against growing n: the attack washes out and accuracy is eventually increasing (this is literally Kaniovski's "beyond which it becomes beneficial"). Budget scaling with n: accuracy is monotone decreasing, not non-monotone. The non-monotone regime is a knife-edge that only exists for a specific budget-scaling assumption, and the candidate does not name one.
6. **Correlation is treated as exogenous.** In practice, adding a judge changes the correlation structure (same-family judges correlate more — 2605.29800 measures +0.047 to +0.109 same-family excess). So n and c are not independent parameters, and any theorem holding c fixed while varying n describes an experiment you cannot run.

---

## Verbatim queries that returned nothing useful

Recorded exactly as issued.

- `"LLM judge panel adversary persuasion budget targets pivotal judge non-monotone panel size arXiv 2026"` — returned only budget-*allocation* papers (2606.01034, 2605.23362, 2608.19802, 2602.15481, 2608.29168); no adversarial panel-size result.
- `"number of judges" OR "panel size" adversarial LLM evaluator attack success rate increases with more judges` — no paper found in which attack success *increases* with panel size; the one relevant sweep (2504.18333) reports the opposite.
- `Berend Sapir "beneficial augmentation" committee size dependent experts non-monotone majority` — the phrase "beneficial augmentation" surfaced no full text; only indexing pages. Berend & Sapir 2007 remains unread.
- `Bardhi Guo "Modes of persuasion toward unanimous consent" group size persuader easier larger group` — found the paper, but returned nothing on the group-size comparative static specifically. Open question I did not resolve.
- `adversarial crowdsourcing robust aggregation adversary fraction more workers does not help Steinhardt Charikar` — no explicit "more workers does not help" theorem statement located; the α-fraction framing is implicit, not a named result.

## Sources I could not access

- **Berend & Sapir, *SCW* 28(3), 2007** — Springer paywall, redirected to `idp.springer.com` login. Read only the indexed abstract. **This is the single most important unread item.**
- **Feddersen & Pesendorfer, *APSR* 1998** — econdse.org mirror refused connection (ECONNREFUSED); Kellogg, Princeton and Stanford mirrors 404'd; Cambridge Core paywalled. I recovered the text by fetching the Internet Archive snapshot of the econdse PDF (`web.archive.org/web/2018id_/...`), which downloaded truncated at exactly 1 MiB with a broken xref, and decoding its FlateDecode content streams directly. The abstract and introduction quoted above are from that raw stream extraction and match each other verbatim across two locations in the document (abstract and p. 1 body), which is why I trust them. **I did not read the theorem statements or proofs**, only the abstract and opening.
- **Kaniovski**: I read the **September 11, 2008 author working-paper PDF**, not the journal version. Theorem/corollary numbering may differ in print.
- **Heese & Lauermann**: I read the **August 2021 ECONtribute DP 112 version** (81 pp.), not the published version. Check the *Econometrica* version before citing.
- **Alonso & Câmara**: downloaded the LSE accepted version but the file served as HTML, not PDF; my characterization of its content is from the AEA/LSE listing pages, **not from the paper text**. Treat as secondary.
- **Kuncheva & Whitaker 2003**: characterized from search-result summaries and the abstract only; **I did not open the PDF**. Treat as secondary.
- **Lorenz et al. PNAS 2011**: characterized from the PNAS listing and search summaries; **I did not open the full text**. Treat as secondary.
