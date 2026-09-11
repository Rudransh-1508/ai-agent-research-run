"""
Reproduction of microsoft/agent-framework issue #8140: AG-UI resume
duplicates the interrupted turn when the client replays its transcript.

Mechanism, confirmed by reading the actual installed agent_framework_ag_ui
1.3.0 package: both the buggy path and the correct path already exist side
by side in the SAME installed version --

- `ThreadSnapshotSession.resume_seeded_messages` (_snapshot_session.py:134)
  naively concatenates stored history with whatever the client sent, with
  no overlap detection at all.
- `_reconstruct_messages_from_thread_snapshot` (_run_common.py:1350) already
  exists in the same package, and IS used by a sibling branch (the
  "client re-sent history" defence) -- it detects the overlap between stored
  and incoming messages and trims the duplicate.

The defect (per the issue and PR #8149, both fetched fresh, unmerged as of
this record) is that the AG-UI *resume* branch in `_agent_run.py` calls the
naive `resume_seeded_messages` instead of the reconciler, when the client
(the reference AG-UI client, by default) replays its full transcript on
resume. This script demonstrates the divergence directly, without needing
to patch anything -- both functions already exist unpatched in 1.3.0; only
which one gets *called* for this code path is the bug.

"embedded" has no equivalent for this defect: "resume with a replayed
transcript" is a hosted-protocol concept with no in-process analogue (an
embedded/direct SDK call has no thread snapshot, no resume payload, and no
client to replay anything). This is stated explicitly rather than forced
into the embedded/served grid.
"""

import json

from agent_framework_ag_ui._run_common import _reconstruct_messages_from_thread_snapshot
from agent_framework_ag_ui._snapshot_session import ThreadSnapshotSession
from agent_framework_ag_ui._snapshots import AGUIThreadSnapshot

# The stored thread snapshot after an interrupted turn: one user message, one
# assistant tool-call awaiting approval.
STORED_MESSAGES = [
    {"id": "msg-user-1", "role": "user", "content": "please transfer $100"},
    {
        "id": "msg-assistant-1",
        "role": "assistant",
        "toolCalls": [{"id": "call-1", "type": "function", "function": {"name": "transfer_funds", "arguments": "{}"}}],
    },
]

# The reference AG-UI client's default behavior on resume: replay the full
# transcript it already has (per the issue: "the reference TypeScript client
# sends the full transcript... there is no resume-aware trimming anywhere on
# that path").
CLIENT_REPLAYED_TRANSCRIPT = [dict(m) for m in STORED_MESSAGES]


def defective_resume_path(stored: list[dict], incoming: list[dict]) -> list[dict]:
    """What agent_framework_ag_ui/_agent_run.py's resume branch actually calls
    in 1.3.0 for a non-service-session resume with a stored pending-approval
    interrupt: ThreadSnapshotSession.resume_seeded_messages -- naive concat."""
    snapshot = AGUIThreadSnapshot(messages=stored)
    session = ThreadSnapshotSession(store=None, scope=None, thread_id="t1", stored=snapshot)
    return session.resume_seeded_messages(incoming)


def corrected_resume_path(stored: list[dict], incoming: list[dict]) -> list[dict]:
    """What PR #8149 routes this branch through instead: the reconciler
    already used by the sibling ('client re-sent history') branch."""
    return _reconstruct_messages_from_thread_snapshot(
        stored_messages=stored,
        incoming_messages=incoming,
        stored_interrupt=None,
    )


def count_by_id(messages: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for m in messages:
        mid = m.get("id", "<no-id>")
        counts[mid] = counts.get(mid, 0) + 1
    return counts


def main():
    defective_result = defective_resume_path(STORED_MESSAGES, CLIENT_REPLAYED_TRANSCRIPT)
    corrected_result = corrected_resume_path(STORED_MESSAGES, CLIENT_REPLAYED_TRANSCRIPT)

    defective_counts = count_by_id(defective_result)
    corrected_counts = count_by_id(corrected_result)

    # Contract: resuming with a client-replayed transcript that already
    # overlaps stored history must not duplicate any message id in the
    # snapshot that gets persisted.
    defective_pass = all(c == 1 for c in defective_counts.values())
    corrected_pass = all(c == 1 for c in corrected_counts.values())

    print(
        json.dumps(
            {
                "defective_path (resume_seeded_messages, what 1.3.0 actually calls)": {
                    "message_count": len(defective_result),
                    "counts_by_id": defective_counts,
                    "pass": defective_pass,
                },
                "corrected_path (_reconstruct_messages_from_thread_snapshot, what PR #8149 routes to)": {
                    "message_count": len(corrected_result),
                    "counts_by_id": corrected_counts,
                    "pass": corrected_pass,
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
