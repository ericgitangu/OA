import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.locks.*;
import java.util.function.*;
import java.util.stream.*;

/**
 * Java 21 Fundamentals — single runnable file.
 * Compile & run:  javac JavaFundamentals.java && java JavaFundamentals
 */
public class JavaFundamentals {

    // Records (JEP 395, Java 16): immutable data carriers that auto-generate
    // equals(), hashCode(), toString(), and accessor methods. They replace the
    // boilerplate of writing POJOs and are final by design — you cannot extend them.
    // Use records when you need a transparent, immutable data holder (like a DTO or value object).
    record Point(double x, double y) {
        // Compact canonical constructor: Java lets you omit the parameter list when
        // you only need to validate/normalize — the fields are assigned automatically
        // after this block runs. This avoids the redundant `this.x = x` pattern.
        Point {
            if (Double.isNaN(x) || Double.isNaN(y))
                throw new IllegalArgumentException("coordinates must not be NaN");
        }

        double distanceTo(Point other) {
            return Math.sqrt(Math.pow(x - other.x, 2) + Math.pow(y - other.y, 2));
        }
    }

    // Generic records work like generic classes — the type parameters are erased at
    // runtime (type erasure, JLS §4.6) but enforced at compile time. You cannot do
    // `instanceof Pair<String, Integer>` at runtime because the JVM only sees `Pair`.
    record Pair<A, B>(A first, B second) {}

    // Sealed classes (JEP 409, Java 17): restrict which classes can implement/extend
    // this interface using `permits`. The compiler knows ALL possible subtypes at compile
    // time, enabling exhaustive switch expressions without a default branch. This is
    // Java's approach to algebraic data types (ADTs) — compare with Kotlin's sealed classes
    // and Scala's sealed traits + case classes.
    sealed interface Shape permits Circle, Rectangle, Triangle {
        double area();
    }

    record Circle(double radius) implements Shape {
        public double area() { return Math.PI * radius * radius; }
    }

    record Rectangle(double width, double height) implements Shape {
        public double area() { return width * height; }
    }

    record Triangle(double base, double height) implements Shape {
        public double area() { return 0.5 * base * height; }
    }

    // Interfaces in Java can have default methods (Java 8+), enabling a form of
    // multiple inheritance for behavior (but not state). Unlike Kotlin/Scala traits,
    // Java interfaces cannot hold mutable state — only constants (public static final).
    interface Describable {
        String describe();

        // Default methods let you add new methods to interfaces without breaking existing
        // implementations. This was critical for evolving the Collections API in Java 8.
        default String tag() { return "[" + describe() + "]"; }
    }

    // Abstract classes vs interfaces: use abstract classes when you need shared state
    // (instance fields like `name`) across subclasses. Interfaces are better for defining
    // capabilities/contracts. Java forces this choice because it lacks Scala/Kotlin's
    // trait state or Kotlin's constructor parameters in interfaces.
    abstract static class Animal implements Describable {
        final String name;
        Animal(String name) { this.name = name; }
        abstract String sound();

        @Override
        public String describe() { return name + " says " + sound(); }
    }

    // Concrete classes must provide implementations for all abstract methods.
    // The `static` modifier is required for nested classes in Java to avoid
    // capturing a reference to the enclosing instance (inner class vs nested class).
    static class Dog extends Animal {
        Dog(String name) { super(name); }
        @Override String sound() { return "woof"; }
    }

    static class Cat extends Animal {
        Cat(String name) { super(name); }
        @Override String sound() { return "meow"; }
    }

    // Upper-bounded generics (`T extends Comparable<T>`): constrains T to types that
    // implement Comparable. This is Java's equivalent of Scala's context bounds or
    // Kotlin's `: Comparable<T>`. The bound is enforced at compile time but erased
    // at runtime — the JVM sees this as just `Object` after erasure.
    static <T extends Comparable<T>> T max(T a, T b) {
        return a.compareTo(b) >= 0 ? a : b;
    }

    // Upper-bounded wildcard (`? extends Number`): accepts List<Integer>, List<Double>,
    // etc. This is the PECS principle — "Producer Extends" — the list PRODUCES Number
    // values (you can read from it but not write to it). Kotlin uses `out` for this.
    static double sumOfNumbers(List<? extends Number> nums) {
        return nums.stream().mapToDouble(Number::doubleValue).sum();
    }

