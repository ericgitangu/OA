# Architectural Patterns Quick Reference

14 patterns across 7 tiers. Each pattern is introduced where it emerges organically from the problem domain.

## Tier 1 — Systems (Rust, C++) — Weeks 1-2

| # | Pattern | Core Idea | Project |
|---|---------|-----------|---------|
| 1 | **Event-Driven Architecture** | Components communicate via async events, not direct calls. Enables back-pressure, replay, audit trails. | Sauti |
| 2 | **BFF (Backend-for-Frontend)** | Dedicated backend per client type. Agent, supervisor, and partner APIs each get tailored backends. | Sauti |
| 3 | **Zero-Copy / Shared-Nothing** | Data moves through pipelines without copying. FFI boundary between Rust and C++ DSP using `Vec<u8>` buffers. | Sauti / LendStream |

## Tier 2 — JVM (Java, Kotlin, Scala) — Weeks 3-4

| # | Pattern | Core Idea | Project |
|---|---------|-----------|---------|
| 4 | **CQRS** | Separate read and write models. Write side optimized for consistency, read side for queries. | LendStream v2 |
| 5 | **Event Sourcing** | Store events, not state. Current state derived by replaying events. Enables temporal queries. | LendStream v2 |
| 6 | **Saga Orchestration** | Coordinate multi-service transactions via a central orchestrator emitting compensating actions on failure. | LendStream v2 |
| 7 | **Hexagonal Architecture** | Ports and adapters. Domain logic isolated from infrastructure. Swap databases, APIs without touching core. | Unicorns v2 |

## Tier 3 — Web (JS, TS) — Weeks 5-6

| # | Pattern | Core Idea | Project |
|---|---------|-----------|---------|
| 8 | **Micro-Frontends** | Independent, deployable UI fragments composed at runtime. Each team owns a vertical slice. | Sherehe |
| 9 | **Server Components** | Server-rendered React components that stream HTML. Reduces client bundle, improves TTFB. | Sherehe |
| 10 | **Edge Functions** | Compute at CDN edge nodes. Sub-50ms latency for personalization, A/B testing, auth. | Sherehe |

## Tier 4 — Concurrent (Go, Zig) — Weeks 7-8

| # | Pattern | Core Idea | Project |
|---|---------|-----------|---------|
| 11 | **Fan-Out/Fan-In** | Distribute work across goroutines, collect results. Channel-based coordination. | Shamba |
| 12 | **Pipeline** | Chain processing stages connected by channels. Each stage is concurrent and independent. | Shamba |

## Tier 5a — Scripting (Ruby, PHP, Elixir) — Weeks 9-10

| # | Pattern | Core Idea | Project |
|---|---------|-----------|---------|
| 13 | **OTP Supervision Trees** | Erlang/Elixir process hierarchy. Supervisors restart failed children. "Let it crash" philosophy. | BSD Engine v2 |

## Tier 6 — .NET (C#, F#) — Weeks 13-14

| # | Pattern | Core Idea | Project |
|---|---------|-----------|---------|
| 14 | **Clean Architecture** | Dependency inversion at every layer. Domain at center, frameworks at edges. ADTs via discriminated unions in F#. | PayGoHub v2 |

## Pattern Relationships

```
Event-Driven ──► CQRS ──► Event Sourcing
     │                         │
     ▼                         ▼
   BFF ──► Micro-Frontends   Saga Orchestration
     │
     ▼
Zero-Copy ──► Pipeline ──► Fan-Out/Fan-In
```

Each tier builds on the previous. Event-driven thinking (Tier 1) becomes the substrate for CQRS (Tier 2), which enables event sourcing. BFF (Tier 1) evolves into micro-frontends (Tier 3).
