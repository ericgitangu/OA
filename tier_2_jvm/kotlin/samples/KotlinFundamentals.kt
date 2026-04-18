/**
 * Kotlin Fundamentals — single runnable file.
 * Compile & run:  kotlinc KotlinFundamentals.kt -include-runtime -d kf.jar && java -jar kf.jar
 * Or:             kotlin KotlinFundamentals.kt  (with Kotlin scripting)
 */

// Sealed classes (Kotlin's ADTs): all subclasses must be defined in the same file
// (relaxed to same compilation unit in Kotlin 1.5+). Unlike Java's `sealed permits`,
// Kotlin infers the permitted subtypes automatically. The compiler can verify exhaustive
// `when` expressions — if you add a new subclass and miss a branch, it won't compile.
sealed class Shape {
    abstract fun area(): Double

    // Data classes inside sealed classes: `data` auto-generates equals(), hashCode(),
    // toString(), copy(), and componentN() destructuring functions. Equivalent to
    // Java's records but available since Kotlin 1.0, years before Java 16.
    data class Circle(val radius: Double) : Shape() {
        override fun area() = Math.PI * radius * radius
    }

    data class Rectangle(val width: Double, val height: Double) : Shape() {
        override fun area() = width * height
    }

    data class Triangle(val base: Double, val height: Double) : Shape() {
        override fun area() = 0.5 * base * height
    }
}

// Enum classes: each enum constant is a singleton instance of the enum class.
// Unlike Java enums, Kotlin enums can have properties declared in the primary
// constructor and use `when` for exhaustive matching (no default needed).
enum class Direction(val dx: Int, val dy: Int) {
    NORTH(0, 1), SOUTH(0, -1), EAST(1, 0), WEST(-1, 0);

    // `when` as an expression must be exhaustive here — the compiler knows all
    // enum values and will error if one is missing.
    fun opposite(): Direction = when (this) {
        NORTH -> SOUTH; SOUTH -> NORTH
        EAST -> WEST; WEST -> EAST
    }
}

// Object declaration: Kotlin's built-in singleton pattern. Unlike Java's manual
// singleton (private constructor + static instance), `object` is thread-safe by
// default — initialized lazily on first access using the JVM's class loading guarantees.
// Compiles to a Java class with a static INSTANCE field.
object Registry {
    private val items = mutableMapOf<String, Any>()
    fun register(key: String, value: Any) { items[key] = value }
    fun lookup(key: String): Any? = items[key]
    override fun toString() = "Registry($items)"
}

// Companion objects: Kotlin's replacement for Java's static members. Since Kotlin has
// no `static` keyword, companion objects hold factory methods, constants, and shared
// behavior. Accessed via `Color.RED` (not `Color.Companion.RED`). Annotate members
// with @JvmStatic for Java interop that looks like true static methods.
data class Color(val r: Int, val g: Int, val b: Int) {
    companion object {
        val RED = Color(255, 0, 0)
        val GREEN = Color(0, 255, 0)
        val BLUE = Color(0, 0, 255)
        fun fromHex(hex: String): Color {
            // Bitwise operations use named functions (shr, and) instead of Java's operators
            // (>>, &) — Kotlin chose readability over familiarity with C-style bit ops.
            val v = hex.removePrefix("#").toLong(16).toInt()
            return Color((v shr 16) and 0xFF, (v shr 8) and 0xFF, v and 0xFF)
        }
    }
}

// Interfaces in Kotlin can have default method implementations (like Java 8+) AND
// property declarations (unlike Java). However, interface properties have no backing
// field — they must be abstract or provide a custom getter. Use interfaces for
// stateless contracts; use abstract classes when you need constructor parameters or state.
interface Describable {
    fun describe(): String
    // Default implementation: implementors inherit this unless they override it.
    // Under the hood, Kotlin compiles this to a DefaultImpls inner class for Java compat.
    fun tag(): String = "[${describe()}]"
}

class NamedItem(val name: String, val value: Int) : Describable {
    override fun describe() = "$name=$value"
}

// Extension functions: add new methods to existing classes without inheritance or
// decoration. Resolved statically at compile time (not virtual dispatch) — they're
// syntactic sugar for a static method with the receiver as the first parameter.
// This means extensions on a supertype won't be overridden by the actual runtime type.
fun String.wordCount(): Int = this.trim().split(Regex("\\s+")).size

// Generic extension function: `T?` return type explicitly encodes the possibility of
// absence, unlike Java where you'd return null without type-level indication.
fun <T> List<T>.secondOrNull(): T? = if (size >= 2) this[1] else null

