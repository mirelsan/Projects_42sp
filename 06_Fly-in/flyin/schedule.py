"""Data structures describing a completed simulation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .colors import ColorPalette
from .models import FlightMap


@dataclass(frozen=True)
class Move:
    """One visible action performed by a drone during a turn."""

    turn: int
    destination: str
    connection: Optional[str] = None
    is_transit: bool = False
    arrival_turn: int = 0
    color: Optional[str] = None
    target_zone: Optional[str] = None


@dataclass
class Trajectory:
    """The complete list of moves of one drone."""

    drone_id: int
    moves: list[Move] = field(default_factory=list)
    arrival_turn: int = 0


@dataclass
class Schedule:
    """A full, validated simulation schedule."""

    flight_map: FlightMap
    trajectories: list[Trajectory]
    total_turns: int
    lower_bound: int
    upper_bound: int
    used_fallback: bool = False

    def moves_by_turn(self) -> dict[int, list[tuple[int, Move]]]:
        """Group every visible move by its simulation turn."""
        grouped: dict[int, list[tuple[int, Move]]] = {}
        for trajectory in self.trajectories:
            for move in trajectory.moves:
                grouped.setdefault(move.turn, []).append(
                    (trajectory.drone_id, move)
                )
        for entries in grouped.values():
            entries.sort(key=lambda item: item[0])
        return grouped

    def lines(self) -> list[str]:
        """Return the simulation output in the required plain format."""
        grouped = self.moves_by_turn()
        lines: list[str] = []
        for turn in range(1, self.total_turns + 1):
            tokens = [
                f"D{drone_id}-{move.destination}"
                for drone_id, move in grouped.get(turn, [])
            ]
            lines.append(" ".join(tokens))
        return lines

    def colored_lines(self, palette: ColorPalette) -> list[str]:
        """Return the simulation output with coloured zone names."""
        grouped = self.moves_by_turn()
        lines: list[str] = []
        for turn in range(1, self.total_turns + 1):
            tokens: list[str] = []
            for drone_id, move in grouped.get(turn, []):
                token = f"D{drone_id}-{move.destination}"
                tokens.append(palette.paint(token, move.color))
            lines.append(" ".join(tokens))
        return lines

    def summary(self) -> str:
        """Return a compact human-readable summary."""
        suffix = ""
        if self.used_fallback:
            suffix = " [safe fallback schedule]"
        return (
            f"{self.flight_map.nb_drones} drones delivered in "
            f"{self.total_turns} turns "
            f"(theoretical lower bound: {self.lower_bound}){suffix}"
        )
