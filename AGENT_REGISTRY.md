# Agent Registry

All 29 officially defined sub-agents in this development organization.

**Total agents:** 29 | **Total lines:** 7,214 | **All agents pass 7-section depth audit**

---

## Governance Standard

Every agent has these 7 mandatory sections:
1. `# Role` — Specialist identity and boundaries
2. `# Primary objectives` — Numbered deliverables
3. `# Non-negotiable rules` — Hard constraints
4. `# Entity taxonomy` — Classification system
5. `# Standard output structure` — Exact markdown template
6. `# Quality gates` — Completion checklist
7. `# Absolute prohibitions` — "Never:" list

---

## Phase 1: Discovery & Brainstorming

| Agent | File | Lines | Output | Key Standards |
|-------|------|-------|--------|---------------|
| Requirements Analyst | `requirements-analyst.md` | 172 | `output/requirements.md` | IEEE 830, INVEST, MoSCoW |
| Market Researcher | `market-researcher.md` | 168 | `output/market-research.md` | SWOT, evidence-based personas |
| Brainstorm Facilitator | `brainstorm-facilitator.md` | 144 | `output/brainstorm.md` | SCAMPER, min 3 approaches + moonshot |
| Devil's Advocate | `devil-advocate.md` | 182 | `output/risk-analysis.md` | Pre-mortem, FMEA, quantified risk matrix |
| Innovation Scout | `innovation-scout.md` | 156 | `output/tech-radar.md` | ThoughtWorks Tech Radar, fallback mandate |

## Phase 2: Architecture & Design

| Agent | File | Lines | Output | Key Standards |
|-------|------|-------|--------|---------------|
| System Architect | `system-architect.md` | 264 | `output/architecture.md` | C4 model (4 levels), ADRs, boring tech |
| Database Architect | `database-architect.md` | 262 | `output/database-design.md` | CAP trade-offs, data classification T1-T4 |
| API Designer | `api-designer.md` | 338 | `output/api-design.md` | OpenAPI 3.1, RFC 7807, idempotency keys |
| Security Architect | `security-architect.md` | 332 | `output/security-design.md` | STRIDE per component, zero-trust, encryption |
| UX Designer | `ux-designer.md` | 397 | `output/ux-design.md` | WCAG 2.1 AA, 9 mandatory states, design tokens |

## Phase 3: Implementation Planning

| Agent | File | Lines | Output | Key Standards |
|-------|------|-------|--------|---------------|
| Tech Lead | `tech-lead.md` | 269 | `output/implementation-plan.md` | 1-3 day tasks, INVEST stories, sprint 0 |
| Backend Developer | `backend-developer.md` | 280 | `output/backend-design.md` | Clean architecture, SOLID, error hierarchy |
| Frontend Developer | `frontend-developer.md` | 274 | `output/frontend-design.md` | Component taxonomy (7 types), Core Web Vitals |
| DevOps Engineer | `devops-engineer.md` | 305 | `output/devops-design.md` | 10 CI stages, <5min rollback, cost estimation |
| Database Engineer | `database-engineer.md` | 301 | `output/database-implementation.md` | Reversible migrations, index justification |

## Phase 4: Quality Assurance

| Agent | File | Lines | Output | Key Standards |
|-------|------|-------|--------|---------------|
| QA Lead | `qa-lead.md` | 212 | `output/qa-strategy.md` | Test pyramid (70/20/10), 7 quality gates |
| Test Engineer | `test-engineer.md` | 243 | `output/test-cases.md` | BDD Given/When/Then, boundary analysis |
| Performance Engineer | `performance-engineer.md` | 244 | `output/performance-plan.md` | 4 load scenarios, SLA with percentiles |
| Security Auditor | `security-auditor.md` | 247 | `output/security-audit.md` | All 10 OWASP Top 10, CVSS severity |
| Accessibility Tester | `accessibility-tester.md` | 237 | `output/accessibility-audit.md` | Full WCAG 2.1 AA, 3 screen readers |

## Phase 5: Review & Delivery

| Agent | File | Lines | Output | Key Standards |
|-------|------|-------|--------|---------------|
| Code Reviewer | `code-reviewer.md` | 248 | `output/code-review.md` | Quality score 1-10, SOLID, severity taxonomy |
| Technical Writer | `technical-writer.md` | 257 | `output/documentation-plan.md` | Diátaxis framework, P0-P3, runbook template |
| Release Manager | `release-manager.md` | 283 | `output/release-plan.md` | Go/no-go checklist, <5min rollback, flags |
| Stakeholder Liaison | `stakeholder-liaison.md` | 258 | `output/stakeholder-report.md` | No-jargon rule, ROI framework |

## Cross-Cutting Agents

| Agent | File | Lines | Output | Authority |
|-------|------|-------|--------|-----------|
| Governance Reviewer | `governance-reviewer.md` | 251 | `output/governance-review-phase-{N}.md` | **BLOCKING** — can halt pipeline |
| Standards Librarian | `standards-librarian.md` | 264 | `output/standards-review.md` | Advisory — flags inconsistencies |

## Meta-Agents

| Agent | File | Lines | Output | Purpose |
|-------|------|-------|--------|---------|
| Orchestrator | `dev-org-orchestrator.md` | 299 | `output/FINAL-REPORT.md` | Runs full 5-phase pipeline |
| Phase Synthesizer | `phase-synthesizer.md` | 134 | `output/phase-{N}-synthesis.md` | Merges phase outputs |
| Debate Moderator | `debate-moderator.md` | 193 | `output/debate-{topic}.md` | 4-round adversarial debates |
