# Tier 1 — Rust

## Build

```bash
cargo build
cargo run
```

## Docker

```bash
docker build -t tier1-rust .
docker run tier1-rust
```

## Focus Areas
- Ownership, borrowing, lifetimes
- Pattern matching, Result/Option
- Async/await with tokio
- Axum web framework
- Traits and generics
- FFI with C++ (zero-copy buffers)
