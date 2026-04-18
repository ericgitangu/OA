#!/usr/bin/env python3
"""Python Fundamentals: Beginner to Advanced — Standard Library Only.

A dense, runnable syntax reference covering core Python concepts.
Run: python3 python_fundamentals.py
"""
from __future__ import annotations

import asyncio
import bisect
import heapq
import math
import operator
import threading
import time
from abc import ABC, abstractmethod
from collections import Counter, OrderedDict, defaultdict, deque, namedtuple
from contextlib import contextmanager, suppress
from dataclasses import dataclass, field
from functools import lru_cache, partial, reduce, singledispatch, wraps
from itertools import chain, combinations, groupby, permutations, product
from multiprocessing import Pool
from typing import Generic, Protocol, TypeVar, overload, runtime_checkable


def section(title: str) -> None:
    print(f"\n{'=' * 60}\n  {title}\n{'=' * 60}")


# ============================================================
#  1. BASICS
# ============================================================
def basics() -> None:
    section("1. BASICS — Variables, Types, F-Strings, Slicing, Comprehensions")

    # --- Types & truthiness ---
    x: int = 42
    pi: float = 3.14
    name: str = "Python"
    flag: bool = True
    nothing: None = None
    print(f"int={x}  float={pi}  str={name!r}  bool={flag}  None={nothing}")
    print(f"Falsy values: {[bool(v) for v in (0, '', [], {}, set(), None)]}")

    # --- F-string tricks (3.12 style) ---
    val = 123456.789
    print(f"Comma sep: {val:,.2f}  Padded: {x:05d}  Hex: {x:#x}  Bin: {x:#010b}")
    print(f"Repr: {name!r}  Centered: {'hi':^10}  Debug: {x = }")

    # --- Slicing ---
    nums = list(range(10))
    print(f"Original: {nums}")
    print(f"[2:7]={nums[2:7]}  [::2]={nums[::2]}  [::-1]={nums[::-1]}")
    print(f"[-3:]={nums[-3:]}  [1:8:3]={nums[1:8:3]}")

    # --- List comprehensions ---
    squares = [n**2 for n in range(6)]
    evens = [n for n in range(20) if n % 2 == 0]
    flat = [x for row in [[1, 2], [3, 4], [5]] for x in row]
    print(f"Squares: {squares}  Evens: {evens}  Flat: {flat}")

    # --- Dict & set comprehensions ---
    word_len = {w: len(w) for w in ("apple", "kiwi", "banana")}
    unique_mods = {n % 3 for n in range(10)}
    print(f"Dict comp: {word_len}")
    print(f"Set comp: {unique_mods}")

    # --- Unpacking ---
    first, *middle, last = [1, 2, 3, 4, 5]
    print(f"Unpack: first={first} middle={middle} last={last}")

    # --- Ternary & chained comparison ---
    status = "even" if x % 2 == 0 else "odd"
    in_range = 1 < 5 < 10 < 100
    print(f"Ternary: {x} is {status}  Chained: {in_range}")


# ============================================================
#  2. DATA STRUCTURES — collections, heapq, bisect
# ============================================================
def data_structures() -> None:
    section("2. DATA STRUCTURES — collections, heapq, bisect")

    # --- Counter ---
    words = "the cat sat on the mat the cat".split()
    c = Counter(words)
    print(f"Counter: {c}")
    print(f"Most common 2: {c.most_common(2)}")

    # --- defaultdict ---
    dd: defaultdict[str, list[str]] = defaultdict(list)
    for animal, sound in [("dog", "woof"), ("cat", "meow"), ("dog", "bark")]:
        dd[animal].append(sound)
    print(f"defaultdict: {dict(dd)}")

    # --- deque ---
    dq: deque[int] = deque(maxlen=5)
    for i in range(7):
        dq.append(i)
    print(f"deque(maxlen=5) after 0..6: {list(dq)}")
    dq.appendleft(99)
    dq.rotate(2)
    print(f"After appendleft(99) + rotate(2): {list(dq)}")

    # --- namedtuple ---
    Point = namedtuple("Point", ["x", "y"])
    p = Point(3, 4)
    print(f"namedtuple: {p}, x={p.x}, as dict={p._asdict()}")

    # --- OrderedDict (move_to_end) ---
    od = OrderedDict(a=1, b=2, c=3)
    od.move_to_end("a")
    print(f"OrderedDict move_to_end('a'): {list(od.items())}")

    # --- heapq (min-heap) ---
    data = [5, 1, 8, 3, 2]
    heapq.heapify(data)
    print(f"Heapified: {data}  Smallest: {heapq.nsmallest(3, data)}")
    heapq.heappush(data, 0)
    popped = heapq.heappop(data)
    print(f"Push 0, pop → {popped}, heap now: {data}")

    # --- bisect (sorted insertion) ---
    arr = [1, 3, 5, 7, 9]
    idx = bisect.bisect_left(arr, 4)
    bisect.insort(arr, 4)
    print(f"bisect_left(4) → idx {idx}, after insort: {arr}")


