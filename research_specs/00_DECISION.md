# Gap Sweep: Final Outcome and Decision

Sweep run 7-8 Sep 2026. Corpus: `masamasa59/ai-agent-papers`, ~1,360 entries, four-slice traversal
(`_survey/`). Four candidates proposed and killed against classical literature (`candidate_*_check.md`,
`03_novelty_review.md`). Spec 01 then independently re-checked from scratch by four fresh agents given
no bibliography (`01_classical_exposure_check.md`, `01_evaluation_practice_check.md`,
`01_synthesis_check.md`, `01_scoop_check.md`).

## Scoreboard: five candidates checked, five headlines closed or eroded

| Candidate | Killed / eroded by |
|---|---|
| Sanctioning under unreliable blame | Grechenig, Nicklisch & Thöni 2010; Ambrus & Greiner 2012; Glynatsi, Hilbe & Murase 2025; Ensign et al. 2018. **Retracted.** |
| Acceptance-gate manipulation-resistance | PACE (arXiv:2606.08106, Jun 2026) already frames the acceptor as "the loop's silent weak point" and "a textbook case of adaptive data analysis"; Hardt et al. 2016; Kleinberg & Kleinberg 2018. **Closed.** |
| The experience commons | Ghosh & McAfee, WWW 2011, exact prediction verbatim; EquiMem (arXiv:2605.09278) already does the LLM-side zero-trust memory game. **Closed.** |
| Verifier panels vs. strategic persuader | Kaniovski 2008 Cor. 1.4 (non-monotonicity from correlation alone, no adversary needed); Feddersen & Pesendorfer 1998; Heese & Lauermann 2021 already stage a persuader against a jury. **Headline closed.** |
| Regret-grounded / Dec-POMDP-optimum LLM teams (spec 01) | See below — closed on the measurement half, eroded but not fully closed on the method half. |

## Spec 01, re-examined cold

**Measurement half (V\*_Cent - V\*_Dec decomposition): closed.** Goldman & Zilberstein (JAIR 2004)
already name this exact gap the **"value of communication"**, quoted directly: *"the value of the
optimal joint policy that allows communication may be larger than the value of the optimal joint
policy without communication."* Pynadath & Tambe (JAIR 2002, COM-MTDP) formalize the identical
no-communication-vs-free-communication comparison, built explicitly on Marschak & Radner's 1962/1972
team theory. Oliehoek, Spaan & Vlassis (JAIR 2008) prove a formal bound hierarchy using the centralized
value as reference against the decentralized optimum, used as a load-bearing planning heuristic.
"Price of decentralization" is itself a pre-existing term outside the LLM literature
(Huang & Wang, arXiv:2409.00728). **Nothing about the decomposition itself survives as a contribution.**

**Evaluation-practice half: partially closed, one clean sliver.** The broad claim ("no LLM-team eval
compares to any computed optimum") is false - quote-verified counterexamples exist (arXiv:2504.02051
Hungarian-algorithm optimum, arXiv:2607.06157 IP-solver optimum, arXiv:2605.16575 Nash Bargaining
distance, arXiv:2505.11556 full-info oracle). But every one of them is centralized/full-information.
**Nobody computes an optimum over the actual decentralized policy class for LLM teams** - largely
because it is NEXP-hard in general, so almost nobody does this for any agent type at non-trivial
scale. That specific sliver is real and clean.

**Synthesis half (Modes B/C): partially closed on all three claims, narrower slivers survive.**
- Claim A (LLM emits a decentralized policy object checked exactly by a solver): RADIANT
  (arXiv:2607.16708) already has an LLM emit a controller, translated to CSP, checked *exactly* by
  the FDR model checker, inside counterexample-driven repair - just not Dec-POMDP-framed. Surviving
  sliver: per-agent, local-history-only FSCs checked exactly against a Dec-POMDP specifically.
- Claim B (LLM translates NL task to a formal Dec-POMDP tuple): the single-agent analog is already
  done - POMDP Coder / Pinductor (arXiv:2505.02216, 2605.13740) has an LLM generate POMDP T/O/R
  functions from NL for a solver. Surviving sliver: the multi-agent/decentralized extension,
  confirmed genuinely absent by direct arXiv index queries.
- Claim C (value-loss-localized counterexample repair): CEGIS-with-LLM-as-synthesizer is already a
  small genre (TraceFix, RADIANT, Property-Guided LLM Program Synthesis, AutoCedar). Surviving
  sliver: ranking counterexamples by value loss and localizing repair to one agent's fragment
  specifically, rather than by violation alone.
- Also found: MAGRPO (AAAI 2026, arXiv:2508.04652) and a Jan 2026 follow-up from **Christopher
  Amato's group (Northeastern)** already frame multi-LLM collaboration as a Dec-POMDP for RL
  fine-tuning - a vocabulary collision reviewers will flag, and the group most likely to add a
  solver-verified decentralized optimum next.

