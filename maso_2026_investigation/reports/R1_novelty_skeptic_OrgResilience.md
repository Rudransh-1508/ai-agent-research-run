# MASO 2026 — REVIEWER 1 (NOVELTY SKEPTIC): "OrgResilience"

**Paper:** "Do Classical Organizational Fault-Handling Results Hold for LLM Multi-Agent Systems? Measuring Organizational Fault Propagation and Containment in Agentic Workflows"
**Reviewer mindset:** Everything is incremental recombination until proven otherwise. I attack novelty, not soundness.
**Date:** 21 Sep 2026
**Citations verified this session or in prior investigation waves:** DebtRank (Battiston et al., Sci. Rep. 2:541, 2012, DOI 10.1038/srep00541 — verified via nature.com full text 21 Sep); Kempe, Kleinberg & Tardos, KDD 2003, DOI 10.1145/956750.956769 (verified via Crossref 21 Sep); Horton, "Homo Silicus," NBER WP 31122 (verified via nber.org 21 Sep); Dellarocas & Klein ICMAS 2000, DOI 10.1109/ICMAS.2000.858440 (full text read, E5); Hägg 1997, DOI 10.1007/BFb0030090 (E5); Containing the Cascade, ICERA 2026, DOI 10.1109/ICERA72709.2026.11666599 (Crossref + Zenodo tombstone, W2-cand1); OrchestraBench arXiv:2608.05263 (full text read, W2-cand1); DamageFlow/BlastGuard, ICML 2026 AIWILD, OpenReview MYvsxnxbCf (B8/B9/E3); Bounded Agents arXiv:2608.15888 (C6); MAS-FIRE arXiv:2602.19843 (B5); IMACS arXiv:2607.25446 (D5/W2); La Malfa et al., NeurIPS 2025 position, arXiv:2505.21298 (W2-cand2); Akata et al., Nat. Hum. Behav. 2025, DOI 10.1038/s41562-025-02172-y (Crossref, W2-cand2); Aher et al., ICML 2023 oral, arXiv:2208.10264 (W2-cand2); "Can Lessons From Human Teams Be Applied to MAS?", arXiv:2510.07488 (W2-cand2); Zhou et al., ICML 2025, arXiv:2408.00989 (wave 1).

---

## 1. Summary as I understand it

