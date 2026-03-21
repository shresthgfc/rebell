# Code Review — Mosaic (Architecture Review)

## 1. Document Info
- Date: 2026-03-21
- Source: phase3-synthesis.md, phase4-synthesis.md, phase3-backend-developer.md
- Reviewer: Code Reviewer Sub-Agent
- Status: Under Review

---

## 2. SOLID Compliance

| Principle | Verdict | Issues Found | Components Affected | Recommendation |
|-----------|---------|--------------|---------------------|----------------|
| Single Responsibility | Minor Violation | `ContributionService.submit()` owns validation, moderation, image rendering, Blob upload, DB write, and Redis increment — 6 distinct reasons to change | ContributionService | Extract `ImageRenderingService` for Sharp operations; submit() should orchestrate, not implement each step |
| Open/Closed | Minor Violation | `content_type` branching (`emoji` / `color` / `drawing`) is inline logic; adding a new type requires modifying submit() | ContributionService, CompositeService | Introduce a `ContentTypeHandler` strategy interface with three concrete implementations; submit() dispatches to handler |
| Liskov Substitution | Pass | No inheritance hierarchies identified in service layer; AppError subclasses extend correctly without changing base contracts | All services | N/A |
| Interface Segregation | Pass | Five focused interfaces, each with 2-4 methods; no client is forced to depend on unused methods | All services | N/A |
| Dependency Inversion | Minor Violation | Service interfaces are defined but no explicit injection mechanism is described; concrete instantiation likely happens at call site in route handlers | All services | Use a lightweight DI pattern (constructor injection or a service-locator module) so route handlers receive interface types, not concrete classes — critical for mocking in tests |

---

## 3. Security Findings

Findings BLK-001 through BLK-004 are confirmed from Phase 4. Two additional concerns arise from the implementation plan:

| ID | Severity | Finding | Location | Impact | Recommended Fix | Blocking? |
|----|----------|---------|----------|--------|----------------|-----------|
| SEC-001 | High | CSP `unsafe-inline` for `script-src` (BLK-001 carry-over) | Middleware | XSS mitigation negated | Nonce-based CSP via Next.js middleware | Yes |
| SEC-002 | High | Static admin bearer token cannot be rotated without redeployment (BLK-002 carry-over) | Admin API routes | Full admin access with a leaked secret | Short-lived JWTs + IP allowlist | Yes |
| SEC-003 | Medium | `z.string().max(700000)` validates base64 length at the Zod layer, but there is no Content-Length gate before the request body is read into memory (NB-001 carry-over) | `ContributionService.submit()` | A 700KB allocation per concurrent request; DoS under modest load | Reject requests where `Content-Length > 700000` in middleware before body parse | No |
| SEC-004 | Medium | Advisory lock key uses `hash of date string` — implementation detail unspecified; a weak hash (e.g., CRC32) causes lock collisions across dates | `CompositeService.generate()` | Two cron runs could simultaneously generate composites for different dates if hashes collide | Use `hashtext(date_string)` (PostgreSQL built-in) or a namespaced bigint key | No |
| SEC-005 | Low | Session farming bypasses per-session rate limit (NB-002 carry-over) | Rate limiting layer | Automated abuse via session churn | Add IP-level rate limit as secondary gate in middleware | No |

### Security Summary
- Critical: 0 — High: 2 — Medium: 2 — Low: 1
- Blocking security issues: Yes (SEC-001, SEC-002 inherited from Phase 4)

---

## 4. Performance Anti-Patterns

| ID | Anti-Pattern | Location | Estimated Impact | Recommended Fix | Blocking? |
|----|-------------|----------|-----------------|----------------|-----------|
| PERF-001 | Unbounded fetch in `getByPromptId()` — no pagination or LIMIT clause specified | `ContributionService` | At 500+ contributions per day, full table scan per composite run; memory spike proportional to row count | Add `LIMIT` / cursor pagination for list queries; composite pipeline should stream or batch-fetch tiles | No |
| PERF-002 | Sequential Sharp tile downloads in composite generation — step 6 downloads each tile one at a time | `CompositeService.generate()` | 500 tiles x ~50ms download = ~25s of serial I/O against the 60s cron budget | Use `Promise.all()` with a concurrency limiter (e.g., p-limit, 10 concurrent) to parallelize Blob downloads | No |
| PERF-003 | Sharp composite pipeline holds all tile buffers in memory simultaneously before writing | `CompositeService.generate()` | 500 tiles x 200x200 RGBA = ~80MB peak heap; Vercel functions have a 1GB limit but this is wasteful and risks OOM on large days | Process tiles in row batches; release buffers after each Sharp `.composite()` call | No |
| PERF-004 | Redis counter `contribution:count:{date}` is correct, but `getTodayPrompt()` cache TTL "until midnight UTC" requires calculating a dynamic TTL on every cache miss — if not done precisely, prompt can serve stale data into the next day | `PromptService.getTodayPrompt()` | Wrong prompt served if TTL is rounded down incorrectly | Compute TTL as `secondsUntilMidnightUTC()` explicitly; add an integration test that crosses midnight | No |

### Performance Summary
- NFR targets at risk: Composite generation 60s budget (PERF-002, PERF-003 combined could consume 35–40s leaving little margin)
- Blocking performance issues: No (all within fixable range before launch)

---

## 5. Technical Debt Inventory

