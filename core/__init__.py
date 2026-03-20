"""Core framework for the multi-agent development organization."""

from core.base_agent import BaseAgent, AgentRole, AgentResponse, invoke_claude_cli
from core.orchestrator import Orchestrator
from core.debate import DebateArena
from core.context import ProjectContext

__all__ = [
    "BaseAgent",
    "AgentRole",
    "AgentResponse",
    "invoke_claude_cli",
    "Orchestrator",
    "DebateArena",
    "ProjectContext",
]
