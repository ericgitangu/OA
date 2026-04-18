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

    // ── Records (immutable data carriers) ──────────────────────────────
    record Point(double x, double y) {
        // compact canonical constructor for validation
        Point {
            if (Double.isNaN(x) || Double.isNaN(y))
                throw new IllegalArgumentException("coordinates must not be NaN");
        }

        double distanceTo(Point other) {
            return Math.sqrt(Math.pow(x - other.x, 2) + Math.pow(y - other.y, 2));
        }
    }

    record Pair<A, B>(A first, B second) {}

    // ── Sealed classes (restricted inheritance) ────────────────────────
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

    // ── OOP: interfaces, abstract classes, generics ───────────────────
    interface Describable {
        String describe();

        default String tag() { return "[" + describe() + "]"; }
    }

    abstract static class Animal implements Describable {
        final String name;
        Animal(String name) { this.name = name; }
        abstract String sound();

        @Override
        public String describe() { return name + " says " + sound(); }
    }

    static class Dog extends Animal {
        Dog(String name) { super(name); }
        @Override String sound() { return "woof"; }
    }

    static class Cat extends Animal {
        Cat(String name) { super(name); }
        @Override String sound() { return "meow"; }
    }

    // ── Generics: bounded types and wildcards ─────────────────────────
    static <T extends Comparable<T>> T max(T a, T b) {
        return a.compareTo(b) >= 0 ? a : b;
    }

    static double sumOfNumbers(List<? extends Number> nums) {
        return nums.stream().mapToDouble(Number::doubleValue).sum();
    }

    static void addIntegers(List<? super Integer> list) {
        list.add(42);
        list.add(99);
    }

    // ── Custom exception ──────────────────────────────────────────────
    static class InsufficientFundsException extends Exception {
        private final double deficit;

        InsufficientFundsException(double deficit) {
            super("Insufficient funds: short by $%.2f".formatted(deficit));
            this.deficit = deficit;
        }

        double getDeficit() { return deficit; }
    }

    // ── AutoCloseable resource for try-with-resources ─────────────────
    static class ManagedResource implements AutoCloseable {
        private final String id;
        private boolean open = true;

        ManagedResource(String id) {
            this.id = id;
            System.out.println("    Resource [" + id + "] opened");
        }

        void use() {
            if (!open) throw new IllegalStateException("resource closed");
            System.out.println("    Resource [" + id + "] in use");
        }

        @Override
        public void close() {
            open = false;
            System.out.println("    Resource [" + id + "] closed");
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
        System.out.println("=== 1. BASICS ===");

        // var — local variable type inference (Java 10+)
        var greeting = "Hello, Java 21!";
        var count = 42;
        var pi = 3.14159;
        System.out.println("  var greeting: " + greeting);
        System.out.println("  var count: " + count + ", pi: " + pi);

        // Text blocks (Java 15+)
        var json = """
                {
                    "name": "Alice",
                    "age": 30,
                    "languages": ["Java", "Kotlin", "Scala"]
                }
                """;
        System.out.println("  Text block:\n" + json);

        // Enhanced switch expressions (Java 14+)
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
        System.out.println("  Day " + dayNum + " = " + dayName);

        // Records
        var p1 = new Point(3.0, 4.0);
        var p2 = new Point(0.0, 0.0);
        System.out.println("  Point: " + p1 + ", distance to origin: " + p1.distanceTo(p2));

        // Sealed classes
        Shape shape = new Circle(5);
        System.out.println("  Circle area: " + shape.area());
        System.out.println();
    }

    // ── 2. Collections ────────────────────────────────────────────────
    static void collections() {
        System.out.println("=== 2. COLLECTIONS ===");

        // Immutable factory methods (Java 9+)
        var names = List.of("Alice", "Bob", "Charlie", "Diana");
        var scores = Map.of("Alice", 95, "Bob", 87, "Charlie", 92);
        var uniqueTags = Set.of("java", "jvm", "oop");
        System.out.println("  List: " + names);
        System.out.println("  Map: " + scores);
        System.out.println("  Set: " + uniqueTags);

        // Mutable collections
        var mutableList = new ArrayList<>(names);
        mutableList.add("Eve");
        mutableList.sort(Comparator.reverseOrder());
        System.out.println("  Sorted desc: " + mutableList);

        // Map operations
        var wordCounts = new HashMap<String, Integer>();
        for (var word : "the cat sat on the mat".split(" ")) {
            wordCounts.merge(word, 1, Integer::sum);
        }
        System.out.println("  Word counts: " + wordCounts);

        // Queue / Deque
        var queue = new ArrayDeque<String>();
        queue.offer("first");
        queue.offer("second");
        queue.offer("third");
        System.out.println("  Queue poll: " + queue.poll() + ", remaining: " + queue);

        // LinkedHashMap for insertion order
        var ordered = new LinkedHashMap<String, Integer>();
        ordered.put("z", 1);
        ordered.put("a", 2);
        ordered.put("m", 3);
        System.out.println("  Insertion-ordered map: " + ordered);
        System.out.println();
    }

    // ── 3. Stream API ─────────────────────────────────────────────────
    static void streams() {
        System.out.println("=== 3. STREAM API ===");

        var numbers = List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

        // map + filter
        var evenSquares = numbers.stream()
                .filter(n -> n % 2 == 0)
                .map(n -> n * n)
                .toList();
        System.out.println("  Even squares: " + evenSquares);

        // reduce
        var sum = numbers.stream().reduce(0, Integer::sum);
        System.out.println("  Sum: " + sum);

        // collect with groupingBy
        var words = List.of("apple", "banana", "avocado", "blueberry", "cherry", "apricot");
        var byFirstLetter = words.stream()
                .collect(Collectors.groupingBy(w -> w.charAt(0)));
        System.out.println("  Grouped by first letter: " + byFirstLetter);

        // collect with joining
        var csv = words.stream().collect(Collectors.joining(", "));
        System.out.println("  Joined: " + csv);

        // flatMap
        var nested = List.of(List.of(1, 2), List.of(3, 4), List.of(5));
        var flat = nested.stream().flatMap(Collection::stream).toList();
        System.out.println("  Flattened: " + flat);

        // partitioning
        var partitioned = numbers.stream()
                .collect(Collectors.partitioningBy(n -> n > 5));
        System.out.println("  Partitioned >5: " + partitioned);

        // statistics
        var stats = numbers.stream().mapToInt(Integer::intValue).summaryStatistics();
        System.out.println("  Stats: avg=" + stats.getAverage() + ", max=" + stats.getMax());
        System.out.println();
    }

    // ── 4. OOP ────────────────────────────────────────────────────────
    static void oop() {
        System.out.println("=== 4. OOP ===");

        Animal dog = new Dog("Rex");
        Animal cat = new Cat("Whiskers");
        System.out.println("  " + dog.describe());
        System.out.println("  " + cat.tag());

        // Generics
        System.out.println("  max(3, 7) = " + max(3, 7));
        System.out.println("  max(\"apple\", \"banana\") = " + max("apple", "banana"));

        // Bounded wildcards
        var ints = List.of(1, 2, 3);
        var doubles = List.of(1.5, 2.5, 3.5);
        System.out.println("  sumOfNumbers(ints) = " + sumOfNumbers(ints));
        System.out.println("  sumOfNumbers(doubles) = " + sumOfNumbers(doubles));

        // Lower-bounded wildcard
        List<Number> numList = new ArrayList<>();
        addIntegers(numList);
        System.out.println("  After addIntegers: " + numList);

        // Generic record
        var pair = new Pair<>("key", 42);
        System.out.println("  Pair: " + pair);
        System.out.println();
    }

    // ── 5. Pattern matching ───────────────────────────────────────────
    static void patternMatching() {
        System.out.println("=== 5. PATTERN MATCHING ===");

        // instanceof pattern (Java 16+)
        Object obj = "Hello, Pattern Matching!";
        if (obj instanceof String s && s.length() > 5) {
            System.out.println("  instanceof pattern: \"" + s.toUpperCase() + "\"");
        }

        // Switch pattern matching (Java 21)
        // List.of() does not allow null — use Arrays.asList() instead
        List<Object> items = java.util.Arrays.asList(42, "text", 3.14, new Point(1, 2), null);
        for (var item : items) {
            var description = switch (item) {
                case Integer i when i > 100 -> "large int: " + i;
                case Integer i              -> "int: " + i;
                case String s               -> "string of length " + s.length();
                case Double d               -> "double: " + d;
                case Point(var x, var y)    -> "point at (" + x + ", " + y + ")";
                case null                   -> "null value";
                default                     -> "other: " + item;
            };
            System.out.println("    " + description);
        }

        // Sealed class exhaustive switch
        Shape shape = new Triangle(10, 5);
        var desc = switch (shape) {
            case Circle c    -> "Circle r=" + c.radius();
            case Rectangle r -> "Rect " + r.width() + "x" + r.height();
            case Triangle t  -> "Triangle base=" + t.base() + " h=" + t.height();
        };
        System.out.println("  Sealed switch: " + desc + ", area=" + shape.area());
        System.out.println();
    }

    // ── 6. Functional programming ─────────────────────────────────────
    static void functional() {
        System.out.println("=== 6. FUNCTIONAL ===");

        // Lambdas
        Comparator<String> byLength = (a, b) -> Integer.compare(a.length(), b.length());
        var sorted = List.of("banana", "fig", "cherry", "apple");
        var result = sorted.stream().sorted(byLength).toList();
        System.out.println("  Sorted by length: " + result);

        // Method references
        var upper = List.of("hello", "world").stream()
                .map(String::toUpperCase)
                .toList();
        System.out.println("  Method ref: " + upper);

        // Function composition
        Function<Integer, Integer> doubleIt = x -> x * 2;
        Function<Integer, Integer> addTen = x -> x + 10;
        Function<Integer, Integer> doubleThenAdd = doubleIt.andThen(addTen);
        Function<Integer, Integer> addThenDouble = doubleIt.compose(addTen);
        System.out.println("  doubleThenAdd(5) = " + doubleThenAdd.apply(5));
        System.out.println("  addThenDouble(5) = " + addThenDouble.apply(5));

        // Predicate composition
        Predicate<String> isLong = s -> s.length() > 4;
        Predicate<String> startsWithA = s -> s.startsWith("a");
        var filtered = List.of("apple", "ant", "banana", "avocado").stream()
                .filter(isLong.and(startsWithA))
                .toList();
        System.out.println("  Long words starting with 'a': " + filtered);

        // Consumer chaining
        Consumer<String> print = s -> System.out.print("    > " + s);
        Consumer<String> println = print.andThen(s -> System.out.println(" [len=" + s.length() + "]"));
        println.accept("chained consumer");

        // Optional
        Optional<String> maybeName = Optional.of("Alice");
        Optional<String> empty = Optional.empty();
        System.out.println("  Optional present: " + maybeName.map(String::toUpperCase).orElse("N/A"));
        System.out.println("  Optional empty: " + empty.map(String::toUpperCase).orElse("N/A"));

        // Optional chaining
        var length = maybeName
                .filter(n -> n.startsWith("A"))
                .map(String::length)
                .orElseThrow(() -> new NoSuchElementException("no match"));
        System.out.println("  Optional chain: length = " + length);
        System.out.println();
    }

    // ── 7. Error handling ─────────────────────────────────────────────
    static void errorHandling() {
        System.out.println("=== 7. ERROR HANDLING ===");

        // try-with-resources (multiple resources)
        try (var r1 = new ManagedResource("A");
             var r2 = new ManagedResource("B")) {
            r1.use();
            r2.use();
        }

        // Custom exception
        try {
            double balance = 50.0;
            double withdrawal = 75.0;
            if (withdrawal > balance) {
                throw new InsufficientFundsException(withdrawal - balance);
            }
        } catch (InsufficientFundsException e) {
            System.out.println("  Caught: " + e.getMessage());
            System.out.println("  Deficit: $" + e.getDeficit());
        }

        // Multi-catch
        try {
            var list = List.of("10", "abc", "20");
            int value = Integer.parseInt(list.get(1));
        } catch (NumberFormatException | IndexOutOfBoundsException e) {
            System.out.println("  Multi-catch: " + e.getClass().getSimpleName() + ": " + e.getMessage());
        }

        // Suppressed exceptions example
        try {
            throw new RuntimeException("primary");
        } catch (RuntimeException e) {
            var suppressed = new IOException("cleanup failed");
            e.addSuppressed(suppressed);
            System.out.println("  Suppressed: " + e.getSuppressed()[0].getMessage());
        }
        System.out.println();
    }

    // ── 8. Concurrency ────────────────────────────────────────────────
    static void concurrency() throws Exception {
        System.out.println("=== 8. CONCURRENCY ===");

        // Virtual threads (Java 21 — Project Loom)
        System.out.println("  -- Virtual Threads --");
        var results = Collections.synchronizedList(new ArrayList<String>());
        var threads = new ArrayList<Thread>();
        for (int i = 0; i < 5; i++) {
            final int id = i;
            var vt = Thread.ofVirtual().name("vt-" + id).start(() -> {
                results.add("Virtual thread " + id + " [" + Thread.currentThread().getName() + "]");
            });
            threads.add(vt);
        }
        for (var t : threads) t.join();
        results.forEach(r -> System.out.println("    " + r));

        // CompletableFuture composition
        System.out.println("  -- CompletableFuture --");
        var future = CompletableFuture.supplyAsync(() -> "Hello")
                .thenApply(s -> s + ", Future")
                .thenApply(String::toUpperCase)
                .thenCombine(
                        CompletableFuture.supplyAsync(() -> "!"),
                        (a, b) -> a + b
                );
        System.out.println("    Result: " + future.get());

        // Multiple futures
        var f1 = CompletableFuture.supplyAsync(() -> 10);
        var f2 = CompletableFuture.supplyAsync(() -> 20);
        var f3 = CompletableFuture.supplyAsync(() -> 30);
        var allDone = CompletableFuture.allOf(f1, f2, f3);
        allDone.get();
        System.out.println("    All futures: " + f1.get() + ", " + f2.get() + ", " + f3.get());

        // Exception handling in futures
        var failing = CompletableFuture.supplyAsync(() -> {
            if (true) throw new RuntimeException("oops");
            return "ok";
        }).exceptionally(ex -> "recovered from: " + ex.getCause().getMessage());
        System.out.println("    Recovered: " + failing.get());

        // synchronized and ReentrantLock
        System.out.println("  -- Locks --");
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
        System.out.println("    ReentrantLock counter: " + counter[0]);

        // Synchronized block
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
        System.out.println("    Synchronized counter: " + syncCounter[0]);
        System.out.println();
    }

    // ── 9. File I/O ──────────────────────────────────────────────────
    static void fileIO() throws Exception {
        System.out.println("=== 9. FILE I/O ===");

        // Path API
        var tmpDir = Path.of(System.getProperty("java.io.tmpdir"));
        var filePath = tmpDir.resolve("java_fundamentals_demo.txt");
        System.out.println("  Temp dir: " + tmpDir);

        // Write file
        var lines = List.of("Line 1: Hello from Java", "Line 2: File I/O demo", "Line 3: Path API");
        Files.write(filePath, lines);
        System.out.println("  Wrote " + lines.size() + " lines to " + filePath.getFileName());

        // Read all lines
        var readBack = Files.readAllLines(filePath);
        System.out.println("  Read back: " + readBack);

        // Read as string
        var content = Files.readString(filePath);
        System.out.println("  File size: " + content.length() + " chars");

        // BufferedReader with try-with-resources
        try (var reader = Files.newBufferedReader(filePath)) {
            var firstLine = reader.readLine();
            System.out.println("  BufferedReader first line: " + firstLine);
        }

        // Stream lines (lazy)
        try (var lineStream = Files.lines(filePath)) {
            var upper = lineStream
                    .map(String::toUpperCase)
                    .toList();
            System.out.println("  Streamed uppercase: " + upper);
        }

        // File metadata
        System.out.println("  Exists: " + Files.exists(filePath));
        System.out.println("  Size: " + Files.size(filePath) + " bytes");

        // Cleanup
        Files.deleteIfExists(filePath);
        System.out.println("  Cleaned up temp file");
        System.out.println();

        System.out.println("=== DONE ===");
    }
}
