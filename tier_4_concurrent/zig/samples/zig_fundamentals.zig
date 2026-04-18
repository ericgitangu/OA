const std = @import("std");
const print = std.debug.print;
const testing = std.testing;
const mem = std.mem;

// ============================================================
// SECTION: Basics — const/var, types, optionals, error unions
// ============================================================

// Zig strings are []const u8 — slices of constant bytes. There is no special string
// type. This design means strings use the same APIs as any other byte slice (mem.eql,
// mem.indexOf, etc.), keeping the language small. See Zig docs: Slices
const greeting: []const u8 = "Hello, Zig!";
const pi: f64 = 3.14159;

fn demoBasics() void {
    print("\n=== BASICS ===\n", .{});  // => === BASICS ===

    // `const` bindings are immutable — the compiler enforces this at compile time.
    // `var` bindings are mutable. Zig has no shadowing — you can't redeclare a name
    // in the same scope. This prevents accidental shadowing bugs common in C/Go.
    const x: i32 = 42;
    var y: i32 = 10;
    y += x;
    print("const x={d}  var y={d}\n", .{ x, y });  // => const x=42  var y=52

    // Zig uses explicit widening, not implicit coercion. A u8 can be assigned to u16
    // because it's a safe (lossless) conversion. Narrowing requires @intCast and the
    // compiler inserts a runtime safety check in debug builds (panic on overflow).
    // This "no hidden control flow" philosophy means no implicit conversions, constructors,
    // or operator overloading. See Zig docs: Type Coercion
    const small: u8 = 200;
    const wide: u16 = small;
    print("u8={d} -> u16={d}\n", .{ small, wide });  // => u8=200 -> u16=200

    // Optionals (?T) are Zig's null safety mechanism — a value is either T or null.
    // This is a tagged union under the hood: the compiler tracks nullability at the type
    // level. You MUST unwrap with `if (maybe) |val|` or `orelse` before using the value.
    // This eliminates null pointer dereference bugs at compile time.
    const maybe: ?i32 = 42;
    const nothing: ?i32 = null;
    if (maybe) |val| {
        print("optional unwrapped: {d}\n", .{val});  // => optional unwrapped: 42
    }
    print("nothing is null: {}\n", .{nothing == null});  // => nothing is null: true

    // `orelse` provides a default value when an optional is null. This is the idiomatic
    // way to provide fallbacks — similar to Rust's unwrap_or() or Swift's ?? operator.
    const fallback = nothing orelse 99;
    print("orelse fallback: {d}\n", .{fallback});  // => orelse fallback: 99

    // Blocks are expressions in Zig — they can return a value via `break :label value`.
    // This eliminates the need for ternary operators or separate variable declarations.
    // Labeled blocks are also used for breaking out of nested loops (see Control Flow section).
    const block_val = blk: {
        var tmp: i32 = 10;
        tmp *= 3;
        break :blk tmp;
    };
    print("block expression: {d}\n", .{block_val});  // => block expression: 30
}

// ============================================================
// SECTION: Comptime — parameters, blocks, type reflection
// ============================================================

// `comptime` is Zig's most distinctive feature: it runs arbitrary Zig code at compile time.
// Unlike C++ templates or Rust generics, comptime uses the SAME language for compile-time
// and runtime code — no separate template/macro language. The compiler acts as an interpreter
// during compilation. This enables generics, metaprogramming, and compile-time validation
// with zero runtime cost. See Zig docs: comptime

// `comptime T: type` makes T a compile-time-known type parameter. The compiler generates
// specialized code for each unique T used — similar to C++ template instantiation, but
// with full language semantics (you can use loops, conditionals, etc. at comptime).
fn comptimeMax(comptime T: type, a: T, b: T) T {
    return if (a > b) a else b;
}

// @typeName is a builtin that returns the string name of a type at compile time.
// Zig builtins (@-prefixed) are compiler intrinsics — they have special behavior
// that can't be implemented in userland code. See Zig docs: Builtin Functions
fn typeName(comptime T: type) []const u8 {
    return @typeName(T);
}

