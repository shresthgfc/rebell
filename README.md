# REBELL — Multi-Agent Dev Org for Claude Code

A complete software development organization as **27 native Claude Code sub-agents**. Drop the `.claude/agents/` folder into any project and run the entire dev lifecycle from your terminal.

No Python. No API keys. No dependencies. Just `claude`.

## How It Works

```
You: "@dev-org-orchestrator Build a SaaS project management platform"

Orchestrator runs 5 phases, each with specialist sub-agents:

Phase 1: Discovery ──→ Phase 2: Architecture ──→ Phase 3: Implementation
  requirements-analyst    system-architect           tech-lead
  market-researcher       database-architect         backend-developer
  brainstorm-facilitator  api-designer               frontend-developer
  devil-advocate          security-architect         devops-engineer
  innovation-scout        ux-designer                database-engineer
        │                       │                          │
        ▼                       ▼                          ▼
Phase 4: QA ─────────→ Phase 5: Review ──────→ FINAL-REPORT.md
  qa-lead                  code-reviewer
  test-engineer            technical-writer
  performance-engineer     release-manager
  security-auditor         stakeholder-liaison
  accessibility-tester
```

Each sub-agent writes its output to `output/`. Downstream agents read upstream outputs, so knowledge accumulates through the pipeline.

## Setup

```bash
# Clone into any project
cp -r .claude/agents/ /path/to/your/project/.claude/agents/

# Or clone the whole repo
git clone https://github.com/shresthgfc/rebell.git
cd rebell
```

That's it. The agents are now available in Claude Code for that project.

## Usage

### Run the Full Pipeline
```bash
claude "@dev-org-orchestrator Build a real-time collaboration platform with 10k concurrent users"
```

This runs all 24 specialist agents through 5 phases and produces a complete project plan in `output/`.

### Run Individual Agents
```bash
# Analyze requirements
claude "@requirements-analyst Here are my client requirements: ..."

# Design the architecture
claude "@system-architect Design a system for: ..."

# Get a security audit
claude "@security-auditor Review the security of this design"

# Challenge assumptions
claude "@devil-advocate Find flaws in this proposal: ..."

# Run a debate between agents
claude "@debate-moderator Debate: monolith vs microservices for this project. Participants: system-architect, devops-engineer, backend-developer"
```

### Run a Specific Phase
```bash
# Just discovery
claude "@requirements-analyst [requirements]"
claude "@market-researcher Analyze the market for this"
claude "@devil-advocate Challenge the requirements"

# Just architecture
claude "@system-architect Design the system"
claude "@database-architect Design the data layer"
claude "@security-architect Design the security model"
```

### Use Session-Wide
```bash
# Start a session as the orchestrator
claude --agent dev-org-orchestrator
```

## The 27 Sub-Agents

