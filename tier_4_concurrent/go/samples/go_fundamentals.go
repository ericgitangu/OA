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

const Pi = 3.14159

const (
	Sunday    = iota // 0
	Monday           // 1
	Tuesday          // 2
	Wednesday        // 3
	Thursday         // 4
	Friday           // 5
	Saturday         // 6
)

func divide(a, b float64) (float64, error) {
	if b == 0 {
		return 0, fmt.Errorf("division by zero")
	}
	return a / b, nil
}

func namedReturns(x, y int) (sum int, diff int) {
	sum = x + y
	diff = x - y
	return // naked return uses named values
}

func demoBasics() {
	fmt.Println("\n=== BASICS ===")

	// var declarations
	var name string = "Go"
	age := 15 // short declaration
	var untyped = 42.0
	fmt.Printf("name=%s  age=%d  untyped=%.1f\n", name, age, untyped)

	// constants & iota
	fmt.Printf("Pi=%.5f  Sunday=%d  Saturday=%d\n", Pi, Sunday, Saturday)

	// multiple return values
	result, err := divide(10, 3)
	fmt.Printf("10/3 = %.4f  err=%v\n", result, err)

	// named returns
	s, d := namedReturns(10, 3)
	fmt.Printf("sum=%d  diff=%d\n", s, d)

	// blank identifier — discard a value
	_, err2 := divide(1, 0)
	fmt.Printf("ignored result, err=%v\n", err2)
}

// ============================================================
// SECTION: Types — structs, interfaces, embedding, assertions
// ============================================================

type Shape interface {
	Area() float64
	Perimeter() float64
}

type Circle struct {
	Radius float64
}

func (c Circle) Area() float64      { return math.Pi * c.Radius * c.Radius }
func (c Circle) Perimeter() float64 { return 2 * math.Pi * c.Radius }

type Rectangle struct {
	Width, Height float64
}

func (r Rectangle) Area() float64      { return r.Width * r.Height }
func (r Rectangle) Perimeter() float64 { return 2 * (r.Width + r.Height) }

// Embedding — LabeledShape "inherits" Shape methods from its embedded field
type LabeledShape struct {
	Shape
	Label string
}

func demoTypes() {
	fmt.Println("\n=== TYPES ===")

	c := Circle{Radius: 5}
	r := Rectangle{Width: 3, Height: 4}
	fmt.Printf("Circle  area=%.2f  perim=%.2f\n", c.Area(), c.Perimeter())
	fmt.Printf("Rect    area=%.2f  perim=%.2f\n", r.Area(), r.Perimeter())

	// Embedding
	ls := LabeledShape{Shape: c, Label: "unit-circle"}
	fmt.Printf("Labeled: %s  area=%.2f\n", ls.Label, ls.Area())

	// Type assertion
	var s Shape = c
	if circle, ok := s.(Circle); ok {
		fmt.Printf("Type assertion: radius=%.1f\n", circle.Radius)
	}

	// Type switch
	shapes := []Shape{c, r}
	for _, sh := range shapes {
		switch v := sh.(type) {
		case Circle:
			fmt.Printf("  type-switch: Circle r=%.1f\n", v.Radius)
		case Rectangle:
			fmt.Printf("  type-switch: Rect %gx%g\n", v.Width, v.Height)
		}
	}
}

// ============================================================
// SECTION: Collections — slices, maps, arrays
// ============================================================

func demoCollections() {
	fmt.Println("\n=== COLLECTIONS ===")

	// Arrays (fixed size)
	arr := [3]int{10, 20, 30}
	fmt.Printf("array: %v  len=%d\n", arr, len(arr))

	// Slices
	nums := []int{5, 3, 8, 1, 9, 2}
	nums = append(nums, 7, 4)
	fmt.Printf("slice after append: %v\n", nums)

	// Copy
	dst := make([]int, 4)
	n := copy(dst, nums)
	fmt.Printf("copied %d elements: %v\n", n, dst)

	// Slicing
	sub := nums[2:5]
	fmt.Printf("nums[2:5] = %v\n", sub)

	// Maps
	m := map[string]int{"alice": 90, "bob": 85, "carol": 92}
	m["dave"] = 88
	delete(m, "bob")
	if score, ok := m["carol"]; ok {
		fmt.Printf("carol's score: %d\n", score)
	}
	fmt.Printf("map keys: ")
	for k := range m {
		fmt.Printf("%s ", k)
	}
	fmt.Println()
}

