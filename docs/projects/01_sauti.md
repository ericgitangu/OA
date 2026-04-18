# PRD — Sauti by Lee Audio

> **Version:** 1.1
> **Date:** April 2026
> **Status:** Draft — Approved for Sprint Weeks 1-2
> **Owner:** Eric Gitangu (Deveric Technologies)
> **Tier:** 1 (Rust + C++)
> **Project Type:** New Greenfield
> **Modules:** (A) Voice AI Platform — primary commercial product; (B) Lee Audio Embedded — hardware/Arduino-based automotive and smart-environment customizations (hobby + longer-term commercial)

---

## 1. Executive Summary

**Lee Audio** is a two-module consumer and professional brand; **Sauti** is the underlying software platform spanning both.

**Module A — Sauti Voice AI Platform** (primary sprint focus, Weeks 1-2):
Production-grade voice AI infrastructure for African languages — starting with Swahili, Kikuyu, Luo, and Sheng. Provides real-time voice-to-text transcription, translation, sentiment analysis, and voice cloning as APIs and embedded SDKs. Primary customers are BPOs running Kenyan call centers, government service desks, accessibility tool providers, and NGOs operating multilingual field programs. Kenya's BPO industry has grown 25%+ annually and serves 50+ mid-size call centers, most of which rely on English-only transcription tools that fail on Swahili/Sheng. Existing solutions (Google Speech-to-Text, Whisper API) have poor accuracy on African languages and do not support on-premises deployment, which government and financial customers require.

**Module B — Lee Audio Embedded** (hobby-first, commercial-later, begins Week 2 weekends, accelerates post-sprint):
Arduino and ESP32-based hardware customizations starting with automotive (car lighting, audio, sensor packages) and expanding to home and office automation. This module serves three purposes: (1) a deliberate hobby that reinforces the systems-level Rust + C++ work from the Sauti platform; (2) a future standalone product line sold as plug-and-play kits; (3) a long-term bridge into IoT territory where Sauti's voice AI can become the control layer for home/office/vehicle automation.

**The naming architecture allows Lee Audio to sell multiple voice products (transcription, IVR, voice cloning) on the same Sauti platform while separately developing the Embedded product line — both sharing the Lee Audio brand but with distinct go-to-market motions.**

---

## 2. Problem Statement

### 2.1 The Pain

1. **English-centric voice AI.** Existing commercial voice APIs (Google, AWS, Azure, OpenAI Whisper) perform at 60-75% word-error-rate on code-switched Swahili/English calls, compared to 5-10% on English-only calls. BPOs running Kenyan call centers have no viable transcription tool.

2. **No on-premises option for regulated industries.** Banks (under CBK data sovereignty rules), government agencies, and healthcare providers cannot send audio to foreign cloud APIs. They need a solution that runs in-country or on-premises.

3. **Real-time QA is manual.** BPOs currently sample 5-10% of calls for quality review, manually, by supervisors listening to recordings. This creates a 24-48 hour feedback loop for agents and catches perhaps 2% of actual issues.

4. **No African-language voice cloning.** Accessibility tools (text-to-speech in Swahili for visually impaired users) and interactive voice response (IVR) systems sound robotic or use foreign voices that don't reflect the user base.

### 2.2 Quantified Market

- **Primary segment:** 50+ Nairobi BPOs with 100-2,000 agents each; average monthly SaaS spend on QA tools $2,000-15,000
- **Secondary segment:** Kenyan government digital service platforms (Huduma, eCitizen) serving 20M+ users with multilingual needs
- **Tertiary segment:** Pan-African NGOs with field operations (Save the Children, Kenya Red Cross, Amref) requiring multilingual call logging and voice-driven workflows

**Total addressable market (Kenya BPO alone):** ~$15M/year. Pan-African: ~$120M/year.

### 2.3 Why Now

- Transformer-based ASR models (Whisper, wav2vec2) have matured to the point that fine-tuning on African languages is tractable on consumer GPUs
- Kenyan data sovereignty regulations (2019 Data Protection Act, 2022 amendments) are tightening enforcement
- African BPO industry is expanding post-pandemic as remote-first operations normalize
- Open-source weights (Whisper Large v3) enable high-quality self-hosted deployments for the first time

---

## 3. Target Users & Personas

### 3.1 Primary Persona: Call Center Supervisor

**Name:** Grace, 34, Nairobi
**Role:** QA Supervisor at a 400-agent BPO handling customer service for East African telcos
**Goals:**
- Monitor call quality across 400 agents in real-time, not via 10% manual sampling
- Identify agents needing coaching before customers escalate
- Generate compliance reports for telco clients weekly

**Pain points:**
- Existing QA tools transcribe English calls but fail on Swahili/Sheng (60%+ of their call volume)
- She currently reviews recordings manually after calls end; feedback to agents comes 2-3 days late
- Her team of 8 QA analysts can sample at most 12% of calls

