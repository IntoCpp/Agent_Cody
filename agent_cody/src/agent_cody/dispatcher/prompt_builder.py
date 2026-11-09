from pathlib import Path


class PromptBuilder:
    """Compose prompts from Markdown agents/standards plus optional conversation transcript.

    Static instructions (agent + task standards) are included only when the caller requests them
    (typically the first Submit for each agent+task after Clear); later turns reuse transcript + user text.
    """

    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.history_limit = -10  # last N messages for context window

    def load_file(self, relative_path: str) -> str:
        path = self.root / relative_path
        return path.read_text(encoding="utf-8")

    def format_transcript(self, history: list | None) -> str:
        """Format prior user/assistant turns (excluding the current message)."""
        if not history:
            return ""

        lines = []
        for msg in history[self.history_limit :]:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            lines.append(f"{role.upper()}: {content}")

        return "\n".join(lines)

    def build_static_prefix_coding(self, task: str) -> str:
        sections = [
            self.load_file("agents/coding.md"),
            self.load_file("standards/common.md"),
            self.load_file(f"standards/{task.lower()}.md"),
        ]
        return "\n\n".join(sections)

    def build_static_prefix_review(self, task: str) -> str:
        sections = [
            self.load_file("agents/review.md"),
            self.load_file("standards/common.md"),
            self.load_file(f"standards/{task.lower()}.md"),
        ]
        return "\n\n".join(sections)

    def build_static_prefix_documentation(self, task: str) -> str:
        sections = [
            self.load_file("agents/documentation.md"),
            self.load_file(f"standards/{task.lower()}.md"),
        ]
        return "\n\n".join(sections)

    def build_coding_prompt(
        self,
        task: str,
        user_prompt: str,
        history: list | None,
        include_static: bool,
    ) -> str:
        """Full prompt for the coding agent."""
        parts: list[str] = []
        if include_static:
            parts.append(self.build_static_prefix_coding(task))

        transcript = self.format_transcript(history)
        if transcript:
            parts.append("## Conversation History")
            parts.append(transcript)

        parts.append("## User Request")
        parts.append(user_prompt)
        return "\n\n".join(parts)

    def build_review_prompt(
        self,
        task: str,
        code: str,
        history: list | None,
        include_static: bool,
        focus_notes: str | None = None,
    ) -> str:
        """Full prompt for the review agent (standalone Review agent or Review button)."""
        parts: list[str] = []
        if include_static:
            parts.append(self.build_static_prefix_review(task))

        transcript = self.format_transcript(history)
        if transcript:
            parts.append("## Conversation History")
            parts.append(transcript)

        parts.append("## Code to Review")
        if focus_notes and focus_notes.strip():
            parts.append("### Focus / instructions from user")
            parts.append(focus_notes.strip())
            parts.append("### Code")
        parts.append(code.strip() if code else "")
        return "\n\n".join(parts)

    def build_documentation_prompt(
        self,
        task: str,
        content: str,
        history: list | None,
        include_static: bool,
    ) -> str:
        """Full prompt for the documentation agent."""
        parts: list[str] = []
        if include_static:
            parts.append(self.build_static_prefix_documentation(task))

        transcript = self.format_transcript(history)
        if transcript:
            parts.append("## Conversation History")
            parts.append(transcript)

        parts.append("## Task")
        parts.append(task)
        parts.append("## Input")
        parts.append(content)
        return "\n\n".join(parts)
