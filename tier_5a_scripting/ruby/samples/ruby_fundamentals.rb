#!/usr/bin/env ruby
# Ruby Fundamentals: Beginner to Advanced — Standard Library Only.
#
# A dense, runnable syntax reference covering core Ruby concepts.
# Run: ruby ruby_fundamentals.rb
# Requires: Ruby 3.0+ (for pattern matching)
#
# Ruby is a dynamically typed, object-oriented language where EVERYTHING is an object —
# even integers, nil, and true/false. This means 42.even? is valid because 42 is an
# instance of Integer. Ruby uses "duck typing": if it responds to a method, it works.
# There are no interfaces or compile-time type checks — just message sends.

require 'set'
require 'ostruct'

def section(title)
  puts "\n#{'=' * 60}\n  #{title}\n#{'=' * 60}"
end

# ============================================================
#  TOP-LEVEL CLASS & MODULE DEFINITIONS
#  (Ruby does not allow class defs inside method bodies)
# ============================================================

# Ruby's object model: every class is an object (instance of Class), and
# every object has a hidden "eigenclass" (singleton class) that sits between
# the object and its class in the method lookup chain. This is how per-object
# methods work and why Ruby can add methods to individual instances.

# attr_accessor generates getter and setter methods at class definition time.
# This is actually metaprogramming — it calls Module#attr_accessor which uses
# define_method under the hood to create the methods dynamically.
class Animal
  attr_accessor :name, :sound

  # initialize is Ruby's constructor — called by Class#new.
  # Instance variables (@name) are always private; you need attr_* to expose them.
  def initialize(name, sound)
    @name = name
    @sound = sound
  end

  # String interpolation in Ruby calls #to_s on the embedded expression.
  # This is duck typing in action — any object that responds to to_s works here.
  def speak
    "#{@name} says #{@sound}"
  end

  def to_s
    "Animal(#{@name})"
  end
end

# Single inheritance with <. Ruby chose single inheritance + mixins (modules)
# over multiple inheritance to avoid the diamond problem.
# super calls the parent's method — Ruby walks the "method lookup path" (ancestors chain)
# to find the next implementation.
class Dog < Animal
  def initialize(name)
    super(name, "Woof")
  end

  def fetch(item)
    "#{@name} fetches the #{item}!"
  end
end

# Modules serve two purposes: (1) namespacing and (2) mixins.
# include inserts the module into the class's ancestor chain, so its methods
# become available as instance methods. This is Ruby's answer to multiple inheritance.
# Method dispatch walks: object -> eigenclass -> class -> included modules -> superclass -> ...
module Greetable
  def greet
    "Hello, I'm #{name}"
  end
end

class Person
  include Greetable
  attr_reader :name

  def initialize(name)
    @name = name
  end
end

# method_missing is the last stop in Ruby's method lookup chain.
# When a message is sent to an object, Ruby searches: eigenclass -> class -> modules -> superclass.
# If nothing is found, it calls method_missing. This enables DSLs and proxy patterns.
# Always override respond_to_missing? alongside method_missing — otherwise introspection
# tools (respond_to?, method(:name)) won't know about your dynamic methods.
class DynamicProxy
  def method_missing(name, *args)
    if name.to_s.start_with?("say_")
      word = name.to_s.sub("say_", "")
      "Saying: #{word}"
    else
      super
    end
  end

  def respond_to_missing?(name, include_private = false)
    name.to_s.start_with?("say_") || super
  end
end

# define_method creates methods dynamically at class definition time.
# Because class bodies are executable code in Ruby (not just declarations),
# you can use loops, conditionals, and metaprogramming to generate methods.
# This is how Rails builds attribute accessors, route helpers, and associations.
class Talker
  %w[english spanish french].each do |lang|
    define_method("speak_#{lang}") do
      "Speaking #{lang.capitalize}!"
    end
  end
end

# method_added is a hook method — Ruby calls it whenever a new method is defined
# on this class. These hooks (method_added, included, inherited, etc.) are how
# Ruby frameworks build declarative APIs.
class Tracked
  def self.method_added(name)
    @methods_added ||= []
    @methods_added << name unless name == :initialize
  end

  def self.tracked_methods
    @methods_added || []
  end

  def foo; end
  def bar; end
end

