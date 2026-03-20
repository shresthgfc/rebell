"""Base Claude sub-agent class — every agent is a real Claude API call."""

from __future__ import annotations

import json
import logging
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import anthropic

logger = logging.getLogger(__name__)


class AgentRole(Enum):
    """Roles agents can assume in the development organization."""

    # Phase 1: Discovery & Brainstorming
    REQUIREMENTS_ANALYST = "requirements_analyst"
    MARKET_RESEARCHER = "market_researcher"
    BRAINSTORM_FACILITATOR = "brainstorm_facilitator"
    DEVIL_ADVOCATE = "devil_advocate"
    INNOVATION_SCOUT = "innovation_scout"

    # Phase 2: Architecture & Design
    SYSTEM_ARCHITECT = "system_architect"
    DATABASE_ARCHITECT = "database_architect"
    API_DESIGNER = "api_designer"
    SECURITY_ARCHITECT = "security_architect"
    UX_DESIGNER = "ux_designer"

    # Phase 3: Implementation
    TECH_LEAD = "tech_lead"
    BACKEND_DEVELOPER = "backend_developer"
    FRONTEND_DEVELOPER = "frontend_developer"
    DEVOPS_ENGINEER = "devops_engineer"
    DATABASE_ENGINEER = "database_engineer"

    # Phase 4: Quality Assurance
    QA_LEAD = "qa_lead"
    TEST_ENGINEER = "test_engineer"
    PERFORMANCE_ENGINEER = "performance_engineer"
    SECURITY_AUDITOR = "security_auditor"
    ACCESSIBILITY_TESTER = "accessibility_tester"

    # Phase 5: Review & Delivery
    CODE_REVIEWER = "code_reviewer"
    TECHNICAL_WRITER = "technical_writer"
    RELEASE_MANAGER = "release_manager"
    STAKEHOLDER_LIAISON = "stakeholder_liaison"


# JSON schema for structured agent output
AGENT_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "analysis": {
            "type": "string",
            "description": "The agent's detailed analysis and recommendations",
        },
        "confidence": {
            "type": "number",
            "description": "Confidence level from 0.0 to 1.0",
        },
        "artifacts": {
            "type": "object",
            "description": "Structured deliverables from this agent",
        },
        "concerns": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Risks, issues, or concerns identified",
        },
        "suggestions": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Actionable suggestions for improvement",
        },
        "dependencies": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Dependencies on other agents or external factors",
        },
    },
    "required": ["analysis", "confidence", "artifacts", "concerns", "suggestions"],
}


@dataclass
class AgentResponse:
    """Structured response from a Claude sub-agent."""

    agent_id: str
    agent_role: AgentRole
    phase: str
    content: str
    confidence: float
    artifacts: dict[str, Any] = field(default_factory=dict)
    concerns: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    raw_response: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "agent_role": self.agent_role.value,
            "phase": self.phase,
            "content": self.content,
            "confidence": self.confidence,
            "artifacts": self.artifacts,
            "concerns": self.concerns,
            "suggestions": self.suggestions,
            "dependencies": self.dependencies,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
        }


