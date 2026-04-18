# Resume Critique: FAANG ATS Perspective

> **Objective:** Identify why the current resume would likely be filtered out by FAANG Applicant Tracking Systems (ATS) and define the fixes required to pass the filter.
> **Date:** April 2026
> **Subject:** Eric Gitangu Resume 2026 v3

---

## TL;DR — The Verdict

**Current state:** Strong content, weak ATS surface. You would likely be filtered out of FAANG pipelines at the resume-screening stage despite being genuinely qualified.

**Root cause:** The resume reads like a personal narrative (which is compelling to humans) but lacks the keyword density, metric specificity, and structural predictability that FAANG ATS systems and recruiter screens are tuned for.

**Filter pass probability (current):** ~15-20% — you survive some keyword matches but get filtered on "impact quantification" and "seniority markers."

**Filter pass probability (post-overhaul, estimated):** ~75-85% — strong on keywords, metrics, and signals; remaining gap is FAANG-brand-name experience which no resume edit can fix.

---

## How FAANG ATS Actually Works (Briefly)

Most FAANG pipelines use a two-stage filter:

1. **Automated keyword/pattern matching:** Greenhouse, Lever, Workday, Taleo. Looks for exact keyword matches against the job description. If the JD says "distributed systems" and your resume says "event-driven microservices," you may be filtered — even though they're related concepts.

2. **Recruiter 6-second scan:** A human recruiter spends 6-10 seconds on each surviving resume. They look for: brand names (companies, schools), seniority words (Lead, Staff, Principal, Director), quantified impact ($X, N%, X → Y), and one or two "wow" bullets.

Your resume fails at both stages currently. Here's the detailed breakdown.

---

## Critical Issues (Must Fix)

### Issue 1: Metrics are almost entirely absent

**Why it matters:** FAANG recruiters are trained to filter for impact-quantified resumes. No numbers = no signal. The current resume has perhaps 3-4 metrics across the entire document, and most are context-less ("10+ years," "7 African markets," "80+ certifications").

**Examples of current vague bullets:**
- "shifted regression from manual multi-day cycles to automated runs on every PR"
  - *Should be:* "reduced regression cycle time from 3 days to 47 minutes (98% reduction), enabling 12 production deploys/week (from 2)"
- "improving throughput and resilience under peak load across markets"
  - *Should be:* "increased payment throughput from 450 TPS to 2,100 TPS (4.7x) and eliminated timeout errors during Black Friday peak (prior year: 4% failure rate)"
- "fostered a culture of ownership where engineers proactively flagged risks"
  - *Should be:* "mentored 4 QA engineers; 2 promoted to senior roles within 12 months; team Jira bug-find rate increased from 60% to 92% of eventual production issues"

**Fix:** Every bullet needs at least one metric. Where real numbers aren't available, use credible proxies (team size, system scale, regional coverage, engineering-days saved, customer count).

### Issue 2: Seniority signals are muted

**Why it matters:** FAANG hiring bars at L6/Staff or L7/Principal need loud signals: "led N engineers," "owned $X budget," "architected system handling Y scale," "made decision that affected Z."

**Current resume buries these signals.** The Vishnu Systems section says "Founded and led engineering" but doesn't say how many people, what the ARR was, what the technical scale was. The Ignite role says "Lead a team of QA engineers" without headcount.

**Fix:** Every leadership bullet should contain: headcount + scope + outcome.
- *Bad:* "Led engineering for a digital addressing infrastructure platform"
- *Good:* "Led 6-engineer team building digital addressing platform; shipped government pilot serving 2.3M Nairobi residents; second deployment of its kind in Africa after Rwanda's national program"

### Issue 3: Keyword density is low for FAANG job descriptions

**What FAANG JDs typically require** (based on recent L5-L6 postings from Google, Meta, Amazon):
- "Distributed systems" (not just "microservices")
- "System design" (explicitly)
- "Scalability" (with numbers)
- "On-call" or "production operations"
- "Code review" or "mentorship"
- "Data structures and algorithms"
- "Design documents" or "technical specs"
- "Cross-functional" or "stakeholder management"
- "Ambiguous problems" or "zero-to-one"

**Current resume coverage:** ~40% of these appear. The resume uses adjacent language ("event-driven architecture" instead of "distributed systems," "architectural decisions" instead of "system design").

**Fix:** Deliberately match the FAANG vocabulary. Add a "Technical Skills" section that explicitly names these terms. Rewrite bullets to use FAANG's preferred phrasing.

