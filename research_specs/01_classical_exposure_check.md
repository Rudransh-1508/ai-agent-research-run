# Adversarial prior-art check: centralized-vs-decentralized shortfall decomposition

**Verdict: closed.** The centralized-optimum/decentralized-optimum/achieved-value three-way comparison, and the two-term decomposition of a team's shortfall into an environment-owned information gap and a team-owned coordination-execution gap, is standard in decentralized control and decentralized-POMDP planning going back at least to Radner 1962 and Marschak & Radner 1972 (team theory: value of an information structure), formalized for multi-agent AI planning no later than Pynadath & Tambe, *JAIR* 2002 (COM-MTDP, "free communication" vs. "no communication" bounds) and Goldman & Zilberstein, *JAIR* 2004 (explicit "value of communication" = value-with-full-observability minus value-without), and it is routine current practice in the Dec-POMDP literature (Oliehoek, Spaan & Vlassis and others) to report a centralized upper bound (MPOMDP/QPOMDP/QMDP) alongside the Dec-POMDP-optimal or heuristic value as exactly this diagnostic.

---

## 1. Team decision theory (Radner 1962; Marschak & Radner 1972; Ho 1980)

Team theory is precisely the study of how much a team loses when decision-makers act on different (decentralized) information rather than pooled (centralized) information, and how much of a further loss comes from suboptimal execution given that information. Ho's 1980 *Proc. IEEE* tutorial-survey, "Team decision theory and information structures," is explicitly a synthesis of this line (Marschak & Radner 1972; Radner 1962), organizing exactly the comparison of information structures and their associated optimal expected payoffs. Pynadath & Tambe's own account (below) states plainly that COM-MTDP is "inspired by work in economic team theory" (Marschak & Radner 1971/1972; Yoshikawa 1978; Ho 1980) and that the team-theoretic apparatus already supplies the comparison of what a team achieves under a given information/decision structure versus what it could achieve under a better one.

I could not obtain the primal AMS 1962 Radner paper or the 1972 book text directly (see null queries below — Project Euclid returned an HTML shell, not the PDF, and no OCR'd scan of the Marschak & Radner book was found). I therefore treat the "value of an information structure" terminology as attested at one remove, through Pynadath & Tambe's direct citation and Ho's tutorial title, rather than by a verbatim quote from Radner or Marschak & Radner themselves. This is a gap in my verification, not in the underlying claim — the concept (comparing the optimal payoff under different information structures, one of which can be full/centralized information) is the entire subject of the field named "team theory," and it long predates 2020.

**What this establishes:** decomposing "how far is the team from doing as well as if information were centralized" is literally team theory's founding question (Radner 1962 title: "Team Decision Problems"). It is not a new idea to compare a decentralized-information optimum against a full-information (centralized) optimum.

## 2. Witsenhausen (1968) and decentralized stochastic control

Witsenhausen's 1968 counterexample is the canonical demonstration that decentralized-information optimal cost can strictly exceed centralized-information optimal cost, and a large control-theory literature (Witsenhausen's own subsequent papers on information structures, and the "Centralized versus Decentralized Team Games of Distributed Stochastic Differential Decision Systems" line, e.g. arXiv:1302.3452) frames control problems exactly around comparing centralized-strategy optimal cost to decentralized-information-structure optimal cost. From arXiv:1302.3452 ("Centralized Versus Decentralized Team Games..."), verbatim:

> "We conclude the preliminary discussion on classical optimization theory of centralized strategies versus decentralized strategies, by stating that there are no limitations in applying classical theory of optimization to distributed systems with decentralized information structures."

This paper's entire framing — title and body — is the centralized-vs-decentralized optimal-cost comparison used as the baseline object of study, i.e., exactly component (a) of the claim ("price of decentralization" = centralized optimum minus decentralized optimum) is the subject matter of this branch of control theory, predating any LLM-agent framing by decades.

## 3. Decentralized stochastic control / information structures (Yuksel-Basar, Nayyar-Mahajan-Teneketzis, Mahajan)

