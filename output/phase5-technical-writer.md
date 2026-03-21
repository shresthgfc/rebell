# Documentation Plan — Mosaic

## 1. Document Info
- Date: 2026-03-21
- Source: phase2-api-design.md, phase3-synthesis.md, phase4-synthesis.md
- Author: Technical Writer Sub-Agent
- Status: Draft

## 2. Executive Summary

Mosaic requires documentation across all four Diataxis categories, anchored by P0 API reference and deployment runbook that must ship with v1.0. Auto-generation via JSDoc and OpenAPI inference is the primary strategy for reference docs. Documentation lives as docs-as-code in `/docs` with CI checks gating every PR.

---

## 3. Documentation Map (Diataxis)

| ID | Type | Document Title | Audience | Priority | Est. Pages | Dependencies |
|----|------|---------------|----------|----------|-----------|-------------|
| DOC-001 | TUT | Getting Started: Run Mosaic Locally | New contributors | P0 | 4 | phase3-synthesis (stack) |
| DOC-002 | TUT | First Contribution Walkthrough | New contributors | P1 | 3 | DOC-005, DOC-007 |
| DOC-003 | HT | Deploy Mosaic to Vercel | Operators | P0 | 3 | DOC-009, DOC-010 |
| DOC-004 | HT | Run the Composite Pipeline Manually | Operators / On-call | P0 | 2 | DOC-008 |
| DOC-005 | HT | Add a New Daily Prompt | Content editors | P1 | 2 | DOC-007 |
| DOC-006 | HT | Moderate a Flagged Contribution | Moderators | P1 | 2 | DOC-007, DOC-008 |
| DOC-007 | REF | API Endpoint Reference | Developers | P0 | 6 | phase2-api-design.md |
| DOC-008 | REF | Admin Endpoint Reference | Operators | P0 | 2 | phase2-api-design.md |
| DOC-009 | REF | Environment Variables Reference | Operators / DevOps | P0 | 2 | phase3-synthesis (stack) |
| DOC-010 | REF | Database Schema Reference | Developers | P1 | 3 | phase3-db-engineer |
| DOC-011 | REF | Error Codes Reference | Developers | P0 | 1 | phase2-api-design.md |
| DOC-012 | EXP | Architecture Overview | Developers / New hires | P1 | 4 | phase3-synthesis |
| DOC-013 | EXP | Composite Pipeline Design | Developers | P1 | 3 | phase3-backend-developer |
| DOC-014 | EXP | Anonymous Session Model | Developers | P2 | 2 | phase2-api-design.md |
| DOC-015 | EXP | Content Moderation Flow | Moderators / Developers | P2 | 2 | phase4-synthesis |

### Coverage Analysis
- [x] Every public API endpoint has reference documentation (DOC-007, DOC-008 cover all 11 endpoints)
- [x] Every operational procedure has a runbook (Section 5: composite pipeline, deployment, moderation)
- [x] Every architecture decision has an explanation document (DOC-012, DOC-013, DOC-014, DOC-015)
- [x] New developer onboarding path is complete (Section 6)
- [x] Every integration has a how-to guide (Vercel deploy, pipeline trigger, content moderation)

---

## 4. Document Outlines

### DOC-001: Getting Started: Run Mosaic Locally (Type: Tutorial)
- **Audience:** New contributors with Next.js familiarity
- **Prerequisites:** Node.js 20+, Git, a Neon account (free tier), an Upstash Redis account
- **Sections:**
  1. Clone and install — `git clone`, `npm install`, verify Node version
  2. Configure environment — Copy `.env.example`, fill Neon DATABASE_URL, Upstash keys, Vercel Blob token
  3. Run database migrations — `npx drizzle-kit migrate`, verify tables exist
  4. Seed a test prompt — `npm run db:seed`
  5. Start the dev server — `npm run dev`, open `localhost:3000`
  6. Verify the happy path — Submit a contribution, confirm it appears
