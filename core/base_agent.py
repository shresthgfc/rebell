"""Base Claude sub-agent class — every agent runs via `claude` CLI."""

from __future__ import annotations

import json
import logging
import subprocess
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

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


def invoke_claude_cli(prompt: str, system_prompt: str, model: str = "sonnet") -> str:
    """Invoke the `claude` CLI as a sub-agent.

    Runs: claude -p "prompt" --model <model> --system-prompt "system_prompt"
    Returns the raw text output from Claude.
    """
    cmd = [
        "claude",
        "-p", prompt,
        "--model", model,
        "--output-format", "text",
    ]

    if system_prompt:
        cmd.extend(["--system-prompt", system_prompt])

    logger.debug(f"Running: claude -p '<prompt>' --model {model}")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=300,  # 5 minute timeout per agent call
    )

    if result.returncode != 0:
        logger.error(f"Claude CLI error: {result.stderr}")
        raise RuntimeError(f"Claude CLI failed (exit {result.returncode}): {result.stderr}")

    return result.stdout.strip()


class BaseAgent(ABC):
    """Abstract base class — each sub-agent invokes `claude` CLI.

    Every agent is a real Claude sub-agent that runs via the `claude`
    command-line tool installed on the user's terminal. No API key
    needed — uses the existing Claude Code authentication.
    """

    def __init__(
        self,
        role: AgentRole,
        name: str,
        expertise: list[str],
        model: str = "sonnet",
    ):
        self.id = str(uuid.uuid4())[:8]
        self.role = role
        self.name = name
        self.expertise = expertise
        self.model = model
        self.conversation_history: list[dict[str, str]] = []

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """The system prompt that defines this sub-agent's persona and behavior."""

    @abstractmethod
    def build_user_prompt(self, context: dict[str, Any]) -> str:
        """Build the user-facing prompt from the current project context."""

    def invoke(self, context: dict[str, Any]) -> AgentResponse:
        """Invoke this Claude sub-agent via `claude` CLI.

        Runs the `claude -p` command with the agent's system prompt
        and parses the structured JSON response.
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

        # Include conversation history in the prompt for multi-turn debates
        if self.conversation_history:
            history_text = "\n\n".join(
                f"[{msg['role'].upper()}]: {msg['content'][:500]}"
                for msg in self.conversation_history[-4:]  # Last 2 exchanges
            )
            structured_prompt = (
                f"Previous conversation context:\n{history_text}\n\n"
                f"---\n\nCurrent task:\n{structured_prompt}"
            )

        logger.info(f"[{self.name}] Invoking via `claude` CLI ({self.model})...")

        raw_text = invoke_claude_cli(
            prompt=structured_prompt,
            system_prompt=self.system_prompt,
            model=self.model,
        )

        # Record in conversation history for multi-turn debates
        self.conversation_history.append({"role": "user", "content": user_prompt})
        self.conversation_history.append({"role": "assistant", "content": raw_text})

        logger.info(f"[{self.name}] Response received ({len(raw_text)} chars)")

        return self._parse_response(raw_text, context)

    def challenge(self, proposal: str, context: dict[str, Any]) -> AgentResponse:
        """Challenge another agent's proposal via `claude` CLI."""
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
            text = raw_text.strip()
            # Strip markdown code fences if present
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
