"""Code Reviewer — Claude sub-agent that reviews implementation quality."""

from __future__ import annotations

from typing import Any

from core.base_agent import AgentRole, BaseAgent


class CodeReviewer(BaseAgent):
    """Claude sub-agent: reviews code quality, patterns, and standards.

    Makes real Claude API calls to perform thorough code reviews
    checking for SOLID violations, security issues, and maintainability.
    """

    def __init__(self, model: str = "sonnet"):
        super().__init__(
            role=AgentRole.CODE_REVIEWER,
            name="Code Reviewer",
            expertise=[
                "code quality analysis",
                "SOLID principles",
                "design pattern review",
                "security code review",
                "performance code review",
                "maintainability assessment",
                "technical debt identification",
                "refactoring recommendations",
            ],
            model=model,
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are a senior Code Reviewer sub-agent who ensures code meets "
            "the highest quality standards. You review for correctness, "
            "maintainability, security, and performance.\n\n"
            "Your review checklist:\n"
            "1. SOLID principle adherence\n"
            "2. Design pattern appropriateness\n"
            "3. Error handling completeness\n"
            "4. Security vulnerabilities (injection, XSS, CSRF)\n"
            "5. Performance anti-patterns (N+1 queries, memory leaks)\n"
            "6. Test coverage adequacy\n"
            "7. Naming conventions and readability\n"
            "8. Documentation completeness\n"
            "9. Edge case handling\n"
            "10. Technical debt introduced\n\n"
            "Be thorough but constructive. Every criticism comes with a solution."
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
            f"Review the implementation plan:\n\n"
            f"## Requirements:\n{requirements}\n\n"
            f"## Architecture:\n{architecture}\n\n"
            f"## Implementation Plan:\n{impl_plan}\n\n"
            f"## Test Plan:\n{test_plan}\n\n"
            f"## Context:\n{topic}\n\n"
            "Deliver:\n"
            "1. Quality assessment (1-10 score with justification)\n"
            "2. SOLID principle compliance review\n"
            "3. Security review findings\n"
            "4. Performance review findings\n"
            "5. Maintainability assessment\n"
            "6. Technical debt risks\n"
            "7. Required changes (blockers)\n"
            "8. Recommended improvements (non-blockers)"
        )
