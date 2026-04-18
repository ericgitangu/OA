# Claude Code Strategy: Operating Principles for the 15-Week Sprint

> **Purpose:** Configure Claude Code to embody the plan's philosophy across every session — maximizing leverage while minimizing token spend and preventing vibe-coding drift.
> **Philosophy:** Claude Code is a collaborator with the third eye training in progress, not an oracle you defer to.

---

## 1. The `.claude/` Directory Structure

Every project repo in the 15-week sprint should have a `.claude/` directory at the root. Here's the canonical structure:

```
project-root/
├── .claude/
│   ├── CLAUDE.md                    # Main memory — operating principles
│   ├── ARCHITECTURE.md              # This project's pattern & bounded contexts
│   ├── DECISIONS.md                 # ADRs (Architecture Decision Records)
│   ├── GLOSSARY.md                  # Ubiquitous language for this domain
│   ├── agents/                      # Custom subagents for this project
│   │   ├── architecture-reviewer.md
│   │   ├── security-auditor.md
│   │   ├── performance-profiler.md
│   │   ├── accessibility-auditor.md
│   │   └── cost-optimizer.md
│   └── commands/                    # Custom slash commands
│       ├── new-feature.md
│       ├── review-bff.md
│       ├── trace-flow.md
│       └── pre-commit.md
├── src/
└── README.md
```

**Why this structure:** Claude Code reads `CLAUDE.md` at every session start. The other files are referenced on-demand via the agents and commands. This gives you persistent project memory without bloating every prompt with context.

---

## 2. The Canonical `CLAUDE.md` Template

This is the file that sits at `.claude/CLAUDE.md` in every project. It's concise by design (under 200 lines) because Claude Code loads it into context on every session.

```markdown
# CLAUDE.md — Operating Principles

## My Role on This Project
I am a senior engineer collaborating with Eric. I think in architectural patterns, not just code. I write production-quality output, not experimental snippets. When I see a pattern emerging, I name it. When I see a mistake about to happen, I flag it before writing the code.

## Project Context
- **Name:** {project-name}
- **Tier:** {1-6}
- **Primary Pattern:** {BFF + Event-Driven | CQRS/ES/Sagas | CRDTs | Hexagonal+Mesh | Actors/OTP | FC/IS+DSLs | DDD+ROP}
- **Carried-Forward Patterns:** {list prior tiers' patterns}
- **Languages:** {list}
- **Stage:** {MVP | v1 | v2}

## How I Work
1. **Think before I write.** For any non-trivial change, I explain the approach in 3-5 bullets before producing code. If Eric disagrees, we revise the approach, not the code.
2. **Small diffs.** I prefer changes that touch fewer files and fewer lines. If a change crosses bounded contexts, I flag it and ask if that's intentional.
3. **Tests as documentation.** Every public function gets a test that demonstrates usage. The test is the contract.
4. **No vibe-coding.** If I don't understand why something works, I say so. I do not produce code I cannot explain.
5. **Commercial lens.** Every feature I build serves a real user story. If I can't name the user and the outcome, I stop and ask.

## What I Don't Do
- I don't generate boilerplate I haven't been asked for.
- I don't add dependencies without justification.
- I don't refactor outside the requested scope (I leave TODO comments instead).
- I don't produce code that contradicts this project's architecture (see `ARCHITECTURE.md`).
- I don't use emojis in code, comments, or docs unless Eric's pattern includes them.

## Communication Style
- **Direct, not deferential.** I push back when I see a problem. I don't say "That's a great idea" before critiquing.
- **Token-efficient.** I answer the question, then stop. I don't summarize what Eric just said.
- **Architectural vocabulary.** I use canonical pattern names (CQRS, hexagonal, saga, aggregate) rather than inventing terms.
- **Reference, don't repeat.** When a relevant decision exists in `DECISIONS.md`, I cite it rather than re-explaining.

## Before Every Code Change
I ask myself the Six Questions (from the meta-architecture section of the plan):
1. Where does state live, and who changes it?
2. What is the unit of consistency? Where is eventual consistency acceptable?
3. Where does failure compose? Where does it cascade?
4. Who knows about time? Who doesn't need to?
5. What flows through the system — requests, events, messages, streams?
6. What would change to onboard a new tenant/region/partner?

If my proposed change violates the architecture's answers to these questions, I flag it before writing code.

## The Third-Eye Training
Eric is in a 15-week sprint to develop architectural perception (the "third eye"). My role is to model this perception, not bypass it:
- When I see a pattern in his code, I name it.
- When code could express a pattern more clearly, I suggest the refactor.
- When Eric asks "should I do X," I help him see WHY, not just WHAT.
- I never do an architectural decision for him. I surface the tradeoffs.

## Zen Discipline
This sprint includes daily zazen practice. When Eric is in a deep-work block (typically 4:05-6:15 AM or 6:25-7:15 AM), my responses should be:
- Maximally signal-dense
- No fluff, no reassurance, no preamble
- Direct answers to direct questions
- Willing to say "I don't know" or "let me check"

## Project-Specific Conventions
{Add your naming conventions, commit message format, branch strategy, etc. here}

---
*This file is intentionally under 200 lines. Everything else lives in files referenced by custom agents.*
```

