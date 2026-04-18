# PRD — BSD Engine v2

> **Version:** 2.0
> **Date:** April 2026
> **Status:** Draft — Approved for Sprint Weeks 11-12
> **Owner:** Eric Gitangu (Deveric Technologies)
> **Tier:** 5b (Clojure)
> **Project Type:** Major Extension of Shipped App
> **Existing system:** BSD Growth Engine (Rust/PyO3 + ML decision-support; internal, deployed at Ignite)

---

## 1. Executive Summary

**BSD Engine v2** transforms the existing proprietary BSD (Business/System Diagnostics) decision-support system into a **white-label diagnostic platform** sold to African consulting firms, sector regulators, and internal corporate strategy teams. The v1 engine combined deterministic Rust-based scoring logic (the protected IP) with LLM-layered interpretation. The v2 thesis: the deterministic logic is generic diagnostic infrastructure that can be re-applied across industries — what differs is the rules, not the engine.

The v2 redesign introduces a **business-readable rules DSL** written in Clojure and compiled to a deterministic scoring function. Consultants write their diagnostic methodology as data (EDN-based rules); the platform executes, scores, explains, and visualizes. This is the exact pattern that Drools (Java), Clara (Clojure), and RETE-based systems have used for decades — adapted for modern LLM-assisted explanation and African-market consulting workflows.

**Commercial thesis:** Consulting firms (McKinsey Africa, Dalberg, Genesis Analytics, local boutiques) currently build bespoke Excel-based assessment tools per engagement, losing IP portability between projects. A white-labeled BSD Engine lets them systematize their diagnostic methodology, charge higher fees, and sell ongoing monitoring subscriptions to clients. Pricing: $199-$4,999/mo per consulting firm; enterprise regulators at custom pricing.

---

## 2. Problem Statement

### 2.1 The Pain

1. **Consulting methodologies don't scale.** When a consulting firm does a business diagnostic for a client, the work is captured in Excel + PowerPoint. The next engagement recreates the methodology from scratch. Senior consultants can't leverage their own prior work efficiently.

2. **Client engagements end when the deliverable is submitted.** Consulting firms deliver a one-time assessment PDF. The client doesn't get ongoing value; the consulting firm doesn't get recurring revenue. Both want a monitoring relationship, but the tooling doesn't exist.

3. **Clients can't re-run diagnostics themselves.** A client who wants to track progress against the consulting firm's recommendations has to re-engage the firm for follow-up studies. If the methodology were executable, the client could run it themselves.

4. **Regulators face the same pattern.** Sector regulators (e.g., Central Bank of Kenya for MFIs, Kenya ICT Authority for tech licenses) assess compliance periodically using spreadsheets and site visits. They'd benefit from continuous monitoring tooling, but licensed products are too expensive / foreign-market-focused.

5. **The "protected IP" problem.** When a consulting firm builds a methodology, they want it encoded somewhere auditable but not replicable by the client. Excel doesn't protect IP; neither does a PDF. A diagnostic engine that executes the rules without exposing them in readable form solves this.

### 2.2 Quantified Market

- **African consulting firms (mid-size):** ~200 across the continent doing strategy/operations work
- **Local Kenyan strategy boutiques:** ~30 with 5-50 consultants each
- **Sector regulators in Kenya:** ~15 major regulators each overseeing 20-500 licensed entities
- **Corporate in-house strategy teams at pan-African corporates:** ~100 (Safaricom, Equity, KCB, etc.)

**Revenue math:** 20 consulting firms at $500/mo average = $10K MRR. 3 regulators at $2,500/mo = $7.5K MRR. Potential $17-30K MRR within 18-24 months.

### 2.3 Why Now

- Clojure is increasingly viable in East African tech (several local startups use it)
- LLM-powered explanation is now good enough that diagnostic outputs are genuinely useful without extensive manual interpretation
- African consulting market is growing (pan-African expansion, ESG/sustainability mandates driving assessments)
- Regulators under increasing pressure to digitize oversight (driven by international ratings agencies, IMF scrutiny)

