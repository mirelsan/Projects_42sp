"""Exception hierarchy used across the Fly-in project."""

from __future__ import annotations


class FlyInError(Exception):
    """Base class for every expected Fly-in error."""


class ParseError(FlyInError):
    """Raised when a map file does not follow the expected syntax."""

    def __init__(self, line: int, message: str) -> None:
        self.line = line
        self.message = message
        super().__init__(f"line {line}: {message}")


class UnsolvableError(FlyInError):
    """Raised when no valid route exists between the start and end hubs."""


class SchedulingError(FlyInError):
    """Raised when the scheduling engine cannot build a valid plan."""


class ValidationError(FlyInError):
    """Raised when a generated schedule breaks a movement rule."""