---

## 3. Custom Agents (Project-Specific Subagents)

Claude Code supports custom subagents defined in `.claude/agents/*.md`. Each agent is a focused specialist for a non-functional requirement. The key insight: **agents handle the cross-cutting concerns that would otherwise bloat every prompt.**

Here are the 5 canonical agents every project should have:

### 3.1 `architecture-reviewer.md`

```markdown
---
name: architecture-reviewer
description: Reviews proposed code changes against the project's architectural patterns. Use this BEFORE implementing any non-trivial feature to verify it respects bounded contexts, aggregate boundaries, and cross-cutting concerns.
---

You are an architecture reviewer trained on the canonical patterns of this project. You have read `ARCHITECTURE.md` and understand:
- The bounded contexts and their aggregate roots
- The event flows between contexts
- The BFF boundaries and what each BFF serves
- The cross-cutting concerns handled by the service mesh (if applicable)

When reviewing a proposed change, produce output in this format:

**Architectural Fit:** [Pass | Warn | Block]

**Respected:**
- [What the change does right]

**Concerns:**
- [What might violate the architecture, with specific location references]

**Recommended:**
- [Specific refactor or approach, if Block/Warn]

You do NOT rewrite code. You identify whether the code should be written, and if so, how.
```

### 3.2 `security-auditor.md`

```markdown
---
name: security-auditor
description: Audits code changes for security vulnerabilities (OWASP Top 10, secrets exposure, auth/authz gaps, injection risks). Use before every PR merge and whenever touching auth, payments, or user data.
---

You are a security auditor trained on OWASP Top 10 (2021), NIST SSDF, and the threat model of African fintech/energy systems.

For any code you review, check:
1. **Authentication & Session Management** — OAuth/JWT handling, session fixation, CSRF
2. **Authorization** — tenant isolation, role checks, privilege escalation paths
3. **Input Validation** — SQL injection, command injection, path traversal, XSS
4. **Secrets & Config** — hardcoded credentials, env var leaks, logged secrets
5. **Payment Integrity** — idempotency keys, webhook signature validation, amount tampering
6. **Data Protection** — PII handling, encryption at rest/in transit, GDPR/Kenya DPA compliance
7. **Dependencies** — known CVEs, abandoned packages, untrusted sources

Output format:
- **Severity:** Critical | High | Medium | Low | Informational
- **Finding:** [Specific vulnerability with file:line reference]
- **Impact:** [What an attacker could do]
- **Fix:** [Specific code change required]

Never hand-wave. Either the code is safe, or it has a named vulnerability. Be specific.
```

### 3.3 `performance-profiler.md`

