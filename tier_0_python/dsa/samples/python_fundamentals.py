#!/usr/bin/env python3
"""Python Fundamentals: Beginner to Advanced — Standard Library Only.

A dense, runnable syntax reference covering core Python concepts.
Run: python3 python_fundamentals.py
"""
# from __future__ import annotations makes all type hints in this module
# "stringified" (PEP 563) — they're not evaluated at import time, which avoids
# circular import issues and lets you reference types before they're defined.
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

    # Python's type hints (x: int) are purely advisory — the runtime ignores them.
    # The interpreter infers types dynamically, so `x` could be reassigned to a str later.
    # Use mypy or pyright for static checking; the annotations are metadata, not constraints.
    x: int = 42
    pi: float = 3.14
    name: str = "Python"
    flag: bool = True
    nothing: None = None
    print(f"int={x}  float={pi}  str={name!r}  bool={flag}  None={nothing}")  # => int=42  float=3.14  str='Python'  bool=True  None=None

    # Python treats these values as falsy: 0, empty string, empty containers, and None.
    # This matters for idiomatic guards like `if not my_list:` instead of `if len(my_list) == 0:`.
    print(f"Falsy values: {[bool(v) for v in (0, '', [], {}, set(), None)]}")  # => Falsy values: [False, False, False, False, False, False]

    # f-string format specs follow the pattern {value:spec}. The spec mini-language supports
    # comma grouping (,), decimal precision (.2f), zero-padding (05d), and base conversion (#x, #b).
    # !r calls repr() on the value — useful for debugging strings with whitespace.
    val = 123456.789
    print(f"Comma sep: {val:,.2f}  Padded: {x:05d}  Hex: {x:#x}  Bin: {x:#010b}")  # => Comma sep: 123,456.79  Padded: 00042  Hex: 0x2a  Bin: 0b00101010
    # The `=` in f-strings (3.8+) prints both the variable name and its value — great for debugging.
    print(f"Repr: {name!r}  Centered: {'hi':^10}  Debug: {x = }")  # => Repr: 'Python'  Centered:     hi      Debug: x = 42

    # Slicing uses [start:stop:step]. Negative indices count from the end.
    # Slices never raise IndexError — they silently clamp to valid bounds, which is
    # safe but can mask bugs if you're expecting an exception.
    nums = list(range(10))
    print(f"Original: {nums}")  # => Original: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(f"[2:7]={nums[2:7]}  [::2]={nums[::2]}  [::-1]={nums[::-1]}")  # => [2:7]=[2, 3, 4, 5, 6]  [::2]=[0, 2, 4, 6, 8]  [::-1]=[9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    print(f"[-3:]={nums[-3:]}  [1:8:3]={nums[1:8:3]}")  # => [-3:]=[7, 8, 9]  [1:8:3]=[1, 4, 7]

    # List comprehensions are syntactic sugar for the map+filter pattern, but they're
    # faster than equivalent for-loops because the iteration happens in C internally.
    # Nested comprehensions read left-to-right: the outer `for row` runs first.
    squares = [n**2 for n in range(6)]
    evens = [n for n in range(20) if n % 2 == 0]
    flat = [x for row in [[1, 2], [3, 4], [5]] for x in row]
    print(f"Squares: {squares}  Evens: {evens}  Flat: {flat}")  # => Squares: [0, 1, 4, 9, 16, 25]  Evens: [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]  Flat: [1, 2, 3, 4, 5]

    # Dict comprehensions create dicts inline. Set comprehensions use {expr for ...}
    # (no key:value pair). Both are O(n) and more readable than dict()/set() constructors.
    word_len = {w: len(w) for w in ("apple", "kiwi", "banana")}
    unique_mods = {n % 3 for n in range(10)}
    print(f"Dict comp: {word_len}")  # => Dict comp: {'apple': 5, 'kiwi': 4, 'banana': 6}
    print(f"Set comp: {unique_mods}")  # => Set comp: {0, 1, 2}

    # Extended unpacking with * captures "the rest" into a list. This works because
    # Python's assignment target is structurally matched — similar to pattern matching
    # but available since Python 3.0. The starred variable always becomes a list.
    first, *middle, last = [1, 2, 3, 4, 5]
    print(f"Unpack: first={first} middle={middle} last={last}")  # => Unpack: first=1 middle=[2, 3, 4] last=5

    # Python's ternary is `value_if_true if condition else value_if_false` — note the
    # inverted order compared to C's `condition ? true : false`.
    # Chained comparisons like `1 < 5 < 10` are unique to Python — they're short-circuit
    # evaluated as `(1 < 5) and (5 < 10)` but each middle expression is evaluated only once.
    status = "even" if x % 2 == 0 else "odd"
    in_range = 1 < 5 < 10 < 100
    print(f"Ternary: {x} is {status}  Chained: {in_range}")  # => Ternary: 42 is even  Chained: True


