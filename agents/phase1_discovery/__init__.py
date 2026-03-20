"""Phase 1: Discovery & Brainstorming agents.

This phase takes raw client requirements and transforms them into a
well-structured, debated, and validated set of project requirements.

Agents in this phase:
- Requirements Analyst: Extracts, structures, and validates requirements
- Market Researcher: Analyzes competitive landscape and market fit
- Brainstorm Facilitator: Generates creative solutions and approaches
- Devil's Advocate: Challenges assumptions and identifies risks
- Innovation Scout: Identifies emerging tech and novel approaches
"""

from agents.phase1_discovery.requirements_analyst import RequirementsAnalyst
from agents.phase1_discovery.market_researcher import MarketResearcher
from agents.phase1_discovery.brainstorm_facilitator import BrainstormFacilitator
from agents.phase1_discovery.devil_advocate import DevilAdvocate
from agents.phase1_discovery.innovation_scout import InnovationScout

__all__ = [
    "RequirementsAnalyst",
    "MarketResearcher",
    "BrainstormFacilitator",
    "DevilAdvocate",
    "InnovationScout",
]
