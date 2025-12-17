"""
Dakora Quickstart: Template Rendering + OpenTelemetry Tracing
==============================================================

This example shows how to add full observability to your LLM application:
render a Dakora template, call OpenAI, and automatically export traces to
Dakora Studio for analysis.

Perfect for:
- Production LLM applications requiring observability
- Understanding model performance and costs
- Debugging prompt execution and LLM behavior
- Tracking token usage across requests

What it does:
1. Sets up OpenTelemetry instrumentation for OpenAI
2. Renders a Dakora template with sample inputs
3. Calls OpenAI with the rendered prompt (automatically traced)
4. Exports execution traces to Dakora Studio

You'll see in Dakora Studio:
- Model used and configuration
- Token usage (prompt + completion)
- Request/response latency
- Estimated costs
- Full execution timeline

Requirements:
- DAKORA_API_KEY environment variable
- OPENAI_API_KEY environment variable
- Optional: OPENAI_MODEL (defaults to gpt-4o-mini)

Run this example:
    python quickstart/01_template_with_tracing.py

View results:
    Visit Dakora Studio → Executions to see your traced run
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path
from textwrap import dedent

from opentelemetry.instrumentation.openai import OpenAIInstrumentor

# Instrument OpenAI before importing or instantiating any clients
OpenAIInstrumentor().instrument()

from dakora import Dakora
from dakora_instrumentation.generic import setup_instrumentation
from dotenv import load_dotenv
from openai import OpenAI

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
    missing = []
    if not os.getenv("DAKORA_API_KEY"):
        missing.append("DAKORA_API_KEY")
    if not os.getenv("OPENAI_API_KEY"):
        missing.append("OPENAI_API_KEY")
    
    if missing:
        raise RuntimeError(
            f"Missing environment variables: {', '.join(missing)}. "
            "Please set them in your .env file or export them in your shell."
        )

    # Initialize Dakora client
    dakora = Dakora(
        api_key=os.getenv("DAKORA_API_KEY"),
        base_url=os.getenv("DAKORA_BASE_URL"),  # Optional: override API endpoint
    )

    # Set up OpenTelemetry instrumentation
    # This configures the OTLP exporter to send traces to Dakora Studio
    setup_instrumentation(
        dakora_client=dakora,
        service_name="dakora-examples-quickstart",
    )

    print("=" * 60)
    print("Dakora Quickstart: Template Render + Tracing")
    print("=" * 60)
    print(f"\n> Using template `{TEMPLATE_ID}` (override with DAKORA_TEMPLATE_ID)")
    print(f"> Rendering template `{TEMPLATE_ID}`...")
    
    # Render the template with sample inputs
    # This call is automatically traced by Dakora instrumentation
    rendered = await dakora.prompts.render(TEMPLATE_ID, TEMPLATE_INPUTS)
    print(f"> Rendered template v{rendered.version}")

    print("\n> Calling OpenAI with rendered template (traced)...")
    
    # Initialize OpenAI client (already instrumented by OpenAIInstrumentor at module level)
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Call OpenAI - this is automatically traced!
    # The trace will include: model, tokens, latency, cost
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": rendered.text}],
    )
    message = response.choices[0].message.content
    print(message)

    # Ensure all traces are sent to Dakora before exiting
    print("\n> Flushing traces to Dakora...")
    
    # Flush OpenTelemetry spans
    try:
        from opentelemetry import trace
        provider = trace.get_tracer_provider()
        if hasattr(provider, "force_flush"):
            provider.force_flush(timeout_millis=5000)
    except ImportError:
        pass
    
    await dakora.close()
    print("> Done. Check Dakora Studio > Executions to see this trace.")


if __name__ == "__main__":
    asyncio.run(main())
