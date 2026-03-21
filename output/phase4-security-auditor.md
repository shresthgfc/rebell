# Security Audit — Mosaic

## 1. Document Info
- Date: 2026-03-21
- Source: phase2-security-architecture.md, phase2-synthesis.md
- Auditor: Security Auditor Sub-Agent
- Status: Draft
- Scope: Architecture and design review — no source code reviewed
- Methodology: OWASP Top 10 (2021), ASVS, threat modeling review

## 2. Executive Summary

Mosaic's security architecture is well-structured for an anonymous-first creative prompt platform. The design correctly applies HttpOnly cookies, Drizzle ORM parameterization, Cloud Vision pre-screening, and Upstash rate limiting. However, three gaps warrant attention before production: the CSP `unsafe-inline` directive undermines XSS protection, session token rotation on privilege change is unspecified, and the admin bearer token scheme lacks a formal rotation and revocation policy. No critical findings were identified based on available design documents; two high-severity concerns are raised.

- Critical findings: 0
- High findings: 2
- Medium findings: 2
- Low findings: 1

---

## 3. OWASP Top 10 Audit

**A01 — Broken Access Control: Pass (with concern)**
Authorization is enforced at middleware with session cookies; admin routes require a separate bearer token with IP allowlist planned. The `UNIQUE(prompt_id, session_id)` constraint prevents one-per-day bypass at the database layer. Concern: the admin bearer token is stored only in environment variables with no documented rotation cadence or revocation process. A compromised token has indefinite validity until manually rotated. The IP allowlist is "recommended" but not confirmed as mandatory — if skipped, any leaked token grants full admin access from any IP.

**A02 — Cryptographic Failures: Pass**
TLS 1.3 is enforced by Vercel at the platform level. Session cookies carry no sensitive payload — only a UUID token. Passwords (v1.1) are bcrypt-hashed and never stored plaintext. Admin tokens live exclusively in environment variables, not the database or logs. Neon PostgreSQL encrypts at rest by default. Application-level encryption is planned for user emails in v1.1. No weak algorithm usage is documented. No plaintext secret storage is documented.

**A03 — Injection: Pass**
Drizzle ORM uses parameterized queries throughout; no raw SQL concatenation is indicated in the design. All inputs pass through Zod schema validation before reaching the ORM. Drawing submissions are base64-encoded and converted to image before storage, not executed. Emoji and color contributions use predefined palettes, eliminating free-text injection surface for those content types. The primary residual risk is second-order injection if admin tooling renders stored contribution metadata without escaping — this is unverifiable without code review.

**A04 — Insecure Design: Pass (with concern)**
A STRIDE threat model is present and covers ten threat vectors with mitigations. Rate limiting (10/min per IP via Upstash sliding window) is designed for contribution endpoints. CAPTCHA is noted as a post-threshold fallback but not confirmed as implemented. Concern: no abuse case is documented for session farming — an attacker can programmatically create unlimited anonymous sessions (each UUID is independent) and use each session to submit one contribution per day, circumventing the per-session idempotency limit. A per-IP daily submission ceiling is not explicitly designed.

**A05 — Security Misconfiguration: Concern**
Security headers are explicitly configured in middleware and cover all required fields. HSTS is set with `max-age=63072000; includeSubDomains; preload` — correct. `X-Content-Type-Options: nosniff` and `X-Frame-Options: DENY` are present. However, `script-src 'self' 'unsafe-inline'` in the CSP critically weakens XSS protection. Next.js 15 supports nonce-based CSP which eliminates the need for `unsafe-inline`. Until this is addressed, XSS via stored content (e.g., a future text field or admin UI) bypasses the CSP entirely.

**A06 — Vulnerable and Outdated Components: Pass (with conditions)**
Dependabot alerts and `npm audit` in CI are documented. Lockfile pinning is required. The design references the correct tooling for the MVP scope. Conditions that must be confirmed in implementation: (1) `npm audit` failures at high/critical CVSS must block the CI build, not merely warn; (2) a transitive dependency scan policy (weekly minimum) must be implemented; (3) an SBOM must be generated on each release build. Sharp (libvips bindings) and the Cloud Vision Node client are high-value targets given their processing of untrusted image data — these must be prioritized for CVE monitoring.

**A07 — Identification and Authentication Failures: Pass**
MVP has no traditional authentication, eliminating credential stuffing, weak password, and MFA-bypass risks. Anonymous session tokens are described as cryptographically random UUIDs. Session tokens are stored in `sessions` table with expiry. No sensitive data is stored in the session payload. Concern (documented as open question below): session rotation behavior upon any privilege escalation event (e.g., admin token use in the same browser context) is unspecified.