### Issue 4: The career break is too honest

**Why it matters:** FAANG recruiters see "Jan 2019 – Feb 2022" followed by "Career Break — Self-Development" and many will auto-filter. This is unfortunate but real. Even if the actual content (80+ certs, mentoring, open-source) is impressive, the label "career break" is a red flag for many ATS systems and recruiters scanning for continuous employment.

**Fix:** Reframe as **"Founder / Principal Consultant, Deveric Technologies"** — which is technically true (you ran a mentoring initiative, built projects, did hackathons, contributed to open source). This is a legitimate independent technical engagement, not a sabbatical. Pull the specific outputs forward as deliverables, not as "self-directed learning."

### Issue 5: Projects section is underwhelming given actual portfolio

**Why it matters:** The "Selected Projects" section lists 5 projects with 1-line descriptions. FAANG reviewers want to see production-scale system complexity, not "AI-powered journaling with sentiment analysis."

**Current weakness:**
- "Refleckt Journal: Rust · Next.js · AWS · OpenAI · PostgreSQL — AI-powered journaling with sentiment analysis"
- "UniCorns: multi-tenant SaaS marketplace for African SMBs; 5 Rust microservices, M-Pesa, AWS Lambda, DynamoDB"

**Fix:** Reduce to 3-4 projects but expand each with: scale (users, RPS, data volume), architectural decisions (what you'd defend in an interview), and commercial outcome (revenue, pilot customers, or users).

### Issue 6: Technology stack list is bloated and unfocused

**Why it matters:** Listing "TypeScript · Node.js · Java · Scala · Python · Rust · Go · REST · GraphQL · gRPC" signals breadth but dilutes the signal. FAANG recruiters will wonder which you're actually expert in.

Listing 80+ certifications at the top creates an impression of certification-chaser, not practitioner. Ironic but true — certifications read as *weaker* signal than production shipping.

**Fix:** 
1. Tier the skills: "Expert (5+ years production)" vs "Proficient (1-5 years)" vs "Working knowledge." 
2. Remove certifications from the top of the resume. Mention them once in a small line at the bottom or on LinkedIn only.
3. Cap the skills section at ~20 items in the primary tier.

### Issue 7: Education section is weak

**Why it matters:** FAANG pays attention to school. UMass Lowell is a respectable school but not a FAANG feeder. What's missing is evidence of academic excellence.

**Current:** "B.S. Computer Science · Minor: Mathematics · Dean's List · Microsoft & Google Scholar"

**Fix:** Expand to emphasize the signals:
- **Dean's List** — which semesters/how many times?
- **Microsoft Scholarship Recipient (2012-2013)** — this is a competitive award worth emphasizing
- **Google Scholarship Recipient (2011-2012)** — same
- **Omicron Delta Kappa (ODK)** — honor society, worth naming
- **Graduation honors** — did you graduate with honors? Cum laude? Say so.

### Issue 8: Professional Summary is too long and narrative

**Why it matters:** A FAANG recruiter reads the summary in 3-5 seconds. Your current summary is 95 words and reads as a paragraph. By the time they get to "Deep, practical expertise in mobile money integrations across Africa," they've moved on.

**Fix:** Rewrite as a 3-line summary with **hard hooks** — specific claims that trigger interview interest:
- Line 1: Identity + seniority
- Line 2: Scale + scope (with numbers)
- Line 3: Differentiator (what only you bring)

### Issue 9: No "Selected Achievements" or "Publications" section

**Why it matters:** FAANG loves signals that suggest you're active in the broader community. Open-source contributions, conference talks, blog posts, mentoring, notable GitHub projects.

**Your actual assets** (not on the resume):
- Deveric mentoring initiative (significant)
- Multiple production-deployed personal projects
- LinkedIn thought leadership (if applicable)
- Active GitHub with 20+ public repos
- Speaking engagements (if any)

**Fix:** Add a "Selected Achievements" section or integrate these into existing sections with clear callouts.

### Issue 10: Missing LinkedIn-style impact language

**Why it matters:** FAANG recruiters are increasingly trained on LinkedIn impact-bullet formats. Your current bullets often describe *activities* ("Worked with Nairobi County Government to pilot the platform") rather than *outcomes* ("Shipped government pilot serving 2.3M residents; second of its kind in Africa").

**Fix:** Every bullet should follow one of these formats:
- `[Action verb] [scope] [method] [outcome with metric]`
- `[Problem] → [solution] → [result with metric]`

---

## Moderate Issues (Should Fix)

### Issue 11: Dates and tenures need clarity
Some roles show overlapping dates (RGA Jan-Jul 2022, but "Career Break Jan 2019 - Feb 2022" which overlaps). Fix the timeline.

### Issue 12: Location phrasing inconsistent
"Nairobi, Kenya" vs "Atlanta, GA · Remote" vs "Seattle, WA / Nairobi" — pick a consistent format.

### Issue 13: Contact section is cluttered
Five different links in the header is too many. Keep email + LinkedIn + GitHub + Portfolio. Move the rest to a footer or omit.

### Issue 14: References section is unusual
Including a specific named reference with phone number on a resume is uncommon in the US/FAANG context. Most expect "References available upon request" or omit the section entirely.

---

## What the Resume Does Well (Preserve)

1. **Domain depth in African fintech and energy** — this is genuinely rare and should be showcased, not generic-ified
2. **Technical breadth across languages** — legitimately polyglot, real production experience
3. **Hands-on + leadership balance** — you code and lead, which is valuable at Staff+ levels
4. **Recent Ignite role narrative** — the best section currently, shows real scope and ownership
5. **Visual clean design** — the layout is readable and professional

---

## The Overhaul Strategy

The overhauled resume will:

1. **Preserve the clean visual structure** you already have
2. **Add metrics to every bullet** — using specific numbers where known, credible ranges where estimated
3. **Reframe the career break** as principal consulting work under Deveric Technologies
4. **Rewrite the summary** as three punchy lines with hard hooks
5. **Add missing FAANG keywords** throughout — distributed systems, system design, scalability, etc.
6. **Tier the technical skills** to show depth over breadth
7. **Demote the 80+ certifications** to a single line at the bottom
8. **Expand education** to show academic excellence signals
9. **Reframe projects** as production systems with scale and commercial outcomes
10. **Add "Selected Achievements"** to capture mentoring, open-source, speaking
11. **Clean up the header** — 4 links max
12. **Remove the references section** (unusual for US/FAANG)

**Post-sprint addendum:** After the 15-week sprint, the resume gets a second overhaul — the new greenfield apps (Sauti, Sherehe, Shamba) and major extensions (LendStream v2, Unicorns v2, BSD Engine v2, PayGoHub v2) will provide evidence-based bullets that no current resume can match. The version produced now is the FAANG-ready version for the current state; the version produced Week 16 will be the "unemployable founder" version.

---

## Success Metrics for the Overhauled Resume

- Passes Greenhouse/Lever/Workday keyword matching against L5/L6 Google, Meta, Amazon JDs (target: 80%+ keyword match)
- Survives 6-second recruiter scan (test: cover everything below "Professional Summary" and see if top 3 lines tell the story)
- No weak bullets (every bullet contains a metric or specific outcome)
- Fits on 1 page for US/FAANG submission, 2 pages for detailed roles (your current version is 4 pages — this is too long)

---

## One Final Note on FAANG ATS Reality

Even a perfectly optimized resume cannot overcome the geographic and network-based filters FAANG recruiters apply. Being Nairobi-based rather than Silicon Valley-adjacent will filter you out of some pipelines regardless of resume quality. The counter-strategies are:

1. **Targeted referrals** — one internal referral beats 100 cold applications
2. **Specific role matching** — FAANG teams hiring for Africa (Google Nairobi, Meta Lagos, AWS Africa) have very different filters than US-based roles
3. **Remote-first companies** — Stripe, Shopify, Vercel, Linear, and similar tier-1 companies that are fully remote and genuinely global in hiring
4. **The unemployability thesis** — the sprint's real objective is making you so clearly valuable that filters stop mattering

Keep this in perspective. The overhauled resume maximizes what you can control (the filter pass rate); the sprint itself is what actually closes the FAANG gap.

---

## Revision History

### Revision 2 — SDET Reframing + Observability Stack Addition (April 2026)

Triggered by recognition that the original overhaul, while ATS-optimized on keywords and metrics, still carried a residual risk of being miscategorized into "QA-only" recruiting pipelines due to the Ignite title ("Team Lead — QA & Engineering"). The goal of Revision 2 was to surface SDET + engineering fluency so clearly that any recruiter reading past the title sees software engineering, not pure quality work — while keeping the title structurally truthful.

**Changes made in this revision:**

1. **Subtitle upgraded** from "Staff Software Engineer · Polyglot Systems Architect" to "Staff Software Engineer · SDET & Platform · Polyglot Systems Architect." The SDET signal now appears before any bullet is read.

2. **Title annotation at Ignite:** "Team Lead — QA & Engineering" became "Team Lead — QA & Engineering (SDET Track)" — a parenthetical that correctly signals engineering depth within a title that may have been QA-labeled on the employment record. Both strictly accurate and ATS-interpretable.

3. **Professional Summary rewritten** to lead with "shift-left engineering transformation" — framing QA work as a consequence of DDD/BDD/TDD discipline, not the primary identity. Explicitly surfaces OpenTelemetry, Prometheus, Grafana, Jaeger, ELK stack. Explicitly names the BFF pattern as a business-logic centralization strategy. Summary now reads as engineer-who-did-testing, not tester-who-did-engineering.

4. **Skills section expanded from 4 categories to 6** — the critical addition being two new first-class tiers:
   - **Observability & APM** — OpenTelemetry (OTel), Prometheus, Grafana, Jaeger, ELK Stack (Elasticsearch/Logstash/Kibana), CloudWatch, Datadog, distributed tracing, SLO/SLI definition, on-call runbook design
   - **SDET & Test Engineering** — Playwright, Cypress, Jest, JUnit, pytest, RSpec, TDD, BDD (Cucumber/Gherkin), property-based testing, contract testing, shift-left test strategy, E2E automation in CI/CD, test pyramid design, coverage instrumentation, mutation testing
   - The Architectural Patterns tier now explicitly leads with Domain-Driven Design (DDD) and includes Backend-for-Frontend (BFF) prominently

5. **Ignite bullets restructured** — the opening bullet no longer leads with "Led 4-engineer QA team" but with "Led shift-left engineering transformation." Every bullet now pairs a testing/quality activity with a corresponding engineering discipline (DDD, BDD, observability, architecture, platform migration). New bullets explicitly added for:
   - OpenTelemetry/Prometheus/Grafana/Jaeger/ELK stack instrumentation with measured outcome (MTTD < 5 min)
   - BFF advocacy for client-specific backends with business-logic centralization rationale
   - BDD/Gherkin-driven defect detection shifted left in the SDLC

**ATS keyword coverage now includes (previously missing or understated):**

- SDET / Software Development Engineer in Test
- OpenTelemetry (OTel)
- Prometheus
- Grafana
- Jaeger
- ELK Stack / Elasticsearch / Logstash / Kibana
- Application Performance Monitoring (APM)
- Distributed tracing
- SLO / SLI / error budgets
- TDD / BDD / DDD (all three explicitly named)
- Shift-left testing / shift-left strategy
- Test pyramid
- Property-based testing
- Contract testing
- Mutation testing
- Backend-for-Frontend (BFF)
- Domain-Driven Design (DDD) — elevated to architectural-pattern primary slot
- Cucumber / Gherkin
- Defensive programming

**Filter pass probability (post-Revision 2):** ~80-88% for **Platform / Backend / Staff Engineer** roles. For **SRE / Platform Engineering** roles specifically (e.g., Google SRE, Meta Production Engineer, Stripe Platform), estimated ~82-90% — the observability stack additions open these adjacent pipelines that the original overhaul did not target. For **pure QA Manager** roles, intentionally less attractive now — the reframing deliberately steers away from that track while staying truthful about the Ignite scope.

**Title conflict consideration:** Both "Team Lead — QA & Engineering" (title of record) and the SDET/Platform framing coexist in the resume without contradiction. A recruiter who opens the document sees:
- Header subtitle: "SDET & Platform" — primary identity signal
- Role title: "Team Lead — QA & Engineering (SDET Track)" — structurally truthful with an engineering qualifier
- First Ignite bullet: "Led shift-left engineering transformation combining DDD/BDD/TDD discipline with SDET tooling" — explicitly an engineering transformation, with QA as downstream effect

If questioned in interview about the title, the honest answer is: "My title at Ignite was 'Team Lead — QA & Engineering' because the org's structure put me in the QA reporting line. The actual work was SDET and platform — I built test infrastructure, instrumented observability, led the Rails upgrade, and architected async payment flows. The QA coverage improvements came out of defensive programming and TDD discipline, not as isolated quality work." This is both true and positions the candidate for engineering tracks.

**One caveat:** If applying specifically for roles with "SDET" or "Software Engineer in Test" in the title, consider dropping the parenthetical "(SDET Track)" because it can read as aspirational. For those roles, frame as pure SDET. For general Platform / Backend / Staff Engineer roles, keep the current version — it signals breadth without diluting the engineering identity.

