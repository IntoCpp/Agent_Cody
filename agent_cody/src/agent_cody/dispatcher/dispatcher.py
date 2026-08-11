import json

from .prompt_builder import PromptBuilder
from agent_cody.crew import run_agent

from agent_cody.workflows.coding_workflow import CodingWorkflow

class Dispatcher:
    """
        Calls the right agent based on the selected task, uses PromptBuilder to create the prompt.
    """

    def __init__(self):

        self.prompt_builder = PromptBuilder()


    def dispatch(self, task, language, prompt, history = None):
        agent_map = {
            "coding": "coding",
            "review": "review",
            "design": "design",
            "documentation": "documentation",
        }

        agent = agent_map[task] # Task for specialized agent

        if agent == "review":
            review_prompt = self.prompt_builder.build_review_prompt(
                language=language,
                code=prompt,
            )
            review_result = run_agent("review", review_prompt)
            return self.format_review_output(review_result)

        if agent == "documentation":
            documentation_prompt = self.prompt_builder.build_documentation_prompt(
                mode=language,
                content=prompt,
            )
            return run_agent("documentation", documentation_prompt)

        final_prompt = self.prompt_builder.build(
            agent=agent, # string for task: `coding` or `design`, etc.
            language=language,
            user_prompt=prompt,
            history=history,
        )

        # Coding task...
        workflow = CodingWorkflow()
        return workflow.run_with_review_loop(agent=agent, language=language, prompt=final_prompt )

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