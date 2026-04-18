# Learning Resources — The 16 Sprint Languages

> **Purpose:** A vetted, curated reference of official docs, interactive tutorials, books, playgrounds, and deep-dive resources for every language in the 15-week sprint.
> **Philosophy:** Start with the official materials. They are almost always the best starting point. Supplement with interactive practice. Reach for books only for depth you can't get elsewhere. Playgrounds are for testing hypotheses, not for learning.
> **Meta-rule:** Each language tier has one "primary path" — the recommended sequence. Everything else is supplementary. Don't paradox-of-choice yourself.

---

## How to Use This Document

For each language below, you'll find:

- **Official docs** — the canonical source of truth. Bookmark these.
- **Interactive primary path** — the one sequence I'd have you follow if you only did one thing.
- **Playground** — in-browser REPL for quick experiments (useful when away from your machine).
- **Book** — optional depth. Recommended for languages you're going deep on (Rust, Java, Elixir, Clojure, F#).
- **Cheat sheet / reference** — fast lookup for syntax you forget.
- **Community** — where to ask questions when stuck.

**The sprint's knowledge acquisition rule:** You're not trying to "learn" each of these languages to native fluency. You're trying to *translate* from Python (your anchor) into each one, see the patterns compound, and build one small thing. Resources are ordered accordingly.

---

# Anchor Language

## Python (Tier 0 — Reference Anchor)

You already know this. Listed for completeness since it's the daily anchor.

