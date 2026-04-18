// js_fundamentals.js — JavaScript Fundamentals (Node.js)
// Run: node js_fundamentals.js

// "use strict" opts into ES5 strict mode: disables silent errors (e.g., assigning to
// undeclared vars throws ReferenceError), forbids `with`, and makes `eval` safer.
// In modules (ESM), strict mode is always on. See MDN: Strict_mode
"use strict";

// ============================================================================
// 1. BASICS
// ============================================================================
console.log("=== 1. BASICS ===\n");

// `let` creates block-scoped mutable bindings (ES6). Unlike `var`, `let` has a
// "temporal dead zone" — referencing it before declaration throws ReferenceError.
// `const` creates block-scoped immutable *bindings* (not immutable values — objects
// and arrays assigned to const can still be mutated internally).
let counter = 0;
const MAX = 100;
console.log(`let/const: counter=${++counter}, MAX=${MAX}`);

// Template literals (backtick strings) use tagged template machinery under the hood:
// the engine splits the string into a TemplateStringsArray + expression values,
// then concatenates them. This enables tagged templates (see BONUS section).
const name = "JavaScript";
console.log(`template literal: ${name} ${2024}`);

// Destructuring uses pattern matching against the iterable protocol (arrays) or
// property access (objects). The engine calls [Symbol.iterator]() for arrays.
// The `...rest` element collects remaining items into a new array via the iterator.
const [first, second, ...remaining] = [10, 20, 30, 40, 50];
console.log(`array destructure: ${first}, ${second}, rest:`, remaining);

// Object destructuring uses property keys to extract values. The `debug: isDebug`
// syntax renames the binding (extracts `debug` but binds it as `isDebug`).
// This is NOT type annotation — it's a rename. A common source of confusion.
const { host, port, debug: isDebug } = { host: "localhost", port: 3000, debug: true };
console.log(`object destructure: ${host}:${port}, debug=${isDebug}`);

// Nested destructuring with defaults: `= {}` provides a fallback if `a` is undefined,
// preventing "Cannot destructure property 'b' of undefined". Defaults only apply
// when the value is `undefined` (not `null` — a common gotcha per TC39 spec).
const { a: { b: nested = 42 } = {} } = { a: { b: 7 } };
console.log(`nested destructure with default: ${nested}`);

// Spread syntax (...) and rest parameters are syntactically identical but semantically
// opposite. Spread *expands* an iterable into individual elements (calls [Symbol.iterator]).
// Rest *collects* individual arguments into an array. Both were introduced in ES6.
const arr1 = [1, 2, 3];
console.log("spread array:", [...arr1, 4, 5]);
// Object spread uses [[OwnPropertyKeys]] + [[Get]] — it performs a shallow copy
// and only copies enumerable own properties. Later properties override earlier ones.
console.log("spread object:", { ...{ x: 1 }, y: 2 });
// Rest parameters replace the legacy `arguments` object. Unlike `arguments`, rest
// params produce a real Array (with map/filter/reduce), not an array-like object.
const sum = (...nums) => nums.reduce((a, n) => a + n, 0);
console.log(`rest params: sum(1,2,3,4) = ${sum(1, 2, 3, 4)}`);

// Optional chaining (?.) short-circuits to `undefined` if the left side is null/undefined.
// Without it, accessing deeply nested properties requires verbose `&&` chains or try/catch.
// It works on property access (.prop), bracket access ([expr]), and method calls (fn?.()).
// See TC39 proposal: https://github.com/tc39/proposal-optional-chaining
const user = { profile: { address: { city: "Portland" } } };
console.log(`optional chain: ${user.profile?.address?.city}`);
// Nullish coalescing (??) returns the right operand ONLY when the left is null/undefined.
// This differs from || which also triggers on falsy values (0, "", false, NaN).
// This distinction matters: `0 ?? "default"` returns 0, but `0 || "default"` returns "default".
console.log(`nullish coal: ${user.profile?.address?.zip ?? "N/A"}`);
// Method optional chaining: ?.() checks if the value is a function before calling it.
// If not callable, it short-circuits to undefined instead of throwing TypeError.
console.log(`method chain: ${user.profile?.getName?.() ?? "no method"}`);

