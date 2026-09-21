# B7 — Authorization, Delegation, and Access Control: Landscape Investigation

**Investigator:** B7 specialist (adversarial evidence-gathering)
**Date:** 21 September 2026
**Mission:** Map Bounded Agents, authorization revocation for long-running agents, capability attenuation/delegation tokens, OAuth-for-agents, confused-deputy problems, and agent identity/AuthN/AuthZ (incl. industry). Determine whether any work connects delegated authority to **failure propagation** or **blast-radius containment** (e.g., revoking authority as containment), and whether anything kills or subsumes the seed hypothesis ("organizational failure propagation and recovery in LLM multi-agent systems").

---

## Bottom line

The authorization/delegation landscape for LLM agents is **crowded and maturing fast** — there is a dense 2025–2026 cluster of papers on delegation security, revocation semantics, privilege control, and agent identity, plus a full industry stack (MCP OAuth 2.1, A2A, Microsoft Entra Agent ID, Auth0/Descope agent identity, OpenID Foundation whitepaper, IETF draft). **However, this entire cluster frames "blast radius" and containment as *security* properties (adversarial prompt injection, compromised agents, zombie credentials), not as *organizational failure propagation* of non-adversarial faults.** The two direct occupants of "blast radius + failure propagation" terminology — *Containing the Cascade* (ICERA 2026) and *What Can One Bad Tool Call Destroy?* (ICML 2026 AIWILD) — study fault/attack propagation containment but **not** through the lens of delegated authority, and (for the former) only in simulation. **Nothing found kills the seed hypothesis, but the terminology "blast radius" is now heavily occupied in adjacent senses; the seed must differentiate explicitly and cite these occupants.** The genuinely open intersection: *does the structure of delegated authority (attenuation, revocation, scope) causally determine the organizational blast radius of an accidental fault, and can runtime authority contraction serve as a containment/recovery mechanism with measurable utility tradeoffs?*

---

## Method and verification notes

- Shared egress IP was heavily rate-limited during this run (arXiv API, Semantic Scholar, OpenAlex all returned sustained 429s; OpenAlex shared daily budget was exhausted by concurrent swarm activity). Verification therefore relied on: arXiv abstract pages via direct fetch (reliable), CrossRef API (reliable), OpenReview API (partial), Semantic Scholar API (intermittent), and direct fetches of standards/industry pages.
- Every paper listed below was verified against its arXiv abstract page, CrossRef record, OpenReview record, or official specification page. Identifiers are exact.
- Two background sweeps (arXiv API: 14 queries; Semantic Scholar: 8 queries) ran with long backoff; partial results are integrated. Raw artifacts: `maso_2026_investigation/raw/b7_arxiv_results.txt`, `b7_s2_results.txt`, sweep scripts `b7_arxiv_sweep.sh`, `b7_s2_sweep.sh`, `b7_oa_search.py`.
- Caution: several 2026 preprints in this space are single-author, low-citation, or from unknown groups; credibility flags are noted per row. One paper ("Blast Radius", arXiv:2608.07440) is a **withdrawn**, unrelated token-management paper — terminology collision only.

---

## 1. The two anchor papers (assignment-named)

### 1.1 Bounded Agents: Delegation Security for Multi-Agent AI Systems

