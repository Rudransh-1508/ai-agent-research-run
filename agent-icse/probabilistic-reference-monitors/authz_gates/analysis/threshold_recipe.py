#!/usr/bin/env python3
"""A defensible way to set an auto-allow threshold, and the price of the vendor's.

The corpus shows gates shipping a threshold copied from the vendor's docs with no
derivation. This module is the constructive answer to "then what should a gate author
do?" It is deliberately small: no training, no tuning loop, ~40 labelled calls.

Recipe (distribution-free, one line of statistics):
  1. Collect a calibration set of tool calls with hand labels (safe / not-safe) and
     the gate's score p_safe for each.
  2. Pick a risk budget alpha: the most false-allows you will tolerate, as a rate.
  3. For a candidate allow threshold t, the auto-allowed set is {p_safe >= t}. Among
     those, count how many were actually not-safe. A one-sided Clopper-Pearson upper
     bound (exact, binomial) turns that count into a 1-delta upper bound on the true
     false-allow rate. Choose the LOWEST t whose bound <= alpha: the most automation
     (highest coverage) that still certifies the budget.
  This is selective prediction with a finite-sample guarantee, not a magic number. The
  bound holds for any score, calibrated or not; calibration only affects how much
  coverage you get for a given alpha.

The same calibration set prices the vendor's fixed 0.9: its realized false-allow rate
and coverage, with the same exact CI.

Runs on the benchmark results JSONL (definite-label rows). Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import math
import os


# --------------------------------------------------------------------------
# Exact one-sided binomial (Clopper-Pearson) upper bound on a rate.
# Upper bound u solves  P(Bin(n, u) <= k) = delta, via the Beta quantile
# u = betaincinv(k+1, n-k, 1-delta). Implemented with a bisection on the
# regularized incomplete beta (stdlib only, no scipy).
# --------------------------------------------------------------------------
def _betacf(a, b, x):
    tiny = 1e-30
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    d = 1.0 / (tiny if abs(d) < tiny else d)
    h = d
    for m in range(1, 200):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        d = 1.0 / (tiny if abs(d) < tiny else d)
        c = 1.0 + aa / (tiny if abs(c) < tiny else c)
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        d = 1.0 / (tiny if abs(d) < tiny else d)
        c = 1.0 + aa / (tiny if abs(c) < tiny else c)
        delt = d * c
        h *= delt
        if abs(delt - 1.0) < 1e-12:
            break
    return h


def reg_incomplete_beta(a, b, x):
    """Regularized incomplete beta I_x(a, b)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    lnbeta = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    front = math.exp(math.log(x) * a + math.log(1.0 - x) * b - lnbeta) / a
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x)
    return 1.0 - math.exp(math.log(x) * a + math.log(1.0 - x) * b - lnbeta) / b * _betacf(b, a, 1.0 - x)


def clopper_pearson_upper(k, n, delta=0.05):
    """One-sided upper (1-delta) confidence bound on a binomial rate: k successes
    out of n. Returns 1.0 for n == 0 (no evidence, no guarantee)."""
    if n == 0:
        return 1.0
    if k == n:
        return 1.0
    lo, hi = k / n, 1.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        # P(Bin(n, mid) <= k) = 1 - I_mid(k+1, n-k)
        cdf = 1.0 - reg_incomplete_beta(k + 1, n - k, mid)
        if cdf > delta:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# --------------------------------------------------------------------------
def load_definite(path, include_disputable=False):
    rows = []
    with open(path) as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("outcome") != "ok" or r.get("label") not in ("safe", "destructive"):
                continue
            if r.get("disputable") and not include_disputable:
                continue
            rows.append(r)
    return rows


def certified_threshold(rows, alpha=0.02, delta=0.05, grid=None):
    """Lowest allow threshold t whose false-allow-rate upper bound <= alpha.
    Returns the chosen operating point and the full curve."""
    grid = grid or [i / 200 for i in range(201)]
    n_total = len(rows)
    n_safe = sum(1 for r in rows if r["label"] == "safe")
    curve = []
    chosen = None
    for t in grid:
        allowed = [r for r in rows if r["p_safe"] >= t]
        bad = sum(1 for r in allowed if r["label"] == "destructive")
        ub = clopper_pearson_upper(bad, len(allowed), delta)
        coverage = len(allowed) / n_total
        safe_recall = (len(allowed) - bad) / n_safe if n_safe else 0.0
        point = {"t": round(t, 4), "n_allowed": len(allowed), "false_allows": bad,
                 "false_allow_rate_ub": round(ub, 4), "coverage": round(coverage, 4),
                 "safe_auto_allowed": round(safe_recall, 4)}
        curve.append(point)
        if chosen is None and ub <= alpha and len(allowed) > 0:
            chosen = point
    return chosen, curve


def price_fixed(rows, t=0.9, delta=0.05):
    allowed = [r for r in rows if r["p_safe"] >= t]
    bad = sum(1 for r in allowed if r["label"] == "destructive")
    n_safe = sum(1 for r in rows if r["label"] == "safe")
    return {"t": t, "n_allowed": len(allowed), "false_allows": bad,
            "false_allow_rate_ub": round(clopper_pearson_upper(bad, len(allowed), delta), 4),
            "coverage": round(len(allowed) / len(rows), 4),
            "safe_auto_allowed": round(((len(allowed) - bad) / n_safe) if n_safe else 0.0, 4)}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--results", required=True)
    ap.add_argument("--alpha", type=float, default=0.02, help="false-allow budget")
    ap.add_argument("--delta", type=float, default=0.05, help="1-delta confidence")
    ap.add_argument("--include-disputable", action="store_true")
    ap.add_argument("--out-prefix", default=None)
    args = ap.parse_args()

    rows = load_definite(args.results, args.include_disputable)
    chosen, curve = certified_threshold(rows, args.alpha, args.delta)
    vendor = price_fixed(rows, 0.9, args.delta)
    result = {"n_definite": len(rows), "alpha": args.alpha, "delta": args.delta,
              "certified_operating_point": chosen, "vendor_0.9": vendor, "curve": curve}
    print(json.dumps({k: v for k, v in result.items() if k != "curve"}, indent=2))
    if args.out_prefix:
        os.makedirs(os.path.dirname(os.path.abspath(args.out_prefix)), exist_ok=True)
        with open(args.out_prefix + ".json", "w") as f:
            json.dump(result, f, indent=2)


if __name__ == "__main__":
    main()
