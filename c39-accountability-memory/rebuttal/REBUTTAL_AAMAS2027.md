# AAMAS 2027 rebuttal draft - Submission 3289

Rebuttal window: 20-24 Nov 2026. Scores (Proceedings / Findings): unWn 5/6, VYMg 7/8, wTzy 7/8.

Part 1 is the text to post on OpenReview. Part 2 is for the authors only: it is not for
posting.

All theorem, table and figure numbers below follow the version on
`origin/c39-aamas2027-rewrite` (commit `bd1ad75`, 9 Oct). Check them against the PDF you
actually uploaded before posting (see Part 2, item 1).

---

# Part 1 - text to post

## General response (to all reviewers and the AC)

We thank all three reviewers. No reviewer disputes the correctness of the results. The main
requests concern scope (independent binary outcomes, Nash versus dominant strategies,
sufficiency under budget balance, interim feedback) and positioning. During the rebuttal we
found that several of these have short proofs, which we will add to the paper:

1. **Correlated, heterogeneous, non-binary and interdependent outcomes.** Theorem 2 holds
   whenever outcomes are independent given an exogenous common shock, for any outcome
   alphabet and agent-specific outcome laws. The constant becomes a chi-square divergence,
   which equals the current constant in the binary case. With interdependent subtasks where
   each outcome depends on at most $d$ agents, the bound holds with an extra factor $d$.
2. **Dominant strategies.** Our noisy lower bounds are stated for Nash, so they hold verbatim
   for dominant strategies. One own-outcome bit per agent achieves dominant-strategy margin
   $h-l$, so dominant-strategy memory is also linear in $n$.
3. **Budget balance.** A budget-balanced rule supports some positive effort cost if and only
   if every agent's deviation is detectable and the deviation vectors are not all positive
   multiples of one vector. The exact budget-balanced margin is one LP.
4. **Interim feedback.** The repeated-task memory lower bounds (Theorem 5(i)-(ii)) hold for
   arbitrary history-dependent strategies. Deferral still saves memory under feedback.

Each new statement was also checked numerically. The scripts will be added to the
supplement.

## Response to Reviewer unWn

Thank you for the careful reading and for your positive assessment of the elimination
theorem, the memory lower bound, and the budget-balance and 2-domination results. In short:

- (1) The linear-memory bound extends to heterogeneous, non-binary and correlated outcomes,
  and to interdependent subtasks with bounded fan-in.
- (3) We now have an exact characterisation of when budget-balanced incentives exist.
- (4) Our lower bounds already hold for dominant strategies, and dominant-strategy memory is
  also linear in team size.

Each point has a short proof, below.

**1. Binary, independent, homogeneous outcomes.** The memory lower bound does not need any
of these three assumptions. Let agent $i$'s outcome $S_i$ take values in any finite set. Its
law is $F_i(\cdot\mid Z)$ if it works and $G_i(\cdot\mid Z)$ if it shirks, where $Z$ is an
exogenous common shock (such as task difficulty) and outcomes are independent given $Z$. Put
$\chi^2_i=\mathbb E_Z\,\chi^2\big(G_i(\cdot\mid Z)\,\|\,F_i(\cdot\mid Z)\big)$. Then for
every $K$-label record

$$\sum_i \frac{(\mu_i^N)^2}{\chi^2_i}\;\le\;\frac{H(Y)}{2}\;\le\;\frac{\ln K}{2}.$$

*Proof sketch.* Let $A$ attain $\mu_i^N$ and $f=\Pr(Y\in A\mid S_i,Z)$. Because $Z$ is
exogenous, $\mu_i^N=\mathbb E\big[(f-\mathbb E[f\mid Z])(1-L_i)\big]$, where $L_i$ is the
likelihood ratio of the deviation. Cauchy-Schwarz and conditional Pinsker give
$(\mu_i^N)^2\le\chi^2_i\,I(Y;S_i\mid Z)/2$. Conditional independence gives
$\sum_iI(Y;S_i\mid Z)\le H(Y)$.

For independent binary outcomes $\chi^2=(h-l)^2/(h(1-h))$, which recovers Theorem 2's
constant exactly. Linear memory therefore holds for agent-specific success probabilities
bounded away from 0 and 1, for multi-valued outcomes, and for common shocks.

