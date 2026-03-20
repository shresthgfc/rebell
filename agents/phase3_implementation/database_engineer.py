"""Database Engineer — Claude sub-agent that implements data access layer."""

from __future__ import annotations

from typing import Any

from core.base_agent import AgentRole, BaseAgent


class DatabaseEngineer(BaseAgent):
    """Claude sub-agent: implements database schemas, migrations, and queries.

    Makes real Claude API calls to produce migration scripts, query
    optimization plans, and data access layer implementations.
    """

    def __init__(self, model: str = "claude-sonnet-4-6"):
        super().__init__(
            role=AgentRole.DATABASE_ENGINEER,
            name="Database Engineer",
            expertise=[
                "SQL optimization",
                "ORM configuration",
                "database migrations",
                "indexing strategies",
                "connection pooling",
                "query performance tuning",
                "data seeding and fixtures",
                "database monitoring",
            ],
            model=model,
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are a senior Database Engineer sub-agent who implements "
            "performant, reliable data access layers.\n\n"
            "Your responsibilities:\n"
            "1. Design migration scripts (up/down, reversible)\n"
            "2. Define indexing strategy based on query patterns\n"
            "3. Configure ORM or query builder\n"
            "4. Design connection pooling strategy\n"
            "5. Plan query optimization approach\n"
            "6. Design seed data and test fixtures\n"
            "7. Plan database monitoring queries\n"
            "8. Design data archival strategy\n\n"
            "Measure twice, query once. Every query should use an index."
        )

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        if override := context.get("_override_prompt"):
            return override

        requirements = context.get("client_requirements", "")
        architecture = context.get("architecture_doc", {})
        topic = context.get("debate_topic", "")

        return (
            f"Design the data access implementation:\n\n"
            f"## Requirements:\n{requirements}\n\n"
            f"## Database Architecture:\n{architecture}\n\n"
            f"## Context:\n{topic}\n\n"
            "Deliver:\n"
            "1. Migration scripts outline (key tables, relationships)\n"
            "2. Indexing strategy\n"
            "3. ORM/query builder configuration\n"
            "4. Connection pooling setup\n"
            "5. Key query patterns (with optimization notes)\n"
            "6. Seed data plan\n"
            "7. Monitoring queries"
        )
