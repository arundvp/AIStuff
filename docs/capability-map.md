# Capability map

What the application does, independent of how it does it. Level 1 is six areas; Level 2 breaks each one into its parts. Services, models and frameworks will change; these capabilities should not.

## Capabilities

| L1 | L2 capabilities | Example question | Sub-agents | Router intents |
| --- | --- | --- | --- | --- |
| Discover | Product search · Recommendations · Product Q&A | "Show me waterproof running shoes under $80" | Product | `product_search` |
| Decide | Stock by location · Delivery promise · Store policy answers | "Red shoes to Boston in 2 days?" | Inventory, Fulfillment | `stock_check`, `delivery_promise`, `store_policy` |
| Buy | Cart · Checkout · Payment (test mode) · Order confirmation | "Buy the red pair in size 9 and ship it to Boston" | Checkout | none yet (see gaps) |
| Fulfil | Warehouse allocation · Shipping and carriers · Shipment tracking · Delivery exceptions | "Has order 48213 shipped yet?" | Fulfillment, Order | `order_status` |
| Serve | Returns and refunds · Cancellations · Account and preferences · Consent | "I want to return the jacket from order A-1009" | Order, Customer | `returns`, `account` |
| Operate | Platform health · Data freshness · Cost per conversation · Incident explanation | Staff: "Why is checkout slow?" | Ops | `platform_health` |

## Sub-agent ownership

Each sub-agent fronts one domain and is the only writer of that domain's data (principle P2). Anything that changes an order, an account or money waits for human approval (principle P4).

| Sub-agent | Owns | Home capability | Access |
| --- | --- | --- | --- |
| Product | Catalog: products, attributes, descriptions, reviews | Discover | Read-only |
| Inventory | Stock levels by warehouse | Decide | Read-only |
| Fulfillment | Warehouses, carriers, transit times, shipments | Fulfil | Read-only |
| Order | Orders and their status history | Serve | Reads freely; cancellations and returns need approval |
| Customer | Accounts, preferences, consent | Serve | Reads only with consent; changes need approval |
| Checkout | Carts and checkout sessions | Buy | Every purchase needs the shopper's confirmation |
| Ops | Nothing: reads the platform's telemetry | Operate | Read-only; never changes the platform |

## Gaps and overlaps

- **Buy has no router intent.** A shopper can't yet say "buy this", so nothing reaches the Checkout sub-agent. It needs a purchase intent, and because buying moves money, P4 applies.
- **Cancellations have no intent of their own.** "Cancel order A-1009" would land in `order_status` or `returns`. A separate cancel intent keeps the approval path explicit.
- **Store policy has no owning sub-agent.** Return, shipping and warranty policies are documents, not records in any domain. Either add a Policy sub-agent over the policy documents, or let the router answer from a policy search tool directly. Decide in an ADR.
- **`other` is not a capability.** The current router's catch-all `other` takes returns, account, policy and platform questions. Split it into the intents above so each question lands in exactly one capability, and keep `other` only for out-of-scope questions.
- **Fulfillment appears in Decide and Fulfil, and Order in Fulfil and Serve.** Not a conflict: each still owns one set of data. Different capabilities simply read it.