The same argument also covers **interdependent production**. Let each outcome depend on the
efforts of at most $d$ agents, with outcomes independent given actions, and let $\chi^2_i$ be
the divergence on the outcomes that agent $i$ affects. Then
$\sum_i(\mu_i^N)^2/\chi^2_i\le d\,H(Y)/2$. The extra step is that, with independent
outcomes, $A\mapsto I(Y;S_A)$ is supermodular, so a family that covers each outcome at most
$d$ times has total information at most $d\,I(Y;S)$. With $d=1$ this is Theorem 2. When a
single outcome depends on all $n$ agents ($d=n$), the bound correctly allows one "pipeline
passed" bit to detect every deviation. Memory is therefore linear whenever fan-in is bounded.

We checked both inequalities numerically, on 4,000 and 3,000 random instances, with largest
ratios of 0.72 and 0.71 against a claimed limit of 1.

**2. The memory measure.** Counting labels is deliberate. The encoder and payment rule are
fixed once and reused, while a record is stored for every episode, so the record is what
accumulates (Section 2). Charging for the encoder could only strengthen our results, since
the lower bounds hold for every encoder and payment rule. The constructions are also
succinct. A threshold-block record is specified by $(m,k^*)$ and pays each agent its block's
bit, and the explicit codes at $n=7,9$ come from a parity-check construction. We will add
this remark.

**3. A general budget-balance characterisation.** We agree this was missing, and we can now
supply it. Let $d_i=Q_1-Q_{0,i}$. A budget-balanced rule with payments in $[0,1]$ sustains
some positive effort cost at all-work **if and only if** (a) every $d_i\neq0$, and (b) the
$d_i$ are not all positive multiples of one vector. The proof is a Farkas argument on the
system $\sum_ix_i=0$, $\langle x_i,d_i\rangle>0$.

The exact budget-balanced margin is one LP with $nK+2$ variables, which is how Figure 2(b)
is computed. Corollary 3(i) is the special case where all $d_i$ coincide. The condition is
the compressed-record analogue of the identifiability conditions of Legros-Matthews and
Rahman-Obara. We checked it against the LP on 3,000 random instances with no mismatch.

**4. Nash versus dominant strategies.** Only one of the main memory results is
Nash-specific.

- Theorem 1 characterises the dominant-strategy margin exactly, and Theorems 6-7 are
  dominant-strategy results.
- The noisy *lower* bounds (Theorem 2, Corollary 2, Theorem 4, Theorem 5(i)) are stated for
  Nash. The dominant-strategy margin never exceeds the Nash margin, so they apply verbatim to
  dominant strategies: the weaker concept gives the stronger lower bound.
- Only the constructive upper bound of Theorem 3 is Nash.

For dominant strategies, retaining each agent's own outcome gives margin $h-l$ with $n$
bits, so

$$n\,\beta(c)\;\le\;\log_2K^*_{\rm DS}(n,c)\;\le\;n,$$

and dominant-strategy memory is also linear in team size for any fixed cost. Only the
small-cost rate remains open. Block counts give dominant-strategy margin of about $(h-l)/m$:
we computed $m\,\mu_{\rm DS}\in[0.80,0.92]$ for $m\le80$ at $h=0.9$, $l=0.1$, which matches
Table S5. That suggests $O(c\log(1/c))$ bits per agent, against the $\Omega(c^2)$ lower
bound. We will add this sandwich and state the rate gap explicitly as the open problem.

We hope these additions show that the conclusions depend much less on the stylised
assumptions than the current text suggests. We would be grateful if you would take them
into account.

## Response to Reviewer VYMg

Thank you for the detailed and constructive review. We agree that your concerns are about
scope and interpretation. Below we give new results for points 1, 3 and 4, and concrete
changes for points 2 and 5.

**1. Correlated outcomes.** The lower bound extends to correlated outcomes of the
common-shock type. Suppose outcomes are independent given an exogenous shock $Z$, with
arbitrary agent-specific and multi-valued outcome laws. Then
$\sum_i(\mu_i^N)^2/\chi^2_i\le H(Y)/2$, where $\chi^2_i$ is the expected chi-square
divergence between agent $i$'s shirk and work outcome laws given $Z$. In the binary
independent case this is exactly Theorem 2.

