# Performance Plan — Mosaic

## 1. Document Info
- Date: 2026-03-21
- Source: phase2-synthesis.md, phase3-synthesis.md
- Engineer: Performance Engineer Sub-Agent
- Status: Draft

## 2. Performance Overview
Mosaic is a low-throughput, high-burst daily creative platform. Normal traffic is modest (~500 contributions/day) but viral spikes are the primary risk vector. The nightly cron composite pipeline is the single most critical performance component: a timeout or OOM kill breaks the entire day's output. All caching TTLs anchor to the 00:00 UTC daily reset cycle, and every SLA maps to either user-perceived wait time or operational reliability of the cron.

---

## 3. SLA Definitions

| ID | Metric | Target | Percentile | Measurement | Alert Warning | Alert Critical | Owner |
|----|--------|--------|-----------|-------------|--------------|----------------|-------|
| SLA-001 | GET /api/prompts/today latency | < 50ms | p50 | k6 + Vercel Analytics | > 40ms | > 50ms | Backend |
| SLA-002 | GET /api/prompts/today latency | < 100ms | p95 | k6 + Vercel Analytics | > 80ms | > 100ms | Backend |
| SLA-003 | GET /api/prompts/today latency | < 200ms | p99 | k6 + Vercel Analytics | > 160ms | > 200ms | Backend |
| SLA-004 | POST /api/contributions latency | < 100ms | p50 | k6 + Vercel Analytics | > 80ms | > 100ms | Backend |
| SLA-005 | POST /api/contributions latency | < 300ms | p95 | k6 + Vercel Analytics | > 240ms | > 300ms | Backend |
| SLA-006 | POST /api/contributions latency | < 500ms | p99 | k6 + Vercel Analytics | > 400ms | > 500ms | Backend |
| SLA-007 | GET /api/composites/today latency | < 50ms | p50 | k6 + Vercel Analytics | > 40ms | > 50ms | Backend |
| SLA-008 | GET /api/composites/today latency | < 150ms | p95 | k6 + Vercel Analytics | > 120ms | > 150ms | Backend |
| SLA-009 | GET /api/composites/today latency | < 300ms | p99 | k6 + Vercel Analytics | > 240ms | > 300ms | Backend |
| SLA-010 | API 5xx error rate | < 1% | — | Vercel Analytics (5xx / total) | > 0.5% | > 1% | Backend |
| SLA-011 | Uptime | 99.9% monthly | — | External uptime monitor (Better Uptime) | < 99.95% | < 99.9% | DevOps |
| SLA-012 | Nightly cron wall-clock time (500 tiles) | < 60s | — | Vercel cron execution logs | > 45s | > 60s or any failure | Backend |
| SLA-013 | Contribution image upload processing | < 2s | p95 | Server-Timing header + Vercel Analytics | > 1.5s | > 2s | Backend |
| SLA-014 | LCP — landing page | < 2.5s | p75 | Lighthouse CI + Vercel Web Vitals | > 2.0s | > 2.5s | Frontend |
| SLA-015 | LCP — create page | < 2.5s | p75 | Lighthouse CI | > 2.0s | > 2.5s | Frontend |
| SLA-016 | LCP — share page | < 2.5s | p75 | Lighthouse CI | > 2.0s | > 2.5s | Frontend |
| SLA-017 | CLS — all pages | < 0.1 | p75 | Lighthouse CI + Vercel Web Vitals | > 0.08 | > 0.1 | Frontend |
| SLA-018 | FID / INP — all pages | < 100ms | p75 | Lighthouse CI + web-vitals.js | > 80ms | > 100ms | Frontend |
| SLA-019 | TTFB — all pages | < 600ms | p75 | Lighthouse CI + WebPageTest | > 480ms | > 600ms | Frontend |

---

## 4. Load Test Scenarios

### 4.1 Normal Load
- **Profile**: 50 concurrent users, ~6 req/s (60% GET /api/prompts/today, 25% POST /api/contributions, 15% GET /api/composites/today)
- **Duration**: 30 minutes
- **Ramp-up**: 10 users/minute over 5 minutes, then hold at 50
- **Success criteria**: All SLAs SLA-001 through SLA-013 met; error rate < 0.1%
- **Data requirements**: Seeded daily prompt, 100 pre-existing approved contributions
- **Tool**: k6

