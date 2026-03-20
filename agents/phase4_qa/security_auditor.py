"""Security Auditor — Claude sub-agent that reviews security posture."""

from __future__ import annotations

from typing import Any

from core.base_agent import AgentRole, BaseAgent


class SecurityAuditor(BaseAgent):
    """Claude sub-agent: performs security review and vulnerability assessment.

    Makes real Claude API calls to audit the design against OWASP Top 10,
    review auth flows, and identify injection points.
    """

    def __init__(self, model: str = "sonnet"):
        super().__init__(
            role=AgentRole.SECURITY_AUDITOR,
            name="Security Auditor",
            expertise=[
                "OWASP Top 10 audit",
                "authentication flow review",
                "injection vulnerability detection",
                "SAST/DAST tooling",
                "dependency vulnerability scanning",
                "secrets detection",
                "CSP and header analysis",
                "penetration test planning",
            ],
            model=model,
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are a Security Auditor sub-agent who reviews designs and "
            "implementation plans for security vulnerabilities.\n\n"
            "Your responsibilities:\n"
            "1. Audit against OWASP Top 10\n"
            "2. Review authentication and session management\n"
            "3. Identify injection points (SQL, XSS, CSRF, etc.)\n"
            "4. Review authorization logic for bypass risks\n"
            "5. Assess dependency security (known CVEs)\n"
            "6. Review secrets handling\n"
            "7. Recommend SAST/DAST tools for CI pipeline\n"
            "8. Design penetration test scope\n\n"
            "Assume every input is malicious. Trust nothing."
        )

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        if override := context.get("_override_prompt"):
            return override

        requirements = context.get("client_requirements", "")
        architecture = context.get("architecture_doc", {})
        impl_plan = context.get("implementation_plan", {})
        topic = context.get("debate_topic", "")

        return (
            f"Perform security audit:\n\n"
            f"## Requirements:\n{requirements}\n\n"
            f"## Architecture:\n{architecture}\n\n"
            f"## Implementation Plan:\n{impl_plan}\n\n"
            f"## Context:\n{topic}\n\n"
            "Deliver:\n"
            "1. OWASP Top 10 audit results\n"
            "2. Auth flow security review\n"
            "3. Injection point analysis\n"
            "4. Authorization bypass risks\n"
            "5. Dependency security assessment\n"
            "6. SAST/DAST tool recommendations\n"
            "7. Penetration test scope"
        )
