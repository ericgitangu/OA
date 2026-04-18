// ts_fundamentals.ts — TypeScript Fundamentals
// Run: npx tsx ts_fundamentals.ts
// ============================================================================
// 1. BASICS — Type Annotations, Interfaces, Aliases, Literals, Enums
// ============================================================================
console.log("=== 1. BASICS ===\n");

const greeting: string = "Hello, TypeScript";
const year: number = 2024;
const active: boolean = true;
console.log(`${greeting} | year: ${year} | active: ${active}`);

// Interfaces
interface User {
  readonly id: number;
  name: string;
  email: string;
  age?: number;
}
const user: User = { id: 1, name: "Alice", email: "alice@example.com" };
console.log("user:", user);

// Type aliases
type Point = { x: number; y: number };
type ID = string | number;
console.log(`point: (${0}, ${0}), userId: ${"abc-123" as ID}`);

// Literal types
type Direction = "north" | "south" | "east" | "west";
type HttpStatus = 200 | 301 | 404 | 500;
console.log(`literal: dir=${"north" satisfies Direction}, status=${200 satisfies HttpStatus}`);

// Enums
enum LogLevel { DEBUG, INFO, WARN, ERROR }
enum Color { Red = "#FF0000", Green = "#00FF00", Blue = "#0000FF" }
console.log(`enum: WARN=${LogLevel.WARN}, Red=${Color.Red}, reverse=${LogLevel[2]}`);

const enum HttpMethod { GET = "GET", POST = "POST", PUT = "PUT", DELETE = "DELETE" }
console.log(`const enum: ${HttpMethod.POST}`);

// ============================================================================
// 2. ADVANCED TYPES
// ============================================================================
console.log("\n=== 2. ADVANCED TYPES ===\n");

// Union
function formatValue(val: string | number | boolean): string {
  if (typeof val === "string") return val.toUpperCase();
  if (typeof val === "number") return val.toFixed(2);
  return val ? "YES" : "NO";
}
console.log(`union: ${formatValue("hello")}, ${formatValue(3.14)}, ${formatValue(true)}`);

// Intersection
type HasName = { name: string };
type HasAge = { age: number };
type Person = HasName & HasAge;
const person: Person = { name: "Bob", age: 30 };
console.log("intersection:", person);

// Discriminated unions
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
console.log(`area: circle=${area({ kind: "circle", radius: 5 }).toFixed(2)}, rect=${area({ kind: "rect", width: 4, height: 6 })}`);

// Mapped types
type Readonly2<T> = { readonly [K in keyof T]: T[K] };
type Optional<T> = { [K in keyof T]?: T[K] };
type Nullable<T> = { [K in keyof T]: T[K] | null };
const frozen: Readonly2<Point> = { x: 1, y: 2 };
console.log("mapped readonly:", frozen);

// Conditional types
type IsString<T> = T extends string ? "yes" : "no";
type A = IsString<string>; // "yes"
type B = IsString<number>; // "no"
type UnpackArray<T> = T extends Array<infer U> ? U : T;
type Unpacked = UnpackArray<string[]>; // string
console.log("(conditional types: compile-time type branching)");

// ============================================================================
// 3. GENERICS
// ============================================================================
console.log("\n=== 3. GENERICS ===\n");

function identity<T>(val: T): T { return val; }
console.log(`identity: ${identity<string>("TypeScript")}, ${identity(42)}`);

// Constraints
interface HasLength { length: number; }
function logLength<T extends HasLength>(val: T): T { console.log(`  length: ${val.length}`); return val; }
logLength("hello");
logLength([1, 2, 3]);

// keyof constraint
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] { return obj[key]; }
console.log(`getProperty: ${getProperty(person, "name")}`);

// Generic class
class Stack<T> {
  private items: T[] = [];
  push(item: T) { this.items.push(item); }
  pop(): T | undefined { return this.items.pop(); }
  peek(): T | undefined { return this.items[this.items.length - 1]; }
  get size() { return this.items.length; }
}
const stack = new Stack<number>();
stack.push(1); stack.push(2); stack.push(3);
console.log(`stack: peek=${stack.peek()}, size=${stack.size}, pop=${stack.pop()}`);

// Default type parameters
interface ApiResponse<T = unknown, E = Error> { data: T | null; error: E | null; status: number; }
const response: ApiResponse<User> = { data: user, error: null, status: 200 };
console.log(`api response: status=${response.status}`);

// infer keyword
type ReturnOf<T> = T extends (...args: any[]) => infer R ? R : never;
type FirstParam<T> = T extends (first: infer F, ...rest: any[]) => any ? F : never;
type FnReturn = ReturnOf<typeof formatValue>; // string
type Param = FirstParam<(x: number, y: string) => void>; // number
console.log("(infer: compile-time type extraction)");

// ============================================================================
// 4. UTILITY TYPES
// ============================================================================
console.log("\n=== 4. UTILITY TYPES ===\n");

interface Config { host: string; port: number; debug: boolean; logLevel: string; }

const partial: Partial<Config> = { host: "localhost" };
console.log("Partial:", partial);

