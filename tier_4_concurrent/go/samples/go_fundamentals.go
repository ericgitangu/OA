package main

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"math"
	"path/filepath"
	"regexp"
	"sort"
	"strconv"
	"strings"
	"sync"
	"time"
)

// ============================================================
// SECTION: Basics — variables, constants, iota, returns
// ============================================================

// Go constants are truly immutable and evaluated at compile time. They can be
// untyped (like Pi below), allowing them to be used in expressions with any
// compatible numeric type without explicit casting. See Go spec: Constants
const Pi = 3.14159

// iota is Go's constant generator — it auto-increments within a const block,
// starting at 0. Each const spec resets iota. This replaces C-style enums.
// The blank identifier pattern `_ = iota` can skip values. Go has no enum keyword;
// iota + typed constants is the idiomatic alternative. See Go spec: Iota
const (
	Sunday    = iota // 0
	Monday           // 1
	Tuesday          // 2
	Wednesday        // 3
	Thursday         // 4
	Friday           // 5
	Saturday         // 6
)

// Go uses multiple return values instead of exceptions for error handling.
// This is a deliberate design choice: errors are values, not control flow.
// The caller MUST handle the error explicitly — no silent exception propagation.
// See Go blog: "Errors are values"
func divide(a, b float64) (float64, error) {
	if b == 0 {
		return 0, fmt.Errorf("division by zero")
	}
	return a / b, nil
}

// Named return values are pre-declared variables initialized to their zero values.
// "Naked return" returns them implicitly. Use sparingly — they help with documentation
// but can reduce readability in longer functions. Best for short functions where the
// names serve as self-documenting return values. See Effective Go: Named results
func namedReturns(x, y int) (sum int, diff int) {
	sum = x + y
	diff = x - y
	return // naked return uses named values
}

func demoBasics() {
	fmt.Println("\n=== BASICS ===")  // => === BASICS ===

	// `var` declares with explicit type; `:=` uses short declaration with type inference.
	// Short declarations are only available inside functions — package-level vars need `var`.
	// Go's type inference is local only (unlike Hindley-Milner in Haskell/ML).
	var name string = "Go"
	age := 15 // short declaration — compiler infers int
	var untyped = 42.0
	fmt.Printf("name=%s  age=%d  untyped=%.1f\n", name, age, untyped)  // => name=Go  age=15  untyped=42.0

	// constants & iota
	fmt.Printf("Pi=%.5f  Sunday=%d  Saturday=%d\n", Pi, Sunday, Saturday)  // => Pi=3.14159  Sunday=0  Saturday=6

	// Multiple return values force explicit error handling at every call site.
	// The Go philosophy: don't hide errors behind exceptions — make them visible.
	result, err := divide(10, 3)
	fmt.Printf("10/3 = %.4f  err=%v\n", result, err)  // => 10/3 = 3.3333  err=<nil>

	// named returns
	s, d := namedReturns(10, 3)
	fmt.Printf("sum=%d  diff=%d\n", s, d)  // => sum=13  diff=7

	// The blank identifier `_` discards a value. The compiler enforces that all declared
	// variables are used — `_` is the escape hatch for intentionally unused values.
	// This prevents bugs from accidentally shadowed or forgotten return values.
	_, err2 := divide(1, 0)
	fmt.Printf("ignored result, err=%v\n", err2)  // => ignored result, err=division by zero
}

// ============================================================
// SECTION: Types — structs, interfaces, embedding, assertions
// ============================================================

// Interfaces in Go are satisfied implicitly — a type implements an interface simply
// by having the right methods. No `implements` keyword needed. This enables
// decoupling between packages that don't know about each other (the "accept interfaces,
// return structs" principle). See Go spec: Interface types
type Shape interface {
	Area() float64
	Perimeter() float64
}

// Structs are value types — assignment copies all fields. For large structs or when
// mutation is needed, use pointers (*Circle). Methods can have value or pointer receivers.
type Circle struct {
	Radius float64
}

// Value receivers operate on a copy of the struct — they can't modify the original.
// Use value receivers for small structs and when the method doesn't mutate state.
func (c Circle) Area() float64      { return math.Pi * c.Radius * c.Radius }
func (c Circle) Perimeter() float64 { return 2 * math.Pi * c.Radius }

type Rectangle struct {
	Width, Height float64
}

