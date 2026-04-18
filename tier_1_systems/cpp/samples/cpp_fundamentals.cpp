// cpp_fundamentals.cpp — C++20 fundamentals showcase
// Compile: clang++ -std=c++20 -o cpp_fundamentals cpp_fundamentals.cpp -lpthread

#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <set>
#include <unordered_map>
#include <array>
#include <deque>
#include <algorithm>
#include <numeric>
#include <ranges>
#include <memory>
#include <optional>
#include <variant>
#include <span>
#include <thread>
#include <mutex>
#include <future>
#include <atomic>
#include <functional>
#include <concepts>
#include <type_traits>
#include <cassert>
#include <sstream>
#include <utility>

void header(const std::string& title) {
    std::cout << "\n============================================================\n";
    std::cout << "  " << title << "\n";
    std::cout << "============================================================\n";
}

// ─── 1. Basics ──────────────────────────────────────────────
void basics() {
    header("1. BASICS — auto, structured bindings, ranges, concepts");

    // `auto` deduces the type from the initializer at compile time. Unlike dynamic typing,
    // the type is fully resolved — auto x = 42 is exactly int, not a flexible type.
    // Use auto to reduce verbosity, especially with iterators and template return types.
    auto x = 42;
    auto pi = 3.14159;
    // std::string("...") is explicit construction. Without it, auto would deduce const char*
    // (a C-style string pointer), not std::string — a common gotcha.
    auto msg = std::string("hello C++20");
    std::cout << "auto: x=" << x << ", pi=" << pi << ", msg=" << msg << "\n";  // => auto: x=42, pi=3.14159, msg=hello C++20

    // Structured bindings (C++17) destructure aggregates into named variables. auto& creates
    // references to the original fields — modifying `name` or `age` modifies `entry`.
    // This replaces the verbose .first/.second pattern for pairs and enables clean iteration over maps.
    std::pair<std::string, int> entry{"Alice", 30};
    auto& [name, age] = entry;
    std::cout << "Structured binding: " << name << " age " << age << "\n";  // => Structured binding: Alice age 30

    // Works with any aggregate type (structs, arrays, tuples) — the compiler matches
    // fields positionally, not by name. The struct must have all public members.
    struct Point { double x, y; };
    auto [px, py] = Point{3.0, 4.0};
    std::cout << "Point destructured: (" << px << ", " << py << ")\n";  // => Point destructured: (3, 4)

    // C++20 Ranges: the pipe operator chains lazy view adaptors. filter and transform
    // create views (no copies) — elements are computed on-demand during iteration.
    // This is the STL's answer to Python's generator pipelines and Rust's iterator adapters.
    std::vector<int> nums{1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    auto evens = nums | std::views::filter([](int n) { return n % 2 == 0; })
                      | std::views::transform([](int n) { return n * n; });
    std::cout << "Even squares (ranges): ";
    for (auto v : evens) std::cout << v << " ";
    std::cout << "\n";  // => Even squares (ranges): 4 16 36 64 100

    // views::take(n) lazily yields only the first n elements — doesn't copy or slice the vector.
    auto first3 = nums | std::views::take(3);
    std::cout << "First 3: ";
    for (auto v : first3) std::cout << v << " ";
    std::cout << "\n";  // => First 3: 1 2 3

    // Concepts (C++20) constrain template parameters with named requirements.
    // `requires std::integral<T>` rejects non-integer types at compile time with a clear error,
    // unlike pre-concepts SFINAE which produced cryptic template error novels.
    auto add = []<typename T>(T a, T b) requires std::integral<T> { return a + b; };
    std::cout << "Concept-constrained add: " << add(10, 20) << "\n";  // => Concept-constrained add: 30
}

// ─── 2. Smart Pointers ─────────────────────────────────────
void smart_pointers() {
    header("2. SMART POINTERS — unique_ptr, shared_ptr");

    // unique_ptr provides exclusive ownership with RAII — the pointed-to object is automatically
    // deleted when the unique_ptr goes out of scope. make_unique is preferred over raw new
    // because it's exception-safe and avoids writing the type twice.
    auto up = std::make_unique<std::string>("unique data");
    std::cout << "unique_ptr: " << *up << "\n";  // => unique_ptr: unique data
    // unique_ptr cannot be copied (the copy constructor is deleted). std::move transfers
    // ownership — after this, `up` is null and `up2` owns the string.
    // This models Rust's move semantics but without compile-time use-after-move detection.
    auto up2 = std::move(up); // transfer ownership
    std::cout << "After move, up is " << (up ? "valid" : "null")
              << ", up2 = " << *up2 << "\n";  // => After move, up is null, up2 = unique data

    // unique_ptr supports array types with [] — it calls delete[] instead of delete.
    // Prefer std::vector in most cases; unique_ptr<T[]> is for C API interop or fixed-size buffers.
    auto arr = std::make_unique<int[]>(5);
    for (int i = 0; i < 5; ++i) arr[i] = i * 10;
    std::cout << "unique_ptr array: ";
    for (int i = 0; i < 5; ++i) std::cout << arr[i] << " ";
    std::cout << "\n";  // => unique_ptr array: 0 10 20 30 40

    // shared_ptr uses reference counting — multiple shared_ptrs can own the same object.
    // The object is destroyed when the last shared_ptr is destroyed. The reference count
    // is thread-safe (atomic), but the pointed-to object itself is NOT automatically thread-safe.
    // Overhead: two extra pointers (control block) + atomic ref count operations.
    auto sp1 = std::make_shared<std::string>("shared data");
    auto sp2 = sp1;
    auto sp3 = sp1;
    std::cout << "shared_ptr use_count: " << sp1.use_count()
              << ", value: " << *sp1 << "\n";  // => shared_ptr use_count: 3, value: shared data
    // reset() decrements the ref count and releases this shared_ptr's ownership.
    sp2.reset();
    std::cout << "After reset: use_count = " << sp1.use_count() << "\n";  // => After reset: use_count = 2

    // weak_ptr breaks reference cycles (e.g., parent-child or observer patterns).
    // It doesn't increment the ref count, so the object can still be destroyed.
    // lock() promotes to shared_ptr if the object is still alive; returns nullptr if not.
    std::weak_ptr<std::string> wp = sp1;
    if (auto locked = wp.lock()) {
        std::cout << "weak_ptr locked: " << *locked << "\n";  // => weak_ptr locked: shared data
    }
}

// ─── 3. Containers ─────────────────────────────────────────
void containers() {
    header("3. CONTAINERS — vector, map, set, unordered_map, array, deque");

    // std::vector is a dynamic array — contiguous memory, amortized O(1) push_back.
    // sort uses introsort (quicksort + heapsort fallback), guaranteed O(n log n).
    std::vector<int> v{5, 3, 1, 4, 2};
    std::sort(v.begin(), v.end());
    std::cout << "Sorted vector: ";
    for (auto n : v) std::cout << n << " ";
    std::cout << "\n";  // => Sorted vector: 1 2 3 4 5

    // std::map is a red-black tree — O(log n) insert/lookup, keys are always sorted.
    // operator[] inserts a default-constructed value if the key doesn't exist — use .at()
    // or .find() when you don't want implicit insertion. Structured bindings make iteration clean.
    std::map<std::string, int> m{{"apple", 3}, {"banana", 1}, {"cherry", 5}};
    m["date"] = 2;
    std::cout << "Map (ordered): ";
    for (auto& [k, val] : m) std::cout << k << "=" << val << " ";
    std::cout << "\n";  // => Map (ordered): apple=3 banana=1 cherry=5 date=2

    // std::set is a sorted unique collection (also a red-black tree). Duplicate inserts
    // are silently ignored. Use it when you need O(log n) membership tests with sorted order;
    // use unordered_set for O(1) average-case membership without ordering.
    std::set<int> s{3, 1, 4, 1, 5, 9, 2, 6};
    std::cout << "Set (unique, ordered): ";
    for (auto n : s) std::cout << n << " ";
    std::cout << "\n";  // => Set (unique, ordered): 1 2 3 4 5 6 9

    // unordered_map is a hash table — O(1) average lookup but no ordering guarantees.
    // operator[] on a missing key default-inserts (0 for int), which is a common bug source.
    // Prefer .find() or .contains() (C++20) for existence checks.
    std::unordered_map<std::string, int> um{{"x", 10}, {"y", 20}, {"z", 30}};
    std::cout << "unordered_map[y] = " << um["y"] << "\n";  // => unordered_map[y] = 20

    // std::array<T, N> is a fixed-size stack-allocated array with STL interface. Unlike
    // C arrays, it knows its own size, is copyable, and doesn't decay to a pointer.
    // The size N is a template parameter — it must be a compile-time constant.
    std::array<int, 5> arr{10, 20, 30, 40, 50};
    std::cout << "std::array size=" << arr.size() << ", [2]=" << arr[2] << "\n";  // => std::array size=5, [2]=30

    // std::deque (double-ended queue) is a segmented array — O(1) push/pop on both ends,
    // unlike vector which is O(n) for push_front. The tradeoff: non-contiguous memory,
    // so cache performance is slightly worse than vector for sequential access.
    std::deque<int> dq{2, 3, 4};
    dq.push_front(1);
    dq.push_back(5);
    std::cout << "Deque: ";
    for (auto n : dq) std::cout << n << " ";
    std::cout << "\n";  // => Deque: 1 2 3 4 5
}

// ─── 4. Algorithms ─────────────────────────────────────────
void algorithms() {
    header("4. ALGORITHMS — sort, transform, accumulate, ranges::views");

    std::vector<int> nums{5, 2, 8, 1, 9, 3};

    // std::greater<>() is a transparent comparator (the empty <> uses template deduction).
    // It reverses the default less-than ordering. The `auto sorted = nums` copies the vector
    // to avoid mutating the original — a pattern for when you need both sorted and unsorted versions.
    auto sorted = nums;
    std::sort(sorted.begin(), sorted.end(), std::greater<>());
    std::cout << "Sorted desc: ";
    for (auto n : sorted) std::cout << n << " ";
    std::cout << "\n";  // => Sorted desc: 9 8 5 3 2 1

    // transform applies a function to each element and writes results to an output iterator.
    // The output vector must be pre-sized — transform doesn't grow it. For growing output,
    // use std::back_inserter(result) as the output iterator.
    std::vector<int> doubled(nums.size());
    std::transform(nums.begin(), nums.end(), doubled.begin(), [](int n) { return n * 2; });
    std::cout << "Doubled: ";
    for (auto n : doubled) std::cout << n << " ";
    std::cout << "\n";  // => Doubled: 10 4 16 2 18 6

    // accumulate is a left fold: starts with an initial value and combines each element.
    // The default operation is addition. std::multiplies<>() is a function object that performs
    // multiplication — it's the STL's way of passing operators as first-class objects.
    // Note: accumulate is in <numeric>, not <algorithm>.
    int sum = std::accumulate(nums.begin(), nums.end(), 0);
    int product = std::accumulate(nums.begin(), nums.end(), 1, std::multiplies<>());
    std::cout << "Sum=" << sum << ", Product=" << product << "\n";  // => Sum=28, Product=2160

    // Ranges pipelines compose filter and transform lazily — no intermediate vectors are created.
    // This is equivalent to the traditional begin/end algorithm chain but far more readable.
    // The pipe syntax mirrors Unix command pipelines: data | step1 | step2.
    auto pipeline = nums | std::views::filter([](int n) { return n > 3; })
                        | std::views::transform([](int n) { return n * n; });
    std::cout << "Ranges (>3, squared): ";
    for (auto v : pipeline) std::cout << v << " ";
    std::cout << "\n";  // => Ranges (>3, squared): 25 64 81

    // ranges:: algorithms accept the container directly instead of begin/end pairs — less
    // boilerplate and safer (no iterator mismatch bugs). ranges::sort is a constrained algorithm
    // that requires the range to satisfy sortable concept.
    auto v2 = nums;
    std::ranges::sort(v2);
    std::cout << "ranges::sort: ";
    for (auto n : v2) std::cout << n << " ";
    std::cout << "\n";  // => ranges::sort: 1 2 3 5 8 9

    auto it = std::ranges::find(v2, 5);
    std::cout << "ranges::find(5): " << (it != v2.end() ? "found" : "not found") << "\n";  // => ranges::find(5): found
}

// ─── 5. OOP ────────────────────────────────────────────────
void oop() {
    header("5. OOP — Classes, Inheritance, Virtual, RAII, Rule of Five");

    // This class demonstrates the Rule of Five: if you define any of destructor, copy constructor,
    // copy assignment, move constructor, or move assignment, you should define all five.
    // Reason: the compiler's auto-generated versions do shallow copies, which would cause
    // double-free bugs when the class manages a raw pointer.
    class Resource {
        std::string name_;
        int* data_;
        size_t size_;
    public:
        // `explicit` prevents implicit conversion from {string, size_t} to Resource.
        // std::move(name) avoids copying the string — the parameter is already a temporary.
        explicit Resource(std::string name, size_t sz)
            : name_(std::move(name)), data_(new int[sz]), size_(sz) {
            std::fill(data_, data_ + sz, 0);
        }
        // Destructor: RAII (Resource Acquisition Is Initialization) — the destructor releases
        // the resource automatically when the object goes out of scope. No garbage collector
        // needed; deterministic cleanup at the end of the scope.
        ~Resource() { delete[] data_; }
        // Copy constructor: deep-copies the heap data so each Resource owns its own memory.
        // Without this, the default shallow copy would make two objects point to the same
        // array, causing a double-free when both destructors run.
        Resource(const Resource& o) : name_(o.name_ + "_copy"), data_(new int[o.size_]), size_(o.size_) {
            std::copy(o.data_, o.data_ + o.size_, data_);
        }
        // Copy assignment: self-assignment check (this != &o) prevents deleting your own data.
        // This is the copy-and-swap idiom's manual equivalent — it first frees old resources,
        // then allocates new ones. In production, prefer the copy-and-swap idiom for exception safety.
        Resource& operator=(const Resource& o) {
            if (this != &o) {
                delete[] data_;
                name_ = o.name_ + "_copy";
                size_ = o.size_;
                data_ = new int[size_];
                std::copy(o.data_, o.data_ + size_, data_);
            }
            return *this;
        }
        // Move constructor: steals the source's resources (pointer, size) instead of copying.
        // Setting o.data_ = nullptr ensures the source's destructor won't free the stolen memory.
        // noexcept is critical — STL containers (vector::push_back) only use move if it's noexcept,
        // otherwise they fall back to copying for exception safety.
        Resource(Resource&& o) noexcept : name_(std::move(o.name_)), data_(o.data_), size_(o.size_) {
            o.data_ = nullptr; o.size_ = 0;
        }
        // Move assignment: same pattern — release your own resources, steal the source's.
        // Self-assignment check is needed even for moves (e.g., x = std::move(x)).
        Resource& operator=(Resource&& o) noexcept {
            if (this != &o) {
                delete[] data_;
                name_ = std::move(o.name_);
                data_ = o.data_; size_ = o.size_;
                o.data_ = nullptr; o.size_ = 0;
            }
            return *this;
        }
        void set(size_t i, int v) { if (i < size_) data_[i] = v; }
        int get(size_t i) const { return i < size_ ? data_[i] : -1; }
        const std::string& name() const { return name_; }
    };

    Resource r("alpha", 3);
    r.set(0, 42);
    Resource r2 = r; // invokes copy constructor — deep copies the array
    Resource r3 = std::move(r); // invokes move constructor — steals r's pointer, r is now hollow
    std::cout << "Original (moved): " << r.name() << "\n";  // => Original (moved):
    std::cout << "Copy: " << r2.name() << " [0]=" << r2.get(0) << "\n";  // => Copy: alpha_copy [0]=42
    std::cout << "Moved: " << r3.name() << " [0]=" << r3.get(0) << "\n";  // => Moved: alpha [0]=42

    // Virtual functions enable runtime polymorphism via vtable dispatch. `= 0` makes area()
    // pure virtual — Shape can't be instantiated, only derived classes can.
    // virtual ~Shape() = default is essential: without a virtual destructor, deleting a
    // derived object through a base pointer would skip the derived destructor (undefined behavior).
    struct Shape {
        virtual ~Shape() = default;
        virtual double area() const = 0;
        virtual std::string desc() const { return "Shape"; }
    };
    // `override` (C++11) is a compile-time assertion that this method actually overrides
    // a virtual function — catches typos and signature mismatches. Always use it.
    struct Circle : Shape {
        double r;
        explicit Circle(double r) : r(r) {}
        double area() const override { return 3.14159 * r * r; }
        std::string desc() const override { return "Circle(r=" + std::to_string(r) + ")"; }
    };
    struct Rect : Shape {
        double w, h;
        Rect(double w, double h) : w(w), h(h) {}
        double area() const override { return w * h; }
        std::string desc() const override { return "Rect(" + std::to_string(w) + "x" + std::to_string(h) + ")"; }
    };

    // vector<unique_ptr<Shape>> owns polymorphic objects. unique_ptr handles deletion,
    // and virtual dispatch routes method calls to the correct derived implementation.
    // This is the modern C++ replacement for raw pointer arrays of base classes.
    std::vector<std::unique_ptr<Shape>> shapes;
    shapes.push_back(std::make_unique<Circle>(5.0));
    shapes.push_back(std::make_unique<Rect>(4.0, 6.0));
    for (auto& s : shapes) {
        std::cout << s->desc() << " area=" << s->area() << "\n";  // => Circle(r=5.000000) area=78.5398 / Rect(4.000000x6.000000) area=24
    }
}

// ─── 6. Templates ───────────────────────────────────────────
// Concepts (C++20) replace SFINAE for constraining templates. `Numeric` is a named
// requirement: "T must be integral or floating-point." If violated, the compiler gives
// a clean error like "constraint not satisfied" instead of pages of template instantiation noise.
template<typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

// Using a concept as a template parameter constraint — only Numeric types are accepted.
// This is checked at the call site: clamp_val("hello", ...) would fail with a clear message.
template<Numeric T>
T clamp_val(T val, T lo, T hi) {
    return val < lo ? lo : (val > hi ? hi : val);
}

// Non-type template parameters (size_t N) let you embed compile-time constants into types.
// StaticVec<int, 8> and StaticVec<int, 16> are completely different types — the size is baked in.
// This enables stack allocation with known bounds, avoiding heap allocation entirely.
template<typename T, size_t N>
class StaticVec {
    std::array<T, N> data_{};
    size_t len_ = 0;
public:
    void push(T val) { if (len_ < N) data_[len_++] = std::move(val); }
    size_t size() const { return len_; }
    T& operator[](size_t i) { return data_[i]; }
    void print() const {
        std::cout << "[";
        for (size_t i = 0; i < len_; ++i) {
            if (i > 0) std::cout << ", ";
            std::cout << data_[i];
        }
        std::cout << "]\n";
    }
};

// SFINAE (Substitution Failure Is Not An Error) — the pre-C++20 way to constrain templates.
// enable_if_t removes this overload from consideration if T isn't arithmetic.
// If substitution fails (e.g., T = string), it's not a compile error — the overload is just ignored.
// Prefer concepts in C++20 code; SFINAE remains common in older codebases and library headers.
template<typename T, typename = std::enable_if_t<std::is_arithmetic_v<T>>>
T square(T x) { return x * x; }

void templates() {
    header("6. TEMPLATES — Function, Class, Concepts, SFINAE");

    std::cout << "clamp(15, 0, 10) = " << clamp_val(15, 0, 10) << "\n";  // => clamp(15, 0, 10) = 10
    std::cout << "clamp(3.5, 0.0, 10.0) = " << clamp_val(3.5, 0.0, 10.0) << "\n";  // => clamp(3.5, 0.0, 10.0) = 3.5

    StaticVec<int, 8> sv;
    sv.push(10); sv.push(20); sv.push(30);
    std::cout << "StaticVec: "; sv.print();  // => StaticVec: [10, 20, 30]
    std::cout << "StaticVec size=" << sv.size() << ", [1]=" << sv[1] << "\n";  // => StaticVec size=3, [1]=20

    std::cout << "SFINAE square(7) = " << square(7) << "\n";  // => SFINAE square(7) = 49
    std::cout << "SFINAE square(2.5) = " << square(2.5) << "\n";  // => SFINAE square(2.5) = 6.25
}

// ─── 7. Concurrency ────────────────────────────────────────
void concurrency() {
    header("7. CONCURRENCY — thread, mutex, async/future, atomic");

    // std::thread creates an OS thread. Unlike Rust, C++ doesn't enforce data ownership
    // at compile time — it's your responsibility to avoid data races. The shared_ptr here
    // is captured by value (reference count incremented), giving the thread shared ownership.
    auto result = std::make_shared<int>(0);
    std::thread t([result]() {
        int sum = 0;
        for (int i = 1; i <= 100; ++i) sum += i;
        *result = sum;
    });
    // join() blocks until the thread finishes. You MUST call join() or detach() before the
    // std::thread object is destroyed — otherwise the destructor calls std::terminate().
    // This is a deliberate design choice to prevent accidentally ignoring thread results.
    t.join();
    std::cout << "Thread result: " << *result << "\n";  // => Thread result: 5050

    // lock_guard is an RAII wrapper — it locks the mutex in its constructor and unlocks in
    // its destructor, guaranteeing the lock is released even if an exception is thrown.
    // [&] captures everything by reference — convenient but dangerous in multithreading
    // because the compiler won't catch data races. Only `counter` and `mtx` are actually used.
    std::mutex mtx;
    int counter = 0;
    std::vector<std::thread> threads;
    for (int i = 0; i < 5; ++i) {
        threads.emplace_back([&]() {
            for (int j = 0; j < 100; ++j) {
                std::lock_guard<std::mutex> lock(mtx);
                ++counter;
            }
        });
    }
    for (auto& th : threads) th.join();
    std::cout << "Mutex counter: " << counter << "\n";  // => Mutex counter: 500

    // std::async launches a task that may run on a new thread (launch::async) or deferred
    // (lazy evaluation on .get()). The returned future holds the result — calling .get()
    // blocks until the task completes. This is higher-level than raw threads: no manual
    // join, no shared state management, exception propagation across threads.
    auto fut = std::async(std::launch::async, []() {
        int product = 1;
        for (int i = 1; i <= 10; ++i) product *= i;
        return product;
    });
    std::cout << "Async 10! = " << fut.get() << "\n";  // => Async 10! = 3628800

    // std::atomic provides lock-free thread-safe operations via CPU atomic instructions.
    // memory_order_relaxed is the weakest ordering — no synchronization guarantees beyond
    // the atomic variable itself. For a simple counter this is sufficient and fastest.
    // Use memory_order_seq_cst (the default) when you need ordering between atomics.
    std::atomic<int> atom{0};
    std::vector<std::thread> athreads;
    for (int i = 0; i < 5; ++i) {
        athreads.emplace_back([&atom]() {
            for (int j = 0; j < 100; ++j) atom.fetch_add(1, std::memory_order_relaxed);
        });
    }
    for (auto& th : athreads) th.join();
    std::cout << "Atomic counter: " << atom.load() << "\n";  // => Atomic counter: 500
}

// ─── 8. Modern C++ ─────────────────────────────────────────
void modern_cpp() {
    header("8. MODERN — optional, variant, span (format requires libfmt)");

    // std::optional<T> (C++17) is a type-safe alternative to "return -1 on failure" or
    // "return a pointer that might be null." It either holds a T or std::nullopt.
    // The boolean conversion (if (r1)) checks whether a value is present.
    // This is C++'s equivalent of Rust's Option<T> or Haskell's Maybe.
    auto find_even = [](const std::vector<int>& v) -> std::optional<int> {
        for (auto n : v) if (n % 2 == 0) return n;
        return std::nullopt;
    };
    auto r1 = find_even({1, 3, 4, 7});
    auto r2 = find_even({1, 3, 7});
    std::cout << "find_even({1,3,4,7}): " << (r1 ? std::to_string(*r1) : "none") << "\n";  // => find_even({1,3,4,7}): 4
    std::cout << "find_even({1,3,7}):   " << (r2 ? std::to_string(*r2) : "none") << "\n";  // => find_even({1,3,7}):   none

    // std::variant<Types...> (C++17) is a type-safe union — it holds exactly one of the
    // listed types at any time. Unlike C unions, accessing the wrong type throws bad_variant_access.
    // std::visit with a generic lambda is the idiomatic way to handle all cases.
    // `if constexpr` makes branching compile-time — only the matching branch is compiled for each type.
    using Var = std::variant<int, double, std::string>;
    std::vector<Var> vars{42, 3.14, std::string("hello")};
    for (auto& v : vars) {
        // std::visit invokes the visitor with the active alternative. The generic lambda
        // is instantiated once per variant type — `if constexpr` selects the branch at compile time.
        // std::decay_t strips references and const to get the clean type for comparison.
        std::visit([](auto&& arg) {
            using T = std::decay_t<decltype(arg)>;
            if constexpr (std::is_same_v<T, int>) std::cout << "int: " << arg << "\n";  // => int: 42
            else if constexpr (std::is_same_v<T, double>) std::cout << "double: " << arg << "\n";  // => double: 3.14
            else std::cout << "string: " << arg << "\n";  // => string: hello
        }, v);
    }

    // std::span<T> (C++20) is a non-owning view over contiguous memory — like a slice in
    // Rust (&[T]) or Go. It stores a pointer and a length, with zero overhead.
    // Use span as a function parameter to accept arrays, vectors, and C arrays uniformly
    // without templates or overloads. subspan(offset, count) creates a sub-view.
    int raw[] = {10, 20, 30, 40, 50};
    auto print_span = [](std::span<int> s) {
        std::cout << "span: ";
        for (auto v : s) std::cout << v << " ";
        std::cout << "\n";
    };
    print_span(raw);  // => span: 10 20 30 40 50
    print_span(std::span(raw).subspan(1, 3));  // => span: 20 30 40
}

// ─── 9. Lambdas ─────────────────────────────────────────────
void lambdas() {
    header("9. LAMBDAS — Capture modes, generic, IIFE");

    // C++ lambdas have explicit capture modes, unlike closures in most languages.
    // [x] captures x by value — a copy is made at lambda creation time. Later changes
    // to the original `x` don't affect the captured copy. The lambda body is const by default.
    int x = 10;
    auto by_val = [x]() { return x * 2; };
    std::cout << "Capture by value: " << by_val() << "\n";  // => Capture by value: 20

    // [&total] captures by reference — the lambda reads and writes the original variable.
    // Danger: if the lambda outlives the referenced variable (e.g., returned from a function),
    // you get a dangling reference. Rust's borrow checker prevents this; C++ does not.
    int total = 0;
    auto by_ref = [&total](int v) { total += v; };
    by_ref(5); by_ref(15);
    std::cout << "Capture by ref, total: " << total << "\n";  // => Capture by ref, total: 20

    // [=] captures ALL referenced variables by value; [&] captures ALL by reference.
    // These are convenient but hide exactly what's captured — prefer explicit captures
    // in production code for clarity and to avoid accidental captures of `this`.
    int a = 1, b = 2;
    auto all_val = [=]() { return a + b; };
    auto all_ref = [&]() { a += 10; b += 20; };
    std::cout << "Capture [=]: " << all_val() << "\n";  // => Capture [=]: 3
    all_ref();
    std::cout << "After [&]: a=" << a << ", b=" << b << "\n";  // => After [&]: a=11, b=22

    // Generic lambdas (auto parameters) are implicitly template lambdas — the compiler
    // generates a separate instantiation for each argument type used. This is C++'s
    // equivalent of Rust's generic closures, but without explicit trait bounds.
    auto generic_add = [](auto a, auto b) { return a + b; };
    std::cout << "Generic lambda int: " << generic_add(3, 4) << "\n";  // => Generic lambda int: 7
    std::cout << "Generic lambda str: " << generic_add(std::string("he"), std::string("llo")) << "\n";  // => Generic lambda str: hello

    // IIFE (Immediately Invoked Function Expression): a lambda called right where it's defined.
    // The trailing () invokes it. Use IIFE to initialize const variables with complex logic
    // that would otherwise require a mutable temporary or a helper function.
    auto val = []() {
        std::vector<int> v{1, 2, 3, 4, 5};
        return std::accumulate(v.begin(), v.end(), 0);
    }();
    std::cout << "IIFE result: " << val << "\n";  // => IIFE result: 15

    // `mutable` on a lambda allows modifying captured-by-value variables. Without it,
    // the lambda's operator() is const, so captured copies can't be changed. The captured `n`
    // is a separate copy — incrementing it doesn't affect anything outside the lambda.
    // Use this for stateful lambdas like counters or accumulators.
    auto counter = [n = 0]() mutable { return ++n; };
    std::cout << "Mutable lambda: " << counter() << ", " << counter() << ", " << counter() << "\n";  // => (varies, e.g. Mutable lambda: 3, 2, 1 — evaluation order is unspecified)
}

// ─── 10. Move Semantics ─────────────────────────────────────
void move_semantics() {
    header("10. MOVE SEMANTICS — rvalue refs, std::move, perfect forwarding");

    // std::move doesn't actually move anything — it's a cast to rvalue reference (T&&).
    // The actual move happens when an rvalue reference is passed to a move constructor or
    // move assignment operator. After the move, `s` is in a "valid but unspecified state" —
    // it's safe to destroy or reassign, but its contents are undefined.
    std::string s = "hello";
    std::string&& rref = std::move(s);
    std::string s2 = std::move(rref);
    std::cout << "After move: s=\"" << s << "\", s2=\"" << s2 << "\"\n";  // => After move: s="", s2="hello"

    // Moving a vector transfers the internal buffer pointer — O(1) instead of O(n) copying.
    // After move, src is empty (size 0). This is why move semantics matter for performance:
    // returning large containers from functions is cheap because the compiler can move them.
    std::vector<std::string> src;
    for (int i = 0; i < 5; ++i) src.push_back("item_" + std::to_string(i));
    auto dst = std::move(src);
    std::cout << "Moved vector — src.size()=" << src.size()
              << ", dst.size()=" << dst.size() << "\n";  // => Moved vector — src.size()=0, dst.size()=5

    // Perfect forwarding preserves the value category (lvalue vs rvalue) of arguments.
    // T&& in a template context is a "forwarding reference" (not an rvalue reference) —
    // it can bind to both lvalues and rvalues. std::forward<T>(val) casts back to the
    // original category. Use this in wrapper functions that pass arguments to another function
    // without losing move semantics. Without forward, rvalues would be treated as lvalues.
    auto forwarder = []<typename T>(T&& val) {
        using Type = std::decay_t<T>;
        if constexpr (std::is_lvalue_reference_v<T>) {
            std::cout << "  Forwarded as lvalue ref\n";  // =>   Forwarded as lvalue ref
        } else {
            std::cout << "  Forwarded as rvalue ref\n";  // =>   Forwarded as rvalue ref
        }
        return std::forward<T>(val);
    };

    std::string lv = "lvalue";
    std::cout << "Forwarding lvalue:\n";  // => Forwarding lvalue:
    forwarder(lv);
    std::cout << "Forwarding rvalue:\n";  // => Forwarding rvalue:
    forwarder(std::string("rvalue"));

    // emplace_back constructs the object in-place within the vector's memory, avoiding a
    // temporary + move. push_back(make_pair(...)) creates a pair, then moves it into the vector.
    // emplace_back("emplace_back", 2) constructs the pair directly — one fewer move operation.
    // In practice the performance difference is small, but emplace is more expressive.
    std::vector<std::pair<std::string, int>> vp;
    vp.push_back(std::make_pair("push_back", 1));  // construct + move
    vp.emplace_back("emplace_back", 2);              // construct in place
    std::cout << "emplace vs push: ";
    for (auto& [k, v] : vp) std::cout << k << "=" << v << " ";
    std::cout << "\n";  // => emplace vs push: push_back=1 emplace_back=2
}

int main() {
    std::cout << "================================================================\n";  // => ================================================================
    std::cout << "  C++20 FUNDAMENTALS — Comprehensive Showcase\n";  // =>   C++20 FUNDAMENTALS — Comprehensive Showcase
    std::cout << "================================================================\n";  // => ================================================================

    basics();
    smart_pointers();
    containers();
    algorithms();
    oop();
    templates();
    concurrency();
    modern_cpp();
    lambdas();
    move_semantics();

    std::cout << "\n================================================================\n";  // => ================================================================
    std::cout << "  All sections complete.\n";  // =>   All sections complete.
    std::cout << "================================================================\n";  // => ================================================================
    return 0;
}
