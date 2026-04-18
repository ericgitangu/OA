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

    // auto type deduction
    auto x = 42;
    auto pi = 3.14159;
    auto msg = std::string("hello C++20");
    std::cout << "auto: x=" << x << ", pi=" << pi << ", msg=" << msg << "\n";

    // structured bindings
    std::pair<std::string, int> entry{"Alice", 30};
    auto& [name, age] = entry;
    std::cout << "Structured binding: " << name << " age " << age << "\n";

    struct Point { double x, y; };
    auto [px, py] = Point{3.0, 4.0};
    std::cout << "Point destructured: (" << px << ", " << py << ")\n";

    // ranges and views
    std::vector<int> nums{1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    auto evens = nums | std::views::filter([](int n) { return n % 2 == 0; })
                      | std::views::transform([](int n) { return n * n; });
    std::cout << "Even squares (ranges): ";
    for (auto v : evens) std::cout << v << " ";
    std::cout << "\n";

    // ranges::take, reverse
    auto first3 = nums | std::views::take(3);
    std::cout << "First 3: ";
    for (auto v : first3) std::cout << v << " ";
    std::cout << "\n";

    // concepts (inline)
    auto add = []<typename T>(T a, T b) requires std::integral<T> { return a + b; };
    std::cout << "Concept-constrained add: " << add(10, 20) << "\n";
}

// ─── 2. Smart Pointers ─────────────────────────────────────
void smart_pointers() {
    header("2. SMART POINTERS — unique_ptr, shared_ptr");

    // unique_ptr — exclusive ownership
    auto up = std::make_unique<std::string>("unique data");
    std::cout << "unique_ptr: " << *up << "\n";
    auto up2 = std::move(up); // transfer ownership
    std::cout << "After move, up is " << (up ? "valid" : "null")
              << ", up2 = " << *up2 << "\n";

    // unique_ptr with custom deleter
    auto arr = std::make_unique<int[]>(5);
    for (int i = 0; i < 5; ++i) arr[i] = i * 10;
    std::cout << "unique_ptr array: ";
    for (int i = 0; i < 5; ++i) std::cout << arr[i] << " ";
    std::cout << "\n";

    // shared_ptr — reference counted
    auto sp1 = std::make_shared<std::string>("shared data");
    auto sp2 = sp1;
    auto sp3 = sp1;
    std::cout << "shared_ptr use_count: " << sp1.use_count()
              << ", value: " << *sp1 << "\n";
    sp2.reset();
    std::cout << "After reset: use_count = " << sp1.use_count() << "\n";

    // weak_ptr
    std::weak_ptr<std::string> wp = sp1;
    if (auto locked = wp.lock()) {
        std::cout << "weak_ptr locked: " << *locked << "\n";
    }
}

// ─── 3. Containers ─────────────────────────────────────────
void containers() {
    header("3. CONTAINERS — vector, map, set, unordered_map, array, deque");

    std::vector<int> v{5, 3, 1, 4, 2};
    std::sort(v.begin(), v.end());
    std::cout << "Sorted vector: ";
    for (auto n : v) std::cout << n << " ";
    std::cout << "\n";

    std::map<std::string, int> m{{"apple", 3}, {"banana", 1}, {"cherry", 5}};
    m["date"] = 2;
    std::cout << "Map (ordered): ";
    for (auto& [k, val] : m) std::cout << k << "=" << val << " ";
    std::cout << "\n";

    std::set<int> s{3, 1, 4, 1, 5, 9, 2, 6};
    std::cout << "Set (unique, ordered): ";
    for (auto n : s) std::cout << n << " ";
    std::cout << "\n";

    std::unordered_map<std::string, int> um{{"x", 10}, {"y", 20}, {"z", 30}};
    std::cout << "unordered_map[y] = " << um["y"] << "\n";

    std::array<int, 5> arr{10, 20, 30, 40, 50};
    std::cout << "std::array size=" << arr.size() << ", [2]=" << arr[2] << "\n";

    std::deque<int> dq{2, 3, 4};
    dq.push_front(1);
    dq.push_back(5);
    std::cout << "Deque: ";
    for (auto n : dq) std::cout << n << " ";
    std::cout << "\n";
}

// ─── 4. Algorithms ─────────────────────────────────────────
void algorithms() {
    header("4. ALGORITHMS — sort, transform, accumulate, ranges::views");

    std::vector<int> nums{5, 2, 8, 1, 9, 3};

    // sort with custom comparator
    auto sorted = nums;
    std::sort(sorted.begin(), sorted.end(), std::greater<>());
    std::cout << "Sorted desc: ";
    for (auto n : sorted) std::cout << n << " ";
    std::cout << "\n";

    // transform
    std::vector<int> doubled(nums.size());
    std::transform(nums.begin(), nums.end(), doubled.begin(), [](int n) { return n * 2; });
    std::cout << "Doubled: ";
    for (auto n : doubled) std::cout << n << " ";
    std::cout << "\n";

    // accumulate
    int sum = std::accumulate(nums.begin(), nums.end(), 0);
    int product = std::accumulate(nums.begin(), nums.end(), 1, std::multiplies<>());
    std::cout << "Sum=" << sum << ", Product=" << product << "\n";

    // ranges pipeline
    auto pipeline = nums | std::views::filter([](int n) { return n > 3; })
                        | std::views::transform([](int n) { return n * n; });
    std::cout << "Ranges (>3, squared): ";
    for (auto v : pipeline) std::cout << v << " ";
    std::cout << "\n";

    // ranges::sort, ranges::find
    auto v2 = nums;
    std::ranges::sort(v2);
    std::cout << "ranges::sort: ";
    for (auto n : v2) std::cout << n << " ";
    std::cout << "\n";

    auto it = std::ranges::find(v2, 5);
    std::cout << "ranges::find(5): " << (it != v2.end() ? "found" : "not found") << "\n";
}

