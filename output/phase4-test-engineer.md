# Phase 4 — Test Engineer: Detailed Test Cases

## 1. Unit Tests — BDD Format

### 1.1 Session Middleware

```gherkin
Given a request with no mosaic_session cookie
When the middleware runs
Then a new UUID session token is generated
And a session record is created in the database
And a Set-Cookie header is returned with HttpOnly, Secure, SameSite=Lax flags
And Max-Age is set to 30 days

Given a request with a valid mosaic_session cookie
When the middleware runs
Then the session is loaded from the database
And the session's lastActiveAt is updated
And no Set-Cookie header is returned

Given a request with an expired or invalid session cookie
When the middleware runs
Then the old cookie is cleared
And a new session is created (same flow as no-cookie case)
```

### 1.2 ContributionService.submit()

```gherkin
Given a valid session and today's prompt exists
When submit is called with contentType "emoji" and valid contentData
Then a contribution record is created with status "approved"
And the contribution image is uploaded to Vercel Blob
And the Redis counter contribution:count:{date} is incremented
And a ContributionResult is returned with shareUrl

Given a session that already contributed to today's prompt
When submit is called again
Then the existing contribution is returned
And isNew is false
And no new record is created (idempotent)

Given contentType "drawing" with imageData exceeding 500KB
When submit is called
Then a ValidationError with code PAYLOAD_TOO_LARGE is thrown

Given contentType "drawing" with valid imageData
When Cloud Vision SafeSearch returns adult >= LIKELY
Then the contribution is created with status "rejected"
And a ModerationError is returned to the user

Given contentType "drawing" with valid imageData
When Cloud Vision API is unavailable (timeout/error)
Then the contribution is created with status "pending"
And the contribution is queued for manual review
```

### 1.3 CompositeService.generate()

```gherkin
Given a date with 50 approved contributions
When generate is called
Then an advisory lock is acquired for that date
And all 50 contribution images are downloaded
And Sharp composites them into a grid (ceil(sqrt(50)) columns)
And the composite image is uploaded to Vercel Blob
And an OG image (1200x630) is generated and uploaded
And the composite record is inserted into the database
And Redis cache composite:today is invalidated
And the advisory lock is released

Given a date with 0 contributions
When generate is called
Then a placeholder composite is created with a "No contributions" message
And a composite record is still created

Given a date where a composite already exists
When generate is called again
Then it returns the existing composite without regenerating (idempotent)
And no new images are uploaded

Given generate is called but the advisory lock is already held
When another process is generating for the same date
Then generate waits for the lock (or returns gracefully)
```

### 1.4 Rate Limiting

```gherkin
Given an IP address making POST /api/contributions requests
When 10 requests are made within 1 minute
Then all 10 return successful responses

Given an IP address that has made 10 POST requests in 1 minute
When the 11th request is made
Then a 429 response is returned
And the response includes a Retry-After header

Given the 1-minute window has elapsed
When a new request is made from the same IP
Then the request is allowed (window reset)
```

### 1.5 ModerationService

```gherkin
Given an image buffer
When scan is called and Cloud Vision returns all categories VERY_UNLIKELY
Then isApproved returns true

Given an image buffer
When scan returns adult = LIKELY, all others UNLIKELY
Then isApproved returns false

Given an image buffer
When scan returns violence = POSSIBLE (below LIKELY)
Then isApproved returns true (threshold is LIKELY)
```

---

## 2. Integration Tests — API Endpoints

### 2.1 GET /api/prompts/today

| # | Scenario | Setup | Expected |
|---|----------|-------|----------|
| IT-01 | Active prompt exists | Seed prompt with today's date | 200, data.promptText present, data.promptDate = today |
| IT-02 | No active prompt | Empty prompts table | 404, error.code = NOT_FOUND |
| IT-03 | Redis cache hit | Call twice; second should hit cache | Both return identical data; DB queried once |
| IT-04 | contributionCount accuracy | Seed 5 approved contributions | data.contributionCount = 5 |

### 2.2 POST /api/contributions