| Field | Value |
|---|---|
| Title | Bounded Agents: Delegation Security for Multi-Agent AI Systems |
| Authors | Xabier Muruaga, Xinming Liu, Joseph Y. Halpern, David Abel, André Barreto, Hado van Hasselt, Benjamin Van Roy, Doina Precup, Satinder Singh, Andrew Critch (DeepMind/Cornell-affiliated author list) |
| Date/venue | arXiv:2608.15888 [cs.AI], v1 16 Aug 2026; 14 pp. |
| URL | https://arxiv.org/abs/2608.15888 |
| Problem | Agent permissions are static at session start; each request evaluated independently; agents can combine permitted actions into prohibited outcomes or delegate authority without limiting it. "A prompt injection poses a risk only if the agent has authority to perform such actions; this is therefore a problem of authorization architecture, not just the model." |
| Method | Agentic Principal Chain (APC): session-scoped authorization state tracked across delegation hops; six authorization checks (incl. scope attenuation, cumulative budgets, composition closure over prior actions, approval binding, evidence, intent binding); enforcement outside the model (PEP/PDP). |
| Formal results | **Blast Radius Monotonicity (Thm 4.6)**: reachable blast radius is non-increasing at each delegation hop (requires scope narrowing, cumulative budget tracking, consistent per-resource blast scores). Composition Soundness (Thm 4.8) for prohibited combinations under complete restriction set + serialized admission. |
| Experimental setting | 3,154 instances: InjecAgent (1,054), AgentDojo (949 utility + 609 compromised-model pairs), ASB (400), 99 delegation-chain scenarios (depth 2–8), 43 adaptive attacks. |
| Metrics | Attack success rate (exfiltration, destruction, manipulation), utility delta, authorization latency (0.24 ms p99). |
| Major findings | AgentDojo exfiltration 75–100% → 0% across all four domains; all 544 InjecAgent data-stealing cases blocked; destruction 38.6%→4.0%, manipulation 90.5%→12.1% via intent binding; utility cost 8.6–13.9 pp on AgentDojo; matched-protocol comparison with Progent within ±2 pp equivalence threshold. |
| Author-stated limitations | Composition Soundness limited to complete restriction sets and serialized admission; per-session composition state (session splitting admitted); blast-radius bound can stay flat without configured attenuation. |
| My inferred limitations | "Blast radius" here is a **deployment-time-assigned static score** per resource (scope × irreversibility × sensitivity, Appendix H), used as budget accounting — **not an empirically measured spread of a fault**. Adversary model is compromise/injection; no accidental-fault injection, no recovery dynamics, no organizational boundaries (role, accountability, human-agent) beyond approval gates. Residual failure taxonomy (18/609 attack successes) is about attack successes, not organizational faults. |
| Code | Publicly available (per abstract). |
| Relation to seed | **Closest formal occupant of "blast radius" + delegation chains.** Occupies: authority attenuation as *preventive* containment of compromised agents, with formal monotonicity. Does NOT occupy: empirical determinants of fault spread, non-adversarial failure propagation, recovery, or utility-preserving containment selection. |

### 1.2 Authorization Revocation for Long-Running AI Agents: Root-Scoped Quiescence under Delegation and Asynchronous Execution

| Field | Value |
|---|---|
| Title | Authorization Revocation for Long-Running AI Agents: Root-Scoped Quiescence under Delegation and Asynchronous Execution |
| Authors | Genliang Zhu, Chu Wang (Accentrust; Georgia Tech; UIUC affiliations) |
| Date/venue | arXiv:2609.21284 [cs.PL], v1 18 Sep 2026 (3 days before this investigation); 39 pp. with proof appendix |
| URL | https://arxiv.org/abs/2609.21284 |
| Problem | Long-running agents outlive initiating processes via credentials, delegated tasks, queues, callbacks, reservations, provider-side operations. Cancellation, process exit, and token revocation (RFC 7009) neither close every pre-cut carrier nor distinguish independently authorized shared work. |
| Method | Root-scoped authorization quiescence: per-sink certificates accounting for cut-relevant acceptances under a retired root-epoch atom; linearized root cut + fences; authority as antichains of minimal sufficient root sets; provider-frontier certificates composed into a cutset; exact channel-token accounting. |
| Formal results | Post-cut issuer non-expansion; support-sound projection; compositional soundness under exact channel conservation; independent-support preservation; merge-order independence; crash/replay stability. |
| Experimental setting | Provider-free late-effect test suite: 17/17 registered outcomes matched; cancellation-only and cut-only executions accept already-scheduled late effects; cut-plus-fence, restart, stale-process executions reject them; independent checker verifies 17/17 traces, rejects 44/44 semantic regressions. |
| Metrics | Trace/certificate match counts; no task-utility or LLM evaluation. |
| Author-stated limitations | Certificate establishes root-relative quiescence within bound manifest/config — **not** global idleness, rollback, or business completion; missing/conflicting evidence remains indeterminate. |
| My inferred limitations | Pure protocol-level correctness; no empirical MAS workload, no organizational semantics, no measurement of what revocation *contains* in task terms. |
| Code | Checker mentioned; artifact availability unclear from abstract. |
| Relation to seed | Occupies **revocation semantics** (what it means for authority to be truly withdrawn under async execution). This is the *mechanism layer* for "revoking authority as containment" — but it contains *authority*, not *failures*, and measures correctness, not blast radius or utility. |

