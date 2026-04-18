/**
 * Kotlin Fundamentals — single runnable file.
 * Compile & run:  kotlinc KotlinFundamentals.kt -include-runtime -d kf.jar && java -jar kf.jar
 * Or:             kotlin KotlinFundamentals.kt  (with Kotlin scripting)
 */

// ── Sealed classes & data classes ─────────────────────────────────────
sealed class Shape {
    abstract fun area(): Double

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

// ── Enum class ────────────────────────────────────────────────────────
enum class Direction(val dx: Int, val dy: Int) {
    NORTH(0, 1), SOUTH(0, -1), EAST(1, 0), WEST(-1, 0);

    fun opposite(): Direction = when (this) {
        NORTH -> SOUTH; SOUTH -> NORTH
        EAST -> WEST; WEST -> EAST
    }
}

// ── Object declaration (singleton) ────────────────────────────────────
object Registry {
    private val items = mutableMapOf<String, Any>()
    fun register(key: String, value: Any) { items[key] = value }
    fun lookup(key: String): Any? = items[key]
    override fun toString() = "Registry($items)"
}

// ── Companion object ─────────────────────────────────────────────────
data class Color(val r: Int, val g: Int, val b: Int) {
    companion object {
        val RED = Color(255, 0, 0)
        val GREEN = Color(0, 255, 0)
        val BLUE = Color(0, 0, 255)
        fun fromHex(hex: String): Color {
            val v = hex.removePrefix("#").toLong(16).toInt()
            return Color((v shr 16) and 0xFF, (v shr 8) and 0xFF, v and 0xFF)
        }
    }
}

// ── Interfaces & generics ────────────────────────────────────────────
interface Describable {
    fun describe(): String
    fun tag(): String = "[${describe()}]"
}

class NamedItem(val name: String, val value: Int) : Describable {
    override fun describe() = "$name=$value"
}

// ── Extension functions ──────────────────────────────────────────────
fun String.wordCount(): Int = this.trim().split(Regex("\\s+")).size

fun <T> List<T>.secondOrNull(): T? = if (size >= 2) this[1] else null

fun Int.isEven(): Boolean = this % 2 == 0

// ── Higher-order functions ───────────────────────────────────────────
fun <T, R> List<T>.mapAndFilter(transform: (T) -> R, predicate: (R) -> Boolean): List<R> =
    this.map(transform).filter(predicate)

// ── Inline function ──────────────────────────────────────────────────
inline fun <T> measureTime(label: String, block: () -> T): T {
    val start = System.nanoTime()
    val result = block()
    val elapsed = (System.nanoTime() - start) / 1_000_000.0
    println("    $label took %.2f ms".format(elapsed))
    return result
}

// ── Lambda with receiver (builder pattern) ────────────────────────────
class HtmlBuilder {
    private val elements = mutableListOf<String>()
    fun h1(text: String) { elements += "<h1>$text</h1>" }
    fun p(text: String) { elements += "<p>$text</p>" }
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

// ── Delegation ───────────────────────────────────────────────────────
class ObservableProperty<T>(private var value: T, private val onChange: (T, T) -> Unit) {
    operator fun getValue(thisRef: Any?, property: kotlin.reflect.KProperty<*>): T = value
    operator fun setValue(thisRef: Any?, property: kotlin.reflect.KProperty<*>, newValue: T) {
        val old = value
        value = newValue
        onChange(old, newValue)
    }
}

class UserProfile {
    val createdAt: Long by lazy {
        println("    (lazy init: computing createdAt)")
        System.currentTimeMillis()
    }

