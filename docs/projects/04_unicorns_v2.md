# PRD — Unicorns v2

> **Version:** 2.0
> **Date:** April 2026
> **Status:** Draft — Approved for Sprint Weeks 7-8
> **Owner:** Eric Gitangu (Deveric Technologies)
> **Tier:** 4 (Go + Zig)
> **Project Type:** Major Extension of Shipped App
> **Existing app:** github.com/ericgitangu/unicorns (live at unicorns.ericgitangu.com)

---

## 1. Executive Summary

**Unicorns v2** is the architectural refactor that takes the existing multi-tenant SaaS marketplace for African SMBs from "works for 100 tenants" to "architecturally ready for 10,000 tenants." The v1 platform already runs 5 Rust Lambda microservices, integrates M-Pesa, offers healthcare EMR functionality, and serves as a marketplace. The v2 work restructures all of this around **hexagonal architecture (ports and adapters)** with **service-mesh-managed cross-cutting concerns** — the architectural shift Shopify, Stripe, and Atlassian each made at similar scale.

The commercial thesis: Africa has 45M+ SMBs with limited access to affordable business software. Existing SaaS is either too expensive (Shopify at $29+/mo, which is 2 weeks of revenue for many Kenyan shops) or not localized (lacks M-Pesa, lacks Swahili UX, lacks offline capability). Unicorns is the "Shopify for African SMBs" — native M-Pesa checkout, offline-capable POS, healthcare EMR module, service bookings, all multi-tenant.

**The v2 architecture is what unlocks scale.** Without hexagonal separation, every new feature would cross-cut every service. Without a service mesh, every microservice would re-implement auth, rate limiting, mTLS, and observability. These patterns are the difference between building a v1 prototype and running a platform.

---

## 2. Problem Statement

### 2.1 The Pain

1. **Existing Unicorns v1 architecture has coupling debts.** 5 Rust Lambdas share database schema; adding a new tenant type (e.g., clinic tenants) requires changes across all 5 services. New features take 2-3x longer than they should.

2. **Cross-cutting concerns are re-implemented everywhere.** Auth check in every service. Rate limiting in every service. Logging format inconsistent. Distributed tracing absent. These are the technical debts that kill platforms at scale.

3. **African SMB market is massively underserved.** Competitors aren't building for this market. Shopify is too expensive. Square doesn't do M-Pesa. WooCommerce requires self-hosting. Local alternatives are fragmented and poorly engineered.

4. **Multi-tenancy at real scale requires intentional architecture.** Data isolation, noisy-neighbor handling, per-tenant rate limiting, tenant-specific feature flags — all these need to be systematic, not ad-hoc.

5. **Offline POS is a real market need.** Kenyan shops in smaller towns have connectivity drops. A POS that goes down when WiFi drops loses sales. Unicorns v1 doesn't handle this yet.

### 2.2 Quantified Market

