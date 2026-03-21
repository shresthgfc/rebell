# Agent Registry

All officially defined sub-agents in this development organization.

---

## Phase 1: Discovery & Brainstorming

| Agent | File | Output | Key Standards |
|-------|------|--------|---------------|
| Requirements Analyst | `requirements-analyst.md` | `output/requirements.md` | IEEE 830, INVEST, MoSCoW |
| Market Researcher | `market-researcher.md` | `output/market-research.md` | SWOT, evidence-based |
| Brainstorm Facilitator | `brainstorm-facilitator.md` | `output/brainstorm.md` | SCAMPER, min 3 approaches |
| Devil's Advocate | `devil-advocate.md` | `output/risk-analysis.md` | Pre-mortem, FMEA |
| Innovation Scout | `innovation-scout.md` | `output/tech-radar.md` | ThoughtWorks Tech Radar |

## Phase 2: Architecture & Design

| Agent | File | Output | Key Standards |
|-------|------|--------|---------------|
| System Architect | `system-architect.md` | `output/architecture.md` | C4 model, ADRs |
| Database Architect | `database-architect.md` | `output/database-design.md` | CAP theorem, data classification |
| API Designer | `api-designer.md` | `output/api-design.md` | OpenAPI 3.1, RFC 7807 |
| Security Architect | `security-architect.md` | `output/security-design.md` | STRIDE, OWASP |
| UX Designer | `ux-designer.md` | `output/ux-design.md` | WCAG 2.1 AA, Nielsen |

## Phase 3: Implementation Planning

| Agent | File | Output | Key Standards |
|-------|------|--------|---------------|
| Tech Lead | `tech-lead.md` | `output/implementation-plan.md` | WBS, INVEST stories |
| Backend Developer | `backend-developer.md` | `output/backend-design.md` | Clean architecture, SOLID |
| Frontend Developer | `frontend-developer.md` | `output/frontend-design.md` | Core Web Vitals |
| DevOps Engineer | `devops-engineer.md` | `output/devops-design.md` | IaC, <5min rollback |
| Database Engineer | `database-engineer.md` | `output/database-implementation.md` | Reversible migrations |

## Phase 4: Quality Assurance

| Agent | File | Output | Key Standards |
|-------|------|--------|---------------|
| QA Lead | `qa-lead.md` | `output/qa-strategy.md` | Test pyramid, shift-left |
| Test Engineer | `test-engineer.md` | `output/test-cases.md` | BDD, boundary analysis |
| Performance Engineer | `performance-engineer.md` | `output/performance-plan.md` | SLAs, load scenarios |
| Security Auditor | `security-auditor.md` | `output/security-audit.md` | OWASP Top 10 |
| Accessibility Tester | `accessibility-tester.md` | `output/accessibility-audit.md` | WCAG 2.1 AA |

## Phase 5: Review & Delivery

| Agent | File | Output | Key Standards |
|-------|------|--------|---------------|
| Code Reviewer | `code-reviewer.md` | `output/code-review.md` | SOLID, quality score |
| Technical Writer | `technical-writer.md` | `output/documentation-plan.md` | Diátaxis framework |
| Release Manager | `release-manager.md` | `output/release-plan.md` | Go/no-go, <5min rollback |
| Stakeholder Liaison | `stakeholder-liaison.md` | `output/stakeholder-report.md` | Business language |

## Cross-Cutting Agents (run after every phase)

| Agent | File | Output | Authority |
|-------|------|--------|-----------|
| Governance Reviewer | `governance-reviewer.md` | `output/governance-review-phase-{N}.md` | **BLOCKING** — can halt pipeline |
| Standards Librarian | `standards-librarian.md` | `output/standards-review.md` | Advisory — flags inconsistencies |

## Meta-Agents

| Agent | File | Output | Purpose |
|-------|------|--------|---------|
| Orchestrator | `dev-org-orchestrator.md` | `output/FINAL-REPORT.md` | Runs full pipeline |
| Phase Synthesizer | `phase-synthesizer.md` | `output/phase-{N}-synthesis.md` | Merges phase outputs |
| Debate Moderator | `debate-moderator.md` | `output/debate-{topic}.md` | Adversarial debates |
