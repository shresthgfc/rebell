"""Frontend Developer — Claude sub-agent that designs frontend architecture."""

from __future__ import annotations

from typing import Any

from core.base_agent import AgentRole, BaseAgent


class FrontendDeveloper(BaseAgent):
    """Claude sub-agent: designs frontend application architecture.

    Makes real Claude API calls to produce component hierarchies,
    state management designs, and performance optimization strategies.
    """

    def __init__(self, model: str = "claude-sonnet-4-6"):
        super().__init__(
            role=AgentRole.FRONTEND_DEVELOPER,
            name="Frontend Developer",
            expertise=[
                "React / Next.js / Vue / Svelte",
                "component architecture",
                "state management",
                "CSS-in-JS / Tailwind",
                "performance optimization",
                "progressive web apps",
                "bundle optimization",
                "accessibility implementation",
            ],
            model=model,
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are a senior Frontend Developer sub-agent who builds performant, "
            "accessible, and maintainable frontends.\n\n"
            "Your responsibilities:\n"
            "1. Choose frontend framework with justification\n"
            "2. Design component hierarchy and composition patterns\n"
            "3. Design state management approach\n"
            "4. Plan routing and code splitting strategy\n"
            "5. Design form handling and validation\n"
            "6. Plan performance optimization (lazy loading, memoization)\n"
            "7. Design styling approach (CSS modules, Tailwind, etc.)\n"
            "8. Plan error boundary and fallback UI strategy\n"
            "9. Design API integration layer (data fetching, caching)\n\n"
            "Performance is a feature. Accessibility is not optional."
        )

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        if override := context.get("_override_prompt"):
            return override

        requirements = context.get("client_requirements", "")
        architecture = context.get("architecture_doc", {})
        design = context.get("design_doc", {})
        topic = context.get("debate_topic", "")

        return (
            f"Design the frontend implementation:\n\n"
            f"## Requirements:\n{requirements}\n\n"
            f"## Architecture:\n{architecture}\n\n"
            f"## UX Design:\n{design}\n\n"
            f"## Context:\n{topic}\n\n"
            "Deliver:\n"
            "1. Framework choice with justification\n"
            "2. Component hierarchy\n"
            "3. State management design\n"
            "4. Routing and code splitting plan\n"
            "5. Styling approach\n"
            "6. Performance optimization strategy\n"
            "7. API integration layer design"
        )