// Demonstrating ?? vs || behavior: ?? only coalesces null/undefined, preserving
// intentional falsy values like 0 and empty string.
const val1 = null ?? "default", val2 = 0 ?? "default", val3 = "" ?? "default";
console.log(`?? : ${val1}, ${val2}, ${val3}`);

// Logical assignment operators (ES2021) combine logical operators with assignment.
// `??=` assigns only if the current value is null/undefined (nullish assignment).
// `||=` assigns only if the current value is falsy. `&&=` assigns only if truthy.
// These short-circuit: the RHS is never evaluated if the condition isn't met.
let la = null; la ??= "assigned";
let lb = 0; lb ||= 99;
console.log(`??= ${la}, ||= ${lb}`);

// ============================================================================
// 2. DATA STRUCTURES
// ============================================================================
console.log("\n=== 2. DATA STRUCTURES ===\n");

// Array methods: map/filter/reduce are the functional programming triad in JS.
// They all return new arrays (immutable pattern) and never modify the original.
// Internally, they iterate using integer indices (not the iterator protocol).
// Time complexity: O(n) for each — chaining them creates multiple passes.
const nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
console.log("map (x2):", nums.map((n) => n * 2));
console.log("filter (even):", nums.filter((n) => n % 2 === 0));
// reduce accumulates a single value from left to right. The second argument (0)
// is the initial accumulator — without it, the first array element is used,
// which throws TypeError on empty arrays.
console.log("reduce (sum):", nums.reduce((a, n) => a + n, 0));
// flatMap = map + flat(1). Useful for one-to-many transformations where each element
// produces an array. More efficient than separate .map().flat() calls.
console.log("flatMap:", [[1, 2], [3, 4]].flatMap((x) => x.map((n) => n * 10)));
console.log("find (>5):", nums.find((n) => n > 5));
console.log("every (>0):", nums.every((n) => n > 0), "| some (>9):", nums.some((n) => n > 9));
// toSorted() and with() are ES2023 "change array by copy" methods. Unlike sort()
// and splice(), they return new arrays without mutating the original — enabling
// immutable data patterns needed for React state, Redux, etc.
console.log("toSorted:", [3, 1, 2].toSorted(), "| with(1,99):", [10, 20, 30].with(1, 99));

// Map maintains insertion order and allows ANY value as keys (objects, functions, etc.).
// Unlike plain objects, Map keys aren't coerced to strings — so 42 !== "42" as keys.
// Map uses the SameValueZero algorithm for key equality (similar to === but NaN === NaN).
// See MDN: Map. Preferred over objects when keys are dynamic or non-string.
const map = new Map([["key1", "value1"], [42, "numeric key"]]);
console.log("Map size:", map.size, "| get(42):", map.get(42));

// Set stores unique values using SameValueZero comparison. Adding a duplicate is a no-op.
// Set operations (union, intersection, difference) were standardized in ES2025 via
// Set.prototype.union(), .intersection(), .difference() — below uses manual polyfills.
const setA = new Set([1, 2, 3, 4]), setB = new Set([3, 4, 5, 6]);
console.log("Set:", [...new Set([1, 2, 3, 3, 2])]);
console.log("union:", [...new Set([...setA, ...setB])]);
console.log("intersection:", [...setA].filter((x) => setB.has(x)));
console.log("difference:", [...setA].filter((x) => !setB.has(x)));

// WeakMap holds weak references to object keys — entries are automatically removed
// when the key object is garbage collected. This prevents memory leaks when associating
// metadata with objects you don't own. Keys MUST be objects (not primitives).
// Common use: storing private data for class instances, caching DOM element metadata.
const weakMap = new WeakMap();
let objKey = { id: 1 };
weakMap.set(objKey, "weak value");
console.log("WeakMap get:", weakMap.get(objKey));

// WeakRef provides a weak reference to an object. Unlike WeakMap, you can read the
// referent via deref() — which returns undefined if the object was garbage collected.
// Use sparingly: GC timing is non-deterministic, so deref() may return undefined
// at any point. Pair with FinalizationRegistry for cleanup callbacks.
let target = { data: "important" };
const weakRef = new WeakRef(target);
console.log("WeakRef deref:", weakRef.deref()?.data);

// ============================================================================
// 3. FUNCTIONS
// ============================================================================
console.log("\n=== 3. FUNCTIONS ===\n");

