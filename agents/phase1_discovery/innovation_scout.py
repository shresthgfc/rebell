"""Innovation Scout — Claude sub-agent that identifies emerging tech opportunities."""

from __future__ import annotations

from typing import Any

from core.base_agent import AgentResponse, AgentRole, BaseAgent


class InnovationScout(BaseAgent):
    """Claude sub-agent: identifies cutting-edge technologies and novel approaches.

    Uses ThoughtWorks Tech Radar methodology via real Claude API calls
    to evaluate emerging tech, AI/ML opportunities, and modern patterns.
    """

    def __init__(self, model: str = "claude-sonnet-4-6"):
        super().__init__(
            role=AgentRole.INNOVATION_SCOUT,
            name="Innovation Scout",
            expertise=[
                "emerging technologies",
                "technology radar analysis",
                "open source ecosystem",
                "AI/ML integration opportunities",
                "cloud-native patterns",
                "developer experience optimization",
            ],
            model=model,
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are an Innovation Scout sub-agent on the bleeding edge of technology. "
            "You identify opportunities to use emerging tech that gives competitive "
            "advantages, while balancing innovation with pragmatism.\n\n"
            "Your responsibilities:\n"
            "1. Identify emerging technologies relevant to the project\n"
            "2. Evaluate maturity using Tech Radar categories:\n"
            "   - ADOPT: proven, production-ready\n"
            "   - TRIAL: worth trying in non-critical paths\n"
            "   - ASSESS: interesting, needs evaluation\n"
            "   - HOLD: not ready, watch closely\n"
            "3. Recommend modern alternatives to traditional approaches\n"
            "4. Assess AI/ML integration opportunities\n"
            "5. Evaluate open source vs build vs buy\n"
            "6. Consider developer experience and productivity\n\n"
            "Always consider the team's ability to adopt new technology."
        )

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        if override := context.get("_override_prompt"):
            return override

        requirements = context.get("client_requirements", "")
        topic = context.get("debate_topic", "")
        budget = context.get("budget_tier", "standard")

        return (
            f"Analyze technology opportunities:\n\n"
            f"## Requirements:\n{requirements}\n\n"
            f"## Context:\n{topic}\n\n"
            f"## Budget: {budget}\n\n"
            "Deliver:\n"
            "1. Tech Radar (ADOPT/TRIAL/ASSESS/HOLD) for relevant technologies\n"
            "2. AI/ML integration opportunities\n"
            "3. Open source recommendations\n"
            "4. Build vs buy analysis for key components\n"
            "5. Developer experience improvements\n"
            "6. Risk assessment for each recommendation"
        )
