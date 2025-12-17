from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - dotenv is an optional install time dep
    load_dotenv = None

ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT_DIR / ".env"


def load_environment() -> None:
    """Load environment variables from .env if python-dotenv is available."""
    if load_dotenv is None:
        return
    if ENV_FILE.exists():
        load_dotenv(ENV_FILE)
    else:
        load_dotenv()


def require_env(keys: Iterable[str]) -> None:
    """Exit early when required environment variables are missing."""
    missing = [key for key in keys if not os.getenv(key)]
    if missing:
        env_hint = ENV_FILE if ENV_FILE.exists() else ".env.example"
        raise RuntimeError(
            f"Missing environment variables: {', '.join(missing)}. "
            f"Update {env_hint} or export them in your shell. "
            "Run `python scripts/setup_env.py` if you need to regenerate .env quickly."
        )


def print_banner(title: str) -> None:
    print("=" * 60)
    print(title)
    print("=" * 60)


def print_step(text: str) -> None:
    print(f"\n> {text}")


def flush_traces(timeout_millis: int = 5000) -> None:
    """Flush OpenTelemetry spans when tracing is enabled."""
    try:
        from opentelemetry import trace
    except ImportError:
        return

    provider = trace.get_tracer_provider()
    flush = getattr(provider, "force_flush", None)
    if callable(flush):
        flush(timeout_millis=timeout_millis)
