// Scala uses implicit imports for common types (scala._, scala.Predef._, java.lang._).
// These explicit imports bring in concurrency utilities from Scala's standard library.
import scala.concurrent.{Future, Promise, Await}
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.duration.*
import scala.util.{Try, Success, Failure}

/**
 * Scala 3 Fundamentals — single runnable file.
 * Compile & run:  scala ScalaFundamentals.scala
 * Or:             scalac ScalaFundamentals.scala && scala ScalaFundamentals
 */

// Sealed traits + case classes: Scala's algebraic data types (ADTs). `sealed` restricts
// all direct subtypes to this file, enabling exhaustive pattern matching. This is the
// foundation of FP in Scala — the compiler warns if a match is non-exhaustive.
// Compare with Java's sealed interfaces (JEP 409) and Kotlin's sealed classes.
sealed trait Shape:
  def area: Double

// Case classes auto-generate: apply() (no `new` needed), unapply() (pattern matching),
// equals(), hashCode(), toString(), copy(), and product iterator. They are Scala's
// primary data modeling tool — equivalent to Java records but available since Scala 2.0
// (15+ years before Java 16). Unlike Java records, case classes support inheritance
// from traits and can have additional methods and fields.
case class Circle(radius: Double) extends Shape:
  def area: Double = Math.PI * radius * radius

case class Rectangle(width: Double, height: Double) extends Shape:
  def area: Double = width * height

case class Triangle(base: Double, height: Double) extends Shape:
  def area: Double = 0.5 * base * height

// Scala 3 enums: a unified syntax replacing Scala 2's sealed trait + case object pattern.
// Enum values can carry parameters (like Kotlin enum classes and Java enums with fields).
// Under the hood, Scala 3 enums compile to sealed classes with companion object valueOf/values.
enum Direction(val dx: Int, val dy: Int):
  case North extends Direction(0, 1)
  case South extends Direction(0, -1)
  case East  extends Direction(1, 0)
  case West  extends Direction(-1, 0)

  // Pattern matching with `match`: Scala's equivalent of switch/when. Unlike Java/Kotlin,
  // Scala's match is an expression (returns a value) and has been pattern-matching since
  // Scala 1.0 — it influenced Java 21's switch pattern matching design.
  def opposite: Direction = this match
    case North => South
    case South => North
    case East  => West
    case West  => East

// Type aliases: create readable names for complex types without creating new types.
// They are fully transparent — `Matrix[Int]` is identical to `List[List[Int]]` at both
// compile time and runtime. Use for documentation; use opaque types (Scala 3) when you
// want type safety without runtime overhead.
type Matrix[A] = List[List[A]]
type Predicate[A] = A => Boolean

// Traits: Scala's primary abstraction mechanism, combining interface and mixin behavior.
// Unlike Java interfaces (no state until default methods in Java 8) and Kotlin interfaces
// (can declare properties but no backing fields), Scala traits can hold concrete state,
// constructors (Scala 3), and are linearized for method resolution.
trait Describable:
  def describe: String
  def tag: String = s"[$describe]"

// Self-type annotation (`self: Describable =>`): declares that any class mixing in
// Loggable MUST also mix in Describable. This is compile-time dependency injection —
// the compiler enforces the constraint. Unlike inheritance (Loggable extends Describable),
// self-types express a "requires" relationship without creating a subtype relationship.
// Use self-types for the cake pattern (dependency injection via traits).
trait Loggable:
  self: Describable =>  // self-type: requires Describable
  def log(): Unit = println(s"    LOG: $describe")  // => (varies)

// Multiple trait mixin with `extends ... with`: Scala linearizes the trait hierarchy
// from right to left, creating a single linear chain for method resolution (no diamond
// problem ambiguity). The linearization order determines which `super` calls resolve to.
class NamedItem(val name: String, val value: Int) extends Describable with Loggable:
  def describe: String = s"$name=$value"

// Stackable trait modifications (decorator pattern via linearization): `abstract override`
// means this trait can only be mixed into a class that already provides a concrete
// implementation of transform(). super.transform() calls the next trait in the
// linearization chain, not a fixed parent. This creates a pipeline of transformations.
trait Transformer:
  def transform(s: String): String

// `abstract override`: this trait overrides transform() but still calls super, which
// must be provided by the class it's mixed into. The linearization order determines
// which `super` resolves to — rightmost trait in the `with` chain wraps outermost.
trait UpperCase extends Transformer:
  abstract override def transform(s: String): String = super.transform(s.toUpperCase)

trait Trimmed extends Transformer:
  abstract override def transform(s: String): String = super.transform(s.trim)

class BaseTransformer extends Transformer:
  def transform(s: String): String = s

// Variance annotations on type parameters: Scala's approach to safe subtyping of
// generic containers. This is declared at the class definition (declaration-site variance),
// unlike Java which uses wildcards at each use site (use-site variance via ? extends/? super).
// Kotlin also supports declaration-site variance with `out`/`in`.
sealed trait Animal:
  def name: String

