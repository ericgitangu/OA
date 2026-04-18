// C# Fundamentals: Beginner to Advanced — Standard Library Only.
//
// A dense, runnable syntax reference covering core C# concepts.
// Run: dotnet script CSharpFundamentals.cs    (with dotnet-script)
//  or: Place in a console project and: dotnet run
// Requires: .NET 7+ / C# 11+
//
// C# is a statically-typed, multi-paradigm language on the .NET runtime (CLR).
// The CLR provides: JIT/AOT compilation, garbage collection, and a unified type system
// where every type ultimately derives from System.Object. C# distinguishes between
// value types (struct, int, bool — stored on stack/inline) and reference types
// (class, string, arrays — stored on heap with GC tracking). This distinction matters
// for performance: value types avoid heap allocations and GC pressure.

using System;
using System.Collections.Generic;
using System.Collections.Concurrent;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using System.Threading.Channels;
using System.Runtime.CompilerServices;

// ============================================================
//  Helpers
// ============================================================
static void Section(string title)
{
    Console.WriteLine($"\n{new string('=', 60)}");
    Console.WriteLine($"  {title}");
    Console.WriteLine(new string('=', 60));
}

// ============================================================
//  1. BASICS
// ============================================================
Section("1. BASICS — var, Interpolation, Null Coalescing, Ranges");

// C# is statically typed — int, double, string are known at compile time.
// int/double/bool are VALUE types (stored on stack, no GC overhead).
// string is a REFERENCE type (stored on heap) but immutable — safe to share.
// object? enables nullable reference types (C# 8+), a compile-time safety feature.
int x = 42;
double pi = 3.14;
string name = "C#";
bool flag = true;
object? nothing = null;
Console.WriteLine($"int={x}  double={pi}  string={name}  bool={flag}  null={nothing}");  // => int=42  double=3.14  string=C#  bool=True  null=

// String interpolation ($"...{expr}...") compiles to string.Format or string.Concat.
// Format specifiers after : control display (F4 = 4 decimal places, ,10 = right-align 10 chars).
Console.WriteLine($"Interpolation: {name} version {11}");  // => Interpolation: C# version 11
Console.WriteLine($"Expression: {x * 2}  Format: {pi:F4}  Align: {name,10}");  // => Expression: 84  Format: 3.1400  Align:         C#
// Raw string literals (C# 11+): use """ delimiters to embed unescaped quotes
var rawStr = """Hello "World" """;
Console.WriteLine($"Raw string: {rawStr.Trim()}");  // => Raw string: Hello "World"

// Null coalescing (??) provides a default when the left operand is null.
// ??= assigns only if the variable is currently null — avoids overwriting existing values.
// These operators work with both nullable value types (int?) and nullable reference types (string?).
string? maybe = null;
string result = maybe ?? "default";
Console.WriteLine($"Null coalesce: {result}");  // => Null coalesce: default
maybe ??= "assigned";
Console.WriteLine($"Null coalesce assign: {maybe}");  // => Null coalesce assign: assigned

// Null conditional (?.) short-circuits to null if the receiver is null.
// It returns a nullable type — int? here because maybe could be null.
int? length = maybe?.Length;
Console.WriteLine($"Null conditional: {length}");  // => Null conditional: 8

// Ranges (Index/Range types, C# 8+) use .. syntax for slicing.
// ^n means "from end" — ^1 is the last element, ^3 is third from end.
// Under the hood, Range is a struct with Start/End Index values — no heap allocation.
int[] arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
Console.WriteLine($"Range [2..5]: [{string.Join(", ", arr[2..5])}]");  // => Range [2..5]: [3, 4, 5]
Console.WriteLine($"Range [^3..]: [{string.Join(", ", arr[^3..])}]");  // => Range [^3..]: [8, 9, 10]
Console.WriteLine($"Index [^1]: {arr[^1]}");  // => Index [^1]: 10

// Tuples are VALUE types (ValueTuple<T1,T2>) — no heap allocation.
// Named elements (X, Y) are compile-time sugar; at runtime they're Item1, Item2.
// Deconstruction (var (px, py) = point) works via the Deconstruct pattern.
var point = (X: 3, Y: 4);
Console.WriteLine($"Tuple: {point}  X={point.X}  Y={point.Y}");  // => Tuple: (3, 4)  X=3  Y=4
var (px, py) = point;
Console.WriteLine($"Deconstructed: px={px}  py={py}");  // => Deconstructed: px=3  py=4

