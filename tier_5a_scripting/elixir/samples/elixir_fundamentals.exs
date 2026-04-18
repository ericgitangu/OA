# Elixir Fundamentals: Beginner to Advanced — Standard Library Only.
#
# A dense, runnable syntax reference covering core Elixir concepts.
# Run: elixir elixir_fundamentals.exs
# Requires: Elixir 1.12+
#
# Elixir runs on the BEAM VM (Bogdan/Bjorn's Erlang Abstract Machine), which was
# designed for telecom systems requiring 99.999% uptime. The BEAM gives Elixir:
# - Lightweight processes (not OS threads) — you can spawn millions of them
# - Per-process garbage collection — no stop-the-world pauses
# - Preemptive scheduling — no single process can starve others
# - Hot code reloading — update running systems without downtime
# All data in Elixir is immutable. "Updating" a value creates a new value;
# the runtime uses structural sharing to make this efficient.

defmodule Section do
  def print(title) do
    IO.puts("\n#{String.duplicate("=", 60)}")
    IO.puts("  #{title}")
    IO.puts(String.duplicate("=", 60))
  end
end

# ============================================================
#  1. BASICS
# ============================================================
Section.print("1. BASICS — Atoms, Tuples, Lists, Maps, Strings")

# Atoms are constants whose name IS their value — like Ruby symbols or Lisp keywords.
# They're stored in a global atom table (never garbage collected) for O(1) comparison.
# true, false, and nil are just atoms (:true, :false, :nil). Module names are also atoms.
IO.puts("Atoms: #{:hello}  #{:ok}  #{true}  #{nil}")  # => Atoms: hello  ok  true
IO.puts("Atom = bool? #{is_atom(true)}  nil is atom? #{is_atom(nil)}")  # => Atom = bool? true  nil is atom? true

# Elixir has arbitrary-precision integers (no overflow) and IEEE 754 floats.
# Underscore separators are allowed: 1_000_000 for readability.
int = 42
float = 3.14
IO.puts("Integer: #{int}  Float: #{float}  Hex: #{0xFF}  Binary: #{0b1010}")  # => Integer: 42  Float: 3.14  Hex: 255  Binary: 10
IO.puts("Integer math: div=#{div(10, 3)}  rem=#{rem(10, 3)}")  # => Integer math: div=3  rem=1

# Tuples are stored contiguously in memory — O(1) access by index, but O(n) to update
# because the entire tuple must be copied. Use tuples for small, fixed-size groups.
# The {:ok, value} / {:error, reason} convention is the BEAM's way of handling errors
# without exceptions — functions return tagged tuples that callers pattern match on.
point = {3, 4}
IO.puts("Tuple: #{inspect(point)}  elem(1): #{elem(point, 1)}  size: #{tuple_size(point)}")  # => Tuple: {3, 4}  elem(1): 4  size: 2
updated = put_elem(point, 0, 10)
IO.puts("put_elem: #{inspect(updated)}")  # => put_elem: {10, 4}

# Lists are linked lists — O(1) prepend, O(n) access by index, O(n) length.
# [head | tail] is the cons cell pattern, fundamental to all BEAM/Lisp languages.
# Because data is immutable, prepending shares the entire tail — zero copying.
list = [1, 2, 3, 4, 5]
IO.puts("List: #{inspect(list)}  hd: #{hd(list)}  tl: #{inspect(tl(list))}")  # => List: [1, 2, 3, 4, 5]  hd: 1  tl: [2, 3, 4, 5]
IO.puts("Prepend: #{inspect([0 | list])}  Concat: #{inspect(list ++ [6, 7])}")  # => Prepend: [0, 1, 2, 3, 4, 5]  Concat: [1, 2, 3, 4, 5, 6, 7]
IO.puts("Length: #{length(list)}  Flatten: #{inspect(List.flatten([[1, 2], [3, [4]]]))}")  # => Length: 5  Flatten: [1, 2, 3, 4]

# Keyword lists are lists of {key, value} tuples. They allow duplicate keys and
# maintain insertion order. They're the idiomatic way to pass options to functions.
# Syntactic sugar: [host: "localhost"] is [{:host, "localhost"}].
opts = [host: "localhost", port: 5432, ssl: true]
IO.puts("Keyword: #{inspect(opts)}  host: #{opts[:host]}")  # => Keyword: [host: "localhost", port: 5432, ssl: true]  host: localhost

