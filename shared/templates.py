from __future__ import annotations

import os
from textwrap import dedent

FAQ_TEMPLATE_ID = "faq_responder"

BUILT_IN_TEMPLATES = {
    "faq_responder": "Answer FAQ questions with optional sources.",
    "research_synthesizer": "Summarize multiple sources into one cohesive output.",
    "technical_documentation": "Generate technical docs with code examples.",
    "social_media_campaign": "Create multi-platform social posts from a brief.",
}


def faq_inputs() -> dict[str, str | bool]:
    """Default inputs for the starter FAQ responder template."""
    return {
        "question": "How do I reset my password?",
        "knowledge_base": dedent(
            """
            Password resets are available in Settings > Security.
            Users receive a confirmation email and must complete the flow within 15 minutes.
            """
        ).strip(),
        "tone": "helpful and concise",
        "include_sources": True,
    }


def default_template_id() -> str:
    """
    Use an override from env or fall back to the default built-in template.

    Override with DAKORA_TEMPLATE_ID if the built-in template was renamed,
    deleted, or you prefer a custom template.
    """
    return os.getenv("DAKORA_TEMPLATE_ID", FAQ_TEMPLATE_ID)


def template_inputs(template_id: str) -> dict[str, str | bool]:
    """
    Provide example inputs for known templates.

    Returns sample inputs for built-ins we have defaults for. If the template
    is unknown, raise so the caller can explain that custom inputs are needed.
    """
    if template_id == FAQ_TEMPLATE_ID:
        return faq_inputs()
    raise ValueError(
        f"No sample inputs defined for template '{template_id}'. "
        "Set DAKORA_TEMPLATE_ID to a built-in template with known inputs "
        "or update shared/templates.py with your template's inputs."
    )
