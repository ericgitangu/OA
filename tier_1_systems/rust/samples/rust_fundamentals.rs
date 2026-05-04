// rust_fundamentals.rs — Comprehensive Rust fundamentals (std only)
// Compile & run: rustc rust_fundamentals.rs && ./rust_fundamentals

use std::collections::{BTreeMap, BinaryHeap, HashMap, HashSet, VecDeque};
use std::cell::RefCell;
use std::fmt;
use std::marker::PhantomData;
use std::rc::Rc;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::{mpsc, Arc, Mutex};
use std::thread;
use std::borrow::Cow;

fn header(title: &str) {
    println!("\n{}", "=".repeat(60));
    println!("  {title}");
    println!("{}", "=".repeat(60));
}

// ─── 1. Basics ──────────────────────────────────────────────
fn basics() {
    header("1. BASICS — Variables, Types, Tuples, Arrays");

    // Rust variables are immutable by default — this is a deliberate design choice that
    // makes code easier to reason about. The compiler can also optimize better when it
    // knows a value won't change. Use `mut` only when you actually need mutation.
    let x = 42;
    let mut y = 10;
    y += x;
    println!("x = {x}, y (mutated) = {y}");  // => x = 42, y (mutated) = 52

    // Shadowing lets you reuse a name with a different type. Unlike `mut`, shadowing
    // creates a new binding entirely — the old `val` (&str) is gone, replaced by an i32.
    // This is idiomatic for type transformations in a pipeline, avoiding names like val_str/val_int.
    let val = "123";
    let val: i32 = val.parse().unwrap();
    println!("Shadowed val: {val}");  // => Shadowed val: 123

    // Rust has no implicit numeric coercion — you must cast explicitly (e.g., `x as f64`).
    // char is 4 bytes (full Unicode scalar value), not 1 byte like C. The _ in 9_000_000
    // is a visual separator ignored by the compiler (like commas in English numbers).
    let _byte: u8 = 255;
    let _signed: i64 = -9_000_000;
    let _float: f64 = 3.141_592_653;
    let _flag: bool = true;
    let _ch: char = 'R';
    println!("Scalars — u8: {_byte}, i64: {_signed}, f64: {_float}, bool: {_flag}, char: {_ch}");  // => Scalars — u8: 255, i64: -9000000, f64: 3.141592653, bool: true, char: R

    // Tuples are fixed-size, heterogeneous collections. Destructuring with `let (a, b, c)`
    // is pattern matching — the compiler verifies you match the exact structure.
    // Access by index (tup.2) uses a literal integer, not a variable — it's resolved at compile time.
    let tup: (i32, f64, &str) = (1, 2.5, "hello");
    let (a, b, c) = tup;
    println!("Tuple destructured: a={a}, b={b}, c={c}, index: {}", tup.2);  // => Tuple destructured: a=1, b=2.5, c=hello, index: hello

    // Arrays are fixed-size and stack-allocated — the size is part of the type ([i32; 5]).
    // Slicing with &arr[1..3] creates a borrowed slice (&[i32]) — a fat pointer containing
    // a pointer to the data and a length. Slices are bounds-checked at runtime, unlike C arrays.
    let arr = [10, 20, 30, 40, 50];
    println!("Array slice [1..3]: {:?}", &arr[1..3]);  // => Array slice [1..3]: [20, 30]
    println!("Array length: {}", arr.len());  // => Array length: 5
}