**Jobs-to-be-done:** Turn 24-hour-late manual QA into 30-minute-late automated flagging, with human review only on flagged calls.

### 3.2 Secondary Persona: Call Center Agent

**Name:** David, 27, Nairobi
**Role:** Customer service agent, 80+ calls/day
**Goals:**
- Receive coaching on his performance without waiting days
- Not have every call reviewed (privacy/autonomy concerns)
- Handle calls in the language the customer prefers (often Swahili, Sheng, Kikuyu)

**Pain points:**
- Feedback he gets is 3-5 days old; he doesn't remember the call clearly
- English-only QA tools mean his Swahili calls get undercounted for coaching

**Jobs-to-be-done:** Fast, fair coaching based on accurate transcription of his actual language.

### 3.3 Tertiary Persona: Partner Integration Engineer

**Name:** Mike, 31, technical lead at a Kenyan BPO
**Role:** Integrates Sauti with their existing CRM and dialer systems
**Goals:**
- Low-friction API integration with Salesforce, Zendesk, or their custom dialer
- Stable webhook delivery with idempotency guarantees
- Clear documentation; SDK for Python and Node.js

**Jobs-to-be-done:** Get Sauti plugged into the call center's existing stack in under 2 weeks, not 2 months.

### 3.4 Non-Target Users (Explicit)

- **Consumer voice apps** (e.g., meeting transcription for individuals) — different buyer, different pricing, different privacy model. Not in initial scope.
- **General-purpose TTS for English** — existing vendors (ElevenLabs, PlayHT) dominate; we do not compete there.

---

## 4. User Stories & Acceptance Criteria

### 4.1 Epic: Live Transcription for Call Center Agents

**User Story 4.1.1:** As a call center agent, I want the supervisor dashboard to show an accurate live transcript of my call in Swahili/English so that QA feedback reflects what I actually said.

**Acceptance Criteria:**
- **Given** an active voice call with mixed Swahili/English content
- **When** audio streams into Sauti's agent BFF
- **Then** transcription appears on the supervisor dashboard within 2 seconds of speech (P95 latency)
- **And** word error rate on Swahili/English code-switched audio is under 20% (measured against human-labeled ground truth)
- **And** speaker diarization correctly separates agent from customer (90%+ accuracy)
- **And** the transcript is stored in the audit event store for later review

**User Story 4.1.2:** As a call center agent, I want my call's sentiment scored in real-time so that I can adjust my tone if a customer is becoming frustrated.

**Acceptance Criteria:**
- **Given** an active call being transcribed
- **When** Sauti's sentiment model processes the audio stream
- **Then** a sentiment score (0-1, negative-to-positive) is emitted every 10 seconds
- **And** scores are visible on the agent's personal dashboard within 2 seconds
- **And** if sentiment drops below 0.3 for 30+ seconds, an alert is surfaced to the agent (not the supervisor — to preserve agent autonomy)

### 4.2 Epic: Compliance and Audit for Regulated Customers

**User Story 4.2.1:** As a compliance officer at a bank-adjacent BPO, I need every call's transcript, sentiment history, and compliance flags stored in an immutable audit log for 7 years per CBK regulations.

**Acceptance Criteria:**
- **Given** a completed call processed by Sauti
- **When** the call ends
- **Then** a complete event record is written to the event store with cryptographic hash of the audio, transcript, timestamps, and speaker metadata
- **And** the event is immutable (no delete, no update; only append)
- **And** the compliance BFF can retrieve the full history for any call by call-id in under 5 seconds
- **And** retention policies are enforced automatically (auto-delete at 7-year mark if configured)

### 4.3 Epic: Partner API Integration

**User Story 4.3.1:** As a partner integration engineer, I want to integrate Sauti with our existing Salesforce CRM so that transcripts and sentiment scores automatically flow to customer records.

**Acceptance Criteria:**
- **Given** a Sauti account with a valid API key
- **When** I configure a webhook URL pointing to our Salesforce endpoint
- **Then** every completed call triggers a webhook delivery within 30 seconds of call end
- **And** webhook payloads include call-id, full transcript, sentiment history, speaker metadata
- **And** webhook deliveries are signed with HMAC-SHA256 for signature validation
- **And** failed webhook deliveries retry with exponential backoff up to 24 hours
- **And** an idempotency key is included so our system can deduplicate

### 4.4 Epic: Hate Speech Detection and Flagging

> **Context:** Kenya's National Cohesion and Integration Act (2008) criminalizes hate speech, but enforcement is hampered by the lack of qualified transcribers who can determine hate speech across Kenya's multilingual landscape. Daniel Mutegi has called for amending the Act to include transcribers who are qualified to determine hate speech. Sauti is uniquely positioned to be that technological backbone — providing AI-assisted first-pass detection with human-in-the-loop determination by qualified transcribers.

