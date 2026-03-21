# Release Plan — Mosaic

## 1. Document Info
- **Date:** 2026-03-21
- **Source:** phase3-synthesis.md, phase4-synthesis.md, phase3-devops-engineer.md
- **Author:** Release Manager Sub-Agent
- **Status:** Draft

## 2. Executive Summary

Mosaic ships as a tag-triggered Vercel production deployment promoted from Preview through Staging. Four blocking QA findings (BLK-001 through BLK-004) must be resolved before go/no-go is granted; no release is approved with open blocking items. The nightly composite cron pipeline, admin panel, and advanced drawing mode are flag-gated to enable safe partial rollout. Vercel's instant deployment rollback provides sub-60-second recovery, meeting the 5-minute SLA with margin.

---

## 3. Release Strategy

- **Method:** Blue-Green via Vercel deployment promotion (Preview -> Staging -> Production tag)
- **Justification:** Vercel's immutable deployment model gives instant switch-back at the LB layer. No stateful server fleet to drain. Single-command rollback satisfies the < 5-minute SLA. Canary by percentage is not natively supported on Vercel Pro; staged feature-flag rollout serves as the canary mechanism for new features.
- **Deployment window:** Sprint 4 completion, scheduled for a Tuesday 10:00 UTC (low-traffic period)
- **Duration estimate:** ~30 minutes from tag push to G7 smoke-test pass
- **Environments:** PR branch (Preview) -> `main` push (Staging @ staging.mosaic.app) -> `v*` tag (Production @ mosaic.app)

---

## 4. Go/No-Go Checklist [GT]