// ============================================================
//  2. COLLECTIONS & LINQ
// ============================================================
Section("2. COLLECTIONS & LINQ");

// List<T> is backed by a resizable array (not a linked list).
// It doubles capacity when full — amortized O(1) Add, O(1) index access.
var list = new List<int> { 3, 1, 4, 1, 5, 9, 2, 6 };
list.Add(5);
list.Sort();
Console.WriteLine($"List: [{string.Join(", ", list)}]");  // => List: [1, 1, 2, 3, 4, 5, 5, 6, 9]

// Dictionary<K,V> is a hash table — O(1) average lookup/insert.
// TryGetValue is the safe pattern: returns bool + out parameter, avoids KeyNotFoundException.
var dict = new Dictionary<string, int> { ["Alice"] = 30, ["Bob"] = 25 };
dict["Carol"] = 28;
Console.WriteLine($"Dict: {string.Join(", ", dict.Select(kv => $"{kv.Key}={kv.Value}"))}");  // => Dict: Alice=30, Bob=25, Carol=28
Console.WriteLine($"TryGet: {(dict.TryGetValue("Alice", out var age) ? age : -1)}");  // => TryGet: 30

// HashSet<T> uses hashing for O(1) contains/add. Set operations (Union, Intersect)
// return new sequences — the original set is not modified by LINQ extension methods.
var set1 = new HashSet<int> { 1, 2, 3, 4 };
var set2 = new HashSet<int> { 3, 4, 5, 6 };
Console.WriteLine($"Union: [{string.Join(", ", set1.Union(set2))}]");  // => Union: [1, 2, 3, 4, 5, 6]
Console.WriteLine($"Intersect: [{string.Join(", ", set1.Intersect(set2))}]");  // => Intersect: [3, 4]

// Queue (FIFO) and Stack (LIFO) — both backed by arrays, not linked nodes.
var queue = new Queue<string>(["first", "second", "third"]);
Console.WriteLine($"Queue dequeue: {queue.Dequeue()}  peek: {queue.Peek()}");  // => Queue dequeue: first  peek: second
var stack = new Stack<int>([1, 2, 3]);
Console.WriteLine($"Stack pop: {stack.Pop()}  peek: {stack.Peek()}");  // => Stack pop: 3  peek: 2

// LINQ (Language Integrated Query) adds declarative query capabilities to any IEnumerable<T>.
// LINQ methods are lazy — they return IEnumerable<T> that only evaluates when iterated.
// Select = map, Where = filter, Aggregate = reduce (fold). Same concepts, C# naming.
var nums = Enumerable.Range(1, 10).ToList();
Console.WriteLine($"Select:  [{string.Join(", ", nums.Select(n => n * 2))}]");  // => Select:  [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
Console.WriteLine($"Where:   [{string.Join(", ", nums.Where(n => n % 2 == 0))}]");  // => Where:   [2, 4, 6, 8, 10]
Console.WriteLine($"GroupBy: {string.Join(", ", nums.GroupBy(n => n % 3).Select(g => $"{g.Key}:[{string.Join(",", g)}]"))}");  // => GroupBy: 1:[1,4,7,10], 2:[2,5,8], 0:[3,6,9]

// Aggregate is C#'s fold/reduce — takes seed + accumulator function.
Console.WriteLine($"Aggregate: {nums.Aggregate(0, (acc, n) => acc + n)}");  // => Aggregate: 55
Console.WriteLine($"OrderByDesc: [{string.Join(", ", nums.OrderByDescending(n => n).Take(5))}]");  // => OrderByDesc: [10, 9, 8, 7, 6]
Console.WriteLine($"Zip: [{string.Join(", ", nums.Take(3).Zip(new[] { "a", "b", "c" }, (n, s) => $"{n}{s}"))}]");  // => Zip: [1a, 2b, 3c]

