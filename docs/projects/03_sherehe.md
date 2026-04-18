# PRD — Sherehe

> **Version:** 1.0
> **Date:** April 2026
> **Status:** Draft — Approved for Sprint Weeks 5-6
> **Owner:** Eric Gitangu (Deveric Technologies)
> **Tier:** 3 (JavaScript + TypeScript)
> **Project Type:** New Greenfield
> **Name meaning:** *Sherehe* = "celebration/event" in Swahili

---

## 1. Executive Summary

**Sherehe** is an autonomous event orchestration platform for East Africa — from 30-person birthday parties at home to 10,000-person corporate conferences at KICC (Kenyatta International Convention Centre). It handles the full event lifecycle: pre-event planning and pricing, vendor coordination, real-time execution with autonomous contingency handling, and post-event settlement.

The platform's distinguishing capability is **real-time autonomous orchestration**. When the caterer runs 30 minutes late, Sherehe automatically: notifies the MC to extend the program, re-sequences the agenda, alerts the venue to adjust bar timing, and triggers a backup catering option if the delay exceeds a configured threshold. No human orchestrator needs to be in the loop for routine contingencies.

Sherehe sits at the intersection of what most existing tools do separately — Eventbrite (ticketing), Aisle Planner (wedding coordination), WeddingWire (vendor directory), Monday.com (project planning) — while adding the autonomous orchestration layer that none provide.

**Commercial opportunity:** Kenya has 10,000+ event planners, 500+ venues, and growing corporate event spend. Pan-African event industry is estimated at $8B+ annually. Primary revenue path: SaaS for event planners ($49-$499/mo) + transaction fees on vendor bookings (2-3%).

---

## 2. Problem Statement

### 2.1 The Pain

1. **Event planning is spreadsheet hell.** Most Kenyan event planners manage 10-30 active events simultaneously in Excel, WhatsApp groups, and a few scattered tools. Changes in one place don't propagate. Vendors get called at the wrong times. Budgets slip silently.

2. **Vendor discovery and pricing is opaque.** There's no Kayak-for-event-vendors. Planners call 5-10 vendors per category (catering, MC, photography, decor, sound, security, venue) and negotiate individually. Pricing is not benchmarked; clients overpay or underpay routinely.

3. **Execution day is chaos.** On event day, the planner is running between vendors with a clipboard and a phone. When something goes wrong (caterer late, rain starts, speaker cancels), manual re-coordination takes 30-60 minutes during which the event stalls.

4. **Contingency plans are theoretical.** Most events have a "rain plan" that exists in someone's head or a Google Doc. When rain actually comes, activation depends on humans remembering the plan and coordinating execution.

5. **Offline execution is required.** Many Kenyan venues have poor/no WiFi. Event staff can't rely on connectivity during execution. Apps that require constant network access are unusable in the field.

6. **Post-event settlement is painful.** Splitting payments with 8-15 vendors, reconciling deposits, handling disputes — all manual, often delayed 30-60 days.

### 2.2 Quantified Market

- **Kenyan event planners:** 10,000+ individual planners; 500+ registered event management companies
- **Annual Kenyan event market:** $800M+ (corporate + social + government)
- **Pan-African event market:** $8B+ and growing at 7-10% annually
- **Sherehe's initial target:** Nairobi event planners handling mid-to-large events ($10K+ budgets). Estimate 2,000+ such planners.

### 2.3 Why Now

- Kenya's middle class is growing, driving demand for professional event planning
- Corporate event spend is rebounding post-pandemic
- Real-time multiplayer collaboration tech (CRDTs via Yjs/Automerge, WebRTC) is production-ready
- LLM-assisted planning (price suggestions, vendor matching, contingency generation) is now tractable and cheap
- Mobile penetration in Kenya is 90%+; most planners own smartphones

---

## 3. Target Users & Personas

### 3.1 Primary Persona: Event Planner

