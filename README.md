# REBELL — Multi-Agent Development Organization for Claude Code

A complete software development organization as **29 native Claude Code sub-agents** with **7,214 lines** of governance depth. Drop `.claude/agents/` into any project and run the entire dev lifecycle from your terminal.

No Python. No API keys. No dependencies. Just `claude`.

Inspired by [luxifel/designAI](https://github.com/luxifel/designAI)'s governance model — adapted from UI/UX to full-stack software development.

---

## How It Works

```
Client requirement
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 1: DISCOVERY                                         │
│  requirements-analyst → market-researcher →                 │
│  brainstorm-facilitator → devil-advocate → innovation-scout │
│        │                                                    │
│        ▼                                                    │
│  phase-synthesizer → governance-reviewer (BLOCK/PASS)       │
├─────────────────────────────────────────────────────────────┤
│  Phase 2: ARCHITECTURE                                      │
│  system-architect → database-architect → api-designer →     │
│  security-architect → ux-designer                           │
│        │                                                    │
│        ▼                                                    │
│  phase-synthesizer → governance-reviewer (BLOCK/PASS)       │
├─────────────────────────────────────────────────────────────┤
│  Phase 3: IMPLEMENTATION                                    │
│  tech-lead → backend-developer → frontend-developer →       │
│  devops-engineer → database-engineer                        │
│        │                                                    │
│        ▼                                                    │
│  phase-synthesizer → governance-reviewer (BLOCK/PASS)       │
├─────────────────────────────────────────────────────────────┤
│  Phase 4: QUALITY ASSURANCE                                 │
│  qa-lead → test-engineer → performance-engineer →           │
│  security-auditor → accessibility-tester                    │
│        │                                                    │
│        ▼                                                    │
│  phase-synthesizer → governance-reviewer (BLOCK/PASS)       │
├─────────────────────────────────────────────────────────────┤
│  Phase 5: REVIEW & DELIVERY                                 │
│  code-reviewer → technical-writer →                         │
│  release-manager → stakeholder-liaison                      │
│        │                                                    │
│        ▼                                                    │
│  governance-reviewer → standards-librarian                  │
├─────────────────────────────────────────────────────────────┤
│  FINAL REPORT                                               │
│  dev-org-orchestrator produces output/FINAL-REPORT.md       │
└─────────────────────────────────────────────────────────────┘
```

### The Governance Loop (from designAI)

After every phase:
1. **Phase Synthesizer** merges all agent outputs into one document
2. **Governance Reviewer** (BLOCKING AUTHORITY) audits compliance
   - **BLOCK?** Pipeline stops. Fix issues. Re-review.
   - **PASS?** Proceed to next phase.
3. After all phases, **Standards Librarian** checks cross-phase consistency

---

## Setup

### Option 1: Copy agents into your project
```bash
cp -r .claude/ /path/to/your/project/.claude/
```

### Option 2: Clone the repo
```bash
git clone https://github.com/shresthgfc/rebell.git
cd rebell
git checkout claude/multi-agent-dev-org-SJmik
```

### Agent Teams (experimental)
Agent Teams is enabled in `.claude/settings.json`. This allows multiple Claude instances to work as a coordinated team:
```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "teammateMode": "auto"
}
```

---

## Usage

### Run the Full Pipeline
```bash
claude "@dev-org-orchestrator Build a real-time collaboration platform with 10k concurrent users"
```

### Run as Session-Wide Agent
```bash
claude --agent dev-org-orchestrator
```

### Run Individual Agents
```bash
claude "@requirements-analyst Analyze these requirements: ..."
claude "@system-architect Design a system for: ..."
claude "@security-auditor Review the security of this design"
claude "@devil-advocate Find flaws in this proposal: ..."
```

### Run a Debate
```bash
claude "@debate-moderator Debate: monolith vs microservices. Participants: system-architect, devops-engineer, backend-developer"
```

### Run a Specific Phase
```bash
claude "@requirements-analyst [requirements]"
claude "@market-researcher Analyze the market"
claude "@devil-advocate Challenge everything"
claude "@phase-synthesizer Merge Phase 1 outputs"
claude "@governance-reviewer Review Phase 1"
```

---

## The 29 Sub-Agents

### Phase 1: Discovery & Brainstorming (5 agents)

| Agent | Lines | Key Standards | Output |
|-------|-------|---------------|--------|
| `requirements-analyst` | 172 | IEEE 830, INVEST, MoSCoW | `output/requirements.md` |
| `market-researcher` | 168 | SWOT, evidence-based personas | `output/market-research.md` |
| `brainstorm-facilitator` | 144 | SCAMPER, min 3 approaches + moonshot | `output/brainstorm.md` |
| `devil-advocate` | 182 | Pre-mortem, FMEA, quantified risk matrix | `output/risk-analysis.md` |
| `innovation-scout` | 156 | ThoughtWorks Tech Radar, fallback mandate | `output/tech-radar.md` |

### Phase 2: Architecture & Design (5 agents)

| Agent | Lines | Key Standards | Output |
|-------|-------|---------------|--------|
| `system-architect` | 264 | C4 model (all 4 levels), ADRs, boring tech rule | `output/architecture.md` |
| `database-architect` | 262 | CAP trade-offs, data classification T1-T4, migration format | `output/database-design.md` |
| `api-designer` | 338 | OpenAPI 3.1, RFC 7807 errors, idempotency keys | `output/api-design.md` |
| `security-architect` | 332 | STRIDE per component, zero-trust, encryption taxonomy | `output/security-design.md` |
| `ux-designer` | 397 | WCAG 2.1 AA, 9 mandatory states, design token hierarchy | `output/ux-design.md` |

### Phase 3: Implementation Planning (5 agents)

| Agent | Lines | Key Standards | Output |
|-------|-------|---------------|--------|
| `tech-lead` | 269 | 1-3 day tasks, INVEST stories, sprint 0 mandatory | `output/implementation-plan.md` |
| `backend-developer` | 280 | Clean architecture layers, SOLID enforcement, error hierarchy | `output/backend-design.md` |
| `frontend-developer` | 274 | Component taxonomy (7 types), Core Web Vitals budgets | `output/frontend-design.md` |
| `devops-engineer` | 305 | 10 mandatory CI stages, <5min rollback SLA, cost estimation | `output/devops-design.md` |
| `database-engineer` | 301 | Reversible migrations, index justification, N+1 forbidden | `output/database-implementation.md` |

### Phase 4: Quality Assurance (5 agents)

| Agent | Lines | Key Standards | Output |
|-------|-------|---------------|--------|
| `qa-lead` | 212 | Test pyramid (70/20/10), 7 quality gates, shift-left | `output/qa-strategy.md` |
| `test-engineer` | 243 | BDD Given/When/Then, boundary analysis, contract tests | `output/test-cases.md` |
| `performance-engineer` | 244 | 4 load scenarios, SLA with percentiles, frontend budgets | `output/performance-plan.md` |
| `security-auditor` | 247 | All 10 OWASP Top 10, injection taxonomy, CVSS severity | `output/security-audit.md` |
| `accessibility-tester` | 237 | Full WCAG 2.1 AA checklist, 3 screen readers, 4.5:1 contrast | `output/accessibility-audit.md` |

### Phase 5: Review & Delivery (4 agents)

| Agent | Lines | Key Standards | Output |
|-------|-------|---------------|--------|
| `code-reviewer` | 248 | Quality score 1-10 rubric, SOLID checklist, severity taxonomy | `output/code-review.md` |
| `technical-writer` | 257 | Diátaxis framework, P0-P3 priority, runbook template | `output/documentation-plan.md` |
| `release-manager` | 283 | Go/no-go checklist, <5min rollback, feature flag lifecycle | `output/release-plan.md` |
| `stakeholder-liaison` | 258 | No-jargon rule, ROI framework, go/no-go recommendation | `output/stakeholder-report.md` |

### Cross-Cutting Agents (2 agents)

| Agent | Lines | Authority | Output |
|-------|-------|-----------|--------|
| `governance-reviewer` | 251 | **BLOCKING** — can halt the pipeline | `output/governance-review-phase-{N}.md` |
| `standards-librarian` | 264 | Advisory — flags inconsistencies | `output/standards-review.md` |

### Meta-Agents (3 agents)

| Agent | Lines | Purpose | Output |
|-------|-------|---------|--------|
| `dev-org-orchestrator` | 299 | Runs the full 5-phase pipeline | `output/FINAL-REPORT.md` |
| `phase-synthesizer` | 134 | Merges phase outputs, resolves conflicts | `output/phase-{N}-synthesis.md` |
| `debate-moderator` | 193 | 4-round adversarial debates | `output/debate-{topic}.md` |

---

## Agent Governance Depth

Every agent has exactly **7 mandatory sections** (inspired by designAI):

| Section | Purpose |
|---------|---------|
| **Role** | Specialist identity and boundaries |
| **Primary objectives** | Numbered list of what the agent must deliver |
| **Non-negotiable rules** | Hard constraints with sub-sections |
| **Entity taxonomy** | Classification system for the agent's domain |
| **Standard output structure** | Exact markdown template the agent must produce |
| **Quality gates** | Checklist — output is NOT complete until all pass |
| **Absolute prohibitions** | "Never:" list of what the agent must never do |

---

## Output Structure

After a full pipeline run, `output/` contains:

```
output/
├── brief.md                         # Client requirements
├── requirements.md                  # Phase 1
├── market-research.md               # Phase 1
├── brainstorm.md                    # Phase 1
├── risk-analysis.md                 # Phase 1
├── tech-radar.md                    # Phase 1
├── phase-1-synthesis.md             # Phase 1 merged
├── governance-review-phase-1.md     # Phase 1 review (PASS/BLOCK)
├── architecture.md                  # Phase 2
├── database-design.md               # Phase 2
├── api-design.md                    # Phase 2
├── security-design.md               # Phase 2
├── ux-design.md                     # Phase 2
├── phase-2-synthesis.md             # Phase 2 merged
├── governance-review-phase-2.md     # Phase 2 review
├── implementation-plan.md           # Phase 3
├── backend-design.md                # Phase 3
├── frontend-design.md               # Phase 3
├── devops-design.md                 # Phase 3
├── database-implementation.md       # Phase 3
├── phase-3-synthesis.md             # Phase 3 merged
├── governance-review-phase-3.md     # Phase 3 review
├── qa-strategy.md                   # Phase 4
├── test-cases.md                    # Phase 4
├── performance-plan.md              # Phase 4
├── security-audit.md                # Phase 4
├── accessibility-audit.md           # Phase 4
├── phase-4-synthesis.md             # Phase 4 merged
├── governance-review-phase-4.md     # Phase 4 review
├── code-review.md                   # Phase 5
├── documentation-plan.md            # Phase 5
├── release-plan.md                  # Phase 5
├── stakeholder-report.md            # Phase 5
├── governance-review-phase-5.md     # Phase 5 review
├── standards-review.md              # Cross-phase consistency
└── FINAL-REPORT.md                  # Complete project plan
```

---

## Governance Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Repo-level orchestration rules |
| `AGENT_REGISTRY.md` | Complete agent catalog with outputs |
| `NAMING_RULES.md` | File and entity naming conventions |
| `REVIEW_CHECKLIST.md` | Quality verification checklist |

---

## Project Structure

```
rebell/
├── .claude/
│   ├── settings.json              # Agent teams enabled
│   └── agents/                    # 29 agent definition files
│       ├── requirements-analyst.md
│       ├── market-researcher.md
│       ├── brainstorm-facilitator.md
│       ├── devil-advocate.md
│       ├── innovation-scout.md
│       ├── system-architect.md
│       ├── database-architect.md
│       ├── api-designer.md
│       ├── security-architect.md
│       ├── ux-designer.md
│       ├── tech-lead.md
│       ├── backend-developer.md
│       ├── frontend-developer.md
│       ├── devops-engineer.md
│       ├── database-engineer.md
│       ├── qa-lead.md
│       ├── test-engineer.md
│       ├── performance-engineer.md
│       ├── security-auditor.md
│       ├── accessibility-tester.md
│       ├── code-reviewer.md
│       ├── technical-writer.md
│       ├── release-manager.md
│       ├── stakeholder-liaison.md
│       ├── governance-reviewer.md
│       ├── standards-librarian.md
│       ├── dev-org-orchestrator.md
│       ├── phase-synthesizer.md
│       └── debate-moderator.md
├── CLAUDE.md
├── AGENT_REGISTRY.md
├── NAMING_RULES.md
├── REVIEW_CHECKLIST.md
├── .gitignore
└── README.md
```
