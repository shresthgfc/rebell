# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

---

# Role

This repository contains 27 Claude Code sub-agent definitions that form a virtual software development organization. The sub-agents are organized across 5 phases of a development lifecycle.

---

# Repository structure

```
.claude/
  agents/
    # Phase 1: Discovery & Brainstorming (5 agents)
    requirements-analyst.md
    market-researcher.md
    brainstorm-facilitator.md
    devil-advocate.md
    innovation-scout.md

    # Phase 2: Architecture & Design (5 agents)
    system-architect.md
    database-architect.md
    api-designer.md
    security-architect.md
    ux-designer.md

    # Phase 3: Implementation Planning (5 agents)
    tech-lead.md
    backend-developer.md
    frontend-developer.md
    devops-engineer.md
    database-engineer.md

    # Phase 4: Quality Assurance (5 agents)
    qa-lead.md
    test-engineer.md
    performance-engineer.md
    security-auditor.md
    accessibility-tester.md

    # Phase 5: Review & Delivery (4 agents)
    code-reviewer.md
    technical-writer.md
    release-manager.md
    stakeholder-liaison.md

    # Meta-agents (3 agents)
    dev-org-orchestrator.md
    phase-synthesizer.md
    debate-moderator.md

output/    # Generated outputs from pipeline runs
```

---

# Governance rules

## Output directory
All sub-agent outputs go to `output/`. Each agent writes to a specific file. Agents read upstream files but never modify them.

## Phase ordering
Phases must run sequentially: Discovery → Architecture → Implementation → QA → Review.

## Agent boundaries
Each agent is a specialist. Agents must not perform work outside their defined scope. The orchestrator coordinates; specialists execute.

## Quality gates
Every agent has a quality gates section in its definition. Output is not complete until all gates pass.

## No invention rule
Agents must not invent requirements, decisions, or data not supported by input. Missing information must be flagged as open questions.
