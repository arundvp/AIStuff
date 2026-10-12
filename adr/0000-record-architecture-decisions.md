# ADR-000: Record architecture decisions

- Status: accepted
- Date: 2026-10-11

## Context

Decisions made early in this application, such as the canonical model, domain boundaries and how the router picks sub-agents, constrain everything built after them. The reasons behind them fade quickly, and AI coding assistants will happily suggest reversing a choice without knowing why it was made.

## Options considered

1. No record: fast now, but the reasons are lost.
2. A wiki or notes app: easy to write, but it drifts away from the code.
3. ADRs as Markdown in the repo: reviewed and versioned with the code they explain.

## Decision

Keep ADRs in `adr/`, numbered, one file per decision, copied from [template.md](template.md). Write one whenever a choice is hard to reverse or affects more than one component, and whenever a principle is broken on purpose. Never edit an accepted ADR; supersede it with a new one.

## Trade-offs

About 15 minutes of writing per decision.

## What would change this decision

If ADRs stop being read before related changes are made, the practice has failed and needs a lighter format, not more ADRs. If writing one regularly takes longer than the decision is worth, shrink the template rather than drop the practice. If the application moves to a team that keeps decisions in a different tool, migrate as long as decisions stay versioned and linked to the code.
