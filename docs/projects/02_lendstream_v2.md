# PRD — LendStream v2

> **Version:** 2.0
> **Date:** April 2026
> **Status:** Draft — Approved for Sprint Weeks 3-4
> **Owner:** Eric Gitangu (Deveric Technologies)
> **Tier:** 2 (Java + Kotlin + Scala)
> **Project Type:** Major Extension of Shipped App
> **Existing app:** github.com/ericgitangu/lendstream (live at nanolend-app.vercel.app)

---

## 1. Executive Summary

**LendStream v2** transforms the existing micro-lending platform into **white-label lending infrastructure** for Kenyan and East African microfinance institutions (MFIs). The v2 thesis: MFIs don't want to build lending software — they want to operate it. LendStream sells them a complete enterprise-grade core banking alternative purpose-built for M-Pesa-denominated, short-cycle, small-ticket lending.

The v1 platform already demonstrates polyglot architecture with Java/Spring Boot, a Clojure scoring engine, and Kafka-based CQRS. The v2 work turns this into a **textbook CQRS + Event Sourcing + Saga Orchestration implementation** — the architecture that Stripe, Adyen, and Wise use for financial infrastructure, adapted for East African mobile money.

**Commercial positioning:** $500-$2,000/mo per MFI based on loan volume. 30+ licensed MFIs operate in Kenya alone. Three pilot conversations by Week 8; one paying MFI by Week 15. Longer-term: pan-African MFI platform with CBK-style regulatory compliance built in.

---

## 2. Problem Statement

### 2.1 The Pain

1. **MFIs build their own software and it's bad.** Most Kenyan MFIs run on Excel spreadsheets, Google Sheets, or custom-built software that was modern in 2012. They struggle with loan officer fraud, reconciliation errors, and CBK audit requirements.

2. **International core-banking software doesn't fit.** Solutions like Mambu, Temenos, and Finacle are designed for traditional banks with 30-year mortgages, not MFIs doing 30-day KES 5,000 loans with M-Pesa disbursement and repayment. Pricing is also out of reach (often $50K+ setup + $10K+/mo).

3. **Regulatory compliance is a mess.** CBK (Central Bank of Kenya) audit requirements for digital credit providers are tightening. MFIs need event-sourced audit trails, not CRUD databases that silently overwrite state.

4. **Lending decisions are manual.** Credit scoring at most Kenyan MFIs is either manual (loan officer judgment) or a simple scorecard. No real risk engine, no portfolio analytics, no early-warning signals for defaults.

### 2.2 Quantified Market

- **Primary:** 30+ CBK-licensed digital credit providers in Kenya; 60+ MFIs total
- **Secondary:** SACCOs (savings and credit cooperatives) — 170+ regulated in Kenya with lending products
- **Tertiary:** Pan-African MFIs (Uganda, Tanzania, Rwanda have similar mobile-money lending markets)

**Revenue math:** If LendStream captures 10% of Kenyan MFIs at average $1,000/mo, that's $6K MRR from Kenya alone. Pan-African expansion multiplies this 5-10x over 3-5 years.

### 2.3 Why Now

- CBK's Digital Credit Providers Regulations (2022) require audit trails and fair-lending practices that most MFIs can't currently produce
- M-Pesa open APIs (Daraja) have matured; integration friction has dropped
- Open-source CQRS/Event Sourcing tooling (Axon, EventStoreDB) is production-ready
- Java 21 virtual threads make high-concurrency JVM services dramatically simpler than a few years ago

---

## 3. Target Users & Personas

### 3.1 Primary Persona: MFI Operations Manager

**Name:** Samuel, 42, Nakuru
**Role:** Operations Manager at a 15-branch MFI with 12,000 active loans
**Goals:**
- Monthly CBK-compliant reporting without 3 days of manual reconciliation
- Real-time portfolio dashboard (NPL ratio, disbursement volume, collection rate by branch)
- Prevent loan officer fraud (fake borrowers, collusion with defaulting customers)

**Pain points:**
- Current system is a custom PHP app + Excel; reconciliation takes 2 days per month
- Audit prep for CBK inspections takes 2 full-time people for 2 weeks
- Suspected fraud can't be proven because there's no immutable audit log

**Jobs-to-be-done:** Replace the custom system with something auditable, scalable, and CBK-ready, without paying $50K+ for international software.

### 3.2 Secondary Persona: Loan Officer