// ============================================================
// SECTION: Functions — variadic, closures, defer/panic/recover
// ============================================================

func sum(nums ...int) int {
	total := 0
	for _, n := range nums {
		total += n
	}
	return total
}

func makeCounter() func() int {
	count := 0
	return func() int {
		count++
		return count
	}
}

func safeDivide(a, b int) (result int, err error) {
	defer func() {
		if r := recover(); r != nil {
			err = fmt.Errorf("recovered panic: %v", r)
		}
	}()
	return a / b, nil // panics if b == 0 (integer division)
}

// Value receiver — operates on a copy
func (r Rectangle) Scale(factor float64) Rectangle {
	return Rectangle{r.Width * factor, r.Height * factor}
}

// Pointer receiver — mutates the original
func (r *Rectangle) ScaleInPlace(factor float64) {
	r.Width *= factor
	r.Height *= factor
}

func demoFunctions() {
	fmt.Println("\n=== FUNCTIONS ===")

	// Variadic
	fmt.Printf("sum(1,2,3) = %d\n", sum(1, 2, 3))
	nums := []int{4, 5, 6}
	fmt.Printf("sum(slice...) = %d\n", sum(nums...))

	// Closure
	counter := makeCounter()
	fmt.Printf("counter: %d, %d, %d\n", counter(), counter(), counter())

	// Defer / panic / recover
	_, err := safeDivide(10, 0)
	fmt.Printf("safeDivide(10,0) err=%v\n", err)

	// Method receivers
	r := Rectangle{3, 4}
	scaled := r.Scale(2)
	fmt.Printf("Scale(2): %gx%g (original %gx%g)\n", scaled.Width, scaled.Height, r.Width, r.Height)
	r.ScaleInPlace(2)
	fmt.Printf("ScaleInPlace(2): %gx%g\n", r.Width, r.Height)
}

// ============================================================
// SECTION: Interfaces — implicit, empty, Stringer, io
// ============================================================

type Stringer interface {
	String() string
}

type Point struct{ X, Y float64 }

func (p Point) String() string {
	return fmt.Sprintf("(%g, %g)", p.X, p.Y)
}

func printAnything(v interface{}) {
	fmt.Printf("  empty-interface: %v (type %T)\n", v, v)
}

func demoInterfaces() {
	fmt.Println("\n=== INTERFACES ===")

	// Implicit satisfaction — Point satisfies Stringer without declaring it
	p := Point{3, 4}
	fmt.Printf("Stringer: %s\n", p)

	// Empty interface accepts any type
	printAnything(42)
	printAnything("hello")
	printAnything([]int{1, 2, 3})

	// io.Reader/Writer via strings
	reader := strings.NewReader("Go is great")
	buf := make([]byte, 5)
	n, _ := reader.Read(buf)
	fmt.Printf("io.Reader first %d bytes: %s\n", n, buf[:n])
}

// ============================================================
// SECTION: Concurrency — goroutines, channels, sync
// ============================================================

func producer(ch chan<- int, start, count int) {
	for i := start; i < start+count; i++ {
		ch <- i
	}
}

