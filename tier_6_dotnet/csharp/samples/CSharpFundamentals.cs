// C# Fundamentals: Beginner to Advanced — Standard Library Only.
//
// A dense, runnable syntax reference covering core C# concepts.
// Run: dotnet script CSharpFundamentals.cs    (with dotnet-script)
//  or: Place in a console project and: dotnet run
// Requires: .NET 7+ / C# 11+

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

// --- Variables & types ---
int x = 42;
double pi = 3.14;
string name = "C#";
bool flag = true;
object? nothing = null;
Console.WriteLine($"int={x}  double={pi}  string={name}  bool={flag}  null={nothing}");

// --- String interpolation ---
Console.WriteLine($"Interpolation: {name} version {11}");
Console.WriteLine($"Expression: {x * 2}  Format: {pi:F4}  Align: {name,10}");
Console.WriteLine($"Raw string: {"""Hello "World" """.Trim()}");

// --- Null coalescing ---
string? maybe = null;
string result = maybe ?? "default";
Console.WriteLine($"Null coalesce: {result}");
maybe ??= "assigned";
Console.WriteLine($"Null coalesce assign: {maybe}");

// Null conditional
int? length = maybe?.Length;
Console.WriteLine($"Null conditional: {length}");

// --- Ranges & indices ---
int[] arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
Console.WriteLine($"Range [2..5]: [{string.Join(", ", arr[2..5])}]");
Console.WriteLine($"Range [^3..]: [{string.Join(", ", arr[^3..])}]");
Console.WriteLine($"Index [^1]: {arr[^1]}");

// --- Tuples ---
var point = (X: 3, Y: 4);
Console.WriteLine($"Tuple: {point}  X={point.X}  Y={point.Y}");
var (px, py) = point;
Console.WriteLine($"Deconstructed: px={px}  py={py}");

// ============================================================
//  2. COLLECTIONS & LINQ
// ============================================================
Section("2. COLLECTIONS & LINQ");

// --- List ---
var list = new List<int> { 3, 1, 4, 1, 5, 9, 2, 6 };
list.Add(5);
list.Sort();
Console.WriteLine($"List: [{string.Join(", ", list)}]");

// --- Dictionary ---
var dict = new Dictionary<string, int> { ["Alice"] = 30, ["Bob"] = 25 };
dict["Carol"] = 28;
Console.WriteLine($"Dict: {string.Join(", ", dict.Select(kv => $"{kv.Key}={kv.Value}"))}");
Console.WriteLine($"TryGet: {(dict.TryGetValue("Alice", out var age) ? age : -1)}");

// --- HashSet ---
var set1 = new HashSet<int> { 1, 2, 3, 4 };
var set2 = new HashSet<int> { 3, 4, 5, 6 };
Console.WriteLine($"Union: [{string.Join(", ", set1.Union(set2))}]");
Console.WriteLine($"Intersect: [{string.Join(", ", set1.Intersect(set2))}]");

// --- Queue & Stack ---
var queue = new Queue<string>(["first", "second", "third"]);
Console.WriteLine($"Queue dequeue: {queue.Dequeue()}  peek: {queue.Peek()}");
var stack = new Stack<int>([1, 2, 3]);
Console.WriteLine($"Stack pop: {stack.Pop()}  peek: {stack.Peek()}");

// --- LINQ ---
var nums = Enumerable.Range(1, 10).ToList();
Console.WriteLine($"Select:  [{string.Join(", ", nums.Select(n => n * 2))}]");
Console.WriteLine($"Where:   [{string.Join(", ", nums.Where(n => n % 2 == 0))}]");
Console.WriteLine($"GroupBy: {string.Join(", ", nums.GroupBy(n => n % 3).Select(g => $"{g.Key}:[{string.Join(",", g)}]"))}");
Console.WriteLine($"Aggregate: {nums.Aggregate(0, (acc, n) => acc + n)}");
Console.WriteLine($"OrderByDesc: [{string.Join(", ", nums.OrderByDescending(n => n).Take(5))}]");
Console.WriteLine($"Zip: [{string.Join(", ", nums.Take(3).Zip(new[] { "a", "b", "c" }, (n, s) => $"{n}{s}"))}]");
Console.WriteLine($"SelectMany: [{string.Join(", ", new[] { new[] { 1, 2 }, new[] { 3, 4 } }.SelectMany(a => a))}]");
Console.WriteLine($"Distinct: [{string.Join(", ", new[] { 1, 1, 2, 3, 3 }.Distinct())}]");

// --- LINQ query syntax ---
var query = from n in nums
            where n > 3
            orderby n descending
            select n * 10;
Console.WriteLine($"Query syntax: [{string.Join(", ", query.Take(5))}]");

// ============================================================
//  3. OOP
// ============================================================
Section("3. OOP — Classes, Interfaces, Records, Structs");

// --- Interface ---
// (Defined below as top-level types aren't allowed inside methods in top-level statements,
//  so we use a nested approach via local demonstration)

// --- Record (reference type, value equality) ---
Console.WriteLine($"Record: {new Person("Alice", 30)}");
Console.WriteLine($"Record with: {new Person("Alice", 30) with { Age = 31 }}");
Console.WriteLine($"Record equality: {new Person("A", 1) == new Person("A", 1)}");

// --- Record struct ---
Console.WriteLine($"Record struct: {new Point3D(1, 2, 3)}");

// --- Abstract & sealed ---
Shape circle = new Circle(5);
Shape rect = new Rectangle(4, 6);
Console.WriteLine($"Circle area: {circle.Area():F2}  perimeter: {circle.Perimeter():F2}");
Console.WriteLine($"Rect area: {rect.Area():F2}  perimeter: {rect.Perimeter():F2}");

// --- Init-only properties ---
var config = new AppConfig { Host = "localhost", Port = 8080 };
Console.WriteLine($"Init-only: {config.Host}:{config.Port}");
// config.Port = 9090; // Error: init-only

// ============================================================
//  4. GENERICS
// ============================================================
Section("4. GENERICS — Constraints, Covariance/Contravariance");

// --- Generic method with constraint ---
static T Max<T>(T a, T b) where T : IComparable<T>
    => a.CompareTo(b) >= 0 ? a : b;

Console.WriteLine($"Generic Max: {Max(3, 7)}  {Max("apple", "banana")}");

// --- Generic class ---
var typedStack = new TypedStack<int>();
typedStack.Push(10);
typedStack.Push(20);
typedStack.Push(30);
Console.WriteLine($"Generic stack pop: {typedStack.Pop()}  peek: {typedStack.Peek()}");

// --- Covariance/Contravariance ---
IEnumerable<object> objects = new List<string> { "hello", "world" }; // covariant
Console.WriteLine($"Covariance: [{string.Join(", ", objects)}]");

// ============================================================
//  5. ASYNC
// ============================================================
Section("5. ASYNC — async/await, Task, IAsyncEnumerable, Channel");

// --- Basic async/await ---
static async Task<int> ComputeAsync(int n)
{
    await Task.Delay(10);
    return n * n;
}

var asyncResult = await ComputeAsync(7);
Console.WriteLine($"async/await: {asyncResult}");

// --- Task.WhenAll ---
var tasks = Enumerable.Range(1, 5).Select(ComputeAsync);
var results2 = await Task.WhenAll(tasks);
Console.WriteLine($"WhenAll: [{string.Join(", ", results2)}]");

// --- ValueTask ---
static ValueTask<int> FastPath(int n) => new(n * 2);
Console.WriteLine($"ValueTask: {await FastPath(21)}");

// --- IAsyncEnumerable ---
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
Console.WriteLine($"IAsyncEnumerable: [{string.Join(", ", asyncItems)}]");

// --- Channel ---
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
Console.WriteLine($"Channel: [{string.Join(", ", channelItems)}]");

// ============================================================
//  6. PATTERN MATCHING
// ============================================================
Section("6. PATTERN MATCHING — is, switch, Property, Relational");

// --- is pattern ---
object obj = 42;
if (obj is int i && i > 0)
    Console.WriteLine($"is pattern: positive int {i}");

// --- Switch expression ---
static string Classify(object o) => o switch
{
    int n when n < 0 => "negative",
    int n when n == 0 => "zero",
    int n => $"positive ({n})",
    string s => $"string '{s}'",
    null => "null",
    _ => "other"
};
Console.WriteLine($"Switch: {Classify(-5)}  {Classify(0)}  {Classify(42)}  {Classify("hi")}");

// --- Property pattern ---
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
    Console.WriteLine($"  Property pattern: {status}");
}

// --- Relational pattern ---
static string Grade(int score) => score switch
{
    >= 90 => "A",
    >= 80 => "B",
    >= 70 => "C",
    >= 60 => "D",
    _ => "F"
};
Console.WriteLine($"Relational: {Grade(95)} {Grade(82)} {Grade(55)}");

// --- List pattern ---
int[] data = [1, 2, 3, 4, 5];
if (data is [var first, var second, .. var rest2])
    Console.WriteLine($"List pattern: first={first} second={second} rest=[{string.Join(", ", rest2)}]");

// ============================================================
//  7. FUNCTIONAL
// ============================================================
Section("7. FUNCTIONAL — Func/Action, Local Functions, Tuples");

// --- Func & Action ---
Func<int, int, int> add = (a, b) => a + b;
Action<string> greet = msg => Console.WriteLine($"  Action: {msg}");
Console.WriteLine($"Func: {add(3, 4)}");
greet("Hello from Action!");

// --- Static lambda ---
Func<int, int> doubleIt = static n => n * 2;
Console.WriteLine($"Static lambda: {doubleIt(21)}");

// --- Local function ---
static int Fibonacci(int n)
{
    if (n <= 1) return n;
    return Fibonacci(n - 1) + Fibonacci(n - 2);
}
Console.WriteLine($"Local fn fib(10): {Fibonacci(10)}");

// --- Deconstruction ---
var (min, max2) = (nums.Min(), nums.Max());
Console.WriteLine($"Deconstruct: min={min} max={max2}");

// --- Closures ---
static Func<int, int> MakeMultiplier(int factor) => n => n * factor;
var triple = MakeMultiplier(3);
Console.WriteLine($"Closure: triple(7) = {triple(7)}");

// ============================================================
//  8. ADVANCED
// ============================================================
Section("8. ADVANCED — Span, Ref Struct, Extension Methods");

// --- Span<T> ---
Span<int> span = stackalloc int[] { 10, 20, 30, 40, 50 };
var slice = span[1..4];
Console.WriteLine($"Span slice: [{slice[0]}, {slice[1]}, {slice[2]}]");

// --- ReadOnlySpan from string ---
ReadOnlySpan<char> greeting2 = "Hello, World!";
var word = greeting2[0..5];
Console.WriteLine($"ReadOnlySpan: {word.ToString()}");

// --- Extension method usage ---
Console.WriteLine($"Extension: {"hello world".WordCount()} words");
Console.WriteLine($"Extension: {42.IsEven()}");

// --- Readonly struct ---
var vel = new Velocity(3.0, 4.0);
Console.WriteLine($"Readonly struct: {vel}  magnitude: {vel.Magnitude:F2}");

// --- Ref struct (stack-only) ---
// Span<T> is itself a ref struct — demonstrated above

// --- String.Create for efficient string building ---
var efficient = string.Create(10, 0, (span2, _) =>
{
    for (int j = 0; j < span2.Length; j++)
        span2[j] = (char)('A' + j % 26);
});
Console.WriteLine($"String.Create: {efficient}");

Console.WriteLine($"\n{new string('=', 60)}");
Console.WriteLine("  All sections complete!");
Console.WriteLine(new string('=', 60));

// ============================================================
//  Type Definitions (required at bottom for top-level statements)
// ============================================================

record Person(string Name, int Age);
record struct Point3D(double X, double Y, double Z);

abstract class Shape
{
    public abstract double Area();
    public abstract double Perimeter();
}

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

readonly struct Velocity(double Vx, double Vy)
{
    public double Magnitude => Math.Sqrt(Vx * Vx + Vy * Vy);
    public override string ToString() => $"Velocity({Vx}, {Vy})";
}

static class StringExtensions
{
    public static int WordCount(this string s) => s.Split(' ', StringSplitOptions.RemoveEmptyEntries).Length;
}

static class IntExtensions
{
    public static bool IsEven(this int n) => n % 2 == 0;
}