| # | Category | Check Item | Pass Criterion | Status | Verified By | Blocking? |
|---|----------|-----------|---------------|--------|-------------|-----------|
| G1 | Quality | All CI checks passing | 100% pass: lint, tsc, unit tests, build | Pending | CI pipeline | Yes |
| G2 | Quality | Test coverage met | ≥ 80% unit (85% on composite + moderation) | Pending | Codecov report | Yes |
| G3 | Quality | Bundle size | Initial JS ≤ 200 KB gzipped | Pending | size-limit CI | Yes |
| G4 | Quality | Code review approved | Score ≥ 7/10, zero blocking findings | Pending | Code Reviewer | Yes |
| G5 | Security | BLK-001 resolved | Nonce-based CSP active, `unsafe-inline` removed | Pending | Security scan | Yes |
| G6 | Security | BLK-002 resolved | Short-lived JWT admin auth + IP allowlist in middleware | Pending | Security scan | Yes |
| G7 | Security | Dependency audit | Zero Critical/High CVEs (`npm audit`) | Pending | CI npm audit | Yes |
| G8 | Accessibility | BLK-003 resolved | Success color ≥ 4.5:1 contrast (#008A5E or equivalent) | Pending | axe-core / manual | Yes |
| G9 | Accessibility | BLK-004 resolved | Secondary button contrast ≥ 4.5:1 at all text sizes | Pending | axe-core / manual | Yes |
| G10 | Performance | Core Web Vitals | LCP < 2.5s, CLS < 0.1, INP < 100ms at p75 | Pending | Lighthouse CI | Yes |
| G11 | Performance | API latency | GET p95 < 150ms, POST p95 < 300ms under load | Pending | k6 load test | Yes |
| G12 | Performance | Composite pipeline | 500-tile generation < 60s in staging | Pending | k6 + cron dry-run | Yes |
| G13 | Data | Migrations verified | Up + down migrations tested on Neon staging branch | Pending | Database Engineer | Yes |
| G14 | Data | Seeding plan ready | Seed script produces ≥ 1 valid composite for Day 1 | Pending | Database Engineer | Yes |
| G15 | Data | Backup / PITR | Neon PITR enabled, 7-day retention confirmed | Pending | DevOps | Yes |
| G16 | Operations | Rollback tested | Instant rollback executed in staging in < 60s | Pending | DevOps | Yes |
| G17 | Operations | Monitoring active | Health check, cron alert, error-rate alert all firing in staging | Pending | DevOps | Yes |
| G18 | Operations | On-call set | Named primary + secondary for 48h post-launch | Pending | Engineering Manager | Yes |
| G19 | Documentation | Runbooks complete | Deployment runbook, cron re-trigger runbook, rollback runbook published | Pending | Technical Writer | Yes |
| G20 | Stakeholders | Notifications sent | Launch timeline communicated to all stakeholder groups | Pending | Release Manager | Yes |
| G21 | Feature flags | All flags default-off in prod | Composite pipeline, advanced drawing, admin panel flags default = false | Pending | Release Manager | Yes |

### Go/No-Go Decision
- **Decision:** No-Go (pending — BLK-001 through BLK-004 unresolved as of plan date)
- **Conditions:** All 21 items must pass. BLK-001–004 are the critical path.
- **Decision maker:** Release Manager + Engineering Manager
- **Decision date:** To be confirmed at Sprint 4 sign-off

---

## 5. Rollback Procedure [RB]

### Automated Rollback — Vercel Deployment

| Phase | Max Duration | Mechanism | Verification | Owner |
|-------|-------------|-----------|-------------|-------|
| Detection | < 60s | G7 gate: `5xx > 0.5% for 5 min` alert OR `/api/health` returning 503 | Vercel Analytics alert fires | Monitoring system |
| Decision | < 30s | On-call engineer acknowledges OR auto-rollback rule fires on critical threshold | Alert acknowledged in Slack | On-call engineer |
| Execution | < 60s | `vercel rollback [deployment-url] --token $VERCEL_TOKEN` — single command | Vercel returns previous immutable deployment | Deployment system |
| Verification | < 60s | `/api/health` returns 200; automated smoke test (GET `/`, GET `/api/prompts/today`) | Smoke test suite passes | CI/CD pipeline |
| **Total** | **< 3.5 min** | Well within 5-minute SLA | | |

### Rollback Triggers (Auto)
| Trigger | Threshold | Action |
|---------|-----------|--------|
| 5xx error rate | > 0.5% sustained 5 min | Page on-call + log event; manual confirm to rollback |
| `/api/health` failure | 3 consecutive failures (30s interval) | Immediate auto-rollback |
| Composite cron failure | Any failure on launch night | Slack alert; manual re-trigger via admin endpoint |
| Vercel function timeout rate | > 2% in 5 min | Page on-call for investigation |

### Manual Rollback Commands
```bash
# Application rollback (< 60s)
vercel rollback --token $VERCEL_TOKEN

# Database migration rollback — only if migration was applied
npx drizzle-kit migrate:down --config drizzle.config.ts

# Redis cache flush (targeted, not full flush)
# Flush only today's composite keys to force DB-backed rebuild
redis-cli -u $UPSTASH_REDIS_REST_URL DEL composite:$(date +%Y-%m-%d) prompts:today
```

- **Who can trigger:** On-call engineer, Engineering Manager, Release Manager
- **When to use manual over auto:** Database or Redis issues that automated health check cannot distinguish from transient errors

### Rollback Testing Schedule
- **Last tested:** Must be completed during Sprint 4 staging deployment — not yet run
- **Required:** Full rollback drill in staging before go/no-go is granted (G16)
- **Next scheduled:** Sprint 4 final week, staging environment
- **Monthly drill:** First Tuesday of each month post-launch

---

## 6. Feature Flag Plan [FLG]

| Flag Name | Feature | Owner | Default (Prod) | Rollout Plan | Expiry Date | Cleanup Sprint |
|-----------|---------|-------|---------------|-------------|------------|---------------|
| `ff_composite_pipeline_20260321` | Nightly composite cron generation | Backend Lead | OFF | Enable after first manual run succeeds; 100% Day 2 | 2026-04-21 | Sprint 5 |
| `ff_advanced_drawing_20260321` | Fabric.js advanced canvas mode | Frontend Lead | OFF | Enable at 10% Week 1; 100% if no JS errors | 2026-04-21 | Sprint 5 |
| `ff_admin_panel_20260321` | Admin moderation + manual re-trigger UI | Engineering Manager | OFF | Enable for admin IPs only on Day 1; no public rollout | 2026-04-21 | Sprint 5 |

### Flag Lifecycle Tracking
| Flag | Created | Testing (staging) | Canary | GA | Cleanup | Archived |
|------|---------|------------------|--------|-----|---------|----------|
| `ff_composite_pipeline_20260321` | Sprint 3 | Sprint 3–4 | Day 2 post-launch | Day 3 if stable | Sprint 5 | Sprint 5 end |
| `ff_advanced_drawing_20260321` | Sprint 2 | Sprint 2–4 | Week 1 (10%) | Week 2 | Sprint 5 | Sprint 5 end |
| `ff_admin_panel_20260321` | Sprint 4 | Sprint 4 | Admin-only | N/A (internal) | Sprint 5 | Sprint 5 end |

All flags must have an owner and expiry. Any flag not archived by 2026-04-21 triggers an automatic review ticket.

---

## 7. Deployment Strategy — Promotion Chain

```
Developer pushes PR
  -> GitHub Actions: lint + tsc + unit tests + build
  -> Vercel: Preview deployment (*.vercel.app)
  -> QA runs Playwright E2E on Preview URL
  -> PR merged to main
  -> GitHub Actions: full suite
  -> Vercel: Staging deployment (staging.mosaic.app)
  -> Lighthouse CI, k6 load test, smoke tests, axe-core
  -> All G1–G21 gates pass
  -> Release Manager cuts v1.0.0 tag
  -> Vercel: Production deployment (mosaic.app)
  -> G7 gate (5xx < 0.5% for 5 min)
  -> Go-live confirmed
```

Canary note: Vercel Pro does not support percentage-based traffic splitting natively. Feature flags (`ff_composite_pipeline`, `ff_advanced_drawing`) serve as the functional canary mechanism — new behavior is enabled incrementally and can be turned off in under 30 seconds via the flag service without a redeployment.

---

## 8. Post-Launch Monitoring [MON]

### Key Metrics
| Metric | Baseline | Warning | Critical | Dashboard | Alert Channel |
|--------|----------|---------|----------|-----------|--------------|
| 5xx error rate | < 0.1% | > 0.5% | > 2% | Vercel Analytics | Slack #mosaic-alerts |
| API p95 latency (GET) | < 150ms | > 300ms | > 1s | Vercel Speed Insights | Slack #mosaic-alerts |
| API p95 latency (POST) | < 300ms | > 600ms | > 2s | Vercel Speed Insights | Slack #mosaic-alerts |
| `/api/health` status | 200 | 503 once | 503 x3 in 90s | Custom dashboard | PagerDuty |
| Composite cron success | 1 run/day | Delayed > 15 min | Failed | Vercel Logs | Slack #mosaic-alerts |
| Contribution count | TBD | < 10 by noon | 0 by noon | Redis counter dashboard | Slack #mosaic-ops |
| Blob storage usage | 0 | > 80% plan limit | > 95% | Vercel dashboard | Email |

### First 24-Hour Monitoring Checklist
- [ ] 00:00–00:05 UTC: Composite cron fires; verify success log and Blob URL generated
- [ ] 00:30 UTC: Confirm share page OG image renders for today's composite
- [ ] 01:00 UTC: Check error rate < 0.5%, `/api/health` = 200
- [ ] 06:00 UTC: Review contribution count for early-morning cohort
- [ ] 12:00 UTC: Contribution count check (< 10 triggers investigation)
- [ ] 18:00 UTC: Review Vercel Analytics — LCP, CLS, INP vs. budgets
- [ ] 23:30 UTC: Confirm Day 2 composite cron is scheduled; check Upstash quota remaining

### Monitoring Windows
| Window | Duration | Focus | Escalation |
|--------|----------|-------|-----------|
| Immediate | 0–1 hour | Error rate, health checks, first contributions | Auto-rollback on critical threshold |
| Short-term | 1–24 hours | Cron success, user behavior, share rate, performance | On-call engineer |
| Medium-term | 1–7 days | Contribution growth, unique visitors, support tickets, Upstash quota | Engineering lead review |

### On-Call Schedule (48h post-launch)
| Shift | Time (UTC) | Primary | Secondary | Escalation |
|-------|-----------|---------|-----------|-----------|
| Launch | T+0 to T+8h | Release Manager | Engineering Manager | CTO |
| Overnight | T+8h to T+24h | On-call Engineer (primary) | Engineering Manager | Release Manager |
| Day 2 | T+24h to T+48h | On-call Engineer (secondary) | Engineering Manager | Release Manager |

---

## 9. Success Metrics [MON]

| Metric | Day 1 Target | Week 1 Target | Month 1 Target | Data Source | Owner |
|--------|-------------|--------------|---------------|------------|-------|
| Unique visitors | ≥ 100 | ≥ 500 | ≥ 2,000 | Vercel Analytics | Product |
| Contributions submitted | ≥ 20 | ≥ 200 | ≥ 1,000 | PostgreSQL `contributions` table | Engineering |
| Composite generation success rate | 100% | 100% | ≥ 99% | Cron success log | DevOps |
| Share events (share page loads) | ≥ 5 | ≥ 50 | ≥ 300 | Vercel Analytics referrer data | Product |
| API error rate | < 0.5% | < 0.5% | < 0.1% | Vercel Analytics | Engineering |
| LCP p75 | < 2.5s | < 2.5s | < 2.5s | Vercel Speed Insights | Frontend Lead |
| Zero P0 incidents | 0 | 0 | 0 | Incident log | Engineering Manager |

### Success Criteria
- **Launch is successful if:** Composite cron succeeds on Night 1, error rate < 0.5%, ≥ 20 contributions on Day 1, zero rollback events
- **Launch requires intervention if:** Cron delayed > 15 min, error rate 0.5–2%, contribution count < 10 by noon
- **Launch is rolled back if:** Health check fails 3x, error rate > 2% sustained, composite pipeline produces corrupt output

---

## 10. Communication Plan [COM]

| Audience | Channel | When | Message | Owner |
|----------|---------|------|---------|-------|
| Engineering | Slack #mosaic-releases | T-24h, T-0, T+1h, T+24h | Technical status, flag states, metrics | Release Manager |
| Stakeholders | Email | T-48h (heads-up), T+24h (summary) | Business summary, Day 1 metrics | Stakeholder Liaison |
| End users | mosaic.app changelog / status page | T+0 (launch), incidents if any | What's new, any degradation notice | Product |
| Support team | Internal wiki | T-24h | FAQ covering contribution limits, canvas issues, session behavior, escalation path | Support Lead |
| On-call | PagerDuty | Auto on critical alert | Incident details, rollback command, runbook link | Monitoring system |

---

## 11. Risk Assessment

| Risk | Likelihood | Impact | Mitigation | Contingency |
|------|-----------|--------|-----------|------------|
| Composite cron fails on Night 1 | Medium | High — no Day 1 mosaic visible | Dry-run in staging same day; manual re-trigger endpoint behind admin flag | Manual composite trigger; display yesterday's seeded composite as placeholder |
| BLK-001/BLK-002 not resolved in Sprint 4 | Low-Medium | High — security blocker, no-go | Prioritize as Sprint 4 P0 tasks; assign dedicated engineer | Delay launch by 1 week; do not release with open security blocking findings |
| Upstash free tier exhausted (10K cmds/day) | Low | Medium — rate limiting breaks | Monitor daily command count; alert at 80% | Upgrade to Upstash Pay-as-you-go (~$0.2/100K cmds); < $5/mo at MVP scale |
| Neon connection pool saturation at launch spike | Low | Medium — DB errors for users | Max pool size configured; Neon serverless scales automatically | Enable Neon connection pooling via PgBouncer mode; reduce pool wait timeout |
| OG image generation slow under traffic | Medium | Medium — poor share card UX | Pre-generate on composite creation; cache in Blob | Fallback to static branded image if generation > 5s |

---

## 12. Open Questions

| # | Question | Priority | Blocking? | Default if Unanswered |
|---|---------|----------|-----------|----------------------|
| OQ-01 | Which engineer is named primary on-call for launch night? | High | Yes | Release blocked until named (G18) |
| OQ-02 | Is the seed script producing a valid composite for Day 1, or does Night 1 cron produce it? | High | Yes | Seed script must produce Day 0 fallback; flag composite cron off until Night 1 completes |
| OQ-03 | What feature flag service is being used (env var, LaunchDarkly, custom)? | Medium | No | Default to environment variable flags in `process.env`; sufficient for MVP scale |
| OQ-04 | Is Vercel Pro plan confirmed and billing active before go/no-go? | Medium | Yes | No production cron support on Hobby plan |
| OQ-05 | Are NB-001 through NB-005 (non-blocking findings) scheduled for Sprint 5? | Low | No | Log as Sprint 5 backlog items; do not block launch |