// SelectMany flattens nested collections — like flatMap in other languages.
Console.WriteLine($"SelectMany: [{string.Join(", ", new[] { new[] { 1, 2 }, new[] { 3, 4 } }.SelectMany(a => a))}]");  // => SelectMany: [1, 2, 3, 4]
Console.WriteLine($"Distinct: [{string.Join(", ", new[] { 1, 1, 2, 3, 3 }.Distinct())}]");  // => Distinct: [1, 2, 3]

// Query syntax is SQL-like sugar that compiles to the same extension method calls above.
// Some developers prefer it for complex joins and groupings; method syntax is more common.
var query = from n in nums
            where n > 3
            orderby n descending
            select n * 10;
Console.WriteLine($"Query syntax: [{string.Join(", ", query.Take(5))}]");  // => Query syntax: [100, 90, 80, 70, 60]

// ============================================================
//  3. OOP
// ============================================================
Section("3. OOP — Classes, Interfaces, Records, Structs");

// (Type definitions at bottom — C# top-level statements require types after executable code)

// Records (C# 9+) are reference types with built-in value equality, immutability, and
// with-expression support. The compiler generates Equals, GetHashCode, ToString, and
// a copy constructor. record struct (C# 10+) is the value-type variant — stack-allocated.
Console.WriteLine($"Record: {new Person("Alice", 30)}");  // => Record: Person { Name = Alice, Age = 30 }
Console.WriteLine($"Record with: {new Person("Alice", 30) with { Age = 31 }}");  // => Record with: Person { Name = Alice, Age = 31 }
Console.WriteLine($"Record equality: {new Person("A", 1) == new Person("A", 1)}");  // => Record equality: True

// Record structs combine value-type performance (no heap allocation) with record features.
Console.WriteLine($"Record struct: {new Point3D(1, 2, 3)}");  // => Record struct: Point3D { X = 1, Y = 2, Z = 3 }

// sealed prevents inheritance — the compiler can optimize virtual dispatch to direct calls
// when it knows the complete type hierarchy. This also enables exhaustive pattern matching.
Shape circle = new Circle(5);
Shape rect = new Rectangle(4, 6);
Console.WriteLine($"Circle area: {circle.Area():F2}  perimeter: {circle.Perimeter():F2}");  // => Circle area: 78.54  perimeter: 31.42
Console.WriteLine($"Rect area: {rect.Area():F2}  perimeter: {rect.Perimeter():F2}");  // => Rect area: 24.00  perimeter: 20.00

// Init-only properties (init accessor, C# 9+) can be set during object initialization
// but are immutable afterward. Combined with required (C# 11+), the compiler ensures
// all required properties are set at construction time.
var config = new AppConfig { Host = "localhost", Port = 8080 };
Console.WriteLine($"Init-only: {config.Host}:{config.Port}");  // => Init-only: localhost:8080
// config.Port = 9090; // Error: init-only

// ============================================================
//  4. GENERICS
// ============================================================
Section("4. GENERICS — Constraints, Covariance/Contravariance");

// Generic constraints (where T : IComparable<T>) restrict which types can be used.
// Unlike Java's type erasure, .NET generics are reified — the runtime knows the actual type.
// This means List<int> stores actual ints (no boxing), unlike Java's ArrayList<Integer>.
static T Max<T>(T a, T b) where T : IComparable<T>
    => a.CompareTo(b) >= 0 ? a : b;

Console.WriteLine($"Generic Max: {Max(3, 7)}  {Max("apple", "banana")}");  // => Generic Max: 7  banana

var typedStack = new TypedStack<int>();
typedStack.Push(10);
typedStack.Push(20);
typedStack.Push(30);
Console.WriteLine($"Generic stack pop: {typedStack.Pop()}  peek: {typedStack.Peek()}");  // => Generic stack pop: 30  peek: 20

// Covariance (out T): IEnumerable<string> can be assigned to IEnumerable<object>
// because strings ARE objects. out means T only appears in output positions.
// Contravariance (in T): Action<object> can be assigned to Action<string>.
IEnumerable<object> objects = new List<string> { "hello", "world" }; // covariant
Console.WriteLine($"Covariance: [{string.Join(", ", objects)}]");  // => Covariance: [hello, world]

// ============================================================
//  5. ASYNC
// ============================================================
Section("5. ASYNC — async/await, Task, IAsyncEnumerable, Channel");

