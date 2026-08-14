from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from crewai import Agent, Crew, Process, Task
import yaml

from agent_cody.model_errors import ModelNotAvailableError, is_invalid_model_error


MODELS_CONFIG_PATH = Path(__file__).parent / "config" / "models_to_use.yaml"
AGENT_DEFAULT_KEYS = ("code", "review", "documentation")


@dataclass(frozen=True)
class ModelsConfig:
    defaults: dict[str, str]
    available_models: dict[str, str]


def load_models_config() -> ModelsConfig:
    """Load default agent models and the user-selectable model catalog."""
    with MODELS_CONFIG_PATH.open(encoding="utf-8") as config_file:
        raw_config = yaml.safe_load(config_file)

    if not isinstance(raw_config, dict):
        raise ValueError(f"Invalid model configuration: {MODELS_CONFIG_PATH}")

    defaults: dict[str, str] = {}
    for agent_key in AGENT_DEFAULT_KEYS:
        model = raw_config.get(agent_key)
        if not isinstance(model, str) or not model.strip():
            raise ValueError(f"Model for '{agent_key}' must be a non-empty string.")
        defaults[agent_key] = model.strip()

    available_models = raw_config.get("available_models", {})
    if not isinstance(available_models, dict):
        raise ValueError("'available_models' must be a mapping of model IDs to descriptions.")

    cleaned_available_models: dict[str, str] = {}
    for model_id, description in available_models.items():
        if not isinstance(model_id, str) or not model_id.strip():
            raise ValueError("Each available model ID must be a non-empty string.")
        if not isinstance(description, str) or not description.strip():
            raise ValueError(f"Description for '{model_id}' must be a non-empty string.")
        cleaned_available_models[model_id.strip()] = description.strip()

    return ModelsConfig(
        defaults=defaults,
        available_models=cleaned_available_models,
    )


def get_model_choices(config: ModelsConfig) -> list[str]:
    """Return selectable models, always including defaults even if missing from the catalog."""
    choices = list(config.available_models.keys())
    for model in config.defaults.values():
        if model not in choices:
            choices.append(model)
    return choices


def get_default_config_warnings(config: ModelsConfig) -> list[str]:
    """Return startup warnings when a default model is missing from available_models."""
    warnings: list[str] = []
    for agent_key, model in config.defaults.items():
        if model not in config.available_models:
            warnings.append(
                f"Default model for '{agent_key}' ({model}) is missing from available_models."
            )
    return warnings


def format_model_description(model_id: str, config: ModelsConfig) -> str:
    description = config.available_models.get(model_id)
    if description:
        return f"{model_id}: {description}"
    return model_id


MODELS_CONFIG = load_models_config()


def _build_agent(agent_type: str, model: str) -> Agent:
    if agent_type == "coding":
        return Agent(
            role="Senior Software Engineer",
            goal="Write correct, clean, maintainable code based on instructions",
            backstory="You are an expert software engineer.",
            llm=model,
            verbose=True,
        )
    if agent_type == "review":
        return Agent(
            role="Senior Code Reviewer",
            goal="Find bugs, inefficiencies, and design issues in code",
            backstory="You are extremely strict about correctness and maintainability.",
            llm=model,
            verbose=True,
        )
    if agent_type == "documentation":
        return Agent(
            role="Senior Technical Documentation Specialist",
            goal="Produce accurate, concise, professional technical documentation and prose",
            backstory=(
                "You are an expert technical writer with extensive software development experience."
            ),
            llm=model,
            verbose=True,
        )
    raise ValueError(f"Unknown agent type: {agent_type}")


def _build_task(agent_type: str, prompt: str, agent: Agent) -> Task:
    if agent_type == "coding":
        return Task(
            description=prompt,
            expected_output="High quality code",
            agent=agent,
        )
    if agent_type == "review":
        return Task(
            description=prompt,
            expected_output="Structured list of review comments",
            agent=agent,
        )
    if agent_type == "documentation":
        return Task(
            description=prompt,
            expected_output="Professional documentation or revised prose",
            agent=agent,
        )
    raise ValueError(f"Unknown agent type: {agent_type}")


def run_agent(agent_type: str, prompt: str, model: str) -> str:
    agent = _build_agent(agent_type, model)
    task = _build_task(agent_type, prompt, agent)

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    try:
        result = crew.kickoff()
    except Exception as exc:
        if is_invalid_model_error(exc):
            raise ModelNotAvailableError(model, exc) from exc
        raise

    return result.raw