func (r Rectangle) Area() float64      { return r.Width * r.Height }
func (r Rectangle) Perimeter() float64 { return 2 * (r.Width + r.Height) }

// Embedding promotes all methods and fields of the embedded type to the outer type.
// This is composition, not inheritance — Go has no class hierarchy. The embedded Shape
// field's methods are "promoted" to LabeledShape, so ls.Area() works directly.
// If there's a name conflict, the outer type's method wins (shadowing).
type LabeledShape struct {
	Shape
	Label string
}

func demoTypes() {
	fmt.Println("\n=== TYPES ===")  // => === TYPES ===

	c := Circle{Radius: 5}
	r := Rectangle{Width: 3, Height: 4}
	fmt.Printf("Circle  area=%.2f  perim=%.2f\n", c.Area(), c.Perimeter())  // => Circle  area=78.54  perim=31.42
	fmt.Printf("Rect    area=%.2f  perim=%.2f\n", r.Area(), r.Perimeter())  // => Rect    area=12.00  perim=14.00

	// Embedding: LabeledShape gets Area() and Perimeter() "for free" from its embedded Shape.
	ls := LabeledShape{Shape: c, Label: "unit-circle"}
	fmt.Printf("Labeled: %s  area=%.2f\n", ls.Label, ls.Area())  // => Labeled: unit-circle  area=78.54

	// Type assertion extracts the concrete type from an interface value.
	// The comma-ok idiom (`circle, ok := s.(Circle)`) avoids panics on wrong types.
	// Without ok, a failed assertion panics. Always use the comma-ok form in production.
	var s Shape = c
	if circle, ok := s.(Circle); ok {
		fmt.Printf("Type assertion: radius=%.1f\n", circle.Radius)  // => Type assertion: radius=5.0
	}

	// Type switch examines the concrete type stored in an interface value.
	// Each case branch has the variable narrowed to that specific type.
	// Unlike assertion chains, type switches are exhaustive when used with a default case.
	shapes := []Shape{c, r}
	for _, sh := range shapes {
		switch v := sh.(type) {
		case Circle:
			fmt.Printf("  type-switch: Circle r=%.1f\n", v.Radius)  // => type-switch: Circle r=5.0
		case Rectangle:
			fmt.Printf("  type-switch: Rect %gx%g\n", v.Width, v.Height)  // => type-switch: Rect 3x4
		}
	}
}

// ============================================================
// SECTION: Collections — slices, maps, arrays
// ============================================================

func demoCollections() {
	fmt.Println("\n=== COLLECTIONS ===")  // => === COLLECTIONS ===

	// Arrays have fixed size determined at compile time — the size is part of the type.
	// [3]int and [4]int are different types. Arrays are rarely used directly in Go;
	// slices (below) are the idiomatic dynamic collection.
	arr := [3]int{10, 20, 30}
	fmt.Printf("array: %v  len=%d\n", arr, len(arr))  // => array: [10 20 30]  len=3

	// Slices are a 3-word struct: (pointer to underlying array, length, capacity).
	// append() may allocate a new backing array if cap is exceeded — the growth
	// strategy roughly doubles capacity. Always reassign: `s = append(s, ...)`.
	// See Go blog: "Go Slices: usage and internals"
	nums := []int{5, 3, 8, 1, 9, 2}
	nums = append(nums, 7, 4)
	fmt.Printf("slice after append: %v\n", nums)  // => slice after append: [5 3 8 1 9 2 7 4]

	// make([]T, len, cap) pre-allocates capacity to avoid repeated allocations.
	// copy() copies elements and returns the count copied (min of src/dst lengths).
	dst := make([]int, 4)
	n := copy(dst, nums)
	fmt.Printf("copied %d elements: %v\n", n, dst)  // => copied 4 elements: [5 3 8 1]

	// Slicing creates a new slice header pointing to the SAME backing array.
	// Mutations to `sub` will affect `nums` unless sub grows beyond its capacity.
	// Use full slice expression `nums[2:5:5]` to limit capacity and prevent aliasing.
	sub := nums[2:5]
	fmt.Printf("nums[2:5] = %v\n", sub)  // => nums[2:5] = [8 1 9]

	// Maps are hash tables with O(1) average lookup. The zero value is nil — reading
	// from nil map returns zero value, but writing to nil map panics.
	// Always initialize with make() or a literal. Map iteration order is randomized
	// by the runtime (intentionally, to prevent depending on order).
	m := map[string]int{"alice": 90, "bob": 85, "carol": 92}
	m["dave"] = 88
	delete(m, "bob")
	// The comma-ok idiom distinguishes "key not found" (zero value) from "key exists with zero value".
	if score, ok := m["carol"]; ok {
		fmt.Printf("carol's score: %d\n", score)  // => carol's score: 92
	}
	fmt.Printf("map keys: ")
	for k := range m {
		fmt.Printf("%s ", k)  // => (varies)
	}
	fmt.Println()
}