# ============================================================
#  2. DATA STRUCTURES — collections, heapq, bisect
# ============================================================
def data_structures() -> None:
    section("2. DATA STRUCTURES — collections, heapq, bisect")

    # Counter is a dict subclass for tallying hashable objects. Internally it's just
    # {element: count}, but it adds arithmetic ops (+, -, &, |) and most_common().
    # In production, use Counter for frequency analysis instead of manual dict counting.
    words = "the cat sat on the mat the cat".split()
    c = Counter(words)
    print(f"Counter: {c}")  # => Counter: Counter({'the': 3, 'cat': 2, 'sat': 1, 'on': 1, 'mat': 1})
    print(f"Most common 2: {c.most_common(2)}")  # => Most common 2: [('the', 3), ('cat', 2)]

    # defaultdict eliminates the "check-then-insert" pattern. The factory function (here `list`)
    # is called whenever a missing key is accessed, so dd["dog"] auto-creates an empty list.
    # This is the idiomatic way to build adjacency lists and grouping structures.
    dd: defaultdict[str, list[str]] = defaultdict(list)
    for animal, sound in [("dog", "woof"), ("cat", "meow"), ("dog", "bark")]:
        dd[animal].append(sound)
    print(f"defaultdict: {dict(dd)}")  # => defaultdict: {'dog': ['woof', 'bark'], 'cat': ['meow']}

    # deque (double-ended queue) provides O(1) append/pop on both ends, unlike list which
    # is O(n) for left operations. maxlen creates a bounded buffer — when full, items are
    # silently discarded from the opposite end. Use deque for BFS queues and sliding windows.
    dq: deque[int] = deque(maxlen=5)
    for i in range(7):
        dq.append(i)
    print(f"deque(maxlen=5) after 0..6: {list(dq)}")  # => deque(maxlen=5) after 0..6: [2, 3, 4, 5, 6]
    # rotate(n) shifts elements n positions to the right (negative = left) in O(n).
    dq.appendleft(99)
    dq.rotate(2)
    print(f"After appendleft(99) + rotate(2): {list(dq)}")  # => After appendleft(99) + rotate(2): [4, 5, 99, 2, 3]

    # namedtuple creates an immutable tuple subclass with named fields — lighter than
    # a dataclass when you just need a simple value object. _asdict() returns an OrderedDict.
    # Prefer dataclass for mutable data or when you need methods beyond simple field access.
    Point = namedtuple("Point", ["x", "y"])
    p = Point(3, 4)
    print(f"namedtuple: {p}, x={p.x}, as dict={p._asdict()}")  # => namedtuple: Point(x=3, y=4), x=3, as dict={'x': 3, 'y': 4}

    # Since Python 3.7, regular dicts preserve insertion order. OrderedDict still exists
    # for its move_to_end() and equality semantics (two OrderedDicts with different order
    # compare unequal, while regular dicts don't consider order).
    od = OrderedDict(a=1, b=2, c=3)
    od.move_to_end("a")
    print(f"OrderedDict move_to_end('a'): {list(od.items())}")  # => OrderedDict move_to_end('a'): [('b', 2), ('c', 3), ('a', 1)]

    # heapq implements a min-heap over a plain list. Python has no max-heap — the standard
    # workaround is to negate values. heapify is O(n), push/pop are O(log n).
    # In production, use heapq for top-K problems and priority queues.
    data = [5, 1, 8, 3, 2]
    heapq.heapify(data)
    print(f"Heapified: {data}  Smallest: {heapq.nsmallest(3, data)}")  # => Heapified: [1, 2, 8, 3, 5]  Smallest: [1, 2, 3]
    heapq.heappush(data, 0)
    popped = heapq.heappop(data)
    print(f"Push 0, pop → {popped}, heap now: {data}")  # => Push 0, pop → 0, heap now: [1, 2, 8, 3, 5]

    # bisect operates on already-sorted lists using binary search (O(log n) lookup).
    # bisect_left returns the leftmost valid insertion index; insort maintains sorted order.
    # This is the go-to for maintaining a sorted collection with fast lookup.
    arr = [1, 3, 5, 7, 9]
    idx = bisect.bisect_left(arr, 4)
    bisect.insort(arr, 4)
    print(f"bisect_left(4) → idx {idx}, after insort: {arr}")  # => bisect_left(4) → idx 2, after insort: [1, 3, 4, 5, 7, 9]