- **Success criteria:** Reader reaches a working local instance and submits one contribution in under 25 minutes
- **Maintenance owner:** Backend team

### DOC-003: Deploy Mosaic to Vercel (Type: How-To)
- **Audience:** Operators performing a first deployment or reprovisioning
- **Prerequisites:** Vercel Pro account, Neon DB provisioned, Upstash Redis provisioned, Vercel Blob store created, admin token generated
- **Sections:**
  1. Problem statement — deploying a fresh Mosaic instance to Vercel
  2. Connect the repository to Vercel
  3. Set all required environment variables (references DOC-009)
  4. Configure the nightly cron in `vercel.json`
  5. Run production migrations via Drizzle
  6. Verify deployment with smoke tests
- **Success criteria:** `GET /api/prompts/today` returns 200 in production
- **Maintenance owner:** DevOps team

### DOC-007: API Endpoint Reference (Type: Reference)
- **Audience:** Developers integrating with or extending the API
- **Prerequisites:** None
- **Sections:**
  1. Base URL and versioning — MVP uses `/api/`, v1.1 introduces `/api/v1/`
  2. Authentication — anonymous session cookie, admin bearer token
  3. Rate limiting table (per endpoint limits, Upstash sliding window)
  4. GET /api/prompts/today — params, response schema, cache behavior
  5. POST /api/contributions — request schema (all 3 content types), 201/200 idempotency behavior
  6. GET /api/contributions/:id — response schema, 404 behavior
  7. GET /api/composites/today — response schema
  8. GET /api/composites/:date — date format, 400/404 behavior
  9. Error format and error codes table (references DOC-011)
  10. Request/response conventions — UUIDs, ISO 8601, envelope pattern
- **Success criteria:** A developer can implement a client without reading source code
- **Maintenance owner:** Backend team; auto-generate from JSDoc/OpenAPI annotations where possible

### DOC-009: Environment Variables Reference (Type: Reference)
- **Audience:** Operators, DevOps, contributors setting up local environments
- **Prerequisites:** None
- **Sections:**
  1. Required variables table — name, description, example value, where to obtain
  2. Optional variables table — feature flags, overrides
  3. `.env.example` listing with inline comments
- **Success criteria:** All variables are documented with no ambiguity about format or source
- **Maintenance owner:** DevOps team

### DOC-011: Error Codes Reference (Type: Reference)
- **Audience:** Developers handling API errors in clients
- **Prerequisites:** Familiarity with DOC-007
- **Sections:**
  1. Error envelope format — `{ error: { code, message, status, details } }`
  2. Full error codes table: VALIDATION_ERROR, INVALID_CONTENT_TYPE, PAYLOAD_TOO_LARGE, INVALID_DATE, NOT_FOUND, CONTRIBUTION_EXISTS, RATE_LIMITED, INTERNAL_ERROR, MODERATION_REJECTED
  3. Retry guidance for 429 (Retry-After header) and 500
- **Success criteria:** Every error code is explained with cause and recommended client action
- **Maintenance owner:** Backend team

---

## 5. Operational Runbooks

| ID | Runbook Title | Trigger | Severity | Owner | Last Tested |
|----|-------------|---------|----------|-------|-------------|
| RB-001 | Composite Pipeline Failed | Vercel cron alert / missing composite by 02:00 UTC | High | Backend on-call | Untested — schedule before launch |
| RB-002 | Production Deployment Rollback | 5xx error rate > 0.5% for 5 min post-deploy | Critical | DevOps on-call | Untested — schedule before launch |
| RB-003 | Moderate a Rejected Contribution | Moderation queue alert / admin report | Medium | Content moderator | Untested — schedule before launch |