**A08 — Software and Data Integrity Failures: Pass**
Vercel handles signed deployments. No user-provided code is executed. Subresource Integrity (SRI) is documented for CDN assets. The composite pipeline runs on a server-side cron with no user-triggerable path. The Vercel Blob upload flow uses signed URLs, preventing unauthorized writes. No deserialization of untrusted objects is described.

**A09 — Security Logging and Monitoring Failures: Pass (with concern)**
Structured logging is provided via Vercel's platform. Admin actions are logged. Moderation decisions (approve/reject) are logged with rejected content retained for review. Concern: no alerting thresholds or SIEM integration are documented. A burst of rejected moderation events (indicating an active bypass attempt) would produce logs but no automatic alert. Logging of individual failed contribution attempts per session is unconfirmed — necessary for detecting session farming.

**A10 — Server-Side Request Forgery (SSRF): Pass**
No user-provided URLs are processed server-side. Image contributions are submitted as base64-encoded data, not as URLs to be fetched. The composite generation pipeline fetches only from Vercel Blob (internal, trusted origin). Cloud Vision API calls originate server-side to a fixed Google endpoint with no user-influenced URL construction. SSRF surface is effectively zero for the documented architecture.

---

## 4. Session Security

| Aspect | Implementation | Finding | Severity |
|--------|---------------|---------|----------|
| HttpOnly flag | Set per design | Prevents JS access to session token | Pass |
| Secure flag | Set per design | Enforces HTTPS-only transmission | Pass |
| SameSite=Lax | Set per design | Mitigates CSRF on top-level navigation | Pass |
| Session rotation | Not documented | No rotation on state change | Medium |
| Sensitive data in session | UUID token only, no PII | Correct — minimal session payload | Pass |
| Token entropy | Described as "cryptographically random UUID" | UUID v4 provides ~122 bits entropy — acceptable | Pass |
| Session expiry | Max-Age=30d documented | Long-lived; no idle timeout documented | Low |

Session rotation on privilege change must be implemented: if a user authenticates as admin in the same browser session, the session token must be rotated to prevent session fixation.

---

## 5. Image Upload Vectors

| Vector | Design Status | Finding | Severity |
|--------|--------------|---------|----------|
| File type validation | Implied by input validation step | Magic-byte validation (not just MIME header) must be confirmed in code | Medium |
| EXIF stripping | Not explicitly documented | Sharp processing converts base64 to output image — EXIF is stripped by default on re-encode | Pass (verify) |
| Maximum file size | Not explicitly specified in reviewed docs | Hard limit must be enforced at API layer before Sharp processing to prevent memory exhaustion | High |
| Sharp as sanitization | Base64 → Sharp → Blob pipeline documented | Re-encoding through Sharp destroys polyglot payloads | Pass |
| User-controlled filenames | Design uses signed Vercel Blob URLs | No evidence of user-supplied filenames in Blob paths | Pass |
| SVG uploads | Not addressed | SVG files can contain embedded scripts — must be explicitly blocked at content-type check | Medium |

---

## 6. Content Moderation Bypass

Cloud Vision SafeSearch can be evaded by low-resolution submissions, heavily stylized drawings, adversarial pixel patterns, or content that falls below the LIKELY threshold. The design sets the rejection threshold at `>= LIKELY` which is correct but leaves the POSSIBLE band approved. Mitigations already designed — manual queue fallback when Cloud Vision is unavailable, logging of rejected content — are appropriate. Additional gaps: no community reporting mechanism is designed for post-publish offensive content that passed automated screening. Rate limiting at 10 submissions/min per IP is present, but session farming (see A04) allows circumventing per-session submission limits. Recommended additions: (1) lower threshold to POSSIBLE for violence/adult categories specifically; (2) add a post-publish report button with admin queue routing; (3) enforce a per-IP daily ceiling independent of session count.

---

## 7. Admin Endpoint Protection

| Aspect | Implementation | Finding | Severity |
|--------|---------------|---------|----------|
| Authentication required | Bearer token in env var | Token scheme is functional but lacks rotation policy | High |
| IP allowlist | Recommended, not confirmed mandatory | Must be enforced in middleware, not just recommended | High |
| Audit logging | Admin actions logged per design | Logging destination and retention period unspecified | Medium |
| Rate limiting | Not specified for admin endpoints | Admin endpoints should have strict rate limiting independent of user limits | Medium |
| Token revocation | No mechanism documented | Compromise requires manual env var rotation and redeployment | High |

Admin bearer tokens stored in Vercel environment variables are rotated only via redeployment. A token compromise window equals the time to detect plus redeployment time. Recommend: short-lived tokens (JWT with 1-hour expiry) signed with a rotating secret, or use of Vercel's environment variable versioning to enable rapid rotation without full redeployment.