---

## 2. The 2025–2026 agent-authorization cluster (verified)

All verified via arXiv abstract pages unless noted. Credibility: ★ = strong venue/authors; ○ = unvetted preprint.

| Paper | ID / venue | Date | Core contribution | Failure/blast-radius link | Cred. |
|---|---|---|---|---|---|
| Authenticated Delegation and Authorized AI Agents (South et al.) | arXiv:2501.09674 | Jan 2025 | OAuth 2.0/OIDC extension with agent-specific credentials; NL permissions → auditable access-control configs | Accountability chains; no failure propagation | ★ (MIT Media Lab authors; widely cited) |
| CaMeL: Defeating Prompt Injections by Design (Debenedetti et al.) | arXiv:2503.18813 | Mar 2025 | Control/data-flow separation + **capabilities** enforced at tool calls; AgentDojo 77% utility with provable security vs 84% undefended | Capability restriction as injection containment | ★ (Google DeepMind/ETH) |
| Progent: Securing AI Agents with Privilege Control (Shi et al.) | arXiv:2504.11703 (v3 May 2026) | Apr 2025 | Least-privilege policy DSL; SMT-checked updates; **monotonic confinement** (privilege only shrinks without approval); AgentDojo/ASB | Privilege contraction as containment; temporal monotonicity | ★ |
| SAGA: Security Architecture for Governing Agentic Systems (Syros et al.) | arXiv:2504.21034 | Apr 2025 | User-controlled agent lifecycle; cryptographic access-control tokens for inter-agent communication; minimal overhead, no utility impact | User oversight/revocation of agents; no failure study | ★ |
| Identity Management for Agentic AI (South et al., 21 authors) | arXiv:2510.25819; **OpenID Foundation whitepaper** | Oct 2025 | Strategic agenda for agent AuthN/AuthZ; surveys existing standards | Frames delegated authority problem space | ★ (standards body) |
| Agent Cascading Injection / "Towards Unifying Quantitative Security Benchmarking for MAS" (Huang et al.) | arXiv:2507.21146 | Jul 2025 | Formalizes **Agent Cascading Injection**; "Agent Impact Chain and Blast Radius" mapped to OWASP agentic risk categories | **Adversarial cascade across inter-agent trust; blast radius as security metric** | ○ |
| SEAgent: Taming Privilege Escalation via MAC (Ji et al.) | arXiv:2601.11893 | Jan 2026 | ABAC-based mandatory access control; information-flow graph; identifies **confused-deputy variant in multi-agent systems** | Privilege escalation containment | ○/★ |
| Authenticated Workflows / MAPL (Rajagopalan & Rao) | arXiv:2602.10465 | Feb 2026 | Trust layer enforcing intent+integrity at prompt/tool/data/context boundaries; 9 frameworks; formal completeness/soundness | Boundary enforcement; no propagation study | ○ |
| Capability Gates Are Not Authorization / ScopeGate (Mellafe Zuvic) | arXiv:2606.28679 | Jun 2026 | Audit: LangChain/LangGraph, LlamaIndex, Stripe Agent Toolkit lack fail-closed per-call value authorization; ScopeGate PDP/PEP; 0/29 unauthorized attempts | **Confused-deputy failures in real frameworks** | ○ |
| Authorization-Execution Gap position paper (Wu et al.) | arXiv:2605.11003 | May 2026 | AEG: divergence between authorized intent and execution; three structural sources (delegation incompleteness, channel corruption, composition fragmentation) | **Explicitly links authorization divergence to agent *failures*; position only, no experiments** | ○ (Baoyuan Wu group) |
| AIRGuard (Qin et al.) | arXiv:2605.28914 | May 2026 | "Authority confusion" failure mode; runtime action-time authorization; AgentTrap ASR 36.3%→5.5%; DTAP-150 utility 76% | Runtime authority control vs attacks | ○ |
| Heartbeat-Bound Hierarchical Credentials (Deochake) | arXiv:2605.20704 | May 2026 | Credential validity bound to parent liveness; **"zombie agents"**; 90× reduction of zombie window vs OAuth 2.0; **cascading revocation across 49-agent 4-level hierarchy**; 0 post-revocation tool calls under injection | **Revocation as containment of compromised/runaway agents — closest to "revoking authority as containment"** | ○ |
| Stop Means Stop / SOUNDGATE (Khan) | arXiv:2607.14166 (v3 Aug 2026) | Jul 2026 | Control primitives (approval gates, cancellation, timeouts) lack barrier semantics on 6 frameworks; sibling leak, cancellation orphans, timeout zombies; formally verified external gate (Verus/TLA+) | **Enforcement gap → containment failure of paused/cancelled runs** | ○ |
| Earned Authority under a Fixed Ceiling (Zhang & Zhang) | arXiv:2607.23586 | Jul 2026 | Authorization continuity for evolving agents; immutable effect ceiling; mutation cannot amplify effects beyond user-issued ceiling | Authority validity under agent evolution | ○ |
| AID-Guard (Tong et al.) | arXiv:2608.21159 | Aug 2026 | Stateful authorization-to-effect closure; at-most-one effect across retry/recovery; crash-recovery schedules; strict profile costs 35.4–43.8 pp utility | **Authorization across crash/recovery; utility tradeoff measured** | ○ |
| VERA: Authority-Preserving Edge Revocation (Liu, Yu, Jiang) | arXiv:2608.30091 | Aug 2026 | Verifiable edge-revocation contract; **tree cascades over-revoke shared agents; deployer-scoped cascades under-revoke cross-domain descendants**; LangGraph/AutoGen/CrewAI traces | **Revocation precision = the blast radius OF a revocation action** | ○ |
| CONTINUITY (Zheng & Yang) | arXiv:2609.05269 | Sep 2026 | Assume-guarantee contracts for composing agent security controls; 32 fault classes, 2,560 attack instances; consequence integrity | Security-context discontinuity as failure mode | ○ |
| ResidualAuth (Choi, Jeong, Lee) | arXiv:2609.08062 | Sep 2026 | Residual authorization state under revocable delegation; exponential state lower bounds; LLM episodes show models can't reconstruct required state from summaries | State needed for correct post-revocation decisions | ○ |
| EFFECTBOUND / "When Does Authorization End?" (Santos-Grueiro) | arXiv:2609.02866 | Sep 2026 | Policy-relative effect closure at provider boundaries; GitHub/K8s/NATS/Kafka case studies show revoked authority can still cause effects | Revocation incompleteness in real systems | ○ |
| Lingering Authority (Santos-Grueiro) | arXiv:2606.22504 | Jun 2026 | Revocable resource-and-effect capabilities for coding agents | Revocation design | ○ |
| Temporary Authority, Permanent Effects (Santos-Grueiro) | arXiv:2607.10487 | Jul 2026 | Commit-time authorization for LLM agents | Commit-boundary semantics | ○ |
| EBL-Core / From Intent to Execution Grant (Wu et al.) | arXiv:2609.11596 | Sep 2026 | Execution-boundary conformance profile; Execution Release Contracts; revoke-redeem races | Execution-boundary semantics | ○ |
| ARC: Agentic Risk & Capability Framework (Khoo et al.) | arXiv:2512.22211; IASEAI 2026 + AAAI 2026 AI Governance WS | Dec 2025 | Capability-centric organizational risk governance framework | Governance framing of agent capability risk | ○/★ |

