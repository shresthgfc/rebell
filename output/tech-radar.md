# Technology Radar — Interactive Creative Web Experience ("Mosaic")

## 1. Context
- **Project**: Daily creative prompt platform with collective composite generation and shareable artifacts
- **Team profile**: Small (2–5 developers); assumed full-stack JavaScript/TypeScript proficiency; no assumed expertise in specialized domains (WebGL, audio synthesis, native mobile)
- **Timeline**: 8–12 weeks to MVP
- **Budget**: Medium-tier startup (~$50K–$150K total project cost)
- **Key technical problems to solve**:
  1. In-browser creative input tool (drawing, emoji, color selection)
  2. Nightly composite image generation (batch processing, image manipulation)
  3. Shareable artifact generation (unique URLs, OG image generation)
  4. Community gallery with pagination and search
  5. User authentication and profiles
  6. Admin moderation panel
  7. Optional: AI-assisted creative suggestions
- **Knowledge cutoff note**: Research based on known tech landscape through Aug 2025; current version numbers and community stats are estimates and require validation at project start.

---

## 2. Tech Radar

### ADOPT (use in production)

| Technology | Category | Solves What Problem | Evidence | Risk |
|-----------|----------|-------------------|---------|------|
| Next.js 15 (App Router) | FW | Full-stack React framework: SSR for SEO on landing/gallery pages; API routes for backend; excellent Vercel deployment integration | Industry standard for React full-stack as of 2025; thousands of production deployments; strong TypeScript support | Low |
| TypeScript 5.x | LR | Type safety across frontend and backend reduces runtime errors; critical for a small team with no dedicated QA on every PR | Universal adoption in modern JavaScript projects; eliminates entire classes of bugs | Low |
| PostgreSQL 16 | DB | Primary relational database: user accounts, daily prompts, contributions, gallery metadata | Gold-standard open-source RDBMS; excellent JSON support; strong ecosystem (Prisma, Drizzle) | Low |
| Prisma ORM | LIB | Type-safe database access; automatic migration management; reduces SQL error surface | Dominant ORM for TypeScript/Node.js; active development; wide adoption | Low |
| Redis 7 | DB | Session caching, rate limiting, daily contribution tracking (prevent double submission), job queue for composite generation | Industry standard in-memory store; extremely mature; Upstash for serverless | Low |
| Vercel | INF | Deployment platform: edge CDN, auto-scaling, preview deployments, zero DevOps overhead for small team | Purpose-built for Next.js; excellent free tier; automatic SSL; global edge network | Low |
| Tailwind CSS 4 | FW | Utility-first CSS; fast UI development; consistent design system without CSS architecture overhead | Near-universal adoption in 2025 modern web; strong tooling; purges unused CSS | Low |
| Zod | LIB | Schema validation at API boundaries and form inputs; TypeScript-native; integrates with React Hook Form | Standard validation library for TypeScript ecosystems | Low |
| React Hook Form | LIB | Form state management with excellent performance (no unnecessary re-renders); Zod integration | Most popular React form library by download count; minimal boilerplate | Low |
| Resend (email) | LIB | Transactional email delivery: registration confirmation, password reset, daily digest | Modern developer-first email API; excellent TypeScript SDK; generous free tier | Low |
| Sharp (image processing) | LIB | Server-side image manipulation for composite generation; resize, composite, format conversion | Industry-leading Node.js image processing; used in production at major sites | Low |
| Cloudflare R2 / AWS S3 | INF | Object storage for daily composite images, user contribution artifacts, OG images | Standard object storage; R2 has zero egress fees (significant at scale); S3 is universal standard | Low |
| NextAuth.js (Auth.js) | LIB | Authentication: email/password + OAuth (Google, GitHub); session management; database adapter for Prisma | Standard auth library for Next.js; handles JWT and session cookies; reduces security surface | Low |

### TRIAL (use in non-critical paths)

