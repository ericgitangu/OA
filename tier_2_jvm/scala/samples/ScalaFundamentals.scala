import scala.concurrent.{Future, Promise, Await}
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.duration.*
import scala.util.{Try, Success, Failure}

/**
 * Scala 3 Fundamentals — single runnable file.
 * Compile & run:  scala ScalaFundamentals.scala
 * Or:             scalac ScalaFundamentals.scala && scala ScalaFundamentals
 */

// ── Sealed traits & case classes (ADTs) ──────────────────────────────
sealed trait Shape:
  def area: Double

case class Circle(radius: Double) extends Shape:
  def area: Double = Math.PI * radius * radius

case class Rectangle(width: Double, height: Double) extends Shape:
  def area: Double = width * height

case class Triangle(base: Double, height: Double) extends Shape:
  def area: Double = 0.5 * base * height

// ── Enum (Scala 3) ───────────────────────────────────────────────────
enum Direction(val dx: Int, val dy: Int):
  case North extends Direction(0, 1)
  case South extends Direction(0, -1)
  case East  extends Direction(1, 0)
  case West  extends Direction(-1, 0)

  def opposite: Direction = this match
    case North => South
    case South => North
    case East  => West
    case West  => East

// ── Type aliases ─────────────────────────────────────────────────────
type Matrix[A] = List[List[A]]
type Predicate[A] = A => Boolean

// ── Traits: composition and self-types ───────────────────────────────
trait Describable:
  def describe: String
  def tag: String = s"[$describe]"

trait Loggable:
  self: Describable =>  // self-type: requires Describable
  def log(): Unit = println(s"    LOG: $describe")

class NamedItem(val name: String, val value: Int) extends Describable with Loggable:
  def describe: String = s"$name=$value"

// ── Stackable trait modifications ────────────────────────────────────
trait Transformer:
  def transform(s: String): String

trait UpperCase extends Transformer:
  abstract override def transform(s: String): String = super.transform(s.toUpperCase)

trait Trimmed extends Transformer:
  abstract override def transform(s: String): String = super.transform(s.trim)

class BaseTransformer extends Transformer:
  def transform(s: String): String = s

// ── Variance examples ────────────────────────────────────────────────
sealed trait Animal:
  def name: String

case class Dog(name: String) extends Animal
case class Cat(name: String) extends Animal

// Covariant container (+A)
class Box[+A](val content: A):
  override def toString: String = s"Box($content)"

// Contravariant printer (-A)
trait Printer[-A]:
  def print(a: A): String

// ── Given/Using (Scala 3 implicits) ──────────────────────────────────
trait Ordering[A]:
  def compare(a: A, b: A): Int

given intOrdering: Ordering[Int] with
  def compare(a: Int, b: Int): Int = a - b

given stringOrdering: Ordering[String] with
  def compare(a: String, b: String): Int = a.compareTo(b)

def maxOf[A](a: A, b: A)(using ord: Ordering[A]): A =
  if ord.compare(a, b) >= 0 then a else b

// ── Extension methods (Scala 3) ──────────────────────────────────────
extension (s: String)
  def wordCount: Int = s.trim.split("\\s+").length
  def isPalindrome: Boolean = s == s.reverse

extension [A](list: List[A])
  def secondOption: Option[A] = if list.length >= 2 then Some(list(1)) else None

// ── Extractors ───────────────────────────────────────────────────────
object Even:
  def unapply(n: Int): Option[Int] = if n % 2 == 0 then Some(n) else None

object Email:
  def unapply(s: String): Option[(String, String)] =
    val parts = s.split("@")
    if parts.length == 2 then Some((parts(0), parts(1))) else None

// ═════════════════════════════════════════════════════════════════════
// MAIN
// ═════════════════════════════════════════════════════════════════════
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
  println("=== 1. BASICS ===")

  // val (immutable) and var (mutable)
  val name = "Scala"
  var counter = 0
  counter += 1
  println(s"  val name=$name, var counter=$counter")

  // Type inference
  val x: Int = 42
  val pi = 3.14159       // inferred as Double
  val flag = true        // inferred as Boolean
  println(s"  x=$x, pi=$pi, flag=$flag")

  // String interpolation
  println(s"  s-interpolation: $name has ${name.length} chars")
  println(f"  f-interpolation: pi=$pi%.3f")
  println(raw"  raw: no escape \n here")

  // Multiline strings
  val text = """
    |Line 1: stripMargin
    |Line 2: trims leading whitespace
    |Line 3: using pipe prefix
    """.stripMargin.trim
  println(s"  Multiline:\n$text")

  // Tuples
  val pair = (42, "hello")
  val triple = (1, "two", 3.0)
  println(s"  Tuple: $pair, first=${pair._1}, second=${pair._2}")
  println(s"  Triple: $triple")

  // Tuple destructuring
  val (num, str) = pair
  println(s"  Destructured: num=$num, str=$str")

  // Option type
  val some: Option[String] = Some("present")
  val none: Option[String] = None
  println(s"  Option: some=${some.getOrElse("N/A")}, none=${none.getOrElse("N/A")}")
  println(s"  Option map: ${some.map(_.toUpperCase)}")

  println()

