# Agent_Cody

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

For details on this project, see the [agent_cody/readme.md](./agent_cody/README.md) ; CrewAI ask to work in sub folders to facilitate the creation of packages.