# ============================================================
#  3. FUNCTIONS — closures, decorators, generators, itertools
# ============================================================
def functions() -> None:
    section("3. FUNCTIONS — Closures, Decorators, Generators, itertools")

    # A closure captures variables from its enclosing scope by reference (not by value).
    # The inner function `multiply` holds a reference to `n` — so even after make_multiplier
    # returns, `n` stays alive in the closure's __closure__ cells. This is how Python
    # implements factory functions and partial application without functools.partial.
    def make_multiplier(n: int):
        def multiply(x: int) -> int:
            return x * n
        return multiply

    triple = make_multiplier(3)
    print(f"Closure: triple(7) = {triple(7)}")  # => Closure: triple(7) = 21

    # This is a decorator factory — a function that returns a decorator. The three-level
    # nesting (repeat -> decorator -> wrapper) is necessary because decorators with arguments
    # need an extra layer: @repeat(3) first calls repeat(3) which returns the actual decorator.
    # @wraps(fn) copies __name__, __doc__, etc. from the original function to the wrapper,
    # which is essential for debugging and introspection in production.
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

    print(f"Decorator: {greet('Eric')}  __name__={greet.__name__}")  # => Decorator: ['Hi Eric', 'Hi Eric', 'Hi Eric']  __name__=greet

    # Generators use `yield` to produce values lazily — they don't compute the full sequence
    # upfront. Each call to next() resumes execution right after the last yield. This makes
    # them memory-efficient for large/infinite sequences. The generator object implements
    # the iterator protocol (__iter__ + __next__) automatically.
    def fib(n: int):
        a, b = 0, 1
        for _ in range(n):
            yield a
            a, b = b, a + b

    print(f"Generator fib(8): {list(fib(8))}")  # => Generator fib(8): [0, 1, 1, 2, 3, 5, 8, 13]

    # Generator expressions are inline generators — they use () instead of []. Unlike list
    # comprehensions, they don't materialize the full list in memory. Here sum() consumes
    # the generator one element at a time, so peak memory is O(1) instead of O(n).
    gen_sum = sum(x**2 for x in range(10))
    print(f"Genexpr sum of squares: {gen_sum}")  # => Genexpr sum of squares: 285

    # itertools provides C-optimized combinatoric iterators. product() is the Cartesian product
    # (nested loops), permutations() generates ordered arrangements, combinations() generates
    # unordered selections. All return lazy iterators, making them viable for large inputs.
    print(f"product('AB', [1,2]): {list(product('AB', [1, 2]))}")  # => product('AB', [1,2]): [('A', 1), ('A', 2), ('B', 1), ('B', 2)]
    print(f"permutations('ABC', 2): {list(permutations('ABC', 2))[:4]}...")  # => permutations('ABC', 2): [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C')]...
    print(f"combinations('ABCD', 2): {list(combinations('ABCD', 2))}")  # => combinations('ABCD', 2): [('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'C'), ('B', 'D'), ('C', 'D')]
    # chain() concatenates iterables without copying — it just yields from each in turn.
    print(f"chain([1,2], [3,4]): {list(chain([1, 2], [3, 4]))}")  # => chain([1,2], [3,4]): [1, 2, 3, 4]

    # groupby() groups consecutive elements with the same key. The input MUST be sorted by
    # the key first — otherwise you'll get fragmented groups. This is a common gotcha.
    # The groups are iterators that are invalidated when you advance to the next group.
    data = sorted([(1, "a"), (1, "b"), (2, "c"), (2, "d")], key=lambda t: t[0])
    grouped = {k: [v for _, v in g] for k, g in groupby(data, key=lambda t: t[0])}
    print(f"groupby: {grouped}")  # => groupby: {1: ['a', 'b'], 2: ['c', 'd']}