# const_missing is like method_missing but for constants.
# It intercepts references to undefined constants within this module.
module AutoConst
  def self.const_missing(name)
    "Auto-generated constant: #{name}"
  end
end

# Comparable is a mixin that gives you <, <=, >, >=, between?, and clamp
# for free — you only need to define <=> (the spaceship operator).
# This is the "template method" pattern: the module provides the algorithm,
# you provide the one piece that varies.
class Temperature
  include Comparable
  attr_reader :degrees

  def initialize(degrees)
    @degrees = degrees
  end

  # <=> returns -1, 0, or 1. Ruby's sort, min, max all rely on this single method.
  def <=>(other)
    @degrees <=> other.degrees
  end

  def to_s
    "#{@degrees}°"
  end
end

# Struct.new dynamically creates a new class with named attributes, equality,
# hash, to_s, and destructuring built in. It's Ruby's lightweight value object.
# The block form lets you add methods to the generated class.
Point = Struct.new(:x, :y) do
  def distance_to(other)
    Math.sqrt((x - other.x)**2 + (y - other.y)**2)
  end
end

# ============================================================
#  1. BASICS
# ============================================================
def basics
  section("1. BASICS — Variables, Symbols, Strings, Ranges, Regex")

  # Ruby is dynamically typed — variables hold references to objects, not typed values.
  # There's no variable declaration syntax; assignment creates the variable.
  x = 42
  pi = 3.14
  name = "Ruby"
  flag = true
  nothing = nil
  puts "int=#{x}  float=#{pi}  str=#{name.inspect}  bool=#{flag}  nil=#{nothing.inspect}"

  # In Ruby, only nil and false are falsy. Everything else — including 0, "", and [] — is truthy.
  # This differs from Python/JS where 0 and "" are falsy.
  puts "Falsy in Ruby: only nil and false — 0 is truthy: #{!!0}"

  # Symbols are immutable, interned strings. They're stored once in memory and
  # compared by identity (object_id), not by value — making them faster than strings
  # for keys, method names, and identifiers. The symbol table is never garbage collected.
  sym = :hello
  puts "Symbol: #{sym}  object_id stable: #{:hello.object_id == :hello.object_id}"
  puts "Symbol to string: #{sym.to_s}  String to symbol: #{"world".to_sym.inspect}"

  # Double-quoted strings support interpolation; single-quoted don't.
  # Strings are mutable by default in Ruby (unlike Python/Java).
  greeting = "Hello, #{name}!"
  puts greeting
  puts "upcase=#{name.upcase}  reverse=#{name.reverse}  chars=#{name.chars}"

  # freeze makes an object immutable. Ruby 3+ has frozen string literals opt-in
  # via `# frozen_string_literal: true` pragma, which improves memory and performance
  # by deduplicating identical string objects.
  puts "Frozen string: #{name.freeze.frozen?}"

  # Heredocs with <<~ strip leading indentation (squiggly heredoc, Ruby 2.3+).
  multiline = <<~HEREDOC
    This is a heredoc.
    It preserves #{2 + 2} interpolation.
  HEREDOC
  puts "Heredoc: #{multiline.strip.inspect}"

  # Ranges are objects that represent intervals. Two dots (..) is inclusive,
  # three dots (...) is exclusive of the end. Ranges are lazy — they don't
  # allocate all elements until you call to_a or iterate.
  inclusive = (1..5)
  exclusive = (1...5)
  puts "Inclusive: #{inclusive.to_a}  Exclusive: #{exclusive.to_a}"
  puts "Range includes 3? #{inclusive.include?(3)}  Alphabet: #{('a'..'e').to_a}"

  # Endless ranges (Ruby 2.6+) have no upper bound — useful with take, lazy, and case/when.
  puts "Endless range: #{(1..).take(5)}"

  # Regex literals use /pattern/ syntax. match returns a MatchData object
  # that supports indexed access to capture groups.
  str = "Ruby 3.2 is great"
  match = str.match(/(\w+)\s(\d+\.\d+)/)
  puts "Match: #{match[0]}  Capture1: #{match[1]}  Capture2: #{match[2]}"
  puts "gsub: #{str.gsub(/\d+/, 'X')}"
  puts "scan: #{str.scan(/\w+/)}"
end