// ─── 2. Ownership ───────────────────────────────────────────
fn ownership() {
    header("2. OWNERSHIP — Move, Borrow, References, Lifetimes");

    // Move semantics: when you assign a heap-allocated type (String, Vec, etc.), ownership
    // transfers to the new binding. s1 is invalidated — the borrow checker prevents use-after-move
    // at compile time. This is Rust's alternative to garbage collection: exactly one owner,
    // automatic deallocation when the owner goes out of scope (RAII/drop).
    let s1 = String::from("hello");
    let s2 = s1; // s1 moved — its pointer, length, and capacity are now in s2
    // println!("{s1}"); // would not compile — use-after-move error
    println!("After move: s2 = {s2}");  // => After move: s2 = hello

    // clone() performs a deep copy — new heap allocation with duplicated data. Use it
    // when you genuinely need two independent copies. It's explicit and visible in code,
    // unlike C++ where copies can happen silently through implicit copy constructors.
    let s3 = s2.clone();
    println!("Cloned: s2 = {s2}, s3 = {s3}");  // => Cloned: s2 = hello, s3 = hello

    // Borrowing: &String is an immutable reference — it lets calc_len read s without taking
    // ownership. The caller keeps ownership, so s2 is still valid after the call.
    // You can have unlimited immutable borrows simultaneously.
    fn calc_len(s: &String) -> usize { s.len() }
    println!("Length of s2 (borrowed): {}", calc_len(&s2));  // => Length of s2 (borrowed): 5

    // Mutable reference: &mut String gives exclusive write access. The borrow checker enforces
    // that you can have EITHER one &mut OR any number of & — never both at the same time.
    // This prevents data races at compile time, which is Rust's key safety guarantee.
    let mut s4 = String::from("hello");
    fn append(s: &mut String) { s.push_str(", world"); }
    append(&mut s4);
    println!("After mutable borrow: {s4}");  // => After mutable borrow: hello, world

    // Lifetime annotations ('a) tell the compiler how long references are valid. The signature
    // `longest<'a>(x: &'a str, y: &'a str) -> &'a str` means: the returned reference lives
    // at least as long as the shorter of x and y's lifetimes. Without this, the compiler can't
    // verify the returned reference won't dangle. Lifetimes are purely compile-time — zero runtime cost.
    fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
        if x.len() >= y.len() { x } else { y }
    }
    let result;
    let str_a = String::from("long string");
    {
        let str_b = String::from("short");
        result = longest(str_a.as_str(), str_b.as_str());
        // result must be used before str_b is dropped — the lifetime 'a is bounded
        // by str_b's scope since both inputs share the same lifetime parameter.
        println!("Longest: {result}");  // => Longest: long string
    }

    // Structs can borrow data instead of owning it, but then they need lifetime annotations
    // to prove the borrowed data outlives the struct. This is a compile-time contract:
    // `Excerpt` can never outlive the string it references.
    #[derive(Debug)]
    struct Excerpt<'a> {
        #[allow(dead_code)]
        part: &'a str,
    }
    let novel = String::from("Call me Ishmael. Some years ago...");
    let first_sentence = novel.split('.').next().unwrap();
    let excerpt = Excerpt { part: first_sentence };
    println!("Excerpt: {:?}", excerpt);  // => Excerpt: Excerpt { part: "Call me Ishmael" }
}

// ─── 3. Structs & Enums ────────────────────────────────────
fn structs_and_enums() {
    header("3. STRUCTS & ENUMS — Methods, Option, Result, Pattern Matching");

    #[derive(Debug)]
    struct Rect { width: f64, height: f64 }

    // impl blocks attach methods to a struct. `Self` is an alias for the struct type.
    // `fn new()` is an associated function (no self) — Rust's convention for constructors.
    // `&self` borrows immutably, `&mut self` borrows mutably — the method signature
    // declares how it accesses the struct, enforced by the borrow checker.
    impl Rect {
        fn new(w: f64, h: f64) -> Self { Self { width: w, height: h } }
        fn area(&self) -> f64 { self.width * self.height }
        fn scale(&mut self, factor: f64) {
            self.width *= factor;
            self.height *= factor;
        }
    }

    let mut r = Rect::new(10.0, 5.0);
    println!("Rect area: {}", r.area());  // => Rect area: 50
    r.scale(2.0);
    println!("Scaled rect: {:?}, area: {}", r, r.area());  // => Scaled rect: Rect { width: 20.0, height: 10.0 }, area: 200

    // Rust enums are algebraic data types (ADTs) — each variant can hold different data.
    // This is fundamentally different from C/Java enums which are just named integers.
    // Circle holds one f64, Rectangle holds two, Triangle uses named fields.
    // Combined with match, enums enable exhaustive pattern matching — the compiler ensures
    // you handle every variant, so adding a new variant causes compile errors at all match sites.
    #[derive(Debug)]
    enum Shape {
        Circle(f64),
        Rectangle(f64, f64),
        Triangle { base: f64, height: f64 },
    }

    impl Shape {
        fn area(&self) -> f64 {
            // match is exhaustive — you must cover every variant or use a wildcard `_`.
            // Each arm destructures the variant, binding its inner data to local variables.
            match self {
                Shape::Circle(r) => std::f64::consts::PI * r * r,
                Shape::Rectangle(w, h) => w * h,
                Shape::Triangle { base, height } => 0.5 * base * height,
            }
        }
    }

    let shapes = vec![
        Shape::Circle(5.0),
        Shape::Rectangle(4.0, 6.0),
        Shape::Triangle { base: 3.0, height: 8.0 },
    ];
    for s in &shapes {
        println!("{:?} -> area = {:.2}", s, s.area());  // => Circle(5.0) -> area = 78.54 / Rectangle(4.0, 6.0) -> area = 24.00 / Triangle { base: 3.0, height: 8.0 } -> area = 12.00
    }

    // Option<T> replaces null — it's an enum with Some(value) and None. The compiler forces
    // you to handle the None case, eliminating null pointer exceptions entirely.
    // .get() returns Option<&T> for safe bounds-checked access (vs [] which panics).
    let nums = vec![2, 4, 6];
    match nums.get(10) {
        Some(v) => println!("Found: {v}"),
        None => println!("Index 10 out of bounds (Option::None)"),  // => Index 10 out of bounds (Option::None)
    }

    // Result<T, E> is the idiomatic way to handle recoverable errors. Like Option, the
    // compiler forces you to handle the error case. No exceptions, no unchecked error codes.
    fn safe_div(a: f64, b: f64) -> Result<f64, String> {
        if b == 0.0 { Err("division by zero".into()) } else { Ok(a / b) }
    }
    println!("10 / 3 = {:?}", safe_div(10.0, 3.0));  // => 10 / 3 = Ok(3.3333333333333335)
    println!("10 / 0 = {:?}", safe_div(10.0, 0.0));  // => 10 / 0 = Err("division by zero")
}