// ============================================================
// SECTION: Functions — variadic, closures, defer/panic/recover
// ============================================================

// Variadic functions accept zero or more arguments of the same type via `...T`.
// Internally, the variadic parameter is a slice. You can pass a slice with `slice...`
// to expand it into individual arguments. See Go spec: Passing arguments to ... parameters
func sum(nums ...int) int {
	total := 0
	for _, n := range nums {
		total += n
	}
	return total
}

// Closures capture variables by reference, not by value. The returned function
// shares the same `count` variable — each call modifies it. This is Go's way
// of achieving stateful functions without structs.
func makeCounter() func() int {
	count := 0
	return func() int {
		count++
		return count
	}
}

// defer schedules a function call to run when the enclosing function returns.
// Deferred calls execute in LIFO (stack) order. Combined with recover(), defer
// can catch panics and convert them to errors — this is Go's equivalent of try/catch,
// but it's deliberately more awkward to discourage using panics for control flow.
// See Effective Go: Panic, Go blog: "Defer, Panic, and Recover"
func safeDivide(a, b int) (result int, err error) {
	defer func() {
		if r := recover(); r != nil {
			err = fmt.Errorf("recovered panic: %v", r)
		}
	}()
	return a / b, nil // panics if b == 0 (integer division)
}

// Value receiver — operates on a copy of the struct, cannot modify the original.
// The original Rectangle is unchanged after calling Scale().
func (r Rectangle) Scale(factor float64) Rectangle {
	return Rectangle{r.Width * factor, r.Height * factor}
}

// Pointer receiver — operates on the original struct via indirection.
// Use pointer receivers when the method mutates state, the struct is large (avoid copy),
// or for consistency (if one method needs a pointer receiver, all should use one).
// Go automatically takes the address: `r.ScaleInPlace(2)` works on a value r.
func (r *Rectangle) ScaleInPlace(factor float64) {
	r.Width *= factor
	r.Height *= factor
}

func demoFunctions() {
	fmt.Println("\n=== FUNCTIONS ===")  // => === FUNCTIONS ===

	// Variadic: sum accepts any number of ints
	fmt.Printf("sum(1,2,3) = %d\n", sum(1, 2, 3))  // => sum(1,2,3) = 6
	// Expanding a slice into variadic args with the ... suffix
	nums := []int{4, 5, 6}
	fmt.Printf("sum(slice...) = %d\n", sum(nums...))  // => sum(slice...) = 15

	// Closure: counter retains state across calls via the closed-over `count` variable
	counter := makeCounter()
	fmt.Printf("counter: %d, %d, %d\n", counter(), counter(), counter())  // => counter: 1, 2, 3

	// Defer + recover converts a panic into a returned error
	_, err := safeDivide(10, 0)
	fmt.Printf("safeDivide(10,0) err=%v\n", err)  // => safeDivide(10,0) err=recovered panic: runtime error: integer divide by zero

	// Value vs pointer receivers: Scale returns a new Rectangle, ScaleInPlace mutates in place
	r := Rectangle{3, 4}
	scaled := r.Scale(2)
	fmt.Printf("Scale(2): %gx%g (original %gx%g)\n", scaled.Width, scaled.Height, r.Width, r.Height)  // => Scale(2): 6x8 (original 3x4)
	r.ScaleInPlace(2)
	fmt.Printf("ScaleInPlace(2): %gx%g\n", r.Width, r.Height)  // => ScaleInPlace(2): 6x8
}

// ============================================================
// SECTION: Interfaces — implicit, empty, Stringer, io
// ============================================================

