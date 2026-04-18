// F# Fundamentals: Beginner to Advanced — Standard Library Only.
//
// A dense, runnable syntax reference covering core F# concepts.
// Run: dotnet fsi FSharpFundamentals.fs
// Requires: .NET 7+ / F# 7+
//
// F# is a statically-typed, functional-first language on .NET. Its type inference is based
// on Hindley-Milner (Algorithm W), which means the compiler can infer most types without
// annotations — you get the safety of static typing with the conciseness of dynamic typing.
// F# compiles to the same IL as C#, so it has full access to the .NET ecosystem.
// Key design principles: immutability by default, expression-oriented (everything returns a value),
// and algebraic data types (discriminated unions + records) for modeling domain logic.

open System
open System.Threading.Tasks

let section title =
    printfn "\n%s" (String.replicate 60 "=")
    printfn "  %s" title
    printfn "%s" (String.replicate 60 "=")

// ============================================================
//  1. BASICS
// ============================================================
section "1. BASICS — let, Immutability, Type Inference, Pipe"

// let bindings are immutable by default — once bound, a value cannot change.
// This isn't a restriction; it's a feature. Immutability eliminates a huge class of bugs:
// no accidental mutations, no race conditions on shared data, and easier reasoning.
// The compiler infers types via Hindley-Milner: x is inferred as int, pi as float, etc.
let x = 42
let pi = 3.14159
let name = "F#"
let flag = true
printfn "int=%d  float=%f  string=%s  bool=%b" x pi name flag  // => int=42  float=3.141590  string=F#  bool=true

// Mutable is explicitly opt-in — the `mutable` keyword signals "this will change."
// <- is the mutation operator (not =, which is equality/binding).
// This makes mutability visible and intentional, not the default.
let mutable counter = 0
counter <- counter + 1
printfn "Mutable counter: %d" counter  // => Mutable counter: 1

// Type annotations are optional because Hindley-Milner infers them.
// The compiler propagates type information bidirectionally — it can infer from usage context.
// Annotations are useful for documentation or when the compiler needs help at module boundaries.
let greet (person: string) : string = $"Hello, {person}!"
printfn "%s" (greet "Alice")  // => Hello, Alice!

// The pipe operator |> passes the left value as the LAST argument to the right function.
// F# originated this pattern (before Elixir adopted it). It enables left-to-right reading
// of data transformations instead of nested function calls.
let result =
    "  Hello, World!  "
    |> fun s -> s.Trim()
    |> fun s -> s.ToLower()
    |> fun s -> s.Split(' ')
    |> Array.toList
printfn "Pipe: %A" result  // => Pipe: ["hello,"; "world!"]

// Backward pipe <| is rarely used — it applies a function to a value from right to left.
// Useful occasionally to avoid parentheses in nested expressions.
let doubled = (fun x -> x * 2) <| 21
printfn "Backward pipe: %d" doubled  // => Backward pipe: 42

// %A is the structural format specifier — it prints any F# value in a readable format.
// printfn uses type-safe format strings checked at compile time (unlike sprintf in C).
printfn "Interpolated: %s is version %d" name 7  // => Interpolated: F# is version 7
printfn $"String interpolation: {name} {1 + 1}"  // => String interpolation: F# 2
printfn "sprintf: %s" (sprintf "Pi is %.4f" pi)  // => sprintf: Pi is 3.1416

// ============================================================
//  2. TYPES
// ============================================================
section "2. TYPES — Discriminated Unions, Records, Tuples, Units of Measure"

// Tuples are ordered, fixed-size groups of values. They're VALUE types in F# — no heap allocation.
// Destructuring with let (px, py) = point extracts elements at bind time.
let point = (3, 4)
let (px, py) = point
printfn "Tuple: %A  fst=%d  snd=%d" point (fst point) (snd point)  // => Tuple: (3, 4)  fst=3  snd=4

// Records are immutable, structurally-typed data containers with named fields.
// Two records with the same fields and values are equal (structural equality).
// `with` creates a modified copy — the original is untouched (immutability).
// Records compile to .NET classes with readonly properties and value-based Equals/GetHashCode.
type Person = { Name: string; Age: int }

