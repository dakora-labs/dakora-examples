# Dakora Examples

Run a Dakora template and see a trace in minutes. All commands assume the repo root (`dakora-examples`).

## Prereqs (once)

- Python 3.11+ with internet for dependency installs.
- Dakora API key from Settings > API Keys (`DAKORA_API_KEY`).
- Optional: `OPENAI_API_KEY` for tracing/OpenAI, `OPENAI_MODEL` (default `gpt-4o-mini`).
- uv installed is recommended; pip works with `--runner pip`.
- Create `.env` quickly: `python scripts/setup_env.py` (copies `.env.example` and prompts for values).

## Quickstart (uv)

1. `python scripts/setup_env.py`
2. `uv run python scripts/doctor.py`
3. `uv run python scripts/run_example.py template-tracing`

Pip fallback: `python -m pip install ".[quickstart]"` then `python scripts/run_example.py template-tracing --runner pip`.

## Pick an example

- `template-tracing` – renders the template, calls OpenAI, and exports OTLP spans to Dakora (best first run). Path: `quickstart/01_template_with_tracing.py`. Command: `uv run python scripts/run_example.py template-tracing`. Needs `DAKORA_API_KEY` + `OPENAI_API_KEY`.
- `template-render` – renders the template without tracing or OpenAI. Path: `quickstart/00_template_render.py`. Command: `uv run python scripts/run_example.py template-render`. Needs `DAKORA_API_KEY` only.

Both commands accept `--runner uv|pip`; `--runner auto` (default) uses uv when available.

## File map

- `scripts/setup_env.py` – prompts and writes `.env` from `.env.example`.
- `scripts/doctor.py` – checks Python version, command availability, env vars, and imports.
- `scripts/run_example.py` – auto-selects uv/pip, installs extras if needed, and runs an example.
- `shared/templates.py` – built-in template IDs and sample inputs.
- `shared/utils.py` – `.env` loader, env validation, banners, and trace flushing.
- `quickstart/00_template_render.py` – render-only quickstart.
- `quickstart/01_template_with_tracing.py` – tracing + OpenAI quickstart.
- `pyproject.toml` – dependency extras (`quickstart`, `openai`, `otel`, etc.).
- `.env.example` – starter env file (copy or generate via setup_env).

## Template defaults

- Default template ID: `faq_responder` (override with `DAKORA_TEMPLATE_ID`).
- Other built-ins: `research_synthesizer`, `technical_documentation`, `social_media_campaign`.
- Sample inputs live in `shared/templates.py`; update to match your template.

## Troubleshooting

- Run `python scripts/doctor.py` to verify env and imports.
- Missing env vars? Edit `.env` or rerun `python scripts/setup_env.py`.
- Traces appear in Dakora Studio > Executions after `template-tracing` finishes.
