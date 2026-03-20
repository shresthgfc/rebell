"""Database Architect — Claude sub-agent that designs data models and storage."""

from __future__ import annotations

from typing import Any

from core.base_agent import AgentResponse, AgentRole, BaseAgent


class DatabaseArchitect(BaseAgent):
    """Claude sub-agent: designs the data layer with CAP theorem awareness.

    Makes real Claude API calls to design ER models, choose storage
    engines, and plan data migration strategies.
    """

    def __init__(self, model: str = "sonnet"):
        super().__init__(
            role=AgentRole.DATABASE_ARCHITECT,
            name="Database Architect",
            expertise=[
                "relational database design",
                "NoSQL data modeling",
                "CAP theorem trade-offs",
                "database sharding and partitioning",
                "data migration strategies",
                "GDPR and data compliance",
                "caching strategies",
            ],
            model=model,
        )

    @property
    def system_prompt(self) -> str:
        return (
            "You are a senior Database Architect sub-agent specializing in "
            "scalable data systems. You design data models that balance "
            "consistency, availability, and performance.\n\n"
            "Your responsibilities:\n"
            "1. Design entity-relationship models\n"
            "2. Choose storage engines with justification\n"
            "3. Define data access patterns and optimize for them\n"
            "4. Design caching strategy\n"
            "5. Plan data migration and versioning\n"
            "6. Address GDPR, CCPA, data residency\n"
            "7. Design backup and disaster recovery\n"
            "8. Define data retention policies\n\n"
            "Design for query patterns, not just data structure."
        )

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        if override := context.get("_override_prompt"):
            return override

        requirements = context.get("client_requirements", "")
        architecture = context.get("architecture_doc", {})
        topic = context.get("debate_topic", "")

        return (
            f"Design the database architecture:\n\n"
            f"## Requirements:\n{requirements}\n\n"
            f"## System Architecture:\n{architecture}\n\n"
            f"## Context:\n{topic}\n\n"
            "Deliver:\n"
            "1. Entity-relationship model (entities, attributes, relationships)\n"
            "2. Storage engine selection with justification\n"
            "3. Access pattern analysis\n"
            "4. Caching strategy\n"
            "5. Migration strategy\n"
            "6. Compliance measures\n"
            "7. Backup and DR plan"
        )
