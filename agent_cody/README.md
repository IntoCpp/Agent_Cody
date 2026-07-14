# Agent Cody (CrewAI)

Welcome to **Agent Cody**, an experimental AI-assisted coding project built with **CrewAI**.

The primary goal of this project was to explore whether a lightweight multi-agent workflow could produce high-quality code while significantly reducing LLM token usage compared to IDE-integrated AI assistants.

The application provides a simple **Gradio** interface where the user selects:

* A task (Code, Documentation, Code Review, etc.)
* A programming language (Python, C++, or C#)
* A prompt describing the work to perform

The request is processed by a specialized coding agent, followed by an iterative code-review loop intended to improve the quality of the generated output.

Unlike general-purpose AI coding assistants that often require an entire project as context, Agent Cody focuses on generating **small, self-contained units of work** (typically individual functions or focused implementations), allowing substantially lower token consumption.

> [!WARNING]
> This project is an exploratory prototype and is no longer under active development.

---

## Background

Agent Cody was my second project using **CrewAI** and served primarily as a learning exercise to better understand multi-agent orchestration, prompt engineering, and iterative AI workflows.

Although the project achieved its original objectives, it also highlighted several architectural limitations that influenced my future AI projects.

> [!NOTE]
> **Project Status:** On Hold
>
> After experimenting with several workflow designs, I concluded that CrewAI introduces more architectural complexity than desired for this particular use case. Future iterations will likely be implemented using a different agent framework together with modern tooling and MCP integration.

---

## Project Goals

The objective was to build a **minimalist AI coding assistant** focused on minimizing token consumption while maintaining high-quality output.

Modern AI coding assistants frequently transmit large portions of a project as context, resulting in significant token usage even for relatively small programming tasks.

Agent Cody instead relies on concise, task-specific prompts combined with carefully designed coding guidelines. Rather than generating large codebases, the workflow focuses on producing one well-designed component at a time, making it both efficient and predictable.

---

## Architecture

CrewAI appeared to be an excellent fit for building a workflow composed of specialized agents such as: Coding, Code Review, Documentation and Testing (planned).

Each programming language has its own coding standards and best practices, while each task type contributes additional prompt instructions. These prompt components are dynamically combined before being sent to the LLM.

A lightweight **Gradio** interface allows users to:

* Select the desired task
* Select the target programming language
* Submit a focused request

Generated code is then evaluated by a reviewer agent through an iterative review loop intended to improve correctness, maintainability, and overall code quality.

The long-term vision was to expand the system with additional specialized agents for software design, automated testing, and documentation generation while keeping each interaction narrowly scoped.

---

## Lessons Learned

One of the most valuable outcomes of this project was understanding the practical complexity involved in orchestrating multiple AI agents.

While introductory CrewAI examples present agent definitions as relatively straightforward, building a maintainable application required significantly more infrastructure, including:

* Prompt composition
* Task dispatching
* Workflow management
* Review loops
* State management

As the project evolved, the supporting architecture became increasingly complex for what was intended to remain a lightweight coding assistant.

Rather than continuing to extend the system, I chose to treat this repository as a successful exploration and apply the lessons learned to future AI projects built on frameworks that better align with my architectural goals.

## Installation

This project requires **Python 3.10 – 3.13** and uses **[uv](https://docs.astral.sh/uv/)** for dependency and virtual environment management.

### 1. Install `uv`

If you do not already have `uv` installed:

```bash
pip install uv
```

### 2. Clone the repository

```bash
git clone <repository-url>
cd agent-cody
```

### 3. Create the virtual environment and install dependencies

Install all project dependencies defined in `pyproject.toml`:

```bash
uv sync
```

This command will:

* Create a virtual environment (if one does not already exist)
* Install all project dependencies
* Generate or update `uv.lock` if necessary

### 4. CrewAI project initialization

If the installed version of **CrewAI** requires additional project setup, run:

```bash
crewai install
```

This command installs any CrewAI-specific resources required by the project. Depending on the CrewAI version you are using, this step may already be handled by `uv sync`.

> [!NOTE]
> `uv` is responsible for Python package management, while `crewai install` performs CrewAI-specific project initialization. They serve different purposes and are not interchangeable.


## Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

## Running the Project

To run the project in Gradio, use this commend: `uv run python src/agent_cody/ui/gradio_app.py`

Example: 

```bash
 PS <project-root>\agent_cody> uv run python src/agent_cody/ui/gradio_app.py
```

## VS-Code note
>
> I usually work by opening the folder `<project root>\agent_cody\` in VSCode. This is where my project main README is located.
> 
> Note that the main project folder `<project root>` is considered the "main" project. It have it's own minimalist README.md.
>
> This is the CrewAI way... the dev in project folder/sub/sub-folder is the way to go to create Python packages. Something I do not need here.

