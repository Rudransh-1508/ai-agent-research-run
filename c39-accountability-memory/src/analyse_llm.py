"""Score the LLM-agent experiment against the predictions registered for it.

Compaction and the judge together induce a channel on the cube,

    q[s][y] = P(judge's predicted profile = y | true effort profile = s),

estimated from the episodes. Once that channel exists the paper's own
instruments apply unchanged: the margin comes from the Theorem 3 LP and the
distortion from Bayes decoding, exactly as in the synthetic experiments. Storage
is the record's real size in bytes.

Two distortions are reported and they answer different questions. `D_judge` is
the error the judge actually made -- the practical attribution number. `D_bayes`
is the best any decoder could do from the same channel, which is the quantity
the theory bounds.

    python src/analyse_llm.py
"""
import json, math, sys, pathlib
from collections import defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "experiments"))
from c39.paths import data
from experiment_agents import popcount, distortion, margin
import numpy as np

N = 3
IDENTITY = {"full_trace", "per_agent_summary"}
ORDER = ["full_trace", "per_agent_summary", "artifact_multiset",
         "global_summary", "final_output"]

raw = json.load(open(data("experiment_llm.json")))
eps = [e for e in raw["episodes"] if "error" not in e]
bad = len(raw["episodes"]) - len(eps)
cfg = raw["config"]
print(f"model {cfg['model']} (temp {cfg['temperature']}, seed {cfg['seed']})")
print(f"{len(eps)} usable episodes, {bad} failed, "
      f"{raw['tokens']['prompt']}+{raw['tokens']['completion']} tokens\n")

NS = 1 << N
results = {}
for rec in ORDER:
    counts = np.zeros((NS, NS))
    dropped = 0
    sizes = []
    for e in eps:
        p = e["predictions"].get(rec)
        if p is None:
            dropped += 1
            continue
        y = sum(b << i for i, b in enumerate(p))
        counts[e["profile"], y] += 1
        sizes.append(e["bytes"][rec])
    seen = counts.sum(axis=1)
    if (seen == 0).any():
        print(f"  [SKIP] {rec}: profiles with no episodes {list(np.where(seen==0)[0])}")
        continue
    q = counts / seen[:, None]
    pi = np.full(NS, 1.0 / NS)
    d_judge = sum(pi[s] * q[s, y] * popcount(s ^ y)
                  for s in range(NS) for y in range(NS))
    results[rec] = dict(
        bytes=float(np.mean(sizes)),
        D_judge=float(d_judge),
        D_bayes=float(distortion(N, pi, q)),
        gamma=float(margin(N, q)),
        episodes=int(seen.sum()), unparsed=dropped)

print(f"{'record':<20}{'bytes':>8}{'D_judge':>10}{'D_bayes':>10}{'gamma':>9}"
      f"{'identity':>10}")
for rec in ORDER:
    if rec not in results:
        continue
    r = results[rec]
    print(f"{rec:<20}{r['bytes']:8.0f}{r['D_judge']:10.3f}{r['D_bayes']:10.3f}"
          f"{r['gamma']:9.3f}{'yes' if rec in IDENTITY else 'no':>10}")


# --- how much can the margin estimate be trusted at this sample size? -------
#
# gamma is a MINIMUM over agents of an LP on the estimated channel. If, for some
# agent i and some teammate profile, the judge happened to return the same
# predictions with and without that agent's effort, then d_i = 0 exactly and
# gamma collapses to 0. Coincidental ties can only push the estimate DOWN, never
# up, so a small-sample gamma is a one-sided artefact rather than a measurement.
per_profile = {}
for e in eps:
    per_profile[e["profile"]] = per_profile.get(e["profile"], 0) + 1
