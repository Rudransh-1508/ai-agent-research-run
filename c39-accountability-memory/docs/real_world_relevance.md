# C39 — P4: does the tension occur in systems that actually exist?

**Date:** 2026-09-14
**Scope:** classification of real logging/attribution behaviour only. No theory,
no solver work, no novelty search. Nothing in `research_state.md` modified.

**The test being applied.** PER-AGENT logging (a separate signal per agent,
however coarse) is SAFE — the incentive guarantee survives compression.
AGGREGATE logging (the team collapsed into a summary) is the DANGER ZONE —
individual effort becomes unrecoverable. The theory says the tension bites when
a record discards more than about `log2(n/2)` bits of an n-agent effort profile.

---

## Classification table

| # | System | Group | Class | Evidence | Effort recoverable? |
|---|---|---|---|---|---|
| 1 | **LangSmith / LangGraph** | A, B | **SAFE** | Run = *"A single unit of work executed by an agent, such as calling an LLM, formatting a prompt, or retrieving documents."* Trace = *"A collection of runs for a single operation."* Each step gets its own run with full inputs/outputs. Per-run `usage_metadata` with `input_tokens`/`output_tokens`, and per-run cost. | **Yes** — per-step, with per-step cost |
| 2 | **OpenAI Agents SDK** | A | **SAFE** | *"Tracing is enabled by default."* Span types: `agent_span()` — *"Each time an agent runs, it is wrapped in `agent_span()`"* — plus `generation_span()`, `function_span()`, `handoff_span()`, `guardrail_span()`. | **Yes** — per agent run |
| 3 | **Claude Agent SDK** | A | **SAFE** | Each subagent gets its own transcript file at `<session>/subagents/agent-<id>.jsonl`; every row carries `agentId` and `isSidechain: true`. Meta file records `{"agentType":...,"spawnDepth":...}`. Subagents appear as nested child spans keyed by the `tool_use_id` that spawned them. | **Yes** — per subagent, separate file |
| 4 | **AutoGen (Microsoft)** | A, B | **MIXED** | Schema-level split. `MessageEvent` carries `sender: AgentId \| None` and `receiver: AgentId \| TopicId \| None`. But `LLMCallEvent` fields are exactly `messages`, `response`, `prompt_tokens`, `completion_tokens` — **no agent field**. `ToolCallEvent` is `tool_name`, `arguments`, `result` — **no agent field**. | **Partly** — who talked to whom, yes; who spent what, **no** |
| 5 | **CrewAI** | A, B | **MIXED** | `CrewOutput` keeps `tasks_output`, *"a list of TaskOutput objects, each representing the output of a task"*. But token usage is a single crew-wide summary. Reported behaviour: *"CrewAI agents don't natively expose token counts per agent"*; *"rolling them all into one number means you can't tell which agent drove the cost."* | **Partly** — outputs yes; cost **no** |
| 6 | **Cooperative MARL (Dec-POMDP / SMAC)** | C | **DANGER** | Primary source: *"all agents in a Dec-POMDP share the same team reward function r(s,u): S×U → ℝ"*. The paper names *"multi-agent credit assignment"* as a defining challenge. A whole research literature (QMIX, COMA, value decomposition) exists to undo this collapse. | **No** — single team scalar |
| 7 | **RLHF sequence-level reward** | C | **DANGER** (analogue) | *"a single sequence-level scalar reward provides only coarse supervision over a long generation trajectory, leaving fine-grained credit assignment fundamentally underspecified."* Process/token-level reward models exist specifically to decompose it. | **No** — one scalar per trajectory |
| — | **Agent marketplaces / bounty platforms** | B | **NOT CLASSIFIED** | Searched; found platform-vs-agent revenue splits (80/20, 85/15, 95/5) which are *fee* splits, not multi-contributor attribution. The one architecture describing recursive sub-bounties with per-agent stake/reward is a **proposal**, not a deployed system. No documented attribution scheme obtained. | Unknown |

## Counts

* **Systems investigated: 8**
* **Classified with specific evidence: 7**
* **SAFE: 3** (LangSmith/LangGraph, OpenAI Agents SDK, Claude Agent SDK)
* **MIXED: 2** (AutoGen, CrewAI)
* **DANGER: 2** (cooperative MARL, RLHF sequence reward)
* **Not classifiable on available evidence: 1** (agent marketplaces)

**Every one of the five production agent frameworks checked (Group A) keeps a
per-agent record by default.** None is purely aggregate. This is reported
plainly because it is the result, not because it is convenient.

## The mechanism finding — and it cuts against C39

C39's model assumes a **binding record budget**: the record must be compressed,
and the compression forces a trade between reconstruction and incentives. The
decisive question is therefore not just *what* real systems log, but *what they
do when logging costs too much*. That was checkable, and the answer is
unambiguous:

