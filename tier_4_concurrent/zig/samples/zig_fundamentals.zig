const std = @import("std");
const print = std.debug.print;
const testing = std.testing;
const mem = std.mem;

// ============================================================
// SECTION: Basics — const/var, types, optionals, error unions
// ============================================================

const greeting: []const u8 = "Hello, Zig!";
const pi: f64 = 3.14159;

fn demoBasics() void {
    print("\n=== BASICS ===\n", .{});

    // const and var
    const x: i32 = 42;
    var y: i32 = 10;
    y += x;
    print("const x={d}  var y={d}\n", .{ x, y });

    // type coercion
    const small: u8 = 200;
    const wide: u16 = small;
    print("u8={d} -> u16={d}\n", .{ small, wide });

    // optionals (?T)
    const maybe: ?i32 = 42;
    const nothing: ?i32 = null;
    if (maybe) |val| {
        print("optional unwrapped: {d}\n", .{val});
    }
    print("nothing is null: {}\n", .{nothing == null});

    // orelse — provide default for optional
    const fallback = nothing orelse 99;
    print("orelse fallback: {d}\n", .{fallback});

    // Blocks as expressions
    const block_val = blk: {
        var tmp: i32 = 10;
        tmp *= 3;
        break :blk tmp;
    };
    print("block expression: {d}\n", .{block_val});
}

// ============================================================
// SECTION: Comptime — parameters, blocks, type reflection
// ============================================================

fn comptimeMax(comptime T: type, a: T, b: T) T {
    return if (a > b) a else b;
}

fn typeName(comptime T: type) []const u8 {
    return @typeName(T);
}

fn demoComptime() void {
    print("\n=== COMPTIME ===\n", .{});

    // comptime function
    const max_int = comptimeMax(i32, 10, 20);
    const max_float = comptimeMax(f64, 3.14, 2.71);
    print("max_int={d}  max_float={d:.2}\n", .{ max_int, max_float });

    // comptime block
    const computed = comptime blk: {
        var result: i32 = 1;
        for (0..10) |_| {
            result *= 2;
        }
        break :blk result;
    };
    print("comptime 2^10 = {d}\n", .{computed});

    // type reflection
    print("i32 type name: {s}\n", .{typeName(i32)});
    print("f64 type name: {s}\n", .{typeName(f64)});

    // @typeInfo reflection
    const info = @typeInfo(i32);
    switch (info) {
        .int => |int_info| {
            print("i32 bits={d} signed={}\n", .{ int_info.bits, int_info.signedness == .signed });
        },
        else => {},
    }
}

// ============================================================
// SECTION: Memory — allocators, manual management
// ============================================================

fn demoMemory() void {
    print("\n=== MEMORY ===\n", .{});

    // FixedBufferAllocator — stack-backed, no syscalls
    var buf: [256]u8 = undefined;
    var fba = std.heap.FixedBufferAllocator.init(&buf);
    const fba_alloc = fba.allocator();
    const fixed_slice = fba_alloc.alloc(u8, 10) catch unreachable;
    for (fixed_slice, 0..) |*byte, i| {
        byte.* = @intCast(i + 65); // 'A', 'B', ...
    }
    print("FixedBuffer: {s}\n", .{fixed_slice});

    // GeneralPurposeAllocator — debug allocator with leak detection
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer {
        const check = gpa.deinit();
        if (check == .leak) {
            print("WARNING: memory leak detected!\n", .{});
        }
    }
    const gpa_alloc = gpa.allocator();

    const data = gpa_alloc.alloc(u32, 5) catch unreachable;
    defer gpa_alloc.free(data);
    for (data, 0..) |*item, i| {
        item.* = @intCast(i * i);
    }
    print("GPA allocated: ", .{});
    for (data) |item| {
        print("{d} ", .{item});
    }
    print("\n", .{});

    // ArenaAllocator — bulk free, no individual frees needed
    var arena = std.heap.ArenaAllocator.init(gpa_alloc);
    defer arena.deinit();
    const arena_alloc = arena.allocator();

    const s1 = arena_alloc.alloc(u8, 5) catch unreachable;
    const s2 = arena_alloc.alloc(u8, 5) catch unreachable;
    @memcpy(s1, "ARENA");
    @memcpy(s2, "ALLOC");
    print("Arena: {s} {s}\n", .{ s1, s2 });
}

// ============================================================
// SECTION: Slices — operations, sentinel-terminated
// ============================================================

