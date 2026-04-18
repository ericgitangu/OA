# OA — Monk Mode: 15-Week Polyglot Architectural Mastery Sprint

[![CI](https://github.com/ericgitangu/OA/actions/workflows/ci.yml/badge.svg?branch=zen)](https://github.com/ericgitangu/OA/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<!-- Tier 0 — Python -->
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
<!-- Tier 1 — Systems -->
![Rust](https://img.shields.io/badge/Rust-1.92-000000?logo=rust&logoColor=white)
![C++](https://img.shields.io/badge/C++-20/23-00599C?logo=cplusplus&logoColor=white)
<!-- Tier 2 — JVM -->
![Java](https://img.shields.io/badge/Java-21-ED8B00?logo=openjdk&logoColor=white)
![Kotlin](https://img.shields.io/badge/Kotlin-2.3-7F52FF?logo=kotlin&logoColor=white)
![Scala](https://img.shields.io/badge/Scala-3.8-DC322F?logo=scala&logoColor=white)
<!-- Tier 3 — Web -->
![JavaScript](https://img.shields.io/badge/JavaScript-ES2024-F7DF1E?logo=javascript&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-6.0-3178C6?logo=typescript&logoColor=white)
<!-- Tier 4 — Concurrent -->
![Go](https://img.shields.io/badge/Go-1.25-00ADD8?logo=go&logoColor=white)
![Zig](https://img.shields.io/badge/Zig-0.15-F7A41D?logo=zig&logoColor=white)
<!-- Tier 5a — Scripting -->
![Ruby](https://img.shields.io/badge/Ruby-3.3-CC342D?logo=ruby&logoColor=white)
![PHP](https://img.shields.io/badge/PHP-8.5-777BB4?logo=php&logoColor=white)
![Elixir](https://img.shields.io/badge/Elixir-1.19-4B275F?logo=elixir&logoColor=white)
<!-- Tier 5b — Lisp -->
![Clojure](https://img.shields.io/badge/Clojure-1.12-5881D8?logo=clojure&logoColor=white)
<!-- Tier 6 — .NET -->
![C#](https://img.shields.io/badge/C%23-10.0-512BD4?logo=dotnet&logoColor=white)
![F#](https://img.shields.io/badge/F%23-10.0-378BBA?logo=dotnet&logoColor=white)

<!-- Tooling -->
![Docker](https://img.shields.io/badge/Docker-29.3-2496ED?logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?logo=githubactions&logoColor=white)
![CMake](https://img.shields.io/badge/CMake-3.20+-064F8C?logo=cmake&logoColor=white)
![Cargo](https://img.shields.io/badge/Cargo-Rust_Build-000000?logo=rust&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-24-339933?logo=nodedotjs&logoColor=white)

<!-- Architecture -->
![Event-Driven](https://img.shields.io/badge/Pattern-Event--Driven-blueviolet)
![BFF](https://img.shields.io/badge/Pattern-BFF-blueviolet)
![CQRS](https://img.shields.io/badge/Pattern-CQRS-blueviolet)
![Hexagonal](https://img.shields.io/badge/Pattern-Hexagonal-blueviolet)
![Clean Architecture](https://img.shields.io/badge/Pattern-Clean_Architecture-blueviolet)
![Micro-Frontends](https://img.shields.io/badge/Pattern-Micro--Frontends-blueviolet)
![OTP](https://img.shields.io/badge/Pattern-OTP_Supervision-blueviolet)
![Fan-Out/Fan-In](https://img.shields.io/badge/Pattern-Fan--Out%2FFan--In-blueviolet)

**Start:** 2026-04-20 | **End:** 2026-08-02 | **Languages:** 16 | **Patterns:** 14

Solve in Python first. Reimplement in paired language groups. Ship a production-grade Saturday project every tier.

## Sprint Status

| Weeks | Tier | Languages | Patterns | Status |
|-------|------|-----------|----------|--------|
| 1-2 | [Tier 1 — Systems](tier_1_systems/) | Rust, C++ | Event-Driven, BFF, Zero-Copy | Upcoming |
| 3-4 | [Tier 2 — JVM](tier_2_jvm/) | Java, Kotlin, Scala | CQRS, Event Sourcing, Saga, Hexagonal | Planned |
| 5-6 | [Tier 3 — Web](tier_3_web/) | JS, TS | Micro-Frontends, Server Components, Edge | Planned |
| 7-8 | [Tier 4 — Concurrent](tier_4_concurrent/) | Go, Zig | Fan-Out/Fan-In, Pipeline | Planned |
| 9-10 | [Tier 5a — Scripting](tier_5a_scripting/) | Ruby, PHP, Elixir | OTP Supervision Trees | Planned |
| 11-12 | [Tier 5b — Lisp](tier_5b_lisp/) | Clojure | Immutable-First, Transducers | Planned |
| 13-14 | [Tier 6 — .NET](tier_6_dotnet/) | C#, F# | Clean Architecture, ADTs | Planned |
| 15 | Buffer | All | Review & polish | Planned |

## Quick Links

| Doc | Description |
|-----|-------------|
| [Sprint Overview](docs/sprint_overview.md) | Full tier breakdown, language pairings, philosophy |
| [Daily Schedule](docs/daily_schedule.md) | 3:30-8:00 AM routine + zazen instructions |
| [Progress Tracker](docs/progress_tracker.md) | Weekly checkbox tracker |
| [Architectural Patterns](docs/architectural_patterns.md) | 14-pattern quick reference with tier mapping |
| [Learning Resources](docs/learning_resources.md) | Curated resources for all 16 languages |
| [Claude Code Strategy](docs/claude_code_strategy.md) | Agent setup, workflows, and best practices |
| [CP Routine](tier_0_python/cp_routine.md) | Original 4AM competitive programming routine |
| [DSA Reference](tier_0_python/dsa_reference.md) | 4,125-line data structures & algorithms guide |

## Saturday Projects

| # | Project | Languages | Patterns | PRD |
|---|---------|-----------|----------|-----|
| 1 | [Sauti](projects/sauti/) | Rust, C++ | Event-Driven, BFF, Zero-Copy | [PRD](docs/projects/01_sauti.md) |
| 2 | [LendStream v2](projects/lendstream_v2/) | Java, Kotlin | CQRS, Event Sourcing, Saga | [PRD](docs/projects/02_lendstream_v2.md) |
| 3 | [Sherehe](projects/sherehe/) | TypeScript | Micro-Frontends, Server Components | [PRD](docs/projects/03_sherehe.md) |
| 4 | [Unicorns v2](projects/unicorns_v2/) | Kotlin, Scala | Hexagonal Architecture | [PRD](docs/projects/04_unicorns_v2.md) |
| 5 | [Shamba](projects/shamba/) | Go | Fan-Out/Fan-In, Pipeline | [PRD](docs/projects/05_shamba.md) |
| 6 | [BSD Engine v2](projects/bsd_engine_v2/) | Elixir | OTP Supervision Trees | [PRD](docs/projects/06_bsd_engine_v2.md) |
| 7 | [PayGoHub v2](projects/paygohub_v2/) | C#, F# | Clean Architecture | [PRD](docs/projects/07_paygohub_v2.md) |

## LeetCode

Organized by [pattern](leetcode/), not language. Solutions sit side-by-side for cross-language comparison:

```text
leetcode/two_pointers/valid_palindrome.py
leetcode/two_pointers/valid_palindrome.rs
```

13 pattern directories: arrays & hashing, two pointers, sliding window, stacks & queues, linked lists, trees & tries, graphs, dynamic programming, greedy, backtracking, bit manipulation, intervals, math & geometry.

## Tooling

| Tool | Version | Status |
|------|---------|--------|
| Python | 3.12 | Installed |
| Rust | 1.92 | Installed |
| Go | 1.25 | Installed |
| Java | 21 | Installed |
| Node.js | 24 | Installed |
| Ruby | 3.3 | Installed |
| Zig | 0.15 | Installed |
| Docker | 29.3 | Installed |
| C++ (clang) | Xcode CLT | Installed |
| Kotlin | 2.3 | Installed |
| Scala | 3.8 | Installed |
| TypeScript | 6.0 | Installed |
| PHP | 8.5 | Installed |
| Elixir | 1.19 | Installed |
| Clojure | 1.12 | Installed |
| .NET | 10.0 | Installed |

## Language Samples

Each tier includes a fundamentals sample demonstrating core language idioms.

| Language | Description | Run |
|----------|-------------|-----|
| Python | Async, collections, data classes, functools via stdlib | `python tier_0_python/dsa/samples/python_fundamentals.py` |
| Rust | Ownership, borrowing, concurrency through variables and threading | `rustc tier_1_systems/rust/samples/rust_fundamentals.rs -o /tmp/rust_fund && /tmp/rust_fund` |
| C++ | Modern C++20 containers, memory management, threading | `cd tier_1_systems/cpp && cmake -B build && cmake --build build && ./build/cpp_fundamentals` |
| Java | Records, sealed classes, streams, lambdas (Java 21) | `java tier_2_jvm/java/samples/JavaFundamentals.java` |
| Kotlin | Sealed classes, data classes, ADTs | `kotlin tier_2_jvm/kotlin/samples/KotlinFundamentals.kt` |
| Scala | Sealed traits, case classes, functional pattern matching | `scala tier_2_jvm/scala/samples/ScalaFundamentals.scala` |
| JavaScript | Lexical scoping, destructuring, iterables | `node tier_3_web/javascript/samples/js_fundamentals.js` |
| TypeScript | Structural typing, interfaces, type safety | `tsc tier_3_web/typescript/samples/ts_fundamentals.ts && node tier_3_web/typescript/samples/ts_fundamentals.js` |
| Go | Constants, iota enums, goroutines, channels | `go run tier_4_concurrent/go/samples/go_fundamentals.go` |
| Zig | Explicit conversions, optionals, error unions, no hidden control flow | `zig run tier_4_concurrent/zig/samples/zig_fundamentals.zig` |
| Ruby | Duck typing, everything-is-an-object, singleton classes | `ruby tier_5a_scripting/ruby/samples/ruby_fundamentals.rb` |
| PHP | Type safety, enums, fibers (PHP 8.1+) | `php tier_5a_scripting/php/samples/php_fundamentals.php` |
| Elixir | BEAM concurrency, immutability, structural types | `elixir tier_5a_scripting/elixir/samples/elixir_fundamentals.exs` |
| Clojure | Immutability, homoiconicity, concurrency primitives on JVM | `clj -M tier_5b_lisp/clojure/samples/clojure_fundamentals.clj` |
| C# | Value/reference types, multi-paradigm on CLR | `dotnet script tier_6_dotnet/csharp/samples/CSharpFundamentals.cs` |
| F# | Functional-first, type inference, ADTs on .NET | `dotnet fsi tier_6_dotnet/fsharp/samples/FSharpFundamentals.fs` |

## Repo Structure

```text
tier_0_python/     Python DSA scripts, reference docs, CP routine
tier_1_systems/    Rust + C++ (Weeks 1-2)
tier_2_jvm/        Java, Kotlin, Scala (Weeks 3-4)
tier_3_web/        JS, TS (Weeks 5-6)
tier_4_concurrent/ Go, Zig (Weeks 7-8)
tier_5a_scripting/ Ruby, PHP, Elixir (Weeks 9-10)
tier_5b_lisp/      Clojure (Weeks 11-12)
tier_6_dotnet/     C#, F# (Weeks 13-14)
leetcode/          Solutions organized by pattern
projects/          Saturday project scaffolds
docs/              Sprint planning artifacts and PRDs
```

## Glossary — Ubiquitous Language

| Term | Definition |
|------|-----------|
| **ADT** | Algebraic Data Type. Sum types (enums) + product types (structs). |
| **BFF** | Backend-for-Frontend. A dedicated backend per client type. |
| **CQRS** | Command Query Responsibility Segregation. Separate read and write models. |
| **DDD** | Domain-Driven Design. Model software around business domains. |
| **Event Sourcing** | Store events, not state. Derive current state by replaying. |
| **Fan-Out/Fan-In** | Distribute work, collect results. Channel-based coordination. |
| **Hexagonal Architecture** | Ports and adapters. Domain isolated from infrastructure. |
| **Monk Mode** | 15-week intensive sprint. Daily 4AM sessions. No distractions. |
| **OTP** | Open Telecom Platform (Erlang/Elixir). Supervision trees, GenServers. |
| **Pipeline** | Chain processing stages connected by channels. |
| **RAII** | Resource Acquisition Is Initialization. C++/Rust ownership pattern. |
| **ROP** | Railway-Oriented Programming. Composable error handling via Result types. |
| **Saga** | Multi-step distributed transaction with compensating actions. |
| **Third Eye** | Architectural perception. Seeing patterns in code before they're named. |
| **Tier** | A 2-week language grouping in the sprint (Tier 1 = Rust+C++). |
| **Zazen** | Seated Zen meditation. 15 minutes daily before code. |
| **Zero-Copy** | Data moves through systems without being copied between buffers. |
