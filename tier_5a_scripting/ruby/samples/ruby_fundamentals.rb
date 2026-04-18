#!/usr/bin/env ruby
# Ruby Fundamentals: Beginner to Advanced — Standard Library Only.
#
# A dense, runnable syntax reference covering core Ruby concepts.
# Run: ruby ruby_fundamentals.rb
# Requires: Ruby 3.0+ (for pattern matching)

require 'set'
require 'ostruct'

def section(title)
  puts "\n#{'=' * 60}\n  #{title}\n#{'=' * 60}"
end

# ============================================================
#  1. BASICS
# ============================================================
def basics
  section("1. BASICS — Variables, Symbols, Strings, Ranges, Regex")

  # --- Variables & types ---
  x = 42
  pi = 3.14
  name = "Ruby"
  flag = true
  nothing = nil
  puts "int=#{x}  float=#{pi}  str=#{name.inspect}  bool=#{flag}  nil=#{nothing.inspect}"
  puts "Falsy in Ruby: only nil and false — 0 is truthy: #{!!0}"

  # --- Symbols ---
  sym = :hello
  puts "Symbol: #{sym}  object_id stable: #{:hello.object_id == :hello.object_id}"
  puts "Symbol to string: #{sym.to_s}  String to symbol: #{"world".to_sym.inspect}"

  # --- String interpolation & methods ---
  greeting = "Hello, #{name}!"
  puts greeting
  puts "upcase=#{name.upcase}  reverse=#{name.reverse}  chars=#{name.chars}"
  puts "Frozen string: #{name.freeze.frozen?}"

  multiline = <<~HEREDOC
    This is a heredoc.
    It preserves #{2 + 2} interpolation.
  HEREDOC
  puts "Heredoc: #{multiline.strip.inspect}"

  # --- Ranges ---
  inclusive = (1..5)
  exclusive = (1...5)
  puts "Inclusive: #{inclusive.to_a}  Exclusive: #{exclusive.to_a}"
  puts "Range includes 3? #{inclusive.include?(3)}  Alphabet: #{('a'..'e').to_a}"
  puts "Endless range: #{(1..).take(5)}"

  # --- Regex ---
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

  # --- Array basics ---
  arr = [3, 1, 4, 1, 5, 9, 2, 6]
  puts "Array: #{arr}"
  puts "push/pop: #{arr.push(7).pop}  unshift/shift: #{arr.unshift(0).shift}"
  puts "slice: #{arr[1..3]}  last: #{arr.last(3)}  flatten: #{[[1, 2], [3]].flatten}"
  puts "compact: #{[1, nil, 2, nil, 3].compact}"
  puts "uniq: #{[1, 1, 2, 3, 3].uniq}  sort: #{arr.sort}"

  # --- Hash basics ---
  h = { name: "Ruby", version: 3.2, paradigm: "OOP" }
  puts "Hash: #{h}"
  puts "fetch: #{h.fetch(:name)}  dig: #{h.dig(:name)}"
  puts "keys: #{h.keys}  values: #{h.values}"
  h.merge!(year: 1995)
  puts "merge!: #{h}"
  puts "select: #{h.select { |_k, v| v.is_a?(Numeric) }}"

  # --- Set ---
  s1 = Set[1, 2, 3, 4]
  s2 = Set[3, 4, 5, 6]
  puts "Set union: #{(s1 | s2).to_a}  intersection: #{(s1 & s2).to_a}  diff: #{(s1 - s2).to_a}"

  # --- Enumerable showcase ---
  nums = (1..10).to_a
  puts "map:       #{nums.map { |n| n * 2 }}"
  puts "select:    #{nums.select(&:even?)}"
  puts "reject:    #{nums.reject(&:even?)}"
  puts "reduce:    #{nums.reduce(0, :+)}"
  puts "group_by:  #{nums.group_by { |n| n % 3 }}"
  puts "flat_map:  #{[[1, 2], [3, 4]].flat_map { |a| a.map { |x| x * 10 } }}"
  puts "zip:       #{[1, 2, 3].zip(['a', 'b', 'c'])}"
  puts "each_with_object: #{nums.each_with_object({}) { |n, h| h[n] = n**2 }.take(5).to_h}"
  puts "tally:     #{%w[a b a c b a].tally}"
  puts "min_by:    #{%w[apple fig banana].min_by(&:length)}"
  puts "chunk:     #{nums.chunk { |n| n <= 5 }.map { |key, vals| [key, vals] }}"
end

# ============================================================
#  3. BLOCKS, PROCS, LAMBDAS
# ============================================================
def blocks_procs_lambdas
  section("3. BLOCKS / PROCS / LAMBDAS")

  # --- Blocks & yield ---
  def with_timing
    start = Process.clock_gettime(Process::CLOCK_MONOTONIC)
    result = yield
    elapsed = Process.clock_gettime(Process::CLOCK_MONOTONIC) - start
    puts "  Elapsed: #{(elapsed * 1000).round(3)}ms, Result: #{result}"
  end

  with_timing { (1..1000).reduce(:+) }

  # --- Explicit &block ---
  def capture_block(&blk)
    puts "  Block class: #{blk.class}, arity: #{blk.arity}"
    blk.call(10)
  end
  capture_block { |x| puts "  Block received: #{x}" }

  # --- Proc vs Lambda ---
  my_proc = Proc.new { |x, y| "proc: #{x}, #{y}" }
  my_lambda = ->(x, y) { "lambda: #{x}, #{y}" }
  puts "Proc (missing arg): #{my_proc.call(1)}"       # y is nil
  puts "Lambda: #{my_lambda.call(1, 2)}"
  puts "Proc lambda?: #{my_proc.lambda?}  Lambda lambda?: #{my_lambda.lambda?}"

  # --- Method objects ---
  method_obj = method(:puts)
  puts "Method object: #{method_obj.class}, name: #{method_obj.name}"
  [1, 2, 3].each(&method(:puts))

  # --- Currying ---
  adder = ->(a, b) { a + b }
  add5 = adder.curry.(5)
  puts "Curried: add5.(10) = #{add5.(10)}"