// ── 2. Collections ───────────────────────────────────────────────────
def collections(): Unit =
  println("=== 2. COLLECTIONS ===")

  // Immutable collections (default)
  val names = List("Alice", "Bob", "Charlie", "Diana")
  val scores = Map("Alice" -> 95, "Bob" -> 87, "Charlie" -> 92)
  val tags = Set("scala", "jvm", "fp")
  println(s"  List: $names")
  println(s"  Map: $scores")
  println(s"  Set: $tags")

  // Vector (efficient random access and updates)
  val vec = Vector(1, 2, 3, 4, 5)
  val updated = vec.updated(2, 99)
  println(s"  Vector: $vec, updated(2,99): $updated")

  // Collection operations
  val numbers = List(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

  val evenSquares = numbers.filter(_ % 2 == 0).map(n => n * n)
  println(s"  Even squares: $evenSquares")

  val sum = numbers.reduce(_ + _)
  val product = numbers.foldLeft(1)(_ * _)
  println(s"  Reduce sum: $sum, foldLeft product: $product")

  val grouped = names.groupBy(_.head)
  println(s"  GroupBy first char: $grouped")

  val flat = List(List(1, 2), List(3, 4), List(5)).flatMap(identity)
  println(s"  FlatMap: $flat")

  // partition
  val (evens, odds) = numbers.partition(_ % 2 == 0)
  println(s"  Partition: evens=$evens, odds=$odds")

  // zip
  val keys = List("a", "b", "c")
  val values = List(1, 2, 3)
  val zipped = keys.zip(values)
  println(s"  Zip: $zipped")
  println(s"  ToMap: ${zipped.toMap}")

  // collect with partial function
  val mixed: List[Any] = List(1, "hello", 2, "world", 3)
  val strings = mixed.collect { case s: String => s.toUpperCase }
  println(s"  Collect strings: $strings")

  // LazyList (lazy evaluation)
  val fibs: LazyList[Long] = 0L #:: 1L #:: fibs.zip(fibs.tail).map(_ + _)
  println(s"  First 12 Fibonacci: ${fibs.take(12).toList}")

  println()

// ── 3. Pattern matching ──────────────────────────────────────────────
def patternMatching(): Unit =
  println("=== 3. PATTERN MATCHING ===")

  // Case class matching
  val shapes: List[Shape] = List(Circle(5), Rectangle(3, 4), Triangle(6, 3))
  for shape <- shapes do
    val desc = shape match
      case Circle(r)       => s"Circle r=$r"
      case Rectangle(w, h) => s"Rect ${w}x$h"
      case Triangle(b, h)  => s"Triangle b=$b h=$h"
    println(s"  $desc -> area=${shape.area}")

  // Guards
  val numbers = List(-3, 0, 5, 12, 100)
  for n <- numbers do
    val label = n match
      case x if x < 0    => "negative"
      case 0              => "zero"
      case x if x <= 10   => "small positive"
      case x if x <= 50   => "medium positive"
      case _              => "large positive"
    println(s"  $n -> $label")

  // Custom extractors
  println("  -- Extractors --")
  val nums = List(1, 2, 3, 4, 5, 6)
  for n <- nums do
    n match
      case Even(e) => println(s"    $n is Even($e)")
      case odd     => println(s"    $odd is odd")

  "user@example.com" match
    case Email(user, domain) => println(s"  Email: user=$user, domain=$domain")
    case other               => println(s"  Not an email: $other")

  // Tuple and list patterns
  val point = (3, 4)
  point match
    case (0, 0)    => println("  origin")
    case (x, 0)    => println(s"  on x-axis at $x")
    case (0, y)    => println(s"  on y-axis at $y")
    case (x, y)    => println(s"  point at ($x, $y)")

  val items = List(1, 2, 3, 4, 5)
  items match
    case head :: second :: tail => println(s"  List head=$head, second=$second, tail=$tail")
    case _                     => println("  too short")

  // Type matching
  val any: Any = List(1, 2, 3)
  any match
    case s: String    => println(s"  String: $s")
    case i: Int       => println(s"  Int: $i")
    case l: List[?]   => println(s"  List of size ${l.size}: $l")
    case _            => println("  unknown type")

  println()

// ── 4. Functional programming ────────────────────────────────────────
def functionalProgramming(): Unit =
  println("=== 4. FUNCTIONAL PROGRAMMING ===")

  // Higher-order functions
  def applyTwice[A](f: A => A, x: A): A = f(f(x))
  println(s"  applyTwice(_ + 1, 5) = ${applyTwice((_: Int) + 1, 5)}")
  println(s"  applyTwice(_.toUpperCase, \"hi\") = ${applyTwice((_: String).toUpperCase, "hi")}")

  // Currying
  def add(a: Int)(b: Int): Int = a + b
  val add5 = add(5)
  println(s"  Curried: add(5)(3) = ${add(5)(3)}")
  println(s"  Partial: add5(3) = ${add5(3)}")

  // Uncurried version -> curried
  val multiply = (a: Int, b: Int) => a * b
  val curriedMult = multiply.curried
  println(s"  .curried: ${curriedMult(3)(4)}")

  // Partial functions
  val divide: PartialFunction[Int, Double] = {
    case n if n != 0 => 1.0 / n
  }
  println(s"  PartialFunction defined at 0? ${divide.isDefinedAt(0)}")
  println(s"  PartialFunction(5) = ${divide(5)}")

  val safeDivide = divide.lift  // converts to Int => Option[Double]
  println(s"  Lifted(0) = ${safeDivide(0)}, Lifted(4) = ${safeDivide(4)}")

  // For-comprehensions (syntactic sugar for flatMap/map/filter)
  val pairs = for
    x <- List(1, 2, 3)
    y <- List('a', 'b')
  yield (x, y)
  println(s"  For-comprehension: $pairs")

  // For-comprehension with Option
  def findUser(id: Int): Option[String] = if id == 1 then Some("Alice") else None
  def findAge(name: String): Option[Int] = if name == "Alice" then Some(30) else None

  val result = for
    name <- findUser(1)
    age  <- findAge(name)
  yield s"$name is $age"
  println(s"  Option for-comp: $result")
  println(s"  Option for-comp (miss): ${for { n <- findUser(2); a <- findAge(n) } yield s"$n is $a"}")

  // Try
  val parsed = Try("42".toInt)
  val failed = Try("abc".toInt)
  println(s"  Try success: $parsed")
  println(s"  Try failure: ${failed.toOption}")

  val recovered = failed.recover { case _: NumberFormatException => -1 }
  println(s"  Try recovered: $recovered")

  println()

// ── 5. Types and variance ────────────────────────────────────────────
def typesAndVariance(): Unit =
  println("=== 5. TYPES & VARIANCE ===")

  // Type aliases
  val matrix: Matrix[Int] = List(List(1, 2), List(3, 4))
  val isPositive: Predicate[Int] = _ > 0
  println(s"  Matrix: $matrix")
  println(s"  Predicate(5): ${isPositive(5)}, Predicate(-1): ${isPositive(-1)}")

  // Covariance (+A): Box[Dog] is subtype of Box[Animal]
  val dogBox: Box[Dog] = Box(Dog("Rex"))
  val animalBox: Box[Animal] = dogBox  // works because Box is covariant
  println(s"  Covariant: $animalBox")

  // Contravariance (-A): Printer[Animal] is subtype of Printer[Dog]
  val animalPrinter: Printer[Animal] = new Printer[Animal]:
    def print(a: Animal): String = s"Animal(${a.name})"

  val dogPrinter: Printer[Dog] = animalPrinter  // works because Printer is contravariant
  println(s"  Contravariant: ${dogPrinter.print(Dog("Buddy"))}")

  // Type bounds
  def findMax[A](list: List[A])(using ord: Ordering[A]): A =
    list.reduce((a, b) => if ord.compare(a, b) >= 0 then a else b)

  println(s"  findMax(List(3,1,4,1,5)): ${findMax(List(3, 1, 4, 1, 5))}")
  println(s"  findMax(List(\"c\",\"a\",\"b\")): ${findMax(List("c", "a", "b"))}")

  // ADT example: Expression tree
  enum Expr:
    case Num(value: Double)
    case Add(left: Expr, right: Expr)
    case Mul(left: Expr, right: Expr)

  def eval(expr: Expr): Double = expr match
    case Expr.Num(v)    => v
    case Expr.Add(l, r) => eval(l) + eval(r)
    case Expr.Mul(l, r) => eval(l) * eval(r)

  val expression = Expr.Add(Expr.Num(3), Expr.Mul(Expr.Num(4), Expr.Num(5)))
  println(s"  ADT eval(3 + 4*5) = ${eval(expression)}")

  println()

// ── 6. Traits and composition ────────────────────────────────────────
def traitsAndComposition(): Unit =
  println("=== 6. TRAITS & COMPOSITION ===")

  // Basic trait composition
  val item = NamedItem("score", 100)
  println(s"  Describable: ${item.describe()}")
  println(s"  Tag: ${item.tag}")

  // Self-type requires Describable
  item.log()

  // Stackable modifications (linearization)
  val transformer = new BaseTransformer with Trimmed with UpperCase
  val result = transformer.transform("  hello world  ")
  println(s"  Stackable traits: '$result'")

  // Mixin order matters — rightmost wraps outermost
  val transformer2 = new BaseTransformer with UpperCase with Trimmed
  val result2 = transformer2.transform("  hello world  ")
  println(s"  Reversed order:   '$result2'")

  println()

// ── 7. Givens and extensions ─────────────────────────────────────────
def givensAndExtensions(): Unit =
  println("=== 7. GIVENS & EXTENSIONS ===")

  // Using given instances
  println(s"  maxOf(3, 7) = ${maxOf(3, 7)}")
  println(s"  maxOf(\"apple\", \"banana\") = ${maxOf("apple", "banana")}")

  // Extension methods
  println(s"  \"hello world\".wordCount = ${"hello world".wordCount}")
  println(s"  \"racecar\".isPalindrome = ${"racecar".isPalindrome}")
  println(s"  \"hello\".isPalindrome = ${"hello".isPalindrome}")
  println(s"  List(1,2,3).secondOption = ${List(1, 2, 3).secondOption}")
  println(s"  List(1).secondOption = ${List(1).secondOption}")

  // Context functions (using)
  given defaultMultiplier: Int = 10
  def scale(value: Int)(using multiplier: Int): Int = value * multiplier
  println(s"  scale(5) with given=10: ${scale(5)}")
  println(s"  scale(5)(using 3): ${scale(5)(using 3)}")

  // Implicit conversion (Scala 3 style)
  given Conversion[String, Int] = _.length
  def needsInt(n: Int): String = s"got int: $n"
  println(s"  Conversion String->Int: ${needsInt("hello")}")

  println()

// ── 8. Concurrency ───────────────────────────────────────────────────
def concurrency(): Unit =
  println("=== 8. CONCURRENCY ===")

  // Future — asynchronous computation
  println("  -- Future --")
  val f1 = Future { Thread.sleep(10); 42 }
  val f2 = Future { Thread.sleep(10); 58 }

  // map / flatMap
  val composed = for
    a <- f1
    b <- f2
  yield a + b

  val result = Await.result(composed, 5.seconds)
  println(s"  Future composition: 42 + 58 = $result")

  // Future with recovery
  val failing = Future[Int] { throw RuntimeException("oops") }
  val recovered = failing.recover { case _: RuntimeException => -1 }
  println(s"  Future recovered: ${Await.result(recovered, 5.seconds)}")

  // sequence — List[Future] => Future[List]
  val futures = List(
    Future { 10 },
    Future { 20 },
    Future { 30 }
  )
  val combined = Future.sequence(futures)
  println(s"  Future.sequence: ${Await.result(combined, 5.seconds)}")

  // traverse
  val traversed = Future.traverse(List(1, 2, 3))(n => Future { n * n })
  println(s"  Future.traverse: ${Await.result(traversed, 5.seconds)}")

  // Promise — manually completable Future
  println("  -- Promise --")
  val promise = Promise[String]()
  val promiseFuture = promise.future

  Future {
    Thread.sleep(10)
    promise.success("Promise fulfilled!")
  }

  val promiseResult = Await.result(promiseFuture, 5.seconds)
  println(s"  Promise result: $promiseResult")

  // onComplete callback
  val callbackFuture = Future { 42 * 2 }
  callbackFuture.onComplete {
    case Success(v) => println(s"  Callback success: $v")
    case Failure(e) => println(s"  Callback failure: ${e.getMessage}")
  }
  Thread.sleep(50) // give callback time to print

  println()
  println("=== DONE ===")
