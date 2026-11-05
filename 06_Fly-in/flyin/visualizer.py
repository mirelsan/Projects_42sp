"""Coloured terminal visualisation of a schedule."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import TextIO

from .colors import ColorPalette
from .schedule import Move, Schedule


@dataclass
class _Flight:
    connection: str
    from_zone: str
    to_zone: str
    arrival_turn: int


class Visualizer:
    """Print a turn-by-turn coloured view of the simulation."""

    def __init__(
        self,
        palette: ColorPalette,
        stream: TextIO = sys.stderr,
    ) -> None:
        self.palette = palette
        self.stream = stream

    def render(self, schedule: Schedule) -> None:
        """Render the whole schedule to the configured stream."""
        flight_map = schedule.flight_map
        print(
            self.palette.paint(
                f"Map: {flight_map.nb_drones} drones, "
                f"{len(flight_map.zones)} zones, "
                f"{len(flight_map.connections)} connections",
                "cyan",
            ),
            file=self.stream,
        )

        positions: dict[int, str] = {
            drone_id: flight_map.start
            for drone_id in range(1, flight_map.nb_drones + 1)
        }
        transits: dict[int, _Flight] = {}
        delivered: set[int] = set()
        grouped = schedule.moves_by_turn()

        for turn in range(1, schedule.total_turns + 1):
            moves = grouped.get(turn, [])
            self._apply_moves(
                moves, positions, transits, delivered, flight_map.end
            )
            header = self.palette.paint(
                f"--- Turn {turn} ---", "cyan"
            )
            print(header, file=self.stream)
            self._print_moves(moves)
            self._print_zone_states(
                positions, transits, delivered, schedule
            )

    def _apply_moves(
        self,
        moves: list[tuple[int, Move]],
        positions: dict[int, str],
        transits: dict[int, _Flight],
        delivered: set[int],
        end_zone: str,
    ) -> None:
        """Update the visual state with one turn of moves."""
        for drone_id, move in moves:
            if move.is_transit:
                current = positions.get(drone_id)
                if current is None:
                    continue
                transits[drone_id] = _Flight(
                    connection=move.destination,
                    from_zone=current,
                    to_zone=move.target_zone or "?",
                    arrival_turn=move.arrival_turn,
                )
                del positions[drone_id]
                continue
            transits.pop(drone_id, None)
            if move.destination == end_zone:
                delivered.add(drone_id)
                positions.pop(drone_id, None)
            else:
                positions[drone_id] = move.destination

    def _print_moves(self, moves: list[tuple[int, Move]]) -> None:
        """Print the visible moves of one turn."""
        if not moves:
            print("  (no visible move)", file=self.stream)
            return
        tokens = []
        for drone_id, move in moves:
            token = f"D{drone_id}-{move.destination}"
            tokens.append(self.palette.paint(token, move.color))
        print("  " + " ".join(tokens), file=self.stream)

    def _print_zone_states(
        self,
        positions: dict[int, str],
        transits: dict[int, _Flight],
        delivered: set[int],
        schedule: Schedule,
    ) -> None:
        """Print a compact occupancy view for the current turn."""
        flight_map = schedule.flight_map
        occupancy: dict[str, int] = {}
        for zone_name in positions.values():
            occupancy[zone_name] = occupancy.get(zone_name, 0) + 1

        states: list[str] = []
        for zone_name in sorted(occupancy):
            zone = flight_map.zone(zone_name)
            label = f"{zone_name}({occupancy[zone_name]})"
            states.append(self.palette.paint(label, zone.color))
        if delivered:
            states.append(
                self.palette.paint(
                    f"{flight_map.end}(delivered={len(delivered)})",
                    flight_map.zone(flight_map.end).color,
                )
            )
        if states:
            print("  Zones: " + " ".join(states), file=self.stream)

        if transits:
            flights = [
                f"{flight.connection} "
                f"({flight.from_zone}->{flight.to_zone})"
                for flight in transits.values()
            ]
            print(
                "  In flight: " + ", ".join(flights),
                file=self.stream,
            )
