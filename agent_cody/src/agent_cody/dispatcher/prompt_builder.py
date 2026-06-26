from pathlib import Path


class PromptBuilder:
    """ Build a prompt to be sent to an AI model. 
        The prompts are based on various configuration that are set in Markdown files (AI **loves** Markdown)
        Just document what you need from the agent in the files, it is all added to the prompt to obtain a great reply.
        A typical prompt is composed of:
        - Instructions for the selected agent,
        - Standards to follow (common to all languages), 
        - Standards to follow for the selected language,
        - User prompt (specific request for the agent/language)
    """

    def __init__(self):
        self.root = Path(__file__).parent.parent

    def load_file(self, relative_path: str) -> str:
        path = self.root / relative_path
        return path.read_text(encoding="utf-8")

    def build(
        self,
        agent: str,
        language: str,
        user_prompt: str,
    ) -> str:

        sections = []

        sections.append(
            self.load_file(f"agents/{agent}.md")
        )

        sections.append(
            self.load_file("standards/common.md")
        )

        sections.append(
            self.load_file(f"standards/{language.lower()}.md")
        )

        sections.append("## User Request")
        sections.append(user_prompt)

        return "\n\n".join(sections)