**User Story 4.4.1:** As a compliance analyst at a government monitoring desk, I want Sauti to flag potential hate speech segments in real-time across Swahili, Sheng, Kikuyu, Luo, and English broadcasts so that qualified transcribers can review flagged segments and make formal determinations.

**Acceptance Criteria:**
- **Given** an active audio stream being transcribed by Sauti
- **When** the NLP classification layer detects language matching hate speech indicators (ethnic targeting, incitement to violence, dehumanizing language, discriminatory slurs)
- **Then** a `HateSpeechFlaggedEvent` is emitted within 5 seconds containing: transcript segment, confidence score (0-1), hate speech category (ethnic, religious, gender, political), timestamp, speaker ID, and source metadata
- **And** the flagged segment is routed to a qualified transcriber review queue
- **And** the AI acts as a first-pass filter only — humans make the determination
- **And** false positive rate is below 15% on the evaluation dataset

**User Story 4.4.2:** As a qualified transcriber reviewing flagged content, I want a review dashboard showing the flagged transcript segment with surrounding context (30 seconds before and after), audio playback, speaker identification, and the AI's confidence score so that I can make an informed determination.

**Acceptance Criteria:**
- **Given** a `HateSpeechFlaggedEvent` in the review queue
- **When** the qualified transcriber opens the review dashboard
- **Then** they see: the flagged segment highlighted in full transcript context, the AI's classification (category + confidence), a 60-second audio clip centered on the flagged segment with playback controls, speaker diarization labels, and the original language with English translation
- **And** the transcriber can mark the segment as: Confirmed Hate Speech, Borderline (escalate to senior reviewer), Dismissed (false positive), or Requires Legal Review
- **And** every determination is immutably logged in the event store with the transcriber's ID, timestamp, and rationale

**User Story 4.4.3:** As a regulatory compliance officer, I want an audit trail of all hate speech flags, determinations, and escalations so that enforcement actions have evidentiary backing that is legally admissible.

**Acceptance Criteria:**
- **Given** accumulated hate speech flags and determinations over a reporting period
- **When** a compliance officer generates a report
- **Then** the report includes: total flags, confirmation rate, category breakdown, response time from flag to determination, transcriber ID and qualifications for each determination
- **And** the report includes cryptographic proof of integrity (hash chain) for evidentiary admissibility
- **And** audio recordings referenced in the report are preserved with chain-of-custody metadata regardless of normal retention policies
- **And** the report format aligns with National Cohesion and Integration Commission (NCIC) submission requirements

---

## 5. Non-Functional Requirements

### 5.1 Performance

| Metric | Target | Measurement |
|--------|--------|-------------|
| Transcription latency (P50) | < 800ms | Time from audio chunk ingestion to transcript fragment emission |
| Transcription latency (P95) | < 2s | Same as above |
| Sentiment scoring latency (P95) | < 1s | Time from 10s audio window close to score emission |
| Webhook delivery latency (P95) | < 30s | Time from call end to first webhook attempt |
| System throughput | 10,000 concurrent calls | Sustained, across all tenants |
| Per-call audio ingestion rate | 16kHz mono PCM | 256 kbps streaming |
| Hate speech detection latency (P95) | < 5s | Time from utterance to HateSpeechFlaggedEvent emission |
| Hate speech false positive rate | < 15% | Measured against human-labeled evaluation set |

### 5.2 Availability

| Component | Target | Approach |
|-----------|--------|----------|
| Core API (agent BFF) | 99.95% | Multi-AZ deployment on AWS, health-check-driven failover |
| Transcription workers | 99.9% | Worker pools with automatic scaling, failed-job retry |
| Event store | 99.99% | EventStoreDB cluster with 3-node replication |
| Partner webhook delivery | 99.5% at first attempt | Graceful retry covers the gap |

### 5.3 Security

- **Authentication:** OAuth 2.0 for partner API; JWT for agent/supervisor dashboards
- **Authorization:** Tenant isolation at every layer; no cross-tenant data access possible
- **Encryption:** TLS 1.3 in transit; AES-256-GCM at rest for audio and transcripts
- **Audit logging:** Every API call logged with user-id, tenant-id, timestamp, operation
- **PII handling:** Audio is treated as PII; access logs retain for 2 years; audio itself retained per tenant policy
- **Compliance:** Kenya Data Protection Act 2019; GDPR-equivalent controls for EU-based partners
- **Secrets:** AWS Secrets Manager; no secrets in code or environment variables

### 5.4 Scalability

- Horizontal scaling of transcription workers based on queue depth
- Stateless BFFs — any BFF instance can serve any client request
- Event store partitioned by tenant-id for write scalability
- Read projections horizontally sharded by tenant-id

### 5.5 Observability

