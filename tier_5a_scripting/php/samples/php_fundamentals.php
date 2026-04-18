<?php
/**
 * PHP Fundamentals: Beginner to Advanced — Standard Library Only.
 *
 * A dense, runnable syntax reference covering core PHP concepts.
 * Run: php php_fundamentals.php
 * Requires: PHP 8.1+ (for enums, fibers, readonly, intersection types)
 *
 * PHP has evolved dramatically since PHP 7. Each major release added features that
 * transformed it from a loosely-typed scripting language into a modern, type-safe language:
 *   PHP 7.4: Arrow functions, typed properties, null coalescing assignment
 *   PHP 8.0: Named args, match expressions, union types, attributes, nullsafe operator
 *   PHP 8.1: Enums, fibers, readonly properties, intersection types, first-class callables
 *   PHP 8.2: Readonly classes, DNF types, standalone true/false/null types
 */

function section(string $title): void {
    echo "\n" . str_repeat('=', 60) . "\n  $title\n" . str_repeat('=', 60) . "\n";
}

// ============================================================
//  1. BASICS
// ============================================================
function basics(): void {
    section("1. BASICS — Types, Strings, Match, Named Args, Null Coalescing");

    // PHP is dynamically typed but supports optional type declarations since PHP 7.
    // Unlike JS, PHP distinguishes int from float and has strict_types mode.
    // With `declare(strict_types=1)`, PHP won't silently coerce "42" to 42.
    $int = 42;
    $float = 3.14;
    $str = "PHP";
    $bool = true;
    $null = null;
    echo "int=$int  float=$float  str=$str  bool=" . ($bool ? 'true' : 'false') . "  null=" . var_export($null, true) . "\n";  // => int=42  float=3.14  str=PHP  bool=true  null=NULL
    echo "Type checking: is_int=" . var_export(is_int($int), true) . "  is_string=" . var_export(is_string($str), true) . "\n";  // => Type checking: is_int=true  is_string=true

    // Double-quoted strings support interpolation with $var or {$expr} syntax.
    // Single-quoted strings are literal — no interpolation, slightly faster parsing.
    $name = "World";
    echo "Hello, $name!\n";  // => Hello, World!
    echo "Expression: {$name} has " . strlen($name) . " chars\n";  // => Expression: World has 5 chars
    $heredoc = <<<EOT
    Heredoc with $name interpolation
    and multiple lines.
    EOT;
    echo "Heredoc: " . trim($heredoc) . "\n";  // => Heredoc: Heredoc with World interpolation\n    and multiple lines.

    // match (PHP 8.0) replaces verbose switch statements. Key differences from switch:
    // 1. Uses strict (===) comparison, not loose (==) — no type juggling
    // 2. Returns a value (it's an expression, not a statement)
    // 3. No fall-through — each arm is independent, no break needed
    // match(true) enables conditional matching, similar to Rust's match or Elixir's cond.
    $status = 200;
    $text = match(true) {
        $status >= 200 && $status < 300 => 'Success',
        $status >= 400 && $status < 500 => 'Client Error',
        $status >= 500 => 'Server Error',
        default => 'Unknown',
    };
    echo "Match: status $status => $text\n";  // => Match: status 200 => Success

    // Named arguments (PHP 8.0) let you pass args by name, in any order.
    // This eliminates the need for boolean flags or options arrays — a common PHP pattern.
    // They also serve as self-documenting code at the call site.
    function createUser(string $name, int $age, string $role = 'user'): string {
        return "$name (age: $age, role: $role)";
    }
    echo "Named args: " . createUser(age: 25, name: 'Alice', role: 'admin') . "\n";  // => Named args: Alice (age: 25, role: admin)

    // Null coalescing (??) returns the left operand if it's not null, otherwise the right.
    // Unlike isset(), it works inline as an expression. This was PHP 7.0.
    // ??= (PHP 7.4) is the null coalescing assignment — assign only if currently null.
    $config = ['db' => ['host' => 'localhost']];
    echo "Null coalesce: " . ($config['db']['port'] ?? 3306) . "\n";  // => Null coalesce: 3306
    $value = null;
    $value ??= 'default';
    echo "Null coalesce assign: $value\n";  // => Null coalesce assign: default

    // Nullsafe operator ?-> (PHP 8.0) short-circuits the entire chain if any link is null.
    // Without it, you'd need nested if-checks or the ?? operator at each step.
    // Note: nullsafe requires object method/property access — it doesn't work with functions.
    $user = new class {
        public ?object $profile = null;
    };
    $user->profile = new class { public function getDisplayName(): string { return "Alice"; } };
    echo "Nullsafe: " . ($user->profile?->getDisplayName() ?? 'no profile') . "\n";  // => Nullsafe: Alice
    $user->profile = null;
    echo "Nullsafe (null): " . ($user->profile?->getDisplayName() ?? 'no profile') . "\n";  // => Nullsafe (null): no profile
}

