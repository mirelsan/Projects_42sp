"""ANSI colour helpers for the terminal visualiser."""

from __future__ import annotations

from typing import Optional

_RESET = "\033[0m"

_COLOR_CODES: dict[str, str] = {
    "black": "30",
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "magenta": "35",
    "cyan": "36",
    "white": "37",
    "gray": "90",
    "grey": "90",
    "orange": "38;5;208",
    "purple": "38;5;93",
    "brown": "38;5;94",
    "maroon": "38;5;88",
    "lime": "38;5;118",
    "gold": "38;5;220",
    "violet": "38;5;135",
    "crimson": "38;5;161",
    "rainbow": "38;5;196",
    "darkred": "38;5;124",
}


class ColorPalette:
    """Turn textual colour names into ANSI escape sequences."""

    def __init__(self, enabled: bool) -> None:
        self.enabled = enabled

    def paint(self, text: str, color: Optional[str]) -> str:
        """Wrap *text* in the requested colour when possible."""
        if not self.enabled or color is None:
            return text
        code = _COLOR_CODES.get(color.lower())
        if code is None:
            return text
        return f"\033[{code}m{text}{_RESET}"
