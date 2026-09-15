# Claude Code kickoff — C39, session 1

Paste the block below as your first message in Claude Code, from the root of
the research repo, after copying `C39_UPDATE_2026-09-13.md` and the three
`exp*.py` files into the repo.

---

You are executing an adversarial research investigation on candidate C39, not
giving suggestions. Read `agent_research_master_context.md` for background and
`C39_UPDATE_2026-09-13.md` for the current corrected state. The update
supersedes section 26 of the master context.

Operating rules from section 23 of the master context apply in full. In
particular: predeclared kill tests, cheapest kill first, strong baselines
mandatory, exact theorem scopes, upper bounds are not optimality, failed
searches are not evidence of absence, and never silently broaden a theorem
after a failed test.

**Session goal: resolve P0, the flatness threshold `K_flat(n)`.** Nothing else
in this session.

Steps:

1. Recreate the pinned environment (Python 3.10.11, NumPy 2.2.6, SciPy 1.15.3)
   in a venv. The bracket scripts were developed under 3.12 / 2.4.4 / 1.17.1
   and must be re-validated before their outputs enter `artifact_hashes.json`.

2. Validate `exp1b.py` against the existing `verify_incentive_distortion.py`
   and `incentive_distortion_onebit_extension.py`. Both should agree on T1 at
   n=3,5,7,9. If they disagree, stop and report; do not proceed.

3. Validate `exp3_bracket.py` by checking that its K=2 output reproduces the
   T1 closed form at n=3 and n=5 with MIP gap 0. It did in development. If it
   does not reproduce in the pinned environment, the bracket model is wrong and
   everything downstream is void.

4. Compute `K_flat(5)`. Use the upper-bound model only (`mode="UB"` in
   `exp3_bracket.solve`), which has `2nK` binaries. For `K` in `4,6,8,10,12,16`
   compute `D0 = UB(K, 0)` and `UB(K, gamma)` at `gamma` in `0.1, 0.15, 0.19`.
   `UB(K,gamma) == D0(K)` with MIP gap 0 proves flatness at that K. Record MIP
   gaps for every solve; a nonzero gap makes the row inconclusive, not negative.
   Expect long solves. Run each as a separate process writing incrementally to
   JSON so partial progress survives. Add symmetry-breaking constraints on the
   label ordering if HiGHS stalls.

5. If n=5 resolves, do n=7 for `K` in `8,16,32,64` at one gamma value, accepting
   that some rows will be inconclusive.

**Predeclared kill test, written before running:** if `K_flat(5) <= 10`, the
reconstruction-incentive tension is a small-K artifact, the organizational
significance claim in its current form is dead, and the correct output of this
session is a downgrade recorded in `research_state.md` plus a new candidate
batch, not a rescue of C39. C39 is not sacred.

**If `K_flat(5) >= 16`,** the tension survives sub-exponential records, the
significance claim holds, and the next session moves to P1 (prior art with the
Boolean-analysis framing) and P2 (closing the K=3 bracket).

Deliverables for this session, written to the repo:

- `exp_kflat.py` and its raw JSON outputs, with MIP gaps recorded per solve
- a new row per solve in `experiment_log.md`, distinguishing certified from
  inconclusive
- an updated `research_state.md` stating `K_flat(5)` or explicitly why it could
  not be determined
- `environment.json` and `artifact_hashes.json` updated for anything that ran
  in the pinned environment

Do not write any part of the paper. Do not run LLM experiments. Do not start
the software-shaped workflow in section 18. Report the number.
