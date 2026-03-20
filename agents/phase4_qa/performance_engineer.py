"""Performance Engineer — Claude sub-agent that designs load and perf tests."""

from __future__ import annotations

from typing import Any

from core.base_agent import AgentRole, BaseAgent


class PerformanceEngineer(BaseAgent):
    """Claude sub-agent: designs performance testing and optimization strategy.

    Makes real Claude API calls to produce load test plans, SLA definitions,
    and performance budgets.
    """

    def __init__(self, model: str = "sonnet"):
        super().__init__(
            role=AgentRole.PERFORMANCE_ENGINEER,
            name="Performance Engineer",
            expertise=[
                "load testing (k6, Locust, JMeter)",
                "performance budgets",
                "SLA definition",
                "bottleneck analysis",
                "caching optimization",
                "CDN strategy",
                "database query optimization",
                "frontend performance (Core Web Vitals)",
            ],
            model=model,
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are a Performance Engineer sub-agent who ensures the system "
            "meets its performance SLAs under real-world conditions.\n\n"
            "Your responsibilities:\n"
            "1. Define performance SLAs (latency, throughput, error rate)\n"
            "2. Design load test scenarios (normal, peak, stress, soak)\n"
            "3. Create performance budgets (frontend and backend)\n"
            "4. Identify potential bottlenecks in the architecture\n"
            "5. Design caching and CDN strategy\n"
            "6. Plan Core Web Vitals optimization\n"
            "7. Design performance monitoring dashboards\n"
            "8. Plan capacity estimation\n\n"
            "If you can't measure it, you can't improve it."
        )

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        if override := context.get("_override_prompt"):
            return override

        requirements = context.get("client_requirements", "")
        architecture = context.get("architecture_doc", {})
        topic = context.get("debate_topic", "")

        return (
            f"Design performance testing strategy:\n\n"
            f"## Requirements:\n{requirements}\n\n"
            f"## Architecture:\n{architecture}\n\n"
            f"## Context:\n{topic}\n\n"
            "Deliver:\n"
            "1. Performance SLAs\n"
            "2. Load test scenarios\n"
            "3. Performance budgets\n"
            "4. Bottleneck analysis\n"
            "5. Caching/CDN strategy\n"
            "6. Monitoring dashboard design\n"
            "7. Capacity estimation"
        )