# ============================================================
#  4. OOP — classes, inheritance, dataclasses, ABC, dunders,
#           descriptors, metaclasses
# ============================================================
def oop() -> None:
    section("4. OOP — Classes, Inheritance, Dataclasses, ABC, Dunders, Descriptors")

    # ABC (Abstract Base Class) enforces an interface contract: subclasses MUST implement
    # all @abstractmethod-decorated methods or they can't be instantiated. This is Python's
    # answer to interfaces — use it when you want compile-time-like guarantees that a
    # subclass provides certain methods, rather than relying on duck typing alone.
    class Shape(ABC):
        @abstractmethod
        def area(self) -> float: ...

    class Circle(Shape):
        def __init__(self, r: float) -> None:
            self.r = r

        def area(self) -> float:
            return math.pi * self.r ** 2

        # __repr__ is for developers (unambiguous), __str__ is for users (readable).
        # When you print() or f-string an object, Python tries __str__ first, then __repr__.
        # Implementing __repr__ is the higher-priority one — it's used in debuggers and logs.
        def __repr__(self) -> str:
            return f"Circle(r={self.r})"

    c = Circle(5)
    print(f"{c}  area={c.area():.2f}  isinstance={isinstance(c, Shape)}")  # => Circle(r=5)  area=78.54  isinstance=True

    # @dataclass auto-generates __init__, __repr__, __eq__ (and optionally __hash__, __lt__, etc).
    # frozen=True makes instances immutable (attempts to set fields raise FrozenInstanceError),
    # which also makes them hashable. order=True generates comparison methods based on field order.
    # field(compare=False) excludes a field from equality/ordering — useful for metadata.
    @dataclass(frozen=True, order=True)
    class Vec:
        x: float
        y: float
        label: str = field(default="", compare=False, repr=False)

        # @property turns a method into a computed attribute — accessed as v1.magnitude, not v1.magnitude().
        # It's the Pythonic replacement for Java-style getters; the caller doesn't know it's computed.
        @property
        def magnitude(self) -> float:
            return (self.x**2 + self.y**2) ** 0.5

    v1, v2 = Vec(3, 4, "a"), Vec(1, 2, "b")
    print(f"Dataclass: {v1}  mag={v1.magnitude:.2f}  v1>v2={v1 > v2}")  # => Dataclass: Vec(x=3, y=4)  mag=5.00  v1>v2=True

    # Dunder (double-underscore) methods let your class hook into Python's syntax.
    # __getitem__ enables indexing (m[0,1]), __len__ enables len(), __contains__ enables `in`.
    # Python passes m[0, 1] as a single tuple argument to __getitem__ — that's why
    # idx is typed as tuple[int, int], not two separate parameters.
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
    print(f"{m}  m[0,1]={m[0, 1]}  len={len(m)}  3 in m={3 in m}")  # => Matrix([[1, 2], [3, 4]])  m[0,1]=2  len=2  3 in m=True

    # Descriptors are the mechanism behind @property, @classmethod, and @staticmethod.
    # A descriptor is any object with __get__, __set__, or __delete__. When assigned as a
    # class variable, Python intercepts attribute access through the descriptor protocol.
    # __set_name__ (3.6+) is called at class creation time, giving the descriptor its field name.
    # Use descriptors for reusable validation logic that would otherwise be duplicated across properties.
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
    print(f"Descriptor: balance={a.balance}")  # => Descriptor: balance=100
    try:
        a.balance = -5
    except ValueError as e:
        print(f"Descriptor guard: {e}")  # => Descriptor guard: _balance must be positive

    # A metaclass is the class of a class — it controls class creation itself. type is the
    # default metaclass. Here SingletonMeta overrides __call__ to intercept instantiation,
    # returning the cached instance instead of creating a new one. Metaclasses are powerful
    # but rarely needed — prefer __init_subclass__ or decorators for simpler use cases.
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
    print(f"Metaclass singleton: c1 is c2 = {c1 is c2}")  # => Metaclass singleton: c1 is c2 = True


