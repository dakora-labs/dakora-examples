"""
Render a Dakora template, call OpenAI, and export traces to Dakora.

Adds OpenTelemetry instrumentation on top of 00_template_render.py so you can
see the execution in Dakora Studio (model, tokens, latency, cost).
"""

from __future__ import annotations

import asyncio
import os

from opentelemetry.instrumentation.openai import OpenAIInstrumentor

# Instrument OpenAI before importing or instantiating any clients.
OpenAIInstrumentor().instrument()

from dakora import Dakora
from dakora_instrumentation.generic import setup_instrumentation
from openai import OpenAI

from shared.templates import default_template_id, template_inputs
from shared.utils import (
    flush_traces,
    load_environment,
    print_banner,
    print_step,
    require_env,
)

load_environment()


async def main() -> None:
    require_env(["DAKORA_API_KEY", "OPENAI_API_KEY"])

    template_id = default_template_id()

    dakora = Dakora(
        api_key=os.getenv("DAKORA_API_KEY"),
        base_url=os.getenv("DAKORA_BASE_URL"),
    )

    setup_instrumentation(
        dakora_client=dakora,
        service_name="dakora-examples-quickstart",
    )

    print_banner("Dakora Quickstart: Template Render + Tracing")

    print_step(f"Using template `{template_id}` (override with DAKORA_TEMPLATE_ID).")
    print_step(f"Rendering template `{template_id}`...")
    rendered = await dakora.prompts.render(template_id, template_inputs(template_id))
    print_step(f"Rendered template v{rendered.version}")

    print_step("Calling OpenAI with rendered template (traced)...")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": rendered.text}],
    )
    message = response.choices[0].message.content
    print(message)

    print_step("Flushing traces to Dakora...")
    flush_traces()
    await dakora.close()
    print_step("Done. Check Dakora Studio > Executions to see this trace.")


if __name__ == "__main__":
    asyncio.run(main())
