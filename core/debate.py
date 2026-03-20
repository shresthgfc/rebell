"""Debate arena where Claude sub-agents challenge, defend, and refine proposals.

Each debate round involves real Claude API calls — agents genuinely argue,
critique, and improve each other's work through multi-turn conversations.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from core.base_agent import AgentResponse, BaseAgent

logger = logging.getLogger(__name__)


@dataclass
class DebateRound:
    """Record of a single debate round."""

    round_number: int
    proposals: list[AgentResponse]
    challenges: list[AgentResponse]
    refinements: list[AgentResponse]
    consensus_score: float


class DebateArena:
    """Orchestrates structured debates between Claude sub-agents.

    Each step is a real Claude API call:
    1. Each sub-agent produces an initial proposal (API call per agent).
    2. Sub-agents cross-challenge each other (API call per agent).
    3. Sub-agents refine based on challenges (API call per agent).
    4. Consensus is scored. If above threshold, debate ends.
    5. Otherwise, repeat with refined proposals.

    This ensures genuine intellectual conflict and idea improvement,
    not just a single-pass generation.
    """

    def __init__(
        self,
        max_rounds: int = 3,
        consensus_threshold: float = 0.75,
    ):
        self.max_rounds = max_rounds
        self.consensus_threshold = consensus_threshold
        self.rounds: list[DebateRound] = []

    def run_debate(
        self,
        agents: list[BaseAgent],
        context: dict[str, Any],
        topic: str,
    ) -> DebateResult:
        """Run a full debate cycle — each step invokes Claude sub-agents."""
        logger.info(f"=== DEBATE START: {topic[:80]}... ===")
        logger.info(f"    Agents: {', '.join(a.name for a in agents)}")
        logger.info(f"    Max rounds: {self.max_rounds}, threshold: {self.consensus_threshold}")

        # Step 1: Initial proposals (one API call per agent)
        debate_context = {**context, "debate_topic": topic}
        proposals = []
        for agent in agents:
            logger.info(f"  [Round 0] {agent.name} generating initial proposal...")
            response = agent.invoke(debate_context)
            proposals.append(response)
            logger.info(f"  [Round 0] {agent.name} done (confidence: {response.confidence:.2f})")

        current_proposals = proposals

        for round_num in range(1, self.max_rounds + 1):
            logger.info(f"\n  --- Debate Round {round_num}/{self.max_rounds} ---")

            # Step 2: Cross-challenge (each agent critiques the others)
            challenges = []
            for i, agent in enumerate(agents):
                other_proposals = [p for j, p in enumerate(current_proposals) if j != i]
                combined_text = "\n\n---\n\n".join(
                    f"**[{p.agent_role.value}]** (confidence: {p.confidence:.2f}):\n{p.content}"
                    for p in other_proposals
                )
                logger.info(f"  [Round {round_num}] {agent.name} challenging peers...")
                challenge = agent.challenge(combined_text, debate_context)
                challenges.append(challenge)

            # Step 3: Refine based on challenges
            refinements = []
            for i, agent in enumerate(agents):
                relevant_challenges = [c for j, c in enumerate(challenges) if j != i]
                logger.info(f"  [Round {round_num}] {agent.name} refining proposal...")
                refinement = agent.refine(relevant_challenges, debate_context)
                refinements.append(refinement)

            # Step 4: Compute consensus
            consensus_score = self._compute_consensus(refinements)
            logger.info(f"  [Round {round_num}] Consensus score: {consensus_score:.2f}")

            self.rounds.append(DebateRound(
                round_number=round_num,
                proposals=current_proposals,
                challenges=challenges,
                refinements=refinements,
                consensus_score=consensus_score,
            ))

            current_proposals = refinements

            if consensus_score >= self.consensus_threshold:
                logger.info(f"  === CONSENSUS REACHED at round {round_num}! ===")
                break

        final_score = self.rounds[-1].consensus_score if self.rounds else 0.0
        logger.info(f"=== DEBATE END: {len(self.rounds)} rounds, score={final_score:.2f} ===")

        return DebateResult(
            final_proposals=current_proposals,
            rounds=self.rounds,
            consensus_reached=final_score >= self.consensus_threshold,
            total_rounds=len(self.rounds),
            final_consensus_score=final_score,
        )

    def _compute_consensus(self, responses: list[AgentResponse]) -> float:
        """Score consensus based on agent confidence and remaining concerns."""
        if not responses:
            return 0.0

        avg_confidence = sum(r.confidence for r in responses) / len(responses)
        total_concerns = sum(len(r.concerns) for r in responses)
        concern_factor = max(0.0, 1.0 - (total_concerns / (len(responses) * 5)))

        return 0.6 * avg_confidence + 0.4 * concern_factor


@dataclass
class DebateResult:
    """Output of a completed debate between Claude sub-agents."""

    final_proposals: list[AgentResponse]
    rounds: list[DebateRound]
    consensus_reached: bool
    total_rounds: int
    final_consensus_score: float

    @property
    def best_proposal(self) -> AgentResponse:
        return max(self.final_proposals, key=lambda p: p.confidence)

    @property
    def merged_concerns(self) -> list[str]:
        seen: set[str] = set()
        concerns: list[str] = []
        for p in self.final_proposals:
            for c in p.concerns:
                if c not in seen:
                    seen.add(c)
                    concerns.append(c)
        return concerns

    @property
    def merged_artifacts(self) -> dict[str, Any]:
        merged: dict[str, Any] = {}
        for p in self.final_proposals:
            merged.update(p.artifacts)
        return merged
