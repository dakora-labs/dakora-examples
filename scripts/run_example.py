from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shared.utils import load_environment, require_env  # noqa: E402

EXAMPLES = {
    "template-render": {
        "path": ROOT / "quickstart" / "00_template_render.py",
        "extra": "quickstart",
        "env": ["DAKORA_API_KEY"],
        "description": "Render the default faq_responder template (no tracing).",
    },
    "template-tracing": {
        "path": ROOT / "quickstart" / "01_template_with_tracing.py",
        "extra": "quickstart",
        "env": ["DAKORA_API_KEY", "OPENAI_API_KEY"],
        "description": "Render template, call OpenAI, export traces to Dakora.",
    },
}


def run(cmd: list[str]) -> int:
    print(f"\n$ {' '.join(cmd)}")
    return subprocess.call(cmd)


def run_with_uv(example: dict[str, object]) -> int:
    cmd = [
        "uv",
        "run",
        "--extra",
        str(example["extra"]),
        "python",
        str(example["path"]),
    ]
    return run(cmd)


def run_with_pip(example: dict[str, object]) -> int:
    install_cmd = [
        sys.executable,
        "-m",
        "pip",
        "install",
        f".[{example['extra']}]",
    ]
    code = run(install_cmd)
    if code != 0:
        return code
    return run([sys.executable, str(example["path"])])


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run Dakora examples with uv (preferred) or pip fallback."
    )
    parser.add_argument(
        "example",
        choices=EXAMPLES.keys(),
        help="Example to run.",
    )
    parser.add_argument(
        "--runner",
        choices=("auto", "uv", "pip"),
        default="auto",
        help="Preferred runner. Default: auto-detect uv, fallback to pip.",
    )
    args = parser.parse_args()

    example = EXAMPLES[args.example]
    load_environment()
    try:
        require_env(example["env"])
    except RuntimeError as exc:
        print(f"Environment check failed: {exc}")
        return 1

    runner = args.runner
    if runner == "auto":
        runner = "uv" if shutil.which("uv") else "pip"

    print(f"Selected example: {args.example} — {example['description']}")
    if runner == "uv":
        if not shutil.which("uv"):
            print("uv not found. Falling back to pip.")
            runner = "pip"
        else:
            return run_with_uv(example)

    if runner == "pip":
        print("Using pip fallback. Installing extras before running...")
        return run_with_pip(example)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
