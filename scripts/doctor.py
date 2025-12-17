from __future__ import annotations

import importlib
import os
import platform
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shared.utils import load_environment  # noqa: E402

ENV_PLACEHOLDERS = {
    "DAKORA_API_KEY": "dk_proj_your_project_key",
    "OPENAI_API_KEY": "sk-your-openai-key",
}


def status(ok: bool) -> str:
    return "OK" if ok else "MISSING"


def check_python() -> bool:
    version = sys.version_info
    ok = (version.major, version.minor) >= (3, 11)
    print(f"Python version: {platform.python_version()} [{status(ok)}]")
    if not ok:
        print("  Upgrade to Python 3.11+ for these examples.")
    return ok


def check_commands() -> None:
    for cmd in ("uv", "pip"):
        found = shutil.which(cmd) is not None
        print(f"Command {cmd}: {status(found)}")


def check_env_vars() -> bool:
    env_path = ROOT / ".env"
    env_hint = env_path if env_path.exists() else ".env.example"
    print(f".env file: {status(env_path.exists())}")
    if not env_path.exists():
        print("  Run `python scripts/setup_env.py` to create it.")

    load_environment()
    all_present = True
    for key, placeholder in ENV_PLACEHOLDERS.items():
        raw = os.getenv(key)
        if raw and raw != placeholder:
            print(f"Env {key}: OK")
            continue

        all_present = False
        if not raw:
            note = "required for tracing/OpenAI" if key.startswith("OPENAI") else "required for all examples"
            print(f"Env {key}: MISSING -> set it in {env_hint} or export it ({note}).")
        else:
            print(f"Env {key}: PLACEHOLDER -> replace the value in {env_hint}.")
    return all_present


def check_imports() -> bool:
    modules = [
        ("dakora", "Install with the core or quickstart extras."),
        ("dakora_instrumentation.generic", "Install with the core or quickstart extras."),
        ("opentelemetry.sdk.trace", "Needed for tracing; comes with the otel/quickstart extras."),
        ("openai", "Needed for tracing example; comes with the openai/quickstart extras."),
    ]
    all_ok = True
    for module, hint in modules:
        try:
            importlib.import_module(module)
            print(f"Import {module}: OK")
        except ImportError:
            all_ok = False
            print(f"Import {module}: MISSING -> {hint}")
    return all_ok


def main() -> int:
    python_ok = check_python()
    check_commands()
    env_ok = check_env_vars()
    check_imports()
    return 0 if python_ok and env_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
