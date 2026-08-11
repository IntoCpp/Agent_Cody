from pathlib import Path

from crewai import Agent, Task, Crew, Process
import yaml


MODELS_CONFIG_PATH = Path(__file__).parent / "config" / "models_to_use.yaml"


def load_models_config() -> dict[str, str]:
    """Load and validate the model assigned to each supported task."""
    with MODELS_CONFIG_PATH.open(encoding="utf-8") as config_file:
        models = yaml.safe_load(config_file)

    if not isinstance(models, dict):
        raise ValueError(f"Invalid model configuration: {MODELS_CONFIG_PATH}")

    required_tasks = {"code", "review", "documentation"}
    missing_tasks = required_tasks - models.keys()
    if missing_tasks:
        missing_list = ", ".join(sorted(missing_tasks))
        raise ValueError(f"Missing model configuration for: {missing_list}")

    for task in required_tasks:
        model = models[task]
        if not isinstance(model, str) or not model.strip():
            raise ValueError(f"Model for '{task}' must be a non-empty string.")

    return models


MODELS_TO_USE = load_models_config()

coding_agent = Agent(
    role="Senior Software Engineer",
    goal="Write correct, clean, maintainable code based on instructions",
    backstory="You are an expert software engineer.",
    llm=MODELS_TO_USE["code"],
    verbose=True,
)

review_agent = Agent(
    role="Senior Code Reviewer",
    goal="Find bugs, inefficiencies, and design issues in code",
    backstory="You are extremely strict about correctness and maintainability.",
    llm=MODELS_TO_USE["review"],
    verbose=True,
)

documentation_agent = Agent(
    role="Senior Technical Documentation Specialist",
    goal="Produce accurate, concise, professional technical documentation and prose",
    backstory="You are an expert technical writer with extensive software development experience.",
    llm=MODELS_TO_USE["documentation"],
    verbose=True,
)

def run_agent(agent_type: str, prompt: str) -> str:

    if agent_type == "coding":
        agent = coding_agent
        task = Task( description=prompt, expected_output="High quality code", agent=agent )
    elif agent_type == "review":
        agent = review_agent
        task = Task( description=prompt, expected_output="Structured list of review comments", agent=agent )
    elif agent_type == "documentation":
        agent = documentation_agent
        task = Task(
            description=prompt,
            expected_output="Professional documentation or revised prose",
            agent=agent,
        )
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")


    crew = Crew(
        agents=[agent],  # TODO: Generalize for other tasks (review, design, etc.)  later.
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    return result.raw