func demoConcurrency() {
	fmt.Println("\n=== CONCURRENCY ===")

	// Goroutines + WaitGroup
	var wg sync.WaitGroup
	for i := 0; i < 3; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			fmt.Printf("  goroutine %d running\n", id)
		}(i)
	}
	wg.Wait()

	// Unbuffered channel
	ch := make(chan string)
	go func() { ch <- "ping" }()
	fmt.Printf("received: %s\n", <-ch)

	// Buffered channel
	bch := make(chan int, 3)
	bch <- 1
	bch <- 2
	bch <- 3
	fmt.Printf("buffered: %d %d %d\n", <-bch, <-bch, <-bch)

	// Select
	ch1 := make(chan string, 1)
	ch2 := make(chan string, 1)
	ch1 <- "one"
	ch2 <- "two"
	select {
	case v := <-ch1:
		fmt.Printf("select got: %s\n", v)
	case v := <-ch2:
		fmt.Printf("select got: %s\n", v)
	}

	// Mutex
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
	fmt.Printf("mutex counter: %d\n", counter)

	// sync.Once
	var once sync.Once
	for i := 0; i < 3; i++ {
		once.Do(func() {
			fmt.Println("once.Do: runs only once")
		})
	}

	// sync.Map
	var sm sync.Map
	sm.Store("lang", "Go")
	sm.Store("year", 2009)
	sm.Range(func(key, value interface{}) bool {
		fmt.Printf("  sync.Map: %v=%v\n", key, value)
		return true
	})
}

// ============================================================
// SECTION: Patterns — fan-out/fan-in, pipeline, context
// ============================================================

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
	fmt.Println("\n=== PATTERNS ===")

	// Pipeline: generator -> square -> consume
	pipeline := square(generator(1, 2, 3, 4, 5))
	fmt.Print("pipeline squares: ")
	for v := range pipeline {
		fmt.Printf("%d ", v)
	}
	fmt.Println()

	// Fan-out / fan-in
	src := generator(10, 20, 30, 40)
	sq1 := square(src) // single fan-out for brevity
	for v := range sq1 {
		fmt.Printf("  fan-out result: %d\n", v)
	}

	// Merge demonstration
	merged := merge(generator(1, 2), generator(3, 4))
	fmt.Print("merged: ")
	for v := range merged {
		fmt.Printf("%d ", v)
	}
	fmt.Println()

	// Context with timeout
	ctx, cancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
	defer cancel()

	select {
	case <-time.After(100 * time.Millisecond):
		fmt.Println("work completed")
	case <-ctx.Done():
		fmt.Printf("context: %v\n", ctx.Err())
	}

	// Context with cancellation
	ctx2, cancel2 := context.WithCancel(context.Background())
	go func() {
		time.Sleep(10 * time.Millisecond)
		cancel2()
	}()
	<-ctx2.Done()
	fmt.Printf("cancelled: %v\n", ctx2.Err())
}

// ============================================================
// SECTION: Generics — type parameters, constraints
// ============================================================

func Min[T int | float64 | string](a, b T) T {
	if a < b {
		return a
	}
	return b
}

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

func Contains[T comparable](slice []T, target T) bool {
	for _, v := range slice {
		if v == target {
			return true
		}
	}
	return false
}

func Map[T any, U any](slice []T, fn func(T) U) []U {
	result := make([]U, len(slice))
	for i, v := range slice {
		result[i] = fn(v)
	}
	return result
}

func demoGenerics() {
	fmt.Println("\n=== GENERICS ===")

	fmt.Printf("Min(3, 7) = %d\n", Min(3, 7))
	fmt.Printf("Min(3.14, 2.71) = %.2f\n", Min(3.14, 2.71))
	fmt.Printf("Min(\"apple\", \"banana\") = %s\n", Min("apple", "banana"))

	fmt.Printf("Sum(ints) = %d\n", Sum([]int{1, 2, 3, 4, 5}))
	fmt.Printf("Sum(floats) = %.1f\n", Sum([]float64{1.1, 2.2, 3.3}))

	fmt.Printf("Contains(\"go\") = %v\n", Contains([]string{"go", "rust", "zig"}, "go"))
	fmt.Printf("Contains(99) = %v\n", Contains([]int{1, 2, 3}, 99))

	doubled := Map([]int{1, 2, 3}, func(n int) int { return n * 2 })
	fmt.Printf("Map(double) = %v\n", doubled)

	asStr := Map([]int{1, 2, 3}, func(n int) string { return fmt.Sprintf("#%d", n) })
	fmt.Printf("Map(format) = %v\n", asStr)
}

// ============================================================
// SECTION: Error Handling — Is, As, wrapping, sentinel, custom
// ============================================================

