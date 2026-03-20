"""Tech Lead — Claude sub-agent that decomposes work and defines standards."""

from __future__ import annotations

from typing import Any

from core.base_agent import AgentRole, BaseAgent


class TechLead(BaseAgent):
    """Claude sub-agent: decomposes architecture into implementable tasks.

    Makes real Claude API calls to create sprint plans, coding standards,
    dependency graphs, and work breakdown structures.
    """

    def __init__(self, model: str = "sonnet"):
        super().__init__(
            role=AgentRole.TECH_LEAD,
            name="Tech Lead",
            expertise=[
                "work breakdown structures",
                "sprint planning",
                "coding standards",
                "dependency management",
                "technical debt management",
                "code review processes",
                "CI/CD pipeline design",
            ],
            model=model,
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are a Tech Lead sub-agent responsible for translating architecture "
            "into actionable implementation work. You think in terms of sprints, "
            "dependencies, and deliverable increments.\n\n"
            "Your responsibilities:\n"
            "1. Decompose architecture into epics and user stories\n"
            "2. Create work breakdown structure with effort estimates\n"
            "3. Identify critical path and dependencies between tasks\n"
            "4. Define coding standards and conventions\n"
            "5. Plan sprint structure and delivery milestones\n"
            "6. Design branch strategy and code review process\n"
            "7. Identify technical debt risks and mitigation\n"
            "8. Define Definition of Done (DoD) for each work item\n\n"
            "Every task must be small enough to complete in 1-3 days. "
            "Every task must have clear acceptance criteria."
        )

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        if override := context.get("_override_prompt"):
            return override

        requirements = context.get("client_requirements", "")
        architecture = context.get("architecture_doc", {})
        topic = context.get("debate_topic", "")
        timeline = context.get("timeline", "standard")

        return (
            f"Create the implementation plan:\n\n"
            f"## Requirements:\n{requirements}\n\n"
            f"## Architecture:\n{architecture}\n\n"
            f"## Context:\n{topic}\n\n"
            f"## Timeline: {timeline}\n\n"
            "Deliver:\n"
            "1. Epics and user stories with acceptance criteria\n"
            "2. Work breakdown structure with effort estimates\n"
            "3. Dependency graph (what blocks what)\n"
            "4. Sprint plan with milestones\n"
            "5. Coding standards document\n"
            "6. Branch strategy and PR process\n"
            "7. Definition of Done"
        )
