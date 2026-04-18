// ts_fundamentals.ts — TypeScript Fundamentals
// Run: npx tsx ts_fundamentals.ts

// TypeScript is a structural type system — compatibility is determined by the shape
// of types (their properties and methods), NOT by explicit declarations or class names.
// This is fundamentally different from Java/C# nominal typing where a class must
// explicitly implement an interface. See TS Handbook: Type Compatibility

// ============================================================================
// 1. BASICS — Type Annotations, Interfaces, Aliases, Literals, Enums
// ============================================================================
console.log("=== 1. BASICS ===\n");  // => === 1. BASICS ===

// Type annotations are erased at compile time (type erasure). The emitted JavaScript
// has no runtime type information — annotations exist only for static analysis.
// This means you can't do `typeof x === "User"` at runtime. See TS docs: Type Erasure
const greeting: string = "Hello, TypeScript";
const year: number = 2024;
const active: boolean = true;
console.log(`${greeting} | year: ${year} | active: ${active}`);  // => Hello, TypeScript | year: 2024 | active: true

// Interfaces define object shapes. They support declaration merging (multiple
// declarations with the same name are automatically combined), which is why
// they're preferred for public API contracts and library type definitions.
// `readonly` prevents reassignment after initialization — enforced only at compile time.
// `?` marks optional properties (equivalent to `prop: T | undefined`).
interface User {
  readonly id: number;
  name: string;
  email: string;
  age?: number;
}
const user: User = { id: 1, name: "Alice", email: "alice@example.com" };
console.log("user:", user);  // => user: { id: 1, name: 'Alice', email: 'alice@example.com' }

// Type aliases create named types using `type`. Unlike interfaces, they can represent
// unions, intersections, primitives, tuples, and mapped types. They CANNOT be
// declaration-merged. Use type aliases for unions/computed types; interfaces for object shapes.
type Point = { x: number; y: number };
// Union types (|) allow a value to be one of several types. The compiler narrows
// the type in conditional branches (control flow analysis).
type ID = string | number;
console.log(`point: (${0}, ${0}), userId: ${"abc-123" as ID}`);  // => point: (0, 0), userId: abc-123

// Literal types restrict a value to specific exact values — not just `string` but
// specific strings. Combined with unions, they create discriminated/tagged unions
// which enable exhaustive pattern matching in switch statements.
type Direction = "north" | "south" | "east" | "west";
type HttpStatus = 200 | 301 | 404 | 500;
// `satisfies` (TS 5.0) validates that a value matches a type WITHOUT widening it.
// Unlike `as`, satisfies preserves the narrower literal type for downstream usage.
console.log(`literal: dir=${"north" satisfies Direction}, status=${200 satisfies HttpStatus}`);  // => literal: dir=north, status=200

// Numeric enums auto-increment from 0. They create a reverse mapping at runtime
// (LogLevel[2] === "WARN") via a double-assignment IIFE in the emitted JS.
// String enums DON'T create reverse mappings. `const enum` is fully inlined at
// compile time — no runtime object exists, reducing bundle size.
enum LogLevel { DEBUG, INFO, WARN, ERROR }
enum Color { Red = "#FF0000", Green = "#00FF00", Blue = "#0000FF" }
console.log(`enum: WARN=${LogLevel.WARN}, Red=${Color.Red}, reverse=${LogLevel[2]}`);  // => enum: WARN=2, Red=#FF0000, reverse=WARN

// const enums are completely erased — each usage is replaced with the literal value.
// This means no runtime overhead, but you lose the ability to iterate over enum values.
// Caveat: const enums break when consumed across package boundaries (--isolatedModules).
const enum HttpMethod { GET = "GET", POST = "POST", PUT = "PUT", DELETE = "DELETE" }
console.log(`const enum: ${HttpMethod.POST}`);  // => const enum: POST

// ============================================================================
// 2. ADVANCED TYPES
// ============================================================================
console.log("\n=== 2. ADVANCED TYPES ===\n");  // => === 2. ADVANCED TYPES ===

// Union types + typeof narrowing: TypeScript's control flow analysis tracks the type
// through conditional branches. After `typeof val === "string"`, the compiler knows
// `val` is `string` in that branch — this is called "type narrowing".
// See TS Handbook: Narrowing
function formatValue(val: string | number | boolean): string {
  if (typeof val === "string") return val.toUpperCase();
  if (typeof val === "number") return val.toFixed(2);
  return val ? "YES" : "NO";
}
console.log(`union: ${formatValue("hello")}, ${formatValue(3.14)}, ${formatValue(true)}`);  // => union: HELLO, 3.14, YES

