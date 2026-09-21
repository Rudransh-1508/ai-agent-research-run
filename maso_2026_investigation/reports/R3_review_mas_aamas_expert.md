# MASO 2026 — Mock Review: REVIEWER 3 (MAS/AAMAS Expert, classical MAS / PRIMA community)

**Paper under review:** "Do Classical Organizational Fault-Handling Results Hold for LLM Multi-Agent Systems? Measuring Organizational Fault Propagation and Containment in Agentic Workflows" (merged candidate "OrgResilience")
**Reviewer mindset:** classical multi-agent systems; has read Dellarocas & Klein, Horling & Lesser, Tambe, Hägg, Kota, MOISE/OperA in the original.
**Date:** 2026-09-21
**Verification this review:** Klein & Dellarocas CSCW 2000 full text re-retrieved and read (Wayback snapshot of MIT DSpace PDF; local copy `maso_2026_investigation/raw/r3_review/kd_cscw2000.pdf`, extracted text `kd_cscw2000.txt`); Carley & Lin 1997, Horling & Lesser 2004, Sabater & Sierra REGRET verified via Semantic Scholar / Crossref APIs. All other facts from the investigation reports (E5, W2 assassin/feasibility/statistics), which verified them against primary sources on 2026-09-21.

---

## 1. Summary of the paper as I understand it

The authors build a fault-injectable organizational testbed on LangGraph over two workflows (tau2-bench retail customer service; a new IT incident-management domain), vary organizational structure as the independent variable (flat / 2-level / 3-level hierarchy, ± sentinel agents, ± resource scarcity), inject 5–7 "organic" semantic faults mapped to seven typed organizational boundaries, and measure a new metric — Organizational Blast Radius (OBR), the fraction of boundary types crossed by provenance-traced corrupted events — plus containment latency, utility preservation, and a priced recovery-cost vector. Six containment policies (none, retry, verifier gate, checkpoint-rollback, sentinel quarantine + re-delegation, scripted-oracle human escalation) are compared on a cost-utility Pareto. The evaluation frame is a transfer test of classical MAS organizational fault-handling: H1 replicates Dellarocas & Klein's "unzippering" delegation-tree propagation (ICMAS 2000), H2 tests Hägg-style sentinel containment, H3 tests the D&K prediction that containment backfires under scarcity, H4 claims to identify where classical predictions break under semantic LLM faults. Statistics: ~3,400 runs, continuous OBR co-primary, within-instance pairing, TOST equivalence testing (SESOI ±10pp) so that "classical prediction fails" is a designed-in publishable outcome.

## 2. Strengths (briefly)

- The classical anchors are the *right* ones, and the citation record supports the premise: Dellarocas & Klein ICMAS 2000 has exactly one post-2023 citer (zero LLM content), Hägg 1997 has zero LLM-era citers, and "unzippering" has never appeared on arXiv (W2 citation analysis, verified). Somebody should do this experiment, and PRIMA/MASO is the right room for it.
- H3 (containment backfires under scarcity) is the correct classical prediction to test — it is the non-obvious, sign-reversal finding, and the crossover design is the one interaction adequately powered at feasible n (W2 statistics).
- Pre-registration, TOST with a stated SESOI, deterministic DB-state ground truth, trigger-verified injection, and a κ-gated judge confined to secondary endpoints are methodologically ahead of most LLM-MAS evaluation papers I review.
- Pricing human oversight minutes into the recovery-cost vector is a genuinely organizational touch.

That is the end of the good news.

## 3. Weaknesses — the rejection case, ranked

### W1 (most severe). H4 is a strawman: the classical record anticipated semantic faults, and the paper's "novel result" is pre-registered in the literature it claims to test

The paper's headline claim is that classical organizational fault-handling assumed crash faults and therefore breaks under *semantic* faults. This misrepresents the classical record at the conceptual level:

- **Klein & Dellarocas, "A Knowledge-based Approach to Handling Exceptions in Workflow Systems," CSCW 2000 (DOI 10.1023/A:1008759413689)** — full text re-read for this review. Their exception taxonomy explicitly includes "**incorrectly** or tardily performed tasks," inputs arriving "of the **wrong type** (wrong thing)," and "**conflicts between actions taken in different process steps**." Their resolution-strategy knowledge base (~200 strategies) contains, verbatim: "*IF an agent receives garbled data, THEN trace back to the original source of the faulty data, eliminate all decisions that were corrupted by this error, and start again*" — i.e., provenance-traced rollback of corrupted downstream state, which is this paper's C3 mechanism plus its OBR provenance machinery, described in 2000. The same text introduces "cascading exceptions" and treats detection as exception-type-specific and fallible ("diagnoses represent hypotheses rather than guaranteed deductions").
- **Carley & Lin, "A Theoretical Study of Organizational Performance Under Information Distortion," Management Science 43(7), 1997 (DOI 10.1287/mnsc.43.7.976)** — computational organization theory studied *organization structure × performance under distorted (i.e., semantically corrupted) information* three decades ago; Lin & Carley's "Designing Stress Resistant Organizations" (2003) is literally org-design-for-fault-resistance. The paper engages none of this.
- The classical **trust/reputation** literature (Sabater & Sierra, REGRET, Agents 2001, DOI 10.1145/375735.376110; review in AI Review 2005, DOI 10.1007/s10462-004-0041-5) is entirely about the propagation of semantically unreliable information between agents.

