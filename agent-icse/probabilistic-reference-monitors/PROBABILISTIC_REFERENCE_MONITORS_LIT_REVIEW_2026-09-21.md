# Probabilistic Reference Monitors: thorough literature review

Date: 2026-09-21. Target: SE4AgenticAI 2026 regular paper (8-10 pp, IEEE 2-col), deadline 2026-10-10 AoE.
Companions: [gap audit](../se4agenticai-exploration/JEV_RESEARCH_GAP_AUDIT_2026-09-21.md) | [academic lit review](../se4agenticai-exploration/JEV_IDEA_EXPANSION_AND_LIT_REVIEW_2026-09-21.md) | [MT paper spec](../se4agenticai-exploration/MR_TYPED_DECISION_MODELS_SPEC_2026-09-21.md)
Method: three parallel verification sweeps (authorization/enforcement cluster; calibration/selective-prediction cluster; mining-precedent + grey gate corpus). Every arXiv ID below was verified against a live abstract page on 2026-09-21. Grey repos were read directly where marked.

## 0. The candidate

**Working title:** *Probabilistic Reference Monitors: Calibrated Decision Models in the Authorization Path of Coding Agents.*

**One-sentence pitch:** the academic literature is unambiguous that per-call authorization must be deterministic, fail-closed, default-deny, and placed outside the untrusted model — and at least 22 public projects do exactly the opposite, wiring a remote, probabilistic, documented-as-injectable decision model into the permission path of coding agents; nobody has studied what they actually built.

**Four results:**
1. **Corpus study** of the ~22 public gates at pinned SHAs: question asked, primitive, threshold constant, threshold *provenance*, action set, sanitisation of attacker-reachable state.
2. **Fail-open analysis**: static read of every gate's error path on timeout / 429 / 5xx / malformed response. Needs no API key and no money.
3. **Benchmarked accuracy** of the calibrated typed gate against TraceSafe's published baselines (13 LLMs + 7 guardrails, best 83.58%).
4. **Cost-sensitive threshold analysis**: re-score allow/ask/deny under asymmetric authorization loss; derive the loss-optimal threshold; locate the vendor docs' illustrative 0.9 against it.

**Verdict up front:** the gap is real and the paper is viable, but the surrounding literature moved hard in June-September 2026. The *framing* (agent gating = selective classification under asymmetric cost) is now occupied; the *specific contribution* (deployed corpus + threshold provenance + fail-open availability + calibrated typed model) is not. Speed matters. Details below.

---

## 1. Cluster A: agent authorization and runtime enforcement

### 1.1 The deterministic-enforcement consensus (the "literature says no" side)

