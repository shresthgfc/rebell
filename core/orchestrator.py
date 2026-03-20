"""Top-level orchestrator — runs the full Claude sub-agent pipeline.

The Orchestrator is the 'CEO' that coordinates all Claude sub-agents
through discovery, architecture, implementation, QA, and review phases.
Each phase involves real Claude API calls and structured debates.
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any, Callable

import anthropic

from core.base_agent import AgentResponse, BaseAgent
from core.context import PhaseResult, ProjectContext
from core.debate import DebateArena

logger = logging.getLogger(__name__)


class Phase:
    """A single phase of the development pipeline."""

    def __init__(
        self,
        name: str,
        description: str,
        agents: list[BaseAgent],
        topic_builder: Callable[[ProjectContext], str] | None = None,
        max_debate_rounds: int = 3,
        consensus_threshold: float = 0.75,
    ):
        self.name = name
        self.description = description
        self.agents = agents
        self.topic_builder = topic_builder
        self.max_debate_rounds = max_debate_rounds
        self.consensus_threshold = consensus_threshold


class Orchestrator:
    """Runs the full multi-agent software development lifecycle.

    Each phase runs a debate between specialized Claude sub-agents.
    A synthesizer sub-agent merges the debate results into a cohesive
    deliverable before passing to the next phase.
    """

    def __init__(
        self,
        phases: list[Phase] | None = None,
        synthesizer_model: str = "claude-sonnet-4-6",
    ):
        self.phases: list[Phase] = phases or []
        self.context: ProjectContext | None = None
        self.synthesizer_model = synthesizer_model
        self.client = anthropic.Anthropic()

    def add_phase(self, phase: Phase) -> None:
        self.phases.append(phase)

    def run(
        self,
        client_requirements: str,
        project_name: str = "Untitled Project",
        constraints: dict[str, Any] | None = None,
        budget_tier: str = "standard",
        timeline: str = "standard",
    ) -> ProjectContext:
        """Run the full pipeline — all phases with Claude sub-agent debates."""
        logger.info(f"\n{'='*60}")
        logger.info(f"  PROJECT: {project_name}")
        logger.info(f"  Budget: {budget_tier} | Timeline: {timeline}")
        logger.info(f"  Phases: {len(self.phases)}")
        logger.info(f"{'='*60}\n")

        self.context = ProjectContext(
            client_requirements=client_requirements,
            project_name=project_name,
            client_constraints=constraints or {},
            budget_tier=budget_tier,
            timeline=timeline,
        )

        for phase in self.phases:
            self._run_phase(phase)

        # Final synthesis across all phases
        self._final_synthesis()

        logger.info(f"\n{'='*60}")
        logger.info(f"  PROJECT COMPLETE: {project_name}")
        logger.info(f"  Phases: {len(self.context.phase_results)}")
        logger.info(f"  Decisions: {len(self.context.decisions)}")
        logger.info(f"  Risks: {len(self.context.risks)}")
        logger.info(f"{'='*60}")

        return self.context

    def _run_phase(self, phase: Phase) -> None:
        """Execute a single phase with Claude sub-agent debate."""
        logger.info(f"\n{'─'*50}")
        logger.info(f"  PHASE: {phase.name}")
        logger.info(f"  {phase.description}")
        logger.info(f"  Sub-agents: {', '.join(a.name for a in phase.agents)}")
        logger.info(f"{'─'*50}")

        start_time = time.time()
        self.context.current_phase = phase.name

        # Build debate topic
        if phase.topic_builder:
            topic = phase.topic_builder(self.context)
        else:
            topic = self._default_topic(phase)

        # Run debate between Claude sub-agents
        arena = DebateArena(
            max_rounds=phase.max_debate_rounds,
            consensus_threshold=phase.consensus_threshold,
        )
        context_dict = {**self.context.to_dict(), "_phase": phase.name}
        debate_result = arena.run_debate(phase.agents, context_dict, topic)

        # Synthesize debate results via another Claude sub-agent call
        synthesis = self._synthesize_phase(phase, debate_result.final_proposals)

        # Merge artifacts
        merged_artifacts = debate_result.merged_artifacts
        merged_artifacts["synthesis"] = synthesis
        self._apply_artifacts(phase.name, merged_artifacts)

        # Record risks
        for concern in debate_result.merged_concerns:
            self.context.add_risk(
                phase=phase.name,
                risk=concern,
                severity="medium",
                mitigation="To be addressed in subsequent phases",
            )

        duration = time.time() - start_time

        phase_result = PhaseResult(
            phase_name=phase.name,
            responses=debate_result.final_proposals,
            debate_rounds=debate_result.total_rounds,
            consensus_reached=debate_result.consensus_reached,
            final_artifacts=merged_artifacts,
            duration_seconds=duration,
            summary=synthesis,
        )
        self.context.phase_results[phase.name] = phase_result

        logger.info(f"  Phase '{phase.name}' completed in {duration:.1f}s")

    def _synthesize_phase(self, phase: Phase, proposals: list[AgentResponse]) -> str:
        """Use a Claude sub-agent to synthesize all debate outputs into one cohesive document."""
        proposals_text = "\n\n---\n\n".join(
            f"## {p.agent_role.value} (confidence: {p.confidence:.2f})\n\n"
            f"{p.content}\n\n"
            f"**Concerns:** {', '.join(p.concerns) if p.concerns else 'None'}\n"
            f"**Suggestions:** {', '.join(p.suggestions) if p.suggestions else 'None'}"
            for p in proposals
        )

        response = self.client.messages.create(
            model=self.synthesizer_model,
            max_tokens=4096,
            system=(
                "You are a senior Technical Program Manager synthesizing outputs from "
                "multiple specialist sub-agents into a single cohesive deliverable. "
                "Merge overlapping insights, resolve conflicts, and produce an "
                "actionable summary that downstream teams can execute on."
            ),
            messages=[{
                "role": "user",
                "content": (
                    f"# Phase: {phase.name}\n\n"
                    f"## Description: {phase.description}\n\n"
                    f"Synthesize these specialist outputs into one cohesive document:\n\n"
                    f"{proposals_text}\n\n"
                    "Produce a unified, non-redundant summary with clear action items."
                ),
            }],
        )

        return response.content[0].text

    def _final_synthesis(self) -> None:
        """Final cross-phase synthesis to produce the complete deliverable."""
        if not self.context.phase_results:
            return

        phase_summaries = "\n\n".join(
            f"## {name}\n{result.summary[:1000]}"
            for name, result in self.context.phase_results.items()
        )

        response = self.client.messages.create(
            model=self.synthesizer_model,
            max_tokens=8192,
            system=(
                "You are the Chief Technical Officer reviewing the complete output "
                "of a multi-phase development planning process. Produce a final "
                "executive summary with key decisions, risks, and next steps."
            ),
            messages=[{
                "role": "user",
                "content": (
                    f"# Project: {self.context.project_name}\n\n"
                    f"## Requirements:\n{self.context.client_requirements}\n\n"
                    f"## Phase Results:\n{phase_summaries}\n\n"
                    "Produce:\n"
                    "1. Executive summary\n"
                    "2. Key architectural decisions\n"
                    "3. Critical risks and mitigations\n"
                    "4. Implementation roadmap\n"
                    "5. Success metrics"
                ),
            }],
        )

        self.context.review_report["final_synthesis"] = response.content[0].text

    def _default_topic(self, phase: Phase) -> str:
        prev_summaries = ""
        for name, result in self.context.phase_results.items():
            prev_summaries += f"\n### {name}:\n{result.summary[:500]}\n"

        return (
            f"# Phase: {phase.name}\n"
            f"## Objective: {phase.description}\n\n"
            f"## Project: {self.context.project_name}\n"
            f"## Client Requirements:\n{self.context.client_requirements}\n"
            f"## Budget: {self.context.budget_tier} | Timeline: {self.context.timeline}\n"
            f"## Previous Phase Results:{prev_summaries or ' (First phase)'}\n\n"
            f"Produce your specialist analysis for this phase."
        )

    def _apply_artifacts(self, phase_name: str, artifacts: dict[str, Any]) -> None:
        mapping = {
            "discovery": "requirements_doc",
            "architecture": "architecture_doc",
            "design": "design_doc",
            "implementation": "implementation_plan",
            "qa": "test_plan",
            "review": "review_report",
        }
        for key, attr in mapping.items():
            if key in phase_name.lower():
                current = getattr(self.context, attr)
                current.update(artifacts)
                break
