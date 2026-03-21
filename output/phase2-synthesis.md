# Phase 2 Synthesis — Architecture & Design

## 1. Phase Summary
- **Agents that contributed**: system-architect, database-architect, api-designer, security-architect, ux-designer
- **Key deliverables**:
  - `output/phase2-system-architecture.md` — C4 diagrams, ADRs, composite pipeline, deployment topology
  - `output/phase2-database-architecture.md` — ER model, table definitions, migrations, GDPR
  - `output/phase2-api-design.md` — REST endpoints, auth flow, error handling, rate limiting
  - `output/phase2-security-architecture.md` — STRIDE model, moderation pipeline, OWASP mitigations
  - `output/phase2-ux-design.md` — User journeys, wireframes, design system, accessibility

---

## 2. Architecture Decisions Summary

| # | Decision | Rationale |
|---|---------|-----------|
| ADR-001 | Next.js 15 App Router on Vercel | Single platform for SSR, API, cron, blob storage — minimal ops |
| ADR-002 | Neon serverless PostgreSQL + Drizzle ORM | Scales to zero, branches for dev, compatible with Vercel |
| ADR-003 | Sharp (libvips) for composite generation | Fast, memory-efficient, runs in Node.js serverless functions |
| ADR-004 | Anonymous-first sessions via HttpOnly cookies | Zero-login barrier; sessions enable idempotent contributions |
| ADR-005 | Cloud Vision SafeSearch for content moderation | Automated pre-screening; fallback to manual queue |
| ADR-006 | Upstash Redis for caching + rate limiting | Serverless-compatible, sliding window rate limiter |

---

## 3. Cross-Cutting Concerns Resolved

### Authentication → API → Database alignment
- Session token issued on first visit (middleware)
- Cookie: `mosaic_session`, HttpOnly, Secure, SameSite=Lax
- Session stored in `sessions` table with optional `user_id` FK
- API idempotency enforced by `UNIQUE(prompt_id, session_id)` constraint
- All agents agree: no login required for MVP core flow

### Content Moderation → Security → UX alignment
- Drawing content runs through Cloud Vision before storage
- Emoji/color contributions use predefined palettes (no moderation needed)
- UX provides two modes: Simple (inherently safe) and Advanced (needs moderation)
- Rejected content hidden but logged; user sees generic error

### Composite Pipeline → System → Database alignment
- Cron at 00:00 UTC fetches approved contributions from DB
- Sharp composites images in grid layout
- Result stored to Vercel Blob; record inserted in `composites` table
- Redis cache invalidated for `composite:today`
- Advisory lock prevents duplicate runs

---

## 4. Key Technical Specifications

| Component | Technology | Notes |
|-----------|-----------|-------|
| Frontend | React 19 + Next.js 15 App Router | Mobile-first, 720px max-width on desktop |
| API | Next.js Route Handlers (REST) | 7 endpoints + 4 admin endpoints |
| Database | PostgreSQL (Neon) + Drizzle ORM | 5 tables, 6 indexes |
| Cache | Redis (Upstash) | 6 key patterns, TTLs aligned to daily cycle |
| Storage | Vercel Blob | Contribution images, composites, OG images |
| Image Processing | Sharp | Composite generation in serverless function |
| Moderation | Cloud Vision SafeSearch | Pre-publish automated screening |
| Deployment | Vercel (Preview/Staging/Production) | Serverless, global CDN, cron functions |

---

## 5. Risks Carried Forward to Implementation

| Risk | Mitigation Designed | Still Needs |
|------|-------------------|-------------|
| Nightly cron failure | Idempotent design, advisory lock, alerting | Implementation + monitoring setup |
| Mobile drawing UX | Canvas with basic tools; simple mode as fallback | Week 1 prototype testing on real devices |
| Content moderation bypass | Cloud Vision + manual queue | Integration testing with edge cases |
| Cold start | Admin seeding mechanism designed | Operational playbook for launch day |
| Vercel function timeout (composite gen) | Pro plan (300s limit); chunked processing for large mosaics | Load testing with 500+ contributions |

---

## 6. Action Items for Phase 3 (Implementation Planning)

| # | Action | Owner |
|---|--------|-------|
| ACT-P3-001 | Tech lead: decompose into 2-week sprints, define coding standards | tech-lead |
| ACT-P3-002 | Backend dev: plan service layer for contributions + composite pipeline | backend-developer |
| ACT-P3-003 | Frontend dev: plan component hierarchy, state management, canvas implementation | frontend-developer |
| ACT-P3-004 | DevOps: plan CI/CD pipeline, environment setup, monitoring | devops-engineer |
| ACT-P3-005 | Database engineer: plan migration scripts, connection pooling, seed data | database-engineer |