| Work | Venue/date | What it establishes |
|---|---|---|
| Capability Gates Are Not Authorization / ScopeGate ([2606.28679](https://arxiv.org/abs/2606.28679)) | arXiv, Jun 2026 | LangChain/LangGraph, LlamaIndex, Stripe Agent Toolkit all lack deterministic fail-closed per-call value authorization by default. ScopeGate: 5-stage PDP, default-deny, 0/48 static bypasses. Body text explicitly excludes probabilistic/ML-driven authorization (**pin the page number from the PDF before quoting**). |
| AgentSpec ([2503.18666](https://arxiv.org/abs/2503.18666)) | **ICSE 2026** | Deterministic trigger/predicate/enforcement DSL; >90% prevention, ms overhead. The deterministic baseline. Two unrelated same-named papers exist (2606.14674, 2608.24004) — cite by ID. |
| Progent ([2504.11703](https://arxiv.org/abs/2504.11703)) | arXiv v3, May 2026 | Least-privilege policy DSL; per-call check deterministic; LLM authors policies but SMT solver gates updates (monotonic confinement). |
| CaMeL ([2503.18813](https://arxiv.org/abs/2503.18813)) | Google DeepMind/ETH | Capabilities + control/data-flow separation; provable injection resistance at 77% AgentDojo utility. |
| ActPlane ([2606.25189](https://arxiv.org/abs/2606.25189)) | arXiv, Jun 2026 | eBPF-level enforcement for agent harnesses; catches paths tool-call interception structurally misses. |
| Autoformalization of Agent Instructions into Policy-as-Code ([2606.26649](https://arxiv.org/abs/2606.26649)) | AIWILD @ ICML 2026 | NL policies → verified Cedar. **Already contains our tension sentence in print**: frames the field as "probabilistic guardrails ... that offer no formal guarantees" vs symbolic enforcement. |
| Bounded Agents ([2608.15888](https://arxiv.org/abs/2608.15888)) | DeepMind/Cornell, Aug 2026 | Blast-radius monotonicity over delegation chains. |
| SOUNDGATE ([2607.14166](https://arxiv.org/abs/2607.14166)) | arXiv, Jul 2026 | Approval gates/cancellation lack barrier semantics on 6 frameworks. |
| Balkanization SoK ([2607.05743](https://arxiv.org/abs/2607.05743)) | arXiv, Jul 2026 | Systematizes 39 execution-security papers; names five cross-cutting gaps; policy-enforcement studies report 69-98% failure on real denylists. Positions our gap. |
| Saltzer & Schroeder 1975 (DOI 10.1109/PROC.1975.9939); Hardy 1988 (DOI 10.1145/54289.871709) | classical | Reference-monitor requirements (complete mediation, tamperproof, verifiable, fail-safe defaults); confused deputy. The standard every gate is judged against. |

### 1.2 Models in the decision path (the "practice/benchmark" side)

| Work | Venue/date | Relevance |
|---|---|---|
| TraceSafe ([2604.07223](https://arxiv.org/abs/2604.07223)) | **COLM 2026** | 12 risk categories, 1,000+ instances, 13 LLM guards + 7 specialized guardrails; structural/JSON competence predicts guardrail efficacy (rho=0.79); specialized guardrails underperform general LLMs. **Our evaluation substrate + 20 published baselines.** |
| AgentTrust ([2605.04785](https://arxiv.org/abs/2605.04785)) | arXiv, May 2026 | Runtime interception returning allow/warn/block/review; rules + cache-aware LLM judge; ships as MCP server. Closest shipped analog to a Jev gate. |
| ScopeJudge ([2607.07774](https://arxiv.org/abs/2607.07774)) | arXiv, Jul 2026 | **Nearest academic neighbor to results 3-4.** LLM judge as pre-execution gate for offensive-security agents; 4,897 tool calls labeled by pentesters (kappa=0.64); 8 judges x 5 context strategies; explicitly asymmetric cost with cost-sensitive and recall-first operating points. |
| CARE ([2607.21642](https://arxiv.org/abs/2607.21642)) | **ISSRE 2026** | Static-first pre-execution verifier for shell commands, escalating borderline cases to an LLM judge; 85.64% F1 at 0.91% FPR. Closest academic analog to `jev-axi`. |
| Cautious Bench / The Guard That Cried Wolf ([2608.27009](https://arxiv.org/abs/2608.27009)) | arXiv, Aug 2026 | First over-refusal benchmark for agent guardrails; guardrails over-refuse on scary object *names*, not authorization context. |
| Influence Is Not Authority ([2608.29942](https://arxiv.org/abs/2608.29942)) | arXiv, Aug 2026 | 96-condition audit: influence-based guardrail signals don't encode whether an action was authorized. |
| GuardAgent ([2406.09187](https://arxiv.org/abs/2406.09187), ICML 2025); ShieldAgent ([2503.22738](https://arxiv.org/abs/2503.22738)); Conseca ([2501.17070](https://arxiv.org/abs/2501.17070), HotOS 2025) | 2025 | Guardrail agents, probabilistic rule circuits, just-in-time contextual policies. |
| Dive into Claude Code ([2604.14228](https://arxiv.org/abs/2604.14228)) | tech report, Apr 2026 | Claude Code's permission system has seven modes **and an ML-based classifier**. Even the vendor ships a model in the permission path — a gift for the intro. |
| Benchmark spine: ToolEmu ([2309.15817](https://arxiv.org/abs/2309.15817), ICLR'24); InjecAgent ([2403.02691](https://arxiv.org/abs/2403.02691), ACL'24 Findings); AgentDojo ([2406.13352](https://arxiv.org/abs/2406.13352), NeurIPS'24 D&B); AgentHarm ([2410.09024](https://arxiv.org/abs/2410.09024), ICLR'25); WASP (**[2504.18575](https://arxiv.org/abs/2504.18575)** — corrected ID) | 2024-25 | Threat taxonomies and baselines. |

**Fail-open / availability axis: near-total null.** No work analyzes what deployed probabilistic gates do on timeout/429/5xx. Closest: "Can MCP Clients Decide What to Do After Failure?" ([2609.00072](https://arxiv.org/abs/2609.00072)) — MCP failure-result actionability with a fail-closed prototype; protocol-level, not model gates. **This is our strongest, cheapest, most novel result.**

---

## 2. Cluster B: calibration, selective prediction, cost-sensitive thresholds

### 2.1 The theory that licenses a threshold

| Work | Venue/date | What it establishes |
|---|---|---|
| UCCI ([2605.18796](https://arxiv.org/abs/2605.18796)) | arXiv, May 2026 | **Load-bearing cite.** Isotonic-calibrated per-query error probability; threshold by constrained cost minimization; threshold policies on calibrated scores provably cost-optimal; 31% cost cut on 75k production queries. Routing for compute cost, not authorization. |
| CAUC: Calibration-Aware Uncertainty Cascades ([2609.11446](https://arxiv.org/abs/2609.11446)) | arXiv, Sep 2026 | States our premise as a theorem: calibration gives confidence thresholds an explicit selective-risk interpretation; uncalibrated scores offer none. |
| CascadeDebate ([2604.12262](https://arxiv.org/abs/2604.12262)); routing survey ([2603.04445](https://arxiv.org/abs/2603.04445), **TMLR 2026**); FrugalGPT ([2305.05176](https://arxiv.org/abs/2305.05176)); RouteLLM ([2406.18665](https://arxiv.org/abs/2406.18665)); RouterBench ([2403.12031](https://arxiv.org/abs/2403.12031)) | 2023-26 | Static thresholds on uncalibrated scores are brittle (CascadeDebate: online optimizer beats fixed policies 21-52%). |
| Chow 1970 (IEEE Trans. IT 16(1)); El-Yaniv & Wiener (JMLR 2010); Geifman & El-Yaniv ([1705.08500](https://arxiv.org/abs/1705.08500), NeurIPS'17); SelectiveNet ([1901.09192](https://arxiv.org/abs/1901.09192), ICML'19) | classical+ | **Chow already owns the cost-derived optimal reject threshold** t=(C_r-C_c)/(C_e-C_c). Our "loss-optimal threshold" is Chow's rule instantiated — frame as instantiation, never invention. |
| Mozannar & Sontag ([2006.01862](https://arxiv.org/abs/2006.01862), ICML'20); Predictor-Rejector ([2310.14772](https://arxiv.org/abs/2310.14772), ALT'24); cost-sensitive deferral under imbalance ([2604.27723](https://arxiv.org/abs/2604.27723), **ICML 2026**) | 2020-26 | Learning-to-defer canon; the strongest recent theory bridge between cost-sensitive learning and deferral. |
| LPP: LLM Performance Predictors ([2601.07006](https://arxiv.org/abs/2601.07006), **AAMAS 2026**) | Jan 2026 | Closest peer-reviewed escalation work: cost-aware selective classification escalating to humans in content moderation. |
| On Calibration of LLM-based Guard Models ([2410.10414](https://arxiv.org/abs/2410.10414), **ICLR 2025**) | Oct 2024 | 9 guard models x 12 benchmarks: guards overconfident, badly miscalibrated under jailbreak. **The foil for Jev's calibration-as-training-objective claim.** |
| ProbGuard ([2608.10621](https://arxiv.org/abs/2608.10621)) | arXiv, Aug 2026 | Calibrated unsafe-probability guardrail, -72% ECE. Field converging on calibrated guardrails for *generation*, not *action authorization*. |
| FlexGuard (ACL 2026, DOI 10.18653/v1/2026.acl-long.263) | Feb 2026 | Calibrated continuous risk score + strictness-adaptive thresholding in production moderation. |
| Guo et al. ([1706.04599](https://arxiv.org/abs/1706.04599), ICML'17); P(True) ([2207.05221](https://arxiv.org/abs/2207.05221)); verbalized confidence ([2305.14975](https://arxiv.org/abs/2305.14975), EMNLP'23; [2412.14737](https://arxiv.org/abs/2412.14737)) | 2017-24 | Calibration canon. |

### 2.2 The nearest neighbor (treat as concurrent work)

**Oversight Has a Capacity: Calibrating Agent Guards to a Subjective, Fatiguing Human** ([2606.08919](https://arxiv.org/abs/2606.08919), Jun 2026). Frames HITL approval gates for irreversible agent actions as selective classification under asymmetric cost; 125 hand-labeled actions; fatigue makes safety an inverted-U in escalation rate; flooding attack. It occupies the *framing*. It does **not**: evaluate a purpose-built calibrated decision model; derive a loss-optimal threshold from calibrated probabilities; audit a vendor-published threshold; study deployed gates; touch availability. Cite and differentiate explicitly — do not claim "first cost-sensitive analysis of agent gating"; that claim is now false.

Also adjacent: role-stratified conformal risk control for tool calls ([2607.24343](https://arxiv.org/abs/2607.24343)) — different guarantee type (conformal, not loss-optimal); AI-control line (Greenblatt et al. [2312.06942](https://arxiv.org/abs/2312.06942), ICML'24; Ctrl-Z [2504.10374](https://arxiv.org/abs/2504.10374)) — thresholded action monitoring with safety/usefulness asymmetry, but audit-budget-set thresholds on uncalibrated scores; one-sentence differentiation suffices.

### 2.3 Thresholds as configuration debt

Essentially empty since Sculley et al. (NeurIPS 2015). arXiv search for technical-debt + threshold + ML returns nothing on point; only MLOps deployment surveys (Paleyes et al., ACM CSUR 2022) are adjacent. **Confirmed open niche** — the threshold-provenance corpus study fills a named-but-empty gap.

---

## 3. Cluster C: mining-study precedent and the gate corpus

### 3.1 Academic precedent for the method

| Work | Venue | Corpus | Relation |
|---|---|---|---|
| Liu et al. ([2601.07136](https://arxiv.org/abs/2601.07136)) | **SE4AgenticAI 2025** | 8 MAS repos, 42k commits, 4.7k issues | **The venue-fit anchor: identical contribution shape, accepted here last year.** |
| MCP at First Glance ([2506.13538](https://arxiv.org/abs/2506.13538)) | **TOSEM** | 1,899 MCP servers | Health/security mining via hybrid static analysis. |
| MCP ecosystem measurement ([2509.25292](https://arxiv.org/abs/2509.25292)) | arXiv | 17,630 marketplace entries | Ecosystem measurement. |
| Empirical Study of MCP Applications ([2607.25635](https://arxiv.org/abs/2607.25635)) | arXiv, Jul 2026 | 1,723 MCP apps | Finds human-oversight mechanisms lacking — closest method cousin. |
| We Urgently Need Privilege Management in MCP ([2507.06250](https://arxiv.org/abs/2507.06250)) | arXiv | 2,562 MCP apps | Nearest "authorization config mining" — but MCP servers, not agent gates. |
| Where Agent Frameworks Fall Short ([2602.21806](https://arxiv.org/abs/2602.21806)); Understanding Bugs in Modern Agentic Frameworks ([2604.08906](https://arxiv.org/abs/2604.08906), **ASE 2026**) | 2026 | 5,669 bug reports; 409 fixed bugs | Framework bug mining. (Correct title for the ASE one — earlier local notes had it wrong.) |
| Agent READMEs ([2511.12884](https://arxiv.org/abs/2511.12884)); AGENTS.md manifests ([2509.14744](https://arxiv.org/abs/2509.14744)); Configuration Smells ([2606.15828](https://arxiv.org/abs/2606.15828)); Evaluating AGENTS.md ([2602.11988](https://arxiv.org/abs/2602.11988)); Guardrails Beat Guidance ([2604.11088](https://arxiv.org/abs/2604.11088)) | 2025-26 | 679-2,303 config files | Agent-config mining cluster; security instructions in only 14.8% of agent READMEs (quotable motivation). |
| **When "Do Not" Is Not Deny ([2608.23550](https://arxiv.org/abs/2608.23550))** | arXiv, Aug 2026 | 481 CLAUDE.md files | **Closest academic neighbor to the corpus half.** Mines NL security rules vs built-in deny controls; only 4.4-16% of rules have a matching control. Different object (NL rules vs deterministic controls, not ML gates). Must-cite; its finding motivates why practitioners reach for model gates. |
| Scanning the Harness ([2609.07360](https://arxiv.org/abs/2609.07360)) | arXiv, **Sep 7 2026** | 3,171 coding-agent config repos | **Most dangerous paper for a reviewer to know that we don't.** Mines instruction files, skills, hooks, MCP declarations for supply-chain defects; 16.0% carry a security defect. Pre-Jev (submitted 8 days before launch); extracts none of our fields. Cite in the first page of related work. |
| Harness Engineering ([2609.00006](https://arxiv.org/abs/2609.00006)) | arXiv, Sep 2026 | 11 production harnesses, ~4M LoC | Permission-surface anatomy of coding harnesses. |

### 3.2 The grey gate corpus, verified directly (16 repos read in full, 2026-09-21)

awesome-jev's Verification & Guardrails category has **25 entries**; "~22 gates" holds depending on inclusion criteria — the paper must state its criteria. Note: `harshwasan/jev-sentinel` from the earlier audit is **not** in the current list; do not cite it.

Preliminary cross-cutting findings (these are nearly results already):

- **Fail-open dominates: 11 of 16 documented error paths fail open**, several explicitly as a stated design choice ("a dead API must not freeze your agent"; "every error path exits 0"; "No key, API error, or timeout: exit 0, silently"). Clear fail-closed: pi-verdict, hermes-jev-approvals, Vercel fx. jev-engineering's recipes page actively *recommends* fail-open for coding agents.
- **Threshold provenance is mostly absent or ad-hoc.** Only jev-belay (swept on 100 labeled stops) and pi-heed (measured) document derivation; jev-belay's README admits 3 of its 4 thresholds are "reasoned, not measured"; jev-engineering ships DENY_ABOVE 0.90 — **the vendor docs' illustrative example, verbatim**.
- **No gate evaluates against any other gate.** Best self-evaluations: pi-heed (79 sessions x 8 versions), jev-belay (bootstrap CIs), limpet (honest weak AUROC 0.51-0.64), Abide (independent reviewer confirmed 10/39 flags).
- Grey precedents to cite and exceed: pi-verdict's `research/pi-permission-landscape.md` (8-project Pi permission comparison *with a fail-open/closed column* — pre-Jev, Pi-only); jev-engineering's 300-call injection test (single implementation, dated 2026-09-20); themsquared/jev-benchmark (n=60, 71.4% ambiguous, no baselines).

---

## 4. The gap statement, precisely

After all three sweeps, the unoccupied space is exactly this combination:

1. **A corpus of deployed, in-the-wild probabilistic authorization gates** — not author-constructed benchmarks (ScopeJudge, Cautious Bench), not pre-Jev harness mining (Scanning the Harness), not NL rules (When "Do Not" Is Not Deny).
2. **Threshold provenance as configuration debt** — empty since Sculley; the corpus already shows undocumented constants and one verbatim copy of the vendor's illustrative 0.9.
3. **The availability/fail-open axis** — a vendor rate limit becomes an authorization-availability property; unstudied academically, and the corpus already shows fail-open is the dominant *deliberate* design choice.
4. **A calibrated typed decision model as the gate** — the UCCI/CAUC premise (calibration licenses selective-risk thresholds) tested where it actually matters, against the ICLR'25 finding that shipped guard models are miscalibrated by default.
5. **Loss-optimal threshold derivation for allow/ask/deny** — Chow's rule instantiated for authorization, auditing the vendor's 0.9, on a real corpus. Framing occupied by Oversight Has a Capacity; this specific derivation + audit is not.

## 5. Claims we must NOT make (each is now false)

- "First cost-sensitive / asymmetric-loss analysis of agent gating" — Oversight Has a Capacity (2606.08919), ScopeJudge (2607.07774).
- "First to mine agent configurations for security defects" — Scanning the Harness (2609.07360); When "Do Not" Is Not Deny (2608.23550).
- "First to put a model in the permission path and evaluate it" — AgentTrust, CARE, TraceSafe, and even Claude Code itself (2604.14228).
- "We derive the cost-optimal threshold" as a method invention — Chow 1970 owns it; ours is an instantiation + audit.

## 6. Consolidated must-cite list (differentiate, don't just list)

**First page of related work:** 2606.28679 (ScopeGate) · 2503.18666 (AgentSpec) · 2609.07360 (Scanning the Harness) · 2606.08919 (Oversight Has a Capacity) · 2607.07774 (ScopeJudge) · 2604.07223 (TraceSafe).
**Theory:** 2605.18796 (UCCI) · 2609.11446 (CAUC) · Chow 1970 · El-Yaniv & Wiener 2010 · 2006.01862 · 2410.10414 (guard-model calibration foil).
**Method/venue anchor:** 2601.07136 (SE4AgenticAI 2025) · 2608.23550 · 2506.13538 · 2607.25635.
**Classics:** Saltzer & Schroeder 1975 · Hardy 1988 · Sculley et al. 2015.
**Supporting:** 2605.04785 (AgentTrust) · 2607.21642 (CARE) · 2608.27009 (Cautious Bench) · 2608.29942 · 2607.05743 (Balkanization SoK) · 2504.11703 (Progent) · 2606.26649 · 2604.14228 · 2601.07006 (LPP) · 2312.06942 + 2504.10374 (AI control) · benchmark spine 2309.15817/2403.02691/2406.13352/2410.09024/2504.18575.
**Grey (cite as artifacts with access dates):** yibie/awesome-jev · themsquared/jev-benchmark · eugeniughelbur/jev-engineering · jesset/pi-verdict · the verified gate repos (Section 3.2).

## 7. Honest risk assessment

- **Scoop risk is moderate and rising.** 2606.08919 (Jun), 2607.07774 + 2607.24343 (Jul), 2608.27009 + 2608.29942 + ProbGuard (Aug), 2609.07360 (Sep 7) all appeared within ~3 months. The specific combination is free; the framing is not. Submit fast; re-sweep arXiv in the first week of October before submission.
- **Security-reviewer risk:** a reviewer may want a full threat model. Mitigate by scoping: this is an empirical SE study of deployed artifacts, with the security literature as the frame, not an attack paper.
- **Corpus-depth risk:** awesome-jev's own curator warns bulk same-day submissions may be unproven scaffolds (jev-harness shows that shape). Inclusion criteria must require a real action wired up and runnable code; state the convenience-sample limitation.
- **Access risk:** results 3-4 need API access; results 1-2 do not. The paper's floor (corpus + fail-open) is achievable at zero cost and zero access — and Section 3.2 shows the preliminary signal is already strong (11/16 fail-open).
- arXiv recall for the last ~2 weeks may be incomplete (rate limits during the sweep). One citation could not be verified ("Trust or Escalate: LLM Judges with Provenance") — do not cite it.

## 8. This paper vs the MT paper (the other live candidate)

| | Probabilistic reference monitors (this) | MT for typed decision models ([spec](../se4agenticai-exploration/MR_TYPED_DECISION_MODELS_SPEC_2026-09-21.md)) |
|---|---|---|
| Story | Stronger: literature-vs-practice tension, named theory, security stakes | Smaller: testing methodology for a new API class |
| Novelty position | Framing occupied; specific combination free; moving fast | Relations mostly known; 3 API-native MRs new; statistical procedure incremental (AgentAssay collision) |
| Floor without API access | Corpus + fail-open (strong, already-signalled) | None — needs the distribution |
| Reviewer risk | May draw security reviewer | May draw "just API testing" |
| Venue-fit anchor | Exact match to accepted 2025 empirical study | Good topical fit, no direct precedent |
| Estimated acceptance (well-executed) | ~65-80% | ~60-75% (higher with strong MR8/MR7 violations) |

They share infrastructure (pinned jev client, logging wrapper, raw-JSONL artifact). Build that first; the choice can be deferred to ~day 5 per the gap audit's plan. If only one is submitted: this one for the stronger paper, the MT one for the safer bet.