**Name:** Wanjiku, 34, Nairobi
**Role:** Owner of a boutique event planning firm, handles 15-25 events/year ranging $5K-$150K
**Goals:**
- Run 10+ events simultaneously without dropping details
- Generate accurate quotes in under 30 minutes (currently 2-3 days)
- Execute events on time with fewer "fires"
- Grow her business without linearly growing her headcount

**Pain points:**
- Clients call at 11pm asking for budget updates; she doesn't have real-time answers
- Her 2 assistants each track different versions of vendor lists
- Vendors complain about last-minute changes that weren't communicated
- She loses 10-15% of quoted revenue to scope creep she can't track

**Jobs-to-be-done:** Turn her current manual coordination into a platform that handles 80% of communication, pricing, and execution automatically, freeing her to focus on client relationships and creative direction.

### 3.2 Secondary Persona: Event Client

**Name:** James, 38, corporate marketing manager
**Role:** Planning his company's 300-person annual conference; this is a side-project for him
**Goals:**
- Transparent pricing and timeline
- Approve things quickly on mobile during meetings
- Get automatic updates without chasing the planner
- Feel confident execution day will go smoothly

**Pain points:**
- Currently gets pricing surprises from vendors his planner booked
- Communication with planner is via WhatsApp; he loses track of decisions
- Has no visibility into execution-day plan until 48 hours before

**Jobs-to-be-done:** Be an engaged, informed client without having to micromanage. Approve decisions fast; trust the plan.

### 3.3 Tertiary Persona: Vendor

**Name:** Peter, 41, catering company owner, serves 150+ events/year
**Role:** Caters for 5-10 event planners regularly plus direct clients
**Goals:**
- Steady booking flow
- Get paid on time (currently 60-90 day cycles)
- Avoid last-minute changes that disrupt his kitchen

**Pain points:**
- Constantly chasing invoices
- Planners change menus 3 days before events; he absorbs the cost
- No quality rating system means good and bad caterers compete on price only

**Jobs-to-be-done:** Predictable bookings, faster payments, reputation-based pricing premium for quality work.

### 3.4 Non-Target Users (Explicit)

- **Individual consumers for tiny events** (10-person birthday parties) — handled better by WhatsApp; not our ICP
- **Ticketing-only use cases** — Eventbrite dominates; we are not competing on pure ticketing
- **Wedding planners exclusively** — we serve weddings but are not wedding-specific like Aisle Planner

---

## 4. User Stories & Acceptance Criteria

### 4.1 Epic: Pre-Event Planning and Pricing

**User Story 4.1.1:** As an event planner, I want to generate a complete event quote in under 30 minutes based on event type, size, date, and location, so that I can respond to client inquiries same-day.

**Acceptance Criteria:**
- **Given** a new event inquiry with type (wedding/corporate/social), guest count, date, and location
- **When** I use the Planner BFF to generate a quote
- **Then** the system suggests vendor categories needed (catering, venue, decor, sound, etc.)
- **And** for each category, provides 3-5 vendor options with benchmarked pricing
- **And** generates a total budget estimate with line items
- **And** the quote PDF is produced in under 5 minutes
- **And** I can adjust any line and see total recalculate in real-time
- **And** my client can view/approve the quote via a shareable link

**User Story 4.1.2:** As a planner, I want the platform to forecast inventory and package pricing based on seasonal demand and vendor availability, so that my quotes are competitive without being loss-leaders.

**Acceptance Criteria:**
- **Given** 50+ historical events in the platform
- **When** I quote a new event
- **Then** the system flags line items that are underpriced compared to historical benchmarks
- **And** suggests adjustments for seasonal factors (e.g., December weddings cost 25% more)
- **And** warns if critical vendors are unavailable on the requested date

### 4.2 Epic: Real-Time Collaborative Planning

**User Story 4.2.1:** As a planner, I want my 2 assistants and I to edit the event plan simultaneously without conflicts, so that we stay in sync even when we're all updating things on our phones.

