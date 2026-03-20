"""System Architect — Claude sub-agent that designs overall system architecture."""

from __future__ import annotations

from typing import Any

from core.base_agent import AgentResponse, AgentRole, BaseAgent


class SystemArchitect(BaseAgent):
    """Claude sub-agent: designs high-level system architecture.

    Makes real Claude API calls to produce C4 model diagrams,
    Architecture Decision Records, and technology stack selections.
    """

    def __init__(self, model: str = "sonnet"):
        super().__init__(
            role=AgentRole.SYSTEM_ARCHITECT,
            name="System Architect",
            expertise=[
                "distributed systems",
                "microservices vs monolith",
                "event-driven architecture",
                "CQRS and event sourcing",
                "cloud-native patterns",
                "architecture decision records",
                "C4 model",
                "twelve-factor app",
            ],
            model=model,
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are a principal System Architect sub-agent with 20+ years of "
            "experience designing systems that serve millions of users. You follow "
            "the C4 model for documentation and write ADRs for every major decision.\n\n"
            "Your responsibilities:\n"
            "1. Choose architectural style (monolith, microservices, modular monolith, serverless)\n"
            "2. Define system components and their responsibilities\n"
            "3. Design communication patterns (sync/async, REST/gRPC/events)\n"
            "4. Select technology stack with detailed justification\n"
            "5. Design deployment topology\n"
            "6. Define cross-cutting concerns (logging, monitoring, tracing)\n"
            "7. Produce ADRs: Context → Decision → Consequences → Alternatives\n\n"
            "Follow SOLID, DRY, KISS. Prefer boring technology for critical paths."
        )

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        if override := context.get("_override_prompt"):
            return override

        requirements = context.get("client_requirements", "")
        req_doc = context.get("requirements_doc", {})
        topic = context.get("debate_topic", "")
        budget = context.get("budget_tier", "standard")

        return (
            f"Design the system architecture:\n\n"
            f"## Requirements:\n{requirements}\n\n"
            f"## Validated Requirements Doc:\n{req_doc}\n\n"
            f"## Context:\n{topic}\n\n"
            f"## Budget: {budget}\n\n"
            "Deliver:\n"
            "1. Architectural style decision with ADR\n"
            "2. Component diagram (text description of C4 model)\n"
            "3. Technology stack with justification per choice\n"
            "4. Communication patterns between components\n"
            "5. Deployment topology\n"
            "6. Cross-cutting concerns strategy\n"
            "7. Scalability plan"
        )
