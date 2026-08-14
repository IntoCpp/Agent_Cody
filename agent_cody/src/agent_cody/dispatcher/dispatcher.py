import json

from .prompt_builder import PromptBuilder
from agent_cody.crew import run_agent

from agent_cody.workflows.coding_workflow import CodingWorkflow

class Dispatcher:
    """
        Routes requests to the selected agent and builds prompts with PromptBuilder.
    """

    def __init__(self):

        self.prompt_builder = PromptBuilder()


    def dispatch(self, agent, task, prompt, history=None, agent_models=None):
        agent_map = {
            "coding": "coding",
            "review": "review",
            "design": "design",
            "documentation": "documentation",
        }

        agent_type = agent_map[agent]
        models = agent_models or {}

        if agent_type == "review":
            review_prompt = self.prompt_builder.build_review_prompt(
                task=task,
                code=prompt,
            )
            review_result = run_agent(
                "review",
                review_prompt,
                model=models["review"],
            )
            return self.format_review_output(review_result)

        if agent_type == "documentation":
            documentation_prompt = self.prompt_builder.build_documentation_prompt(
                task=task,
                content=prompt,
            )
            return run_agent(
                "documentation",
                documentation_prompt,
                model=models["documentation"],
            )

        final_prompt = self.prompt_builder.build(
            agent=agent_type,
            task=task,
            user_prompt=prompt,
            history=history,
        )

        workflow = CodingWorkflow()
        return workflow.run_with_review_loop(
            agent=agent_type,
            task=task,
            prompt=final_prompt,
            coding_model=models["coding"],
            review_model=models["review"],
        )

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