**Scoop risk: low for a direct hit (~10-15%) by 8 Oct, but the framing itself is no longer fresh.**
Zero hits for classical Dec-POMDP benchmark domains (Dec-Tiger, Box Pushing, etc.) combined with LLMs
- that specific empirical setting is genuinely clean. AAMAS 2026 proceedings could not be exhaustively
scraped (ACM DL 403, IFAAMAS page didn't expose the TOC) - **do a manual pass before committing.**

## What this adds up to

Spec 01 as originally written - "no LLM multi-agent evaluation measures team performance against a
computed decentralized optimum while separately reporting the intrinsic cost of decentralization,"
sold as a fresh measurement framework plus a fresh synthesis method - **does not survive.** Every
headline claim in it is a known result, a known term, or a published mechanism with the LLM piece
already attached by someone else.

What survives is a **stack of narrow, correctly-scoped slivers**, each real but small:
1. Compute the decentralized-policy optimum (not just centralized) specifically for LLM teams, on
   small tractable Dec-POMDP instances where it's actually feasible.
2. Extend LLM-to-POMDP model synthesis (already done, single-agent) to the multi-agent/decentralized
   case (confirmed absent).
3. Extend LLM-to-FSC-with-exact-model-checking (already done, general) to per-agent local-observation
   controllers specifically evaluated against a Dec-POMDP (confirmed absent).
4. Extend counterexample-guided LLM repair (already a genre) to value-loss localization on a single
   agent's fragment (confirmed absent).

None of these four is independently a headline. Together, applied to the one setting (classical
finite-horizon Dec-POMDPs with published exact solutions) where all four connect, they could still
be a legitimate AAMAS paper - but it is now explicitly a **combination/extension paper standing on
five 2026 papers' shoulders** (Goldman & Zilberstein/Pynadath & Tambe for the decomposition,
RADIANT, POMDP Coder/Pinductor, the CEGIS-with-LLM genre, and MAGRPO as the vocabulary neighbor to
distinguish from), not a paper opening new territory. The abstract must say exactly this, or a
reviewer who knows this literature will say it for you, unfavorably.

## Recommendation

Given the 8 Oct deadline, ~1,360 papers surveyed, and five straight headline claims eroding under a
classical-literature check: **do not submit a "we are first to X" paper from this sweep to the AAMAS
2027 main track.** The honest options are:

1. **A narrowly-scoped combination paper** on spec 01's four surviving slivers, explicit from the
   abstract about standing on RADIANT / POMDP Coder / Goldman & Zilberstein / the CEGIS-with-LLM
   genre, with the contribution being "connect these four for the first time, in the one setting
   where the connection is checkable" - Findings-track realistic, main-track possible only if the
   experiments are unusually clean. Requires the AAMAS 2026 manual TOC check first.
2. **Blue Sky Ideas track** (4 pages, no experiments required, abstract 5 Nov / paper 12 Nov 2026) -
   the honest venue for a not-yet-fully-differentiated idea, and it buys five more weeks.
3. **Stop the sweep and treat this as the actual finding**: report to whoever this work is for that
   the "apply AAMAS machinery to LLM agents" framing, across five independent attempts checked
   against classical literature, systematically rediscovers 1998-2016 results. That is itself a
   defensible (if unusual) thing to have learned in a week, and cheaper than a sixth candidate.

17 Sep 2026 OpenReview author registration remains a hard gate independent of which path is chosen.

---

## Update 8 Sep 2026 (later): sixth candidate found, checked, and split

After spec 01 also eroded under classical re-examination (see above), a fresh sweep deliberately
avoided the "import a classical AAMAS concept" shape and hunted three LLM-substrate-specific
directions instead (`hunt_A/B/C_*.md`). The strongest survivor,
`04_factual_attrition_mechanism.md`, went through one more adversarial round
(`04_classical_check.md`, `04_scoop_check.md`, `04_venue_fit_check.md`).

**Result: split verdict, not a kill.**

- **H1/H1-alt** (recall-probe dissociation of attentional loss vs. motivated suppression) is
  **closed**. It is Tulving & Pearlstone (1966), "Availability versus accessibility of information
  in memory" - the founding free-recall-vs-cued-recall paradigm - applied to LLM agents rather than
  a new mechanism. The paper's own stated defense ("no way to ask this for a human subject") is
  factually wrong. Spiral-of-silence/pluralistic-ignorance research separately anticipates the
  "motivated suppression" half.
- **H1/H1-alt is also the wrong shape for AAMAS regardless of novelty** - it is a single-agent
  recall/attention probe that does not require a second agent to exist, confirmed by calibrating
  against actual AAMAS 2026 GAAI/COINE accepted-paper samples (all interaction-effect papers; none
  resembling "probe one model, compare to what it said"). Both anchor papers read as NLP-benchmark
  work (one confirmed accepted at EMNLP 2026), not AAMAS-audience work.
- **H2 (compaction hits peer-established commitments specifically) and H3 (shared-transcript vs.
  relay architecture shapes attrition differently) survive both checks clean.** Neither has a
  classical antecedent - they depend on context compaction, an artifact that only exists for LLMs.
  Both are genuinely multi-agent - they require a group converging on a stance to exist at all.
  Scoop check: nothing published since the June 2026 anchor papers closes either.

**Revised recommendation**: restructure the paper to lead with H2/H3 as the headline, demote the
recall probe to a diagnostic instrument embedded within that study rather than a standalone result,
and instrument actual attention weights over the KV-cache as data (the current design only asserts
this mechanism, never measures it - flagged as the single biggest remaining execution risk). Check
arXiv:2602.17674 ("Lost Before Translation," AI-AI relay chains) directly before finalizing scope -
possible partial H3 overlap. Re-check two NeurIPS 2026 agent-evaluation workshops once their
decisions post (expected before 8 Oct) - the one remaining blind spot in the scoop check.

This is the first candidate in the entire sweep where the classical and modern checks did NOT
converge on "kill everything" - they converged on "cut exactly one hypothesis and keep the rest."
That is a meaningfully different, more usable outcome than candidates one through five.
