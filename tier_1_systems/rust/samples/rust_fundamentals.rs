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

    // immutable by default
    let x = 42;
    let mut y = 10;
    y += x;
    println!("x = {x}, y (mutated) = {y}");

    // shadowing — reuse name with new type
    let val = "123";
    let val: i32 = val.parse().unwrap();
    println!("Shadowed val: {val}");

    // scalar types
    let _byte: u8 = 255;
    let _signed: i64 = -9_000_000;
    let _float: f64 = 3.141_592_653;
    let _flag: bool = true;
    let _ch: char = 'R';
    println!("Scalars — u8: {_byte}, i64: {_signed}, f64: {_float}, bool: {_flag}, char: {_ch}");

    // tuples
    let tup: (i32, f64, &str) = (1, 2.5, "hello");
    let (a, b, c) = tup;
    println!("Tuple destructured: a={a}, b={b}, c={c}, index: {}", tup.2);

    // arrays (fixed size, stack-allocated)
    let arr = [10, 20, 30, 40, 50];
    println!("Array slice [1..3]: {:?}", &arr[1..3]);
    println!("Array length: {}", arr.len());
}

// ─── 2. Ownership ───────────────────────────────────────────
fn ownership() {
    header("2. OWNERSHIP — Move, Borrow, References, Lifetimes");

    // move semantics
    let s1 = String::from("hello");
    let s2 = s1; // s1 moved
    // println!("{s1}"); // would not compile
    println!("After move: s2 = {s2}");

    // clone for deep copy
    let s3 = s2.clone();
    println!("Cloned: s2 = {s2}, s3 = {s3}");

    // borrowing — immutable references
    fn calc_len(s: &String) -> usize { s.len() }
    println!("Length of s2 (borrowed): {}", calc_len(&s2));

    // mutable reference
    let mut s4 = String::from("hello");
    fn append(s: &mut String) { s.push_str(", world"); }
    append(&mut s4);
    println!("After mutable borrow: {s4}");

    // lifetime annotations
    fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
        if x.len() >= y.len() { x } else { y }
    }
    let result;
    let str_a = String::from("long string");
    {
        let str_b = String::from("short");
        result = longest(str_a.as_str(), str_b.as_str());
        println!("Longest: {result}");
    }

    // struct with lifetimes
    #[derive(Debug)]
    struct Excerpt<'a> { part: &'a str }
    let novel = String::from("Call me Ishmael. Some years ago...");
    let first_sentence = novel.split('.').next().unwrap();
    let excerpt = Excerpt { part: first_sentence };
    println!("Excerpt: {:?}", excerpt);
}

