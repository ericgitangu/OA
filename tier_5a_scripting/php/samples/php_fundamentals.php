<?php
/**
 * PHP Fundamentals: Beginner to Advanced — Standard Library Only.
 *
 * A dense, runnable syntax reference covering core PHP concepts.
 * Run: php php_fundamentals.php
 * Requires: PHP 8.1+ (for enums, fibers, readonly, intersection types)
 */

function section(string $title): void {
    echo "\n" . str_repeat('=', 60) . "\n  $title\n" . str_repeat('=', 60) . "\n";
}

// ============================================================
//  1. BASICS
// ============================================================
function basics(): void {
    section("1. BASICS — Types, Strings, Match, Named Args, Null Coalescing");

    // --- Types ---
    $int = 42;
    $float = 3.14;
    $str = "PHP";
    $bool = true;
    $null = null;
    echo "int=$int  float=$float  str=$str  bool=" . ($bool ? 'true' : 'false') . "  null=" . var_export($null, true) . "\n";
    echo "Type checking: is_int=" . var_export(is_int($int), true) . "  is_string=" . var_export(is_string($str), true) . "\n";

    // --- String interpolation ---
    $name = "World";
    echo "Hello, $name!\n";
    echo "Expression: {$name} has " . strlen($name) . " chars\n";
    $heredoc = <<<EOT
    Heredoc with $name interpolation
    and multiple lines.
    EOT;
    echo "Heredoc: " . trim($heredoc) . "\n";

    // --- Match expression (PHP 8) ---
    $status = 200;
    $text = match(true) {
        $status >= 200 && $status < 300 => 'Success',
        $status >= 400 && $status < 500 => 'Client Error',
        $status >= 500 => 'Server Error',
        default => 'Unknown',
    };
    echo "Match: status $status => $text\n";

    // --- Named arguments (PHP 8) ---
    function createUser(string $name, int $age, string $role = 'user'): string {
        return "$name (age: $age, role: $role)";
    }
    echo "Named args: " . createUser(age: 25, name: 'Alice', role: 'admin') . "\n";

    // --- Null coalescing ---
    $config = ['db' => ['host' => 'localhost']];
    echo "Null coalesce: " . ($config['db']['port'] ?? 3306) . "\n";
    $value = null;
    $value ??= 'default';
    echo "Null coalesce assign: $value\n";

    // --- Nullsafe operator (?->) chains method calls, short-circuiting on null ---
    // Strings are not objects in PHP — nullsafe requires object methods, not functions.
    $user = new class {
        public ?object $profile = null;
    };
    $user->profile = new class { public function getDisplayName(): string { return "Alice"; } };
    echo "Nullsafe: " . ($user->profile?->getDisplayName() ?? 'no profile') . "\n";
    $user->profile = null;
    echo "Nullsafe (null): " . ($user->profile?->getDisplayName() ?? 'no profile') . "\n";
}

// ============================================================
//  2. COLLECTIONS
// ============================================================
function collections(): void {
    section("2. COLLECTIONS — Arrays, Array Functions, SplFixedArray");

    // --- Array basics ---
    $indexed = [10, 20, 30, 40, 50];
    $assoc = ['name' => 'PHP', 'version' => 8.2, 'typed' => true];
    echo "Indexed: " . implode(', ', $indexed) . "\n";
    echo "Assoc: " . json_encode($assoc) . "\n";

    // --- Spread operator ---
    $more = [0, ...$indexed, 60];
    echo "Spread: " . implode(', ', $more) . "\n";

    // --- Destructuring ---
    [$first, $second] = $indexed;
    ['name' => $name, 'version' => $version] = $assoc;
    echo "Destructure: first=$first, name=$name, version=$version\n";

    // --- Array functions ---
    $nums = range(1, 10);
    echo "array_map:    " . implode(', ', array_map(fn($n) => $n * 2, $nums)) . "\n";
    echo "array_filter: " . implode(', ', array_filter($nums, fn($n) => $n % 2 === 0)) . "\n";
    echo "array_reduce: " . array_reduce($nums, fn($carry, $n) => $carry + $n, 0) . "\n";
    echo "array_slice:  " . implode(', ', array_slice($nums, 2, 3)) . "\n";
    echo "array_chunk:  " . json_encode(array_chunk($nums, 3)) . "\n";
    echo "array_combine: " . json_encode(array_combine(['a', 'b', 'c'], [1, 2, 3])) . "\n";
    echo "array_unique: " . implode(', ', array_unique([1, 1, 2, 3, 3])) . "\n";

    $words = ['banana', 'apple', 'cherry'];
    usort($words, fn($a, $b) => strlen($a) <=> strlen($b));
    echo "usort by length: " . implode(', ', $words) . "\n";

    // --- array_column (like pluck) ---
    $people = [
        ['name' => 'Alice', 'age' => 30],
        ['name' => 'Bob', 'age' => 25],
    ];
    echo "array_column: " . implode(', ', array_column($people, 'name')) . "\n";

    // --- SplFixedArray ---
    $fixed = new SplFixedArray(5);
    for ($i = 0; $i < 5; $i++) { $fixed[$i] = $i * 10; }
    echo "SplFixedArray: ";
    foreach ($fixed as $v) { echo "$v "; }
    echo "(size: {$fixed->getSize()})\n";
}