// ============================================================
//  2. COLLECTIONS
// ============================================================
function collections(): void {
    section("2. COLLECTIONS — Arrays, Array Functions, SplFixedArray");

    // PHP arrays are actually ordered hash maps (dictionaries) — they support both
    // integer and string keys in the same structure. This is unique among languages.
    // The tradeoff: they use more memory than true arrays (each element stores key + value + hash).
    $indexed = [10, 20, 30, 40, 50];
    $assoc = ['name' => 'PHP', 'version' => 8.2, 'typed' => true];
    echo "Indexed: " . implode(', ', $indexed) . "\n";  // => Indexed: 10, 20, 30, 40, 50
    echo "Assoc: " . json_encode($assoc) . "\n";  // => Assoc: {"name":"PHP","version":8.2,"typed":true}

    // Spread operator (...) unpacks arrays (PHP 7.4 for numeric, 8.1 for string keys).
    $more = [0, ...$indexed, 60];
    echo "Spread: " . implode(', ', $more) . "\n";  // => Spread: 0, 10, 20, 30, 40, 50, 60

    // Array destructuring uses [] on the left side of assignment.
    // For associative arrays, you use key => $var syntax to pick specific keys.
    [$first, $second] = $indexed;
    ['name' => $name, 'version' => $version] = $assoc;
    echo "Destructure: first=$first, name=$name, version=$version\n";  // => Destructure: first=10, name=PHP, version=8.2

    // PHP's array functions are prefix-based (array_*) because PHP predates namespaces.
    // They take callbacks as the last argument, unlike JS where the callback comes first.
    // fn() => is the arrow function syntax (PHP 7.4) — automatically captures outer scope.
    $nums = range(1, 10);
    echo "array_map:    " . implode(', ', array_map(fn($n) => $n * 2, $nums)) . "\n";  // => array_map:    2, 4, 6, 8, 10, 12, 14, 16, 18, 20
    echo "array_filter: " . implode(', ', array_filter($nums, fn($n) => $n % 2 === 0)) . "\n";  // => array_filter: 2, 4, 6, 8, 10

    // array_reduce folds the array into a single value. The 3rd arg is the initial accumulator.
    echo "array_reduce: " . array_reduce($nums, fn($carry, $n) => $carry + $n, 0) . "\n";  // => array_reduce: 55
    echo "array_slice:  " . implode(', ', array_slice($nums, 2, 3)) . "\n";  // => array_slice:  3, 4, 5
    echo "array_chunk:  " . json_encode(array_chunk($nums, 3)) . "\n";  // => array_chunk:  [[1,2,3],[4,5,6],[7,8,9],[10]]
    echo "array_combine: " . json_encode(array_combine(['a', 'b', 'c'], [1, 2, 3])) . "\n";  // => array_combine: {"a":1,"b":2,"c":3}
    echo "array_unique: " . implode(', ', array_unique([1, 1, 2, 3, 3])) . "\n";  // => array_unique: 1, 2, 3

    // <=> is the spaceship operator (PHP 7.0) — returns -1, 0, or 1.
    // Used with usort for custom comparison, same concept as Ruby's <=>.
    $words = ['banana', 'apple', 'cherry'];
    usort($words, fn($a, $b) => strlen($a) <=> strlen($b));
    echo "usort by length: " . implode(', ', $words) . "\n";  // => usort by length: apple, banana, cherry

    // array_column extracts a single column from a 2D array — like SQL SELECT or Lodash _.pluck.
    $people = [
        ['name' => 'Alice', 'age' => 30],
        ['name' => 'Bob', 'age' => 25],
    ];
    echo "array_column: " . implode(', ', array_column($people, 'name')) . "\n";  // => array_column: Alice, Bob

    // SplFixedArray is a true fixed-size array (not a hash map) — uses ~60% less memory
    // than regular arrays for large datasets. The tradeoff: fixed size, integer keys only.
    $fixed = new SplFixedArray(5);
    for ($i = 0; $i < 5; $i++) { $fixed[$i] = $i * 10; }
    echo "SplFixedArray: ";
    foreach ($fixed as $v) { echo "$v "; }
    echo "(size: {$fixed->getSize()})\n";  // => SplFixedArray: 0 10 20 30 40 (size: 5)
}

