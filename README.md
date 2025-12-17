# Dakora Examples

See a Dakora trace in a few minutes. Start with the quickstart track, then branch into providers/agents/production as they fill in.

## Zero to trace (3 commands)

1. `python scripts/setup_env.py` (creates `.env` and prompts for your keys)
2. `uv run python scripts/doctor.py` (or `python scripts/doctor.py` if you do not use uv)
3. `uv run python scripts/run_example.py template-tracing`

No `uv`? Use `python -m pip install ".[quickstart]"` then `python scripts/run_example.py template-tracing`.

## Pick an example

- `template-tracing` — renders the default template, calls OpenAI, and exports OTLP traces to Dakora (best first run).
- `template-render` — renders the template without tracing or OpenAI (works offline, good for key checks).

Both commands accept `--runner uv|pip` if you want to force a runner. Defaults auto-detect `uv`.

## Prereqs

- Python 3.11+ and internet access for dependency install.
- A Dakora API key from **Settings > API Keys** in your project (`DAKORA_API_KEY`).
- Optional: `DAKORA_BASE_URL` if you self-host; `OPENAI_API_KEY` for tracing/OpenAI example.

## Template defaults

- Default template ID: `faq_responder` (ships with every project). Override via `DAKORA_TEMPLATE_ID`.
- Other built-ins: `research_synthesizer`, `technical_documentation`, `social_media_campaign`.
- Sample inputs live in `shared/templates.py`. Update there if you target your own template.

## Handy scripts

- `scripts/setup_env.py` — generates `.env` from `.env.example` with prompts.
- `scripts/doctor.py` — checks Python version, required env vars, and imports.
- `scripts/run_example.py` — runs examples with uv (preferred) or pip fallback; ensures env is loaded.

## Layout

- `quickstart/` — ready-to-run quickstart files.
- `providers/`, `maf_agents/`, `workflows/`, `production/` — upcoming tracks (placeholders for now).
- `shared/` — helpers reused across examples.
- `pyproject.toml` — extras for quickstart/otel/providers.
- `.env.example` — minimal keys; copy to `.env` before running anything.