# ============================================================
#  5. CONCURRENCY — threading, asyncio, multiprocessing
# ============================================================
def concurrency() -> None:
    section("5. CONCURRENCY — threading, asyncio, multiprocessing")

    # Python's GIL (Global Interpreter Lock) means only one thread executes Python bytecode
    # at a time. Threading is still useful for I/O-bound tasks (network, disk) because the
    # GIL is released during I/O waits. For CPU-bound parallelism, use multiprocessing instead.
    # The Lock here prevents race conditions on the shared `results` list — even though the
    # GIL exists, list.append isn't guaranteed atomic at the Python level.
    results: list[str] = []
    lock = threading.Lock()

    def worker(n: int) -> None:
        time.sleep(0.01)
        # `with lock` acquires and auto-releases the mutex — RAII-style resource management
        # via the context manager protocol. Always prefer this over manual acquire/release.
        with lock:
            results.append(f"t{n}")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(4)]
    for t in threads:
        t.start()
    # join() blocks until the thread completes. Without it, the main thread could exit
    # before workers finish, potentially corrupting shared state.
    for t in threads:
        t.join()
    print(f"Threading results: {results}")  # => (thread-dependent, e.g. ['t0', 't1', 't2', 't3'])

    # asyncio is cooperative concurrency — coroutines voluntarily yield control at `await`
    # points. Unlike threads, there's no preemption and no GIL concern because everything
    # runs in a single thread. This makes asyncio ideal for high-concurrency I/O (e.g.,
    # thousands of HTTP requests) without the overhead of thread context switching.
    async def fetch(name: str, delay: float) -> str:
        await asyncio.sleep(delay)
        return f"{name}:{delay}s"

    async def run_async():
        # gather() runs coroutines concurrently and returns results in the same order.
        # It's the asyncio equivalent of threading + join, but without OS thread overhead.
        tasks = [fetch("A", 0.02), fetch("B", 0.01), fetch("C", 0.03)]
        results = await asyncio.gather(*tasks)
        print(f"asyncio.gather: {results}")  # => asyncio.gather: ['A:0.02s', 'B:0.01s', 'C:0.03s']

    asyncio.run(run_async())

    # ProcessPoolExecutor spawns separate OS processes, each with its own Python interpreter
    # and memory space — completely bypassing the GIL. The tradeoff is higher startup cost
    # and IPC serialization (pickle). Use this for CPU-bound work like number crunching.
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=2) as executor:
        mp_result = list(executor.map(pow, range(6), [2] * 6))
    print(f"ProcessPoolExecutor map (x**2): {mp_result}")  # => ProcessPoolExecutor map (x**2): [0, 1, 4, 9, 16, 25]


# ============================================================
#  6. FUNCTIONAL — functools, operator
# ============================================================
def functional() -> None:
    section("6. FUNCTIONAL — functools, operator")

    # reduce applies a binary function cumulatively: reduce(f, [a,b,c]) = f(f(a,b), c).
    # The third argument (1) is the initial accumulator value. Python moved reduce out of
    # builtins into functools because Guido considers explicit loops more Pythonic for most cases.
    factorial = reduce(operator.mul, range(1, 7), 1)
    print(f"reduce(mul, 1..6) = {factorial}")  # => reduce(mul, 1..6) = 720

    # partial freezes some arguments of a function, creating a new callable. It's useful
    # for adapting function signatures — e.g., passing a 2-arg function where a 1-arg callback
    # is expected. Unlike lambdas, partial objects are picklable (needed for multiprocessing).
    base2_log = partial(math.log2)
    print(f"partial log base 2: log2(8)={base2_log(8):.1f}")  # => partial log base 2: log2(8)=3.0

    # lru_cache memoizes function results in a thread-safe dict keyed by arguments.
    # maxsize=128 means it evicts the Least Recently Used entry when full (LRU policy).
    # Arguments must be hashable. cache_info() reports hits/misses — use it to verify
    # your cache is actually helping. For unbounded caching, use @cache (3.9+).
    @lru_cache(maxsize=128)
    def fib_cached(n: int) -> int:
        if n < 2:
            return n
        return fib_cached(n - 1) + fib_cached(n - 2)

    print(f"lru_cache fib(30)={fib_cached(30)}")  # => lru_cache fib(30)=832040
    print(f"Cache info: {fib_cached.cache_info()}")  # => Cache info: CacheInfo(hits=28, misses=31, maxsize=128, currsize=31)

    # singledispatch is Python's version of function overloading — dispatch based on the
    # type of the first argument. Unlike method overloading in Java/C++, this is single-dispatch
    # (only the first arg's type matters). For multiple-dispatch, you'd need a third-party lib.
    # Register implementations with @process.register(type); the base function is the fallback.
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

    print(f"singledispatch: {process(5)}  {process('hi')}  {process([1,2,3])}")  # => singledispatch: int: 10  str: HI  list[3]

    # operator.itemgetter("name") creates a callable equivalent to lambda x: x["name"],
    # but faster because it's implemented in C. Use it as a sort key for dicts or tuples —
    # it's the idiomatic alternative to lambdas for simple field extraction.
    items = [{"name": "b", "val": 2}, {"name": "a", "val": 1}]
    items.sort(key=operator.itemgetter("name"))
    print(f"itemgetter sort: {[i['name'] for i in items]}")  # => itemgetter sort: ['a', 'b']

    # The operator module exposes Python's built-in operators as regular functions.
    # operator.add(a, b) is equivalent to a + b. Useful for reduce(), map(), and
    # anywhere you need to pass an operator as a first-class function.
    ops = [(operator.add, 3, 4), (operator.mod, 10, 3), (operator.pow, 2, 8)]
    print(f"operator calls: {[op(a, b) for op, a, b in ops]}")  # => operator calls: [7, 1, 256]