    // Lower-bounded wildcard (`? super Integer`): accepts List<Integer>, List<Number>,
    // List<Object>. This is "Consumer Super" — the list CONSUMES Integer values (you can
    // write to it but reads only give you Object). Kotlin uses `in` for this.
    static void addIntegers(List<? super Integer> list) {
        list.add(42);
        list.add(99);
    }

    // Custom checked exceptions extend Exception (must be caught or declared).
    // Unchecked exceptions extend RuntimeException (no obligation to handle).
    // Kotlin and Scala eliminated checked exceptions entirely — they're a Java-only
    // JVM concept that the bytecode doesn't enforce.
    static class InsufficientFundsException extends Exception {
        private final double deficit;

        InsufficientFundsException(double deficit) {
            // String.formatted() (Java 15+): instance method alternative to String.format().
            super("Insufficient funds: short by $%.2f".formatted(deficit));
            this.deficit = deficit;
        }

        double getDeficit() { return deficit; }
    }

    // AutoCloseable enables try-with-resources (Java 7+): the JVM guarantees close()
    // is called even if an exception is thrown, in reverse declaration order. This is
    // Java's RAII-like pattern — compare with Kotlin's .use{} and Scala's Using().
    static class ManagedResource implements AutoCloseable {
        private final String id;
        private boolean open = true;

        ManagedResource(String id) {
            this.id = id;
            System.out.println("    Resource [" + id + "] opened");  // => (varies)
        }

        void use() {
            if (!open) throw new IllegalStateException("resource closed");
            System.out.println("    Resource [" + id + "] in use");  // => (varies)
        }

        @Override
        public void close() {
            open = false;
            System.out.println("    Resource [" + id + "] closed");  // => (varies)
        }
    }

    // ═══════════════════════════════════════════════════════════════════
    // MAIN
    // ═══════════════════════════════════════════════════════════════════
    public static void main(String[] args) throws Exception {
        basics();
        collections();
        streams();
        oop();
        patternMatching();
        functional();
        errorHandling();
        concurrency();
        fileIO();
    }

    // ── 1. Basics ─────────────────────────────────────────────────────
    static void basics() {
        System.out.println("=== 1. BASICS ===");  // => === 1. BASICS ===

        // `var` (JEP 286, Java 10): local variable type inference. The compiler infers
        // the type from the right-hand side — `var` is NOT dynamic typing, the type is
        // still fixed at compile time. Cannot be used for fields, method params, or return
        // types. Kotlin's `val`/`var` and Scala's `val`/`var` serve a similar role but
        // also work at class level and distinguish mutability.
        var greeting = "Hello, Java 21!";
        var count = 42;
        var pi = 3.14159;
        System.out.println("  var greeting: " + greeting);  // => var greeting: Hello, Java 21!
        System.out.println("  var count: " + count + ", pi: " + pi);  // => var count: 42, pi: 3.14159

        // Text blocks (JEP 378, Java 15): multi-line string literals that preserve
        // formatting. The closing `"""` position determines the indentation baseline —
        // common leading whitespace is stripped automatically. Compare with Kotlin's
        // trimMargin() and Scala's stripMargin, which use explicit margin characters.
        var json = """
                {
                    "name": "Alice",
                    "age": 30,
                    "languages": ["Java", "Kotlin", "Scala"]
                }
                """;
        System.out.println("  Text block:\n" + json);  // => Text block: (followed by formatted JSON)

        // Switch expressions (JEP 361, Java 14): unlike switch statements, these return
        // a value and use `->` (arrow) syntax that doesn't fall through. The compiler
        // enforces exhaustiveness when used as an expression. This is Java's version of
        // Kotlin's `when` expression and Scala's `match` expression.
        var dayNum = 3;
        var dayName = switch (dayNum) {
            case 1 -> "Monday";
            case 2 -> "Tuesday";
            case 3 -> "Wednesday";
            case 4 -> "Thursday";
            case 5 -> "Friday";
            case 6, 7 -> "Weekend";
            default -> "Unknown";
        };
        System.out.println("  Day " + dayNum + " = " + dayName);  // => Day 3 = Wednesday

        // Record instantiation: no `new` keyword elimination in Java (unlike Scala's
        // case classes). Records provide value semantics — two Points with the same
        // coordinates are equals() and have the same hashCode().
        var p1 = new Point(3.0, 4.0);
        var p2 = new Point(0.0, 0.0);
        System.out.println("  Point: " + p1 + ", distance to origin: " + p1.distanceTo(p2));  // => Point: Point[x=3.0, y=4.0], distance to origin: 5.0

        // Sealed types + records together form Java's algebraic data type system.
        // The sealed interface defines the sum type, records define the product types.
        Shape shape = new Circle(5);
        System.out.println("  Circle area: " + shape.area());  // => Circle area: 78.53981633974483
        System.out.println();
    }

