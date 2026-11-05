"""Core graph model for the Fly-in drone network."""

from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from .errors import UnsolvableError


class ZoneType(str, Enum):
    """Supported zone kinds."""

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


@dataclass(frozen=True)
class Zone:
    """A single zone (node) of the drone network."""

    name: str
    x: int
    y: int
    zone_type: ZoneType = ZoneType.NORMAL
    color: Optional[str] = None
    max_drones: int = 1
    is_start: bool = False
    is_end: bool = False

    @property
    def movement_cost(self) -> int:
        """Return the number of turns needed to enter this zone."""
        if self.zone_type is ZoneType.RESTRICTED:
            return 2
        return 1

    @property
    def is_blocked(self) -> bool:
        """Tell whether this zone can never be entered."""
        return self.zone_type is ZoneType.BLOCKED

    def capacity(self, nb_drones: int) -> int:
        """Return the maximum simultaneous occupancy of this zone."""
        if self.is_start or self.is_end:
            return nb_drones
        return self.max_drones


@dataclass(frozen=True)
class Connection:
    """A bidirectional link between two zones."""

    zone_a: str
    zone_b: str
    max_link_capacity: int = 1

    @property
    def name(self) -> str:
        """Return the connection name exactly as written in the map."""
        return f"{self.zone_a}-{self.zone_b}"

    @property
    def key(self) -> tuple[str, str]:
        """Return an order-independent key used for duplicate detection."""
        if self.zone_a <= self.zone_b:
            return (self.zone_a, self.zone_b)
        return (self.zone_b, self.zone_a)

    def other(self, zone: str) -> str:
        """Return the endpoint opposite to *zone*."""
        if zone == self.zone_a:
            return self.zone_b
        if zone == self.zone_b:
            return self.zone_a
        raise ValueError(f"{zone!r} is not part of connection {self.name!r}")


@dataclass
class FlightMap:
    """A complete map: its zones, connections and fleet size."""

    nb_drones: int
    zones: dict[str, Zone]
    connections: list[Connection]
    start: str
    end: str
    _adjacency: dict[str, list[tuple[str, Connection]]] = field(
        init=False, repr=False
    )
    _connections_by_name: dict[str, Connection] = field(
        init=False, repr=False
    )

    def __post_init__(self) -> None:
        """Build the adjacency structures once the map is loaded."""
        self._adjacency = {name: [] for name in self.zones}
        self._connections_by_name = {}
        for connection in self.connections:
            self._adjacency[connection.zone_a].append(
                (connection.zone_b, connection)
            )
            self._adjacency[connection.zone_b].append(
                (connection.zone_a, connection)
            )
            self._connections_by_name[connection.name] = connection

    def zone(self, name: str) -> Zone:
        """Return the zone called *name*."""
        return self.zones[name]

    def neighbors(self, name: str) -> list[tuple[str, Connection]]:
        """Return every zone directly connected to *name*."""
        return self._adjacency[name]

    def connection(self, zone_a: str, zone_b: str) -> Optional[Connection]:
        """Return the connection between two adjacent zones, if any."""
        for neighbor, connection in self._adjacency[zone_a]:
            if neighbor == zone_b:
                return connection
        return None

    def connection_by_name(self, name: str) -> Optional[Connection]:
        """Return a connection from its textual name."""
        return self._connections_by_name.get(name)

    def capacity(self, zone_name: str) -> int:
        """Return the maximum occupancy of a zone."""
        return self.zone(zone_name).capacity(self.nb_drones)

    def shortest_path(self) -> tuple[list[str], int]:
        """Return the cheapest start-to-end path and its turn cost.

        The primary cost is the number of turns.  Ties are broken by
        preferring priority zones and then by using fewer hops.
        """
        start_zone = self.zone(self.start)
        if start_zone.is_blocked or self.zone(self.end).is_blocked:
            raise UnsolvableError(
                "start or end hub is blocked, so no route can exist"
            )

        distance: dict[str, tuple[int, int, int]] = {
            self.start: (0, 0, 0)
        }
        parent: dict[str, str] = {}
        heap: list[tuple[int, int, int, str]] = [(0, 0, 0, self.start)]

        while heap:
            turns, penalty, hops, current = heapq.heappop(heap)
            if (turns, penalty, hops) != distance.get(current):
                continue
            if current == self.end:
                break
            for neighbor, _connection in self.neighbors(current):
                target = self.zone(neighbor)
                if target.is_blocked:
                    continue
                step = target.movement_cost
                priority_penalty = 0
                if target.zone_type is not ZoneType.PRIORITY:
                    priority_penalty = 1
                candidate = (
                    turns + step,
                    penalty + priority_penalty,
                    hops + 1,
                )
                previous = distance.get(neighbor)
                if previous is None or candidate < previous:
                    distance[neighbor] = candidate
                    parent[neighbor] = current
                    heapq.heappush(
                        heap,
                        (candidate[0], candidate[1], candidate[2], neighbor),
                    )

        if self.end not in distance:
            raise UnsolvableError(
                f"no path connects {self.start!r} to {self.end!r}"
            )

        path: list[str] = [self.end]
        cursor = self.end
        while cursor != self.start:
            cursor = parent[cursor]
            path.append(cursor)
        path.reverse()
        return path, distance[self.end][0]
