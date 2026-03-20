"""Technical Writer — Claude sub-agent that produces documentation."""

from __future__ import annotations

from typing import Any

from core.base_agent import AgentRole, BaseAgent


class TechnicalWriter(BaseAgent):
    """Claude sub-agent: produces comprehensive technical documentation.

    Makes real Claude API calls to generate API docs, architecture docs,
    runbooks, and onboarding guides.
    """

    def __init__(self, model: str = "sonnet"):
        super().__init__(
            role=AgentRole.TECHNICAL_WRITER,
            name="Technical Writer",
            expertise=[
                "API documentation",
                "architecture documentation",
                "runbooks and playbooks",
                "onboarding guides",
                "README and getting started",
                "change logs",
                "Diátaxis framework",
                "docs-as-code",
            ],
            model=model,
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are a Technical Writer sub-agent who produces clear, "
            "comprehensive, and maintainable documentation. You follow "
            "the Diátaxis framework (tutorials, how-tos, reference, explanation).\n\n"
            "Your responsibilities:\n"
            "1. Architecture overview documentation\n"
            "2. API reference documentation\n"
            "3. Getting started / quickstart guide\n"
            "4. Operational runbooks\n"
            "5. Troubleshooting guide\n"
            "6. Change log and migration guides\n"
            "7. Developer onboarding guide\n"
            "8. Deployment documentation\n\n"
            "Good docs are the difference between adoption and abandonment."
        )

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        if override := context.get("_override_prompt"):
            return override

        requirements = context.get("client_requirements", "")
        architecture = context.get("architecture_doc", {})
        impl_plan = context.get("implementation_plan", {})
        topic = context.get("debate_topic", "")

        return (
            f"Plan the documentation:\n\n"
            f"## Requirements:\n{requirements}\n\n"
            f"## Architecture:\n{architecture}\n\n"
            f"## Implementation Plan:\n{impl_plan}\n\n"
            f"## Context:\n{topic}\n\n"
            "Deliver:\n"
            "1. Documentation plan (what docs are needed)\n"
            "2. Architecture overview outline\n"
            "3. API reference outline\n"
            "4. Getting started guide outline\n"
            "5. Runbook templates\n"
            "6. Developer onboarding outline\n"
            "7. Docs-as-code setup (tools, CI integration)"
        )
