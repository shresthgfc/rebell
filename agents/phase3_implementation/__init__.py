"""Phase 3: Implementation Claude sub-agents.

Takes architecture/design and produces implementation plans, code structure,
CI/CD pipelines, and infrastructure as code — all via Claude API calls.

Sub-agents:
- Tech Lead: Decomposes work, defines coding standards, manages dependencies
- Backend Developer: Designs backend code structure, patterns, and APIs
- Frontend Developer: Designs frontend architecture, components, state management
- DevOps Engineer: Designs CI/CD, infrastructure, and deployment pipelines
- Database Engineer: Implements migrations, queries, and data access layer
"""

from agents.phase3_implementation.tech_lead import TechLead
from agents.phase3_implementation.backend_developer import BackendDeveloper
from agents.phase3_implementation.frontend_developer import FrontendDeveloper
from agents.phase3_implementation.devops_engineer import DevOpsEngineer
from agents.phase3_implementation.database_engineer import DatabaseEngineer

__all__ = [
    "TechLead",
    "BackendDeveloper",
    "FrontendDeveloper",
    "DevOpsEngineer",
    "DatabaseEngineer",
]
