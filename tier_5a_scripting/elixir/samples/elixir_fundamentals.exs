# Elixir Fundamentals: Beginner to Advanced — Standard Library Only.
#
# A dense, runnable syntax reference covering core Elixir concepts.
# Run: elixir elixir_fundamentals.exs
# Requires: Elixir 1.12+

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

# --- Atoms ---
IO.puts("Atoms: #{:hello}  #{:ok}  #{true}  #{nil}")
IO.puts("Atom = bool? #{is_atom(true)}  nil is atom? #{is_atom(nil)}")

# --- Numbers ---
int = 42
float = 3.14
IO.puts("Integer: #{int}  Float: #{float}  Hex: #{0xFF}  Binary: #{0b1010}")
IO.puts("Integer math: div=#{div(10, 3)}  rem=#{rem(10, 3)}")

# --- Tuples ---
point = {3, 4}
IO.puts("Tuple: #{inspect(point)}  elem(1): #{elem(point, 1)}  size: #{tuple_size(point)}")
updated = put_elem(point, 0, 10)
IO.puts("put_elem: #{inspect(updated)}")

# --- Lists ---
list = [1, 2, 3, 4, 5]
IO.puts("List: #{inspect(list)}  hd: #{hd(list)}  tl: #{inspect(tl(list))}")
IO.puts("Prepend: #{inspect([0 | list])}  Concat: #{inspect(list ++ [6, 7])}")
IO.puts("Length: #{length(list)}  Flatten: #{inspect(List.flatten([[1, 2], [3, [4]]]))}")

# --- Keyword lists ---
opts = [host: "localhost", port: 5432, ssl: true]
IO.puts("Keyword: #{inspect(opts)}  host: #{opts[:host]}")

# --- Maps ---
user = %{name: "Alice", age: 30, role: :admin}
IO.puts("Map: #{inspect(user)}  name: #{user.name}")
updated_user = %{user | age: 31}
IO.puts("Updated: #{inspect(updated_user)}")
IO.puts("Map.get: #{Map.get(user, :missing, "default")}")
IO.puts("Map.keys: #{inspect(Map.keys(user))}")