fun Int.isEven(): Boolean = this % 2 == 0

// Higher-order functions: functions that take other functions as parameters.
// The type `(T) -> R` is Kotlin's function type — it compiles to FunctionN interfaces
// on the JVM (e.g., Function1<T, R>). Unlike Java's functional interfaces, Kotlin
// function types are first-class and don't require SAM conversion.
fun <T, R> List<T>.mapAndFilter(transform: (T) -> R, predicate: (R) -> Boolean): List<R> =
    this.map(transform).filter(predicate)

// Inline functions: the compiler copies the function body AND the lambda body into
// the call site, eliminating the overhead of creating a Function object on the heap.
// Critical for performance-sensitive higher-order functions. Without `inline`, each
// lambda creates an anonymous class instance (or uses invokedynamic on newer JVMs).
// Use `inline` when: (1) the function takes lambdas, (2) it's called frequently,
// (3) the lambda body is small. Avoid for large function bodies (code size bloat).
inline fun <T> measureTime(label: String, block: () -> T): T {
    val start = System.nanoTime()
    val result = block()
    val elapsed = (System.nanoTime() - start) / 1_000_000.0
    println("    $label took %.2f ms".format(elapsed))  // => (varies)
    return result
}

// Lambda with receiver (`HtmlBuilder.() -> Unit`): inside this lambda, `this` refers
// to an HtmlBuilder instance. This is the foundation of Kotlin's type-safe DSL builders.
// Java has no equivalent — the closest is a builder pattern with method chaining.
// Scala achieves similar DSLs with implicit parameters and by-name parameters.
class HtmlBuilder {
    private val elements = mutableListOf<String>()
    fun h1(text: String) { elements += "<h1>$text</h1>" }
    fun p(text: String) { elements += "<p>$text</p>" }
    // Nested receiver: UlBuilder.() -> Unit means `this` inside the lambda is a UlBuilder.
    // This creates a scoped DSL where only UlBuilder methods are available.
    fun ul(block: UlBuilder.() -> Unit) {
        val ul = UlBuilder()
        ul.block()
        elements += "<ul>${ul.build()}</ul>"
    }
    fun build(): String = elements.joinToString("\n")
}

class UlBuilder {
    private val items = mutableListOf<String>()
    fun li(text: String) { items += "  <li>$text</li>" }
    fun build(): String = items.joinToString("\n")
}

fun html(block: HtmlBuilder.() -> Unit): String {
    val builder = HtmlBuilder()
    builder.block()
    return builder.build()
}

// Property delegation: Kotlin's `by` keyword delegates getter/setter to another object.
// The delegate must implement operator functions getValue() and setValue() matching
// the KProperty protocol. This is Kotlin's unique approach — neither Java nor Scala
// have built-in property delegation (Scala uses implicits for similar patterns).
class ObservableProperty<T>(private var value: T, private val onChange: (T, T) -> Unit) {
    // The `operator` keyword enables using this class with `by` syntax.
    // `thisRef` is the object containing the delegated property, `property` has metadata.
    operator fun getValue(thisRef: Any?, property: kotlin.reflect.KProperty<*>): T = value
    operator fun setValue(thisRef: Any?, property: kotlin.reflect.KProperty<*>, newValue: T) {
        val old = value
        value = newValue
        onChange(old, newValue)
    }
}

class UserProfile {
    // `by lazy`: built-in delegate that initializes the value on first access and caches it.
    // Thread-safe by default (uses LazyThreadSafetyMode.SYNCHRONIZED). Use
    // LazyThreadSafetyMode.NONE if you guarantee single-threaded access for ~10% better perf.
    val createdAt: Long by lazy {
        println("    (lazy init: computing createdAt)")  // => (lazy init: computing createdAt)
        System.currentTimeMillis()
    }

    // Custom observable delegate: fires the onChange callback on every write.
    // Kotlin's stdlib also provides Delegates.observable() and Delegates.vetoable()
    // for common patterns without writing your own delegate class.
    var displayName: String by ObservableProperty("Anonymous") { old, new ->
        println("    (observed: displayName changed '$old' -> '$new')")  // => (varies)
    }
}

// ═════════════════════════════════════════════════════════════════════
// MAIN
// ═════════════════════════════════════════════════════════════════════
fun main() {
    basics()
    collections()
    sequences()
    classesAndObjects()
    patternMatchingWithWhen()
    functional()
    scopeFunctions()
    delegation()
    dslBuilding()
    coroutinesConcepts()
}

