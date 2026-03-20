"""Brainstorm Facilitator — Claude sub-agent that generates creative solutions."""

from __future__ import annotations

from typing import Any

from core.base_agent import AgentResponse, AgentRole, BaseAgent


class BrainstormFacilitator(BaseAgent):
    """Claude sub-agent: generates divergent solution approaches.

    Uses SCAMPER, Six Thinking Hats, and lateral thinking via real
    Claude API calls to explore the full solution space.
    """

    def __init__(self, model: str = "sonnet"):
        super().__init__(
            role=AgentRole.BRAINSTORM_FACILITATOR,
            name="Brainstorm Facilitator",
            expertise=[
                "design thinking",
                "SCAMPER method",
                "six thinking hats",
                "lateral thinking",
                "solution architecture brainstorming",
                "feature ideation",
            ],
            model=model,
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are a creative Brainstorm Facilitator sub-agent who ensures the "
            "team explores the full solution space before converging.\n\n"
            "Your approach:\n"
            "1. Generate minimum 3 distinct solution approaches\n"
            "2. For each: pros, cons, technical feasibility, estimated effort\n"
            "3. Apply SCAMPER (Substitute, Combine, Adapt, Modify, Put to other "
            "uses, Eliminate, Reverse)\n"
            "4. Identify hybrid approaches combining the best of multiple solutions\n"
            "5. Rank solutions by feasibility, impact, and alignment\n"
            "6. Always propose at least one unconventional 'moonshot' approach\n\n"
            "Push beyond obvious solutions. Creativity within constraints."
        )

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        if override := context.get("_override_prompt"):
            return override

        requirements = context.get("client_requirements", "")
        topic = context.get("debate_topic", "")
        budget = context.get("budget_tier", "standard")

        return (
            f"Brainstorm solution approaches for:\n\n"
            f"## Requirements:\n{requirements}\n\n"
            f"## Context:\n{topic}\n\n"
            f"## Budget Tier: {budget}\n\n"
            "Deliver:\n"
            "1. At least 3 distinct solution approaches with pros/cons\n"
            "2. SCAMPER analysis on the top approach\n"
            "3. One unconventional 'moonshot' idea\n"
            "4. Hybrid recommendation combining best elements\n"
            "5. Feasibility ranking"
        )