    // ── 2. Collections ────────────────────────────────────────────────
    static void collections() {
        System.out.println("=== 2. COLLECTIONS ===");  // => === 2. COLLECTIONS ===

        // Immutable factory methods (JEP 269, Java 9): List.of(), Map.of(), Set.of()
        // create truly unmodifiable collections (not just wrapped — the internal
        // implementation rejects mutations). Attempting add/remove throws
        // UnsupportedOperationException. Kotlin/Scala collections are immutable by default.
        var names = List.of("Alice", "Bob", "Charlie", "Diana");
        var scores = Map.of("Alice", 95, "Bob", 87, "Charlie", 92);
        var uniqueTags = Set.of("java", "jvm", "oop");
        System.out.println("  List: " + names);  // => List: [Alice, Bob, Charlie, Diana]
        System.out.println("  Map: " + scores);  // => Map: {Alice=95, Bob=87, Charlie=92}
        System.out.println("  Set: " + uniqueTags);  // => Set: [java, jvm, oop]

        // Mutable collections require explicit construction. Java's Collections framework
        // defaults to mutable — the opposite of Kotlin and Scala, which default to
        // immutable views. In production, prefer immutable unless mutation is necessary.
        var mutableList = new ArrayList<>(names);
        mutableList.add("Eve");
        mutableList.sort(Comparator.reverseOrder());
        System.out.println("  Sorted desc: " + mutableList);  // => Sorted desc: [Eve, Diana, Charlie, Bob, Alice]

        // Map.merge(): atomically combines a new value with an existing one using
        // a remapping function. The third argument (Integer::sum) is called only when
        // the key already exists. This replaces the get-check-put pattern.
        var wordCounts = new HashMap<String, Integer>();
        for (var word : "the cat sat on the mat".split(" ")) {
            wordCounts.merge(word, 1, Integer::sum);
        }
        System.out.println("  Word counts: " + wordCounts);  // => (varies — HashMap order is non-deterministic)

        // ArrayDeque: Java's recommended queue/stack implementation (faster than
        // LinkedList for both FIFO and LIFO). offer/poll for queues, push/pop for stacks.
        // Unlike Stack (legacy, synchronized), ArrayDeque is unsynchronized and resizable.
        var queue = new ArrayDeque<String>();
        queue.offer("first");
        queue.offer("second");
        queue.offer("third");
        System.out.println("  Queue poll: " + queue.poll() + ", remaining: " + queue);  // => Queue poll: first, remaining: [second, third]

        // LinkedHashMap maintains insertion order (unlike HashMap which is unordered
        // and TreeMap which is sorted by key). Useful for caches — its constructor
        // accepts an `accessOrder` flag for LRU eviction.
        var ordered = new LinkedHashMap<String, Integer>();
        ordered.put("z", 1);
        ordered.put("a", 2);
        ordered.put("m", 3);
        System.out.println("  Insertion-ordered map: " + ordered);  // => Insertion-ordered map: {z=1, a=2, m=3}
        System.out.println();
    }