let alice = { Name = "Alice"; Age = 30 }
let olderAlice = { alice with Age = 31 }
printfn "Record: %A" alice  // => Record: { Name = "Alice"; Age = 30 }
printfn "Updated: %A" olderAlice  // => Updated: { Name = "Alice"; Age = 31 }
printfn "Equality: %b" (alice = { Name = "Alice"; Age = 30 })  // => Equality: true

// Discriminated Unions (DUs) are the crown jewel of F#'s type system.
// Each case is a distinct alternative — the type is the SUM of all its cases.
// Combined with pattern matching, DUs enforce exhaustive handling of all possibilities.
// The compiler warns if you miss a case — making illegal states unrepresentable.
// This is the "algebraic" in algebraic data types: product types (records) + sum types (DUs).
type Shape =
    | Circle of radius: float
    | Rectangle of width: float * height: float
    | Triangle of a: float * b: float * c: float

// Pattern matching on DUs is exhaustive — the compiler verifies all cases are handled.
// Each branch deconstructs the case and binds its fields to local variables.
let area shape =
    match shape with
    | Circle r -> Math.PI * r * r
    | Rectangle(w, h) -> w * h
    | Triangle(a, b, c) ->
        let s = (a + b + c) / 2.0
        sqrt (s * (s - a) * (s - b) * (s - c))

printfn "Circle area: %.2f" (area (Circle 5.0))  // => Circle area: 78.54
printfn "Rect area: %.2f" (area (Rectangle(4.0, 6.0)))  // => Rect area: 24.00

// Recursive DUs model tree structures naturally.
// `rec` enables recursive function definitions that reference themselves.
type Tree =
    | Leaf of int
    | Node of Tree * Tree

let rec treeSum tree =
    match tree with
    | Leaf v -> v
    | Node(left, right) -> treeSum left + treeSum right

let sampleTree = Node(Node(Leaf 1, Leaf 2), Leaf 3)
printfn "Tree sum: %d" (treeSum sampleTree)  // => Tree sum: 6

// Single-case DUs create type-safe wrappers — Email is NOT a raw string.
// The compiler prevents accidentally passing a string where an Email is expected.
// This is the "parse, don't validate" pattern — illegal values can't be constructed.
type Email = Email of string
let (Email addr) = Email "alice@example.com"
printfn "Single-case DU: %s" addr  // => Single-case DU: alice@example.com

// Units of Measure are compile-time dimensional analysis — they PREVENT unit errors.
// The compiler tracks units through arithmetic: m/s * s = m, kg * m/s^2 = force.
// Units are erased at runtime — zero overhead. This caught the Mars Climate Orbiter bug
// (mixed metric/imperial) at compile time rather than after a $125M crash.
[<Measure>] type m
[<Measure>] type s
[<Measure>] type kg

let distance = 100.0<m>
let time = 9.58<s>
let speed = distance / time
printfn "Speed: %.2f m/s" (float speed)  // => Speed: 10.44 m/s

let mass = 70.0<kg>
let force = mass * (9.81<m/s^2>)
printfn "Force: %.2f kg*m/s^2" (float force)  // => Force: 686.70 kg*m/s^2

// ============================================================
//  3. PATTERN MATCHING
// ============================================================
section "3. PATTERN MATCHING — match, Active Patterns"

// Pattern matching in F# is exhaustive — the compiler verifies all cases are covered.
// `when` guards add conditional logic that patterns alone can't express.
// _ is the wildcard pattern — matches anything without binding.
let classify n =
    match n with
    | 0 -> "zero"
    | n when n > 0 -> "positive"
    | _ -> "negative"

printfn "Classify: %s  %s  %s" (classify 5) (classify 0) (classify -3)  // => Classify: positive  zero  negative

// List patterns use :: (cons) for head/tail decomposition.
// [] matches empty list, [x] matches singleton, [x; y] matches exactly two elements.
// head :: _ matches any non-empty list — :: destructures into head and tail.
let describeList lst =
    match lst with
    | [] -> "empty"
    | [x] -> $"singleton: {x}"
    | [x; y] -> $"pair: {x}, {y}"
    | head :: _ -> $"starts with {head}"