// This Stringer interface mirrors fmt.Stringer from the standard library.
// Any type with a String() method is automatically a Stringer — no declaration needed.
// This is "structural typing" or "duck typing" — if it quacks like a Stringer, it is one.
// This decouples interface definition from implementation, unlike Java's `implements`.
type Stringer interface {
	String() string
}

type Point struct{ X, Y float64 }

// By implementing String(), Point satisfies fmt.Stringer. The fmt package checks
// for this interface at runtime and calls it for %s and %v formatting.
// This is how Go achieves polymorphism without inheritance.
func (p Point) String() string {
	return fmt.Sprintf("(%g, %g)", p.X, p.Y)
}

// interface{} (or `any` in Go 1.18+) is the empty interface — every type satisfies it
// because every type has zero or more methods. Use sparingly: you lose type safety.
// The fmt package uses interface{} extensively because it must accept any type.
func printAnything(v interface{}) {
	fmt.Printf("  empty-interface: %v (type %T)\n", v, v)
}

func demoInterfaces() {
	fmt.Println("\n=== INTERFACES ===")  // => === INTERFACES ===

	// Implicit satisfaction — Point satisfies Stringer without declaring it.
	// The compiler verifies this statically; no runtime registration needed.
	p := Point{3, 4}
	fmt.Printf("Stringer: %s\n", p)  // => Stringer: (3, 4)

	// Empty interface accepts any type — similar to Object in Java or any in TS.
	// The value is stored as (type, pointer) pair internally (iface representation).
	printAnything(42)       // => empty-interface: 42 (type int)
	printAnything("hello")  // => empty-interface: hello (type string)
	printAnything([]int{1, 2, 3})  // => empty-interface: [1 2 3] (type []int)

	// io.Reader/io.Writer are the most important interfaces in Go's stdlib.
	// They enable composition: any type that reads bytes can be used anywhere
	// an io.Reader is expected (files, network, strings, compression, etc.).
	// This is the "small interface" philosophy — define interfaces with 1-2 methods.
	reader := strings.NewReader("Go is great")
	buf := make([]byte, 5)
	n, _ := reader.Read(buf)
	fmt.Printf("io.Reader first %d bytes: %s\n", n, buf[:n])  // => io.Reader first 5 bytes: Go is
}

// ============================================================
// SECTION: Concurrency — goroutines, channels, sync
// ============================================================

// Channel direction annotations (chan<-, <-chan) enforce send-only or receive-only
// access at compile time. This prevents bugs where a producer accidentally reads
// from a channel it should only write to. Always restrict direction in function signatures.
func producer(ch chan<- int, start, count int) {
	for i := start; i < start+count; i++ {
		ch <- i
	}
}

