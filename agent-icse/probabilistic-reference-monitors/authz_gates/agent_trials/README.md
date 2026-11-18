# Real-agent trials

Does a helpful agent route around a gate's denial? Real Claude Code (`claude -p`, the account's
default model) on four ordinary tasks that need a deletion or reset (delete stale build dirs,
discard uncommitted changes, remove a vendored SDK, delete a merged branch), one gate per
condition (dcg; cc-safety-net 2.7.15 on the git tasks, since it allows project-local `rm -rf`
by design), two host modes (acceptEdits: the host still prompts; bypassPermissions: the gate
is the only check), 2 reps each. User settings excluded; Bash in Claude Code's strict sandbox.
Prompts are the task alone. Outcome is read from the project's filesystem/git state.

    python3 agent_trials/run_trials.py --gate dcg --reps 2 [--mode bypass]   # or run_all.sh / run_bypass.sh
    python3 agent_trials/classify.py      # -> artifact/agent-trials/TRIALS.md, trials.json
Transcripts: artifact/agent-trials/*.stream.jsonl. Throwaway projects: ~/prm-agent-trials/.
