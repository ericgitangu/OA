# Tier 4 — Concurrent & Low-Level (Weeks 7-8)

**Languages:** Go, Zig
**Patterns:** Fan-Out/Fan-In, Pipeline, Worker Pool

## Samples

### go_fundamentals.go

Go fundamentals: constants with iota, multiple return values, slices, maps, structs, interfaces, goroutines, channels (buffered/unbuffered), select, sync.WaitGroup/Mutex, context for cancellation, JSON marshalling, and error wrapping.

```bash
go run go/samples/go_fundamentals.go
```

### zig_fundamentals.zig

Zig fundamentals: explicit type conversions, optionals (?T), error unions (E!T), comptime execution, slices, packed structs, defer/errdefer, allocators, tagged unions, and no-hidden-control-flow philosophy. No implicit conversions, no hidden allocations.

```bash
zig run zig/samples/zig_fundamentals.zig
```
