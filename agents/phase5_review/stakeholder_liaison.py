"""Stakeholder Liaison — Claude sub-agent that translates tech to business."""

from __future__ import annotations

from typing import Any

from core.base_agent import AgentRole, BaseAgent


class StakeholderLiaison(BaseAgent):
    """Claude sub-agent: translates technical outcomes into business language.

    Makes real Claude API calls to produce executive summaries,
    ROI analyses, and stakeholder-ready presentations.
    """

    def __init__(self, model: str = "sonnet"):
        super().__init__(
            role=AgentRole.STAKEHOLDER_LIAISON,
            name="Stakeholder Liaison",
            expertise=[
                "executive communication",
                "ROI analysis",
                "risk communication",
                "project status reporting",
                "stakeholder management",
                "business case development",
                "technical translation",
            ],
            model=model,
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are a Stakeholder Liaison sub-agent who bridges the gap "
            "between technical teams and business stakeholders.\n\n"
            "Your responsibilities:\n"
            "1. Translate technical decisions into business impact\n"
            "2. Produce executive summary of the project plan\n"
            "3. Create ROI analysis\n"
            "4. Communicate risks in business terms\n"
            "5. Define success metrics stakeholders care about\n"
            "6. Create project timeline for non-technical audience\n"
            "7. Prepare go/no-go recommendation\n"
            "8. Draft stakeholder communication plan\n\n"
            "Speak in outcomes, not in technology."
        )

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        if override := context.get("_override_prompt"):
            return override

        requirements = context.get("client_requirements", "")
        phases_completed = context.get("phases_completed", [])
        risks = context.get("risks", [])
        decisions = context.get("decisions", [])
        topic = context.get("debate_topic", "")

        return (
            f"Prepare stakeholder deliverables:\n\n"
            f"## Client Requirements:\n{requirements}\n\n"
            f"## Phases Completed: {phases_completed}\n\n"
            f"## Key Risks:\n{risks}\n\n"
            f"## Key Decisions:\n{decisions}\n\n"
            f"## Context:\n{topic}\n\n"
            "Deliver:\n"
            "1. Executive summary (1 page)\n"
            "2. Business impact analysis\n"
            "3. Risk summary (business language)\n"
            "4. Timeline and milestones\n"
            "5. Success metrics\n"
            "6. Go/no-go recommendation\n"
            "7. Stakeholder communication plan"
        )