| # | Scenario | Request Body | Expected |
|---|----------|-------------|----------|
| IT-05 | Valid emoji submission | `{ contentType: "emoji", contentData: { emoji: "🌅", backgroundColor: "#FF6B35" } }` | 201, data.contentType = "emoji", data.shareUrl present |
| IT-06 | Valid color submission | `{ contentType: "color", contentData: { colors: ["#FF6B35"], pattern: "solid" } }` | 201 |
| IT-07 | Valid drawing submission | `{ contentType: "drawing", contentData: { imageData: "<valid-base64>" } }` | 201 |
| IT-08 | Duplicate submission (idempotent) | Same session submits twice | First: 201 (isNew=true), Second: 200 (isNew=false), same id |
| IT-09 | Invalid contentType | `{ contentType: "video" }` | 400, INVALID_CONTENT_TYPE |
| IT-10 | Missing required fields | `{ contentType: "emoji" }` | 400, VALIDATION_ERROR |
| IT-11 | Drawing too large | `{ contentType: "drawing", contentData: { imageData: "<700KB>" } }` | 400, PAYLOAD_TOO_LARGE |
| IT-12 | No session cookie | Omit cookie | New session created, contribution succeeds |
| IT-13 | Rate limited | 11 requests in 1 minute | 11th returns 429 |

### 2.3 GET /api/contributions/:id

| # | Scenario | Expected |
|---|----------|----------|
| IT-14 | Valid existing ID | 200, data.id matches, data.imageUrl present |
| IT-15 | Non-existent UUID | 404, NOT_FOUND |
| IT-16 | Malformed ID (not UUID) | 400, VALIDATION_ERROR |
| IT-17 | Rejected contribution | 404 (rejected contributions not publicly visible) |

### 2.4 GET /api/composites/today

| # | Scenario | Expected |
|---|----------|----------|
| IT-18 | Composite exists for yesterday | 200, data.imageUrl present, data.contributionCount > 0 |
| IT-19 | No composites exist | 404 |
| IT-20 | Redis cache hit | Second call returns same data, DB not re-queried |

### 2.5 POST /api/admin/moderate/:id

| # | Scenario | Expected |
|---|----------|----------|
| IT-21 | Valid admin token, approve | 200, contribution status → approved |
| IT-22 | Valid admin token, reject | 200, contribution status → rejected |
| IT-23 | No auth header | 401, UNAUTHORIZED |
| IT-24 | Invalid admin token | 403, FORBIDDEN |

---

## 3. Contract Tests

| Contract | Provider | Consumer | Verified Fields |
|----------|----------|----------|-----------------|
| Prompt response | GET /api/prompts/today | PromptCard component | data.id (UUID), data.promptText (string), data.promptDate (YYYY-MM-DD), data.contributionCount (number) |
| Contribution response | POST /api/contributions | PreviewSubmitSheet | data.id (UUID), data.shareUrl (URL), data.isNew (boolean), data.imageUrl (URL) |
| Composite response | GET /api/composites/today | MosaicViewer | data.imageUrl (URL), data.contributionCount (number), data.promptDate (YYYY-MM-DD) |
| Error response | All endpoints | Error handler | error.code (string), error.message (string), error.status (number) |

---

## 4. Boundary Value Analysis

| Input | Min Valid | Max Valid | Just Over Max | Notes |
|-------|-----------|-----------|---------------|-------|
| Drawing imageData size | 1 byte | 500KB (666,666 base64 chars) | 500.001KB | Zod max 700,000 chars (~500KB) |
| Emoji string length | 1 char | 10 chars | 11 chars | Single emoji to emoji sequence |
| backgroundColor hex | #000000 | #FFFFFF | #GGGGGG (invalid) | Regex validated |
| Color array length | 1 color | 6 colors | 7 colors | Zod .min(1).max(6) |
| Rate limit window | 1 request | 10 requests/min | 11 requests/min | Sliding window |
| Session Max-Age | Fresh session | 30 days | 31 days (expired) | Cookie expiry |
| Prompt date format | 2026-01-01 | 2026-12-31 | 2026-13-01 (invalid) | YYYY-MM-DD validated |