type ServerAddr = Pick<Config, "host" | "port">;
console.log("Pick:", { host: "0.0.0.0", port: 8080 } satisfies ServerAddr);

type PublicConfig = Omit<Config, "debug" | "logLevel">;
console.log("Omit:", { host: "prod.example.com", port: 443 } satisfies PublicConfig);

type StatusMap = Record<HttpStatus, string>;
console.log("Record:", { 200: "OK", 404: "Not Found" } as Partial<StatusMap>);

// Extract / Exclude
type Nums = Extract<string | number | boolean, number | boolean>;
type OnlyStr = Exclude<string | number | boolean, number | boolean>;
console.log("(Extract/Exclude: compile-time union filtering)");

// ReturnType / Parameters
function createUser(name: string, age: number): User {
  return { id: Date.now(), name, email: `${name}@example.com`, age };
}
type CreateParams = Parameters<typeof createUser>;
type CreateReturn = ReturnType<typeof createUser>;

// Awaited, NonNullable
type PromiseResult = Awaited<Promise<Promise<string>>>; // string
type MaybeStr = string | null | undefined;
type DefiniteStr = NonNullable<MaybeStr>; // string
console.log("(Awaited, NonNullable: compile-time unwrapping)");

// ============================================================================
// 5. TEMPLATE LITERAL TYPES
// ============================================================================
console.log("\n=== 5. TEMPLATE LITERAL TYPES ===\n");

type EventName = "click" | "focus" | "blur";
type OnEvent = `on${Capitalize<EventName>}`; // "onClick" | "onFocus" | "onBlur"

type CSSUnit = "px" | "rem" | "em" | "%";
type CSSValue = `${number}${CSSUnit}`;
const margin: CSSValue = "16px";
const padding: CSSValue = "1.5rem";
console.log(`CSS: margin=${margin}, padding=${padding}`);

// String manipulation types
type Upper = Uppercase<"hello">;     // "HELLO"
type Lower = Lowercase<"HELLO">;     // "hello"
type Cap = Capitalize<"hello">;      // "Hello"
type Uncap = Uncapitalize<"Hello">;  // "hello"

// Type-safe event system
type EventMap = {
  click: { x: number; y: number };
  keydown: { key: string; code: number };
  resize: { width: number; height: number };
};

function on<T extends keyof EventMap>(event: T, handler: (e: EventMap[T]) => void): void {
  console.log(`  registered '${event}'`);
}
on("click", (e) => console.log(`  click (${e.x},${e.y})`));
on("keydown", (e) => console.log(`  key: ${e.key}`));

// ============================================================================
// 6. TYPE GUARDS
// ============================================================================
console.log("\n=== 6. TYPE GUARDS ===\n");

// typeof
function processVal(val: string | number): string {
  return typeof val === "string" ? val.trim() : val.toFixed(2);
}
console.log(`typeof: "${processVal("  spaced  ")}", "${processVal(3.14159)}"`);

// instanceof
class ApiError extends Error {
  constructor(public statusCode: number, message: string) { super(message); }
}
function handleError(err: Error): string {
  return err instanceof ApiError ? `API ${err.statusCode}: ${err.message}` : `Error: ${err.message}`;
}
console.log(handleError(new ApiError(404, "Not Found")));

// 'in' operator
type Fish = { swim: () => void };
type Bird = { fly: () => void };
function move(a: Fish | Bird): string { return "swim" in a ? "swimming" : "flying"; }
console.log(`in: ${move({ swim: () => {} })}`);

// Custom type predicates
function isUser(obj: unknown): obj is User {
  return typeof obj === "object" && obj !== null && "id" in obj && "name" in obj && "email" in obj;
}
const maybe: unknown = { id: 1, name: "Test", email: "t@t.com" };
if (isUser(maybe)) console.log(`predicate: verified user ${maybe.name}`);

// Assertion functions
function assertDefined<T>(val: T | null | undefined, name: string): asserts val is T {
  if (val == null) throw new Error(`${name} must be defined`);
}
let maybeVal: string | null = "exists";
assertDefined(maybeVal, "maybeVal");
console.log(`assertion: ${maybeVal.toUpperCase()}`);

// ============================================================================
// 7. DECORATORS (patterns via manual application)
// ============================================================================
console.log("\n=== 7. DECORATORS ===\n");

// Class decorator pattern (no flag needed — shown as HOF)
function logged<T extends { new (...args: any[]): {} }>(Base: T) {
  return class extends Base {
    constructor(...args: any[]) { console.log(`  creating ${Base.name}:`, args); super(...args); }
  };
}

class Service { constructor(public name: string) {} run() { return `${this.name} running`; } }
const LoggedService = logged(Service);
const svc = new LoggedService("MyService");
console.log(`result: ${svc.run()}`);

// Method decorator pattern
function measure(_t: any, key: string, desc: PropertyDescriptor) {
  const orig = desc.value;
  desc.value = function (...args: any[]) {
    const t0 = performance.now();
    const r = orig.apply(this, args);
    console.log(`  ${key} took ${(performance.now() - t0).toFixed(3)}ms`);
    return r;
  };
}
class MathOps { compute(n: number) { let s = 0; for (let i = 0; i < n; i++) s += i; return s; } }
const d = Object.getOwnPropertyDescriptor(MathOps.prototype, "compute")!;
measure(MathOps.prototype, "compute", d);
Object.defineProperty(MathOps.prototype, "compute", d);
console.log(`measured: ${new MathOps().compute(100000)}`);