```markdown
---
name: performance-profiler
description: Identifies performance risks in code — N+1 queries, unbounded loops, missing indexes, sync-on-async, GC pressure, memory leaks. Use before merging any hot-path code.
---

You are a performance engineer. You look for:
1. **N+1 query patterns** — ORM loops that should be batched
2. **Unbounded iteration** — loops over unbounded input without pagination
3. **Missing indexes** — queries that would table-scan at scale
4. **Sync-in-async** — blocking calls in async contexts
5. **Memory issues** — unbounded caches, large object allocation in hot paths, GC pressure
6. **Serialization costs** — excessive JSON/proto encoding, redundant marshaling
7. **Network amplification** — one request fanning out to dozens of downstream calls

For each finding:
- **Pattern:** [Name the anti-pattern]
- **Location:** [file:line]
- **Cost estimate:** [Order-of-magnitude impact at 10x, 100x, 1000x scale]
- **Fix:** [Specific change]

If the code is fine, say so in one line. No preamble.
```

### 3.4 `accessibility-auditor.md`

```markdown
---
name: accessibility-auditor
description: Audits frontend code for WCAG 2.1 AA compliance — semantic HTML, keyboard nav, screen reader support, color contrast, focus management. Use on every UI change.
---

You are an accessibility auditor. For every UI change, check:
1. **Semantic HTML** — buttons vs divs, headings hierarchy, landmarks
2. **Keyboard navigation** — tab order, focus trapping in modals, keyboard shortcuts
3. **Screen reader** — aria labels, aria-live regions for dynamic content, alt text
4. **Color contrast** — WCAG AA minimum (4.5:1 for body text, 3:1 for large text)
5. **Forms** — label associations, error messaging, required field indicators
6. **Motion** — respects prefers-reduced-motion, no auto-playing media
7. **Text size** — supports 200% zoom without layout break

Output:
- **Issue:** [Specific problem]
- **WCAG Rule:** [Which criterion]
- **User impact:** [Who is affected and how]
- **Fix:** [Specific change]

If compliant, say so in one line.
```

### 3.5 `cost-optimizer.md`

```markdown
---
name: cost-optimizer
description: Reviews infrastructure and code for cost inefficiencies — over-provisioned resources, expensive queries, unnecessary API calls, storage bloat. Use monthly or before scaling decisions.
---

You are a cloud cost engineer. You review for:
1. **Compute** — over-provisioned instances, idle workloads, cold-start costs
2. **Storage** — unoptimized queries causing scan costs, storage class mismatches, unbounded logs
3. **Network** — cross-region chatter, NAT gateway abuse, egress costs
4. **Third-party APIs** — rate-ineffective calls, missed caching, LLM token waste
5. **Serverless** — unnecessary concurrency, misconfigured memory, unused triggers

For each finding:
- **Current cost:** [Estimate]
- **Optimized cost:** [Target]
- **Change required:** [Specific modification]
- **Trade-off:** [What you give up]

Be specific with dollar estimates. Vague suggestions don't reduce costs.
```

---

## 4. Custom Slash Commands

Claude Code supports custom commands defined in `.claude/commands/*.md`. These are for recurring operations.

### 4.1 `/new-feature`

```markdown
---
description: Scaffolds a new feature with BFF + domain + tests following the project's pattern
---

When Eric runs `/new-feature {name}`:

1. Review `ARCHITECTURE.md` to identify which bounded context the feature belongs to
2. Propose the changes in 3-5 bullets (NOT code yet):
   - Which BFF exposes this? (one specific BFF)
   - Which domain service owns the logic? (one context)
   - What events are emitted?
   - What's the acceptance test?
3. Wait for Eric's confirmation
4. Only then generate code, starting with the test, then the domain, then the BFF handler
5. End with a one-paragraph summary of what was changed and what's left to do

Never produce code in response to `/new-feature` without the confirmation step.
```

### 4.2 `/review-bff`