### Runbook RB-001: Composite Pipeline Failed
- **Trigger:** Vercel cron monitoring alert fires; or `GET /api/composites/today` returns 404 after 02:00 UTC
- **Severity:** High
- **Prerequisites:** Vercel dashboard access, `ADMIN_TOKEN` env var, staging familiarity
- **Steps:**
  1. Check Vercel function logs for the cron invocation: Dashboard → Functions → `/api/cron/composite`
  2. Identify error (DB timeout, Sharp OOM, Blob upload failure)
  3. If DB: verify Neon connection pool (`DATABASE_URL` valid, pool not exhausted)
  4. Manually re-trigger: `curl -X POST https://mosaic.app/api/admin/composite/generate -H "Authorization: Bearer $ADMIN_TOKEN"`
  5. Monitor response — pipeline is idempotent; safe to re-run
  6. Confirm composite appears: `curl https://mosaic.app/api/composites/today`
- **Verification:** `GET /api/composites/today` returns 200 with valid `imageUrl`
- **Rollback:** No rollback needed — pipeline is additive. If partially written composite exists, re-trigger overwrites it safely via idempotency key.
- **Escalation:** Backend team lead if pipeline fails after 3 manual attempts; check Neon and Vercel Blob status pages
- **Last Tested:** Not yet — must be tested in staging before Sprint 4 sign-off
- **Owner:** Backend team

### Runbook RB-002: Production Deployment Rollback
- **Trigger:** Vercel alert: 5xx rate > 0.5% for 5 minutes following a deployment; or G7 production gate failure
- **Severity:** Critical
- **Prerequisites:** Vercel dashboard access with deployment admin role
- **Steps:**
  1. Open Vercel dashboard → Deployments → identify previous successful deployment
  2. Click "Promote to Production" on the last known-good deployment
  3. Verify rollback: `curl -I https://mosaic.app/api/prompts/today` should return 200
  4. If DB migration was part of the failed deploy: assess whether migration is backward-compatible
  5. If not backward-compatible: open Neon console, run reversal migration from `/drizzle/rollback/` scripts
  6. Post incident note in #incidents Slack channel with deployment hash and symptom summary
- **Verification:** Smoke test suite passes; 5xx rate returns below 0.1% for 5 minutes
- **Rollback:** This runbook IS the rollback procedure; no further undo available beyond reverting to previous deployment
- **Escalation:** DevOps lead if Vercel promotion fails; Neon support if DB rollback needed
- **Last Tested:** Not yet — must be tested in staging before launch
- **Owner:** DevOps team

### Runbook RB-003: Moderate a Flagged Contribution
- **Trigger:** Cloud Vision SafeSearch flags a contribution; or admin report via `/api/admin/moderate/:id` queue
- **Severity:** Medium
- **Prerequisites:** Admin token, access to moderation queue at `/admin` dashboard
- **Steps:**
  1. Open admin panel: `https://mosaic.app/admin` (requires admin bearer token)
  2. Locate contribution by ID in the moderation queue
  3. Review content visually
  4. To reject: `curl -X PATCH https://mosaic.app/api/admin/moderate/{id} -H "Authorization: Bearer $ADMIN_TOKEN" -d '{"action":"reject","reason":"policy_violation"}'`
  5. To approve: same endpoint with `"action":"approve"`
  6. Rejected contributions return `403 MODERATION_REJECTED` on share URL
  7. Audit log entry is written automatically
- **Verification:** `GET /api/contributions/:id` returns 403 for rejected contribution; moderation audit log shows entry
- **Rollback:** Re-approve via same endpoint: `"action":"approve"`
- **Escalation:** Legal/Trust & Safety team for CSAM or serious policy violations; do not attempt manual resolution
- **Last Tested:** Not yet — must be tested in staging before Sprint 3 sign-off
- **Owner:** Content moderation team

---

## 6. Developer Onboarding Path

| Phase | Timeline | Documents | Outcome |
|-------|----------|-----------|---------|
| Day 1 | First day | DOC-001 (local setup tutorial), DOC-009 (env vars), DOC-012 (architecture overview) | Local dev environment running, first prompt visible in browser |
| Week 1 | First week | DOC-007 (API reference), DOC-010 (DB schema), DOC-011 (error codes), DOC-013 (composite pipeline) | Can trace a contribution from POST through DB to composite; first PR open |
| Month 1 | First month | DOC-002 (contribution walkthrough), DOC-014 (session model), DOC-015 (moderation flow), DOC-005 (add a prompt) | Independent contributor; can add prompts, debug pipeline issues, review PRs |