- **Tracing:** OpenTelemetry across all services; every request has a trace-id
- **Metrics:** Prometheus-compatible; dashboards in Grafana
- **Logging:** Structured JSON logs; shipped to CloudWatch and archived to S3
- **Alerting:** PagerDuty for P0/P1; Slack for P2/P3
- **SLIs:** Transcription accuracy, latency, throughput, error rate per tenant

### 5.6 Deployability

- **Environments:** dev, staging, production on AWS (us-east-1 primary, af-south-1 for Kenya data residency)
- **CI/CD:** GitHub Actions; every PR runs unit + integration tests; main branch auto-deploys to staging
- **Blue/green deployments** for BFFs; canary deployments for model updates
- **Rollback:** < 5 minutes from detection to rollback execution
- **On-premises option:** Packaged as Docker Compose + Kubernetes Helm chart for regulated customers (added in v1.1)

---

## 6. Success Metrics

### 6.1 Business Metrics (End of Week 15)

| Metric | Target | Current |
|--------|--------|---------|
| Paying customers (Sauti-Pro tier) | 3 | 0 |
| Monthly Recurring Revenue | $500 | $0 |
| Pilot conversations in progress | 10 | 0 |
| Customer retention (pilots who paid) | 70%+ | N/A |

### 6.2 Technical Metrics (End of Sprint)

| Metric | Target |
|--------|--------|
| Swahili WER on code-switched audio | < 20% |
| End-to-end transcription latency (P95) | < 2s |
| System uptime | > 99.5% |
| Calls processed during sprint | 10,000+ (across all pilots + synthetic load tests) |

### 6.3 Product Metrics (by Week 8)

| Metric | Target |
|--------|--------|
| Agent BFF endpoints shipped | 5+ |
| Supervisor BFF endpoints shipped | 8+ |
| Partner API endpoints shipped | 3+ |
| Webhook delivery reliability | > 99.5% |

---

## 7. Architecture Mapping

### 7.1 Primary Pattern Introduced: BFF + Event-Driven Architecture

This project teaches BFF and event-driven architecture as foundational patterns that every subsequent tier will inherit. Specifically:

**BFF Pattern Applied:**
- Three separate BFFs, each optimized for its client's needs:
  - **Agent BFF:** Low-latency SSE streaming of transcript fragments and live sentiment to the agent's browser
  - **Supervisor BFF:** Aggregated real-time dashboards (all agents' status) with WebSocket push for team metrics
  - **Partner API BFF:** REST endpoints with stable API contracts + webhook delivery for external CRM/dialer systems
- Each BFF shapes data differently for its consumer. No endpoint serves multiple clients.

**Event-Driven Applied:**
- Audio chunks flow as events from ingestion → DSP pipeline → ASR → sentiment → storage
- Every transformation emits events; downstream consumers subscribe
- Back-pressure handled via Redis Streams consumer group offsets
- Event store provides replayable history for audit, compliance, and debugging

### 7.2 Tier-Specific Capabilities Leveraged

**Rust (Axum, tokio, tonic):**
- Axum-powered BFFs for each client — low overhead, high concurrency via tokio
- Tonic for gRPC between internal services (strong typing, efficient wire format)
- PyO3 bindings where calling Python ML models directly is simpler than RPC

**C++ (modern C++20/23):**
- DSP pipeline for FFT, MFCC feature extraction, VAD
- SIMD intrinsics for performance-critical signal processing
- Exposed to Rust via `cxx` crate with zero-copy buffer sharing

**Rationale for the Rust+C++ pairing:**
- Voice processing is genuinely systems-level; needs allocation control and memory layout awareness
- Rust provides safety and concurrency ergonomics for the business logic layer
- C++ provides battle-tested DSP libraries and SIMD access for the hot path
- The FFI boundary between them is the single most valuable teaching vehicle for understanding zero-cost abstractions, ownership, and memory layout

### 7.3 Bounded Contexts

| Context | Responsibility | Language |
|---------|---------------|----------|
| Ingestion | Accept audio streams, enqueue for processing | Rust |
| DSP | Feature extraction, VAD, audio segmentation | C++ |
| Transcription | ASR inference (Whisper + fine-tuned adapters) | Rust (calls Python models via PyO3) |
| Sentiment | Sentiment classification on transcribed text | Rust (calls Python models) |
| Content Moderation | Hate speech detection, flagging, transcriber review queue, determination tracking | Rust (PyO3 to Python) |
| Session | Call lifecycle, speaker diarization state | Rust |
| Compliance | Event store writes, audit retrieval | Rust |
| Webhook Delivery | External integration push | Rust |

Each context has its own aggregate root; cross-context communication happens only via events on the event bus.

### 7.4 Technology Stack

**Backend:**
- Rust 1.80+ (Axum, tokio, tower)
- C++ 20 (DSP, SIMD)
- Python 3.12 (ML model serving, called from Rust via PyO3)
- ONNX Runtime + Whisper Large v3 (fine-tuned on Swahili)

**Data:**
- Redis Streams (event bus)
- EventStoreDB (compliance/audit event store)
- PostgreSQL (projections, tenant config)
- S3 (audio archival, per-tenant retention policies)

**Infrastructure:**
- AWS (primary region us-east-1; secondary af-south-1 for Kenya customers)
- Kubernetes (EKS) for orchestration
- Linkerd (service mesh — will be deepened in Tier 4)
- OpenTelemetry (tracing)

**Frontend (minimal in this tier; deepened in Tier 3):**
- Next.js + TypeScript for admin/supervisor dashboards
- Tailwind + shadcn/ui

---

## 8. Phased Rollout Plan

### 8.1 MVP (Week 2, end of Tier 1 sprint)

**Scope:**
- Agent BFF: audio ingestion + SSE transcript streaming
- DSP pipeline: working FFT/MFCC/VAD in C++ called from Rust
- Transcription: Whisper baseline (no Swahili fine-tuning yet — just prove the pipeline)
- Event bus: Redis Streams operational
- Deployment: AWS us-east-1, single availability zone

**Commercial goal:** 1 pilot customer actively testing with real call audio. Feedback loop open.

### 8.2 v1.0 (Week 8, end of Tier 4 sprint — after Unicorns v2 work propagates service mesh patterns back)

**Scope:**
- Swahili fine-tuning shipped; WER improvements validated
- Supervisor BFF with real-time team dashboards
- Partner API BFF with webhook delivery
- Multi-AZ deployment; production SLAs met
- 3 paying customers ($99-499/mo tiers)

**Commercial goal:** $500 MRR; 3 paying customers in the Kenyan BPO market.

### 8.3 v1.5 (Week 12)

**Scope:**
- On-premises deployment option (Docker Compose + Helm chart)
- Additional languages: Luo, Kikuyu, Sheng support
- Voice cloning prototype (Kikuyu + Swahili) for IVR customers
- 5+ paying customers

**Commercial goal:** $1,500 MRR; expansion into government/banking pilots.

### 8.4 v2.0 (Week 15+, post-sprint)

**Scope:**
- Voice cloning commercialized
- French/Portuguese (Senegal, Côte d'Ivoire, Mozambique) added
- Self-service onboarding for BPO tier
- Enterprise tier with custom model training for top 5 customers

---

## 9. Commercial Terms

### 9.1 Pricing Tiers

| Tier | Price | Features | Target |
|------|-------|----------|--------|
| **Sauti-Free** | $0/mo | 1,000 minutes/mo, English + Swahili, 1 agent | Pilots, dev trials |
| **Sauti-Pro** | $99/mo | 10,000 minutes, all languages, 10 agents, basic analytics | Small BPOs, NGOs |
| **Sauti-Business** | $499/mo | 100,000 minutes, unlimited agents, advanced QA, API access | Mid BPOs |
| **Sauti-Enterprise** | Custom (from $2,500/mo) | Unlimited usage, on-premises option, custom model training, SLA | Government, banking, large BPOs |
| **Partner API** | $0.02/minute | Pay-as-you-go API access | System integrators, developers |

### 9.2 Customer Acquisition Strategy

- **Week 1-2:** Personal outreach to 10 Nairobi BPO contacts (leveraging existing network and Ignite/ENGIE engineering connections)
- **Week 3-4:** Free 30-day pilot for 3 BPOs; collect testimonials and accuracy benchmarks
- **Week 5-8:** Content marketing on LinkedIn (technical posts about Swahili ASR, African language AI); outreach to iHub, Nairobi Garage tenants
- **Week 9-12:** Apply to AWS FinTech Africa Accelerator; pitch at Nairobi tech meetups
- **Week 13+:** Referrals from existing customers; consulting/integration services as upsell

### 9.3 Go-to-Market Channels

1. **Direct sales** to Nairobi BPO network (primary)
2. **Developer API** (self-service via Lee Audio website) — for integrators and smaller shops
3. **Partnerships** with CRM resellers (Salesforce implementers, Zendesk partners in East Africa)
4. **Content-led** — technical blog posts, GitHub-visible open-source tools (e.g., open-source Swahili audio dataset cleanup utility)

---

## 10. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|-----------|
| Whisper fine-tuning produces insufficient accuracy | Medium | High | Multi-model fallback (combine Whisper + wav2vec2); degrade gracefully; manual correction UI as Tier 2 backup |
| AWS African region latency degrades real-time UX | Low | Medium | Deploy edge proxy in Fly.io Nairobi for ingestion; move full inference to af-south-1 in v1.1 |
| BPO customers slow to pay (African B2B sales cycles can be 6-9 months) | High | Medium | Target smaller, faster-moving shops first; consulting/implementation revenue bridges the gap |
| Google/AWS launch Swahili support and undercut | Medium | High | Moat = on-premises option, custom vocabulary, local support, deeper African language roadmap (not just Swahili) |
| Model hosting costs exceed revenue | Medium | High | Aggressive model quantization; optimized Rust inference; pricing model includes minute caps to protect margins |
| Hate speech classifier bias toward specific ethnic groups | Medium | High | Multi-ethnic training data; regular bias audits; community advisory board; human determination requirement prevents AI-only enforcement |
| Legal liability for hate speech detection false negatives | Medium | High | Clear terms of service: Sauti is a tool assisting qualified transcribers, not a replacement; insurance review; legal counsel on liability framework |

---

## 11. Open Questions

1. Should voice cloning be a separate product (Lee Voice?) or a Sauti feature? Lean toward feature for now; spin out if it grows independently.
2. How do we handle agent consent for voice cloning from their own calls? (Ethical/legal question — needs privacy policy work before v1.5)
3. Do we self-host Whisper or use OpenAI's hosted API during the MVP? Lean toward self-hosted for cost + control, even though slower to start.
4. Should the compliance event store use EventStoreDB or Kafka with a specialized topic? EventStoreDB is purpose-built but less familiar. Decision to be made in Week 1.
5. What training data sources can be used for the hate speech classifier? Possible sources: NCIC case records, social media monitoring datasets, Kenya Human Rights Commission archives. All require consent and ethical review.
6. How should Sauti handle code-switching within hate speech — e.g., a speaker using Kikuyu slurs in an otherwise Swahili conversation? The classifier must be multilingual-aware, not language-siloed.
7. What legal liability does Sauti face for false negatives (hate speech not detected) vs. false positives (non-hate-speech incorrectly flagged)? Legal counsel needed before v1.0 of this feature.

---

## 12. Appendix: Definition of Done for v1.0

A v1.0 release is shippable when:

- [ ] All user stories in Section 4 have passing acceptance tests
- [ ] WER on Swahili/English code-switched evaluation set < 20%
- [ ] P95 transcription latency < 2s measured over 1,000 real call minutes
- [ ] 3 paying customers signed; first invoices collected
- [ ] Security audit passed (external review or internal checklist per claude_code_strategy.md)
- [ ] Documentation complete: API reference, integration guide, admin guide
- [ ] Deployment reproducible from scratch in under 2 hours via Terraform + Helm
- [ ] On-call rotation defined (even if just Eric rotating with himself for now)
- [ ] Monitoring + alerting operational; PagerDuty integrated
- [ ] Legal: Terms of Service, Privacy Policy, Data Processing Agreement drafted
- [ ] Hate speech classification model trained and evaluated on multilingual Kenyan dataset
- [ ] Qualified transcriber review dashboard operational with full audit trail
- [ ] False positive rate below 15% on evaluation set
- [ ] NCIC-aligned reporting format validated with compliance stakeholders

---

## 13. Module B — Lee Audio Embedded (Arduino/ESP32 Hardware Extensions)

### 13.1 Scope and Philosophy

Lee Audio Embedded is deliberately treated as a **hobby-first, product-later** module. The rationale is threefold:

1. **Hobbies beat burnout.** The 15-week sprint is intensive; a Saturday evening soldering session is cognitive rest that still reinforces the Tier 1 Rust + C++ systems work.
2. **The embedded world teaches what the cloud obscures.** Memory-mapped I/O, timing-sensitive code, no GC, no threads, no OS — this is the deepest form of the "third eye" training. Building it alongside Sauti's cloud platform creates a hardware/software duality that few engineers master.
3. **Commercial surface area is real.** Kenya's car customization market (Nairobi's Mombasa Road, Industrial Area) serves thousands of enthusiasts spending $500-$5,000 per car on aesthetic and performance modifications. Most current LED/lighting kits are cheap Chinese imports with poor quality control. A locally-designed, programmable, quality-controlled alternative has a real market.

### 13.2 Three Subsystems

**Subsystem B1 — Automotive Customization (sprint-era focus)**

Programmable lighting, audio control, and sensor integration for enthusiast-modified vehicles. Product archetypes:

| Product | Description | Primary Hardware | Estimated Kit Price |
|---------|-------------|------------------|--------------------|
| **LeeGlow Cabin** | RGB interior lighting with music-reactive mode, phone BLE control, custom presets | ESP32-S3 + WS2812B LED strips | KES 8,000 ($60) |
| **LeeGlow Underglow** | Exterior RGB underglow with synchronized sequences, weather-sealed | ESP32-S3 + WS2815 (12V) | KES 15,000 ($110) |
| **LeeDash** | Programmable digital dash overlay (speed, RPM, boost, custom gauges from OBD-II) | ESP32 + SSD1322 OLED + OBD-II Bluetooth | KES 18,000 ($135) |
| **LeeSub** | Subwoofer controller with real-time EQ, cabin-tuned presets, phone app | ESP32 + class-D amp control interface | KES 12,000 ($90) |
| **LeeTag** | Smart keyless entry with BLE proximity, phone-as-key | ESP32 + relay + accelerometer | KES 10,000 ($75) |
| **LeeWatch** | Multi-sensor security package (intrusion, tilt, GPS, SMS alerts) | ESP32 + SIM800L + MPU-6050 | KES 20,000 ($150) |

**Subsystem B2 — Home Automation (post-sprint, Year 2)**

Standalone and Sauti-integrated home systems:

- Voice-controlled lighting, HVAC, security — commands issued in Swahili/Kikuyu via Sauti (the commercial moat: local language smart home, not Alexa's bad Swahili)
- Smart metering (water, electricity) with M-Pesa auto-topup integration
- Solar + battery management dashboards (PayGoHub customer upsell)
- Farm automation (drip irrigation control, soil sensors) — connects directly to Shamba/Greenland module

**Subsystem B3 — Office Automation (post-sprint, Year 2-3)**

- Conference room systems (occupancy sensors, booking displays, A/V control)
- Access control with BLE badges
- Voice-activated meeting room controls via Sauti
- Environmental monitoring (CO2, temperature, humidity) with analytics dashboards

### 13.3 Recommended Hardware Platforms

| Platform | Use Case | Why |
|----------|----------|-----|
| **ESP32-S3** (primary) | Most car products, all wireless features | Dual-core Xtensa, built-in WiFi + BLE, ~$4 chip cost, Arduino-compatible, large community |
| **ESP32-C6** (new builds) | Future products needing Wi-Fi 6 / Thread / Matter | Latest RISC-V ESP with Matter support — smart home ready |
| **Arduino Nano ESP32** | Quick prototyping, hobbyist-friendly packages | Official Arduino form factor with ESP32-S3 inside |
| **Raspberry Pi Pico 2 (RP2350)** | High-speed real-time work (audio DSP, FFT, gauge rendering) | Dual-core ARM + RISC-V, PIO state machines, $5, stable supply |
| **Teensy 4.1** | Premium audio products (LeeSub), high-performance | 600 MHz ARM M7, excellent audio library, sub-microsecond timing |
| **STM32 "Blue Pill"** (F103C8) | Ultra-low-cost sensor nodes | $2 each, ARM Cortex-M3, Arduino-compatible via STM32Duino |

**Sprint-era hardware shortlist (buy one of each to start):** ESP32-S3 DevKitC-1, Arduino Nano ESP32, RP2040 Pico (Pi Pico), Teensy 4.1, plus peripherals — WS2812B LED strip (5m), MPU-6050, OBD-II BLE adapter, SIM800L GSM module, SSD1322 OLED.

### 13.4 Development Tooling

**Primary IDE stack:**
- **PlatformIO** (via VS Code) — the professional choice. Unified toolchain across all MCU families, proper dependency management, CI-friendly, works with Arduino libraries while bypassing the Arduino IDE's limitations.
- **ESP-IDF** (Espressif's native SDK) — for ESP32 products needing deep control (low-power modes, security features, custom partitions). Move here as products mature.
- **Arduino IDE 2.x** — only for very quick throwaway tests; don't commit to it long-term.

**Programming languages (aligns with sprint polyglot theme):**
- **C++ (Arduino core / ESP-IDF)** — primary for all MCU work. Reinforces the Tier 1 C++ skills.
- **Rust (via `esp-rs` and `embassy`)** — secondary target for specific products once proficient. Embassy is an async executor for bare-metal Rust; production-quality. Reinforces Tier 1 Rust skills further.
- **MicroPython** — only for prototyping UX flows; never ship in production (performance + determinism).

**Additional tooling:**
- **Saleae Logic Analyzer (or cheap clone)** — non-negotiable for debugging I2C/SPI/UART. ~$12 for the clone.
- **Benchtop multimeter** and **oscilloscope** (cheap Rigol DS1054Z, $400) — the DSO becomes essential once debugging RF/audio.
- **KiCad 8** — PCB design for the transition from breadboard prototypes to manufacturable boards. Free, open-source, professional-grade.
- **JLCPCB / PCBWay** — cheap PCB fabrication; 5 boards for ~$10 delivered to Nairobi in ~2 weeks.
- **3D printer** (if household already has one, or Buruburu/Kilimani makerspaces) — enclosure prototyping.

**Firmware architecture pattern to adopt from Day 1:**
- Deterministic event loop — no `delay()` calls; use millis-based state machines or FreeRTOS tasks
- Separation of concerns: sensor drivers → state machine → output drivers (yes, hexagonal architecture at the MCU level; the third-eye training applies down to 240 MHz dual-core)
- OTA (over-the-air) updates from Day 1 via ESP32's built-in support — so you never need to physically connect to deployed units
- Telemetry to a Sauti-adjacent cloud endpoint (MQTT over TLS) — lays the infrastructure for future cloud-connected products

### 13.5 Sprint-Era Commitment (What Happens in Weeks 1-15)

To keep this true to "hobby-first," the sprint commitment is **light and explicit**:

| Week | Commitment | Total Time |
|------|------------|-----------|
| Week 1-2 (Tier 1) | Order the starter hardware kit; read through ESP32-S3 datasheet as "Sunday reading" | 2 hours |
| Week 3-4 | One weekend evening: blink LED, drive WS2812B, confirm toolchain works | 3 hours |
| Week 5-8 | LeeGlow Cabin MVP firmware (phone BLE control, 5 preset modes) | 10-15 hours total |
| Week 9-12 | LeeDash prototype (OBD-II read, OLED display, 2 gauges) | 15-20 hours total |
| Week 13-15 | Polish one product to "sellable to a friend" state | 10-15 hours total |

**Total sprint-era commitment:** ~40-55 hours spread across 15 weeks. This is the Saturday-evening-plus-one-Sunday-morning rhythm. It does NOT compete with Sauti platform work during the 4 AM deep work blocks. It replaces what would otherwise be idle scrolling time.

### 13.6 Commercial Pathway (Post-Sprint)

**Months 4-6 (Year 1):**
- One product (likely LeeGlow Cabin) finalized with proper PCB, enclosure, packaging
- Sell to 10-20 beta customers through Nairobi car enthusiast community (Facebook groups: "Kenya Car Enthusiasts," Mombasa Road workshops)
- Price aggressively for feedback; target is learning the market, not profit

**Months 7-12 (Year 1):**
- Product catalog of 3-5 items
- Small-batch manufacturing (PCBA via JLCPCB; assembly in-house or via Nairobi contract assembler)
- E-commerce site (leeaudio.co.ke) running on Unicorns v2 platform (dogfood!)
- Target: 100 units/month across product line

**Year 2:**
- Extend into home automation (Subsystem B2) with Sauti voice control integration
- First B2B deal (fleet of cars for a company; 20-50 units at once)
- Possible Kickstarter/pre-order campaign for a flagship product

**Year 3+:**
- Office automation vertical (Subsystem B3)
- Licensing firmware to other hardware brands
- Possible acquisition interest from automotive accessory chains or electronics distributors

### 13.7 Synergy with Other Sprint Projects

This module is not a silo. It deliberately reinforces the rest:

- **Sauti Voice AI** — Lee Audio Embedded products become hardware targets for Sauti voice control (local-language smart home is the long-term play)
- **PayGoHub** — Automotive anti-theft/tracking products share GPS/cellular technology with PAYG device fleet management; lessons transfer both ways
- **Unicorns v2** — Lee Audio sells through a Unicorns tenant, dogfooding the platform; real orders validate Unicorns' multi-tenant SaaS
- **Shamba/Greenland** — Farm automation sensors (soil moisture, water flow, solar pump control) share architectural patterns with Lee Audio Embedded. Greenland's irrigation controllers are functionally a Lee Audio Embedded product tuned for agriculture.

### 13.8 Risks Specific to Module B

| Risk | Mitigation |
|------|------------|
| Hobby expands to consume sprint deep-work time | Strict weekly budget (Section 13.5); use calendar blocks; if overruns, pause Module B until catch-up |
| Hardware supply disruptions in Kenya | Source dual (Aliexpress direct + local suppliers like Jumia / Africa's Electronics); keep buffer stock of critical MCUs |
| Automotive regulatory issues (some LED underglow is illegal on public roads) | Clear labeling; "off-road/show use only" where applicable; KRA import compliance |
| Product liability (automotive products) | Limit early products to non-safety-critical (lighting, aesthetics); defer brakes/engine-management type products indefinitely |
| Competing with Chinese imports on price | Compete on quality, local warranty, customization, brand — not on price |

### 13.9 Definition of Done for Module B v0.1 (by end of sprint)

- [ ] Hardware toolkit acquired and operational
- [ ] PlatformIO + ESP-IDF development environment configured and documented
- [ ] LeeGlow Cabin MVP firmware written, demonstrable on a breadboard prototype
- [ ] One "show and tell" video posted to LinkedIn / YouTube (doubles as marketing and self-accountability)
- [ ] PCB design for LeeGlow Cabin drafted in KiCad (even if not yet manufactured)
- [ ] Bill of Materials (BOM) calculated for LeeGlow Cabin unit cost (target: < KES 2,500 parts)
- [ ] Decision made on first post-sprint product to commercialize