| Technology | Category | Solves What Problem | Fallback | Risk |
|-----------|----------|-------------------|---------|------|
| Fabric.js (canvas library) | LIB | In-browser drawing tool: HTML5 Canvas abstraction for the creative input tool; handles touch, mouse, object manipulation | Fall back to direct Canvas API with a simpler drawing implementation; or remove drawing in favor of emoji/color picker (lower skill barrier) | Medium — library is mature but maintained by a small team; check GitHub activity before committing |
| BullMQ (job queue) | LIB | Background job queue for nightly composite generation and OG image creation; Redis-backed | Vercel Cron + direct function execution (works for up to 5-minute jobs; may timeout for large batch composite generation) | Medium — adds Redis dependency for queuing; but Redis is already in ADOPT |
| TanStack Query (React Query) | LIB | Server state management on the frontend: gallery pagination, real-time updates, caching | SWR (simpler, also excellent, mature) | Low-Medium — TanStack Query is very mature; TRIAL because team may prefer SWR's simpler API |
| Playwright | DT | E2E and cross-browser automated testing | Cypress (well-established alternative; slightly larger bundle overhead for test runner) | Low — both are excellent; TRIAL because test suite setup takes time the small team may not have in MVP |
| Sentry | OBS | Error monitoring and performance tracking in production | Datadog (higher cost); LogRocket (different focus) | Low — Sentry is near-universal; TRIAL because it requires setup and configuration investment |

### ASSESS (spike/POC only)

| Technology | Category | Why Interesting | Validation Needed | Fallback |
|-----------|----------|----------------|-------------------|---------|
| Claude API (Anthropic) for AI creative suggestions | AI | AI-assisted creative prompt suggestions: "I don't know what to draw" helper; generates a starting sketch description or color palette | Validate API latency for interactive use (< 2s acceptable); validate cost per 1,000 requests against budget; validate output quality for creative prompts | Anthropic Claude API is production-ready in general but its specific use in creative hint generation for this context needs a spike; Fallback: OpenAI GPT-4o-mini (similar capability, competitive pricing) |
| Stable Diffusion (local/API) for contribution enhancement | AI | Transform simple user sketches into polished AI artwork; dramatically improves composite visual quality | Assess: latency acceptable for UX? Cost per generation sustainable? Legal/copyright implications of user sketch → AI art transformation? | Stability AI API or Replicate.com (Fallback: skip AI enhancement entirely; raw user contributions are the authentic value) |
| Liveblocks (real-time collaboration) | LIB | If a real-time "live contributions" view is added to the gallery | Assess API cost at scale; assess WebSocket server management overhead | Standard WebSocket with Redis pub/sub (ADOPT-level fallback) |

### HOLD (do not use)

| Technology | Category | Why Not Now | Watch For |
|-----------|----------|-----------|-----------|
| Three.js / WebGL for 3D gallery | FW | Moonshot only — far exceeds team capability and timeline for MVP; mobile performance risk is critical given 60%+ mobile traffic | Watch if WebGPU + WebGL performance on mobile improves significantly by v2 |
| Web Audio API for generative sound | LIB | Approach C (Sound Portrait) was not selected for MVP; complex implementation with no team experience flagged | Potential v2 feature if concept evolves toward audio |
| Remix (web framework) | FW | Next.js App Router has converged on a similar progressive enhancement model; switching cost not justified for this project | Remix's web-standards approach is conceptually strong; revisit if Next.js introduces significant breaking changes |
| Supabase (hosted Postgres + Auth + Realtime) | INF | Appealing all-in-one but introduces vendor lock-in on auth, database, and realtime; separating concerns with Vercel + Prisma + NextAuth + Redis gives better long-term flexibility | Supabase Realtime is useful — reassess for v2 if real-time features are added |
| MongoDB | DB | No clear advantage over PostgreSQL for this relational data model; JSON documents can be stored in PostgreSQL JSONB; schemaless brings consistency risks | N/A for this project |