    var displayName: String by ObservableProperty("Anonymous") { old, new ->
        println("    (observed: displayName changed '$old' -> '$new')")
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
    println("=== 1. BASICS ===")

    // val (immutable) vs var (mutable)
    val name = "Kotlin"
    var counter = 0
    counter += 1
    println("  val name=$name, var counter=$counter")

    // String templates
    val x = 42
    println("  x=$x, x*2=${x * 2}, name has ${name.length} chars")

    // Multiline strings
    val text = """
        |Line 1: trimMargin strips leading whitespace
        |Line 2: using pipe as margin prefix
        |Line 3: raw string literal
    """.trimMargin()
    println("  Multiline:\n$text")

    // Null safety
    val nullable: String? = "hello"
    val alsoNull: String? = null

    // Safe call ?.
    println("  nullable?.length = ${nullable?.length}")
    println("  alsoNull?.length = ${alsoNull?.length}")

    // Elvis operator ?:
    val len = alsoNull?.length ?: -1
    println("  alsoNull?.length ?: -1 = $len")

    // ?.let for non-null execution
    nullable?.let { println("  nullable is not null: '$it'") }
    alsoNull?.let { println("  THIS SHOULD NOT PRINT") }

    // Not-null assertion !! (use sparingly)
    val definitelyNotNull: String = nullable!!
    println("  !! assertion: $definitelyNotNull")

    // Type checks and smart casts
    val obj: Any = "I'm a String"
    if (obj is String) {
        println("  Smart cast: length=${obj.length}")  // obj is auto-cast to String
    }

    println()
}

// ── 2. Collections ───────────────────────────────────────────────────
fun collections() {
    println("=== 2. COLLECTIONS ===")

    // Immutable collections
    val names = listOf("Alice", "Bob", "Charlie", "Diana")
    val scores = mapOf("Alice" to 95, "Bob" to 87, "Charlie" to 92)
    val tags = setOf("kotlin", "jvm", "oop")
    println("  List: $names")
    println("  Map: $scores")
    println("  Set: $tags")

    // Mutable collections
    val mutableNames = mutableListOf("Eve", "Frank")
    mutableNames += "Grace"
    mutableNames.removeAt(0)
    println("  Mutable list: $mutableNames")

    // Collection operations
    val numbers = listOf(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

    val evenSquares = numbers.filter { it.isEven() }.map { it * it }
    println("  Even squares: $evenSquares")

    val sum = numbers.reduce { acc, n -> acc + n }
    println("  Reduce sum: $sum")

    val grouped = names.groupBy { it.first() }
    println("  Grouped by first char: $grouped")

    val flat = listOf(listOf(1, 2), listOf(3, 4), listOf(5)).flatMap { it }
    println("  FlatMap: $flat")

    // associate / associateBy
    val nameLengths = names.associateWith { it.length }
    println("  AssociateWith: $nameLengths")

    // partition
    val (evens, odds) = numbers.partition { it.isEven() }
    println("  Partition evens=$evens, odds=$odds")

    // zip and unzip
    val keys = listOf("a", "b", "c")
    val values = listOf(1, 2, 3)
    val zipped = keys.zip(values)
    println("  Zip: $zipped")
    val (unzippedKeys, unzippedVals) = zipped.unzip()
    println("  Unzip: keys=$unzippedKeys, vals=$unzippedVals")

    println()
}

// ── 3. Sequences (lazy evaluation) ───────────────────────────────────
fun sequences() {
    println("=== 3. SEQUENCES ===")

    // Sequences are lazy — operations are not executed until a terminal operation
    val result = (1..1_000_000).asSequence()
        .filter { it % 3 == 0 }
        .map { it * it }
        .take(5)
        .toList()
    println("  First 5 squares of multiples of 3: $result")

    // generateSequence
    val powers = generateSequence(1) { it * 2 }.take(10).toList()
    println("  Powers of 2: $powers")

    // sequence builder
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
    println("  First 12 Fibonacci: ${fibs.take(12).toList()}")

    println()
}

// ── 4. Classes & objects ─────────────────────────────────────────────
fun classesAndObjects() {
    println("=== 4. CLASSES & OBJECTS ===")

    // Data class — auto-generates equals, hashCode, toString, copy
    data class User(val name: String, val age: Int)

    val user = User("Alice", 30)
    val updated = user.copy(age = 31)
    println("  Data class: $user")
    println("  Copy with modification: $updated")
    println("  Destructuring: name=${user.name}, age=${user.age}")

    // Sealed class + exhaustive when
    val shapes = listOf(Shape.Circle(5.0), Shape.Rectangle(3.0, 4.0), Shape.Triangle(6.0, 3.0))
    for (shape in shapes) {
        val desc = when (shape) {
            is Shape.Circle -> "Circle r=${shape.radius}"
            is Shape.Rectangle -> "Rect ${shape.width}x${shape.height}"
            is Shape.Triangle -> "Triangle b=${shape.base} h=${shape.height}"
        }
        println("  $desc -> area=${shape.area()}")
    }

    // Enum class
    val dir = Direction.NORTH
    println("  Direction: $dir, opposite=${dir.opposite()}, dx=${dir.dx} dy=${dir.dy}")

    // Object (singleton)
    Registry.register("version", "1.0")
    Registry.register("lang", "Kotlin")
    println("  Singleton: $Registry")

    // Companion object
    println("  Companion: RED=${Color.RED}, fromHex=${Color.fromHex("#FF8800")}")

    // Interface with default method
    val item = NamedItem("score", 100)
    println("  Interface: ${item.describe()}, tag=${item.tag()}")

    println()
}

// ── 5. When expressions ──────────────────────────────────────────────
fun patternMatchingWithWhen() {
    println("=== 5. WHEN EXPRESSIONS ===")

    // when as expression
    val x = 15
    val label = when {
        x < 0 -> "negative"
        x == 0 -> "zero"
        x in 1..10 -> "small"
        x in 11..100 -> "medium"
        else -> "large"
    }
    println("  $x is $label")

    // when with subject
    val obj: Any = listOf(1, 2, 3)
    val typeDesc = when (obj) {
        is Int -> "integer: $obj"
        is String -> "string of length ${obj.length}"
        is List<*> -> "list of size ${obj.size}"
        else -> "unknown"
    }
    println("  Type matching: $typeDesc")

    // when with multiple values
    val char = 'e'
    val kind = when (char) {
        'a', 'e', 'i', 'o', 'u' -> "vowel"
        in 'a'..'z' -> "consonant"
        in 'A'..'Z' -> "uppercase letter"
        else -> "other"
    }
    println("  '$char' is a $kind")

    println()
}

// ── 6. Functional ────────────────────────────────────────────────────
fun functional() {
    println("=== 6. FUNCTIONAL ===")

    // Lambdas
    val double: (Int) -> Int = { it * 2 }
    val add: (Int, Int) -> Int = { a, b -> a + b }
    println("  double(5)=${double(5)}, add(3,4)=${add(3, 4)}")

    // Higher-order functions
    val numbers = listOf(1, 2, 3, 4, 5)
    val result = numbers.mapAndFilter({ it * it }, { it > 10 })
    println("  mapAndFilter (square, >10): $result")

    // Extension function
    println("  \"hello world\".wordCount() = ${"hello world".wordCount()}")
    println("  listOf(1,2,3).secondOrNull() = ${listOf(1, 2, 3).secondOrNull()}")

    // Function references
    val words = listOf("Hello", "WORLD", "kotlin")
    val lower = words.map(String::lowercase)
    println("  Method ref lowercase: $lower")

    // Inline function with measurement
    val computed = measureTime("sum 1..1M") {
        (1..1_000_000).sum()
    }
    println("    result=$computed")

    // Function composition (manual — Kotlin stdlib doesn't have compose)
    fun <A, B, C> compose(f: (B) -> C, g: (A) -> B): (A) -> C = { a -> f(g(a)) }
    val doubleAndToString = compose(Int::toString, double)
    println("  compose(toString, double)(21) = ${doubleAndToString(21)}")

    println()
}

// ── 7. Scope functions ───────────────────────────────────────────────
fun scopeFunctions() {
    println("=== 7. SCOPE FUNCTIONS ===")

    // let — transform nullable / scoped variable
    val name: String? = "Alice"
    val greeting = name?.let { "Hello, $it!" } ?: "Hello, stranger!"
    println("  let: $greeting")

    // run — execute block with receiver, return result
    val result = "Hello, World!".run {
        println("  run: original='$this'")
        uppercase().reversed()
    }
    println("  run result: $result")

    // with — like run but takes receiver as argument
    val numbers = mutableListOf(1, 2, 3)
    val summary = with(numbers) {
        add(4)
        add(5)
        "List has $size items, sum=${sum()}"
    }
    println("  with: $summary")

    // apply — configure an object, return the object itself
    val sb = StringBuilder().apply {
        append("Hello")
        append(", ")
        append("World")
        append("!")
    }
    println("  apply: $sb")

    // also — side effects, return the object
    val items = mutableListOf("a", "b").also {
        println("  also: initial list = $it")
        it.add("c")
    }
    println("  also: after = $items")

    println()
}

// ── 8. Delegation ────────────────────────────────────────────────────
fun delegation() {
    println("=== 8. DELEGATION ===")

    val profile = UserProfile()

    // by lazy — initialized on first access
    println("  First access to createdAt:")
    println("    createdAt = ${profile.createdAt}")
    println("  Second access (cached):")
    println("    createdAt = ${profile.createdAt}")

    // Observable property (custom delegate)
    profile.displayName = "Alice"
    profile.displayName = "Bob"

    // Map delegation
    class Config(map: Map<String, Any?>) {
        val host: String by map
        val port: Int by map
        val debug: Boolean by map
    }

    val config = Config(mapOf("host" to "localhost", "port" to 8080, "debug" to true))
    println("  Map delegate: host=${config.host}, port=${config.port}, debug=${config.debug}")

    println()
}

// ── 9. DSL building ──────────────────────────────────────────────────
fun dslBuilding() {
    println("=== 9. DSL BUILDING ===")

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
    println("  Generated HTML:")
    page.lines().forEach { println("    $it") }

    // Infix functions for DSL-like syntax
    infix fun Int.shouldEqual(expected: Int) {
        check(this == expected) { "Expected $expected but got $this" }
        println("    PASS: $this == $expected")
    }

    println("  Mini test DSL:")
    5 shouldEqual 5
    (2 + 3) shouldEqual 5

    println()
}

// ── 10. Coroutines (conceptual) ──────────────────────────────────────
fun coroutinesConcepts() {
    println("=== 10. COROUTINES (conceptual — requires kotlinx.coroutines) ===")
    println("""
    |  // launch — fire and forget
    |  runBlocking {
    |      val job = launch {
    |          delay(1000)
    |          println("World!")
    |      }
    |      println("Hello,")
    |      job.join()
    |  }
    |
    |  // async/await — concurrent computation
    |  runBlocking {
    |      val deferred1 = async { fetchUser(1) }
    |      val deferred2 = async { fetchUser(2) }
    |      val users = listOf(deferred1.await(), deferred2.await())
    |  }
    |
    |  // Flow — cold asynchronous stream
    |  fun numbers(): Flow<Int> = flow {
    |      for (i in 1..5) {
    |          delay(100)
    |          emit(i)
    |      }
    |  }
    |  runBlocking {
    |      numbers()
    |          .filter { it % 2 == 0 }
    |          .map { it * it }
    |          .collect { println(it) }
    |  }
    |
    |  // Channel — hot stream for communication between coroutines
    |  runBlocking {
    |      val channel = Channel<Int>()
    |      launch { for (i in 1..5) channel.send(i); channel.close() }
    |      for (value in channel) println(value)
    |  }
    |
    |  // Structured concurrency with coroutineScope
    |  suspend fun fetchAll() = coroutineScope {
    |      val a = async { api.fetchA() }
    |      val b = async { api.fetchB() }
    |      Result(a.await(), b.await())  // if one fails, both are cancelled
    |  }
    """.trimMargin())

    println()
    println("=== DONE ===")
}