Not independently re-verified with primary-source quotes in this pass (time-boxed), but the Ho 1980 tutorial and the arXiv:1302.3452 paper both sit squarely in this tradition and confirm that "gap between centralized-information optimal cost and decentralized-information optimal cost" is the standard organizing quantity of the whole area — this is not a fact that later surveys (Yuksel-Basar, Nayyar-Mahajan-Teneketzis common-information approach) invented; it is the founding question they build tools to attack.

## 4. Dec-POMDP literature — is centralized-vs-decentralized value reporting routine practice?

**Yes, and it is formalized with a name: "value of communication."** This is the strongest, most directly on-point result.

### Goldman & Zilberstein, JAIR 2004, "Decentralized Control of Cooperative Systems: Categorization and Complexity Analysis" (verified from the arXiv preprint text, arXiv:1107.0047, downloaded and read in full)

Section 5, "Decentralized Control with Communication," opens (verbatim, from the extracted PDF text):

> "Direct communication can be beneficial in decentralized control because the agents lack full observability of the global state. That is, the value of the optimal joint policy that allows communication may be larger than the value of the optimal joint policy without communication."

And on the centralized/full-observability limit:

> "If we assume that direct communication leads to full observability of the system state that direct communication is free and that the observations are independent then obviously the agents will benefit most by communicating constantly. This results in a fully observable decentralized process, which is equivalent to an MMDP (Boutilier, 1999)."