// ─── 4. Collections ────────────────────────────────────────
fn collections() {
    header("4. COLLECTIONS — Vec, HashMap, HashSet, BTreeMap, VecDeque, BinaryHeap");

    // Vec is a growable, heap-allocated array. vec![] is a macro that creates and initializes it.
    // sort() is in-place and stable (preserves order of equal elements). dedup() removes
    // consecutive duplicates only — sort first to remove all duplicates.
    let mut v = vec![3, 1, 4, 1, 5, 9];
    v.sort();
    v.dedup();
    println!("Vec sorted+dedup: {:?}", v);  // => Vec sorted+dedup: [1, 3, 4, 5, 9]

    // entry() API is the idiomatic way to insert-or-update. or_insert(0) returns a &mut to
    // the value (existing or newly inserted), which we dereference and increment.
    // This avoids two separate lookups (contains_key + insert) — a pattern borrowed from C++ STL.
    let mut map = HashMap::new();
    for &n in &v { *map.entry(n % 3).or_insert(0) += 1; }
    println!("HashMap (n%3 -> count): {:?}", map);  // => (varies, e.g. {0: 2, 1: 2, 2: 1})

    // HashSet is a HashMap<T, ()> wrapper. Set operations (intersection, union, difference)
    // return lazy iterators — you must .collect() to materialize the result.
    // .copied() converts &i32 references to owned i32 values during iteration.
    let set: HashSet<_> = v.iter().copied().collect();
    let set2: HashSet<i32> = [1, 2, 3, 4].iter().copied().collect();
    println!("HashSet intersection: {:?}", set.intersection(&set2).collect::<Vec<_>>());  // => (varies, contains 1, 3, 4)
    println!("HashSet union: {:?}", set.union(&set2).collect::<Vec<_>>());  // => (varies, contains 1, 2, 3, 4, 5, 9)

    // BTreeMap keeps keys sorted (backed by a B-tree). Use it when you need ordered iteration
    // or range queries. HashMap is O(1) average lookup; BTreeMap is O(log n) but sorted.
    let mut btree = BTreeMap::new();
    for (i, &n) in v.iter().enumerate() { btree.insert(n, i); }
    println!("BTreeMap (sorted keys): {:?}", btree);  // => BTreeMap (sorted keys): {1: 0, 3: 1, 4: 2, 5: 3, 9: 4}

    // VecDeque is a ring buffer — O(1) push/pop on both ends, unlike Vec which is O(n)
    // for push_front. Use it for BFS queues, sliding windows, or any double-ended access pattern.
    let mut deque = VecDeque::from([1, 2, 3]);
    deque.push_front(0);
    deque.push_back(4);
    println!("VecDeque: {:?}", deque);  // => VecDeque: [0, 1, 2, 3, 4]

    // BinaryHeap is a max-heap (largest element first). Rust has no min-heap — the standard
    // workaround is wrapping values in std::cmp::Reverse. peek() is O(1), push/pop are O(log n).
    // from_fn(|| heap.pop()) drains the heap in descending order — a common heapsort pattern.
    let mut heap = BinaryHeap::from([3, 1, 4, 1, 5]);
    println!("BinaryHeap max: {:?}", heap.peek());  // => BinaryHeap max: Some(5)
    let sorted: Vec<_> = std::iter::from_fn(|| heap.pop()).collect();
    println!("Heap drain (desc): {:?}", sorted);  // => Heap drain (desc): [5, 4, 3, 1, 1]
}

