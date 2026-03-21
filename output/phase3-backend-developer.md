# Phase 3 — Backend Developer: Service Layer Plan

## 1. Service Architecture (Clean Architecture)

```
API Route Handlers (thin controllers)
        │
        ▼
   Service Layer (business logic)
        │
        ▼
   Repository Layer (data access via Drizzle)
        │
        ▼
   Database (PostgreSQL) + Cache (Redis) + Storage (Blob)
```

---

## 2. Service Modules

### 2.1 PromptService (`src/lib/services/prompt.service.ts`)

```typescript
interface PromptService {
  getTodayPrompt(): Promise<Prompt>;           // Redis-cached, fallback to DB
  createPrompt(data: CreatePromptInput): Promise<Prompt>;  // Admin only
  listPrompts(options?: { upcoming?: boolean }): Promise<Prompt[]>;
}
```

**Logic**:
- `getTodayPrompt()`: Check Redis `prompt:today` → if miss, query DB for `prompt_date = CURRENT_DATE` → cache result until midnight UTC
- Daily prompt rotation: Cron sets `is_active` flag at midnight, or query by date

### 2.2 ContributionService (`src/lib/services/contribution.service.ts`)

```typescript
interface ContributionService {
  submit(sessionId: string, input: ContributionInput): Promise<ContributionResult>;
  getById(id: string): Promise<Contribution | null>;
  getByPromptId(promptId: string, status?: Status): Promise<Contribution[]>;
  moderate(id: string, action: 'approve' | 'reject'): Promise<void>;
}
```

**Submit logic (critical path)**:
```
1. Validate input with Zod schema
2. Get today's prompt
3. Check for existing contribution (prompt_id + session_id)
   → If exists, return existing (idempotent)
4. If content_type === 'drawing':
   a. Decode base64, validate size (<500KB)
   b. Run Cloud Vision SafeSearch
   c. If flagged → reject immediately
5. Generate contribution image (Sharp):
   - emoji: render emoji on colored background
   - color: render color pattern
   - drawing: use uploaded image directly
6. Upload image to Vercel Blob
7. INSERT contribution record (status: approved or pending)
8. Increment Redis counter `contribution:count:{date}`
9. Return contribution with share URL
```

### 2.3 CompositeService (`src/lib/services/composite.service.ts`)

```typescript
interface CompositeService {
  generate(promptDate: string): Promise<Composite>;  // Called by cron
  getToday(): Promise<Composite | null>;
  getByDate(date: string): Promise<Composite | null>;
}
```

**Generate logic (nightly cron — critical)**:
```
1. Acquire pg_advisory_lock(hash of date string)
2. Check if composite already exists for this date → if yes, skip (idempotent)
3. Fetch prompt + all approved contributions for the date
4. If 0 contributions → create placeholder composite with message
5. Calculate grid dimensions: cols = ceil(sqrt(count)), rows = ceil(count/cols)
6. For each contribution:
   a. Download image from Blob
   b. Resize to tile size (e.g., 200x200)
7. Create composite canvas: cols * tileSize x rows * tileSize
8. Composite all tiles using Sharp
9. Generate OG image (1200x630 crop/fit)
10. Upload composite + OG to Vercel Blob
11. INSERT composite record
12. Invalidate Redis cache: composite:today
13. Release advisory lock
14. Log metrics: contribution_count, generation_time_ms, image_size_bytes
```

### 2.4 SessionService (`src/lib/services/session.service.ts`)

```typescript
interface SessionService {
  getOrCreate(request: Request): Promise<Session>;
  refresh(sessionId: string): Promise<void>;
  delete(sessionId: string): Promise<void>;  // GDPR
}
```

### 2.5 ModerationService (`src/lib/services/moderation.service.ts`)

```typescript
interface ModerationService {
  scan(imageBuffer: Buffer): Promise<ModerationResult>;
  isApproved(result: ModerationResult): boolean;
}
```

**Logic**: Call Cloud Vision `annotateImage` with `SAFE_SEARCH_DETECTION`. Reject if any category ≥ `LIKELY`.

---

## 3. Error Handling Strategy

```typescript
// Base application error
class AppError extends Error {
  constructor(
    public code: string,
    public statusCode: number,
    message: string,
    public details?: Record<string, unknown>
  ) {
    super(message);
  }
}

// Specific errors
class ValidationError extends AppError { /* 400 */ }
class NotFoundError extends AppError { /* 404 */ }
class DuplicateError extends AppError { /* 409 → returns existing */ }
class RateLimitError extends AppError { /* 429 */ }
class ModerationError extends AppError { /* 403 */ }
```

API routes catch errors and return consistent JSON:
```typescript
// In route handler
try {
  const result = await contributionService.submit(sessionId, input);
  return Response.json({ data: result }, { status: 201 });
} catch (error) {
  if (error instanceof AppError) {
    return Response.json({ error: { code: error.code, message: error.message, status: error.statusCode } }, { status: error.statusCode });
  }
  // Unexpected error — log and return 500
  console.error(error);
  return Response.json({ error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred', status: 500 } }, { status: 500 });
}
```

---

## 4. Validation Schemas (Zod)

```typescript
const contributionInputSchema = z.object({
  contentType: z.enum(['emoji', 'color', 'drawing']),
  contentData: z.union([
    z.object({ emoji: z.string().min(1).max(10), backgroundColor: z.string().regex(/^#[0-9A-Fa-f]{6}$/) }),
    z.object({ colors: z.array(z.string().regex(/^#[0-9A-Fa-f]{6}$/)).min(1).max(6), pattern: z.enum(['solid', 'gradient', 'mosaic']) }),
    z.object({ imageData: z.string().max(700000) })  // ~500KB base64
  ])
});
```

---

## 5. Background Jobs

| Job | Schedule | Function | Timeout |
|-----|----------|----------|---------|
| Composite generation | Daily 00:00 UTC | `src/app/api/cron/composite/route.ts` | 300s |
| Session cleanup | Weekly Sunday 03:00 UTC | `src/app/api/cron/cleanup/route.ts` | 60s |
| Prompt activation | Daily 00:00 UTC | Part of composite cron | — |

Configured in `vercel.json`:
```json
{
  "crons": [
    { "path": "/api/cron/composite", "schedule": "0 0 * * *" },
    { "path": "/api/cron/cleanup", "schedule": "0 3 * * 0" }
  ]
}
```
