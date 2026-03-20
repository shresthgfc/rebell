"""Project context that flows through the entire agent pipeline."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from core.base_agent import AgentResponse


@dataclass
class PhaseResult:
    """Result of a completed phase."""

    phase_name: str
    responses: list[AgentResponse]
    debate_rounds: int
    consensus_reached: bool
    final_artifacts: dict[str, Any]
    duration_seconds: float
    summary: str


@dataclass
class ProjectContext:
    """Shared context that accumulates knowledge as it passes through phases.

    This is the 'single source of truth' for the project. Each phase reads
    from it and writes its outputs back, so downstream phases have access
    to all upstream decisions.
    """

    # Client input
    client_requirements: str
    project_name: str = "Untitled Project"
    client_constraints: dict[str, Any] = field(default_factory=dict)
    budget_tier: str = "standard"  # "startup", "standard", "enterprise"
    timeline: str = "standard"  # "urgent", "standard", "relaxed"

    # Accumulated artifacts from each phase
    phase_results: dict[str, PhaseResult] = field(default_factory=dict)

    # Living documents updated by agents
    requirements_doc: dict[str, Any] = field(default_factory=dict)
    architecture_doc: dict[str, Any] = field(default_factory=dict)
    design_doc: dict[str, Any] = field(default_factory=dict)
    implementation_plan: dict[str, Any] = field(default_factory=dict)
    test_plan: dict[str, Any] = field(default_factory=dict)
    review_report: dict[str, Any] = field(default_factory=dict)

    # Risk register
    risks: list[dict[str, Any]] = field(default_factory=list)

    # Decision log
    decisions: list[dict[str, Any]] = field(default_factory=list)

    # Metadata
    created_at: float = field(default_factory=time.time)
    current_phase: str = ""

    def add_decision(self, phase: str, decision: str, rationale: str, agents_involved: list[str]) -> None:
        self.decisions.append({
            "phase": phase,
            "decision": decision,
            "rationale": rationale,
            "agents_involved": agents_involved,
            "timestamp": time.time(),
        })

    def add_risk(self, phase: str, risk: str, severity: str, mitigation: str) -> None:
        self.risks.append({
            "phase": phase,
            "risk": risk,
            "severity": severity,
            "mitigation": mitigation,
            "timestamp": time.time(),
        })

    def get_phase_summary(self, phase_name: str) -> str:
        """Get a text summary of a completed phase for downstream agents."""
        result = self.phase_results.get(phase_name)
        if not result:
            return f"Phase '{phase_name}' has not been completed yet."
        return result.summary

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_name": self.project_name,
            "client_requirements": self.client_requirements,
            "client_constraints": self.client_constraints,
            "budget_tier": self.budget_tier,
            "timeline": self.timeline,
            "requirements_doc": self.requirements_doc,
            "architecture_doc": self.architecture_doc,
            "design_doc": self.design_doc,
            "implementation_plan": self.implementation_plan,
            "test_plan": self.test_plan,
            "review_report": self.review_report,
            "risks": self.risks,
            "decisions": self.decisions,
            "phases_completed": list(self.phase_results.keys()),
        }
