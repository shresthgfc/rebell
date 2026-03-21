# Phase 3 — DevOps Engineer: CI/CD & Infrastructure

## 1. Environment Setup

| Environment | Branch | URL | Purpose |
|-------------|--------|-----|---------|
| Preview | PR branches | `*.vercel.app` | Per-PR preview deployments |
| Staging | `main` | `staging.mosaic.app` | Pre-production testing |
| Production | Release tags | `mosaic.app` | Live site |

### Environment Variables

| Variable | Staging | Production | Where |
|----------|---------|------------|-------|
| `DATABASE_URL` | Neon staging branch | Neon main branch | Vercel env |
| `UPSTASH_REDIS_REST_URL` | Upstash staging | Upstash production | Vercel env |
| `UPSTASH_REDIS_REST_TOKEN` | Staging token | Production token | Vercel env |
| `BLOB_READ_WRITE_TOKEN` | Auto (Vercel) | Auto (Vercel) | Vercel integration |
| `GOOGLE_CLOUD_VISION_KEY` | Shared key | Production key | Vercel env |
| `ADMIN_TOKEN` | Dev token | Rotated monthly | Vercel env |
| `NEXT_PUBLIC_BASE_URL` | staging URL | production URL | Vercel env |

---

## 2. CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/ci.yml
name: CI
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  lint-and-type-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: 'npm' }
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check

  test:
    runs-on: ubuntu-latest
    needs: lint-and-type-check
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: 'npm' }
      - run: npm ci
      - run: npm test -- --coverage
      - uses: codecov/codecov-action@v4

  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: 'npm' }
      - run: npm ci
      - run: npm run build

  # Vercel handles deployment via GitHub integration
```

### Pipeline Stages
```
PR opened → Lint → Type Check → Unit Tests → Build → Vercel Preview Deploy
PR merged to main → Same checks → Vercel Staging Deploy
Tag created (v*) → Same checks → Vercel Production Deploy
```

---

## 3. Monitoring & Observability

### Vercel Built-in
- **Analytics**: Core Web Vitals, page views, geography
- **Logs**: Function invocation logs, error logs
- **Speed Insights**: Real User Monitoring (RUM)

### Custom Monitoring

| Metric | Tool | Alert Threshold |
|--------|------|-----------------|
| Composite cron success/failure | Vercel Logs + webhook | Any failure → Slack alert |
| API error rate | Vercel Analytics | > 5% errors in 5 min → alert |
| Response time (p95) | Vercel Speed Insights | > 3s → warning |
| Contribution count per day | Custom dashboard (Redis counter) | < 10 by noon → investigate |
| Blob storage usage | Vercel dashboard | > 80% of plan limit → alert |

### Health Check Endpoint
```typescript
// GET /api/health
export async function GET() {
  const checks = {
    database: await checkDB(),      // Simple SELECT 1
    redis: await checkRedis(),      // PING
    blob: 'ok',                     // Vercel-managed
  };
  const healthy = Object.values(checks).every(v => v === 'ok');
  return Response.json({ status: healthy ? 'ok' : 'degraded', checks },
    { status: healthy ? 200 : 503 });
}
```

---

## 4. Infrastructure as Code

Minimal IaC needed — Vercel manages most infrastructure. Key configs:

### vercel.json
```json
{
  "crons": [
    { "path": "/api/cron/composite", "schedule": "0 0 * * *" },
    { "path": "/api/cron/cleanup", "schedule": "0 3 * * 0" }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" }
      ]
    }
  ]
}
```

### Neon Database
- Staging: Branch off main for each feature (auto-created via Neon GitHub integration)
- Production: Main branch, PITR enabled, 7-day retention

---

## 5. Rollback Procedure

| Scenario | Action | Time |
|----------|--------|------|
| Bad deployment | Vercel instant rollback to previous deployment | < 1 min |
| Database migration issue | Neon branch restore to pre-migration point | < 5 min |
| Cron job failure | Manual trigger via admin endpoint | < 2 min |
| Redis data corruption | Flush affected keys; data self-heals from DB | < 5 min |

---

## 6. Cost Estimate (Monthly)

| Service | Tier | Est. Cost |
|---------|------|-----------|
| Vercel | Pro ($20/mo) | $20 |
| Neon PostgreSQL | Free tier (up to 0.5GB) | $0 |
| Upstash Redis | Free tier (10K commands/day) | $0 |
| Vercel Blob | Included in Pro (up to 1GB) | $0 |
| Cloud Vision API | 1K images/mo free; $1.50/1K after | ~$5 |
| Domain | Annual | ~$1/mo |
| **Total MVP** | | **~$26/mo** |

Scales to ~$100/mo at 10K daily users before needing tier upgrades.