func demoConcurrency() {
	fmt.Println("\n=== CONCURRENCY ===")  // => === CONCURRENCY ===

	// Goroutines are lightweight, user-space threads managed by the Go runtime scheduler.
	// Unlike OS threads (~1MB stack), goroutines start at ~2KB and grow dynamically.
	// The runtime multiplexes goroutines onto OS threads (M:N scheduling model).
	// WaitGroup tracks goroutine completion — Add before launching, Done when finished.
	var wg sync.WaitGroup
	for i := 0; i < 3; i++ {
		wg.Add(1)
		// The `id` parameter captures the loop variable by value — without it, all
		// goroutines would share the same `i` variable (a common closure bug).
		go func(id int) {
			defer wg.Done()
			fmt.Printf("  goroutine %d running\n", id)  // => (varies)
		}(i)
	}
	wg.Wait()

	// Unbuffered channels synchronize sender and receiver — the sender blocks until
	// a receiver is ready, and vice versa. This provides a communication-based
	// synchronization primitive, following CSP (Communicating Sequential Processes).
	// Go proverb: "Don't communicate by sharing memory; share memory by communicating."
	ch := make(chan string)
	go func() { ch <- "ping" }()
	fmt.Printf("received: %s\n", <-ch)  // => received: ping

	// Buffered channels decouple sender and receiver timing. Sends only block when
	// the buffer is full; receives only block when empty. Use buffered channels
	// when you know the number of items upfront or need to reduce synchronization overhead.
	bch := make(chan int, 3)
	bch <- 1
	bch <- 2
	bch <- 3
	fmt.Printf("buffered: %d %d %d\n", <-bch, <-bch, <-bch)  // => buffered: 1 2 3

	// select multiplexes across multiple channel operations — it blocks until ONE
	// case is ready, then executes it. If multiple cases are ready, one is chosen
	// at random (preventing starvation). `default` makes it non-blocking.
	// select is the core primitive for implementing timeouts, cancellation, and fan-in.
	ch1 := make(chan string, 1)
	ch2 := make(chan string, 1)
	ch1 <- "one"
	ch2 <- "two"
	select {
	case v := <-ch1:
		fmt.Printf("select got: %s\n", v)  // => (varies)
	case v := <-ch2:
		fmt.Printf("select got: %s\n", v)  // => (varies)
	}

	// sync.Mutex provides mutual exclusion for shared state. Use when channels are
	// overkill (e.g., protecting a simple counter or map). The Go community prefers
	// channels for coordination between goroutines, mutexes for protecting data structures.
	// RWMutex provides read/write locking when reads vastly outnumber writes.
	var mu sync.Mutex
	counter := 0
	var wg2 sync.WaitGroup
	for i := 0; i < 100; i++ {
		wg2.Add(1)
		go func() {
			defer wg2.Done()
			mu.Lock()
			counter++
			mu.Unlock()
		}()
	}
	wg2.Wait()
	fmt.Printf("mutex counter: %d\n", counter)  // => mutex counter: 100

	// sync.Once guarantees a function runs exactly once, even across goroutines.
	// Common uses: lazy initialization, singleton pattern, one-time setup.
	// Thread-safe without external locking. Internally uses atomic operations + mutex.
	var once sync.Once
	for i := 0; i < 3; i++ {
		once.Do(func() {
			fmt.Println("once.Do: runs only once")  // => once.Do: runs only once
		})
	}

	// sync.Map is a concurrent-safe map optimized for two patterns: (1) keys written once
	// but read many times, (2) disjoint sets of keys per goroutine. For most other cases,
	// a regular map + sync.RWMutex performs better. See sync.Map docs for when to use it.
	var sm sync.Map
	sm.Store("lang", "Go")
	sm.Store("year", 2009)
	sm.Range(func(key, value interface{}) bool {
		fmt.Printf("  sync.Map: %v=%v\n", key, value)  // => (varies)
		return true
	})
}

// ============================================================
// SECTION: Patterns — fan-out/fan-in, pipeline, context
// ============================================================

// Pipeline pattern: each stage is a function that takes a receive-only channel and
// returns a receive-only channel. Stages run concurrently as goroutines.
// Closing the output channel signals downstream stages that no more data is coming.
// Always `defer close(out)` to prevent goroutine leaks. See Go blog: "Go Concurrency Patterns: Pipelines"
func generator(nums ...int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for _, n := range nums {
			out <- n
		}
	}()
	return out
}

func square(in <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for n := range in {
			out <- n * n
		}
	}()
	return out
}

// Fan-in merges multiple input channels into a single output channel.
// A WaitGroup tracks when all input channels are drained, then closes the output.
// The goroutine that waits and closes runs concurrently to avoid blocking the caller.
// This is the inverse of fan-out (splitting work across multiple goroutines).
func merge(channels ...<-chan int) <-chan int {
	var wg sync.WaitGroup
	out := make(chan int)
	for _, ch := range channels {
		wg.Add(1)
		go func(c <-chan int) {
			defer wg.Done()
			for v := range c {
				out <- v
			}
		}(ch)
	}
	go func() {
		wg.Wait()
		close(out)
	}()
	return out
}

