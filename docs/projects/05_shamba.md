# PRD — Shamba (with Greenland AgriTech Module)

> **Version:** 1.1
> **Date:** April 2026
> **Status:** Draft — Approved for Sprint Weeks 9-10
> **Owner:** Eric Gitangu (Deveric Technologies)
> **Tier:** 5a (Ruby + PHP + Elixir)
> **Project Type:** New Greenfield
> **Name meaning:** *Shamba* = "farm" in Swahili
> **Modules:** (A) Shamba Cooperative Platform — primary B2B product for cooperatives; (B) Greenland AgriTech — farm-level decision support platform, Kajiado farm as first proving ground

---

## 1. Executive Summary

**Shamba** is an agricultural cooperative operations platform for East African coffee, tea, dairy, and horticulture cooperatives. Each registered farmer becomes a supervised actor in the platform — their deliveries, payments, loans, agronomy advice, and extension visits are coordinated through the system. The platform serves the cooperative (as the primary tenant/customer) and all its member farmers (as end users, often 2G/feature-phone-only).

The architecture thesis: cooperatives have 500-15,000 members each, each farmer is an independent supervised process, state is long-lived (years per farmer), and failure modes are local (one farmer's bad data doesn't break others). This is precisely what OTP (Open Telecom Platform) was built for. Phoenix + GenServer per farmer, with supervision trees mirroring cooperative organizational structure, is the natural architecture.

