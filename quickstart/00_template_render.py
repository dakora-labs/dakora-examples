"""
Dakora Quickstart: Template Rendering (No Tracing)
===================================================

This example demonstrates the simplest way to use Dakora templates:
render a prompt template with dynamic inputs and get the result as text.

Perfect for:
- Testing template outputs before adding tracing
- Lightweight prompt management without observability overhead
- Scenarios where you don't need execution tracking

What it does:
1. Loads your Dakora API key from .env
2. Renders the default `faq_responder` template with sample inputs
3. Prints the rendered text so you can use it in your application

Requirements:
- DAKORA_API_KEY environment variable

Run this example:
    python quickstart/00_template_render.py
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path
from textwrap import dedent

from dakora import Dakora
from dotenv import load_dotenv

# Load environment variables from .env file
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
else:
    load_dotenv()

# Template configuration
TEMPLATE_ID = os.getenv("DAKORA_TEMPLATE_ID", "faq_responder")

# Sample inputs for the FAQ responder template
TEMPLATE_INPUTS = {
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


async def main() -> None:
    # Check for required environment variables
    if not os.getenv("DAKORA_API_KEY"):
        raise RuntimeError(
            "Missing DAKORA_API_KEY environment variable. "
            "Please set it in your .env file or export it in your shell."
        )

    # Initialize Dakora client
    dakora = Dakora(
        api_key=os.getenv("DAKORA_API_KEY"),
        base_url=os.getenv("DAKORA_BASE_URL"),  # Optional: override API endpoint
    )

    print("=" * 60)
    print("Dakora Quickstart: Template Render (no OTLP)")
    print("=" * 60)
    print(f"\n> Using template `{TEMPLATE_ID}` (override with DAKORA_TEMPLATE_ID)")
    print(f"> Rendering template `{TEMPLATE_ID}` without tracing...")

    # Render the template with sample inputs
    rendered = await dakora.prompts.render(TEMPLATE_ID, TEMPLATE_INPUTS)

    print("\n> Rendered content preview:")
    preview = rendered.text
    if len(preview) > 800:
        preview = preview[:800] + "\n...[truncated]..."
    print(preview)

    print(f"\n> Template version: v{rendered.version}")
    await dakora.close()


if __name__ == "__main__":
    asyncio.run(main())