fn demoSlices() void {
    print("\n=== SLICES ===\n", .{});

    // Basic slice from array
    const arr = [_]i32{ 10, 20, 30, 40, 50 };
    const slice = arr[1..4];
    print("arr[1..4]: ", .{});
    for (slice) |v| print("{d} ", .{v});
    print("\n", .{});

    // Slice length and pointer
    print("slice len={d}\n", .{slice.len});

    // Sentinel-terminated slices (null-terminated strings are common)
    const c_string: [:0]const u8 = "hello";
    print("sentinel string: {s}  len={d}\n", .{ c_string, c_string.len });

    // Comparing slices
    const a = "hello";
    const b = "hello";
    print("slices equal: {}\n", .{mem.eql(u8, a, b)});

    // Searching
    if (mem.indexOf(u8, "hello world", "world")) |idx| {
        print("indexOf 'world': {d}\n", .{idx});
    }
}

// ============================================================
// SECTION: Structs — methods, packed, anonymous
// ============================================================

const Vec2 = struct {
    x: f64,
    y: f64,

    const Self = @This();

    fn init(x: f64, y: f64) Self {
        return .{ .x = x, .y = y };
    }

    fn length(self: Self) f64 {
        return @sqrt(self.x * self.x + self.y * self.y);
    }

    fn add(self: Self, other: Self) Self {
        return .{ .x = self.x + other.x, .y = self.y + other.y };
    }

    fn scale(self: *Self, factor: f64) void {
        self.x *= factor;
        self.y *= factor;
    }
};

// Packed struct — exact memory layout
const Flags = packed struct {
    readable: bool,
    writable: bool,
    executable: bool,
    _reserved: u5 = 0,
};

fn demoStructs() void {
    print("\n=== STRUCTS ===\n", .{});

    const a = Vec2.init(3.0, 4.0);
    const b = Vec2.init(1.0, 2.0);
    const c = a.add(b);
    print("a=({d:.1},{d:.1})  len={d:.2}\n", .{ a.x, a.y, a.length() });
    print("a+b=({d:.1},{d:.1})\n", .{ c.x, c.y });

    // Mutation via pointer receiver
    var mutable = Vec2.init(1.0, 1.0);
    mutable.scale(5.0);
    print("scaled=({d:.1},{d:.1})\n", .{ mutable.x, mutable.y });

    // Packed struct
    const flags = Flags{ .readable = true, .writable = false, .executable = true };
    print("packed size={d} bytes\n", .{@sizeOf(Flags)});
    print("flags: r={} w={} x={}\n", .{ flags.readable, flags.writable, flags.executable });

    // Anonymous struct
    const point = .{ .name = "origin", .x = @as(i32, 0), .y = @as(i32, 0) };
    print("anon struct: {s} ({d},{d})\n", .{ point.name, point.x, point.y });
}

// ============================================================
// SECTION: Enums — methods, tagged unions, non-exhaustive
// ============================================================

const Color = enum(u8) {
    red = 1,
    green = 2,
    blue = 3,

    fn isWarm(self: Color) bool {
        return self == .red;
    }

    fn name(self: Color) []const u8 {
        return switch (self) {
            .red => "Red",
            .green => "Green",
            .blue => "Blue",
        };
    }
};

// Tagged union — type-safe discriminated union
const Value = union(enum) {
    int: i64,
    float: f64,
    boolean: bool,
    none,

    fn format(self: Value) [64]u8 {
        var buf: [64]u8 = .{0} ** 64;
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
    print("\n=== ENUMS & UNIONS ===\n", .{});

    const c = Color.green;
    print("color={s}  isWarm={}\n", .{ c.name(), c.isWarm() });
    print("color int value={d}\n", .{@intFromEnum(c)});

    // Tagged union
    const vals = [_]Value{
        .{ .int = 42 },
        .{ .float = 3.14 },
        .{ .boolean = true },
        .none,
    };
    for (vals) |v| {
        const formatted = v.format();
        const end = mem.indexOfScalar(u8, &formatted, 0) orelse formatted.len;
        print("  value: {s}\n", .{formatted[0..end]});
    }

    // Switch on enum
    const dir = Direction.north;
    const desc: []const u8 = switch (dir) {
        .north => "up",
        .south => "down",
        .east => "right",
        .west => "left",
    };
    print("direction: {s}\n", .{desc});
}

// ============================================================
// SECTION: Error Handling — error sets, try, catch, errdefer
// ============================================================

const ParseError = error{
    InvalidCharacter,
    Overflow,
    Empty,
};

fn parseDigit(c: u8) ParseError!u8 {
    if (c < '0' or c > '9') return ParseError.InvalidCharacter;
    return c - '0';
}

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
    print("\n=== ERROR HANDLING ===\n", .{});

    // try — propagates error
    if (parseNumber("123")) |val| {
        print("parsed: {d}\n", .{val});
    } else |_| {}

    // catch — handle error
    const result = parseNumber("abc") catch |err| blk: {
        print("caught error: {}\n", .{err});
        break :blk -1;
    };
    print("fallback value: {d}\n", .{result});

    // Error from empty
    const empty_result = parseNumber("");
    if (empty_result) |_| {} else |err| {
        print("empty error: {}\n", .{err});
    }

    // errdefer demonstration concept
    print("errdefer: runs cleanup only on error path\n", .{});
}

