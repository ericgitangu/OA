(ns clojure-fundamentals
  "Clojure Fundamentals: Beginner to Advanced — Standard Library Only.

   A dense, runnable syntax reference covering core Clojure concepts.
   Run: clj -M clojure_fundamentals.clj
        or: clojure clojure_fundamentals.clj
   Requires: Clojure 1.11+

   Clojure is a Lisp dialect on the JVM, designed around three core ideas:
   1. Immutability by default — all data structures are persistent (immutable).
   2. Homoiconicity — code is data. Clojure code is written in Clojure data structures
      (lists, vectors, maps), so programs can manipulate their own code via macros.
   3. Concurrency primitives — atoms, refs, agents provide different coordination models
      without manual locking."
  (:require [clojure.string :as str]
            [clojure.set :as cset]
            [clojure.spec.alpha :as s]))

(defn section [title]
  (println (str "\n" (apply str (repeat 60 "="))
               "\n  " title
               "\n" (apply str (repeat 60 "=")))))

;; ============================================================
;;  1. BASICS
;; ============================================================
(defn basics []
  (section "1. BASICS — def, let, Atoms, Keywords, Strings, Regex")

  ;; Clojure has rich numeric types. Ratios (22/7) are exact — no floating-point
  ;; rounding errors. BigInt (42N) and BigDecimal (3.14M) support arbitrary precision.
  ;; The JVM handles the heavy lifting for numeric types.
  (println "Integer:" 42 " Long:" 9999999999 " BigInt:" 42N)
  (println "Float:" 3.14 " Ratio:" (/ 22 7) " BigDecimal:" 3.14M)
  (println "String:" "hello" " Char:" \a " Boolean:" true " Nil:" nil)

  ;; Keywords (:name) are interned strings that evaluate to themselves.
  ;; They're also functions — (:name map) looks up :name in the map.
  ;; This dual nature (data AND function) is idiomatic Clojure and enables concise code.
  ;; Namespaced keywords (::local) expand to :current-ns/local for global uniqueness.
  (println "Keyword:" :name " Namespaced:" ::local)
  (println "Keyword as fn:" (:name {:name "Alice" :age 30}))

  ;; def creates a global var (like a global constant). It's not variable assignment —
  ;; vars are stable references that can be rebound at the REPL but shouldn't change in production.
  ;; let creates lexical bindings — local, immutable, and scoped to the let block.
  ;; All bindings are expressed as vectors of pairs: [name value name value ...].
  (def pi 3.14159)
  (let [x 10
        y 20
        sum (+ x y)]
    (println "let binding: x=" x "y=" y "sum=" sum))

  ;; Strings are Java strings. str concatenates by calling .toString on each arg.
  ;; clojure.string provides functional string operations that compose with pipelines.
  (println "str concat:" (str "Hello" ", " "World!"))
  (println "format:" (format "Pi is %.4f" pi))
  (println "split:" (str/split "a,b,c" #","))
  (println "join:" (str/join "-" ["hello" "world"]))
  (println "upper:" (str/upper-case "hello"))
  (println "includes?:" (str/includes? "hello world" "world"))

  ;; Regex literals use #"pattern" syntax — compiled to java.util.regex.Pattern at read time.
  (println "re-find:" (re-find #"\d+" "abc 123 def"))
  (println "re-seq:" (re-seq #"\w+" "hello world 42"))
  (println "re-matches:" (re-matches #"(\d{4})-(\d{2})" "2024-01")))

;; ============================================================
;;  2. DATA STRUCTURES
;; ============================================================
(defn data-structures []
  (section "2. DATA STRUCTURES — Lists, Vectors, Maps, Sets")

  ;; All Clojure collections are persistent (immutable) data structures that use
  ;; STRUCTURAL SHARING. When you "modify" a vector, the new version shares most of
  ;; its internal tree nodes with the original — typically O(log32 n) nodes are copied.
  ;; This makes immutability practical: updates are nearly as fast as mutation.

  ;; Lists are singly-linked — O(1) prepend (conj adds to front), O(n) random access.
  ;; Quoted '(1 2 3) prevents evaluation (without quote, Clojure would try to call 1 as a function).
  (let [lst '(1 2 3 4 5)]
    (println "List:" lst "first:" (first lst) "rest:" (rest lst))
    (println "conj (prepend):" (conj lst 0))
    (println "cons:" (cons 0 lst)))

  ;; Vectors are the workhorse collection — O(~1) access, O(~1) append.
  ;; Internally they're 32-way branching trees (Hash Array Mapped Tries).
  ;; conj adds to the END (unlike lists where conj adds to the front).
  ;; This polymorphic conj behavior means algorithms work with any collection type.
  (let [v [10 20 30 40 50]]
    (println "Vector:" v "nth:" (nth v 2) "get:" (get v 1))
    (println "conj (append):" (conj v 60))
    (println "assoc:" (assoc v 2 99))
    (println "subvec:" (subvec v 1 4))
    (println "peek:" (peek v) "pop:" (pop v)))

  ;; Maps are hash array mapped tries — O(~1) lookup, insert, update.
  ;; They use structural sharing internally, so (assoc m :key val) creates a new map
  ;; that shares most of its structure with m. Keywords as keys are idiomatic.
  (let [m {:name "Clojure" :year 2007 :creator "Rich Hickey"}]
    (println "Map:" m)
    (println "get:" (get m :name) "keyword-as-fn:" (:year m))
    (println "assoc:" (assoc m :version "1.11"))
    (println "dissoc:" (dissoc m :year))
    (println "merge:" (merge m {:paradigm "FP"}))
    (println "select-keys:" (select-keys m [:name :year]))
    (println "update:" (update m :year inc)))

  ;; get-in, assoc-in, update-in navigate nested data structures using key paths.
  ;; This eliminates the need for lens libraries or mutable nested updates.
  (let [nested {:user {:address {:city "Portland"}}}]
    (println "get-in:" (get-in nested [:user :address :city]))
    (println "assoc-in:" (assoc-in nested [:user :address :zip] "97201"))
    (println "update-in:" (update-in nested [:user :address :city] str/upper-case)))

  ;; Sets are unordered collections of unique values. #{} is the literal syntax.
  ;; Sets are also functions — (#{1 2 3} 2) returns 2 (truthy), (#{1 2 3} 4) returns nil.
  (let [s1 #{1 2 3 4}
        s2 #{3 4 5 6}]
    (println "Set:" s1 "contains?:" (contains? s1 3))
    (println "union:" (cset/union s1 s2))
    (println "intersection:" (cset/intersection s1 s2))
    (println "difference:" (cset/difference s1 s2))
    (println "conj:" (conj s1 5) "disj:" (disj s1 2)))

  ;; Persistence demo: v1 is NOT modified when v2 is created.
  ;; Both v1 and v2 share internal tree structure — only the path from root to the
  ;; changed leaf is copied. This is O(log32 n) time and space.
  (let [v1 [1 2 3]
        v2 (conj v1 4)]
    (println "Persistent: v1=" v1 "v2=" v2 "(v1 unchanged)")))

;; ============================================================
;;  3. FUNCTIONS
;; ============================================================
(defn functions-demo []
  (section "3. FUNCTIONS — defn, Anonymous, Partial, Comp, Threading")

  ;; Multi-arity functions define different bodies for different argument counts.
  ;; Each arity is a separate list within the defn. One arity often delegates to another.
  (defn greet
    ([name] (greet name "Hello"))
    ([name greeting] (str greeting ", " name "!")))
  (println "Multi-arity:" (greet "Alice") (greet "Bob" "Hey"))

  ;; fn creates an anonymous function. #(* %1 %1 %1) is the reader macro shorthand —
  ;; %1, %2, etc. refer to positional arguments. Use fn for multi-line bodies,
  ;; #() for quick one-liners. #() cannot be nested.
  (let [square (fn [x] (* x x))
        cube #(* %1 %1 %1)]
    (println "Anonymous fn:" (square 5) "Reader macro:" (cube 3)))

  ;; apply "unpacks" a collection into positional arguments — like spread in JS.
  ;; map, filter, remove return lazy sequences — they don't compute until consumed.
  (println "apply:" (apply + [1 2 3 4 5]))
  (println "map:" (map inc [1 2 3]))
  (println "filter:" (filter even? (range 1 11)))
  (println "remove:" (remove even? (range 1 11)))

  ;; partial fixes some arguments, returning a new function.
  ;; comp composes functions right-to-left: (comp f g) = f(g(x)).
  ;; juxt applies multiple functions to the same args, returning a vector of results.
  ;; These three compose simple functions into complex ones without defining new ones.
  (let [add10 (partial + 10)
        double-then-inc (comp inc #(* 2 %))
        stats (juxt count #(apply min %) #(apply max %))]
    (println "partial:" (add10 5))
    (println "comp:" (double-then-inc 5))
    (println "juxt:" (stats [3 1 4 1 5 9])))

  ;; Threading macros restructure nested calls into sequential pipelines.
  ;; -> (thread-first) inserts each result as the FIRST arg of the next form.
  ;; ->> (thread-last) inserts as the LAST arg. These are macros, not functions —
  ;; they rewrite the code at compile time, so there's zero runtime overhead.
  (println "->  (thread-first):"
           (-> "  Hello, World!  "
               str/trim
               str/lower-case
               (str/split #" ")
               first))
  (println "->> (thread-last):"
           (->> (range 1 11)
                (filter even?)
                (map #(* % %))
                (reduce +))))

;; ============================================================
;;  4. SEQUENCES
;; ============================================================
(defn sequences-demo []
  (section "4. SEQUENCES — map, filter, reduce, and friends")

  ;; The sequence abstraction (ISeq) unifies all collection types.
  ;; map, filter, reduce work on ANY seq-able thing: lists, vectors, maps, sets, strings,
  ;; Java collections, files, etc. This is because they operate on the sequence interface,
  ;; not concrete types. Most sequence operations return lazy sequences.
  (let [nums (range 1 11)]
    (println "map:"         (map #(* % 2) nums))
    ;; mapcat = map + concat. Like flatMap in other languages.
    (println "mapcat:"      (mapcat #(vector % (* % 10)) [1 2 3]))
    (println "frequencies:" (frequencies [:a :b :a :c :b :a]))
    (println "group-by:"    (group-by #(mod % 3) nums))
    (println "partition:"   (partition 3 nums))
    (println "partition-by:" (partition-by #(< % 5) nums))
    ;; (range) with no args is infinite — take 5 realizes only 5 elements.
    ;; Lazy sequences are computed on demand and cached once computed.
    (println "take:"        (take 5 (range)))
    (println "drop:"        (drop 7 nums))
    (println "take-while:"  (take-while #(< % 5) nums))
    (println "interleave:"  (interleave [:a :b :c] [1 2 3]))
    (println "interpose:"   (interpose ", " ["a" "b" "c"]))
    ;; zipmap creates a map from two sequences — keys and values.
    (println "zipmap:"      (zipmap [:a :b :c] [1 2 3]))
    ;; into pours one collection into another, using the target's conj behavior.
    (println "into:"        (into {} [[:a 1] [:b 2] [:c 3]]))
    (println "distinct:"    (distinct [1 1 2 3 3 2 4]))
    (println "sort-by:"     (sort-by count ["banana" "fig" "apple"]))))

;; ============================================================
;;  5. POLYMORPHISM
;; ============================================================
(defn polymorphism-demo []
  (section "5. POLYMORPHISM — Multimethods, Protocols, Records")

  ;; Multimethods dispatch on an arbitrary function (the dispatch function).
  ;; Here, :shape extracts the dispatch value from the argument map.
  ;; Unlike OOP dispatch (based on receiver type), multimethods can dispatch on
  ;; any computable value — type, value, combination of fields, etc.
  ;; This is open dispatch: anyone can add new methods without modifying existing code.
  (defmulti area :shape)
  (defmethod area :circle [{:keys [radius]}]
    (* Math/PI radius radius))
  (defmethod area :rectangle [{:keys [width height]}]
    (* width height))
  (defmethod area :default [shape]
    (str "Unknown shape: " (:shape shape)))

  (println "Circle area:" (format "%.2f" (area {:shape :circle :radius 5})))
  (println "Rect area:" (area {:shape :rectangle :width 4 :height 6}))

  ;; Protocols are like interfaces but dispatching on the type of the first argument.
  ;; They're faster than multimethods (JVM-level dispatch) but less flexible (type-only dispatch).
  ;; Use protocols when you need type-based polymorphism; multimethods for value-based.
  (defprotocol Describable
    (describe [this] "Return a description"))

  ;; Records are map-like types with fixed keys, faster field access, and protocol implementations.
  ;; They compile to JVM classes with typed fields — faster than plain maps for known schemas.
  ;; Records still support all map operations (assoc, get, etc.) via the map interface.
  (defrecord Dog [name breed]
    Describable
    (describe [_] (str name " the " breed " dog")))

  (defrecord Cat [name indoor?]
    Describable
    (describe [_] (str name " the " (if indoor? "indoor" "outdoor") " cat")))

  (println "Protocol:" (describe (->Dog "Rex" "Lab")))
  (println "Protocol:" (describe (->Cat "Whiskers" true)))

  ;; Records support map operations because they implement IPersistentMap.
  (let [d (->Dog "Buddy" "Beagle")
        d2 (assoc d :age 5)]
    (println "Record:" d "name:" (:name d))
    (println "assoc'd:" d2))

  ;; reify creates an anonymous, one-off implementation of a protocol or interface.
  ;; Like Kotlin's object expression or Java's anonymous class, but more concise.
  (let [obj (reify Describable
              (describe [_] "I'm a reified object"))]
    (println "reify:" (describe obj))))

;; ============================================================
;;  6. CONCURRENCY
;; ============================================================
(defn concurrency-demo []
  (section "6. CONCURRENCY — Atom, Ref, Agent, Future, Promise")

  ;; Clojure's concurrency model has four reference types, each for a different use case:
  ;; - Atom: uncoordinated, synchronous (one value, compare-and-swap)
  ;; - Ref: coordinated, synchronous (multiple values, transactions via STM)
  ;; - Agent: uncoordinated, asynchronous (one value, fire-and-forget updates)
  ;; - Var: thread-local (per-thread binding, used for dynamic scope)

  ;; Atom uses CAS (compare-and-swap) — swap! retries if another thread changed the value.
  ;; Because the swap function must be pure (it may run multiple times), atoms are safe
  ;; without locks. @ (deref) reads the current value atomically.
  (let [counter (atom 0)]
    (swap! counter inc)
    (swap! counter inc)
    (swap! counter + 10)
    (println "Atom:" @counter)
    (reset! counter 0)
    (println "After reset:" @counter))

  ;; Validators ensure atoms only hold valid values — the validator function runs on every
  ;; swap!/reset! and throws if it returns false. This is runtime invariant enforcement.
  (let [age (atom 25 :validator #(and (integer? %) (>= % 0)))]
    (swap! age inc)
    (println "Validated atom:" @age)
    (try
      (reset! age -1)
      (catch Exception e
        (println "Validator rejected:" (.getMessage e)))))

  ;; Refs use Software Transactional Memory (STM) — Clojure's answer to coordinated state.
  ;; dosync creates a transaction: ALL ref changes within it are atomic, consistent, and isolated.
  ;; If two transactions conflict, one is automatically retried (optimistic concurrency).
  ;; This eliminates deadlocks and race conditions without manual lock management.
  ;; STM is ideal when multiple pieces of state must change together (like a bank transfer).
  (let [account-a (ref 1000)
        account-b (ref 500)]
    (dosync
     (alter account-a - 200)
     (alter account-b + 200))
    (println "Refs after transfer: A=" @account-a "B=" @account-b))

  ;; Agents handle state changes asynchronously. send dispatches the update function
  ;; to a thread pool — the caller doesn't wait. Agents process messages sequentially,
  ;; so no two updates run concurrently for the same agent.
  (let [log-agent (agent [])]
    (send log-agent conj "message 1")
    (send log-agent conj "message 2")
    (await log-agent)
    (println "Agent:" @log-agent))

  ;; Futures run a computation on another thread. Dereferencing (@f) blocks until complete.
  ;; This is like Java's Future but with Clojure's immutable value semantics.
  (let [f (future (Thread/sleep 10) (* 6 7))]
    (println "Future:" @f "realized?:" (realized? f)))

  ;; Promises are single-write containers — deliver sets the value, deref reads it.
  ;; A promise can only be delivered once; subsequent delivers are no-ops.
  (let [p (promise)]
    (future (Thread/sleep 10) (deliver p 42))
    (println "Promise:" @p "realized?:" (realized? p))))

;; ============================================================
;;  7. TRANSDUCERS
;; ============================================================
(defn transducers-demo []
  (section "7. TRANSDUCERS — transduce, into, comp")

  ;; Transducers are composable transformation pipelines that are INDEPENDENT of their
  ;; input/output source. Unlike (map f (filter g coll)) which creates intermediate lazy
  ;; sequences, transducers compose the transformations themselves — no intermediate allocations.
  ;; The same transducer works with sequences, channels (core.async), and reducibles.
  ;; When you call (filter even?) with ONE arg (no collection), it returns a transducer.
  (let [xf (comp
            (filter even?)
            (map #(* % %))
            (take 5))]

    ;; transduce applies the transducer xf while reducing with +.
    ;; into applies xf while pouring results into a target collection.
    ;; sequence lazily applies xf to produce a seq.
    (println "transduce:" (transduce xf + (range 1 100)))
    (println "into vec:" (into [] xf (range 1 100)))
    (println "into set:" (into #{} xf (range 1 100)))
    (println "sequence:" (sequence xf (range 1 100))))

  (let [xf (comp (map inc) (filter even?))]
    (println "transduce sum:" (transduce xf + 0 (range 10)))
    (println "transduce str:" (transduce xf str (range 5)))))

;; ============================================================
;;  8. MACROS
;; ============================================================
(defn macros-demo []
  (section "8. MACROS — defmacro, quote, syntax-quote")

  ;; Homoiconicity is why Lisp macros are so powerful. Clojure code IS data:
  ;; (+ 1 2) is a list containing the symbol +, the number 1, and the number 2.
  ;; quote (') prevents evaluation, returning the raw data structure.
  ;; syntax-quote (`) is like quote but resolves symbols to their fully-qualified names
  ;; and supports unquoting (~) to inject evaluated values.
  (println "quote:" '(1 2 3))
  (println "syntax-quote:" `(+ 1 2))

  ;; Macros receive unevaluated code (as data structures), transform it, and return new code.
  ;; The compiler evaluates the macro at COMPILE TIME, replacing the call with the returned form.
  ;; ~ (unquote) evaluates an expression within a syntax-quote.
  ;; ~@ (unquote-splicing) evaluates and splices a sequence into the surrounding form.
  (defmacro unless [condition & body]
    `(when (not ~condition)
       ~@body))

  (unless false
    (println "unless macro: condition was false, so this prints"))

  ;; Auto-gensym (result#) generates a unique symbol to prevent variable capture.
  ;; Without it, a macro's internal variable could shadow the caller's variable,
  ;; causing subtle bugs. This is called "hygiene" in macro systems.
  (defmacro dbg [expr]
    `(let [result# ~expr]
       (println (str "  dbg: " '~expr " => " result#))
       result#))

  (dbg (+ 1 2 3))
  (dbg (map inc [1 2 3]))

  ;; macroexpand shows the code a macro generates — essential for debugging macros.
  ;; You can see that (unless false (println "hi")) becomes (when (not false) (println "hi")).
  (println "macroexpand:" (macroexpand '(unless false (println "hi"))))

  ;; when-let* chains multiple conditional bindings — if any is nil/false, the whole
  ;; form returns nil. This is a recursive macro that expands into nested when-let forms.
  (defmacro when-let* [bindings & body]
    (if (seq bindings)
      `(when-let [~(first bindings) ~(second bindings)]
         (when-let* ~(drop 2 bindings) ~@body))
      `(do ~@body)))

  (when-let* [a (get {:x 1} :x)
              b (inc a)]
    (println "when-let* result:" b)))

;; ============================================================
;;  9. SPEC
;; ============================================================
(defn spec-demo []
  (section "9. SPEC — s/def, s/valid?, s/conform, s/fdef")

  ;; clojure.spec is Clojure's approach to validation and documentation.
  ;; Instead of static types, specs are composable predicates that describe data shapes.
  ;; Specs can be used for: validation, destructuring, generative testing, and documentation.
  ;; They're registered globally by namespaced keyword — ::name is :clojure-fundamentals/name.
  (s/def ::name (s/and string? #(> (count %) 0)))
  (s/def ::age (s/and int? #(>= % 0) #(<= % 150)))
  (s/def ::email (s/and string? #(re-matches #".+@.+\..+" %)))

  (println "valid? name:" (s/valid? ::name "Alice"))
  (println "valid? name:" (s/valid? ::name ""))
  (println "valid? age:" (s/valid? ::age 30))
  (println "valid? email:" (s/valid? ::email "a@b.com"))

  ;; s/keys specs for maps — :req-un means required keys (un-namespaced).
  ;; Each key's spec is looked up by its namespaced version, so ::name validates :name.
  ;; conform returns the conformed value (with tagged unions) or :clojure.spec.alpha/invalid.
  (s/def ::person (s/keys :req-un [::name ::age]
                          :opt-un [::email]))

  (println "valid? person:" (s/valid? ::person {:name "Alice" :age 30}))
  (println "conform:" (s/conform ::person {:name "Bob" :age 25 :email "b@c.com"}))

  ;; Collection specs describe the shape of collections — what elements they contain,
  ;; their kind (vector, list), and cardinality constraints.
  (s/def ::names (s/coll-of ::name :kind vector? :min-count 1))
  (println "valid? names:" (s/valid? ::names ["Alice" "Bob"]))

  ;; explain-str returns human-readable error messages describing why data doesn't conform.
  (println "explain-str:")
  (println " " (s/explain-str ::person {:name "" :age -1}))

  ;; s/or tags each alternative — conform returns the matched tag + value pair.
  ;; This is how you know WHICH branch matched, unlike union types in other languages.
  (s/def ::id (s/or :int int? :str string?))
  (println "conform or:" (s/conform ::id 42))
  (println "conform or:" (s/conform ::id "abc")))

;; ============================================================
;;  10. JAVA INTEROP
;; ============================================================
(defn java-interop-demo []
  (section "10. JAVA INTEROP — .method, Class/static, proxy")

  ;; Clojure runs on the JVM and has first-class Java interop — no FFI or wrappers needed.
  ;; .method calls instance methods, Class/field accesses statics, Class. constructs objects.
  ;; This gives Clojure access to the entire Java ecosystem without performance penalties.
  (println ".toUpperCase:" (.toUpperCase "hello"))
  (println ".substring:" (.substring "Hello, World!" 7))
  (println ".length:" (.length "hello"))

  ;; Static methods and fields use Class/member syntax.
  (println "Math/PI:" Math/PI)
  (println "Math/sqrt:" (Math/sqrt 144))
  (println "Integer/parseInt:" (Integer/parseInt "42"))
  (println "System/currentTimeMillis:" (System/currentTimeMillis))

  ;; Constructor calls use ClassName. (with trailing dot) syntax.
  (let [sb (StringBuilder. "Hello")]
    (.append sb ", ")
    (.append sb "World!")
    (println "StringBuilder:" (.toString sb)))

  (let [al (java.util.ArrayList.)]
    (.add al "one")
    (.add al "two")
    (.add al "three")
    (println "ArrayList:" al "size:" (.size al)))

  ;; doto is a macro that threads an object through multiple method calls and returns it.
  ;; It's like a builder pattern in one expression — saves repeating the variable name.
  (let [m (doto (java.util.HashMap.)
            (.put "a" 1)
            (.put "b" 2))]
    (println "doto HashMap:" m))

  ;; proxy creates a subclass or interface implementation at runtime.
  ;; It generates a JVM class that delegates to Clojure functions.
  (let [runnable (proxy [Runnable] []
                   (run [] (println "  proxy Runnable executed!")))]
    (.run runnable))

  ;; Type hints (^ClassName) tell the compiler the exact type, avoiding reflection.
  ;; Without hints, Clojure uses reflection for Java interop — slower at runtime.
  ;; Use *warn-on-reflection* to find unhinted interop calls in hot paths.
  (let [^String s "hello"]
    (println "Type-hinted:" (.charAt s 0))))

;; ============================================================
;;  MAIN
;; ============================================================
(defn -main [& _args]
  (println (str "Clojure " (clojure-version) " Fundamentals"))
  (println (apply str (repeat 60 "=")))

  (basics)
  (data-structures)
  (functions-demo)
  (sequences-demo)
  (polymorphism-demo)
  (concurrency-demo)
  (transducers-demo)
  (macros-demo)
  (spec-demo)
  (java-interop-demo)

  (println (str "\n" (apply str (repeat 60 "="))))
  (println "  All sections complete!")
  (println (apply str (repeat 60 "="))))

(-main)
