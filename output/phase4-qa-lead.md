# QA Strategy — Mosaic

## 1. Document Info
- Date: 2026-03-21
- Source: phase2-synthesis.md, phase3-synthesis.md
- Analyst: QA Lead Sub-Agent
- Status: Draft

---

## 2. Strategy Overview

Mosaic is a daily-cycle creative platform with a small but highly risk-concentrated critical path: one nightly cron job composites all contributions into the day's mosaic, a mobile drawing canvas handles raw user-generated content, and anonymous sessions underpin idempotency and abuse prevention. The QA philosophy is shift-left with risk-weighted investment — the nightly pipeline and moderation path receive disproportionately high test coverage because a single failure is visible to every user the next morning. The test pyramid is enforced structurally via CI gates; no stage may be skipped.

---

## 3. Test Pyramid

| Level | Target Ratio | Min Threshold | Tool | Focus Area | Speed Target |
|-------|-------------|---------------|------|------------|-------------|
| Unit | 70% | 65% | Vitest | Services, utilities, validators, Drizzle query builders, Sharp pipeline logic, rate-limit helpers | < 10ms/test |
| Component | (within unit tier) | — | Vitest + React Testing Library | React Server Components, creation tool UI state, Fabric.js canvas tool controls | < 100ms/test |
| Integration | 20% | 15% | Vitest + testcontainers + msw | API route handlers against real Postgres; Upstash Redis test env; Cloud Vision mocked via msw | < 1s/test |
| Contract | — | — | Not required for MVP; revisit if external API surface expands | — | < 500ms/test |
| E2E | 10% | 5% | Playwright | Full user journeys: view prompt, submit contribution, share page, admin moderation queue | < 30s/test |

**Anti-pattern rule:** If E2E tests exceed 20% of total test count at any sprint review, escalate immediately and decompose E2E scenarios into integration tests.

---

## 4. Quality Gates

| Gate | CI Stage | Criteria | Blocker? | Enforcement |
|------|----------|----------|----------|-------------|
| G1 | Pre-commit | ESLint + Prettier pass; `tsc --noEmit` zero errors | Yes | Husky pre-commit hook via lint-staged |
| G2 | Pre-push | All unit + component tests pass; line coverage >= 80% on changed files (`vitest --coverage --changed`) | Yes | Husky pre-push hook |
| G3 | PR Build | Full unit suite passes; integration tests pass against testcontainers DB; zero new ESLint errors; `npm audit --audit-level=high` clean; bundle size JS < 200KB gzipped | Yes | GitHub Actions required check |
| G4 | PR Review | One peer approval; no open P0/P1 bugs linked to the PR diff; CodeQL SAST shows zero new HIGH findings | Yes | GitHub branch protection |
| G5 | Merge to Main | Full Playwright E2E suite passes on Vercel Preview URL (Chrome desktop + Safari mobile viewports); axe-core scan reports zero critical violations | Yes | GitHub Actions post-merge check |
| G6 | Staging Deploy | Lighthouse CI: Performance >= 90, Accessibility >= 90, Best Practices >= 90, SEO >= 90; smoke tests pass (health, GET /api/prompts/today, session cookie issuance) | Yes | Vercel deployment gate |
| G7 | Production Deploy | First 5 minutes of traffic: 5xx rate < 0.5%; nightly composite cron dry-run passes; rollback plan verified via Vercel instant rollback | Yes | Manual approval + automated metric gate |

---

## 5. Automation Framework Selection