// ============================================================================
// 8. ADVANCED PATTERNS
// ============================================================================
console.log("\n=== 8. ADVANCED PATTERNS ===\n");

// Branded types
type Brand<T, B> = T & { __brand: B };
type USD = Brand<number, "USD">;
type EUR = Brand<number, "EUR">;
function usd(n: number): USD { return n as USD; }
function eur(n: number): EUR { return n as EUR; }
function addUSD(a: USD, b: USD): USD { return (a + b) as USD; }
console.log(`branded: $${addUSD(usd(10), usd(20))}`);
// addUSD(usd(10), eur(20));  // compile error — can't mix currencies

// Builder pattern with types
class QueryBuilder<S extends string = never> {
  private parts: Record<string, any> = {};
  select<F extends string>(f: F): QueryBuilder<S | F> {
    this.parts.select = [...(this.parts.select || []), f];
    return this as unknown as QueryBuilder<S | F>;
  }
  where(cond: string): this { this.parts.where = cond; return this; }
  build(): string { return `SELECT ${this.parts.select?.join(", ")} WHERE ${this.parts.where}`; }
}
console.log(`builder: ${new QueryBuilder().select("name").select("email").where("active=true").build()}`);

// Type-safe event emitter
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
emitter.on("login", (d) => console.log(`  login: ${d.userId}`));
emitter.on("error", (d) => console.log(`  error: ${d.code} ${d.message}`));
emitter.emit("login", { userId: "u123", ts: Date.now() });
emitter.emit("error", { code: 500, message: "Internal" });

// ============================================================================
// 9. MODULE PATTERNS
// ============================================================================
console.log("\n=== 9. MODULE PATTERNS ===\n");

// Declaration merging
interface Box { width: number; height: number; }
interface Box { color: string; }
const box: Box = { width: 10, height: 20, color: "red" };
console.log("declaration merge:", box);

// Namespace merging
function buildGreeting(name: string) { return `Hello, ${name}`; }
namespace buildGreeting { export const defaultName = "World"; }
console.log(`namespace merge: ${buildGreeting(buildGreeting.defaultName)}`);

// Ambient declarations (.d.ts):
//   declare module "my-lib" { export function doThing(x: string): number; }
//   declare global { interface Window { myApp: AppInstance; } }
// Module augmentation:
//   declare module "express" { interface Request { userId?: string; } }
console.log("(ambient declarations & augmentation: .d.ts patterns)");

// ============================================================================
// 10. SATISFIES, CONST ASSERTIONS, NOINFER
// ============================================================================
console.log("\n=== 10. SATISFIES, CONST ASSERTIONS, NOINFER ===\n");

// satisfies — validate without widening
type ColorMap = Record<string, string | number[]>;
const colors = { red: "#FF0000", green: [0, 255, 0], blue: "#0000FF" } satisfies ColorMap;
console.log(`satisfies: red=${colors.red.toUpperCase()}, green=${colors.green.join(",")}`);

// const assertions
const routes = { home: "/", about: "/about", users: "/users" } as const;
type Route = (typeof routes)[keyof typeof routes];
console.log(`as const: home=${routes.home}`);

const tuple = [1, "two", true] as const;
console.log(`const tuple: ${tuple[0]} (literal 1, not number)`);

// NoInfer
function createFSM<S extends string>(config: { initial: NoInfer<S>; states: S[] }) { return config; }
const fsm = createFSM({ initial: "idle", states: ["idle", "loading", "success", "error"] });
console.log(`NoInfer FSM: ${fsm.initial}`);

// satisfies + Record for exhaustive checking
type Status = "active" | "inactive" | "pending";
const labels = { active: "Active", inactive: "Inactive", pending: "Pending" } satisfies Record<Status, string>;
console.log(`exhaustive: ${labels.active}`);

// ============================================================================
// BONUS: Additional Type Patterns
// ============================================================================
console.log("\n=== BONUS: ADDITIONAL PATTERNS ===\n");

// Recursive types
type JSONValue = string | number | boolean | null | JSONValue[] | { [k: string]: JSONValue };
const jsonData: JSONValue = { name: "test", nested: { arr: [1, "two", true, null] } };
console.log("recursive type:", JSON.stringify(jsonData));

// Variadic tuple types
type Concat<A extends any[], B extends any[]> = [...A, ...B];
type Result = Concat<[1, 2], [3, 4]>; // [1, 2, 3, 4]

function concat<A extends any[], B extends any[]>(a: A, b: B): Concat<A, B> {
  return [...a, ...b] as Concat<A, B>;
}
console.log("variadic tuple:", concat([1, 2], ["a", "b"]));

// Exhaustiveness checking with never
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
console.log(`exhaustive: ${fruitColor("cherry")}`);

console.log("\n=== ALL DEMOS COMPLETE ===");