// ─── 5. Traits ──────────────────────────────────────────────
fn traits_demo() {
    header("5. TRAITS — Definitions, Generics, Trait Objects, Associated Types");

    // Traits are Rust's version of interfaces — they define shared behavior. Unlike Java
    // interfaces, traits can provide default method implementations. A type opts in by
    // writing `impl TraitName for Type`. Traits are also used as bounds on generics.
    trait Describable {
        fn describe(&self) -> String;
        fn label(&self) -> &str { "unknown" } // default impl — overridable but not required
    }

    #[derive(Debug, Clone)]
    struct Dog { name: String, age: u8 }
    #[derive(Debug)]
    struct Cat { name: String }

    impl Describable for Dog {
        fn describe(&self) -> String { format!("{} the dog, age {}", self.name, self.age) }
        fn label(&self) -> &str { "canine" }
    }
    impl Describable for Cat {
        fn describe(&self) -> String { format!("{} the cat", self.name) }
        // label() uses the default impl "unknown" since Cat doesn't override it
    }

    // Generic with trait bound: `T: Describable` means this function works with ANY type
    // that implements Describable. The compiler generates specialized code for each concrete
    // type used (monomorphization) — zero-cost abstraction with no virtual dispatch overhead.
    fn print_desc<T: Describable>(item: &T) {
        println!("[{}] {}", item.label(), item.describe());
    }
    print_desc(&Dog { name: "Rex".into(), age: 5 });  // => [canine] Rex the dog, age 5
    print_desc(&Cat { name: "Whiskers".into() });  // => [unknown] Whiskers the cat

    // Trait objects (dyn Trait) enable dynamic dispatch — the concrete type is erased behind
    // a vtable pointer. Use Box<dyn Trait> when you need a heterogeneous collection of different
    // types sharing a trait. The tradeoff vs generics: runtime indirection cost, but the
    // collection can hold mixed types (Dog and Cat in the same Vec).
    let animals: Vec<Box<dyn Describable>> = vec![
        Box::new(Dog { name: "Buddy".into(), age: 3 }),
        Box::new(Cat { name: "Luna".into() }),
    ];
    for a in &animals { println!("Dyn dispatch: {}", a.describe()); }  // => Dyn dispatch: Buddy the dog, age 3 / Dyn dispatch: Luna the cat

    // Associated types are like type parameters, but fixed per implementation. Unlike
    // generics (where the caller chooses the type), associated types are chosen by the
    // implementor. Use associated types when there's exactly one logical output type per impl;
    // use generics when the same type could implement the trait with different type parameters.
    trait Converter {
        type Output;
        fn convert(&self) -> Self::Output;
    }
    impl Converter for Dog {
        type Output = String;
        fn convert(&self) -> String { format!("Dog({})", self.name) }
    }
    let d = Dog { name: "Ace".into(), age: 2 };
    println!("Associated type convert: {}", d.convert());  // => Associated type convert: Dog(Ace)
}

// ─── 6. Error Handling ──────────────────────────────────────
fn error_handling() {
    header("6. ERROR HANDLING — Custom Errors, ?, From/Into");

    // Custom error enums let you represent all failure modes of your module as one type.
    // Each variant wraps a different underlying error. In production, crates like `thiserror`
    // auto-derive Display and From impls, but understanding the manual pattern is essential.
    #[derive(Debug)]
    enum AppError {
        Parse(std::num::ParseIntError),
        Validation(String),
    }

    // Display is required for error types — it provides human-readable messages.
    // The convention is lowercase, no trailing period, for composability with format!.
    impl fmt::Display for AppError {
        fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
            match self {
                AppError::Parse(e) => write!(f, "Parse error: {e}"),
                AppError::Validation(msg) => write!(f, "Validation: {msg}"),
            }
        }
    }

    // impl From<X> for Y enables the ? operator to auto-convert error types. When
    // parse() returns Err(ParseIntError), the ? operator calls AppError::from() to wrap it.
    // This is how Rust achieves ergonomic error propagation without exceptions.
    impl From<std::num::ParseIntError> for AppError {
        fn from(e: std::num::ParseIntError) -> Self { AppError::Parse(e) }
    }

    // The ? operator is syntactic sugar for: match result { Ok(v) => v, Err(e) => return Err(e.into()) }
    // It early-returns on error and auto-converts via From. This replaces try/catch with
    // explicit, type-safe error propagation that's visible in the function signature.
    fn parse_and_validate(s: &str) -> Result<i32, AppError> {
        let n: i32 = s.parse()?; // auto-converts ParseIntError -> AppError via From
        if n < 0 { return Err(AppError::Validation("must be non-negative".into())); }
        Ok(n)
    }

    for input in &["42", "abc", "-5"] {
        match parse_and_validate(input) {
            Ok(n) => println!("  '{input}' -> Ok({n})"),  // => '42' -> Ok(42)
            Err(e) => println!("  '{input}' -> Err({e})"),  // => 'abc' -> Err(Parse error: invalid digit found in string) / '-5' -> Err(Validation: must be non-negative)
        }
    }
}

