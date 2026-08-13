from pathlib import Path


class PromptBuilder:
    """ Build a prompt to be sent to an AI model, based on input variables.
        The prompts are based on various configuration that are set in Markdown files (AI **loves** Markdown)
        Just document what you need from the agent in the files, it is all added to the prompt to obtain a great reply.
        A typical prompt is composed of:
        - Instructions for the selected agent,
        - Standards to follow (common to all programming tasks), 
        - Standards to follow for the selected task,
        - User prompt (specific request for the agent/task)
    """

    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.history_limit = -10 # limit context size to last X calls

    def load_file(self, relative_path: str) -> str:
        path = self.root / relative_path
        return path.read_text(encoding="utf-8")

    def format_history(self, history):
        """ Format the history of previous prompts and responses into a string to be added to the prompt."""
        if not history:
            return ""

        lines = []
        for msg in history[self.history_limit:]: # limit context size to last X calls
            role = msg.get("role", "user")
            content = msg.get("content", "")

            lines.append(f"{role.upper()}: {content}")

        return "\n".join(lines)

    def build(
        self,
        agent: str,
        task: str,
        user_prompt: str,
        history: str,
    ) -> str:
        """ Build a prompt for the selected agent, task, user prompt and history.
            The prompt is built from various Markdown files that contain instructions and standards for the agent.
        """

        if agent in {"review", "documentation"}:
            raise ValueError(f"Use the dedicated prompt builder for the {agent} agent.")

        sections = []

        sections.append( self.load_file(f"agents/{agent}.md") )
        sections.append( self.load_file("standards/common.md") )
        sections.append( self.load_file(f"standards/{task.lower()}.md") )

        history_text = self.format_history(history)
        if history_text:
            sections.append("## Conversation History")
            sections.append(history_text)

        sections.append("## User Request")
        sections.append(user_prompt)

        return "\n\n".join(sections)
    
    def build_review_prompt(self, task: str, code: str ) -> str:
        """ Build a prompt for the review agent, with the code to be reviewed.
            The prompt is built from various Markdown files that contain instructions and standards for the agent.
        """
        sections = []

        sections.append( self.load_file(f"agents/review.md") )
        sections.append( self.load_file("standards/common.md") )
        sections.append( self.load_file(f"standards/{task.lower()}.md") )

        sections.append("## Code to Review")
        sections.append(code)

        return "\n\n".join(sections)

    def build_documentation_prompt(self, task: str, content: str) -> str:
        """Build a documentation prompt without applying common coding rules."""
        sections = [
            self.load_file("agents/documentation.md"),
            self.load_file(f"standards/{task.lower()}.md"),
            "## Task",
            task,
            "## Input",
            content,
        ]

        return "\n\n".join(sections)