fn demoComptime() void {
    print("\n=== COMPTIME ===\n", .{});  // => === COMPTIME ===

    // These calls are fully resolved at compile time — no runtime dispatch or vtable lookup.
    // The compiler generates separate, optimized machine code for comptimeMax(i32, ...) and
    // comptimeMax(f64, ...). This is how Zig achieves generic programming without boxing.
    const max_int = comptimeMax(i32, 10, 20);
    const max_float = comptimeMax(f64, 3.14, 2.71);
    print("max_int={d}  max_float={d:.2}\n", .{ max_int, max_float });  // => max_int=20  max_float=3.14

    // comptime blocks execute arbitrary code during compilation. The result is embedded
    // as a constant in the binary. This replaces build scripts, code generators, and
    // constexpr in C++. You can read files, parse data, generate lookup tables, etc.
    const computed = comptime blk: {
        var result: i32 = 1;
        for (0..10) |_| {
            result *= 2;
        }
        break :blk result;
    };
    print("comptime 2^10 = {d}\n", .{computed});  // => comptime 2^10 = 1024

    // Type reflection at compile time via @typeInfo: returns a tagged union describing
    // the type's structure (fields, methods, alignment, signedness, etc.).
    // This enables writing generic serialization, validation, and formatting code.
    print("i32 type name: {s}\n", .{typeName(i32)});  // => i32 type name: i32
    print("f64 type name: {s}\n", .{typeName(f64)});  // => f64 type name: f64

    // @typeInfo returns a std.builtin.Type union — you can switch on it to inspect
    // any type's properties. This is compile-time reflection, not runtime reflection
    // (unlike Go's reflect package). Zero overhead in the final binary.
    const info = @typeInfo(i32);
    switch (info) {
        .int => |int_info| {
            print("i32 bits={d} signed={}\n", .{ int_info.bits, int_info.signedness == .signed });  // => i32 bits=32 signed=true
        },
        else => {},
    }
}

// ============================================================
// SECTION: Memory — allocators, manual management
// ============================================================

// Zig's allocator philosophy: there is no default allocator. Every allocation requires
// an explicit allocator parameter. This makes allocation visible, testable, and swappable.
// Unlike C's malloc or Rust's global allocator, Zig forces you to choose: stack (FixedBuffer),
// debug (GPA with leak detection), arena (bulk free), or custom. This design prevents
// hidden allocations — a core "no hidden control flow" principle. See Zig docs: Allocators

fn demoMemory() void {
    print("\n=== MEMORY ===\n", .{});  // => === MEMORY ===

    // FixedBufferAllocator allocates from a stack-provided buffer — no syscalls, no heap.
    // Ideal for embedded systems or when you know the max allocation size upfront.
    // Fails (returns error) when the buffer is exhausted — no silent overflow.
    var buf: [256]u8 = undefined;
    var fba = std.heap.FixedBufferAllocator.init(&buf);
    const fba_alloc = fba.allocator();
    const fixed_slice = fba_alloc.alloc(u8, 10) catch unreachable;
    for (fixed_slice, 0..) |*byte, i| {
        byte.* = @intCast(i + 65); // 'A', 'B', ...
    }
    print("FixedBuffer: {s}\n", .{fixed_slice});  // => FixedBuffer: ABCDEFGHIJ

    // GeneralPurposeAllocator (GPA) is the debug/development allocator. It detects:
    // - Memory leaks (on deinit)
    // - Double frees
    // - Use-after-free (via poisoning freed memory)
    // Use GPA during development, then swap to a faster allocator (c_allocator, page_allocator)
    // for production via the allocator parameter — no code changes needed.
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer {
        const check = gpa.deinit();
        if (check == .leak) {
            print("WARNING: memory leak detected!\n", .{});
        }
    }
    const gpa_alloc = gpa.allocator();

    // Every alloc returns an error union (![]T) — you must handle allocation failure.
    // `catch unreachable` asserts "this can't fail" (panics in debug, UB in release).
    // In production, use `catch return error.OutOfMemory` to propagate gracefully.
    const data = gpa_alloc.alloc(u32, 5) catch unreachable;
    // defer ensures cleanup runs when the function returns — Zig's RAII equivalent.
    // Unlike C++ destructors, defer is explicit and visible at the allocation site.
    defer gpa_alloc.free(data);
    for (data, 0..) |*item, i| {
        item.* = @intCast(i * i);
    }
    print("GPA allocated: ", .{});
    for (data) |item| {
        print("{d} ", .{item});  // => 0 1 4 9 16
    }
    print("\n", .{});

    // ArenaAllocator allocates from a backing allocator but never frees individually.
    // All memory is freed at once via arena.deinit(). This is optimal for request-scoped
    // or frame-scoped allocations (web servers, game loops) where individual frees
    // would add complexity with no benefit.
    var arena = std.heap.ArenaAllocator.init(gpa_alloc);
    defer arena.deinit();
    const arena_alloc = arena.allocator();

    const s1 = arena_alloc.alloc(u8, 5) catch unreachable;
    const s2 = arena_alloc.alloc(u8, 5) catch unreachable;
    @memcpy(s1, "ARENA");
    @memcpy(s2, "ALLOC");
    print("Arena: {s} {s}\n", .{ s1, s2 });  // => Arena: ARENA ALLOC
}