> LangSmith default retention is 14 days; extended retention costs up to 10x per
> trace. The documented response is **sampling** — `LANGSMITH_TRACING_SAMPLING_RATE`
> between 0 and 1 — and reported practice is that customers *"routinely sample
> down to 0.1% of their actual traces."*

Real budget pressure exists and is severe. But it is resolved by **dropping
whole traces**, not by **summarising within a trace**. A 0.1% sample retains
0.1% of episodes at *full per-agent resolution* and discards the rest entirely.

That is a different compression geometry from the one C39 models. Under
episode-level sampling the retained record stays firmly in the SAFE zone, and
the discarded episodes contribute nothing to settlement at all. **The observed
industry response to a record budget does not produce C39's tension.**

## Strongest single danger-zone example found

**AutoGen's `LLMCallEvent`.** This is the best candidate because it is a
documented API surface, checkable in one page, and it fails on exactly the axis
C39 cares about — effort, not conversation.

AutoGen logs two kinds of thing. Agent-to-agent messages are fully attributed:

    MessageEvent(payload, sender: AgentId | None, receiver: AgentId | TopicId | None,
                 kind, delivery_stage)

But the events that carry the *costly work* are not:

    LLMCallEvent(messages, response, prompt_tokens, completion_tokens)
    ToolCallEvent(tool_name, arguments, result)

Neither carries an agent identifier. So from the default structured log you can
reconstruct **who talked to whom**, but not **who burned the tokens**. The
effort signal is present in aggregate and unattributable per agent — precisely
the collapse the theory says destroys the incentive guarantee.

CrewAI corroborates the same failure on the same axis from the opposite
direction: it *keeps* per-task outputs but *aggregates* token usage crew-wide,
and a third-party product exists specifically to retrofit per-agent billing —
evidence that practitioners hit this and feel it.

**The honest weakness of this example**, which must not be glossed: in both
frameworks the information is *not destroyed*. The per-agent attribution is
recoverable with modest instrumentation (wrap the LLM client, tag by calling
agent), and people do exactly that. These systems aggregate **by default
convenience, not under a storage bound**. C39 models a regime where you *cannot
afford* the per-agent record. AutoGen and CrewAI could afford it trivially and
simply do not bother. That is a meaningfully weaker claim than C39 needs.

## VERDICT: STAKES UNCLEAR

The evidence found **points toward STAKES ABSENT**, and that lean should not be
softened:

* All 5 production agent frameworks log per-agent by default (3 fully SAFE,
  2 MIXED only on the cost axis, both cheaply fixable).
* Where a real record budget bites, the industry response is episode sampling,
  which *preserves* per-agent resolution in what it keeps.
* The 2 genuine DANGER cases are both in **training**, not deferred settlement,
  and neither arises from a record budget. MARL's shared team reward is a
  property of the *environment* — the per-agent signal never existed to be
  discarded — so it exhibits C39's consequence without C39's mechanism. RLHF's
  contributors are tokens and steps, not agents at all.

It is recorded as UNCLEAR rather than ABSENT for one specific reason: **the
setting C39 actually targets — a deployed system that pays multiple agents from
a bounded shared record — produced zero checkable instances.** Agent
marketplaces are the right place to look and they exist, but no attribution
scheme could be documented; what surfaced were platform fee splits and
proposals. "Nobody operates in this regime" is therefore not a claim the
evidence supports; "nobody I could check operates in it, and the nearest
analogues do not" is.

Per the standing rule, this is **not** upgraded to CONFIRMED on the strength of
AutoGen's schema alone.

### Exactly what is missing

1. **A deployed multi-agent payment system** where several agents contribute to
   one task, settlement happens after the fact, and the retained record is
   genuinely bounded. Marketplace platforms (BountyBook, TaskBounty, gigs.sh and
   similar) are the candidates; what is needed is their actual attribution
   scheme or trace schema, not their fee split.
2. **Evidence of within-episode summarisation under a real budget** — any
   production system that compresses a multi-agent trace by aggregating across
   agents rather than by dropping episodes. Nothing found does this.
3. **Whether AutoGen/CrewAI aggregation ever becomes load-bearing** — i.e. a
   case where settlement actually used the aggregate and per-agent recovery was
   not performed. Currently the aggregation is a default, not a constraint.

### What would settle it

Obtaining the trace/attribution schema of one operating agent marketplace that
pays multiple contributors per task. If it attributes per contributor, the
verdict is ABSENT and C39's engineering case does not exist as posed. If it
settles from a bounded aggregate, the verdict is CONFIRMED and that platform is
the motivating example.

### Consequence for C39

This does not touch the mathematics, which stands. It bears on §4 of
`research_state.md`, which already concluded that the engineering case "turns
entirely on whether real records keep per-agent resolution or aggregate it."
The answer, for everything checkable here: **they keep per-agent resolution**,
and when they cannot afford to, they drop whole episodes rather than aggregate.
P4 remains C39's main exposure and this session did not reduce it.