**Name:** Beatrice, 29, Mombasa
**Role:** Field loan officer, originates 40-60 loans/week
**Goals:**
- Approve qualified borrowers in under 10 minutes in the field
- Not carry paper forms; everything mobile
- Get real-time alerts when her borrowers are late

**Pain points:**
- Current paper-based KYC takes 30-45 minutes per applicant
- No mobile app; she uses WhatsApp to communicate with the office
- Gets no feedback loop on which of her borrowers are paying on time

**Jobs-to-be-done:** Turn loan origination into a 10-minute mobile workflow, with risk scoring done automatically.

### 3.3 Tertiary Persona: MFI CEO / Compliance Officer

**Name:** Rose, 51, Nairobi
**Role:** CEO of a 50-branch digital credit provider
**Goals:**
- CBK license remains in good standing
- Fraud risk reduced to near-zero
- Platform that can scale from 10K to 100K loans/month without rearchitecture

**Pain points:**
- Compliance team is overworked
- Current system is a liability at scale — multiple near-misses on CBK audits
- Can't get real-time portfolio analytics to investors

**Jobs-to-be-done:** De-risk the business. The platform must be defensible to regulators, investors, and internal auditors.

### 3.4 Non-Target Users (Explicit)

- **Individual borrowers/consumers** — LendStream is infrastructure, not a consumer lending app. MFIs use LendStream to serve their own borrowers.
- **Traditional banks** — too slow, too regulated, too different from MFI economics. Banks buy Temenos; they are not the target.
- **US/European fintechs** — different regulatory regime, different payment rails.

---

## 4. User Stories & Acceptance Criteria

### 4.1 Epic: Loan Origination

**User Story 4.1.1:** As a loan officer, I want to originate a loan in under 10 minutes from the field, with credit scoring and M-Pesa disbursement automated, so that I can serve more borrowers per day.

**Acceptance Criteria:**
- **Given** a borrower's National ID and phone number
- **When** I enter these into the Loan Officer BFF on my mobile device
- **Then** KYC verification completes in under 30 seconds (integrated with NIDS and CRB)
- **And** credit scoring runs via the Scala saga orchestrator and returns a decision in under 60 seconds
- **And** if approved, M-Pesa disbursement is initiated (saga step: debit lender wallet → credit borrower phone → confirm receipt)
- **And** the borrower receives SMS confirmation within 2 minutes of approval
- **And** if any saga step fails, compensating actions are triggered automatically (refund, alerting, manual review queue)

**User Story 4.1.2:** As a compliance officer, I want every loan origination to produce an immutable audit trail that CBK can inspect, so that we pass regulatory audits without manual scrambling.

**Acceptance Criteria:**
- **Given** a completed loan origination (approved or rejected)
- **When** the origination saga completes
- **Then** every command and event is written to EventStoreDB
- **And** the event log is signed and timestamped
- **And** events are immutable — no update, no delete
- **And** the compliance BFF can produce a PDF audit report for any loan ID in under 10 seconds
- **And** the audit report includes every decision point, every system that touched the loan, and every state change

### 4.2 Epic: Portfolio Management

**User Story 4.2.1:** As an MFI operations manager, I want real-time portfolio analytics across all branches so that I can spot defaulting cohorts before they become NPL.

**Acceptance Criteria:**
- **Given** an active portfolio of 10,000+ loans
- **When** I open the Portfolio Dashboard in the Lender BFF
- **Then** I see NPL ratio, PAR30/60/90, disbursement volume, collection rate by branch, loan officer, product, and cohort
- **And** data freshness is under 30 seconds (driven by CQRS projections consuming the event stream)
- **And** I can drill down to individual loan level in 2 clicks
- **And** I can export any view to Excel/CSV for board reports

### 4.3 Epic: Repayment and Collection

**User Story 4.3.1:** As a borrower, I want to repay my loan via M-Pesa and have my loan balance update within 60 seconds, so that I don't worry about being marked late.

**Acceptance Criteria:**
- **Given** a borrower with an active loan
- **When** the borrower initiates M-Pesa payment to the MFI paybill
- **Then** M-Pesa webhook reaches LendStream within 10 seconds
- **And** the payment is idempotency-protected (webhook replay safe)
- **And** the repayment saga runs (allocate to principal → interest → fees → update balance → emit event)
- **And** the borrower's balance is updated in the projection store within 60 seconds of webhook receipt
- **And** the borrower receives SMS confirmation