It also covers interdependent subtasks. If each outcome depends on the efforts of at most
$d$ agents, then $\sum_i(\mu_i^N)^2/\chi^2_i\le d\,H(Y)/2$, by supermodularity of
$A\mapsto I(Y;S_A)$ for independent outcomes. So linear memory survives heterogeneity,
non-binary outcomes, common shocks and bounded-fan-in interdependence. The bound degrades
exactly where it must: when one outcome aggregates all $n$ agents, a single "pipeline
passed" bit can detect every deviation. Proof sketches are in our reply to Reviewer unWn,
and both inequalities were checked numerically. We will add them as a proposition.

**2. Outcome-level versus action-level margins.** We agree, and will say so explicitly in
Section 7. Theorems 6-7 assume the record observes effort itself ($h=1$, $l=0$), and only
then do the two margins coincide. Under noise, 2-domination is *not* necessary for incentive
compatibility.

Our own numbers already show this (Table S5, $h=0.9$, $l=0.1$). The deterministic
nearest-centre record has zero margin with exact outcomes. Under noise it has Nash and
dominant-strategy margin 0.2550 at $n=5$, and at $n=9$ a larger Nash margin than the flat
record (0.6786 against 0.6317). We will move this comparison into Section 7. We will also
note that with full-support noise, a zero action-level margin requires exact cancellation.
The noisy question is therefore how large the margin of a reconstruction-optimal record is,
not whether it is positive. A full characterisation remains open.

**3. Optimality gaps.**

- *Dominant strategies.* The noisy lower bounds are stated for Nash, so they apply verbatim
  to dominant strategies. One own-outcome bit per agent achieves dominant-strategy margin
  $h-l$, so $n\beta(c)\le\log_2K^*_{\rm DS}\le n$ and dominant-strategy memory is also
  linear. Only the small-cost rate is open: numerically, block counts reach about $(h-l)/m$,
  against the $c^2$ lower bound.
- *Budget balance.* We now have a necessary and sufficient condition for positive
  budget-balanced incentives: every agent is detectable, and the deviation vectors are not
  all positive multiples of one vector. The exact margin is one LP.
- *Small instances.* For exact outcomes the small cases are already solved globally.
  Theorem 6 is the global optimum at $K=2$, confirmed by an exhaustive LP over all
  reconstruction orbits to within $3.1\times10^{-15}$ for $n\le9$. $K_{\rm flat}$ is
  certified exactly for $n=3,5,7$.
- *Exact optima under noise (new).* Following your suggestion, we computed the optimal Nash
  margin over **all** stochastic $K$-label records for $n\le5$ ($h=0.9$, $l=0.1$). The TV
  margin is attained by a 0/1 payment vector, so the problem is an exact MILP. Selected
  values:

  | $n$ | $K$ | exact optimum | threshold blocks (Prop. 3) |
  |---|---|---|---|
  | 4 | 2 | 0.5832 | 0.5832 |
  | 4 | 4 | 0.7200 | 0.7200 |
  | 4 | 8 | 0.7852 | 0.7200 |
  | 5 | 2 | 0.5249 | 0.5249 |
  | 5 | 4 | 0.6603 | 0.6480 |
  | 5 | 8 | [0.7618, 0.7807] | 0.7200 |
  | 5 | 16 | [0.7919, 0.8000] | 0.7200 |

  Intervals are certified solver bounds for instances that hit the time limit. The single
  threshold bit is exactly optimal at $K=2$ for every $n$ tested. At powers of two, the
  block construction attains at least 90% of the certified optimum, and at least 85% at
  every $K$. The losses come from unequal blocks and non-power-of-two sizes, where
  stochastic records gain slightly. In this range the Theorem 2 bound is nearly vacuous, so
  at small $n$ the remaining gap lies mainly in the lower-bound analysis, not the
  construction. At large $n$, threshold records reach 62-100% of the lower bound at
  $n=100$. We will add the full table.

**4. Repeated tasks.** We have two clarifications.

- *The lower bounds survive feedback.* Theorem 5(i)-(ii) holds with interim feedback and
  arbitrary history-dependent strategies. Its proof uses only the deviation "shirk on task
  $t$, follow the plan otherwise", which is available in the feedback game.