---

## 8. SAST/DAST Plan

| Tool | Type | Integration Point | Blocking? | Threshold |
|------|------|-------------------|-----------|-----------|
| eslint-plugin-security | SAST | PR check — pre-merge | Yes | Zero errors |
| npm audit | SCA | PR check — pre-merge | Yes | Zero critical/high CVEs |
| Snyk or Dependabot | SCA | Scheduled weekly scan | Yes (critical) | CVSS >= 9.0 blocks next release |
| OWASP ZAP (baseline scan) | DAST | Staging deployment post-deploy | Yes | Zero critical alerts |
| truffleHog or gitleaks | Secret detection | Pre-commit hook + PR check | Yes | Zero secrets |

OWASP ZAP should be configured with the Mosaic-specific context: authenticated admin session (grey-box), contribution submission endpoint fuzzing, and file upload probing. The ZAP baseline scan covers passive rules; add active scan rules for the contribution POST endpoint specifically. DAST must not run against production — staging with seeded test data only.

---

## 9. Top 5 Findings

**FIND-001 — High: CSP `unsafe-inline` Negates XSS Protection**
The `script-src 'self' 'unsafe-inline'` directive allows any inline script to execute, rendering the CSP ineffective against XSS. Next.js 15 supports nonce-based CSP via middleware. Remediation: implement per-request nonce injection in middleware, pass nonce to Next.js script components, remove `unsafe-inline` from script-src. Severity: High (CVSS ~7.4 — network-accessible, no auth required if a stored XSS vector exists in future text fields).

**FIND-002 — High: Admin Token Has No Expiry or Revocation Path**
Static bearer tokens in environment variables cannot be revoked without redeployment. A leaked token grants full admin access until manually rotated. Remediation: replace static bearer token with short-lived JWT (1-hour expiry) signed with a secret stored in Vercel env vars. Add a token refresh endpoint accessible only from the IP allowlist. Enforce IP allowlist as a hard middleware check, not a recommendation. Severity: High (CVSS ~8.1 — network-accessible, low complexity once token is obtained).

**FIND-003 — Medium: No Maximum File Size Enforced at API Boundary**
The design documents Sharp processing of uploaded base64 images but does not specify a maximum size limit enforced before processing begins. A malicious submission of a very large base64 payload reaches Sharp before rejection, enabling memory exhaustion in the serverless function. Remediation: enforce a hard Content-Length check (recommended: 5 MB max) at the API route handler before any processing. Return HTTP 413 immediately on oversize submissions. Severity: Medium (CVSS ~5.3 — requires network access, results in function timeout/DoS).

**FIND-004 — Medium: Session Farming Bypasses Per-Session Submission Limit**
Anonymous sessions are issued freely on first visit with no friction. An automated client can create unlimited sessions, each eligible for one daily contribution, effectively bypassing the idempotency control. Remediation: add a per-IP daily submission ceiling (e.g., 3 per IP per day) enforced in Upstash Redis independently of session identity. Optionally, add proof-of-work or invisible CAPTCHA at session issuance for clients exhibiting automated patterns. Severity: Medium (CVSS ~5.0 — enables content flooding and moderation queue saturation).

**FIND-005 — Low: Session Idle Timeout Not Documented**
Sessions are valid for 30 days (Max-Age) with no idle timeout. A session token captured from an unattended device remains valid for up to 30 days. Remediation: implement server-side idle timeout (recommended: 7 days of inactivity) by recording `last_seen_at` in the `sessions` table and invalidating stale sessions via a cleanup cron. Update the cookie Max-Age on each active request (sliding expiry). Severity: Low (CVSS ~3.1 — requires physical or network access to obtain session cookie).

---

## 10. Open Questions

| # | Question | Priority | Blocking? | Default if Unanswered |
|---|---------|----------|-----------|----------------------|
| OQ-001 | Is the IP allowlist for admin routes enforced in middleware code, or only a deployment recommendation? | High | Yes | Treat as unimplemented — block release until confirmed |
| OQ-002 | What is the maximum accepted image payload size at the contribution API endpoint? | High | Yes | Enforce 5 MB until specified |
| OQ-003 | Does Sharp re-encode strip EXIF by default in the configured output format? Confirm via code review. | Medium | No | Assume strip — verify before launch |
| OQ-004 | Are `npm audit` failures at high/critical severity configured to fail the CI build, or only report? | High | Yes | Must fail build — confirm in CI config |
| OQ-005 | Is session rotation implemented when an admin bearer token is presented in a browser context? | Medium | No | Document as known gap; implement before v1.1 registered-user auth |