end

# ============================================================
#  4. OOP
# ============================================================
def oop_demo
  section("4. OOP — Classes, Modules, Mixins, Open Classes")

  # --- Basic class ---
  class Animal
    attr_accessor :name, :sound

    def initialize(name, sound)
      @name = name
      @sound = sound
    end

    def speak
      "#{@name} says #{@sound}"
    end

    def to_s
      "Animal(#{@name})"
    end
  end

  # --- Inheritance ---
  class Dog < Animal
    def initialize(name)
      super(name, "Woof")
    end

    def fetch(item)
      "#{@name} fetches the #{item}!"
    end
  end

  dog = Dog.new("Rex")
  puts dog.speak
  puts dog.fetch("ball")

  # --- Modules as mixins ---
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

  puts Person.new("Alice").greet
  puts "Person ancestors: #{Person.ancestors.take(4)}"

  # --- method_missing & respond_to_missing? ---
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

  proxy = DynamicProxy.new
  puts proxy.say_hello
  puts "responds to say_hi? #{proxy.respond_to?(:say_hi)}"

  # --- Open classes (monkey patching) ---
  class Integer
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

  # --- define_method ---
  class Talker
    %w[english spanish french].each do |lang|
      define_method("speak_#{lang}") do
        "Speaking #{lang.capitalize}!"
      end
    end
  end

  t = Talker.new
  puts t.speak_english
  puts t.speak_french

  # --- class_eval ---
  String.class_eval do
    def shout
      upcase + "!!!"
    end
  end
  puts "hello".shout

  # --- instance_eval ---
  obj = Object.new
  obj.instance_eval do
    @secret = 42
    def reveal
      @secret
    end
  end
  puts "instance_eval secret: #{obj.reveal}"

  # --- Hook: method_added ---
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
  puts "Tracked methods: #{Tracked.tracked_methods}"

  # --- const_missing ---
  module AutoConst
    def self.const_missing(name)
      "Auto-generated constant: #{name}"
    end
  end
  puts AutoConst::ANYTHING
end

# ============================================================
#  6. FUNCTIONAL PATTERNS
# ============================================================
def functional_demo
  section("6. FUNCTIONAL — Freeze, Comparable, Lazy Enumerators")

  # --- Frozen / immutable ---
  frozen_arr = [1, 2, 3].freeze
  begin
    frozen_arr << 4
  rescue => e
    puts "FrozenError: #{e.message}"
  end

  # --- Comparable ---
  class Temperature
    include Comparable
    attr_reader :degrees

    def initialize(degrees)
      @degrees = degrees
    end

    def <=>(other)
      @degrees <=> other.degrees
    end

    def to_s
      "#{@degrees}°"
    end
  end

  temps = [30, 20, 25, 15].map { |d| Temperature.new(d) }
  puts "Sorted temps: #{temps.sort}"
  puts "Max: #{temps.max}  Min: #{temps.min}"
  puts "Between? #{Temperature.new(22).between?(Temperature.new(20), Temperature.new(25))}"

  # --- Lazy enumerators ---
  lazy_result = (1..Float::INFINITY).lazy
    .select { |n| n.odd? }
    .map { |n| n ** 2 }
    .first(5)
  puts "Lazy odd squares: #{lazy_result}"

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
  Point = Struct.new(:x, :y) do
    def distance_to(other)
      Math.sqrt((x - other.x)**2 + (y - other.y)**2)
    end
  end

  p1 = Point.new(0, 0)
  p2 = Point.new(3, 4)
  puts "Point: #{p1}  Distance: #{p1.distance_to(p2)}"
  puts "Struct members: #{Point.members}"

  # --- OpenStruct ---
  config = OpenStruct.new(host: "localhost", port: 8080)
  config.debug = true
  puts "OpenStruct: host=#{config.host} port=#{config.port} debug=#{config.debug}"

  # --- Pattern matching (Ruby 3+) ---
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

  # Array pattern
  case [1, 2, 3, 4, 5]
  in [Integer => first, Integer => second, *rest]
    puts "Array pattern: first=#{first}, second=#{second}, rest=#{rest}"
  end

  # Find pattern
  case [1, 2, 3, "hello", 4]
  in [*, String => s, *]
    puts "Find pattern found string: #{s}"
  end

  # Pin operator
  expected = 42
  case { value: 42 }
  in { value: ^expected }
    puts "Pin operator matched expected value: #{expected}"
  end

  # --- Ractor (Ruby 3+ actor-based concurrency) ---
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
