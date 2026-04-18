# Tier 1 — Systems Programming (Weeks 1-2)

**Languages:** Rust, C++
**Patterns:** BFF (Backend-for-Frontend), Event-Driven Architecture, Zero-Copy / Shared-Nothing

## Focus

- Ownership, lifetimes, RAII
- Systems-level concurrency (async/await in Rust, threads in C++)
- Memory-safe design patterns
- Performance-critical data structures

## Samples

### rust_fundamentals.rs

Rust fundamentals covering ownership, borrowing, lifetimes, pattern matching, traits, generics, error handling with Result/Option, and concurrency via threads, channels (mpsc), Arc/Mutex, and atomics. Explores Cow, PhantomData, and interior mutability with RefCell/Rc.

```bash
rustc rust/samples/rust_fundamentals.rs -o /tmp/rust_fund && /tmp/rust_fund
```

### cpp_fundamentals.cpp

Modern C++20 showcase: auto, structured bindings, ranges, concepts, smart pointers (unique_ptr, shared_ptr), RAII, std::optional/variant, threading with mutex/future/async, and constexpr. Covers containers (vector, map, set, deque) and algorithm pipelines.

```bash
clang++ -std=c++20 -o /tmp/cpp_fund cpp/samples/cpp_fundamentals.cpp -lpthread && /tmp/cpp_fund
```
