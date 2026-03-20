"""Configuration settings for the multi-agent dev org pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PipelineConfig:
    """Configuration for running the pipeline."""

    # Model configuration
    model: str = "claude-sonnet-4-6"
    synthesizer_model: str = "claude-sonnet-4-6"
    max_tokens: int = 4096

    # Pipeline preset: "full", "standard", "lean"
    preset: str = "full"

    # Debate configuration
    max_debate_rounds: int = 3
    consensus_threshold: float = 0.75

    # Project configuration
    budget_tier: str = "standard"  # "startup", "standard", "enterprise"
    timeline: str = "standard"  # "urgent", "standard", "relaxed"

    # Logging
    log_level: str = "INFO"
    log_to_file: bool = True
    log_file: str = "pipeline_output.log"

    # Output
    output_dir: str = "./output"
    save_intermediate: bool = True

    @classmethod
    def enterprise(cls) -> PipelineConfig:
        """Enterprise preset: thorough, all agents, max debate."""
        return cls(
            model="claude-sonnet-4-6",
            preset="full",
            max_debate_rounds=3,
            consensus_threshold=0.80,
            budget_tier="enterprise",
        )

    @classmethod
    def startup(cls) -> PipelineConfig:
        """Startup preset: lean, fast, essential agents only."""
        return cls(
            model="claude-sonnet-4-6",
            preset="lean",
            max_debate_rounds=1,
            consensus_threshold=0.65,
            budget_tier="startup",
            timeline="urgent",
        )

    @classmethod
    def standard(cls) -> PipelineConfig:
        """Standard preset: balanced coverage and speed."""
        return cls(
            model="claude-sonnet-4-6",
            preset="standard",
            max_debate_rounds=2,
            consensus_threshold=0.75,
        )