func demoPatterns() {
	fmt.Println("\n=== PATTERNS ===")  // => === PATTERNS ===

	// Pipeline: data flows through stages: generator -> square -> consume.
	// Each stage runs in its own goroutine, processing elements concurrently.
	pipeline := square(generator(1, 2, 3, 4, 5))
	fmt.Print("pipeline squares: ")
	for v := range pipeline {
		fmt.Printf("%d ", v)  // => 1 4 9 16 25
	}
	fmt.Println()

	// Fan-out: multiple goroutines read from the same channel to parallelize work.
	// Fan-in: merge results back into one channel for the consumer.
	src := generator(10, 20, 30, 40)
	sq1 := square(src) // single fan-out for brevity
	for v := range sq1 {
		fmt.Printf("  fan-out result: %d\n", v)  // => 100, 400, 900, 1600
	}

	// Merge demonstration: combines outputs from multiple generators into one stream
	merged := merge(generator(1, 2), generator(3, 4))
	fmt.Print("merged: ")
	for v := range merged {
		fmt.Printf("%d ", v)  // => (varies)
	}
	fmt.Println()

	// context.WithTimeout creates a context that automatically cancels after a duration.
	// Contexts propagate cancellation, deadlines, and request-scoped values through
	// call chains. Every long-running or I/O operation should accept a context.
	// The cancel function MUST be called (usually via defer) to release resources.
	// See Go blog: "Go Concurrency Patterns: Context"
	ctx, cancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
	defer cancel()

	select {
	case <-time.After(100 * time.Millisecond):
		fmt.Println("work completed")  // => (not reached — context times out first)
	case <-ctx.Done():
		// ctx.Err() returns context.DeadlineExceeded or context.Canceled
		fmt.Printf("context: %v\n", ctx.Err())  // => context: context deadline exceeded
	}

	// context.WithCancel provides manual cancellation — useful when you need to
	// stop goroutines based on application logic rather than a timer.
	ctx2, cancel2 := context.WithCancel(context.Background())
	go func() {
		time.Sleep(10 * time.Millisecond)
		cancel2()
	}()
	<-ctx2.Done()
	fmt.Printf("cancelled: %v\n", ctx2.Err())  // => cancelled: context canceled
}

// ============================================================
// SECTION: Generics — type parameters, constraints
// ============================================================

// Generics (Go 1.18) add type parameters to functions and types. The constraint
// `int | float64 | string` is a type set — it lists which types are allowed.
// Go uses type sets (not type classes like Haskell) for constraints.
// The `comparable` built-in constraint includes all types that support == and !=.
func Min[T int | float64 | string](a, b T) T {
	if a < b {
		return a
	}
	return b
}

// Interface constraints define type sets — any type in the set can be used.
// The `~int` syntax would include named types based on int (e.g., `type Age int`).
// Without `~`, only the exact types are allowed.
type Number interface {
	int | int32 | int64 | float64
}

func Sum[T Number](nums []T) T {
	var total T
	for _, n := range nums {
		total += n
	}
	return total
}

// `comparable` is a built-in constraint for types that support == and !=.
// Maps require comparable keys; this constraint mirrors that requirement.
// Note: comparable excludes slices, maps, and functions (which can't be compared).
func Contains[T comparable](slice []T, target T) bool {
	for _, v := range slice {
		if v == target {
			return true
		}
	}
	return false
}

// Multi-type-parameter generics: T and U can be different types, enabling
// transformations like []int -> []string. The `any` constraint is an alias for
// interface{} — it allows any type but provides no methods to call on it.
func Map[T any, U any](slice []T, fn func(T) U) []U {
	result := make([]U, len(slice))
	for i, v := range slice {
		result[i] = fn(v)
	}
	return result
}

func demoGenerics() {
	fmt.Println("\n=== GENERICS ===")  // => === GENERICS ===

	// Type inference: the compiler infers T from the arguments — no need to write Min[int](3, 7)
	fmt.Printf("Min(3, 7) = %d\n", Min(3, 7))  // => Min(3, 7) = 3
	fmt.Printf("Min(3.14, 2.71) = %.2f\n", Min(3.14, 2.71))  // => Min(3.14, 2.71) = 2.71
	fmt.Printf("Min(\"apple\", \"banana\") = %s\n", Min("apple", "banana"))  // => Min("apple", "banana") = apple

	fmt.Printf("Sum(ints) = %d\n", Sum([]int{1, 2, 3, 4, 5}))  // => Sum(ints) = 15
	fmt.Printf("Sum(floats) = %.1f\n", Sum([]float64{1.1, 2.2, 3.3}))  // => Sum(floats) = 6.6

	fmt.Printf("Contains(\"go\") = %v\n", Contains([]string{"go", "rust", "zig"}, "go"))  // => Contains("go") = true
	fmt.Printf("Contains(99) = %v\n", Contains([]int{1, 2, 3}, 99))  // => Contains(99) = false

	doubled := Map([]int{1, 2, 3}, func(n int) int { return n * 2 })
	fmt.Printf("Map(double) = %v\n", doubled)  // => Map(double) = [2 4 6]

	asStr := Map([]int{1, 2, 3}, func(n int) string { return fmt.Sprintf("#%d", n) })
	fmt.Printf("Map(format) = %v\n", asStr)  // => Map(format) = [#1 #2 #3]
}

