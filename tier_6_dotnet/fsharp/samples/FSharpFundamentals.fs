// F# Fundamentals: Beginner to Advanced — Standard Library Only.
//
// A dense, runnable syntax reference covering core F# concepts.
// Run: dotnet fsi FSharpFundamentals.fs
// Requires: .NET 7+ / F# 7+

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

// --- let bindings (immutable by default) ---
let x = 42
let pi = 3.14159
let name = "F#"
let flag = true
printfn "int=%d  float=%f  string=%s  bool=%b" x pi name flag

// --- Mutable ---
let mutable counter = 0
counter <- counter + 1
printfn "Mutable counter: %d" counter

// --- Type annotations (optional, inferred) ---
let greet (person: string) : string = $"Hello, {person}!"
printfn "%s" (greet "Alice")

// --- Pipe operator ---
let result =
    "  Hello, World!  "
    |> fun s -> s.Trim()
    |> fun s -> s.ToLower()
    |> fun s -> s.Split(' ')
    |> Array.toList
printfn "Pipe: %A" result

// --- Backward pipe ---
let doubled = (fun x -> x * 2) <| 21
printfn "Backward pipe: %d" doubled

// --- String formatting ---
printfn "Interpolated: %s is version %d" name 7
printfn $"String interpolation: {name} {1 + 1}"
printfn "sprintf: %s" (sprintf "Pi is %.4f" pi)

// ============================================================
//  2. TYPES
// ============================================================
section "2. TYPES — Discriminated Unions, Records, Tuples, Units of Measure"

// --- Tuples ---
let point = (3, 4)
let (px, py) = point
printfn "Tuple: %A  fst=%d  snd=%d" point (fst point) (snd point)

// --- Records ---
type Person = { Name: string; Age: int }

let alice = { Name = "Alice"; Age = 30 }
let olderAlice = { alice with Age = 31 }
printfn "Record: %A" alice
printfn "Updated: %A" olderAlice
printfn "Equality: %b" (alice = { Name = "Alice"; Age = 30 })

// --- Discriminated Unions ---
type Shape =
    | Circle of radius: float
    | Rectangle of width: float * height: float
    | Triangle of a: float * b: float * c: float

let area shape =
    match shape with
    | Circle r -> Math.PI * r * r
    | Rectangle(w, h) -> w * h
    | Triangle(a, b, c) ->
        let s = (a + b + c) / 2.0
        sqrt (s * (s - a) * (s - b) * (s - c))

printfn "Circle area: %.2f" (area (Circle 5.0))
printfn "Rect area: %.2f" (area (Rectangle(4.0, 6.0)))

// --- Option type ---
type Tree =
    | Leaf of int
    | Node of Tree * Tree

let rec treeSum tree =
    match tree with
    | Leaf v -> v
    | Node(left, right) -> treeSum left + treeSum right

let sampleTree = Node(Node(Leaf 1, Leaf 2), Leaf 3)
printfn "Tree sum: %d" (treeSum sampleTree)

// --- Single-case DU (wrapper type) ---
type Email = Email of string
let (Email addr) = Email "alice@example.com"
printfn "Single-case DU: %s" addr

// --- Units of Measure ---
[<Measure>] type m
[<Measure>] type s
[<Measure>] type kg

let distance = 100.0<m>
let time = 9.58<s>
let speed = distance / time
printfn "Speed: %.2f m/s" (float speed)

let mass = 70.0<kg>
let force = mass * (9.81<m/s^2>)
printfn "Force: %.2f kg*m/s^2" (float force)

// ============================================================
//  3. PATTERN MATCHING
// ============================================================
section "3. PATTERN MATCHING — match, Active Patterns"

// --- Basic match ---
let classify n =
    match n with
    | 0 -> "zero"
    | n when n > 0 -> "positive"
    | _ -> "negative"

printfn "Classify: %s  %s  %s" (classify 5) (classify 0) (classify -3)

// --- List patterns ---
let describeList lst =
    match lst with
    | [] -> "empty"
    | [x] -> $"singleton: {x}"
    | [x; y] -> $"pair: {x}, {y}"
    | head :: _ -> $"starts with {head}"

printfn "List pattern: %s" (describeList [1; 2; 3])

// --- Tuple pattern ---
let addTuple = function
    | (0, y) -> y
    | (x, 0) -> x
    | (x, y) -> x + y
printfn "Tuple pattern: %d" (addTuple (3, 4))

// --- Active Patterns (complete) ---
let (|Even|Odd|) n = if n % 2 = 0 then Even else Odd