| Test Level | Framework | Alternatives Considered | Justification |
|-----------|-----------|------------------------|---------------|
| Unit + Component | **Vitest** | Jest, Bun test | Vitest is native to the Vite/Next.js 15 toolchain, shares the app's tsconfig, and runs in parallel with zero transform configuration. Jest requires heavier ESM/App Router transform setup. Bun test lacks mature snapshot and diff-coverage tooling. Vitest: >13k GitHub stars, weekly releases, first-class TypeScript support. |
| Integration | **Vitest + testcontainers-node + msw** | Supertest + Jest + Docker Compose, Playwright API mode | testcontainers spins a real Postgres-compatible instance per suite without a persistent Docker Compose file, keeping CI stateless. msw intercepts Cloud Vision and Vercel Blob HTTP calls at the network layer without module patching. Playwright API mode adds E2E-tier overhead to what are service-boundary tests. testcontainers requires Docker in CI, which is already present per the phase3 DevOps plan. |
| E2E | **Playwright** | Cypress, Selenium WebDriver | Playwright supports mobile viewport emulation (critical for Fabric.js canvas testing), runs in parallel across Chromium, Firefox, and WebKit from one test file, and natively injects Vercel Preview URLs. Cypress lacks true multi-browser parallelism and has limited mobile canvas interaction support. Selenium requires separate driver management with higher maintenance cost. Playwright: >65k GitHub stars, Microsoft-maintained, active release cadence. |
| Performance | **Lighthouse CI** | k6, WebPageTest API | Lighthouse CI integrates directly with Vercel Preview URLs, produces structured JSON assertions for Core Web Vitals, and covers accessibility and SEO in the same pass. k6 is retained as a supplemental load-test tool for the composite pipeline (Sprint 4) but does not measure frontend performance budgets. |
| Accessibility | **axe-core via @axe-core/playwright** | Pa11y, IBM Equal Access Checker | axe-core runs embedded in the Playwright E2E pass, meaning no extra CI jobs. Pa11y requires a separate CLI invocation and does not integrate with component-level assertions. axe-core covers WCAG 2.1 AA, which aligns with the UX design accessibility requirements from phase2. |

---

## 6. Coverage Requirements

| Module | Line Min | Branch Min | Critical Path | New Code Min |
|--------|----------|------------|---------------|-------------|
| `lib/composite-pipeline` (Sharp orchestration, cron handler, advisory lock) | 85% | 80% | 100% | 90% |
| `lib/moderation` (Cloud Vision adapter, threshold logic, manual queue) | 85% | 80% | 100% | 90% |
| `lib/session` (cookie issuance, middleware, idempotency key generation) | 85% | 80% | 100% | 90% |
| `lib/rate-limit` (Upstash sliding window wrapper) | 80% | 75% | 100% | 90% |
| `app/api/contributions` (route handler, validation, idempotency) | 80% | 75% | 100% | 90% |
| `app/api/prompts` (today + history endpoints) | 80% | 75% | 100% | 90% |
| `components/creation-tool` (SimpleMode + AdvancedMode/Fabric.js canvas) | 80% | 75% | 100% | 90% |
| `components/mosaic-viewer` (daily composite display) | 80% | 75% | — | 90% |
| `app/share/[id]` (OG image generation, share page meta) | 80% | 75% | 100% | 90% |
| Admin endpoints + panel | 80% | 75% | — | 90% |
| `drizzle/` schema + migrations | N/A (SQL) | N/A | Migration idempotency verified via integration suite | — |

Coverage is enforced by Vitest's v8 provider. The diff-coverage check at G2 enforces the 90% new-code threshold on every PR using `vitest run --coverage --changed`.

---

## 7. Test Data Management

| Aspect | Strategy | Tool | Rules |
|--------|----------|------|-------|
| Generation | Factory functions returning typed objects matching Drizzle schema | Custom factory module at `test/factories/` (prompts, contributions, sessions, composites) | No production data ever used in any test environment |
| Fixtures | Version-controlled SQL seed files for integration suite | testcontainers init scripts at `test/fixtures/seed.sql` | Seed applied once per container lifecycle; each test resets state via transaction rollback |
| Masking | All test data is synthetic; no masking pipeline required at MVP | — | Factories must never embed real email addresses, real IP addresses, or identifiable PII |
| Cleanup | Each integration test runs inside a DB transaction rolled back in `afterEach` | Vitest lifecycle hooks | No orphaned rows; testcontainers container destroyed after the full suite |
| Isolation | Unit: full mocks (no DB, no network). Integration: testcontainers Postgres + msw. E2E: Neon branch per PR | msw for HTTP; Neon branching for E2E | Tests must not share mutable state; no `describe`-level DB mutations without transaction wrapping |
| Cloud Vision mock | msw handler at `test/mocks/cloud-vision.ts` returning configurable SafeSearch scores | msw | Required scenarios: all-safe, adult=LIKELY, violence=POSSIBLE (boundary), API timeout (503) |
| Redis mock | `@upstash/redis` vi.mock for unit; real Upstash test environment for integration | Vitest module mocking | Rate limit counters reset between tests via `afterEach` flush |

