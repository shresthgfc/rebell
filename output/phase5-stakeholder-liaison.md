# Stakeholder Report — Mosaic

## 1. Document Info
- **Date:** 2026-03-21
- **Source:** phase-1-synthesis.md, phase3-synthesis.md, phase4-synthesis.md
- **Author:** Stakeholder Liaison Sub-Agent
- **Status:** Draft — awaiting client sign-off on concept direction

---

## 2. Executive Summary [SUM]

**Recommendation: Go with Conditions**

Mosaic is a daily creative website where anyone can contribute a small piece of art — a color, a shape, a drawing — in response to a shared daily prompt. Every individual contribution is stitched together into one collective image for that day, and each contributor receives a personal shareable link. The concept is proven by analogy: it combines the daily habit of Wordle with the delightful discovery of creative browser experiences. The technical plan is complete, the build cost is low, and quality testing is thorough. Two security gaps and two color issues must be fixed before public launch, and the client must confirm the concept direction and provide a day-one audience seeding strategy.

**What we are building:** A website where the daily prompt drives participation, the collective result drives curiosity, and the personal shareable link drives new visitors — a self-reinforcing growth loop requiring no advertising budget.

**Investment required:** 8 weeks of development, approximately $26 per month in ongoing operating costs.

**Expected return:** Success is measured by daily active contributors, the share-to-new-visitor conversion rate, and how often users complete a contribution. Comparable daily habit products (Wordle) demonstrate that a small, loyal daily audience is more valuable than a large inactive one.

**Key risks:**
- The site launches to an empty gallery unless 20–50 early contributors are recruited before public launch. This is the single highest-risk business scenario.
- Inappropriate user-submitted images could appear publicly without a content screening system in place — a reputational and legal exposure that must be resolved before launch.
- The nightly job that assembles the daily collective image must run reliably every day without exception, or the core product promise breaks.

**Next steps:**
- Client formally confirms the Mosaic concept and approves the reduced launch scope (gallery and streak features deferred to a later release).
- Client commits to a day-one audience seeding strategy — who will contribute on day one before the public arrives?
- Engineering team resolves the four pre-launch technical issues flagged by the quality review (two security items, two color contrast items) before the site goes live.

---

## 3. What We Are Building [SUM]

Mosaic is a creative participation website built around a daily ritual. Each day, the site presents a single creative prompt — a theme, a mood, a subject. Visitors respond by contributing a small visual element: a color, a pattern, or a simple drawing. No account required to participate.

At the end of each day, all contributions are combined into one collective image — the day's Mosaic. Every contributor receives a unique personal link showing their piece within the whole. That link is designed to be shared on social media, and every share brings new visitors to the site.

The experience is deliberately simple. The default contribution method requires no artistic skill — color or pattern selection is available to anyone. An optional drawing mode is available for those who want more creative control. The simplest path is always the most visible one.

The site does not require a login to participate. Visitors can create and share before they ever register, removing the single biggest barrier to first-time engagement.

---

## 4. Timeline and Cost [TML + FIN]

**Total build time:** 8 weeks across 4 two-week periods.
**Ongoing operating cost:** approximately $26 per month after launch.

| Period | Weeks | What Gets Built | Business Value Delivered |
|--------|-------|----------------|--------------------------|
| Sprint 1 | 1–2 | Site foundation, database, visitor sessions, landing page, basic creation tool | A working page visitors can land on and interact with |
| Sprint 2 | 3–4 | Contribution submission, image generation, drawing tool | The full create-and-submit experience is functional |
| Sprint 3 | 5–6 | Nightly collective image assembly, share pages, content screening | The product's core promise works end-to-end; sharing goes live |
| Sprint 4 | 7–8 | Error handling, admin controls, performance tuning, accessibility fixes | Site is stable, safe, and ready for public launch |

The $26/month operating cost covers hosting, database, file storage, and automated screening of user-submitted images. This is a low-cost operating model appropriate for an audience-building phase.

---

## 5. Key Risks in Business Terms [RSK]