// ============================================================
// SECTION: Slices — operations, sentinel-terminated
// ============================================================

fn demoSlices() void {
    print("\n=== SLICES ===\n", .{});  // => === SLICES ===

    // Arrays have compile-time-known length (part of the type). Slices are (pointer, length)
    // pairs that can reference any contiguous memory — arrays, heap allocations, or subregions.
    // Slicing an array (`arr[1..4]`) creates a view into the original — no copy, no allocation.
    const arr = [_]i32{ 10, 20, 30, 40, 50 };
    const slice = arr[1..4];
    print("arr[1..4]: ", .{});
    for (slice) |v| print("{d} ", .{v});  // => 20 30 40
    print("\n", .{});

    // .len is a field on the slice fat pointer, not a function call. O(1) access.
    print("slice len={d}\n", .{slice.len});  // => slice len=3

    // Sentinel-terminated slices ([:0]const u8) guarantee a known value after the last element.
    // Null-terminated strings (C interop) are the most common use. The sentinel is NOT included
    // in .len but IS accessible at slice[slice.len]. This enables safe C string interop
    // without manual null termination.
    const c_string: [:0]const u8 = "hello";
    print("sentinel string: {s}  len={d}\n", .{ c_string, c_string.len });  // => sentinel string: hello  len=5

    // mem.eql compares slices element-by-element. Zig has no operator overloading, so
    // == on slices compares the fat pointer (address + length), not contents.
    // Always use mem.eql for content comparison. This explicitness prevents the
    // "is it pointer or value equality?" bugs common in Java/Python.
    const a = "hello";
    const b = "hello";
    print("slices equal: {}\n", .{mem.eql(u8, a, b)});  // => slices equal: true

    // mem.indexOf performs linear search on byte slices. Returns an optional (?usize) —
    // null if not found. This forces you to handle the "not found" case explicitly.
    if (mem.indexOf(u8, "hello world", "world")) |idx| {
        print("indexOf 'world': {d}\n", .{idx});  // => indexOf 'world': 6
    }
}

// ============================================================
// SECTION: Structs — methods, packed, anonymous
// ============================================================

// Structs in Zig are compile-time types with no hidden vtable, no RTTI, no default
// constructors. The compiler may reorder fields for optimal alignment (unless `packed`
// or `extern` is used). Methods are just namespaced functions — `self` is an explicit
// parameter, not a hidden `this` pointer. See Zig docs: Structs
const Vec2 = struct {
    x: f64,
    y: f64,

    // @This() returns the type of the enclosing struct — used to avoid repeating
    // the struct name. This is a comptime function, resolved during compilation.
    const Self = @This();

    // Zig has no constructors — `init` is a convention, not a language feature.
    // It's just a function that returns Self. No hidden allocation, no implicit calls.
    fn init(x: f64, y: f64) Self {
        return .{ .x = x, .y = y };
    }

    // `self: Self` is a value receiver — the struct is passed by value (copied).
    // For large structs, use `self: *const Self` to pass by pointer (avoid copy).
    // Zig makes this choice explicit — no compiler magic to auto-reference/dereference.
    fn length(self: Self) f64 {
        return @sqrt(self.x * self.x + self.y * self.y);
    }

    fn add(self: Self, other: Self) Self {
        return .{ .x = self.x + other.x, .y = self.y + other.y };
    }

    // `self: *Self` is a pointer receiver — allows mutation of the original struct.
    // The caller can use `mutable.scale(5.0)` syntax — Zig auto-references for method calls.
    fn scale(self: *Self, factor: f64) void {
        self.x *= factor;
        self.y *= factor;
    }
};

// Packed structs guarantee exact memory layout with no padding between fields.
// This is essential for memory-mapped I/O, network protocols, and binary file formats.
// The total size is exactly the sum of field sizes. Fields may not be aligned —
// accessing them may be slower on some architectures.
const Flags = packed struct {
    readable: bool,
    writable: bool,
    executable: bool,
    _reserved: u5 = 0,
};