---

## 3. Standards and industry (verified by direct fetch)

| Artifact | Identifier | What it establishes |
|---|---|---|
| MCP Authorization spec (2025-06-18) | modelcontextprotocol.io/specification/2025-06-18/basic/authorization | OAuth 2.1 for MCP; **explicit Confused Deputy section**; token audience binding (RFC 8707); token passthrough forbidden; PKCE; short-lived tokens |
| A2A Protocol v1.0.0 | a2a-protocol.org/latest/specification | Agent interoperability; "enterprise ready" authN/Z deferred to standard web security; opaque execution; task cancel op (cooperative, not authoritative per 2609.21284) |
| IETF Internet-Draft | draft-daniel-ai-agent-internet-architecture-03 (Park & Siddique, Samsung/Opaque, Aug 2026) | Architectural requirements for Internet-scale agents: naming/discovery, authN/Z/delegation, workload identity, **revocation (§18)**, provenance, payments |
| OAuth 2.0 Token Revocation | RFC 7009 (2013) | Baseline token revocation (named-token only) |
| OAuth 2.0 Token Exchange | RFC 8693 (2020) | act/on-behalf-of chains — delegation representation |
| OAuth Rich Authorization Requests | RFC 9396 (2023) | Fine-grained authorization details |
| OpenID Foundation whitepaper | arXiv:2510.25819 (see §2) | Industry-consensus agenda for agent identity |
| Microsoft Entra Agent ID | learn.microsoft.com/en-us/entra/agent-id/ (docs live) | Enterprise agent identity platform; OAuth flows; "Agent 365" control plane; Zero Trust positioning |
| Auth0 for AI Agents | auth0.com/ai | Token Vault (short-lived scoped tokens), FGA for RAG, CIBA-style human approval, MCP OAuth 2.1; **"revoke an individual agent's access without taking down your entire workflow"** (marketing-level revocation-as-containment) |
| Descope Agentic Identity Hub | descope.com/ai | Agent directory, per-agent/per-tool scopes, ID-JAG cross-app access, **"revoke a misbehaving agent instantly"** |
| Okta | okta.com/ai (page live, thin content) | "Secure AI" positioning; AI at Work 2025 report |
| OWASP GenAI Security Project | owasp.org/www-project-top-10-for-large-language-model-applications | Agentic Top 10; MAS Threat Modelling Guide; Agentic AI Vulnerability Scoring System (cited by 2507.21146) |
| CSA MAESTRO; AIUC-1 | cited in Bounded Agents refs (2025) | Multi-agent threat framework; agent security/safety/reliability standard |

