# PRD — PayGoHub v2

> **Version:** 2.0
> **Date:** April 2026
> **Status:** Draft — Approved for Sprint Weeks 13-14 (Capstone)
> **Owner:** Eric Gitangu (Deveric Technologies)
> **Tier:** 6 (C# + F#)
> **Project Type:** Major Extension of Shipped App; Sprint Capstone
> **Existing system:** PayGoHub (ASP.NET Core + PostgreSQL + Azure; Eric's internal exploration project)

---

## 1. Executive Summary

**PayGoHub v2** is the capstone project of the 15-week sprint — the application that **composes all 14 architectural patterns** developed across Tiers 1-5 into a single, production-grade, commercializable system. It is a **white-label PAYG (Pay-As-You-Go) solar energy management platform** targeting mid-size African utilities and solar distributors who need enterprise-grade infrastructure but cannot afford Atlas, Q-Energy, or similar international solutions.

The v1 PayGoHub explored the domain as an individual's study project. The v2 transforms it into a commercial product. The domain matches Eric's prior work at Ignite/ENGIE precisely — but this version demonstrates that the architectural third eye developed across the sprint produces a categorically better system than v1 could.

**Commercial thesis:** Africa has 300+ PAYG solar distributors, each serving 10,000-2M customers. Incumbent software (Angaza, Paygops, Solaris) is expensive and foreign. A purpose-built African platform with Azure-native architecture (aligning with Eric's Solvo Global interview target) can capture the mid-market. Pricing: $10K-$50K setup + $0.10-$0.50 per active customer per month.

**Architectural thesis:** This project demonstrates DDD (Domain-Driven Design) bounded contexts composed with Railway-Oriented Programming (F#) for all validation flows, sitting on top of a service mesh, with CQRS/ES, sagas, hexagonal boundaries, CRDTs for field apps, OTP-style supervision for device fleet management, and a DSL for tariff rules. Every pattern from Tiers 1-5 finds its natural expression.

---

## 2. Problem Statement

### 2.1 The Pain

1. **PAYG solar distributors outgrow their initial software stack.** Small distributors start on Excel; mid-size ones graduate to Angaza or Paygops (international, expensive); the largest build in-house. There's no well-engineered middle tier.

2. **Existing software is expensive AND doesn't fit African operational patterns.** Angaza subscriptions run $1-$3 per customer per month for companies with 1% net margins. Distributor agents want offline-capable mobile apps; foreign software often assumes connectivity.

3. **Integration with device fleets is fragmented.** Each hardware manufacturer (D.Light, Greenlight Planet, Sun King, Zola) has their own tokenization protocol and fleet management API. Distributors using multiple device types juggle 3-5 integration layers.

4. **Call center operations are manual.** When a customer can't pay, needs tech support, or has a device problem, call center agents pull up 3+ tools. Voice AI (from Sauti) could massively improve this — but current platforms don't integrate it.

5. **Regulatory reporting is painful.** Kenya's Energy and Petroleum Regulatory Authority (EPRA) requires PAYG operators to report periodically. Pulling this from existing platforms is a manual extraction job.

6. **Pricing/tariff engineering is rigid.** A distributor wanting to test a new tariff (e.g., "pay-less-for-the-first-30-days") has to file a support ticket with their software vendor. Should be config; is code.

### 2.2 Quantified Market

- **African PAYG solar distributors:** 300+ active companies across 35 countries
- **Customer base served by PAYG solar:** 35M+ people with PAYG-deployed devices
- **Mid-market target (10K-500K customers each):** ~150 distributors globally
- **Revenue math:** Capture 20 mid-market distributors at $25K setup + $2K-$10K MRR average = $400K setup + $100K MRR within 2-3 years

### 2.3 Why Now

- Africa's PAYG solar market is still growing (~15-20% annually) but consolidating (big players acquiring small)
- Azure adoption is increasing in African corporate IT (alignment with banks, telcos, government tender requirements)
- Voice AI (Sauti) and deterministic rule engines (BSD Engine v2) provide genuine differentiation vs incumbents
- Eric's Ignite/ENGIE network provides warm introductions to 10+ distributors

---

## 3. Target Users & Personas

### 3.1 Primary Persona: PAYG Distributor COO

**Name:** Michael, 46, Kampala (Uganda)
**Role:** COO of a PAYG solar distributor serving 80,000 active customers with 5 hardware suppliers
**Goals:**
- Reduce customer default rate (currently 12%; industry average 8%)
- Cut call center cost per contact (currently $1.20; target $0.50)
- Launch new tariff structures without engineering tickets
- Integrate new device manufacturers in weeks, not months

**Pain points:**
- Current software (Angaza) is expensive and slow to evolve
- Can't easily run A/B tests on collection strategies
- Regulatory reporting takes 4 days/quarter of manual work
- Integration with 5th hardware supplier took 6 months

**Jobs-to-be-done:** Replace Angaza with a platform he can configure and extend, at half the cost.

### 3.2 Secondary Persona: Field Installer

**Name:** Lilian, 28, Mbarara (Uganda)
**Role:** Installer who deploys 8-15 systems per day across rural areas
**Goals:**
- Quick customer onboarding (under 15 min including KYC, device pairing, first payment)
- Work offline; sync when back in coverage
- Get paid commission accurately and promptly

**Pain points:**
- Current app crashes when she loses connectivity
- Customer onboarding takes 30+ minutes; some customers walk away
- Her commission isn't calculated until month-end; she doesn't know what she's earning

**Jobs-to-be-done:** Fast offline-capable onboarding with real-time commission tracking.

### 3.3 Tertiary Persona: Call Center Agent

**Name:** Peter, 32, Nairobi
**Role:** Call center agent for a PAYG distributor's customer service line
**Goals:**
- Handle customer calls faster while maintaining quality
- Access customer info in one screen, not five
- Record call outcomes accurately for follow-up

**Pain points:**
- Uses 5 different tools during a single call
- Average call is 8 minutes; targeting 5
- Can't serve Swahili-speaking customers efficiently (language barriers)

**Jobs-to-be-done:** Unified agent desktop with Sauti-powered voice transcription and sentiment monitoring.

### 3.4 Quaternary Persona: Utility Partner

**Name:** Rural Electrification Authority
**Role:** Distributes subsidies for clean energy access
**Goals:**
- Track subsidy program effectiveness
- Verify subsidized customers are real (anti-fraud)
- Report on program outcomes to donors

**Jobs-to-be-done:** API access to aggregated, anonymized customer and usage data for program monitoring.

### 3.5 Non-Target Users (Explicit)

- **Grid utilities** (Kenya Power, Uganda Electricity) — different domain, different regulations
- **Micro-grid operators** — adjacent domain; could be v3 expansion
- **Consumer-direct startups** without field operations — too different an operating model

---

## 4. User Stories & Acceptance Criteria

### 4.1 Epic: Customer Onboarding

**User Story 4.1.1:** As a field installer, I want to onboard a new customer (KYC, device pairing, financing, first payment) in under 15 minutes including offline scenarios, so that I complete more installations per day.

**Acceptance Criteria:**
- **Given** a field installer with the mobile PWA and a new customer
- **When** they initiate a new installation
- **Then** KYC capture (photo ID, selfie, GPS, basic details) completes in under 5 minutes
- **And** device pairing (enter serial, pair with physical unit) completes in under 2 minutes
- **And** financing plan is selected from pre-approved templates
- **And** first payment is collected via M-Pesa
- **And** the entire flow works offline (syncs when connectivity returns)
- **And** the customer receives SMS confirmation within 5 minutes of connectivity
- **And** installer commission accrues in real-time on their dashboard

### 4.2 Epic: Metering and Payment Allocation

**User Story 4.2.1:** As a customer, I want my M-Pesa payment to unlock my solar system's tokens within 60 seconds, so that my family has light/charging tonight without waiting.

**Acceptance Criteria:**
- **Given** a customer with an active PAYG system and outstanding balance
- **When** the customer pays via M-Pesa
- **Then** the webhook is processed within 10 seconds
- **And** the payment allocation saga runs (allocate to principal → interest → fees → compute new unlock duration)
- **And** tokens are generated deterministically from the payment amount
- **And** tokens are dispatched to the customer's device (via SMS or IoT API depending on device type)
- **And** the customer's SMS confirmation includes the new unlock period (e.g., "Your Sun King is now on for 14 days")
- **And** the whole flow completes in under 60 seconds

### 4.3 Epic: Multi-Manufacturer Device Fleet

**User Story 4.3.1:** As a platform operator, I want to integrate a new hardware manufacturer in under 4 weeks, so that distributors can expand their device portfolio quickly.

**Acceptance Criteria:**
- **Given** a new device manufacturer with documented tokenization and fleet APIs
- **When** I add an integration
- **Then** the integration lives in a hexagonal adapter (no changes to core)
- **And** the manufacturer-specific tokenization logic lives in a dedicated module
- **And** device-specific fleet management (firmware updates, diagnostics) is exposed via a unified port
- **And** end-to-end test exercises the full flow for the new manufacturer
- **And** the integration can be rolled out to specific distributors via feature flag

### 4.4 Epic: Tariff DSL

**User Story 4.4.1:** As a distributor's product manager, I want to define new tariff structures in a business-readable DSL and A/B test them, without engineering involvement, so that I can experiment with commercial strategies quickly.

**Acceptance Criteria:**
- **Given** a product manager with access to the Partner BFF's tariff editor
- **When** they define a new tariff (e.g., "first 30 days free, then $0.50/day unlock with $15 device cost amortized over 12 months")
- **Then** the DSL (F#-based) validates the tariff for mathematical consistency
- **And** the PM can simulate the tariff against historical customer data (what would this have charged them?)
- **And** the PM can activate the tariff for a specified cohort (e.g., 10% of new customers in Uganda)
- **And** the A/B test runs deterministically; results are comparable after 30 days
- **And** the PM can roll the tariff back without code deployment

### 4.5 Epic: Unified Call Center Agent Desktop

**User Story 4.5.1:** As a call center agent, I want one screen that shows everything about the calling customer, with live Sauti transcription and sentiment scoring, so that I handle calls in 5 minutes instead of 8.

**Acceptance Criteria:**
- **Given** a call center agent with Call Center BFF open
- **When** an inbound call from a known customer arrives
- **Then** the customer's full profile auto-loads in under 2 seconds (balance, payment history, device status, recent contacts)
- **And** Sauti live transcription appears in the same view (integration with Sauti platform — see PRD 01)
- **And** sentiment score updates every 10 seconds
- **And** suggested next actions appear based on the call context (e.g., "customer balance is KES 500 short; offer 7-day grace period")
- **And** call outcome is captured with one click and feeds the customer profile

### 4.6 Epic: Regulator Reporting

**User Story 4.6.1:** As a compliance officer, I want EPRA (and equivalent regulators in other countries) quarterly reports generated automatically from platform data, so that quarter-end isn't a 4-day manual project.

**Acceptance Criteria:**
- **Given** a distributor configured with regulatory reporting rules
- **When** the reporting period ends (e.g., end of Q2)
- **Then** the system aggregates required data per regulator's format
- **And** generates the report as Excel + PDF
- **And** includes cryptographic signature proving data integrity
- **And** compliance officer reviews, approves, submits
- **And** the full process takes under 4 hours (vs 4 days previously)

---

## 5. Non-Functional Requirements

### 5.1 Performance

| Metric | Target |
|--------|--------|
| Payment webhook processing (P95) | < 5s |
| Token generation and dispatch (P95) | < 60s end-to-end |
| Field installer onboarding | < 15 min |
| Call center customer load | < 2s |
| Tariff simulation (against 10,000 customers) | < 30s |
| Regulator report generation | < 4 hours |

### 5.2 Availability

| Component | Target |
|-----------|--------|
| Customer-facing BFFs (USSD, SMS, mobile) | 99.95% |
| Payment processing core | 99.99% (financial) |
| Device fleet management | 99.9% |
| Call Center BFF | 99.95% (agent productivity) |
| Regulator BFF | 99.5% (periodic use) |

### 5.3 Security

- **Authentication:** OIDC + MFA for all internal users; customer-facing flows via SIM-authenticated USSD/SMS and app-level OAuth
- **Authorization:** Multi-tenant distributor isolation; row-level security throughout
- **Device security:** Tokens signed with HSM-stored keys; per-distributor signing keys
- **PCI DSS SAQ-A:** No card data stored; mobile money integrations use official APIs
- **Compliance:** Kenya DPA, Uganda DPA equivalents, GDPR for EU partner data; SOC 2 Type I target Year 2
- **Audit logging:** Event-sourced throughout; every domain event immutably logged

### 5.4 Scalability

- Support 20+ distributor tenants on shared infrastructure
- Each distributor up to 500K active customers
- Horizontal scaling of all stateless services
- Device fleet management can supervise 5M+ connected devices

### 5.5 Regulatory Compliance

- **Data residency:** Kenya customer data in Kenya (Azure South Africa North or local); Uganda data in appropriate region
- **Retention:** 7 years for financial records; 3 years for call recordings with consent
- **Reporting:** Automated generation for EPRA (Kenya), ERA (Uganda), ENEE (Honduras), others as onboarded

### 5.6 Observability

- Full distributed tracing (OpenTelemetry → Azure Monitor)
- Per-tenant dashboards in Grafana (hosted or Azure-native)
- Business SLIs: onboarding success rate, payment allocation accuracy, token dispatch latency
- Platform SLIs: service mesh health, database latency, event store write rate
- Alerting: PagerDuty for P0/P1; Slack for P2/P3

---

## 6. Success Metrics

### 6.1 Business Metrics (End of Week 15 / Sprint End)

| Metric | Target |
|--------|--------|
| Paying distributor tenants | 1 (the capstone customer) |
| Pilot conversations in progress | 3 |
| Monthly Recurring Revenue | $500+ (from first paid tenant) |
| End-of-sprint credibility artifact | Production-grade platform powering real customer PAYG operations |

### 6.2 Architectural Metrics (Sprint Synthesis)

| Metric | Target |
|--------|--------|
| Bounded contexts implemented | 6 (matches DDD capstone) |
| Architectural patterns composed | 14 (all from prior tiers integrated) |
| Service mesh coverage | 100% of inter-service calls |
| Event-sourced contexts | 6 (all) |
| Railway-oriented validation paths | All major flows |
| F# modules for DSLs and scheduling | 3+ (tariff DSL, scheduling, ROP validation) |

### 6.3 Technical Quality Metrics

| Metric | Target |
|--------|--------|
| Test coverage on domain logic | > 90% |
| CI/CD pipeline green rate | > 95% |
| Security audit findings | 0 critical; 0 high |
| Cost per customer per month (platform overhead) | < $0.05 |

---

## 7. Architecture Mapping

### 7.1 Primary Pattern Introduced: DDD (Domain-Driven Design) + Railway-Oriented Programming (ROP)

PayGoHub v2 is the textbook DDD implementation, bounded contexts defined rigorously, ubiquitous language consistent, aggregates enforcing invariants. F# provides ROP for every validation and workflow composition — every cross-boundary call is a `Result<Success, Error>` chain. The code reads like a specification.

**All Prior Patterns Composed (this is the capstone):**

| Tier | Pattern | Usage in PayGoHub v2 |
|------|---------|---------------------|
| 1 | BFF pattern | 5 distinct BFFs |
| 1 | Event-driven architecture | Domain events between every bounded context via Azure Service Bus |
| 2 | CQRS | Command side in C#, query side optimized per consumer |
| 2 | Event Sourcing | Every financial transaction event-sourced for audit |
| 2 | Sagas | Payment allocation, device provisioning, subsidy claim processing |
| 3 | CRDTs | Field installer offline app; merge conflict-free with server |
| 3 | Offline-first | Field ops and call center work through connectivity drops |
| 4 | Hexagonal | All 6 bounded contexts structured as ports + adapters |
| 4 | Service Mesh | Full Linkerd mesh with mTLS + tracing |
| 5a | Actor Model / Supervision | Device fleet management (one process per device, OTP-style via Orleans) |
| 5b | Functional Core / Imperative Shell | F# modules for tariff calculation, scheduling |
| 5b | Macro DSLs | Tariff DSL (F# computation expressions) |
| 6 | DDD | Primary organizing principle |
| 6 | Railway-Oriented Programming | All validation + workflow composition |

### 7.2 The Six Bounded Contexts

| Context | Responsibility | Primary Tech |
|---------|---------------|--------------|
| **Customer** | Identity, KYC, lifecycle, consent management | C# / EF Core |
| **Installation** | Field onboarding, device pairing, installer management | C# + F# validation |
| **Metering** | Device state, token generation, fleet management | F# + Orleans (actor model) |
| **Payments** | M-Pesa integration, payment allocation, wallets | C# + F# (ROP for allocation) |
| **Tariffs** | Tariff DSL, pricing, A/B tests | F# (computation expressions) |
| **Partners** | Distributor admin, regulator reporting, subsidy programs | C# |

Each context has its own domain model, aggregate roots, commands, events, and anti-corruption layers protecting it from neighboring contexts.

### 7.3 The Five BFFs

| BFF | Client | Technology | Key Responsibilities |
|-----|--------|------------|---------------------|
| Customer BFF | Mobile app + USSD + SMS | C# (ASP.NET Core Minimal APIs) | Balance, payment history, device status, support requests |
| Installer BFF | Field PWA (offline-first) | C# + CRDTs via Yjs | Onboarding, device pairing, commission tracking |
| Call Center BFF | Agent desktop web app | C# + Blazor Server (real-time) | Customer context, Sauti integration, call disposition |
| Partner BFF | Distributor admin web | C# + Blazor WASM | Tariff management, reporting, analytics |
| Regulator BFF | Regulator portal | C# + static Razor Pages | Read-only access to aggregate data, report downloads |

### 7.4 F# Usage (Where and Why)

**F# Module 1: Tariff Engine**
- Computation expressions encode tariff structures
- Type system prevents mathematical inconsistencies at compile time
- Interop with C# via clean module boundaries

**F# Module 2: Validation (ROP)**
- All incoming commands validated via Result chains
- Errors accumulated and returned as structured data
- Zero exceptions in validation path; error cases are first-class

**F# Module 3: Scheduling**
- Token expiration scheduling
- Commission payout scheduling
- Regulator reporting cadence

**Why F# for these, C# for the rest:**
- F# is sharper for DSL and pure-computation work; C# is sharper for CRUD and infrastructure
- The split teaches the right tool for the right job, a core "third eye" lesson

### 7.5 Sauti Integration (Cross-Project Synergy)

PayGoHub v2 integrates Sauti (PRD 01) at the Call Center BFF:
- Incoming calls transcribed via Sauti in real-time
- Sentiment scores update the agent's UI
- Suggested actions use transcripts + customer context
- This demonstrates the sprint's conglomerate thesis — apps reinforcing each other

### 7.6 LendStream Integration (Credit Underwriting as a First-Class Capability)

PayGoHub v2 treats **credit underwriting as a first-class bounded context**, implemented as a LendStream integration rather than a rebuilt lending stack. This is the sprint's most concrete demonstration of the conglomerate thesis: two products in the portfolio reinforcing each other at the architectural level, not just in marketing decks.

**The commercial problem being solved:** PAYG distributors operate with thin margins and high default risk. Currently, most distributors approve financing based on thin heuristics (does the applicant own a phone? have they paid a deposit?). They have no real credit model. LendStream has the scoring engine, the event-sourced audit trail, and the CBK-compliant lending infrastructure. PayGoHub needs underwriting; LendStream has it.

**Integration architecture:**

**Anti-Corruption Layer (ACL):** PayGoHub's `Payments` and `Installation` contexts talk to LendStream through an anti-corruption layer that translates between PayGoHub's domain language ("financing plan," "device amortization," "tariff") and LendStream's ("loan product," "repayment schedule," "interest accrual"). This is DDD in action — two bounded contexts, one shared kernel, no leakage of vocabulary.

**Flows routed through LendStream:**

| Flow | Who handles it | Why |
|------|----------------|-----|
| Basic PAYG tokenization ($0.50/day unlock) | PayGoHub Tariff context | Simple; no credit decision required |
| Device financing (customer pays for the unit over 12 months) | LendStream underwriting + PayGoHub collections | Real credit decision; regulatory loan |
| Bundle financing (solar + TV + fan) | LendStream | Larger amounts; full underwriting required |
| Installer commission advances | LendStream (as micro-lender) | Short-term advances; LendStream's domain |
| Distributor working capital loans | LendStream | Enterprise B2B lending |
| Subsidy-backed financing (REA, donor programs) | Hybrid (LendStream processes; PayGoHub records subsidy side) | Complex multi-party settlement |

**Technical integration:**

- **gRPC contract** between PayGoHub `Payments` and LendStream `Scoring` contexts (typed, versioned, code-generated from a shared `.proto`)
- **Event bridge** via Azure Service Bus topics: PayGoHub publishes `CustomerRequestedFinancing`, LendStream publishes `LoanOriginated` / `LoanRejected`, PayGoHub projects back
- **Shared identity**: Customer IDs reconciled via the Customer context as system of record; LendStream tracks them as `external_customer_id`
- **Shared audit trail**: Both platforms event-source; a compliance query can span both event stores via the Customer ID
- **Data sovereignty**: PayGoHub stays on Azure (customer alignment); LendStream stays on AWS (existing stack). Cross-cloud is fine at event-bus boundaries; never in the hot path.

**Commercial upside of the integration:**

- PayGoHub distributors get a CBK-compliant underwriting engine without building it
- LendStream gets 20+ new B2B customers (each PAYG distributor's book becomes a new LendStream tenant)
- Shared data improves credit models (PAYG repayment history is predictive for cash loans; cash loan history is predictive for device financing)
- One sales conversation with a distributor can result in two subscriptions

**Sprint implementation:**

- Weeks 13-14 (Tier 6): PayGoHub ACL + gRPC contract + one end-to-end financing flow
- Week 15: Full flow tested; first distributor pilot exercises both systems
- Post-sprint: Full product catalog migrated to LendStream underwriting

### 7.7 Azure Stack (Alignment with Solvo Global Interview)

This project uses Azure-native components to match Eric's Solvo Global interview target stack:
- **App hosting:** Azure App Service + AKS
- **Event bus:** Azure Service Bus
- **Event store:** Azure Cosmos DB (event log container)
- **Query projections:** Azure SQL Database
- **Key storage:** Azure Key Vault
- **Observability:** Azure Monitor + Application Insights
- **CI/CD:** Azure DevOps Pipelines
- **Identity:** Azure AD B2C for customer auth; Azure AD for internal users
- **Messaging:** Azure Communication Services for SMS (secondary to Africa's Talking)

Rationale: Eric's Solvo Global interview was for a .NET/C#/React/Azure role; the capstone project demonstrates direct competence on that stack.

### 7.8 Full Technology Stack

**Backend:**
- C# 12 + .NET 8 (primary language)
- F# 8 (DSL, validation, pure domain)
- Microsoft Orleans (actor model for device fleet)
- MediatR (in-process messaging)
- MassTransit (service-bus integration)

**Data:**
- Azure SQL Database (projections, transactional data)
- Cosmos DB (event store, large scale)
- Redis (sessions, caching)
- Blob Storage (documents, reports)

**Integrations:**
- M-Pesa Daraja APIs
- Manufacturer device APIs (D.Light, Greenlight Planet, Sun King, Zola, PayGo)
- Africa's Talking (SMS, USSD)
- Sauti (from PRD 01; voice AI)

**Infrastructure:**
- Azure (primary, per interview alignment)
- AKS (Kubernetes)
- Linkerd (service mesh)
- Azure DevOps Pipelines
- Terraform for IaC

**Frontend:**
- Blazor Server (call center, real-time)
- Blazor WASM (distributor admin)
- Next.js + TypeScript (customer-facing mobile PWA, shared patterns with Sauti/Sherehe)

---

## 8. Phased Rollout Plan

### 8.1 MVP (Week 14, end of Tier 6 sprint)

**Scope:**
- All 6 bounded contexts implemented with DDD structure
- Customer BFF and Installer BFF operational
- M-Pesa integration live
- One device manufacturer integration (D.Light or similar)
- Tariff DSL operational with 3-5 default tariffs
- 1 distributor onboarded for pilot

**Commercial goal:** 1 pilot distributor, paying or committed to paying.

### 8.2 v1.0 (Week 15 + Week 16 integration week)

**Scope:**
- All 5 BFFs operational
- Sauti integration live (call center)
- LendStream integration live (lending flows)
- Multi-device manufacturer support
- 1 paid distributor tenant

**Commercial goal:** $500+ MRR; 3 more pilots in discussion.

### 8.3 v1.5 (Months 4-6 post-sprint)

**Scope:**
- Regulator reporting for Kenya (EPRA), Uganda (ERA)
- Subsidy program management module
- 3+ paying distributors
- $3K+ MRR

### 8.4 v2.0 (Year 2)

- Pan-African expansion (10+ country regulator support)
- White-label mobile app builder
- Marketplace for accessory financing (fans, radios, TVs bundled with solar)
- $20K+ MRR target

---

## 9. Commercial Terms

### 9.1 Pricing

| Tier | Setup | Monthly | Per-Customer | Features |
|------|-------|---------|--------------|----------|
| **Pilot** | $5,000 | $500 | $0.25 | Up to 5,000 customers, core features |
| **Growth** | $15,000 | $1,500 | $0.20 | Up to 50,000 customers, multi-device, tariff DSL |
| **Scale** | $35,000 | $3,500 | $0.15 | Up to 500,000 customers, all features, regulator reporting |
| **Enterprise** | Custom from $50,000 | From $7,500 | Custom | Unlimited customers, white-label, dedicated deployment, SLA |

### 9.2 Customer Acquisition

- **Primary:** Direct outreach through Eric's Ignite/ENGIE network (warm intros to 10+ distributors)
- **Secondary:** GOGLA (Global Off-Grid Lighting Association) partnerships; conferences
- **Tertiary:** Content marketing; technical credibility via architecture blog posts
- **Regulatory:** Work with EPRA and peers to become a preferred platform; this drives distributor adoption

### 9.3 Positioning vs Competitors

| Competitor | Positioning | PayGoHub v2 Differentiation |
|------------|-------------|----------------------------|
| Angaza | Market leader, expensive | 50%+ lower TCO; African-built; Azure-native for enterprise; Sauti integration |
| Paygops | Mid-tier international | Better device coverage; deeper African localization; tariff DSL |
| In-house builds | Expensive to maintain | "Buy not build" economics; ongoing platform investment |
| Solaris / Others | Smaller / niche | Broader capability; service mesh architecture; Azure alignment for corporates |

---

## 10. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|-----------|
| Incumbent (Angaza) response / feature parity | Medium | High | Move fast; focus on differentiation (Azure, Sauti integration, tariff DSL); lock in first customers with contracts |
| Distributor integration complexity (5+ device manufacturers) | High | Medium | Hexagonal adapters make each integration isolated; budget 4 weeks per manufacturer |
| M-Pesa rate limits on high-volume distributors | Medium | High | Batch processing; coordinate with Safaricom for elevated limits |
| Azure cost overruns | Medium | Medium | Cost monitoring from Day 1; reserved capacity; cost-optimizer agent from Claude Code strategy |
| Capstone scope too ambitious for 2 weeks | High | Medium | Core DDD + ROP in 2 weeks; integrations and polish in Week 15; acceptable MVP trajectory |

---

## 11. Open Questions

1. Should we build the regulator portal from Day 1 or add it in v1.5? **Answer:** Defer — pilot distributors don't need it; build in v1.5.
2. Microsoft Orleans or a custom actor implementation? **Answer:** Orleans — battle-tested, .NET-native, reduces custom code.
3. Do we support non-Azure deployment (e.g., AWS for distributors who prefer it)? **Answer:** Cloud-agnostic hexagonal design makes it feasible, but Azure only at MVP for focus.
4. Should LendStream integration be mandatory or optional? **Answer:** Optional add-on; some distributors don't do financed sales.

---

## 12. Appendix: Definition of Done for v1.0

- [ ] All 6 bounded contexts with DDD structure and F# validation
- [ ] All 5 BFFs operational
- [ ] 1 distributor paying ($500+ MRR)
- [ ] Sauti integration live in call center
- [ ] M-Pesa integration live
- [ ] 2+ device manufacturer integrations
- [ ] Tariff DSL operational with real A/B test
- [ ] All 14 architectural patterns composed and measurable
- [ ] Security audit passed
- [ ] Azure cost per customer < $0.05/month
- [ ] Documentation: architecture guide (capstone-quality), API reference, distributor onboarding guide
- [ ] On-call rotation active
- [ ] Week 15 sprint retrospective captures the third-eye lessons from composing all 14 patterns in one system

---

## 13. Sprint Capstone Reflection (for Week 15 retrospective)

PayGoHub v2 is not just a commercial product; it's the architectural summation of the 15-week sprint. When complete, Eric should be able to:

1. **Point at any piece of code** and name the pattern it implements and why that pattern was chosen
2. **Walk a FAANG interviewer through the system** design in 45 minutes without needing to review the code
3. **Show the cross-project synergies** (Sauti in the call center, LendStream in financing) as evidence of the conglomerate thesis
4. **Justify every architectural decision** with the specific tradeoffs considered
5. **Demonstrate that the third eye is trained** — patterns visible across this system are the same patterns visible across Stripe, Shopify, Netflix, and other tier-1 engineering orgs at scale

If all six PRDs from this sprint compose into a recognizable architectural style, the sprint succeeded — regardless of revenue hit or missed. The revenue will compound; the architectural training is permanent.
