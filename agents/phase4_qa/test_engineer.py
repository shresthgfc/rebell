"""Test Engineer — Claude sub-agent that designs test cases and automation."""

from __future__ import annotations

from typing import Any

from core.base_agent import AgentRole, BaseAgent


class TestEngineer(BaseAgent):
    """Claude sub-agent: designs detailed test cases and test automation.

    Makes real Claude API calls to produce test suites, boundary tests,
    and BDD-style acceptance tests.
    """

    def __init__(self, model: str = "claude-sonnet-4-6"):
        super().__init__(
            role=AgentRole.TEST_ENGINEER,
            name="Test Engineer",
            expertise=[
                "test case design",
                "boundary value analysis",
                "equivalence partitioning",
                "BDD / Gherkin",
                "test automation",
                "mocking and stubbing",
                "contract testing",
                "visual regression testing",
            ],
            model=model,
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are a Test Engineer sub-agent who designs thorough, "
            "maintainable test suites.\n\n"
            "Your responsibilities:\n"
            "1. Design test cases for each requirement\n"
            "2. Apply boundary value analysis and equivalence partitioning\n"
            "3. Write BDD scenarios (Given/When/Then)\n"
            "4. Design mocking and stubbing strategy\n"
            "5. Plan contract tests for service boundaries\n"
            "6. Design visual regression tests\n"
            "7. Plan test data fixtures\n"
            "8. Identify negative test cases and error paths\n\n"
            "A test not written is a bug not found."
        )

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        if override := context.get("_override_prompt"):
            return override

        requirements = context.get("client_requirements", "")
        req_doc = context.get("requirements_doc", {})
        topic = context.get("debate_topic", "")

        return (
            f"Design test cases:\n\n"
            f"## Requirements:\n{requirements}\n\n"
            f"## Requirements Doc:\n{req_doc}\n\n"
            f"## Context:\n{topic}\n\n"
            "Deliver:\n"
            "1. Test cases per requirement (happy path + edge cases)\n"
            "2. BDD scenarios for key user flows\n"
            "3. Negative test cases\n"
            "4. Boundary value tests\n"
            "5. Mocking strategy\n"
            "6. Contract test design\n"
            "7. Test data fixtures plan"
        )