**Acceptance Criteria:**
- **Given** three users (planner + 2 assistants) logged into Sherehe on their mobile devices
- **When** they all edit different fields of the same event simultaneously
- **Then** changes merge automatically via CRDTs without conflict dialogs
- **And** each user sees others' changes within 5 seconds when online
- **And** if one user goes offline and makes changes, those changes merge cleanly when they reconnect
- **And** a full event history log shows who changed what and when

**User Story 4.2.2:** As a planner in a venue with spotty WiFi, I want to continue working offline and have changes sync when connectivity returns, so that I don't lose work.

**Acceptance Criteria:**
- **Given** an active event being edited
- **When** my device loses internet connectivity
- **Then** all features continue working (edit, view, add notes, log decisions)
- **And** changes are persisted locally in IndexedDB
- **And** when connectivity returns, changes sync automatically within 30 seconds
- **And** no user intervention is required to resolve sync

### 4.3 Epic: Autonomous Execution-Day Orchestration

**User Story 4.3.1:** As a planner on event day, I want the platform to autonomously handle routine contingencies (vendor delays, small schedule adjustments, notifications) so that I can focus on VIP clients and creative problems.

**Acceptance Criteria:**
- **Given** an active event with configured vendor arrival times and contingency rules
- **When** the caterer's GPS-tagged arrival is 20+ minutes behind schedule
- **Then** the system autonomously:
  - Sends SMS to MC to delay the opening by 20 minutes
  - Notifies the bar to extend pre-drinks service
  - Alerts the photographer to the schedule shift
  - Triggers a "supervisor-needs-to-know" notification to me if delay exceeds 45 min
- **And** I can see the autonomous action log in real-time
- **And** I can override any autonomous action with one tap

**User Story 4.3.2:** As a planner, I want pre-configured contingency packages (rain plan, power outage, no-show) that can activate with one tap or autonomously based on conditions, so that execution-day chaos becomes execution-day calm.

**Acceptance Criteria:**
- **Given** an event with configured "rain plan" contingency
- **When** weather API indicates rain probability > 80% within 2 hours
- **Then** system produces a "Rain Plan Ready" prompt to the planner
- **And** one-tap activation triggers:
  - SMS notification to guests with venue adjustment
  - Notification to decor team to move tables indoors
  - MC script update inserted
  - Photography plan adjusted
- **And** autonomous activation is opt-in per contingency type

### 4.4 Epic: Vendor Marketplace and Bidding

**User Story 4.4.1:** As a vendor, I want to receive booking opportunities relevant to my services and pricing, so that I can bid on work I'm positioned to win.

**Acceptance Criteria:**
- **Given** a vendor registered in my category and price range
- **When** an event planner posts an RFP
- **Then** I receive notification within 10 minutes
- **And** I can submit a bid with pricing and availability in under 5 minutes
- **And** the planner sees my bid alongside 2-4 competitors
- **And** if selected, I get booking confirmation + 50% deposit via M-Pesa immediately

### 4.5 Epic: Post-Event Settlement

**User Story 4.5.1:** As a planner, I want vendor payments to settle automatically after event completion, with clean accounting and no manual reconciliation, so that I don't spend 2 days/month on post-event admin.

**Acceptance Criteria:**
- **Given** an event completed with all vendors' services delivered
- **When** I mark the event complete in Sherehe
- **Then** final payments are triggered for each vendor (minus deposits already paid)
- **And** commission deductions apply automatically
- **And** M-Pesa transfers execute within 1 hour
- **And** a settlement report is generated for my records
- **And** disputed line items are held in escrow pending resolution

---

## 5. Non-Functional Requirements

### 5.1 Performance

| Metric | Target |
|--------|--------|
| Quote generation (P95) | < 5 minutes |
| Page load (P95, on 3G) | < 3 seconds |
| CRDT sync latency when online (P95) | < 5 seconds |
| Offline-to-online reconciliation (P95) | < 30 seconds |
| Contingency auto-activation (P95) | < 60 seconds from trigger |
| Autonomous action log updates | < 2 seconds |

### 5.2 Availability

