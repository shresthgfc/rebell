"""API Designer — Claude sub-agent that designs API contracts and protocols."""

from __future__ import annotations

from typing import Any

from core.base_agent import AgentResponse, AgentRole, BaseAgent


class APIDesigner(BaseAgent):
    """Claude sub-agent: designs RESTful APIs following OpenAPI 3.1 standards.

    Makes real Claude API calls to produce endpoint designs, schema
    definitions, and versioning strategies.
    """

    def __init__(self, model: str = "claude-sonnet-4-6"):
        super().__init__(
            role=AgentRole.API_DESIGNER,
            name="API Designer",
            expertise=[
                "RESTful API design",
                "GraphQL schema design",
                "gRPC and Protocol Buffers",
                "OpenAPI 3.1 specifications",
                "API versioning strategies",
                "rate limiting and throttling",
                "webhook design",
            ],
            model=model,
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are a senior API Designer sub-agent who creates APIs that "
            "developers love. You follow REST best practices and design-first "
            "methodology.\n\n"
            "Your responsibilities:\n"
            "1. Design resource-oriented API endpoints\n"
            "2. Define request/response schemas with validation\n"
            "3. Design authentication and authorization flows\n"
            "4. Plan API versioning strategy\n"
            "5. Design rate limiting and quota policies\n"
            "6. Define error format (RFC 7807)\n"
            "7. Design webhook/event notification system\n"
            "8. Design pagination, filtering, sorting patterns\n\n"
            "REST maturity level 3. Consistent naming. Idempotent mutations."
        )

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        if override := context.get("_override_prompt"):
            return override

        requirements = context.get("client_requirements", "")
        architecture = context.get("architecture_doc", {})
        topic = context.get("debate_topic", "")

        return (
            f"Design the API layer:\n\n"
            f"## Requirements:\n{requirements}\n\n"
            f"## System Architecture:\n{architecture}\n\n"
            f"## Context:\n{topic}\n\n"
            "Deliver:\n"
            "1. API endpoints (method, path, description, request/response)\n"
            "2. Authentication design\n"
            "3. Versioning strategy\n"
            "4. Rate limiting policy\n"
            "5. Error response format\n"
            "6. Pagination pattern\n"
            "7. Webhook design (if applicable)"
        )
