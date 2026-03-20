"""QA Lead — Claude sub-agent that designs test strategy and quality gates."""

from __future__ import annotations

from typing import Any

from core.base_agent import AgentRole, BaseAgent


class QALead(BaseAgent):
    """Claude sub-agent: designs comprehensive test strategy.

    Makes real Claude API calls to produce test pyramids, quality gates,
    and testing infrastructure plans.
    """

    def __init__(self, model: str = "sonnet"):
        super().__init__(
            role=AgentRole.QA_LEAD,
            name="QA Lead",
            expertise=[
                "test strategy design",
                "test pyramid",
                "quality gates",
                "test automation frameworks",
                "risk-based testing",
                "shift-left testing",
                "test environments",
            ],
            model=model,
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are a QA Lead sub-agent who designs comprehensive quality "
            "assurance strategies. You follow the test pyramid model and "
            "believe in shift-left testing.\n\n"
            "Your responsibilities:\n"
            "1. Design test strategy (unit, integration, E2E, contract)\n"
            "2. Define test pyramid ratios\n"
            "3. Design quality gates for CI/CD pipeline\n"
            "4. Choose test automation frameworks\n"
            "5. Define test coverage requirements\n"
            "6. Plan test data management\n"
            "7. Design test environment strategy\n"
            "8. Define bug severity and priority matrix\n"
            "9. Plan regression test suite\n\n"
            "Quality is everyone's responsibility, but you're the champion."
        )

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        if override := context.get("_override_prompt"):
            return override

        requirements = context.get("client_requirements", "")
        architecture = context.get("architecture_doc", {})
        impl_plan = context.get("implementation_plan", {})
        topic = context.get("debate_topic", "")

        return (
            f"Design the QA strategy:\n\n"
            f"## Requirements:\n{requirements}\n\n"
            f"## Architecture:\n{architecture}\n\n"
            f"## Implementation Plan:\n{impl_plan}\n\n"
            f"## Context:\n{topic}\n\n"
            "Deliver:\n"
            "1. Test strategy overview\n"
            "2. Test pyramid with ratios and tools\n"
            "3. Quality gates definition\n"
            "4. Test automation framework selection\n"
            "5. Coverage requirements\n"
            "6. Test data management plan\n"
            "7. Test environment setup"
        )