// ============================================================
//  3. OOP
// ============================================================
function oop_demo(): void {
    section("3. OOP — Classes, Interfaces, Traits, Enums, Readonly");

    // Constructor promotion (PHP 8.0) combines parameter declaration, property declaration,
    // and assignment into one line. readonly (PHP 8.1) makes the property write-once —
    // it can only be set in the constructor. This eliminates boilerplate getters and
    // immutable value objects that previously needed 3x the code.
    class Point {
        public function __construct(
            public readonly float $x,
            public readonly float $y,
        ) {}

        public function distanceTo(Point $other): float {
            return sqrt(($this->x - $other->x) ** 2 + ($this->y - $other->y) ** 2);
        }

        // __toString is a magic method — PHP calls it when an object is used in string context.
        // PHP has ~20 magic methods (__get, __set, __call, etc.) for operator overloading.
        public function __toString(): string {
            return "Point({$this->x}, {$this->y})";
        }
    }

    $p1 = new Point(0, 0);
    $p2 = new Point(3, 4);
    echo "Point: $p1  Distance: {$p1->distanceTo($p2)}\n";  // => Point: Point(0, 0)  Distance: 5

    // Interfaces define contracts — method signatures without implementations.
    // PHP supports multiple interface implementation (unlike single class inheritance).
    interface Describable {
        public function describe(): string;
    }

    // Traits solve PHP's lack of multiple inheritance. They're horizontal code reuse —
    // the compiler copies trait methods into the using class at compile time.
    // Unlike interfaces, traits provide implementation. Unlike inheritance, you can use multiple.
    // Conflict resolution: if two traits define the same method, you must explicitly resolve it
    // with `insteadof` and `as` operators.
    trait HasId {
        private static int $counter = 0;
        public readonly int $id;

        public function initId(): void {
            $this->id = ++self::$counter;
        }
    }

    class User implements Describable {
        use HasId;

        public function __construct(
            public readonly string $name,
            public readonly string $role = 'user',
        ) {
            $this->initId();
        }

        public function describe(): string {
            return "User #{$this->id}: {$this->name} ({$this->role})";
        }
    }

    $u = new User('Alice', 'admin');
    echo $u->describe() . "\n";  // => User #1: Alice (admin)

    // Enums (PHP 8.1) are first-class types — they're not just constants like in older PHP.
    // Backed enums (: string or : int) have a stored value; pure enums don't.
    // Enums can implement interfaces and use traits, and they can have methods.
    // They're singletons — Color::Red === Color::Red is always true.
    enum Color: string {
        case Red = 'red';
        case Green = 'green';
        case Blue = 'blue';

        public function hex(): string {
            return match($this) {
                self::Red => '#FF0000',
                self::Green => '#00FF00',
                self::Blue => '#0000FF',
            };
        }
    }

    $c = Color::Red;
    echo "Enum: {$c->name} = {$c->value}, hex = {$c->hex()}\n";  // => Enum: Red = red, hex = #FF0000

    // from() converts a backing value to an enum case, throwing ValueError if invalid.
    // tryFrom() returns null instead — use it when the input is untrusted.
    echo "From string: " . Color::from('blue')->name . "\n";  // => From string: Blue

    // Abstract classes provide partial implementations that subclasses must complete.
    // Use abstract when you want to share code; use interfaces when you want to define contracts.
    abstract class Shape {
        abstract public function area(): float;
    }

    class Circle extends Shape {
        public function __construct(private readonly float $radius) {}
        public function area(): float { return M_PI * $this->radius ** 2; }
    }

    echo "Circle area: " . round((new Circle(5))->area(), 2) . "\n";  // => Circle area: 78.54

    // Anonymous classes (PHP 7.0) are useful for one-off implementations — testing, adapters,
    // or anywhere you need a quick interface implementation without polluting the namespace.
    $logger = new class {
        public function log(string $msg): void { echo "  [LOG] $msg\n"; }
    };
    $logger->log("Anonymous class works!");  // => [LOG] Anonymous class works!
}