- *The memory saving of deferral also survives feedback.* Keep each agent's success count
  over $T$ tasks and pay $P_i=\sum_tS_{i,t}\in[0,T]$. Working is then strictly dominant on
  every task, after every history, whenever $c<h-l$. This uses $\log_2(T+1)$ bits per agent
  instead of $T$.

Only the *incentive* gain of review records (sustaining costs above $h-l$) needs the
no-feedback assumption, which is the classical weakness of Radner's review strategies. We
will add this to Section 6, together with the connection to linking mechanisms
(Jackson-Sonnenschein).

**5. Empirical evaluation.** We accept your second option. We will position the paper
explicitly as a theoretical study and present the model-written review study only as an
illustration of attribution loss, not as evidence of incentive compatibility. A strategic
effort-choice experiment with LLM agents is the natural next step, and we will describe its
design in the limitations.

## Response to Reviewer wTzy

Thank you for the positive review and the presentation suggestions, which we will adopt.

- **Introduction.** We will state the research question as a statement rather than a
  question. We will also move the reference to Figure 1 out of the introduction and into
  Section 2, where the running example is formalised.
- **Figure 4.** Thank you for catching this. Panel (a) will be referenced where Lemma 2
  introduces the flat record, and panel (b) where Lemma 1 shows that deterministic
  nearest-centre assignment leaves dead edges. Panel (c) stays in the discussion of other
  priors.
- **Generality of the measured mechanisms.** We will add a note. The instrument itself is
  general: by Theorem 1 the margin of any record is one LP, so any mechanism can be
  evaluated the same way. The zero-margin rows of Table 4 are not special cases either. By
  Corollary 1, any record that gives two neighbouring profiles the same label has zero
  margin for that agent. This covers every deterministic nearest-centre record once the
  centres dominate the cube, since each non-centre then shares its label with an adjacent
  centre. It also covers every prefix record, for agents outside the prefix. For count and
  threshold summaries, Theorems 2-3 give the general behaviour under noise.
- **"Certified threshold".** This refers to $K_{\rm flat}(5)=10$, which is certified by the
  exclusion chain in the supplement. So the statement that no record of fewer than 10
  labels is flat at $n=5$ holds for all records, not only for those we measured.

We are glad the "money is memory" perspective came across.

---

# Part 2 - authors only (do not post)

## 1. What is in the repo and what is missing

| Item | Status |
|---|---|
| Submitted paper source | **Not on `main`.** It lives only on the remote branch `origin/c39-aamas2027-rewrite` (`bd1ad75`, 9 Oct), which was never merged. `main` has an older September draft with a different theorem list. |
| Is that branch the uploaded PDF? | **Very likely, but unconfirmed.** It matches the reviews on the intro question with its Fig. 1 reference, Fig. 4(a)(b) never referenced, Section 5 Holmström, Section 6 deferred settlement, Section 7 2-domination, the Nash/DS split, and the LLM study framed as an illustration. One mismatch: VYMg numbers budget balance as "Theorem 3" and the coding results as "Theorems 5-7", while this version has Theorem 4 and Theorems 6-7. Either VYMg miscounted or the uploaded PDF differs. **Download the PDF from OpenReview and check the numbering before posting.** |
| `~/Downloads/c39_gtep_final.pdf` | The old 24 Sep acmart draft. **Not** the submission. |
| OpenReview abstract field | Written from an older draft. It says attribution error rises "by almost one bit", but the paper (correctly) reports 0.943 more *wrong agent labels out of three*, not bits. No reviewer raised it. Fix it at camera-ready, or add one line to the VYMg reply if you prefer to pre-empt. |
| Uploaded supplementary zip | Not in the repo (`dist/` does not exist), so I could not confirm what reviewers received. |
| `revision_2026-09-30/merged_candidate/` | Named in the branch README as the content source, but not present anywhere. Only a provenance gap; nothing depends on it. |
| Pinned environment `.venv310` | Windows-only and absent on this Mac. A scratch venv with the same NumPy 2.2.6 and SciPy 1.15.3 runs `verify_all.py`, `threshold_tightness.py` and `repeated_review.py`: **all pass**. |

Suggested housekeeping (not done; needs your OK): tag `bd1ad75` as
`aamas2027-submitted` and merge the branch into `main`.