m_min = min(per_profile.values()) if per_profile else 0
ties = []
for rec in [r for r in ORDER if r in results]:
    rows = {}
    for e in eps:
        rows.setdefault(e["profile"], []).append(tuple(e["predictions"][rec]))
    for i in range(N):
        for sm in range(1 << (N - 1)):
            lo = sm & ((1 << i) - 1)
            hi = (sm >> i) << (i + 1)
            s0 = lo | hi
            s1 = s0 | (1 << i)
            if rows.get(s0) and sorted(rows.get(s0, [])) == sorted(rows.get(s1, [])):
                ties.append((rec, i, format(sm, "0" + str(N - 1) + "b")))
print("")
print("margin reliability: " + str(m_min) + " episodes per profile; "
      + str(len(ties)) + " exact-tie cells force a zero margin")
for rec, i, sm in ties[:4]:
    print("   " + rec + ": agent " + str(i) + ", teammates " + sm
          + " -- identical predictions with and without that agent's effort")
if ties:
    print("   gamma is therefore biased DOWNWARD here and is not interpretable; "
          "see L5 below.")


# --- the attribution gap, with a bootstrap interval ------------------------
def _err(e, rec):
    p = e["predictions"].get(rec)
    if p is None:
        return None
    return sum(((e["profile"] >> i) & 1) != p[i] for i in range(N))


_rng = np.random.default_rng(20260915)
pairs = [(_err(e, "full_trace"), _err(e, "artifact_multiset")) for e in eps]
pairs = [p for p in pairs if None not in p]
if pairs:
    dif = []
    for _ in range(20000):
        idx = _rng.integers(0, len(pairs), len(pairs))
        dif.append(np.mean([pairs[k][1] for k in idx])
                   - np.mean([pairs[k][0] for k in idx]))
    lo_ci, hi_ci = np.percentile(dif, [2.5, 97.5])
    ft_e = float(np.mean([p[0] for p in pairs]))
    am_e = float(np.mean([p[1] for p in pairs]))
    print("")
    print("attribution error over " + str(len(pairs)) + " episodes (bits wrong of "
          + str(N) + "):")
    print("   full_trace        %.3f" % ft_e)
    print("   artifact_multiset %.3f   same text, ~30 bytes of labels apart" % am_e)
    print("   difference        %.3f  95%% bootstrap CI [%.3f, %.3f]  excludes zero: %s"
          % (am_e - ft_e, lo_ci, hi_ci, lo_ci > 0))
    results["_attribution_gap"] = dict(
        full_trace=ft_e, artifact_multiset=am_e, difference=am_e - ft_e,
        ci95=[float(lo_ci), float(hi_ci)], episodes=len(pairs))


# --- decomposition: how much of the gap is assignment rather than content? ---
import itertools as _it
dec = {}
for rec in ("full_trace", "artifact_multiset"):
    raw_e, best_e, cnt_e = [], [], []
    for e in eps:
        truth = [(e["profile"] >> i) & 1 for i in range(N)]
        p_ = e["predictions"].get(rec)
        if p_ is None:
            continue
        raw_e.append(sum(t != q for t, q in zip(truth, p_)))
        best_e.append(min(sum(t != q for t, q in zip(truth, perm))
                          for perm in _it.permutations(p_)))
        cnt_e.append(abs(sum(truth) - sum(p_)))
    dec[rec] = dict(raw=float(np.mean(raw_e)), best_perm=float(np.mean(best_e)),
                    count=float(np.mean(cnt_e)))
print("")
print("error decomposition (raw / best-relabelling / count-only):")
for rec, v in dec.items():
    print("   %-20s %.3f  %.3f  %.3f" % (rec, v["raw"], v["best_perm"], v["count"]))
results["_decomposition"] = dec