### 4.4 Epic: MFI Onboarding (Partner BFF)

**User Story 4.4.1:** As a new MFI signing up for LendStream, I want to onboard my institution's data in under 1 week so that I can go live quickly.

**Acceptance Criteria:**
- **Given** a new MFI with existing loan data in Excel/CSV
- **When** they use the Partner Onboarding BFF
- **Then** they can upload existing loans via bulk CSV (up to 50,000 loans)
- **And** validation runs via Scala ROP pipeline (each loan either passes all checks or fails with a specific error)
- **And** failed loans are returned in a downloadable error report with specific remediation
- **And** successful loans are projected into the event store as `HistoricalLoanImported` events
- **And** the MFI can be operational within 7 days of contract signing

---

## 5. Non-Functional Requirements

### 5.1 Performance

| Metric | Target |
|--------|--------|
| Loan origination end-to-end (P95) | < 90 seconds (KYC + scoring + disbursement) |
| Portfolio dashboard query (P95) | < 2s |
| Event store write latency (P99) | < 100ms |
| Projection lag (events → read models) | < 30s |
| Repayment webhook processing (P95) | < 5s |
| System throughput | 1,000 loans/minute peak |

### 5.2 Availability

| Component | Target |
|-----------|--------|
| Loan Officer BFF | 99.95% (field operations can't tolerate downtime) |
| Lender BFF | 99.9% |
| Event store | 99.99% (audit requirement) |
| Compliance BFF | 99.9% (audit support) |
| Scoring engine (Scala sagas) | 99.9% |

### 5.3 Security

- **Authentication:** OAuth 2.0 / OIDC for MFI staff; mTLS for M-Pesa integration; JWT for internal service calls
- **Authorization:** Fine-grained RBAC (loan officer, branch manager, operations manager, compliance officer, CEO)
- **Encryption:** TLS 1.3 in transit; AES-256 at rest for borrower PII; FIPS 140-2 compliant key management
- **Audit logging:** Every API call logged with user-id, loan-id, operation, outcome
- **PII handling:** Borrower national IDs encrypted at rest; redacted in logs; access requires documented reason
- **Compliance:** CBK Digital Credit Providers Regulations 2022; Kenya Data Protection Act; POPIA for South African expansion
- **Fraud controls:** Loan officer commission tied to collection rates; suspicious-pattern detection on origination

### 5.4 Scalability

- Event store partitioned by tenant (MFI) ID
- Projections horizontally shardable
- BFFs stateless; horizontal scaling via Kubernetes HPA
- Saga orchestrator partitioned by saga-id; handles 10,000+ concurrent sagas

### 5.5 Regulatory Compliance

- Every loan must produce a CBK-compliant audit trail queryable within 10 seconds
- Event retention: 7 years minimum per CBK requirements
- Data residency: Kenya customer data stays in Kenya (AWS af-south-1 or on-premises)
- Right-to-be-forgotten: implemented via CQRS — events are immutable, but projections can be rebuilt with anonymized data

### 5.6 Observability

- Distributed tracing across all services (OpenTelemetry)
- SLIs: origination success rate, scoring latency, M-Pesa success rate, audit report generation time
- Per-MFI dashboards for customer success team
- Alerting on: spike in rejected loans (possible scoring model drift), M-Pesa failure rate > 2%, event store lag > 2 min

---

## 6. Success Metrics

### 6.1 Business Metrics (End of Week 15)

| Metric | Target | Current |
|--------|--------|---------|
| Paying MFI customers | 1 | 0 |
| Pilot conversations in progress | 3 | 0 |
| Monthly Recurring Revenue | $500 | $0 |
| Loans originated through platform | 5,000+ | N/A |

### 6.2 Technical Metrics

| Metric | Target |
|--------|--------|
| Origination end-to-end latency (P95) | < 90s |
| Event store uptime | > 99.99% |
| Audit report generation | < 10s for any loan |
| Test coverage on domain layer | > 90% |

### 6.3 Compliance Metrics

| Metric | Target |
|--------|--------|
| CBK audit report generation time | < 10 minutes for full-month report |
| Events with missing signatures | 0 |
| Projections reconcile with events | 100% (automated nightly check) |

---

## 7. Architecture Mapping

### 7.1 Primary Pattern Introduced: CQRS + Event Sourcing + Saga Orchestration

LendStream v2 is the textbook implementation of these patterns in their natural habitat (financial infrastructure). Every command produces events; events are the source of truth; read models are projections.

**Compounding patterns from Tier 1 carried forward:**
- **BFF pattern:** Four distinct BFFs (Loan Officer, Lender/Operations, Compliance, Partner API)
- **Event-driven architecture:** Every domain event flows through Kafka; Kafka is the backbone

### 7.2 Bounded Contexts

| Context | Responsibility | Primary Language |
|---------|---------------|------------------|
| Customer | Borrower onboarding, KYC, identity | Java/Spring Boot |
| Loan | Loan lifecycle, state, terms | Java/Spring Boot (command side) |
| Scoring | Credit scoring, underwriting rules | Scala (saga orchestration) + existing Clojure rules engine |
| Disbursement | M-Pesa integration, fund movement | Java/Spring Boot |
| Repayment | Payment allocation, reconciliation | Java/Spring Boot + Kotlin/Ktor projections |
| Portfolio | Read models for analytics | Kotlin/Ktor (query side) |
| Audit | Compliance event store access, reports | Java/Spring Boot |

### 7.3 Language Allocation (Why Each Role)

**Java 21 + Spring Boot (Command Side + Core Domain):**
- Axon Framework: most mature CQRS/ES toolkit in the JVM ecosystem
- Virtual threads: handle thousands of concurrent origination sagas without coroutine complexity
- Familiar to future hires: most East African Spring Boot engineers can work on this
- **Role:** Aggregate roots, command handlers, event store persistence

**Kotlin + Ktor (Read Side / Projections):**
- Coroutines: perfect for non-blocking Kafka consumers building projections
- Concise: projections are tedious in Java, elegant in Kotlin
- Ktor: lightweight, purpose-built for BFF-style servers
- **Role:** CQRS query side, Lender BFF, Portfolio BFF

**Scala 3 + cats-effect or ZIO (Saga Orchestration):**
- ADTs encode saga state machines; compiler prevents illegal transitions
- Pure functional error handling with `Either[SagaError, SagaState]`
- **Role:** Origination saga, repayment saga, scoring orchestration

**Clojure (existing, kept as-is):**
- Scoring rules DSL (existing from v1)
- Will be deepened in Tier 5b (BSD Engine v2 pattern reuses the lessons here)

### 7.4 The Four BFFs

| BFF | Client | Language | Key Endpoints |
|-----|--------|----------|---------------|
| Loan Officer BFF | Mobile app (loan officers in field) | Kotlin/Ktor | `POST /loans/originate`, `GET /loans/my-portfolio`, `POST /repayments/manual` |
| Lender BFF | Operations dashboard (web) | Kotlin/Ktor | `GET /portfolio/dashboard`, `GET /branches/performance`, `GET /cohorts/analysis` |
| Compliance BFF | Compliance officer tools (web) | Java/Spring Boot | `GET /audit/loan/{id}`, `GET /audit/reports/cbk-monthly`, `POST /audit/custom-query` |
| Partner API BFF | Integration partners (CRM, mobile banking) | Kotlin/Ktor | `POST /loans` (origination API), webhook deliveries, `POST /imports/bulk` |

### 7.5 Technology Stack

**Backend:**
- Java 21 (Spring Boot 3.3, Axon Framework 4.x)
- Kotlin 2.x (Ktor 3.x, Kotlin Serialization)
- Scala 3 (cats-effect or ZIO 2)
- Clojure (existing scoring engine from v1)

**Data:**
- EventStoreDB (authoritative event store)
- Apache Kafka (event bus between contexts)
- PostgreSQL (projection databases, one per query context)
- MongoDB (flexible borrower profile projection)
- Elasticsearch (loan search)
- Redis (saga state, distributed locks)

**Integrations:**
- M-Pesa Daraja APIs (B2C disbursement, C2B collection)
- NIDS (National ID verification)
- CRB (Credit Reference Bureau) APIs
- Africa's Talking (SMS notifications)

**Infrastructure:**
- AWS (af-south-1 primary for Kenya data residency)
- Kubernetes (EKS)
- Istio service mesh (full implementation comes in Tier 4)
- OpenTelemetry for tracing

---

## 8. Phased Rollout Plan

### 8.1 MVP (Week 4, end of Tier 2 sprint)

**Scope:**
- CQRS + Event Sourcing skeleton with Loan aggregate
- Origination saga (Scala) with KYC + scoring + M-Pesa steps (simulated; no live M-Pesa yet)
- Lender BFF with basic portfolio view
- Compliance BFF with audit report generation for any loan

**Commercial goal:** Demo to 3 MFI contacts; 1 pilot signed.

### 8.2 v1.0 (Week 8, end of Tier 4 sprint — after service mesh work)

**Scope:**
- Live M-Pesa integration
- Full 4-BFF architecture deployed
- Multi-tenant isolation operational
- Istio service mesh (from Tier 4 propagating back)
- 1 MFI in paid pilot ($500/mo)

### 8.3 v1.5 (Week 12)

**Scope:**
- Bulk import tool (Partner BFF CSV import)
- Fraud detection module (anomaly detection on origination patterns)
- Advanced portfolio analytics (cohort retention, DSO, etc.)
- 3 paying MFIs

### 8.4 v2.0 (Post-sprint, Months 4-6)

**Scope:**
- Uganda + Tanzania M-Pesa equivalents
- SACCO-specific features (savings tied to lending)
- White-label branding tools for MFIs with their own app presence
- 10+ paying MFIs

---

## 9. Commercial Terms

### 9.1 Pricing Tiers

| Tier | Price | Features | Target |
|------|-------|----------|--------|
| **Starter** | $500/mo | Up to 5,000 active loans, 2 branches, basic analytics | Small MFIs |
| **Growth** | $1,200/mo | 25,000 active loans, 10 branches, advanced analytics, API access | Mid MFIs |
| **Scale** | $2,500/mo | 100,000+ active loans, unlimited branches, custom integrations | Large MFIs, SACCOs |
| **Enterprise** | Custom (from $5,000/mo) | On-premises option, custom scoring models, dedicated support | Digital credit providers, banks |
| **Implementation fee** | $2,500 – $15,000 | Data migration, training, customization | One-time per MFI |

### 9.2 Customer Acquisition

- **Primary channel:** Direct outreach to CBK-registered MFIs via Eric's existing fintech network
- **Secondary:** iHub Spark Accelerator (applied in Week 12); AWS FinTech Africa Accelerator
- **Referral channel:** First successful MFI becomes reference account for next 3-5
- **Content:** Technical blog posts on CQRS for African fintech; conference talks at Africa Fintech Summit

---

## 10. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|-----------|
| MFI sales cycles are 6-9 months | High | High | Start outreach Week 1; maintain 10+ active conversations in parallel |
| CBK regulatory changes mid-sprint | Medium | Medium | Build to current regs; event-sourced architecture makes adaptation easier |
| M-Pesa API changes or outages | Medium | High | Abstract M-Pesa behind a port (hexagonal); build simulator for dev/test |
| MFI doesn't trust outside vendor | High | High | Offer on-premises deployment option; partner with Kenyan CA-registered entity; SOC 2 Type I by Month 6 |
| Scoring model liability | Medium | High | Scoring runs inside the MFI's boundary; LendStream provides tooling, MFI owns the model decisions |

---

## 11. Open Questions

1. Do we take a transaction fee (bps on loan volume) in addition to SaaS fee? Cleaner revenue model; but MFIs may resist. Decision: SaaS only for v1, revisit v2.
2. Should bulk import support legacy systems other than CSV (e.g., direct database migration)? Prioritize CSV first; API-based integration for advanced cases in v1.5.
3. How much customization do we allow per MFI before it becomes untenable? Hard rule: no custom code branches per MFI. All customization via config and rule DSL (Tier 5b work will help here).
4. What happens when an MFI wants to leave the platform? Define data-portability commitment upfront; build export tools from Day 1.

---

## 12. Appendix: Definition of Done for v1.0

- [ ] All user stories in Section 4 have passing acceptance tests
- [ ] Origination saga handles all 12 defined failure modes with correct compensation
- [ ] Event store reconciles with projections nightly (zero discrepancies over 7 consecutive days)
- [ ] Audit report for any loan generated in under 10 seconds
- [ ] 1 MFI live in production handling real loans (minimum 100 loans/week)
- [ ] Security audit complete (OWASP Top 10 + fintech-specific threat model)
- [ ] CBK audit rehearsal passed (present to local compliance consultant for sign-off)
- [ ] Documentation: API reference, MFI onboarding guide, architecture docs, runbook
- [ ] Disaster recovery tested (full restore from event store in staging)
- [ ] On-call rotation + alerting operational