    // ── 3. Stream API ─────────────────────────────────────────────────
    static void streams() {
        System.out.println("=== 3. STREAM API ===");  // => === 3. STREAM API ===

        var numbers = List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

        // Streams (Java 8+): a pipeline of lazy, one-shot transformations over data.
        // Intermediate operations (filter, map) are lazy — nothing executes until a
        // terminal operation (toList, reduce, collect) triggers the pipeline. Compare
        // with Kotlin's Sequences and Scala's LazyList/views.
        var evenSquares = numbers.stream()
                .filter(n -> n % 2 == 0)
                .map(n -> n * n)
                .toList();
        System.out.println("  Even squares: " + evenSquares);  // => Even squares: [4, 16, 36, 64, 100]

        // reduce(): combines elements into a single result using an associative
        // accumulator. The first argument (0) is the identity value — it must satisfy
        // identity + x == x for all x. Using the wrong identity corrupts parallel streams.
        var sum = numbers.stream().reduce(0, Integer::sum);
        System.out.println("  Sum: " + sum);  // => Sum: 55

        // Collectors.groupingBy(): partitions elements into a Map<K, List<V>> by a
        // classifier function. This is a downstream collector pattern — you can chain
        // secondary collectors like counting(), averaging(), etc.
        var words = List.of("apple", "banana", "avocado", "blueberry", "cherry", "apricot");
        var byFirstLetter = words.stream()
                .collect(Collectors.groupingBy(w -> w.charAt(0)));
        System.out.println("  Grouped by first letter: " + byFirstLetter);  // => Grouped by first letter: {a=[apple, avocado, apricot], b=[banana, blueberry], c=[cherry]}

        // Collectors.joining(): concatenates CharSequence elements with a delimiter.
        // More efficient than repeated string concatenation because it uses StringBuilder
        // internally.
        var csv = words.stream().collect(Collectors.joining(", "));
        System.out.println("  Joined: " + csv);  // => Joined: apple, banana, avocado, blueberry, cherry, apricot

        // flatMap(): flattens nested structures by mapping each element to a stream and
        // concatenating the results. Essential for one-to-many transformations. Equivalent
        // to Scala's flatMap and Kotlin's flatMap.
        var nested = List.of(List.of(1, 2), List.of(3, 4), List.of(5));
        var flat = nested.stream().flatMap(Collection::stream).toList();
        System.out.println("  Flattened: " + flat);  // => Flattened: [1, 2, 3, 4, 5]

        // partitioningBy(): a specialized groupingBy that splits into exactly two groups
        // (true/false) based on a predicate. Returns Map<Boolean, List<T>>.
        var partitioned = numbers.stream()
                .collect(Collectors.partitioningBy(n -> n > 5));
        System.out.println("  Partitioned >5: " + partitioned);  // => Partitioned >5: {false=[1, 2, 3, 4, 5], true=[6, 7, 8, 9, 10]}

        // IntStream/LongStream/DoubleStream: primitive-specialized streams that avoid
        // boxing overhead. summaryStatistics() computes count, sum, min, max, and average
        // in a single pass — far more efficient than computing each separately.
        var stats = numbers.stream().mapToInt(Integer::intValue).summaryStatistics();
        System.out.println("  Stats: avg=" + stats.getAverage() + ", max=" + stats.getMax());  // => Stats: avg=5.5, max=10
        System.out.println();
    }

    // ── 4. OOP ────────────────────────────────────────────────────────
    static void oop() {
        System.out.println("=== 4. OOP ===");  // => === 4. OOP ===

        // Polymorphism through abstract classes: the variable type is Animal but the
        // runtime type determines which sound() is called (virtual method dispatch).
        // Java methods are virtual by default — unlike C++ where you must say `virtual`.
        Animal dog = new Dog("Rex");
        Animal cat = new Cat("Whiskers");
        System.out.println("  " + dog.describe());  // => Rex says woof
        System.out.println("  " + cat.tag());  // => [Whiskers says meow]

        // Generics with Comparable bound: the compiler ensures both arguments are the
        // same type T and that T has a natural ordering. After type erasure, the JVM
        // sees max(Comparable, Comparable) — generic type information is compile-time only.
        System.out.println("  max(3, 7) = " + max(3, 7));  // => max(3, 7) = 7
        System.out.println("  max(\"apple\", \"banana\") = " + max("apple", "banana"));  // => max("apple", "banana") = banana

        // PECS in action: `? extends Number` lets us read Numbers from any numeric list
        // (List<Integer>, List<Double>, etc.) without unsafe casts.
        var ints = List.of(1, 2, 3);
        var doubles = List.of(1.5, 2.5, 3.5);
        System.out.println("  sumOfNumbers(ints) = " + sumOfNumbers(ints));  // => sumOfNumbers(ints) = 6.0
        System.out.println("  sumOfNumbers(doubles) = " + sumOfNumbers(doubles));  // => sumOfNumbers(doubles) = 7.5

        // `? super Integer` lets us write Integers into any list that can hold them
        // (List<Integer>, List<Number>, List<Object>).
        List<Number> numList = new ArrayList<>();
        addIntegers(numList);
        System.out.println("  After addIntegers: " + numList);  // => After addIntegers: [42, 99]

        // Generic records use the same type erasure as generic classes — the type
        // parameters are available via reflection only as metadata, not at runtime.
        var pair = new Pair<>("key", 42);
        System.out.println("  Pair: " + pair);  // => Pair: Pair[first=key, second=42]
        System.out.println();
    }

