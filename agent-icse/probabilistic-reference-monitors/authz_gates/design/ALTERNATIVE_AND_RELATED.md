# Two designs for the gate, and the 2026 literature they sit in

We evaluate two designs for the empty cell and report the tradeoff between them, rather than
a single "best" gate. The second is drawn from where the 2026 literature has converged.

## Where recent work converged (2026)

The dominant answer to "secure a tool-using agent" is now: **enforce outside the model with
a deterministic policy, and consult the model at most once per task - never per call.**

- **Progent** (Securing AI Agents with Privilege Control, arXiv 2504.11703): programmable
  least-privilege policies over tool calls in a DSL; the model proposes policy *expansion*,
  an SMT check gates it. Cuts AgentDojo indirect-injection success 39.9% -> 1.0%.
- **CaMeL** (Defeating Prompt Injections by Design, arXiv 2503.18813): separates control from
  data flow; capabilities tag a value's provenance and permitted sinks, checked at tool-call
  sinks. 77% of AgentDojo tasks solved under attack with no successful injection.
- **ToolFence** (2026): checks where sensitive argument values come from and whether calls
  stay within assigned budgets, using structured rules over permitted tools and arg sources.
- **Intent-graph auditing** (Least-Privilege Auditing of Agent Tool Calls with Intent Graphs
  and Reasoning-Guided Escalation, arXiv 2611.11305): one LLM call per *task* derives an
  executable intent graph; every tool call is then checked by a **deterministic loop with no
  LLM call**, with reasoning-guided escalation for the residue.
- **LeanGuard** (arXiv 2611.02332): every proposed call checked against a Lean4 policy
  (state predicates + scoped temporal operators over history), fail-closed.
- **ChainCaps** (arXiv 2605.26542): monotonic capability attenuation for composition safety;
  and surveys (Rethinking Access Control for AI Agents, arXiv 2611.06764; the Springer
  authorization-assurance review, 2026) frame least-privilege as authority narrowing and note
  that evaluable revocation claims are still largely missing.

Common thread: take the model out of the per-call path; make per-call enforcement
deterministic and least-privilege; use the model sparingly and out-of-band.

## Design A - per-call asymmetric gate (model-in-the-loop)

`gate.py`. Deterministic layers deny freely and allow only from a small parsed read-only /
scratch-write set; the model may allow only above a version-certified p_safe threshold; a
total failure function denies-under-bypass / asks-in-default on everything else. Needs no task
context. Pays a model call on the ambiguous minority.

## Design B - deterministic least-privilege capability gate (no model)

`gate_capability.py`. The per-call, fixed-policy degenerate of the 2026 paradigm: a
default-deny capability allowlist (reads, read-only shell, scratch writes) with **no model
call**. The faithful form derives the capability set per task from the user's objective (one
model call per task); our corpus is isolated tool calls with no task context, so that form is
future work and B here uses a fixed policy. B is what A would be with the model path removed.

## Result: a Pareto tradeoff, not a winner (same bench, both host modes)

| design | destr main | destr held-out | padded | safe auto-approved | safe blocked (bypass) | median latency |
|---|---|---|---|---|---|---|
| A (model-in-the-loop) | 0/127 | 0/100 | 0/220 | **94/94** | 0 | 0.49s (47% fast path) |
| B (pure capability)   | 0/127 | 0/100 | 0/220 | 60/94 | **34/94** | ~0.01-0.10s (no model) |

Both are perfect on protection and padding after a shared fix (see below). They separate on
automation vs latency:

- **B is maximally protective and ~10-50x faster** (no model round-trip), but **over-restrictive**:
  it blocks 34/94 safe calls it cannot clear from syntax alone - `curl`/`HEAD` GETs to benign
  hosts, `pip show`, `npm view` - because a fixed policy cannot distinguish a safe read from
  exfiltration without judgment. Under bypass those become false-denies (lost availability).
- **A recovers all 34 safe automations** under a certified false-allow budget (<=3.1% on the
  calibration set), at the cost of a model call on ~half of decisions. This is the concrete
  value of the probabilistic layer that the pure-policy trend gives up: semantic judgment of
  the safe-but-not-syntactically-obvious middle.

The paper's position: the 2026 move to deterministic-only enforcement buys protection and
latency but pays friction on exactly the calls that make an agent useful; a *certified*
model-in-the-loop layer, bounded and host-mode-aware, buys that friction back without
reopening the protection hole - provided its threshold is re-certified across model versions
(the distribution-shift caveat, Conformity Breaks Conformal Prediction, arXiv 2609.04445).

## A bug both designs shared, found by the comparison

Building B exposed an argument-blind-allowlist hole in the shared read-only set: `env`
(and other command *launchers* - `nohup`, `setsid`, `timeout`, `xargs`, `sudo`, ...) were
treated as read-only, so `env rm -rf ~/.aws` was allowlisted. B leaked it (1/100 held-out);
A was saved only because dcg happened to catch that `rm`. The fix (a `COMMAND_LAUNCHERS`
denylist in `is_readonly_command`) hardened both. That the exact failure class this paper
indicts - allowlists that ignore arguments - appeared in our own gate, and was caught by
stress-testing rather than by inspection, is itself a finding about how these gates should
be validated.
