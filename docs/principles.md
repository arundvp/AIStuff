# Architecture principles

These rules apply to every service, sub-agent and data pipeline in this application. Each one answers a worry from the [vision](vision.md) and names what will catch a violation.

| ID | Name | Answers this worry from the vision |
| --- | --- | --- |
| P1 | One canonical meaning | Shopper: a confident promise that turns out wrong |
| P2 | One owner per data product | Engineers: hidden glue code |
| P3 | Every answer cites evidence | Shopper: a confident promise that turns out wrong |
| P4 | No write without human approval | Store staff: an agent that cancels or refunds on its own |
| P5 | Measure before you trust | Engineers: unmeasured quality |

## P1 · One canonical meaning

- **Statement:** Every customer, product, order, inventory record and decision has one definition and one stable ID, shared by every service and agent.
- **Rationale:** The router merges answers from several domains. If "in stock" means one thing to Inventory and another to Fulfillment, the shopper gets a confident, wrong delivery promise.
- **Implications:** Services translate to the canonical model at their edges. A new field changes the model first, and agents never invent their own field names. It costs up-front design and slower schema changes.
- **Checked by:** contract tests in CI that validate every service's inputs and outputs against the canonical schema.

## P2 · One owner per data product

- **Statement:** Each data product has exactly one owning service. Only the owner writes it; everything else reads it through the owner's API, events or published contract.
- **Rationale:** When two components write the same stock figure, nobody can say which value is true or who fixes it when it is wrong. One owner makes every number traceable to the one component that answers for it.
- **Implications:** Services never share database tables. Cross-domain needs go through APIs or events, and each data product lists its owner in a catalog. It costs more APIs and events than one shared database, plus some copied read models.
- **Checked by:** a separate database schema and credentials for each service, so no other service can write its data, and an owner recorded for every data product in the catalog.

## P3 · Every answer cites evidence

- **Statement:** Every answer names the records, documents or measurements it relied on. With no evidence, the assistant says it does not know.
- **Rationale:** Shoppers act on answers: they buy and they wait for deliveries. A cited answer can be checked and replayed; an uncited one is a guess that looks like a fact.
- **Implications:** Sub-agents return evidence with every result, and the router merges evidence, not just text. Every run logs its prompt version, model, sub-agents called and evidence used. "I don't know" is a valid, tested outcome. It costs bigger responses and logs, and extra eval work.
- **Checked by:** evals that fail any answer without citations and any answer given when evidence is missing; a decision and evidence log that can replay any answer; and a groundedness objective on live traffic.

## P4 · No write without human approval

- **Statement:** No agent changes an order, an account or money until a person with authority for that action has seen the exact change and confirmed it. Agents get read-only access by default.
- **Rationale:** A wrong answer costs a follow-up question; a wrong cancellation or refund costs money and trust, and may not be reversible. Text hidden in a product review can trick a language model, so a model must never hold write power alone.
- **Implications:** Write tools are separate from read tools and always pass through an approval step, which is logged with its evidence. Agents that query data use read-only credentials and an allow-list of queries. It costs an extra step for shoppers and staff, and slower bulk changes.
- **Checked by:** tests that call every write tool without approval and expect a refusal; read-only credentials for every querying agent; and prompt-injection red-team tests in CI.

## P5 · Measure before you trust

- **Statement:** A change to a prompt, model, retrieval setting or routing rule is done only when it passes the eval set for the part it changes, and its score is recorded.
- **Rationale:** An AI change that looks better on three examples often gets worse on fifty. Recorded scores turn "which model or prompt is better?" from an opinion into a comparison, and catch regressions before shoppers see them.
- **Implications:** Each AI component has a golden set and a one-command scorecard, and CI fails when a score drops below its target. It costs ongoing time to build and maintain eval sets, and makes merges slower.
- **Checked by:** a golden set and scorecard for every AI component; CI gates that fail the build when a score drops below its target; and releases rolled out gradually, gated on eval scores.

## When principles conflict

- P4 wins over everything else: an approval step is never removed for speed or convenience.
- P3 wins over latency and cost: a slower answer with evidence beats a fast guess.
- To break any principle, write an ADR that names the principle, the reason and when the exception ends. Never break one silently.