// ─── 7. Iterators ───────────────────────────────────────────
fn iterators_demo() {
    header("7. ITERATORS — map, filter, fold, collect, custom iterators");

    let nums = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

    // Iterator adapters (filter, map) are lazy — they build a chain of transformations that
    // only execute when a consumer (collect, sum, for_each) drives the iteration.
    // This means no intermediate allocations: filter+map+collect does a single pass.
    // The double reference &&n in filter comes from: iter() yields &i32, filter passes &(&i32).
    let evens_squared: Vec<i32> = nums.iter()
        .filter(|&&n| n % 2 == 0)
        .map(|&n| n * n)
        .collect();
    println!("Even squares: {:?}", evens_squared);  // => Even squares: [4, 16, 36, 64, 100]

    // sum() and fold() are consuming adapters — they take ownership of the iterator.
    // fold(initial, closure) is the most general reducer: sum, product, min, max can all
    // be expressed as folds. Rust's iterator optimizations often compile these to the
    // same machine code as hand-written loops (zero-cost abstractions).
    let sum: i32 = nums.iter().sum();
    let product: i32 = nums.iter().fold(1, |acc, &x| acc * x);
    println!("Sum: {sum}, Product: {product}");  // => Sum: 55, Product: 3628800

    // flat_map combines map + flatten: for each word, it produces a char iterator, and
    // flat_map concatenates them all into a single stream. This is the monadic bind
    // operation — equivalent to SelectMany in C# or >>= in Haskell.
    let words = vec!["hello", "world"];
    let chars: Vec<char> = words.iter().flat_map(|w| w.chars()).collect();
    println!("Flattened chars: {:?}", chars);  // => Flattened chars: ['h', 'e', 'l', 'l', 'o', 'w', 'o', 'r', 'l', 'd']

    // zip pairs elements from two iterators. (0..) is an infinite range — zip stops when
    // the shorter iterator runs out. This is idiomatic for attaching indices.
    let pairs: Vec<_> = (0..).zip(words.iter()).collect();
    println!("Zipped with index: {:?}", pairs);  // => Zipped with index: [(0, "hello"), (1, "world")]

    // Custom iterators implement the Iterator trait, which requires only next() -> Option<Item>.
    // Returning None signals the end of iteration. All adapter methods (map, filter, take, etc.)
    // are provided for free by the trait's default implementations — you get a full iterator
    // toolkit by implementing just one method.
    struct Fib { a: u64, b: u64 }
    impl Fib { fn new() -> Self { Fib { a: 0, b: 1 } } }
    impl Iterator for Fib {
        type Item = u64;
        fn next(&mut self) -> Option<u64> {
            let val = self.a;
            self.a = self.b;
            self.b = val + self.b;
            Some(val)
        }
    }
    // take(12) limits an infinite iterator. Without it, collect() would loop forever.
    let fibs: Vec<u64> = Fib::new().take(12).collect();
    println!("Fibonacci (12): {:?}", fibs);  // => Fibonacci (12): [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

    // partition splits an iterator into two collections based on a predicate. The type
    // annotation is required because partition can produce any FromIterator type.
    let (evens, odds): (Vec<&i32>, Vec<&i32>) = nums.iter().partition(|&&n| n % 2 == 0);
    println!("Partition — evens: {:?}, odds: {:?}", evens, odds);  // => Partition — evens: [2, 4, 6, 8, 10], odds: [1, 3, 5, 7, 9]
}