fn demoStructs() void {
    print("\n=== STRUCTS ===\n", .{});  // => === STRUCTS ===

    const a = Vec2.init(3.0, 4.0);
    const b = Vec2.init(1.0, 2.0);
    const c = a.add(b);
    print("a=({d:.1},{d:.1})  len={d:.2}\n", .{ a.x, a.y, a.length() });  // => a=(3.0,4.0)  len=5.00
    print("a+b=({d:.1},{d:.1})\n", .{ c.x, c.y });  // => a+b=(4.0,6.0)

    // Method call on mutable variable — Zig auto-takes the address of `mutable`
    // because scale() requires *Self. This is one of the few implicit behaviors in Zig.
    var mutable = Vec2.init(1.0, 1.0);
    mutable.scale(5.0);
    print("scaled=({d:.1},{d:.1})\n", .{ mutable.x, mutable.y });  // => scaled=(5.0,5.0)

    // Packed struct: @sizeOf returns 1 byte (8 bits = 1 bool + 1 bool + 1 bool + 5-bit padding).
    // Compare with a regular struct where each bool would occupy a full byte due to alignment.
    const flags = Flags{ .readable = true, .writable = false, .executable = true };
    print("packed size={d} bytes\n", .{@sizeOf(Flags)});  // => packed size=1 bytes
    print("flags: r={} w={} x={}\n", .{ flags.readable, flags.writable, flags.executable });  // => flags: r=true w=false x=true

    // Anonymous structs infer their type from usage. The `.{ }` syntax creates a value
    // of an anonymous struct type — useful for passing structured data to generic functions
    // (like print's .{} argument tuples). See Zig docs: Anonymous Struct Literals
    const point = .{ .name = "origin", .x = @as(i32, 0), .y = @as(i32, 0) };
    print("anon struct: {s} ({d},{d})\n", .{ point.name, point.x, point.y });  // => anon struct: origin (0,0)
}

// ============================================================
// SECTION: Enums — methods, tagged unions, non-exhaustive
// ============================================================

// Enums in Zig can have an explicit backing integer type (u8 here) and methods.
// Unlike C enums, Zig enums are type-safe — you can't implicitly convert between
// enum and integer. Use @intFromEnum/@enumFromInt for explicit conversion.
const Color = enum(u8) {
    red = 1,
    green = 2,
    blue = 3,

    // Enum methods are namespaced functions — `Color.isWarm(.red)` or `c.isWarm()`.
    fn isWarm(self: Color) bool {
        return self == .red;
    }

    // Switch on enum must be exhaustive — every variant must be handled (or use `else`).
    // The compiler errors if you add a new variant without handling it in all switches.
    // This is Zig's exhaustive checking — no silent fallthrough like C.
    fn name(self: Color) []const u8 {
        return switch (self) {
            .red => "Red",
            .green => "Green",
            .blue => "Blue",
        };
    }
};

// Tagged unions are Zig's discriminated union — they combine an enum tag with variant data.
// The tag is stored alongside the payload, enabling safe access. Switching on a tagged union
// provides the payload for each variant automatically. This replaces inheritance hierarchies,
// visitor patterns, and void* casts. Similar to Rust's enum with data, Haskell's ADTs.
const Value = union(enum) {
    int: i64,
    float: f64,
    boolean: bool,
    none,

    fn format(self: Value) [64]u8 {
        var buf: [64]u8 = .{0} ** 64;
        // Switch on tagged union: each case captures the variant's payload via |v|.
        // The compiler guarantees you can only access the active variant's data.
        switch (self) {
            .int => |v| _ = std.fmt.bufPrint(&buf, "int({d})", .{v}) catch {},
            .float => |v| _ = std.fmt.bufPrint(&buf, "float({d:.2})", .{v}) catch {},
            .boolean => |v| _ = std.fmt.bufPrint(&buf, "bool({})", .{v}) catch {},
            .none => _ = std.fmt.bufPrint(&buf, "none", .{}) catch {},
        }
        return buf;
    }
};

const Direction = enum { north, south, east, west };