let parity n =
    match n with
    | Even -> "even"
    | Odd -> "odd"

printfn "Active pattern: %s  %s" (parity 4) (parity 7)

// --- Partial Active Pattern ---
let (|DivisibleBy|_|) divisor n =
    if n % divisor = 0 then Some(n / divisor) else None

let fizzBuzz n =
    match n with
    | DivisibleBy 15 _ -> "FizzBuzz"
    | DivisibleBy 3 _ -> "Fizz"
    | DivisibleBy 5 _ -> "Buzz"
    | _ -> string n

printfn "FizzBuzz: %s" (String.concat " " (List.map fizzBuzz [1..15]))

// ============================================================
//  4. COLLECTIONS
// ============================================================
section "4. COLLECTIONS — List, Array, Seq, Map, Set"

// --- List ---
let nums = [1..10]
printfn "List: %A" nums
printfn "List.map:    %A" (List.map (fun n -> n * 2) nums)
printfn "List.filter: %A" (List.filter (fun n -> n % 2 = 0) nums)
printfn "List.fold:   %d" (List.fold (+) 0 nums)
printfn "List.head:   %d  List.tail: %A" (List.head nums) (List.tail nums |> List.take 3)
printfn "List.zip:    %A" (List.zip [1;2;3] ["a";"b";"c"])
printfn "List.groupBy:%A" (List.groupBy (fun n -> n % 3) nums)
printfn "List.choose: %A" (List.choose (fun n -> if n % 2 = 0 then Some(n * 10) else None) nums)
printfn "List.collect:%A" (List.collect (fun n -> [n; n * 10]) [1;2;3])
printfn "List.scan:   %A" (List.scan (+) 0 [1;2;3;4])

// --- Cons operator ---
let extended = 0 :: nums
printfn "Cons: %A" (List.take 5 extended)

// --- Array ---
let arr = [| 10; 20; 30; 40; 50 |]
printfn "Array: %A  index: %d" arr arr.[2]
printfn "Array.filter: %A" (Array.filter (fun n -> n > 25) arr)

// --- Seq (lazy) ---
let fibs =
    Seq.unfold (fun (a, b) -> Some(a, (b, a + b))) (0, 1)
    |> Seq.take 10
    |> Seq.toList
printfn "Fibonacci: %A" fibs

let infiniteEvens = Seq.initInfinite (fun i -> i * 2) |> Seq.take 5 |> Seq.toList
printfn "Seq.initInfinite: %A" infiniteEvens

// --- Map ---
let scores = Map.ofList [("Alice", 95); ("Bob", 87); ("Carol", 92)]
printfn "Map: %A" scores
printfn "Map.find: %d" (Map.find "Alice" scores)
printfn "Map.tryFind: %A" (Map.tryFind "Dave" scores)
let updated = Map.add "Dave" 88 scores
printfn "Map.add: %A" updated

// --- Set ---
let s1 = Set.ofList [1;2;3;4]
let s2 = Set.ofList [3;4;5;6]
printfn "Set union: %A" (Set.union s1 s2)
printfn "Set intersect: %A" (Set.intersect s1 s2)
printfn "Set difference: %A" (Set.difference s1 s2)

// ============================================================
//  5. FUNCTIONAL PROGRAMMING
// ============================================================
section "5. FP — Currying, Partial Application, Composition"

// --- Currying (automatic) ---
let add a b = a + b
let add5 = add 5
printfn "Curried: add5 10 = %d" (add5 10)