// ============================================================
// SECTION: Error Handling — Is, As, wrapping, sentinel, custom
// ============================================================

// Sentinel errors are package-level variables used as unique error identifiers.
// Compare with errors.Is(), not ==, because Is() unwraps error chains.
// Convention: name them ErrXxx. See Go blog: "Working with Errors in Go 1.13"
var ErrNotFound = errors.New("not found")

// Custom error types implement the error interface (Error() string).
// Use a pointer receiver so that errors.As() can match the concrete type.
// Custom types carry structured data beyond just a message string.
type ValidationError struct {
	Field   string
	Message string
}

func (e *ValidationError) Error() string {
	return fmt.Sprintf("validation: %s — %s", e.Field, e.Message)
}

// fmt.Errorf with %w wraps an error, creating an error chain. The wrapped error
// can be found with errors.Is() (for sentinel comparison) or errors.As() (for type
// extraction). This enables adding context while preserving the original error.
func findUser(id int) error {
	if id <= 0 {
		return &ValidationError{Field: "id", Message: "must be positive"}
	}
	if id > 1000 {
		return fmt.Errorf("findUser(%d): %w", id, ErrNotFound)
	}
	return nil
}

func demoErrors() {
	fmt.Println("\n=== ERROR HANDLING ===")  // => === ERROR HANDLING ===

	// errors.Is traverses the error chain (via Unwrap()) to find a matching sentinel.
	// This works even when the error has been wrapped multiple times with fmt.Errorf %w.
	err := findUser(9999)
	fmt.Printf("errors.Is(ErrNotFound): %v\n", errors.Is(err, ErrNotFound))  // => errors.Is(ErrNotFound): true

	// errors.As extracts a specific error type from the chain. It assigns the matched
	// error to the target variable, giving you access to structured error data.
	// The target must be a pointer to the error type you're looking for.
	err2 := findUser(-1)
	var ve *ValidationError
	if errors.As(err2, &ve) {
		fmt.Printf("errors.As: field=%s msg=%s\n", ve.Field, ve.Message)  // => errors.As: field=id msg=must be positive
	}

	// Error wrapping with %w creates a chain: "database query failed" wraps "connection refused".
	// errors.Is(wrapped, inner) returns true because it traverses the chain.
	inner := errors.New("connection refused")
	wrapped := fmt.Errorf("database query failed: %w", inner)
	fmt.Printf("wrapped: %v\n", wrapped)  // => wrapped: database query failed: connection refused
	fmt.Printf("unwrap match: %v\n", errors.Is(wrapped, inner))  // => unwrap match: true
}

// ============================================================
// SECTION: Standard Library — strings, strconv, sort, json, etc
// ============================================================

// Struct tags (backtick strings) are metadata read at runtime via reflection.
// The `json` tag tells encoding/json how to marshal/unmarshal fields.
// Tags follow the format: `key:"value"`. Multiple tags are space-separated.
// Common tags: json, xml, yaml, db, validate. See Go spec: Struct types
type Person struct {
	Name string `json:"name"`
	Age  int    `json:"age"`
}

