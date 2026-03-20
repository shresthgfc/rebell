"""Accessibility Tester — Claude sub-agent that validates WCAG compliance."""

from __future__ import annotations

from typing import Any

from core.base_agent import AgentRole, BaseAgent


class AccessibilityTester(BaseAgent):
    """Claude sub-agent: validates accessibility and assistive tech support.

    Makes real Claude API calls to review designs against WCAG 2.1 AA,
    plan screen reader testing, and audit keyboard navigation.
    """

    def __init__(self, model: str = "claude-sonnet-4-6"):
        super().__init__(
            role=AgentRole.ACCESSIBILITY_TESTER,
            name="Accessibility Tester",
            expertise=[
                "WCAG 2.1 AA compliance",
                "screen reader testing",
                "keyboard navigation",
                "color contrast analysis",
                "ARIA attributes",
                "assistive technology",
                "axe-core and Lighthouse",
                "inclusive design",
            ],
            model=model,
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are an Accessibility Tester sub-agent who ensures products "
            "are usable by everyone, including people with disabilities.\n\n"
            "Your responsibilities:\n"
            "1. Review designs against WCAG 2.1 AA criteria\n"
            "2. Audit keyboard navigation and focus management\n"
            "3. Review color contrast ratios\n"
            "4. Validate ARIA usage and semantic HTML\n"
            "5. Plan screen reader testing (NVDA, VoiceOver, JAWS)\n"
            "6. Design automated a11y testing in CI\n"
            "7. Review form labeling and error messaging\n"
            "8. Audit animation and motion for vestibular disorders\n\n"
            "Accessibility is not a feature — it's a right."
        )

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        if override := context.get("_override_prompt"):
            return override

        requirements = context.get("client_requirements", "")
        design = context.get("design_doc", {})
        topic = context.get("debate_topic", "")

        return (
            f"Perform accessibility review:\n\n"
            f"## Requirements:\n{requirements}\n\n"
            f"## UX Design:\n{design}\n\n"
            f"## Context:\n{topic}\n\n"
            "Deliver:\n"
            "1. WCAG 2.1 AA compliance checklist\n"
            "2. Keyboard navigation audit\n"
            "3. Color contrast review\n"
            "4. ARIA and semantic HTML review\n"
            "5. Screen reader test plan\n"
            "6. Automated a11y testing setup\n"
            "7. Remediation priorities"
        )
