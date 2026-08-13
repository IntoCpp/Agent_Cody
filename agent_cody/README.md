# Agent Cody (CrewAI)

Agent Cody is an experimental AI-assisted coding project built with **CrewAI** and **Gradio**.

Its goal is to produce high-quality results for small, focused software-development work while using less context and fewer LLM tokens than full-project IDE assistants.

> [!WARNING]
> This project is an exploratory prototype and is no longer under active development.

## Capabilities

The Gradio interface provides three agents:

* **Code** — Generate Python, C++, or C# code and refine it through an iterative review cycle.
* **Review** — Perform one code-review pass using the selected task's standards and present a readable list of issues and recommendations.
* **Documentation** — Generate language-native code documentation, proofread professional text, or translate between English and French.

Each agent is paired with a **task** that selects the programming language (Python, C++, C#) or, for Documentation only, a text mode (Syntax or Translate).

Submitted text and responses are retained in the chat history. The input box is cleared after each successful submission and shows at least ten lines while typing.

## Background

Agent Cody was the author's second CrewAI project and a learning exercise in multi-agent orchestration, prompt engineering, and iterative AI workflows.

The project demonstrated that narrowly scoped prompts can reduce token consumption, but it also highlighted the infrastructure required for prompt composition, agent dispatching, workflow management, review loops, and state management.

> [!NOTE]
> **Project Status:** On Hold
>
> Future iterations may use a different agent framework and modern MCP-based tooling.

## Architecture

Agent Cody uses three specialized CrewAI agents:

* A coding agent generates code and applies reviewer feedback.
* A review agent checks correctness, security, performance, maintainability, and style.
* A documentation agent generates code documentation, corrects prose, and translates text.

The dispatcher selects one of three execution paths:

* **Code** builds a coding prompt and runs the coding/review workflow for up to three review passes.
* **Review** builds a review prompt and calls the review agent once.
* **Documentation** builds a documentation prompt and calls the documentation agent once.

### Prompt composition

Agent instructions are stored in:

`src/agent_cody/agents/`

Task-specific standards are stored in:

`src/agent_cody/standards/`

The shared `common.md` coding rules apply to Code and Review. Documentation intentionally excludes those rules and combines `documentation.md` with one of:

* `python.md`, `cpp.md`, or `csharp.md` for code documentation
* `syntax.md` for professional proofreading
* `translate.md` for English/French translation

The Gradio task selector adds **Syntax** and **Translate** only while the Documentation agent is selected.

### Model configuration

Each agent can use a different LLM. Configure the assignments in:

`src/agent_cody/config/models_to_use.yaml`

Model names must use CrewAI's `provider/model-id` format. The defaults are:

* Code agent: `openai/gpt-5.6-sol`
* Review agent: `openai/gpt-4o-mini`
* Documentation agent: `openai/gpt-4o-mini`

Set the appropriate provider API key whenever you configure a model from another provider.

## Installation

Agent Cody requires **Python 3.10–3.13** and uses [uv](https://docs.astral.sh/uv/) for dependency and virtual-environment management.

### 1. Install uv

```bash
pip install uv
```

### 2. Clone and enter the project

```bash
git clone <repository-url>
cd agent-cody/agent_cody
```

### 3. Install dependencies

```bash
uv sync
```

This is the only dependency-installation command required for Agent Cody. It reads `pyproject.toml` and `uv.lock`, creates the project virtual environment, and installs the pinned `crewai[tools]` package together with Gradio and the other dependencies.

Do **not** run `crewai install` afterward. CrewAI documents that command for its generated projects, but it is only a thin wrapper around `uv sync`; it does not perform additional CrewAI initialization. This project does not use CrewAI's authenticated Tool Repository or any other installation step that would require the wrapper.

If you already use the CrewAI CLI, you may run `crewai install` **instead of** `uv sync`, but running both is redundant.

### 4. Configure credentials

Add your `OPENAI_API_KEY` to an `.env` file in the `agent_cody` directory. Add other provider keys if you change the configured models.

## Running the Project

From the `agent_cody` directory:

```powershell
uv run python src/agent_cody/ui/gradio_app.py
```

From the repository root on Windows, `start_agent_cody.ps1` opens the browser and starts the application.

## Development Folder

The `agent_cody` directory contains the Python project and its detailed documentation. The repository root has an intentionally minimal README.

The nested `src/agent_cody` structure follows Python package conventions used by CrewAI.
