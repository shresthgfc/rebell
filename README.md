# REBELL — Multi-Agent Development Organization

A complete software development organization powered by **25 Claude sub-agents** that collaborate, debate, and refine work through 5 phases — from brainstorming to implementation review.

Each agent runs via the **`claude` CLI** (Claude Code) — no API key needed. Agents don't just generate output — they **challenge each other** in structured debate rounds until consensus emerges.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ORCHESTRATOR (CEO)                         │
│                    Manages phases, synthesizes results              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Phase 1: DISCOVERY          Phase 2: ARCHITECTURE                 │
│  ┌──────────────────┐        ┌──────────────────┐                  │
│  │ Requirements      │        │ System Architect  │                  │
│  │ Analyst           │        │                  │                  │
│  │ Market Researcher │        │ Database Architect│                  │
│  │ Brainstorm        │  ───►  │ API Designer     │                  │
│  │ Facilitator       │        │ Security Architect│                  │
│  │ Devil's Advocate  │        │ UX Designer      │                  │
│  │ Innovation Scout  │        │                  │                  │
│  └──────────────────┘        └──────────────────┘                  │
│           │                           │                             │
│           ▼                           ▼                             │
│  Phase 3: IMPLEMENTATION     Phase 4: QA                           │
│  ┌──────────────────┐        ┌──────────────────┐                  │
│  │ Tech Lead         │        │ QA Lead          │                  │
│  │ Backend Developer │        │ Test Engineer    │                  │
│  │ Frontend Developer│  ───►  │ Performance Eng. │                  │
│  │ DevOps Engineer   │        │ Security Auditor │                  │
│  │ Database Engineer │        │ Accessibility    │                  │
│  └──────────────────┘        └──────────────────┘                  │
│                                       │                             │
│                                       ▼                             │
│                          Phase 5: REVIEW & DELIVERY                │
│                          ┌──────────────────┐                      │
│                          │ Code Reviewer     │                      │
│                          │ Technical Writer  │                      │
│                          │ Release Manager   │                      │
│                          │ Stakeholder       │                      │
│                          │ Liaison           │                      │
│                          └──────────────────┘                      │
└─────────────────────────────────────────────────────────────────────┘
```

## How It Works

### The Debate Mechanism

Within each phase, agents don't just produce output independently. They engage in structured **debate rounds**:

1. **Propose** — Each sub-agent produces its initial analysis via Claude API
2. **Challenge** — Each sub-agent critiques the others' proposals via Claude API
3. **Refine** — Each sub-agent improves its work based on challenges via Claude API
4. **Consensus** — If alignment is above threshold, move on. Otherwise, repeat.
5. **Synthesize** — A synthesizer sub-agent merges all outputs into one cohesive deliverable

This means a full pipeline run with 3 debate rounds invokes Claude **hundreds of times**, each call with a specialized system prompt and accumulated context.

### The 25 Sub-Agents

| Phase | Agent | Role |
|-------|-------|------|
| **Discovery** | Requirements Analyst | IEEE 830 requirements, MoSCoW prioritization |
| | Market Researcher | SWOT, competitive analysis, user personas |
| | Brainstorm Facilitator | SCAMPER, divergent solution generation |
| | Devil's Advocate | Pre-mortem, FMEA, assumption challenging |
| | Innovation Scout | Tech Radar, emerging tech, build-vs-buy |
| **Architecture** | System Architect | C4 model, ADRs, tech stack selection |
| | Database Architect | ER models, CAP trade-offs, migration strategy |
| | API Designer | OpenAPI 3.1, REST design, versioning |
| | Security Architect | STRIDE, zero trust, encryption strategy |
| | UX Designer | User journeys, WCAG 2.1, design systems |
| **Implementation** | Tech Lead | WBS, sprint planning, coding standards |
| | Backend Developer | Clean architecture, DDD, service patterns |
| | Frontend Developer | Component architecture, state management |
| | DevOps Engineer | CI/CD, IaC, containerization, monitoring |
| | Database Engineer | Migrations, indexing, query optimization |
| **QA** | QA Lead | Test pyramid, quality gates, test strategy |
| | Test Engineer | BDD scenarios, boundary analysis, contract tests |
| | Performance Engineer | Load tests, SLAs, Core Web Vitals |
| | Security Auditor | OWASP audit, SAST/DAST, pen test planning |
| | Accessibility Tester | WCAG audit, screen reader, keyboard nav |
| **Review** | Code Reviewer | SOLID review, security review, tech debt |
| | Technical Writer | Diátaxis docs, API docs, runbooks |
| | Release Manager | Go/no-go, rollback, feature flags |
| | Stakeholder Liaison | Executive summary, ROI, business impact |

## Quick Start

### Prerequisites

Just have **Claude Code** (`claude`) installed on your terminal. No API key needed.

```bash
# Verify claude CLI is available
claude --version
```

### CLI Usage

```bash
# Full enterprise pipeline (25 agents, 3 debate rounds)
python run.py -r "Build a real-time collaboration platform" -p full

# Standard balanced pipeline (15 agents, 2 debate rounds)
python run.py -r "Create an e-commerce API" -p standard

# Lean startup pipeline (8 agents, 1 debate round)
python run.py -r "MVP for task tracker" -p lean

# Custom settings
python run.py \
  -r "Build a CRM system" \
  -n "MyCRM" \
  -p full \
  -m opus \
  --debate-rounds 2 \
  --budget enterprise \
  --timeline standard \
  -o ./output/mycrm

# Available models: sonnet (default), opus, haiku
```

### Programmatic Usage

```python
from pipeline.factory import PipelineFactory

pipeline = PipelineFactory.create(
    preset="full",
    model="sonnet",  # or "opus", "haiku"
    max_debate_rounds=2,
)

context = pipeline.run(
    client_requirements="Build a project management SaaS platform",
    project_name="ProjectFlow",
    budget_tier="enterprise",
    timeline="standard",
)

# Access results
print(context.requirements_doc)
print(context.architecture_doc)
print(context.implementation_plan)
print(context.test_plan)
print(context.review_report)
print(context.risks)
print(context.decisions)
```

## Pipeline Presets

| Preset | Agents | Phases | Debate Rounds | Best For |
|--------|--------|--------|---------------|----------|
| `full` | 25 | 5 | 3 | Enterprise projects, thorough analysis |
| `standard` | 15 | 5 | 2 | Balanced coverage and speed |
| `lean` | 8 | 3 | 1 | Startups, MVPs, quick validation |

## Output

The pipeline produces:
- `project_output.json` — Full structured output from all phases
- `phase_*_summary.md` — Markdown summary for each phase
- `final_synthesis.md` — CTO-level executive summary

## Project Structure

```
rebell/
├── core/                          # Core framework
│   ├── base_agent.py              # BaseAgent ABC with Claude API integration
│   ├── context.py                 # ProjectContext (shared state)
│   ├── debate.py                  # DebateArena (multi-agent debate)
│   └── orchestrator.py            # Orchestrator (pipeline runner)
├── agents/
│   ├── phase1_discovery/          # 5 discovery sub-agents
│   ├── phase2_architecture/       # 5 architecture sub-agents
│   ├── phase3_implementation/     # 5 implementation sub-agents
│   ├── phase4_qa/                 # 5 QA sub-agents
│   └── phase5_review/             # 4 review sub-agents
├── pipeline/
│   └── factory.py                 # Pipeline factory (full/standard/lean)
├── config/
│   └── settings.py                # Configuration presets
├── examples/
│   └── example_saas.py            # Full example
├── run.py                         # CLI entry point
└── pyproject.toml
```