// ─── 5. OOP ────────────────────────────────────────────────
void oop() {
    header("5. OOP — Classes, Inheritance, Virtual, RAII, Rule of Five");

    class Resource {
        std::string name_;
        int* data_;
        size_t size_;
    public:
        // constructor
        explicit Resource(std::string name, size_t sz)
            : name_(std::move(name)), data_(new int[sz]), size_(sz) {
            std::fill(data_, data_ + sz, 0);
        }
        // destructor (RAII)
        ~Resource() { delete[] data_; }
        // copy constructor
        Resource(const Resource& o) : name_(o.name_ + "_copy"), data_(new int[o.size_]), size_(o.size_) {
            std::copy(o.data_, o.data_ + o.size_, data_);
        }
        // copy assignment
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
        // move constructor
        Resource(Resource&& o) noexcept : name_(std::move(o.name_)), data_(o.data_), size_(o.size_) {
            o.data_ = nullptr; o.size_ = 0;
        }
        // move assignment
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
    Resource r2 = r; // copy
    Resource r3 = std::move(r); // move
    std::cout << "Original (moved): " << r.name() << "\n";
    std::cout << "Copy: " << r2.name() << " [0]=" << r2.get(0) << "\n";
    std::cout << "Moved: " << r3.name() << " [0]=" << r3.get(0) << "\n";

    // inheritance + virtual
    struct Shape {
        virtual ~Shape() = default;
        virtual double area() const = 0;
        virtual std::string desc() const { return "Shape"; }
    };
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

    std::vector<std::unique_ptr<Shape>> shapes;
    shapes.push_back(std::make_unique<Circle>(5.0));
    shapes.push_back(std::make_unique<Rect>(4.0, 6.0));
    for (auto& s : shapes) {
        std::cout << s->desc() << " area=" << s->area() << "\n";
    }
}

// ─── 6. Templates ───────────────────────────────────────────
template<typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

template<Numeric T>
T clamp_val(T val, T lo, T hi) {
    return val < lo ? lo : (val > hi ? hi : val);
}

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

// SFINAE example
template<typename T, typename = std::enable_if_t<std::is_arithmetic_v<T>>>
T square(T x) { return x * x; }

void templates() {
    header("6. TEMPLATES — Function, Class, Concepts, SFINAE");

    std::cout << "clamp(15, 0, 10) = " << clamp_val(15, 0, 10) << "\n";
    std::cout << "clamp(3.5, 0.0, 10.0) = " << clamp_val(3.5, 0.0, 10.0) << "\n";

    StaticVec<int, 8> sv;
    sv.push(10); sv.push(20); sv.push(30);
    std::cout << "StaticVec: "; sv.print();
    std::cout << "StaticVec size=" << sv.size() << ", [1]=" << sv[1] << "\n";

    std::cout << "SFINAE square(7) = " << square(7) << "\n";
    std::cout << "SFINAE square(2.5) = " << square(2.5) << "\n";
}

// ─── 7. Concurrency ────────────────────────────────────────
void concurrency() {
    header("7. CONCURRENCY — thread, mutex, async/future, atomic");

    // basic thread
    auto result = std::make_shared<int>(0);
    std::thread t([result]() {
        int sum = 0;
        for (int i = 1; i <= 100; ++i) sum += i;
        *result = sum;
    });
    t.join();
    std::cout << "Thread result: " << *result << "\n";

    // mutex
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
    std::cout << "Mutex counter: " << counter << "\n";

    // async + future
    auto fut = std::async(std::launch::async, []() {
        int product = 1;
        for (int i = 1; i <= 10; ++i) product *= i;
        return product;
    });
    std::cout << "Async 10! = " << fut.get() << "\n";

    // atomic
    std::atomic<int> atom{0};
    std::vector<std::thread> athreads;
    for (int i = 0; i < 5; ++i) {
        athreads.emplace_back([&atom]() {
            for (int j = 0; j < 100; ++j) atom.fetch_add(1, std::memory_order_relaxed);
        });
    }
    for (auto& th : athreads) th.join();
    std::cout << "Atomic counter: " << atom.load() << "\n";
}

// ─── 8. Modern C++ ─────────────────────────────────────────
void modern_cpp() {
    header("8. MODERN — optional, variant, span (format requires libfmt)");

    // optional
    auto find_even = [](const std::vector<int>& v) -> std::optional<int> {
        for (auto n : v) if (n % 2 == 0) return n;
        return std::nullopt;
    };
    auto r1 = find_even({1, 3, 4, 7});
    auto r2 = find_even({1, 3, 7});
    std::cout << "find_even({1,3,4,7}): " << (r1 ? std::to_string(*r1) : "none") << "\n";
    std::cout << "find_even({1,3,7}):   " << (r2 ? std::to_string(*r2) : "none") << "\n";

    // variant
    using Var = std::variant<int, double, std::string>;
    std::vector<Var> vars{42, 3.14, std::string("hello")};
    for (auto& v : vars) {
        std::visit([](auto&& arg) {
            using T = std::decay_t<decltype(arg)>;
            if constexpr (std::is_same_v<T, int>) std::cout << "int: " << arg << "\n";
            else if constexpr (std::is_same_v<T, double>) std::cout << "double: " << arg << "\n";
            else std::cout << "string: " << arg << "\n";
        }, v);
    }

    // span — non-owning view
    int raw[] = {10, 20, 30, 40, 50};
    auto print_span = [](std::span<int> s) {
        std::cout << "span: ";
        for (auto v : s) std::cout << v << " ";
        std::cout << "\n";
    };
    print_span(raw);
    print_span(std::span(raw).subspan(1, 3));
}

// ─── 9. Lambdas ─────────────────────────────────────────────
void lambdas() {
    header("9. LAMBDAS — Capture modes, generic, IIFE");

    // capture by value
    int x = 10;
    auto by_val = [x]() { return x * 2; };
    std::cout << "Capture by value: " << by_val() << "\n";

    // capture by reference
    int total = 0;
    auto by_ref = [&total](int v) { total += v; };
    by_ref(5); by_ref(15);
    std::cout << "Capture by ref, total: " << total << "\n";

    // capture all by value [=], all by ref [&]
    int a = 1, b = 2;
    auto all_val = [=]() { return a + b; };
    auto all_ref = [&]() { a += 10; b += 20; };
    std::cout << "Capture [=]: " << all_val() << "\n";
    all_ref();
    std::cout << "After [&]: a=" << a << ", b=" << b << "\n";

    // generic lambda (C++14/20)
    auto generic_add = [](auto a, auto b) { return a + b; };
    std::cout << "Generic lambda int: " << generic_add(3, 4) << "\n";
    std::cout << "Generic lambda str: " << generic_add(std::string("he"), std::string("llo")) << "\n";

    // immediately invoked function expression (IIFE)
    auto val = []() {
        std::vector<int> v{1, 2, 3, 4, 5};
        return std::accumulate(v.begin(), v.end(), 0);
    }();
    std::cout << "IIFE result: " << val << "\n";

    // mutable lambda
    auto counter = [n = 0]() mutable { return ++n; };
    std::cout << "Mutable lambda: " << counter() << ", " << counter() << ", " << counter() << "\n";
}

// ─── 10. Move Semantics ─────────────────────────────────────
void move_semantics() {
    header("10. MOVE SEMANTICS — rvalue refs, std::move, perfect forwarding");

    // rvalue reference
    std::string s = "hello";
    std::string&& rref = std::move(s);
    std::string s2 = std::move(rref);
    std::cout << "After move: s=\"" << s << "\", s2=\"" << s2 << "\"\n";

    // demonstrating move vs copy performance
    std::vector<std::string> src;
    for (int i = 0; i < 5; ++i) src.push_back("item_" + std::to_string(i));
    auto dst = std::move(src);
    std::cout << "Moved vector — src.size()=" << src.size()
              << ", dst.size()=" << dst.size() << "\n";

    // perfect forwarding
    auto forwarder = []<typename T>(T&& val) {
        using Type = std::decay_t<T>;
        if constexpr (std::is_lvalue_reference_v<T>) {
            std::cout << "  Forwarded as lvalue ref\n";
        } else {
            std::cout << "  Forwarded as rvalue ref\n";
        }
        return std::forward<T>(val);
    };

    std::string lv = "lvalue";
    std::cout << "Forwarding lvalue:\n";
    forwarder(lv);
    std::cout << "Forwarding rvalue:\n";
    forwarder(std::string("rvalue"));

    // emplace_back vs push_back
    std::vector<std::pair<std::string, int>> vp;
    vp.push_back(std::make_pair("push_back", 1));  // construct + move
    vp.emplace_back("emplace_back", 2);              // construct in place
    std::cout << "emplace vs push: ";
    for (auto& [k, v] : vp) std::cout << k << "=" << v << " ";
    std::cout << "\n";
}

int main() {
    std::cout << "================================================================\n";
    std::cout << "  C++20 FUNDAMENTALS — Comprehensive Showcase\n";
    std::cout << "================================================================\n";

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

    std::cout << "\n================================================================\n";
    std::cout << "  All sections complete.\n";
    std::cout << "================================================================\n";
    return 0;
}
