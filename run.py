#!/usr/bin/env python3
"""Main entry point — run the multi-agent dev org pipeline.

Usage:
    python run.py --requirements "Build a SaaS project management tool"
    python run.py --requirements-file requirements.txt --preset full
    python run.py --requirements "Build an API" --preset lean --model claude-haiku-4-5-20251001
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path

from config.settings import PipelineConfig
from pipeline.factory import PipelineFactory

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("rebell")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="REBELL — Multi-Agent Development Organization Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full enterprise pipeline
  python run.py --requirements "Build a real-time collaboration platform" --preset full

  # Standard balanced pipeline
  python run.py --requirements "Create an e-commerce API" --preset standard

  # Lean startup pipeline
  python run.py --requirements "MVP for task tracker" --preset lean

  # Load requirements from file
  python run.py --requirements-file requirements.txt --preset full

  # Custom model and debate settings
  python run.py --requirements "Build a CRM" --model claude-sonnet-4-6 --debate-rounds 2
        """,
    )

    parser.add_argument(
        "--requirements", "-r",
        type=str,
        help="Client requirements as a string",
    )
    parser.add_argument(
        "--requirements-file", "-f",
        type=str,
        help="Path to a file containing client requirements",
    )
    parser.add_argument(
        "--project-name", "-n",
        type=str,
        default="Untitled Project",
        help="Name of the project",
    )
    parser.add_argument(
        "--preset", "-p",
        choices=["full", "standard", "lean"],
        default="full",
        help="Pipeline preset (default: full)",
    )
    parser.add_argument(
        "--model", "-m",
        type=str,
        default="claude-sonnet-4-6",
        help="Claude model to use (default: claude-sonnet-4-6)",
    )
    parser.add_argument(
        "--debate-rounds",
        type=int,
        default=None,
        help="Max debate rounds per phase (default: depends on preset)",
    )
    parser.add_argument(
        "--consensus-threshold",
        type=float,
        default=0.75,
        help="Consensus threshold for debates (default: 0.75)",
    )
    parser.add_argument(
        "--budget",
        choices=["startup", "standard", "enterprise"],
        default="standard",
        help="Budget tier (default: standard)",
    )
    parser.add_argument(
        "--timeline",
        choices=["urgent", "standard", "relaxed"],
        default="standard",
        help="Timeline (default: standard)",
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        default="./output",
        help="Output directory for results",
    )

    args = parser.parse_args()

    # Get requirements
    if args.requirements:
        requirements = args.requirements
    elif args.requirements_file:
        requirements = Path(args.requirements_file).read_text()
    else:
        parser.error("Either --requirements or --requirements-file is required")

    # Create pipeline
    pipeline = PipelineFactory.create(
        preset=args.preset,
        model=args.model,
        max_debate_rounds=args.debate_rounds,
        consensus_threshold=args.consensus_threshold,
    )

    # Run pipeline
    context = pipeline.run(
        client_requirements=requirements,
        project_name=args.project_name,
        budget_tier=args.budget,
        timeline=args.timeline,
    )

    # Save output
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save full context
    output_file = output_dir / "project_output.json"
    with open(output_file, "w") as f:
        json.dump(context.to_dict(), f, indent=2, default=str)

    logger.info(f"Output saved to: {output_file}")

    # Save phase summaries
    for phase_name, result in context.phase_results.items():
        safe_name = phase_name.lower().replace(" ", "_").replace(":", "")
        summary_file = output_dir / f"{safe_name}_summary.md"
        with open(summary_file, "w") as f:
            f.write(result.summary)
        logger.info(f"Phase summary saved: {summary_file}")

    # Save final synthesis
    if context.review_report.get("final_synthesis"):
        synthesis_file = output_dir / "final_synthesis.md"
        with open(synthesis_file, "w") as f:
            f.write(context.review_report["final_synthesis"])
        logger.info(f"Final synthesis saved: {synthesis_file}")

    print(f"\n{'='*60}")
    print(f"  Pipeline complete!")
    print(f"  Output: {output_dir}")
    print(f"  Phases: {len(context.phase_results)}")
    print(f"  Risks identified: {len(context.risks)}")
    print(f"  Decisions made: {len(context.decisions)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