**Industry summary:** every major identity vendor now sells agent AuthN/AuthZ with per-agent identity, scoped short-lived tokens, human-approval gates, and instant revocation. None publishes failure-propagation analysis; revocation is sold as a security/compliance feature, not evaluated as a fault-containment mechanism with utility tradeoffs.

---

## 4. Classical anchors (verified via CrossRef / reference lists of §1–2 papers)

| Work | Identifier | Relevance |
|---|---|---|
| Hardy, "The Confused Deputy" | ACM SIGOPS OSR 22(4), Oct 1988, DOI 10.1145/54289.871709 | Origin of confused-deputy; capability motivation |
| Dennis & Van Horn, capability semantics | CACM 9(3), 1966 | Capabilities |
| Saltzer & Schroeder, protection principles | Proc. IEEE 63(9), 1975, DOI 10.1109/PROC.1975.9939 | Least privilege, fail-safe defaults |
| Denning, lattice model of information flow | CACM 19(5), 1976 | IFC |
| Miller, "Robust Composition" | PhD thesis, Johns Hopkins, 2006 | Object-capability composition |
| SPKI Certificate Theory | RFC 2693 (Ellison et al., 1999) | Delegation certificates |
| Abadi, Burrows, Lampson, Plotkin, access-control calculus | ACM TOPLAS 15(4), 1993, DOI 10.1145/155183.155225 | "Speaks-for" delegation logic |
| Li, Mitchell, Winsborough, RT trust management | IEEE S&P 2002, DOI 10.1109/secpri.2002.1004366 | Role-based delegated trust |
| Li, Grosof, Feigenbaum, Delegation Logic | ACM TISSEC 6(1), 2003, DOI 10.1145/605434.605438 | Distributed authorization logic |
| Zhang, Ahn, Chu, role-based delegation+revocation | ACM TISSEC 6(3), 2003, DOI 10.1145/937527.937530 | Delegation/revocation models |
| Hagström et al., "Revocations—A Classification" | IEEE CSFW 2001, DOI 10.1109/CSFW.2001.930135 | Revocation taxonomy (propagation, dominance) |
| Wainer, Kumar, Barthelmess, DW-RBAC | Information Systems 32(3), 2007, DOI 10.1016/j.is.2005.11.008 | Delegation/revocation in **workflow systems** |
| Park & Sandhu, UCON ABC | ACM TISSEC 7(1), 2004, DOI 10.1145/984334.984339 | Usage control: **ongoing-access revocation, mutable attributes** |
| Birgisson et al., Macaroons | NDSS 2014, DOI 10.14722/ndss.2014.23212 | **Contextual caveats = token attenuation** |
| Myers & Liskov, DIFC | SOSP 1997; ACM TOSEM 9(4), 2000 | Decentralized information flow |
| Pang et al., Zanzibar | USENIX ATC 2019 | Global authorization at scale |
| Chandy & Lamport, distributed snapshots | ACM TOCS 3(1), 1985, DOI 10.1145/214451.214456 | Quiescence foundations |
| Garcia-Molina & Salem, Sagas | ACM SIGMOD 1987, DOI 10.1145/38713.38742 | Compensation/recovery |
| Gray & Cheriton, Leases | SOSP 1989, DOI 10.1145/74850.74870 | Time-bounded authority (heartbeat credentials echo this) |
| NIST SP 800-207 (Zero Trust); NIST SP 800-162 (ABAC); Sandhu et al. RBAC (1996) | DOI 10.6028/NIST.SP.800-207 | Enterprise authorization baselines |

