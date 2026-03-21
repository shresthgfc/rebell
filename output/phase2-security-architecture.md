# Phase 2 — Security Architecture: Mosaic

## 1. STRIDE Threat Model

| Threat | Category | Target | Mitigation |
|--------|----------|--------|------------|
| T1: Attacker submits offensive/illegal images | Tampering | Contribution API | Cloud Vision SafeSearch pre-screening + admin moderation queue |
| T2: Session token stolen via XSS | Spoofing | Session cookie | HttpOnly + Secure + SameSite=Lax cookies; CSP headers |
| T3: Brute-force contribution spam | DoS | API endpoints | Rate limiting (10/min per IP); CAPTCHA after threshold |
| T4: SQL injection via content_data | Tampering | Database | Parameterized queries via Drizzle ORM; input validation |
| T5: Unauthorized admin access | Elevation | Admin endpoints | Bearer token auth; IP allowlist for admin routes |
| T6: Enumeration of contribution IDs | Info Disclosure | GET /contributions/:id | UUIDs are non-sequential; no listing endpoint for MVP |
| T7: Image URL manipulation | Tampering | Vercel Blob | Signed URLs for uploads; public reads are fine (content is meant to be shared) |
| T8: CSRF on contribution submission | Spoofing | POST endpoints | SameSite=Lax cookie + Origin header validation |
| T9: PII leak from session data | Info Disclosure | Sessions table | Sessions contain no PII; registered user emails encrypted at rest |
| T10: DDoS on composite generation | DoS | Cron function | Cron is internal (not user-triggered); manual trigger is admin-only |

---

## 2. Authentication & Authorization

### Anonymous Sessions
```
┌──────────┐     ┌──────────────┐     ┌──────────┐
│  Browser  │────▶│  Middleware   │────▶│  API      │
│           │     │  Check cookie │     │  Route    │
│           │◀────│  Set if none  │     │          │
└──────────┘     └──────────────┘     └──────────┘

Cookie: mosaic_session={uuid-token}
Flags: HttpOnly, Secure, SameSite=Lax, Path=/, Max-Age=30d
```

### Authorization Matrix

| Role | View Prompt | Create Contribution | View Composite | Admin Actions |
|------|-------------|-------------------|----------------|---------------|
| Anonymous | Yes | Yes (1/day) | Yes | No |
| Registered (v1.1) | Yes | Yes (1/day) | Yes | No |
| Admin | Yes | Yes | Yes | Yes |

---

## 3. Content Moderation Pipeline

```
User submits contribution
        │
        ▼
┌─────────────────┐
│ Input Validation │ ── Reject if invalid format/size
│ (API Route)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Cloud Vision     │ ── SafeSearch detection
│ SafeSearch API   │    (adult, violence, racy)
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
  PASS      FAIL
    │         │
    ▼         ▼
 status:   status:
 approved  rejected
    │         │
    ▼         ▼
 Visible    Hidden;
 in mosaic  logged for
            review
```

**Thresholds**: Reject if any SafeSearch category >= LIKELY.
**Fallback**: If Cloud Vision is unavailable, queue as `pending` for manual review.
**Drawing content**: Convert base64 to image, run through SafeSearch before storing.
**Emoji/color content**: No moderation needed (predefined palettes).

---

## 4. OWASP Top 10 Mitigations

| # | Vulnerability | Mosaic-Specific Mitigation |
|---|--------------|---------------------------|
| A01 | Broken Access Control | Session-based access; admin routes require bearer token; no user-to-user data access |
| A02 | Cryptographic Failures | TLS 1.3 enforced (Vercel); passwords hashed with bcrypt (v1.1); no sensitive data in cookies |
| A03 | Injection | Drizzle ORM parameterized queries; Zod schema validation on all inputs |
| A04 | Insecure Design | Threat model above; idempotency prevents duplicate submissions; rate limiting |
| A05 | Security Misconfiguration | Security headers (CSP, X-Frame-Options, etc.); env vars for secrets; no debug in prod |
| A06 | Vulnerable Components | Dependabot alerts; `npm audit` in CI; lockfile pinning |
| A07 | Auth Failures | No traditional auth in MVP; session tokens are cryptographically random UUIDs |
| A08 | Data Integrity Failures | Signed Vercel deployments; no user-provided code execution; Subresource Integrity for CDN assets |
| A09 | Logging Failures | Structured logging via Vercel; admin actions logged; moderation decisions logged |
| A10 | SSRF | No user-provided URLs processed server-side; image data is uploaded as base64, not fetched |

---

## 5. Data Classification

| Data | Classification | Storage | Encryption |
|------|---------------|---------|------------|
| Session tokens | Internal | PostgreSQL + Redis | At rest (Neon default) |
| Contribution images | Public | Vercel Blob | In transit (TLS) |
| Composite images | Public | Vercel Blob | In transit (TLS) |
| User emails (v1.1) | PII / Confidential | PostgreSQL | At rest (Neon) + application-level encryption |
| Passwords (v1.1) | Secret | PostgreSQL | bcrypt hashed (never stored plaintext) |
| Admin tokens | Secret | Environment variables | Never stored in DB or logs |

---

## 6. Security Headers

```typescript
// middleware.ts
const securityHeaders = {
  'Content-Security-Policy': [
    "default-src 'self'",
    "script-src 'self' 'unsafe-inline'",  // Next.js requires inline scripts
    "style-src 'self' 'unsafe-inline'",
    "img-src 'self' blob: https://*.vercel-storage.com",
    "connect-src 'self'",
    "frame-ancestors 'none'",
  ].join('; '),
  'X-Content-Type-Options': 'nosniff',
  'X-Frame-Options': 'DENY',
  'X-XSS-Protection': '0',  // Deprecated; CSP handles this
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
  'Strict-Transport-Security': 'max-age=63072000; includeSubDomains; preload',
};
```

---

## 7. Incident Response

| Severity | Example | Response Time | Action |
|----------|---------|---------------|--------|
| Critical | Data breach, admin token compromised | < 1 hour | Rotate all tokens, notify affected users, audit logs |
| High | Offensive content bypasses moderation | < 4 hours | Remove content, tighten thresholds, review pipeline |
| Medium | Rate limiting bypassed | < 24 hours | Add IP to blocklist, review rate limit config |
| Low | Failed login attempts (v1.1) | < 48 hours | Monitor patterns, consider lockout policy |