// --- Partial application ---
let multiply a b = a * b
let double' = multiply 2
let triple = multiply 3
printfn "Partial: double 7 = %d  triple 7 = %d" (double' 7) (triple 7)

// --- Function composition ---
let square n = n * n
let negate n = -n
let squareThenNegate = square >> negate
let negateThenSquare = negate >> square
printfn "Compose >>: squareThenNegate 5 = %d" (squareThenNegate 5)
printfn "Compose >>: negateThenSquare 5 = %d" (negateThenSquare 5)

// --- Higher-order functions ---
let applyTwice f x = f (f x)
printfn "applyTwice double 3 = %d" (applyTwice double' 3)

// --- Function as parameter ---
let transform items fn = List.map fn items
printfn "HOF: %A" (transform [1;2;3] (fun x -> x * x))

// ============================================================
//  6. COMPUTATION EXPRESSIONS
// ============================================================
section "6. COMPUTATION EXPRESSIONS — async, task, seq, custom"

// --- Async ---
let fetchData url = async {
    do! Async.Sleep 10
    return $"Data from {url}"
}

let asyncResult =
    fetchData "https://example.com"
    |> Async.RunSynchronously
printfn "Async: %s" asyncResult

// --- Parallel async ---
let parallelResults =
    [1..5]
    |> List.map (fun i -> async { return i * i })
    |> Async.Parallel
    |> Async.RunSynchronously
printfn "Async.Parallel: %A" parallelResults

// --- Seq expression ---
let evens = seq {
    for i in 1..10 do
        if i % 2 = 0 then
            yield i
}
printfn "Seq expr: %A" (Seq.toList evens)

let nested = seq {
    yield! [1;2;3]
    yield! [4;5;6]
}
printfn "Seq yield!: %A" (Seq.toList nested)

// --- Custom computation expression (Maybe/Option) ---
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

let computation = maybe {
    let! x = safeDivide 10 2
    let! y = safeDivide x 0   // This will short-circuit
    return y
}
printfn "Maybe CE (short-circuit): %A" computation

let successComputation = maybe {
    let! x = safeDivide 100 10
    let! y = safeDivide x 2
    return y
}
printfn "Maybe CE (success): %A" successComputation

// ============================================================
//  7. OOP IN F#
// ============================================================
section "7. OOP — Classes, Interfaces, Object Expressions"

// --- Interface ---
type IDescribable =
    abstract member Describe: unit -> string

// --- Class ---
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
printfn "%s" (dog.Speak())
printfn "%s" (dog.Fetch("ball"))
printfn "%s" ((dog :> IDescribable).Describe())

// --- Object expression (anonymous interface implementation) ---
let describable =
    { new IDescribable with
        member _.Describe() = "Anonymous describable" }
printfn "Object expression: %s" (describable.Describe())

// --- Type extensions ---
type System.Int32 with
    member this.IsEven = this % 2 = 0
    member this.Factorial =
        let rec fact n = if n <= 1 then 1 else n * fact (n - 1)
        fact this

printfn "Extension: 4.IsEven=%b  5.Factorial=%d" (4).IsEven (5).Factorial

// ============================================================
//  8. ERROR HANDLING
// ============================================================
section "8. ERROR HANDLING — Result, Option, Railway"

// --- Option ---
let tryParseInt (s: string) =
    match Int32.TryParse(s) with
    | true, v -> Some v
    | false, _ -> None

printfn "Option: %A  %A" (tryParseInt "42") (tryParseInt "abc")

let withDefault = Option.defaultValue 0 (tryParseInt "abc")
printfn "Option.defaultValue: %d" withDefault

// --- Result type ---
type ValidationError =
    | TooShort of minLen: int
    | TooLong of maxLen: int
    | InvalidChars

let validateName (name: string) : Result<string, ValidationError> =
    if name.Length < 2 then Error(TooShort 2)
    elif name.Length > 50 then Error(TooLong 50)
    elif name |> Seq.exists (fun c -> not (Char.IsLetter c || c = ' ')) then Error InvalidChars
    else Ok name

printfn "Result ok: %A" (validateName "Alice")
printfn "Result err: %A" (validateName "A")

// --- Railway-oriented programming ---
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

printfn "Railway ok: %A" (validateUser "Alice" 30 "a@b.com")
printfn "Railway err: %A" (validateUser "A" 30 "a@b.com")

// ============================================================
//  9. ADVANCED
// ============================================================
section "9. ADVANCED — Quotations, MailboxProcessor"

// --- Code quotations ---
let expr = <@ 1 + 2 * 3 @>
printfn "Quotation: %A" expr

let exprWithVar = <@ fun x -> x * x + 1 @>
printfn "Quotation fn: %A" exprWithVar

// --- MailboxProcessor (agent) ---
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
printfn "MailboxProcessor: %d" agentResult

// --- Recursive types & computation ---
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
printfn "Expr eval (3*4+5): %.0f" (eval expression)

// --- Memoization ---
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
printfn "Memoized: %d %d" (slowSquare 5) (slowSquare 5)

// --- Computation with measures ---
let inline average (xs: ^a list) =
    let sum = List.fold (+) LanguagePrimitives.GenericZero xs
    let count = List.length xs
    LanguagePrimitives.DivideByInt sum count

printfn "Generic average: %.2f" (average [1.0; 2.0; 3.0; 4.0; 5.0])

printfn "\n%s" (String.replicate 60 "=")
printfn "  All sections complete!"
printfn "%s" (String.replicate 60 "=")