class BaseAgent(ABC):
    """Abstract base class — each sub-agent calls Claude API directly.

    Every agent is a real Claude sub-agent with its own system prompt,
    conversation history, and structured output parsing. The agent calls
    the Anthropic API, parses the JSON response, and returns a structured
    AgentResponse.
    """

    def __init__(
        self,
        role: AgentRole,
        name: str,
        expertise: list[str],
        model: str = "claude-sonnet-4-6",
        max_tokens: int = 4096,
    ):
        self.id = str(uuid.uuid4())[:8]
        self.role = role
        self.name = name
        self.expertise = expertise
        self.model = model
        self.max_tokens = max_tokens
        self.conversation_history: list[dict[str, str]] = []
        self.client = anthropic.Anthropic()

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """The system prompt that defines this sub-agent's persona and behavior."""

    @abstractmethod
    def build_user_prompt(self, context: dict[str, Any]) -> str:
        """Build the user-facing prompt from the current project context."""

    def invoke(self, context: dict[str, Any]) -> AgentResponse:
        """Invoke this Claude sub-agent via the Anthropic API.

        This is the core method — it calls the Claude API with the agent's
        system prompt and context, then parses the structured JSON response.
        """
        user_prompt = self.build_user_prompt(context)

        # Wrap the prompt to request structured JSON output
        structured_prompt = (
            f"{user_prompt}\n\n"
            "---\n"
            "Respond with a JSON object containing:\n"
            '- "analysis": your detailed analysis (string)\n'
            '- "confidence": your confidence level 0.0-1.0 (number)\n'
            '- "artifacts": structured deliverables as key-value pairs (object)\n'
            '- "concerns": list of risks/issues (array of strings)\n'
            '- "suggestions": actionable next steps (array of strings)\n'
            '- "dependencies": what this depends on (array of strings)\n\n'
            "Return ONLY valid JSON, no markdown fencing."
        )

        messages = list(self.conversation_history)
        messages.append({"role": "user", "content": structured_prompt})

        logger.info(f"[{self.name}] Invoking Claude sub-agent ({self.model})...")

        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=self.system_prompt,
            messages=messages,
        )

        raw_text = response.content[0].text

        # Record in conversation history for multi-turn debates
        self.conversation_history.append({"role": "user", "content": structured_prompt})
        self.conversation_history.append({"role": "assistant", "content": raw_text})

        return self._parse_response(raw_text, context)

    def challenge(self, proposal: str, context: dict[str, Any]) -> AgentResponse:
        """Challenge another agent's proposal via a Claude API call."""
        challenge_prompt = (
            f"As {self.name} ({self.role.value}), critically evaluate this proposal "
            f"from your colleagues:\n\n{proposal}\n\n"
            "Identify weaknesses, risks, missing considerations, and suggest "
            "improvements. Be constructive but thorough. Consider industrial "
            "standards and best practices in your critique."
        )
        challenge_context = {**context, "_override_prompt": challenge_prompt}
        return self.invoke(challenge_context)

    def refine(self, feedback: list[AgentResponse], context: dict[str, Any]) -> AgentResponse:
        """Refine own proposal based on feedback from other sub-agents."""
        feedback_text = "\n\n".join(
            f"**[{r.agent_role.value}]** (confidence: {r.confidence:.2f}):\n{r.content}"
            for r in feedback
        )
        refine_prompt = (
            f"Your colleagues have provided the following feedback on your work:\n\n"
            f"{feedback_text}\n\n"
            "Refine your proposal to address valid concerns, incorporate good "
            "suggestions, and explain what you changed and why. Maintain industrial "
            "standards compliance."
        )
        refine_context = {**context, "_override_prompt": refine_prompt}
        return self.invoke(refine_context)

    def _parse_response(self, raw_text: str, context: dict[str, Any]) -> AgentResponse:
        """Parse Claude's response into a structured AgentResponse."""
        try:
            # Try to extract JSON from the response
            text = raw_text.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

            data = json.loads(text)
            return AgentResponse(
                agent_id=self.id,
                agent_role=self.role,
                phase=context.get("_phase", "unknown"),
                content=data.get("analysis", raw_text),
                confidence=float(data.get("confidence", 0.75)),
                artifacts=data.get("artifacts", {}),
                concerns=data.get("concerns", []),
                suggestions=data.get("suggestions", []),
                dependencies=data.get("dependencies", []),
                raw_response=raw_text,
            )
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.warning(f"[{self.name}] Failed to parse JSON, using raw text: {e}")
            return AgentResponse(
                agent_id=self.id,
                agent_role=self.role,
                phase=context.get("_phase", "unknown"),
                content=raw_text,
                confidence=0.70,
                raw_response=raw_text,
            )

    def __repr__(self) -> str:
        return f"<SubAgent:{self.name} id={self.id} role={self.role.value} model={self.model}>"