---

## 3. AI/ML Integration Opportunities

| Opportunity | Specific Value | Implementation Approach | Cost Estimate | Risk |
|------------|---------------|----------------------|--------------|------|
| Daily prompt generation assistance | Automate prompt curation to reduce ongoing operational cost; generate variety and novelty over time | Claude API: batch generate 30–50 prompts per request; human curator selects/edits; store prompt bank | ~$0.02–$0.05 per generation session; effectively free at low frequency | Low — AI used for content generation, not real-time interaction; can be done offline |
| "I need help" creative starter | When user clicks "inspire me," generate a specific, concrete starting suggestion ("Try drawing a house made of books") | Claude API: streaming response on button click; 1–2 second latency acceptable | ~$0.001 per request; at 10K requests/day = ~$10/day = ~$300/month | Medium — budget dependency; rate limit per user required |
| AI-powered content moderation supplement | Augment human moderation with AI classification of potentially inappropriate content | Google Cloud Vision SafeSearch (existing specialized API) or AWS Rekognition | $1.50 per 1,000 images; at 10K submissions/day = $15/day = ~$450/month | Low — specialized computer vision API is well-suited; has fallback (human moderation) |
| Composite quality enhancement | Use AI image upscaling or style-transfer to improve the visual quality of the daily composite before publishing | Replicate.com API (ESRGAN upscaling); applied once per day during composite generation | ~$0.01–$0.05 per composite generation; negligible cost | Medium (ASSESS-level) — quality improvement is nice-to-have; adds latency to nightly job; defer to v2 |

---

## 4. Open Source Recommendations

| Need | Recommendation | License | Stars/Activity | Maintenance Risk | Alternative |
|------|---------------|---------|---------------|-----------------|-------------|
| In-browser drawing | Fabric.js v6 | MIT | ~28K stars, active PRs as of 2025 | Low-Medium (small maintainer team) | Konva.js (also MIT, strong React integration) |
| Image processing | Sharp (Node.js) | Apache 2.0 | ~28K stars, highly active | Low (backed by Lovell Fuller; used at scale) | Jimp (pure JavaScript, slower but no native dependencies) |
| Email templates | react-email | MIT | ~14K stars, active | Low (Resend team maintains it) | MJML (older, battle-tested) |
| Scheduled tasks | BullMQ | MIT | ~6K stars, active | Low-Medium (small team, but widely used) | Vercel Cron (zero-dependency but limited to 1-minute max execution for hobby tier) |
| Analytics (self-hosted option) | Plausible CE | AGPL | ~20K stars | Low | PostHog (more powerful, more complex) |

---

## 5. Build vs Buy Analysis

| Component | Build (Cost/Time/Risk) | Buy (Cost/Vendor Lock-in/Risk) | Recommendation | Reasoning |
|-----------|----------------------|-------------------------------|----------------|-----------|
| Authentication | 2–4 weeks, medium security risk | Auth.js: free, MIT, minimal lock-in | **Buy** (Auth.js) | Auth is a security-critical component; rolling custom auth in 8-week timeline is high risk |
| Email delivery | 1–2 days plumbing, medium deliverability risk | Resend: free tier covers launch; ~$20/mo at 50K emails | **Buy** (Resend) | Email deliverability is a solved problem; SES/Resend handle domain reputation |
| Image composite generation | 1–2 weeks, low-medium risk with Sharp | No direct buy option for this specific use case | **Build** | Custom business logic; Sharp (open source) handles the image operations; this is core IP |
| In-browser drawing tool | 3–5 weeks custom, or 1–2 weeks with Fabric.js | Figma/Canva: completely wrong product category | **Build** with Fabric.js | Core UX must be purpose-built for the concept; Fabric.js reduces raw Canvas API work significantly |
| Content moderation | 3–4 weeks for basic rule engine; complex ML = months | Google Vision SafeSearch: $1.50/1K images; AWS Rekognition: similar | **Buy** (Cloud Vision) | Safety-critical; specialized AI models significantly outperform heuristics; cost is manageable |
| Search / gallery pagination | 1–2 days (PostgreSQL full-text search for MVP) | Algolia/Meilisearch | **Build for MVP** (PostgreSQL FTS) | MVP search needs are simple; defer Algolia until search quality is a stated user pain point |
| Infrastructure / CI/CD | 1–2 weeks full setup | Vercel: free to $20/mo for pro | **Buy** (Vercel) | Small team cannot afford DevOps overhead; Vercel's zero-config is the correct trade-off |