// ============================================================
//  4. FUNCTIONS
// ============================================================
function functions_demo(): void {
    section("4. FUNCTIONS — Closures, Arrow Fns, First-Class Callables");

    // Closures in PHP require explicit `use ($var)` to capture outer variables.
    // This is intentional — PHP wants you to be explicit about what state a closure holds.
    // Unlike JS/Ruby where closures capture everything automatically, PHP's approach
    // prevents accidental captures and makes the closure's dependencies visible.
    // `use` captures by value by default; use `use (&$var)` for reference capture.
    $multiplier = function(int $factor): Closure {
        return function(int $x) use ($factor): int {
            return $x * $factor;
        };
    };
    $double = $multiplier(2);
    $triple = $multiplier(3);
    echo "Closure: double(5)={$double(5)}  triple(5)={$triple(5)}\n";  // => Closure: double(5)=10  triple(5)=15

    // Arrow functions (PHP 7.4) are short closures that auto-capture by value.
    // They can only be a single expression — no statements, no multi-line bodies.
    // This is fn($x) => expr, NOT function($x) use(...) { return expr; }.
    $nums = [1, 2, 3, 4, 5];
    $squared = array_map(fn($n) => $n ** 2, $nums);
    echo "Arrow fn: " . implode(', ', $squared) . "\n";  // => Arrow fn: 1, 4, 9, 16, 25

    // First-class callable syntax (PHP 8.1): strlen(...) creates a Closure from any callable.
    // Before 8.1, you had to wrap callables in Closure::fromCallable() or pass string names.
    // The ... is a placeholder that says "I'll fill in the arguments later."
    $strlen = strlen(...);
    echo "First-class callable: strlen('hello') = {$strlen('hello')}\n";  // => First-class callable: strlen('hello') = 5
    $words = ['hi', 'hello', 'hey'];
    $lengths = array_map(strlen(...), $words);
    echo "Mapped lengths: " . implode(', ', $lengths) . "\n";  // => Mapped lengths: 2, 5, 3

    // Variadic params (...$nums) collect remaining arguments into an array.
    // The splat operator (...$args) does the reverse — spreads an array into arguments.
    $sum = function(int ...$nums): int { return array_sum($nums); };
    echo "Variadic sum: {$sum(1, 2, 3, 4, 5)}\n";  // => Variadic sum: 15
    $args = [10, 20, 30];
    echo "Splat sum: {$sum(...$args)}\n";  // => Splat sum: 60
}