case class Dog(name: String) extends Animal
case class Cat(name: String) extends Animal

// Covariance (+A): Box[Dog] <: Box[Animal] if Dog <: Animal. Safe because Box only
// PRODUCES A values (via `val content`). The compiler forbids covariant types in
// contravariant (input) positions — you can't have a `def put(a: A)` method.
class Box[+A](val content: A):
  override def toString: String = s"Box($content)"

// Contravariance (-A): Printer[Animal] <: Printer[Dog] (reversed!). Safe because
// Printer only CONSUMES A values (via `def print(a: A)`). A printer that can handle
// any Animal can certainly handle a Dog. This is Liskov Substitution in action.
trait Printer[-A]:
  def print(a: A): String

// Given/Using (Scala 3): replaces Scala 2's implicits with clearer semantics.
// `given` defines a canonical value for a type; `using` requests it at the call site.
// The compiler searches for given instances in companion objects, imports, and the
// current scope. This powers type classes, dependency injection, and context passing.
// Compare with Kotlin's lack of type classes (uses extension functions instead) and
// Java's complete absence of implicit resolution.
trait Ordering[A]:
  def compare(a: A, b: A): Int

// `given ... with`: defines a named given instance. The name (intOrdering) is optional
// but useful for debugging and explicit imports. Anonymous givens (`given Ordering[Int] with`)
// are also valid but harder to reference.
given intOrdering: Ordering[Int] with
  def compare(a: Int, b: Int): Int = a - b

given stringOrdering: Ordering[String] with
  def compare(a: String, b: String): Int = a.compareTo(b)

// `(using ord: Ordering[A])`: the compiler automatically passes the appropriate given
// instance based on the type parameter A. This is the type class pattern — Ordering[A]
// is a type class, and given instances are its implementations for specific types.
def maxOf[A](a: A, b: A)(using ord: Ordering[A]): A =
  if ord.compare(a, b) >= 0 then a else b

// Extension methods (Scala 3): add methods to existing types without modification.
// Unlike Scala 2's implicit classes (which allocated a wrapper object), Scala 3
// extensions are compiled to static methods — zero allocation overhead.
// Compare with Kotlin's extension functions (same concept, same static dispatch).
extension (s: String)
  def wordCount: Int = s.trim.split("\\s+").length
  def isPalindrome: Boolean = s == s.reverse

// Generic extension: adds methods to List[A] for any A. The Option return type
// follows Scala's convention of encoding absence in the type system rather than
// using null. Option is a sealed trait with Some(value) and None subtypes.
extension [A](list: List[A])
  def secondOption: Option[A] = if list.length >= 2 then Some(list(1)) else None

// Custom extractors: objects with an unapply() method enable custom pattern matching.
// When you write `case Even(n)`, the compiler calls Even.unapply(n) and matches if
// it returns Some. This is what makes case classes work — the compiler auto-generates
// unapply() for them. Custom extractors let you pattern-match on ANY condition.
object Even:
  def unapply(n: Int): Option[Int] = if n % 2 == 0 then Some(n) else None

// Multi-value extractors return Option[TupleN] to destructure into multiple bindings.
object Email:
  def unapply(s: String): Option[(String, String)] =
    val parts = s.split("@")
    if parts.length == 2 then Some((parts(0), parts(1))) else None

// ═════════════════════════════════════════════════════════════════════
// MAIN
// ═════════════════════════════════════════════════════════════════════
// @main annotation (Scala 3): generates a main class from a top-level function.
// Replaces Scala 2's `object Main extends App` or `def main(args: Array[String])`.
@main def run(): Unit =
  basics()
  collections()
  patternMatching()
  functionalProgramming()
  typesAndVariance()
  traitsAndComposition()
  givensAndExtensions()
  concurrency()