// ============================================================
// SECTION: Control Flow — expressions, loops, labeled blocks
// ============================================================

fn demoControlFlow() void {
    print("\n=== CONTROL FLOW ===\n", .{});

    // if as expression
    const x: i32 = 42;
    const abs_x = if (x < 0) -x else x;
    print("abs({d}) = {d}\n", .{ x, abs_x });

    // while with continue expression
    var sum: i32 = 0;
    var i: i32 = 0;
    while (i < 10) : (i += 1) {
        sum += i;
    }
    print("while sum 0..9 = {d}\n", .{sum});

    // for loop with index
    const items = [_][]const u8{ "alpha", "beta", "gamma" };
    print("for: ", .{});
    for (items, 0..) |item, idx| {
        print("[{d}]={s} ", .{ idx, item });
    }
    print("\n", .{});

    // Labeled block as expression
    const found = blk: {
        const haystack = [_]i32{ 4, 8, 15, 16, 23, 42 };
        for (haystack) |val| {
            if (val == 23) break :blk val;
        }
        break :blk @as(i32, -1);
    };
    print("labeled block found: {d}\n", .{found});

    // Labeled break from nested loop
    var outer_count: u32 = 0;
    outer: for (0..5) |_| {
        for (0..5) |j| {
            if (j == 3) continue :outer;
            outer_count += 1;
        }
    }
    print("nested loop count (break at j=3): {d}\n", .{outer_count});
}

// ============================================================
// SECTION: Functions — generic via comptime, inline
// ============================================================

fn swap(comptime T: type, a: *T, b: *T) void {
    const tmp = a.*;
    a.* = b.*;
    b.* = tmp;
}

fn repeat(comptime T: type, value: T, comptime count: usize) [count]T {
    return .{value} ** count;
}

fn arraySum(comptime T: type, arr: []const T) T {
    var total: T = 0;
    for (arr) |v| {
        total += v;
    }
    return total;
}

fn demoFunctions() void {
    print("\n=== FUNCTIONS ===\n", .{});

    // Generic swap
    var a: i32 = 10;
    var b: i32 = 20;
    swap(i32, &a, &b);
    print("swap: a={d} b={d}\n", .{ a, b });

    // Comptime repeat
    const fives = repeat(u8, 5, 4);
    print("repeat: ", .{});
    for (fives) |v| print("{d} ", .{v});
    print("\n", .{});

    // Generic sum
    const ints = [_]i32{ 1, 2, 3, 4, 5 };
    print("arraySum(ints) = {d}\n", .{arraySum(i32, &ints)});

    const floats = [_]f64{ 1.1, 2.2, 3.3 };
    print("arraySum(floats) = {d:.1}\n", .{arraySum(f64, &floats)});
}

// ============================================================
// SECTION: Testing — test blocks
// ============================================================

test "parseDigit valid" {
    const result = try parseDigit('5');
    try testing.expectEqual(@as(u8, 5), result);
}

test "parseDigit invalid" {
    const result = parseDigit('x');
    try testing.expectError(ParseError.InvalidCharacter, result);
}

test "parseNumber" {
    const val = try parseNumber("456");
    try testing.expectEqual(@as(i32, 456), val);
}

test "Vec2 length" {
    const v = Vec2.init(3.0, 4.0);
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
    print("\n=== ADVANCED ===\n", .{});

    // SIMD vectors — hardware-accelerated parallel operations
    const VecType = @Vector(4, f32);
    const a: VecType = .{ 1.0, 2.0, 3.0, 4.0 };
    const b: VecType = .{ 5.0, 6.0, 7.0, 8.0 };
    const added = a + b;
    const multiplied = a * b;
    print("SIMD add: ", .{});
    for (0..4) |i| print("{d:.0} ", .{added[i]});
    print("\n", .{});
    print("SIMD mul: ", .{});
    for (0..4) |i| print("{d:.0} ", .{multiplied[i]});
    print("\n", .{});

    // @import is used at top of file (std = @import("std"))
    // @embedFile embeds a file at comptime as a string:
    //   const data = @embedFile("config.txt");
    print("@import: used to import std and other modules\n", .{});
    print("@embedFile: embeds file contents at compile time\n", .{});

    // Async note: Zig async/await was removed in 0.11+
    // The feature may return in a future version with different semantics
    print("async: removed in 0.11, may return in future versions\n", .{});
}

// ============================================================
// MAIN
// ============================================================

pub fn main() void {
    print("==================================================\n", .{});
    print("  Zig Fundamentals — Comprehensive Reference\n", .{});
    print("==================================================\n", .{});

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

    print("\n== Done ==\n", .{});
}