### 4.2 Peak Load (Viral Spike)
- **Profile**: 500 concurrent users, ~60 req/s — simulates 5,000 contributions/hour
- **Duration**: 20 minutes sustained after ramp
- **Ramp-up**: 50 users/minute over 10 minutes
- **Success criteria**: All SLAs met; error rate < 1%; rate limiter returns 429s (not 500s); no DB connection pool exhaustion
- **Trigger simulation**: Single viral social media post driving inbound referral burst
- **Key risks**: Neon connection pool ceiling (10 on free tier, 100 on Pro — confirm before test); Upstash rate-limit key churn
- **Tool**: k6 with `ramping-vus` executor

### 4.3 Stress Test
- **Profile**: Ramp from 50 to 2,000 concurrent users at 100 users/minute
- **Duration**: Until p95 latency exceeds 2x any SLA target OR 5xx error rate exceeds 5%, whichever comes first
- **Success criteria**: System returns 429 or 503 gracefully (no data corruption); recovers to baseline within 5 minutes after load drops; no zombie connections in Neon
- **Observations during test**: Neon active connection count, Upstash command latency, Vercel function concurrency, Sharp process memory during any overlap with cron window
- **Tool**: k6 with custom thresholds and abortOnFail

### 4.4 Soak Test
- **Profile**: Normal load (50 concurrent users, ~6 req/s) sustained continuously
- **Duration**: 12 hours (overnight; must span at least one 00:00 UTC daily reset)
- **Success criteria**: p95 latency does not drift > 20% from the first-hour baseline; Neon active connections stable; Redis memory stable; cron executes successfully during the soak window; no 5xx errors in the final hour that were not present in the first hour
- **Monitoring**: Vercel function memory in logs, Neon active connections graph, Upstash memory graph, cron execution record at 00:00 UTC
- **Tool**: k6 with `constant-vus` executor; metrics exported to Grafana Cloud (free tier) for time-series review

---

## 5. Frontend Performance Budgets

| Metric | Budget | Measurement Tool | CI Enforcement |
|--------|--------|-----------------|----------------|
| JavaScript bundle (initial load) | < 200KB gzipped | @next/bundle-analyzer + size-limit | Fail build if exceeded |
| CSS bundle | < 50KB gzipped | size-limit | Fail build if exceeded |
| Fabric.js (drawing canvas) | Not in initial bundle — lazy only | Bundle analyzer chunk audit | Fail if found in main chunk |
| LCP | < 2.5s | Lighthouse CI (lhci autorun) | Fail PR if > 2.5s |
| FID / INP | < 100ms | Lighthouse CI | Fail PR if > 100ms |
| CLS | < 0.1 | Lighthouse CI | Fail PR if > 0.1 |
| TTFB | < 600ms | Lighthouse CI | Warn if > 600ms |
| Total page weight (initial load) | < 1.5MB | Lighthouse CI | Fail PR if exceeded |
| Font families | max 2 | Manual PR audit | PR review gate |
| Images | WebP/AVIF; lazy except above-fold | next/image lint rule | Fail if raw PNG/JPG > 100KB |

**Fabric.js note**: Fabric.js (~200KB gzipped) must be loaded exclusively via `next/dynamic` on the create page. Its presence in the initial bundle would single-handedly breach the JS budget and regress LCP on every page.

---

## 6. Backend Performance Budgets

| Endpoint | p50 | p95 | p99 | Max Throughput | DB Query Budget (p95) |
|----------|-----|-----|-----|----------------|-----------------------|
| GET /api/prompts/today | < 50ms | < 100ms | < 200ms | 200 req/s | < 5ms (Redis hit); < 30ms (cold DB) |
| POST /api/contributions | < 100ms | < 300ms | < 500ms | 20 req/s | < 50ms; Cloud Vision async |
| GET /api/composites/today | < 50ms | < 150ms | < 300ms | 100 req/s | < 5ms (Redis hit) |
| GET /api/contributions/:id | < 30ms | < 80ms | < 150ms | 50 req/s | < 10ms (PK lookup) |
| Nightly cron (composite gen, 500 tiles) | — | < 60s total | — | 1 concurrent | N/A |

---

## 7. Image Processing Budget

**Sharp composite generation (nightly cron):**
- Target: < 30s wall-clock for 500 tiles (Vercel Pro 300s timeout gives 10x headroom)
- Memory ceiling: < 512MB peak RSS; enforce by batching tiles in groups of 50
- Strategy: load batch of 50 tile buffers, call `sharp().composite([...])`, write intermediate, repeat; final merge in last pass
- Fallback: if tile count exceeds 500, reduce individual tile dimensions from 200x200 to 100x100 to stay under 512MB