// Sentinel error
var ErrNotFound = errors.New("not found")

// Custom error type
type ValidationError struct {
	Field   string
	Message string
}

func (e *ValidationError) Error() string {
	return fmt.Sprintf("validation: %s — %s", e.Field, e.Message)
}

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
	fmt.Println("\n=== ERROR HANDLING ===")

	// Sentinel error with errors.Is (works through wrapping)
	err := findUser(9999)
	fmt.Printf("errors.Is(ErrNotFound): %v\n", errors.Is(err, ErrNotFound))

	// Custom error with errors.As
	err2 := findUser(-1)
	var ve *ValidationError
	if errors.As(err2, &ve) {
		fmt.Printf("errors.As: field=%s msg=%s\n", ve.Field, ve.Message)
	}

	// fmt.Errorf wrapping
	inner := errors.New("connection refused")
	wrapped := fmt.Errorf("database query failed: %w", inner)
	fmt.Printf("wrapped: %v\n", wrapped)
	fmt.Printf("unwrap match: %v\n", errors.Is(wrapped, inner))
}

// ============================================================
// SECTION: Standard Library — strings, strconv, sort, json, etc
// ============================================================

type Person struct {
	Name string `json:"name"`
	Age  int    `json:"age"`
}

func demoStdlib() {
	fmt.Println("\n=== STANDARD LIBRARY ===")

	// strings
	fmt.Printf("Contains: %v\n", strings.Contains("gopher", "pher"))
	fmt.Printf("Split: %v\n", strings.Split("a,b,c", ","))
	fmt.Printf("Join: %s\n", strings.Join([]string{"Go", "is", "fast"}, " "))
	fmt.Printf("Replace: %s\n", strings.ReplaceAll("foo-bar-baz", "-", "_"))
	fmt.Printf("TrimSpace: [%s]\n", strings.TrimSpace("  hello  "))

	// strconv
	n, _ := strconv.Atoi("42")
	s := strconv.Itoa(42)
	f, _ := strconv.ParseFloat("3.14", 64)
	fmt.Printf("Atoi=%d  Itoa=%s  ParseFloat=%.2f\n", n, s, f)

	// sort
	nums := []int{5, 3, 8, 1, 9}
	sort.Ints(nums)
	fmt.Printf("sorted: %v\n", nums)

	words := []string{"banana", "apple", "cherry"}
	sort.Strings(words)
	fmt.Printf("sorted: %v\n", words)

	// encoding/json
	p := Person{Name: "Alice", Age: 30}
	data, _ := json.Marshal(p)
	fmt.Printf("json: %s\n", data)

	var p2 Person
	json.Unmarshal([]byte(`{"name":"Bob","age":25}`), &p2)
	fmt.Printf("unmarshal: %+v\n", p2)

	// time
	now := time.Now()
	fmt.Printf("now: %s\n", now.Format(time.RFC3339))
	later := now.Add(2 * time.Hour)
	fmt.Printf("duration: %v\n", later.Sub(now))
	parsed, _ := time.Parse("2006-01-02", "2024-06-15")
	fmt.Printf("parsed: %s\n", parsed.Format("Jan 2, 2006"))

	// regexp
	re := regexp.MustCompile(`(\w+)@(\w+)\.(\w+)`)
	match := re.FindStringSubmatch("user@example.com")
	fmt.Printf("regex groups: %v\n", match)
	replaced := re.ReplaceAllString("contact user@example.com", "REDACTED")
	fmt.Printf("regex replace: %s\n", replaced)

	// filepath
	full := filepath.Join("home", "user", "docs", "file.txt")
	fmt.Printf("filepath.Join: %s\n", full)
	fmt.Printf("Dir=%s  Base=%s  Ext=%s\n", filepath.Dir(full), filepath.Base(full), filepath.Ext(full))
}

// ============================================================
// MAIN
// ============================================================

func main() {
	fmt.Println("==================================================")
	fmt.Println("  Go Fundamentals — Comprehensive Reference")
	fmt.Println("==================================================")

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

	fmt.Println("\n== Done ==")
}