    // ── 5. Pattern matching ───────────────────────────────────────────
    static void patternMatching() {
        System.out.println("=== 5. PATTERN MATCHING ===");  // => === 5. PATTERN MATCHING ===

        // Pattern matching for instanceof (JEP 394, Java 16): combines type check and
        // cast in one expression. The binding variable `s` is in scope only where the
        // pattern matches — the compiler uses flow scoping (not block scoping) so `s`
        // is usable in the && clause and the if-body but not after.
        Object obj = "Hello, Pattern Matching!";
        if (obj instanceof String s && s.length() > 5) {
            System.out.println("  instanceof pattern: \"" + s.toUpperCase() + "\"");  // => instanceof pattern: "HELLO, PATTERN MATCHING!"
        }

        // Switch pattern matching (JEP 441, Java 21): combines type patterns, guarded
        // patterns (`when`), record deconstruction, and null handling in a single switch.
        // This is Java's most powerful pattern matching feature — comparable to Scala's
        // match expressions (which have had this since Scala 1.0). Order matters: more
        // specific patterns (Integer with guard) must precede more general ones (Integer).
        // List.of() does not allow null — use Arrays.asList() instead
        List<Object> items = java.util.Arrays.asList(42, "text", 3.14, new Point(1, 2), null);
        for (var item : items) {
            var description = switch (item) {
                case Integer i when i > 100 -> "large int: " + i;
                case Integer i              -> "int: " + i;
                case String s               -> "string of length " + s.length();
                case Double d               -> "double: " + d;
                // Record pattern (JEP 440): deconstructs the record into its components.
                // This works recursively — you can nest patterns inside patterns.
                case Point(var x, var y)    -> "point at (" + x + ", " + y + ")";
                // null case (new in Java 21): previously, switch would throw NPE on null.
                // Now you can explicitly handle it as a case.
                case null                   -> "null value";
                default                     -> "other: " + item;
            };
            System.out.println("    " + description);  // => int: 42 | string of length 4 | double: 3.14 | point at (1.0, 2.0) | null value
        }

        // Exhaustive switch on sealed types: the compiler knows all permitted subtypes,
        // so no `default` branch is needed. If you add a new Shape subtype and forget
        // to update this switch, the compiler will produce an error — a major advantage
        // over if-else chains for maintaining correctness during refactoring.
        Shape shape = new Triangle(10, 5);
        var desc = switch (shape) {
            case Circle c    -> "Circle r=" + c.radius();
            case Rectangle r -> "Rect " + r.width() + "x" + r.height();
            case Triangle t  -> "Triangle base=" + t.base() + " h=" + t.height();
        };
        System.out.println("  Sealed switch: " + desc + ", area=" + shape.area());  // => Sealed switch: Triangle base=10.0 h=5.0, area=25.0
        System.out.println();
    }

