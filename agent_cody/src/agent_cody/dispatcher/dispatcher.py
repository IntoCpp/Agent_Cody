import json
from typing import Any

from .prompt_builder import PromptBuilder
from agent_cody.crew import run_agent


def _session_visited_set(session_state: dict[str, Any] | None) -> set[tuple[str, str]]:
    raw = (session_state or {}).get("visited") or []
    return {tuple(x) for x in raw if len(x) == 2}


def _session_mark_visited(session_state: dict[str, Any] | None, agent_type: str, task: str) -> None:
    if session_state is None:
        return
    key = [agent_type, task.lower()]
    visited = session_state.setdefault("visited", [])
    if key not in visited:
        visited.append(key)


def _should_include_static(session_state: dict[str, Any] | None, agent_type: str, task: str) -> bool:
    return (agent_type, task.lower()) not in _session_visited_set(session_state)


class Dispatcher:
    """Routes requests and builds prompts with PromptBuilder (static block once per agent+task per session)."""

    def __init__(self):
        self.prompt_builder = PromptBuilder()

    def dispatch(
        self,
        agent: str,
        task: str,
        prompt: str,
        history: list | None = None,
        agent_models: dict[str, str] | None = None,
        session_state: dict[str, Any] | None = None,
    ) -> str:
        agent_map = {
            "coding": "coding",
            "review": "review",
            "design": "design",
            "documentation": "documentation",
        }

        agent_type = agent_map[agent]
        models = agent_models or {}
        hist = history or []

        if agent_type == "review":
            include_static = _should_include_static(session_state, "review", task)
            review_prompt = self.prompt_builder.build_review_prompt(
                task=task,
                code=prompt,
                history=hist,
                include_static=include_static,
                focus_notes=None,
            )
            review_result = run_agent(
                "review",
                review_prompt,
                model=models["review"],
            )
            _session_mark_visited(session_state, "review", task)
            return self.format_review_output(review_result)

        if agent_type == "documentation":
            include_static = _should_include_static(session_state, "documentation", task)
            documentation_prompt = self.prompt_builder.build_documentation_prompt(
                task=task,
                content=prompt,
                history=hist,
                include_static=include_static,
            )
            result = run_agent(
                "documentation",
                documentation_prompt,
                model=models["documentation"],
            )
            _session_mark_visited(session_state, "documentation", task)
            return result

        include_static = _should_include_static(session_state, "coding", task)
        coding_prompt = self.prompt_builder.build_coding_prompt(
            task=task,
            user_prompt=prompt,
            history=hist,
            include_static=include_static,
        )
        result = run_agent(
            "coding",
            coding_prompt,
            model=models["coding"],
        )
        _session_mark_visited(session_state, "coding", task)
        return result

    def dispatch_review_shortcut(
        self,
        task: str,
        code: str,
        focus_notes: str,
        history: list | None = None,
        agent_models: dict[str, str] | None = None,
        session_state: dict[str, Any] | None = None,
    ) -> str:
        """Review the latest code; optional focus text from the prompt box."""
        models = agent_models or {}
        hist = history or []
        include_static = _should_include_static(session_state, "review", task)
        notes = focus_notes.strip() or None
        review_prompt = self.prompt_builder.build_review_prompt(
            task=task,
            code=code,
            history=hist,
            include_static=include_static,
            focus_notes=notes,
        )
        review_result = run_agent(
            "review",
            review_prompt,
            model=models["review"],
        )
        _session_mark_visited(session_state, "review", task)
        return self.format_review_output(review_result)

    @staticmethod
    def format_review_output(review_text: str) -> str:
        """Convert a structured review response into a readable issue list."""
        try:
            review = json.loads(review_text)
        except json.JSONDecodeError:
            return review_text

        issues = review.get("issues", [])
        if review.get("approved", False) and not issues:
            return "Code approved. No issues found."

        if not issues:
            return "Review completed. No issues were provided."

        formatted_issues = []
        for index, issue in enumerate(issues, start=1):
            severity = issue.get("severity", "unspecified")
            category = issue.get("category", "unspecified")
            description = issue.get("description", "No description provided.")
            recommendation = issue.get("recommendation", "No recommendation provided.")

            formatted_issues.append(
                f"{index}. ({severity} / {category}) {description}\n"
                f"   recommendation: {recommendation}"
            )

        return "\n\n".join(formatted_issues)