func demoStdlib() {
	fmt.Println("\n=== STANDARD LIBRARY ===")  // => === STANDARD LIBRARY ===

	// strings package provides immutable string operations. Go strings are UTF-8
	// encoded byte slices — len() returns byte count, not rune count. Use
	// utf8.RuneCountInString() or range loop for Unicode-aware iteration.
	fmt.Printf("Contains: %v\n", strings.Contains("gopher", "pher"))  // => Contains: true
	fmt.Printf("Split: %v\n", strings.Split("a,b,c", ","))  // => Split: [a b c]
	fmt.Printf("Join: %s\n", strings.Join([]string{"Go", "is", "fast"}, " "))  // => Join: Go is fast
	fmt.Printf("Replace: %s\n", strings.ReplaceAll("foo-bar-baz", "-", "_"))  // => Replace: foo_bar_baz
	fmt.Printf("TrimSpace: [%s]\n", strings.TrimSpace("  hello  "))  // => TrimSpace: [hello]

	// strconv converts between strings and basic types. Atoi/Itoa handle integers.
	// ParseFloat's second arg (64) specifies the bit size for precision.
	// These functions return errors for invalid input — always check them in production.
	n, _ := strconv.Atoi("42")
	s := strconv.Itoa(42)
	f, _ := strconv.ParseFloat("3.14", 64)
	fmt.Printf("Atoi=%d  Itoa=%s  ParseFloat=%.2f\n", n, s, f)  // => Atoi=42  Itoa=42  ParseFloat=3.14

	// sort package uses an introsort variant (quicksort + heapsort + insertion sort).
	// sort.Ints/sort.Strings sort in-place. For custom sorting, implement sort.Interface
	// or use sort.Slice with a comparison function (Go 1.8+).
	nums := []int{5, 3, 8, 1, 9}
	sort.Ints(nums)
	fmt.Printf("sorted: %v\n", nums)  // => sorted: [1 3 5 8 9]

	words := []string{"banana", "apple", "cherry"}
	sort.Strings(words)
	fmt.Printf("sorted: %v\n", words)  // => sorted: [apple banana cherry]

	// encoding/json uses reflection + struct tags for serialization.
	// json.Marshal produces []byte; json.Unmarshal parses into a struct.
	// For performance-critical code, consider code-generated alternatives (easyjson).
	p := Person{Name: "Alice", Age: 30}
	data, _ := json.Marshal(p)
	fmt.Printf("json: %s\n", data)  // => json: {"name":"Alice","age":30}

	var p2 Person
	json.Unmarshal([]byte(`{"name":"Bob","age":25}`), &p2)
	fmt.Printf("unmarshal: %+v\n", p2)  // => unmarshal: {Name:Bob Age:25}

	// time package: Go uses a reference time "Mon Jan 2 15:04:05 MST 2006" (1/2 3:04:05 PM 2006)
	// as the format template — you write what that specific moment looks like in your desired format.
	// This is unique to Go; most languages use strftime-style %Y-%m-%d patterns.
	now := time.Now()
	fmt.Printf("now: %s\n", now.Format(time.RFC3339))  // => (varies)
	later := now.Add(2 * time.Hour)
	fmt.Printf("duration: %v\n", later.Sub(now))  // => duration: 2h0m0s
	parsed, _ := time.Parse("2006-01-02", "2024-06-15")
	fmt.Printf("parsed: %s\n", parsed.Format("Jan 2, 2006"))  // => parsed: Jun 15, 2024

	// regexp uses RE2 syntax — guaranteed linear time O(n) matching (no backtracking).
	// This means no catastrophic backtracking DoS, but also no backreferences or lookahead.
	// MustCompile panics on invalid patterns (use at init time); Compile returns an error.
	re := regexp.MustCompile(`(\w+)@(\w+)\.(\w+)`)
	match := re.FindStringSubmatch("user@example.com")
	fmt.Printf("regex groups: %v\n", match)  // => regex groups: [user@example.com user example com]
	replaced := re.ReplaceAllString("contact user@example.com", "REDACTED")
	fmt.Printf("regex replace: %s\n", replaced)  // => regex replace: contact REDACTED

	// filepath provides OS-aware path manipulation (uses / on Unix, \ on Windows).
	// Always use filepath.Join instead of string concatenation for cross-platform paths.
	full := filepath.Join("home", "user", "docs", "file.txt")
	fmt.Printf("filepath.Join: %s\n", full)  // => filepath.Join: home/user/docs/file.txt
	fmt.Printf("Dir=%s  Base=%s  Ext=%s\n", filepath.Dir(full), filepath.Base(full), filepath.Ext(full))  // => Dir=home/user/docs  Base=file.txt  Ext=.txt
}

// ============================================================
// MAIN
// ============================================================

func main() {
	fmt.Println("==================================================")  // => ==================================================
	fmt.Println("  Go Fundamentals — Comprehensive Reference")  // => Go Fundamentals — Comprehensive Reference
	fmt.Println("==================================================")  // => ==================================================

	demoBasics()
	demoTypes()
	demoCollections()
	demoFunctions()
	demoInterfaces()
	demoConcurrency()
	demoPatterns()
	demoGenerics()
	demoErrors()
	demoStdlib()

	fmt.Println("\n== Done ==")  // => == Done ==
}
