from .prompt_builder import PromptBuilder
from agent_cody.crew import run_agent

# from crew import run_coding_task, run_review_task
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

        final_prompt = self.prompt_builder.build(
            agent=agent, # string for task: `coding` or `design`, etc.
            language=language,
            user_prompt=prompt,
            history=history,
        )

        workflow = CodingWorkflow()
        return workflow.run_with_review_loop(agent=agent, prompt=final_prompt )
        # return run_agent(final_prompt)
        # return final_prompt