---

## 8. Environment Strategy

| Environment | Purpose | Data Source | Refresh Cycle | Promotion Gate |
|-------------|---------|-------------|---------------|----------------|
| Local | Developer unit + component testing | Seed factories + Neon dev branch | On demand (`npm run db:seed`) | Lint + unit tests pass (G1 + G2) |
| CI | Automated unit + integration tests | testcontainers ephemeral Postgres + msw (stateless) | Per build | All tests pass, coverage thresholds met (G3) |
| Preview (Vercel) | Per-PR E2E + Lighthouse + a11y | Neon branch cloned from staging schema + seed data | Created/destroyed per PR by CI | E2E pass + axe zero critical + Lighthouse >= 90 (G5 + G6) |
| Staging | Pre-production validation + manual exploratory testing | Seed data (no real user content at MVP scale) | Weekly refresh or on-demand | Smoke tests pass, zero open P0/P1 bugs (G6) |
| Production | Live system | Real data | N/A | Canary metrics healthy, rollback plan verified (G7) |

---

## 9. Shift-Left Practices

| Practice | Stage | Tool | Enforcement |
|----------|-------|------|-------------|
| TypeScript strict type check | Pre-commit | `tsc --noEmit` (strict mode) | Husky pre-commit; blocks commit on any type error |
| ESLint + Prettier | Pre-commit | `eslint` + `prettier --check` via lint-staged | Husky pre-commit; runs on changed files only for speed |
| Unit tests (changed files) | Pre-push | `vitest run --changed` | Husky pre-push; target < 60s for typical PR |
| Full unit + integration suite | PR Build | GitHub Actions | Required CI check; blocks merge |
| SAST | PR | GitHub CodeQL (JavaScript/TypeScript) | Required CI check; HIGH findings block merge |
| Dependency vulnerability scan | PR | `npm audit --audit-level=high` + Dependabot | Required CI check; HIGH/CRITICAL CVEs block merge |
| E2E + a11y | Post-merge to main | Playwright on Vercel Preview | Required post-merge check before staging promotion |
| Lighthouse CI | Post-merge to main | `lhci autorun` against Preview URL | Required; scores < 90 on Performance or Accessibility block staging promotion |

---

## 10. Risk-Based Test Prioritization

| Risk Area | Impact | Likelihood | Test Investment | Rationale |
|-----------|--------|-----------|----------------|-----------|
| Nightly composite pipeline failure | Critical — zero mosaic visible to all users next morning | Medium (cron + Sharp + Blob + DB all in sequence) | Unit: full pipeline logic, idempotency, advisory lock; Integration: end-to-end pipeline with real DB + mocked Blob; E2E: admin manual re-trigger; load test with 500+ contributions (k6, Sprint 4) | Single point of failure for the core product value; must also test the 300s Vercel Pro function timeout headroom |
| Mobile drawing canvas (Fabric.js) | High — primary contribution path broken on mobile | High (canvas APIs vary across mobile browsers) | Component tests for tool state machines; Playwright E2E on 375px (iPhone SE) and 390px (iPhone 15) viewports; real-device exploratory session in Sprint 2 | Make-or-break for user engagement per phase3 critical path |
| Content moderation bypass | Critical — harmful content in public mosaic | Low-Medium (Cloud Vision reliable but not comprehensive) | Integration tests with full range of SafeSearch responses; E2E for manual moderation queue workflow; boundary test for POSSIBLE threshold behavior | Reputational and legal risk; zero tolerance for bypass in production |
| Session management (anonymous-first) | High — broken sessions prevent contribution or allow duplicate submissions | Medium (serverless cold starts affect cookie middleware timing) | Unit: session creation, validation, expiry; Integration: full request lifecycle with cookie propagation; E2E: cross-request session persistence and `UNIQUE(prompt_id, session_id)` idempotency | Foundation for idempotent contributions; failure affects every user |
| Rate limiting (Upstash sliding window) | Medium — abuse exhausts Vercel function budget; degrades service | Medium (anonymous endpoints are exposed targets) | Unit: sliding window at-limit, over-limit, and reset boundaries; Integration: real Upstash test env; E2E: verify 429 response and Retry-After header | Cost containment at ~$26/month MVP budget; anonymous surface is the highest-risk attack vector |
| OG image generation for share pages | Medium — every share is a user acquisition event | Low-Medium (Sharp + Vercel Blob in sequence) | Integration: OG route handler with real Sharp rendering; E2E: share URL produces correct og:image meta tag; visual regression snapshot | Viral acquisition channel; silent failure has high opportunity cost |
| Vercel function timeout on large composite | Medium — 500+ contributions may breach time budget | Low at MVP scale | k6 load test simulating 500-contribution composite job; assert completion within 240s (60s headroom below 300s Pro limit) | Identified risk in phase2; must be validated before Sprint 4 launch |