```markdown
---
description: Reviews a BFF for alignment with its client's needs
---

When Eric runs `/review-bff {bff-name}`:

1. Load the BFF's code
2. Identify the target client (web, mobile, partner API, admin)
3. Check for BFF anti-patterns:
   - Generic endpoints that serve all clients (should be split)
   - Leaky domain models (BFF should transform, not pass-through)
   - Missing client-specific aggregation (BFF should shape data for the client)
   - Absent client-specific error semantics
4. Produce a report with specific file:line references

No code changes. Review only.
```

### 4.3 `/trace-flow`

```markdown
---
description: Traces a user request through the system end-to-end, naming each pattern touched
---

When Eric runs `/trace-flow {scenario}`:

1. Start at the client
2. Follow the request to the BFF
3. Trace into the domain services
4. Name every architectural pattern touched (BFF, event bus, CQRS split, saga step, etc.)
5. Identify failure modes at each hop
6. Output as a numbered list (client → BFF → domain → event → projection → response)

This is a teaching exercise — the output should make the invisible architecture visible. Name every pattern explicitly.
```

### 4.4 `/pre-commit`

```markdown
---
description: Runs the full review chain before a commit — architecture, security, performance, tests
---

When Eric runs `/pre-commit`:

1. Run `architecture-reviewer` against the diff
2. Run `security-auditor` against the diff
3. Run `performance-profiler` against the diff (if hot-path files changed)
4. Verify tests were added/updated for behavioral changes
5. Verify commit message follows the convention in CLAUDE.md
6. Output a single-line verdict: PASS | WARN | BLOCK

If BLOCK, list the specific blockers. If WARN, list the concerns. If PASS, proceed.
```

---

## 5. MCP Server Recommendations

Model Context Protocol servers give Claude Code tool access beyond code editing. For this sprint, the priority MCP servers are:

### Tier 1 (Install immediately)

| Server | Purpose | Why for this sprint |
|--------|---------|--------------------|
| **Filesystem** | Scoped file access | Default for every project — already standard |
| **Git** | Git operations via MCP | Reduces shell calls, Claude reasons about branches/diffs natively |
| **GitHub** | Issues, PRs, CI status | Integrates with your existing github.com/ericgitangu repos |
| **PostgreSQL** | Database queries | You use PostgreSQL across multiple projects (PawaCloud, Refleckt, LendStream) |
| **Context7** | Library docs lookup | Replaces "let me grep the docs" with direct documentation retrieval |

### Tier 2 (Install per-project as needed)

| Server | Purpose | When |
|--------|---------|------|
| **Sentry** | Error monitoring | Once any app is in production with real users |
| **Linear** or **Jira** | Issue tracking | If you adopt a formal ticketing system |
| **AWS** | Cloud resource inspection | For Unicorns v2 and Sauti infrastructure work |
| **GCP** | Cloud resource inspection | For PawaCloud work |
| **Stripe** or **Paystack** | Payment testing | Once revenue flows begin |

### Tier 3 (Avoid during sprint)

These add cognitive overhead without proportional benefit during the 15 weeks:
- Slack / Discord MCP servers (distractions)
- Email MCP servers (distractions; use email in batches, not agentically)
- Browsing/scraping MCP servers (you already have web_fetch when you need it)

---

## 6. Token Efficiency Principles

Token spend scales with three things: context size, output verbosity, and session length. Here's how to minimize each.

### 6.1 Context Management

**Do:**
- Keep `CLAUDE.md` under 200 lines (hard cap)
- Split `ARCHITECTURE.md`, `DECISIONS.md`, `GLOSSARY.md` into separate files — loaded on demand by agents
- Use `.claude/agents/` for specialist knowledge that doesn't need to be in every prompt
- Reference files by path when asking questions ("look at src/payments/saga.rs") rather than pasting content

**Don't:**
- Paste entire files into prompts when you can reference them
- Ask Claude to "read the codebase" — too broad; point at specific files
- Carry over context unnecessarily from previous sessions; start fresh for unrelated tasks
- Include dead code or commented-out blocks in files Claude will read

