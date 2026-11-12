# Agent_Cody

**Agent Cody** is an experimental, agent-focused AI coding assistant built with CrewAI and Gradio.

It supports single-pass code generation, on-demand code review (including a **Review** shortcut after Code), and documentation utilities for code, proofreading, and translation.

> [!WARNING]
> This project is an exploratory prototype and is no longer under active development.

See [agent_cody/README.md](./agent_cody/README.md) for installation, configuration, architecture, and usage details.

## History

- **2026-11-09** — Documentation task **Professional** for workplace prose revision (`standards/professional.md`); visible only when the Documentation agent is selected.
- **2026-11-06** — Conversation history without duplicating static prompts; single-pass Code generation; **Review** button after successful Code; removed automatic coding review loop (`coding_workflow.py`).
- **2026-08-14** — Added user-selectable models in the Gradio UI: an `available_models` catalog in `models_to_use.yaml`, a Model dropdown with per-agent session memory, a compact model description line, and startup or runtime errors when a default or selected model is missing or unavailable.
- **2026-08-13** — Renamed UI labels to CrewAI terminology (Agent/Task), expanded the prompt area, and rearranged the control bar.
- **2026-08-11** — Added C# task and language-specific coding standards.
- **2026-08-11** — Added standalone code reviews with readable issue formatting.
- **2026-08-11** — Completed documentation generation, professional proofreading, and English/French translation agents.
- **2026-08-11** — Added agent-dependent task choices and automatic prompt clearing after submission.
- **2026-08-11** — Added per-agent model configuration and assigned GPT-5.6 Sol to the Code agent.
