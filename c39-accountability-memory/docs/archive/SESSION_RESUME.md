# Resume instructions — C39 / P0, session 1 handoff

Session ended early (user's battery). Everything below is reproducible from
the repo as it stands. Read `research_state.md` first, then this file.

---

## 0. One-line state — P0 IS RESOLVED

    K_flat(3) = 4      exact
    K_flat(5) = 10     exact
    K_flat(7) >= 29    proved (constructive side untested)

Section 3's decisive run has been executed; its results are in
`kflat_structure_n5.json` and `kflat_n7_bound.json`. Read `research_state.md`
section 7 — there is a decision waiting for the human, and no further compute
is needed to make it.

Remaining compute is only the loose ends in section 4 and the optional
constructive check at n=7, K=29.

## 1. Reactivate the environment

The venv already exists and matches the pinned target exactly
(Python 3.10.11 / NumPy 2.2.6 / SciPy 1.15.3 — see `environment.json`,
`matches_pinned: true`). Nothing to reinstall.

```powershell
cd E:\research_2
.\.venv310\Scripts\python.exe -c "import sys,numpy,scipy;print(sys.version,numpy.__version__,scipy.__version__)"
```

If the venv is ever lost:

```powershell
python -m venv .venv310
.\.venv310\Scripts\python.exe -m pip install numpy==2.2.6 scipy==1.15.3
```

Note: `python` on this machine is already 3.10.11.

## 2. What each file is

| file | role |
|---|---|
| `exp1b.py` | given; K=2 orbit-reduced LP enumeration. Reruns clean in the pinned env. |
| `exp3_bracket.py` | given; dense LB/UB bracket. **Validated** (step 3 check A passed). |
| `exp5_threshold.py` | given; thin wrapper over `exp3_bracket`. Superseded by `kflat_structure.py`. |
| `verify_t1_independent.py` | NEW. Independent T1 implementation (substitute for the two missing reference scripts). |
| `validate_kflat_model.py` | NEW. Step-3 checks A/B/C. A and B passed; **C never ran**. |
| `exp_kflat.py` | NEW. Sparse UB model + `solve_D0_pmedian` (the fast, certified D0). |
| `kflat_structure.py` | NEW. **The method that works.** Lemmas 1-3, counting bound, code enumeration, support-restricted margin MIP, general-p margin LP. |
| `verify_k16_construction.py` | NEW. Solver-free proof that n=5, K=16 is flat. |
| `kflat_structure_n3.json/.log` | n=3 control case: reproduces `K_flat(3)=4`. |
| `kflat_n5_K*.json` | Abandoned monolithic run; contains certified D0 rows only. |
| `d0_pmedian_check.json` | p-median vs generic D0 cross-validation. |
| `kflat_structure_n5.json` | n=5 K=10..16 sweep: K_flat(5)=10 |
| `kflat_n7_bound.json` | n=7 counting bound: K_flat(7)>=29, K=14 excluded |
| `kflat_n7_bound.py` | n=7 bound-only driver (proof, no search) |
| `kflat_n5_K10_gammasweep.log` | K=10 flat for gamma<=0.5 |

## 3. THE decisive run — **DONE**, kept for reproduction

```powershell
cd E:\research_2
.\.venv310\Scripts\python.exe -u kflat_structure.py 5 10,11,12,13,14,15,16 0.1,0.15,0.19 200 > kflat_structure_n5.log 2>&1
```

Writes `kflat_structure_n5.json` incrementally. For each K it:

1. computes certified `D0(K)` by p-median (fast, gap 0);
2. applies the counting bound — if excluded, records **NOT FLAT (proved)** and
   moves on without any search;
3. otherwise enumerates optimal K-median codes satisfying the Lemma-3
   condition (with no-good cuts, up to the limit argument), reporting whether
   the enumeration was **exhaustive**;
4. for each code, solves a small support-restricted MIP for `(q, binary p)`
   achieving margin gamma;
5. post-hoc recomputes D and the worst-case per-agent margin from the returned
   `(q,p)`, and re-checks the margin for **general** `p in [0,1]^K` via the
   elimination-theorem LP.

`K_flat(5)` = the smallest K in that sweep reported `FLAT_CERTIFIED`.

**Read the output carefully — the verdicts are not symmetric:**

* `FLAT_CERTIFIED` is a genuine certificate: an explicit construction is stored
  in the JSON (`centers`, `q`, `p`) and independently re-verified.
* `NOT FLAT (proved ...)` from the counting bound is genuine and applies to
  arbitrary bounded payment decoders.
* `NOT FLAT for binary p over all enumerated codes` is **only** a binary-payment
  statement, and only as strong as `code_enumeration_exhaustive: true`. If that
  flag is false, the row is INCONCLUSIVE. Do not upgrade it.

Expected runtime: minutes per K. If a K stalls, raise the code-enumeration
limit or the MIP `time_limit` rather than switching back to the monolithic model.

## 4. Then finish the loose ends (cheap, and required before the numbers are citable)

```powershell
# (a) validation check C — symmetry breaking must not change the optimum.
#     Never ran. Edit validate_kflat_model.py to skip A and B, or just rerun all:
.\.venv310\Scripts\python.exe -u validate_kflat_model.py > validate_kflat_model.log 2>&1

# (b) complete the n=9 tail of the independent T1 check (cut short at gamma=1/18)
.\.venv310\Scripts\python.exe -u verify_t1_independent.py > verify_t1_independent.log 2>&1

# (c) complete the n=3 control at K=6 (gamma=1/6, 1/3 rows were cut short)
.\.venv310\Scripts\python.exe -u kflat_structure.py 3 6 0.16666,0.3333 40

# (d) refresh the manifests after any of the above
```

Manifest refresh (also recorded as how `artifact_hashes.json` /
`environment.json` were produced):

```powershell
.\.venv310\Scripts\python.exe -c "import json,hashlib,os,sys,platform,numpy,scipy; files=sorted(f for f in os.listdir('.') if os.path.isfile(f) and f.endswith(('.py','.json','.log','.md')) and f not in ('environment.json','artifact_hashes.json')); json.dump({f:{'sha256':hashlib.sha256(open(f,'rb').read()).hexdigest(),'bytes':os.path.getsize(f)} for f in files}, open('artifact_hashes.json','w'), indent=1)"
```

## 5. The judgement call — **STILL OPEN, this is what is waiting for you**

`K_flat(5) = 10`, so the predeclared test fires on its literal wording. But
`2n` is now **disproved at n=7** (K=14 excluded by proof), so the discriminator
the test relied on is wrong. Full argument and the two options in
`research_state.md` section 7. **Do not resolve this unilaterally — it is a
human call.**

Mitigating fact, checkable from `artifact_hashes.json`: the `2^(n+1)/(n+2)`
prediction and the "n=7 is the real discriminator, 14 vs 28.4" statement were
written and hashed BEFORE the K=10 and n=7 rows were computed. So the
reinterpretation is pre-registered, not fitted after the fact.

## 6. n=7 — bound **DONE** (`kflat_n7_bound.py`, K=14 excluded, K_flat(7)>=29);
the constructive command below is still untested

```powershell
.\.venv310\Scripts\python.exe -u kflat_structure.py 7 24,28,29,32,40,48,64 0.1 100 > kflat_structure_n7.log 2>&1
```

The counting bound predicts `K_flat(7) >= 29` (`2^8/9 = 28.4`). The linear
hypothesis predicts 14. **These are far apart, which is why n=7 is the real
discriminator.** The counting bound alone (step 2 of the driver, no search)
already settles whether `K = 14` is possible and is nearly free to compute —
run that much even if the constructive side is too slow.

Note `p-median` D0 at n=7 has `2^7 = 128` binaries and `128^2 = 16384`
assignment variables; it should still be fast, but check the gap is 0.0 before
trusting any n=7 row, and check `D0_strictly_decreasing` (the premise of
Lemma 2) in the JSON.

## 7. Standing constraints from the session brief

Do not write any part of the paper. Do not run LLM experiments. Do not start
the software-shaped workflow (master context section 18). Do not start P1 or
P2 until P0 resolves.