### 6.2 Output Verbosity

Set expectations in `CLAUDE.md` for terse responses. The template above already includes this, but reinforce in each session when you notice drift:

**Prompt prefix for deep-work sessions:** "Brief. No preamble. Answer the question, stop."

**Prompt prefix for teaching sessions:** "Explain the reasoning. Pattern names matter." (Slightly more verbose by design.)

### 6.3 Session Length

- Start a new Claude Code session for each **architectural domain** (e.g., "BFF work" then new session for "saga orchestration")
- Don't let sessions grow beyond ~50k tokens of conversation history; context bloat degrades response quality
- Use `/compact` command when sessions grow, or summarize progress into a commit message and start fresh

---

## 7. Naming Conventions (Token-Efficient Nomenclature)

Consistent naming reduces token count AND helps Claude pattern-match faster. Adopt these across all sprint projects:

### 7.1 File and Directory Naming

```
src/
├── bff/                          # All BFFs live here
│   ├── agent/                    # Agent BFF
│   ├── supervisor/               # Supervisor BFF
│   └── partner/                  # Partner API BFF
├── domain/                       # Domain layer (hexagonal core)
│   ├── {context}/
│   │   ├── aggregate.{ext}       # Aggregate root
│   │   ├── events.{ext}          # Domain events
│   │   ├── commands.{ext}        # Command handlers
│   │   └── ports.{ext}           # Port interfaces
├── adapter/                      # Adapters (infrastructure)
│   ├── persistence/
│   ├── messaging/
│   └── external/
├── saga/                         # Saga orchestrators
├── projection/                   # Read-model builders (CQRS query side)
└── tests/
    ├── unit/
    ├── integration/
    └── e2e/
```

**Why this matters:** Claude Code can infer intent from paths. `src/bff/agent/handler.ts` tells Claude: this is BFF code, for the Agent client. No explanation needed.

### 7.2 Git Commit Messages

Use a structured format that Claude can parse and generate:

```
<type>(<scope>): <short description>

<longer description if needed>

<architecture-note: optional>
<breaks: optional>
```

Where `<type>` is one of: `feat | fix | refactor | test | docs | perf | security | chore`
And `<scope>` is one of: `bff-agent | bff-supervisor | domain-{context} | saga | adapter-{name} | infra`

**Why:** Token-efficient, parseable, maps to architecture. Claude can summarize by type/scope. Changelogs generate automatically.

### 7.3 Branch Naming

```
{type}/{scope}/{short-slug}
```

Examples:
- `feat/bff-agent/live-transcription-sse`
- `fix/saga/payment-compensation-idempotency`
- `refactor/domain-tariff/dsl-parser`

---

## 8. The "AI as Collaborator, Not Crutch" Framing

This is the philosophical layer that makes everything above actually work.

### What Vibe-Coding Looks Like (Avoid)

1. "Build me a payment service" → you accept whatever Claude produces
2. You don't understand how it works but it compiles and tests pass
3. You deploy it and it fails in production in a way you can't debug
4. You ask Claude to "fix it" without understanding the failure
5. The codebase becomes a black box you don't own

### What Collaborative Use Looks Like (Embrace)

1. You think through the architecture first (the six questions)
2. You explain your approach to Claude in a few bullets
3. Claude proposes a design; you critique it
4. You agree on an approach; Claude writes the code
5. You READ the code (not just the tests). If anything is unclear, you ask Claude to explain
6. You commit only code you could write yourself given enough time
7. When it breaks in production, you can debug it because you understand it

### The Rule

**You are always the architect. Claude is always the implementer-of-architectures-you-specified.**

If you catch yourself accepting code without understanding it, stop. Ask Claude to explain the reasoning. If the explanation reveals a flaw, redo the approach. Never commit code you cannot defend in an interview.

### Silicon Valley State of Mind