---

## 6. Developer Experience

| Area | Current Pain (for a small team) | Recommendation | Impact |
|------|--------------------------------|---------------|--------|
| Local development environment | Setting up PostgreSQL + Redis locally is friction-heavy | Use Docker Compose for local dev (postgres + redis services with one command) | Reduces new developer onboarding from 1 day to 30 minutes |
| Type safety across API boundary | Frontend and backend can drift on data shapes | Use tRPC or Zod-inferred types shared between Next.js API routes and React components | Eliminates runtime type mismatch errors; large DX improvement |
| Image processing debugging | Sharp pipeline failures are hard to debug in production | Add verbose logging + local test harness for composite generation before deployment | Reduces debugging time for the most critical nightly job |
| Environment configuration | Scattered .env variables across services | Use a structured config schema with Zod validation at startup; fail fast if required env vars are missing | Prevents "missing env variable" production bugs |

---

## 7. Adoption Risk Assessment

| Technology | Learning Curve | Migration Effort | Rollback Difficulty | Team Readiness |
|-----------|---------------|-----------------|-------------------|---------------|
| Next.js 15 App Router | Medium (App Router is newer pattern vs Pages Router) | Low (new project) | Low (can fall back to Pages Router if needed) | High (assumed React familiarity) |
| Prisma | Low (excellent docs, TypeScript-native) | N/A (greenfield) | Medium (can switch to Drizzle; migration is doable) | High |
| Fabric.js | Medium (custom event model; Canvas API quirks) | Low (isolated to drawing component) | Medium (replace with emoji/color picker if too complex) | Medium — recommend spike in week 1 |
| BullMQ | Medium (queue concepts, Redis integration) | Low (can start with Vercel Cron) | Low (can switch to Vercel Cron for MVP) | Medium |
| Auth.js | Low-Medium (config-heavy but well-documented) | N/A (greenfield) | Low (can swap adapters) | Medium |
| TanStack Query | Medium (caching concepts; devtools help) | N/A (greenfield) | Low (SWR is near-equivalent) | Medium-High |

---

## 8. Unknowns & Validation Needed

| # | Technology | What Needs Validation | Suggested Approach |
|---|-----------|----------------------|-------------------|
| 1 | Fabric.js v6 | Performance on low-end Android with a complex canvas; touch event handling quality | Spike in week 1: build minimal drawing component; test on Samsung Galaxy A-series (representative low-end Android) |
| 2 | Sharp composite generation | Memory usage when compositing 1,000+ small images into a single output; timing under load | Benchmark locally: generate composite from 500, 1,000, 5,000 inputs; measure peak memory and duration |
| 3 | Claude API for creative hints | Latency for interactive "inspire me" button (must be < 2s p95); cost at target usage rate | API spike: test with 50 representative prompts; measure latency and token consumption |
| 4 | Google Cloud Vision SafeSearch | Accuracy for creative/artistic inputs (low-resolution pixel drawings may have poor classification accuracy) | Test with 100 sample contributions including edge cases; measure false positive rate |
| 5 | Vercel cron + BullMQ | Whether Vercel's serverless architecture can handle a 60-second composite generation job; Pro plan cron limits | Test composite generation on Vercel; if timeout, move to BullMQ on a dedicated worker (Fly.io or Railway) |