// ============================================================
//  5. TYPE SYSTEM
// ============================================================
function type_system_demo(): void {
    section("5. TYPE SYSTEM — Union, Intersection, Readonly Classes");

    // Union types (PHP 8.0) let a parameter accept multiple types.
    // This replaces the old @param int|string phpdoc approach with runtime enforcement.
    // PHP validates the type at call time and throws TypeError on mismatch.
    function processInput(int|string $input): string {
        return match(true) {
            is_int($input) => "Integer: $input",
            is_string($input) => "String: '$input'",
        };
    }
    echo processInput(42) . "\n";  // => Integer: 42
    echo processInput("hello") . "\n";  // => String: 'hello'

    // Intersection types (PHP 8.1) require a value to satisfy ALL listed types.
    // This is like TypeScript's `&` — the value must implement every interface.
    // Use case: accepting only objects that implement multiple interfaces.
    interface Countable2 { public function count(): int; }
    interface Serializable2 { public function serialize(): string; }

    function processCollection(Countable2&Serializable2 $item): string {
        return "Count: {$item->count()}, Serialized: {$item->serialize()}";
    }

    $coll = new class implements Countable2, Serializable2 {
        public function count(): int { return 5; }
        public function serialize(): string { return json_encode(['items' => 5]); }
    };
    echo "Intersection type: " . processCollection($coll) . "\n";  // => Intersection type: Count: 5, Serialized: {"items":5}

    // Typed properties (PHP 7.4) enforce types on class properties at write time.
    // Nullable types (?string) allow null as a valid value alongside the declared type.
    class Config {
        public string $host = 'localhost';
        public int $port = 3306;
        public ?string $password = null;
    }

    $cfg = new Config();
    echo "Typed props: host={$cfg->host} port={$cfg->port} password=" . var_export($cfg->password, true) . "\n";  // => Typed props: host=localhost port=3306 password=NULL
}

// ============================================================
//  6. FIBERS
// ============================================================
function fibers_demo(): void {
    section("6. FIBERS — Cooperative Concurrency (PHP 8.1)");

    // Fibers (PHP 8.1) are lightweight coroutines for cooperative multitasking.
    // Unlike threads, fibers don't run in parallel — they voluntarily suspend (Fiber::suspend)
    // and resume on the SAME thread. The calling code decides when to resume them.
    //
    // Why fibers instead of threads? PHP's architecture is share-nothing, request-scoped.
    // True threads would require locks, mutexes, and shared memory — alien to PHP's model.
    // Fibers enable async I/O frameworks (Revolt, AMPHP) to interleave operations without
    // the complexity of threads or the callback hell of promises.
    $fiber = new Fiber(function(): string {
        $value = Fiber::suspend('first suspend');
        echo "  Fiber resumed with: $value\n";  // => Fiber resumed with: hello from main
        Fiber::suspend('second suspend');
        return 'fiber complete';
    });

    // start() begins execution until the first Fiber::suspend(), returning the suspended value.
    $result1 = $fiber->start();
    echo "After start: $result1\n";  // => After start: first suspend

    // resume() passes a value INTO the fiber (returned by Fiber::suspend inside the fiber).
    $result2 = $fiber->resume('hello from main');
    echo "After resume: $result2\n";  // => After resume: second suspend

    // After the fiber's function returns, getReturn() retrieves the return value.
    $fiber->resume();
    echo "Return value: {$fiber->getReturn()}\n";  // => Return value: fiber complete

    // Fibers can model generators, but generators are simpler for yielding sequences.
    // Fibers shine when you need bidirectional communication and full call stack preservation.
    function rangeGenerator(int $start, int $end): Fiber {
        return new Fiber(function() use ($start, $end): void {
            for ($i = $start; $i <= $end; $i++) {
                Fiber::suspend($i);
            }
        });
    }

    $gen = rangeGenerator(1, 5);
    $values = [];
    $val = $gen->start();
    while (!$gen->isTerminated()) {
        $values[] = $val;
        $val = $gen->resume();
    }
    echo "Fiber generator: " . implode(', ', $values) . "\n";  // => Fiber generator: 1, 2, 3, 4, 5
}