    // ── 6. Functional programming ─────────────────────────────────────
    static void functional() {
        System.out.println("=== 6. FUNCTIONAL ===");  // => === 6. FUNCTIONAL ===

        // Lambdas (Java 8+): anonymous functions that implement a functional interface
        // (an interface with exactly one abstract method, aka SAM type). Under the hood,
        // the JVM uses invokedynamic (JEP 276) to generate lambda classes at runtime —
        // more efficient than anonymous inner classes.
        Comparator<String> byLength = (a, b) -> Integer.compare(a.length(), b.length());
        var sorted = List.of("banana", "fig", "cherry", "apple");
        var result = sorted.stream().sorted(byLength).toList();
        System.out.println("  Sorted by length: " + result);  // => Sorted by length: [fig, apple, banana, cherry]

        // Method references: shorthand for lambdas that just call an existing method.
        // Four kinds: static (Class::static), instance (obj::method), arbitrary instance
        // (Class::instance), and constructor (Class::new). The compiler infers which
        // form based on the target functional interface's signature.
        var upper = List.of("hello", "world").stream()
                .map(String::toUpperCase)
                .toList();
        System.out.println("  Method ref: " + upper);  // => Method ref: [HELLO, WORLD]

        // Function composition: andThen() applies this function first, then the argument.
        // compose() applies the argument first, then this function. These are the only
        // built-in composition methods — Kotlin and Scala offer richer function combinators.
        Function<Integer, Integer> doubleIt = x -> x * 2;
        Function<Integer, Integer> addTen = x -> x + 10;
        Function<Integer, Integer> doubleThenAdd = doubleIt.andThen(addTen);
        Function<Integer, Integer> addThenDouble = doubleIt.compose(addTen);
        System.out.println("  doubleThenAdd(5) = " + doubleThenAdd.apply(5));  // => doubleThenAdd(5) = 20
        System.out.println("  addThenDouble(5) = " + addThenDouble.apply(5));  // => addThenDouble(5) = 30

        // Predicate composition: and(), or(), negate() combine predicates logically.
        // These are short-circuiting — same semantics as && and ||.
        Predicate<String> isLong = s -> s.length() > 4;
        Predicate<String> startsWithA = s -> s.startsWith("a");
        var filtered = List.of("apple", "ant", "banana", "avocado").stream()
                .filter(isLong.and(startsWithA))
                .toList();
        System.out.println("  Long words starting with 'a': " + filtered);  // => Long words starting with 'a': [apple, avocado]

        // Consumer chaining with andThen(): sequences side effects. Unlike Function,
        // Consumer returns void, so you can only chain (not compose) them.
        Consumer<String> print = s -> System.out.print("    > " + s);  // => (partial line)
        Consumer<String> println = print.andThen(s -> System.out.println(" [len=" + s.length() + "]"));  // => > chained consumer [len=16]
        println.accept("chained consumer");

        // Optional (Java 8+): a container that may or may not hold a value. Designed to
        // replace null returns from methods — NOT for field types or method parameters.
        // Unlike Kotlin's null safety (built into the type system with `?`) or Scala's
        // Option (a sealed trait with Some/None), Java's Optional is a library solution
        // that cannot prevent null at the language level.
        Optional<String> maybeName = Optional.of("Alice");
        Optional<String> empty = Optional.empty();
        System.out.println("  Optional present: " + maybeName.map(String::toUpperCase).orElse("N/A"));  // => Optional present: ALICE
        System.out.println("  Optional empty: " + empty.map(String::toUpperCase).orElse("N/A"));  // => Optional empty: N/A

        // Optional chaining: filter() + map() + orElseThrow() composes a pipeline that
        // short-circuits to empty at any step. This is monadic composition — Optional
        // is essentially a monad with map (functor) and flatMap (bind).
        var length = maybeName
                .filter(n -> n.startsWith("A"))
                .map(String::length)
                .orElseThrow(() -> new NoSuchElementException("no match"));
        System.out.println("  Optional chain: length = " + length);  // => Optional chain: length = 5
        System.out.println();
    }

    // ── 7. Error handling ─────────────────────────────────────────────
    static void errorHandling() {
        System.out.println("=== 7. ERROR HANDLING ===");  // => === 7. ERROR HANDLING ===

        // Try-with-resources (Java 7+): resources are closed in reverse declaration
        // order (B closes before A). If both the try-body and close() throw, the close()
        // exception becomes a "suppressed" exception attached to the primary one —
        // accessible via getSuppressed(). This prevents exception swallowing.
        try (var r1 = new ManagedResource("A");
             var r2 = new ManagedResource("B")) {
            r1.use();
            r2.use();
        }

        // Custom checked exceptions: Java's unique feature among JVM languages. The
        // compiler enforces that checked exceptions are either caught or declared in the
        // method signature with `throws`. This provides documentation but adds verbosity —
        // which is why Kotlin and Scala dropped checked exceptions entirely.
        try {
            double balance = 50.0;
            double withdrawal = 75.0;
            if (withdrawal > balance) {
                throw new InsufficientFundsException(withdrawal - balance);
            }
        } catch (InsufficientFundsException e) {
            System.out.println("  Caught: " + e.getMessage());  // => Caught: Insufficient funds: short by $25.00
            System.out.println("  Deficit: $" + e.getDeficit());  // => Deficit: $25.0
        }

        // Multi-catch (Java 7+): catches multiple unrelated exception types in one block.
        // The caught variable `e` is effectively final and its type is the common supertype.
        // Use this when the handling logic is identical — otherwise use separate catch blocks.
        try {
            var list = List.of("10", "abc", "20");
            int value = Integer.parseInt(list.get(1));
        } catch (NumberFormatException | IndexOutOfBoundsException e) {
            System.out.println("  Multi-catch: " + e.getClass().getSimpleName() + ": " + e.getMessage());  // => Multi-catch: NumberFormatException: For input string: "abc"
        }

        // Suppressed exceptions: when multiple things fail (e.g., both the main operation
        // and cleanup), Java attaches secondary failures via addSuppressed() rather than
        // losing them. Try-with-resources does this automatically for close() failures.
        try {
            throw new RuntimeException("primary");
        } catch (RuntimeException e) {
            var suppressed = new IOException("cleanup failed");
            e.addSuppressed(suppressed);
            System.out.println("  Suppressed: " + e.getSuppressed()[0].getMessage());  // => Suppressed: cleanup failed
        }
        System.out.println();
    }

