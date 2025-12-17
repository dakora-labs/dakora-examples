"""
Render a Dakora template without enabling OpenTelemetry tracing.

What it does:
- Loads your Dakora API key from .env
- Renders the default `faq_responder` template with sample inputs
- Prints the rendered text so you can copy/paste it elsewhere
"""

from __future__ import annotations

import asyncio
import os

from dakora import Dakora

from shared.templates import default_template_id, template_inputs
from shared.utils import load_environment, print_banner, print_step, require_env

load_environment()


async def main() -> None:
    require_env(["DAKORA_API_KEY"])

    template_id = default_template_id()

    dakora = Dakora(
        api_key=os.getenv("DAKORA_API_KEY"),
        base_url=os.getenv("DAKORA_BASE_URL"),
    )

    print_banner("Dakora Quickstart: Template Render (no OTLP)")
    print_step(f"Using template `{template_id}` (override with DAKORA_TEMPLATE_ID).")
    print_step(f"Rendering template `{template_id}` without tracing...")

    rendered = await dakora.prompts.render(template_id, template_inputs(template_id))

    print_step("Rendered content preview")
    preview = rendered.text
    if len(preview) > 800:
        preview = preview[:800] + "\n...[truncated]..."
    print(preview)

    print_step(f"Template version: v{rendered.version}")
    await dakora.close()


if __name__ == "__main__":
    asyncio.run(main())
