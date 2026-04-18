// js_fundamentals.js — JavaScript Fundamentals (Node.js)
// Run: node js_fundamentals.js
"use strict";

// ============================================================================
// 1. BASICS
// ============================================================================
console.log("=== 1. BASICS ===\n");

let counter = 0;
const MAX = 100;
console.log(`let/const: counter=${++counter}, MAX=${MAX}`);

const name = "JavaScript";
console.log(`template literal: ${name} ${2024}`);

// Destructuring
const [first, second, ...remaining] = [10, 20, 30, 40, 50];
console.log(`array destructure: ${first}, ${second}, rest:`, remaining);

const { host, port, debug: isDebug } = { host: "localhost", port: 3000, debug: true };
console.log(`object destructure: ${host}:${port}, debug=${isDebug}`);

const { a: { b: nested = 42 } = {} } = { a: { b: 7 } };
console.log(`nested destructure with default: ${nested}`);

// Spread / rest
const arr1 = [1, 2, 3];
console.log("spread array:", [...arr1, 4, 5]);
console.log("spread object:", { ...{ x: 1 }, y: 2 });
const sum = (...nums) => nums.reduce((a, n) => a + n, 0);
console.log(`rest params: sum(1,2,3,4) = ${sum(1, 2, 3, 4)}`);

// Optional chaining + nullish coalescing
const user = { profile: { address: { city: "Portland" } } };
console.log(`optional chain: ${user.profile?.address?.city}`);
console.log(`nullish coal: ${user.profile?.address?.zip ?? "N/A"}`);
console.log(`method chain: ${user.profile?.getName?.() ?? "no method"}`);

const val1 = null ?? "default", val2 = 0 ?? "default", val3 = "" ?? "default";
console.log(`?? : ${val1}, ${val2}, ${val3}`);

// Logical assignment
let la = null; la ??= "assigned";
let lb = 0; lb ||= 99;
console.log(`??= ${la}, ||= ${lb}`);

// ============================================================================
// 2. DATA STRUCTURES
// ============================================================================
console.log("\n=== 2. DATA STRUCTURES ===\n");

const nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
console.log("map (x2):", nums.map((n) => n * 2));
console.log("filter (even):", nums.filter((n) => n % 2 === 0));
console.log("reduce (sum):", nums.reduce((a, n) => a + n, 0));
console.log("flatMap:", [[1, 2], [3, 4]].flatMap((x) => x.map((n) => n * 10)));
console.log("find (>5):", nums.find((n) => n > 5));
console.log("every (>0):", nums.every((n) => n > 0), "| some (>9):", nums.some((n) => n > 9));
console.log("toSorted:", [3, 1, 2].toSorted(), "| with(1,99):", [10, 20, 30].with(1, 99));

// Map
const map = new Map([["key1", "value1"], [42, "numeric key"]]);
console.log("Map size:", map.size, "| get(42):", map.get(42));

// Set + operations
const setA = new Set([1, 2, 3, 4]), setB = new Set([3, 4, 5, 6]);
console.log("Set:", [...new Set([1, 2, 3, 3, 2])]);
console.log("union:", [...new Set([...setA, ...setB])]);
console.log("intersection:", [...setA].filter((x) => setB.has(x)));
console.log("difference:", [...setA].filter((x) => !setB.has(x)));

// WeakMap + WeakRef
const weakMap = new WeakMap();
let objKey = { id: 1 };
weakMap.set(objKey, "weak value");
console.log("WeakMap get:", weakMap.get(objKey));

let target = { data: "important" };
const weakRef = new WeakRef(target);
console.log("WeakRef deref:", weakRef.deref()?.data);

// ============================================================================
// 3. FUNCTIONS
// ============================================================================
console.log("\n=== 3. FUNCTIONS ===\n");

// Closures
function makeCounter(init = 0) {
  let count = init;
  return { inc: () => ++count, dec: () => --count, val: () => count };
}
const ctr = makeCounter(10);
ctr.inc(); ctr.inc(); ctr.dec();
console.log(`closure counter: ${ctr.val()}`);

// IIFE
console.log(`IIFE: ${(() => "hidden".toUpperCase())()}`);

// Arrow — lexical this
const obj = { value: 42, getArrow: function () { return () => this.value; } };
console.log(`arrow this: ${obj.getArrow()()}`);

// Higher-order: compose & pipe
const compose = (...fns) => (x) => fns.reduceRight((a, f) => f(a), x);
const pipe = (...fns) => (x) => fns.reduce((a, f) => f(a), x);
const double = (x) => x * 2, addOne = (x) => x + 1;
console.log(`compose(addOne,double)(5): ${compose(addOne, double)(5)}`);
console.log(`pipe(addOne,double)(5): ${pipe(addOne, double)(5)}`);