// ============================================================
//  3. OOP
// ============================================================
function oop_demo(): void {
    section("3. OOP — Classes, Interfaces, Traits, Enums, Readonly");

    // --- Constructor promotion & readonly (PHP 8.1) ---
    class Point {
        public function __construct(
            public readonly float $x,
            public readonly float $y,
        ) {}

        public function distanceTo(Point $other): float {
            return sqrt(($this->x - $other->x) ** 2 + ($this->y - $other->y) ** 2);
        }

        public function __toString(): string {
            return "Point({$this->x}, {$this->y})";
        }
    }

    $p1 = new Point(0, 0);
    $p2 = new Point(3, 4);
    echo "Point: $p1  Distance: {$p1->distanceTo($p2)}\n";

    // --- Interface ---
    interface Describable {
        public function describe(): string;
    }

    // --- Trait ---
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
    echo $u->describe() . "\n";

    // --- Enum (PHP 8.1) ---
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
    echo "Enum: {$c->name} = {$c->value}, hex = {$c->hex()}\n";
    echo "From string: " . Color::from('blue')->name . "\n";

    // --- Abstract class ---
    abstract class Shape {
        abstract public function area(): float;
    }

    class Circle extends Shape {
        public function __construct(private readonly float $radius) {}
        public function area(): float { return M_PI * $this->radius ** 2; }
    }

    echo "Circle area: " . round((new Circle(5))->area(), 2) . "\n";

    // --- Anonymous class ---
    $logger = new class {
        public function log(string $msg): void { echo "  [LOG] $msg\n"; }
    };
    $logger->log("Anonymous class works!");
}

// ============================================================
//  4. FUNCTIONS
// ============================================================
function functions_demo(): void {
    section("4. FUNCTIONS — Closures, Arrow Fns, First-Class Callables");

    // --- Closures ---
    $multiplier = function(int $factor): Closure {
        return function(int $x) use ($factor): int {
            return $x * $factor;
        };
    };
    $double = $multiplier(2);
    $triple = $multiplier(3);
    echo "Closure: double(5)={$double(5)}  triple(5)={$triple(5)}\n";

    // --- Arrow functions (PHP 7.4+) ---
    $nums = [1, 2, 3, 4, 5];
    $squared = array_map(fn($n) => $n ** 2, $nums);
    echo "Arrow fn: " . implode(', ', $squared) . "\n";

    // --- First-class callable syntax (PHP 8.1) ---
    $strlen = strlen(...);
    echo "First-class callable: strlen('hello') = {$strlen('hello')}\n";
    $words = ['hi', 'hello', 'hey'];
    $lengths = array_map(strlen(...), $words);
    echo "Mapped lengths: " . implode(', ', $lengths) . "\n";

    // --- Variadic & splat ---
    $sum = function(int ...$nums): int { return array_sum($nums); };
    echo "Variadic sum: {$sum(1, 2, 3, 4, 5)}\n";
    $args = [10, 20, 30];
    echo "Splat sum: {$sum(...$args)}\n";
}

