# Phase 2 — Database Architecture: Mosaic

## 1. Overview

PostgreSQL (Neon serverless) with Drizzle ORM. Designed around the daily lifecycle: prompt → contributions → composite.

---

## 2. Entity-Relationship Diagram

```mermaid
erDiagram
    PROMPTS ||--o{ CONTRIBUTIONS : "has many"
    PROMPTS ||--o| COMPOSITES : "produces one"
    SESSIONS ||--o{ CONTRIBUTIONS : "creates"
    USERS ||--o| SESSIONS : "owns (optional)"

    PROMPTS {
        uuid id PK
        text prompt_text
        date prompt_date UK
        boolean is_active
        timestamp created_at
        timestamp updated_at
    }

    SESSIONS {
        uuid id PK
        uuid user_id FK "nullable"
        text fingerprint
        text session_token UK
        timestamp created_at
        timestamp expires_at
    }

    USERS {
        uuid id PK
        text email UK
        text display_name
        text password_hash "nullable - social auth"
        timestamp created_at
        timestamp updated_at
    }

    CONTRIBUTIONS {
        uuid id PK
        uuid prompt_id FK
        uuid session_id FK
        text content_type "emoji | color | drawing"
        jsonb content_data "type-specific payload"
        text image_url "Vercel Blob URL"
        text status "pending | approved | rejected"
        integer grid_position "assigned during composite gen"
        timestamp created_at
    }

    COMPOSITES {
        uuid id PK
        uuid prompt_id FK UK
        text image_url "composite image URL"
        text og_image_url "1200x630 OG image"
        integer contribution_count
        jsonb metadata "grid dimensions, generation stats"
        timestamp created_at
    }
```

---

## 3. Table Definitions

### 3.1 prompts
```sql
CREATE TABLE prompts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prompt_text TEXT NOT NULL,
    prompt_date DATE NOT NULL UNIQUE,
    is_active BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_prompts_date ON prompts (prompt_date);
CREATE INDEX idx_prompts_active ON prompts (is_active) WHERE is_active = true;
```

### 3.2 sessions
```sql
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    fingerprint TEXT,
    session_token TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at TIMESTAMPTZ NOT NULL DEFAULT (now() + INTERVAL '30 days')
);

CREATE INDEX idx_sessions_token ON sessions (session_token);
CREATE INDEX idx_sessions_user ON sessions (user_id) WHERE user_id IS NOT NULL;
```

### 3.3 users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE,
    display_name TEXT,
    password_hash TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### 3.4 contributions
```sql
CREATE TABLE contributions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prompt_id UUID NOT NULL REFERENCES prompts(id),
    session_id UUID NOT NULL REFERENCES sessions(id),
    content_type TEXT NOT NULL CHECK (content_type IN ('emoji', 'color', 'drawing')),
    content_data JSONB NOT NULL,
    image_url TEXT,
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    grid_position INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (prompt_id, session_id)  -- one contribution per session per prompt
);

CREATE INDEX idx_contributions_prompt ON contributions (prompt_id);
CREATE INDEX idx_contributions_prompt_status ON contributions (prompt_id, status);
CREATE INDEX idx_contributions_session ON contributions (session_id);
CREATE INDEX idx_contributions_created ON contributions (created_at);
```

### 3.5 composites
```sql
CREATE TABLE composites (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prompt_id UUID NOT NULL UNIQUE REFERENCES prompts(id),
    image_url TEXT NOT NULL,
    og_image_url TEXT,
    contribution_count INTEGER NOT NULL DEFAULT 0,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_composites_prompt ON composites (prompt_id);
```

---

## 4. Key Constraints

| Constraint | Type | Purpose |
|-----------|------|---------|
| `contributions(prompt_id, session_id) UNIQUE` | Business invariant | One contribution per user per day |
| `prompts(prompt_date) UNIQUE` | Business invariant | One prompt per day |
| `composites(prompt_id) UNIQUE` | Business invariant | One composite per prompt |
| `contributions.content_type CHECK` | Data integrity | Only valid content types |
| `contributions.status CHECK` | Data integrity | Only valid statuses |

---

## 5. Migration Plan

```
migrations/
├── 001_create_users.sql
├── 002_create_sessions.sql
├── 003_create_prompts.sql
├── 004_create_contributions.sql
├── 005_create_composites.sql
├── 006_seed_initial_prompts.sql
```

Using Drizzle Kit for migration generation and execution. All migrations are forward-only, versioned, and idempotent.

---

## 6. Data Lifecycle

```
Day N (any time):
  1. Prompt for Day N is active (set by cron or pre-seeded)
  2. Users submit contributions → status: pending
  3. Auto-moderation runs → status: approved/rejected

Day N → N+1 transition (00:00 UTC):
  1. Cron fetches all approved contributions for Day N
  2. Generates composite image
  3. Stores composite record
  4. Day N+1 prompt becomes active

Retention:
  - Contributions: Retained indefinitely (shareable URLs)
  - Composites: Retained indefinitely (public gallery in v1.1)
  - Sessions: Expired sessions purged after 90 days
  - Rejected contributions: Purged after 30 days
```

---

## 7. GDPR Compliance

| Requirement | Implementation |
|------------|----------------|
| **Lawful basis** | Legitimate interest (anonymous); Consent (registered) |
| **Data minimization** | Anonymous sessions store no PII; only email for registered |
| **Right to erasure** | DELETE /api/account → cascade delete user, unlink sessions, anonymize contributions |
| **Right to export** | GET /api/account/export → JSON dump of user data + contribution URLs |
| **Data retention** | Sessions: 90 days; Rejected content: 30 days; Accounts: until deletion |
| **Cookie consent** | Session cookie is functional (exempt); analytics cookie requires consent |

---

## 8. Backup & Recovery

- **Neon**: Automatic point-in-time recovery (PITR) with 7-day retention
- **Vercel Blob**: Built-in redundancy, no backup needed
- **RPO**: < 1 hour (Neon continuous archiving)
- **RTO**: < 15 minutes (Neon branch restore)