// Closures: a function "closes over" variables from its enclosing lexical scope.
// The inner functions retain a reference to the outer `count` variable — not a copy.
// This is how JavaScript achieves data encapsulation without classes: the closed-over
// variable is truly private, inaccessible from outside. This works because JS uses
// lexical (static) scoping — scope is determined at write time, not call time.
function makeCounter(init = 0) {
  let count = init;
  return { inc: () => ++count, dec: () => --count, val: () => count };
}
const ctr = makeCounter(10);
ctr.inc(); ctr.inc(); ctr.dec();
console.log(`closure counter: ${ctr.val()}`);

// IIFE (Immediately Invoked Function Expression) creates a new scope and executes
// immediately. Before ES6 block scoping (let/const), IIFEs were the primary way
// to avoid polluting the global scope. Still useful for one-time initialization.
console.log(`IIFE: ${(() => "hidden".toUpperCase())()}`);

// Arrow functions capture `this` lexically from the enclosing scope (they have no
// own `this` binding). Regular functions get `this` determined by HOW they're called
// (call-site binding). This is why arrow functions can't be used as constructors
// or with .call()/.apply()/.bind() to change `this`. See MDN: Arrow_functions
const obj = { value: 42, getArrow: function () { return () => this.value; } };
console.log(`arrow this: ${obj.getArrow()()}`);

// compose applies functions right-to-left: compose(f, g)(x) = f(g(x)).
// pipe applies functions left-to-right: pipe(f, g)(x) = g(f(x)).
// Both use rest params to accept any number of functions, then reduce/reduceRight
// to chain them. This is the foundation of functional programming pipelines.
// TC39 has a Stage 2 pipeline operator proposal: `x |> f |> g` (similar to pipe).
const compose = (...fns) => (x) => fns.reduceRight((a, f) => f(a), x);
const pipe = (...fns) => (x) => fns.reduce((a, f) => f(a), x);
const double = (x) => x * 2, addOne = (x) => x + 1;
console.log(`compose(addOne,double)(5): ${compose(addOne, double)(5)}`);
console.log(`pipe(addOne,double)(5): ${pipe(addOne, double)(5)}`);

// Currying transforms a function of N arguments into N nested functions of 1 argument.
// `fn.length` returns the number of declared parameters (excluding rest/default params).
// When fewer args are provided than needed, a new function is returned that waits for more.
// This enables partial application: `curriedAdd(1, 2)` returns a function awaiting the 3rd arg.
function curry(fn) {
  return function curried(...args) {
    return args.length >= fn.length ? fn(...args) : (...more) => curried(...args, ...more);
  };
}
const curriedAdd = curry((a, b, c) => a + b + c);
console.log(`curry: ${curriedAdd(1)(2)(3)}, partial: ${curriedAdd(1, 2)(3)}`);

// Memoization caches function results keyed by arguments. Subsequent calls with
// the same arguments return the cached result in O(1) instead of recomputing.
// JSON.stringify(args) is used as the cache key — this works for primitives and simple
// objects, but fails for functions, circular references, or Map/Set arguments.
// `fn.apply(this, args)` preserves `this` context if the memoized function is a method.
function memoize(fn) {
  const cache = new Map();
  return function (...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const val = fn.apply(this, args);
    cache.set(key, val);
    return val;
  };
}
// Recursive calls must invoke the memoized wrapper (fib), not the inner function,
// otherwise the cache is bypassed on recursive sub-calls — reducing O(2^n) to O(n).
const fib = memoize(function(n) { return n <= 1 ? n : fib(n - 1) + fib(n - 2); });
console.log(`memoized fib(10): ${fib(10)}`);

// ============================================================================
// 4. OOP
// ============================================================================
console.log("\n=== 4. OOP ===\n");

