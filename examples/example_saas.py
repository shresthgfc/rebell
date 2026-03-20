#!/usr/bin/env python3
"""Example: Run the full pipeline for a SaaS project management tool.

This example demonstrates how to use the pipeline programmatically
instead of via the CLI.
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline.factory import PipelineFactory

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)


def main() -> None:
    # Define client requirements
    requirements = """
    We need a modern SaaS project management platform with the following needs:

    1. CORE FEATURES:
       - Task management with drag-and-drop Kanban boards
       - Real-time collaboration (multiple users editing simultaneously)
       - Time tracking and reporting
       - File attachments and document sharing
       - Team chat integrated into project context

    2. USER MANAGEMENT:
       - Multi-tenant architecture (each company is isolated)
       - Role-based access control (Admin, Manager, Member, Guest)
       - SSO integration (Google, Microsoft, Okta)
       - Team invitations and onboarding flow

    3. INTEGRATIONS:
       - REST API for third-party integrations
       - Webhooks for event notifications
       - Slack and Microsoft Teams integration
       - GitHub/GitLab integration for dev teams
       - Zapier/Make connectivity

    4. ANALYTICS:
       - Project health dashboards
       - Team velocity and burndown charts
       - Custom report builder
       - Export to PDF/CSV

    5. CONSTRAINTS:
       - Must handle 10,000+ concurrent users
       - 99.9% uptime SLA
       - GDPR and SOC2 compliance required
       - Mobile-responsive (PWA)
       - Sub-200ms API response time (p95)
    """

    # Create and run the full pipeline
    pipeline = PipelineFactory.create(
        preset="full",
        model="sonnet",
        max_debate_rounds=2,
        consensus_threshold=0.75,
    )

    context = pipeline.run(
        client_requirements=requirements,
        project_name="ProjectFlow SaaS",
        budget_tier="enterprise",
        timeline="standard",
    )

    # Output results
    output_dir = Path("output/example_saas")
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / "full_output.json", "w") as f:
        json.dump(context.to_dict(), f, indent=2, default=str)

    print(f"\nResults saved to: {output_dir}")
    print(f"Phases completed: {list(context.phase_results.keys())}")
    print(f"Risks identified: {len(context.risks)}")
    print(f"Decisions made: {len(context.decisions)}")


if __name__ == "__main__":
    main()