fn demoEnums() void {
    print("\n=== ENUMS & UNIONS ===\n", .{});  // => === ENUMS & UNIONS ===

    const c = Color.green;
    print("color={s}  isWarm={}\n", .{ c.name(), c.isWarm() });  // => color=Green  isWarm=false
    // @intFromEnum extracts the backing integer value. This is explicit because
    // Zig prevents accidental enum-to-int conversion (unlike C where enums are just ints).
    print("color int value={d}\n", .{@intFromEnum(c)});  // => color int value=2

    // Tagged union: each variant carries different data. The .none variant has no payload.
    const vals = [_]Value{
        .{ .int = 42 },
        .{ .float = 3.14 },
        .{ .boolean = true },
        .none,
    };
    for (vals) |v| {
        const formatted = v.format();
        const end = mem.indexOfScalar(u8, &formatted, 0) orelse formatted.len;
        print("  value: {s}\n", .{formatted[0..end]});  // => int(42), float(3.14), bool(true), none
    }

    // Switch is an expression in Zig — it returns a value. All switches on enums must
    // be exhaustive. This is safer than if/else chains and enables the compiler to
    // warn you when new variants are added to an enum.
    const dir = Direction.north;
    const desc: []const u8 = switch (dir) {
        .north => "up",
        .south => "down",
        .east => "right",
        .west => "left",
    };
    print("direction: {s}\n", .{desc});  // => direction: up
}

// ============================================================
// SECTION: Error Handling — error sets, try, catch, errdefer
// ============================================================

// Error sets are compile-time-known sets of possible errors. Unlike exceptions, errors
// are values carried in the return type (error union: ErrorSet!T). The compiler tracks
// which errors a function can return, enabling exhaustive error handling.
// No stack unwinding, no hidden control flow — errors propagate explicitly via `try`.
// See Zig docs: Errors
const ParseError = error{
    InvalidCharacter,
    Overflow,
    Empty,
};

// The return type `ParseError!u8` is an error union: either a ParseError or a u8.
// This is a tagged union under the hood — the error set is the tag, the payload is the value.
// The caller must handle the error (try, catch, or if/else).
fn parseDigit(c: u8) ParseError!u8 {
    if (c < '0' or c > '9') return ParseError.InvalidCharacter;
    return c - '0';
}

// `try` is syntactic sugar for `catch |err| return err` — it propagates the error
// to the caller. This makes error propagation a one-keyword operation (like Rust's ?).
// The compiler verifies that the caller's error set is a superset of the callee's.
fn parseNumber(s: []const u8) ParseError!i32 {
    if (s.len == 0) return ParseError.Empty;
    var result: i32 = 0;
    for (s) |c| {
        const digit = try parseDigit(c);
        result = result * 10 + digit;
    }
    return result;
}

fn demoErrors() void {
    print("\n=== ERROR HANDLING ===\n", .{});  // => === ERROR HANDLING ===

    // if/else on error union: |val| captures the success value, |_| captures the error.
    // This is the explicit pattern — use when you need to handle the error differently.
    if (parseNumber("123")) |val| {
        print("parsed: {d}\n", .{val});  // => parsed: 123
    } else |_| {}

    // `catch` provides a fallback value or block when an error occurs.
    // Combined with labeled blocks, catch can execute complex recovery logic.
    // The error payload is captured in |err| for inspection.
    const result = parseNumber("abc") catch |err| blk: {
        print("caught error: {}\n", .{err});  // => caught error: error.InvalidCharacter
        break :blk -1;
    };
    print("fallback value: {d}\n", .{result});  // => fallback value: -1

    // Error from empty input — demonstrates exhaustive error handling
    const empty_result = parseNumber("");
    if (empty_result) |_| {} else |err| {
        print("empty error: {}\n", .{err});  // => empty error: error.Empty
    }

    // errdefer runs cleanup ONLY when the function returns an error — not on success.
    // This is critical for resource cleanup in fallible functions: allocate, then errdefer
    // free. If the function succeeds, the caller owns the resource. If it fails, errdefer
    // cleans up automatically. This eliminates the "goto cleanup" pattern from C.
    print("errdefer: runs cleanup only on error path\n", .{});  // => errdefer: runs cleanup only on error path
}

// ============================================================
// SECTION: Control Flow — expressions, loops, labeled blocks
// ============================================================