// Currying
function curry(fn) {
  return function curried(...args) {
    return args.length >= fn.length ? fn(...args) : (...more) => curried(...args, ...more);
  };
}
const curriedAdd = curry((a, b, c) => a + b + c);
console.log(`curry: ${curriedAdd(1)(2)(3)}, partial: ${curriedAdd(1, 2)(3)}`);

// Memoization
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
const fib = memoize(function f(n) { return n <= 1 ? n : f(n - 1) + f(n - 2); });
console.log(`memoized fib(10): ${fib(10)}`);

// ============================================================================
// 4. OOP
// ============================================================================
console.log("\n=== 4. OOP ===\n");

class Animal {
  #sound;
  static count = 0;
  constructor(name, sound) { this.name = name; this.#sound = sound; Animal.count++; }
  speak() { return `${this.name} says ${this.#sound}`; }
  static totalCreated() { return Animal.count; }
}

class Dog extends Animal {
  #tricks = [];
  constructor(name) { super(name, "woof"); }
  learn(trick) { this.#tricks.push(trick); return this; }
  showTricks() { return `${this.name} knows: ${this.#tricks.join(", ")}`; }
}

const dog = new Dog("Rex");
dog.learn("sit").learn("shake");
console.log(dog.speak());
console.log(dog.showTricks());
console.log(`Animals created: ${Animal.totalCreated()}`);

// Symbol
const sym = Symbol("desc");
const symObj = { [sym]: "symbol value", regular: "normal" };
console.log(`Symbol prop: ${symObj[sym]}, keys:`, Object.keys(symObj));

// Proxy + Reflect
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
console.log("Reflect.ownKeys:", Reflect.ownKeys(symObj));

// ============================================================================
// 5. ASYNC
// ============================================================================
console.log("\n=== 5. ASYNC ===\n");

function fetchPromise(id) {
  return new Promise((resolve, reject) => {
    id < 0 ? reject(new Error("Invalid ID")) : resolve({ id, data: `result_${id}` });
  });
}

async function runAsyncDemo() {
  const res = await fetchPromise(1);
  console.log("await:", res);

  const results = await Promise.all([fetchPromise(1), fetchPromise(2), fetchPromise(3)]);
  console.log("Promise.all:", results.map((r) => r.id));

  const fastest = await Promise.race([
    new Promise((r) => setTimeout(() => r("slow"), 100)),
    new Promise((r) => setTimeout(() => r("fast"), 10)),
  ]);
  console.log(`Promise.race: ${fastest}`);

  const settled = await Promise.allSettled([fetchPromise(1), fetchPromise(-1), fetchPromise(3)]);
  console.log("Promise.allSettled:", settled.map((s) => s.status));

  const any = await Promise.any([
    fetchPromise(-1).catch(() => Promise.reject("err")),
    fetchPromise(5),
  ]);
  console.log("Promise.any:", any);

  // AbortController
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

class Range {
  constructor(start, end) { this.start = start; this.end = end; }
  [Symbol.iterator]() {
    let cur = this.start; const end = this.end;
    return { next() { return cur <= end ? { value: cur++, done: false } : { done: true }; } };
  }
}
console.log("custom iterable:", [...new Range(1, 5)]);

function* fibonacci() { let [a, b] = [0, 1]; while (true) { yield a; [a, b] = [b, a + b]; } }
function take(gen, n) { const r = []; for (const v of gen) { r.push(v); if (r.length >= n) break; } return r; }
console.log("fibonacci(10):", take(fibonacci(), 10));

// Generator with send
function* stateful() {
  const x = yield "first";
  const y = yield `received: ${x}`;
  return `done: ${y}`;
}
const gen = stateful();
console.log("gen:", gen.next().value, "|", gen.next(42).value, "|", gen.next(99).value);

// Delegation
function* inner() { yield "a"; yield "b"; }
function* outer() { yield 1; yield* inner(); yield 2; }
console.log("delegation:", [...outer()]);

// Async generator
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
// export const API_URL = "...";          // named export
// export default class Router { ... }    // default export
// export { default as Router } from "./router.js";  // re-export
// const mod = await import("./heavy.js");            // dynamic import
// import data from "./config.json" with { type: "json" };  // import attributes
console.log("(module patterns documented in source comments)");

// ============================================================================
// 8. ERROR HANDLING
// ============================================================================
console.log("\n=== 8. ERROR HANDLING ===\n");

class ValidationError extends Error {
  constructor(field, msg) { super(msg); this.name = "ValidationError"; this.field = field; }
}

try { throw new ValidationError("email", "Invalid format"); }
catch (e) { console.log(`${e.name} on '${e.field}': ${e.message}`); }
finally { console.log("finally always runs"); }

// AggregateError
const aggErr = new AggregateError([new Error("DB fail"), new Error("Cache miss")], "Multiple failures");
console.log(`AggregateError: ${aggErr.message} [${aggErr.errors.map((e) => e.message)}]`);

// Error cause
try { try { throw new Error("root"); } catch (e) { throw new Error("wrapped", { cause: e }); } }
catch (e) { console.log(`cause chain: ${e.message} <- ${e.cause.message}`); }

// ============================================================================
// 9. METAPROGRAMMING
// ============================================================================
console.log("\n=== 9. METAPROGRAMMING ===\n");

// Validation proxy
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

// Observable proxy
const observed = new Proxy({ x: 1 }, {
  set(o, p, v) { console.log(`  ${p}: ${o[p]} -> ${v}`); o[p] = v; return true; },
});
console.log("observable:"); observed.x = 2; observed.y = 3;

// Reflect.apply
function greet(g) { return `${g}, ${this.name}!`; }
console.log("Reflect.apply:", Reflect.apply(greet, { name: "World" }, ["Hello"]));

// WeakRef + FinalizationRegistry
const registry = new FinalizationRegistry((v) => console.log(`GC'd: ${v}`));
let ephemeral = { temp: true };
registry.register(ephemeral, "ephemeral");
console.log("WeakRef alive:", new WeakRef(ephemeral).deref() !== undefined);
console.log("(FinalizationRegistry runs on GC — non-deterministic)");

// ============================================================================
// 10. ADVANCED
// ============================================================================
console.log("\n=== 10. ADVANCED ===\n");

// structuredClone
const original = { date: new Date(), nested: { arr: [1, 2, 3] }, regex: /test/gi };
const cloned = structuredClone(original);
cloned.nested.arr.push(4);
console.log("original:", original.nested.arr, "| cloned:", cloned.nested.arr);

// Object.groupBy
const items = [{ n: "apple", t: "fruit" }, { n: "carrot", t: "veg" }, { n: "banana", t: "fruit" }];
const grouped = Object.groupBy(items, (i) => i.t);
console.log("groupBy:", { fruit: grouped.fruit?.map((i) => i.n), veg: grouped.veg?.map((i) => i.n) });

// SharedArrayBuffer (concepts)
// const sab = new SharedArrayBuffer(1024);
// Atomics.store(new Int32Array(sab), 0, 42); Atomics.load/add/wait/notify
console.log("(SharedArrayBuffer/Atomics: requires cross-origin isolation)");

// Temporal API (Stage 3)
// Temporal.Now.plainDateTimeISO(), Temporal.PlainDate.from("2024-03-15")
// Immutable, timezone-aware, replaces Date
console.log("(Temporal: Stage 3 — immutable date/time API)");

// Promise.withResolvers
const { promise, resolve } = Promise.withResolvers();
resolve("resolved externally");
promise.then((v) => console.log(`Promise.withResolvers: ${v}`));

// ============================================================================
// BONUS: Patterns & Idioms
// ============================================================================
console.log("\n=== BONUS: PATTERNS & IDIOMS ===\n");

// Tagged template literals
function sql(strings, ...values) {
  const escaped = values.map((v) => typeof v === "string" ? `'${v.replace(/'/g, "''")}'` : v);
  return strings.reduce((acc, str, i) => acc + str + (escaped[i] ?? ""), "");
}
const table = "users";
const id = 42;
console.log("tagged template:", sql`SELECT * FROM ${table} WHERE id = ${id}`);

// Private class methods + accessor keyword
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

// Pattern matching with object destructuring
function handleResponse({ status, data, error }) {
  if (status >= 200 && status < 300) return `OK: ${JSON.stringify(data)}`;
  if (status >= 400) return `Error ${status}: ${error}`;
  return `Redirect: ${status}`;
}
console.log(handleResponse({ status: 200, data: { ok: true }, error: null }));
console.log(handleResponse({ status: 404, data: null, error: "Not found" }));

// Async iteration over events pattern
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

// Using symbols for private protocols
const serialize = Symbol("serialize");
class Config {
  constructor(data) { this.data = data; }
  [serialize]() { return JSON.stringify(this.data); }
}
const cfg = new Config({ env: "prod", port: 443 });
console.log(`symbol protocol: ${cfg[serialize]()}`);

// Nullish-aware property access chains
const deepObj = { a: { b: { c: [{ d: "found" }] } } };
const deep = deepObj?.a?.b?.c?.[0]?.d ?? "missing";
const missing = deepObj?.x?.y?.z?.[0]?.w ?? "missing";
console.log(`deep access: ${deep}, missing: ${missing}`);

// ============================================================================
// RUN ASYNC DEMOS
// ============================================================================
(async () => {
  await runAsyncDemo();
  await asyncGenDemo();
  console.log("\n=== ALL DEMOS COMPLETE ===");
})();