# --- per-agent margin, to show which agent binds each record -----------------
per_agent = {}
for rec in [r for r in ORDER if r in results]:
    counts = np.zeros((NS, NS))
    for e in eps:
        p_ = e["predictions"].get(rec)
        if p_ is None:
            continue
        counts[e["profile"], sum(b << i for i, b in enumerate(p_))] += 1
    q = counts / counts.sum(axis=1)[:, None]
    # per-agent margin: the same LP restricted to one agent. gamma is their min.
    from scipy.optimize import linprog as _lp
    gs = []
    for i in range(N):
        A = []
        for sm in range(1 << (N - 1)):
            lo = sm & ((1 << i) - 1); hi = (sm >> i) << (i + 1)
            s0 = lo | hi; s1 = s0 | (1 << i)
            A.append(q[s1] - q[s0])
        A = np.array(A); T, K = A.shape
        r = _lp(np.concatenate([np.zeros(T), 0.5 * np.ones(K)]),
                A_ub=np.block([[A.T, -np.eye(K)], [-A.T, -np.eye(K)]]),
                b_ub=np.zeros(2 * K),
                A_eq=np.concatenate([np.ones(T), np.zeros(K)])[None, :], b_eq=[1.0],
                bounds=[(0, None)] * (T + K), method="highs")
        gs.append(float(r.fun))
    per_agent[rec] = gs
print("")
print("per-agent margin (the minimum over these is gamma):")
for rec, gs in per_agent.items():
    print("   %-20s " % rec + "  ".join("%.3f" % g for g in gs)
          + "   binds: agent %d" % int(np.argmin(gs)))
results["_per_agent_margin"] = per_agent

print("\nScoring the predictions registered in addendum 3\n")


def verdict(tag, label, ok, detail=""):
    print(f"  [{'CONFIRMED' if ok else 'FALSIFIED':>9}] {tag} {label}"
          + (f"\n              {detail}" if detail else ""))


have = [r for r in ORDER if r in results]
g = {r: results[r]["gamma"] for r in have}

if len(have) < len(ORDER):
    print(f"  [NOT EVALUABLE] only {len(have)}/{len(ORDER)} records have every "
          f"profile covered; predictions are not scored on partial data.")
    print(f"                  present: {have}")
    sys.exit(0)

verdict("L1 [U]", "margin ordering matches the synthetic episode experiment",
        all(g[a] >= g[b] - 1e-9 for a, b in zip(have, have[1:])),
        " >= ".join(f"{r}:{g[r]:.3f}" for r in have))

if "full_trace" in g and "artifact_multiset" in g:
    ft, am = g["full_trace"], g["artifact_multiset"]
    drop = (ft - am) / ft if ft > 1e-9 else 0.0
    verdict("L2 [U]", "same text, attribution removed, margin drops by >= a third",
            am < ft and drop >= 1 / 3,
            f"full_trace {ft:.3f} vs artifact_multiset {am:.3f} "
            f"({drop:.0%} drop); bytes "
            f"{results['full_trace']['bytes']:.0f} vs "
            f"{results['artifact_multiset']['bytes']:.0f}")

if "final_output" in g:
    verdict("L3 [U]", "final_output margin is near zero but not exactly zero",
            0 < g["final_output"] < 0.1, f"{g['final_output']:.4f}")

if {"full_trace", "artifact_multiset"} <= set(results):
    dft, dam = results["full_trace"]["D_judge"], results["artifact_multiset"]["D_judge"]
    gap_D = abs(dam - dft) / max(dft, 1e-9)
    if g["full_trace"] <= 1e-9:
        print("  [NOT EVALUABLE] L4: gamma(full_trace) is zero, so a relative "
              "gap in gamma is undefined.")
        print(f"                  D gap is {gap_D:.0%}; revisit once gamma is "
              f"estimable.")
    else:
        gap_g = abs(g["artifact_multiset"] - g["full_trace"]) / g["full_trace"]
        verdict("L4 [U]", "D is not ordered as sharply as gamma", gap_D < gap_g,
                f"relative gap in D {gap_D:.0%} vs in gamma {gap_g:.0%}")

if "full_trace" in g:
    usable = g["full_trace"] > 0.05
    verdict("L5 [U]", "the judge produces a usable signal on the full trace",
            usable, f"gamma(full_trace) = {g['full_trace']:.3f}"
                    + ("" if usable else "  -- EXPERIMENT INCONCLUSIVE, "
                                         "the ordering below is noise"))

json.dump(results, open(data("results") / "experiment_llm_scored.json", "w"), indent=1)
print("\nwrote results/experiment_llm_scored.json")