// Intersection types (&) combine multiple types into one that has ALL properties.
// This is different from union (|) which is "one of". Intersections are used for
// mixins and composing types. If properties conflict, the result is `never`.
type HasName = { name: string };
type HasAge = { age: number };
type Person = HasName & HasAge;
const person: Person = { name: "Bob", age: 30 };
console.log("intersection:", person);  // => intersection: { name: 'Bob', age: 30 }

// Discriminated unions use a shared literal property (the "discriminant") to enable
// exhaustive type narrowing in switch/if. The compiler tracks which variant you're in
// and narrows the type accordingly — `s.radius` is only accessible in the "circle" case.
// This pattern replaces class hierarchies and visitor patterns in many use cases.
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rect"; width: number; height: number }
  | { kind: "tri"; base: number; height: number };

function area(s: Shape): number {
  switch (s.kind) {
    case "circle": return Math.PI * s.radius ** 2;
    case "rect": return s.width * s.height;
    case "tri": return (s.base * s.height) / 2;
  }
}
console.log(`area: circle=${area({ kind: "circle", radius: 5 }).toFixed(2)}, rect=${area({ kind: "rect", width: 4, height: 6 })}`);  // => area: circle=78.54, rect=24

// Mapped types iterate over the keys of a type and transform each property.
// `keyof T` produces a union of T's property names. `[K in keyof T]` iterates them.
// Adding `readonly` or `?` modifiers creates new types from existing ones.
// The built-in Readonly<T>, Partial<T>, Required<T> are all mapped types.
type Readonly2<T> = { readonly [K in keyof T]: T[K] };
type Optional<T> = { [K in keyof T]?: T[K] };
type Nullable<T> = { [K in keyof T]: T[K] | null };
const frozen: Readonly2<Point> = { x: 1, y: 2 };
console.log("mapped readonly:", frozen);  // => mapped readonly: { x: 1, y: 2 }

// Conditional types enable type-level if/else: `T extends U ? X : Y`.
// When T is a union, conditional types distribute over each member automatically
// (distributive conditional types). This is why `IsString<string | number>` produces
// `"yes" | "no"`, not a single result.
// `infer` captures a type variable within a conditional for extraction.
type IsString<T> = T extends string ? "yes" : "no";
type A = IsString<string>; // "yes"
type B = IsString<number>; // "no"
// `infer U` extracts the element type from an array — like pattern matching at the type level.
type UnpackArray<T> = T extends Array<infer U> ? U : T;
type Unpacked = UnpackArray<string[]>; // string
console.log("(conditional types: compile-time type branching)");  // => (conditional types: compile-time type branching)

// ============================================================================
// 3. GENERICS
// ============================================================================
console.log("\n=== 3. GENERICS ===\n");  // => === 3. GENERICS ===

// Generics parameterize types, enabling code that works with any type while preserving
// type safety. TypeScript infers generic arguments from usage when possible — you
// don't always need to specify them explicitly (type argument inference).
function identity<T>(val: T): T { return val; }
console.log(`identity: ${identity<string>("TypeScript")}, ${identity(42)}`);  // => identity: TypeScript, 42

// Generic constraints (`extends`) restrict what types can be passed. Without constraints,
// T could be anything and you can't access specific properties. `extends HasLength`
// guarantees the type has a `.length` property. This is structural — any type with
// a `length: number` satisfies the constraint, not just types that explicitly implement it.
interface HasLength { length: number; }
function logLength<T extends HasLength>(val: T): T { console.log(`  length: ${val.length}`); return val; }  // => length: 5 / length: 3
logLength("hello");
logLength([1, 2, 3]);

// `keyof` produces a union of an object type's keys. Using `K extends keyof T`
// constrains the key parameter to only valid keys of T — the return type T[K]
// is then the precise type of that property (indexed access type).
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] { return obj[key]; }
console.log(`getProperty: ${getProperty(person, "name")}`);  // => getProperty: Bob