**Per-contribution upload (POST /api/contributions):**
- Target: < 2s p95 total handler time
- Sharp thumbnail generation: < 200ms per image (resize to 200x200, convert to WebP)
- Vercel Blob write: < 500ms p95
- Cloud Vision SafeSearch: fire-and-forget async; contribution stored with `status = pending` immediately; moderation result updates status asynchronously
- Max accepted file size: 5MB enforced at API boundary before Sharp receives the buffer

---

## 8. Caching Strategy

| Layer | What to Cache | TTL | Invalidation Strategy | Cache Size Limit |
|-------|-------------|-----|----------------------|-----------------|
| Upstash Redis | `prompt:today` | Absolute expiry at 00:05 UTC | Cron sets new key, deletes old key | 1MB per key |
| Upstash Redis | `composite:today` (Blob URL + metadata) | Absolute expiry at 00:05 UTC | Cron writes new key after successful Blob upload | 1MB per key |
| Upstash Redis | `count:today:{date}` (contribution count) | Absolute expiry at 00:05 UTC | Atomic INCR on write; DEL at daily reset | Small |
| Upstash Redis | `rl:{session}:{endpoint}` (rate limit) | 60s sliding window | Automatic TTL expiry | Per key |
| Vercel CDN | Composite images (Blob URLs, date-stamped) | 24h (Cache-Control: max-age=86400) | New URL per day (date in filename = no collision) | — |
| Vercel CDN | OG share images (contribution-specific) | 7d (Cache-Control: max-age=604800) | URL includes contribution ID; treat as immutable | — |
| Vercel CDN | Static assets (_next/static/*) | 1 year immutable (max-age=31536000, immutable) | Content hash in filename | — |
| Browser | Static assets | 1 year immutable | Content hash | — |
| Browser | API responses (/api/prompts/today, /api/composites/today) | No browser cache (Cache-Control: no-store) | N/A — stale response = wrong day's data | — |

**Daily reset sequence (00:00 UTC cron, must complete in order):**
1. Acquire Postgres advisory lock to prevent duplicate cron runs.
2. Fetch all approved contributions for today from Neon.
3. Generate composite via Sharp (batched), upload to Vercel Blob with date-stamped key.
4. Insert record into `composites` table.
5. Write `composite:today` to Redis with absolute TTL = 00:05 UTC next day.
6. DEL `prompt:today`, `count:today:{date}` (new prompt is seeded by admin or seed script separately).
7. Release advisory lock. Log completion time.

---

## 9. Bottleneck Analysis

| Component | Potential Bottleneck | Impact | Likelihood | Mitigation | Monitoring |
|-----------|---------------------|--------|-----------|------------|------------|
| Neon connection pool | Viral spike exhausts pool (10 free / 100 Pro) | 500 errors on all DB writes | Medium | Upstash rate limiter caps inbound before DB; use Neon's built-in PgBouncer connection pooler | Neon dashboard active connections |
| Sharp in serverless (cron) | OOM kill on 500+ tiles without batching | Daily composite fails; no mosaic for the day | Medium | Batch 50 tiles at a time; set Node `--max-old-space-size=512` | Vercel function memory logs |
| Redis cache miss at daily reset | 00:00–00:01 UTC cache cleared; cold DB requests stampede | DB latency spike for ~60s | High (daily, predictable) | Cron pre-warms `prompt:today` Redis key before old key expires; use SWR pattern in API route | Redis hit rate in Upstash metrics |
| Cloud Vision API | Latency spike (>2s) or quota exhaustion during viral spike | Contribution queue backs up | Low | Async moderation (store first, moderate after); contributions visible after moderation completes | Cloud Vision error rate in GCP console |
| Vercel function cold start | First request of low-traffic window: 300–800ms init | p99 spike; TTFB SLA breach | Medium | Next.js 15 partial prerendering for landing and share pages; keep-warm cron ping if needed | Vercel Analytics function init duration |
| Fabric.js accidental eager load | If not lazy-loaded: +~200KB to initial JS bundle | LCP regression on all pages; CI budget breach | High (if misconfigured) | Enforce `next/dynamic` with `ssr: false`; CI bundle check blocks merge | @next/bundle-analyzer in CI |
| Vercel Blob upload throughput | 500 contribution uploads in 1 hour during viral spike | Individual upload latency increases | Low | Blob writes are independent per contribution; Vercel Blob scales horizontally | Vercel Blob usage dashboard |

---

## 10. Monitoring and Alerting

| Metric | Dashboard | Warning Threshold | Critical Threshold | Escalation |
|--------|-----------|------------------|-------------------|------------|
| API p95 latency | Vercel Analytics | > 240ms | > 500ms | Slack #alerts |
| API 5xx error rate | Vercel Analytics | > 0.5% over 5 min | > 1% over 5 min | Slack #alerts + PagerDuty |
| Nightly cron status | Vercel Cron logs | Execution > 45s | Any failure or timeout | Slack #alerts + email (immediate) |
| Neon active connections | Neon dashboard | > 70% of pool limit | > 90% of pool limit | Slack #alerts |
| Upstash Redis memory | Upstash metrics | > 80% of plan quota | > 95% of plan quota | Slack #alerts |
| Upstash Redis command latency | Upstash metrics | > 20ms | > 50ms | Slack #alerts |
| LCP (real user, p75) | Vercel Web Vitals | > 2.0s | > 2.5s | Slack #frontend |
| CLS (real user, p75) | Vercel Web Vitals | > 0.08 | > 0.1 | Slack #frontend |
| Vercel function memory (cron) | Vercel logs | > 400MB | > 490MB | Immediate investigation |
| JS bundle size | GitHub Actions size-limit | Increase > 10KB | Exceeds 200KB | PR blocked |

---

## 11. Performance CI (GitHub Actions)

```yaml
# .github/workflows/perf.yml — triggered on every PR to main
jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci && npm run build && npm run start &
      - uses: treosh/lighthouse-ci-action@v11
        with:
          urls: |
            http://localhost:3000/
            http://localhost:3000/create
            http://localhost:3000/share/test-id
          budgetPath: .lighthouserc.json
          uploadArtifacts: true

  bundle-size:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build
      - uses: andresz1/size-limit-action@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

**.lighthouserc.json:**
```json
{
  "ci": {
    "assert": {
      "assertions": {
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }],
        "total-blocking-time": ["error", { "maxNumericValue": 200 }],
        "first-contentful-paint": ["warn", { "maxNumericValue": 1800 }]
      }
    }
  }
}
```

**size-limit in package.json:**
```json
"size-limit": [
  { "path": ".next/static/chunks/main-*.js", "limit": "200 kB" },
  { "path": ".next/static/css/*.css", "limit": "50 kB" }
]
```

---

## 12. Performance Test Schedule

| Test Type | Frequency | Trigger | Environment | Owner |
|-----------|-----------|---------|-------------|-------|
| Lighthouse CI | Every PR to main | GitHub Actions | Preview deployment | Frontend |
| Bundle size check | Every PR to main | GitHub Actions | Build artifact | Frontend |
| Normal load (k6) | Every release | Post-merge to main | Vercel staging | QA |
| Viral spike (k6) | Weekly | Saturday 10:00 UTC scheduled | Vercel staging | Perf Eng |
| Stress test (k6) | Monthly | First Sunday of month | Dedicated Vercel preview | Perf Eng |
| Soak test (k6) | Monthly | First Monday night of month | Dedicated Vercel preview | Perf Eng |
| Cron smoke test | Every deployment | Post-deploy hook | Staging | DevOps |

---

## 13. Open Questions

| # | Question | Priority | Blocking? | Default if Unanswered |
|---|---------|----------|-----------|----------------------|
| OQ-001 | Is the Neon plan at launch Free (10 connections) or Pro (100)? | High | Yes — determines stress test design and peak SLAs | Assume 10; design rate limiting to protect it |
| OQ-002 | Is Cloud Vision SafeSearch call synchronous or async in the POST /api/contributions handler? | High | Yes — determines p95 target for SLA-005 | Default: async; contribution stored with status=pending |
| OQ-003 | What is the confirmed Vercel Pro function memory limit for the cron route? Default is 1024MB but verify. | Medium | No | Assume 512MB ceiling in Sharp batch sizing |
| OQ-004 | Are OG images for share pages generated on-demand (Vercel OG) or pre-generated at contribution time? | Medium | No | Default: on-demand via @vercel/og, cached at CDN edge |
| OQ-005 | Is there a target geographic user distribution? CDN edge region strategy depends on this. | Low | No | Default: global Vercel CDN, no region pinning |