- **Docs:** [docs.python.org](https://docs.python.org/3/) · [FastAPI docs](https://fastapi.tiangolo.com/) · [Pydantic](https://docs.pydantic.dev/)
- **Playground:** [try.jupyter.org](https://jupyter.org/try) · [Replit Python](https://replit.com/languages/python3) · local `python -i` or `ipython`
- **Cheat sheet:** [PEP 8 style guide](https://peps.python.org/pep-0008/)

---

# Tier 1 — Systems (Rust + C++)

## Rust — PRIMARY LANGUAGE FOR WEEK 1-2

Rust is the language you're starting with on Monday. The depth and quality of Rust learning resources is extraordinary; if anything the problem is too much choice. Follow this path precisely:

- **Official docs:** [doc.rust-lang.org](https://doc.rust-lang.org/) — the hub linking to everything below
- **The Rust Book:** [doc.rust-lang.org/book](https://doc.rust-lang.org/book/) — "the Book." Canonical. Read chapters 1-10 before Monday if time permits.
  - Alternative with better diagrams: [Brown University Rust Book](https://rust-book.cs.brown.edu/) — interactive quizzes embedded; superior for self-study
- **Rust by Example:** [doc.rust-lang.org/rust-by-example](https://doc.rust-lang.org/rust-by-example/) — code-first companion to the Book
- **Rustlings:** [github.com/rust-lang/rustlings](https://github.com/rust-lang/rustlings) — small exercises; the recommended hands-on. Install with `cargo install rustlings && rustlings init`

### **Primary interactive path (most recommended):**
**[100 Exercises To Learn Rust](https://rust-exercises.com/100-exercises/)** by Luca Palmieri — builds a project-management system one concept at a time. This is the best modern Rust course. You can work in-browser, or clone locally. Available also as a [free PDF](https://rust-exercises.com/100-exercises-to-learn-rust.pdf) and as a [JetBrains RustRover integrated course](https://academy.jetbrains.com/course/27805-100-exercises-to-learn-rust).

- **Playground:** [play.rust-lang.org](https://play.rust-lang.org) — the official playground; supports top 100 crates, rustfmt, clippy, and LLVM IR / assembly view
- **Alternative playground:** [rustfinity.com/playground](https://www.rustfinity.com/playground) — more modern UI with progressive exercises

### **For depth (pick one, read during Weeks 1-2 deep-work blocks):**
- **"Rust for Rustaceans"** by Jon Gjengset — the post-Book book; assumes you know basic Rust and pushes into idiomatic use. Pair with Gjengset's [Crust of Rust YouTube series](https://www.youtube.com/playlist?list=PLqbS7AVVErFiWDOAVrPt7aYmnuuOLYvOa).
- **"Zero to Production in Rust"** by Luca Palmieri — full web-service build (API, database, observability, deployment). Directly applicable to Sauti.
- **"Rust Atomics and Locks"** by Mara Bos — concurrency, memory ordering; necessary reading when Sauti's transcription workers start scaling. Free online: [marabos.nl/atomics](https://marabos.nl/atomics/).

### **Deep/advanced:**
- **[The Rustonomicon](https://doc.rust-lang.org/nomicon/)** — unsafe Rust. Only when you need it.
- **[Effective Rust](https://www.lurklurk.org/effective-rust/)** by David Drysdale — 35 items of best practice, free online
- **[Comprehensive Rust](https://google.github.io/comprehensive-rust/)** — Google's internal course, public. Good for fast exposure.

### **Community:**
- [users.rust-lang.org](https://users.rust-lang.org) — the friendliest beginner forum on the internet, frankly
- [r/rust](https://reddit.com/r/rust)
- [This Week in Rust](https://this-week-in-rust.org/) — weekly newsletter

### **Sprint recommendation for Rust:**
Thu-Sun: Read Brown Rust Book chapters 1-4 (ownership, borrowing). Do 10-20 Rustlings. Skim 100 Exercises table of contents.
Monday onward: `cargo new sauti` and start writing. Reach for the Book only when blocked.

---

## C++ (Modern C++20/23)

C++ resources are more fragmented than Rust's. Stick to the modern (C++17+) era; ignore everything from the pre-C++11 era unless you have a specific reason.

- **Official-ish hub:** [isocpp.org](https://isocpp.org/get-started) — the C++ standards committee's starter page
- **Canonical reference:** [cppreference.com](https://en.cppreference.com/) — bookmark. This is the MDN-equivalent for C++.
- **Interactive tutorial:** [learncpp.com](https://www.learncpp.com/) — the single best free online C++ tutorial; modern, opinionated, well-maintained
- **Playground:** [godbolt.org](https://godbolt.org) (Compiler Explorer) — essential for C++, shows you the assembly output. Use it daily.
- **Alternative playground:** [quick-bench.com](https://quick-bench.com/) — for micro-benchmarking
- **Book (if going deep):**
  - **"A Tour of C++"** (3rd ed) by Bjarne Stroustrup — concise overview by the creator. 300 pages.
  - **"C++ Crash Course"** by Josh Lospinoso — pragmatic, modern
  - **"Effective Modern C++"** by Scott Meyers — required reading for idiomatic C++11/14
- **Guidelines:** [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) — Stroustrup + Sutter; what "good C++" looks like today
- **Build tool:** CMake — learn via [Modern CMake](https://cliutils.gitlab.io/modern-cmake/)

### **Sprint recommendation for C++:**
You don't need to learn C++ before writing it. You'll use it for Sauti's DSP pipeline (FFT, MFCC, VAD). Start with learncpp.com chapters 1-8 for syntax fluency, then dive into a real DSP library (KissFFT, or Eigen). Let the task drive the learning.

---

# Tier 2 — JVM Enterprise (Java + Kotlin + Scala)

## Java 21+

The "official docs" for Java are extraordinarily deep but not beginner-friendly. Use the tutorial + a modern intro book, not the JLS.

- **Official docs (reference):** [dev.java](https://dev.java/) — Oracle's newer official site, replacing the old tutorials
- **Modern Java tutorial:** [dev.java/learn](https://dev.java/learn/) — organized by concept; reflects Java 17+ features
- **Spring Boot docs:** [spring.io/guides](https://spring.io/guides) — the "Building a RESTful Web Service" guide is where most devs start
- **Axon Framework docs:** [docs.axoniq.io](https://docs.axoniq.io/) — for CQRS/ES work in LendStream v2
- **Playground:** [onecompiler.com/java](https://onecompiler.com/java) · [JDoodle](https://www.jdoodle.com/online-java-compiler) · or IntelliJ IDEA Community (free)
- **Book:**
  - **"Modern Java in Action"** by Raoul-Gabriel Urma — covers streams, lambdas, modules
  - **"Effective Java"** (3rd ed) by Joshua Bloch — still the canonical idiomatic Java reference
- **Virtual threads (Java 21 feature, big deal for LendStream):** [openjdk.org/jeps/444](https://openjdk.org/jeps/444)

### **Sprint recommendation for Java:**
You've used Java before (Veracode, RGA). Treat Weeks 3-4 as a refresher focused on the modern features (virtual threads, records, sealed classes, pattern matching). The Spring Boot + Axon stack is where you'll spend time.

---

## Kotlin

Kotlin has some of the best official learning material of any language.

- **Official docs:** [kotlinlang.org](https://kotlinlang.org/docs/home.html)
- **Kotlin Tour:** [kotlinlang.org/docs/kotlin-tour-welcome.html](https://kotlinlang.org/docs/kotlin-tour-welcome.html) — the official interactive tour
- **Kotlin Koans:** [play.kotlinlang.org/koans](https://play.kotlinlang.org/koans) — the canonical exercise series, in-browser
- **Playground:** [play.kotlinlang.org](https://play.kotlinlang.org) — official
- **Ktor (for LendStream projections/BFFs):** [ktor.io/docs](https://ktor.io/docs)
- **Coroutines deep dive:** [kotlinlang.org/docs/coroutines-guide.html](https://kotlinlang.org/docs/coroutines-guide.html) — required reading for LendStream's read-side work
- **Book:** **"Kotlin in Action"** (2nd ed) by Roman Elizarov et al — worth it

### **Sprint recommendation for Kotlin:**
Kotlin Tour → Kotlin Koans → then just start writing LendStream projections. Coroutines understanding is essential; budget a dedicated session for the coroutines guide.

---

## Scala 3

- **Official docs:** [docs.scala-lang.org](https://docs.scala-lang.org/)
- **Tour of Scala:** [docs.scala-lang.org/tour](https://docs.scala-lang.org/tour/tour-of-scala.html) — official, concept-at-a-time
- **Scala 3 Book:** [docs.scala-lang.org/scala3/book](https://docs.scala-lang.org/scala3/book/introduction.html) — free, official
- **Playground:** [scastie.scala-lang.org](https://scastie.scala-lang.org) — by the Scala Center. Supports Scala 3, Scala.js, Scala Native, library imports. The gold standard of Scala playgrounds.
- **Scala Exercises:** [scala-exercises.org](https://www.scala-exercises.org/) — in-browser practice organized by library (cats, scalaz, stdlib)
- **Exercism Scala track:** [exercism.org/tracks/scala](https://exercism.org/tracks/scala)
- **cats-effect (for LendStream sagas):** [typelevel.org/cats-effect](https://typelevel.org/cats-effect/)
- **ZIO (alternative for sagas):** [zio.dev](https://zio.dev)
- **Book (highly recommended if going deep on FP):**
  - **"Functional Programming in Scala"** (2nd ed, "The Red Book") by Chiusano & Bjarnason — will genuinely change how you think about types
  - **"Programming in Scala"** (5th ed) by Odersky — by the language creator

### **Sprint recommendation for Scala:**
Saga orchestration is what you need Scala for — not full-stack Scala. Focus on cats-effect or ZIO's effect system; the ADT-based state machines for sagas are the target.

---

# Tier 3 — Web (JavaScript + TypeScript)

## JavaScript (Modern, ES2024+)

- **Canonical reference:** [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript) — the definitive JS reference
- **Modern tutorial:** [javascript.info](https://javascript.info/) — comprehensive, well-paced, free
- **Playground:** Browser devtools console (F12) — fastest available · [jsfiddle.net](https://jsfiddle.net) · [codesandbox.io](https://codesandbox.io) for full projects
- **Node.js docs:** [nodejs.org/docs](https://nodejs.org/docs/latest/api/)
- **Book:**
  - **"You Don't Know JS Yet"** (Kyle Simpson) — free on GitHub: [github.com/getify/You-Dont-Know-JS](https://github.com/getify/You-Dont-Know-JS)
  - **"Eloquent JavaScript"** (Marijn Haverbeke) — free online: [eloquentjavascript.net](https://eloquentjavascript.net/)

## TypeScript

- **Official docs:** [typescriptlang.org/docs](https://www.typescriptlang.org/docs/)
- **TS Handbook:** [typescriptlang.org/docs/handbook](https://www.typescriptlang.org/docs/handbook/intro.html) — THE starting point
- **Playground:** [typescriptlang.org/play](https://www.typescriptlang.org/play) — official. Shows compiled JS output. Excellent.
- **Type Challenges:** [github.com/type-challenges/type-challenges](https://github.com/type-challenges/type-challenges) — puzzles for type-system mastery
- **Total TypeScript:** [totaltypescript.com](https://www.totaltypescript.com/) — Matt Pocock's tutorials; exceptional for deep TS
- **Yjs (for Sherehe CRDTs):** [docs.yjs.dev](https://docs.yjs.dev)
- **Next.js docs:** [nextjs.org/docs](https://nextjs.org/docs)

### **Sprint recommendation for JS/TS:**
You already know this well. Weeks 5-6 should focus on Yjs/CRDT mastery and offline-first PWA patterns. Budget deep time on the Yjs docs; they're shorter than you'd think.

---

# Tier 4 — Cloud Native (Go + Zig)

## Go

Go's docs are famously concise and excellent.

- **Official docs:** [go.dev/doc](https://go.dev/doc/)
- **A Tour of Go:** [go.dev/tour](https://go.dev/tour/) — interactive, in-browser, covers the whole language in ~2 hours
- **Effective Go:** [go.dev/doc/effective_go](https://go.dev/doc/effective_go) — written by the Go team; idiomatic patterns
- **Go by Example:** [gobyexample.com](https://gobyexample.com/) — pattern-matched examples; my go-to for "how do I do X in Go"
- **Playground:** [go.dev/play](https://go.dev/play) — official
- **Exercism Go track:** [exercism.org/tracks/go](https://exercism.org/tracks/go)
- **Book:**
  - **"The Go Programming Language"** by Donovan & Kernighan (yes, that Kernighan) — still the best
  - **"Learning Go"** by Jon Bodner — more modern, covers newer features
- **Concurrency patterns:** [go.dev/doc/effective_go#concurrency](https://go.dev/doc/effective_go#concurrency) + [Ardan Labs blog](https://www.ardanlabs.com/blog/)

### **Sprint recommendation for Go:**
Do Tour of Go in full (2 hours, seriously). Then start writing Unicorns v2 hexagonal cores. Pattern-match from Go by Example when stuck.

## Zig

Zig is still pre-1.0 (currently around 0.14/0.15), so resources are thinner but the official ones are excellent.

- **Official docs:** [ziglang.org/documentation](https://ziglang.org/documentation/master/) — reference doc
- **Official learn page:** [ziglang.org/learn](https://ziglang.org/learn/)
- **Zig Guide (comprehensive):** [zig.guide](https://zig.guide) — the closest Zig has to a "Book"
- **Ziglings:** [codeberg.org/ziglings/exercises](https://codeberg.org/ziglings/exercises) — fix tiny broken programs (Rustlings-inspired). This is your primary practice path.
- **Zig by Example:** [zig-by-example.com](https://zig-by-example.com/)
- **Learning Zig (for GC-language devs):** [openmymind.net/learning_zig](https://www.openmymind.net/learning_zig/) — excellent for Python/JS devs
- **Playground:** [zig-play.dev](https://zig-play.dev) — online editor with snippet sharing
- **Exercism Zig track:** [exercism.org/tracks/zig](https://exercism.org/tracks/zig)
- **Community:** [Zig Showtime YouTube](https://www.youtube.com/@ZigSHOWTIME), Ziggit forum

### **Sprint recommendation for Zig:**
Do Ziglings exercises 1-40 during Week 7 evenings. Then write one Zig performance adapter for Unicorns v2 (search index or image thumbnailer). Don't try to build entire services in Zig — it's a surgical tool in this tier.

---

# Tier 5a — Web Framework Trinity (Ruby + PHP + Elixir)

## Ruby + Rails

- **Official Ruby docs:** [ruby-doc.org](https://ruby-doc.org/) · [ruby-lang.org](https://www.ruby-lang.org/en/documentation/)
- **Ruby tutorial (in-browser):** [try.ruby-lang.org](https://try.ruby-lang.org/) — official
- **Rails Guides:** [guides.rubyonrails.org](https://guides.rubyonrails.org/) — the canonical Rails docs; exceptionally well-written
- **Playground:** [replit.com/languages/ruby](https://replit.com/languages/ruby) · local `irb`
- **Ruby Koans:** [github.com/edgecase/ruby_koans](http://rubykoans.com/) — learn by making failing tests pass
- **Exercism Ruby:** [exercism.org/tracks/ruby](https://exercism.org/tracks/ruby)
- **Book:**
  - **"The Well-Grounded Rubyist"** (3rd ed) by David Black — best modern Ruby intro
  - **"Agile Web Development with Rails 7"** by David Heinemeier Hansson et al — the Rails canonical text

## PHP + Laravel

- **Official PHP docs:** [php.net/docs.php](https://www.php.net/docs.php) — reference, not tutorial
- **Modern PHP tutorial:** [phptherightway.com](https://phptherightway.com/) — this is what you should read first to avoid legacy PHP patterns
- **Laravel docs:** [laravel.com/docs](https://laravel.com/docs) — outstanding; one of the best framework docs in any ecosystem
- **Laracasts:** [laracasts.com](https://laracasts.com/) — video tutorials, partially free. "Laravel From Scratch" series is the standard first path.
- **Playground:** [onlinephp.io](https://onlinephp.io/) · [phpsandbox.io](https://phpsandbox.io/)
- **Exercism PHP:** [exercism.org/tracks/php](https://exercism.org/tracks/php)

## Elixir + Phoenix + LiveView

- **Official docs:** [elixir-lang.org](https://elixir-lang.org/) · [hexdocs.pm/elixir](https://hexdocs.pm/elixir/introduction.html)
- **Getting Started guide:** [hexdocs.pm/elixir/introduction.html](https://hexdocs.pm/elixir/introduction.html) — the official tutorial
- **Mix and OTP guide:** [hexdocs.pm/elixir/introduction-to-mix.html](https://hexdocs.pm/elixir/introduction-to-mix.html) — THE resource for learning OTP (which is what you need for Shamba)
- **Phoenix docs:** [hexdocs.pm/phoenix](https://hexdocs.pm/phoenix/overview.html)
- **Phoenix LiveView docs:** [hexdocs.pm/phoenix_live_view](https://hexdocs.pm/phoenix_live_view/welcome.html)
- **Playground / Interactive:** **[Livebook](https://livebook.dev)** — by José Valim (Elixir creator); Jupyter-for-Elixir with real OTP support. Exceptional learning tool. Install locally; it's first-class.
- **Exercism Elixir:** [exercism.org/tracks/elixir](https://exercism.org/tracks/elixir)
- **Book (highly recommended):**
  - **"Programming Elixir ≥ 1.6"** by Dave Thomas — the standard intro
  - **"Programming Phoenix LiveView"** by Bruce Tate & Sophie DeBenedetto — for Shamba's LiveView work
  - **"Designing Elixir Systems with OTP"** by Bruce Tate — essential for OTP depth
- **Community:** [elixirforum.com](https://elixirforum.com) — very beginner-friendly

### **Sprint recommendation for Tier 5a:**
You're combining three languages but the common thread is "web frameworks with increasing philosophical sophistication." Don't try to master Rails or Laravel from scratch — focus on Elixir + OTP + Phoenix deeply (it's the architecture teacher), and use Rails/Laravel as "this is what the back-office/public site is built in, written at idiomatic competence." Livebook will be your daily Elixir learning environment.

---

# Tier 5b — Functional Deep (Clojure)

Clojure is ~where functional programming meets Lisp meets the JVM. Resources are high-quality but fewer than mainstream languages.

- **Official docs:** [clojure.org](https://clojure.org/) · [clojure.org/guides/getting_started](https://clojure.org/guides/getting_started)
- **ClojureDocs:** [clojuredocs.org](https://clojuredocs.org) — community-enhanced function reference with examples. Bookmark immediately.
- **Brave Clojure (the book, free online):** [braveclojure.com](https://www.braveclojure.com/) — "Clojure for the Brave and True" by Daniel Higginbotham. The recommended starting point. Funny, thorough, pragmatic.
- **Playground:**
  - **[Try Clojure](https://tryclojure.org/)** — quick in-browser REPL, good for first minutes
  - **[Replit Clojure](https://replit.com/languages/clojure)** — full environment
  - Local: `clj` (install Clojure CLI tools)
- **Interactive practice:**
  - **[4ever-clojure](https://4clojure.oxal.org/)** — the reborn 4clojure, 156 problems from easy to elder. Your main practice path.
  - **[Rich 4Clojure](https://github.com/PEZ/rich4clojure)** — same problems but in a real editor with REPL-driven development. Better if you want to practice the actual workflow.
  - **[Exercism Clojure track](https://exercism.org/tracks/clojure)** — 105 exercises with mentorship option
- **Editor:** VS Code + **Calva** extension ([calva.io](https://calva.io)) — REPL integration, debugger, inline evaluation. Or Emacs + CIDER if you're in that tribe.
- **Book (for going deep, recommended for the sprint):**
  - **"Clojure Applied"** by Ben Vandgrift — idiomatic patterns at the architecture level
  - **"The Joy of Clojure"** (2nd ed) by Fogus & Houser — the advanced-thinking book
- **Functional Core / Imperative Shell (primary pattern for BSD Engine v2):** Gary Bernhardt's [Boundaries talk](https://www.destroyallsoftware.com/talks/boundaries) — originally about Ruby but exports fully to Clojure
- **Community:** [Clojurians Slack](https://clojurians.slack.com) — #beginners channel is exceptionally welcoming · [ask.clojure.org](https://ask.clojure.org)

### **Sprint recommendation for Clojure:**
Install VS Code + Calva immediately (Weeks 1-2 setup period). Do the Calva get-started guide end to end — REPL-driven development is THE Clojure skill. Then work through Brave Clojure chapters 1-8 during Weeks 9-10 evenings. Rich 4Clojure problems during the Tier 5b deep-work blocks. The DSL-authoring work in BSD Engine v2 is where Clojure's macros shine.

---

# Tier 6 — .NET Capstone (C# + F#)

## C# 12 + .NET 8

- **Official docs:** [learn.microsoft.com/en-us/dotnet/csharp](https://learn.microsoft.com/en-us/dotnet/csharp/) — Microsoft's learning portal. Well-organized.
- **C# tutorial:** [learn.microsoft.com/en-us/dotnet/csharp/tour-of-csharp](https://learn.microsoft.com/en-us/dotnet/csharp/tour-of-csharp/) — the Tour
- **ASP.NET Core docs:** [learn.microsoft.com/en-us/aspnet/core](https://learn.microsoft.com/en-us/aspnet/core/)
- **Orleans (actor model for device fleet in PayGoHub):** [learn.microsoft.com/en-us/dotnet/orleans](https://learn.microsoft.com/en-us/dotnet/orleans/overview)
- **Playground:** [dotnetfiddle.net](https://dotnetfiddle.net/) · [sharplab.io](https://sharplab.io/) — shows IL output; excellent for understanding compilation
- **Exercism C#:** [exercism.org/tracks/csharp](https://exercism.org/tracks/csharp)
- **Book:**
  - **"C# 12 in a Nutshell"** by Joseph & Ben Albahari — encyclopedic reference, trust it
  - **"Dependency Injection Principles, Practices, and Patterns"** by Seemann & van Deursen — architectural depth for DDD work

## F# 8

- **Official docs:** [learn.microsoft.com/en-us/dotnet/fsharp](https://learn.microsoft.com/en-us/dotnet/fsharp/)
- **F# tour:** [learn.microsoft.com/en-us/dotnet/fsharp/tour](https://learn.microsoft.com/en-us/dotnet/fsharp/tour)
- **F# for Fun and Profit:** [fsharpforfunandprofit.com](https://fsharpforfunandprofit.com/) — Scott Wlaschin's site. THE F# resource. Railway-Oriented Programming originated here.
- **Playground:** [fsbolero.io/try](https://fsbolero.io/try/) · F# Interactive (`dotnet fsi`)
- **Exercism F#:** [exercism.org/tracks/fsharp](https://exercism.org/tracks/fsharp)
- **Book (required reading for Tier 6):**
  - **"Domain Modeling Made Functional"** by Scott Wlaschin — this is the book. If you read only one book during the sprint, make it this one. It makes DDD + ROP operational.
- **Community:** [F# Software Foundation](https://fsharp.org/) community Slack

### **Sprint recommendation for Tier 6:**
Before Week 13 starts, read "Domain Modeling Made Functional" cover to cover. It's ~280 pages but reads fast. It will give you the mental model for the entire PayGoHub v2 capstone. Wlaschin's website is free supplementary material.

---

# Embedded Platform (Module B of Sauti / Greenland sensors)

## Arduino / ESP32 / PlatformIO

- **Arduino docs:** [docs.arduino.cc](https://docs.arduino.cc/)
- **Arduino Reference:** [docs.arduino.cc/language-reference](https://docs.arduino.cc/language-reference/) — syntax reference
- **ESP32 / ESP-IDF docs:** [docs.espressif.com/projects/esp-idf](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/index.html)
- **PlatformIO docs:** [docs.platformio.org](https://docs.platformio.org/) — primary build system; learn this, not Arduino IDE
- **Arduino Project Hub:** [projecthub.arduino.cc](https://projecthub.arduino.cc/) — thousands of example projects
- **Embedded Rust Book:** [doc.rust-lang.org/stable/embedded-book](https://doc.rust-lang.org/stable/embedded-book/) — when ready to try `esp-rs`
- **Embassy (async Rust for embedded):** [embassy.dev](https://embassy.dev/)
- **Random Nerd Tutorials:** [randomnerdtutorials.com](https://randomnerdtutorials.com/) — pragmatic ESP32 walkthroughs; exceptionally well-maintained
- **Playground:** [wokwi.com](https://wokwi.com/) — Arduino/ESP32 SIMULATOR in the browser. You can prototype and debug firmware before any hardware arrives. This is genuinely extraordinary and often overlooked.

### **Recommendation:**
Wokwi is legitimately a game-changer for the pre-hardware phase. You can start writing LeeGlow firmware this weekend without owning anything. When the hardware arrives, move the code over.

---

# The Meta-Resources (Apply to All 16)

## Exercism

**[exercism.org](https://exercism.org)** — tracks for all 16 languages in this sprint. Free. Download exercises via CLI, solve locally, optionally get mentor feedback. Consistent structure across languages makes it ideal for rapid multi-language comparison. Your "Two Sum Rosetta Stone" can live entirely in Exercism.

## Rosetta Code

**[rosettacode.org](https://rosettacode.org)** — same problem solved in 800+ languages. When you want to see "how does X look in Zig vs C++ vs Go," this is the place.

## LeetCode

**[leetcode.com](https://leetcode.com)** — for the FAANG-prep angle. Accepts Rust, Go, C++, Java, Python, JS, TS, Kotlin, Scala, PHP, Ruby, Elixir, C#. Not Zig, F#, Clojure — use those in other practice settings. Suggested: 1-2 problems/day starting Week 4, in the language of current focus. Forces language-specific idioms.

## Codewars

**[codewars.com](https://codewars.com)** — kata (code challenges) in most sprint languages. More community-driven than LeetCode; good complement.

## AI-Assisted Learning (used responsibly)

When stuck on syntax or idioms, Claude Code, ChatGPT, Gemini can unblock you fast. **But:**
- Never ask "write this for me" — ask "why doesn't this compile?" or "what's the idiomatic version of this code?"
- Always read the generated answer, adapt it to your mental model, don't paste-and-ship
- Verify against official docs when the answer feels like it's inventing syntax

This aligns with the "AI as Collaborator, Not Crutch" principle in claude_code_strategy.md.

## GitHub (as a learning tool)

For any language, find 3-5 high-quality production repos and read them. For each language in the sprint, here's one I'd recommend skimming:

| Language | Repo | Why |
|----------|------|-----|
| Rust | [tokio-rs/tokio](https://github.com/tokio-rs/tokio) | Async runtime; idiomatic Rust at scale |
| C++ | [abseil/abseil-cpp](https://github.com/abseil/abseil-cpp) | Google's C++ foundations; modern idioms |
| Java | [spring-projects/spring-boot](https://github.com/spring-projects/spring-boot) | Canonical Spring patterns |
| Kotlin | [ktorio/ktor](https://github.com/ktorio/ktor) | Idiomatic Kotlin server framework |
| Scala | [zio/zio](https://github.com/zio/zio) | Idiomatic modern Scala 3 FP |
| JS/TS | [fastify/fastify](https://github.com/fastify/fastify) | Clean Node framework |
| Go | [kubernetes/kubernetes](https://github.com/kubernetes/kubernetes) | Large-scale idiomatic Go (pick small packages) |
| Zig | [ziglang/zig](https://github.com/ziglang/zig) | Zig itself is written in Zig; the compiler is readable |
| Ruby | [rails/rails](https://github.com/rails/rails) | Idiomatic Rails core |
| PHP | [laravel/framework](https://github.com/laravel/framework) | Idiomatic Laravel core |
| Elixir | [phoenixframework/phoenix](https://github.com/phoenixframework/phoenix) | Read the source of Phoenix; educational |
| Clojure | [metabase/metabase](https://github.com/metabase/metabase) | Large production Clojure codebase |
| C# | [dotnet/aspnetcore](https://github.com/dotnet/aspnetcore) | ASP.NET Core source |
| F# | [fsprojects/FSharp.SystemTextJson](https://github.com/Tarmil/FSharp.SystemTextJson) | Compact, idiomatic F# library |

---

# Recommended Reading Order Between Now and Monday

You have ~3 days. Do NOT try to learn Rust to fluency before Monday. Do this instead:

### **Thursday evening (1-2 hours):**
1. Skim [The Rust Book](https://doc.rust-lang.org/book/) Chapter 1 (Getting Started) and Chapter 4 (Understanding Ownership). These two chapters are 80% of what matters.
2. Install Rust locally: `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
3. Install VS Code + `rust-analyzer` extension if not already
4. Test: `cargo new hello_sauti && cd hello_sauti && cargo run` — confirm toolchain works

### **Friday evening (1-2 hours):**
1. Read Brown Rust Book Chapter 4 ([rust-book.cs.brown.edu](https://rust-book.cs.brown.edu/)) — same content with the superior interactive quizzes on ownership
2. Install Rustlings: `cargo install rustlings && rustlings init`
3. Do exercises `intro/`, `variables/`, `functions/` (~20-30 min)
4. DO NOT continue past that — you're calibrating, not training

### **Saturday (the weekend dry-run morning — 3 hours max):**
1. Full zazen + kinhin sequence (see the main plan)
2. ONE hour at most on Rustlings `if/`, `primitive_types/`, `structs/` (maybe 10 more exercises)
3. The rest of the morning: environment setup (`.claude/` directory in your Sauti repo skeleton, CLAUDE.md customized for Tier 1, MCP servers configured)

### **Sunday:**
1. Rest. Time with your daughter.
2. Evening: set your 3:20 AM alarm. Prepare breakfast for 8:10 AM. Clear tomorrow's decisions.

### **Monday 3:20 AM:**
1. The sprint begins. You have enough Rust to start writing Sauti. The Book stays open on a second screen.

**Specific rule:** If you find yourself reading theory after Saturday evening, STOP. Every additional hour of pre-reading past that point is anticipation anxiety dressed up as preparation. You learn Rust by writing Rust. Monday is when you start writing.

---

# CodinGame — Short Community Competitions

> **Why this has its own section:** CodinGame is structurally different from Exercism, LeetCode, or Codewars. It's not primarily for learning syntax or preparing for interviews. It's for **short, community-driven, competitive bursts** — the coding equivalent of a quick pickup basketball game at lunch. Given that you enjoy this format, it deserves dedicated framing within the sprint structure.

## What CodinGame Actually Is (in 2026)

CodinGame ([codingame.com](https://www.codingame.com)) is a puzzle and competition platform that has been running since 2012 with an active ~500,000+ user base. It's still active in 2026 — the current Winter Challenge (SNAKEBYTE) is live, and Clash of Code runs continuously. The platform has four distinct modes that serve different purposes, and recognizing the difference matters for how you'd fit it into the sprint.

### Mode 1 — **Clash of Code** (your main interest, by your own words)

5-15 minute battles between up to 8 coders, one of three randomly-chosen formats:
- **Fastest:** Pass all test cases as quickly as possible. Speed matters. Write ugly, write fast.
- **Reverse:** You see only the input and output — you must infer the algorithm from examples. This is a genuinely different cognitive skill from normal programming.
- **Shortest:** Code golf. Least characters wins. Ruby tends to dominate; Python is competitive. Your usual languages won't win here, but it's instructive.

This is the mode that matches your "short quick community competitions" preference most directly. 5-minute chunks. No multi-day commitments. No streaks to maintain.

### Mode 2 — **Classic Puzzles** (solo)

Self-paced puzzles ranked by difficulty. You solve at your own pace, as many languages as you want. Good for comparing your Python solution to your Rust solution to your Go solution on the same problem — which is exactly your sprint's "Two Sum Rosetta Stone" philosophy. Hundreds of puzzles available.

### Mode 3 — **Bot Programming / AI Competitions** (multiplayer turn-based)

You write a bot that competes against other bots in games like Tron, Ghost in the Cell, Coders of the Caribbean. Turn-based — your bot gets inputs each turn, outputs an action. These go DEEP — people sometimes spend weeks perfecting a single bot. This mode would eat your sprint whole if you let it. Stay away during the 15 weeks.

### Mode 4 — **Seasonal Contests** (Spring Challenge, Summer Challenge, Autumn Challenge, Winter Challenge)

10-day AI programming competitions, ~3x/year. Same trap as Mode 3 at higher intensity. Great community events for year 2.

## Languages CodinGame Supports (vs. your 16 sprint languages)

| Sprint Language | CodinGame Support | Notes |
|----------------|-------------------|-------|
| Python | ✅ Full | Anchor language, always available |
| Rust | ✅ Full | Your Monday language |
| C++ | ✅ Full | |
| Java | ✅ Full | |
| Kotlin | ✅ Full | |
| Scala | ✅ Full | |
| JavaScript | ✅ Full | |
| TypeScript | ✅ Full | |
| Go | ✅ Full | |
| **Zig** | ❌ Not supported | Use other practice for Zig |
| Ruby | ✅ Full | Dominant in shortest-mode clashes |
| PHP | ✅ Full | |
| **Elixir** | ⚠️ Only in enterprise "CodinGame for Work" product, not in Clash of Code | Use Exercism for Elixir practice instead |
| Clojure | ✅ Full | |
| C# | ✅ Full | |
| F# | ✅ Full | |

**14 of 16 languages covered.** The two gaps (Zig, Elixir) you can cover on Exercism, which supports both.

## How CodinGame Fits Into the Sprint (Carefully)

CodinGame has a specific risk profile you should take seriously: **it's designed to be fun enough that you lose track of time.** A single clash is 5 minutes, but the "one more clash" urge is real, and an hour disappears. Multiply that across 15 weeks and you've ceded significant deep-work time to what was supposed to be a 5-minute break.

Therefore, treat CodinGame as a **scheduled reward**, not a background activity. Budget it explicitly:

### **Recommended sprint integration:**

**Option A — The Weekend Warmup (recommended):**
- Saturday morning, as part of the weekly retreat, after zazen but before deep work: **3 clashes maximum** (15-20 minutes total). Use them as cognitive warmup — they get your brain into "recognize-pattern-write-code" mode at competition speed.
- Use this as a chance to clash in the tier's current language. Week 1-2: try doing Fastest-mode clashes in Rust (you'll lose at first; that's the point).
- Close the browser tab after 3 clashes. Non-negotiable.

**Option B — The Friday Celebration:**
- Friday evening, after the week's last deep-work session, as a wind-down: 30 minutes of Clash of Code. Celebrate the week's grind by doing something that uses the same muscles but lightly.
- Stop at 30 minutes. Phone alarm. No exceptions.

**Option C — The Commute Substitute:**
- If you find yourself with 15-20 unexpected minutes (waiting for your daughter at a clinic, stuck in Nairobi traffic as a passenger, etc.), one clash fills the time productively.

### **What NOT to do:**
- Don't do clashes during 4 AM deep-work blocks. The cognitive profile is wrong — clashes reward fast, ugly, throwaway code. Deep work requires slow, careful, architectural thinking. Contamination between the two damages both.
- Don't start Bot Programming (Mode 3) during the sprint. It's genuinely addictive and eats unlimited time.
- Don't chase leaderboard rank. You're a working engineer with a daughter, not a competitive clasher. The rank is meaningless to the sprint's goals.

## Strategic Use: Multi-Language Clashing

Here's a specific sprint technique CodinGame enables that other platforms don't:

**The same clash can be solved in multiple languages.** After you submit a solution in one language, you can replay the same problem in a different language. This is an extraordinary way to feel the idiomatic differences between languages solving the same problem, fast.

**Sprint-aligned practice:**
- Week 1-2 (Tier 1): Solve each Saturday clash first in Python, then translate to Rust. Feel where the borrow checker complains.
- Week 3-4 (Tier 2): Solve each clash in Java, Kotlin, and Scala. Feel the progression from imperative to null-safe to functional.
- Week 5-6 (Tier 3): JavaScript vs TypeScript comparison.
- Week 7-8 (Tier 4): Python vs Go — feel Go's explicitness.
- Week 9-10 (Tier 5a): Ruby vs PHP vs Elixir on the same problem. Feel the web-framework lineage in the language designs themselves.
- Week 11-12 (Tier 5b): Rewrite a few prior clashes in Clojure. Feel what homoiconicity lets you do.
- Week 13-14 (Tier 6): C# vs F# on the same problem. Feel what ROP buys you.

This turns a 3-clash Saturday session into genuine cross-language architectural observation. The clash itself takes 5 minutes; the translation takes another 10-20. You end up with a feel for the language that pure reading never gives you.

## Tips for Specifically Winning (since you enjoy the competitive side)

- **Fastest mode:** Use your strongest language. Don't use Rust for Fastest clashes; the borrow checker costs seconds. Use Python for Fastest mode; it's the fastest to write.
- **Reverse mode:** This is the most cognitively interesting. Before writing any code, produce the pattern on paper. Write `f(input) = output` for each test case, squint at them, find the relationship. Then write the code.
- **Shortest mode:** Use Ruby. The language wins shortest mode almost always. If you don't know Ruby well, Python is second-best but a distant one. You can win some shortest clashes just by knowing one Ruby trick (the `gets.chomp`, `puts`, and array tricks).
- **Read the other players' solutions after each clash.** CodinGame shows you everyone's submitted code post-clash. This is the single most valuable 30 seconds of each clash — see how someone else compressed your 30-line solution into 8 lines. Pattern-match. Steal the idioms.
- **Use keyboard shortcuts in the editor.** Clashes are about seconds. Mouse-use kills you. Vim or Emacs mode in the CG editor is a force multiplier.

## Alternatives Worth Knowing

If CodinGame is down, or you want variety:

- **[Advent of Code](https://adventofcode.com)** — December only. 25 days of puzzles, solve in any language, genuinely excellent problems. Rustfinity runs [Advent of Rust](https://www.rustfinity.com/advent-of-rust). Excellent year-end tradition.
- **[Kattis](https://open.kattis.com)** — competitive programming judge. Cleaner than CodinGame, less game-like.
- **[Codewars kata](https://codewars.com)** — async "kata" format. Less time-pressure than Clash of Code; good for when you want the competitive feel without the clock.
- **[CSES Problem Set](https://cses.fi/problemset/)** — Finnish competitive programming curriculum. Serious. Use when you want depth, not speed.

## The Integration Rule for the Sprint

**CodinGame during the sprint = Saturday morning warmup (3 clashes) + Friday evening wind-down (30 min).** That's it. About 45 minutes per week, bounded, enjoyable, aligned with the language you're currently working in.

Post-sprint, if the lifestyle stays, you can re-engage with Bot Programming and Seasonal Contests. They're fun. But during the 15 weeks, they're too addictive to be safe.

---



Resources are infinite. Attention is finite. For every language in this sprint:

1. Bookmark the **official docs** (single source of truth).
2. Find **one primary interactive path** (Rustlings for Rust, Tour of Go for Go, Livebook for Elixir, etc.).
3. Own **one reference book** if going deep (Rust for Rustaceans, Domain Modeling Made Functional, Clojure Applied).
4. Use the **playground** for hypothesis-testing, not learning.
5. Write real code in the language as soon as possible.

The goal is not "mastery" of each language. The goal is **architectural literacy** — being able to read, translate, and pattern-match across all 16. That's what the sprint is training. The resources above are tools, not destinations.

Chop wood. Carry water. Write code. The patterns will reveal themselves.