// Generic classes work like generic functions — the type parameter is specified at
// instantiation and flows through all methods. Stack<number> and Stack<string> are
// different types, but the implementation is shared (type erasure — generics don't
// exist at runtime, unlike Java's type erasure which uses Object + casts).
class Stack<T> {
  private items: T[] = [];
  push(item: T) { this.items.push(item); }
  pop(): T | undefined { return this.items.pop(); }
  peek(): T | undefined { return this.items[this.items.length - 1]; }
  get size() { return this.items.length; }
}
const stack = new Stack<number>();
stack.push(1); stack.push(2); stack.push(3);
console.log(`stack: peek=${stack.peek()}, size=${stack.size}, pop=${stack.pop()}`);  // => stack: peek=3, size=3, pop=3

// Default type parameters provide a fallback when the caller doesn't specify a type.
// `T = unknown` means the data field defaults to `unknown` (safer than `any` because
// you must narrow it before use). This mirrors default function arguments but at the type level.
interface ApiResponse<T = unknown, E = Error> { data: T | null; error: E | null; status: number; }
const response: ApiResponse<User> = { data: user, error: null, status: 200 };
console.log(`api response: status=${response.status}`);  // => api response: status=200

// `infer` in conditional types performs type-level pattern matching to extract parts
// of a type. ReturnOf extracts the return type from a function signature; FirstParam
// extracts the first parameter type. These replicate the built-in ReturnType<T> and
// Parameters<T> utility types. `infer` only works inside conditional type branches.
type ReturnOf<T> = T extends (...args: any[]) => infer R ? R : never;
type FirstParam<T> = T extends (first: infer F, ...rest: any[]) => any ? F : never;
type FnReturn = ReturnOf<typeof formatValue>; // string
type Param = FirstParam<(x: number, y: string) => void>; // number
console.log("(infer: compile-time type extraction)");  // => (infer: compile-time type extraction)

// ============================================================================
// 4. UTILITY TYPES
// ============================================================================
console.log("\n=== 4. UTILITY TYPES ===\n");  // => === 4. UTILITY TYPES ===

interface Config { host: string; port: number; debug: boolean; logLevel: string; }

// Partial<T> makes all properties optional. Use for update/patch operations where
// you only want to change some fields. Implemented as: { [K in keyof T]?: T[K] }
const partial: Partial<Config> = { host: "localhost" };
console.log("Partial:", partial);  // => Partial: { host: 'localhost' }

// Pick<T, K> creates a type with only the specified keys. Use when you need a subset
// of an interface for a specific context (e.g., only address fields for a form).
type ServerAddr = Pick<Config, "host" | "port">;
console.log("Pick:", { host: "0.0.0.0", port: 8080 } satisfies ServerAddr);  // => Pick: { host: '0.0.0.0', port: 8080 }

// Omit<T, K> creates a type with all properties EXCEPT the specified keys.
// Inverse of Pick. Implemented as Pick<T, Exclude<keyof T, K>>.
type PublicConfig = Omit<Config, "debug" | "logLevel">;
console.log("Omit:", { host: "prod.example.com", port: 443 } satisfies PublicConfig);  // => Omit: { host: 'prod.example.com', port: 443 }

// Record<K, V> creates an object type with keys of type K and values of type V.
// Useful for dictionaries/lookup tables. Record<string, T> is equivalent to { [key: string]: T }.
type StatusMap = Record<HttpStatus, string>;
console.log("Record:", { 200: "OK", 404: "Not Found" } as Partial<StatusMap>);  // => Record: { '200': 'OK', '404': 'Not Found' }

// Extract pulls union members that match a condition; Exclude removes them.
// Extract<T, U> = T extends U ? T : never. These distribute over unions automatically.
// Use Extract to filter a union to specific types; Exclude to remove unwanted types.
type Nums = Extract<string | number | boolean, number | boolean>;
type OnlyStr = Exclude<string | number | boolean, number | boolean>;
console.log("(Extract/Exclude: compile-time union filtering)");  // => (Extract/Exclude: compile-time union filtering)

// ReturnType<T> extracts the return type of a function type. Parameters<T> extracts
// the parameter types as a tuple. Both use conditional types with `infer` internally.
// `typeof createUser` gets the function type from a value — needed because ReturnType
// operates on types, not values.
function createUser(name: string, age: number): User {
  return { id: Date.now(), name, email: `${name}@example.com`, age };
}
type CreateParams = Parameters<typeof createUser>;
type CreateReturn = ReturnType<typeof createUser>;