# ============================================================
#  3. FUNCTIONS — closures, decorators, generators, itertools
# ============================================================
def functions() -> None:
    section("3. FUNCTIONS — Closures, Decorators, Generators, itertools")

    # --- Closure ---
    def make_multiplier(n: int):
        def multiply(x: int) -> int:
            return x * n
        return multiply

    triple = make_multiplier(3)
    print(f"Closure: triple(7) = {triple(7)}")

    # --- Decorator with args ---
    def repeat(times: int):
        def decorator(fn):
            @wraps(fn)
            def wrapper(*args, **kwargs):
                return [fn(*args, **kwargs) for _ in range(times)]
            return wrapper
        return decorator

    @repeat(3)
    def greet(name: str) -> str:
        return f"Hi {name}"

    print(f"Decorator: {greet('Eric')}  __name__={greet.__name__}")

    # --- Generator + yield from ---
    def fib(n: int):
        a, b = 0, 1
        for _ in range(n):
            yield a
            a, b = b, a + b

    print(f"Generator fib(8): {list(fib(8))}")

    # --- Generator expression ---
    gen_sum = sum(x**2 for x in range(10))
    print(f"Genexpr sum of squares: {gen_sum}")

    # --- itertools ---
    print(f"product('AB', [1,2]): {list(product('AB', [1, 2]))}")
    print(f"permutations('ABC', 2): {list(permutations('ABC', 2))[:4]}...")
    print(f"combinations('ABCD', 2): {list(combinations('ABCD', 2))}")
    print(f"chain([1,2], [3,4]): {list(chain([1, 2], [3, 4]))}")

    data = sorted([(1, "a"), (1, "b"), (2, "c"), (2, "d")], key=lambda t: t[0])
    grouped = {k: [v for _, v in g] for k, g in groupby(data, key=lambda t: t[0])}
    print(f"groupby: {grouped}")


