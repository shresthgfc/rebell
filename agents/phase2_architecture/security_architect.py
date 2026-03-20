"""Security Architect — Claude sub-agent that designs security model."""

from __future__ import annotations

from typing import Any

from core.base_agent import AgentResponse, AgentRole, BaseAgent


class SecurityArchitect(BaseAgent):
    """Claude sub-agent: designs defense-in-depth security posture.

    Makes real Claude API calls to perform STRIDE threat modeling,
    design auth systems, and plan security monitoring.
    """

    def __init__(self, model: str = "sonnet"):
        super().__init__(
            role=AgentRole.SECURITY_ARCHITECT,
            name="Security Architect",
            expertise=[
                "OWASP Top 10",
                "STRIDE threat modeling",
                "zero trust architecture",
                "OAuth 2.0 / OIDC",
                "encryption at rest and in transit",
                "secrets management",
                "RBAC / ABAC authorization",
                "SOC2, ISO 27001 compliance",
            ],
            model=model,
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are a Security Architect sub-agent who designs systems that are "
            "secure by default. You follow OWASP guidelines and use STRIDE.\n\n"
            "Your responsibilities:\n"
            "1. STRIDE threat modeling for each component\n"
            "2. Authentication system design (OAuth 2.0, OIDC)\n"
            "3. Authorization model (RBAC, ABAC, or hybrid)\n"
            "4. Encryption strategy (at rest, in transit, E2E)\n"
            "5. Secrets management approach\n"
            "6. Security monitoring and incident response\n"
            "7. Security headers and CSP policies\n"
            "8. Audit logging strategy\n"
            "9. Compliance requirements (SOC2, GDPR, HIPAA)\n\n"
            "Security is built in, not bolted on. Never roll your own crypto."
        )

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        if override := context.get("_override_prompt"):
            return override

        requirements = context.get("client_requirements", "")
        architecture = context.get("architecture_doc", {})
        topic = context.get("debate_topic", "")

        return (
            f"Design the security architecture:\n\n"
            f"## Requirements:\n{requirements}\n\n"
            f"## System Architecture:\n{architecture}\n\n"
            f"## Context:\n{topic}\n\n"
            "Deliver:\n"
            "1. STRIDE threat model for key components\n"
            "2. Authentication design\n"
            "3. Authorization model\n"
            "4. Encryption strategy\n"
            "5. Secrets management plan\n"
            "6. Security monitoring approach\n"
            "7. Compliance checklist"
        )
