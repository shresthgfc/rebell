"""Market Researcher — Claude sub-agent that analyzes competitive landscape."""

from __future__ import annotations

from typing import Any

from core.base_agent import AgentResponse, AgentRole, BaseAgent


class MarketResearcher(BaseAgent):
    """Claude sub-agent: analyzes market positioning and competitive landscape.

    Makes real Claude API calls to perform SWOT analysis, persona
    development, and competitive differentiation strategy.
    """

    def __init__(self, model: str = "claude-sonnet-4-6"):
        super().__init__(
            role=AgentRole.MARKET_RESEARCHER,
            name="Market Researcher",
            expertise=[
                "competitive analysis",
                "market sizing",
                "trend analysis",
                "SWOT analysis",
                "product-market fit",
                "user persona development",
            ],
            model=model,
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are a senior Market Researcher and Product Strategist sub-agent. "
            "You analyze competitive landscapes, identify market opportunities, "
            "and ensure technical decisions align with market realities.\n\n"
            "Your responsibilities:\n"
            "1. Identify direct and indirect competitors\n"
            "2. Analyze competitor strengths and weaknesses\n"
            "3. Identify market gaps and opportunities\n"
            "4. Define target user personas with demographics and pain points\n"
            "5. Assess product-market fit\n"
            "6. Recommend differentiating features\n"
            "7. Flag market risks (saturated segments, declining trends)\n\n"
            "Ground all recommendations in competitive reality."
        )

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        if override := context.get("_override_prompt"):
            return override

        requirements = context.get("client_requirements", "")
        topic = context.get("debate_topic", "")

        return (
            f"Perform a market and competitive analysis:\n\n"
            f"## Project Requirements:\n{requirements}\n\n"
            f"## Debate Topic:\n{topic}\n\n"
            "Deliver:\n"
            "1. Competitor analysis (at least 3 competitors)\n"
            "2. SWOT analysis\n"
            "3. User personas (at least 2)\n"
            "4. Market gaps and opportunities\n"
            "5. Recommended differentiators\n"
            "6. Market risks"
        )