// Awaited<T> recursively unwraps Promise types: Awaited<Promise<Promise<string>>> = string.
// NonNullable<T> removes null and undefined from a union: string | null | undefined -> string.
// Both are commonly used to extract the "real" type from wrapped values.
type PromiseResult = Awaited<Promise<Promise<string>>>; // string
type MaybeStr = string | null | undefined;
type DefiniteStr = NonNullable<MaybeStr>; // string
console.log("(Awaited, NonNullable: compile-time unwrapping)");  // => (Awaited, NonNullable: compile-time unwrapping)

// ============================================================================
// 5. TEMPLATE LITERAL TYPES
// ============================================================================
console.log("\n=== 5. TEMPLATE LITERAL TYPES ===\n");  // => === 5. TEMPLATE LITERAL TYPES ===

// Template literal types (TS 4.1) apply string interpolation at the TYPE level.
// Combined with union types, they generate the cartesian product of all combinations.
// `Capitalize<T>` is a built-in intrinsic type that capitalizes the first character.
// This enables type-safe event naming, CSS-in-TS, and route-based typing.
type EventName = "click" | "focus" | "blur";
type OnEvent = `on${Capitalize<EventName>}`; // "onClick" | "onFocus" | "onBlur"

// Template literal types compose with unions: `${number}${CSSUnit}` creates a type
// that matches any number followed by any unit string. This provides compile-time
// validation of CSS values without runtime parsing.
type CSSUnit = "px" | "rem" | "em" | "%";
type CSSValue = `${number}${CSSUnit}`;
const margin: CSSValue = "16px";
const padding: CSSValue = "1.5rem";
console.log(`CSS: margin=${margin}, padding=${padding}`);  // => CSS: margin=16px, padding=1.5rem

// Built-in string manipulation types are compiler intrinsics — they transform literal
// string types at compile time. They can't be implemented in userland TypeScript.
type Upper = Uppercase<"hello">;     // "HELLO"
type Lower = Lowercase<"HELLO">;     // "hello"
type Cap = Capitalize<"hello">;      // "Hello"
type Uncap = Uncapitalize<"Hello">;  // "hello"

// Type-safe event system: using generics with a string literal key constraint ensures
// the handler function receives the exact payload type for that event. The compiler
// infers T from the event name and narrows EventMap[T] to the specific payload type.
// This pattern is used by libraries like EventEmitter3 and tRPC.
type EventMap = {
  click: { x: number; y: number };
  keydown: { key: string; code: number };
  resize: { width: number; height: number };
};

function on<T extends keyof EventMap>(event: T, handler: (e: EventMap[T]) => void): void {
  console.log(`  registered '${event}'`);  // => registered 'click' / registered 'keydown'
}
on("click", (e) => console.log(`  click (${e.x},${e.y})`));
on("keydown", (e) => console.log(`  key: ${e.key}`));

// ============================================================================
// 6. TYPE GUARDS
// ============================================================================
console.log("\n=== 6. TYPE GUARDS ===\n");  // => === 6. TYPE GUARDS ===

// Type guards narrow a union type to a more specific type within a conditional block.
// `typeof` works for primitives (string, number, boolean, symbol, bigint, undefined, function).
// The compiler analyzes the control flow and narrows the type in each branch.
function processVal(val: string | number): string {
  return typeof val === "string" ? val.trim() : val.toFixed(2);
}
console.log(`typeof: "${processVal("  spaced  ")}", "${processVal(3.14159)}"`);  // => typeof: "spaced", "3.14"

// `instanceof` narrows to class instances. It checks the prototype chain at runtime,
// so it works with class hierarchies. The compiler narrows to the class type in the
// truthy branch, giving you access to class-specific properties like `statusCode`.
class ApiError extends Error {
  constructor(public statusCode: number, message: string) { super(message); }
}
function handleError(err: Error): string {
  return err instanceof ApiError ? `API ${err.statusCode}: ${err.message}` : `Error: ${err.message}`;
}
console.log(handleError(new ApiError(404, "Not Found")));  // => API 404: Not Found

// The `in` operator narrows discriminated unions by checking for property existence.
// If `"swim" in a` is true, TypeScript knows `a` must be the Fish variant.
// This is a runtime check that the compiler uses for compile-time narrowing.
type Fish = { swim: () => void };
type Bird = { fly: () => void };
function move(a: Fish | Bird): string { return "swim" in a ? "swimming" : "flying"; }
console.log(`in: ${move({ swim: () => {} })}`);  // => in: swimming