**Classical note:** revocation-propagation semantics (Hagström 2001), usage control with ongoing revocation (UCON 2004), and delegation/revocation in workflows (DW-RBAC 2007) all predate LLMs and provide ready-made formal vocabulary. The 2026 agent-revocation cluster (§2) is re-deriving much of this with LLM-specific evidence.

---

## 5. The key question: delegated authority ↔ failure propagation / blast-radius containment

### 5.1 Direct occupants of "failure propagation + blast radius" (NOT authorization-based)

| Paper | Identifier | What it does | Why it doesn't subsume the seed |
|---|---|---|---|
| **Containing the Cascade: A Benchmark and Reference Mediator for Failure Propagation in Tool-Using LLM Multi-Agent Systems** (Divi, Gullapalli, Brahmandam) | IEEE ICERA 2026, DOI 10.1109/ICERA72709.2026.11666599, Jul 2026; OA PDF at Zenodo (10.5281/zenodo.21314250, 403 on fetch) | Taxonomy of 6 cascading-failure modes; containment metrics (**containment rate, cascade depth, blast radius, MTTD**); Cascade-Bench: 1,080 fault-injection scenarios, 6 domains, **discrete-event simulation** calibrated to reported MAS failure stats; Sentinel mediator (typed message contracts, semantic anomaly gate, circuit breaker, checkpoint recovery); 48 configs, 590k simulated executions; task success 31.3%→83.7% | **Serious novelty threat on terminology and benchmark shape.** But: simulation-only (no real LLM agents); containment via message-mediator, **not via authority/delegation structure**; no organizational boundaries (authority, accountability, human-agent); low-tier venue, 0 citations; abstract truncated at "containment…" (full numbers unverified) |
| **What Can One Bad Tool Call Destroy? Measuring and Minimizing Blast Radius in Agentic Tool Use** | OpenReview MYvsxnxbCf, **ICML 2026 AIWILD workshop** | Title/venue verified via OpenReview API; abstract not anonymously retrievable (browser check on web, empty note fetch) | Occupies "blast radius of one bad tool call" framing at a credible venue. Scope unknown (likely single-agent tool use). Must be obtained and cited; if it measures blast radius empirically in real agent stacks, it is the closest occupant of the *measurement* idea |
| Agent Cascading Injection (Huang et al.) | arXiv:2507.21146, Jul 2025 | Adversarial cascade across inter-agent trust; blast radius as OWASP-style security metric | Adversarial only; position/benchmarking-methodology paper |
| Behavioral Drift in Multi-Agent LLM Systems (Gagne) | SSRN 2026, DOI 10.2139/ssrn.6420858 | Empirical longitudinal drift; **cascade propagation** (one agent's failure degrades others), agent collapse, compensatory expansion; black-box, 200–500 turns | Failure propagation evidence but no containment mechanisms, no authority dimension |
| Failure Modes in Production Multi-Agent LLM Systems (Ahmed & Akbar) | SSRN 2026, DOI 10.2139/ssrn.7041478 | 5 production failure classes (intent misclassification >80% on boundary queries, context amnesia, cache poisoning, inference bottlenecks, cross-session contamination) | Practice report; no containment formalism |
| PACMI (Wang et al.) | SSRN 2026, DOI 10.2139/ssrn.7480138 | Provenance-aware **cascading memory invalidation** for long-term agent memory | Memory-boundary failure containment — adjacent to one seed boundary type |
| Multi-Agent Orchestration: Coordination, Trust, and Cascading Failures (Tanveer) | SSRN 2026, DOI 10.2139/ssrn.6734798 | Synthesis/review | Review only |

### 5.2 Authorization-side works that touch containment (security framing)

- **Bounded Agents (2608.15888):** blast-radius monotonicity across delegation hops — preventive, adversarial, static per-resource scores.
- **HBHC (2605.20704):** cascading credential revocation kills zombie agents within bounded window — revocation *as* containment, but of compromised agents, measured as zombie-window length, not task-failure spread.
- **VERA (2608.30091):** over/under-revocation in delegation graphs — the *blast radius of revocation itself*; correctness framing, no fault-injection of task failures.
- **SOUNDGATE (2607.14166):** cancellation/approval primitives fail to contain side effects on 6 frameworks — containment *enforcement gap*, not propagation dynamics.
- **AID-Guard (2608.21159):** authorization-to-effect closure under crash/recovery, with measured utility cost (35–44 pp strict) — closest to utility-containment tradeoff measurement, but for effect duplication, not organizational faults.
- **AEG position (2605.11003):** argues agent *failures* trace to authorization divergence (delegation incompleteness, channel corruption, composition fragmentation) — conceptual link only, no experiments.

### 5.3 The unoccupied intersection

No located work does all of: (a) inject **non-adversarial, organizational faults** (role confusion, stale memory, mis-scoped delegation, accountability gaps) into **real LLM MAS**; (b) measure **empirical blast radius across multiple boundary types** (role, communication, authority, tool, memory, accountability, human-agent); (c) treat **authority contraction/revocation/attenuation as runtime containment levers** and compare them against other containment mechanisms (circuit breakers, checkpoints, mediators) on **both containment and task utility**; (d) study **recovery** after containment. Each ingredient exists separately; the combination is open.

---

## 6. Does anything kill or subsume the seed hypothesis?

**No kill.** But three genuine threats to manage:

1. **Terminology occupation.** "Blast radius" is now used by: Bounded Agents (formal, delegation chains, security), Containing the Cascade (metric in a failure-propagation benchmark), ICML 2026 AIWILD paper (agentic tool use), ACI/OWASP (adversarial cascade), plus networking ("Failure Domain Isolation… Blast Radius Containment", DOI 10.23919/iccmsocps00092.2026.00027). A MASO paper must define "organizational blast radius" precisely and differentiate from all five senses.
2. **Benchmark-shape occupation.** Containing the Cascade already claims "first benchmark + reference mediator for failure propagation containment with blast-radius metrics" (albeit simulated, low-tier venue, 0 citations). The seed's contribution must be real-LLM, organizational, and authority-aware — and must cite this.
3. **Occupied delegation-invariants territory.** The repo's existing MASO proposal already lists "cascade depth and blast radius", "time to containment", "revocation propagation time" as metrics for delegation chains (maso/policy_preserving_delegation_research_proposal.md:344-352). The authority-boundary slice of the seed overlaps that proposal; positioning must be coordinated.

**Subsumption risk: low.** The authorization cluster subsumes *mechanisms* (attenuation, revocation, quiescence, effect closure) that a seed project would *use*, not the seed's research question (what determines fault spread; which containment minimizes systemic impact while preserving utility).

---

## 7. Credibility and caveats

- Bounded Agents has a heavyweight author list (DeepMind/Cornell) but is arXiv-only as of this writing.
- The 2026 revocation/effect-closure cluster (Santos-Grueiro ×3, Lee/RISU, Choi et al., Tong et al., Liu et al., Zhang & Zhang, Zheng & Yang, Wu et al. ×2) is almost entirely **single-venue arXiv preprints with zero citations**, several from the same small orbit (cross-citing each other). Treat as emerging, unvetted work.
- "Blast Radius" (arXiv:2608.07440) is **withdrawn** and unrelated (token/memory management) — terminology collision only.
- ICERA is a low-tier IEEE venue; the Containing the Cascade claims (esp. 590k simulated executions) could not be fully verified beyond the abstract (IEEE page JS-blocked; Zenodo 403).
- ICML 2026 AIWILD paper: title/venue verified via OpenReview API; abstract inaccessible anonymously.
- arXiv API and Semantic Scholar were rate-limited for much of this run; recall on 2026 preprints may be incomplete. Background sweeps (scripts preserved in `maso_2026_investigation/raw/`) were terminated after sustained 429 starvation; re-running them later on an uncontended network is a cheap completeness check.

---

## 8. Search log (queries executed)

arXiv API (background sweep, heavy 429 contention): "confused deputy"+agent; OAuth+AI agent; agent identity+authorization; delegation+token+LLM; "blast radius"+agent; "failure propagation"+multi-agent; "least privilege"+agent; revocation+AI agent; capability+delegation+LLM; MCP+authorization; agentic+authorization; "error cascade"+agent; containment+prompt injection; privilege+LLM agent+control.
Semantic Scholar (background sweep): blast radius+agent+containment (completed); revocation+containment+AI agent+authority; capability attenuation+delegation+token; OAuth+AI agents; delegation+authorization+multi-agent+LLM; agent identity+authentication+agentic; failure propagation+containment+LLM agents; cascade+containment+multi-agent.
CrossRef: Macaroons; confused deputy (Hardy); Abadi calculus; RT framework; IsolateGPT; AirGapAgent; failure propagation/cascading failures/error propagation × multi-agent LLM; agentic AI security surveys; SSRN records (7041478, 6420858, 6734798, 7480138); ICERA DOI.
OpenReview API: "blast radius agent"; "agent revocation"; "delegation security agent".
Direct fetches: arXiv abs pages (2608.15888, 2609.21284, 2503.18813, 2504.11703, 2501.09674, 2510.25819, 2601.11893, 2602.10465, 2512.22211, 2607.14166, 2605.11003, 2605.28914, 2608.21159, 2609.08062, 2607.23586, 2608.30091, 2605.20704, 2609.05269, 2609.02866, 2609.11596, 2507.21146, 2608.07440); arXiv HTML full text (2608.15888, 2609.21284 — reference lists mined); MCP authorization spec; A2A spec v1.0.0; IETF draft-daniel-ai-agent-internet-architecture-03; Auth0 for AI Agents; Descope Agentic Identity Hub; Microsoft Entra Agent ID docs; Okta /ai; OWASP GenAI project.