---

## 3. Target Users & Personas

### 3.1 Primary Persona: Boutique Consulting Firm Partner

**Name:** Sarah, 42, Nairobi
**Role:** Partner at a 15-consultant strategy boutique serving pan-African clients
**Goals:**
- Systematize firm methodology (currently in senior consultants' heads and Excel templates)
- Win larger engagements by demonstrating repeatable, tech-enabled diagnostics
- Generate recurring revenue through post-engagement monitoring subscriptions
- Reduce junior consultant onboarding time (currently 6 months to productivity)

**Pain points:**
- Methodology IP walks out when senior consultants leave
- Can't prove to clients that this engagement will be replicable next year
- Junior consultants recreate analysis frameworks from scratch every engagement

**Jobs-to-be-done:** Encode the firm's diagnostic methodology in executable form, offer clients ongoing monitoring, protect IP from replication.

### 3.2 Secondary Persona: Consulting Analyst

**Name:** Brian, 28, Nairobi
**Role:** Analyst at same boutique, 3 years of experience
**Goals:**
- Do higher-value work, not data entry
- Understand the firm's methodology deeply (career development)
- Get results faster so he can go home before 8 PM

**Pain points:**
- Spends 60% of time collecting/structuring client data
- Partners review his analyses late at night; feedback loop is slow
- Can't experiment with methodology variations without breaking the firm's templates

**Jobs-to-be-done:** Data entry becomes structured input forms; analysis engine runs methodology; Brian interprets outputs and presents to clients. Faster loop, higher-skill work.

### 3.3 Tertiary Persona: Regulator Compliance Officer

**Name:** Joseph, 48, CBK's Digital Credit Providers unit
**Role:** Oversees 30+ licensed digital credit providers (MFIs)
**Goals:**
- Continuously assess each licensee against CBK's DCP regulations
- Flag high-risk licensees before they cause customer harm
- Reduce manual spreadsheet-based quarterly assessments

**Pain points:**
- Each quarter, his team compiles Excel assessments per licensee; takes 2 weeks of 4 people's time
- Issues are caught at quarterly review, not in real-time
- No way to track issue remediation systematically

**Jobs-to-be-done:** Turn quarterly manual review into continuous automated monitoring with regulator-defined rules. Flag issues in real-time.

### 3.4 Quaternary Persona: Corporate Strategy Director

**Name:** Grace, 44, pan-African retail conglomerate
**Role:** Head of Strategy, reports to CEO
**Goals:**
- Monitor subsidiary company performance against strategic KPIs
- Run "what-if" scenarios (if we increase advertising by 20%, what happens?)
- Present board-ready dashboards monthly

**Pain points:**
- Monthly data collection from 12 subsidiaries is manual and late
- Each subsidiary reports in a different format
- Excel-based consolidation introduces errors

**Jobs-to-be-done:** Encode the corporate strategic model once; have subsidiaries feed in data monthly; get consolidated board-ready analysis with minimal manual work.

### 3.5 Non-Target Users (Explicit)

- **Big-4 consulting firms (McKinsey, BCG, Bain)** — they have their own proprietary tooling; not the ICP
- **Small freelance consultants** — insufficient budget; would use free/low-cost alternatives
- **Data scientists** — they already have Python/R; don't need a DSL

---

## 4. User Stories & Acceptance Criteria

### 4.1 Epic: Methodology Authoring

**User Story 4.1.1:** As a senior consultant, I want to write my firm's diagnostic methodology as a set of rules that the engine executes, so that my expertise becomes durable infrastructure rather than tacit knowledge.

**Acceptance Criteria:**
- **Given** access to the Analyst BFF rule editor
- **When** I define a rule (e.g., "if revenue growth < 5% AND customer acquisition cost > 3x LTV, flag as 'unsustainable unit economics' with severity 'high'")
- **Then** the rule is written in a Clojure-based DSL (EDN)
- **And** validation runs immediately (syntax, semantic, rule dependencies)
- **And** I can test the rule against sample data in the integrated REPL
- **And** rules are version-controlled (every edit is an event in the event log)
- **And** I can compose rules into a full methodology (e.g., "Business Sustainability Diagnostic")

**User Story 4.1.2:** As an analyst, I want to run our firm's methodology against a client's data and get a diagnostic report in under 2 minutes, so that I can iterate quickly with the partner on recommendations.

**Acceptance Criteria:**
- **Given** a published methodology and a client's structured data input
- **When** I trigger a diagnostic run
- **Then** the engine executes all applicable rules
- **And** scores are calculated deterministically (same input → same output every time)
- **And** an LLM-generated explanation accompanies each flagged issue (why it matters, typical remediation)
- **And** the full report is generated as PDF + interactive dashboard
- **And** total runtime is under 2 minutes for a methodology of 200+ rules

### 4.2 Epic: Client Dashboard (Ongoing Monitoring)

**User Story 4.2.1:** As a client (e.g., a CEO who engaged a consulting firm), I want to see my company's diagnostic scores updated monthly without needing a new consulting engagement, so that I track progress against the firm's recommendations.

**Acceptance Criteria:**
- **Given** a client account provisioned by the consulting firm
- **When** new monthly data is uploaded (either by the client or via API integration with their ERP)
- **Then** the diagnostic re-runs automatically
- **And** the client dashboard shows score changes vs prior period
- **And** recommendations marked "addressed" are tracked for effectiveness
- **And** the client receives an email summary with changes highlighted
- **And** the client can drill into any score but cannot see the raw rule logic (IP protection)

### 4.3 Epic: Methodology Library and White-Labeling

**User Story 4.3.1:** As a consulting firm partner, I want to white-label the platform with our firm's branding so that clients see our brand, not "BSD Engine," and our methodology is presented as our product.

**Acceptance Criteria:**
- **Given** a consulting firm subscription
- **When** they customize the white-label settings
- **Then** they can configure: logo, color palette, domain name (CNAME), PDF report template, email templates
- **And** clients see the firm's branding throughout
- **And** "Powered by BSD Engine" footer is removable at Enterprise tier
- **And** the firm's name appears as methodology author

### 4.4 Epic: REPL-Driven Methodology Development

**User Story 4.4.1:** As a consulting firm's methodology architect, I want to explore client data interactively via REPL and incrementally build rules, so that my methodology development workflow matches how Clojure developers actually build software.

**Acceptance Criteria:**
- **Given** an authenticated methodology architect
- **When** they open the Analyst BFF's integrated REPL
- **Then** they have a live Clojure REPL with access to current client data (read-only)
- **And** they can query data, develop rules interactively, and see results immediately
- **And** rules they develop can be saved, versioned, and promoted to the main methodology
- **And** the REPL runs in a sandboxed environment (no filesystem, no network, CPU-limited)

### 4.5 Epic: Integration with Existing Rust Scoring Engine

**User Story 4.5.1:** As a system operator, I want the existing Rust scoring engine (from BSD v1) to remain the fast-path for numeric scoring while Clojure handles the rules DSL and interpretation, so that we benefit from both performance and expressiveness.

**Acceptance Criteria:**
- **Given** a methodology with both rule-based logic (Clojure) and numeric scoring (Rust)
- **When** the engine runs a diagnostic
- **Then** Clojure compiles rules to a deterministic execution plan
- **And** numeric-heavy scoring is delegated to the existing Rust scoring engine via gRPC
- **And** Clojure orchestrates; Rust computes
- **And** the split is invisible to the user
- **And** total runtime benefits from Rust's speed on hot paths

---

## 5. Non-Functional Requirements

### 5.1 Performance

| Metric | Target |
|--------|--------|
| Diagnostic run (200 rules, 1,000 data points) | < 2 minutes |
| Rule compilation (DSL → execution plan) | < 30 seconds |
| REPL evaluation (simple query) | < 500ms |
| PDF report generation | < 30 seconds |
| Dashboard page load | < 2 seconds |

### 5.2 Determinism and Reproducibility

- **Same input → same output, always.** No randomness, no external state.
- **Full audit trail:** Every diagnostic run logs version of methodology, version of input data, computed scores, timestamp.
- **Reproducibility:** Any past diagnostic can be re-run and produce identical results.
- **LLM explanations:** Cached per-result to ensure stability across views of the same diagnostic.

### 5.3 Availability

| Component | Target |
|-----------|--------|
| Analyst BFF (methodology authoring) | 99.5% (business hours) |
| Client Dashboard | 99.9% |
| Consultant BFF | 99.9% |
| Rule execution engine | 99.99% (diagnostics must complete) |

### 5.4 Security

- **Authentication:** OIDC (Auth0 or Keycloak); SAML for enterprise regulators
- **Authorization:** Multi-tenant; methodology IP isolated per consulting firm; client data isolated per engagement
- **IP protection:** Rules stored encrypted at rest; executed in sandbox; rule text never returned to client dashboard
- **Audit logging:** Every rule edit, every diagnostic run, every client data upload logged
- **Compliance:** Kenya DPA; GDPR-equivalent for EU regulator clients; SOC 2 Type I by end of Year 1

### 5.5 Scalability

- Support 50+ consulting firms on shared multi-tenant infrastructure
- Each firm can have 100+ methodologies and 1,000+ client engagements
- Rule execution horizontally scalable (stateless workers)
- Event store partitioned by tenant

### 5.6 Observability

- Per-tenant dashboards for the consulting firms
- Platform-wide dashboards for Shamba operators
- Anomaly detection on diagnostic runs (drastic score shifts flagged for review)
- Rule execution performance monitoring (slow rules highlighted for optimization)

---

## 6. Success Metrics

### 6.1 Business Metrics (End of Week 15)

| Metric | Target |
|--------|--------|
| Paying consulting firms | 2 |
| Active methodologies in production | 5+ |
| Total client engagements monitored | 20+ |
| Monthly Recurring Revenue | $400+ |

### 6.2 Product Metrics

| Metric | Target |
|--------|--------|
| Time from signup to first diagnostic | < 5 business days |
| Methodology authoring time (20-rule methodology) | < 10 hours |
| Client dashboard usage (monthly active users per client) | > 40% |
| LLM explanation quality (thumbs-up rate) | > 70% |

### 6.3 Technical Metrics

| Metric | Target |
|--------|--------|
| Diagnostic execution reliability | > 99.9% (runs complete successfully) |
| Determinism verification | 100% (automated tests verify reproducibility) |
| Rule DSL expressiveness (rules written vs rules attempted) | > 95% (rare cases escape to custom code) |

---

## 7. Architecture Mapping

### 7.1 Primary Pattern Introduced: Functional Core / Imperative Shell + Macro DSLs

BSD Engine v2 is the archetypal functional core: diagnostic rules are pure functions from data to scores. The shell (imperative I/O, database, HTTP, LLM calls) surrounds the core but is cleanly separated. Clojure's macros enable a DSL that compiles to the pure core.

**Compounding patterns from prior tiers:**
- **BFF pattern (Tier 1):** 3 BFFs — Analyst (rule authoring), Client Dashboard (view-only), Consultant (methodology mgmt)
- **Event-driven (Tier 1):** Every rule edit, every diagnostic run emits events; event log is source of truth
- **CQRS (Tier 2):** Rule edits are commands; diagnostics read from projections
- **Event Sourcing (Tier 2):** Methodology versioning via events
- **Hexagonal (Tier 4):** Clojure core, adapters for HTTP, database, LLM calls, Rust engine integration
- **Actor model (Tier 5a):** Rule execution runs on Clojure's `core.async` channels + BEAM-style process-per-diagnostic (mapped to JVM threads)

### 7.2 The DSL Design

**Rule Example (Clojure EDN):**
```clojure
(defrule unsustainable-unit-economics
  {:severity :high
   :category :financial-health
   :description "Customer acquisition cost exceeds sustainable multiple of customer lifetime value"}
  [:when
   (< (:revenue-growth data) 0.05)
   (> (:cac data) (* 3.0 (:ltv data)))]
  [:then
   {:flag :unsustainable-unit-economics
    :evidence [(:cac data) (:ltv data) (:revenue-growth data)]
    :severity :high
    :remediation-hints [:review-acquisition-channels :improve-retention :increase-pricing]}])
```

**Why Clojure as DSL host:**
- Homoiconicity: rules ARE data; trivial to store, version, and transform
- Macros let us create syntax that reads naturally to business users without parsing hell
- Immutability ensures determinism
- REPL is a first-class authoring tool

### 7.3 The Three BFFs

| BFF | Client | Technology | Key Responsibilities |
|-----|--------|------------|---------------------|
| Analyst BFF | Web app with REPL | ClojureScript + Re-frame | Rule authoring, REPL, methodology management |
| Client Dashboard BFF | Web app (client-facing) | ClojureScript + Re-frame | View diagnostics, track progress, download reports |
| Consultant BFF | Web app (firm admin) | Clojure Ring + Reitit | Firm management, client provisioning, billing, white-label config |

### 7.4 Integration with Rust Scoring Engine (from v1)

The existing Rust/PyO3 scoring engine from BSD v1 is preserved and exposed as a gRPC service. Clojure calls it for:
- Heavy numeric computation (time series, statistical tests)
- ML-based scoring (XGBoost, random forests)
- Large dataset transformations

The split:
- **Clojure:** Rule orchestration, DSL compilation, LLM calls, event logging, user-facing logic
- **Rust:** Raw numeric scoring, ML inference, data transformations at scale

### 7.5 LLM Integration (Explanation Layer)

- LLM calls are adapter implementations (hexagonal port: `ExplanationService`)
- Inputs: flagged rule, evidence data, severity, methodology context
- Outputs: human-readable explanation in the consultant's voice (tone calibrated via system prompt)
- Caching: Per-(rule, evidence-hash) to keep explanations stable
- Providers: Gemini (default for cost), OpenAI (fallback), Anthropic (enterprise tier)

### 7.6 Technology Stack

**Backend:**
- Clojure 1.12 (core engine, BFFs)
- ClojureScript (Analyst BFF frontend)
- Re-frame (ClojureScript state management)
- Reitit (Clojure routing)
- Malli (schema validation)
- Rust (existing scoring engine, unchanged)

**Data:**
- PostgreSQL (tenant data, methodology storage, client engagements)
- Datomic or XTDB (rule version history — event-sourced by design)
- Redis (session, caching)
- S3 (PDF reports, exported data)

**Integrations:**
- Gemini/OpenAI/Anthropic APIs (explanation layer)
- Stripe / Paystack (billing)
- SendGrid (email)

**Infrastructure:**
- AWS (us-east-1 primary)
- Kubernetes (EKS)
- JVM-optimized nodes for rule execution workers

---

## 8. Phased Rollout Plan

### 8.1 MVP (Week 12)

**Scope:**
- Clojure DSL compiler operational (basic predicates, severity, flagging)
- Analyst BFF with rule editor + REPL
- One full methodology encoded (migrated from BSD v1 or new)
- Client dashboard with PDF export
- 1 consulting firm in pilot

**Commercial goal:** 1 paid consulting firm signed; 5 client engagements running.

### 8.2 v1.0 (Week 15)

**Scope:**
- White-labeling
- Rust scoring engine integration
- LLM explanation layer
- Multi-methodology support per firm
- 2 paying firms

**Commercial goal:** $400+ MRR

### 8.3 v1.5 (Months 4-5 post-sprint)

- Regulator tier (CBK pilot)
- API for client system integration (auto-data-feed)
- Methodology marketplace (firms can license methodologies to each other)
- Mobile client dashboard app

### 8.4 v2.0 (Year 2)

- Industry-specific methodology packs (banking, retail, manufacturing, healthcare)
- Advanced analytics (cohort tracking, benchmarking)
- Academic research partnerships (validated diagnostic methodologies published)

---

## 9. Commercial Terms

### 9.1 Pricing Tiers

| Tier | Price | Features | Target |
|------|-------|----------|--------|
| **Starter** | $199/mo | 1 methodology, 5 clients, basic explanations | Small boutiques |
| **Professional** | $999/mo | 5 methodologies, 50 clients, white-labeling, priority support | Mid consulting firms |
| **Agency** | $2,999/mo | Unlimited methodologies, 500 clients, API access, dedicated explanation models | Large consulting firms |
| **Enterprise / Regulator** | From $4,999/mo | Custom deployment, on-premises option, SLAs, custom DSL extensions | Regulators, pan-African corporates |
| **Methodology license fee** | 20% markup on methodology | Optional add-on | Firms licensing methodologies to each other |

### 9.2 Customer Acquisition

- **Direct outreach:** Known Nairobi consulting network, pan-African professional services firms
- **Partnerships:** Strathmore Business School, AMI (African Management Institute) — these produce consultants
- **Content marketing:** Technical blog on diagnostic methodology digitization; case studies
- **Speaking:** African Management Institute conferences, Strathmore events
- **Regulatory sales:** Direct engagement with CBK, Communications Authority via policy network

---

## 10. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|-----------|
| Clojure adoption too niche for enterprise sales | Medium | Medium | Hide Clojure behind UI; enterprise clients never see it. "Powered by" not required. |
| Consulting firms resistant to systematizing their IP | High | Medium | Position as "IP protection and scaling tool," not "we'll replace your consultants" |
| LLM explanation errors undermine trust | Medium | High | Explanations reviewable before publishing; audit trail; easy flag-and-improve workflow |
| Rule DSL complexity limits non-technical consultants | Medium | Medium | Build visual rule-builder UI on top of DSL; "no-code" wraps the code |
| Determinism fails due to LLM variability | Low | High | Cache all LLM outputs; enforce deterministic re-runs return cached explanation |

---

## 11. Open Questions

1. Should methodology authoring be visual (drag-drop) or code (DSL)? **Answer:** Both — DSL primary, visual layer on top for junior analysts.
2. How do consulting firms share methodologies with other firms? **Answer:** Methodology marketplace in v1.5; revenue share via platform.
3. Should clients be able to run diagnostics without the consulting firm in the loop? **Answer:** Only at the firm's discretion; clients pay consulting firm, firm pays platform.
4. What's the competitive moat vs a well-funded US SaaS vendor entering this space? **Answer:** African consulting methodologies, local regulatory knowledge, African data residency, Swahili/French UI support.

---

## 12. Appendix: Definition of Done for v1.0

- [ ] All user stories in Section 4 have passing acceptance tests
- [ ] DSL compiler handles 95%+ of real methodology cases
- [ ] Determinism verified by automated regression tests (1,000+ runs)
- [ ] 2 consulting firms in production, $400+ MRR
- [ ] White-labeling works end-to-end (custom domain, branding, reports)
- [ ] LLM explanation quality > 70% thumbs-up rate
- [ ] Rust scoring engine integration live
- [ ] Security audit passed
- [ ] Documentation: DSL reference, methodology authoring guide, consultant guide
- [ ] On-call rotation active