---

## 11. Flaky Test Policy

- Detection: any test failing in >= 2% of CI runs over a rolling 7-day window is flagged automatically via GitHub Actions test reporter annotations.
- Quarantine: flagged tests are moved to a `describe.skip` block with a `// FLAKY: <issue-link>` comment within 24 hours of detection. They run in a separate nightly job that does not block the main pipeline.
- Resolution SLA: quarantined tests must be fixed or deleted within one sprint (2 weeks). Tests surviving two sprints in quarantine are deleted and logged as test debt.
- Zero tolerance: no flaky test may block a PR merge once quarantined.
- Mosaic-specific flaky-test triggers to monitor: Playwright canvas interactions (add explicit `waitFor` for Fabric.js ready state); testcontainers startup timing (use `waitForPort` readiness probe, not fixed sleep); Upstash test environment counter state leakage between suites (explicit flush in `afterEach`).

---

## 12. Defect Classification

| Severity | Definition | SLA Response | SLA Fix | Blocks Release? |
|----------|-----------|-------------|---------|-----------------|
| P0 — Critical | Nightly composite did not generate and mosaic is absent; data loss; site completely down | 15 min | 4h | Yes |
| P1 — Major | Contribution submission fails for all users; confirmed moderation bypass; session cookies not issued; rate limiting not enforced | 1h | 24h | Yes |
| P2 — Minor | Drawing canvas broken on one specific browser or device; OG image absent on share page; admin panel feature non-functional | 4h | 1 sprint | No |
| P3 — Trivial | Visual misalignment; copy error; non-blocking console warning; Lighthouse score regresses to 85-89 | 1 day | Backlog | No |

---

## 13. Definition of Done

A feature is complete when all of the following hold:

- Unit test line coverage >= 80% and branch coverage >= 75% on all files touched by the feature; critical paths at 100%.
- New code coverage >= 90% enforced by diff-coverage at G2.
- All integration tests pass for affected API routes and service boundaries.
- E2E scenarios cover the full user journey for the feature on both desktop (1280px) and mobile (375px) Playwright viewports.
- Lighthouse CI scores >= 90 on Performance, Accessibility, Best Practices, and SEO for pages affected by the feature.
- axe-core reports zero critical or serious violations on affected pages.
- Zero open P0 or P1 bugs linked to the feature.
- TypeScript strict mode: zero type errors (`tsc --noEmit`).
- ESLint: zero new errors or warnings introduced.

---

## 14. Open Questions

| # | Question | Priority | Blocking? | Default if Unanswered |
|---|---------|----------|-----------|----------------------|
| OQ-1 | Will the Neon branch-per-PR workflow stay within Neon free-tier branch limits, or does it require a paid plan? | High | Yes — affects Preview environment strategy | Fall back to a single shared staging DB with transaction-isolated test runs per PR |
| OQ-2 | Is a dedicated Upstash test instance available, or must integration tests use a local Redis emulator? | Medium | No | Use `ioredis-mock` for integration; document that sliding-window boundary behavior may differ from production Upstash |
| OQ-3 | Has the team agreed on a mobile device testing matrix for the drawing canvas (real devices vs. BrowserStack vs. Playwright emulation only)? | High | No | Playwright mobile emulation only; schedule one real-device exploratory session as a Sprint 2 QA task |
| OQ-4 | Is a separate Cloud Vision billing project available for CI, or will automated integration tests consume production API quota? | High | Yes — affects moderation test strategy | Mock Cloud Vision in all automated tests via msw; never call the real API in CI |
| OQ-5 | Is k6 load testing in scope for Sprint 4 or deferred post-launch? | Medium | No | Include as best-effort Sprint 4 task; composite pipeline load test is the minimum viable scope |
