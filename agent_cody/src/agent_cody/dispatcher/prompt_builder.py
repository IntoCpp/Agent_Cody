from pathlib import Path


class PromptBuilder:
    """ Build a prompt to be sent to an AI model, based on input variables.
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

    def format_history(self, history):
        if not history:
            return ""

        lines = []
        for msg in history[-10:]:  # limit context size to last X calls TODO use a const please
            role = msg.get("role", "user")
            content = msg.get("content", "")

            lines.append(f"{role.upper()}: {content}")

        return "\n".join(lines)

    # TODO: Rename "build_initial_prompt" and document how this is used for the first pass of a task.
    def build(
        self,
        agent: str,
        language: str,
        user_prompt: str,
        history: str,
    ) -> str:
        """ Build a prompt for the selected agent, language, user prompt and history.
            The prompt is built from various Markdown files that contain instructions and standards for the agent.
        """

        sections = []

        # Basic prompt for this task
        sections.append( self.load_file(f"agents/{agent}.md") )
        sections.append( self.load_file("standards/common.md") )
        sections.append( self.load_file(f"standards/{language.lower()}.md") )

        # Add History
        history_text = self.format_history(history)
        if history_text:
            sections.append("## Conversation History")
            sections.append(history_text)

        # Add user latest request
        sections.append("## User Request")
        sections.append(user_prompt)
       

        return "\n\n".join(sections)
    
    def build_review_prompt(self, language: str, code: str ) -> str:
        """ Build a prompt for the review agent, based on the code to be reviewed, and history of previous reviews. 
            The prompt is built from various Markdown files that contain instructions and standards for the agent.
        """
        sections = []

        # Basic prompt for this task
        sections.append( self.load_file(f"agents/review.md") ) # Agent is hard-coded to `review` for this function, since it is only used for the review agent.
        sections.append( self.load_file("standards/common.md") )
        sections.append( self.load_file(f"standards/{language.lower()}.md") )

        # Add code to review
        sections.append("## Code to Review")
        sections.append(code)

        return "\n\n".join(sections)