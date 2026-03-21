# Phase 2 — API Design: Mosaic

## 1. Overview

REST API via Next.js 15 Route Handlers. All responses are JSON. Authentication is session-based with anonymous-first design.

**Base URL**: `https://mosaic.app/api`
**Versioning**: URL prefix (`/api/v1/`) — deferred to v1.1; MVP uses `/api/`

---

## 2. Authentication Flow

### Anonymous Session (Default)
```
1. First visit → Server checks for session cookie
2. No cookie → Generate UUID session token, create session record
3. Set HttpOnly, Secure, SameSite=Lax cookie: `mosaic_session={token}`
4. Session valid for 30 days, refreshed on each visit
```

### Optional Registration (v1.1)
```
1. User provides email + password on /register
2. Link existing anonymous session to new user record
3. All prior contributions preserved under the account
```

---

## 3. Endpoint Specifications

### 3.1 GET /api/prompts/today
Get the current daily prompt.

**Response 200**:
```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "promptText": "Draw your morning mood using only shapes",
    "promptDate": "2026-03-21",
    "contributionCount": 142
  }
}
```

**Cache**: Redis `prompt:today`, TTL until midnight UTC.

---

### 3.2 POST /api/contributions
Submit a contribution. **Idempotent**: if session already contributed today, returns existing contribution (200, not 409).

**Request**:
```json
{
  "contentType": "emoji",
  "contentData": {
    "emoji": "🌅",
    "backgroundColor": "#FF6B35"
  }
}
```

Content types:
- `emoji`: `{ emoji: string, backgroundColor: string }`
- `color`: `{ colors: string[], pattern: "solid" | "gradient" | "mosaic" }`
- `drawing`: `{ imageData: string }` (base64 PNG, max 500KB)

**Response 201** (new contribution):
```json
{
  "data": {
    "id": "contribution-uuid",
    "contentType": "emoji",
    "imageUrl": "https://blob.vercel-storage.com/...",
    "shareUrl": "https://mosaic.app/piece/contribution-uuid",
    "isNew": true
  }
}
```

**Response 200** (idempotent — already contributed):
```json
{
  "data": {
    "id": "existing-contribution-uuid",
    "contentType": "emoji",
    "imageUrl": "https://blob.vercel-storage.com/...",
    "shareUrl": "https://mosaic.app/piece/existing-contribution-uuid",
    "isNew": false
  }
}
```

**Errors**:
- `400 INVALID_CONTENT_TYPE` — unsupported content type
- `400 PAYLOAD_TOO_LARGE` — drawing exceeds 500KB
- `400 VALIDATION_ERROR` — missing required fields
- `429 RATE_LIMITED` — too many requests

**Idempotency**: Enforced by DB unique constraint `(prompt_id, session_id)`. On conflict, SELECT and return existing.

---

### 3.3 GET /api/contributions/:id
Get a single contribution for the share page.

**Response 200**:
```json
{
  "data": {
    "id": "contribution-uuid",
    "contentType": "emoji",
    "imageUrl": "https://blob.vercel-storage.com/...",
    "promptText": "Draw your morning mood using only shapes",
    "promptDate": "2026-03-21",
    "createdAt": "2026-03-21T14:30:00Z"
  }
}
```

**Errors**: `404 NOT_FOUND`

---

### 3.4 GET /api/composites/today
Get today's composite (or the most recent one).

**Response 200**:
```json
{
  "data": {
    "id": "composite-uuid",
    "promptDate": "2026-03-20",
    "imageUrl": "https://blob.vercel-storage.com/...",
    "contributionCount": 287,
    "promptText": "Yesterday's prompt text"
  }
}
```

**Response 404**: No composites generated yet.

---

### 3.5 GET /api/composites/:date
Get composite for a specific date (format: YYYY-MM-DD).

**Response 200**: Same as above.
**Errors**: `404 NOT_FOUND`, `400 INVALID_DATE`

---

### 3.6 Admin Endpoints

| Endpoint | Method | Purpose | Auth |
|----------|--------|---------|------|
| `/api/admin/prompts` | POST | Create future prompts | Admin token |
| `/api/admin/prompts` | GET | List all prompts | Admin token |
| `/api/admin/moderate/:id` | PATCH | Approve/reject contribution | Admin token |
| `/api/admin/composite/generate` | POST | Manually trigger composite gen | Admin token |

Admin auth: Bearer token in `Authorization` header, stored as environment variable.

---

## 4. Rate Limiting

| Endpoint | Limit | Window | Key |
|----------|-------|--------|-----|
| POST /api/contributions | 10 | 1 minute | IP address |
| GET endpoints | 60 | 1 minute | IP address |
| Admin endpoints | 30 | 1 minute | Admin token |

Implemented via Upstash Redis sliding window. Returns `429` with `Retry-After` header.

---

## 5. Error Format

All errors follow a consistent format:
```json
{
  "error": {
    "code": "SNAKE_CASE_ERROR_CODE",
    "message": "Human-readable description",
    "status": 400,
    "details": {}
  }
}
```

### Error Codes
| Code | Status | Description |
|------|--------|-------------|
| `VALIDATION_ERROR` | 400 | Request body validation failed |
| `INVALID_CONTENT_TYPE` | 400 | Unsupported contribution type |
| `PAYLOAD_TOO_LARGE` | 400 | Drawing data exceeds limit |
| `INVALID_DATE` | 400 | Date parameter malformed |
| `NOT_FOUND` | 404 | Resource does not exist |
| `CONTRIBUTION_EXISTS` | 200 | Already contributed (returns existing) |
| `RATE_LIMITED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Unexpected server error |
| `MODERATION_REJECTED` | 403 | Content flagged by moderation |

---

## 6. CORS & Security Headers

```typescript
// next.config.ts
headers: [
  {
    source: '/api/:path*',
    headers: [
      { key: 'X-Content-Type-Options', value: 'nosniff' },
      { key: 'X-Frame-Options', value: 'DENY' },
      { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
    ]
  }
]
```

CORS: Same-origin only for MVP. No cross-origin API access needed.

---

## 7. Request/Response Conventions

- **IDs**: UUID v4
- **Dates**: ISO 8601 (`2026-03-21T14:30:00Z`)
- **Date-only**: `YYYY-MM-DD` format
- **Pagination**: Not needed for MVP (single prompt per day)
- **Envelope**: All responses wrapped in `{ data: ... }` or `{ error: ... }`
