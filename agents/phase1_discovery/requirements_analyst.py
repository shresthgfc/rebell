"""Requirements Analyst — Claude sub-agent that extracts and structures requirements."""

from __future__ import annotations

from typing import Any

from core.base_agent import AgentResponse, AgentRole, BaseAgent


class RequirementsAnalyst(BaseAgent):
    """Claude sub-agent: transforms vague client input into IEEE 830 compliant requirements.

    Makes real Claude API calls to analyze client requirements using
    INVEST criteria and MoSCoW prioritization.
    """

    def __init__(self, model: str = "sonnet"):
        super().__init__(
            role=AgentRole.REQUIREMENTS_ANALYST,
            name="Requirements Analyst",
            expertise=[
                "requirements engineering",
                "stakeholder analysis",
                "user story mapping",
                "acceptance criteria",
                "IEEE 830 SRS",
                "INVEST criteria",
            ],
            model=model,
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are a senior Requirements Analyst sub-agent with 15+ years of "
            "experience in software requirements engineering. You follow IEEE 830 "
            "standards and INVEST criteria for user stories.\n\n"
            "Your responsibilities:\n"
            "1. Extract functional and non-functional requirements from client input\n"
            "2. Identify ambiguities and flag them as open questions\n"
            "3. Structure requirements using MoSCoW prioritization\n"
            "4. Define clear acceptance criteria for each requirement\n"
            "5. Identify implicit requirements the client hasn't stated\n"
            "6. Map stakeholders and their concerns\n"
            "7. Create a requirements traceability outline\n\n"
            "Be precise, thorough, and never assume. Flag ambiguities explicitly."
        )

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        if override := context.get("_override_prompt"):
            return override

        requirements = context.get("client_requirements", "")
        budget = context.get("budget_tier", "standard")
        timeline = context.get("timeline", "standard")
        topic = context.get("debate_topic", "")

        return (
            f"Analyze the following and produce a structured requirements document:\n\n"
            f"## Client Requirements:\n{requirements}\n\n"
            f"## Debate Topic:\n{topic}\n\n"
            f"## Constraints:\nBudget: {budget} | Timeline: {timeline}\n\n"
            "Deliver:\n"
            "1. Functional requirements (ID, description, priority, acceptance criteria)\n"
            "2. Non-functional requirements (performance, security, scalability)\n"
            "3. Assumptions you're making\n"
            "4. Items explicitly out of scope\n"
            "5. Open questions needing client clarification\n"
            "6. MoSCoW prioritization of all requirements"
        )