// Custom type predicates (`obj is User`) tell the compiler that when this function
// returns true, the argument is of the specified type. You're making a contract with
// the compiler — if the predicate logic is wrong, you get unsound types.
// Use for complex validation that typeof/instanceof can't express.
function isUser(obj: unknown): obj is User {
  return typeof obj === "object" && obj !== null && "id" in obj && "name" in obj && "email" in obj;
}
const maybe: unknown = { id: 1, name: "Test", email: "t@t.com" };
if (isUser(maybe)) console.log(`predicate: verified user ${maybe.name}`);  // => predicate: verified user Test

// Assertion functions (`asserts val is T`) narrow the type for ALL subsequent code,
// not just within an if-block. If the assertion fails, it throws — so the compiler
// knows the type is narrowed after the call returns. Similar to Node's assert().
function assertDefined<T>(val: T | null | undefined, name: string): asserts val is T {
  if (val == null) throw new Error(`${name} must be defined`);
}
let maybeVal: string | null = "exists";
assertDefined(maybeVal, "maybeVal");
// After assertDefined, compiler knows maybeVal is `string` (not string | null)
console.log(`assertion: ${maybeVal.toUpperCase()}`);  // => assertion: EXISTS

// ============================================================================
// 7. DECORATORS (patterns via manual application)
// ============================================================================
console.log("\n=== 7. DECORATORS ===\n");  // => === 7. DECORATORS ===

// Decorators modify classes/methods at definition time. TC39 Stage 3 decorators
// (TS 5.0+) differ from the older experimental decorators (--experimentalDecorators).
// Here we simulate them as higher-order functions to avoid requiring compiler flags.
// A class decorator receives the class constructor and returns a new (extended) class.
function logged<T extends { new (...args: any[]): {} }>(Base: T) {
  return class extends Base {
    constructor(...args: any[]) { console.log(`  creating ${Base.name}:`, args); super(...args); }  // => creating Service: [ 'MyService' ]
  };
}

class Service { constructor(public name: string) {} run() { return `${this.name} running`; } }
const LoggedService = logged(Service);
const svc = new LoggedService("MyService");
console.log(`result: ${svc.run()}`);  // => result: MyService running

// Method decorators receive the target prototype, method name, and property descriptor.
// By wrapping desc.value, you can add cross-cutting concerns (logging, timing, caching)
// without modifying the original method — this is the Aspect-Oriented Programming pattern.
function measure(_t: any, key: string, desc: PropertyDescriptor) {
  const orig = desc.value;
  desc.value = function (...args: any[]) {
    const t0 = performance.now();
    const r = orig.apply(this, args);
    console.log(`  ${key} took ${(performance.now() - t0).toFixed(3)}ms`);  // => compute took <N>ms
    return r;
  };
}
class MathOps { compute(n: number) { let s = 0; for (let i = 0; i < n; i++) s += i; return s; } }
const d = Object.getOwnPropertyDescriptor(MathOps.prototype, "compute")!;
measure(MathOps.prototype, "compute", d);
Object.defineProperty(MathOps.prototype, "compute", d);
console.log(`measured: ${new MathOps().compute(100000)}`);  // => measured: 4999950000

// ============================================================================
// 8. ADVANCED PATTERNS
// ============================================================================
console.log("\n=== 8. ADVANCED PATTERNS ===\n");  // => === 8. ADVANCED PATTERNS ===

// Branded types add a phantom property (__brand) that exists only at the type level
// (never set at runtime) to create nominal-like typing in a structural system.
// USD and EUR are both numbers, but the brand prevents accidentally mixing them.
// This pattern catches unit-of-measure errors, ID type confusion, and similar bugs.
type Brand<T, B> = T & { __brand: B };
type USD = Brand<number, "USD">;
type EUR = Brand<number, "EUR">;
function usd(n: number): USD { return n as USD; }
function eur(n: number): EUR { return n as EUR; }
function addUSD(a: USD, b: USD): USD { return (a + b) as USD; }
console.log(`branded: $${addUSD(usd(10), usd(20))}`);  // => branded: $30
// addUSD(usd(10), eur(20));  // compile error — can't mix currencies