// ── 1. Basics ────────────────────────────────────────────────────────
fun basics() {
    println("=== 1. BASICS ===")  // => === 1. BASICS ===

    // `val` (immutable reference) vs `var` (mutable reference): Kotlin makes immutability
    // the natural choice by requiring `var` explicitly. `val` is like Java's `final` but
    // applied by default idiomatically. Note: `val` means the REFERENCE is immutable,
    // not the object — a `val list = mutableListOf(...)` can still be modified.
    val name = "Kotlin"
    var counter = 0
    counter += 1
    println("  val name=$name, var counter=$counter")  // => val name=Kotlin, var counter=1

    // String templates: `$variable` for simple references, `${expression}` for complex
    // expressions. Compiled to StringBuilder.append() calls — no performance penalty
    // vs manual concatenation. Java requires explicit concatenation or String.format().
    val x = 42
    println("  x=$x, x*2=${x * 2}, name has ${name.length} chars")  // => x=42, x*2=84, name has 6 chars

    // Raw strings (triple-quoted): preserve all whitespace and special characters literally.
    // trimMargin() strips leading whitespace up to the margin character (default: `|`).
    // Compare with Java's text blocks (which auto-strip common indentation) and Scala's
    // stripMargin (same concept, same `|` convention).
    val text = """
        |Line 1: trimMargin strips leading whitespace
        |Line 2: using pipe as margin prefix
        |Line 3: raw string literal
    """.trimMargin()
    println("  Multiline:\n$text")  // => Multiline: (followed by 3 trimmed lines)

    // Null safety: Kotlin's type system distinguishes nullable (`String?`) from non-null
    // (`String`) at compile time. This is Kotlin's flagship feature over Java — it
    // eliminates NullPointerException at the type level. The JVM bytecode still uses
    // null references, but the compiler inserts null checks and prevents unsafe access.
    val nullable: String? = "hello"
    val alsoNull: String? = null

    // Safe call operator `?.`: returns null if the receiver is null, otherwise calls the
    // method. Chains gracefully: `a?.b?.c?.d` short-circuits at the first null.
    println("  nullable?.length = ${nullable?.length}")  // => nullable?.length = 5
    println("  alsoNull?.length = ${alsoNull?.length}")  // => alsoNull?.length = null

    // Elvis operator `?:`: provides a default value when the left side is null.
    // Named after Elvis Presley's hairstyle (turn `?:` sideways). Equivalent to
    // Java's `Optional.orElse()` but works with any nullable type, not just Optional.
    val len = alsoNull?.length ?: -1
    println("  alsoNull?.length ?: -1 = $len")  // => alsoNull?.length ?: -1 = -1

    // `?.let {}`: executes the block only if the receiver is non-null. The non-null
    // value is available as `it` inside the lambda. This is idiomatic for null-guarded
    // transformations — cleaner than `if (x != null) { ... }`.
    nullable?.let { println("  nullable is not null: '$it'") }  // => nullable is not null: 'hello'
    alsoNull?.let { println("  THIS SHOULD NOT PRINT") }  // (not printed — alsoNull is null)

    // Not-null assertion `!!`: converts nullable to non-null, throwing KotlinNullPointerException
    // if null. Use sparingly — it defeats the purpose of null safety. Legitimate uses:
    // bridging with Java APIs or after a null check the compiler can't track.
    val definitelyNotNull: String = nullable!!
    println("  !! assertion: $definitelyNotNull")  // => !! assertion: hello

    // Smart casts: after an `is` check, the compiler automatically casts the variable
    // to the checked type within the scope where the check holds. No explicit cast needed.
    // This is possible because Kotlin tracks control flow — Java requires explicit casting
    // even after instanceof (until Java 16's pattern matching for instanceof).
    val obj: Any = "I'm a String"
    if (obj is String) {
        println("  Smart cast: length=${obj.length}")  // obj is auto-cast to String  // => Smart cast: length=12
    }

    println()
}

