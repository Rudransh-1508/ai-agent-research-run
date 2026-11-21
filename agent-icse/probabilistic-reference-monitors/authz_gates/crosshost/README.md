# Cross-host seam survey

Does each deployed agent harness exhibit the same authorization seams the study measures on
Claude Code? Four harnesses (Qwen Code 0.28.0, Gemini CLI 0.68.0, Goose 1.59.2, Crush 0.100.0)
are driven headless by a scripted model backend (no real model, ToS-clean), each calling its
OWN shell tool with a test command that only touches a throwaway `victim/` dir. "Ran" is read
from the work dir afterwards, never from harness output.

    mkdir -p /tmp/prm-xhost
    python3 crosshost/stub_model.py --port 8765 --state /tmp/prm-xhost/state.json &
    python3 crosshost/survey.py        # -> artifact/crosshost/survey.jsonl

- `stub_model.py` speaks OpenAI chat-completions (stream+non), OpenAI Responses, and Gemini
  generateContent. Turn 1 -> call the shell tool with the command; after a tool result -> stop.
  Tool-less requests (titles/summaries/safety classifiers) are answered per `classifier` in the
  state file: safe / unsafe / http500 / malformed / echo-text.
- `harnesses.py` per-harness adapters (argv, env, config) + approval modes.
- `run_one.py` one run in a fresh work dir; outcome from `victim/data.txt` gone or MARKER_RAN.
- `survey.py` scenarios S1 (mode coupling), S2 (allowlist), S3 (classifier failure).

Gemini needs `GEMINI_CLI_TRUST_WORKSPACE=true` (set in the adapter). Goose supervised modes
refuse headless by design. Results and interpretation: RESULTS_COMPARISON section 24.
