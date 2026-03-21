# Phase 3 — Tech Lead: Sprint Plan & Standards

## 1. Sprint Breakdown (8-Week MVP)

### Sprint 1 (Weeks 1–2): Foundation
| Story | Points | Priority |
|-------|--------|----------|
| Project scaffolding: Next.js 15, TypeScript, Drizzle, Tailwind | 3 | P0 |
| Database setup: Neon connection, migrations 001-005, seed prompts | 5 | P0 |
| Session middleware: anonymous session cookie issuance | 3 | P0 |
| GET /api/prompts/today endpoint + Redis cache | 2 | P0 |
| Mobile-first landing page with prompt display | 3 | P0 |
| **Sprint 1 prototype**: Simple creation tool (emoji/color picker) | 5 | P0 |
| **Total**: 21 points | | |

### Sprint 2 (Weeks 3–4): Core Creation Flow
| Story | Points | Priority |
|-------|--------|----------|
| POST /api/contributions endpoint with idempotency | 5 | P0 |
| Image generation from emoji/color contributions (Sharp) | 5 | P0 |
| Vercel Blob integration for contribution storage | 3 | P0 |
| Advanced creation tool: drawing canvas (Fabric.js) | 8 | P0 |
| Preview + submit flow | 3 | P0 |
| **Total**: 24 points | | |

### Sprint 3 (Weeks 5–6): Composite Pipeline + Sharing
| Story | Points | Priority |
|-------|--------|----------|
| Nightly composite generation cron job | 8 | P0 |
| Composite viewer page with zoom | 5 | P0 |
| Share page with OG meta tags + image generation | 5 | P0 |
| Social share buttons (Twitter, Facebook, copy link) | 3 | P0 |
| Content moderation: Cloud Vision integration | 5 | P1 |
| **Total**: 26 points | | |

### Sprint 4 (Weeks 7–8): Polish + Launch
| Story | Points | Priority |
|-------|--------|----------|
| Error handling + loading states across all pages | 3 | P0 |
| Rate limiting implementation | 2 | P0 |
| Admin panel: prompt management + moderation queue | 5 | P1 |
| Micro-interactions: submit animation, counter pulse | 3 | P1 |
| Performance optimization: Core Web Vitals | 3 | P1 |
| Accessibility audit + fixes | 3 | P1 |
| Seed 7 days of prompts for launch | 1 | P0 |
| Production deployment + monitoring setup | 3 | P0 |
| **Total**: 23 points | | |

---

## 2. Coding Standards

### TypeScript
- Strict mode enabled (`"strict": true`)
- No `any` types — use `unknown` + type guards
- Zod for runtime validation at API boundaries
- Path aliases: `@/components`, `@/lib`, `@/db`

### React / Next.js
- Server Components by default; `'use client'` only when needed
- Collocated styles via Tailwind CSS utility classes
- No barrel exports — import directly from component files
- Error boundaries for each major page section

### File Naming
- Components: `PascalCase.tsx` (e.g., `CreationTool.tsx`)
- Utilities: `camelCase.ts` (e.g., `generateComposite.ts`)
- API routes: `route.ts` inside App Router directories
- Database: `schema.ts`, `migrations/*.sql`

### Git
- Branch naming: `feat/`, `fix/`, `chore/` prefixes
- Commit messages: Conventional Commits (`feat:`, `fix:`, `chore:`)
- PR required for main branch; CI must pass
- Squash merge to main

---

## 3. Project Structure

```
mosaic/
├── src/
│   ├── app/
│   │   ├── layout.tsx              # Root layout
│   │   ├── page.tsx                # Homepage (daily prompt)
│   │   ├── create/
│   │   │   └── page.tsx            # Creation tool
│   │   ├── piece/[id]/
│   │   │   └── page.tsx            # Individual share page
│   │   ├── mosaic/[date]/
│   │   │   └── page.tsx            # Composite view
│   │   └── api/
│   │       ├── prompts/today/route.ts
│   │       ├── contributions/route.ts
│   │       ├── contributions/[id]/route.ts
│   │       ├── composites/today/route.ts
│   │       ├── composites/[date]/route.ts
│   │       └── admin/
│   │           ├── prompts/route.ts
│   │           └── moderate/[id]/route.ts
│   ├── components/
│   │   ├── CreationTool/
│   │   │   ├── SimpleMode.tsx
│   │   │   ├── AdvancedMode.tsx
│   │   │   └── ModeToggle.tsx
│   │   ├── ShareCard.tsx
│   │   ├── MosaicViewer.tsx
│   │   ├── PromptCard.tsx
│   │   └── LiveCounter.tsx
│   ├── lib/
│   │   ├── db/
│   │   │   ├── schema.ts           # Drizzle schema
│   │   │   ├── client.ts           # DB connection
│   │   │   └── migrations/
│   │   ├── redis.ts                # Upstash client
│   │   ├── blob.ts                 # Vercel Blob helpers
│   │   ├── session.ts              # Session management
│   │   ├── moderation.ts           # Cloud Vision integration
│   │   ├── composite.ts            # Composite generation logic
│   │   └── validation.ts           # Zod schemas
│   └── middleware.ts               # Session + security headers
├── public/
│   └── og-default.png              # Default OG image
├── drizzle.config.ts
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

---

## 4. Definition of Done

A story is done when:
1. Code is written and passes TypeScript strict checks
2. Unit tests cover core logic (>80% for lib/ functions)
3. API endpoints have integration tests
4. Responsive design verified on mobile (375px) and desktop (1280px)
5. PR reviewed and approved
6. Deployed to preview environment without errors
7. Accessibility: keyboard navigable, no axe-core violations