// ─── 8. Closures ────────────────────────────────────────────
fn closures_demo() {
    header("8. CLOSURES — Fn, FnMut, FnOnce, move, returning closures");

    // Rust closures have three traits based on how they capture variables:
    // Fn — borrows captured variables immutably (can be called multiple times concurrently)
    // FnMut — borrows mutably (can be called multiple times, but not concurrently)
    // FnOnce — takes ownership (can only be called once, consumes captured values)
    // The compiler infers the most permissive trait automatically.

    // Fn: greeting is captured by immutable reference — the closure can read it but not modify.
    // Multiple calls are fine because no mutation occurs.
    let greeting = String::from("Hello");
    let greet = |name: &str| println!("{greeting}, {name}!");
    greet("Alice");  // => Hello, Alice!
    greet("Bob");  // => Hello, Bob!

    // FnMut: count is captured by mutable reference. The closure mutates it on each call.
    // The closure itself must be declared `mut` because calling it modifies captured state.
    let mut count = 0;
    let mut counter = || { count += 1; count };
    println!("Counter: {}, {}, {}", counter(), counter(), counter());  // => Counter: 1, 2, 3

    // FnOnce + move: `move` forces the closure to take ownership of all captured variables.
    // Since the closure returns `data` (moving it out), it can only be called once — hence FnOnce.
    // Without `move`, the closure would borrow `data`, and you couldn't return it.
    let data = vec![1, 2, 3];
    let consume = move || {
        println!("Consumed data: {:?}", data);  // => Consumed data: [1, 2, 3]
        data // returns owned data
    };
    let _recovered = consume();
    // consume(); // can't call again — FnOnce consumed the captured data

    // Closures can't be returned directly because their types are anonymous (each closure
    // has a unique, unnameable type). Box<dyn Fn> uses dynamic dispatch to erase the type.
    // `move` is required here so the closure owns `x` — otherwise `x` would be a dangling
    // reference after make_adder returns.
    fn make_adder(x: i32) -> Box<dyn Fn(i32) -> i32> {
        Box::new(move |y| x + y)
    }
    let add5 = make_adder(5);
    println!("make_adder(5)(10) = {}", add5(10));  // => make_adder(5)(10) = 15

    // Generic trait bounds on closures: `F: Fn(i32) -> i32` accepts any closure/function
    // with that signature. This uses static dispatch (monomorphization) — zero overhead
    // compared to Box<dyn Fn> which has vtable indirection.
    fn apply_twice<F: Fn(i32) -> i32>(f: F, x: i32) -> i32 { f(f(x)) }
    println!("apply_twice(|x| x*2, 3) = {}", apply_twice(|x| x * 2, 3));  // => apply_twice(|x| x*2, 3) = 12
}

// ─── 9. Smart Pointers ─────────────────────────────────────
fn smart_pointers() {
    header("9. SMART POINTERS — Box, Rc, Arc, RefCell, Cow");

    // Box<T> allocates T on the heap and provides a unique owning pointer. It's needed for:
    // 1. Recursive types (the compiler can't determine size of a self-referential struct)
    // 2. Large data you want on the heap, not the stack
    // 3. Trait objects (Box<dyn Trait>)
    // Box has zero overhead beyond the heap allocation — dereferencing is a single pointer follow.
    #[derive(Debug)]
    #[allow(dead_code)]
    enum List { Cons(i32, Box<List>), Nil }
    let list = List::Cons(1, Box::new(List::Cons(2, Box::new(List::Cons(3, Box::new(List::Nil))))));
    println!("Boxed linked list: {:?}", list);  // => Boxed linked list: Cons(1, Cons(2, Cons(3, Nil)))

    // Rc<T> (Reference Counted) enables shared ownership — multiple owners of the same data.
    // Rc::clone() increments the reference count (cheap — no deep copy). The data is freed
    // when the last Rc is dropped and the count reaches zero.
    // Rc is NOT thread-safe (no atomic operations) — use Arc for multithreaded sharing.
    let shared = Rc::new(String::from("shared data"));
    let a = Rc::clone(&shared);
    let b = Rc::clone(&shared);
    println!("Rc strong count: {} (a={a}, b={b})", Rc::strong_count(&shared));  // => Rc strong count: 3 (a=shared data, b=shared data)

    // RefCell<T> provides interior mutability — it moves borrow checking from compile time
    // to runtime. borrow() and borrow_mut() return smart guards that panic if you violate
    // the borrowing rules (e.g., two simultaneous mutable borrows). Use it when the compiler
    // can't prove your borrowing is safe but you know it is.
    let cell = RefCell::new(vec![1, 2, 3]);
    cell.borrow_mut().push(4);
    println!("RefCell contents: {:?}", cell.borrow());  // => RefCell contents: [1, 2, 3, 4]

    // Rc<RefCell<T>> is the common pattern for shared mutable state in single-threaded code.
    // Rc provides shared ownership, RefCell provides mutability — together they give you
    // something like a garbage-collected mutable reference. This is the escape hatch when
    // the borrow checker's static analysis is too restrictive for your data structure (e.g., graphs).
    let shared_vec = Rc::new(RefCell::new(Vec::new()));
    let clone1 = Rc::clone(&shared_vec);
    let clone2 = Rc::clone(&shared_vec);
    clone1.borrow_mut().push("from clone1");
    clone2.borrow_mut().push("from clone2");
    println!("Rc<RefCell<Vec>>: {:?}", shared_vec.borrow());  // => Rc<RefCell<Vec>>: ["from clone1", "from clone2"]

    // Cow (Clone on Write) is an optimization for the read-mostly case. It starts as a
    // borrowed reference (zero-cost) and only allocates a clone when mutation is needed.
    // In production, use Cow for functions that usually return the input unchanged but
    // occasionally need to transform it — avoids allocation in the common path.
    fn maybe_uppercase(s: &str, upper: bool) -> Cow<'_, str> {
        if upper { Cow::Owned(s.to_uppercase()) } else { Cow::Borrowed(s) }
    }
    println!("Cow borrowed: {}", maybe_uppercase("hello", false));  // => Cow borrowed: hello
    println!("Cow owned:    {}", maybe_uppercase("hello", true));  // => Cow owned:    HELLO
}