// ─── 3. Structs & Enums ────────────────────────────────────
fn structs_and_enums() {
    header("3. STRUCTS & ENUMS — Methods, Option, Result, Pattern Matching");

    #[derive(Debug)]
    struct Rect { width: f64, height: f64 }

    impl Rect {
        fn new(w: f64, h: f64) -> Self { Self { width: w, height: h } }
        fn area(&self) -> f64 { self.width * self.height }
        fn scale(&mut self, factor: f64) {
            self.width *= factor;
            self.height *= factor;
        }
    }

    let mut r = Rect::new(10.0, 5.0);
    println!("Rect area: {}", r.area());
    r.scale(2.0);
    println!("Scaled rect: {:?}, area: {}", r, r.area());

    // enum with data
    #[derive(Debug)]
    enum Shape {
        Circle(f64),
        Rectangle(f64, f64),
        Triangle { base: f64, height: f64 },
    }

    impl Shape {
        fn area(&self) -> f64 {
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
        println!("{:?} -> area = {:.2}", s, s.area());
    }

    // Option and Result
    let nums = vec![2, 4, 6];
    match nums.get(10) {
        Some(v) => println!("Found: {v}"),
        None => println!("Index 10 out of bounds (Option::None)"),
    }

    fn safe_div(a: f64, b: f64) -> Result<f64, String> {
        if b == 0.0 { Err("division by zero".into()) } else { Ok(a / b) }
    }
    println!("10 / 3 = {:?}", safe_div(10.0, 3.0));
    println!("10 / 0 = {:?}", safe_div(10.0, 0.0));
}

// ─── 4. Collections ────────────────────────────────────────
fn collections() {
    header("4. COLLECTIONS — Vec, HashMap, HashSet, BTreeMap, VecDeque, BinaryHeap");

    let mut v = vec![3, 1, 4, 1, 5, 9];
    v.sort();
    v.dedup();
    println!("Vec sorted+dedup: {:?}", v);

    let mut map = HashMap::new();
    for &n in &v { *map.entry(n % 3).or_insert(0) += 1; }
    println!("HashMap (n%3 -> count): {:?}", map);

    let set: HashSet<_> = v.iter().copied().collect();
    let set2: HashSet<i32> = [1, 2, 3, 4].iter().copied().collect();
    println!("HashSet intersection: {:?}", set.intersection(&set2).collect::<Vec<_>>());
    println!("HashSet union: {:?}", set.union(&set2).collect::<Vec<_>>());

    let mut btree = BTreeMap::new();
    for (i, &n) in v.iter().enumerate() { btree.insert(n, i); }
    println!("BTreeMap (sorted keys): {:?}", btree);

    let mut deque = VecDeque::from([1, 2, 3]);
    deque.push_front(0);
    deque.push_back(4);
    println!("VecDeque: {:?}", deque);

    let mut heap = BinaryHeap::from([3, 1, 4, 1, 5]);
    println!("BinaryHeap max: {:?}", heap.peek());
    let sorted: Vec<_> = std::iter::from_fn(|| heap.pop()).collect();
    println!("Heap drain (desc): {:?}", sorted);
}

// ─── 5. Traits ──────────────────────────────────────────────
fn traits_demo() {
    header("5. TRAITS — Definitions, Generics, Trait Objects, Associated Types");

    trait Describable {
        fn describe(&self) -> String;
        fn label(&self) -> &str { "unknown" } // default impl
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
    }

    // generic with trait bound
    fn print_desc<T: Describable>(item: &T) {
        println!("[{}] {}", item.label(), item.describe());
    }
    print_desc(&Dog { name: "Rex".into(), age: 5 });
    print_desc(&Cat { name: "Whiskers".into() });

    // trait objects (dynamic dispatch)
    let animals: Vec<Box<dyn Describable>> = vec![
        Box::new(Dog { name: "Buddy".into(), age: 3 }),
        Box::new(Cat { name: "Luna".into() }),
    ];
    for a in &animals { println!("Dyn dispatch: {}", a.describe()); }

    // associated types
    trait Converter {
        type Output;
        fn convert(&self) -> Self::Output;
    }
    impl Converter for Dog {
        type Output = String;
        fn convert(&self) -> String { format!("Dog({})", self.name) }
    }
    let d = Dog { name: "Ace".into(), age: 2 };
    println!("Associated type convert: {}", d.convert());
}

// ─── 6. Error Handling ──────────────────────────────────────
fn error_handling() {
    header("6. ERROR HANDLING — Custom Errors, ?, From/Into");

    #[derive(Debug)]
    enum AppError {
        Parse(std::num::ParseIntError),
        Validation(String),
    }

    impl fmt::Display for AppError {
        fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
            match self {
                AppError::Parse(e) => write!(f, "Parse error: {e}"),
                AppError::Validation(msg) => write!(f, "Validation: {msg}"),
            }
        }
    }

    impl From<std::num::ParseIntError> for AppError {
        fn from(e: std::num::ParseIntError) -> Self { AppError::Parse(e) }
    }

    fn parse_and_validate(s: &str) -> Result<i32, AppError> {
        let n: i32 = s.parse()?; // auto-converts via From
        if n < 0 { return Err(AppError::Validation("must be non-negative".into())); }
        Ok(n)
    }

    for input in &["42", "abc", "-5"] {
        match parse_and_validate(input) {
            Ok(n) => println!("  '{input}' -> Ok({n})"),
            Err(e) => println!("  '{input}' -> Err({e})"),
        }
    }
}