**Commercial thesis:** Kenya has 5M+ coffee farmers, 800K+ tea farmers, and 1.5M+ dairy farmers, organized into ~2,000 registered cooperatives. Existing software is either enterprise ERP (too expensive, wrong fit) or donor-funded pilots (don't survive the pilot). Shamba is a sustainable SaaS purpose-built for this market: $0.50/farmer/month + 0.5% transaction fee. A 5,000-farmer cooperative = $2,500/mo + transaction upside.

---

## 2. Problem Statement

### 2.1 The Pain

1. **Farmer records are paper-based or fragmented Excel files.** Cooperative accountants reconcile deliveries, payments, and inputs manually. A 3,000-farmer cooperative takes 2 full-time bookkeepers just to manage delivery and payment records.

2. **Payment cycles are opaque to farmers.** A farmer delivering milk daily may not know what they earned for the month until payday. This creates distrust and drives side-selling (selling to middlemen outside the coop for immediate cash).

3. **Input distribution is chaotic.** Fertilizer, seed, and pesticide distributions require farmer-level allocation (based on land size and crop), ordering, delivery logistics, and cost recovery (usually deducted from farmer payments). Most coops do this in Excel + WhatsApp.

4. **Extension officer visits aren't tracked.** Cooperatives (and funders like the World Bank, USAID) want to know which farmers received agronomy advice, when, and what was discussed. Currently this is in paper notebooks or not recorded at all.

5. **Lending to farmers is manual.** Farmer loans (for inputs, school fees, emergencies) are approved informally, tracked in ledgers, and repaid through milk/coffee payment deductions. Reconciliation errors are common and damaging to farmer trust.

6. **2G/feature phone reality.** Many smallholder farmers have feature phones only, or share a smartphone with the household. USSD, SMS, and ultra-lightweight web are the only viable channels for farmer-facing features.

### 2.2 Quantified Market

- **Kenya:** ~2,000 registered agricultural cooperatives; ~7M+ farmer members across crops
- **Pan-East-Africa (Kenya, Uganda, Tanzania, Rwanda, Ethiopia):** ~15M farmer members in cooperatives
- **Revenue math:** 50 cooperatives at 5,000 farmers/coop average = $125,000/mo at $0.50/farmer. Transaction fee on ~$2B of farmer payments/year = $10M/year potential at 0.5%.
- **Realistic Year 1:** 10 cooperatives, 30,000 farmers total = $15K MRR. Still meaningful; growth rate can be steep given low acquisition cost per cooperative.

### 2.3 Why Now

- Mobile penetration in rural Kenya now 85%+
- Safaricom's Daraja API is mature; M-Pesa for farmers is ubiquitous
- SMS and USSD infrastructure via Africa's Talking is cheap and reliable
- Cooperatives face growing pressure (from funders, governments) to digitize for transparency
- Post-COVID, donors are funding digitization initiatives; Shamba can ride that wave
- Elixir/Phoenix/LiveView has matured enough to build rich back-office UX with minimal JS

---

## 3. Target Users & Personas

### 3.1 Primary Persona: Cooperative Manager

**Name:** Peter, 51, Nyeri (coffee farming region)
**Role:** General Manager of a 3,500-farmer coffee cooperative
**Goals:**
- Pay farmers accurately and on time
- Track deliveries, grades, and weights without errors
- Manage input loans and recoveries
- Provide transparent reports to the cooperative's board and funders

**Pain points:**
- Current system is a custom Access database + Excel; crashes frequently
- 2 staff reconcile payments manually; takes 3 days per month
- Constant disputes with farmers over delivery weights
- Can't produce real-time reports for board meetings

**Jobs-to-be-done:** Turn a 3-day reconciliation into a 30-minute review. Give farmers transparency into their own accounts so disputes drop.

### 3.2 Secondary Persona: Smallholder Farmer

**Name:** Mary, 45, Nyeri, coffee farmer
**Role:** Member of the cooperative, delivers ~500kg coffee cherries/year from ½ acre
**Goals:**
- Know what she's earned and when she'll be paid
- Understand why her grade was "AA" vs "AB" this delivery
- Access input loans when the season demands
- Get practical agronomy advice

**Pain points:**
- Owns a Nokia feature phone only (no smartphone in her household)
- Cooperative tells her "you'll be paid next month" but she can't verify the amount
- Can't check her input loan balance without going to the cooperative office (10km walk)
- Has no easy way to ask an agronomist a question

**Jobs-to-be-done:** Check account, loan balance, pending payments via SMS/USSD. Report issues. Request extension visits.

### 3.3 Tertiary Persona: Extension Officer

**Name:** David, 32, Embu (tea growing region)
**Role:** Field extension officer covering 800 farmers across 3 cooperatives
**Goals:**
- Track his own visits and advice given
- Target advice to farmers whose yields are dropping
- Document outcomes of interventions
- Report to cooperative and government on field activity

**Pain points:**
- Currently uses a paper notebook; records often lost or unreadable
- No way to prioritize — visits the farmers who call him, not the ones who need him
- No data on intervention outcomes (did yield improve after advice?)

**Jobs-to-be-done:** Mobile-first visit logging with offline capability; farmer prioritization based on data; outcome tracking.

### 3.4 Quaternary Persona: Buyer / Processor

**Name:** Nairobi Coffee Exchange (NCE) representative
**Role:** Purchases graded coffee from multiple cooperatives
**Goals:**
- Traceability of coffee lots back to cooperative and ideally farmer level
- Quality consistency and grading transparency
- Reliable delivery schedules

**Jobs-to-be-done:** Traceable, quality-transparent coffee purchases with reliable logistics. Gives cooperatives using Shamba a commercial advantage (premium pricing).

### 3.5 Non-Target Users (Explicit)

- **Individual commercial farms** (100+ acres) — they use different tools; not cooperative-driven
- **Large agribusiness corporations** — different buyer, different sales cycle, enterprise pricing needed
- **Non-farming rural cooperatives** (SACCOs, transport coops) — different domain, out of scope

---

## 4. User Stories & Acceptance Criteria

### 4.1 Epic: Farmer Onboarding and Registration

**User Story 4.1.1:** As a cooperative manager, I want to bulk-register 3,500 existing farmer members into the system in under a week, so that I can migrate from our current Access database without business interruption.

**Acceptance Criteria:**
- **Given** a CSV/Excel export from an existing cooperative system
- **When** I upload it via the Cooperative Officer BFF
- **Then** validation runs on every row (name format, phone number format, ID number, land size plausibility, crop categories)
- **And** valid rows become registered farmers with a spawned GenServer process each
- **And** invalid rows are returned in a downloadable remediation report
- **And** successfully registered farmers receive SMS welcome with their cooperative ID
- **And** the process handles 10,000+ rows without timeout (streaming upload)

### 4.2 Epic: Delivery Recording

**User Story 4.2.1:** As a cooperative weigher at a collection point, I want to record a farmer's delivery in under 30 seconds, including weight, grade, and quality notes, so that long farmer queues move quickly during peak harvest.

**Acceptance Criteria:**
- **Given** a logged-in collection-point clerk with a list of expected farmers
- **When** a farmer presents at the scale
- **Then** clerk enters farmer's 4-digit ID (or scans QR code on farmer card)
- **And** weight is captured (optionally from an integrated scale)
- **And** grade is selected from configured options for that crop
- **And** delivery is recorded and an SMS confirmation sent to the farmer within 10 seconds
- **And** the farmer's GenServer processes the delivery event, updating running totals
- **And** the delivery is immediately reflected in the cooperative's running dashboard

### 4.3 Epic: Farmer Self-Service (USSD/SMS)

**User Story 4.3.1:** As a farmer with a feature phone, I want to check my account balance, pending payments, and loan status via USSD in under 60 seconds, so that I have transparency into my cooperative relationship.

**Acceptance Criteria:**
- **Given** a farmer with a registered phone number
- **When** they dial `*384*{coop-code}#` on any mobile network
- **Then** a USSD menu is presented in their preferred language (Swahili/English/Kikuyu)
- **And** option 1 shows current account balance (YTD deliveries, YTD earnings, balance due)
- **And** option 2 shows outstanding loans (input loan balance, repayment schedule)
- **And** option 3 requests an extension officer visit
- **And** option 4 reports a problem (delivery dispute, input issue)
- **And** session response times are under 3 seconds per screen

**User Story 4.3.2:** As a farmer, I want to receive an SMS after every delivery confirming weight, grade, and expected payment, so that I have a record and trust in the system.

**Acceptance Criteria:**
- **Given** a delivery recorded in the system
- **When** the delivery event fires on the farmer's GenServer
- **Then** an SMS is sent within 30 seconds in the farmer's language
- **And** the SMS includes: date, weight, grade, running YTD total, payment date
- **And** failed SMS deliveries retry (Africa's Talking handles this) and fallbacks to voice call notification for critical events (payments due)

### 4.4 Epic: Payment Cycles

**User Story 4.4.1:** As a cooperative manager, I want to run the monthly payment cycle for 3,500 farmers in under 1 hour, with M-Pesa disbursement, so that farmers are paid predictably and without errors.

**Acceptance Criteria:**
- **Given** a month's deliveries recorded and graded
- **When** I initiate the monthly payment run via the Cooperative Officer BFF
- **Then** the system calculates each farmer's payment (deliveries × price - loan repayments - input deductions)
- **And** presents a preview with totals by farmer, class, branch
- **And** on my confirmation, each farmer's GenServer triggers an M-Pesa B2C disbursement saga
- **And** sagas execute in parallel (with concurrency limit to respect M-Pesa API rate limits)
- **And** each successful disbursement triggers SMS to the farmer
- **And** failed disbursements are queued for manual review without blocking others
- **And** the full cycle completes in under 1 hour for 3,500 farmers
- **And** an audit report is produced showing every payment and its status

### 4.5 Epic: Input Distribution and Loans

**User Story 4.5.1:** As a cooperative manager, I want to run the annual fertilizer distribution as a coordinated workflow with per-farmer allocations, delivery logistics, and automatic loan setup, so that inputs reach farmers on time without manual tracking.

**Acceptance Criteria:**
- **Given** a planned input distribution (e.g., 500 tons of fertilizer)
- **When** I configure the distribution (product, allocation formula, price, repayment terms)
- **Then** each farmer's allocation is calculated (e.g., 50kg per acre coffee)
- **And** each farmer receives SMS with their allocation and opt-in / opt-out choice
- **And** farmers who opt in are assigned to distribution points and dates
- **And** distribution-point clerks can check off deliveries in real-time
- **And** each distribution automatically creates a loan on the farmer's account
- **And** the loan appears in the farmer's USSD balance and next payment deduction

### 4.6 Epic: Extension Officer Workflows

**User Story 4.6.1:** As an extension officer in the field, I want to log farm visits offline and have them sync when I'm back in coverage, so that I can work in remote areas without losing data.

**Acceptance Criteria:**
- **Given** an extension officer logged into the Extension Officer BFF on their phone
- **When** they visit a farmer in an area with no connectivity
- **Then** they can log the visit (GPS, duration, advice topics, photos, follow-up actions)
- **And** the data persists locally
- **And** when coverage returns, data syncs to the server within 60 seconds
- **And** the farmer's GenServer processes the visit event, updating their profile
- **And** the cooperative sees the visit in real-time reports

### 4.7 Epic: Traceability for Buyers

**User Story 4.7.1:** As a coffee buyer (e.g., Nairobi Coffee Exchange, direct-trade buyer), I want to trace a coffee lot back to the farmers who contributed to it, so that I can offer provenance premiums.

**Acceptance Criteria:**
- **Given** a lot of processed coffee ready for sale
- **When** the buyer requests traceability via the Buyer BFF
- **Then** they see the aggregated contributing farmers (anonymized to ID if privacy required)
- **And** grade distribution, region, processing method
- **And** a cryptographic hash proving lot composition (optionally on public blockchain for premium lots)

---

## 5. Non-Functional Requirements

### 5.1 Performance

| Metric | Target |
|--------|--------|
| Delivery recording (collection-point UX) | < 10 seconds end-to-end |
| USSD response time (per screen) | < 3 seconds |
| SMS delivery latency (P95) | < 30 seconds |
| Monthly payment run (3,500 farmers) | < 1 hour |
| Farmer GenServer spawn time | < 100ms |
| Phoenix LiveView dashboard update | < 2 seconds |

### 5.2 Availability

| Component | Target |
|-----------|--------|
| Cooperative Officer BFF (back-office) | 99.5% (office hours) |
| Farmer USSD/SMS interface | 99.9% (this is the trust system) |
| Payment runs | Must never corrupt state — prefer failure over partial |
| GenServer supervision | 99.99% (automatic restart on crash) |

### 5.3 Scalability

- Support cooperatives from 500 to 15,000 members
- Support a single platform instance serving 50+ cooperatives (multi-tenant)
- Support seasonal delivery spikes (10x normal during harvest)
- Horizontally scale Phoenix nodes behind a load balancer
- BEAM cluster for GenServer distribution (farmers sharded across nodes)

### 5.4 Connectivity Tolerance

- Collection-point UX works offline (2G-tolerant, sync later)
- Extension officer app works fully offline
- Cooperative back-office requires connectivity (acceptable — rural HQ typically has a connection)
- Farmer USSD/SMS has no offline requirement (channel itself is the solution)

### 5.5 Language Support

- UI in Swahili, English (initial)
- Expandable to Kikuyu, Luo, Kamba (depending on cooperative's member dominant language)
- SMS template localization (farmer receives messages in their preferred language)

### 5.6 Security

- **Authentication:** 
  - Cooperative staff: email/password + MFA for managers
  - Extension officers: phone number + PIN (simpler for field)
  - Farmers: no login (SMS/USSD authenticated by SIM)
- **Authorization:** RBAC; farmer can only see their own data; cooperative staff see their cooperative only
- **PII handling:** Farmer national IDs encrypted; phone numbers hashed for lookups; access auditing
- **Financial controls:** Payment runs require dual approval (officer initiates + manager approves)
- **Compliance:** Kenya Data Protection Act; cooperative sector regulations

### 5.7 Observability

- Per-cooperative dashboards (metrics they care about: active farmers, delivery volume, payment accuracy)
- Platform-wide monitoring (Erlang observer, Phoenix LiveDashboard, Grafana for business metrics)
- Alerting: payment failures, SMS delivery drops, USSD response degradation
- GenServer health monitoring (supervision tree visualizations)

---

## 6. Success Metrics

### 6.1 Business Metrics (End of Week 15)

| Metric | Target |
|--------|--------|
| Paying cooperatives | 2+ |
| Total farmers registered | 5,000+ |
| Monthly Recurring Revenue | $1,000+ |
| Transaction volume (farmer payments) | $100K+ |
| Transaction fee revenue | $500+ |

### 6.2 Operational Metrics

| Metric | Target |
|--------|--------|
| Payment accuracy | 99.99%+ (farmer-perceived errors < 1 per 10,000 payments) |
| Farmer NPS (via SMS survey) | > 50 |
| SMS delivery success rate | > 99% |
| USSD session completion rate | > 90% |
| Collection-point clerk time per delivery | < 30 seconds |

### 6.3 Technical Metrics

| Metric | Target |
|--------|--------|
| BEAM cluster uptime | > 99.95% |
| GenServer crash rate | < 0.001% per day (crashes should be vanishingly rare) |
| Payment run completion in under 1 hour | 100% |
| Code coverage on domain logic | > 85% |

---

## 7. Architecture Mapping

### 7.1 Primary Pattern Introduced: Actor Model + OTP Supervision

Shamba is the archetypal Erlang/OTP use case: millions of independent entities (farmers), each with long-lived state, each capable of failing independently without affecting others. Phoenix + GenServer + supervision trees is the natural architecture.

**Compounding patterns from prior tiers:**
- **BFF pattern (Tier 1):** 4 BFFs (Farmer/USSD-SMS, Cooperative Officer, Buyer, Extension Officer)
- **Event-driven (Tier 1):** Delivery events, payment events, visit events flow between GenServers and into projections
- **CQRS (Tier 2):** Command side is OTP; query side is Phoenix LiveView + PostgreSQL projections
- **Sagas (Tier 2):** Payment disbursement is a saga orchestrated by a dedicated supervisor
- **Offline-first (Tier 3):** Extension officer app uses CRDTs; collection point uses event log + sync
- **Hexagonal (Tier 4):** Each context has ports; M-Pesa, SMS, USSD are adapter implementations

### 7.2 The OTP Architecture

**Farmer GenServer:**
- One process per registered farmer
- State: YTD deliveries, pending payments, active loans, last visit, preferences
- Handles: delivery events, payment events, loan updates, visit logs
- Supervised by a `DynamicSupervisor`
- Passivated to database after idle period; rehydrated on demand

**Cooperative Supervisor:**
- Supervises all Farmer GenServers belonging to a cooperative
- Restart strategy: `:one_for_one` — one farmer crash doesn't affect others
- Handles cooperative-wide broadcasts (e.g., "payment run starting")

**Payment Saga Supervisor:**
- Spawns a saga GenServer per payment run
- Coordinates parallel M-Pesa disbursements with concurrency limits
- Supervision ensures saga state survives node crashes (via persistent state + recovery)

**Extension Officer GenServer:**
- One per active officer
- Tracks assigned farmers, planned visits, pending sync from offline app

### 7.3 The Ruby and PHP Roles

**Why Elixir for the core:** described above — actor model fit.

**Why Ruby for admin UI:**
- Rails is the fastest framework for CRUD-heavy back-office UIs
- Cooperative admin (user management, permissions, billing, reports) is pure CRUD
- Rails conventions save weeks of work vs rebuilding these in Phoenix

**Why PHP/Laravel for the public marketplace:**
- Public-facing cooperative website + member portal
- Traceability browser for buyers
- Laravel has excellent SEO tooling (important for public pages)
- Mature PHP hosting in East Africa means cooperatives can self-host if they want white-label

**The lineage deliberately taught:** Rails (2005) → Laravel (2011) → Phoenix (2014) is the web framework evolution. Building all three in one project demonstrates how the conventions propagated and diverged.

### 7.4 The Four BFFs

| BFF | Client | Technology | Key Responsibilities |
|-----|--------|------------|---------------------|
| Farmer BFF | USSD menus + SMS | Elixir (GenServer-based USSD handler) | Balance, loans, visit requests, SMS notifications |
| Cooperative Officer BFF | Web back-office (Rails) | Ruby on Rails + React embeds | Farmer management, delivery recording, payment runs, reports |
| Buyer BFF | Public website + API (Laravel) | PHP/Laravel + Blade | Lot browsing, traceability, purchase orders |
| Extension Officer BFF | Mobile PWA (Phoenix LiveView) | Elixir Phoenix LiveView | Visit logging (offline), farmer prioritization, outcome tracking |

### 7.5 Technology Stack

**Backend:**
- Elixir 1.17+ with OTP (core farmer processes, payment sagas)
- Phoenix 1.7+ (LiveView for real-time back-office; API endpoints)
- Ruby 3.3+ with Rails 7.2+ (cooperative admin UI)
- PHP 8.3+ with Laravel 11 (public marketplace, traceability)

**Data:**
- PostgreSQL (farmers, deliveries, payments, loans, events)
- Redis (session, pub/sub, caching)
- Mnesia (optional, for hot farmer cache in BEAM cluster)

**Integrations:**
- M-Pesa Daraja (B2C farmer payments, C2B input loan repayments)
- Africa's Talking (SMS bulk, voice notifications, USSD short code)
- Safaricom USSD gateway
- WhatsApp Business API (v1.5 feature)

**Infrastructure:**
- AWS (af-south-1 for Kenya data residency)
- Kubernetes (EKS)
- Erlang distribution for BEAM clustering
- Terraform, ArgoCD

---

## 8. Phased Rollout Plan

### 8.1 MVP (Week 10, end of Tier 5a sprint)

**Scope:**
- Farmer GenServer per member (OTP core)
- Cooperative Officer BFF with farmer registration and delivery recording
- Basic SMS notifications
- M-Pesa payment integration (live, testing with small amounts)
- One pilot cooperative onboarded (free tier)

**Commercial goal:** 1 pilot cooperative actively using the platform with 500+ farmers.

### 8.2 v1.0 (Week 15)

**Scope:**
- USSD interface fully live
- All 4 BFFs operational
- Payment runs at full scale
- Input distribution and loan module
- Extension officer mobile app
- 2 paying cooperatives; 5,000+ farmers

### 8.3 v1.5 (Months 4-5 post-sprint)

**Scope:**
- Traceability with cryptographic proof
- Buyer marketplace (connects buyers to verified lots)
- WhatsApp channel alongside SMS
- AI-powered agronomy advice (LLM-driven, tailored to crop + region)
- 10+ paying cooperatives

### 8.4 v2.0 (Year 2)

- Pan-East-Africa expansion (Uganda, Tanzania, Rwanda)
- Credit scoring for farmer loans based on delivery history
- Direct-to-buyer marketplace (farmers sell directly for premium prices)
- Carbon credit integration (regenerative agriculture tracking)

---

## 9. Commercial Terms

### 9.1 Pricing Tiers

| Tier | Price | Features | Target |
|------|-------|----------|--------|
| **Pilot** | Free for 6 months | Up to 500 farmers | New cooperatives, onboarding |
| **Growth** | $0.50/farmer/month | All core features | Small cooperatives (500-2,000 farmers) |
| **Standard** | $0.40/farmer/month | All features + priority support | Mid cooperatives (2,000-10,000) |
| **Enterprise** | Negotiated (from $0.30/farmer/month) | Custom integrations, dedicated support, on-prem option | Large cooperatives (10,000+) |
| **Transaction fee** | 0.5% on M-Pesa disbursements | All tiers | On total payment volume |

### 9.2 Customer Acquisition

- **Partnerships with cooperative umbrellas:** Kenya Co-operative Coffee Exporters, KTDA, Kenya Dairy Board, New KPCU
- **Donor-funded pilots:** World Bank, USAID, KCB Foundation (fund initial cooperative onboarding)
- **Extension agency partnerships:** Ministry of Agriculture extension officers become de facto advocates
- **Pan-African Farmers Organization (PAFO)** network for multi-country expansion
- **Existing personal network:** Eric's existing contacts in Kenyan agriculture

---

## 10. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|-----------|
| Cooperative adoption is slow (trust-based sector) | High | High | Start with pilot cooperatives through personal network; paid pilot with success-fee pricing possible |
| BEAM cluster operational complexity | Medium | Medium | Start with single-node deployment; cluster only when 10+ coops loaded |
| M-Pesa bulk payment rate limits | Medium | High | Coordinate with Safaricom for elevated limits; smooth payment runs across time windows |
| Connectivity in remote collection points | High | Medium | Offline-first design; sync when possible |
| Farmer literacy / phone literacy | Medium | Medium | USSD menus in local languages; voice call fallbacks; extension officer training |
| Donor-funded pilots end (common pattern) | High | Medium | Sustainable SaaS pricing from Day 1; no reliance on grant money for operations |

---

## 11. Open Questions

1. Should farmer loans be originated on Shamba, or integrated with a partner MFI (e.g., LendStream)? **Answer:** Integrate with LendStream — cross-platform synergy; avoid building full lending stack.
2. Do we support horticulture (vegetable) cooperatives from Day 1, or coffee/tea/dairy only? **Answer:** Coffee first (Eric's origin region), dairy second; horticulture in v1.5.
3. WhatsApp Business API costs $0.005-$0.02 per message in Kenya; is this sustainable at scale? **Answer:** SMS primary; WhatsApp for premium tier with acceptable margins.
4. Should farmer data be owned by the cooperative, the farmer, or the platform? **Answer:** Farmer owns their personal data (per Kenya DPA); cooperative has business use rights; platform has processing rights only.

---

## 12. Appendix: Definition of Done for v1.0

- [ ] All user stories in Section 4 have passing acceptance tests
- [ ] 2 cooperatives live in production (1 paid, 1 final-stage pilot)
- [ ] 5,000+ farmers registered
- [ ] Monthly payment run successfully executed for full farmer base
- [ ] USSD response time consistently under 3 seconds
- [ ] SMS delivery rate > 99% over 30-day window
- [ ] BEAM cluster stable; supervision restart rate normal
- [ ] Security audit passed (financial + PII threat model)
- [ ] Documentation: admin guide (Swahili + English), extension officer guide, USSD reference
- [ ] Onboarding playbook for new cooperatives (template contracts, training materials, data migration scripts)
- [ ] On-call rotation (harvest season stakes are high)

---

## 13. Module B — Greenland AgriTech (Kajiado Farm as Proving Ground)

### 13.1 Framing

Eric operates a commercial farm in Kajiado County (semi-arid, drip-irrigation-dependent, growing onions among other horticulture produce). This farm is not just a personal interest — it is the **ideal first customer and product laboratory** for an AgriTech platform. The difference between Shamba Module A (cooperatives) and Greenland Module B is the unit of analysis:

| | **Shamba** (Module A) | **Greenland** (Module B) |
|---|----------------------|--------------------------|
| **Unit** | Cooperative + its members | Individual commercial farm |
| **Scale** | 500-15,000 farmers | 1-500 acres |
| **Primary user** | Cooperative officer | Farmer / farm manager / agronomist |
| **Value prop** | Operational & financial backbone | Decision support, yield optimization, ROI maximization |
| **Pricing** | Per-farmer subscription | Per-farm subscription + per-hectare premium features |
| **Kajiado farm role** | N/A | First customer, first pilot, first case study |

### 13.2 Problem Statement (Farm-Level)

Commercial horticulture in Kenya (onions, tomatoes, capsicum, flowers for export, etc.) has high revenue potential but is riddled with avoidable losses:

1. **Water is the most expensive input in Kajiado** and most semi-arid regions. Irrigation scheduling is typically done by instinct ("looks dry, water"), leading to both over-watering (wasted water, root disease) and under-watering (yield loss).

2. **Pest and disease diagnosis is reactive.** Farmers notice plant damage, then call an agronomist (if they have one), then wait days for intervention. By then, 20-40% of the crop may be compromised. Early image-based diagnosis could catch outbreaks at 2-3% damage.

3. **Yield predictions are guesswork.** Most farmers don't know what they'll harvest until they harvest it. This makes pre-selling (getting contracts at better prices) and financing nearly impossible.

4. **ROI per plot is not tracked.** A 10-acre farm growing 4 crops rarely knows which crop earned the best return per hectare, per cubic meter of water, per labor-hour. Investment decisions next season are therefore not data-driven.

5. **Climate variability is increasing.** Kajiado rains are less predictable year-on-year. Planting windows shift. Farmers relying on traditional calendars are being caught off-guard.

6. **Market timing is guess-based.** Onion prices can vary 5x within a 6-week window. Farmers who can time harvest and storage to peak pricing windows can multiply revenue.

### 13.3 Quantified Market

- **Kenya commercial horticulture farms (10+ acres):** ~15,000
- **Kenya smallholder commercial farms (1-10 acres with cash crops):** ~500,000
- **Pan-African commercial horticulture (East + Southern Africa):** ~200,000 farms at Greenland's target size
- **Current AgriTech solutions:** Fragmented. Apollo Agriculture (inputs + advice). iCow (SMS advice). Hello Tractor (equipment). None do integrated decision support well.
- **Pricing assumption:** $15-$150/month depending on farm size and feature tier. Kajiado farm alone would be $50-$100/month at self-pricing — multiply by 500 similar farms and the math works.

### 13.4 Feature Set (Ordered by "Problems That Will Surface First" on the Kajiado Farm)

The module is designed around Eric's explicit principle: **organically surfaced problems become first-class features.** These are the expected problem-surfacing order:

#### **F1 — Irrigation Scheduling Optimization** (highest immediate value)

- Soil moisture sensors (multi-depth capacitive probes) deployed across plot zones
- ESP32-based sensor gateways (bridges to Module B of Sauti/Lee Audio Embedded!) that report every 15 minutes via LoRaWAN or GSM
- Weather station (OTT-MF-1 or equivalent) or integration with Kenya Meteorological Department data
- Evapotranspiration model: FAO-56 Penman-Monteith as baseline, refined with on-farm data
- Recommendation engine: "Zone 3 needs watering in 6 hours; Zone 1 can wait 2 days"
- Solenoid valve integration (future): irrigation controller acts on recommendations autonomously with farmer veto

#### **F2 — Yield Prediction** (ROI clarity)

- Historical yield data captured per plot, per crop, per season
- Growing-degree-day (GDD) tracking using farm weather data
- Plant density and health indices from computer vision scans (F3 feeds this)
- Machine learning model: Random Forest or gradient boosting on historical + current features
- Output: expected harvest tonnage range with confidence interval, updated weekly
- Commercial value: farmers can pre-sell contracts with confidence; financiers can underwrite operations with data

#### **F3 — Computer Vision for Pest and Disease Diagnosis**

- Farmer takes photos on phone (or fixed cameras on future drone/ground robot)
- Cloud-based CNN classifier trained on African pest/disease dataset
- Outputs: identified pest/disease, severity, recommended treatment, treatment cost estimate
- Initial models: fine-tuned PlantVillage + Crop Pest Diagnosis dataset; African-specific fine-tuning in v1.5
- Fallback: human agronomist review for uncertain cases (queue-based)
- Integration: diagnosis triggers F5 (input recommendation) and F7 (cost tracking)

#### **F4 — Climate and Weather Forecasting for Farm Operations**

- Integration with Kenya Met Department, ECMWF, and commercial weather APIs
- Farm-localized forecasts (downscaled from regional models using farm microclimate data)
- Alerts: "60% chance of rain in next 48 hours; consider delaying fertilizer application"
- Frost, hail, and extreme temperature warnings
- Planting window recommendations based on seasonal forecasts

#### **F5 — Input Optimization (Fertilizer, Pesticide, Seed)**

- Soil test integration (farmer uploads lab results; system interprets)
- Per-crop, per-plot fertilizer recommendations
- Pesticide usage tracking with pest-pressure-triggered applications only (not calendar-based overuse)
- Seed variety selection tool based on local conditions, market demand, disease resistance
- Integration with Apollo Agriculture or similar for input ordering

#### **F6 — ROI and P&L per Plot**

- Revenue tracking per crop per plot (tons harvested × market price at time of sale)
- Cost tracking: inputs, labor, water (!), equipment, overhead
- Water ROI specifically: revenue per cubic meter of irrigation water used
- Labor ROI: revenue per labor-hour
- Comparative: this season vs last season; this crop vs alternatives
- Output: season-end report with next-season recommendations

#### **F7 — Market Intelligence and Timing**

- Wholesale market price feeds (Wakulima market, Gikomba, Mombasa market)
- Price trend analysis: when is the onion window peaking?
- Storage capacity and decay modeling (if you hold onions 2 more weeks, what's the net upside vs storage cost and shrinkage?)
- Contract offer surfacing (buyers looking for specific produce at specific volumes)
- Integration potential with Shamba's buyer marketplace (cross-module synergy)

#### **F8 — Labor and Operations Management**

- Workforce scheduling (plant, weed, spray, harvest crews)
- Task-based pay tracking (M-Pesa integration for worker payments)
- Productivity per worker analytics
- Training content in Swahili / Kikuyu / Maasai (given Kajiado context) for workers

#### **F9 — Traceability for Premium Markets**

- Per-batch tracking from plot to sale
- Good Agricultural Practices (GAP) compliance documentation
- Export certification support (KEPHIS, GlobalG.A.P.)
- Enables farm-to-buyer premium positioning (European supermarket chains, export markets)

### 13.5 Architecture (Leverages Prior Sprint Patterns)

Greenland deliberately reuses architectural patterns from elsewhere in the sprint:

| Pattern | Source Tier | Application in Greenland |
|---------|-------------|-------------------------|
| Actor model (farm-as-actor, plot-as-actor) | Tier 5a Shamba | Each farm and plot has a supervised GenServer owning state |
| Event sourcing (all farm events immutable) | Tier 2 LendStream | Every sensor reading, observation, decision recorded as event |
| CRDT for offline mobile app | Tier 3 Sherehe | Farm manager app works in poor-connectivity field |
| Hexagonal core | Tier 4 Unicorns | Sensor adapters, weather adapters, market-data adapters all pluggable |
| ML pipeline (Rust + PyO3) | Tier 1 Sauti + Vishnu experience | Yield prediction and CV models served via proven infrastructure |
| LLM explanation layer | Tier 5b BSD Engine | "Why does the system recommend watering today?" answered in natural language |

### 13.6 Hardware Requirements (Kajiado Farm Proving Ground)

Initial sensor deployment for the Kajiado farm:

| Device | Quantity | Approx Cost (KES) | Role |
|--------|----------|---------------------|------|
| Soil moisture sensor (capacitive, multi-depth) | 8-12 | 2,500 each | Spread across zones |
| ESP32-S3 + LoRa gateway | 2-3 | 4,000 each | Aggregates sensor data |
| Weather station (pro-sumer: Davis Vantage Vue or equivalent) | 1 | 45,000 | Rain, wind, solar, temp, humidity |
| Flow meters on irrigation lines | 4-6 | 3,500 each | Water usage per zone |
| Camera (fixed, solar-powered, time-lapse) | 2-3 | 12,000 each | Visual crop monitoring |
| **Total initial hardware budget** | | **~200,000 KES (~$1,500)** | |

This is deliberately Lee Audio Embedded + Greenland overlap territory — the sensor gateways and controllers use the exact hardware stack from Module B Section 13 of the Sauti PRD. The cross-learning is the point.

### 13.7 Commercial Pathway

**Months 1-4 (overlap with sprint):**
- Kajiado farm runs as internal pilot
- Sensor hardware deployed, data streaming, basic irrigation recommendations
- Farm manager uses the mobile app; feedback captured

**Months 5-12 (Year 1 post-sprint):**
- 3-5 paying pilot farms (other Kajiado farms, Laikipia ranches, Naivasha flower farms)
- v1.0 feature set stabilized (F1-F4 core, F5-F6 in beta)
- Pricing: $50-$100/month per farm at pilot; likely free for first 6 months to collect data

**Year 2:**
- 20-50 paying farms across Kenya
- Features F7-F9 shipped
- Export market capability (F9) enables premium positioning for farms
- $500-$1,500/month tier for larger commercial operations

**Year 3:**
- Pan-East-Africa expansion (Tanzania, Uganda, Rwanda, Ethiopia)
- Partnerships with fertilizer companies (Yara, Apollo), financing (LendStream integration), buyers (export consolidators)
- $50K+ MRR target

### 13.8 Pricing Tiers (Greenland)

| Tier | Price | Features | Target |
|------|-------|----------|--------|
| **Greenland-Scout** | $15/month | 1 farm, F1 + F4 (irrigation + weather), mobile app | Smallholders, early adopters |
| **Greenland-Grow** | $50/month | Up to 50 acres, F1-F5 (adds CV diagnosis, input optimization) | Mid-size commercial farms |
| **Greenland-Pro** | $150/month | Up to 500 acres, all features F1-F9, priority support | Large commercial operations |
| **Greenland-Enterprise** | From $500/month | Multi-farm, custom ML models, white-label, dedicated agronomist support | Flower farms, export operations, corporate farms |
| **Hardware** | At-cost + 15% margin | Sensor kits, gateways, weather stations | Starter + expansion packs |

### 13.9 Sprint-Era Commitment (Greenland Specifically)

Like Module B of Sauti, this is scoped lightly for the sprint period:

| Week | Commitment | Hours |
|------|------------|-------|
| Week 9-10 (Tier 5a main focus is Shamba cooperative platform) | Design Greenland schema; prototype farm GenServer; sketch sensor data model | 8-10 hours |
| Week 11-12 (Tier 5b) | BSD Engine DSL explored for agricultural rules ("if soil moisture < X AND forecast dry THEN water Zone Y") | 5-8 hours |
| Week 13-14 (Tier 6) | Deploy 2-3 soil moisture sensors on Kajiado farm; confirm data flow end-to-end | 10-15 hours (includes physical farm time) |
| Week 15 | Basic irrigation recommendation live for one plot | 5-10 hours |

**Total sprint-era Greenland commitment:** ~30-45 hours. Fits within the "Saturday project variations" pattern — Greenland becomes the Saturday project on weeks when the primary-tier Saturday project is ahead of schedule.

### 13.10 Synergy with Other Sprint Projects (Greenland Specifically)

- **Shamba Module A (cooperatives):** Greenland farms may deliver into Shamba cooperatives; data flow in both directions — Greenland shares yield data with coop; coop shares market data with Greenland
- **Lee Audio Embedded:** Hardware platform shared; farm sensor gateways and controllers are literally Lee Audio Embedded products configured for agriculture
- **BSD Engine v2:** Agronomy rules defined in the same DSL that BSD uses for consulting diagnostics
- **Sauti:** Field workers get voice-controlled logging in Swahili/Maasai — "Ngombe tatu zimeingia shamba la kitunguu" (three cows entered the onion field) becomes a tagged alert
- **LendStream:** Farm ROI data becomes input to agricultural credit scoring (farmers with better data get better loan terms)
- **PayGoHub:** Solar-powered irrigation pumps financed via PayGoHub; Greenland usage data proves payback

### 13.11 Risks Specific to Greenland

| Risk | Mitigation |
|------|------------|
| Sensor hardware fails in harsh farm conditions (dust, heat, theft) | IP67-rated enclosures; theft-resistant mounting; redundant sensors per zone |
| Connectivity in remote Kajiado | LoRaWAN for sensor-to-gateway; GSM uplink from gateway; store-and-forward on gateway |
| Farm manager/workers don't adopt the mobile app | SMS/USSD fallbacks; training; the farm owner (Eric) is the first user — dogfooding matters |
| ML model accuracy insufficient for real farming decisions | Start with advisory only (not autonomous control); gather data; improve iteratively |
| Kenyan weather data quality is poor | Invest in on-farm weather station early; don't rely solely on national data |
| Regulatory (KEPHIS, KALRO) constraints on autonomous farm systems | Start advisory; avoid autonomous decisions on pesticide application or land management until regulations clear |

### 13.12 Definition of Done for Greenland v0.1 (by end of sprint)

- [ ] 2-3 soil moisture sensors operational on the Kajiado farm
- [ ] ESP32 gateway streaming data to cloud
- [ ] Dashboard showing farm sensor data in near-real-time
- [ ] Farm GenServer architecture implemented (minimum: per-plot state tracking)
- [ ] First irrigation recommendation rule encoded in DSL
- [ ] Basic yield history recorded for onion crop
- [ ] Documentation: hardware setup guide, deployment photos, lessons learned
- [ ] Decision on commercial pathway: standalone product or Shamba add-on

---

## 14. Relationship Between Modules A (Shamba) and B (Greenland)

**Module A (Shamba)** is the **cooperative-scale product** — operating backbone for the cooperative itself and its many farmer-members.

**Module B (Greenland)** is the **farm-scale product** — decision-support toolkit for individual commercial farms.

They share codebase foundations, architectural patterns, and team — but serve different buyers and solve different problems.

**Decision tree for where a feature goes:**
- "Does this feature scale linearly with number of cooperatives?" → Shamba
- "Does this feature scale linearly with acres of farmland?" → Greenland
- "Does it scale with both but via different mechanisms?" → Probably a shared service with context-specific BFFs

A commercial farm growing onions is a Greenland customer. A coffee cooperative with 5,000 smallholders is a Shamba customer. A Kajiado-based onion-farming cooperative with a commercial processing line might be both — using Greenland for the central farm and Shamba for member coordination.