// ── 1. Basics ────────────────────────────────────────────────────────
def basics(): Unit =
  println("=== 1. BASICS ===")  // => === 1. BASICS ===

  // `val` (immutable) and `var` (mutable): like Kotlin, Scala encourages immutability
  // by convention. In idiomatic Scala, `var` is rare — prefer `val` with functional
  // transformations. Scala's `val` is compiled to a Java `final` field.
  val name = "Scala"
  var counter = 0
  counter += 1
  println(s"  val name=$name, var counter=$counter")  // => val name=Scala, var counter=1

  // Type inference: Scala's type inference is more powerful than Java's or Kotlin's —
  // it can infer return types of methods, type parameters, and complex generic types
  // using local type inference (Hindley-Milner inspired, but not full HM). Explicit
  // type annotations are recommended for public API methods for documentation and
  // to avoid inference surprises.
  val x: Int = 42
  val pi = 3.14159       // inferred as Double
  val flag = true        // inferred as Boolean
  println(s"  x=$x, pi=$pi, flag=$flag")  // => x=42, pi=3.14159, flag=true

  // String interpolation: three built-in interpolators. `s""` evaluates expressions,
  // `f""` adds printf-style formatting, `raw""` disables escape processing.
  // You can define custom interpolators via extension methods on StringContext.
  println(s"  s-interpolation: $name has ${name.length} chars")  // => s-interpolation: Scala has 5 chars
  println(f"  f-interpolation: pi=$pi%.3f")  // => f-interpolation: pi=3.142
  println(raw"  raw: no escape \n here")  // => raw: no escape \n here

  // Multiline strings with stripMargin: uses `|` as the margin delimiter by default.
  // Same concept as Kotlin's trimMargin(). Java's text blocks (Java 15+) handle
  // indentation automatically without a margin character.
  val text = """
    |Line 1: stripMargin
    |Line 2: trims leading whitespace
    |Line 3: using pipe prefix
    """.stripMargin.trim
  println(s"  Multiline:\n$text")  // => Multiline: (followed by 3 stripped lines)

  // Tuples: fixed-size heterogeneous collections. Scala supports tuples up to 22
  // elements (Tuple1 through Tuple22). Access elements with _1, _2, etc. (1-indexed).
  // Java has no built-in tuples; Kotlin has Pair and Triple only. Scala 3's tuples
  // are more flexible than Scala 2's — they support concatenation and dynamic sizes.
  val pair = (42, "hello")
  val triple = (1, "two", 3.0)
  println(s"  Tuple: $pair, first=${pair._1}, second=${pair._2}")  // => Tuple: (42,hello), first=42, second=hello
  println(s"  Triple: $triple")  // => Triple: (1,two,3.0)

  // Destructuring (pattern-based): uses the unapply() method of Tuple2 to extract
  // components. This works with any type that has an unapply() — not just tuples.
  val (num, str) = pair
  println(s"  Destructured: num=$num, str=$str")  // => Destructured: num=42, str=hello

  // Option[T]: Scala's null-safe container — a sealed trait with two subtypes: Some(value)
  // and None. Unlike Kotlin's nullable types (?), Option is a full-fledged type that
  // supports map, flatMap, filter, fold, etc. — it's a monad. This makes it composable
  // in for-comprehensions. Use Option instead of null to make absence explicit in the type.
  val some: Option[String] = Some("present")
  val none: Option[String] = None
  println(s"  Option: some=${some.getOrElse("N/A")}, none=${none.getOrElse("N/A")}")  // => Option: some=present, none=N/A
  println(s"  Option map: ${some.map(_.toUpperCase)}")  // => Option map: Some(PRESENT)

  println()