# ============================================================
#  4. OOP — classes, inheritance, dataclasses, ABC, dunders,
#           descriptors, metaclasses
# ============================================================
def oop() -> None:
    section("4. OOP — Classes, Inheritance, Dataclasses, ABC, Dunders, Descriptors")

    # --- ABC + inheritance ---
    class Shape(ABC):
        @abstractmethod
        def area(self) -> float: ...

    class Circle(Shape):
        def __init__(self, r: float) -> None:
            self.r = r

        def area(self) -> float:
            return math.pi * self.r ** 2

        def __repr__(self) -> str:
            return f"Circle(r={self.r})"

    c = Circle(5)
    print(f"{c}  area={c.area():.2f}  isinstance={isinstance(c, Shape)}")

    # --- Dataclass ---
    @dataclass(frozen=True, order=True)
    class Vec:
        x: float
        y: float
        label: str = field(default="", compare=False, repr=False)

        @property
        def magnitude(self) -> float:
            return (self.x**2 + self.y**2) ** 0.5

    v1, v2 = Vec(3, 4, "a"), Vec(1, 2, "b")
    print(f"Dataclass: {v1}  mag={v1.magnitude:.2f}  v1>v2={v1 > v2}")

    # --- Dunder methods ---
    class Matrix:
        def __init__(self, rows: list[list[float]]) -> None:
            self.rows = rows

        def __getitem__(self, idx: tuple[int, int]) -> float:
            r, c = idx
            return self.rows[r][c]

        def __len__(self) -> int:
            return len(self.rows)

        def __contains__(self, val: float) -> bool:
            return any(val in row for row in self.rows)

        def __repr__(self) -> str:
            return f"Matrix({self.rows})"

    m = Matrix([[1, 2], [3, 4]])
    print(f"{m}  m[0,1]={m[0, 1]}  len={len(m)}  3 in m={3 in m}")

    # --- Descriptor ---
    class Positive:
        def __set_name__(self, owner, name):
            self.name = f"_{name}"

        def __get__(self, obj, objtype=None):
            return getattr(obj, self.name, None)

        def __set__(self, obj, value):
            if value < 0:
                raise ValueError(f"{self.name} must be positive")
            setattr(obj, self.name, value)

    class Account:
        balance = Positive()

        def __init__(self, bal: float):
            self.balance = bal

    a = Account(100)
    print(f"Descriptor: balance={a.balance}")
    try:
        a.balance = -5
    except ValueError as e:
        print(f"Descriptor guard: {e}")

    # --- Metaclass ---
    class SingletonMeta(type):
        _instances: dict = {}

        def __call__(cls, *args, **kwargs):
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
            return cls._instances[cls]

    class Config(metaclass=SingletonMeta):
        def __init__(self):
            self.debug = False

    c1, c2 = Config(), Config()
    print(f"Metaclass singleton: c1 is c2 = {c1 is c2}")


# ============================================================
#  5. CONCURRENCY — threading, asyncio, multiprocessing
# ============================================================
def concurrency() -> None:
    section("5. CONCURRENCY — threading, asyncio, multiprocessing")

    # --- Threading ---
    results: list[str] = []
    lock = threading.Lock()

    def worker(n: int) -> None:
        time.sleep(0.01)
        with lock:
            results.append(f"t{n}")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"Threading results: {results}")

    # --- asyncio ---
    async def fetch(name: str, delay: float) -> str:
        await asyncio.sleep(delay)
        return f"{name}:{delay}s"

    async def run_async():
        tasks = [fetch("A", 0.02), fetch("B", 0.01), fetch("C", 0.03)]
        results = await asyncio.gather(*tasks)
        print(f"asyncio.gather: {results}")

    asyncio.run(run_async())

    # --- Multiprocessing (Pool) ---
    def square(x: int) -> int:
        return x * x

    with Pool(2) as pool:
        mp_result = pool.map(square, range(6))
    print(f"multiprocessing Pool.map: {mp_result}")


# ============================================================
#  6. FUNCTIONAL — functools, operator
# ============================================================
def functional() -> None:
    section("6. FUNCTIONAL — functools, operator")

    # --- reduce ---
    factorial = reduce(operator.mul, range(1, 7), 1)
    print(f"reduce(mul, 1..6) = {factorial}")

    # --- partial ---
    base2_log = partial(math.log, base=2)
    print(f"partial log base 2: log2(8)={base2_log(8):.1f}")

    # --- lru_cache ---
    @lru_cache(maxsize=128)
    def fib_cached(n: int) -> int:
        if n < 2:
            return n
        return fib_cached(n - 1) + fib_cached(n - 2)

    print(f"lru_cache fib(30)={fib_cached(30)}")
    print(f"Cache info: {fib_cached.cache_info()}")

    # --- singledispatch ---
    @singledispatch
    def process(val):
        return f"unknown: {val}"

    @process.register(int)
    def _(val):
        return f"int: {val * 2}"

    @process.register(str)
    def _(val):
        return f"str: {val.upper()}"

    @process.register(list)
    def _(val):
        return f"list[{len(val)}]"

    print(f"singledispatch: {process(5)}  {process('hi')}  {process([1,2,3])}")

    # --- operator module ---
    items = [{"name": "b", "val": 2}, {"name": "a", "val": 1}]
    items.sort(key=operator.itemgetter("name"))
    print(f"itemgetter sort: {[i['name'] for i in items]}")

    ops = [(operator.add, 3, 4), (operator.mod, 10, 3), (operator.pow, 2, 8)]
    print(f"operator calls: {[op(a, b) for op, a, b in ops]}")


