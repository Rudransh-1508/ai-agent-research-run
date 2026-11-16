# Related work and positioning (draft for the paper)

Each citation below was checked against its arXiv / proceedings page on 2026-11-17; keys
refer to `paper/refs.bib`. The paper's claim to novelty is narrow on purpose: we do not
propose a new classifier or a new attack. We **measure the authorization gates people
actually deploy**, find that their security fails at the integration seams with the host
(permission mode, failure handling, argument-blind allowlists, prompt/threshold coupling),
and show a gate design plus a certification procedure that closes those seams.

## 1. Guardrail systems for agents (what the deployed gates are instances of)

- **LlamaFirewall** [llamafirewall2025] (arXiv 2505.03574): Meta's open-source,
  production guardrail framework - PromptGuard, an agent-alignment checker over chain of
  thought, CodeShield static analysis. *Difference:* it proposes and evaluates a guardrail
  in isolation; we evaluate guardrails as integrated into a host, where the host's permission
  mode and failure contract decide whether a verdict is enforced. Our results show the
  enforced outcome depends on the host mode, not on the verdict: jev-engineering's guard
  configuration lets 0/127 destructive calls run in Claude Code's default mode and 75/127
  under auto mode, with the same gate code and the same model (scorecard-all).
- **Progent** [progent2025] (arXiv 2504.11703) and **CaMeL** [camel2025] (arXiv 2503.18813):
  deterministic privilege control / control-data separation. They motivate our Design B
  (deterministic least privilege) and the Pareto comparison with Design A.
- The measured hooks (jev-guard, jev-engineering, AgentGuards, CC Safety Net, dcg, sdkks)
  are practitioner systems with no peer-reviewed evaluation; FRAMING_EVIDENCE.md quotes their
  protection claims.

## 2. Benchmarks for agent safety (what our corpus differs from)

- **AgentDojo** [agentdojo2024] (arXiv 2406.13352): 97 tasks, prompt-injection attacks and
  defenses in an extensible environment. **ToolEmu** [toolemu2024] (ICLR 2024): LM-emulated
  tools and an LM safety evaluator (68.8% of found failures valid in reality).
  **R-Judge** [rjudge2024] (arXiv 2401.10019): 162 interaction records to test LLMs as
  safety judges.
- *Difference:* they evaluate agents or judges on emulated or recorded traces with labels
  from annotators or an LM evaluator. Our labels are **verified by executing every command**
  in a disposable sandbox seeded with real victim state (372 confirmed, 0 mismatches), our
  attacks include real ATT&CK procedures (Atomic Red Team) and GTFOBins techniques plus a
  pre-registered blind set, and the unit of evaluation is the gate *as deployed in the host*,
  in each permission mode, including its failure behaviour under injected faults.

## 3. Thresholds with guarantees (what the certification recipe builds on)

- **Selective classification** [geifman2017] (NeurIPS 2017; also [elyaniv2010],
  reject option [chow1970]): pick a confidence threshold so selective risk is bounded with
  high probability. Our setting is the same risk-coverage trade, applied to auto-allow.
- **Learn then Test** [ltt2021] (arXiv 2110.01052): risk control as multiple testing;
  fixed-sequence testing gives a valid guarantee without multiplicity correction when the
  hypotheses are ordered in advance. **Conformal risk control** [crc2024] (ICLR 2024):
  controls the expectation of a monotone loss.
- *Our use and correction:* an earlier version of our recipe bounded false allows among
  allowed calls and picked the lowest passing threshold - not monotone, not corrected.
  We bound the **leak rate** P(allow | destructive), which is monotone in the threshold, and
  certify it by fixed-sequence testing [ltt2021] with an exact Clopper-Pearson bound
  [clopper1934]. We add two deployment conditions the guarantees above do not cover: the
  threshold must be certified on the exact prompt the gate sends (we measured a rendering
  change moving a destructive call across it), and on the worst case over repeated runs.
- *Limit we state:* the guarantee assumes exchangeability; our held-out ATT&CK leak on
  gpt-oss-20b is the predicted failure under distribution shift.

## 4. Nondeterminism at temperature 0

- **Defeating Nondeterminism in LLM Inference** [he2025nondet] (Thinking Machines, 2025):
  batch-size-dependent kernels, not sampling, make temperature-0 outputs vary on hosted
  serving. We measure the security consequence: per-judge run-to-run spread up to 0.65 in
  p_safe, one destructive call crossing a certified threshold in a live run, and a min-of-k
  sampling rule that removes it.

## 5. Reference monitors

- Classic requirements - complete mediation, fail-safe defaults [saltzer1975] - are the lens:
  every seam we measure is a violation of one of them by the composition (gate + host), not by
  either part alone.
