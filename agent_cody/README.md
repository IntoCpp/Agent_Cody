# AgentCody Crew

Welcome to the AgentCody Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

This could be a nice read to revise how I did things: https://blog.crewai.com/getting-started-with-crewai-build-your-first-crew/



## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/agent_cody/config/agents.yaml` to define your agents
- Modify `src/agent_cody/config/tasks.yaml` to define your tasks
- Modify `src/agent_cody/crew.py` to add your own logic, tools and specific args
- Modify `src/agent_cody/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the agent-cody Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The agent-cody Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the AgentCody Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.


## Ongoing Dev Notes

### Phase 8 – Add Gradio

Create a minimal interface.

Language

Task

Prompt

Submit

No project context.

No file upload.

No chat history.

Just prove the end-to-end flow.

Commit.

### Phase 9 – Add Conversation History

Maintain the conversation between requests.

This allows follow-up questions.

Commit.

### Phase 10 – Add Project Context

Allow:

Select Folder

or

Upload Files

The dispatcher includes relevant files in the prompt.

Commit.

### Phase 11 – Add Agent Hand-offs

Onwly after everything above orks.

Example:

Coding Agent

↓

"I'd like the Review Agent to verify this."

↓

Review Agent

↓

Return

This is where CrewAI starts providing real value.

Commit.

#### Once stable: Upgrade to structured output for the code-review.

### Phase 12 – Refine

Expand gradually:

More languages
More standards
Framework knowledge
Documentation agent
Design agent
Testing agent
Refactoring agent
Security review agent

Each should be a small, incremental addition.

### Development Philosophy

I recommend following this order:

✓ CrewAI project

↓

✓ Dispatcher

↓

✓ One working agent

↓

✓ Prompt composition

↓

✓ Gradio UI

↓

✓ Conversation memory

↓

✓ Project context

↓

✓ Agent collaboration

↓

✓ Additional agents

The key is to avoid building all the agents upfront. Once you have a single agent working with the dispatcher and prompt composition, every additional capability becomes mostly a matter of writing a new role prompt and plugging it into the existing architecture. That keeps each commit small, testable, and easy to debug.
