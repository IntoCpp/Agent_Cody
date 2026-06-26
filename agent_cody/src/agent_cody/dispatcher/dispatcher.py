from .prompt_builder import PromptBuilder


class Dispatcher:
    """
        Calls the right agent based on the selected task, uses PromptBuilder to create the prompt.
    """

    def __init__(self):

        self.prompt_builder = PromptBuilder()

    def dispatch(
        self,
        task,
        language,
        prompt,
    ):

        agent_map = {
            "coding": "coding",
            "review": "review",
            "design": "design",
            "documentation": "documentation",
        }

        agent = agent_map[task]

        final_prompt = self.prompt_builder.build(
            agent=agent,
            language=language,
            user_prompt=prompt,
        )

        return final_prompt