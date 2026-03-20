"""Devil's Advocate — Claude sub-agent that challenges assumptions and finds risks."""

from __future__ import annotations

from typing import Any

from core.base_agent import AgentResponse, AgentRole, BaseAgent


class DevilAdvocate(BaseAgent):
    """Claude sub-agent: systematically challenges every assumption and proposal.

    Uses pre-mortem analysis, FMEA, and threat modeling via real Claude
    API calls to prevent groupthink and identify failure modes.
    """

    def __init__(self, model: str = "claude-sonnet-4-6"):
        super().__init__(
            role=AgentRole.DEVIL_ADVOCATE,
            name="Devil's Advocate",
            expertise=[
                "risk analysis",
                "failure mode analysis (FMEA)",
                "pre-mortem analysis",
                "assumption challenging",
                "edge case identification",
                "worst-case scenario planning",
            ],
            model=model,
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are the Devil's Advocate sub-agent. Your job is to find flaws, "
            "risks, and hidden assumptions in every proposal. You are constructively "
            "critical to make the final product stronger.\n\n"
            "Your techniques:\n"
            "1. Pre-mortem: 'Imagine the project failed — what went wrong?'\n"
            "2. Assumption mapping: list and challenge every assumption\n"
            "3. Edge cases: scale, bad data, high load, network failures\n"
            "4. Failure mode analysis: single points of failure\n"
            "5. Dependency risk: external services, libraries, APIs\n"
            "6. Security threat modeling: attack vectors\n"
            "7. Scalability stress testing: where does the design break?\n\n"
            "For every concern, provide a mitigation strategy. "
            "Goal: strengthen, not block."
        )

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        if override := context.get("_override_prompt"):
            return override

        requirements = context.get("client_requirements", "")
        topic = context.get("debate_topic", "")

        return (
            f"Perform a critical risk analysis:\n\n"
            f"## Proposal/Requirements:\n{requirements}\n\n"
            f"## Context:\n{topic}\n\n"
            "Deliver:\n"
            "1. Pre-mortem: top 5 failure scenarios\n"
            "2. Challenged assumptions (list each + why it's risky)\n"
            "3. Edge cases and boundary conditions\n"
            "4. Single points of failure\n"
            "5. Dependency risks\n"
            "6. Mitigation strategies for each risk\n"
            "7. Risk severity matrix (likelihood x impact)"
        )