printfn "List pattern: %s" (describeList [1; 2; 3])  // => List pattern: starts with 1

// `function` is shorthand for `fun x -> match x with` — combines lambda + match.
let addTuple = function
    | (0, y) -> y
    | (x, 0) -> x
    | (x, y) -> x + y
printfn "Tuple pattern: %d" (addTuple (3, 4))  // => Tuple pattern: 7

// Active Patterns let you define custom pattern matching decompositions.
// Complete active patterns (|Case1|Case2|) must cover all possibilities.
// They're functions that PRODUCE pattern cases — extending the match syntax.
let (|Even|Odd|) n = if n % 2 = 0 then Even else Odd

let parity n =
    match n with
    | Even -> "even"
    | Odd -> "odd"

printfn "Active pattern: %s  %s" (parity 4) (parity 7)  // => Active pattern: even  odd

// Partial active patterns (|Case|_|) return Option — Some for match, None for no match.
// The |_| in the name signals "this pattern might not match."
// They're composable: you can use multiple partial patterns in the same match expression.
let (|DivisibleBy|_|) divisor n =
    if n % divisor = 0 then Some(n / divisor) else None

let fizzBuzz n =
    match n with
    | DivisibleBy 15 _ -> "FizzBuzz"
    | DivisibleBy 3 _ -> "Fizz"
    | DivisibleBy 5 _ -> "Buzz"
    | _ -> string n

printfn "FizzBuzz: %s" (String.concat " " (List.map fizzBuzz [1..15]))  // => FizzBuzz: 1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz

// ============================================================
//  4. COLLECTIONS
// ============================================================
section "4. COLLECTIONS — List, Array, Seq, Map, Set"

// F# lists are immutable, singly-linked lists — O(1) prepend, O(n) access.
// The List module provides functional operations: map, filter, fold (reduce).
// F# lists, Map, and Set are structurally-shared persistent data structures.
let nums = [1..10]
printfn "List: %A" nums  // => List: [1; 2; 3; 4; 5; 6; 7; 8; 9; 10]
printfn "List.map:    %A" (List.map (fun n -> n * 2) nums)  // => List.map:    [2; 4; 6; 8; 10; 12; 14; 16; 18; 20]
printfn "List.filter: %A" (List.filter (fun n -> n % 2 = 0) nums)  // => List.filter: [2; 4; 6; 8; 10]

// List.fold is F#'s reduce — (+) is the operator passed as a function.
// fold is left-fold; foldBack is right-fold. The first arg is the combining function,
// second is the initial accumulator, third is the list.
printfn "List.fold:   %d" (List.fold (+) 0 nums)  // => List.fold:   55
printfn "List.head:   %d  List.tail: %A" (List.head nums) (List.tail nums |> List.take 3)  // => List.head:   1  List.tail: [2; 3; 4]
printfn "List.zip:    %A" (List.zip [1;2;3] ["a";"b";"c"])  // => List.zip:    [(1, "a"); (2, "b"); (3, "c")]
printfn "List.groupBy:%A" (List.groupBy (fun n -> n % 3) nums)  // => List.groupBy:[(1, [1; 4; 7; 10]); (2, [2; 5; 8]); (0, [3; 6; 9])]

// List.choose combines filter + map: the function returns Some to keep, None to skip.
// This avoids two passes through the list (filter then map).
printfn "List.choose: %A" (List.choose (fun n -> if n % 2 = 0 then Some(n * 10) else None) nums)  // => List.choose: [20; 40; 60; 80; 100]

// List.collect is flatMap — maps each element to a list and concatenates results.
printfn "List.collect:%A" (List.collect (fun n -> [n; n * 10]) [1;2;3])  // => List.collect:[1; 10; 2; 20; 3; 30]

// List.scan is like fold but returns all intermediate accumulator values.
printfn "List.scan:   %A" (List.scan (+) 0 [1;2;3;4])  // => List.scan:   [0; 1; 3; 6; 10]

// :: (cons) prepends an element to a list in O(1) — the new list shares the tail.
let extended = 0 :: nums
printfn "Cons: %A" (List.take 5 extended)  // => Cons: [0; 1; 2; 3; 4]

