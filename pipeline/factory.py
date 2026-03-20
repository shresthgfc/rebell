"""Pipeline factory — assembles the full multi-agent dev org pipeline.

This is the main entry point for creating a configured pipeline with
all 25 Claude sub-agents organized across 5 phases.
"""

from __future__ import annotations

from typing import Any, Callable

from agents.phase1_discovery import (
    BrainstormFacilitator,
    DevilAdvocate,
    InnovationScout,
    MarketResearcher,
    RequirementsAnalyst,
)
from agents.phase2_architecture import (
    APIDesigner,
    DatabaseArchitect,
    SecurityArchitect,
    SystemArchitect,
    UXDesigner,
)
from agents.phase3_implementation import (
    BackendDeveloper,
    DatabaseEngineer,
    DevOpsEngineer,
    FrontendDeveloper,
    TechLead,
)
from agents.phase4_qa import (
    AccessibilityTester,
    PerformanceEngineer,
    QALead,
    SecurityAuditor,
    TestEngineer,
)
from agents.phase5_review import (
    CodeReviewer,
    ReleaseManager,
    StakeholderLiaison,
    TechnicalWriter,
)
from core.context import ProjectContext
from core.orchestrator import Orchestrator, Phase


class PipelineFactory:
    """Creates a fully configured dev org pipeline.

    Supports three preset configurations:
    - "full": All 25 sub-agents, 5 phases, 3 debate rounds (enterprise)
    - "standard": 15 key sub-agents, 5 phases, 2 debate rounds (standard)
    - "lean": 8 essential sub-agents, 3 phases, 1 debate round (startup)
    """

    @staticmethod
    def create(
        preset: str = "full",
        model: str = "claude-sonnet-4-6",
        max_debate_rounds: int | None = None,
        consensus_threshold: float = 0.75,
    ) -> Orchestrator:
        """Create a pipeline with the given preset configuration."""
        builders = {
            "full": PipelineFactory._build_full,
            "standard": PipelineFactory._build_standard,
            "lean": PipelineFactory._build_lean,
        }

        builder = builders.get(preset)
        if not builder:
            raise ValueError(f"Unknown preset: {preset}. Use: full, standard, lean")

        return builder(model, max_debate_rounds, consensus_threshold)

    @staticmethod
    def _build_full(
        model: str,
        max_rounds: int | None,
        threshold: float,
    ) -> Orchestrator:
        """Full pipeline: 25 sub-agents, 5 phases, 3 debate rounds."""
        rounds = max_rounds or 3

        phases = [
            Phase(
                name="Phase 1: Discovery & Brainstorming",
                description=(
                    "Transform raw client requirements into validated, structured, "
                    "and prioritized requirements through multi-agent debate."
                ),
                agents=[
                    RequirementsAnalyst(model),
                    MarketResearcher(model),
                    BrainstormFacilitator(model),
                    DevilAdvocate(model),
                    InnovationScout(model),
                ],
                max_debate_rounds=rounds,
                consensus_threshold=threshold,
            ),
            Phase(
                name="Phase 2: Architecture & Design",
                description=(
                    "Design the system architecture, data model, API contracts, "
                    "security posture, and user experience through specialist debate."
                ),
                agents=[
                    SystemArchitect(model),
                    DatabaseArchitect(model),
                    APIDesigner(model),
                    SecurityArchitect(model),
                    UXDesigner(model),
                ],
                max_debate_rounds=rounds,
                consensus_threshold=threshold,
            ),
            Phase(
                name="Phase 3: Implementation Planning",
                description=(
                    "Decompose architecture into implementable tasks, design code "
                    "structure, CI/CD pipelines, and data access layer."
                ),
                agents=[
                    TechLead(model),
                    BackendDeveloper(model),
                    FrontendDeveloper(model),
                    DevOpsEngineer(model),
                    DatabaseEngineer(model),
                ],
                max_debate_rounds=rounds,
                consensus_threshold=threshold,
            ),
            Phase(
                name="Phase 4: Quality Assurance",
                description=(
                    "Design test strategy, test cases, performance benchmarks, "
                    "security audit, and accessibility validation."
                ),
                agents=[
                    QALead(model),
                    TestEngineer(model),
                    PerformanceEngineer(model),
                    SecurityAuditor(model),
                    AccessibilityTester(model),
                ],
                max_debate_rounds=rounds,
                consensus_threshold=threshold,
            ),
            Phase(
                name="Phase 5: Review & Delivery",
                description=(
                    "Final code review, documentation planning, release strategy, "
                    "and stakeholder communication."
                ),
                agents=[
                    CodeReviewer(model),
                    TechnicalWriter(model),
                    ReleaseManager(model),
                    StakeholderLiaison(model),
                ],
                max_debate_rounds=rounds,
                consensus_threshold=threshold,
            ),
        ]

        return Orchestrator(phases=phases, synthesizer_model=model)

    @staticmethod
    def _build_standard(
        model: str,
        max_rounds: int | None,
        threshold: float,
    ) -> Orchestrator:
        """Standard pipeline: 15 key sub-agents, 5 phases, 2 debate rounds."""
        rounds = max_rounds or 2

        phases = [
            Phase(
                name="Phase 1: Discovery",
                description="Requirements analysis and risk identification.",
                agents=[
                    RequirementsAnalyst(model),
                    BrainstormFacilitator(model),
                    DevilAdvocate(model),
                ],
                max_debate_rounds=rounds,
                consensus_threshold=threshold,
            ),
            Phase(
                name="Phase 2: Architecture",
                description="System and data architecture design.",
                agents=[
                    SystemArchitect(model),
                    DatabaseArchitect(model),
                    SecurityArchitect(model),
                ],
                max_debate_rounds=rounds,
                consensus_threshold=threshold,
            ),
            Phase(
                name="Phase 3: Implementation",
                description="Implementation planning and code structure.",
                agents=[
                    TechLead(model),
                    BackendDeveloper(model),
                    FrontendDeveloper(model),
                ],
                max_debate_rounds=rounds,
                consensus_threshold=threshold,
            ),
            Phase(
                name="Phase 4: QA",
                description="Test strategy and security audit.",
                agents=[
                    QALead(model),
                    TestEngineer(model),
                    SecurityAuditor(model),
                ],
                max_debate_rounds=rounds,
                consensus_threshold=threshold,
            ),
            Phase(
                name="Phase 5: Review",
                description="Code review, documentation, and release planning.",
                agents=[
                    CodeReviewer(model),
                    TechnicalWriter(model),
                    ReleaseManager(model),
                ],
                max_debate_rounds=rounds,
                consensus_threshold=threshold,
            ),
        ]

        return Orchestrator(phases=phases, synthesizer_model=model)

    @staticmethod
    def _build_lean(
        model: str,
        max_rounds: int | None,
        threshold: float,
    ) -> Orchestrator:
        """Lean pipeline: 8 essential sub-agents, 3 phases, 1 debate round."""
        rounds = max_rounds or 1

        phases = [
            Phase(
                name="Discovery & Design",
                description="Combined requirements, architecture, and risk analysis.",
                agents=[
                    RequirementsAnalyst(model),
                    SystemArchitect(model),
                    DevilAdvocate(model),
                ],
                max_debate_rounds=rounds,
                consensus_threshold=threshold,
            ),
            Phase(
                name="Implementation & QA",
                description="Implementation planning with built-in quality assurance.",
                agents=[
                    TechLead(model),
                    BackendDeveloper(model),
                    QALead(model),
                ],
                max_debate_rounds=rounds,
                consensus_threshold=threshold,
            ),
            Phase(
                name="Review & Delivery",
                description="Final review and stakeholder delivery.",
                agents=[
                    CodeReviewer(model),
                    StakeholderLiaison(model),
                ],
                max_debate_rounds=rounds,
                consensus_threshold=threshold,
            ),
        ]

        return Orchestrator(phases=phases, synthesizer_model=model)
