<div align="center">

# 🚀 Dakora Examples

Learn how to use Dakora prompt templates and OpenTelemetry tracing with practical examples.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[Getting Started](#-quick-start) • [Examples](#-examples) • [Docs](#-documentation)

</div>

---

## ✨ What's Inside

Standalone examples showing how to:

- Render prompt templates with the Dakora SDK
- Track LLM calls with OpenTelemetry instrumentation
- View execution analytics in Dakora Studio

---

## 🎯 Quick Start

### Prerequisites

- Python 3.11+
- Dakora API key from [Dakora Studio](https://playground.dakora.io/) (Settings → API Keys)
- OpenAI API key (only for `01_template_with_tracing.py`) from [OpenAI Platform](https://platform.openai.com/api-keys)

### Installation

```bash
pip install -e ".[quickstart]"
```

### Setup

Create a `.env` file with your API key:

```bash
cp .env.example .env
```

Edit `.env` and set `DAKORA_API_KEY` (add `OPENAI_API_KEY` if running the tracing example).

### Run Examples

```bash
# Simple template rendering
python quickstart/00_template_render.py

# Template + OpenAI with tracing
python quickstart/01_template_with_tracing.py
```

View execution logs and analytics in [Dakora Studio](https://playground.dakora.io/project/default/executions).

---

## 📚 Examples

### [00_template_render.py](quickstart/00_template_render.py)

Basic template rendering without tracing. Use this when you just need to render prompts.

**Requires:** `DAKORA_API_KEY`

### [01_template_with_tracing.py](quickstart/01_template_with_tracing.py)

Renders a template, calls OpenAI, and sends traces to Dakora Studio. View token usage, costs, and latency in the dashboard.

**Requires:** `DAKORA_API_KEY` + `OPENAI_API_KEY`

---

## 🛠️ Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DAKORA_API_KEY` | Yes | Your Dakora API key |
| `OPENAI_API_KEY` | Only for `01_*` | Your OpenAI API key |
| `DAKORA_TEMPLATE_ID` | No | Template ID (default: `faq_responder`) |
| `OPENAI_MODEL` | No | Model name (default: `gpt-4o-mini`) |

Examples use the `faq_responder` starter template by default. Edit template IDs and inputs directly in the example files to use your own templates.

---

## 📖 Documentation

- [Dakora Overview](https://docs.dakora.io/getting-started/overview) — Learn what Dakora does
- [Quick Start Guide](https://docs.dakora.io/getting-started/quickstart) — 5-minute setup tutorial
- [Templates](https://docs.dakora.io/concepts/templates) — Create and manage prompts
- [Studio](https://playground.dakora.io/) — Test templates and view analytics

---

## 🐛 Troubleshooting

**Missing API keys?**  
Copy `.env.example` to `.env` and add your `DAKORA_API_KEY`. Add `OPENAI_API_KEY` only if running `01_template_with_tracing.py`.

**Import errors?**  
Run `pip install -e ".[quickstart]"` to install dependencies.

**Traces not showing in Studio?**  
Wait 10-30 seconds after the script completes. Check that your API key is valid in [Studio Settings](https://playground.dakora.io/settings).

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes by running the examples
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **Dakora Studio:** [Visit Studio](https://playground.dakora.io)
- **Documentation:** [Read the docs](https://docs.dakora.io)
- **Issues:** [Report an issue](https://github.com/dakora-labs/dakora-examples/issues)

---

<div align="center">

### Built with ❤️ by the Dakora team

[⭐ Star us on GitHub](https://github.com/dakora-labs/dakora-examples) • [📖 Read the docs](https://docs.dakora.io) • [💬 Join our Discord](https://discord.gg/QSRRcFjzE8)

</div>