// async/await is compiler-generated state machine sugar. The compiler transforms the method
// into a state machine struct (IAsyncStateMachine) that tracks which await point you're at.
// When you await, the method suspends and frees the thread — no thread is blocked.
// The continuation is scheduled on the original SynchronizationContext (if any) when the
// awaited task completes. This is fundamentally different from threads — it's cooperative.
static async Task<int> ComputeAsync(int n)
{
    await Task.Delay(10);
    return n * n;
}

var asyncResult = await ComputeAsync(7);
Console.WriteLine($"async/await: {asyncResult}");  // => async/await: 49

// Task.WhenAll starts all tasks concurrently and waits for all to complete.
// Each Task runs on the thread pool — the runtime manages thread scheduling.
var tasks = Enumerable.Range(1, 5).Select(ComputeAsync);
var results2 = await Task.WhenAll(tasks);
Console.WriteLine($"WhenAll: [{string.Join(", ", results2)}]");  // => WhenAll: [1, 4, 9, 16, 25]

// ValueTask<T> (struct) avoids heap-allocating a Task when the result is already available.
// Use it for methods that often complete synchronously (cache hits, buffered reads).
// Warning: ValueTask can only be awaited ONCE — don't cache or await multiple times.
static ValueTask<int> FastPath(int n) => new(n * 2);
Console.WriteLine($"ValueTask: {await FastPath(21)}");  // => ValueTask: 42

// IAsyncEnumerable<T> (C# 8+) enables async iteration with await foreach.
// The producer yields values asynchronously — great for streaming DB results, API pages, etc.
// [EnumeratorCancellation] wires up cancellation tokens through the async iterator.
static async IAsyncEnumerable<int> GenerateAsync(int count,
    [EnumeratorCancellation] CancellationToken ct = default)
{
    for (int i = 0; i < count; i++)
    {
        await Task.Delay(1, ct);
        yield return i * i;
    }
}

var asyncItems = new List<int>();
await foreach (var item in GenerateAsync(5))
    asyncItems.Add(item);
Console.WriteLine($"IAsyncEnumerable: [{string.Join(", ", asyncItems)}]");  // => IAsyncEnumerable: [0, 1, 4, 9, 16]

// Channels are thread-safe producer-consumer queues — the CSP (Communicating Sequential
// Processes) pattern from Go, built into .NET. Bounded channels apply backpressure when full.
// This is the recommended way to pass data between async producers and consumers.
var channel = Channel.CreateBounded<int>(10);
_ = Task.Run(async () =>
{
    for (int i = 0; i < 5; i++)
        await channel.Writer.WriteAsync(i * 10);
    channel.Writer.Complete();
});

var channelItems = new List<int>();
await foreach (var item in channel.Reader.ReadAllAsync())
    channelItems.Add(item);
Console.WriteLine($"Channel: [{string.Join(", ", channelItems)}]");  // => Channel: [0, 10, 20, 30, 40]

// ============================================================
//  6. PATTERN MATCHING
// ============================================================
Section("6. PATTERN MATCHING — is, switch, Property, Relational");

// The is pattern (C# 7+) combines type check + cast + condition in one expression.
// The variable i is only in scope when the pattern matches — no separate cast needed.
object obj = 42;
if (obj is int i && i > 0)
    Console.WriteLine($"is pattern: positive int {i}");  // => is pattern: positive int 42

// Switch expressions (C# 8+) are exhaustive — the compiler warns if cases are missing.
// Each arm uses pattern matching: type patterns, when guards, discard (_) for default.
// Unlike switch statements, switch expressions return a value.
static string Classify(object o) => o switch
{
    int n when n < 0 => "negative",
    int n when n == 0 => "zero",
    int n => $"positive ({n})",
    string s => $"string '{s}'",
    null => "null",
    _ => "other"
};
Console.WriteLine($"Switch: {Classify(-5)}  {Classify(0)}  {Classify(42)}  {Classify("hi")}");  // => Switch: negative  zero  positive (42)  string 'hi'

// Property patterns (C# 8+) match against object properties.
// Nested property access (Name.Length) works in C# 10+.
// Combined with relational patterns (>= 18), this replaces complex if/else chains.
var people = new[]
{
    new Person("Alice", 30),
    new Person("Bob", 17),
    new Person("Carol", 25),
};

