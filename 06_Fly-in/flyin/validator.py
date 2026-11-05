"""Replay a schedule and verify every movement rule."""

from __future__ import annotations

from dataclasses import dataclass

from .errors import ValidationError
from .models import FlightMap
from .schedule import Move, Schedule


@dataclass
class _Transit:
    """Internal state of a drone crossing a restricted connection."""

    connection: str
    from_zone: str
    to_zone: str
    arrival_turn: int


class ScheduleValidator:
    """Check that a schedule is physically valid on its map."""

    def __init__(self, flight_map: FlightMap) -> None:
        self.flight_map = flight_map

    def validate(self, schedule: Schedule) -> None:
        """Raise :class:`ValidationError` on the first broken rule."""
        nb_drones = self.flight_map.nb_drones
        positions: dict[int, str] = {
            drone_id: self.flight_map.start
            for drone_id in range(1, nb_drones + 1)
        }
        transits: dict[int, _Transit] = {}
        delivered: set[int] = set()
        grouped = schedule.moves_by_turn()

        for turn in range(1, schedule.total_turns + 1):
            departures: dict[str, int] = {}
            arrivals: dict[int, str] = {}
            new_transits: dict[int, _Transit] = {}
            moved: set[int] = set()

            for drone_id, move in grouped.get(turn, []):
                if drone_id in moved:
                    raise ValidationError(
                        f"turn {turn}: D{drone_id} moves twice"
                    )
                moved.add(drone_id)
                if drone_id in delivered:
                    raise ValidationError(
                        f"turn {turn}: D{drone_id} already delivered"
                    )
                self._process_move(
                    drone_id,
                    move,
                    turn,
                    positions,
                    transits,
                    departures,
                    arrivals,
                    new_transits,
                )

            for drone_id in transits:
                if drone_id not in moved:
                    raise ValidationError(
                        f"turn {turn}: D{drone_id} must finish its "
                        "restricted crossing this turn"
                    )

            self._check_connection_capacity(departures, turn)
            self._apply_arrivals(arrivals, positions, delivered)
            transits.update(new_transits)
            self._check_zone_capacity(positions, turn)
            if set(positions) & set(transits):
                raise ValidationError(
                    f"turn {turn}: a drone is both in a zone and in flight"
                )

        if transits:
            raise ValidationError(
                "the simulation ends while drones are still in flight"
            )
        expected = set(range(1, nb_drones + 1))
        if delivered != expected:
            missing = sorted(expected - delivered)
            raise ValidationError(
                f"drones not delivered at the end: {missing}"
            )

    def _process_move(
        self,
        drone_id: int,
        move: Move,
        turn: int,
        positions: dict[int, str],
        transits: dict[int, _Transit],
        departures: dict[str, int],
        arrivals: dict[int, str],
        new_transits: dict[int, _Transit],
    ) -> None:
        """Apply one move to the temporary state."""
        if drone_id in transits:
            transit = transits[drone_id]
            if move.is_transit:
                raise ValidationError(
                    f"turn {turn}: D{drone_id} cannot wait in flight"
                )
            if turn != transit.arrival_turn:
                raise ValidationError(
                    f"turn {turn}: D{drone_id} arrives at the wrong turn"
                )
            if move.destination != transit.to_zone:
                raise ValidationError(
                    f"turn {turn}: D{drone_id} arrives in the wrong zone"
                )
            arrivals[drone_id] = move.destination
            del transits[drone_id]
            return

        current = positions.get(drone_id)
        if current is None:
            raise ValidationError(
                f"turn {turn}: D{drone_id} is not in a known zone"
            )
        if move.is_transit:
            connection = self.flight_map.connection_by_name(
                move.connection or ""
            )
            if connection is None:
                raise ValidationError(
                    f"turn {turn}: unknown connection {move.connection!r}"
                )
            try:
                destination = connection.other(current)
            except ValueError as exc:
                raise ValidationError(
                    f"turn {turn}: D{drone_id} cannot enter "
                    f"{move.connection!r} from {current!r}"
                ) from exc
            target = self.flight_map.zone(destination)
            if target.is_blocked:
                raise ValidationError(
                    f"turn {turn}: D{drone_id} enters a blocked zone"
                )
            departures[connection.name] = (
                departures.get(connection.name, 0) + 1
            )
            new_transits[drone_id] = _Transit(
                connection=connection.name,
                from_zone=current,
                to_zone=destination,
                arrival_turn=turn + 1,
            )
            del positions[drone_id]
            return

        connection = self.flight_map.connection(
            current, move.destination
        )
        if connection is None:
            raise ValidationError(
                f"turn {turn}: D{drone_id} cannot move from "
                f"{current!r} to {move.destination!r}"
            )
        target = self.flight_map.zone(move.destination)
        if target.is_blocked:
            raise ValidationError(
                f"turn {turn}: D{drone_id} enters a blocked zone"
            )
        departures[connection.name] = (
            departures.get(connection.name, 0) + 1
        )
        arrivals[drone_id] = move.destination
        del positions[drone_id]

    def _check_connection_capacity(
        self, departures: dict[str, int], turn: int
    ) -> None:
        """Verify that no connection is overused during a turn."""
        for connection_name, count in departures.items():
            connection = self.flight_map.connection_by_name(
                connection_name
            )
            if connection is None:
                raise ValidationError(
                    f"turn {turn}: unknown connection "
                    f"{connection_name!r}"
                )
            if count > connection.max_link_capacity:
                raise ValidationError(
                    f"turn {turn}: connection {connection_name!r} "
                    f"carries {count} drones but its capacity is "
                    f"{connection.max_link_capacity}"
                )

    def _apply_arrivals(
        self,
        arrivals: dict[int, str],
        positions: dict[int, str],
        delivered: set[int],
    ) -> None:
        """Place every arriving drone in its destination zone."""
        for drone_id, destination in arrivals.items():
            if destination == self.flight_map.end:
                delivered.add(drone_id)
            else:
                positions[drone_id] = destination

    def _check_zone_capacity(
        self, positions: dict[int, str], turn: int
    ) -> None:
        """Verify that no zone exceeds its maximum occupancy."""
        occupancy: dict[str, int] = {}
        for zone_name in positions.values():
            occupancy[zone_name] = occupancy.get(zone_name, 0) + 1
        for zone_name, count in occupancy.items():
            if zone_name in (self.flight_map.start, self.flight_map.end):
                continue
            zone = self.flight_map.zone(zone_name)
            if count > zone.max_drones:
                raise ValidationError(
                    f"turn {turn}: zone {zone_name!r} holds "
                    f"{count} drones but its capacity is "
                    f"{zone.max_drones}"
                )