// Classes are syntactic sugar over JavaScript's prototype-based inheritance.
// Under the hood, `class Animal` creates a constructor function + prototype object.
// `new Dog()` sets up a prototype chain: dog -> Dog.prototype -> Animal.prototype -> Object.prototype.
// This is how method lookup works: the engine walks the chain until it finds the property.
// See MDN: Inheritance_and_the_prototype_chain
class Animal {
  // Private fields (#) are truly private — enforced by the engine, not convention.
  // They're not accessible via bracket notation, Reflect, or Proxy. Introduced in ES2022.
  // Under the hood, they use a WeakMap-like mechanism keyed by the instance.
  #sound;
  // Static properties belong to the constructor function itself, not the prototype.
  // They're shared across all instances and accessed via the class name.
  static count = 0;
  constructor(name, sound) { this.name = name; this.#sound = sound; Animal.count++; }
  speak() { return `${this.name} says ${this.#sound}`; }
  static totalCreated() { return Animal.count; }
}

// `extends` sets up two prototype chain links: Dog.prototype -> Animal.prototype (for
// instance methods) and Dog -> Animal (for static methods). `super()` must be called
// before `this` in derived constructors — this is enforced by the engine.
class Dog extends Animal {
  #tricks = [];
  constructor(name) { super(name, "woof"); }
  // Returning `this` from methods enables fluent chaining (builder pattern).
  learn(trick) { this.#tricks.push(trick); return this; }
  showTricks() { return `${this.name} knows: ${this.#tricks.join(", ")}`; }
}

const dog = new Dog("Rex");
dog.learn("sit").learn("shake");
console.log(dog.speak());
console.log(dog.showTricks());
console.log(`Animals created: ${Animal.totalCreated()}`);

// Symbols are unique, immutable primitives used as property keys. They don't collide
// with string keys, making them ideal for "hidden" or framework-internal properties.
// Well-known symbols (Symbol.iterator, Symbol.toPrimitive, etc.) customize language behavior.
// Symbol properties are NOT enumerable by Object.keys() or for...in — only by
// Object.getOwnPropertySymbols() or Reflect.ownKeys().
const sym = Symbol("desc");
const symObj = { [sym]: "symbol value", regular: "normal" };
console.log(`Symbol prop: ${symObj[sym]}, keys:`, Object.keys(symObj));

// Proxy intercepts fundamental object operations (get, set, has, deleteProperty, etc.)
// via "traps" defined in a handler object. It wraps the target transparently.
// Reflect provides the default behavior for each trap — always use Reflect inside traps
// to ensure correct receiver handling and spec-compliant forwarding.
// Proxies power Vue 3's reactivity system and many validation/logging frameworks.
const handler = {
  get(t, p, r) { return p in t ? Reflect.get(t, p, r) : `'${p}' not found`; },
  set(t, p, v, r) {
    if (typeof v !== "number") throw new TypeError("Must be number");
    return Reflect.set(t, p, v, r);
  },
};
const proxied = new Proxy({ x: 1, y: 2 }, handler);
console.log(`proxy: x=${proxied.x}, z=${proxied.z}`);
proxied.x = 10;
console.log(`proxy set: x=${proxied.x}`);
// Reflect.ownKeys returns ALL own property keys: string keys + symbol keys,
// unlike Object.keys which only returns enumerable string keys.
console.log("Reflect.ownKeys:", Reflect.ownKeys(symObj));

// ============================================================================
// 5. ASYNC
// ============================================================================
console.log("\n=== 5. ASYNC ===\n");

// Promises represent a value that may not be available yet. They have 3 states:
// pending -> fulfilled (resolved) or rejected. Once settled, the state is immutable.
// Promise handlers (.then/.catch) are scheduled as microtasks — they run after the
// current synchronous code completes but BEFORE any macrotasks (setTimeout, I/O).
// This is why `await` in a loop doesn't yield to setTimeout callbacks between iterations.
// See MDN: Using_Promises, Event_loop (microtask queue vs. task queue)
function fetchPromise(id) {
  return new Promise((resolve, reject) => {
    id < 0 ? reject(new Error("Invalid ID")) : resolve({ id, data: `result_${id}` });
  });
}

// async/await is syntactic sugar over Promise chains. `async` makes a function return
// a Promise; `await` suspends execution until the Promise settles, then unwraps the value.
// Under the hood, the engine uses microtask scheduling — each `await` is a suspension
// point where other microtasks can run (but NOT macrotasks like setTimeout).
async function runAsyncDemo() {
  const res = await fetchPromise(1);
  console.log("await:", res);

  // Promise.all runs promises concurrently and resolves when ALL succeed.
  // If ANY promise rejects, the entire Promise.all rejects immediately (fail-fast).
  // The results array preserves the original order regardless of completion order.
  const results = await Promise.all([fetchPromise(1), fetchPromise(2), fetchPromise(3)]);
  console.log("Promise.all:", results.map((r) => r.id));

  // Promise.race resolves/rejects with whichever promise settles first.
  // The "losing" promises continue running (they aren't cancelled) — JS has no
  // built-in promise cancellation. Use AbortController for cancellable operations.
  const fastest = await Promise.race([
    new Promise((r) => setTimeout(() => r("slow"), 100)),
    new Promise((r) => setTimeout(() => r("fast"), 10)),
  ]);
  console.log(`Promise.race: ${fastest}`);

  // Promise.allSettled (ES2020) never rejects — it waits for ALL promises to settle
  // and returns an array of {status, value/reason} objects. Use when you need results
  // from all promises regardless of individual failures (e.g., batch API calls).
  const settled = await Promise.allSettled([fetchPromise(1), fetchPromise(-1), fetchPromise(3)]);
  console.log("Promise.allSettled:", settled.map((s) => s.status));

  // Promise.any (ES2021) resolves with the FIRST fulfilled promise. It only rejects
  // if ALL promises reject (with AggregateError). Inverse of Promise.all's fail-fast.
  const any = await Promise.any([
    fetchPromise(-1).catch(() => Promise.reject("err")),
    fetchPromise(5),
  ]);
  console.log("Promise.any:", any);

  // AbortController is the standard cancellation mechanism for async operations in JS.
  // The controller produces an AbortSignal that can be passed to fetch(), addEventListener(),
  // or any custom async operation. Calling abort() fires the "abort" event on the signal.
  // This is the ONLY recommended way to cancel fetch requests. See MDN: AbortController
  const controller = new AbortController();
  const abortable = new Promise((resolve, reject) => {
    const timer = setTimeout(() => resolve("done"), 1000);
    controller.signal.addEventListener("abort", () => { clearTimeout(timer); reject(new Error("Aborted")); });
  });
  controller.abort();
  try { await abortable; } catch (e) { console.log(`AbortController: ${e.message}`); }
}

// ============================================================================
// 6. ITERATORS & GENERATORS
// ============================================================================
console.log("\n=== 6. ITERATORS & GENERATORS ===\n");

// The iterable protocol: any object with a [Symbol.iterator]() method that returns
// an iterator (an object with a next() method returning {value, done}) can be used
// with for...of, spread syntax, destructuring, Array.from(), Promise.all(), etc.
// This protocol decouples data producers from consumers — the foundation of lazy evaluation.
class Range {
  constructor(start, end) { this.start = start; this.end = end; }
  [Symbol.iterator]() {
    let cur = this.start; const end = this.end;
    return { next() { return cur <= end ? { value: cur++, done: false } : { done: true }; } };
  }
}
console.log("custom iterable:", [...new Range(1, 5)]);

// Generators (function*) produce iterators that can pause execution via `yield`.
// Each call to next() resumes from the last yield point. This enables lazy sequences
// that compute values on demand — the fibonacci generator below uses O(1) memory
// regardless of how many values you consume. Generators are the basis for async/await
// (which was originally implemented as generators + promises in Babel/regenerator).
function* fibonacci() { let [a, b] = [0, 1]; while (true) { yield a; [a, b] = [b, a + b]; } }
function take(gen, n) { const r = []; for (const v of gen) { r.push(v); if (r.length >= n) break; } return r; }
console.log("fibonacci(10):", take(fibonacci(), 10));

// Generators are bidirectional: next(value) sends a value INTO the generator.
// The sent value becomes the result of the `yield` expression inside the generator.
// This enables coroutine-style communication — the generator produces values AND
// receives input, making it a cooperative multitasking primitive.
function* stateful() {
  const x = yield "first";
  const y = yield `received: ${x}`;
  return `done: ${y}`;
}
const gen = stateful();
console.log("gen:", gen.next().value, "|", gen.next(42).value, "|", gen.next(99).value);

// yield* delegates to another iterable/generator, flattening its values into the
// outer generator's output. This enables composing generators like building blocks.
function* inner() { yield "a"; yield "b"; }
function* outer() { yield 1; yield* inner(); yield 2; }
console.log("delegation:", [...outer()]);

// Async generators combine generators with promises: `async function*` can both
// `yield` values and `await` async operations. Consumed with `for await...of`.
// This is the pattern for streaming data: reading files line-by-line, SSE events,
// WebSocket messages, paginated API responses, etc.
async function asyncGenDemo() {
  async function* asyncRange(s, e) {
    for (let i = s; i <= e; i++) { await new Promise((r) => setTimeout(r, 1)); yield i; }
  }
  const collected = [];
  for await (const val of asyncRange(1, 5)) collected.push(val);
  console.log("async generator:", collected);
}

// ============================================================================
// 7. MODULES (comment-based patterns)
// ============================================================================
console.log("\n=== 7. MODULES ===\n");
// ESM (ECMAScript Modules) are statically analyzed — imports/exports must be top-level,
// enabling tree-shaking (dead code elimination) by bundlers. This is impossible with
// CommonJS `require()` because require is a runtime function call.
// export const API_URL = "...";          // named export — can have many per module
// export default class Router { ... }    // default export — one per module, any name on import
// export { default as Router } from "./router.js";  // re-export — barrel file pattern
// const mod = await import("./heavy.js");            // dynamic import — code splitting, returns Promise
// import data from "./config.json" with { type: "json" };  // import attributes (ES2025) — type assertions for non-JS
console.log("(module patterns documented in source comments)");

// ============================================================================
// 8. ERROR HANDLING
// ============================================================================
console.log("\n=== 8. ERROR HANDLING ===\n");

// Custom errors should extend Error to get proper stack traces and instanceof checks.
// Setting `this.name` is important — it appears in stack traces and error messages.
// Custom properties (like `field`) enable structured error handling beyond just messages.
class ValidationError extends Error {
  constructor(field, msg) { super(msg); this.name = "ValidationError"; this.field = field; }
}

// try/catch/finally: `catch` handles synchronous errors and rejected promises (with await).
// `finally` ALWAYS runs — even if catch re-throws. It's used for cleanup (closing files,
// releasing locks). Note: `finally` does NOT receive the error — use catch for that.
try { throw new ValidationError("email", "Invalid format"); }
catch (e) { console.log(`${e.name} on '${e.field}': ${e.message}`); }
finally { console.log("finally always runs"); }

// AggregateError (ES2021) groups multiple errors into one. It's thrown by Promise.any()
// when all promises reject. The `.errors` property contains the individual Error objects.
const aggErr = new AggregateError([new Error("DB fail"), new Error("Cache miss")], "Multiple failures");
console.log(`AggregateError: ${aggErr.message} [${aggErr.errors.map((e) => e.message)}]`);

// Error cause (ES2022) enables error chaining via the `cause` option. This preserves
// the original error context when wrapping errors at higher abstraction levels.
// Access via `error.cause`. Can be chained: error.cause.cause, etc.
try { try { throw new Error("root"); } catch (e) { throw new Error("wrapped", { cause: e }); } }
catch (e) { console.log(`cause chain: ${e.message} <- ${e.cause.message}`); }

// ============================================================================
// 9. METAPROGRAMMING
// ============================================================================
console.log("\n=== 9. METAPROGRAMMING ===\n");

// Proxy-based validation: the `set` trap intercepts property assignment, enabling
// runtime type checking that plain JavaScript lacks. Each property can have its own
// validation function. This pattern powers ORMs, form validation libraries, and
// reactive state systems. See MDN: Proxy — handler.set()
function createValidated(schema) {
  return new Proxy({}, {
    set(t, p, v) {
      if (schema[p] && !schema[p](v)) throw new TypeError(`Invalid '${p}': ${v}`);
      t[p] = v; return true;
    },
  });
}
const person = createValidated({
  age: (v) => typeof v === "number" && v >= 0 && v <= 150,
  name: (v) => typeof v === "string" && v.length > 0,
});
person.name = "Alice"; person.age = 30;
console.log(`validated: ${person.name}, ${person.age}`);
try { person.age = -5; } catch (e) { console.log(`rejected: ${e.message}`); }

// Observable proxy: the `set` trap logs property changes before they happen.
// This is the core mechanism behind Vue 3's reactivity: wrap data in a Proxy,
// intercept get (track dependencies) and set (trigger re-renders).
const observed = new Proxy({ x: 1 }, {
  set(o, p, v) { console.log(`  ${p}: ${o[p]} -> ${v}`); o[p] = v; return true; },
});
console.log("observable:"); observed.x = 2; observed.y = 3;

// Reflect.apply calls a function with a specific `this` context and arguments array.
// Unlike Function.prototype.apply, Reflect.apply is a standalone function — useful
// when the target might have overridden `.apply` on its prototype.
function greet(g) { return `${g}, ${this.name}!`; }
console.log("Reflect.apply:", Reflect.apply(greet, { name: "World" }, ["Hello"]));

// FinalizationRegistry (ES2021) registers a callback that runs when an object is
// garbage collected. This is for cleanup of external resources (closing file handles,
// releasing native memory) — NOT for critical logic, as GC timing is non-deterministic.
// The held value (2nd arg to register) is passed to the callback — use it instead of
// closing over the target (which would prevent GC).
const registry = new FinalizationRegistry((v) => console.log(`GC'd: ${v}`));
let ephemeral = { temp: true };
registry.register(ephemeral, "ephemeral");
console.log("WeakRef alive:", new WeakRef(ephemeral).deref() !== undefined);
console.log("(FinalizationRegistry runs on GC — non-deterministic)");

// ============================================================================
// 10. ADVANCED
// ============================================================================
console.log("\n=== 10. ADVANCED ===\n");

// structuredClone (2022) performs a deep clone using the structured clone algorithm
// (same algorithm used by postMessage, IndexedDB, etc.). Unlike JSON.parse(JSON.stringify()),
// it handles Date, RegExp, Map, Set, ArrayBuffer, Error, and circular references.
// It CANNOT clone functions, DOM nodes, or Proxy objects — those throw DataCloneError.
const original = { date: new Date(), nested: { arr: [1, 2, 3] }, regex: /test/gi };
const cloned = structuredClone(original);
cloned.nested.arr.push(4);
console.log("original:", original.nested.arr, "| cloned:", cloned.nested.arr);

// Object.groupBy (ES2024) groups array elements by a callback's return value.
// Returns a null-prototype object (no inherited properties). This replaces the
// common lodash _.groupBy pattern. Also available as Map.groupBy for Map results.
const items = [{ n: "apple", t: "fruit" }, { n: "carrot", t: "veg" }, { n: "banana", t: "fruit" }];
const grouped = Object.groupBy(items, (i) => i.t);
console.log("groupBy:", { fruit: grouped.fruit?.map((i) => i.n), veg: grouped.veg?.map((i) => i.n) });

// SharedArrayBuffer enables true shared memory between Web Workers (or worker_threads
// in Node.js). Atomics provides thread-safe operations (store, load, add, wait, notify)
// to prevent data races. Requires cross-origin isolation headers in browsers (COOP/COEP).
// const sab = new SharedArrayBuffer(1024);
// Atomics.store(new Int32Array(sab), 0, 42); Atomics.load/add/wait/notify
console.log("(SharedArrayBuffer/Atomics: requires cross-origin isolation)");

// Temporal API (TC39 Stage 3) replaces the notoriously broken Date object.
// Key improvements: immutable values, proper timezone handling, calendar support,
// nanosecond precision, and clear distinction between absolute/wall-clock time.
// Temporal.Now.plainDateTimeISO(), Temporal.PlainDate.from("2024-03-15")
// Immutable, timezone-aware, replaces Date
console.log("(Temporal: Stage 3 — immutable date/time API)");

// Promise.withResolvers (ES2024) extracts resolve/reject from a Promise constructor,
// avoiding the "deferred pattern" boilerplate of declaring outer variables. Useful when
// resolve/reject need to be called from outside the Promise constructor callback.
const { promise, resolve } = Promise.withResolvers();
resolve("resolved externally");
promise.then((v) => console.log(`Promise.withResolvers: ${v}`));

// ============================================================================
// BONUS: Patterns & Idioms
// ============================================================================
console.log("\n=== BONUS: PATTERNS & IDIOMS ===\n");

// Tagged template literals: the tag function receives the string parts as a
// TemplateStringsArray and the interpolated values as separate arguments.
// The raw strings are split at interpolation points, so strings.length === values.length + 1.
// This pattern enables DSLs: SQL query builders (escaping injection), CSS-in-JS (styled-components),
// GraphQL queries (gql`...`), and internationalization (i18n).
function sql(strings, ...values) {
  const escaped = values.map((v) => typeof v === "string" ? `'${v.replace(/'/g, "''")}'` : v);
  return strings.reduce((acc, str, i) => acc + str + (escaped[i] ?? ""), "");
}
const table = "users";
const id = 42;
console.log("tagged template:", sql`SELECT * FROM ${table} WHERE id = ${id}`);

// Getters and setters create computed properties that look like regular property access.
// Under the hood, they're accessor descriptors on the prototype (Object.defineProperty).
// The engine calls the get/set function on each access — no caching unless you implement it.
// This is how frameworks implement reactive properties (e.g., Ember, MobX).
class Temperature {
  #celsius;
  constructor(c) { this.#celsius = c; }
  get fahrenheit() { return this.#celsius * 9 / 5 + 32; }
  set fahrenheit(f) { this.#celsius = (f - 32) * 5 / 9; }
  toString() { return `${this.#celsius.toFixed(1)}C / ${this.fahrenheit.toFixed(1)}F`; }
}
const temp = new Temperature(100);
console.log(`Temperature: ${temp}`);
temp.fahrenheit = 72;
console.log(`After set F=72: ${temp}`);

// Pattern matching via destructuring: simulate match/case by destructuring the
// input object to extract fields, then branching on values. This is a pragmatic
// alternative to the TC39 Stage 1 Pattern Matching proposal (`match (x) { ... }`).
function handleResponse({ status, data, error }) {
  if (status >= 200 && status < 300) return `OK: ${JSON.stringify(data)}`;
  if (status >= 400) return `Error ${status}: ${error}`;
  return `Redirect: ${status}`;
}
console.log(handleResponse({ status: 200, data: { ok: true }, error: null }));
console.log(handleResponse({ status: 404, data: null, error: "Not found" }));

// Async iteration queue: implements the async iterable protocol ([Symbol.asyncIterator])
// for push-based data sources. The producer calls push(), the consumer uses for-await-of.
// When no data is available, next() returns a pending Promise that resolves when data arrives.
// This bridges push-based APIs (events, WebSocket messages) with pull-based consumption.
function createAsyncQueue() {
  const queue = [];
  let resolve = null;
  return {
    push(val) {
      if (resolve) { resolve({ value: val, done: false }); resolve = null; }
      else queue.push(val);
    },
    [Symbol.asyncIterator]() {
      return {
        next() {
          if (queue.length > 0) return Promise.resolve({ value: queue.shift(), done: false });
          return new Promise((r) => { resolve = r; });
        },
      };
    },
  };
}
console.log("(async queue pattern: push/pull async iteration)");

// Using Symbols as private protocol identifiers: unlike string method names, Symbols
// can't collide with other properties. This is how you define "private interfaces" that
// only code with access to the Symbol can invoke. The well-known Symbol pattern
// (Symbol.iterator, Symbol.toPrimitive) uses this same technique at the language level.
const serialize = Symbol("serialize");
class Config {
  constructor(data) { this.data = data; }
  [serialize]() { return JSON.stringify(this.data); }
}
const cfg = new Config({ env: "prod", port: 443 });
console.log(`symbol protocol: ${cfg[serialize]()}`);

// Optional chaining with bracket notation (?.[]) and nested array access.
// The entire chain short-circuits to undefined on the first null/undefined,
// then ?? provides the fallback. This replaces deeply nested if-checks or try/catch.
const deepObj = { a: { b: { c: [{ d: "found" }] } } };
const deep = deepObj?.a?.b?.c?.[0]?.d ?? "missing";
const missing = deepObj?.x?.y?.z?.[0]?.w ?? "missing";
console.log(`deep access: ${deep}, missing: ${missing}`);

// ============================================================================
// RUN ASYNC DEMOS
// ============================================================================
// The top-level async IIFE is needed because top-level await only works in ESM modules.
// In CommonJS (.js files run by node without --input-type=module), you must wrap
// await in an async function. Node 14.8+ supports top-level await in .mjs files.
(async () => {
  await runAsyncDemo();
  await asyncGenDemo();
  console.log("\n=== ALL DEMOS COMPLETE ===");
})();