// Builder pattern with progressive type narrowing: each call to select() adds a
// field to the generic parameter S, creating a compile-time record of which fields
// have been selected. This enables type-safe query builders where the compiler tracks
// what's been configured (used by Prisma, Drizzle, and similar ORMs).
class QueryBuilder<S extends string = never> {
  private parts: Record<string, any> = {};
  select<F extends string>(f: F): QueryBuilder<S | F> {
    this.parts.select = [...(this.parts.select || []), f];
    return this as unknown as QueryBuilder<S | F>;
  }
  where(cond: string): this { this.parts.where = cond; return this; }
  build(): string { return `SELECT ${this.parts.select?.join(", ")} WHERE ${this.parts.where}`; }
}
console.log(`builder: ${new QueryBuilder().select("name").select("email").where("active=true").build()}`);  // => builder: SELECT name, email WHERE active=true

// Type-safe event emitter: the Events generic constrains which event names can be
// emitted and ensures the data payload matches the expected type for that event.
// This eliminates the common bugs of misspelled event names and wrong payload shapes.
class TypedEmitter<Events extends Record<string, any>> {
  private handlers = new Map<keyof Events, Set<Function>>();
  on<E extends keyof Events>(event: E, handler: (data: Events[E]) => void) {
    if (!this.handlers.has(event)) this.handlers.set(event, new Set());
    this.handlers.get(event)!.add(handler);
  }
  emit<E extends keyof Events>(event: E, data: Events[E]) {
    this.handlers.get(event)?.forEach((h) => h(data));
  }
}
interface AppEvents {
  login: { userId: string; ts: number };
  error: { code: number; message: string };
}
const emitter = new TypedEmitter<AppEvents>();
emitter.on("login", (d) => console.log(`  login: ${d.userId}`));  // => login: u123
emitter.on("error", (d) => console.log(`  error: ${d.code} ${d.message}`));  // => error: 500 Internal
emitter.emit("login", { userId: "u123", ts: Date.now() });
emitter.emit("error", { code: 500, message: "Internal" });

// ============================================================================
// 9. MODULE PATTERNS
// ============================================================================
console.log("\n=== 9. MODULE PATTERNS ===\n");  // => === 9. MODULE PATTERNS ===

// Declaration merging: multiple interface declarations with the same name in the
// same scope are automatically combined. This is why libraries use interfaces for
// extensible APIs — consumers can augment them. Type aliases CANNOT be merged.
// This is the key practical difference between `interface` and `type`.
interface Box { width: number; height: number; }
interface Box { color: string; }
const box: Box = { width: 10, height: 20, color: "red" };
console.log("declaration merge:", box);  // => declaration merge: { width: 10, height: 20, color: 'red' }

// Namespace merging: a function and a namespace with the same name are merged.
// The function becomes callable, and the namespace adds static properties to it.
// This is how libraries like jQuery ($ function + $.ajax) model their APIs in TS.
function buildGreeting(name: string) { return `Hello, ${name}`; }
namespace buildGreeting { export const defaultName = "World"; }
console.log(`namespace merge: ${buildGreeting(buildGreeting.defaultName)}`);  // => namespace merge: Hello, World

// Ambient declarations (.d.ts files) describe the types of external code without
// implementing it. `declare module` types a whole module; `declare global` extends
// the global scope. Module augmentation lets you add properties to existing modules
// (e.g., adding userId to Express Request). These only exist at compile time.
// Ambient declarations (.d.ts):
//   declare module "my-lib" { export function doThing(x: string): number; }
//   declare global { interface Window { myApp: AppInstance; } }
// Module augmentation:
//   declare module "express" { interface Request { userId?: string; } }
console.log("(ambient declarations & augmentation: .d.ts patterns)");  // => (ambient declarations & augmentation: .d.ts patterns)

// ============================================================================
// 10. SATISFIES, CONST ASSERTIONS, NOINFER
// ============================================================================
console.log("\n=== 10. SATISFIES, CONST ASSERTIONS, NOINFER ===\n");  // => === 10. SATISFIES, CONST ASSERTIONS, NOINFER ===

// `satisfies` (TS 5.0) validates a value matches a type without changing the inferred type.
// With `as ColorMap`, `colors.red` would be `string | number[]` (widened).
// With `satisfies ColorMap`, `colors.red` stays `string` and `colors.green` stays `number[]` —
// you get validation AND narrow types. Use satisfies over `as` when you want both.
type ColorMap = Record<string, string | number[]>;
const colors = { red: "#FF0000", green: [0, 255, 0], blue: "#0000FF" } satisfies ColorMap;
console.log(`satisfies: red=${colors.red.toUpperCase()}, green=${colors.green.join(",")}`);  // => satisfies: red=#FF0000, green=0,255,0