// ============================================================
//  5. TYPE SYSTEM
// ============================================================
function type_system_demo(): void {
    section("5. TYPE SYSTEM — Union, Intersection, Readonly Classes");

    // --- Union types (PHP 8.0) ---
    function processInput(int|string $input): string {
        return match(true) {
            is_int($input) => "Integer: $input",
            is_string($input) => "String: '$input'",
        };
    }
    echo processInput(42) . "\n";
    echo processInput("hello") . "\n";

    // --- Intersection types (PHP 8.1) ---
    interface Countable2 { public function count(): int; }
    interface Serializable2 { public function serialize(): string; }

    function processCollection(Countable2&Serializable2 $item): string {
        return "Count: {$item->count()}, Serialized: {$item->serialize()}";
    }

    $coll = new class implements Countable2, Serializable2 {
        public function count(): int { return 5; }
        public function serialize(): string { return json_encode(['items' => 5]); }
    };
    echo "Intersection type: " . processCollection($coll) . "\n";

    // --- Typed properties & nullable ---
    class Config {
        public string $host = 'localhost';
        public int $port = 3306;
        public ?string $password = null;
    }

    $cfg = new Config();
    echo "Typed props: host={$cfg->host} port={$cfg->port} password=" . var_export($cfg->password, true) . "\n";
}

// ============================================================
//  6. FIBERS
// ============================================================
function fibers_demo(): void {
    section("6. FIBERS — Cooperative Concurrency (PHP 8.1)");

    $fiber = new Fiber(function(): string {
        $value = Fiber::suspend('first suspend');
        echo "  Fiber resumed with: $value\n";
        Fiber::suspend('second suspend');
        return 'fiber complete';
    });

    $result1 = $fiber->start();
    echo "After start: $result1\n";

    $result2 = $fiber->resume('hello from main');
    echo "After resume: $result2\n";

    $fiber->resume();
    echo "Return value: {$fiber->getReturn()}\n";

    // --- Practical fiber example: simple coroutine ---
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
    echo "Fiber generator: " . implode(', ', $values) . "\n";
}

// ============================================================
//  7. ADVANCED
// ============================================================
function advanced_demo(): void {
    section("7. ADVANCED — Generators, Attributes, Reflection, WeakMap");

    // --- Generators ---
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
    echo "Fibonacci: " . implode(', ', $fibs) . "\n";

    // Generator with send
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
    echo "\n";

    // yield from delegation
    function inner(): Generator { yield 1; yield 2; }
    function outer(): Generator { yield from inner(); yield 3; }
    $delegated = [];
    foreach (outer() as $v) { $delegated[] = $v; }
    echo "yield from: " . implode(', ', $delegated) . "\n";

    // --- Attributes (PHP 8.0) ---
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

    // Read attribute via reflection
    $ref = new ReflectionMethod(Controller::class, 'createUser');
    $attrs = $ref->getAttributes(Route::class);
    foreach ($attrs as $attr) {
        $route = $attr->newInstance();
        echo "Attribute: {$route->method} {$route->path}\n";
    }

    // --- Reflection ---
    $refClass = new ReflectionClass(Point::class);
    echo "Reflection: " . $refClass->getName() . " has " . count($refClass->getProperties()) . " properties\n";
    echo "Methods: " . implode(', ', array_map(fn($m) => $m->getName(), $refClass->getMethods())) . "\n";

    // --- Stringable interface ---
    class Label implements Stringable {
        public function __construct(private string $text) {}
        public function __toString(): string { return "[$this->text]"; }
    }
    $label = new Label("important");
    echo "Stringable: $label\n";

    // --- WeakMap ---
    $map = new WeakMap();
    $obj1 = new stdClass();
    $obj2 = new stdClass();
    $map[$obj1] = 'data for obj1';
    $map[$obj2] = 'data for obj2';
    echo "WeakMap count: " . count($map) . "\n";
    unset($obj1);
    echo "WeakMap after unset: " . count($map) . "\n";
}

// ============================================================
//  MAIN
// ============================================================
echo "PHP " . PHP_VERSION . " Fundamentals\n";
echo str_repeat('=', 60) . "\n";

basics();
collections();
oop_demo();
functions_demo();
type_system_demo();
fibers_demo();
advanced_demo();

echo "\n" . str_repeat('=', 60) . "\n";
echo "  All sections complete!\n";
echo str_repeat('=', 60) . "\n";