---

## 7. Docs-as-Code Setup

### Tooling
- **Framework:** Docusaurus 3 — fits the project scale; MDX support for interactive API examples
- **Location:** `/docs` folder in the monorepo; README at root links to `/docs`
- **Hosting:** Vercel (same project, `/docs` path prefix) — zero additional infra
- **Search:** Pagefind (static, no external service dependency)
- **Versioning:** Docs branch per release tag; MVP docs live on `main`
- **API Reference generation:** Extract OpenAPI spec from Next.js route handlers via `next-swagger-doc`; auto-render DOC-007 and DOC-008 from spec rather than hand-writing

### CI Integration

| Check | Tool | Gate Type | Runs On |
|-------|------|-----------|---------|
| Link validation | markdown-link-check | Blocking | Every PR |
| Spell check | cspell | Warning | Every PR |
| Markdown lint | markdownlint-cli2 | Blocking | Every PR |
| API spec validation | Spectral with OpenAPI ruleset | Blocking | Every PR |
| Build test | `npm run docs:build` | Blocking | Every PR |
| Stale content detection | Custom script: flag docs with `last-modified` > 90 days | Warning | Scheduled weekly |

### Review Process
- Documentation PRs require approval from: one domain expert (backend lead for API docs, DevOps for runbooks) plus one technical writer pass
- Review checklist: accuracy against current code, completeness of all fields, audience-appropriate language, markdownlint compliance
- Style guide: Google Developer Documentation Style Guide (external reference); project-specific terms in `/docs/style-guide.md`

---

## 8. Documentation Maintenance Strategy

| Activity | Frequency | Owner | Process |
|----------|-----------|-------|---------|
| Accuracy review | Per sprint release | Domain expert per doc | Verify docs reflect merged code changes; update version notes |
| Stale content audit | Quarterly | Technical writer | CI stale-detection report reviewed; docs not updated in 90+ days flagged for rewrite or deletion |
| Runbook testing | Quarterly (and before each launch) | On-call team | Execute RB-001, RB-002, RB-003 in staging; update "Last Tested" field |
| Link checking | Every PR (CI) + weekly scheduled | Automated | Broken links must be fixed within 1 business day of detection |
| API spec sync | Every PR touching route handlers | Backend developer | `next-swagger-doc` regeneration is part of build; drift is a blocking CI failure |
| User feedback review | Monthly | Technical writer | Review GitHub issues tagged `documentation`; prioritize corrections |

---

## 9. Open Questions

| # | Question | Priority | Blocking? | Default if Unanswered |
|---|---------|----------|-----------|----------------------|
| OQ-001 | Will `/api/v1/` versioning prefix ship in v1.1 as planned? DOC-007 needs a versioning section updated at that point. | High | No | Document current `/api/` paths; add versioning section as P1 task for v1.1 |
| OQ-002 | Is there a public-facing changelog or is it internal only? Affects whether DOC set needs a CHANGELOG entry pattern. | Medium | No | Treat as internal; add to `CHANGELOG.md` in repo only |
| OQ-003 | Static admin bearer token (BLK-002 from QA) is flagged for replacement with short-lived JWTs. Admin auth docs must be rewritten when that ships. | High | No | Document current bearer token pattern with a prominent deprecation notice |
| OQ-004 | Will the `/admin` dashboard have a UI or remain curl-only? Affects whether DOC-006 and RB-003 need UI screenshots. | Medium | No | Document curl-based workflow; add UI steps as amendment once dashboard ships |
| OQ-005 | Is there a nominated documentation owner post-launch, or does the backend lead own all doc updates? | High | No | Assign backend lead as interim owner; revisit at Sprint 4 retrospective |