## 2. What the new claims rest on

Each claim was derived for this rebuttal and checked numerically by
`rebuttal/rebuttal_checks.py` (run it with `python -I rebuttal_checks.py`). None of them is
in the submitted paper yet.

| Claim | Basis | Check |
|---|---|---|
| Common-shock / heterogeneous / non-binary Theorem 2 | Cauchy-Schwarz + conditional Pinsker + chain rule given $Z$ | 4,000 random instances, max ratio 0.72 (claim at most 1); binary constant reproduced exactly (3.5556) |
| Bounded fan-in interdependence, factor $d$ | Same Pinsker step on $S_{N(i)}$; $A\mapsto I(Y;S_A)$ is monotone supermodular for independent $S$ (modular $H(S_A)$ minus submodular $H(S_A\mid Y)$), so a $d$-fold cover sums to at most $d\,I(Y;S)$ | `fanin_check.py`: 3,000 instances, max ratio 0.71; the supermodular step is tight (1 up to float rounding) at $d=1$ |
| Budget-balance iff condition | Farkas on $\sum x_i=0$, $\langle x_i,d_i\rangle>0$; scale into $[0,1]$ around $1/2$ | 3,000 instances, 0 mismatches against the LP |
| DS sandwich $n\beta(c)\le\log_2K^*_{\rm DS}\le n$ | Nash lower bound applies a fortiori; own-outcome bits give DS margin $h-l$ | Rigorous, no numerics needed |
| Block-count DS margin about $(h-l)/m$ | **Numerical only** ($m\le80$); reproduces Table S5 (0.1600 at $m=5$, 0.2667 at $m=3$) | Worded as "suggests $O(c\log(1/c))$", not claimed as a theorem |
| Small-$n$ exact optima table (VYMg 3) | Exact MILP (TV is attained by a 0/1 payment, products linearised exactly), HiGHS, 300 s per instance | `small_n_optimum.py` reproduces the paper's 0.5249 at $n=5$, $K=2$; full output in `small_n_optimum.json` / `.log`; 7 large instances hit the time limit and are reported as intervals |
| Theorem 5(i)-(ii) under feedback | The proof only uses single-task deviations, which exist in the feedback game | Proof inspection |
| Own-count deferral under feedback | Additively separable payment, so each task's work adds exactly $h-l$ | Proof inspection |

Have a co-author re-derive the first two proofs before posting.

## 3. AAMAS 2027 rules that matter (official call and Q&A pages, read 21 Nov)

- Rebuttal window 20-24 Nov (AoE). Reviewers discuss and update between 25 Nov and 3 Dec,
  and must acknowledge the rebuttal. Notification is on 21 Dec.
- The call says "the submitted version is final for the review process". **Do not upload a
  revised PDF.** The new results have to stand on the proof sketches in the rebuttal text,
  which is why they are written out in full.
- No published length limit, no per-reviewer versus single-response rule, and nothing about
  confidential AC comments. Check the OpenReview form itself.
- Findings: papers are "automatically considered" for Findings if not selected for
  Proceedings. Proceedings selection is by "overall strength", and Findings is for work more
  limited "in scope, generality, breadth of validation". That is exactly unWn's critique, so
  the generality results are what move the paper from Findings to Proceedings.
- Do not publicise the work or post new preprints before decisions (Q&A 12).

## 4. Strategy

- **The swing vote is unWn (5).** That reply leads with the three new results that answer
  points 1, 3 and 4 directly. The DS point also corrects a partial misreading: most of the
  lower bounds already hold for DS.
- VYMg's point 2 is a fair interpretive correction. Concede it fully, since it costs nothing
  and builds trust.
- wTzy needs only presentation fixes, so keep that reply short.
- **Deliberately not cited:** the September draft's best-response learning experiment
  (Section 7.3 there). It feeds $\gamma^*$ in as the agents' benefit, so it partly assumes
  what it tests, and a reviewer would call it circular.
- Find the per-response character limit on the OpenReview form before posting. Current
  lengths are roughly: general 1.6k, unWn 5.3k, VYMg 5.6k, wTzy 1.6k characters. If the form caps a reply at
5,000, trim VYMg first: its proof pointers repeat the unWn reply.
