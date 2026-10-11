# Build log

## Day 1 — Set up the workspace and a shopping-question CLI — 2026-10-10
- Built: uv project, OCI Arm VM (2 OCPU, 10 GiB, OL 9.8) with Docker and Ollama, SSH tunnel, and `uv run ask` extracting intents + details as schema-constrained JSON from qwen3.5:2b and 4b. Baseline on 10 questions: both 5/10; median 8.6 s (2b) vs 15.7 s (4b).
- Qwen 3.5 "thinks" by default (slow) — turned off with think=False. 2b put an intent name in `category`: field descriptions never reach the model unless the schema is in the prompt.
- Can now explain: structured outputs constrain which tokens the model may write, so the output always parses, but they don't teach the model what fields mean; and for a router, a missed intent is worse than an extra one.