# ============================================================
#  7. TYPE HINTS — generics, Protocol, TypeVar, overload
# ============================================================
def type_hints() -> None:
    section("7. TYPE HINTS — Generics, Protocol, TypeVar, overload")

    # TypeVar creates a type variable that can be "filled in" by the caller. When you write
    # Stack[int], T is bound to int throughout that instance. This gives you type-safe
    # containers without code duplication — similar to Java generics or C++ templates,
    # but purely at the type-checker level (no runtime enforcement).
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
    print(f"Generic Stack: {s}  peek={s.peek()}  pop={s.pop()}")  # => Generic Stack: Stack([10, 20])  peek=20  pop=20

    # Protocol enables structural subtyping (duck typing with static checking). Unlike ABC,
    # classes don't need to explicitly inherit from Protocol — they just need to have the right
    # methods. This is Go-style "interfaces satisfied implicitly." @runtime_checkable adds
    # isinstance() support, but it only checks method existence, not signatures.
    @runtime_checkable
    class Drawable(Protocol):
        def draw(self) -> str: ...

    # Box satisfies Drawable without inheriting from it — it just has a compatible draw() method.
    class Box:
        def draw(self) -> str:
            return "[box]"

    class Line:
        def draw(self) -> str:
            return "---line---"

    def render(obj: Drawable) -> str:
        return obj.draw()

    b = Box()
    print(f"Protocol: isinstance(Box, Drawable)={isinstance(b, Drawable)}")  # => Protocol: isinstance(Box, Drawable)=True
    print(f"Render: {render(Box())}  {render(Line())}")  # => Render: [box]  ---line---

    # @overload provides type-checker hints for functions that return different types based on
    # input types. The overloaded signatures are ONLY for the type checker — the actual
    # implementation (without @overload) is the one that runs. This gives you precise
    # return-type narrowing that a single Union return type can't express.
    @overload
    def double(x: int) -> int: ...
    @overload
    def double(x: str) -> str: ...

    def double(x):
        if isinstance(x, int):
            return x * 2
        return x + x

    print(f"overload: double(5)={double(5)}  double('ab')={double('ab')}")  # => overload: double(5)=10  double('ab')=abab