// `as const` (const assertions) makes all properties readonly and narrows types to
// their literal values. Without it, `routes.home` is `string`; with it, it's `"/"`.
// This is essential for deriving union types from object values using typeof + keyof.
const routes = { home: "/", about: "/about", users: "/users" } as const;
// `typeof routes` gets the type of the value; `keyof typeof routes` gets "home" | "about" | "users";
// indexing with that union extracts "/" | "/about" | "/users".
type Route = (typeof routes)[keyof typeof routes];
console.log(`as const: home=${routes.home}`);  // => as const: home=/

// For tuples, `as const` preserves the exact types and positions — without it,
// [1, "two", true] is inferred as (string | number | boolean)[].
const tuple = [1, "two", true] as const;
console.log(`const tuple: ${tuple[0]} (literal 1, not number)`);  // => const tuple: 1 (literal 1, not number)

// NoInfer<T> (TS 5.4) prevents TypeScript from using a parameter for type inference.
// Without it, `initial` would contribute to inferring S, potentially widening the union.
// With NoInfer, only the `states` array determines S — `initial` must match a known state.
// This prevents accidentally creating states via typos in `initial`.
function createFSM<S extends string>(config: { initial: NoInfer<S>; states: S[] }) { return config; }
const fsm = createFSM({ initial: "idle", states: ["idle", "loading", "success", "error"] });
console.log(`NoInfer FSM: ${fsm.initial}`);  // => NoInfer FSM: idle

// satisfies + Record for exhaustive compile-time checking: if you add a new Status
// variant without adding a label, the compiler errors. This is safer than a switch
// with assertNever because it's checked at the definition site, not the usage site.
type Status = "active" | "inactive" | "pending";
const labels = { active: "Active", inactive: "Inactive", pending: "Pending" } satisfies Record<Status, string>;
console.log(`exhaustive: ${labels.active}`);  // => exhaustive: Active

// ============================================================================
// BONUS: Additional Type Patterns
// ============================================================================
console.log("\n=== BONUS: ADDITIONAL PATTERNS ===\n");  // => === BONUS: ADDITIONAL PATTERNS ===

// Recursive types reference themselves in their definition. JSONValue can contain
// arrays of JSONValue or objects mapping strings to JSONValue — modeling the full
// JSON spec. TypeScript handles recursive types lazily (they're expanded on demand).
type JSONValue = string | number | boolean | null | JSONValue[] | { [k: string]: JSONValue };
const jsonData: JSONValue = { name: "test", nested: { arr: [1, "two", true, null] } };
console.log("recursive type:", JSON.stringify(jsonData));  // => recursive type: {"name":"test","nested":{"arr":[1,"two",true,null]}}

// Variadic tuple types (TS 4.0) allow spreading tuple types within other tuples.
// [...A, ...B] concatenates two tuple types at the type level. This enables typed
// versions of array operations like concat, push, and unshift while preserving
// the exact types and positions of each element.
type Concat<A extends any[], B extends any[]> = [...A, ...B];
type Result = Concat<[1, 2], [3, 4]>; // [1, 2, 3, 4]

function concat<A extends any[], B extends any[]>(a: A, b: B): Concat<A, B> {
  return [...a, ...b] as Concat<A, B>;
}
console.log("variadic tuple:", concat([1, 2], ["a", "b"]));  // => variadic tuple: [ 1, 2, 'a', 'b' ]

// Exhaustiveness checking: `never` represents a type with no possible values.
// In a switch over a discriminated union, after handling all variants, the type
// narrows to `never`. Assigning to `assertNever(x: never)` catches missing cases
// at compile time — adding a new Fruit variant without a case causes a type error.
function assertNever(x: never): never { throw new Error(`Unexpected: ${x}`); }
type Fruit = "apple" | "banana" | "cherry";
function fruitColor(f: Fruit): string {
  switch (f) {
    case "apple": return "red";
    case "banana": return "yellow";
    case "cherry": return "dark red";
    // If a new variant is added, this fails at compile time:
    // default: return assertNever(f);
  }
}
console.log(`exhaustive: ${fruitColor("cherry")}`);  // => exhaustive: dark red

console.log("\n=== ALL DEMOS COMPLETE ===");  // => === ALL DEMOS COMPLETE ===
