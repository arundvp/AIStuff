# Vision: Open Commerce Agents

A multi-agent sample commerce application. A router agent reads each question, calls the sub-agents that own each domain (Product, Inventory, Order, Fulfillment, Customer, Ops, Checkout), and merges their answers with evidence.

## Vision statement

For engineers at mid-size online retailers who want shopping agents they can trust, Open Commerce Agents is an open-source sample application that shows how a router agent and domain sub-agents answer shopping questions from one canonical commerce model. Unlike closed agent platforms, it runs on free, open-source tools and cites the evidence behind every answer.

## Problem

A shopper asks "Red shoes to Boston in 2 days?", and answering needs product, stock and delivery data at once. That data sits in separate systems with different IDs and meanings, so chatbots answer from one source, guess the rest, and promise what the warehouse can't deliver. The retailer pays in cancellations, support tickets and lost trust, or spends months wiring data together first.

## Stakeholders and their concerns

| Stakeholder | What they want | What worries them |
| --- | --- | --- |
| Shopper | A correct answer in one message | A confident promise that turns out wrong |
| Store staff | Order, stock and platform answers in one place | An agent that cancels or refunds on its own |
| Engineers adopting the sample | A reference they can run and copy | Hidden glue, paid dependencies, unmeasured quality |
| Builder and operator (me) | All 15 target skills, and a possible product | Scope creep, surprise costs, a VM out of memory |

## Scenarios it must handle

1. "Red shoes to Boston in 2 days?" (product search + delivery promise)
2. "Do you have the black rain jacket in size M?" (stock check)
3. "Where is my order 48213?" (order status)
4. "Cancel order A-1009." (a write: needs human approval)
5. Staff: "Why is checkout slow?" (platform health, from telemetry)

## Goals for Jan 3, 2027

- The router picks the right sub-agents on a golden set, gated in CI (draft target 90%+, to be fixed in the non-functional requirements).
- A 40-question multi-domain eval passes: every answer cites evidence, and the assistant declines when evidence is missing.
- No cancel, refund or checkout runs without human approval, proven by a test.
- The full stack starts with one command and costs $0 a month outside trial credits.
- Published under Apache 2.0 with docs, ADRs and a 3-minute demo.

## Constraints

- Free and open-source tools only; synthetic data only.
- Runs on an OCI Always Free Arm VM (2 OCPUs, 10 GiB RAM) plus free cloud tiers.
- One builder, 60–90 minutes on weekdays.

## Out of scope

- Real payments (test mode only) and real customer data.
- Production hosting for real stores.
- Training models from scratch.