# ============================================================
#  2. COLLECTIONS
# ============================================================
def collections
  section("2. COLLECTIONS — Array, Hash, Set, Enumerable")

  # Arrays are ordered, integer-indexed, heterogeneous collections.
  # Internally they're C arrays of VALUE pointers — O(1) random access.
  arr = [3, 1, 4, 1, 5, 9, 2, 6]
  puts "Array: #{arr}"
  puts "push/pop: #{arr.push(7).pop}  unshift/shift: #{arr.unshift(0).shift}"
  puts "slice: #{arr[1..3]}  last: #{arr.last(3)}  flatten: #{[[1, 2], [3]].flatten}"
  puts "compact: #{[1, nil, 2, nil, 3].compact}"
  puts "uniq: #{[1, 1, 2, 3, 3].uniq}  sort: #{arr.sort}"

  # Hashes are ordered (since Ruby 1.9) key-value stores.
  # The symbol shorthand { name: "Ruby" } is syntactic sugar for { :name => "Ruby" }.
  # fetch raises KeyError if missing (safer than [] which returns nil silently).
  h = { name: "Ruby", version: 3.2, paradigm: "OOP" }
  puts "Hash: #{h}"
  puts "fetch: #{h.fetch(:name)}  dig: #{h.dig(:name)}"
  puts "keys: #{h.keys}  values: #{h.values}"
  h.merge!(year: 1995)
  puts "merge!: #{h}"
  puts "select: #{h.select { |_k, v| v.is_a?(Numeric) }}"

  # Set requires 'set' — it's a Hash wrapper where keys are the elements and values are true.
  s1 = Set[1, 2, 3, 4]
  s2 = Set[3, 4, 5, 6]
  puts "Set union: #{(s1 | s2).to_a}  intersection: #{(s1 & s2).to_a}  diff: #{(s1 - s2).to_a}"

  # Enumerable is Ruby's most powerful mixin — mixed into Array, Hash, Range, Set, etc.
  # It provides 50+ methods; you only need to define #each and include Enumerable.
  # The &:method_name syntax creates a Proc from a method name via Symbol#to_proc.
  nums = (1..10).to_a
  puts "map:       #{nums.map { |n| n * 2 }}"
  puts "select:    #{nums.select(&:even?)}"
  puts "reject:    #{nums.reject(&:even?)}"

  # reduce (alias: inject) folds the collection into a single value.
  # The :+ shorthand passes the method name directly — no block needed.
  puts "reduce:    #{nums.reduce(0, :+)}"
  puts "group_by:  #{nums.group_by { |n| n % 3 }}"
  puts "flat_map:  #{[[1, 2], [3, 4]].flat_map { |a| a.map { |x| x * 10 } }}"
  puts "zip:       #{[1, 2, 3].zip(['a', 'b', 'c'])}"
  puts "each_with_object: #{nums.each_with_object({}) { |n, h| h[n] = n**2 }.take(5).to_h}"

  # tally (Ruby 2.7+) counts occurrences — equivalent to group_by + count.
  puts "tally:     #{%w[a b a c b a].tally}"
  puts "min_by:    #{%w[apple fig banana].min_by(&:length)}"
  puts "chunk:     #{nums.chunk { |n| n <= 5 }.map { |key, vals| [key, vals] }}"
end

# ============================================================
#  3. BLOCKS, PROCS, LAMBDAS
# ============================================================

# yield transfers control to the block passed to this method.
# Blocks are Ruby's closure syntax — they capture the surrounding scope.
# Every Ruby method can implicitly accept a block without declaring it.
def with_timing
  start = Process.clock_gettime(Process::CLOCK_MONOTONIC)
  result = yield
  elapsed = Process.clock_gettime(Process::CLOCK_MONOTONIC) - start
  puts "  Elapsed: #{(elapsed * 1000).round(3)}ms, Result: #{result}"
end

# The & prefix converts a block into a Proc object, making it a first-class value
# you can store, pass around, and call later. Without &, blocks are invisible to the method.
def capture_block(&blk)
  puts "  Block class: #{blk.class}, arity: #{blk.arity}"
  blk.call(10)
end

