"""Helpers for detecting model-related API failures."""

from __future__ import annotations

import re


_MODEL_ERROR_PATTERNS = (
    r"model not found",
    r"model_not_found",
    r"does not exist",
    r"invalid model",
    r"unknown model",
    r"no such model",
    r"model .* not (found|available|supported)",
    r"the model .* does not exist",
)


def is_invalid_model_error(exc: BaseException) -> bool:
    """Return True when an exception likely indicates an invalid or unavailable model."""
    messages: list[str] = [str(exc).lower()]

    response = getattr(exc, "response", None)
    if response is not None:
        status_code = getattr(response, "status_code", None)
        if status_code == 404:
            return True

    body = getattr(exc, "body", None)
    if isinstance(body, dict):
        error = body.get("error", {})
        if isinstance(error, dict):
            messages.append(str(error.get("message", "")).lower())
            messages.append(str(error.get("code", "")).lower())

    combined = " ".join(messages)
    return any(re.search(pattern, combined) for pattern in _MODEL_ERROR_PATTERNS)


class ModelNotAvailableError(Exception):
    """Raised when the selected model cannot be used."""

    def __init__(self, model: str, cause: BaseException):
        self.model = model
        self.cause = cause
        super().__init__(str(cause))