// ─── 10. Concurrency ───────────────────────────────────────
fn concurrency() {
    header("10. CONCURRENCY — Threads, Channels, Mutex, Arc+Mutex, Atomics");

    // thread::spawn creates an OS thread. The closure must be 'static + Send — meaning it
    // can't borrow from the spawning thread (use move to transfer ownership).
    // join() returns a Result: Ok(value) if the thread completed, Err if it panicked.
    let handle = thread::spawn(|| {
        let mut sum = 0u64;
        for i in 1..=100 { sum += i; }
        sum
    });
    println!("Thread result: {}", handle.join().unwrap());  // => Thread result: 5050

    // `move` transfers ownership of `data` into the thread's closure. Without it, the
    // closure would try to borrow `data`, but the compiler can't prove the main thread
    // won't drop `data` before the spawned thread finishes — so it would refuse to compile.
    let data = vec![1, 2, 3, 4, 5];
    let handle = thread::spawn(move || {
        let sum: i32 = data.iter().sum();
        sum
    });
    println!("Moved data sum: {}", handle.join().unwrap());  // => Moved data sum: 15

    // mpsc (Multiple Producer, Single Consumer) channels provide message passing between threads.
    // tx.clone() creates additional producers. The channel is unbounded by default — producers
    // never block. recv() blocks until a message arrives. This is Go's channel model in Rust,
    // but with compile-time guarantees that sent types are Send-safe.
    let (tx, rx) = mpsc::channel();
    let tx2 = tx.clone();
    thread::spawn(move || { tx.send("from thread 1").unwrap(); });
    thread::spawn(move || { tx2.send("from thread 2").unwrap(); });
    let mut msgs = vec![rx.recv().unwrap(), rx.recv().unwrap()];
    msgs.sort();
    println!("Channel messages: {:?}", msgs);  // => Channel messages: ["from thread 1", "from thread 2"]

    // Arc (Atomic Reference Counted) is the thread-safe version of Rc — it uses atomic
    // operations for the reference count. Mutex provides mutual exclusion: lock() returns
    // a MutexGuard that auto-unlocks when dropped (RAII). The Arc<Mutex<T>> pattern is
    // Rust's equivalent of synchronized shared state in Java or Go's sync.Mutex.
    let counter = Arc::new(Mutex::new(0i32));
    let mut handles = vec![];
    for _ in 0..5 {
        let counter = Arc::clone(&counter);
        handles.push(thread::spawn(move || {
            // lock() blocks until the mutex is available. The MutexGuard auto-releases
            // the lock when it goes out of scope — no risk of forgetting to unlock.
            let mut num = counter.lock().unwrap();
            *num += 1;
        }));
    }
    for h in handles { h.join().unwrap(); }
    println!("Arc<Mutex> counter: {}", *counter.lock().unwrap());  // => Arc<Mutex> counter: 5

    // Atomics provide lock-free thread-safe operations on primitive types. They're faster
    // than Mutex for simple counters because they use CPU-level atomic instructions (CAS)
    // instead of OS-level locking. SeqCst (sequentially consistent) is the strongest ordering —
    // use Relaxed for better performance when you don't need cross-variable ordering guarantees.
    static GLOBAL_COUNT: AtomicUsize = AtomicUsize::new(0);
    let mut handles = vec![];
    for _ in 0..5 {
        handles.push(thread::spawn(|| {
            for _ in 0..100 {
                GLOBAL_COUNT.fetch_add(1, Ordering::SeqCst);
            }
        }));
    }
    for h in handles { h.join().unwrap(); }
    println!("Atomic counter: {}", GLOBAL_COUNT.load(Ordering::SeqCst));  // => Atomic counter: 500
}

