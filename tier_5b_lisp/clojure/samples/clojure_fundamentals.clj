(ns clojure-fundamentals
  "Clojure Fundamentals: Beginner to Advanced — Standard Library Only.

   A dense, runnable syntax reference covering core Clojure concepts.
   Run: clj -M clojure_fundamentals.clj
        or: clojure clojure_fundamentals.clj
   Requires: Clojure 1.11+"
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

  ;; --- Literals ---
  (println "Integer:" 42 " Long:" 9999999999 " BigInt:" 42N)
  (println "Float:" 3.14 " Ratio:" (/ 22 7) " BigDecimal:" 3.14M)
  (println "String:" "hello" " Char:" \a " Boolean:" true " Nil:" nil)

  ;; --- Keywords & symbols ---
  (println "Keyword:" :name " Namespaced:" ::local)
  (println "Keyword as fn:" (:name {:name "Alice" :age 30}))

  ;; --- def & let ---
  (def pi 3.14159)
  (let [x 10
        y 20
        sum (+ x y)]
    (println "let binding: x=" x "y=" y "sum=" sum))

  ;; --- Strings ---
  (println "str concat:" (str "Hello" ", " "World!"))
  (println "format:" (format "Pi is %.4f" pi))
  (println "split:" (str/split "a,b,c" #","))
  (println "join:" (str/join "-" ["hello" "world"]))
  (println "upper:" (str/upper-case "hello"))
  (println "includes?:" (str/includes? "hello world" "world"))

  ;; --- Regex ---
  (println "re-find:" (re-find #"\d+" "abc 123 def"))
  (println "re-seq:" (re-seq #"\w+" "hello world 42"))
  (println "re-matches:" (re-matches #"(\d{4})-(\d{2})" "2024-01")))

;; ============================================================
;;  2. DATA STRUCTURES
;; ============================================================
(defn data-structures []
  (section "2. DATA STRUCTURES — Lists, Vectors, Maps, Sets")

  ;; --- Lists (linked, prepend-optimized) ---
  (let [lst '(1 2 3 4 5)]
    (println "List:" lst "first:" (first lst) "rest:" (rest lst))
    (println "conj (prepend):" (conj lst 0))
    (println "cons:" (cons 0 lst)))

  ;; --- Vectors (indexed, append-optimized) ---
  (let [v [10 20 30 40 50]]
    (println "Vector:" v "nth:" (nth v 2) "get:" (get v 1))
    (println "conj (append):" (conj v 60))
    (println "assoc:" (assoc v 2 99))
    (println "subvec:" (subvec v 1 4))
    (println "peek:" (peek v) "pop:" (pop v)))

  ;; --- Maps ---
  (let [m {:name "Clojure" :year 2007 :creator "Rich Hickey"}]
    (println "Map:" m)
    (println "get:" (get m :name) "keyword-as-fn:" (:year m))
    (println "assoc:" (assoc m :version "1.11"))
    (println "dissoc:" (dissoc m :year))
    (println "merge:" (merge m {:paradigm "FP"}))
    (println "select-keys:" (select-keys m [:name :year]))
    (println "update:" (update m :year inc)))

  ;; Nested access
  (let [nested {:user {:address {:city "Portland"}}}]
    (println "get-in:" (get-in nested [:user :address :city]))
    (println "assoc-in:" (assoc-in nested [:user :address :zip] "97201"))
    (println "update-in:" (update-in nested [:user :address :city] str/upper-case)))

  ;; --- Sets ---
  (let [s1 #{1 2 3 4}
        s2 #{3 4 5 6}]
    (println "Set:" s1 "contains?:" (contains? s1 3))
    (println "union:" (cset/union s1 s2))
    (println "intersection:" (cset/intersection s1 s2))
    (println "difference:" (cset/difference s1 s2))
    (println "conj:" (conj s1 5) "disj:" (disj s1 2)))

  ;; --- Persistence demo ---
  (let [v1 [1 2 3]
        v2 (conj v1 4)]
    (println "Persistent: v1=" v1 "v2=" v2 "(v1 unchanged)")))

;; ============================================================
;;  3. FUNCTIONS
;; ============================================================
(defn functions-demo []
  (section "3. FUNCTIONS — defn, Anonymous, Partial, Comp, Threading")

  ;; --- defn with multiple arities ---
  (defn greet
    ([name] (greet name "Hello"))
    ([name greeting] (str greeting ", " name "!")))
  (println "Multi-arity:" (greet "Alice") (greet "Bob" "Hey"))

  ;; --- Anonymous functions ---
  (let [square (fn [x] (* x x))
        cube #(* %1 %1 %1)]
    (println "Anonymous fn:" (square 5) "Reader macro:" (cube 3)))

  ;; --- Higher-order ---
  (println "apply:" (apply + [1 2 3 4 5]))
  (println "map:" (map inc [1 2 3]))
  (println "filter:" (filter even? (range 1 11)))
  (println "remove:" (remove even? (range 1 11)))

  ;; --- partial, comp, juxt ---
  (let [add10 (partial + 10)
        double-then-inc (comp inc #(* 2 %))
        stats (juxt count #(apply min %) #(apply max %))]
    (println "partial:" (add10 5))
    (println "comp:" (double-then-inc 5))
    (println "juxt:" (stats [3 1 4 1 5 9])))

  ;; --- Threading macros ---
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

  (let [nums (range 1 11)]
    (println "map:"         (map #(* % 2) nums))
    (println "mapcat:"      (mapcat #(vector % (* % 10)) [1 2 3]))
    (println "frequencies:" (frequencies [:a :b :a :c :b :a]))
    (println "group-by:"    (group-by #(mod % 3) nums))
    (println "partition:"   (partition 3 nums))
    (println "partition-by:" (partition-by #(< % 5) nums))
    (println "take:"        (take 5 (range)))
    (println "drop:"        (drop 7 nums))
    (println "take-while:"  (take-while #(< % 5) nums))
    (println "interleave:"  (interleave [:a :b :c] [1 2 3]))
    (println "interpose:"   (interpose ", " ["a" "b" "c"]))
    (println "zipmap:"      (zipmap [:a :b :c] [1 2 3]))
    (println "into:"        (into {} [[:a 1] [:b 2] [:c 3]]))
    (println "distinct:"    (distinct [1 1 2 3 3 2 4]))
    (println "sort-by:"     (sort-by count ["banana" "fig" "apple"]))))

;; ============================================================
;;  5. POLYMORPHISM
;; ============================================================
(defn polymorphism-demo []
  (section "5. POLYMORPHISM — Multimethods, Protocols, Records")

  ;; --- Multimethods ---
  (defmulti area :shape)
  (defmethod area :circle [{:keys [radius]}]
    (* Math/PI radius radius))
  (defmethod area :rectangle [{:keys [width height]}]
    (* width height))
  (defmethod area :default [shape]
    (str "Unknown shape: " (:shape shape)))

  (println "Circle area:" (format "%.2f" (area {:shape :circle :radius 5})))
  (println "Rect area:" (area {:shape :rectangle :width 4 :height 6}))

  ;; --- Protocols ---
  (defprotocol Describable
    (describe [this] "Return a description"))

  (defrecord Dog [name breed]
    Describable
    (describe [_] (str name " the " breed " dog")))

  (defrecord Cat [name indoor?]
    Describable
    (describe [_] (str name " the " (if indoor? "indoor" "outdoor") " cat")))

  (println "Protocol:" (describe (->Dog "Rex" "Lab")))
  (println "Protocol:" (describe (->Cat "Whiskers" true)))

  ;; --- Records ---
  (let [d (->Dog "Buddy" "Beagle")
        d2 (assoc d :age 5)]
    (println "Record:" d "name:" (:name d))
    (println "assoc'd:" d2))

  ;; --- reify ---
  (let [obj (reify Describable
              (describe [_] "I'm a reified object"))]
    (println "reify:" (describe obj))))

;; ============================================================
;;  6. CONCURRENCY
;; ============================================================
(defn concurrency-demo []
  (section "6. CONCURRENCY — Atom, Ref, Agent, Future, Promise")

  ;; --- Atom (uncoordinated, synchronous) ---
  (let [counter (atom 0)]
    (swap! counter inc)
    (swap! counter inc)
    (swap! counter + 10)
    (println "Atom:" @counter)
    (reset! counter 0)
    (println "After reset:" @counter))

  ;; --- Atom with validator ---
  (let [age (atom 25 :validator #(and (integer? %) (>= % 0)))]
    (swap! age inc)
    (println "Validated atom:" @age)
    (try
      (reset! age -1)
      (catch Exception e
        (println "Validator rejected:" (.getMessage e)))))

  ;; --- Ref (coordinated, synchronous via STM) ---
  (let [account-a (ref 1000)
        account-b (ref 500)]
    (dosync
     (alter account-a - 200)
     (alter account-b + 200))
    (println "Refs after transfer: A=" @account-a "B=" @account-b))

  ;; --- Agent (uncoordinated, asynchronous) ---
  (let [log-agent (agent [])]
    (send log-agent conj "message 1")
    (send log-agent conj "message 2")
    (await log-agent)
    (println "Agent:" @log-agent))

  ;; --- Future ---
  (let [f (future (Thread/sleep 10) (* 6 7))]
    (println "Future:" @f "realized?:" (realized? f)))

  ;; --- Promise ---
  (let [p (promise)]
    (future (Thread/sleep 10) (deliver p 42))
    (println "Promise:" @p "realized?:" (realized? p))))

;; ============================================================
;;  7. TRANSDUCERS
;; ============================================================
(defn transducers-demo []
  (section "7. TRANSDUCERS — transduce, into, comp")

  ;; Transducers compose transformations without creating intermediate sequences
  (let [xf (comp
            (filter even?)
            (map #(* % %))
            (take 5))]

    (println "transduce:" (transduce xf + (range 1 100)))
    (println "into vec:" (into [] xf (range 1 100)))
    (println "into set:" (into #{} xf (range 1 100)))
    (println "sequence:" (sequence xf (range 1 100))))

  ;; Transducer with completing function
  (let [xf (comp (map inc) (filter even?))]
    (println "transduce sum:" (transduce xf + 0 (range 10)))
    (println "transduce str:" (transduce xf str (range 5)))))

;; ============================================================
;;  8. MACROS
;; ============================================================
(defn macros-demo []
  (section "8. MACROS — defmacro, quote, syntax-quote")

  ;; --- Quote ---
  (println "quote:" '(1 2 3))
  (println "syntax-quote:" `(+ 1 2))

  ;; --- Simple macro ---
  (defmacro unless [condition & body]
    `(when (not ~condition)
       ~@body))

  (unless false
    (println "unless macro: condition was false, so this prints"))

  ;; --- Debug macro ---
  (defmacro dbg [expr]
    `(let [result# ~expr]
       (println (str "  dbg: " '~expr " => " result#))
       result#))

  (dbg (+ 1 2 3))
  (dbg (map inc [1 2 3]))

  ;; --- macroexpand ---
  (println "macroexpand:" (macroexpand '(unless false (println "hi"))))

  ;; --- Anaphoric macro ---
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

  ;; --- Basic specs ---
  (s/def ::name (s/and string? #(> (count %) 0)))
  (s/def ::age (s/and int? #(>= % 0) #(<= % 150)))
  (s/def ::email (s/and string? #(re-matches #".+@.+\..+" %)))

  (println "valid? name:" (s/valid? ::name "Alice"))
  (println "valid? name:" (s/valid? ::name ""))
  (println "valid? age:" (s/valid? ::age 30))
  (println "valid? email:" (s/valid? ::email "a@b.com"))

  ;; --- Composite specs ---
  (s/def ::person (s/keys :req-un [::name ::age]
                          :opt-un [::email]))

  (println "valid? person:" (s/valid? ::person {:name "Alice" :age 30}))
  (println "conform:" (s/conform ::person {:name "Bob" :age 25 :email "b@c.com"}))

  ;; --- Collection specs ---
  (s/def ::names (s/coll-of ::name :kind vector? :min-count 1))
  (println "valid? names:" (s/valid? ::names ["Alice" "Bob"]))

  ;; --- explain ---
  (println "explain-str:")
  (println " " (s/explain-str ::person {:name "" :age -1}))

  ;; --- s/or ---
  (s/def ::id (s/or :int int? :str string?))
  (println "conform or:" (s/conform ::id 42))
  (println "conform or:" (s/conform ::id "abc")))

;; ============================================================
;;  10. JAVA INTEROP
;; ============================================================
(defn java-interop-demo []
  (section "10. JAVA INTEROP — .method, Class/static, proxy")

  ;; --- Instance methods ---
  (println ".toUpperCase:" (.toUpperCase "hello"))
  (println ".substring:" (.substring "Hello, World!" 7))
  (println ".length:" (.length "hello"))

  ;; --- Static methods & fields ---
  (println "Math/PI:" Math/PI)
  (println "Math/sqrt:" (Math/sqrt 144))
  (println "Integer/parseInt:" (Integer/parseInt "42"))
  (println "System/currentTimeMillis:" (System/currentTimeMillis))

  ;; --- Constructing Java objects ---
  (let [sb (StringBuilder. "Hello")]
    (.append sb ", ")
    (.append sb "World!")
    (println "StringBuilder:" (.toString sb)))

  (let [al (java.util.ArrayList.)]
    (.add al "one")
    (.add al "two")
    (.add al "three")
    (println "ArrayList:" al "size:" (.size al)))

  ;; --- doto ---
  (let [m (doto (java.util.HashMap.)
            (.put "a" 1)
            (.put "b" 2))]
    (println "doto HashMap:" m))

  ;; --- proxy ---
  (let [runnable (proxy [Runnable] []
                   (run [] (println "  proxy Runnable executed!")))]
    (.run runnable))

  ;; --- Type hints for performance ---
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