// Arrays are mutable, contiguous memory — O(1) random access, same as C# arrays.
// Use arrays when you need indexing performance or interop with .NET APIs.
let arr = [| 10; 20; 30; 40; 50 |]
printfn "Array: %A  index: %d" arr arr.[2]  // => Array: [|10; 20; 30; 40; 50|]  index: 30
printfn "Array.filter: %A" (Array.filter (fun n -> n > 25) arr)  // => Array.filter: [|30; 40; 50|]

// Seq is F#'s lazy sequence — equivalent to IEnumerable<T> in C#.
// Elements are computed on demand, not upfront. Seq.unfold generates from a state function.
// This is how you model infinite sequences without blowing up memory.
let fibs =
    Seq.unfold (fun (a, b) -> Some(a, (b, a + b))) (0, 1)
    |> Seq.take 10
    |> Seq.toList
printfn "Fibonacci: %A" fibs  // => Fibonacci: [0; 1; 1; 2; 3; 5; 8; 13; 21; 34]

let infiniteEvens = Seq.initInfinite (fun i -> i * 2) |> Seq.take 5 |> Seq.toList
printfn "Seq.initInfinite: %A" infiniteEvens  // => Seq.initInfinite: [0; 2; 4; 6; 8]

// Map is an immutable dictionary backed by a balanced binary tree — O(log n) operations.
// Unlike Dictionary<K,V> (hash table), Map is persistent and structurally comparable.
// tryFind returns Option — no exceptions on missing keys.
let scores = Map.ofList [("Alice", 95); ("Bob", 87); ("Carol", 92)]
printfn "Map: %A" scores  // => Map: map [("Alice", 95); ("Bob", 87); ("Carol", 92)]
printfn "Map.find: %d" (Map.find "Alice" scores)  // => Map.find: 95
printfn "Map.tryFind: %A" (Map.tryFind "Dave" scores)  // => Map.tryFind: None
let updated = Map.add "Dave" 88 scores
printfn "Map.add: %A" updated  // => Map.add: map [("Alice", 95); ("Bob", 87); ("Carol", 92); ("Dave", 88)]

// Set is an immutable sorted set — O(log n) add/contains, structural equality.
let s1 = Set.ofList [1;2;3;4]
let s2 = Set.ofList [3;4;5;6]
printfn "Set union: %A" (Set.union s1 s2)  // => Set union: set [1; 2; 3; 4; 5; 6]
printfn "Set intersect: %A" (Set.intersect s1 s2)  // => Set intersect: set [3; 4]
printfn "Set difference: %A" (Set.difference s1 s2)  // => Set difference: set [1; 2]

// ============================================================
//  5. FUNCTIONAL PROGRAMMING
// ============================================================
section "5. FP — Currying, Partial Application, Composition"

// In F#, ALL multi-parameter functions are automatically curried.
// `let add a b = a + b` is actually `let add = fun a -> fun b -> a + b`.
// This means you can apply one arg at a time to get a specialized function.
// Currying is foundational — it's why |> and >> work so naturally in F#.
let add a b = a + b
let add5 = add 5
printfn "Curried: add5 10 = %d" (add5 10)  // => Curried: add5 10 = 15

