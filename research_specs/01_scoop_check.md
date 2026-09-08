# Scoop-Risk Reconnaissance — LLM Agent Teams vs. Decentralized-Optimal Dec-POMDP Values

Date of check: 2026-09-08. AAMAS 2027 deadline: 2026-10-08 (~4 weeks out).

## Bottom line

No paper found does the specific thing planned: **evaluating LLM agent teams against a solver-computed decentralized-optimal value for small finite-horizon Dec-POMDPs, with LLM-synthesized policy controllers verified by a solver.** Nobody in this sweep uses a decentralized (non-centralized) optimum as the evaluation ground truth, and nobody uses a model checker or Dec-POMDP solver to *verify* an LLM-synthesized controller. None of the classical Dec-POMDP benchmark domains (Dec-Tiger, Box Pushing, Meeting on a Grid, Broadcast Channel, Mars Rovers, Recycling Robots) turned up in any LLM paper on arXiv, in any search combination tried.

That said, the field is closing in from two directions simultaneously, and the risk is not zero:

1. **Christopher Amato's group (Northeastern)** — a leading Dec-POMDP theorist — has pivoted directly into "LLM collaboration as Dec-POMDP," with two 2026 papers (MAGRPO at AAAI 2026, and a January 2026 follow-up, CoLLM/MAAC) that explicitly frame multi-LLM collaboration as a Dec-POMDP and study centralized-vs-decentralized critics/execution. Neither compares against a computed decentralized-optimal value or verifies policies with a solver — both are RL fine-tuning papers on writing/coding/game tasks, not small finite-horizon benchmark evaluation. But this group has the domain expertise and stated interest to make the jump you're planning; they are the single highest-probability source of a scoop between now and October.
2. **Two independent August 2026 papers** explicitly invoke the Dec-POMDP / macro-action Dec-POMDP framework for LLM multi-agent coordination (see table). Neither computes or benchmarks against a decentralized-optimal solver value; one measures against MARL baselines and human trust ratings, the other against reward/behavioral audits. These indicate the "Dec-POMDP + LLM" framing itself is no longer novel as a framing — the novelty in your proposal has to rest on the solver-verified, optimum-grounded evaluation methodology, not on invoking Dec-POMDPs for LLM teams per se.

**Realistic probability of being scooped outright (the exact combination: decentralized-optimal solver ground truth + LLM policy-controller synthesis + solver/model-checker verification) before/around 8 Oct 2026: low, roughly 10-15%.** Probability that a paper appears using "Dec-POMDP" + "LLM" framing more generally, requiring you to sharpen your differentiation in the related-work section: high, effectively already happening (see table). The Amato group is the wildcard — they publish fast (three related papers in under 8 months) and are exactly positioned to add a decentralized-optimum comparison next.

## Chronological table of most relevant recent work

| Date | Title | Venue/Status | Link | Overlap |
|---|---|---|---|---|
| 2025-08-06 (v7: 2025-12-09) | LLM Collaboration With Multi-Agent Reinforcement Learning (MAGRPO) | AAAI 2026 (accepted) | arxiv.org/abs/2508.04652 | Formalizes multi-LLM collaboration as Dec-POMDP; MARL fine-tuning (MAGRPO), not solver-verified evaluation; benchmarks are writing/coding tasks (TLDR, HumanEval, CoopHumanEval), not classical Dec-POMDP domains; no decentralized-optimal ground truth used. |
| 2026-01-29 (arXiv 2601.21972, listed onward through 2026-05-26) | Learning Decentralized LLM Collaboration with Multi-Agent Actor Critic (CoLLM-CC / CoLLM-DC) | OpenReview (openreview.net/forum?id=Qj8FwWtTuQ) / arXiv | arxiv.org/abs/2601.21972 | Same Amato-lab lineage (Liu, Chen, Amiri, Amato). Compares centralized vs. decentralized critics for LLM MARL fine-tuning across writing/coding/game domains. Still no solver-computed decentralized optimum, no classical Dec-POMDP domains, no policy-verification-by-solver. Closest "adjacent group" risk. |
| 2026-07-07 | LLM Agents for Deliberative Collaboration: A Study on Joint Decision Making Under Partial Observability | arXiv (v1 only, cs.CL/cs.AI) | arxiv.org/abs/2607.06157 | The tracked paper. Partial-observability benchmark scored with mathematical/IP tools vs. centralized baseline. No decentralized optimum. No sequel found (see author-tracking section). |
| 2026-08-02 | Training Small LLMs as Spatial Multi-Agent Policies | arXiv (cs.MA/cs.LG) | arxiv.org/abs/2608.01425 | Explicitly invokes "macro-action Dec-POMDPs" as the multi-agent extension of options/semi-MDP framework for LLM policies-over-options. Trains via per-agent GRPO (PA-MAGRPO); evaluates via reward + behavioral audits, not against a computed decentralized optimum, no solver verification. |
| 2026-08-05 | Structured LLM Reasoning for Zero-Shot Human–Robot Coordination Under Hidden Goals | arXiv (cs.RO/eess.SY) | arxiv.org/abs/2608.04309 | "Guided by a Dec-POMDP formulation" for a human-robot cooperative construction task with private goal views. Compares to an MARL baseline and human trust ratings, not a computed decentralized optimum. Zero-shot LLM architecture, not policy synthesis + solver verification. |

## 2607.06157 author-tracking result