def blocks_procs_lambdas
  section("3. BLOCKS / PROCS / LAMBDAS")

  # --- Blocks & yield ---
  with_timing { (1..1000).reduce(:+) }

  # --- Explicit &block ---
  capture_block { |x| puts "  Block received: #{x}" }

  # Proc vs Lambda: two kinds of callable objects with different semantics.
  # Procs have loose arity (missing args become nil, extra args ignored).
  # Lambdas enforce arity (wrong arg count raises ArgumentError).
  # Procs' return exits the enclosing method; Lambda's return exits only the lambda.
  # This makes lambdas behave like methods, while procs behave like inline code blocks.
  my_proc = Proc.new { |x, y| "proc: #{x}, #{y}" }
  my_lambda = ->(x, y) { "lambda: #{x}, #{y}" }
  puts "Proc (missing arg): #{my_proc.call(1)}"       # y is nil
  puts "Lambda: #{my_lambda.call(1, 2)}"
  puts "Proc lambda?: #{my_proc.lambda?}  Lambda lambda?: #{my_lambda.lambda?}"

  # method(:puts) returns a Method object — a bound reference to the method.
  # The & converts it to a Proc so it can be passed as a block argument.
  method_obj = method(:puts)
  puts "Method object: #{method_obj.class}, name: #{method_obj.name}"
  [1, 2, 3].each(&method(:puts))

  # Currying transforms a multi-argument function into a chain of single-argument functions.
  # This enables partial application — fix some args now, supply the rest later.
  adder = ->(a, b) { a + b }
  add5 = adder.curry.(5)
  puts "Curried: add5.(10) = #{add5.(10)}"
end

# ============================================================
#  4. OOP
# ============================================================
def oop_demo
  section("4. OOP — Classes, Modules, Mixins, Open Classes")

  dog = Dog.new("Rex")
  puts dog.speak
  puts dog.fetch("ball")

  puts Person.new("Alice").greet

  # ancestors shows the full method lookup chain: class -> included modules -> superclass -> ...
  # This is how Ruby resolves method calls — it walks this chain until it finds a match.
  puts "Person ancestors: #{Person.ancestors.take(4)}"

  proxy = DynamicProxy.new
  puts proxy.say_hello
  puts "responds to say_hi? #{proxy.respond_to?(:say_hi)}"

  # Open classes: Ruby lets you reopen ANY class (including built-in ones like Integer)
  # and add or override methods at runtime. This is called "monkey patching."
  # class_eval executes a block in the context of a class, allowing method definitions
  # inside method bodies (where `class` keyword syntax is not allowed).
  # Powerful but dangerous — use Refinements (Module#refine) for scoped patches in production.
  Integer.class_eval do
    def factorial
      return 1 if self <= 1
      self * (self - 1).factorial
    end
  end
  puts "5! = #{5.factorial}"
end

# ============================================================
#  5. METAPROGRAMMING
# ============================================================
def metaprogramming_demo
  section("5. METAPROGRAMMING — define_method, eval, hooks")

  t = Talker.new
  puts t.speak_english
  puts t.speak_french

  # class_eval opens a class for modification — equivalent to reopening with `class` keyword
  # but works with variables (class keyword requires a constant).
  # This evaluates the block in the context of String's class scope.
  String.class_eval do
    def shout
      upcase + "!!!"
    end
  end
  puts "hello".shout

  # instance_eval evaluates code in the context of a specific object's eigenclass
  # (singleton class). The eigenclass is an invisible class unique to each object,
  # sitting between the object and its class in the lookup chain.
  # Methods defined here exist only on this one object, not on all instances.
  obj = Object.new
  obj.instance_eval do
    @secret = 42
    def reveal
      @secret
    end
  end
  puts "instance_eval secret: #{obj.reveal}"

  puts "Tracked methods: #{Tracked.tracked_methods}"
  puts AutoConst::ANYTHING
end