// Partial application: fix some arguments, get a new function for the rest.
// This works because of currying — multiply 2 returns (fun b -> 2 * b).
let multiply a b = a * b
let double' = multiply 2
let triple = multiply 3
printfn "Partial: double 7 = %d  triple 7 = %d" (double' 7) (triple 7)  // => Partial: double 7 = 14  triple 7 = 21

// >> is forward function composition: (f >> g) x = g(f(x)).
// This creates new functions from existing ones without lambdas.
// Composition is associative: (f >> g) >> h = f >> (g >> h).
let square n = n * n
let negate n = -n
let squareThenNegate = square >> negate
let negateThenSquare = negate >> square
printfn "Compose >>: squareThenNegate 5 = %d" (squareThenNegate 5)  // => Compose >>: squareThenNegate 5 = -25
printfn "Compose >>: negateThenSquare 5 = %d" (negateThenSquare 5)  // => Compose >>: negateThenSquare 5 = 25

// Higher-order functions take functions as parameters or return them.
// applyTwice shows that functions are values — passed and applied like any other data.
let applyTwice f x = f (f x)
printfn "applyTwice double 3 = %d" (applyTwice double' 3)  // => applyTwice double 3 = 12

let transform items fn = List.map fn items
printfn "HOF: %A" (transform [1;2;3] (fun x -> x * x))  // => HOF: [1; 4; 9]

// ============================================================
//  6. COMPUTATION EXPRESSIONS
// ============================================================
section "6. COMPUTATION EXPRESSIONS — async, task, seq, custom"

// Computation Expressions (CEs) are F#'s generalization of monads — but more accessible.
// async { } is a CE for asynchronous programming. let! unwraps the async value (like await).
// do! runs an async operation for its side effects. return wraps a value in Async<T>.
// Unlike C# async/await, F# async is cold — it doesn't start until you run it.
// This makes composition easier: you build up async pipelines, then execute them.
let fetchData url = async {
    do! Async.Sleep 10
    return $"Data from {url}"
}

let asyncResult =
    fetchData "https://example.com"
    |> Async.RunSynchronously
printfn "Async: %s" asyncResult  // => Async: Data from https://example.com

// Async.Parallel runs multiple async operations concurrently and collects results.
let parallelResults =
    [1..5]
    |> List.map (fun i -> async { return i * i })
    |> Async.Parallel
    |> Async.RunSynchronously
printfn "Async.Parallel: %A" parallelResults  // => Async.Parallel: [|1; 4; 9; 16; 25|]

// seq { } is a CE for lazy sequences. yield produces one element; yield! produces many.
// The sequence is lazy — values are computed only when consumed by Seq.toList, for, etc.
let evens = seq {
    for i in 1..10 do
        if i % 2 = 0 then
            yield i
}
printfn "Seq expr: %A" (Seq.toList evens)  // => Seq expr: [2; 4; 6; 8; 10]

// yield! flattens a nested sequence — like SelectMany in LINQ or flatMap in other languages.
let nested = seq {
    yield! [1;2;3]
    yield! [4;5;6]
}
printfn "Seq yield!: %A" (Seq.toList nested)  // => Seq yield!: [1; 2; 3; 4; 5; 6]

// Custom CEs let you define your own monadic control flow.
// The Builder class defines how let!, return, etc. behave for your type.
// This MaybeBuilder implements the Option monad: let! unwraps Some, short-circuits on None.
// CEs are more flexible than monads — they support additional operations like yield, for,
// try/with, use, etc. This is F#'s way of embedding DSLs into the language.
type MaybeBuilder() =
    member _.Bind(opt, f) =
        match opt with
        | Some v -> f v
        | None -> None
    member _.Return(v) = Some v
    member _.ReturnFrom(opt) = opt
    member _.Zero() = None

let maybe = MaybeBuilder()

let safeDivide a b =
    if b = 0 then None else Some(a / b)

// let! in the CE calls Bind — if safeDivide returns None, the rest is skipped.
// This eliminates nested match expressions for chaining fallible operations.
let computation = maybe {
    let! x = safeDivide 10 2
    let! y = safeDivide x 0   // This will short-circuit
    return y
}
printfn "Maybe CE (short-circuit): %A" computation  // => Maybe CE (short-circuit): None

let successComputation = maybe {
    let! x = safeDivide 100 10
    let! y = safeDivide x 2
    return y
}
printfn "Maybe CE (success): %A" successComputation  // => Maybe CE (success): Some 5

// ============================================================
//  7. OOP IN F#
// ============================================================
section "7. OOP — Classes, Interfaces, Object Expressions"

// F# supports OOP for .NET interop, but idiomatic F# prefers modules + functions + DUs.
// Interfaces use abstract member syntax. Unlike C#, interface implementations are explicit —
// you must upcast (:>) to call interface methods. This prevents accidental method shadowing.
type IDescribable =
    abstract member Describe: unit -> string

// Primary constructors put parameters right after the type name.
// Members are defined with member self.Name = expr syntax.
type Animal(name: string, sound: string) =
    member _.Name = name
    member _.Sound = sound
    member _.Speak() = $"{name} says {sound}"
    interface IDescribable with
        member this.Describe() = $"Animal: {this.Name}"

type Dog(name: string) =
    inherit Animal(name, "Woof")
    member _.Fetch(item) = $"{name} fetches the {item}!"

let dog = Dog("Rex")
printfn "%s" (dog.Speak())  // => Rex says Woof
printfn "%s" (dog.Fetch("ball"))  // => Rex fetches the ball!

// :> is the upcast operator — required to access interface methods in F#.
// This explicit upcast is intentional: it makes the type conversion visible.
printfn "%s" ((dog :> IDescribable).Describe())  // => Animal: Rex

// Object expressions create anonymous interface implementations inline — no class needed.
// Like Kotlin's object expressions or Java's anonymous classes, but more concise.
// Great for one-off implementations in tests or callbacks.
let describable =
    { new IDescribable with
        member _.Describe() = "Anonymous describable" }
printfn "Object expression: %s" (describable.Describe())  // => Object expression: Anonymous describable

// Type extensions add members to existing types — like C# extension methods but more natural.
// Intrinsic extensions (in the same file/namespace) become real members of the type.
// Optional extensions (in different files) work like C# extension methods.
type System.Int32 with
    member this.IsEven = this % 2 = 0
    member this.Factorial =
        let rec fact n = if n <= 1 then 1 else n * fact (n - 1)
        fact this

printfn "Extension: 4.IsEven=%b  5.Factorial=%d" (4).IsEven (5).Factorial  // => Extension: 4.IsEven=true  5.Factorial=120

// ============================================================
//  8. ERROR HANDLING
// ============================================================
section "8. ERROR HANDLING — Result, Option, Railway"

// Option<T> is F#'s null-safe type — Some value or None. No NullReferenceExceptions.
// Pattern matching on Option forces you to handle the None case — the compiler ensures it.
// This is F#'s answer to Tony Hoare's "billion dollar mistake" (null references).
let tryParseInt (s: string) =
    match Int32.TryParse(s) with
    | true, v -> Some v
    | false, _ -> None

printfn "Option: %A  %A" (tryParseInt "42") (tryParseInt "abc")  // => Option: Some 42  None

let withDefault = Option.defaultValue 0 (tryParseInt "abc")
printfn "Option.defaultValue: %d" withDefault  // => Option.defaultValue: 0

// Result<'T, 'TError> carries either a success value (Ok) or a typed error (Error).
// Unlike exceptions, Result values are explicit — the type signature tells you what can fail.
// DUs for error types (ValidationError) enumerate ALL possible failure modes.
type ValidationError =
    | TooShort of minLen: int
    | TooLong of maxLen: int
    | InvalidChars

let validateName (name: string) : Result<string, ValidationError> =
    if name.Length < 2 then Error(TooShort 2)
    elif name.Length > 50 then Error(TooLong 50)
    elif name |> Seq.exists (fun c -> not (Char.IsLetter c || c = ' ')) then Error InvalidChars
    else Ok name

printfn "Result ok: %A" (validateName "Alice")  // => Result ok: Ok "Alice"
printfn "Result err: %A" (validateName "A")  // => Result err: Error (TooShort 2)

// Railway-oriented programming chains Result-returning functions.
// bind (Result.bind) passes the Ok value forward or short-circuits on Error.
// Each step in the pipeline can fail independently — errors propagate automatically.
// The "railway" metaphor: Ok stays on the success track, Error switches to the failure track.
let bind f result =
    match result with
    | Ok v -> f v
    | Error e -> Error e

let validateAge age =
    if age >= 0 && age <= 150 then Ok age
    else Error "Invalid age"

let validateEmail (email: string) =
    if email.Contains("@") then Ok email
    else Error "Invalid email"

let validateUser name age email =
    Ok name
    |> bind (fun n -> if n.Length >= 2 then Ok n else Error "Name too short")
    |> bind (fun n ->
        validateAge age
        |> Result.map (fun a -> (n, a)))
    |> bind (fun (n, a) ->
        validateEmail email
        |> Result.map (fun e -> (n, a, e)))

printfn "Railway ok: %A" (validateUser "Alice" 30 "a@b.com")  // => Railway ok: Ok ("Alice", 30, "a@b.com")
printfn "Railway err: %A" (validateUser "A" 30 "a@b.com")  // => Railway err: Error "Name too short"

// ============================================================
//  9. ADVANCED
// ============================================================
section "9. ADVANCED — Quotations, MailboxProcessor"

// Code quotations capture F# expressions as data — similar to LINQ expression trees.
// <@ expr @> creates a typed quotation (Expr<T>). Used by type providers and query DSLs
// to translate F# code into SQL, JavaScript, or GPU kernels at compile/runtime.
let expr = <@ 1 + 2 * 3 @>
printfn "Quotation: %A" expr  // => Quotation: Call (None, op_Addition, [Value (1), Call (None, op_Multiply, [Value (2), Value (3)])])

let exprWithVar = <@ fun x -> x * x + 1 @>
printfn "Quotation fn: %A" exprWithVar  // => (varies)

// MailboxProcessor is F#'s actor model — a message-processing loop with an inbox queue.
// Each agent processes messages sequentially (no concurrency within an agent).
// Messages are DU cases, and the agent pattern-matches on them.
// This is the same actor pattern as Erlang/Akka — isolated state, message-passing concurrency.
// Post is fire-and-forget; PostAndReply sends a message and waits for the response.
type CounterMsg =
    | Increment
    | Decrement
    | Get of AsyncReplyChannel<int>

let counterAgent = MailboxProcessor.Start(fun inbox ->
    let rec loop count = async {
        let! msg = inbox.Receive()
        match msg with
        | Increment -> return! loop (count + 1)
        | Decrement -> return! loop (count - 1)
        | Get channel ->
            channel.Reply(count)
            return! loop count
    }
    loop 0)

counterAgent.Post(Increment)
counterAgent.Post(Increment)
counterAgent.Post(Increment)
counterAgent.Post(Decrement)
let agentResult = counterAgent.PostAndReply(fun ch -> Get ch)
printfn "MailboxProcessor: %d" agentResult  // => MailboxProcessor: 2

// Recursive DUs model ASTs (Abstract Syntax Trees) — a natural fit for interpreters,
// compilers, and expression evaluators. The rec keyword enables mutual/self-recursion.
type Expr =
    | Num of float
    | Add of Expr * Expr
    | Mul of Expr * Expr

let rec eval expr =
    match expr with
    | Num n -> n
    | Add(a, b) -> eval a + eval b
    | Mul(a, b) -> eval a * eval b

let expression = Add(Mul(Num 3.0, Num 4.0), Num 5.0)
printfn "Expr eval (3*4+5): %.0f" (eval expression)  // => Expr eval (3*4+5): 17

// Memoization wraps a function with a cache. In F#, functions are values, so you can
// wrap any function transparently. The Dictionary provides O(1) lookup for repeated calls.
// This is a closure — the cache dictionary is captured by the returned function.
let memoize f =
    let cache = System.Collections.Generic.Dictionary<_, _>()
    fun x ->
        match cache.TryGetValue(x) with
        | true, v -> v
        | false, _ ->
            let v = f x
            cache.[x] <- v
            v

let slowSquare = memoize (fun n ->
    System.Threading.Thread.Sleep(1)
    n * n)
printfn "Memoized: %d %d" (slowSquare 5) (slowSquare 5)  // => Memoized: 25 25

// Statically resolved type parameters (^a) use compile-time duck typing.
// inline functions are expanded at each call site, enabling constraints like (+) and GenericZero
// that work across int, float, decimal, etc. This is more powerful than C# generics
// because it uses structural typing (member constraints) rather than interface constraints.
let inline average (xs: ^a list) =
    let sum = List.fold (+) LanguagePrimitives.GenericZero xs
    let count = List.length xs
    LanguagePrimitives.DivideByInt sum count

printfn "Generic average: %.2f" (average [1.0; 2.0; 3.0; 4.0; 5.0])  // => Generic average: 3.00

printfn "\n%s" (String.replicate 60 "=")
printfn "  All sections complete!"  // => All sections complete!
printfn "%s" (String.replicate 60 "=")