    // ── 8. Concurrency ────────────────────────────────────────────────
    static void concurrency() throws Exception {
        System.out.println("=== 8. CONCURRENCY ===");  // => === 8. CONCURRENCY ===

        // Virtual threads (Project Loom, JEP 444, Java 21): lightweight threads managed
        // by the JVM, not the OS. Unlike platform threads (which map 1:1 to OS threads
        // and cost ~1MB stack each), virtual threads are cheap enough to create millions of.
        // They're mounted/unmounted onto carrier (platform) threads by the JVM scheduler.
        // Use for I/O-bound tasks; for CPU-bound work, platform threads are still better.
        // Compare with Kotlin coroutines (compile-time CPS transform) and Scala's Cats
        // Effect / ZIO fibers (library-level green threads).
        System.out.println("  -- Virtual Threads --");  // => -- Virtual Threads --
        var results = Collections.synchronizedList(new ArrayList<String>());
        var threads = new ArrayList<Thread>();
        for (int i = 0; i < 5; i++) {
            final int id = i;
            // Thread.ofVirtual(): factory API for virtual threads. The .name() and .start()
            // builder pattern replaces the old `new Thread(runnable)` constructor.
            var vt = Thread.ofVirtual().name("vt-" + id).start(() -> {
                results.add("Virtual thread " + id + " [" + Thread.currentThread().getName() + "]");
            });
            threads.add(vt);
        }
        for (var t : threads) t.join();
        results.forEach(r -> System.out.println("    " + r));  // => (varies — thread execution order is non-deterministic)

        // CompletableFuture (Java 8+): composable async computation. supplyAsync() runs
        // on the common ForkJoinPool by default. thenApply() chains transformations
        // (like map on a Future), thenCombine() merges two independent futures. This is
        // Java's answer to Scala's Future.map/flatMap composition.
        System.out.println("  -- CompletableFuture --");  // => -- CompletableFuture --
        var future = CompletableFuture.supplyAsync(() -> "Hello")
                .thenApply(s -> s + ", Future")
                .thenApply(String::toUpperCase)
                .thenCombine(
                        CompletableFuture.supplyAsync(() -> "!"),
                        (a, b) -> a + b
                );
        System.out.println("    Result: " + future.get());  // => Result: HELLO, FUTURE!

        // CompletableFuture.allOf(): waits for ALL futures to complete. Returns
        // CompletableFuture<Void> — you must extract individual results separately.
        // Compare with Scala's Future.sequence (List[Future] => Future[List]).
        var f1 = CompletableFuture.supplyAsync(() -> 10);
        var f2 = CompletableFuture.supplyAsync(() -> 20);
        var f3 = CompletableFuture.supplyAsync(() -> 30);
        var allDone = CompletableFuture.allOf(f1, f2, f3);
        allDone.get();
        System.out.println("    All futures: " + f1.get() + ", " + f2.get() + ", " + f3.get());  // => All futures: 10, 20, 30

        // exceptionally(): recovers from failures in the async pipeline. The exception
        // is wrapped in CompletionException, so getCause() gives the original. This is
        // analogous to Scala's Future.recover { case ex => fallback }.
        var failing = CompletableFuture.supplyAsync(() -> {
            if (true) throw new RuntimeException("oops");
            return "ok";
        }).exceptionally(ex -> "recovered from: " + ex.getCause().getMessage());
        System.out.println("    Recovered: " + failing.get());  // => Recovered: recovered from: oops

        // ReentrantLock (java.util.concurrent.locks): more flexible than synchronized —
        // supports tryLock(), timed waits, interruptible locking, and fairness policies.
        // Always use lock/try/finally to guarantee unlock. In production, prefer
        // higher-level abstractions (concurrent collections, CompletableFuture) over raw locks.
        System.out.println("  -- Locks --");  // => -- Locks --
        var counter = new int[]{0};
        var lock = new ReentrantLock();

        var latchThreads = new ArrayList<Thread>();
        for (int i = 0; i < 100; i++) {
            latchThreads.add(Thread.ofVirtual().start(() -> {
                lock.lock();
                try {
                    counter[0]++;
                } finally {
                    lock.unlock();
                }
            }));
        }
        for (var t : latchThreads) t.join();
        System.out.println("    ReentrantLock counter: " + counter[0]);  // => ReentrantLock counter: 100

        // synchronized: Java's built-in monitor lock. Every object has an intrinsic lock.
        // Simpler than ReentrantLock but less flexible (no tryLock, no fairness control).
        // Note: virtual threads can pin their carrier thread when holding a synchronized
        // lock (JEP 491 in Java 24 fixes this) — prefer ReentrantLock with virtual threads.
        var syncCounter = new int[]{0};
        var syncThreads = new ArrayList<Thread>();
        var monitor = new Object();
        for (int i = 0; i < 100; i++) {
            syncThreads.add(Thread.ofVirtual().start(() -> {
                synchronized (monitor) {
                    syncCounter[0]++;
                }
            }));
        }
        for (var t : syncThreads) t.join();
        System.out.println("    Synchronized counter: " + syncCounter[0]);  // => Synchronized counter: 100
        System.out.println();
    }

