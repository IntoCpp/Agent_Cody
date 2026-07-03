from dataclasses import dataclass
from typing import List


@dataclass
class ReviewIssue:
    id: str
    severity: str   # "critical", "major", "minor"
    category: str   # "correctness", "style", etc.
    description: str
    recommendation: str


@dataclass
class ReviewResult:
    approved: bool
    issues: List[ReviewIssue]