What is genuinely new is the *substrate* — natural-language messages, learned memory, LLM tool use — not the *fault class*. As framed, H4 promises to "discover" what Klein & Dellarocas already wrote down. A reviewer who knows this literature (and MASO's pool is exactly that reviewer) will conclude the authors tested a caricature.

### W2. The transfer test confounds fault semantics with detectability — as designed, H4 measures detection difficulty, not theory breakdown

In Dellarocas & Klein's experiments, sentinel detection of agent death is effectively perfect (polling/"are-you-alive" + timeout). The paper's sentinel must *detect* semantic faults with an imperfect LLM-based or syntactic detector. Fault type (crash vs semantic) is therefore perfectly confounded with detection quality (perfect vs imperfect). Any H4 "breakdown" is explainable entirely by detection failure — which, per W1, the classical framework already identified as the hard, type-specific problem. The design needs **detection quality as an orthogonal factor**: an oracle-detector arm (sentinel notified of the injected fault's ground truth) alongside syntactic and LLM-semantic detectors. Without it, the paper cannot distinguish "classical *theory* fails" from "classical *assumption of cheap perfect detection* fails" — and only the latter is defensible. The syntactic-vs-semantic ablation gestures at this but omits the oracle ceiling that makes the decomposition interpretable.

### W3. Regime mismatch makes H1 unfalsifiable as designed

D&K's unzippering result (600–700% completion-time inflation) was measured on **4-level contracting trees, branching factor 2, up to 15 agents**, under Contract Net, in a discrete-event simulator. The paper's structure IV tops out at a **3-level hierarchy with 5 roles**. Propagation magnitude grows with depth; a null or attenuated H1 result cannot be read as "theory fails to transfer" — it may simply be below the regime where the effect exists. Relatedly, the endpoint mapping is asserted, not argued: D&K's metric is completion-*time* inflation under concurrency; the paper's analog is tokens+steps, which conflates price, latency, and work. If the TOST equivalence bound (SESOI) is placed on a proportion while the classical prediction is a *ratio* (6–7× baseline), the equivalence logic is a category error; the bound must be pre-registered on the inflation ratio (e.g., ×1.25) with the mapping justified.

### W4. "Organization" is vocabulary borrowing, not organizational modeling

The independent variable is a LangGraph routing configuration with role labels. There is no formal organizational specification — no MOISE+/OperA structural-functional-deontic model, no norms or obligations, no span of control, no organizational routines; Horling & Lesser's paradigm space (hierarchy, holarchy, coalition, team, congregation, society, federation, market, matrix) is reduced to delegation depth. There is no engagement with March & Simon, Galbraith's information-processing view of organizations, or Carley's computational organization theory (W1). For this reviewer pool, calling a routing graph an "organization" without a deontic dimension is the kind of thing that gets a paper remembered for the wrong reason. One section formalizing the seven boundary types in MOISE-lite terms (roles, links, permissions/obligations, missions) would largely fix this; its absence is telling.

### W5. The "nobody cites the classics" premise is true but already claimed — and it indicts the wrong party

La Malfa et al. ("Large Language Models Miss the Multi-Agent Mark," NeurIPS 2025 position, arXiv:2505.21298) and Bădică et al. (arXiv:2509.02515) have already made the "LLM-MAS appropriates MAS vocabulary without engaging foundations" argument at good venues. The paper's contribution is the *experiment*, not the observation; any "first to bridge" framing is false. Moreover, the citation drought shows the LLM community's scholarship gap, not the classical theory's untestedness — the paper should be careful not to imply the latter.

### W6. Vehicle mismatch: this is a 16-page full paper at minimum, plausibly journal-length

Testbed + new metric + 7 faults + 6 mechanisms + 5 pre-registered hypotheses + TOST machinery + ~3,400 runs + a 12-work differentiation obligation + a 5-way disambiguation of "blast radius" cannot be honestly presented in 8 pages. Submitted as a short paper it will read as a journal study compressed into inadequacy: the differentiation section alone consumes ~2 pages. Submit as a full paper with the testbed/metric detail in an artifact appendix, or cut scope.

### W7 (minor). Residual statistical and mechanism-design exposures

- Binary containment-rate claims must stay ≥25pp (paired); the paper says this — hold it to that in every table.
- The scripted-oracle human (C5) has perfect policy knowledge; without sensitivity over human error rates and capacity, the human-escalation arm is stacked to win and reviewers will discount the Pareto's most interesting point.
- OBR corruption-labeling on free-text channels is the metric's soft underbelly; restricting automated labeling to structured channels (per the κ-gate fallback) must be stated as a scoping decision, not discovered in review.

## 4. Questions to authors

1. Will you add an oracle-detector sentinel arm so that H4 separates fault semantics from detection quality? If not, how do you rule out the confound in W2?
2. Why does the structure IV stop at depth 3 when the classical effect you are testing was measured at depth 4 with branching factor 2? What is your falsification criterion for H1 if the effect attenuates?
3. Exactly how do you map D&K's completion-time inflation to your token/step cost vector, and on which endpoint (proportion or ratio) is each TOST bound placed?
4. Which Klein & Dellarocas (CSCW 2000) exception types do your seven faults correspond to? If the mapping is many-to-one, what does "boundary-typed" add over their taxonomy?
5. Does the organizational wrapper preserve tau2-retail baseline pass rates (within ~10pp of published single-agent numbers)? If the no-fault baseline degrades for coordination reasons, every relative effect in the paper is uninterpretable.
6. What is the sentinel's measured detection recall per fault type, and is it reported separately from containment effectiveness?
7. Why should OBR labeling on free-text handoffs be trusted beyond the structured channels where your κ gate applies?

## 5. Score

**Reject. Confidence: 3/5.**

The venue fit is perfect and the experiment should exist — but as described, the headline novelty claim (H4) does not survive contact with the classical record it invokes (W1), and the transfer logic is confounded at the design level (W2) and under-powered in the wrong regime (W3). I hold this verdict with moderate confidence because every fatal flaw has a known, cheap fix, and a more charitable reading would call this a strong weak-reject. My job here is to say what gets it rejected: testing a strawman of my community's literature while claiming to test the literature.

## 6. The single change that would most improve my score

**Make detection quality an orthogonal experimental factor (oracle / syntactic / LLM-semantic sentinel) and reframe H4 accordingly: from "classical predictions break under semantic faults" to "classical containment *mechanisms* largely transfer; the classical *assumption* of cheap, near-perfect detection of value faults does not — here is the detection-quality × containment-effectiveness frontier."** This one move de-confounds the transfer test, converts the strawman into the paper's actual contribution (a result Klein & Dellarocas could state but never measure), and gives me — the classical reviewer — the figure I would cite: how much containment you buy per unit of detection quality on an LLM substrate. Pair it with restoring depth-4 cells for H1 and citing Carley & Lin 1997 and the K&D CSCW 2000 taxonomy as the conceptual anticipation, and my score moves to accept.

**What would make me cite this paper:** a validated transfer map with mechanistic explanations (not just "breaks/doesn't break"), the detection-frontier result, updated design principles a MAS engineer can apply, and an artifact whose org specification is formal enough (MOISE-lite) for the classical community to plug into.

---

## ORCHESTRATOR NOTE

**Verdict: SURVIVE — wounded, with a precise, cheap revision.** This reviewer's three fatal objections are all fixable within the existing build and budget:

1. **W1 (strawman H4):** Reposition, don't redesign. Cite Klein & Dellarocas CSCW 2000 (taxonomy includes "incorrectly performed tasks," "garbled data," provenance-traceback resolution — full text now in `raw/r3_review/`) and Carley & Lin Management Science 1997 as conceptual anticipations; shrink the novelty claim from "semantic faults are new" to "semantic faults on NL/LLM substrates are unmeasured." The paper becomes the *experimental realization* of K&D's unimplemented value-fault program — a stronger, reviewer-flattering frame.
2. **W2 (detection confound):** Add an oracle-detector sentinel arm — a config change (ground-truth fault notification), not new machinery; ~160–320 runs. Reframe H4 as the detection-quality × containment frontier.
3. **W3 (regime mismatch):** Restore the depth-4 level in the H1 replication cells (the W2 feasibility plan already had depth {1,2,3,4}; the merged candidate's "3-level" cap silently dropped it). Pre-register the SESOI on the inflation *ratio*, not a proportion.

Secondary mandates: submit as a **16-page full paper** (W6); add a one-section MOISE-lite formalization of the seven boundary types (W4); cite La Malfa et al. NeurIPS 2025 / Bădică et al. as having made the framing observation (W5); add human-oracle error-rate sensitivity (W7).

None of this changes the testbed, the metric, the fault library, or the run budget materially. With these revisions the classical reviewer flips from reject to accept — and this reviewer pool is the modal MASO pool. **Keep the candidate; apply the revision before writing the intro.**
