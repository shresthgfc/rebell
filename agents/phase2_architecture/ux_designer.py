"""UX Designer — Claude sub-agent that designs user experience and flows."""

from __future__ import annotations

from typing import Any

from core.base_agent import AgentResponse, AgentRole, BaseAgent


class UXDesigner(BaseAgent):
    """Claude sub-agent: designs user-centered experiences.

    Makes real Claude API calls to produce user journeys, information
    architecture, and WCAG 2.1 AA compliant design systems.
    """

    def __init__(self, model: str = "claude-sonnet-4-6"):
        super().__init__(
            role=AgentRole.UX_DESIGNER,
            name="UX Designer",
            expertise=[
                "user-centered design",
                "information architecture",
                "interaction design",
                "WCAG accessibility",
                "design systems",
                "user flow mapping",
                "responsive design",
                "Nielsen's usability heuristics",
            ],
            model=model,
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are a senior UX Designer sub-agent who creates intuitive, "
            "accessible, and delightful user experiences. You follow Nielsen's "
            "usability heuristics and WCAG 2.1 AA standards.\n\n"
            "Your responsibilities:\n"
            "1. Map user journeys for each persona\n"
            "2. Design information architecture\n"
            "3. Define interaction patterns and micro-interactions\n"
            "4. Specify responsive breakpoints and behavior\n"
            "5. Design error, empty, and loading states\n"
            "6. Define design system (typography, spacing, color, components)\n"
            "7. Ensure WCAG 2.1 AA compliance\n"
            "8. Design onboarding flow\n"
            "9. Plan for i18n and l10n\n\n"
            "Function follows user intent. Form supports function."
        )

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        if override := context.get("_override_prompt"):
            return override

        requirements = context.get("client_requirements", "")
        req_doc = context.get("requirements_doc", {})
        topic = context.get("debate_topic", "")

        return (
            f"Design the user experience:\n\n"
            f"## Requirements:\n{requirements}\n\n"
            f"## Requirements Doc:\n{req_doc}\n\n"
            f"## Context:\n{topic}\n\n"
            "Deliver:\n"
            "1. User journey maps (per persona)\n"
            "2. Information architecture / navigation\n"
            "3. Key interaction patterns\n"
            "4. Responsive strategy\n"
            "5. Design system foundations\n"
            "6. Accessibility guidelines\n"
            "7. Onboarding flow"
        )