- **African SMB count:** ~45 million (formal + informal, varying estimates)
- **Kenyan SMB count:** 7.5M+ (formal registered) + millions more informal
- **Target subset (Unicorns' ICP):** "Digital-ready" SMBs — have a smartphone, take M-Pesa, want to grow online. Estimate 2-5M in Kenya alone.
- **Total addressable market (Kenya):** ~$200M/year at current ARPU assumptions
- **Pan-African TAM:** $1.5B+

### 2.3 Why Now

- M-Pesa open APIs (Daraja) are mature
- Africa's cloud adoption is growing 25%+ annually (market validation for SaaS readiness)
- Government push for digital economy (Kenya's Digital Economy Blueprint)
- Competitors (Shopify, Gumroad) have not localized for African payment rails
- v1 traction validates demand — time to scale architecturally before scaling users

---

## 3. Target Users & Personas

### 3.1 Primary Persona: Small Shop Owner

**Name:** Kamau, 38, Nakuru
**Role:** Owner of a hardware shop; 400 SKUs, 8 employees, KES 2M/month revenue
**Goals:**
- Track inventory accurately (currently loses ~5% to theft/miscount)
- Accept M-Pesa payments with automatic reconciliation
- Know which products are profitable
- Expand to online sales without hiring a developer

**Pain points:**
- Uses 3 different systems (Excel for inventory, M-Pesa app for payments, WhatsApp for orders)
- Can't answer basic questions like "what's my best-selling product this month?"
- Loses sales when WiFi is down (can't process card; can't use any "modern" POS)

**Jobs-to-be-done:** One system that handles inventory, POS, M-Pesa, basic analytics — with a Swahili UI, works offline, and costs less than hiring a part-time bookkeeper.

### 3.2 Secondary Persona: Clinic Manager

**Name:** Dr. Achieng, 36, Kisumu
**Role:** Manages a 4-doctor private clinic serving 3,000+ patients
**Goals:**
- Digital patient records (currently paper-based, prone to loss)
- Efficient billing for NHIF and private insurance claims
- Appointment scheduling + reminders
- Pharmacy inventory tied to prescriptions

**Pain points:**
- EMR software designed for Western clinics is expensive and doesn't fit her workflow
- Insurance claim rejections due to paperwork errors
- No way to remind patients about appointments — no-show rate 30%+

**Jobs-to-be-done:** Run a modern clinic without enterprise-grade overhead; tenant of Unicorns that gets healthcare-specific features.

### 3.3 Tertiary Persona: Service Provider

**Name:** Wanjiru, 29, Nairobi
**Role:** Independent hair stylist, home service + salon
**Goals:**
- Accept bookings 24/7 (sleep without missing inquiries)
- Predictable income (not feast-or-famine)
- Collect payment before no-shows waste her time

**Pain points:**
- Currently books via WhatsApp; no calendar integration; double-bookings common
- 40% no-show rate because she doesn't charge deposits
- No repeat-customer tracking; doesn't know her loyal base

**Jobs-to-be-done:** Turn her service business into a scheduled, pre-paid, repeat-customer engine.

### 3.4 Non-Target Users (Explicit)

- **Large enterprises** — wrong price point; enterprise SaaS needs enterprise sales
- **Digital-native e-commerce founders** — already using Shopify; we'd lose on platform maturity
- **Pure B2B software** — we build for B2C-facing SMBs with physical operations

---

## 4. User Stories & Acceptance Criteria

### 4.1 Epic: Multi-Tenant Onboarding

**User Story 4.1.1:** As a new SMB signing up for Unicorns, I want to be operational in under 15 minutes, so that I can start using the platform today.

**Acceptance Criteria:**
- **Given** a phone number and basic business info (name, type, M-Pesa till)
- **When** I complete signup via the Merchant BFF
- **Then** a new tenant is provisioned with isolated database schema in under 30 seconds
- **And** default storefront, POS, and basic inventory structure are created
- **And** M-Pesa till number is validated and linked
- **And** I receive SMS with login credentials and a getting-started link
- **And** first successful transaction can happen within 15 minutes of signup

### 4.2 Epic: Hexagonal Domain Core

**User Story 4.2.1:** As a developer extending Unicorns with a new feature, I want to add it without touching infrastructure code, so that feature development stays fast as the platform grows.

**Acceptance Criteria:**
- **Given** the hexagonal architecture with defined ports
- **When** I add a new feature (e.g., "loyalty points")
- **Then** I write pure domain logic that uses existing ports (PaymentGateway, CustomerStore)
- **And** no infrastructure code (HTTP, database, M-Pesa API) appears in the domain layer
- **And** unit tests run in under 2 seconds with no external dependencies
- **And** the feature works with the swap-in-memory adapter for dev, and the real adapter in production

### 4.3 Epic: Offline POS

**User Story 4.3.1:** As a shop owner on unreliable WiFi, I want to continue processing sales when connectivity drops and have everything reconcile when it returns, so that I never lose a sale to a network issue.

**Acceptance Criteria:**
- **Given** a shop running Unicorns POS on a tablet
- **When** WiFi drops during a transaction
- **Then** the transaction completes locally (customer selects items, pays via M-Pesa direct or cash, receipt prints)
- **And** inventory adjusts locally via CRDT
- **And** when WiFi returns, transactions sync to server automatically
- **And** inventory reconciles without conflicts (CRDTs resolve)
- **And** M-Pesa transactions (which happen on the customer's phone, not the POS) reconcile via webhook upon reconnection

### 4.4 Epic: Service Mesh Reliability

**User Story 4.4.1:** As a platform operator, I want every service-to-service call to be encrypted, retried, and traced, without any service having to implement this itself, so that cross-cutting concerns don't bloat business logic.

**Acceptance Criteria:**
- **Given** Unicorns running on EKS with Linkerd service mesh
- **When** a request flows from BFF → marketplace service → payments service
- **Then** all communication is mTLS-encrypted
- **And** failed requests retry automatically per policy (e.g., 3 retries with backoff on idempotent calls)
- **And** every request has a trace-id propagated end-to-end
- **And** I can view the full request path in Grafana/Tempo within 30 seconds
- **And** circuit breakers open after 10 consecutive failures, protecting downstream services

### 4.5 Epic: EMR Module for Clinic Tenants

**User Story 4.5.1:** As a clinic manager, I want patient records, prescriptions, and billing in one system with NHIF integration, so that I can run my clinic without juggling 3 apps.

**Acceptance Criteria:**
- **Given** a clinic tenant subscribed to the EMR module
- **When** I record a patient visit (diagnosis, prescription, billing)
- **Then** the visit is saved with full HIPAA-style audit trail
- **And** prescriptions flow to the pharmacy module (inventory deducts automatically)
- **And** NHIF claims are generated in the correct format
- **And** patient data is isolated from other tenants (enforced at the adapter layer)

### 4.6 Epic: Unified Search (Zig-Powered)

**User Story 4.6.1:** As a shopper, I want to find products fast in Swahili or English, including fuzzy matches for misspellings, so that I find what I need without scrolling.

**Acceptance Criteria:**
- **Given** a marketplace with 100,000+ products across all tenants
- **When** I search "sukuma wiki" or "sukuma wik" (misspelled)
- **Then** matching products appear in under 100ms
- **And** results include exact matches, synonym matches (Swahili/English), fuzzy matches
- **And** personalization ranks results by my prior browsing/purchases
- **And** tenant filtering is respected (I only see the merchant's products, not all tenants')

---

## 5. Non-Functional Requirements

### 5.1 Performance

| Metric | Target |
|--------|--------|
| API response (P95) | < 200ms |
| Search query (P95) | < 100ms |
| Tenant provisioning | < 30s |
| POS transaction (online) | < 2s |
| POS transaction (offline) | < 500ms (fully local) |
| Image thumbnail generation (Zig) | < 50ms per image |
| Service mesh overhead | < 5ms per hop |

### 5.2 Availability

| Component | Target |
|-----------|--------|
| Merchant BFF | 99.95% |
| Shopper BFF | 99.9% |
| Payments core | 99.99% (no financial loss tolerance) |
| Marketplace core | 99.9% |
| EMR core | 99.95% (healthcare tenants can't tolerate outages) |
| Search service | 99.5% (graceful degradation — fallback to basic ILIKE) |

### 5.3 Scalability

- Platform must handle 10,000+ tenants without architectural changes
- Per-tenant data isolation enforced at the adapter layer (no leakage possible)
- Hot tenants should not starve others (per-tenant rate limiting at the mesh)
- Horizontal scaling of any service without downtime

### 5.4 Security

- **Multi-tenancy isolation:** Row-level security (RLS) in PostgreSQL; tenant-id in every query; automated tests verify no cross-tenant reads possible
- **Payment security:** M-Pesa Daraja integration via hexagonal port; webhook signature validation; idempotency keys on all monetary operations
- **Healthcare compliance (EMR tenants):** HIPAA-equivalent controls; audit log for every PHI access; encryption at rest; access requires documented purpose
- **Authentication:** OIDC via Auth0 or self-hosted Keycloak; per-tenant SSO for enterprise customers
- **Authorization:** Fine-grained RBAC + ABAC; tenant-admin can define custom roles
- **Mesh-level:** mTLS between all services; service mesh policies enforce zero-trust

### 5.5 Observability

- Distributed tracing (OpenTelemetry → Tempo)
- Per-tenant dashboards in Grafana (tenant operators see their own metrics)
- Platform-wide dashboards for operators
- Alerting: per-tenant SLO breaches, platform-wide error budgets, mesh anomalies
- Log aggregation (Loki or CloudWatch)

### 5.6 Developer Experience

- Local dev environment spins up in under 5 minutes (docker-compose)
- All services build in parallel (monorepo with Nx or Bazel)
- Test suite runs in under 10 minutes
- Pre-commit hooks enforce lint, format, type-check, security scans

---

## 6. Success Metrics

### 6.1 Business Metrics (End of Week 15)

| Metric | Target |
|--------|--------|
| Active tenants | 20 (up from ~5 currently in v1) |
| Paying tenants | 5 |
| Total transaction volume via platform | KES 2M+ (≈ $15K+) |
| Transaction fee revenue (1.5%) | $225+ |
| Subscription revenue | $500+ |

### 6.2 Technical Metrics

| Metric | Target |
|--------|--------|
| Architecture: cross-context coupling | Measurably lower (dependency graph cleaner) |
| Feature development velocity | 2x+ improvement vs v1 (lines changed per feature) |
| Service mesh traces captured | 100% of inter-service calls |
| Zero cross-tenant data leaks | Verified by automated security tests |
| Platform-wide uptime | 99.9%+ |

### 6.3 Architectural Metrics

| Metric | Target |
|--------|--------|
| Number of bounded contexts | 6+ (marketplace, payments, EMR, services, identity, search) |
| Each context has defined ports | 100% |
| Each context has swappable adapters | 100% |
| Service mesh coverage | 100% of service-to-service calls |

---

## 7. Architecture Mapping

### 7.1 Primary Pattern Introduced: Hexagonal Architecture + Service Mesh

Unicorns v2 implements the full Ports and Adapters (hexagonal) pattern for every bounded context, managed by a service mesh that handles cross-cutting concerns.

**Compounding patterns from prior tiers:**
- **BFF pattern (Tier 1):** 4+ BFFs (Merchant, Shopper, Clinic, Platform API)
- **Event-driven (Tier 1):** Domain events cross context boundaries via NATS JetStream
- **CQRS (Tier 2):** Each context splits commands and queries
- **Sagas (Tier 2):** Order-fulfillment-payment is a saga spanning marketplace, payments, inventory contexts
- **CRDTs (Tier 3):** POS offline-first uses CRDTs; syncs into the marketplace core when online

### 7.2 The Six Bounded Contexts

| Context | Responsibility |
|---------|----------------|
| **Identity** | User accounts, tenants, authentication, authorization |
| **Marketplace** | Product catalog, orders, pricing, tenant isolation |
| **Payments** | M-Pesa orchestration, wallets, settlements, reconciliation |
| **EMR** | Patient records, prescriptions, NHIF claims (healthcare tenants only) |
| **Services** | Appointment booking, calendars, deposits (service provider tenants) |
| **Search** | Indexing, querying, tenant-scoped results (Zig adapter) |

### 7.3 Hexagonal Core (Go)

Each bounded context has:
- **Pure domain code** (no I/O, no framework)
- **Ports** (Go interfaces for dependencies)
- **Adapters** (HTTP handlers, database access, M-Pesa client)
- **Tests** run against in-memory adapters for speed

**Example: Marketplace context structure**

```
marketplace/
├── domain/
│   ├── product.go        # Aggregate root (pure)
│   ├── order.go          # Order aggregate (pure)
│   └── ports.go          # ProductRepository, OrderRepository, PaymentGateway
├── adapter/
│   ├── http/             # REST handlers for the Merchant BFF to call
│   ├── postgres/         # Real product/order repository
│   ├── memory/           # In-memory for tests
│   └── mpesa/            # M-Pesa payment gateway adapter
├── application/
│   └── services.go       # Orchestrates domain using ports
└── marketplace_test.go   # Pure domain tests (no infra)
```

### 7.4 Zig Performance Adapters

Specific performance-critical paths implemented as Zig modules, called from Go via C FFI:

- **Full-text search with custom Swahili/Kikuyu tokenizer:** BM25 ranking, inverted index
- **Image thumbnailing:** Fast WebP generation for product catalogs
- **Fuzzy product matching:** Levenshtein + trigram for search "did you mean"
- **PDF generation:** Fast, dependency-free PDF generation for receipts and invoices

Zig's strengths here:
- Predictable performance (no GC pauses)
- Small binaries (matters for Docker image sizes)
- Explicit allocation (no surprise memory pressure)
- Comptime metaprogramming (tokenizer customization at compile time)

### 7.5 Service Mesh (Linkerd)

**What the mesh handles:**
- **mTLS** between every service (automatic cert rotation)
- **Distributed tracing** (OpenTelemetry propagation)
- **Traffic management** (canary deployments, traffic splitting)
- **Circuit breakers** (protect downstream services from cascading failures)
- **Retries** with exponential backoff
- **Rate limiting** per tenant at the mesh layer
- **Policy enforcement** (deny cross-tenant traffic at the network level)

**What services still handle:**
- Business logic
- Domain-specific authorization (who can see what inside a tenant)
- Tenant data isolation (belt-and-suspenders with mesh policies)

### 7.6 The Four+ BFFs

| BFF | Client | Technology | Key Endpoints |
|-----|--------|------------|---------------|
| Merchant BFF | Web admin (PWA) | Go + gin | `POST /storefront`, `GET /orders/dashboard`, `POST /inventory/bulk` |
| Shopper BFF | Mobile app (React Native / PWA) | Go + gin | `GET /catalog/search`, `POST /cart`, `POST /checkout` |
| Clinic BFF | Clinic staff web + mobile | Go + gin | `GET /patients`, `POST /visits`, `POST /prescriptions` |
| Platform API BFF | Third-party integrations | Go + gin | OAuth 2.0 API, webhook delivery, partner data exports |

### 7.7 Technology Stack

**Backend:**
- Go 1.22+ (hexagonal cores, BFFs)
- Zig 0.13+ (performance adapters via cgo FFI)
- Existing Rust Lambdas (gradually absorbed into Go services)

**Data:**
- PostgreSQL with row-level security (per-context databases, shared auth)
- Redis (sessions, caching, rate limit counters)
- Elasticsearch or Meilisearch (search backing; Zig tokenizer integration)
- NATS JetStream (inter-context events)
- S3 (media, documents, EMR attachments)

**Infrastructure:**
- AWS EKS (Kubernetes)
- Linkerd service mesh
- Istio (evaluated; Linkerd preferred for simplicity)
- Terraform for all infrastructure
- ArgoCD for GitOps deployments

**Monitoring:**
- Prometheus + Grafana
- Loki (logs)
- Tempo (traces)
- Alertmanager + PagerDuty

---

## 8. Phased Rollout Plan

### 8.1 Week 7-8 (Tier 4 Sprint)

**Scope:**
- Hexagonal refactor of the Marketplace context (largest, highest value)
- Go BFF for Merchant and Shopper
- Linkerd service mesh deployed; mTLS + tracing operational
- Zig search adapter integrated (new inverted index)

**Commercial goal:** Existing tenants migrated with no downtime; architecture cleaner; observability full.

### 8.2 Week 9-10 (parallel with Tier 5a Shamba work)

**Scope:**
- Payments context hexagonalized
- EMR context hexagonalized (first clinic tenant onboarded)
- Zig image thumbnailing in production
- First enterprise customer discussion (large SMB chain)

### 8.3 Week 13-14 (parallel with Tier 6 PayGoHub work)

**Scope:**
- All 6 bounded contexts fully hexagonal
- Search service fully Zig-powered
- Multi-country support (Uganda, Tanzania pilot tenants)
- 20 active tenants, 5 paying

### 8.4 Post-Sprint

- DDD refinement using Tier 6 learnings
- Enterprise tier rollout
- Self-service tenant onboarding
- AWS Marketplace listing

---

## 9. Commercial Terms

### 9.1 Pricing Tiers (retained from v1)

| Tier | Price | Features |
|------|-------|----------|
| **Starter** | Free | 1 store, basic inventory, M-Pesa checkout |
| **Growth** | $25/mo | 3 stores, analytics, AI recommendations, customer management |
| **Business** | $75/mo | Unlimited stores, EMR module, multi-user, API access |
| **Transaction fee** | 1.5% on M-Pesa payments | All tiers |

---

## 10. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|-----------|
| Hexagonal refactor breaks existing users | Medium | High | Parallel old + new stacks during transition; gradual migration; extensive regression testing |
| Linkerd operational complexity | Medium | Medium | Use Linkerd's simpler model vs Istio; hire short-term DevOps consulting if needed |
| Zig adapters introduce bugs in hot paths | Low | High | Property-based testing; fall back to Go implementations during incidents |
| Tenant growth outpaces architecture improvements | Medium | Medium | Feature-flag new tenant onboarding; cap growth if needed during migration |

---

## 11. Open Questions

1. Should we move away from Rust Lambdas entirely, or keep them as a performance-critical tier? Likely keep for specific workloads (image resize, search indexing) but move platform services to Go.
2. How much EMR functionality is needed at launch? Enough for a private clinic's billing and records; not full hospital EMR.
3. Should we support bank transfers alongside M-Pesa? Yes, in v2.5 — necessary for larger merchants.
4. Monorepo or polyrepo? Strong lean toward monorepo with Nx or Bazel for shared tooling.

---

## 12. Appendix: Definition of Done for v2.0

- [ ] All 6 bounded contexts have hexagonal structure with defined ports
- [ ] Service mesh operational with mTLS and 100% trace coverage
- [ ] Zig adapters in production for search, image thumbnailing
- [ ] Offline POS works end-to-end with CRDT sync
- [ ] 20 active tenants; 5 paying; no regressions vs v1
- [ ] Per-tenant dashboards live
- [ ] Security audit passed (including multi-tenancy isolation)
- [ ] Disaster recovery tested (full restore)
- [ ] Documentation: architecture overview, per-context guides, operator runbook
- [ ] AWS Solutions Architect Associate cert obtained (aligns with Week 2 cert schedule)