# ============================================================
#  7. TYPE HINTS — generics, Protocol, TypeVar, overload
# ============================================================
def type_hints() -> None:
    section("7. TYPE HINTS — Generics, Protocol, TypeVar, overload")

    # --- TypeVar + Generic ---
    T = TypeVar("T")

    class Stack(Generic[T]):
        def __init__(self) -> None:
            self._items: list[T] = []

        def push(self, item: T) -> None:
            self._items.append(item)

        def pop(self) -> T:
            return self._items.pop()

        def peek(self) -> T:
            return self._items[-1]

        def __repr__(self) -> str:
            return f"Stack({self._items})"

    s: Stack[int] = Stack()
    s.push(10)
    s.push(20)
    print(f"Generic Stack: {s}  peek={s.peek()}  pop={s.pop()}")

    # --- Protocol (structural subtyping) ---
    @runtime_checkable
    class Drawable(Protocol):
        def draw(self) -> str: ...

    class Box:
        def draw(self) -> str:
            return "[box]"

    class Line:
        def draw(self) -> str:
            return "---line---"

    def render(obj: Drawable) -> str:
        return obj.draw()

    b = Box()
    print(f"Protocol: isinstance(Box, Drawable)={isinstance(b, Drawable)}")
    print(f"Render: {render(Box())}  {render(Line())}")

    # --- overload ---
    @overload
    def double(x: int) -> int: ...
    @overload
    def double(x: str) -> str: ...

    def double(x):
        if isinstance(x, int):
            return x * 2
        return x + x

    print(f"overload: double(5)={double(5)}  double('ab')={double('ab')}")


# ============================================================
#  8. CONTEXT MANAGERS — contextlib, custom __enter__/__exit__
# ============================================================
def context_managers() -> None:
    section("8. CONTEXT MANAGERS — contextlib, custom class-based")

    # --- Class-based ---
    class Timer:
        def __enter__(self) -> "Timer":
            self.start = time.perf_counter()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
            self.elapsed = time.perf_counter() - self.start
            print(f"  Timer: {self.elapsed:.6f}s")
            return False  # don't suppress exceptions

    with Timer():
        sum(range(100_000))

    # --- @contextmanager decorator ---
    @contextmanager
    def tag(name: str):
        print(f"  <{name}>", end="")
        yield
        print(f"</{name}>")

    with tag("b"):
        print("bold text", end="")

    # --- suppress ---
    with suppress(FileNotFoundError):
        open("/nonexistent/file.txt")
    print("  suppress(FileNotFoundError): no crash")

    # --- Nested context managers ---
    @contextmanager
    def indent(level: int):
        prefix = "  " * level
        print(f"{prefix}entering level {level}")
        yield prefix
        print(f"{prefix}exiting level {level}")

    with indent(1) as p1:
        print(f"{p1}  work at level 1")
        with indent(2) as p2:
            print(f"{p2}  work at level 2")


# ============================================================
#  9. PATTERN MATCHING — match/case (3.10+)
# ============================================================
def pattern_matching() -> None:
    section("9. PATTERN MATCHING — match/case (Python 3.10+)")

    # --- Literal + capture ---
    def http_status(code: int) -> str:
        match code:
            case 200:
                return "OK"
            case 301 | 302:
                return "Redirect"
            case 404:
                return "Not Found"
            case int(c) if 500 <= c < 600:
                return f"Server Error ({c})"
            case _:
                return "Unknown"

    for code in (200, 302, 404, 503, 999):
        print(f"  {code} → {http_status(code)}")

    # --- Sequence + star pattern ---
    def describe_seq(seq):
        match seq:
            case []:
                return "empty"
            case [x]:
                return f"single: {x}"
            case [x, y]:
                return f"pair: {x}, {y}"
            case [x, *rest]:
                return f"head={x}, tail=[{len(rest)} items]"

    for s in ([], [1], [1, 2], [1, 2, 3, 4]):
        print(f"  {s} → {describe_seq(s)}")

    # --- Mapping pattern ---
    def handle_event(event: dict):
        match event:
            case {"type": "click", "x": x, "y": y}:
                return f"Click at ({x}, {y})"
            case {"type": "key", "code": code}:
                return f"Key: {code}"
            case {"type": t, **rest}:
                return f"Other event: {t}, extra={rest}"

    events = [
        {"type": "click", "x": 10, "y": 20},
        {"type": "key", "code": "Enter"},
        {"type": "scroll", "delta": -3},
    ]
    for e in events:
        print(f"  {e} → {handle_event(e)}")

    # --- Class pattern ---
    @dataclass
    class Cmd:
        action: str
        target: str = ""

    def run_cmd(cmd: Cmd) -> str:
        match cmd:
            case Cmd(action="quit"):
                return "Goodbye"
            case Cmd(action="greet", target=t) if t:
                return f"Hello, {t}!"
            case Cmd(action=a):
                return f"Unknown action: {a}"

    for cmd in [Cmd("quit"), Cmd("greet", "Eric"), Cmd("dance")]:
        print(f"  {cmd} → {run_cmd(cmd)}")


