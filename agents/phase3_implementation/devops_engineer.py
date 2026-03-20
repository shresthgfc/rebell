"""DevOps Engineer — Claude sub-agent that designs CI/CD and infrastructure."""

from __future__ import annotations

from typing import Any

from core.base_agent import AgentRole, BaseAgent


class DevOpsEngineer(BaseAgent):
    """Claude sub-agent: designs CI/CD pipelines and infrastructure as code.

    Makes real Claude API calls to produce Dockerfiles, CI/CD configs,
    Terraform/Pulumi plans, and monitoring dashboards.
    """

    def __init__(self, model: str = "claude-sonnet-4-6"):
        super().__init__(
            role=AgentRole.DEVOPS_ENGINEER,
            name="DevOps Engineer",
            expertise=[
                "CI/CD pipeline design",
                "Docker and containerization",
                "Kubernetes orchestration",
                "infrastructure as code (Terraform/Pulumi)",
                "cloud platforms (AWS/GCP/Azure)",
                "monitoring and alerting",
                "GitOps workflows",
                "blue-green / canary deployments",
            ],
            model=model,
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are a senior DevOps Engineer sub-agent who designs reliable, "
            "automated, and observable deployment pipelines.\n\n"
            "Your responsibilities:\n"
            "1. Design CI pipeline (lint, test, build, security scan)\n"
            "2. Design CD pipeline (staging, canary, production)\n"
            "3. Containerization strategy (Dockerfile, multi-stage builds)\n"
            "4. Infrastructure as Code (Terraform/Pulumi)\n"
            "5. Kubernetes manifests or serverless config\n"
            "6. Monitoring, alerting, and dashboards\n"
            "7. Log aggregation strategy\n"
            "8. Secrets and config management in deployment\n"
            "9. Disaster recovery and rollback procedures\n\n"
            "Automate everything. If it's manual, it's a bug."
        )

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        if override := context.get("_override_prompt"):
            return override

        requirements = context.get("client_requirements", "")
        architecture = context.get("architecture_doc", {})
        topic = context.get("debate_topic", "")
        budget = context.get("budget_tier", "standard")

        return (
            f"Design the DevOps and infrastructure:\n\n"
            f"## Requirements:\n{requirements}\n\n"
            f"## Architecture:\n{architecture}\n\n"
            f"## Context:\n{topic}\n\n"
            f"## Budget: {budget}\n\n"
            "Deliver:\n"
            "1. CI pipeline design (stages, tools, quality gates)\n"
            "2. CD pipeline design (environments, promotion strategy)\n"
            "3. Containerization approach\n"
            "4. Infrastructure as Code outline\n"
            "5. Monitoring and alerting plan\n"
            "6. Rollback and DR procedures\n"
            "7. Cost estimation for infrastructure"
        )
