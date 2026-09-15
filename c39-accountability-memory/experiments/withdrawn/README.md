# Withdrawn: the general-prior threshold scripts

These two scripts, and the artifacts they produced, computed

    K_flat(pi) = min { K : some pi-optimal K-median set is 2-DOMINATING }

That specification is **wrong**. Lemma 3' (necessity) says each non-centre has at
least two centres at *its own nearest distance* `d(s,C)`, which is 2-domination
only when the optimal code is dominating. The uniform prior makes it dominating
above `gamma(Q_n)`, so Theorem 9 is unaffected. A tilted prior need not, and
there the 2-domination test is strictly too strong.

They are kept, unmodified, because they are the evidence for the methodological
point made in Appendix A: `prior_threshold.py` (a MILP) and `verify_all.py` block
G (solver-free enumeration) shared no code, agreed on 6, 28 and 122 at n = 3, 5, 7,
and were both wrong, because they encoded the same wrong specification. Agreement
between independent implementations of one specification is not evidence that the
specification is right.

The corrected computation is `experiments/prior_threshold.py`, which does not test
a proxy condition at all: it exhibits a flat record and measures its distortion
and margin directly.

Do not cite any number in `results/withdrawn/`.