| # | Agent | Phase | Specialty |
|---|-------|-------|-----------|
| 1 | `requirements-analyst` | Discovery | IEEE 830 requirements, MoSCoW |
| 2 | `market-researcher` | Discovery | SWOT, competitors, personas |
| 3 | `brainstorm-facilitator` | Discovery | SCAMPER, divergent solutions |
| 4 | `devil-advocate` | Discovery | Pre-mortem, risk analysis |
| 5 | `innovation-scout` | Discovery | Tech Radar, build-vs-buy |
| 6 | `system-architect` | Architecture | C4 model, ADRs, tech stack |
| 7 | `database-architect` | Architecture | ER models, CAP, caching |
| 8 | `api-designer` | Architecture | OpenAPI, REST, versioning |
| 9 | `security-architect` | Architecture | STRIDE, zero trust, encryption |
| 10 | `ux-designer` | Architecture | User journeys, WCAG, design system |
| 11 | `tech-lead` | Implementation | WBS, sprints, coding standards |
| 12 | `backend-developer` | Implementation | Clean architecture, DDD |
| 13 | `frontend-developer` | Implementation | Components, state management |
| 14 | `devops-engineer` | Implementation | CI/CD, Docker, Terraform |
| 15 | `database-engineer` | Implementation | Migrations, indexing, queries |
| 16 | `qa-lead` | QA | Test pyramid, quality gates |
| 17 | `test-engineer` | QA | BDD, boundary analysis |
| 18 | `performance-engineer` | QA | Load tests, SLAs, budgets |
| 19 | `security-auditor` | QA | OWASP Top 10, pen test |
| 20 | `accessibility-tester` | QA | WCAG 2.1 AA, screen readers |
| 21 | `code-reviewer` | Review | SOLID, security, tech debt |
| 22 | `technical-writer` | Review | Diátaxis docs, runbooks |
| 23 | `release-manager` | Review | Go/no-go, rollback, flags |
| 24 | `stakeholder-liaison` | Review | Executive summary, ROI |
| 25 | `dev-org-orchestrator` | Meta | Runs the full pipeline |
| 26 | `phase-synthesizer` | Meta | Merges phase outputs |
| 27 | `debate-moderator` | Meta | Runs adversarial debates |

## Output Structure

After a full pipeline run:

```
output/
├── brief.md                    # Original client requirements
├── requirements.md             # Phase 1: Structured requirements
├── market-research.md          # Phase 1: Competitive analysis
├── brainstorm.md               # Phase 1: Solution approaches
├── risk-analysis.md            # Phase 1: Risk assessment
├── tech-radar.md               # Phase 1: Technology recommendations
├── phase-1-synthesis.md        # Phase 1: Merged summary
├── architecture.md             # Phase 2: System architecture
├── database-design.md          # Phase 2: Data architecture
├── api-design.md               # Phase 2: API contracts
├── security-design.md          # Phase 2: Security model
├── ux-design.md                # Phase 2: User experience
├── phase-2-synthesis.md        # Phase 2: Merged summary
├── implementation-plan.md      # Phase 3: Sprint plan & WBS
├── backend-design.md           # Phase 3: Backend structure
├── frontend-design.md          # Phase 3: Frontend architecture
├── devops-design.md            # Phase 3: CI/CD & infra
├── database-implementation.md  # Phase 3: Migrations & queries
├── phase-3-synthesis.md        # Phase 3: Merged summary
├── qa-strategy.md              # Phase 4: Test strategy
├── test-cases.md               # Phase 4: Test cases
├── performance-plan.md         # Phase 4: Performance testing
├── security-audit.md           # Phase 4: Security audit
├── accessibility-audit.md      # Phase 4: Accessibility audit
├── phase-4-synthesis.md        # Phase 4: Merged summary
├── code-review.md              # Phase 5: Quality review
├── documentation-plan.md       # Phase 5: Docs plan
├── release-plan.md             # Phase 5: Release strategy
├── stakeholder-report.md       # Phase 5: Executive summary
└── FINAL-REPORT.md             # Complete project plan
```

## Project Structure

```
rebell/
└── .claude/
    └── agents/
        ├── requirements-analyst.md
        ├── market-researcher.md
        ├── brainstorm-facilitator.md
        ├── devil-advocate.md
        ├── innovation-scout.md
        ├── system-architect.md
        ├── database-architect.md
        ├── api-designer.md
        ├── security-architect.md
        ├── ux-designer.md
        ├── tech-lead.md
        ├── backend-developer.md
        ├── frontend-developer.md
        ├── devops-engineer.md
        ├── database-engineer.md
        ├── qa-lead.md
        ├── test-engineer.md
        ├── performance-engineer.md
        ├── security-auditor.md
        ├── accessibility-tester.md
        ├── code-reviewer.md
        ├── technical-writer.md
        ├── release-manager.md
        ├── stakeholder-liaison.md
        ├── dev-org-orchestrator.md
        ├── phase-synthesizer.md
        └── debate-moderator.md
```
