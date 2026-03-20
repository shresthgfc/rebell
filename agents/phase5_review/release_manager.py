"""Release Manager — Claude sub-agent that plans release and go-live."""

from __future__ import annotations

from typing import Any

from core.base_agent import AgentRole, BaseAgent


class ReleaseManager(BaseAgent):
    """Claude sub-agent: plans release strategy, rollback, and go-live.

    Makes real Claude API calls to produce release checklists,
    rollback procedures, and go/no-go criteria.
    """

    def __init__(self, model: str = "sonnet"):
        super().__init__(
            role=AgentRole.RELEASE_MANAGER,
            name="Release Manager",
            expertise=[
                "release planning",
                "semantic versioning",
                "blue-green deployments",
                "canary releases",
                "feature flags",
                "rollback procedures",
                "go/no-go criteria",
                "post-launch monitoring",
            ],
            model=model,
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are a Release Manager sub-agent who ensures smooth, safe, "
            "and reversible releases.\n\n"
            "Your responsibilities:\n"
            "1. Define release strategy (big bang, phased, canary)\n"
            "2. Create go/no-go checklist\n"
            "3. Design rollback procedure (< 5 min rollback target)\n"
            "4. Plan feature flag strategy\n"
            "5. Define post-launch monitoring criteria\n"
            "6. Plan communication to stakeholders\n"
            "7. Define success metrics for launch\n"
            "8. Plan post-mortem process\n\n"
            "A release is not done until it's monitored and stable."
        )

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        if override := context.get("_override_prompt"):
            return override

        requirements = context.get("client_requirements", "")
        architecture = context.get("architecture_doc", {})
        impl_plan = context.get("implementation_plan", {})
        test_plan = context.get("test_plan", {})
        topic = context.get("debate_topic", "")

        return (
            f"Plan the release:\n\n"
            f"## Requirements:\n{requirements}\n\n"
            f"## Architecture:\n{architecture}\n\n"
            f"## Implementation Plan:\n{impl_plan}\n\n"
            f"## Test Plan:\n{test_plan}\n\n"
            f"## Context:\n{topic}\n\n"
            "Deliver:\n"
            "1. Release strategy\n"
            "2. Go/no-go checklist\n"
            "3. Rollback procedure\n"
            "4. Feature flag plan\n"
            "5. Post-launch monitoring plan\n"
            "6. Success metrics\n"
            "7. Communication plan"
        )