The authors build a fault-injectable organizational testbed (tau2-bench retail + a new IT-incident workflow, on LangGraph), vary organizational structure (flat / 2-level / 3-level hierarchy, ± sentinel agents, ± resource scarcity), inject 5–7 benign semantic faults, and measure an "Organizational Blast Radius" (OBR: fraction of seven typed organizational boundaries crossed by provenance-traced corrupted events), containment latencies, utility preservation, and a priced recovery-cost vector. Six containment policies (none, retry, verifier gate, checkpoint-rollback, sentinel quarantine + re-delegation, scripted-oracle human escalation) are compared on a cost-utility Pareto. The evaluation frame is a pre-registered transfer test of classical MAS fault-handling predictions (Dellarocas & Klein's unzippering and scarcity-backfire, Hägg's sentinels, Horling & Lesser's hierarchy), with TOST equivalence testing so that "classical prediction fails" is a designed-in outcome. ~3,400 runs; continuous OBR co-primary; within-instance pairing.

## 2. Strengths (grudging)

- The pre-registration + TOST design is methodologically respectable; equivalence bounds make nulls publishable rather than p-hunted.
- Deterministic DB-state ground truth as primary endpoint, LLM-judge gated and audited, is better measurement hygiene than most of this literature (including several of the papers the authors must differentiate from).
- The specific conjunction — org structure as IV × organic faults × real multi-agent LLM execution × typed-boundary spread × mechanism bake-off — is, per my own checking of the record, verifiably empty. Nobody has run exactly this experiment.
- Pricing human oversight minutes against automated containment is a genuinely under-measured quantity.
- Venue fit is excellent; the classical lineage will flatter this reviewer pool. (This is also a weakness — see W5.)

## 3. Weaknesses — the rejection case, ranked

### W1 (most severe). The paper is a recombination of four named, published antecedents, and each leg of the differentiation is a substrate swap, not an idea.

I take the four "is it just X?" charges in turn.

**(a) "Just IMACS + MAS-FIRE"?** *Differentiation holds on artifacts, collapses on concept.* Yes, neither artifact is runnable (MAS-FIRE's repo is data-only; IMACS has no released code), and the boundary-typed fault model and spread instrumentation do not exist off the shelf. But the *research plan* — "make org structure a config knob (IMACS), inject typed faults (MAS-FIRE), measure spread" — is a one-sentence recombination that any competent team could state after reading those two abstracts. The delta is engineering effort, not intellectual content. Engineering effort is not a workshop-paper contribution unless the measurements surprise; see W3.

**(b) "Just Containing the Cascade with real LLMs"?** *Partially collapses, and this is the most damaging single comparison.* CtC (ICERA 2026) already has: the metric name ("blast radius"), the containment mechanisms (sentinel mediator, circuit breaker, checkpoint rollback — three of this paper's six arms), MTTD, containment rate, and a fail-safe/fail-operational ablation. The authors' differentiation is: CtC is simulation-only, and they add org-structure IV, typed boundaries, and priced human escalation. But "we ran it with real LLMs" is a substrate argument, and "we vary hierarchy depth" is Dellarocas & Klein's variable from 2000, not a new one. The honest residual claim is "real multi-agent executions with organizational structure as the varied factor" — one independent variable and one substrate swap away from a published, peer-reviewed 2026 paper.

**(c) "Just DamageFlow for benign faults"?** *Metric philosophy collapses; organizational semantics survive.* DamageFlow's Blast Radius Score already decomposes damage into propagation and recovery cost, is provenance-based, and is evaluated against benign-utility preservation (87.5% retained) — which is exactly this paper's OBR + recovery-cost vector + utility-preservation triad. The differentiation is the threat model (adversarial → organic) and the boundary typing (tool-state → role/authority/memory/accountability/human). The threat-model swap is a scope decision; the boundary typing is real but is a *labeling scheme* (see W2). A reviewer who has read DamageFlow will read OBR as "BRS with a different denominator."

**(d) "Just Dellarocas & Klein rerun on GPT"?** *For H1–H3, yes, by design — and the authors say so. The problem is that H4, the novel leg, is predictable.* H1 (unzippering magnitude), H2 (sentinel containment), H3 (containment backfires under scarcity) are D&K's three experiments with LLMs substituted for contract-net agents. The paper's novelty therefore rests entirely on H4: "classical predictions break under semantic LLM faults." But the headline version of H4 — *syntactic/structural detectors fail to detect semantic faults* — is true by definition and needs no 3,400-run matrix. If the paper's surprises are confined to magnitudes, it is a measurement paper about an experiment whose qualitative outcome the abstract already gives away.

### W2. OBR is a renamed cascade-size measure; the "typing" is a denominator relabeling, not a new instrument.

OBR = |boundaries crossed by corrupted provenance-descendants| / |boundaries|. Strip the vocabulary: this is the *final outbreak size* of a cascade, normalized by a partition of the system into compartments. The lineage: epidemic final-size and cascade-size measures (Kempe, Kleinberg & Tardos, KDD 2003, DOI 10.1145/956750.956769); DebtRank's "fraction of total economic value affected by the distress of node i" (Battiston et al., Sci. Rep. 2012, DOI 10.1038/srep00541); CtC's blast radius; OrchestraBench's cascade radius (downstream stages corrupted); DamageFlow's BRS propagation component; Hallucination Snowball's per-stage escape probabilities. What is new is the *partition*: seven typed organizational boundaries instead of pipeline stages or network nodes. That is a definitional contribution, and a useful one for this community — but the paper presents OBR as a metric contribution, and a metric whose novelty is the choice of denominator is a measurement convention, not a measurement advance. The fact that the authors must disambiguate "blast radius" from *five occupied senses* in their own related-work section is the tell: the term is crowded precisely because the underlying quantity is 25 years old in five fields.

### W3. The classical-transfer frame is the Akata/Aher/Horton genre template applied once more — and this instance has less suspense than its predecessors.

"Take classical result X, re-run with LLMs, report where it breaks" is now a four-year-old genre with top-venue instances: Aher et al. (ICML 2023 oral, arXiv:2208.10264), Horton's Homo silicus (NBER WP 31122), Akata et al. (Nat. Hum. Behav. 2025, DOI 10.1038/s41562-025-02172-y), and — closest in spirit — "Can Lessons From Human Teams Be Applied to Multi-Agent Systems?" (arXiv:2510.07488), which already does structure-transfer (flat > hierarchical) for LLM teams. The genre is also accumulating methodological fatigue critiques (analytic-flexibility concerns, Crossref-registered reviews 2025–26). The authors' version is better engineered than most, but the *frame* contributes nothing the genre hasn't established, and the specific predictions under test have a suspense problem: H2 transferring would be unsurprising (sentinels are just monitors), H4's qualitative direction is foreordained (W1d), and H1/H3 depend on whether "scarcity of subcontractors" maps onto "scarcity of tokens/specialist agents" in a way that preserves the classical mechanism — a mapping the paper asserts rather than justifies. La Malfa et al. (NeurIPS 2025, arXiv:2505.21298) already issued the call this paper answers; answering a named, published call is valuable but is, definitionally, not a novel framing.

### W4. The differentiation obligations are self-incriminating.

A paper that must cite-and-differentiate twelve named 2025–2026 occupants (CtC, DamageFlow, Bounded Agents, OrchestraBench, From Spark to Fire, MAS-FIRE, AgentChaos, Emergence World, Collective Loss of Control, TPSC, La Malfa, plus the classical line) before its contribution is visible is telling the program committee that its neighborhood is densely settled. Each individual differentiation is defensible; collectively they describe a contribution defined by a conjunction of negations. Conjunctions of occupied ideas are fragile: any one occupant adding one experiment (OrchestraBench going multi-agent — its own stated future work; TPSC adding a spread metric; Emergence World adding fault injection) collapses the claim. The authors acknowledge none of this fragility.

### W5 (least severe, for this pool). The classical-MAS reviewer pool will like this paper for the wrong reason.

The replication content flatters the community's heritage. That buys goodwill, not novelty; a novelty-focused reviewer (or the meta-reviewer counting "incremental" votes) will discount it.

## 4. Questions to authors

1. Name one quantitative prediction of the classical literature that your experiment could plausibly *confirm with a surprising magnitude* or *falsify in a surprising direction* — i.e., a result a reader could not write down before seeing your data. If H4's answer is "syntactic sentinels miss semantic faults," why does that require 3,400 runs?
2. What does OBR measure that a per-boundary escape-probability table (Hallucination Snowball style) or a cascade-radius count (OrchestraBench style) over the same traces does not? Show the metric changing a conclusion, not just relabeling it.
3. Your scarcity manipulation: is the scarce resource tokens, specialist-agent capacity, or approval-tool rate limits? D&K's backfire mechanism is competition for a bottleneck *redeployment* resource — which of your operationalizations preserves that mechanism, and how do you know?
4. If OrchestraBench's authors run their stated future work (a real multi-agent harness) with a hierarchy variable before December, what remains of this paper?
5. Why is the memory boundary — the one boundary with no classical antecedent and no 2026 occupant — confined to a sub-study rather than headline?

## 5. Score

**Reject. Confidence: 3.5/5.**

Not strong reject: the conjunction is verifiably empty, the execution is non-trivial, the statistics are honest, and the venue fit is real. But on novelty — my mandate — every load-bearing element has a named antecedent, the metric is a relabeled cascade size, the frame is a fatigued genre template, and the one novel hypothesis has a foreordained qualitative answer. This is a good engineering study of other people's ideas.

## 6. Single change that would most improve my score

**Re-center the paper on a result that is not predictable from its own related-work section.** Concretely: make the *memory boundary* (memory poisoning/staleness propagation — the one boundary with zero classical coverage and zero 2026 occupancy) and any *qualitatively non-classical* transfer failure (e.g., containment backfiring through a mechanism D&K never had, such as semantic laundering of corrupted content through authority chains) the headline, pre-registered hypotheses — with the unzippering/sentinel/scarcity replication demoted to a "classical grounding" section, OBR demoted to instrumentation, and the testbed to an artifact claim. If the headline finding is something Dellarocas & Klein could not have stated and OrchestraBench cannot produce by adding one harness, the recombination charge dies. As submitted, the headline is a 26-year-old experiment with a new substrate.

---

## ORCHESTRATOR NOTE

**Recommendation: SURVIVES, wounded — revise, don't kill.**

The novelty skeptic's case is strong on framing but cannot land a clean kill: the specific conjunction (org structure as IV × organic faults × real multi-agent LLM execution × typed-boundary spread × priced mechanism bake-off) is verified empty across two waves of search, and the recombination charge fails on artifacts (nothing to recombine — no runnable prior system exists). What the review gets right, and what must be fixed:

1. **H4 as currently framed is suspense-free.** "Syntactic detectors miss semantic faults" is definitional. The paper must pre-register *quantitative, non-obvious* transfer predictions: magnitude shifts of unzippering under semantic faults, the scarcity-backfire crossover under token/specialist scarcity (a sign reversal is the one adequately powered interaction), and detection-granularity thresholds.
2. **Promote the memory boundary from sub-study to headline.** It is the only boundary with no classical antecedent (E5) and no 2026 occupant — the cleanest novelty the candidate owns.
3. **Demote OBR from "metric contribution" to instrumentation**; present per-boundary escape probabilities as the table and OBR as the summary statistic. Pre-empt the DebtRank/cascade-size lineage in one paragraph.
4. **Frame as answering La Malfa et al.'s NeurIPS 2025 call**, never as "first to bridge classical MAS and LLMs."
5. **Keep the name "Organizational Blast Radius" only with the five-sense disambiguation**, or rename to "boundary-typed failure spread."

With those revisions the surviving novelty-skeptic objection shrinks to "incremental but well-executed" — which, at a workshop colocated with PRIMA's "Beyond Traditional MAS" theme, is an accept.