fn demoControlFlow() void {
    print("\n=== CONTROL FLOW ===\n", .{});  // => === CONTROL FLOW ===

    // if is an expression in Zig — it returns a value. No ternary operator needed.
    // This reduces the language surface area while keeping the same expressiveness.
    const x: i32 = 42;
    const abs_x = if (x < 0) -x else x;
    print("abs({d}) = {d}\n", .{ x, abs_x });  // => abs(42) = 42

    // while loops have an optional "continue expression" (the `: (i += 1)` part) that
    // runs after each iteration AND after `continue` statements. This prevents the
    // common C bug of forgetting to increment after a `continue`. Zig while loops
    // can also return values via `break :label value`.
    var sum: i32 = 0;
    var i: i32 = 0;
    while (i < 10) : (i += 1) {
        sum += i;
    }
    print("while sum 0..9 = {d}\n", .{sum});  // => while sum 0..9 = 45

    // for loops iterate over slices and ranges. Multi-object for (`items, 0..`) iterates
    // multiple sequences in lockstep — the loop ends when the shortest sequence is exhausted.
    // This replaces the need for enumerate() or zip() functions.
    const items = [_][]const u8{ "alpha", "beta", "gamma" };
    print("for: ", .{});
    for (items, 0..) |item, idx| {
        print("[{d}]={s} ", .{ idx, item });  // => [0]=alpha [1]=beta [2]=gamma
    }
    print("\n", .{});

    // Labeled blocks + break: `break :blk value` exits the labeled block and returns
    // a value. This enables complex expressions without temporary variables or helper
    // functions. Similar to Rust's block expressions or Kotlin's labeled returns.
    const found = blk: {
        const haystack = [_]i32{ 4, 8, 15, 16, 23, 42 };
        for (haystack) |val| {
            if (val == 23) break :blk val;
        }
        break :blk @as(i32, -1);
    };
    print("labeled block found: {d}\n", .{found});  // => labeled block found: 23

    // Labeled break from nested loops: `continue :outer` breaks from the inner loop
    // and continues the outer loop. This replaces boolean flags and goto statements
    // used in C for breaking out of nested loops.
    var outer_count: u32 = 0;
    outer: for (0..5) |_| {
        for (0..5) |j| {
            if (j == 3) continue :outer;
            outer_count += 1;
        }
    }
    print("nested loop count (break at j=3): {d}\n", .{outer_count});  // => nested loop count (break at j=3): 15
}

// ============================================================
// SECTION: Functions — generic via comptime, inline
// ============================================================

// comptime type parameters make functions generic. The compiler monomorphizes each
// unique call — swap(i32, ...) and swap(f64, ...) generate separate machine code.
// Unlike C++ templates, comptime errors produce clear messages at the call site.
// Pointer parameters (*T) allow mutation of the caller's variables.
fn swap(comptime T: type, a: *T, b: *T) void {
    const tmp = a.*;
    a.* = b.*;
    b.* = tmp;
}

// comptime count parameter: the array size must be known at compile time because
// Zig arrays have compile-time-known lengths (the size is part of the type).
// `[count]T` is a different type for each count value. The `**` operator repeats
// an array initializer — `.{value} ** count` creates [count]T filled with value.
fn repeat(comptime T: type, value: T, comptime count: usize) [count]T {
    return .{value} ** count;
}

// Slices ([]const T) are runtime-sized — their length is stored in the fat pointer.
// This function works with any slice length, unlike array-based functions above.
fn arraySum(comptime T: type, arr: []const T) T {
    var total: T = 0;
    for (arr) |v| {
        total += v;
    }
    return total;
}

fn demoFunctions() void {
    print("\n=== FUNCTIONS ===\n", .{});  // => === FUNCTIONS ===

    // Pointers (&a, &b) are passed to swap — Zig has no references, only explicit pointers.
    // The * and & operators make all indirection visible — "no hidden control flow".
    var a: i32 = 10;
    var b: i32 = 20;
    swap(i32, &a, &b);
    print("swap: a={d} b={d}\n", .{ a, b });  // => swap: a=20 b=10

    // repeat(u8, 5, 4) generates [4]u8{ 5, 5, 5, 5 } at compile time.
    // The array is embedded directly in the binary — no runtime allocation or loop.
    const fives = repeat(u8, 5, 4);
    print("repeat: ", .{});
    for (fives) |v| print("{d} ", .{v});  // => 5 5 5 5
    print("\n", .{});

    // &ints coerces the array to a slice ([]const i32). The compiler knows the array
    // is on the stack and creates a fat pointer (address + length) automatically.
    const ints = [_]i32{ 1, 2, 3, 4, 5 };
    print("arraySum(ints) = {d}\n", .{arraySum(i32, &ints)});  // => arraySum(ints) = 15

    const floats = [_]f64{ 1.1, 2.2, 3.3 };
    print("arraySum(floats) = {d:.1}\n", .{arraySum(f64, &floats)});  // => arraySum(floats) = 6.6
}

