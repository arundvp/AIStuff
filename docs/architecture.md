# Architecture

Six layers, each built from free and open-source parts. A router agent answers each question through domain sub-agents that share one canonical commerce model. See the [vision](vision.md), [principles](principles.md) and [capability map](capability-map.md).

```mermaid
flowchart TB
    q(["Shopper or staff question<br/>'Red shoes to Boston in 2 days?'"])

    subgraph L1["1 · Ask and route"]
        router["Router agent<br/>intent + details → plan"]
        agents["Sub-agents<br/>Product · Inventory · Order · Fulfillment<br/>Customer · Ops · Checkout"]
    end

    approval{{"Human approval<br/>(writes only)"}}

    subgraph L2["2 · Agent fabric"]
        fabric["agentgateway · LiteLLM<br/>Agent Card registry · Kafka broker"]
    end

    subgraph L3["3 · Bounded domains"]
        domains["Product · Inventory · Order services<br/>PostgreSQL · Cassandra · Valkey"]
    end

    subgraph L4["4 · Evidence pipeline"]
        pipeline["Kafka + Debezium → Iceberg on SeaweedFS<br/>Spark + dbt Core → gold data products"]
    end

    subgraph L5["5 · Projections: one meaning, many views"]
        views["pgvector · Qdrant · Oracle AI Vector Search<br/>Apache AGE · DuckDB · BigQuery"]
    end

    canon[("Canonical Commerce Model<br/>Customer · Product · Order · Inventory<br/>Decision + Evidence")]

    subgraph L6["6 · Controls (apply to every layer)"]
        controls["Ownership · contracts · freshness<br/>security + consent · lineage + audit<br/>cost + continuity"]
    end

    q --> router
    router -- "plan: which sub-agents, in what order" --> agents
    agents -- "reads: tool and model calls" --> fabric
    agents -- "writes" --> approval
    approval -- "confirmed" --> fabric
    fabric --> domains
    fabric --> views
    domains -- "change events (CDC)" --> pipeline
    pipeline -- "gold data products" --> views
    canon -.- domains
    canon -.- views
    agents -- "answer + cited evidence" --> q
```

## How a question flows

The router turns the question into intents and details ("red shoes", "Boston", "2 days") and plans which sub-agents to call, in what order. Each sub-agent reaches data only through the agent fabric, which handles identity, model access and tracing: live records come from the domain services, and search, analytics and graph questions go to the projections. Every change in a domain flows as an event through the evidence pipeline into gold data products, which keep the projections current. All of it speaks the canonical model, so "in stock" means the same thing everywhere. The router merges the sub-agents' results into one answer that cites its evidence, and any action that changes an order, an account or money stops for human approval first.

## Where the principles apply

| Principle | Where it shows in the diagram |
| --- | --- |
| P1 One canonical meaning | The canonical model, shared by domains and projections |
| P2 One owner per data product | Each domain service writes only its own data; others read through the fabric or the projections |
| P3 Every answer cites evidence | The "answer + cited evidence" arrow back to the question |
| P4 No write without human approval | The approval step on the write path |
| P5 Measure before you trust | Evals on the router and sub-agents, enforced by the controls layer |
