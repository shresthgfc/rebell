# Phase 3 — Database Engineer: Migration & Implementation Plan

## 1. Migration Scripts

### Migration 001: Create Users Table
```sql
-- 001_create_users.sql
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE,
    display_name TEXT,
    password_hash TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### Migration 002: Create Sessions Table
```sql
-- 002_create_sessions.sql
CREATE TABLE IF NOT EXISTS sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    fingerprint TEXT,
    session_token TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at TIMESTAMPTZ NOT NULL DEFAULT (now() + INTERVAL '30 days')
);

CREATE INDEX idx_sessions_token ON sessions (session_token);
CREATE INDEX idx_sessions_user ON sessions (user_id) WHERE user_id IS NOT NULL;
CREATE INDEX idx_sessions_expires ON sessions (expires_at);
```

### Migration 003: Create Prompts Table
```sql
-- 003_create_prompts.sql
CREATE TABLE IF NOT EXISTS prompts (
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

### Migration 004: Create Contributions Table
```sql
-- 004_create_contributions.sql
CREATE TABLE IF NOT EXISTS contributions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prompt_id UUID NOT NULL REFERENCES prompts(id),
    session_id UUID NOT NULL REFERENCES sessions(id),
    content_type TEXT NOT NULL CHECK (content_type IN ('emoji', 'color', 'drawing')),
    content_data JSONB NOT NULL,
    image_url TEXT,
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    grid_position INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (prompt_id, session_id)
);

CREATE INDEX idx_contributions_prompt ON contributions (prompt_id);
CREATE INDEX idx_contributions_prompt_status ON contributions (prompt_id, status);
CREATE INDEX idx_contributions_session ON contributions (session_id);
CREATE INDEX idx_contributions_created ON contributions (created_at);
```

### Migration 005: Create Composites Table
```sql
-- 005_create_composites.sql
CREATE TABLE IF NOT EXISTS composites (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prompt_id UUID NOT NULL UNIQUE REFERENCES prompts(id),
    image_url TEXT NOT NULL,
    og_image_url TEXT,
    contribution_count INTEGER NOT NULL DEFAULT 0,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_composites_created ON composites (created_at DESC);
```

### Migration 006: Seed Initial Prompts
```sql
-- 006_seed_initial_prompts.sql
INSERT INTO prompts (prompt_text, prompt_date, is_active) VALUES
    ('Express your morning mood using only colors', CURRENT_DATE, true),
    ('What does kindness look like to you?', CURRENT_DATE + 1, false),
    ('Draw something that makes you smile', CURRENT_DATE + 2, false),
    ('Show us your favorite season in one image', CURRENT_DATE + 3, false),
    ('What does your happy place look like?', CURRENT_DATE + 4, false),
    ('Express the sound of rain visually', CURRENT_DATE + 5, false),
    ('What color is today?', CURRENT_DATE + 6, false)
ON CONFLICT (prompt_date) DO NOTHING;
```

---

## 2. Drizzle Schema

```typescript
// src/lib/db/schema.ts
import { pgTable, uuid, text, date, boolean, timestamptz, integer, jsonb, unique } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: uuid('id').primaryKey().defaultRandom(),
  email: text('email').unique(),
  displayName: text('display_name'),
  passwordHash: text('password_hash'),
  createdAt: timestamptz('created_at').notNull().defaultNow(),
  updatedAt: timestamptz('updated_at').notNull().defaultNow(),
});

export const sessions = pgTable('sessions', {
  id: uuid('id').primaryKey().defaultRandom(),
  userId: uuid('user_id').references(() => users.id, { onDelete: 'set null' }),
  fingerprint: text('fingerprint'),
  sessionToken: text('session_token').notNull().unique(),
  createdAt: timestamptz('created_at').notNull().defaultNow(),
  expiresAt: timestamptz('expires_at').notNull(),
});

export const prompts = pgTable('prompts', {
  id: uuid('id').primaryKey().defaultRandom(),
  promptText: text('prompt_text').notNull(),
  promptDate: date('prompt_date').notNull().unique(),
  isActive: boolean('is_active').notNull().default(false),
  createdAt: timestamptz('created_at').notNull().defaultNow(),
  updatedAt: timestamptz('updated_at').notNull().defaultNow(),
});

export const contributions = pgTable('contributions', {
  id: uuid('id').primaryKey().defaultRandom(),
  promptId: uuid('prompt_id').notNull().references(() => prompts.id),
  sessionId: uuid('session_id').notNull().references(() => sessions.id),
  contentType: text('content_type').notNull(),
  contentData: jsonb('content_data').notNull(),
  imageUrl: text('image_url'),
  status: text('status').notNull().default('pending'),
  gridPosition: integer('grid_position'),
  createdAt: timestamptz('created_at').notNull().defaultNow(),
}, (table) => ({
  uniqueContribution: unique().on(table.promptId, table.sessionId),
}));

export const composites = pgTable('composites', {
  id: uuid('id').primaryKey().defaultRandom(),
  promptId: uuid('prompt_id').notNull().unique().references(() => prompts.id),
  imageUrl: text('image_url').notNull(),
  ogImageUrl: text('og_image_url'),
  contributionCount: integer('contribution_count').notNull().default(0),
  metadata: jsonb('metadata').default({}),
  createdAt: timestamptz('created_at').notNull().defaultNow(),
});
```

---

## 3. Connection Pooling

```typescript
// src/lib/db/client.ts
import { neon } from '@neondatabase/serverless';
import { drizzle } from 'drizzle-orm/neon-http';
import * as schema from './schema';

const sql = neon(process.env.DATABASE_URL!);
export const db = drizzle(sql, { schema });
```

Neon serverless driver handles connection pooling automatically — no PgBouncer needed. Each Vercel function invocation gets a fresh HTTP-based connection.

---

## 4. Query Performance Targets

| Query | Target | Index Used |
|-------|--------|------------|
| Get today's prompt | < 5ms | `idx_prompts_date` |
| Check existing contribution | < 5ms | `UNIQUE(prompt_id, session_id)` |
| Insert contribution | < 10ms | Primary key |
| Get all approved contributions for prompt | < 50ms | `idx_contributions_prompt_status` |
| Get composite by prompt | < 5ms | `UNIQUE(composites.prompt_id)` |
| Session lookup by token | < 5ms | `UNIQUE(sessions.session_token)` |

---

## 5. Data Seeding for Development

```typescript
// scripts/seed-dev.ts
// Seeds 30 days of prompts + fake contributions for testing composite generation
async function seedDev() {
  // Insert 30 prompts
  for (let i = 0; i < 30; i++) {
    const date = new Date();
    date.setDate(date.getDate() + i);
    await db.insert(prompts).values({
      promptText: SAMPLE_PROMPTS[i % SAMPLE_PROMPTS.length],
      promptDate: date.toISOString().split('T')[0],
      isActive: i === 0,
    }).onConflictDoNothing();
  }

  // Create test session
  const session = await db.insert(sessions).values({
    sessionToken: 'dev-test-session',
    expiresAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
  }).returning();

  // Insert sample contributions for today
  const todayPrompt = await db.query.prompts.findFirst({
    where: eq(prompts.isActive, true),
  });

  if (todayPrompt) {
    for (let i = 0; i < 20; i++) {
      await db.insert(contributions).values({
        promptId: todayPrompt.id,
        sessionId: session[0].id,
        contentType: 'color',
        contentData: { colors: [randomColor()], pattern: 'solid' },
        status: 'approved',
      }).onConflictDoNothing();
    }
  }
}
```