Confirmed author list via arXiv (fetched raw HTML metadata, not the summarizer): **Chenxu Wang, Yongkun Yang, Boyuan Du, Shiwei Lin, Huaping Liu**. Submitted 2026-07-07, v1 only (checked directly on the abstract page — no v2 exists).

Checked each author's full arXiv history via the arXiv API (`export.arxiv.org/api/query`, filtered to cs.MA/cs.AI/cs.LG/cs.CL, sorted by date):

- **Chenxu Wang** — very common name; many results are unrelated (physics, video generation, jailbreak red-teaming, modulation classification). Relevant recent CS work: "Generalizable Agent Modeling for Agent Collaboration-Competition Adaptation" (2025-06-20, cs.MA) predates 2607.06157 and is not a follow-up. Nothing post-July-2026 links back to the deliberative-collaboration benchmark.
- **Yongkun Yang** — only 3 arXiv papers total; the other two (GLM-4.5 tech report as one of dozens of co-authors, and a video causal-testing benchmark) are unrelated. No follow-up.
- **Boyuan Du** — 2607.06157 is the *only* arXiv paper under this name in cs categories. No follow-up.
- **Shiwei Lin** — 2607.06157 is the *only* arXiv paper under this name in cs categories. No follow-up.
- **Huaping Liu** (Tsinghua, senior/PI) — prolific; other 2026 papers are robotics/embodied-AI/RL (world models, UAV navigation, robust RL), unrelated to Dec-POMDP evaluation. No Dec-POMDP or decentralized-optimum work found under his name besides 2607.06157.

**Conclusion: no evidence of a follow-up from this author group as of 2026-09-08.** No decentralized-optimum extension, no sequential-task extension found. This should be re-checked closer to the submission deadline since arXiv indexing can lag by a few days and this group could post a v2 or a new paper at any time.

## Classical Dec-POMDP benchmark domains — used by any LLM paper?

No. Targeted arXiv full-text searches for combinations of "Dec-Tiger," "tiger problem," "Box-Pushing," "Meeting on a Grid," "Broadcast Channel" (decentralized), "Mars Rovers," and "Recycling Robots" together with "LLM" / "large language model" returned **zero relevant hits** in every combination tried. The "Broadcast Channel" search returned only unrelated information-theory/wireless papers. This is a genuinely clean gap: nobody has run LLM agents through the classical finite Dec-POMDP benchmark suite.

## Relevant upcoming venues/deadlines

- **ICLR 2026 Workshop on Multi-Agent Learning and Generative AI** — submission deadline already passed (Feb 5/10, 2026), accepted-papers list live at iclr26-mal-gai.github.io/papers.html — worth a targeted look at that list for decentralized-optimum framings (not yet checked title-by-title in this sweep).
- **WMAC 2026 (AAAI 2026 Bridge Program on Advancing LLM-Based Multi-Agent Collaboration)** — ongoing program, topics include protocols for heterogeneous LLM-agent collaboration.
- **COLM 2026, 2nd Workshop on Lifelong Agents** — submissions closed July 3, 2026, workshop held Oct 9, 2026 — output could surface findings relevant to your topic right around your deadline.
- **NeurIPS 2026 workshops** (announced per NeurIPS blog, Aug 2026) include agentic-systems and decentralized/collaborative foundation-model training workshops — titles not yet individually checked.
- **ICAPS 2026** accepted-papers list (icaps26.icaps-conference.org/program/accepted/) includes Dec-POMDP-adjacent planning work (e.g., "GammaZero: ... belief-space search for long-horizon POMDPs") but nothing found combining this with LLMs.
- AAMAS 2027 CFP/OpenReview page could not be meaningfully queried (no submissions visible yet — see below).

## What could not be accessed / verify again closer to deadline

- **AAMAS 2026 full proceedings table of contents** (ifaamas.org/Proceedings/aamas2026/ and the ACM DL proceedings page, dl.acm.org/doi/proceedings/10.5555/3776572) could not be scraped directly — the ACM DL page returned HTTP 403, and the IFAAMAS page's actual paper listing is on a linked "Table of Contents" page that was not separately fetched. **This is a real gap** — AAMAS is the single most likely venue for exactly this kind of paper and its full accepted-paper list was not exhaustively checked title-by-title. Recommend a manual pass through the AAMAS 2026 table of contents before submission.
- **OpenReview group pages for AAMAS 2026/2027 and ICLR 2027** returned mostly bot/verification pages or empty navigation shells when fetched directly — OpenReview appears to gate/JS-render content in a way WebFetch could not get past. Search-engine-mediated results were used as a fallback where possible (e.g., finding the Amato-lab OpenReview submission via Google indexing), but this is not equivalent to a direct listing sweep.
- **IJCAI 2026 and full NeurIPS 2025/2026 / ICML 2026 proceedings** were checked only via web search, not via direct proceedings index pages — no direct index fetch was performed for these venues.
- ICLR 2026 Workshop MALGAI's accepted-papers page (iclr26-mal-gai.github.io/papers.html) was identified but not opened/read title-by-title.
- arXiv indexing lag means anything posted in the last few days of this search window may not yet be fully searchable via the API.

## Method note

All arXiv facts in this report (titles, authors, dates, abstracts) were pulled from raw arXiv HTML/API responses (`arxiv.org/abs/...` pages and `export.arxiv.org/api/query`), not from WebFetch's summarizer, per the instruction to avoid fabricated summaries on load-bearing facts. Venue/workshop facts came from WebSearch result snippets and were cross-checked against arXiv where a paper was involved; these were not independently opened as raw pages in every case and should be treated as slightly lower-confidence than the arXiv-sourced facts.