# ============================================================
#  8. CONTEXT MANAGERS — contextlib, custom __enter__/__exit__
# ============================================================
def context_managers() -> None:
    section("8. CONTEXT MANAGERS — contextlib, custom class-based")

    # Context managers implement the "with" protocol: __enter__ runs on entry, __exit__
    # runs on exit — even if an exception occurs. This is Python's RAII equivalent,
    # guaranteeing cleanup of resources (files, locks, DB connections, timers).
    # __exit__ receives exception info; returning True suppresses the exception.
    class Timer:
        def __enter__(self) -> "Timer":
            self.start = time.perf_counter()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
            self.elapsed = time.perf_counter() - self.start
            print(f"  Timer: {self.elapsed:.6f}s")  # => (varies, e.g. Timer: 0.000823s)
            return False  # don't suppress exceptions

    with Timer():
        sum(range(100_000))

    # @contextmanager turns a generator into a context manager. Code before `yield` is
    # __enter__, code after is __exit__. This avoids writing a full class for simple cases.
    # The yielded value becomes the `as` target in `with tag("b") as t:`.
    @contextmanager
    def tag(name: str):
        print(f"  <{name}>", end="")  # => <b>
        yield
        print(f"</{name}>")  # => </b>

    with tag("b"):
        print("bold text", end="")  # => bold text

    # suppress() is a context manager that silently catches specified exceptions.
    # Equivalent to try/except with a pass, but more readable for simple cases.
    # Use it when you expect an exception and intentionally want to ignore it.
    with suppress(FileNotFoundError):
        open("/nonexistent/file.txt")
    print("  suppress(FileNotFoundError): no crash")  # =>   suppress(FileNotFoundError): no crash

    # Context managers can be nested and composed. Each one's __exit__ is guaranteed
    # to run in reverse order (LIFO), providing deterministic cleanup ordering.
    @contextmanager
    def indent(level: int):
        prefix = "  " * level
        print(f"{prefix}entering level {level}")  # => (e.g. "  entering level 1")
        yield prefix
        print(f"{prefix}exiting level {level}")  # => (e.g. "  exiting level 1")

    with indent(1) as p1:
        print(f"{p1}  work at level 1")  # =>     work at level 1
        with indent(2) as p2:
            print(f"{p2}  work at level 2")  # =>       work at level 2


# ============================================================
#  9. PATTERN MATCHING — match/case (3.10+)
# ============================================================
def pattern_matching() -> None:
    section("9. PATTERN MATCHING — match/case (Python 3.10+)")

    # match/case (PEP 634) is structural pattern matching — not just a switch statement.
    # It destructures values, binds variables, and supports guards. Unlike C's switch, there's
    # no fall-through, and the `_` wildcard acts as a catch-all (like `default`).
    # Patterns are tried top-to-bottom; the first match wins.
    def http_status(code: int) -> str:
        match code:
            case 200:
                return "OK"
            # The | operator combines patterns — matches if ANY alternative matches.
            case 301 | 302:
                return "Redirect"
            case 404:
                return "Not Found"
            # Guard clauses (`if`) add conditions beyond structural matching. int(c) captures
            # the value into `c` while confirming the type is int.
            case int(c) if 500 <= c < 600:
                return f"Server Error ({c})"
            case _:
                return "Unknown"

    for code in (200, 302, 404, 503, 999):
        print(f"  {code} → {http_status(code)}")  # => 200 → OK / 302 → Redirect / 404 → Not Found / 503 → Server Error (503) / 999 → Unknown

    # Sequence patterns destructure lists/tuples. The * prefix captures remaining elements
    # into a list — similar to extended unpacking in assignments. The match engine checks
    # both structure (length) and content simultaneously.
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
        print(f"  {s} → {describe_seq(s)}")  # => [] → empty / [1] → single: 1 / [1, 2] → pair: 1, 2 / [1, 2, 3, 4] → head=1, tail=[3 items]

    # Mapping patterns match dicts by key presence. Unmatched keys are ignored by default;
    # **rest captures them explicitly. Keys must be literals or constants — you can't use
    # variables as keys in a pattern (they'd be treated as capture variables).
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
        print(f"  {e} → {handle_event(e)}")  # => {'type': 'click', ...} → Click at (10, 20) / {'type': 'key', ...} → Key: Enter / {'type': 'scroll', ...} → Other event: scroll, extra={'delta': -3}

    # Class patterns match dataclass/namedtuple instances by field values. The pattern
    # Cmd(action="quit") checks both the type (isinstance) and the field value simultaneously.
    # This is where pattern matching truly surpasses if/elif chains — you get type narrowing,
    # destructuring, and guards in a single expression.
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
        print(f"  {cmd} → {run_cmd(cmd)}")  # => Cmd(action='quit', target='') → Goodbye / Cmd(action='greet', target='Eric') → Hello, Eric! / Cmd(action='dance', target='') → Unknown action: dance


