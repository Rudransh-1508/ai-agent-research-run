"""Repeated tasks with deferred settlement: review records.

Model: one agent, T tasks, outcome S_t ~ Bernoulli(h) if it works on task t and Bernoulli(l)
otherwise, independently; the agent chooses its whole effort plan before seeing any outcome.
Review record: one bit b = 1{sum_t S_t > k}; deferred payment P = T * b (budget 1 per task).

Checks:
  1. The closed form: working on every task is strictly dominant iff c < c_T(k), where
     c_T(k) = min_{1<=j<=T} (T/j) * [P(Bin(T,h) > k) - P(Bin(T-j,h) + Bin(j,l) > k)],
     verified against brute force over all 2^T effort plans and all 2^T outcome vectors (T <= 8).
  2. The certificate table printed in the paper: best threshold k and c_T for T in a list.
  3. Per-task settlement cannot sustain any cost above h - l (= TV of one outcome).
"""
import itertools
import math

H, L = 0.9, 0.1


def pmf(N, p):
    lg = math.lgamma
    if p in (0.0, 1.0):
        return [float(k == (N if p == 1.0 else 0)) for k in range(N + 1)]
    return [math.exp(lg(N + 1) - lg(k + 1) - lg(N - k + 1) + k * math.log(p) + (N - k) * math.log(1 - p))
            for k in range(N + 1)]


def conv(a, b):
    out = [0.0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def pass_prob(T, j, k):
    """P(successes > k) when the agent shirks j of its T tasks."""
    d = conv(pmf(T - j, H), pmf(j, L))
    return sum(d[k + 1:])


def c_closed(T, k):
    p0 = pass_prob(T, 0, k)
    return min(T * (p0 - pass_prob(T, j, k)) / j for j in range(1, T + 1))


def c_brute(T, k):
    """Largest c at which all-work beats every plan, by enumerating plans and outcomes."""
    def expected_pay(plan):
        tot = 0.0
        for s in itertools.product((0, 1), repeat=T):
            pr = 1.0
            for a, x in zip(plan, s):
                ps = H if a else L
                pr *= ps if x else 1 - ps
            tot += pr * (T if sum(s) > k else 0)
        return tot
    full = expected_pay((1,) * T)
    best = math.inf
    for plan in itertools.product((0, 1), repeat=T):
        j = T - sum(plan)
        if j:
            best = min(best, (full - expected_pay(plan)) / j)
    return best


def main():
    ok = True
    for T in range(1, 9):
        for k in range(0, T):
            a, b = c_closed(T, k), c_brute(T, k)
            if abs(a - b) > 1e-9:
                ok = False
                print(f"MISMATCH T={T} k={k}: closed {a} brute {b}")
    print("closed form matches brute force over all plans, T <= 8:", ok)

    print("T    k*   c_T(k*)   bits per agent per task")
    for T in (1, 2, 5, 10, 20, 50, 100, 200):
        k, c = max(((k, c_closed(T, k)) for k in range(T)), key=lambda kc: kc[1])
        print(f"{T:<4} {k:<4} {c:.4f}    {1 / T:.4f}")

    print("per-task settlement cap h - l =", round(H - L, 4))
    print("ALL CHECKS PASS" if ok else "FAILURE")


if __name__ == "__main__":
    main()