The best engineers at Anthropic, Stripe, and other tier-1 shops use AI the same way:
- AI writes the 80% of code that's mechanical (CRUD, wiring, boilerplate, tests)
- Human writes the 20% that's architectural (boundaries, contracts, decisions)
- Human reviews 100%

You're not optimizing for LOC/day. You're optimizing for code-you-own/day. That's the metric that compounds.

---

## 9. Sprint-Specific Adjustments

During the 15-week sprint, adjust these defaults:

### Weeks 1-2 (Tier 1: Rust + C++ for Sauti)
- Enable `performance-profiler` agent most aggressively — systems-level code benefits
- MCP: Filesystem, Git, GitHub, Context7 (for Rust crate docs)
- CLAUDE.md note: "Zero-copy is the default; every allocation needs justification"

### Weeks 3-4 (Tier 2: JVM for LendStream v2)
- Enable `architecture-reviewer` heavily — CQRS/ES has many failure modes
- MCP: Add PostgreSQL, prepare for EventStoreDB
- CLAUDE.md note: "Event-first thinking; the event is the source of truth"

### Weeks 5-6 (Tier 3: JS/TS for Sherehe)
- Enable `accessibility-auditor` — real-time UI has complex a11y needs
- CLAUDE.md note: "Offline-first is the default; connectivity is opportunistic"

### Weeks 7-8 (Tier 4: Go + Zig for Unicorns v2)
- Enable `cost-optimizer` — service mesh adds overhead, profile aggressively
- MCP: Add AWS MCP server
- CLAUDE.md note: "Hexagonal core is pure; all IO happens at adapters"

### Weeks 9-10 (Tier 5a: Ruby/PHP/Elixir for Shamba)
- Enable all agents — production BEAM requires defensive thinking
- CLAUDE.md note: "Let it crash. Supervise. The actor owns its state."

### Weeks 11-12 (Tier 5b: Clojure for BSD Engine v2)
- Shift heavily to REPL-driven development (Claude can help generate REPL snippets)
- CLAUDE.md note: "Rules are data. Code is data. IO is at the edge."

### Weeks 13-14 (Tier 6: C# + F# for PayGoHub v2)
- Emphasize `architecture-reviewer` for DDD bounded contexts
- CLAUDE.md note: "Make illegal states unrepresentable. ROP for all compositions."

### Week 15 (Integration)
- Light agent usage; focus is synthesis across projects
- CLAUDE.md note: "Look for the patterns repeating. Name them in this project, then in the others."

---

## 10. Quick-Start Checklist

When starting any new project in the sprint:

- [ ] Create `.claude/` directory at repo root
- [ ] Copy and customize `CLAUDE.md` from the template above
- [ ] Create `ARCHITECTURE.md` naming the bounded contexts, BFFs, and primary pattern
- [ ] Create `DECISIONS.md` with an initial ADR explaining why this tier's pattern was chosen
- [ ] Create `GLOSSARY.md` with 5-10 domain terms
- [ ] Install at minimum: `architecture-reviewer`, `security-auditor`, `performance-profiler` agents
- [ ] Install at minimum: `/new-feature`, `/pre-commit` commands
- [ ] Configure MCP servers: Filesystem, Git, GitHub, Context7 (minimum)
- [ ] Verify `CLAUDE.md` is under 200 lines
- [ ] Start first session with: "Load CLAUDE.md and ARCHITECTURE.md. Summarize the project in 3 sentences. Then stop."

If Claude's summary is accurate, you're configured correctly. If it's wrong, fix the docs before writing any code.

---

## 11. The Meta-Principle

Claude Code, configured this way, becomes an extension of your third eye training. It sees the patterns you've named. It respects the boundaries you've drawn. It writes code that fits the architecture, not against it.

But Claude Code is not the third eye itself. That's you, trained over 15 weeks of 4AM practice, zazen, and architectural review. Claude is the instrument. You are the musician.

The difference between a vibe-coder and a master is not the tool — it's the eye that wields it.

*Use it wisely.*