# Maps are Elixir's key-value store — any type as key, O(log n) access.
# Small maps (<= 32 keys) are sorted lists; larger maps use Hash Array Mapped Tries (HAMT).
# The %{key: value} syntax creates atom keys; %{"key" => value} allows any key type.
# Updating with %{map | key: new_value} enforces that the key already exists (safety check).
user = %{name: "Alice", age: 30, role: :admin}
IO.puts("Map: #{inspect(user)}  name: #{user.name}")  # => Map: %{name: "Alice", age: 30, role: :admin}  name: Alice
updated_user = %{user | age: 31}
IO.puts("Updated: #{inspect(updated_user)}")  # => Updated: %{name: "Alice", age: 31, role: :admin}
IO.puts("Map.get: #{Map.get(user, :missing, "default")}")  # => Map.get: default
IO.puts("Map.keys: #{inspect(Map.keys(user))}")  # => Map.keys: [:age, :name, :role]

# Strings are UTF-8 encoded binaries. Charlists (~c"...") are lists of codepoints.
# Strings and charlists are different types — strings for modern Elixir code,
# charlists for Erlang interop (Erlang uses charlists natively).
str = "Hello"
charlist = ~c"Hello"
IO.puts("String: #{str}  Charlist: #{inspect(charlist)}")  # => String: Hello  Charlist: ~c"Hello"
IO.puts("Interpolation: #{"1 + 1 = #{1 + 1}"}")  # => Interpolation: 1 + 1 = 2
IO.puts("String.split: #{inspect(String.split("a,b,c", ","))}")  # => String.split: ["a", "b", "c"]
IO.puts("String.upcase: #{String.upcase(str)}  reverse: #{String.reverse(str)}")  # => String.upcase: HELLO  reverse: olleH

# ============================================================
#  2. PATTERN MATCHING
# ============================================================
Section.print("2. PATTERN MATCHING — =, Pin, Destructuring, Function Clauses")

# In Elixir, = is the MATCH operator, not assignment. The left side is a pattern.
# When you write x = 42, Elixir binds x to 42 to make the pattern match succeed.
# This is fundamentally different from imperative assignment — it's declarative.
x = 42
{a, b} = {1, 2}
IO.puts("Match: x=#{x}  a=#{a}  b=#{b}")  # => Match: x=42  a=1  b=2

# [head | tail] destructures a list into its first element and the rest.
# This is how you process lists recursively — the fundamental pattern in functional programming.
[head | tail] = [10, 20, 30]
IO.puts("Head: #{head}  Tail: #{inspect(tail)}")  # => Head: 10  Tail: [20, 30]

# The pin operator (^) prevents rebinding — it matches against the variable's current value.
# Without ^, pattern matching always succeeds by binding a new value.
# This is critical when you want to assert equality, not just capture.
pinned = 42
case 42 do
  ^pinned -> IO.puts("Pin matched: #{pinned}")  # => Pin matched: 42
  _ -> IO.puts("No match")  # => No match
end

# Maps can be partially matched — you only need to specify the keys you care about.
# The remaining keys are ignored. This is different from tuples where size must match exactly.
%{name: name, role: role} = %{name: "Bob", age: 25, role: :user}
IO.puts("Map destructure: name=#{name}  role=#{role}")  # => Map destructure: name=Bob  role=user

# Function clauses are the BEAM's version of polymorphism.
# Instead of if/else chains inside a function, you define multiple clauses with different
# patterns. The BEAM compiles these into efficient pattern-matching jump tables.
# Guards (when) add additional constraints that patterns alone can't express.
defmodule Greeting do
  def greet(:morning), do: "Good morning!"
  def greet(:evening), do: "Good evening!"
  def greet(name) when is_binary(name), do: "Hello, #{name}!"
  def greet(_), do: "Hello!"
end

IO.puts(Greeting.greet(:morning))  # => Good morning!
IO.puts(Greeting.greet("Alice"))  # => Hello, Alice!

# ============================================================
#  3. COLLECTIONS — Enum & Stream
# ============================================================
Section.print("3. COLLECTIONS — Enum, Stream")

# The pipe operator |> passes the result of the left expression as the first argument
# to the function on the right. This transforms nested calls into readable pipelines.
# data |> transform1() |> transform2() instead of transform2(transform1(data)).
nums = 1..10 |> Enum.to_list()

# Enum is Elixir's workhorse module for eager collection processing.
# All Enum functions work on any data type that implements the Enumerable protocol.
IO.puts("map:      #{inspect(Enum.map(nums, &(&1 * 2)))}")  # => map:      [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
IO.puts("filter:   #{inspect(Enum.filter(nums, &(rem(&1, 2) == 0)))}")  # => filter:   [2, 4, 6, 8, 10]

# &+/2 is the capture syntax for the built-in + operator with arity 2.
# &(&1 * 2) is shorthand for fn x -> x * 2 end. &1 refers to the first argument.
IO.puts("reduce:   #{Enum.reduce(nums, 0, &+/2)}")  # => reduce:   55
IO.puts("group_by: #{inspect(Enum.group_by(nums, &(rem(&1, 3))))}")  # => group_by: %{0 => [3, 6, 9], 1 => [1, 4, 7, 10], 2 => [2, 5, 8]}
IO.puts("zip:      #{inspect(Enum.zip([1, 2, 3], [:a, :b, :c]))}")  # => zip:      [{1, :a}, {2, :b}, {3, :c}]
IO.puts("chunk_by: #{inspect(Enum.chunk_by([1, 1, 2, 2, 3], & &1))}")  # => chunk_by: [[1, 1], [2, 2], [3]]
IO.puts("sort_by:  #{inspect(Enum.sort_by(["banana", "fig", "apple"], &String.length/1))}")  # => sort_by:  ["fig", "apple", "banana"]
IO.puts("min_max:  #{inspect(Enum.min_max(nums))}")  # => min_max:  {1, 10}
IO.puts("frequencies: #{inspect(Enum.frequencies(~w(a b a c b a)))}")  # => frequencies: %{"a" => 3, "b" => 2, "c" => 1}
IO.puts("flat_map: #{inspect(Enum.flat_map([[1, 2], [3, 4]], & &1))}")  # => flat_map: [1, 2, 3, 4]

# Stream is the lazy counterpart to Enum. It builds a pipeline of transformations
# that only execute when a terminal operation (like Enum.take) consumes values.
# This avoids creating intermediate lists — critical for large or infinite sequences.
# Internally, Streams compose functions; they don't iterate until forced.
lazy_result =
  Stream.iterate(1, &(&1 + 1))
  |> Stream.filter(&(rem(&1, 2) == 1))
  |> Stream.map(&(&1 * &1))
  |> Enum.take(5)

IO.puts("Stream (lazy odd squares): #{inspect(lazy_result)}")  # => Stream (lazy odd squares): [1, 9, 25, 49, 81]

# Stream.unfold generates a sequence from a state function.
# Each step returns {value_to_emit, next_state} or nil to stop.
# This is how you create infinite sequences from a seed value.
fibs =
  Stream.unfold({0, 1}, fn {a, b} -> {a, {b, a + b}} end)
  |> Enum.take(10)

IO.puts("Fibonacci: #{inspect(fibs)}")  # => Fibonacci: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# ============================================================
#  4. FUNCTIONS
# ============================================================
Section.print("4. FUNCTIONS — Anonymous, Capture, Pipeline, Guards")

# Anonymous functions use fn -> end syntax. Note the dot in add.(3, 4) —
# Elixir requires it to distinguish anonymous function calls from named function calls.
# This is because named and anonymous functions live in different namespaces.
add = fn a, b -> a + b end
IO.puts("Anonymous: #{add.(3, 4)}")  # => Anonymous: 7

# The capture operator & creates anonymous functions from expressions.
# &(&1 * 2) is equivalent to fn x -> x * 2 end.
# &String.upcase/1 captures a named function — the /1 specifies arity.
double = &(&1 * 2)
IO.puts("Capture: #{double.(21)}")  # => Capture: 42

to_upper = &String.upcase/1
IO.puts("Named capture: #{to_upper.("hello")}")  # => Named capture: HELLO

# The pipeline operator |> is Elixir's signature feature. It makes data flow explicit
# and reads top-to-bottom instead of inside-out. Each step transforms and passes forward.
result =
  "  Hello, World!  "
  |> String.trim()
  |> String.downcase()
  |> String.split()
  |> Enum.join("-")

IO.puts("Pipeline: #{result}")  # => Pipeline: hello,-world!

# Guards are compile-time checks that extend pattern matching.
# Only a limited set of expressions are allowed in guards (no custom functions) because
# guards must be side-effect-free — the BEAM needs to guarantee they can't crash.
defmodule TypeChecker do
  def check(x) when is_integer(x) and x > 0, do: "positive integer"
  def check(x) when is_integer(x), do: "non-positive integer"
  def check(x) when is_float(x), do: "float"
  def check(x) when is_binary(x), do: "string"
  def check(x) when is_list(x), do: "list"
  def check(_), do: "other"
end

IO.puts("Guard: #{TypeChecker.check(42)}")  # => Guard: positive integer
IO.puts("Guard: #{TypeChecker.check(-1)}")  # => Guard: non-positive integer
IO.puts("Guard: #{TypeChecker.check("hi")}")  # => Guard: string

# Default arguments use \\ syntax. Under the hood, Elixir generates multiple
# function clauses — one for each arity — so default args are just clause dispatch.
defmodule Defaults do
  def greet(name, greeting \\ "Hello") do
    "#{greeting}, #{name}!"
  end
end

IO.puts("Default: #{Defaults.greet("Alice")}")  # => Default: Hello, Alice!
IO.puts("Custom:  #{Defaults.greet("Alice", "Hey")}")  # => Custom:  Hey, Alice!

# ============================================================
#  5. MODULES
# ============================================================
Section.print("5. MODULES — defmodule, Attributes, use/import/alias")

# Modules are the primary code organization unit in Elixir — there are no classes.
# Module attributes (@attr) are compile-time constants inlined at every usage site.
# @moduledoc and @doc generate documentation accessible via `h Module` in IEx.
defmodule MathUtils do
  @moduledoc "Math utility functions"
  @pi 3.14159265

  def circle_area(r), do: @pi * r * r

  # defp defines a private function — only callable within this module.
  # There's no protected visibility in Elixir; it's either public or private.
  defp square(x), do: x * x

  # Elixir can call Erlang modules directly with :module syntax.
  # :math.sqrt calls Erlang's math:sqrt — the entire Erlang ecosystem is available.
  def hypotenuse(a, b) do
    :math.sqrt(square(a) + square(b))
  end
end

IO.puts("Circle area: #{MathUtils.circle_area(5)}")  # => Circle area: 78.53981625
IO.puts("Hypotenuse: #{MathUtils.hypotenuse(3, 4)}")  # => Hypotenuse: 5.0

# Structs are maps with a fixed set of keys and default values, backed by a module.
# @enforce_keys makes certain keys required at creation time — compile-time safety.
# Structs enable pattern matching on the struct name: %User{name: n} only matches User structs.
# Under the hood, structs are maps with a __struct__ key pointing to the module.
defmodule User do
  @enforce_keys [:name]
  defstruct name: nil, age: 0, role: :user

  def adult?(%User{age: age}), do: age >= 18
end

alice = %User{name: "Alice", age: 30, role: :admin}
IO.puts("Struct: #{inspect(alice)}  adult? #{User.adult?(alice)}")  # => Struct: %User{name: "Alice", age: 30, role: :admin}  adult? true
IO.puts("Update: #{inspect(%User{alice | age: 31})}")  # => Update: %User{name: "Alice", age: 31, role: :admin}

# ============================================================
#  6. OTP BASICS
# ============================================================
Section.print("6. OTP — GenServer, Agent, Task, Supervisor")

# GenServer (Generic Server) is the OTP abstraction for stateful processes.
# It separates the client API (cast/call) from server callbacks (handle_cast/handle_call).
# The BEAM VM gives each process its own heap — no shared memory, no locks.
# call is synchronous (blocks until reply), cast is asynchronous (fire-and-forget).
# This actor model means state is never shared — processes communicate only via messages.
defmodule Counter do
  use GenServer

  # Client API — these functions run in the CALLER's process.
  # They send messages to the GenServer process and (for call) wait for a reply.
  def start_link(initial \\ 0), do: GenServer.start_link(__MODULE__, initial)
  def increment(pid), do: GenServer.call(pid, :increment)
  def get(pid), do: GenServer.call(pid, :get)
  def reset(pid), do: GenServer.cast(pid, :reset)

  # Server callbacks — these run in the GenServer's OWN process.
  # @impl true tells the compiler these implement behaviour callbacks (catches typos).
  @impl true
  def init(initial), do: {:ok, initial}

  # handle_call must return {:reply, response, new_state}.
  # The second arg (_from) contains the caller's PID and a reference for the reply.
  @impl true
  def handle_call(:increment, _from, state), do: {:reply, state + 1, state + 1}
  def handle_call(:get, _from, state), do: {:reply, state, state}

  # handle_cast returns {:noreply, new_state} — the caller doesn't wait for a response.
  @impl true
  def handle_cast(:reset, _state), do: {:noreply, 0}
end

{:ok, counter} = Counter.start_link(0)
Counter.increment(counter)
Counter.increment(counter)
Counter.increment(counter)
IO.puts("GenServer counter: #{Counter.get(counter)}")  # => GenServer counter: 3
Counter.reset(counter)
IO.puts("After reset: #{Counter.get(counter)}")  # => After reset: 0
GenServer.stop(counter)

# Agent is a simplified GenServer for when you only need to store and retrieve state.
# It wraps GenServer with a simpler API — no need to define callback modules.
# Use Agent for simple state; use GenServer when you need custom message handling.
{:ok, agent} = Agent.start_link(fn -> [] end)
Agent.update(agent, fn list -> ["hello" | list] end)
Agent.update(agent, fn list -> ["world" | list] end)
IO.puts("Agent: #{inspect(Agent.get(agent, & &1))}")  # => Agent: ["world", "hello"]
Agent.stop(agent)

# Task wraps a computation in a process for concurrent execution.
# Task.async/await is like a future/promise — start work, do other things, collect result.
# Tasks are linked to the caller — if the task crashes, the caller crashes too.
task = Task.async(fn -> :timer.sleep(10); 42 end)
result = Task.await(task)
IO.puts("Task result: #{result}")  # => Task result: 42

# Task.await_many waits for multiple concurrent tasks — like Promise.all in JavaScript.
tasks = Enum.map(1..5, fn i -> Task.async(fn -> i * i end) end)
results = Task.await_many(tasks)
IO.puts("Task.await_many: #{inspect(results)}")  # => Task.await_many: [1, 4, 9, 16, 25]

# ============================================================
#  7. CONCURRENCY
# ============================================================
Section.print("7. CONCURRENCY — spawn, send/receive, Process")

# spawn creates a new BEAM process — extremely lightweight (~2KB initial memory).
# BEAM processes are not OS threads; the VM schedules them across OS threads (schedulers).
# Each process has its own heap, so GC for one process doesn't affect others.
# send/receive is the actor model: processes communicate only through message passing.
parent = self()

child = spawn(fn ->
  receive do
    {:greet, name} -> send(parent, {:response, "Hello, #{name}!"})
  end
end)

send(child, {:greet, "Elixir"})

# receive blocks until a matching message arrives in the process mailbox.
# The `after` clause provides a timeout — essential to avoid hanging indefinitely.
# Messages that don't match any clause stay in the mailbox (can cause memory issues).
receive do
  {:response, msg} -> IO.puts("Received: #{msg}")  # => Received: Hello, Elixir!
after
  1000 -> IO.puts("Timeout!")  # => Timeout!
end

IO.puts("Self PID: #{inspect(self())}")  # => (varies)
IO.puts("Alive? #{Process.alive?(self())}")  # => Alive? true

# spawn_link creates a linked process. Links are bidirectional — if either process crashes,
# the other crashes too. This is the foundation of OTP's "let it crash" philosophy:
# instead of defensive error handling, let processes crash and let supervisors restart them.
defmodule LinkDemo do
  def run do
    parent = self()
    spawn_link(fn ->
      send(parent, {:linked, "I'm linked to parent"})
    end)

    receive do
      {:linked, msg} -> IO.puts("Linked: #{msg}")  # => Linked: I'm linked to parent
    after
      1000 -> IO.puts("Timeout")  # => Timeout
    end
  end
end

LinkDemo.run()

# spawn_monitor is one-directional (unlike links). The monitoring process receives a
# :DOWN message when the monitored process exits, without crashing itself.
# Use monitors when you need to observe a process without coupling your fate to it.
{pid, ref} = spawn_monitor(fn -> :timer.sleep(10) end)
receive do
  {:DOWN, ^ref, :process, ^pid, reason} ->
    IO.puts("Monitored process exited: #{inspect(reason)}")  # => Monitored process exited: :normal
after
  1000 -> IO.puts("Timeout")  # => Timeout
end

# ============================================================
#  8. PROTOCOLS
# ============================================================
Section.print("8. PROTOCOLS — defprotocol, defimpl")

# Protocols are Elixir's mechanism for polymorphism — similar to interfaces or type classes.
# Unlike OOP inheritance, protocols are open: you can implement a protocol for any type,
# even types you didn't define (like built-in BitString below).
# Protocol dispatch is resolved at runtime based on the data type of the first argument.
# Protocols are how Enum works with lists, maps, ranges — they all implement Enumerable.
defprotocol Describable do
  @doc "Returns a description of the data"
  def describe(data)
end

defmodule Dog do
  defstruct [:name, :breed]
end

defmodule Cat do
  defstruct [:name, :indoor]
end

# defimpl implements a protocol for a specific type.
# Each type gets its own implementation — no inheritance hierarchy needed.
defimpl Describable, for: Dog do
  def describe(dog), do: "#{dog.name} the #{dog.breed} dog"
end

defimpl Describable, for: Cat do
  def describe(cat), do: "#{cat.name} the #{if cat.indoor, do: "indoor", else: "outdoor"} cat"
end

# Implementing a protocol for a built-in type — this is the "open" part.
# You can add protocol implementations for types defined anywhere, at any time.
defimpl Describable, for: BitString do
  def describe(str), do: "String '#{str}' (#{String.length(str)} chars)"
end

IO.puts(Describable.describe(%Dog{name: "Rex", breed: "Lab"}))  # => Rex the Lab dog
IO.puts(Describable.describe(%Cat{name: "Whiskers", indoor: true}))  # => Whiskers the indoor cat
IO.puts(Describable.describe("Hello"))  # => String 'Hello' (5 chars)

# ============================================================
#  9. ADVANCED
# ============================================================
Section.print("9. ADVANCED — Macros, Behaviours, Comprehensions, With, Sigils")

# Comprehensions (for) are syntactic sugar for mapping, filtering, and collecting.
# They combine generators (<-), filters, and a collector (into:) in one expression.
squares = for n <- 1..5, do: n * n
IO.puts("Comprehension: #{inspect(squares)}")  # => Comprehension: [1, 4, 9, 16, 25]

# Multiple generators create a cartesian product; filters narrow the results.
combos = for x <- 1..3, y <- 1..3, x != y, do: {x, y}
IO.puts("Multi-gen: #{inspect(combos)}")  # => Multi-gen: [{1, 2}, {1, 3}, {2, 1}, {2, 3}, {3, 1}, {3, 2}]

# into: specifies the output collection type — the comprehension uses the Collectable protocol.
letter_map = for {k, v} <- Enum.with_index(~w(a b c)), into: %{}, do: {k, v}
IO.puts("Into map: #{inspect(letter_map)}")  # => Into map: %{"a" => 0, "b" => 1, "c" => 2}

# `with` chains pattern matches, short-circuiting on the first failure.
# It's like a railway-oriented programming pattern — if any match fails,
# execution jumps to the `else` block. This replaces nested case statements.
defmodule Parser do
  def parse_config(data) do
    with {:ok, name} <- Map.fetch(data, :name),
         {:ok, port} <- Map.fetch(data, :port),
         true <- is_integer(port) do
      {:ok, "#{name}:#{port}"}
    else
      :error -> {:error, "missing field"}
      false -> {:error, "port must be integer"}
    end
  end
end

IO.puts("With ok:    #{inspect(Parser.parse_config(%{name: "app", port: 8080}))}")  # => With ok:    {:ok, "app:8080"}
IO.puts("With error: #{inspect(Parser.parse_config(%{name: "app"}))}")  # => With error: {:error, "missing field"}

# Sigils are shortcuts for common data types. ~ prefix + letter + delimiters.
# ~w creates a word list (like %w in Ruby), ~r creates a regex.
# You can define custom sigils with sigil_x/2 functions.
IO.puts("Sigil ~w: #{inspect(~w(hello world foo))}")  # => Sigil ~w: ["hello", "world", "foo"]
IO.puts("Sigil ~r: #{inspect(Regex.match?(~r/^\d+$/, "123"))}")  # => Sigil ~r: true

# Behaviours define a set of callbacks a module must implement — like interfaces in OOP.
# The compiler verifies at compile time that all required callbacks are present.
# OTP modules (GenServer, Supervisor) are behaviours — `use GenServer` sets up the behaviour.
defmodule Serializer do
  @callback encode(term()) :: {:ok, String.t()} | {:error, String.t()}
  @callback decode(String.t()) :: {:ok, term()} | {:error, String.t()}
end

defmodule JsonSerializer do
  @behaviour Serializer

  @impl Serializer
  def encode(term), do: {:ok, inspect(term)}

  @impl Serializer
  def decode(str), do: {:ok, str}
end

IO.puts("Behaviour: #{inspect(JsonSerializer.encode(%{key: "value"}))}")  # => Behaviour: {:ok, "%{key: \"value\"}"}

# Macros are code that writes code — they operate on the AST (Abstract Syntax Tree).
# Elixir code is homoiconic: it can be represented as Elixir data structures (tuples of
# {function, metadata, arguments}). quote captures code as AST, unquote injects values into it.
# Macros run at compile time, so they have zero runtime cost.
# Most Elixir "keywords" (if, unless, def, defmodule) are actually macros.
defmodule MyMacros do
  defmacro say(expression) do
    string = Macro.to_string(expression)
    quote do
      IO.puts("#{unquote(string)} => #{inspect(unquote(expression))}")
    end
  end

  # This macro transforms into an if expression at compile time.
  # The generated code has no macro overhead — it's just an if statement.
  defmacro unless(condition, do: block) do
    quote do
      if !unquote(condition), do: unquote(block)
    end
  end
end

defmodule MacroDemo do
  require MyMacros

  def run do
    MyMacros.say(1 + 2 * 3)
    MyMacros.say(Enum.map(1..3, &(&1 * 10)))
    MyMacros.unless false do
      IO.puts("unless macro: this prints because condition is false")  # => unless macro: this prints because condition is false
    end
  end
end

MacroDemo.run()

# Error handling in Elixir favors {:ok, value} / {:error, reason} tuples over exceptions.
# Exceptions exist (raise/rescue) but are reserved for truly unexpected situations.
# The BEAM philosophy is "let it crash" — supervisors restart failed processes rather
# than trying to handle every possible error inline.
defmodule SafeDiv do
  def divide(_, 0), do: {:error, :division_by_zero}
  def divide(a, b), do: {:ok, a / b}
end

case SafeDiv.divide(10, 3) do
  {:ok, result} -> IO.puts("Division: #{result}")  # => Division: 3.3333333333333335
  {:error, reason} -> IO.puts("Error: #{reason}")  # => Error: <reason>
end

# try/rescue is available but discouraged for control flow.
# Use it only for interop with libraries that raise, or truly exceptional conditions.
try do
  raise "something went wrong"
rescue
  e in RuntimeError -> IO.puts("Rescued: #{e.message}")  # => Rescued: something went wrong
after
  IO.puts("After block always runs")  # => After block always runs
end

# ============================================================
#  DONE
# ============================================================
IO.puts("\n#{String.duplicate("=", 60)}")
IO.puts("  All sections complete!")  # => All sections complete!
IO.puts(String.duplicate("=", 60))