    // ── 9. File I/O ──────────────────────────────────────────────────
    static void fileIO() throws Exception {
        System.out.println("=== 9. FILE I/O ===");  // => === 9. FILE I/O ===

        // Path API (java.nio.file, Java 7+): replaced java.io.File with an immutable,
        // filesystem-agnostic path representation. Path.of() creates paths; resolve()
        // appends child segments. NIO.2 paths are interoperable with the old File API
        // via Path.toFile() and File.toPath().
        var tmpDir = Path.of(System.getProperty("java.io.tmpdir"));
        var filePath = tmpDir.resolve("java_fundamentals_demo.txt");
        System.out.println("  Temp dir: " + tmpDir);  // => (varies)

        // Files.write(): convenience method that opens, writes, and closes in one call.
        // Defaults to UTF-8 and overwrites. For append mode, pass StandardOpenOption.APPEND.
        var lines = List.of("Line 1: Hello from Java", "Line 2: File I/O demo", "Line 3: Path API");
        Files.write(filePath, lines);
        System.out.println("  Wrote " + lines.size() + " lines to " + filePath.getFileName());  // => Wrote 3 lines to java_fundamentals_demo.txt

        // Files.readAllLines(): reads entire file into memory as List<String>.
        // Fine for small files; for large files use Files.lines() (lazy stream) instead.
        var readBack = Files.readAllLines(filePath);
        System.out.println("  Read back: " + readBack);  // => Read back: [Line 1: Hello from Java, Line 2: File I/O demo, Line 3: Path API]

        // Files.readString() (Java 11+): reads entire file as a single String.
        // Uses UTF-8 by default. Simpler than the old BufferedReader boilerplate.
        var content = Files.readString(filePath);
        System.out.println("  File size: " + content.length() + " chars");  // => (varies)

        // BufferedReader with try-with-resources: the reader is automatically closed
        // when the block exits, even on exception. This is idiomatic Java I/O — always
        // wrap I/O resources in try-with-resources to prevent resource leaks.
        try (var reader = Files.newBufferedReader(filePath)) {
            var firstLine = reader.readLine();
            System.out.println("  BufferedReader first line: " + firstLine);  // => BufferedReader first line: Line 1: Hello from Java
        }

        // Files.lines(): returns a lazy Stream<String> — reads lines on demand, not all
        // at once. The stream MUST be closed (hence try-with-resources) because it holds
        // an open file handle. This is the preferred approach for processing large files.
        try (var lineStream = Files.lines(filePath)) {
            var upper = lineStream
                    .map(String::toUpperCase)
                    .toList();
            System.out.println("  Streamed uppercase: " + upper);  // => Streamed uppercase: [LINE 1: HELLO FROM JAVA, LINE 2: FILE I/O DEMO, LINE 3: PATH API]
        }

        // Files utility methods: exists(), size(), isDirectory(), getLastModifiedTime()
        // provide metadata without opening the file.
        System.out.println("  Exists: " + Files.exists(filePath));  // => Exists: true
        System.out.println("  Size: " + Files.size(filePath) + " bytes");  // => (varies)

        // deleteIfExists(): returns false instead of throwing if the file doesn't exist.
        // Prefer over delete() to avoid NoSuchFileException in cleanup code.
        Files.deleteIfExists(filePath);
        System.out.println("  Cleaned up temp file");  // => Cleaned up temp file
        System.out.println();

        System.out.println("=== DONE ===");  // => === DONE ===
    }
}