| Component | Target |
|-----------|--------|
| Planner BFF | 99.9% |
| Sync service | 99.95% (tolerates brief outages; clients work offline) |
| Autonomous orchestration engine | 99.99% (critical during active events) |
| Vendor marketplace | 99.5% |

### 5.3 Offline-First Requirements

**Mandatory capabilities while offline:**
- All event data readable
- New edits possible (saved to IndexedDB)
- Check-ins and vendor arrival logging
- Notes and photos
- Reference vendor contact info
- View contingency plans

**Not required offline:**
- Real-time sync with teammates (queued for when online)
- Vendor marketplace (search/bidding)
- Autonomous orchestration engine triggers (runs server-side when connected)

### 5.4 Security

- **Authentication:** OAuth 2.0 + magic-link; MFA for planner accounts handling >$50K events
- **Authorization:** Role-based (owner, co-planner, assistant, view-only)
- **Encryption:** TLS 1.3 in transit; AES-256 at rest; end-to-end for client contract documents
- **Payment security:** PCI DSS SAQ-A (no card data stored); M-Pesa integration via official Daraja APIs
- **PII handling:** Guest lists encrypted; retention per configurable policy
- **GDPR/POPIA/Kenya DPA:** Right to delete, data portability, consent management

### 5.5 Scalability

- Sync service must support 10,000 concurrent active editing sessions
- Event state can be up to 100MB per event (decor plans, seating charts, photo gallery)
- CRDT state is efficiently encoded (no linear growth with change count)

### 5.6 Accessibility

- WCAG 2.1 AA compliance
- Screen reader support for all planning flows
- Keyboard navigation
- High-contrast mode
- Swahili + English UI translations

### 5.7 Autonomous Orchestration Safety

- All autonomous actions logged with full audit trail
- Each autonomous action has a configurable "human-in-the-loop" threshold
- Kill switch: planner can disable autonomy with one tap on event day
- Autonomous actions use only APIs, never send spontaneous messages to non-registered parties
- Weekly review report: "Here's what the system did autonomously this week; would you make the same decisions?"

---

## 6. Success Metrics

### 6.1 Business Metrics (End of Week 15)

| Metric | Target | Current |
|--------|--------|---------|
| Active planners on platform | 25 | 0 |
| Paying planners (any tier) | 10 | 0 |
| Events managed through platform | 50+ | 0 |
| Monthly Recurring Revenue | $500+ | $0 |
| Transaction fee revenue | $200+ | $0 |

### 6.2 Product Metrics

| Metric | Target |
|--------|--------|
| Quote generation time (avg) | < 20 min (vs 2-3 days baseline) |
| Planner NPS | > 40 |
| Events using autonomous orchestration | 50%+ |
| Offline session completion rate | > 99% |

### 6.3 Technical Metrics

| Metric | Target |
|--------|--------|
| CRDT merge conflict rate | < 0.1% |
| Event day execution error rate | < 2% |
| Sync success rate | > 99.5% |

---

## 7. Architecture Mapping

### 7.1 Primary Pattern Introduced: CRDTs + Offline-First + Local-First Architecture

Sherehe is built on CRDTs (Conflict-free Replicated Data Types) from day one. The event plan itself lives on the client as a CRDT document; the server is a relay and projection builder, not the source of truth. This is the modern local-first architecture pioneered by Figma, Linear, and multiplayer tools.

**Compounding patterns carried forward:**
- **BFF pattern (Tier 1):** Three BFFs — Planner (primary UI), Vendor (marketplace + bidding), Client (view-only shared link)
- **Event-driven (Tier 1):** Every planning decision emits an event; autonomous orchestrator subscribes and acts
- **CQRS (Tier 2):** Command side accepts edits from CRDT sync; query side projects into analytics views, reports, search
- **Sagas (Tier 2):** Multi-step workflows (vendor booking → deposit → confirmation → contract delivery) as sagas

### 7.2 The CRDT Architecture

