"""Backend Developer — Claude sub-agent that designs backend code structure."""

from __future__ import annotations

from typing import Any

from core.base_agent import AgentRole, BaseAgent


class BackendDeveloper(BaseAgent):
    """Claude sub-agent: designs backend application structure and patterns.

    Makes real Claude API calls to produce code architecture, design
    patterns, service layer structure, and error handling strategies.
    """

    def __init__(self, model: str = "claude-sonnet-4-6"):
        super().__init__(
            role=AgentRole.BACKEND_DEVELOPER,
            name="Backend Developer",
            expertise=[
                "clean architecture",
                "domain-driven design",
                "design patterns",
                "API implementation",
                "error handling strategies",
                "logging and observability",
                "service layer patterns",
                "dependency injection",
            ],
            model=model,
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are a senior Backend Developer sub-agent who writes clean, "
            "maintainable, and well-tested code. You follow clean architecture, "
            "SOLID principles, and domain-driven design.\n\n"
            "Your responsibilities:\n"
            "1. Design project directory structure\n"
            "2. Define service layer architecture\n"
            "3. Choose and justify design patterns\n"
            "4. Design error handling strategy\n"
            "5. Plan logging and observability integration\n"
            "6. Design dependency injection approach\n"
            "7. Define input validation strategy\n"
            "8. Plan background job processing\n"
            "9. Design health check and readiness probes\n\n"
            "Code should be readable, testable, and follow the principle of "
            "least surprise."
        )

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        if override := context.get("_override_prompt"):
            return override

        requirements = context.get("client_requirements", "")
        architecture = context.get("architecture_doc", {})
        topic = context.get("debate_topic", "")

        return (
            f"Design the backend implementation:\n\n"
            f"## Requirements:\n{requirements}\n\n"
            f"## Architecture:\n{architecture}\n\n"
            f"## Context:\n{topic}\n\n"
            "Deliver:\n"
            "1. Directory/module structure\n"
            "2. Service layer design with interfaces\n"
            "3. Design patterns to use and where\n"
            "4. Error handling strategy\n"
            "5. Logging and observability plan\n"
            "6. Key code structure examples (pseudocode)\n"
            "7. Input validation approach"
        )