# ============================================================
#  10. ADVANCED — walrus, structural subtyping, __slots__
# ============================================================
def advanced() -> None:
    section("10. ADVANCED — Walrus Operator, Slots, Misc")

    # --- Walrus operator (:=) ---
    data = [1, 5, 3, 8, 2, 9, 4]
    above_avg = [x for x in data if x > (avg := sum(data) / len(data))]
    print(f"Walrus: data={data}  avg={avg:.1f}  above_avg={above_avg}")

    # Walrus in while
    import io
    stream = io.StringIO("line1\nline2\nline3\n")
    lines = []
    while (line := stream.readline()):
        lines.append(line.strip())
    print(f"Walrus while-read: {lines}")

    # --- __slots__ ---
    class SlottedPoint:
        __slots__ = ("x", "y")

        def __init__(self, x: float, y: float):
            self.x = x
            self.y = y

        def __repr__(self) -> str:
            return f"SP({self.x}, {self.y})"

    class RegularPoint:
        def __init__(self, x: float, y: float):
            self.x = x
            self.y = y

    sp = SlottedPoint(1, 2)
    rp = RegularPoint(1, 2)
    print(f"Slots: {sp}  has __dict__={hasattr(sp, '__dict__')}")
    print(f"Regular: has __dict__={hasattr(rp, '__dict__')}  dict={rp.__dict__}")
    try:
        sp.z = 3  # type: ignore
    except AttributeError as e:
        print(f"Slots guard: {e}")

    # --- Structural subtyping (duck typing made explicit) ---
    @runtime_checkable
    class Sized(Protocol):
        def __len__(self) -> int: ...

    class Bag:
        def __init__(self, n: int):
            self._n = n

        def __len__(self) -> int:
            return self._n

    bag = Bag(42)
    print(f"Structural subtyping: isinstance(Bag, Sized)={isinstance(bag, Sized)}")
    print(f"  len(bag)={len(bag)}  (no inheritance needed)")

    # --- Enum-like with __init_subclass__ ---
    class PluginRegistry:
        _plugins: dict[str, type] = {}

        def __init_subclass__(cls, name: str = "", **kwargs):
            super().__init_subclass__(**kwargs)
            if name:
                PluginRegistry._plugins[name] = cls

    class JSONPlugin(PluginRegistry, name="json"):
        pass

    class XMLPlugin(PluginRegistry, name="xml"):
        pass

    print(f"__init_subclass__ registry: {list(PluginRegistry._plugins.keys())}")

    # --- Assignment expressions in comprehensions ---
    results = {
        k: v
        for word in ["hello", "world", "hi"]
        if (k := word[0]) and (v := len(word)) > 2
    }
    print(f"Walrus in dict comp: {results}")


# ============================================================
#  MAIN — run all sections
# ============================================================
if __name__ == "__main__":
    print("PYTHON FUNDAMENTALS — Beginner to Advanced Reference")
    print(f"{'=' * 60}")

    basics()
    data_structures()
    functions()
    oop()
    concurrency()
    functional()
    type_hints()
    context_managers()
    pattern_matching()
    advanced()

    print(f"\n{'=' * 60}")
    print("  Done. All sections executed successfully.")
    print(f"{'=' * 60}")