# ============================================================
#  10. ADVANCED — walrus, structural subtyping, __slots__
# ============================================================
def advanced() -> None:
    section("10. ADVANCED — Walrus Operator, Slots, Misc")

    # The walrus operator (:=) assigns a value as part of an expression (PEP 572).
    # It's useful when you need to both compute and test a value — avoiding redundant
    # computation or the need for a temporary variable outside the expression.
    # Caution: avg is computed once but the := "leaks" into the enclosing scope.
    data = [1, 5, 3, 8, 2, 9, 4]
    above_avg = [x for x in data if x > (avg := sum(data) / len(data))]
    print(f"Walrus: data={data}  avg={avg:.1f}  above_avg={above_avg}")  # => Walrus: data=[1, 5, 3, 8, 2, 9, 4]  avg=4.6  above_avg=[5, 8, 9]

    # Walrus shines in while-loops where you need to read-and-check in one step.
    # Without :=, you'd need an assignment before the loop and a duplicate at the end.
    import io
    stream = io.StringIO("line1\nline2\nline3\n")
    lines = []
    while (line := stream.readline()):
        lines.append(line.strip())
    print(f"Walrus while-read: {lines}")  # => Walrus while-read: ['line1', 'line2', 'line3']

    # __slots__ replaces the per-instance __dict__ with a fixed-size struct of named fields.
    # This saves ~40-60% memory per instance and slightly speeds up attribute access.
    # The tradeoff: you can't add arbitrary attributes at runtime, and multiple inheritance
    # with slots is tricky. Use slots for data-heavy classes with many instances (e.g., ORM rows).
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
    print(f"Slots: {sp}  has __dict__={hasattr(sp, '__dict__')}")  # => Slots: SP(1, 2)  has __dict__=False
    print(f"Regular: has __dict__={hasattr(rp, '__dict__')}  dict={rp.__dict__}")  # => Regular: has __dict__=True  dict={'x': 1, 'y': 2}
    try:
        sp.z = 3  # type: ignore
    except AttributeError as e:
        print(f"Slots guard: {e}")  # => Slots guard: 'SlottedPoint' object has no attribute 'z'

    # Protocol provides structural subtyping — the static-typing formalization of Python's
    # duck typing. If a class has __len__, it satisfies this Sized protocol WITHOUT inheriting
    # from it. This is the opposite of nominal typing (Java interfaces) where you must
    # explicitly declare that you implement an interface.
    @runtime_checkable
    class Sized(Protocol):
        def __len__(self) -> int: ...

    class Bag:
        def __init__(self, n: int):
            self._n = n

        def __len__(self) -> int:
            return self._n

    bag = Bag(42)
    print(f"Structural subtyping: isinstance(Bag, Sized)={isinstance(bag, Sized)}")  # => Structural subtyping: isinstance(Bag, Sized)=True
    print(f"  len(bag)={len(bag)}  (no inheritance needed)")  # =>   len(bag)=42  (no inheritance needed)

    # __init_subclass__ (PEP 487) is called whenever a class is subclassed. It's a simpler
    # alternative to metaclasses for the common case of registering or validating subclasses.
    # Here it implements a plugin registry — subclasses auto-register themselves by name.
    # In production, this pattern replaces manual registry dicts and avoids metaclass complexity.
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

    print(f"__init_subclass__ registry: {list(PluginRegistry._plugins.keys())}")  # => __init_subclass__ registry: ['json', 'xml']

    # Walrus in comprehensions: := binds inside the comprehension but the variable
    # is accessible in the enclosing scope. This is intentional but surprising —
    # it's one of the few ways a comprehension can leak a variable into outer scope.
    results = {
        k: v
        for word in ["hello", "world", "hi"]
        if (k := word[0]) and (v := len(word)) > 2
    }
    print(f"Walrus in dict comp: {results}")  # => Walrus in dict comp: {'h': 5, 'w': 5}


# ============================================================
#  MAIN — run all sections
# ============================================================
if __name__ == "__main__":
    print("PYTHON FUNDAMENTALS — Beginner to Advanced Reference")  # => PYTHON FUNDAMENTALS — Beginner to Advanced Reference
    print(f"{'=' * 60}")  # => ============================================================

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

    print(f"\n{'=' * 60}")  # => ============================================================
    print("  Done. All sections executed successfully.")  # =>   Done. All sections executed successfully.
    print(f"{'=' * 60}")  # => ============================================================