// ─── 7. Iterators ───────────────────────────────────────────
fn iterators_demo() {
    header("7. ITERATORS — map, filter, fold, collect, custom iterators");

    let nums = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

    let evens_squared: Vec<i32> = nums.iter()
        .filter(|&&n| n % 2 == 0)
        .map(|&n| n * n)
        .collect();
    println!("Even squares: {:?}", evens_squared);

    let sum: i32 = nums.iter().sum();
    let product: i32 = nums.iter().fold(1, |acc, &x| acc * x);
    println!("Sum: {sum}, Product: {product}");

    // chaining: enumerate, zip, flatten
    let words = vec!["hello", "world"];
    let chars: Vec<char> = words.iter().flat_map(|w| w.chars()).collect();
    println!("Flattened chars: {:?}", chars);

    let pairs: Vec<_> = (0..).zip(words.iter()).collect();
    println!("Zipped with index: {:?}", pairs);

    // custom iterator
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
    let fibs: Vec<u64> = Fib::new().take(12).collect();
    println!("Fibonacci (12): {:?}", fibs);

    // partition
    let (evens, odds): (Vec<&i32>, Vec<&i32>) = nums.iter().partition(|&&n| n % 2 == 0);
    println!("Partition — evens: {:?}, odds: {:?}", evens, odds);
}

// ─── 8. Closures ────────────────────────────────────────────
fn closures_demo() {
    header("8. CLOSURES — Fn, FnMut, FnOnce, move, returning closures");

    // Fn — borrows immutably
    let greeting = String::from("Hello");
    let greet = |name: &str| println!("{greeting}, {name}!");
    greet("Alice");
    greet("Bob");

    // FnMut — borrows mutably
    let mut count = 0;
    let mut counter = || { count += 1; count };
    println!("Counter: {}, {}, {}", counter(), counter(), counter());

    // FnOnce — takes ownership
    let data = vec![1, 2, 3];
    let consume = move || {
        println!("Consumed data: {:?}", data);
        data // returns owned data
    };
    let _recovered = consume();
    // consume(); // can't call again — FnOnce

    // returning closures (boxed)
    fn make_adder(x: i32) -> Box<dyn Fn(i32) -> i32> {
        Box::new(move |y| x + y)
    }
    let add5 = make_adder(5);
    println!("make_adder(5)(10) = {}", add5(10));

    // closure as function argument
    fn apply_twice<F: Fn(i32) -> i32>(f: F, x: i32) -> i32 { f(f(x)) }
    println!("apply_twice(|x| x*2, 3) = {}", apply_twice(|x| x * 2, 3));
}

// ─── 9. Smart Pointers ─────────────────────────────────────
fn smart_pointers() {
    header("9. SMART POINTERS — Box, Rc, Arc, RefCell, Cow");

    // Box — heap allocation, recursive types
    #[derive(Debug)]
    enum List { Cons(i32, Box<List>), Nil }
    let list = List::Cons(1, Box::new(List::Cons(2, Box::new(List::Cons(3, Box::new(List::Nil))))));
    println!("Boxed linked list: {:?}", list);

    // Rc — reference counting (single thread)
    let shared = Rc::new(String::from("shared data"));
    let a = Rc::clone(&shared);
    let b = Rc::clone(&shared);
    println!("Rc strong count: {} (a={a}, b={b})", Rc::strong_count(&shared));

    // RefCell — interior mutability
    let cell = RefCell::new(vec![1, 2, 3]);
    cell.borrow_mut().push(4);
    println!("RefCell contents: {:?}", cell.borrow());

    // Rc + RefCell combo — shared mutable state
    let shared_vec = Rc::new(RefCell::new(Vec::new()));
    let clone1 = Rc::clone(&shared_vec);
    let clone2 = Rc::clone(&shared_vec);
    clone1.borrow_mut().push("from clone1");
    clone2.borrow_mut().push("from clone2");
    println!("Rc<RefCell<Vec>>: {:?}", shared_vec.borrow());

    // Cow — clone on write
    fn maybe_uppercase(s: &str, upper: bool) -> Cow<str> {
        if upper { Cow::Owned(s.to_uppercase()) } else { Cow::Borrowed(s) }
    }
    println!("Cow borrowed: {}", maybe_uppercase("hello", false));
    println!("Cow owned:    {}", maybe_uppercase("hello", true));
}