foreach (var p in people)
{
    var status = p switch
    {
        { Age: >= 18, Name.Length: > 4 } => $"{p.Name}: adult with long name",
        { Age: >= 18 } => $"{p.Name}: adult",
        _ => $"{p.Name}: minor"
    };
    Console.WriteLine($"  Property pattern: {status}");  // => (varies per person)
}

// Relational patterns (C# 9+) compare against constants directly in pattern position.
// The compiler evaluates top-to-bottom and takes the first match.
static string Grade(int score) => score switch
{
    >= 90 => "A",
    >= 80 => "B",
    >= 70 => "C",
    >= 60 => "D",
    _ => "F"
};
Console.WriteLine($"Relational: {Grade(95)} {Grade(82)} {Grade(55)}");  // => Relational: A B F

// List patterns (C# 11+) destructure arrays/lists with positional syntax.
// .. is the slice pattern — captures remaining elements into a variable.
int[] data = [1, 2, 3, 4, 5];
if (data is [var first, var second, .. var rest2])
    Console.WriteLine($"List pattern: first={first} second={second} rest=[{string.Join(", ", rest2)}]");  // => List pattern: first=1 second=2 rest=[3, 4, 5]

// ============================================================
//  7. FUNCTIONAL
// ============================================================
Section("7. FUNCTIONAL — Func/Action, Local Functions, Tuples");

// Func<TArgs..., TReturn> and Action<TArgs...> are the built-in delegate types.
// Func returns a value; Action returns void. Lambdas (=>) create instances of these.
// Under the hood, lambdas compile to private methods + delegate instances.
Func<int, int, int> add = (a, b) => a + b;
Action<string> greet = msg => Console.WriteLine($"  Action: {msg}");
Console.WriteLine($"Func: {add(3, 4)}");  // => Func: 7
greet("Hello from Action!");  // => Action: Hello from Action!

// Static lambdas (C# 9+) guarantee no variable capture — the compiler rejects any
// reference to local variables. This prevents accidental closure allocations.
Func<int, int> doubleIt = static n => n * 2;
Console.WriteLine($"Static lambda: {doubleIt(21)}");  // => Static lambda: 42

// Local functions are methods defined inside other methods. Unlike lambdas, they can:
// 1. Be recursive without a variable (lambdas need Func<int,int> fib = null; fib = n => ...)
// 2. Use ref/out/in parameters and ref returns
// 3. Be marked static to prevent captures (like static lambdas)
static int Fibonacci(int n)
{
    if (n <= 1) return n;
    return Fibonacci(n - 1) + Fibonacci(n - 2);
}
Console.WriteLine($"Local fn fib(10): {Fibonacci(10)}");  // => Local fn fib(10): 55

// Deconstruction works with any type that has a Deconstruct method or is a tuple.
var (min, max2) = (nums.Min(), nums.Max());
Console.WriteLine($"Deconstruct: min={min} max={max2}");  // => Deconstruct: min=1 max=10

// Closures in C# capture variables by reference (not by value like in PHP).
// The captured variable is hoisted to a compiler-generated class on the heap.
// This means mutations to the captured variable are visible to the closure and vice versa.
static Func<int, int> MakeMultiplier(int factor) => n => n * factor;
var triple = MakeMultiplier(3);
Console.WriteLine($"Closure: triple(7) = {triple(7)}");  // => Closure: triple(7) = 21

// ============================================================
//  8. ADVANCED
// ============================================================
Section("8. ADVANCED — Span, Ref Struct, Extension Methods");

// Span<T> is a ref struct that provides safe, bounds-checked access to contiguous memory
// (arrays, stack memory, native buffers) WITHOUT heap allocation.
// stackalloc allocates on the STACK — automatically freed when the method returns.
// Span ensures memory safety: no dangling pointers, no buffer overruns.
// Because Span is a ref struct, it can ONLY live on the stack — never on the heap,
// never in async methods, never as a class field. This is enforced by the compiler.
Span<int> span = stackalloc int[] { 10, 20, 30, 40, 50 };
var slice = span[1..4];
Console.WriteLine($"Span slice: [{slice[0]}, {slice[1]}, {slice[2]}]");  // => Span slice: [20, 30, 40]