| ID | Category | Description | Severity | Cost to Fix | Recommendation | Blocking? |
|----|----------|-----------|----------|------------|----------------|-----------|
| TD-001 | DD | `ContributionService.submit()` is a 9-step mega-method; content-type strategy is inline | High | Medium (2d) | Extract `ContentTypeHandler` strategy; see OCP finding | No |
| TD-002 | CD | No DI mechanism defined; concrete service instantiation in route handlers makes testing brittle | Medium | Low (1d) | Constructor injection + a `createServices()` factory module | No |
| TD-003 | TD | Advisory lock hash implementation unspecified; no test for concurrent cron invocations | Medium | Low (1d) | Integration test: two concurrent calls to `generate()` for same date must produce exactly one composite | No |
| TD-004 | CD | `z.string().max(700000)` magic number for base64 limit; comment says "~500KB" but no named constant | Low | Low (<1d) | `const MAX_DRAWING_BASE64_BYTES = 700_000; // 500KB binary + ~40% base64 overhead` | No |
| TD-005 | ID | Prompt activation is described as "part of composite cron" — coupling two independent concerns into one cron job | Medium | Low (1d) | Separate cron functions or a clearly named internal step; document the dependency explicitly | No |
| TD-006 | DOC | `pg_advisory_lock` key derivation and Sharp buffer lifecycle are undocumented | Low | Low (<1d) | Inline comments in `CompositeService.generate()` before code is written | No |

### Debt Summary
- Total items: 6 — Blocking debt items: 0 — Estimated total fix cost: ~6 person-days

---

## 6. Quality Rubric (1–5)

| Dimension | Score | Justification |
|-----------|-------|--------------|
| Architecture | 4/5 | Clean separation of layers, well-scoped interfaces. Docked one point for SRP violation in ContributionService and absent DIP mechanism. |
| Security | 3/5 | Two High findings (CSP, static admin token) from Phase 4 remain unresolved. No new Critical issues found, but SEC-004 (lock collision) is an undocumented gap. |
| Performance | 3/5 | Sequential tile downloads and full-buffer holding in Sharp put the 60s composite budget at real risk. No pagination on list queries is an unbounded fetch waiting for a bad day. |
| Testability | 4/5 | Zod validation and modular interface design make unit testing straightforward. Docked one point for missing DI pattern, which forces test doubles to monkey-patch modules. |
| Maintainability | 4/5 | Strong error hierarchy, consistent response shape, typed interfaces. Inline content-type branching and the mega-method in submit() are the main maintenance risks. |

---

## 7. Blocking Findings (Must Fix Before Launch)

| # | Finding | Category | Severity | Location | Required Action |
|---|---------|----------|----------|----------|----------------|
| 1 | CSP `unsafe-inline` for `script-src` (SEC-001 / BLK-001) | SEC | High | Next.js middleware | Implement nonce-based CSP |
| 2 | Static admin bearer token (SEC-002 / BLK-002) | SEC | High | Admin API routes | Replace with short-lived JWTs + IP allowlist |
| 3 | Success color #00C48C fails WCAG contrast (BLK-003) | SEC/A11y | High | Design tokens | Change to #008A5E |
| 4 | Secondary button #FF6B35 fails small text contrast (BLK-004) | SEC/A11y | High | Design tokens | Darken to #E55A20 |

---

## 8. Non-Blocking Findings (Recommended Improvements)

| # | Finding | Category | Priority | Location | Suggested Action |
|---|---------|----------|----------|----------|-----------------|
| 1 | ContributionService SRP violation (mega-method) | ARCH | High | contribution.service.ts | Extract ImageRenderingService; submit() orchestrates |
| 2 | Content-type branching violates OCP | ARCH | Medium | contribution.service.ts | ContentTypeHandler strategy pattern |
| 3 | No DI mechanism; concrete instantiation in routes | ARCH | Medium | All service consumers | Constructor injection factory |
| 4 | Sequential tile downloads in composite gen (PERF-002) | PERF | High | composite.service.ts | p-limit concurrency wrapper around Blob downloads |
| 5 | All tile buffers held in memory simultaneously (PERF-003) | PERF | High | composite.service.ts | Row-batched Sharp compositing |
| 6 | Unbounded `getByPromptId()` (PERF-001) | PERF | Medium | contribution.service.ts | Add LIMIT / cursor pagination |
| 7 | Advisory lock key hash unspecified (SEC-004) | SEC | Medium | composite.service.ts | Use PostgreSQL hashtext() |
| 8 | No Content-Length gate before body parse (SEC-003) | SEC | Medium | Middleware | Reject oversized requests pre-parse |
| 9 | Magic number 700000 with no named constant (TD-004) | DEBT | Low | contribution.service.ts | Named constant with comment |
| 10 | Prompt activation coupled to composite cron (TD-005) | DEBT | Medium | cron/composite/route.ts | Separate or clearly document coupling |

---

## 9. Review Verdict

- **Verdict:** Rejected
- **Conditions:** The four blocking findings (SEC-001 through BLK-004) — two security issues and two WCAG contrast failures — must be resolved before any production deployment. All four were identified in Phase 4 and carry forward unresolved. No new Critical findings were discovered in this review.
- **Next review:** Re-review triggered when all four blocking findings are closed and verified in the staging environment (G6 gate).

---

## 10. Open Questions

| # | Question | Priority | Blocking? | Default if Unanswered |
|---|---------|----------|-----------|----------------------|
| 1 | Which hash function is used for `pg_advisory_lock` key derivation in CompositeService? | High | No | Assume PostgreSQL `hashtext()`; document before implementation |
| 2 | Is there a defined maximum number of contributions per day (for Sharp memory budgeting)? | Medium | No | Assume 1000 max; plan composite batching accordingly |
| 3 | What is the fallback behavior if Cloud Vision is unavailable during submission? | Medium | No | Fail open (approve + flag for manual review) or fail closed (reject submission)? Must be an explicit product decision |
| 4 | Does the session cleanup cron hard-delete session rows, or soft-delete for audit trail? | Low | No | Soft-delete recommended for GDPR right-to-erasure audit; confirm with product |