| # | Risk | Business Impact | Likelihood | Mitigation | Status |
|---|------|----------------|-----------|-----------|--------|
| 1 | Cold start — site launches with no community | First visitors see an empty or near-empty gallery; no reason to return or share | High | Recruit 20–50 early contributors before public launch; admin can seed contributions on day one | Not yet actioned — client decision required |
| 2 | Inappropriate images appear publicly | Reputational damage; potential legal exposure, especially under EU data protection rules | Medium | Automated content screening (Cloud Vision) + manual review queue before images go public | Designed but not yet built |
| 3 | Daily assembly job fails silently | The collective image does not update; the site appears broken; daily habit loop breaks | Medium | Build in automatic alerts and a manual re-trigger for the daily assembly process | Designed into implementation plan |
| 4 | Mobile contribution experience is clunky | Most visitors are on phones; a poor mobile experience kills completion and sharing rates | Medium | Mobile-first prototype to be tested on real phones in week one | Planned for Sprint 1 |
| 5 | GDPR exposure before EU visitors arrive | Fines up to 4% of annual revenue; reputational damage in EU markets | Low-Medium | Consent management required before any data is stored from EU visitors | Defined but not yet implemented |

### Top 3 Risks Explained

**Risk 1 — Will anyone show up?**
A daily creative community only works when there is already something to see. If the first hundred visitors arrive and find two contributions in the gallery, the experience falls flat. The product is designed to deliver individual value even without community volume — your personal shareable link exists regardless of how many others contributed — but a near-empty collective image is a poor first impression. The fix is operational, not technical: the client needs to identify who contributes before the public arrives. This is the most important business decision before launch.

**Risk 2 — What if someone submits something harmful?**
User-submitted images carry inherent content risk. The technical team has designed an automated screening layer (images are checked by an external service before they appear publicly) and a manual review queue. Neither is built yet. This must be operational before the site accepts public contributions. Without it, the site is one bad submission away from a news story.

**Risk 3 — What if the daily image does not get built?**
Mosaic's entire value proposition depends on a new collective image appearing every day. That assembly happens automatically each night. If it fails without anyone noticing, visitors arrive to a stale or missing image. The technical plan builds in automatic failure alerts and a manual backup trigger. This is the highest-consequence single automated process in the product and has been treated as such throughout the planning pipeline.

---

## 6. Quality Assurance Summary [MET]

The quality review covered five areas: overall test strategy, functional testing, speed and performance, security, and accessibility for users with disabilities. The findings give a business confidence level of **medium-high** — the plans are thorough and the identified issues have clear fixes, but four issues must be resolved before the site can launch responsibly.

**What testing covers, in plain terms:**

- Every code change goes through 7 automated checkpoints before it can reach real users — catching problems early when they are cheapest to fix.
- The daily image assembly process is tested against 500 contributions and must complete within 60 seconds.
- The site is tested under simulated visitor load to confirm it responds quickly even when many people arrive at once.
- Security testing follows an industry-standard checklist of the 10 most common ways websites are compromised. The site passes 8 of 10 categories; 2 have fixes in progress.
- Accessibility testing confirms the site works for users with visual impairments, keyboard-only users, and screen reader users. The simple contribution mode is fully accessible by default.

**Four issues must be fixed before launch (all have defined solutions):**

| Issue | Business Translation | Fix Defined? |
|-------|---------------------|-------------|
| Security gap 1 | The admin area uses a permanent password that cannot be revoked without a full redeployment — an unnecessary risk | Yes |
| Security gap 2 | A specific browser security setting is misconfigured, slightly increasing exposure to content injection attacks | Yes |
| Accessibility issue 1 | The success confirmation color fails readability standards for users with low vision | Yes — use a darker green |
| Accessibility issue 2 | An action button color fails readability standards at small text sizes | Yes — darken or enlarge |

None of these issues are architectural. All four have documented, low-effort fixes scheduled for Sprint 4.

---

## 7. ROI Indicators [FIN + MET]

Mosaic is not a direct-revenue product at launch — it is an audience-building product. ROI is measured by the strength of the daily habit loop and the viral reach of the sharing mechanic. The three headline indicators are:

| Metric | What It Measures | Target at 90 Days | How to Measure |
|--------|-----------------|-------------------|---------------|
| Daily active contributors | Whether the habit loop is working | Growing week-over-week | Count of unique contributions per day |
| Share-to-new-visitor conversion | Whether the sharing mechanic drives real growth | At least 1 new visitor per 3 shares | Referral source tracking on landing page |
| Contribution completion rate | Whether the creation experience is easy enough | 70% of visitors who start a contribution finish it | Start event vs. submit event tracking |

**How we know it worked (plain language):** Three months after launch, a healthy Mosaic shows more contributors each week than the week before, shares that reliably bring in new faces, and a contribution experience where most people who start also finish. If daily contributors are flat or declining, the prompt quality or creation experience needs attention. If the share-to-visitor rate is low, the shared image preview needs improvement. If completion rate is below 50%, the creation tool is too difficult and must be simplified.

**Break-even context:** At $26/month in operating costs, the financial bar for viability is extremely low. The meaningful investment is development time. The primary return is audience and brand equity, which convert to revenue through monetization options (optional tips, premium features, partnerships) that are out of scope for this phase but enabled by the audience Mosaic builds.

---

## 8. Go/No-Go Recommendation [DEC]

- **Recommendation:** Go with Conditions
- **Rationale:** The concept is well-researched, the technical plan is complete, the build cost is modest, and the quality review identified only four pre-launch issues — all with clear, low-effort fixes. The product is ready to build. However, two conditions must be met before the client can be confident the launch will succeed: the concept must be formally confirmed as the direction (all downstream work to date is provisional), and a day-one seeding strategy must be committed to. Without early contributors in place before public launch, the product's first impression will underperform regardless of technical quality.
- **Conditions:**
  1. Client formally confirms the Mosaic concept as the approved direction — in writing — before Sprint 1 begins.
  2. Client commits to a named person or group responsible for recruiting 20–50 contributors who will participate before the public launch date.
  3. All four pre-launch quality issues (two security, two accessibility) are resolved and verified before the site accepts public traffic.
- **Re-assessment:** If conditions 1 and 2 are not confirmed within two weeks of this report, re-assess whether the 8-week build timeline remains achievable for the intended launch window.

### Approval

| Role | Name | Decision | Date |
|------|------|----------|------|
| Product Owner | | | |
| Engineering Lead | | | |
| Business Sponsor | | | |

---

## 9. Next Steps [DEC]

| # | Action | Owner | Deadline | Dependency |
|---|--------|-------|----------|-----------|
| 1 | Formally confirm Mosaic as the approved product concept | Product Owner | Before Sprint 1 starts | Unblocks all downstream work |
| 2 | Name the person responsible for day-one audience seeding; define who contributes before public launch | Product Owner | Before Sprint 3 ends | Required for a successful launch |
| 3 | Resolve all four pre-launch quality issues (security + accessibility) | Engineering Lead | End of Sprint 4 | Site cannot go live without these |
| 4 | Confirm team size and composition | Engineering Lead | Immediately | Sprint 1 planning depends on it |
| 5 | Define budget formally | Product Owner / Business Sponsor | Before Sprint 2 | Required for infrastructure commitments |

---

## 10. Open Questions [DEC]

| # | Question | Priority | Blocking? | Default if Unanswered |
|---|---------|----------|-----------|----------------------|
| 1 | Has the client formally approved the Mosaic concept? | Critical | Yes | Pipeline work is provisional; Sprint 1 should not begin without this |
| 2 | Who is responsible for recruiting early contributors before launch? | Critical | No, but launch success depends on it | Launch proceeds with no seeded community — high failure risk |
| 3 | What is the confirmed budget? | High | No | Planning assumes medium-tier budget; $26/month operating cost is confirmed |
| 4 | Is the 8-week timeline fixed or flexible if the team is smaller than assumed? | Medium | No | Plan assumes 2–5 developers with relevant experience |
| 5 | Are there specific geographic markets targeted at launch (affects data privacy obligations)? | Medium | No | EU visitors assumed possible; GDPR compliance is included in plan |