// ── 2. Collections ───────────────────────────────────────────────────
fun collections() {
    println("=== 2. COLLECTIONS ===")  // => === 2. COLLECTIONS ===

    // Kotlin collections default to read-only interfaces (List, Map, Set) that expose
    // no mutation methods. This is a wrapper-level distinction — the underlying JVM
    // collection may still be mutable. Use mutableListOf() when mutation is needed.
    // This design choice makes Kotlin safer than Java (mutable by default) while
    // still interoperable with Java collections at the bytecode level.
    val names = listOf("Alice", "Bob", "Charlie", "Diana")
    val scores = mapOf("Alice" to 95, "Bob" to 87, "Charlie" to 92)
    val tags = setOf("kotlin", "jvm", "oop")
    println("  List: $names")  // => List: [Alice, Bob, Charlie, Diana]
    println("  Map: $scores")  // => Map: {Alice=95, Bob=87, Charlie=92}
    println("  Set: $tags")  // => Set: [kotlin, jvm, oop]

    // Mutable collections: explicitly requested. The `+=` operator on mutable collections
    // calls add() — this is operator overloading via the `plusAssign` convention.
    val mutableNames = mutableListOf("Eve", "Frank")
    mutableNames += "Grace"
    mutableNames.removeAt(0)
    println("  Mutable list: $mutableNames")  // => Mutable list: [Frank, Grace]

    // Kotlin's collection operations are eager by default (unlike Java Streams which are
    // lazy). Each filter/map creates an intermediate list. For large collections, use
    // .asSequence() to get lazy evaluation (see Sequences section below).
    val numbers = listOf(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

    // `it`: implicit name for a single-parameter lambda. Equivalent to Scala's `_`
    // placeholder but more readable in complex expressions.
    val evenSquares = numbers.filter { it.isEven() }.map { it * it }
    println("  Even squares: $evenSquares")  // => Even squares: [4, 16, 36, 64, 100]

    // reduce(): folds without an initial value — uses the first element as the
    // accumulator. Throws on empty collections. Use fold() with an initial value
    // for safety, or reduceOrNull() for nullable result on empty input.
    val sum = numbers.reduce { acc, n -> acc + n }
    println("  Reduce sum: $sum")  // => Reduce sum: 55

    val grouped = names.groupBy { it.first() }
    println("  Grouped by first char: $grouped")  // => Grouped by first char: {A=[Alice], B=[Bob], C=[Charlie], D=[Diana]}

    // flatMap: maps each element to a collection and flattens the result.
    // `{ it }` is short for `{ list -> list }` — uses the identity transform.
    val flat = listOf(listOf(1, 2), listOf(3, 4), listOf(5)).flatMap { it }
    println("  FlatMap: $flat")  // => FlatMap: [1, 2, 3, 4, 5]

    // associateWith: creates a Map from keys to computed values. Compare with
    // associateBy (which computes keys from values). Both are Kotlin-specific
    // convenience functions not found in Java's Stream API or Scala's collections.
    val nameLengths = names.associateWith { it.length }
    println("  AssociateWith: $nameLengths")  // => AssociateWith: {Alice=5, Bob=3, Charlie=7, Diana=5}

    // Destructuring declarations: `val (a, b) = pair` calls component1() and component2().
    // partition() returns a Pair<List, List> which supports destructuring. Data classes
    // and Pairs auto-generate componentN() functions; regular classes need `operator fun`.
    val (evens, odds) = numbers.partition { it.isEven() }
    println("  Partition evens=$evens, odds=$odds")  // => Partition evens=[2, 4, 6, 8, 10], odds=[1, 3, 5, 7, 9]

    // zip: combines two lists element-wise into a list of Pairs. Stops at the shorter
    // list's length. unzip: reverses the operation, splitting Pairs back into two lists.
    val keys = listOf("a", "b", "c")
    val values = listOf(1, 2, 3)
    val zipped = keys.zip(values)
    println("  Zip: $zipped")  // => Zip: [(a, 1), (b, 2), (c, 3)]
    val (unzippedKeys, unzippedVals) = zipped.unzip()
    println("  Unzip: keys=$unzippedKeys, vals=$unzippedVals")  // => Unzip: keys=[a, b, c], vals=[1, 2, 3]

    println()
}

// ── 3. Sequences (lazy evaluation) ───────────────────────────────────
fun sequences() {
    println("=== 3. SEQUENCES ===")  // => === 3. SEQUENCES ===

    // Sequences: Kotlin's lazy collection pipeline, analogous to Java's Streams and
    // Scala's LazyLists/Views. Operations are applied element-by-element (vertical
    // processing) rather than creating intermediate collections (horizontal processing).
    // Critical for large datasets or infinite sequences. Unlike Java Streams, Kotlin
    // Sequences are reusable (not one-shot) and don't support parallelism directly.
    val result = (1..1_000_000).asSequence()
        .filter { it % 3 == 0 }
        .map { it * it }
        .take(5)
        .toList()
    println("  First 5 squares of multiples of 3: $result")  // => First 5 squares of multiples of 3: [9, 36, 81, 144, 225]

    // generateSequence: creates a potentially infinite sequence from a seed value
    // and a successor function. The sequence terminates when the function returns null.
    val powers = generateSequence(1) { it * 2 }.take(10).toList()
    println("  Powers of 2: $powers")  // => Powers of 2: [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]

    // sequence { } builder: uses Kotlin's suspend mechanism (coroutine-based) to
    // generate values lazily with yield(). The builder suspends after each yield and
    // resumes when the next element is requested. This is syntactic sugar over a
    // coroutine state machine — no threads are involved.
    val fibs = sequence {
        var a = 0
        var b = 1
        while (true) {
            yield(a)
            val next = a + b
            a = b
            b = next
        }
    }
    println("  First 12 Fibonacci: ${fibs.take(12).toList()}")  // => First 12 Fibonacci: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

    println()
}

// ── 4. Classes & objects ─────────────────────────────────────────────
fun classesAndObjects() {
    println("=== 4. CLASSES & OBJECTS ===")  // => === 4. CLASSES & OBJECTS ===

    // Data class: Kotlin generates equals(), hashCode(), toString(), copy(), and
    // componentN() from ALL properties declared in the primary constructor.
    // Properties declared in the class body are NOT included in these generated methods.
    // copy() creates a shallow copy with optional parameter overrides — useful for
    // immutable update patterns (compare with Java's record wither pattern).
    data class User(val name: String, val age: Int)

    val user = User("Alice", 30)
    val updated = user.copy(age = 31)
    println("  Data class: $user")  // => Data class: User(name=Alice, age=30)
    println("  Copy with modification: $updated")  // => Copy with modification: User(name=Alice, age=31)
    println("  Destructuring: name=${user.name}, age=${user.age}")  // => Destructuring: name=Alice, age=30

    // Sealed class exhaustive `when`: the compiler verifies every subtype is handled.
    // No `else` branch needed because the compiler knows all subtypes. If you add a
    // new Shape subclass, all `when` expressions missing it will fail to compile.
    val shapes = listOf(Shape.Circle(5.0), Shape.Rectangle(3.0, 4.0), Shape.Triangle(6.0, 3.0))
    for (shape in shapes) {
        val desc = when (shape) {
            is Shape.Circle -> "Circle r=${shape.radius}"
            is Shape.Rectangle -> "Rect ${shape.width}x${shape.height}"
            is Shape.Triangle -> "Triangle b=${shape.base} h=${shape.height}"
        }
        println("  $desc -> area=${shape.area()}")  // => Circle r=5.0 -> area=78.5... | Rect 3.0x4.0 -> area=12.0 | Triangle b=6.0 h=3.0 -> area=9.0
    }

    val dir = Direction.NORTH
    println("  Direction: $dir, opposite=${dir.opposite()}, dx=${dir.dx} dy=${dir.dy}")  // => Direction: NORTH, opposite=SOUTH, dx=0 dy=1

    // Object singleton: Registry.INSTANCE on the JVM. Thread-safe initialization
    // is guaranteed by the JVM class loader.
    Registry.register("version", "1.0")
    Registry.register("lang", "Kotlin")
    println("  Singleton: $Registry")  // => Singleton: Registry({version=1.0, lang=Kotlin})

    // Companion object usage: looks like static access but is actually an object instance.
    // This means companion objects can implement interfaces and be passed around as values.
    println("  Companion: RED=${Color.RED}, fromHex=${Color.fromHex("#FF8800")}")  // => Companion: RED=Color(r=255, g=0, b=0), fromHex=Color(r=255, g=136, b=0)

    // Interface with default method: Kotlin compiles defaults differently than Java —
    // it generates a static DefaultImpls class to maintain backward compatibility
    // with Java 6/7 bytecode targets (though modern Kotlin targets Java 8+).
    val item = NamedItem("score", 100)
    println("  Interface: ${item.describe()}, tag=${item.tag()}")  // => Interface: score=100, tag=[score=100]

    println()
}

// ── 5. When expressions ──────────────────────────────────────────────
fun patternMatchingWithWhen() {
    println("=== 5. WHEN EXPRESSIONS ===")  // => === 5. WHEN EXPRESSIONS ===

    // `when` without a subject: acts as a cleaner if-else-if chain. Each branch
    // is a boolean condition. The first matching branch wins. When used as an
    // expression (assigned to a variable), the `else` branch is mandatory.
    val x = 15
    val label = when {
        x < 0 -> "negative"
        x == 0 -> "zero"
        x in 1..10 -> "small"
        x in 11..100 -> "medium"
        else -> "large"
    }
    println("  $x is $label")  // => 15 is medium

    // `when` with a subject: the subject is matched against each branch using `is`
    // (type check), `in` (range/collection containment), or equality. Smart casts
    // apply within each branch — after `is String`, you can call String methods directly.
    // Note: `List<*>` uses star projection because of JVM type erasure — at runtime,
    // the JVM cannot distinguish List<Int> from List<String>.
    val obj: Any = listOf(1, 2, 3)
    val typeDesc = when (obj) {
        is Int -> "integer: $obj"
        is String -> "string of length ${obj.length}"
        is List<*> -> "list of size ${obj.size}"
        else -> "unknown"
    }
    println("  Type matching: $typeDesc")  // => Type matching: list of size 3

    // Multiple values in one branch: comma-separated alternatives are like Java's
    // case fallthrough but without the bug-prone fall-through semantics.
    val char = 'e'
    val kind = when (char) {
        'a', 'e', 'i', 'o', 'u' -> "vowel"
        in 'a'..'z' -> "consonant"
        in 'A'..'Z' -> "uppercase letter"
        else -> "other"
    }
    println("  '$char' is a $kind")  // => 'e' is a vowel

    println()
}

// ── 6. Functional ────────────────────────────────────────────────────
fun functional() {
    println("=== 6. FUNCTIONAL ===")  // => === 6. FUNCTIONAL ===

    // Lambda syntax: `{ params -> body }`. When a lambda has a single parameter,
    // you can omit it and use `it`. Kotlin lambdas are closures — they capture
    // variables from the enclosing scope by reference (including mutable vars).
    // Unlike Java lambdas (which require effectively-final captures), Kotlin wraps
    // captured mutable vars in IntRef/ObjectRef wrapper objects on the JVM.
    val double: (Int) -> Int = { it * 2 }
    val add: (Int, Int) -> Int = { a, b -> a + b }
    println("  double(5)=${double(5)}, add(3,4)=${add(3, 4)}")  // => double(5)=10, add(3,4)=7

    // Higher-order function usage: passing lambdas as arguments. The trailing lambda
    // syntax (last lambda outside parentheses) is a Kotlin convention that enables
    // DSL-like code. If the lambda is the ONLY argument, parentheses can be omitted entirely.
    val numbers = listOf(1, 2, 3, 4, 5)
    val result = numbers.mapAndFilter({ it * it }, { it > 10 })
    println("  mapAndFilter (square, >10): $result")  // => mapAndFilter (square, >10): [16, 25]

    // Extension functions called on instances: these look like member methods but
    // are statically dispatched. The extension is resolved based on the compile-time
    // type of the expression, NOT the runtime type.
    println("  \"hello world\".wordCount() = ${"hello world".wordCount()}")  // => "hello world".wordCount() = 2
    println("  listOf(1,2,3).secondOrNull() = ${listOf(1, 2, 3).secondOrNull()}")  // => listOf(1,2,3).secondOrNull() = 2

    // Method/function references use `::` — same syntax as Java. Can reference
    // class methods (String::lowercase), instance methods (obj::method), or
    // top-level functions (::topLevelFun). Bound references (obj::method) capture
    // the receiver; unbound references (String::lowercase) need it as a parameter.
    val words = listOf("Hello", "WORLD", "kotlin")
    val lower = words.map(String::lowercase)
    println("  Method ref lowercase: $lower")  // => Method ref lowercase: [hello, world, kotlin]

    // Inline function in action: the compiler will copy measureTime's body AND the
    // lambda body directly into this call site. No Function object is allocated.
    // Check the bytecode with `javap -c` to verify inlining occurred.
    val computed = measureTime("sum 1..1M") {
        (1..1_000_000).sum()
    }
    println("    result=$computed")  // => result=500000500000

    // Manual function composition: Kotlin's stdlib doesn't include compose/andThen
    // (unlike Java's Function.andThen() or Scala's Function.compose()). You can
    // write your own as a generic higher-order function. Arrow-kt library provides
    // this and much more for FP-heavy codebases.
    fun <A, B, C> compose(f: (B) -> C, g: (A) -> B): (A) -> C = { a -> f(g(a)) }
    val doubleAndToString = compose(Int::toString, double)
    println("  compose(toString, double)(21) = ${doubleAndToString(21)}")  // => compose(toString, double)(21) = 42

    println()
}

// ── 7. Scope functions ───────────────────────────────────────────────
fun scopeFunctions() {
    println("=== 7. SCOPE FUNCTIONS ===")  // => === 7. SCOPE FUNCTIONS ===

    // Kotlin's 5 scope functions (let, run, with, apply, also) differ by:
    // 1. How they reference the object: `this` (run, with, apply) vs `it` (let, also)
    // 2. What they return: the lambda result (let, run, with) vs the object itself (apply, also)
    // Choose based on: do you need the object as `this` or `it`? Do you need the result or the object?

    // let: transforms a value or scopes a nullable check. Returns the lambda result.
    // The object is available as `it`. Most common use: `nullable?.let { ... }` to
    // execute code only when non-null — Kotlin's alternative to Optional.map().
    val name: String? = "Alice"
    val greeting = name?.let { "Hello, $it!" } ?: "Hello, stranger!"
    println("  let: $greeting")  // => let: Hello, Alice!

    // run: executes a block with the object as `this` (receiver). Returns the lambda
    // result. Use when you need to compute something from an object's properties.
    val result = "Hello, World!".run {
        println("  run: original='$this'")  // => run: original='Hello, World!'
        uppercase().reversed()
    }
    println("  run result: $result")  // => run result: !DLROW ,OLLEH

    // with: same as run but takes the receiver as an argument instead of an extension.
    // Prefer `with` when the object is already in scope and you want to call multiple
    // methods on it without repeating the variable name.
    val numbers = mutableListOf(1, 2, 3)
    val summary = with(numbers) {
        add(4)
        add(5)
        "List has $size items, sum=${sum()}"
    }
    println("  with: $summary")  // => with: List has 5 items, sum=15

    // apply: configures an object and returns the object itself. The object is `this`
    // inside the lambda. Ideal for object initialization — Kotlin's builder pattern
    // replacement. Since it returns the object, you can chain apply calls.
    val sb = StringBuilder().apply {
        append("Hello")
        append(", ")
        append("World")
        append("!")
    }
    println("  apply: $sb")  // => apply: Hello, World!

    // also: performs side effects and returns the object itself. The object is `it`
    // inside the lambda. Use for logging, debugging, or validation without breaking
    // a call chain. Equivalent to Java's peek() in streams.
    val items = mutableListOf("a", "b").also {
        println("  also: initial list = $it")  // => also: initial list = [a, b]
        it.add("c")
    }
    println("  also: after = $items")  // => also: after = [a, b, c]

    println()
}

// ── 8. Delegation ────────────────────────────────────────────────────
fun delegation() {
    println("=== 8. DELEGATION ===")  // => === 8. DELEGATION ===

    val profile = UserProfile()

    // `by lazy`: the lambda runs exactly once on first access, then the result is
    // cached. Subsequent accesses return the cached value without re-executing.
    // This is thread-safe (synchronized) by default. Use for expensive initialization
    // that might not be needed — avoids paying the cost upfront.
    println("  First access to createdAt:")  // => First access to createdAt:
    println("    createdAt = ${profile.createdAt}")  // => (varies — prints lazy init message, then timestamp)
    println("  Second access (cached):")  // => Second access (cached):
    println("    createdAt = ${profile.createdAt}")  // => (varies — same cached timestamp)

    // Custom observable delegate in action: the onChange callback fires on every
    // property assignment with the old and new values.
    profile.displayName = "Alice"
    profile.displayName = "Bob"

    // Map delegation: properties are backed by a Map instead of fields. The property
    // name is used as the map key. Read-only properties use Map; read-write use
    // MutableMap. Useful for config objects, JSON deserialization, or dynamic property bags.
    class Config(map: Map<String, Any?>) {
        val host: String by map
        val port: Int by map
        val debug: Boolean by map
    }

    val config = Config(mapOf("host" to "localhost", "port" to 8080, "debug" to true))
    println("  Map delegate: host=${config.host}, port=${config.port}, debug=${config.debug}")  // => Map delegate: host=localhost, port=8080, debug=true

    println()
}

// ── 9. DSL building ──────────────────────────────────────────────────
fun dslBuilding() {
    println("=== 9. DSL BUILDING ===")  // => === 9. DSL BUILDING ===

    // Type-safe builder using lambdas with receivers: html { } calls the lambda with
    // an HtmlBuilder as `this`, so h1(), p(), ul() are called directly without a
    // builder reference. This pattern is Kotlin's signature feature for DSLs —
    // used extensively in Gradle Kotlin DSL, Ktor, Jetpack Compose, and kotlinx.html.
    val page = html {
        h1("Kotlin DSL Demo")
        p("This is a type-safe builder pattern.")
        ul {
            li("Item 1")
            li("Item 2")
            li("Item 3")
        }
        p("Footer text here.")
    }
    println("  Generated HTML:")  // => Generated HTML:
    page.lines().forEach { println("    $it") }  // => (HTML lines: <h1>..., <p>..., <ul>..., etc.)

    // Infix functions: called without dot or parentheses (`5 shouldEqual 5` instead of
    // `5.shouldEqual(5)`). Requirements: must be member or extension functions, must
    // have exactly one parameter, cannot have varargs or default values. Used heavily
    // in testing frameworks (Kotest), collection operations (`to`, `until`, `downTo`),
    // and DSLs. Abuse leads to unreadable code — use judiciously.
    infix fun Int.shouldEqual(expected: Int) {
        check(this == expected) { "Expected $expected but got $this" }
        println("    PASS: $this == $expected")  // => (varies)
    }

    println("  Mini test DSL:")  // => Mini test DSL:
    5 shouldEqual 5
    (2 + 3) shouldEqual 5

    println()
}

// ── 10. Coroutines (conceptual) ──────────────────────────────────────
fun coroutinesConcepts() {
    println("=== 10. COROUTINES (conceptual — requires kotlinx.coroutines) ===")  // => === 10. COROUTINES (conceptual — requires kotlinx.coroutines) ===
    // Kotlin coroutines (kotlinx.coroutines, KEEP-87): lightweight concurrency primitives
    // that use CPS (continuation-passing style) transformation at compile time. Unlike
    // Java's virtual threads (JVM-level, blocking-friendly), Kotlin coroutines are a
    // compiler feature — `suspend` functions are transformed into state machines with
    // callbacks. This means coroutines work on any JVM version (even Java 8) and on
    // Kotlin/JS and Kotlin/Native. The tradeoff: you must use `suspend` functions and
    // coroutine-aware libraries; blocking code will block the underlying thread.
    println("""
    |  // launch — fire-and-forget coroutine builder. Returns a Job (handle to cancel/join).
    |  // The coroutine inherits the parent's CoroutineScope for structured concurrency.
    |  runBlocking {
    |      val job = launch {
    |          delay(1000)  // suspends without blocking the thread (unlike Thread.sleep)
    |          println("World!")
    |      }
    |      println("Hello,")
    |      job.join()
    |  }
    |
    |  // async/await — concurrent computation that returns a value via Deferred<T>.
    |  // Unlike CompletableFuture, async starts eagerly but can be made lazy with
    |  // CoroutineStart.LAZY. Both coroutines run concurrently on the dispatcher's thread pool.
    |  runBlocking {
    |      val deferred1 = async { fetchUser(1) }
    |      val deferred2 = async { fetchUser(2) }
    |      val users = listOf(deferred1.await(), deferred2.await())
    |  }
    |
    |  // Flow — cold asynchronous stream (Kotlin's reactive streams equivalent).
    |  // Cold means no data is produced until collect() is called (unlike Channels which are hot).
    |  // Flows support backpressure naturally because emit() suspends until the collector is ready.
    |  fun numbers(): Flow<Int> = flow {
    |      for (i in 1..5) {
    |          delay(100)
    |          emit(i)  // suspends if the collector is slow (backpressure)
    |      }
    |  }
    |  runBlocking {
    |      numbers()
    |          .filter { it % 2 == 0 }
    |          .map { it * it }
    |          .collect { println(it) }
    |  }
    |
    |  // Channel — hot stream for communication between coroutines (CSP-style).
    |  // Unlike Flow, Channels are eager and can have multiple producers/consumers.
    |  // send() suspends when the buffer is full; receive() suspends when empty.
    |  runBlocking {
    |      val channel = Channel<Int>()
    |      launch { for (i in 1..5) channel.send(i); channel.close() }
    |      for (value in channel) println(value)
    |  }
    |
    |  // Structured concurrency: coroutineScope { } ensures ALL child coroutines
    |  // complete (or are cancelled) before the scope exits. If any child fails,
    |  // all siblings are cancelled automatically. This prevents coroutine leaks —
    |  // a guarantee that Java's virtual threads don't provide (unless using
    |  // StructuredTaskScope from Project Loom's preview API).
    |  suspend fun fetchAll() = coroutineScope {
    |      val a = async { api.fetchA() }
    |      val b = async { api.fetchB() }
    |      Result(a.await(), b.await())  // if one fails, both are cancelled
    |  }
    """.trimMargin())

    println()
    println("=== DONE ===")  // => === DONE ===
}