// ── 2. Collections ───────────────────────────────────────────────────
def collections(): Unit =
  println("=== 2. COLLECTIONS ===")  // => === 2. COLLECTIONS ===

  // Scala collections are immutable by default (scala.collection.immutable._).
  // Mutable variants exist in scala.collection.mutable._ but are discouraged.
  // Immutable collections use structural sharing for efficiency — e.g., adding to a
  // List prepends in O(1) and shares the tail. This is fundamentally different from
  // Java/Kotlin where "immutable" often means a mutable collection wrapped in an
  // unmodifiable view.
  val names = List("Alice", "Bob", "Charlie", "Diana")
  val scores = Map("Alice" -> 95, "Bob" -> 87, "Charlie" -> 92)
  val tags = Set("scala", "jvm", "fp")
  println(s"  List: $names")  // => List: List(Alice, Bob, Charlie, Diana)
  println(s"  Map: $scores")  // => Map: Map(Alice -> 95, Bob -> 87, Charlie -> 92)
  println(s"  Set: $tags")  // => Set: Set(scala, jvm, fp)

  // Vector: persistent (immutable) data structure with O(log32 N) ~ effectively O(1)
  // random access, update, prepend, and append. Preferred over List when you need
  // indexed access. List is better for head/tail recursive processing.
  val vec = Vector(1, 2, 3, 4, 5)
  val updated = vec.updated(2, 99)
  println(s"  Vector: $vec, updated(2,99): $updated")  // => Vector: Vector(1, 2, 3, 4, 5), updated(2,99): Vector(1, 2, 99, 4, 5)

  val numbers = List(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

  // Underscore `_` as placeholder: `_ % 2 == 0` expands to `(x) => x % 2 == 0`.
  // Each `_` refers to a different parameter. Use only for simple expressions —
  // for anything complex, name the parameter explicitly.
  val evenSquares = numbers.filter(_ % 2 == 0).map(n => n * n)
  println(s"  Even squares: $evenSquares")  // => Even squares: List(4, 16, 36, 64, 100)

  // reduce vs foldLeft: reduce uses the first element as the initial accumulator and
  // throws on empty collections. foldLeft takes an explicit initial value and is safe
  // on empty collections. foldLeft processes left-to-right; foldRight processes
  // right-to-left (important for non-associative operations and lazy evaluation).
  val sum = numbers.reduce(_ + _)
  val product = numbers.foldLeft(1)(_ * _)
  println(s"  Reduce sum: $sum, foldLeft product: $product")  // => Reduce sum: 55, foldLeft product: 3628800

  val grouped = names.groupBy(_.head)
  println(s"  GroupBy first char: $grouped")  // => (varies — HashMap order is non-deterministic)

  // flatMap with identity: `flatMap(identity)` is equivalent to `flatten`. The `identity`
  // function `x => x` is imported from Predef. In Scala, flatMap is the monadic bind
  // operator — it's how for-comprehensions desugar (see functional section).
  val flat = List(List(1, 2), List(3, 4), List(5)).flatMap(identity)
  println(s"  FlatMap: $flat")  // => FlatMap: List(1, 2, 3, 4, 5)

  val (evens, odds) = numbers.partition(_ % 2 == 0)
  println(s"  Partition: evens=$evens, odds=$odds")  // => Partition: evens=List(2, 4, 6, 8, 10), odds=List(1, 3, 5, 7, 9)

  val keys = List("a", "b", "c")
  val values = List(1, 2, 3)
  val zipped = keys.zip(values)
  println(s"  Zip: $zipped")  // => Zip: List((a,1), (b,2), (c,3))
  println(s"  ToMap: ${zipped.toMap}")  // => ToMap: Map(a -> 1, b -> 2, c -> 3)

  // collect with partial functions: applies a PartialFunction that both tests AND
  // transforms in one step. More efficient than filter + map because it avoids
  // two passes. The `{ case s: String => ... }` syntax creates a PartialFunction literal.
  // This is unique to Scala — Java and Kotlin have no equivalent.
  val mixed: List[Any] = List(1, "hello", 2, "world", 3)
  val strings = mixed.collect { case s: String => s.toUpperCase }
  println(s"  Collect strings: $strings")  // => Collect strings: List(HELLO, WORLD)

  // LazyList (Scala 2.13+, replaces Stream): a lazily evaluated linked list where
  // elements are computed on demand and memoized. `#::` is the lazy cons operator.
  // This recursive definition of Fibonacci works because LazyList only evaluates
  // elements when accessed. Equivalent to Kotlin's sequence { } builder.
  val fibs: LazyList[Long] = 0L #:: 1L #:: fibs.zip(fibs.tail).map(_ + _)
  println(s"  First 12 Fibonacci: ${fibs.take(12).toList}")  // => First 12 Fibonacci: List(0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89)

  println()

// ── 3. Pattern matching ──────────────────────────────────────────────
def patternMatching(): Unit =
  println("=== 3. PATTERN MATCHING ===")  // => === 3. PATTERN MATCHING ===

  // Pattern matching on case classes: the compiler calls the auto-generated unapply()
  // to destructure. This is the core of Scala's expression-oriented style — match
  // returns a value, and the compiler warns if the match is non-exhaustive on sealed types.
  val shapes: List[Shape] = List(Circle(5), Rectangle(3, 4), Triangle(6, 3))
  for shape <- shapes do
    val desc = shape match
      case Circle(r)       => s"Circle r=$r"
      case Rectangle(w, h) => s"Rect ${w}x$h"
      case Triangle(b, h)  => s"Triangle b=$b h=$h"
    println(s"  $desc -> area=${shape.area}")  // => Circle r=5.0 -> area=78.5... | Rect 3.0x4.0 -> area=12.0 | Triangle b=6.0 h=3.0 -> area=9.0

  // Guards (`if` after pattern): add extra conditions to a pattern match.
  // The guard is evaluated only if the pattern itself matches.
  // Underscore `_` is the wildcard pattern — matches anything without binding.
  val numbers = List(-3, 0, 5, 12, 100)
  for n <- numbers do
    val label = n match
      case x if x < 0    => "negative"
      case 0              => "zero"
      case x if x <= 10   => "small positive"
      case x if x <= 50   => "medium positive"
      case _              => "large positive"
    println(s"  $n -> $label")  // => -3 -> negative | 0 -> zero | 5 -> small positive | 12 -> medium positive | 100 -> large positive

  // Custom extractors: Even.unapply() is called by the pattern matcher. If it returns
  // Some(n), the pattern matches and binds `e` to n. If None, the next case is tried.
  // This lets you pattern match on arbitrary conditions — not just data structure shape.
  println("  -- Extractors --")  // => -- Extractors --
  val nums = List(1, 2, 3, 4, 5, 6)
  for n <- nums do
    n match
      case Even(e) => println(s"    $n is Even($e)")  // => 2 is Even(2) | 4 is Even(4) | 6 is Even(6)
      case odd     => println(s"    $odd is odd")  // => 1 is odd | 3 is odd | 5 is odd

  // Multi-value extractor: Email.unapply returns Option[(String, String)], which
  // destructures into two bindings (user, domain).
  "user@example.com" match
    case Email(user, domain) => println(s"  Email: user=$user, domain=$domain")  // => Email: user=user, domain=example.com
    case other               => println(s"  Not an email: $other")

  // Tuple patterns: destructure tuples directly in match expressions. The compiler
  // uses TupleN.unapply() under the hood. Each position can be a nested pattern.
  val point = (3, 4)
  point match
    case (0, 0)    => println("  origin")
    case (x, 0)    => println(s"  on x-axis at $x")
    case (0, y)    => println(s"  on y-axis at $y")
    case (x, y)    => println(s"  point at ($x, $y)")  // => point at (3, 4)

  // List pattern with `::` (cons): destructures a list into head and tail.
  // `::` is actually a case class in Scala's List implementation, so this is
  // case class pattern matching. `head :: second :: tail` matches a list with
  // at least 2 elements, binding the rest to `tail` (which may be Nil).
  val items = List(1, 2, 3, 4, 5)
  items match
    case head :: second :: tail => println(s"  List head=$head, second=$second, tail=$tail")  // => List head=1, second=2, tail=List(3, 4, 5)
    case _                     => println("  too short")

  // Type patterns: match on runtime type using `: Type`. Due to JVM type erasure,
  // generic type parameters are erased — `case l: List[Int]` would match ANY List,
  // not just List[Int]. Scala uses `List[?]` (existential type) to acknowledge this.
  // Scala 3 can partially work around erasure with TypeTest and inline matching.
  val any: Any = List(1, 2, 3)
  any match
    case s: String    => println(s"  String: $s")
    case i: Int       => println(s"  Int: $i")
    case l: List[?]   => println(s"  List of size ${l.size}: $l")  // => List of size 3: List(1, 2, 3)
    case _            => println("  unknown type")

  println()

// ── 4. Functional programming ────────────────────────────────────────
def functionalProgramming(): Unit =
  println("=== 4. FUNCTIONAL PROGRAMMING ===")  // => === 4. FUNCTIONAL PROGRAMMING ===

  // Higher-order functions: functions that take or return functions. In Scala, functions
  // are values — `A => B` is syntactic sugar for `Function1[A, B]`. Scala compiles
  // lambda expressions to anonymous classes implementing FunctionN traits (or uses
  // Java 8's invokedynamic for SAM types). Unlike Kotlin's `inline`, Scala relies on
  // the JVM's JIT compiler to inline small lambdas automatically.
  def applyTwice[A](f: A => A, x: A): A = f(f(x))
  println(s"  applyTwice(_ + 1, 5) = ${applyTwice((_: Int) + 1, 5)}")  // => applyTwice(_ + 1, 5) = 7
  println(s"  applyTwice(_.toUpperCase, \"hi\") = ${applyTwice((_: String).toUpperCase, "hi")}")  // => applyTwice(_.toUpperCase, "hi") = HI

  // Currying with multiple parameter lists: `def add(a: Int)(b: Int)` is syntactic
  // sugar for `def add(a: Int): Int => Int`. This enables partial application — calling
  // add(5) returns a function `Int => Int`. Currying is fundamental to Scala's design:
  // implicit/using parameters must be in their own parameter list, and it enables
  // type inference to flow left-to-right across parameter lists.
  def add(a: Int)(b: Int): Int = a + b
  val add5 = add(5)
  println(s"  Curried: add(5)(3) = ${add(5)(3)}")  // => Curried: add(5)(3) = 8
  println(s"  Partial: add5(3) = ${add5(3)}")  // => Partial: add5(3) = 8

  // `.curried`: converts a multi-parameter function into a chain of single-parameter
  // functions. `(Int, Int) => Int` becomes `Int => (Int => Int)`. This is the
  // mathematical definition of currying (named after Haskell Curry).
  val multiply = (a: Int, b: Int) => a * b
  val curriedMult = multiply.curried
  println(s"  .curried: ${curriedMult(3)(4)}")  // => .curried: 12

  // PartialFunction[A, B]: a function that is only defined for some inputs of type A.
  // `isDefinedAt()` checks applicability; calling it on an undefined input throws
  // MatchError. The `{ case ... }` syntax creates a PartialFunction literal.
  // Partial functions are used extensively in Scala: collect(), recover(), onComplete(),
  // and actor message handlers (Akka). Java and Kotlin have no equivalent concept.
  val divide: PartialFunction[Int, Double] = {
    case n if n != 0 => 1.0 / n
  }
  println(s"  PartialFunction defined at 0? ${divide.isDefinedAt(0)}")  // => PartialFunction defined at 0? false
  println(s"  PartialFunction(5) = ${divide(5)}")  // => PartialFunction(5) = 0.2

  // lift(): converts PartialFunction[A, B] to A => Option[B] — wraps the result in
  // Some if defined, None otherwise. This makes partial functions safe to use without
  // catching MatchError. The inverse is `Function.unlift()`.
  val safeDivide = divide.lift  // converts to Int => Option[Double]
  println(s"  Lifted(0) = ${safeDivide(0)}, Lifted(4) = ${safeDivide(4)}")  // => Lifted(0) = None, Lifted(4) = Some(0.25)

  // For-comprehensions: syntactic sugar that desugars to flatMap/map/withFilter chains.
  // `for { x <- xs; y <- ys } yield (x, y)` becomes `xs.flatMap(x => ys.map(y => (x, y)))`.
  // This works with ANY type that has flatMap/map/withFilter — List, Option, Future, Try,
  // Either, or your own monadic types. This is Scala's equivalent of Haskell's do-notation.
  val pairs = for
    x <- List(1, 2, 3)
    y <- List('a', 'b')
  yield (x, y)
  println(s"  For-comprehension: $pairs")  // => For-comprehension: List((1,a), (1,b), (2,a), (2,b), (3,a), (3,b))

  // For-comprehension with Option: desugars to flatMap/map. If findUser returns None,
  // the entire expression short-circuits to None without calling findAge. This is
  // monadic composition — Option.flatMap returns None if the Option is empty,
  // avoiding nested null/None checks. Compare with Kotlin's `?.let {}` chains.
  def findUser(id: Int): Option[String] = if id == 1 then Some("Alice") else None
  def findAge(name: String): Option[Int] = if name == "Alice" then Some(30) else None

  val result = for
    name <- findUser(1)
    age  <- findAge(name)
  yield s"$name is $age"
  println(s"  Option for-comp: $result")  // => Option for-comp: Some(Alice is 30)
  println(s"  Option for-comp (miss): ${for { n <- findUser(2); a <- findAge(n) } yield s"$n is $a"}")  // => Option for-comp (miss): None

  // Try[T]: a monadic wrapper for computations that may throw exceptions. Success(value)
  // or Failure(exception). Like Option but carries the error cause. Use Try instead of
  // try/catch when you want to compose error-prone operations functionally.
  // Java uses checked exceptions (compile-time); Kotlin ignores them; Scala prefers
  // encoding errors in the type system via Try, Either, or effect systems (ZIO, Cats Effect).
  val parsed = Try("42".toInt)
  val failed = Try("abc".toInt)
  println(s"  Try success: $parsed")  // => Try success: Success(42)
  println(s"  Try failure: ${failed.toOption}")  // => Try failure: None

  // recover: applies a partial function to the Failure case, converting specific
  // exceptions into success values. Like Java's CompletableFuture.exceptionally()
  // but using Scala's PartialFunction for type-safe exception matching.
  val recovered = failed.recover { case _: NumberFormatException => -1 }
  println(s"  Try recovered: $recovered")  // => Try recovered: Success(-1)

  println()

// ── 5. Types and variance ────────────────────────────────────────────
def typesAndVariance(): Unit =
  println("=== 5. TYPES & VARIANCE ===")  // => === 5. TYPES & VARIANCE ===

  val matrix: Matrix[Int] = List(List(1, 2), List(3, 4))
  val isPositive: Predicate[Int] = _ > 0
  println(s"  Matrix: $matrix")  // => Matrix: List(List(1, 2), List(3, 4))
  println(s"  Predicate(5): ${isPositive(5)}, Predicate(-1): ${isPositive(-1)}")  // => Predicate(5): true, Predicate(-1): false

  // Covariance (+A) in action: Box[Dog] can be assigned to Box[Animal] because Dog <: Animal
  // and Box is covariant. The compiler checks that A only appears in covariant (output)
  // positions — return types and val types. If you tried `def put(a: A)`, the compiler
  // would reject it because that's a contravariant position.
  val dogBox: Box[Dog] = Box(Dog("Rex"))
  val animalBox: Box[Animal] = dogBox  // works because Box is covariant
  println(s"  Covariant: $animalBox")  // => Covariant: Box(Dog(Rex))

  // Contravariance (-A) in action: Printer[Animal] can be assigned to Printer[Dog]
  // because the subtyping is REVERSED. Intuition: if you can print any animal, you
  // can certainly print a dog. The compiler checks that A only appears in contravariant
  // (input) positions — method parameters. Java expresses this per-use with `? super T`.
  val animalPrinter: Printer[Animal] = new Printer[Animal]:
    def print(a: Animal): String = s"Animal(${a.name})"

  val dogPrinter: Printer[Dog] = animalPrinter  // works because Printer is contravariant
  println(s"  Contravariant: ${dogPrinter.print(Dog("Buddy"))}")  // => Contravariant: Animal(Buddy)

  // Context-bounded generics with `using`: the compiler passes the appropriate Ordering
  // instance based on A's type. This is the type class pattern — Ordering is the type class,
  // given instances provide implementations for specific types.
  def findMax[A](list: List[A])(using ord: Ordering[A]): A =
    list.reduce((a, b) => if ord.compare(a, b) >= 0 then a else b)

  println(s"  findMax(List(3,1,4,1,5)): ${findMax(List(3, 1, 4, 1, 5))}")  // => findMax(List(3,1,4,1,5)): 5
  println(s"  findMax(List(\"c\",\"a\",\"b\")): ${findMax(List("c", "a", "b"))}")  // => findMax(List("c","a","b")): c

  // GADTs (Generalized Algebraic Data Types): Scala 3 enums can carry type information
  // in each variant. Here, each case of Expr holds its structure, and the match
  // expression recursively evaluates the tree. This is the expression problem solution
  // from the FP side — adding new operations (eval, print, optimize) is easy.
  enum Expr:
    case Num(value: Double)
    case Add(left: Expr, right: Expr)
    case Mul(left: Expr, right: Expr)

  def eval(expr: Expr): Double = expr match
    case Expr.Num(v)    => v
    case Expr.Add(l, r) => eval(l) + eval(r)
    case Expr.Mul(l, r) => eval(l) * eval(r)

  val expression = Expr.Add(Expr.Num(3), Expr.Mul(Expr.Num(4), Expr.Num(5)))
  println(s"  ADT eval(3 + 4*5) = ${eval(expression)}")  // => ADT eval(3 + 4*5) = 23.0

  println()

// ── 6. Traits and composition ────────────────────────────────────────
def traitsAndComposition(): Unit =
  println("=== 6. TRAITS & COMPOSITION ===")  // => === 6. TRAITS & COMPOSITION ===

  val item = NamedItem("score", 100)
  println(s"  Describable: ${item.describe()}")  // => Describable: score=100
  println(s"  Tag: ${item.tag}")  // => Tag: [score=100]

  // Self-type in action: item.log() compiles because NamedItem extends both
  // Describable and Loggable. If NamedItem only mixed in Loggable without
  // Describable, the compiler would reject it at the class definition.
  item.log()

  // Stackable trait linearization: `BaseTransformer with Trimmed with UpperCase`
  // creates the chain: UpperCase -> Trimmed -> BaseTransformer.
  // UpperCase.transform() calls super.transform(s.toUpperCase) which resolves to
  // Trimmed.transform(), which calls super.transform(s.trim) resolving to
  // BaseTransformer.transform(). So the pipeline is: toUpperCase -> trim -> identity.
  // Result: "  hello world  " -> "  HELLO WORLD  " -> "HELLO WORLD" -> "HELLO WORLD"
  val transformer = new BaseTransformer with Trimmed with UpperCase
  val result = transformer.transform("  hello world  ")
  println(s"  Stackable traits: '$result'")  // => Stackable traits: 'HELLO WORLD'

  // Reversed order: `BaseTransformer with UpperCase with Trimmed`
  // Chain: Trimmed -> UpperCase -> BaseTransformer.
  // Trimmed.transform() calls super.transform(s.trim) -> UpperCase.transform(s.trim)
  // -> super.transform(s.trim.toUpperCase) -> BaseTransformer -> identity.
  // Result: "  hello world  " -> "hello world" -> "HELLO WORLD" -> "HELLO WORLD"
  // Same final result here, but order matters for non-commutative transformations.
  val transformer2 = new BaseTransformer with UpperCase with Trimmed
  val result2 = transformer2.transform("  hello world  ")
  println(s"  Reversed order:   '$result2'")  // => Reversed order:   'HELLO WORLD'

  println()

// ── 7. Givens and extensions ─────────────────────────────────────────
def givensAndExtensions(): Unit =
  println("=== 7. GIVENS & EXTENSIONS ===")  // => === 7. GIVENS & EXTENSIONS ===

  // The compiler resolves given Ordering[Int] and Ordering[String] automatically
  // based on the type arguments. This is implicit resolution — the compiler searches
  // the current scope, imports, and companion objects for matching given instances.
  println(s"  maxOf(3, 7) = ${maxOf(3, 7)}")  // => maxOf(3, 7) = 7
  println(s"  maxOf(\"apple\", \"banana\") = ${maxOf("apple", "banana")}")  // => maxOf("apple", "banana") = banana

  // Extension methods in action: called with dot syntax as if they were members.
  // The compiler rewrites `"hello world".wordCount` to the static extension method.
  println(s"  \"hello world\".wordCount = ${"hello world".wordCount}")  // => "hello world".wordCount = 2
  println(s"  \"racecar\".isPalindrome = ${"racecar".isPalindrome}")  // => "racecar".isPalindrome = true
  println(s"  \"hello\".isPalindrome = ${"hello".isPalindrome}")  // => "hello".isPalindrome = false
  println(s"  List(1,2,3).secondOption = ${List(1, 2, 3).secondOption}")  // => List(1,2,3).secondOption = Some(2)
  println(s"  List(1).secondOption = ${List(1).secondOption}")  // => List(1).secondOption = None

  // Context functions with `using`: `given defaultMultiplier: Int = 10` provides
  // a default value that the compiler passes implicitly to `scale()`. You can
  // override it explicitly with `(using 3)`. Be careful with given primitives —
  // `given Int` affects ALL functions expecting an implicit Int in this scope.
  given defaultMultiplier: Int = 10
  def scale(value: Int)(using multiplier: Int): Int = value * multiplier
  println(s"  scale(5) with given=10: ${scale(5)}")  // => scale(5) with given=10: 50
  println(s"  scale(5)(using 3): ${scale(5)(using 3)}")  // => scale(5)(using 3): 15

  // Implicit conversion (Scala 3 style): `given Conversion[String, Int]` enables
  // automatic conversion from String to Int. The compiler inserts the conversion
  // when a String is passed where Int is expected. Use with extreme caution —
  // implicit conversions can make code confusing and are discouraged in most cases.
  // Prefer extension methods for adding functionality to existing types.
  given Conversion[String, Int] = _.length
  def needsInt(n: Int): String = s"got int: $n"
  println(s"  Conversion String->Int: ${needsInt("hello")}")  // => Conversion String->Int: got int: 5

  println()

// ── 8. Concurrency ───────────────────────────────────────────────────
def concurrency(): Unit =
  println("=== 8. CONCURRENCY ===")  // => === 8. CONCURRENCY ===

  // Future[T]: Scala's built-in asynchronous computation. Starts executing immediately
  // on a thread from the ExecutionContext (imported globally above). Unlike Java's
  // CompletableFuture, Scala's Future is immutable — once completed, its value never
  // changes. Unlike Kotlin's coroutines (which are lazy/structured), Futures are eager
  // (start immediately) and unstructured (no parent-child cancellation).
  // For production, consider ZIO or Cats Effect for structured concurrency + resource safety.
  println("  -- Future --")  // => -- Future --
  val f1 = Future { Thread.sleep(10); 42 }
  val f2 = Future { Thread.sleep(10); 58 }

  // For-comprehension on Futures: desugars to flatMap/map. Looks sequential but f1 and
  // f2 were already started above — they run concurrently. If you put `Future { ... }`
  // inside the for-comprehension, they would run sequentially (because flatMap only
  // starts the next Future after the previous one completes).
  val composed = for
    a <- f1
    b <- f2
  yield a + b

  // Await.result(): blocks the current thread until the Future completes. Use only in
  // main methods, tests, or REPL — never in production async code (defeats the purpose).
  // The timeout parameter prevents indefinite blocking.
  val result = Await.result(composed, 5.seconds)
  println(s"  Future composition: 42 + 58 = $result")  // => Future composition: 42 + 58 = 100

  // recover: handles failures using a PartialFunction (pattern matching on the exception).
  // Like Try.recover(), this converts specific exceptions into successful values.
  // Compare with Java's CompletableFuture.exceptionally() and Kotlin's
  // coroutine try/catch or CoroutineExceptionHandler.
  val failing = Future[Int] { throw RuntimeException("oops") }
  val recovered = failing.recover { case _: RuntimeException => -1 }
  println(s"  Future recovered: ${Await.result(recovered, 5.seconds)}")  // => Future recovered: -1

  // Future.sequence: transforms List[Future[T]] into Future[List[T]]. All futures must
  // succeed; if any fails, the resulting Future fails. This is the applicative traverse
  // operation. Compare with Java's CompletableFuture.allOf() (which returns Void and
  // requires manual result extraction) — Scala's version is more ergonomic.
  val futures = List(
    Future { 10 },
    Future { 20 },
    Future { 30 }
  )
  val combined = Future.sequence(futures)
  println(s"  Future.sequence: ${Await.result(combined, 5.seconds)}")  // => Future.sequence: List(10, 20, 30)

  // Future.traverse: maps a collection through an async function and sequences the results.
  // Equivalent to `list.map(f).sequence` but more efficient. This is the canonical way
  // to run N async operations and collect all results.
  val traversed = Future.traverse(List(1, 2, 3))(n => Future { n * n })
  println(s"  Future.traverse: ${Await.result(traversed, 5.seconds)}")  // => Future.traverse: List(1, 4, 9)

  // Promise[T]: a writable, single-assignment container that produces a Future.
  // You create a Promise, hand out its .future to consumers, and later complete it
  // with success(value) or failure(exception). Once completed, it cannot be changed.
  // This is the producer side of the Future — useful for bridging callback-based APIs
  // into Future-based ones.
  println("  -- Promise --")  // => -- Promise --
  val promise = Promise[String]()
  val promiseFuture = promise.future

  Future {
    Thread.sleep(10)
    promise.success("Promise fulfilled!")
  }

  val promiseResult = Await.result(promiseFuture, 5.seconds)
  println(s"  Promise result: $promiseResult")  // => Promise result: Promise fulfilled!

  // onComplete: registers a callback that fires when the Future completes. The callback
  // receives a Try[T] — either Success(value) or Failure(exception). Callbacks execute
  // on the ExecutionContext's thread pool, NOT the calling thread. Use for fire-and-forget
  // side effects; prefer map/flatMap/recover for composable transformations.
  val callbackFuture = Future { 42 * 2 }
  callbackFuture.onComplete {
    case Success(v) => println(s"  Callback success: $v")  // => Callback success: 84
    case Failure(e) => println(s"  Callback failure: ${e.getMessage}")
  }
  Thread.sleep(50) // give callback time to print

  println()
  println("=== DONE ===")  // => === DONE ===