---

## 5. Negative Test Cases

| # | Scenario | Input | Expected |
|---|----------|-------|----------|
| NEG-01 | XSS in emoji field | `<script>alert(1)</script>` | Rejected by Zod (not valid emoji) |
| NEG-02 | SQL injection in contentData | `'; DROP TABLE contributions;--` | Parameterized query via Drizzle; no injection |
| NEG-03 | Expired session token | UUID that doesn't exist in DB | New session created transparently |
| NEG-04 | Malformed JSON body | `{invalid json` | 400, parse error |
| NEG-05 | Missing Content-Type header | No application/json | 400 |
| NEG-06 | Polyglot file as drawing | PNG header + embedded JS | Sharp processes only pixel data; JS ignored |
| NEG-07 | EXIF data in drawing | Image with GPS coordinates | Sharp strips EXIF on processing |
| NEG-08 | Concurrent duplicate submissions | Same session, same prompt, 10 parallel POSTs | Only 1 record created (DB unique constraint); all return same contribution |
| NEG-09 | Admin endpoint without token | POST /api/admin/prompts with no auth | 401 |
| NEG-10 | Contribution to future prompt | Submit for tomorrow's prompt | 400 or uses today's prompt (prompt lookup is by date, not user-supplied) |

---

## 6. Mocking Strategy

| Dependency | Mock Approach | Library |
|------------|--------------|---------|
| PostgreSQL (unit tests) | In-memory Drizzle with SQLite adapter | drizzle-orm/sqlite-core |
| PostgreSQL (integration) | testcontainers PostgreSQL | @testcontainers/postgresql |
| Upstash Redis | In-memory Map-based mock | Custom mock implementing get/set/incr/expire |
| Cloud Vision API | MSW intercept | msw — return configurable SafeSearch responses |
| Vercel Blob | In-memory store | Custom mock: put() stores to Map, returns URL |
| Sharp | Real Sharp (fast enough for tests) | No mock needed — processes actual images |
| fetch (frontend) | MSW browser handlers | msw/browser for component tests |

---

## 7. Test Data Fixtures

```typescript
// test/fixtures/index.ts
export const fixtures = {
  prompts: {
    today: { id: 'prompt-today-uuid', promptText: 'Draw your morning mood', promptDate: '2026-03-21', isActive: true },
    yesterday: { id: 'prompt-yesterday-uuid', promptText: 'Express joy in color', promptDate: '2026-03-20', isActive: false },
    tomorrow: { id: 'prompt-tomorrow-uuid', promptText: 'What does silence look like?', promptDate: '2026-03-22', isActive: false },
  },
  sessions: {
    anonymous: { id: 'session-anon-uuid', userId: null, lastActiveAt: new Date(), expiresAt: new Date(Date.now() + 30 * 86400000) },
    contributed: { id: 'session-contributed-uuid', userId: null, lastActiveAt: new Date(), expiresAt: new Date(Date.now() + 30 * 86400000) },
  },
  contributions: {
    emoji: { id: 'contrib-emoji-uuid', sessionId: 'session-contributed-uuid', promptId: 'prompt-today-uuid', contentType: 'emoji', imageUrl: 'https://blob.vercel-storage.com/emoji.png', status: 'approved' },
    drawing: { id: 'contrib-drawing-uuid', sessionId: 'session-anon-uuid', promptId: 'prompt-today-uuid', contentType: 'drawing', imageUrl: 'https://blob.vercel-storage.com/drawing.png', status: 'approved' },
    rejected: { id: 'contrib-rejected-uuid', sessionId: 'session-anon-uuid', promptId: 'prompt-today-uuid', contentType: 'drawing', imageUrl: null, status: 'rejected' },
  },
  composites: {
    yesterday: { id: 'composite-uuid', promptDate: '2026-03-20', imageUrl: 'https://blob.vercel-storage.com/composite.png', contributionCount: 42 },
  },
};
```