// ─── 11. Advanced ───────────────────────────────────────────
fn advanced() {
    header("11. ADVANCED — PhantomData, unsafe, macro_rules!, fmt traits");

    // PhantomData<Unit> is a zero-sized type (ZST) that tells the compiler "this struct
    // is logically associated with Unit, even though it doesn't store one." This enables
    // the type system to distinguish Quantity<Meters> from Quantity<Seconds> at compile time
    // while adding zero runtime cost — the PhantomData field takes no memory.
    // This is the typestate pattern: using the type system to prevent unit-mismatch bugs.
    #[derive(Debug)]
    struct Meters;
    #[derive(Debug)]
    struct Seconds;
    #[derive(Debug)]
    struct Quantity<Unit> {
        #[allow(dead_code)]
        value: f64,
        _unit: PhantomData<Unit>,
    }
    impl<U> Quantity<U> {
        fn new(value: f64) -> Self { Quantity { value, _unit: PhantomData } }
    }
    let dist: Quantity<Meters> = Quantity::new(100.0);
    let time: Quantity<Seconds> = Quantity::new(9.58);
    println!("PhantomData — distance: {:?}, time: {:?}", dist, time);  // => PhantomData — distance: Quantity { value: 100.0, _unit: PhantomData<..::Meters> }, time: Quantity { value: 9.58, _unit: PhantomData<..::Seconds> }

    // unsafe opts out of Rust's safety guarantees for specific operations. Raw pointer
    // dereferencing is unsafe because the compiler can't verify the pointer is valid.
    // Use unsafe only when you need FFI, hardware access, or performance-critical code
    // that the borrow checker can't express. Always minimize the unsafe block's scope.
    let mut val = 42;
    let ptr = &mut val as *mut i32;
    unsafe {
        *ptr += 8;
        println!("Unsafe raw pointer deref: {}", *ptr);  // => Unsafe raw pointer deref: 50
    }

    // macro_rules! defines declarative macros — pattern-matching code generators.
    // $($key:expr => $val:expr),* matches repeated comma-separated key=>value pairs.
    // The macro expands at compile time into a series of insert() calls. Unlike functions,
    // macros can accept variable numbers of arguments and generate arbitrary code.
    // The $(,)? at the end optionally matches a trailing comma.
    macro_rules! map_of {
        ($($key:expr => $val:expr),* $(,)?) => {{
            let mut m = HashMap::new();
            $(m.insert($key, $val);)*
            m
        }};
    }
    let m = map_of!("a" => 1, "b" => 2, "c" => 3);
    println!("macro map_of!: {:?}", m);  // => (varies, e.g. {"a": 1, "b": 2, "c": 3})

    // This macro demonstrates a fold-like expansion: 0 $(+ $x)* expands to 0 + 1 + 2 + 3 + 4 + 5.
    // The compiler evaluates this at compile time if all values are const — zero runtime overhead.
    macro_rules! sum_all {
        ($($x:expr),*) => {{ 0 $(+ $x)* }};
    }
    println!("sum_all!(1,2,3,4,5) = {}", sum_all!(1, 2, 3, 4, 5));  // => sum_all!(1,2,3,4,5) = 15

    // Display (user-facing, via {}) and Debug (developer-facing, via {:?}) are separate traits.
    // Display is for end-user output and must be manually implemented — there's no auto-derive.
    // Debug can be auto-derived with #[derive(Debug)]. Implement Display when your type
    // has a natural string representation (e.g., Color -> #FF8000).
    struct Color { r: u8, g: u8, b: u8 }
    impl fmt::Display for Color {
        fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
            write!(f, "#{:02X}{:02X}{:02X}", self.r, self.g, self.b)
        }
    }
    impl fmt::Debug for Color {
        fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
            write!(f, "Color(r={}, g={}, b={})", self.r, self.g, self.b)
        }
    }
    let c = Color { r: 255, g: 128, b: 0 };
    println!("Display: {c}");  // => Display: #FF8000
    println!("Debug:   {c:?}");  // => Debug:   Color(r=255, g=128, b=0)

    // Format spec alignment: > right, < left, ^ center. The number is the total width.
    // Rust's format syntax mirrors Python's — {:08b} means 8 chars wide, zero-padded, binary.
    println!("Formatted: {:>10} | {:<10} | {:^10}", "right", "left", "center");  // => Formatted:      right | left       |   center
    println!("Binary: {:08b}, Octal: {:o}, Hex: {:x}", 42, 42, 42);  // => Binary: 00101010, Octal: 52, Hex: 2a
}

fn main() {
    println!("================================================================");  // => ================================================================
    println!("  RUST FUNDAMENTALS — Beginner to Advanced (std library only)");  // =>   RUST FUNDAMENTALS — Beginner to Advanced (std library only)
    println!("================================================================");  // => ================================================================

    basics();
    ownership();
    structs_and_enums();
    collections();
    traits_demo();
    error_handling();
    iterators_demo();
    closures_demo();
    smart_pointers();
    concurrency();
    advanced();

    println!("\n================================================================");  // => ================================================================
    println!("  All sections complete.");  // =>   All sections complete.
    println!("================================================================");  // => ================================================================
}