# ============================================================
#  6. FUNCTIONAL PATTERNS
# ============================================================
def functional_demo
  section("6. FUNCTIONAL — Freeze, Comparable, Lazy Enumerators")

  # freeze makes an object immutable. Any modification attempt raises FrozenError.
  # In Ruby, immutability is opt-in (unlike Elixir/Clojure where it's the default).
  frozen_arr = [1, 2, 3].freeze
  begin
    frozen_arr << 4
  rescue => e
    puts "FrozenError: #{e.message}"
  end

  # --- Comparable ---
  temps = [30, 20, 25, 15].map { |d| Temperature.new(d) }
  puts "Sorted temps: #{temps.sort}"
  puts "Max: #{temps.max}  Min: #{temps.min}"
  puts "Between? #{Temperature.new(22).between?(Temperature.new(20), Temperature.new(25))}"

  # Lazy enumerators defer computation until values are consumed.
  # Without lazy, (1..Float::INFINITY).select would try to build an infinite array.
  # Lazy creates a pipeline that pulls one element at a time — like Unix pipes.
  lazy_result = (1..Float::INFINITY).lazy
    .select { |n| n.odd? }
    .map { |n| n ** 2 }
    .first(5)
  puts "Lazy odd squares: #{lazy_result}"

  # Enumerator.new creates a custom lazy sequence using a yielder.
  # The loop + y.yield pattern produces values on demand — the enumerator
  # suspends between yields (using fibers internally for the coroutine behavior).
  fibs = Enumerator.new do |y|
    a, b = 0, 1
    loop do
      y.yield a
      a, b = b, a + b
    end
  end
  puts "First 10 fibs: #{fibs.take(10)}"
end

# ============================================================
#  7. PATTERNS — Struct, OpenStruct, Pattern Matching, Ractor
# ============================================================
def patterns_demo
  section("7. PATTERNS — Struct, OpenStruct, Pattern Matching, Ractor")

  # --- Struct ---
  p1 = Point.new(0, 0)
  p2 = Point.new(3, 4)
  puts "Point: #{p1}  Distance: #{p1.distance_to(p2)}"
  puts "Struct members: #{Point.members}"

  # OpenStruct creates objects with arbitrary attributes defined at runtime.
  # It uses method_missing internally — convenient for prototyping but slower
  # than Struct (which generates real methods at creation time).
  config = OpenStruct.new(host: "localhost", port: 8080)
  config.debug = true
  puts "OpenStruct: host=#{config.host} port=#{config.port} debug=#{config.debug}"

  # Pattern matching (Ruby 3+) brings ML-style structural matching to Ruby.
  # `case/in` is different from `case/when`: it matches structure not just equality.
  # `in` performs exhaustive structural destructuring with variable binding.
  data = { name: "Alice", age: 30, role: :admin }

  result = case data
           in { name: String => name, role: :admin }
             "Admin user: #{name}"
           in { name: String => name, age: (18..) }
             "Adult user: #{name}"
           else
             "Unknown"
           end
  puts "Pattern match: #{result}"

  # Array pattern matching with splat (*rest) captures remaining elements.
  case [1, 2, 3, 4, 5]
  in [Integer => first, Integer => second, *rest]
    puts "Array pattern: first=#{first}, second=#{second}, rest=#{rest}"
  end

  # Find pattern (Ruby 3.1+) searches for elements matching criteria anywhere in the array.
  case [1, 2, 3, "hello", 4]
  in [*, String => s, *]
    puts "Find pattern found string: #{s}"
  end

  # Pin operator (^) prevents rebinding — it matches against the variable's current value
  # instead of capturing a new value. Without ^, pattern matching would always succeed
  # by binding any value to the variable name.
  expected_val = 42
  case { value: 42 }
  in { value: ^expected_val }
    puts "Pin operator matched expected value: #{expected_val}"
  end

  # Ractor (Ruby 3+) is Ruby's actor-based concurrency model for true parallelism.
  # Unlike threads (limited by the GVL/GIL), each Ractor has its own GVL and cannot
  # share mutable state. Objects must be deeply frozen or copied to cross Ractor boundaries.
  # This provides memory safety without locks by enforcing isolation at the VM level.
  if defined?(Ractor)
    r = Ractor.new do
      msg = Ractor.receive
      "Ractor processed: #{msg.upcase}"
    end
    r.send("hello")
    puts r.take
  else
    puts "Ractor not available in this Ruby version"
  end
end

# ============================================================
#  MAIN
# ============================================================
puts "Ruby #{RUBY_VERSION} Fundamentals"
puts "=" * 60

basics
collections
blocks_procs_lambdas
oop_demo
metaprogramming_demo
functional_demo
patterns_demo

puts "\n#{'=' * 60}"
puts "  All sections complete!"
puts "=" * 60
