# Paper outline (8 pages, IEEE two-column, single-anonymous) - for the authors to lock

**Working title:** *Where Agent Authorization Gates Break: Integration Seams, Not Model
Judgment* (alternative: *The Gate Is Not the Guarantee*).

**One-sentence claim:** Deployed authorization gates for coding agents mostly judge correctly
in isolation; what lets destructive calls run is how they are wired into the host - permission
mode, failure handling, argument-blind allowlists, and a threshold detached from the model and
prompt it was set on - and a gate designed around those seams, with a certified threshold,
closes them at a measured automation cost.

Every claim below names the result that carries it (RESULTS section / artifact).

## 1. Introduction (~1 page)
- Agents run shell commands; users install PreToolUse "gates" to stop destructive ones, and
  increasingly run hosts in auto/bypass modes. Gates advertise protection in exactly those
  modes (FRAMING_EVIDENCE sec 1).
- Gap: guardrails are evaluated in isolation (LlamaFirewall, AgentDojo, R-Judge); nobody
  measures the enforced outcome of the gate *as installed in the host*.
- Contributions (numbered, each with its headline number):
  1. An execution-grounded benchmark: 221 main / 189 held-out / 220 padded calls, labels
     verified by running each command in a sandbox (372 confirmed, 0 mismatch), real ATT&CK
     and GTFOBins procedures, a pre-registered blind set (sec 9-12, 16, 21).
  2. A measurement of 9 deployed gate projects - 6 end to end in the live host (8
     configurations), all 9 under injected model faults - showing four
     seams (sec 2-8): host-mode coupling (same gate: 0/127 default vs 75/127 auto),
     availability->authorization (padding -> model 400 -> run: 220/220), argument-blind
     allowlists (`git branch -D`, launcher wrapping), fail-open failure paths (documented by
     the host).
  3. A certification recipe valid under threshold selection (leak rate, fixed-sequence /
     Learn-then-Test, worst case over runs, on the deployed prompt) and a 7-judge study: the
     right threshold is model-specific (0.245-0.955); a copied 0.9 leaks on 4 of 7 judges
     (sec 17, 19; Fig. 1-2).
  4. A composed gate that closes the seams - 0 destructive runs on main/held-out/padded in
     both modes with full safe automation - and a deterministic alternative, as a Pareto
     pair; plus the three seams our own gate hit (sec 13, 15, 18, 21).

## 2. Background and threat model (~0.5 page)
- Claude Code hooks: allow / deny / ask / defer; permission modes; failure = action proceeds
  unless `onFailure: block` (v2.1.295+). Threat model: agent proposes a destructive call
  (mistake, injection, or disguise); attacker controls tool-call text, not the host or gate.

## 3. Benchmark and method (~1 page)
- Corpus construction, tiers, sandbox label verification (Table: corpus composition).
- Live harness (each call per host mode), fault server, padded inputs.
- Gates measured (Table: 9 projects / 8 live configurations, versions - REPRODUCIBILITY.md).
- Labels: automated rater panel (sec 20) + human panel (if done).

## 4. Findings: where deployed gates break (~2 pages, the core)
- Table 1: scorecard - destructive run main/held-out/padded per gate x host mode, safe
  automation (scorecard-all), with CIs (CONFIDENCE.md).
- 4.1 Host-mode coupling (F1). 4.2 Availability -> authorization (padding, fault matrix).
  4.3 Argument-blind allowlists and launchers. 4.4 Disguise: evasion + LOLBins (EVASION.md):
  rule gates miss interpreter one-liners; model gates catch them.
  4.5 Unseen tradecraft: blind set reproduces the host-mode seam (sec 21).

## 5. Setting the threshold: certification and seven judges (~1.25 pages)
- Recipe (leak rate, fixed sequence, exact CP bound, floor CP(0,n)); alpha sweep.
- Fig. 1 (where thresholds land) and Fig. 2 (leaks at certified t vs copied 0.9).
- Held-out validation; the distribution-shift failure (gpt-oss-20b, ATT&CK T1070);
  injectability of a safety classifier (gpt-oss-safeguard); run-to-run variance.

## 6. A gate built for the seams (~1 page)
- Design A: asymmetric authority, total failure function with a model budget, whole-command
  visibility, certified threshold on the deployed prompt, min-of-k. Design B for contrast.
- Table: A vs B (protection, automation, latency).
- What our own gate taught us (sec 18): prompt/threshold coupling, variance leak, host
  timeout seam; the blind-set miss (`at` job, benign payload) reported as is.

## 7. Related work (~0.5 page) - paper/RELATED_WORK.md

## 8. Limitations and threats to validity (~0.5 page)
- One host measured live (cross-host survey: sec TBD); single-language shell corpus; labels
  partly authored (sandbox + rater panel mitigate); exchangeability; free-tier rate limits;
  hosted models drift (raw scores committed); blind set n = 5.

## 9. Conclusion + responsible disclosure + artifact statement (~0.25 page)

## Decisions needed from the authors before writing
1. Title and the one-sentence claim above.
2. Is the cross-host survey in (adds external validity; changes sec 4 to "across hosts")?
3. Human rater panel: in, or report the automated panel only and list it as a limitation?
4. Author block and affiliations; AGENT@ICSE as preview vs. full-venue target.