# --- Strings vs Charlists ---
str = "Hello"
charlist = ~c"Hello"
IO.puts("String: #{str}  Charlist: #{inspect(charlist)}")
IO.puts("Interpolation: #{"1 + 1 = #{1 + 1}"}")
IO.puts("String.split: #{inspect(String.split("a,b,c", ","))}")
IO.puts("String.upcase: #{String.upcase(str)}  reverse: #{String.reverse(str)}")

# ============================================================
#  2. PATTERN MATCHING
# ============================================================
Section.print("2. PATTERN MATCHING — =, Pin, Destructuring, Function Clauses")

# --- Basic match ---
x = 42
{a, b} = {1, 2}
IO.puts("Match: x=#{x}  a=#{a}  b=#{b}")

[head | tail] = [10, 20, 30]
IO.puts("Head: #{head}  Tail: #{inspect(tail)}")

# --- Pin operator ---
pinned = 42
case 42 do
  ^pinned -> IO.puts("Pin matched: #{pinned}")
  _ -> IO.puts("No match")
end

# --- Destructuring maps ---
%{name: name, role: role} = %{name: "Bob", age: 25, role: :user}
IO.puts("Map destructure: name=#{name}  role=#{role}")

# --- Function clauses ---
defmodule Greeting do
  def greet(:morning), do: "Good morning!"
  def greet(:evening), do: "Good evening!"
  def greet(name) when is_binary(name), do: "Hello, #{name}!"
  def greet(_), do: "Hello!"
end

IO.puts(Greeting.greet(:morning))
IO.puts(Greeting.greet("Alice"))

# ============================================================
#  3. COLLECTIONS — Enum & Stream
# ============================================================
Section.print("3. COLLECTIONS — Enum, Stream")

nums = 1..10 |> Enum.to_list()

IO.puts("map:      #{inspect(Enum.map(nums, &(&1 * 2)))}")
IO.puts("filter:   #{inspect(Enum.filter(nums, &(rem(&1, 2) == 0)))}")
IO.puts("reduce:   #{Enum.reduce(nums, 0, &+/2)}")
IO.puts("group_by: #{inspect(Enum.group_by(nums, &(rem(&1, 3))))}")
IO.puts("zip:      #{inspect(Enum.zip([1, 2, 3], [:a, :b, :c]))}")
IO.puts("chunk_by: #{inspect(Enum.chunk_by([1, 1, 2, 2, 3], & &1))}")
IO.puts("sort_by:  #{inspect(Enum.sort_by(["banana", "fig", "apple"], &String.length/1))}")
IO.puts("min_max:  #{inspect(Enum.min_max(nums))}")
IO.puts("frequencies: #{inspect(Enum.frequencies(~w(a b a c b a)))}")
IO.puts("flat_map: #{inspect(Enum.flat_map([[1, 2], [3, 4]], & &1))}")

# --- Stream (lazy) ---
lazy_result =
  Stream.iterate(1, &(&1 + 1))
  |> Stream.filter(&(rem(&1, 2) == 1))
  |> Stream.map(&(&1 * &1))
  |> Enum.take(5)

IO.puts("Stream (lazy odd squares): #{inspect(lazy_result)}")

fibs =
  Stream.unfold({0, 1}, fn {a, b} -> {a, {b, a + b}} end)
  |> Enum.take(10)

IO.puts("Fibonacci: #{inspect(fibs)}")

# ============================================================
#  4. FUNCTIONS
# ============================================================
Section.print("4. FUNCTIONS — Anonymous, Capture, Pipeline, Guards")

# --- Anonymous functions ---
add = fn a, b -> a + b end
IO.puts("Anonymous: #{add.(3, 4)}")

# --- Capture operator ---
double = &(&1 * 2)
IO.puts("Capture: #{double.(21)}")

to_upper = &String.upcase/1
IO.puts("Named capture: #{to_upper.("hello")}")

# --- Pipeline operator ---
result =
  "  Hello, World!  "
  |> String.trim()
  |> String.downcase()
  |> String.split()
  |> Enum.join("-")

IO.puts("Pipeline: #{result}")

# --- Guards ---
defmodule TypeChecker do
  def check(x) when is_integer(x) and x > 0, do: "positive integer"
  def check(x) when is_integer(x), do: "non-positive integer"
  def check(x) when is_float(x), do: "float"
  def check(x) when is_binary(x), do: "string"
  def check(x) when is_list(x), do: "list"
  def check(_), do: "other"
end

IO.puts("Guard: #{TypeChecker.check(42)}")
IO.puts("Guard: #{TypeChecker.check(-1)}")
IO.puts("Guard: #{TypeChecker.check("hi")}")

# --- Default arguments ---
defmodule Defaults do
  def greet(name, greeting \\ "Hello") do
    "#{greeting}, #{name}!"
  end
end

IO.puts("Default: #{Defaults.greet("Alice")}")
IO.puts("Custom:  #{Defaults.greet("Alice", "Hey")}")

# ============================================================
#  5. MODULES
# ============================================================
Section.print("5. MODULES — defmodule, Attributes, use/import/alias")

defmodule MathUtils do
  @moduledoc "Math utility functions"
  @pi 3.14159265

  def circle_area(r), do: @pi * r * r

  # Private function
  defp square(x), do: x * x

  def hypotenuse(a, b) do
    :math.sqrt(square(a) + square(b))
  end
end

IO.puts("Circle area: #{MathUtils.circle_area(5)}")
IO.puts("Hypotenuse: #{MathUtils.hypotenuse(3, 4)}")

# --- Structs ---
defmodule User do
  @enforce_keys [:name]
  defstruct name: nil, age: 0, role: :user

  def adult?(%User{age: age}), do: age >= 18
end

alice = %User{name: "Alice", age: 30, role: :admin}
IO.puts("Struct: #{inspect(alice)}  adult? #{User.adult?(alice)}")
IO.puts("Update: #{inspect(%User{alice | age: 31})}")

# ============================================================
#  6. OTP BASICS
# ============================================================
Section.print("6. OTP — GenServer, Agent, Task, Supervisor")

# --- GenServer ---
defmodule Counter do
  use GenServer

  # Client API
  def start_link(initial \\ 0), do: GenServer.start_link(__MODULE__, initial)
  def increment(pid), do: GenServer.call(pid, :increment)
  def get(pid), do: GenServer.call(pid, :get)
  def reset(pid), do: GenServer.cast(pid, :reset)

  # Server callbacks
  @impl true
  def init(initial), do: {:ok, initial}

  @impl true
  def handle_call(:increment, _from, state), do: {:reply, state + 1, state + 1}
  def handle_call(:get, _from, state), do: {:reply, state, state}

  @impl true
  def handle_cast(:reset, _state), do: {:noreply, 0}
end

{:ok, counter} = Counter.start_link(0)
Counter.increment(counter)
Counter.increment(counter)
Counter.increment(counter)
IO.puts("GenServer counter: #{Counter.get(counter)}")
Counter.reset(counter)
IO.puts("After reset: #{Counter.get(counter)}")
GenServer.stop(counter)

# --- Agent ---
{:ok, agent} = Agent.start_link(fn -> [] end)
Agent.update(agent, fn list -> ["hello" | list] end)
Agent.update(agent, fn list -> ["world" | list] end)
IO.puts("Agent: #{inspect(Agent.get(agent, & &1))}")
Agent.stop(agent)

# --- Task ---
task = Task.async(fn -> :timer.sleep(10); 42 end)
result = Task.await(task)
IO.puts("Task result: #{result}")

tasks = Enum.map(1..5, fn i -> Task.async(fn -> i * i end) end)
results = Task.await_many(tasks)
IO.puts("Task.await_many: #{inspect(results)}")

# ============================================================
#  7. CONCURRENCY
# ============================================================
Section.print("7. CONCURRENCY — spawn, send/receive, Process")

# --- spawn & message passing ---
parent = self()

child = spawn(fn ->
  receive do
    {:greet, name} -> send(parent, {:response, "Hello, #{name}!"})
  end
end)

send(child, {:greet, "Elixir"})

receive do
  {:response, msg} -> IO.puts("Received: #{msg}")
after
  1000 -> IO.puts("Timeout!")
end

# --- Process info ---
IO.puts("Self PID: #{inspect(self())}")
IO.puts("Alive? #{Process.alive?(self())}")

# --- Linked processes ---
defmodule LinkDemo do
  def run do
    parent = self()
    spawn_link(fn ->
      send(parent, {:linked, "I'm linked to parent"})
    end)

    receive do
      {:linked, msg} -> IO.puts("Linked: #{msg}")
    after
      1000 -> IO.puts("Timeout")
    end
  end
end

LinkDemo.run()

# --- Process.monitor ---
{pid, ref} = spawn_monitor(fn -> :timer.sleep(10) end)
receive do
  {:DOWN, ^ref, :process, ^pid, reason} ->
    IO.puts("Monitored process exited: #{inspect(reason)}")
after
  1000 -> IO.puts("Timeout")
end

# ============================================================
#  8. PROTOCOLS
# ============================================================
Section.print("8. PROTOCOLS — defprotocol, defimpl")

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

defimpl Describable, for: Dog do
  def describe(dog), do: "#{dog.name} the #{dog.breed} dog"
end

defimpl Describable, for: Cat do
  def describe(cat), do: "#{cat.name} the #{if cat.indoor, do: "indoor", else: "outdoor"} cat"
end

# Protocol for built-in types
defimpl Describable, for: BitString do
  def describe(str), do: "String '#{str}' (#{String.length(str)} chars)"
end

IO.puts(Describable.describe(%Dog{name: "Rex", breed: "Lab"}))
IO.puts(Describable.describe(%Cat{name: "Whiskers", indoor: true}))
IO.puts(Describable.describe("Hello"))

# ============================================================
#  9. ADVANCED
# ============================================================
Section.print("9. ADVANCED — Macros, Behaviours, Comprehensions, With, Sigils")

# --- Comprehensions ---
squares = for n <- 1..5, do: n * n
IO.puts("Comprehension: #{inspect(squares)}")

# Multiple generators + filter
combos = for x <- 1..3, y <- 1..3, x != y, do: {x, y}
IO.puts("Multi-gen: #{inspect(combos)}")

# Into a map
letter_map = for {k, v} <- Enum.with_index(~w(a b c)), into: %{}, do: {k, v}
IO.puts("Into map: #{inspect(letter_map)}")

# --- With statement ---
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

IO.puts("With ok:    #{inspect(Parser.parse_config(%{name: "app", port: 8080}))}")
IO.puts("With error: #{inspect(Parser.parse_config(%{name: "app"}))}")

# --- Sigils ---
IO.puts("Sigil ~w: #{inspect(~w(hello world foo))}")
IO.puts("Sigil ~r: #{inspect(Regex.match?(~r/^\d+$/, "123"))}")

# --- Behaviours ---
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

IO.puts("Behaviour: #{inspect(JsonSerializer.encode(%{key: "value"}))}")

# --- Macros (basic) ---
defmodule MyMacros do
  defmacro say(expression) do
    string = Macro.to_string(expression)
    quote do
      IO.puts("#{unquote(string)} => #{inspect(unquote(expression))}")
    end
  end

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
      IO.puts("unless macro: this prints because condition is false")
    end
  end
end

MacroDemo.run()

# --- Error handling ---
defmodule SafeDiv do
  def divide(_, 0), do: {:error, :division_by_zero}
  def divide(a, b), do: {:ok, a / b}
end

case SafeDiv.divide(10, 3) do
  {:ok, result} -> IO.puts("Division: #{result}")
  {:error, reason} -> IO.puts("Error: #{reason}")
end

# try/rescue
try do
  raise "something went wrong"
rescue
  e in RuntimeError -> IO.puts("Rescued: #{e.message}")
after
  IO.puts("After block always runs")
end

# ============================================================
#  DONE
# ============================================================
IO.puts("\n#{String.duplicate("=", 60)}")
IO.puts("  All sections complete!")
IO.puts(String.duplicate("=", 60))