// ============================================================
// SECTION: Testing — test blocks
// ============================================================

// Zig tests are first-class language constructs, not a separate framework.
// `test "name" { ... }` blocks are compiled and run by `zig test file.zig`.
// They're stripped from production builds automatically. Tests can use the same
// allocator infrastructure — use testing.allocator for leak-checked test allocations.
// See Zig docs: Testing

test "parseDigit valid" {
    const result = try parseDigit('5');
    try testing.expectEqual(@as(u8, 5), result);
}

test "parseDigit invalid" {
    // expectError verifies that a function returns a specific error variant.
    // This is how you test error paths — no try/catch gymnastics needed.
    const result = parseDigit('x');
    try testing.expectError(ParseError.InvalidCharacter, result);
}

test "parseNumber" {
    const val = try parseNumber("456");
    try testing.expectEqual(@as(i32, 456), val);
}

test "Vec2 length" {
    const v = Vec2.init(3.0, 4.0);
    // expectApproxEqAbs compares floats with an epsilon tolerance, avoiding
    // floating-point comparison pitfalls. The third arg is the maximum allowed difference.
    try testing.expectApproxEqAbs(5.0, v.length(), 0.0001);
}

test "swap works" {
    var x: i32 = 1;
    var y: i32 = 2;
    swap(i32, &x, &y);
    try testing.expectEqual(@as(i32, 2), x);
    try testing.expectEqual(@as(i32, 1), y);
}

// ============================================================
// SECTION: Advanced — SIMD vectors, @embedFile
// ============================================================

fn demoAdvanced() void {
    print("\n=== ADVANCED ===\n", .{});  // => === ADVANCED ===

    // @Vector creates SIMD (Single Instruction, Multiple Data) types that map directly
    // to hardware SIMD registers (SSE, AVX, NEON). Operations on vectors execute in
    // parallel on all lanes simultaneously — a 4-lane multiply does 4 multiplications
    // in a single CPU instruction. Zig exposes SIMD as a first-class type, unlike C
    // which requires intrinsics or compiler extensions. See Zig docs: Vectors
    const VecType = @Vector(4, f32);
    const a: VecType = .{ 1.0, 2.0, 3.0, 4.0 };
    const b: VecType = .{ 5.0, 6.0, 7.0, 8.0 };
    const added = a + b;
    const multiplied = a * b;
    print("SIMD add: ", .{});
    for (0..4) |i| print("{d:.0} ", .{added[i]});  // => 6 8 10 12
    print("\n", .{});
    print("SIMD mul: ", .{});
    for (0..4) |i| print("{d:.0} ", .{multiplied[i]});  // => 5 12 21 32
    print("\n", .{});

    // @import brings in other Zig files or the standard library at compile time.
    // @embedFile reads a file at compile time and embeds its contents as a []const u8
    // in the binary. This is useful for embedding templates, shaders, certificates,
    // or configuration files without runtime I/O. The file path is relative to the source file.
    //   const data = @embedFile("config.txt");
    print("@import: used to import std and other modules\n", .{});  // => @import: used to import std and other modules
    print("@embedFile: embeds file contents at compile time\n", .{});  // => @embedFile: embeds file contents at compile time

    // Zig's async/await was removed in 0.11 due to implementation complexity and
    // interaction with the allocator model. The feature may return with different
    // semantics. For concurrent I/O, use std.Thread or platform-specific async I/O (io_uring, kqueue).
    print("async: removed in 0.11, may return in future versions\n", .{});  // => async: removed in 0.11, may return in future versions
}

// ============================================================
// MAIN
// ============================================================

pub fn main() void {
    print("==================================================\n", .{});  // => ==================================================
    print("  Zig Fundamentals — Comprehensive Reference\n", .{});  // => Zig Fundamentals — Comprehensive Reference
    print("==================================================\n", .{});  // => ==================================================

    demoBasics();
    demoComptime();
    demoMemory();
    demoSlices();
    demoStructs();
    demoEnums();
    demoErrors();
    demoControlFlow();
    demoFunctions();
    demoAdvanced();

    print("\n== Done ==\n", .{});  // => == Done ==
}