// ============================================================
//  7. ADVANCED
// ============================================================
function advanced_demo(): void {
    section("7. ADVANCED — Generators, Attributes, Reflection, WeakMap");

    // Generators are memory-efficient iterators. Instead of building an entire array in memory,
    // yield produces one value at a time. A generator function returns a Generator object
    // that implements the Iterator interface. Internally, PHP suspends and resumes the function
    // at each yield — similar to fibers but specialized for sequential iteration.
    function fibonacci(): Generator {
        [$a, $b] = [0, 1];
        while (true) {
            yield $a;
            [$a, $b] = [$b, $a + $b];
        }
    }

    $fibs = [];
    foreach (fibonacci() as $i => $fib) {
        if ($i >= 10) break;
        $fibs[] = $fib;
    }
    echo "Fibonacci: " . implode(', ', $fibs) . "\n";  // => Fibonacci: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34

    // Generator with send() — you can push values INTO a generator via send().
    // The sent value becomes the return value of the yield expression inside the generator.
    // This enables bidirectional communication: generator yields OUT, caller sends IN.
    function accumulator(): Generator {
        $total = 0;
        while (true) {
            $value = yield $total;
            $total += $value;
        }
    }

    $acc = accumulator();
    $acc->current();
    echo "Accumulator: ";
    foreach ([10, 20, 30] as $v) {
        echo $acc->send($v) . " ";
    }
    echo "\n";  // => Accumulator: 10 30 60

    // yield from delegates iteration to another generator — like calling a sub-generator.
    // The outer generator pauses while the inner one produces values.
    function inner(): Generator { yield 1; yield 2; }
    function outer(): Generator { yield from inner(); yield 3; }
    $delegated = [];
    foreach (outer() as $v) { $delegated[] = $v; }
    echo "yield from: " . implode(', ', $delegated) . "\n";  // => yield from: 1, 2, 3

    // Attributes (PHP 8.0) replace docblock annotations with native, structured metadata.
    // Before 8.0, frameworks like Symfony/Doctrine used /** @Route("/path") */ comments,
    // which required parsing docblocks at runtime. Attributes are part of the AST and
    // accessible via Reflection — faster, type-safe, and IDE-friendly.
    #[Attribute]
    class Route {
        public function __construct(
            public readonly string $path,
            public readonly string $method = 'GET',
        ) {}
    }

    class Controller {
        #[Route('/api/users', method: 'POST')]
        public function createUser(): string { return 'created'; }
    }

    // Attributes are read via the Reflection API — you get the class, then its attributes.
    // newInstance() instantiates the attribute class with the arguments from the declaration.
    $ref = new ReflectionMethod(Controller::class, 'createUser');
    $attrs = $ref->getAttributes(Route::class);
    foreach ($attrs as $attr) {
        $route = $attr->newInstance();
        echo "Attribute: {$route->method} {$route->path}\n";  // => Attribute: POST /api/users
    }

    // Reflection is PHP's introspection API — inspect classes, methods, properties at runtime.
    // Frameworks use it for dependency injection, route discovery, and ORM mapping.
    $refClass = new ReflectionClass(Point::class);
    echo "Reflection: " . $refClass->getName() . " has " . count($refClass->getProperties()) . " properties\n";  // => Reflection: Point has 2 properties
    echo "Methods: " . implode(', ', array_map(fn($m) => $m->getName(), $refClass->getMethods())) . "\n";  // => Methods: __construct, distanceTo, __toString

    // Stringable (PHP 8.0) is an interface automatically implemented by any class with __toString.
    // You can type-hint Stringable to accept any object that can be cast to string.
    class Label implements Stringable {
        public function __construct(private string $text) {}
        public function __toString(): string { return "[$this->text]"; }
    }
    $label = new Label("important");
    echo "Stringable: $label\n";  // => Stringable: [important]

    // WeakMap (PHP 8.0) holds references to objects that don't prevent garbage collection.
    // When the object is destroyed, its WeakMap entry is automatically removed.
    // Use case: caching computed values for objects without creating memory leaks.
    // Regular arrays/SplObjectStorage hold strong references that prevent GC.
    $map = new WeakMap();
    $obj1 = new stdClass();
    $obj2 = new stdClass();
    $map[$obj1] = 'data for obj1';
    $map[$obj2] = 'data for obj2';
    echo "WeakMap count: " . count($map) . "\n";  // => WeakMap count: 2
    unset($obj1);
    echo "WeakMap after unset: " . count($map) . "\n";  // => WeakMap after unset: 1
}

// ============================================================
//  MAIN
// ============================================================
echo "PHP " . PHP_VERSION . " Fundamentals\n";  // => PHP <version> Fundamentals
echo str_repeat('=', 60) . "\n";

basics();
collections();
oop_demo();
functions_demo();
type_system_demo();
fibers_demo();
advanced_demo();

echo "\n" . str_repeat('=', 60) . "\n";
echo "  All sections complete!\n";  // => All sections complete!
echo str_repeat('=', 60) . "\n";