**Client:**
- Yjs or Automerge library as the document store
- IndexedDB for persistence (survives browser close/crash/offline)
- WebSocket (y-websocket) for real-time sync when online
- WebRTC peer-to-peer fallback for venue WiFi-free scenarios

**Server:**
- Yjs server or custom sync relay in TypeScript/Fastify
- Persistent event log of CRDT operations (source-of-truth archive)
- Projections built by consuming CRDT ops and producing read models in PostgreSQL

**Why local-first:**
- Kenyan venue WiFi is unreliable; must work offline
- Multiple planner team members edit simultaneously; conflict resolution must be automatic
- Guest list + vendor list can be large (1000s of items); server round-trips for every edit would be unusable
- Sync conflicts in traditional systems lead to data loss; CRDTs are mathematically guaranteed to merge cleanly

### 7.3 The Autonomous Orchestration Engine

This is Sherehe's differentiating capability. Implementation:

**Rule Engine:**
- TypeScript rules compiled from a simple DSL (`when caterer.status == "late" && delay > 20min then notify(mc, "extend_program"); adjust(bar, "extend_service")`)
- Rules defined per event (default templates for common event types)
- Rules evaluated server-side when events arrive from any source (GPS, timeline triggers, weather API, manual updates)

**Action Executors:**
- SMS (via Africa's Talking)
- Email
- Push notifications
- Schedule adjustments (CRDT document updates)
- M-Pesa payment triggers (for automatic backup vendor activation)
- Third-party API calls (e.g., weather lookups, traffic lookups)

**Safety Rails:**
- Every autonomous action logged with full context
- Configurable thresholds per action type
- Human-in-the-loop escalation paths
- Dry-run mode for testing new rules
- Kill switch always available to planner

**LLM Assist (not core, augmentation):**
- LLM helps generate contingency plans during planning ("what should happen if it rains?")
- LLM drafts SMS templates in local language
- LLM is NOT in the execution loop; rules-based logic is

### 7.4 The Three BFFs

| BFF | Client | Technology | Key Responsibilities |
|-----|--------|------------|---------------------|
| Planner BFF | Next.js PWA (mobile-first) | TypeScript + Fastify | Event planning, CRDT sync, autonomous action controls |
| Vendor BFF | Next.js PWA | TypeScript + Fastify | Marketplace browsing, bidding, earnings dashboard |
| Client BFF | Shareable link, read-mostly | TypeScript + Fastify | View event, approve quotes, make payments |

### 7.5 Technology Stack

**Frontend:**
- Next.js 15+ PWA
- React + TypeScript (strict mode)
- Tailwind CSS + shadcn/ui
- Yjs (CRDT)
- IndexedDB via Dexie.js
- WebRTC via simple-peer (for venue peer sync)

**Backend:**
- TypeScript + Fastify (BFFs)
- Node.js workers for autonomous orchestration engine
- Start in raw JavaScript for event-loop mastery, migrate to strict TS over the sprint

**Data:**
- PostgreSQL (projections, user accounts)
- Redis (session, pub/sub for cross-service events)
- S3 or Cloudflare R2 (images, contract PDFs)
- Yjs document store (custom persistence layer)

**Integrations:**
- M-Pesa Daraja (payments)
- Africa's Talking (SMS)
- OpenWeatherMap (weather triggers)
- Google Maps (vendor GPS tracking, venue routing)
- Twilio (voice backup)
- OpenAI or Gemini (planning assist)

**Infrastructure:**
- Vercel for frontend hosting
- Fly.io for BFFs (Nairobi region)
- AWS for data and autonomous engine
- Ably or self-hosted for real-time sync

---

## 8. Phased Rollout Plan

### 8.1 MVP (Week 6)

**Scope:**
- Planner BFF with event CRUD
- CRDT-based offline-first editing
- Multi-user real-time sync
- Basic quote generator (vendors list + pricing)
- One autonomous rule: vendor-late-notify-MC (demo scenario)

**Commercial goal:** 5 planners using free tier; collecting feedback

### 8.2 v1.0 (Week 10)

**Scope:**
- Vendor BFF operational
- Client BFF for shared quotes
- 5+ autonomous orchestration rules
- M-Pesa integration for vendor deposits
- Pricing tier launched

**Commercial goal:** 25 active planners; 10 paying; $500 MRR

### 8.3 v1.5 (Week 15)

**Scope:**
- Full marketplace with vendor bidding
- Post-event settlement + auto-payouts
- Contingency packages library
- WebRTC peer sync for venue operations

**Commercial goal:** 50+ events managed; $1,000+ MRR; first enterprise customer (large event planning company)

### 8.4 v2.0 (Post-sprint)

- Multi-country (Uganda, Tanzania, Rwanda)
- Event insurance integration
- Corporate event features (guest RSVP workflows, badge printing, session scheduling)
- AI-powered event design (seating charts, decor suggestions from Pinterest-style mood boards)

---

## 9. Commercial Terms

### 9.1 Pricing Tiers

| Tier | Price | Features | Target |
|------|-------|----------|--------|
| **Sherehe-Free** | $0/mo | 1 event/month, basic features | Trial, 1-off planners |
| **Sherehe-Solo** | $49/mo | Unlimited events, 1 planner, basic autonomous rules | Solo planners |
| **Sherehe-Team** | $149/mo | 5 planners, advanced autonomy, vendor marketplace access | Small firms |
| **Sherehe-Pro** | $499/mo | Unlimited planners, custom rules, white-label client views | Established firms |
| **Transaction fees** | 2-3% on vendor bookings | All tiers | Marketplace revenue |

### 9.2 Customer Acquisition

- **Direct outreach:** Nairobi event planners via Instagram (large community), LinkedIn
- **Vendor seeding:** Sign up 50+ vendors first; offer "your planner can book you faster if they use Sherehe"
- **Content:** Weekly blog/Instagram posts on event planning in Kenya (SEO-driven)
- **Conference demos:** Kenya Wedding Expo, Nairobi Events Summit
- **Partnerships:** Event venues (KICC, Sarova, Crowne Plaza) offer Sherehe-managed events a discount

---

## 10. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|-----------|
| CRDT edge cases cause data loss | Low | High | Extensive testing; conflict resolution UI for the <0.1% edge case; full audit log |
| Autonomous actions cause customer embarrassment (e.g., SMS to wrong person) | Medium | High | Strong safety rails; dry-run mode; opt-in per action; audit log |
| Vendor adoption lags | High | Medium | Seed marketplace manually first; charge no fee to vendors until 100+ onboarded |
| Event planners are not software-savvy | High | Medium | UX-first design; optional concierge onboarding for Team+ tiers |
| M-Pesa transaction fees erode margins | Medium | Medium | Build in margin from Day 1; consider bank transfer fallback for high-value events |

---

## 11. Open Questions

1. Should we support non-M-Pesa payment rails from Day 1 (bank transfers, card)? Probably card via Stripe; bank transfers as manual approval workflow.
2. How do we handle vendor quality disputes? Starting with planner-mediated arbitration; longer-term ratings system + escrow dispute process.
3. Event insurance partnership? Explore in v2.0; not core for MVP.
4. Should Sherehe itself be the "planner of record" for clients who don't have one? Potentially a future tier ("Sherehe Concierge") but out of scope for 15-week sprint.

---

## 12. Appendix: Definition of Done for v1.0

- [ ] All user stories in Section 4 have passing acceptance tests
- [ ] CRDT sync tested with 5+ concurrent users, no data loss
- [ ] Offline-to-online sync works 100% reliably in testing
- [ ] Autonomous orchestration engine with 10+ rule templates deployed
- [ ] M-Pesa payment integration live
- [ ] 10 paying planners onboarded
- [ ] Security audit passed
- [ ] Accessibility audit passed (WCAG 2.1 AA)
- [ ] Documentation: user guide, vendor onboarding guide, API docs
- [ ] On-call rotation active for event-day incidents