// ─── 10. Concurrency ───────────────────────────────────────
fn concurrency() {
    header("10. CONCURRENCY — Threads, Channels, Mutex, Arc+Mutex, Atomics");

    // basic thread spawn + join
    let handle = thread::spawn(|| {
        let mut sum = 0u64;
        for i in 1..=100 { sum += i; }
        sum
    });
    println!("Thread result: {}", handle.join().unwrap());

    // move data into thread
    let data = vec![1, 2, 3, 4, 5];
    let handle = thread::spawn(move || {
        let sum: i32 = data.iter().sum();
        sum
    });
    println!("Moved data sum: {}", handle.join().unwrap());

    // channels (mpsc)
    let (tx, rx) = mpsc::channel();
    let tx2 = tx.clone();
    thread::spawn(move || { tx.send("from thread 1").unwrap(); });
    thread::spawn(move || { tx2.send("from thread 2").unwrap(); });
    let mut msgs = vec![rx.recv().unwrap(), rx.recv().unwrap()];
    msgs.sort();
    println!("Channel messages: {:?}", msgs);

    // Arc + Mutex — shared mutable state across threads
    let counter = Arc::new(Mutex::new(0i32));
    let mut handles = vec![];
    for _ in 0..5 {
        let counter = Arc::clone(&counter);
        handles.push(thread::spawn(move || {
            let mut num = counter.lock().unwrap();
            *num += 1;
        }));
    }
    for h in handles { h.join().unwrap(); }
    println!("Arc<Mutex> counter: {}", *counter.lock().unwrap());

    // atomic types
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
    println!("Atomic counter: {}", GLOBAL_COUNT.load(Ordering::SeqCst));
}

// ─── 11. Advanced ───────────────────────────────────────────
fn advanced() {
    header("11. ADVANCED — PhantomData, unsafe, macro_rules!, fmt traits");

    // PhantomData — zero-sized type marker
    #[derive(Debug)]
    struct Meters;
    #[derive(Debug)]
    struct Seconds;
    #[derive(Debug)]
    struct Quantity<Unit> {
        value: f64,
        _unit: PhantomData<Unit>,
    }
    impl<U> Quantity<U> {
        fn new(value: f64) -> Self { Quantity { value, _unit: PhantomData } }
    }
    let dist: Quantity<Meters> = Quantity::new(100.0);
    let time: Quantity<Seconds> = Quantity::new(9.58);
    println!("PhantomData — distance: {:?}, time: {:?}", dist, time);

    // unsafe — raw pointer dereferencing
    let mut val = 42;
    let ptr = &mut val as *mut i32;
    unsafe {
        *ptr += 8;
        println!("Unsafe raw pointer deref: {}", *ptr);
    }

    // macro_rules!
    macro_rules! map_of {
        ($($key:expr => $val:expr),* $(,)?) => {{
            let mut m = HashMap::new();
            $(m.insert($key, $val);)*
            m
        }};
    }
    let m = map_of!("a" => 1, "b" => 2, "c" => 3);
    println!("macro map_of!: {:?}", m);

    // variadic-style macro
    macro_rules! sum_all {
        ($($x:expr),*) => {{ 0 $(+ $x)* }};
    }
    println!("sum_all!(1,2,3,4,5) = {}", sum_all!(1, 2, 3, 4, 5));

    // custom Display and Debug via fmt traits
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
    println!("Display: {c}");
    println!("Debug:   {c:?}");

    // fmt padding and alignment
    println!("Formatted: {:>10} | {:<10} | {:^10}", "right", "left", "center");
    println!("Binary: {:08b}, Octal: {:o}, Hex: {:x}", 42, 42, 42);
}

fn main() {
    println!("================================================================");
    println!("  RUST FUNDAMENTALS — Beginner to Advanced (std library only)");
    println!("================================================================");

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

    println!("\n================================================================");
    println!("  All sections complete.");
    println!("================================================================");
}