// ReadOnlySpan<char> from a string is a zero-allocation slice — no new string is created.
// The span points directly into the original string's memory.
// This is how high-performance parsers avoid string allocations.
ReadOnlySpan<char> greeting2 = "Hello, World!";
var word = greeting2[0..5];
Console.WriteLine($"ReadOnlySpan: {word.ToString()}");  // => ReadOnlySpan: Hello

// Extension methods add methods to existing types without modifying them.
// The `this` keyword on the first parameter marks it as an extension method.
// They must be in a static class and are resolved at compile time (not virtual dispatch).
Console.WriteLine($"Extension: {"hello world".WordCount()} words");  // => Extension: 2 words
Console.WriteLine($"Extension: {42.IsEven()}");  // => Extension: True

// Readonly structs guarantee all fields are readonly — the compiler verifies this.
// This enables the JIT to optimize: no defensive copies when passing by `in` reference.
// Use readonly struct for small, immutable value types (vectors, colors, coordinates).
var vel = new Velocity(3.0, 4.0);
Console.WriteLine($"Readonly struct: {vel}  magnitude: {vel.Magnitude:F2}");  // => Readonly struct: Velocity(3, 4)  magnitude: 5.00

// --- Ref struct (stack-only) ---
// Span<T> is itself a ref struct — demonstrated above

// String.Create avoids intermediate allocations — it gives you a writable Span<char>
// that becomes the final immutable string. Useful for building strings from computed data.
var efficient = string.Create(10, 0, (span2, _) =>
{
    for (int j = 0; j < span2.Length; j++)
        span2[j] = (char)('A' + j % 26);
});
Console.WriteLine($"String.Create: {efficient}");  // => String.Create: ABCDEFGHIJ

Console.WriteLine($"\n{new string('=', 60)}");
Console.WriteLine("  All sections complete!");  // => All sections complete!
Console.WriteLine(new string('=', 60));

// ============================================================
//  Type Definitions (required at bottom for top-level statements)
// ============================================================

// record generates a reference type with value-based equality (Equals, GetHashCode),
// a copy constructor for `with` expressions, and a readable ToString.
// Positional syntax (string Name, int Age) creates a constructor + readonly properties.
record Person(string Name, int Age);

// record struct is a VALUE type — allocated on stack, no GC overhead.
// Use for small data carriers that benefit from value semantics.
record struct Point3D(double X, double Y, double Z);

// abstract forces subclasses to implement Area/Perimeter — compile-time enforcement.
abstract class Shape
{
    public abstract double Area();
    public abstract double Perimeter();
}

// sealed + primary constructor (C# 12+). Primary constructor params are available
// throughout the class body — no need for fields or property declarations.
sealed class Circle(double Radius) : Shape
{
    public override double Area() => Math.PI * Radius * Radius;
    public override double Perimeter() => 2 * Math.PI * Radius;
}

sealed class Rectangle(double Width, double Height) : Shape
{
    public override double Area() => Width * Height;
    public override double Perimeter() => 2 * (Width + Height);
}

// required (C# 11+) makes properties mandatory at construction time.
// init makes them settable only during initialization — immutable afterward.
class AppConfig
{
    public required string Host { get; init; }
    public required int Port { get; init; }
}

class TypedStack<T>
{
    private readonly List<T> _items = [];
    public void Push(T item) => _items.Add(item);
    public T Pop()
    {
        var item = _items[^1];
        _items.RemoveAt(_items.Count - 1);
        return item;
    }
    public T Peek() => _items[^1];
}

// readonly struct: ALL fields must be readonly. The compiler enforces immutability.
// This is a value type — copied on assignment, no heap allocation, no GC.
readonly struct Velocity(double Vx, double Vy)
{
    public double Magnitude => Math.Sqrt(Vx * Vx + Vy * Vy);
    public override string ToString() => $"Velocity({Vx}, {Vy})";
}

// Extension methods must be in a top-level static class.
// The `this` keyword on the first parameter is what makes it an extension.
static class StringExtensions
{
    public static int WordCount(this string s) => s.Split(' ', StringSplitOptions.RemoveEmptyEntries).Length;
}

static class IntExtensions
{
    public static bool IsEven(this int n) => n % 2 == 0;
}