This is exactly the claim's "centralized reference": full communication/full observability collapses the Dec-POMDP to an MMDP (a **centralized, jointly-fully-observable multi-agent MDP**), whose value is by definition ≥ the no-communication decentralized-optimal value. Goldman & Zilberstein's companion paper, "Optimizing Information Exchange in Cooperative Multi-Agent Systems" (Goldman & Zilberstein, AAMAS 2003 / the JAAMAS 2007 journal version I also pulled, arXiv/rbr.cs.umass.edu copy), is the one that names this gap "the value of communication" and builds an entire cost-benefit framework (communication cost vs. information value) around it — i.e., the *exact* two-sided accounting the claim proposes (an intrinsic gap belonging to the environment/information-structure, and a further gap that is the team's to close by acting/communicating better) is the explicit topic of this 2003/2004/2007 body of work.

### Pynadath & Tambe, JAIR 2002, "The Communicative Multiagent Team Decision Problem" (COM-MTDP) (verified from a downloaded preprint copy, jmvidal.cse.sc.edu/library/pynadath02a.pdf, and an arXiv abstract copy for the JAIR version's context)

COM-MTDP explicitly compares team value under **"No Communication"** and **"Free Communication"** conditions and proves complexity/value results for each, i.e., it computes and contrasts a decentralized-information value against a centralized/free-information value as the organizing structure of the whole paper. Verbatim from the extracted text:

> "We start by examining the case under the condition of free communication, where we would expect the benefit of communication to be the greatest... Theorem 2. Under free communication, consider a team of agents using a coordination policy... this combined policy is dominant over any other policies."

> "Theorem 3. The decision problem of determining whether there exist policies... for a given COM-MTDP with free communication and collective observability, that yield a total reward at least K over some finite horizon T is P-complete." [contrasted with Theorem 1's reduction showing the general no/general-communication case is NEXP-complete, citing Bernstein et al.]

> "Under collective observability and partial observability, teamwork without communication is highly intractable, but, with free communication, the complexity becomes on par with that of single-agent planning problems."

And the paper self-identifies its ancestry directly in team theory (verbatim, from the OCR'd text, some ligatures garbled by extraction — "de ision" = "decision" etc.):

> "...inspired by work in economic team theory (Marschak & Radner, 1971; Yoshikawa, 1978; Ho, 1980)."

So the claim's exact two-endpoint comparison — decentralized-optimal value vs. centralized/free-communication-optimal value — is literally the paper's Table of complexity results (no-communication case vs. free-communication case), with free-communication used as the ceiling reference exactly the way the claim proposes using a centralized-policy value as the reference.

### Oliehoek, Spaan & Vlassis, JAIR 2008, "Optimal and Approximate Q-value Functions for Decentralized POMDPs" (verified from arXiv:1111.0062, downloaded and read)

This paper makes the centralized-value-as-upper-bound practice a formal theorem and names the specific centralized quantity `QPOMDP`, explicitly built on the assumption of centralized control, and used as an upper bound on the Dec-POMDP-optimal `Q*`:

> "QPOMDP does share the assumption of centralized control." 

> "Theorem 5.1 (Hierarchy of upper bounds). The approximate Q-value functions QBG and QPOMDP correspond to the optimal Q-value functions of appropriately defined k-step delayed communication models. Moreover these Q-value functions form a hierarchy of upper bounds to the optimal Q∗ of the Dec-POMDP: Q∗ ≤ QBG ≤ QPOMDP ≤ QMDP."

This is precisely "compute the centralized-policy value as a reference and measure the gap to the decentralized-optimal (or heuristic) value" — used not as a one-off illustration but as the load-bearing admissible heuristic for the MAA* Dec-POMDP solver described later in the same paper. Web search additionally surfaced (not independently re-verified via primary source in this pass, but consistent and widely cited): "The value of an optimal T-period joint policy for a Dec-POMDP is bounded from above by the value of an optimal T-period policy for a POMDP derived from the Dec-POMDP by assuming a centralized controller," and recent Dec-POMDP solvers (e.g. Multi-Agent A*, arXiv:2405.05662) report policy values "only 1% smaller than their upper bounds" on Box Pushing — i.e., routinely reporting achieved value against the centralized/MPOMDP ceiling is standard benchmarking practice on exactly the canonical Dec-POMDP benchmark suite (Dec-Tiger, Box Pushing, Broadcast Channel, Mars Rover, Grid) named in the prompt.

### Complexity results (Bernstein et al.; Papadimitriou & Tsitsiklis)

Confirmed via the Goldman & Zilberstein and Pynadath & Tambe texts: Dec-MDP/Dec-POMDP (decentralized, no/costly communication) is NEXP-complete (Bernstein, Zilberstein & Immerman 2000, cited in both papers), while the centralized/fully-observable/free-communication reduction (MMDP) is P-complete (Papadimitriou & Tsitsiklis, 1987, cited explicitly in Goldman & Zilberstein: *"This problem is known to be P-complete (Papadimitriou & Tsitsiklis, 1987)"*). This complexity cliff is precisely why the field treats the centralized value as a distinguished, separately-computed reference point rather than just another policy value — it's cheap (P/poly-time solvable via MMDP/MDP reduction) relative to the decentralized optimum (NEXP-hard), which is exactly the practical justification for using it as a ceiling/diagnostic in benchmarking, same as the claim proposes for LLM teams.

## 5. Price of anarchy / price of decentralization terminology

"Price of anarchy" (Koutsoupias-Papadimitriou 1999) is the equilibrium-vs-social-optimum version of this idea in game theory, not identical to the claim's decentralized-optimal-vs-centralized-optimal comparison, but structurally the same "ratio/gap to a benchmark" move, decades old. More directly on point: "price of decentralization" is an existing, literal term of art in control/detection theory. From Huang & Wang, "On the Price of Decentralization in Decentralized Detection" (arXiv:2409.00728, downloaded and read):

> "To elucidate the price of decentralization, further analysis on the higher-order asymptotics of the error probability is conducted. It turns out that the price is at most a constant multiplicative factor in the error probability..."

> "Compared to the centralized performance, how much is lost?"

This confirms "price of decentralization" as a pre-existing phrase for centralized-minus-decentralized performance gaps, used in exactly this sense (not coined by the proposal), albeit in a detection-theory rather than Dec-POMDP context, and postdating the Dec-POMDP-era terminology ("value of communication") by roughly two decades.

## 6. MARL evaluation practice

Confirmed above under (4): Dec-POMDP planning/MARL benchmarking on Dec-Tiger, Box Pushing, Meeting-on-a-Grid, Mars Rover, Broadcast Channel routinely reports algorithm value against the Dec-POMDP-optimal or centralized-upper-bound (MPOMDP/QPOMDP) value as a ceiling — this is standard, decades-old practice in that community, not something novel to apply to LLM teams. The "excess coordination loss" (decentralized-optimal minus achieved) is exactly the "optimality gap" figure such benchmark tables already report for approximate/heuristic Dec-POMDP solvers and learned policies.

## Is the decomposition already named?

Yes, in two overlapping ways that any proposal on this topic should adopt rather than re-coin:

1. **"Value of communication"** (Goldman & Zilberstein, AAMAS/JAAMAS 2003–2007; used implicitly via the free-communication vs. no-communication contrast in Pynadath & Tambe, JAIR 2002) — the gap between the centralized/full-communication optimum and the decentralized (no/costly-communication) optimum. This is component (a) of the claim, "price of decentralization."
2. **"Price of decentralization"** — attested, in this literal phrase, in the control/detection-theory literature (Huang & Wang 2024/2025, arXiv:2409.00728) for the environment-owned centralized-minus-decentralized-optimal gap. The claim's own proposed name for component (a) is therefore not new coinage — it already exists as a term of art, just not previously applied to Dec-POMDP/LLM-team settings under that exact label (Dec-POMDP work uses "value of communication" instead).
3. Component (b), decentralized-optimal minus achieved, does not appear to have a single canonical name across these literatures — it is simply "the optimality gap," "regret to the Dec-POMDP optimum," or "suboptimality" in Dec-POMDP/MARL benchmark tables (e.g., the Box Pushing "1% smaller than upper bounds" framing). A term like "excess coordination loss" for this piece is a reasonable, non-conflicting label, but the overall three-way accounting (centralized optimum / decentralized optimum / achieved) is not new.

## What specifically survives

Essentially nothing about the decomposition itself survives as novel. What could survive, narrowly, as a reviewer-acceptable contribution:

- **Applying this decades-old three-point accounting (centralized optimum, decentralized optimum, achieved value) specifically to LLM-agent teams**, where computing the "decentralized optimal policy value" is itself hard/approximate because the policy class is LLM prompting/behavior rather than a solvable Dec-POMDP — if the proposal's actual contribution is a *method for estimating or approximating the decentralized optimum* for LLM teams (since exact Dec-POMDP solving is NEXP-hard and doesn't apply to open-ended language-based agents), that could be a real, narrow technical contribution. The diagnostic framing itself is not.
- An empirical *finding* about where LLM teams sit on this decomposition (e.g., "LLM teams lose more to excess coordination loss than to price of decentralization, unlike X") could be a legitimate empirical contribution, but must be framed as measurement using known tools, not as inventing the tools.

If the paper's headline claim is "we propose decomposing team shortfall into a price-of-decentralization term and an excess-coordination-loss term" — that headline does not survive; it must cite Goldman & Zilberstein (2003/2004), Pynadath & Tambe (2002), and ideally Radner (1962)/Marschak & Radner (1972) as the origin, and reframe the contribution as the LLM-specific instantiation/approximation method, not the decomposition itself.

## Ranked risks

1. **(Highest)** The core decomposition is not just "known" but is the literal organizing concept of an entire named subfield (team theory) since 1962, formalized for Dec-POMDPs by 2002–2004, and given the exact phrase "price of decentralization" in the control literature. A reviewer familiar with Dec-POMDPs (a near-certainty for any multi-agent-systems venue) will reject the novelty claim on sight, likely citing Goldman & Zilberstein or Oliehoek & Amato's book directly.
2. **High.** The "centralized reference" (MPOMDP/MMDP value) vs. "decentralized reference" (Dec-POMDP optimal) vs. "achieved value" three-way comparison, with the achieved-value gap reported as an optimality gap, is standard benchmark-table practice in Dec-POMDP/MARL papers (Box Pushing, Dec-Tiger, etc.) — so even the "diagnostic for a team" framing, not just the terminology, is precedented practice, not just theory.
3. **Medium.** I was not able to independently verify the Marschak & Radner 1972 book text or the original 1962 Radner AMS paper via primary source (paywalled/no accessible OCR found) — this is a residual gap in my check, though the concept is corroborated at one remove via Ho 1980 and Pynadath & Tambe's direct citation, so I am confident the underlying claim (team theory already studies this) holds even without the primal quote.
4. **Medium.** If the proposal's real distinguishing move is "compute or approximate the decentralized optimum for LLM-based agents specifically," that could survive, but the write-up as given (in the prompt) does not foreground that distinction — it currently reads exactly like a restatement of the Dec-POMDP diagnostic.

## Verbatim null queries (returned nothing directly useful / had to redirect)

- `Goldman Zilberstein "Decentralized control of cooperative systems" JAIR 2004 value of communication centralized decentralized gap` — WebSearch returned only general summaries, not the specific "value of communication" quote (had to fetch and grep the PDF directly).
- `Marschak Radner "Economic Theory of Teams" value of information centralized team decentralized team gross value` — no primary-source hit; only secondary summaries.
- `Marschak Radner team theory "gross value" "value of an information structure" "net value" definition maximal expected payoff` — no relevant hits at all; results were generic "value of information" / EVPI material unrelated to team theory specifically.
- `Radner 1962 "Team Decision Problems" Annals Mathematical Statistics Cowles Foundation paper pdf` — Project Euclid link found but the downloaded file was an HTML shell, not a readable PDF (`curl` on `https://projecteuclid.org/journals/.../10.1214/aoms/1177704455.pdf` returned `HTML document text` per `file`, not a real PDF).
- `curl -sL -o pt02b.pdf "https://www.jair.org/index.php/jair/article/download/10304/24632"` — download was not a valid PDF (pdftotext: "May not be a PDF file," "Couldn't find trailer dictionary"); had to fall back to a mirrored preprint copy (jmvidal.cse.sc.edu) instead.
- `"cost of decentralization" OR "price of decentralization" optimal centralized minus decentralized control information structure Witsenhausen` — no direct hit connecting Witsenhausen specifically to the phrase "price of decentralization"; the phrase itself was found instead in a separate, later (2024/2025) detection-theory paper (arXiv:2409.00728), not in Witsenhausen-adjacent literature.
- `Ho 1980 "Team decision theory and information structures" Proceedings IEEE value of information structure comparison complete information` — no accessible full text found (IEEE Xplore paywalled); relied on secondary description and on Pynadath & Tambe's direct citation of it instead.

## Sources consulted (primary, downloaded and read in full or in relevant part)

- Goldman, C. V., & Zilberstein, S. (2004). "Decentralized Control of Cooperative Systems: Categorization and Complexity Analysis." *JAIR* 22:143–174. Read via arXiv:1107.0047 (full PDF text extracted and grepped).
- Goldman, C. V., & Zilberstein, S. (2003/2007). "Optimizing/Learning information exchange in cooperative multi-agent systems." JAAMAS 2007 version read via rbr.cs.umass.edu/shlomo/papers/GAZjaamas07.pdf.
- Pynadath, D. V., & Tambe, M. (2002). "The Communicative Multiagent Team Decision Problem: Analyzing Teamwork Theories and Models." *JAIR* 16:389–423. Read via jmvidal.cse.sc.edu/library/pynadath02a.pdf (AAMAS-length preprint) and cross-checked against arXiv:1106.4569 abstract.
- Oliehoek, F. A., Spaan, M. T. J., & Vlassis, N. (2008). "Optimal and Approximate Q-value Functions for Decentralized POMDPs." *JAIR* 32:289–353. Read via arXiv:1111.0062 (full PDF text extracted).
- Huang, B. Y.-C., & Wang, I-H. "On the Price of Decentralization in Decentralized Detection." arXiv:2409.00728 (read directly).
- "Centralized Versus Decentralized Team Games of Distributed Stochastic Differential Decision Systems..." arXiv:1302.3452 (read directly, control-theory framing of centralized-vs-decentralized value).
