"""Optimal turn scheduling using a time-expanded flow network."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional

from .errors import SchedulingError, ValidationError
from .flow import DinicNetwork, FlowEdge
from .models import FlightMap
from .schedule import Move, Schedule, Trajectory
from .validator import ScheduleValidator


@dataclass(frozen=True)
class _NodeInfo:
    """Describe what a time-expanded node represents."""

    kind: Literal["zone", "connection", "source", "sink"]
    zone: Optional[str] = None
    time: int = 0
    side: int = 0
    connection_name: Optional[str] = None
    departure: int = 0


class FlowScheduler:
    """Compute a minimum-turn schedule with max-flow over time.

    Every zone is split into an ``in`` and an ``out`` node for each
    simulation turn.  A zone-capacity edge joins the two halves, waiting
    edges connect consecutive turns, and movement edges jump from the
    departure turn to the arrival turn.  A small shared-capacity gadget
    per connection and departure turn enforces the bidirectional
    ``max_link_capacity`` rule.  A flow of ``nb_drones`` units from the
    super-source to the super-sink is therefore exactly a valid schedule.
    Binary search finds the smallest feasible horizon.
    """

    FLOW_DRONE_LIMIT = 60

    def __init__(self, flight_map: FlightMap) -> None:
        self.flight_map = flight_map

    def solve(self) -> Schedule:
        """Return a validated schedule with the fewest possible turns."""
        if self.flight_map.nb_drones > self.FLOW_DRONE_LIMIT:
            schedule = self._build_fallback_schedule()
            ScheduleValidator(self.flight_map).validate(schedule)
            return schedule
        try:
            return self._solve_with_flow()
        except (SchedulingError, ValidationError):
            schedule = self._build_fallback_schedule()
            ScheduleValidator(self.flight_map).validate(schedule)
            return schedule

    def _solve_with_flow(self) -> Schedule:
        """Solve the problem with the time-expanded flow model."""
        _path, lower_bound = self.flight_map.shortest_path()
        upper_bound = lower_bound + self.flight_map.nb_drones - 1

        low = lower_bound
        high = upper_bound
        while low < high:
            middle = (low + high) // 2
            if self._is_feasible(middle):
                high = middle
            else:
                low = middle + 1

        total_turns = low
        network, source, sink, node_info = self._build_network(
            total_turns
        )
        flow = network.max_flow(source, sink)
        if flow != self.flight_map.nb_drones:
            raise SchedulingError(
                "internal error: the flow did not deliver every drone"
            )
        edge_paths = network.extract_paths(
            source, sink, self.flight_map.nb_drones
        )
        trajectories = self._build_trajectories(
            edge_paths, node_info, source
        )
        schedule = Schedule(
            flight_map=self.flight_map,
            trajectories=trajectories,
            total_turns=total_turns,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
        )
        ScheduleValidator(self.flight_map).validate(schedule)
        return schedule

    def _build_fallback_schedule(self) -> Schedule:
        """Build a guaranteed-valid pipeline along the shortest path."""
        path, lower_bound = self.flight_map.shortest_path()
        nb_drones = self.flight_map.nb_drones
        trajectories: list[Trajectory] = []
        for drone_id in range(1, nb_drones + 1):
            moves: list[Move] = []
            departure = drone_id
            for from_zone, to_zone in zip(path, path[1:]):
                connection = self.flight_map.connection(
                    from_zone, to_zone
                )
                if connection is None:
                    raise SchedulingError(
                        "internal error: shortest path has no connection"
                    )
                target = self.flight_map.zone(to_zone)
                arrival = departure + target.movement_cost - 1
                if target.movement_cost == 2:
                    moves.append(
                        Move(
                            turn=departure,
                            destination=connection.name,
                            connection=connection.name,
                            is_transit=True,
                            arrival_turn=arrival,
                            color=target.color,
                            target_zone=to_zone,
                        )
                    )
                    moves.append(
                        Move(
                            turn=arrival,
                            destination=to_zone,
                            connection=None,
                            is_transit=False,
                            arrival_turn=arrival,
                            color=target.color,
                            target_zone=to_zone,
                        )
                    )
                else:
                    moves.append(
                        Move(
                            turn=departure,
                            destination=to_zone,
                            connection=None,
                            is_transit=False,
                            arrival_turn=arrival,
                            color=target.color,
                            target_zone=to_zone,
                        )
                    )
                departure = arrival + 1
            trajectories.append(
                Trajectory(
                    drone_id=drone_id,
                    moves=moves,
                    arrival_turn=departure - 1,
                )
            )
        total_turns = lower_bound + nb_drones - 1
        return Schedule(
            flight_map=self.flight_map,
            trajectories=trajectories,
            total_turns=total_turns,
            lower_bound=lower_bound,
            upper_bound=total_turns,
            used_fallback=True,
        )

    def _is_feasible(self, horizon: int) -> bool:
        """Tell whether every drone can arrive within *horizon* turns."""
        network, source, sink, _node_info = self._build_network(horizon)
        flow = network.max_flow(source, sink)
        return flow == self.flight_map.nb_drones

    def _build_network(
        self, horizon: int
    ) -> tuple[DinicNetwork, int, int, dict[int, _NodeInfo]]:
        """Build the time-expanded graph for a fixed horizon."""
        node_info: dict[int, _NodeInfo] = {}
        next_id = 0

        def new_node(info: _NodeInfo) -> int:
            nonlocal next_id
            node_id = next_id
            next_id += 1
            node_info[node_id] = info
            return node_id

        zone_index: dict[tuple[str, int, int], int] = {}

        def node(zone_name: str, time: int, side: int) -> int:
            key = (zone_name, time, side)
            existing = zone_index.get(key)
            if existing is not None:
                return existing
            created = new_node(
                _NodeInfo(
                    kind="zone",
                    zone=zone_name,
                    time=time,
                    side=side,
                )
            )
            zone_index[key] = created
            return created

        connection_index: dict[tuple[str, int, int], int] = {}

        def connection_node(
            connection_name: str, departure: int, side: int
        ) -> int:
            key = (connection_name, departure, side)
            existing = connection_index.get(key)
            if existing is not None:
                return existing
            created = new_node(
                _NodeInfo(
                    kind="connection",
                    connection_name=connection_name,
                    departure=departure,
                    side=side,
                )
            )
            connection_index[key] = created
            return created

        for zone_name in self.flight_map.zones:
            for time in range(horizon + 1):
                node(zone_name, time, 0)
                node(zone_name, time, 1)

        for connection in self.flight_map.connections:
            for departure in range(1, horizon + 1):
                connection_node(connection.name, departure, 0)
                connection_node(connection.name, departure, 1)

        source = new_node(_NodeInfo(kind="source"))
        sink = new_node(_NodeInfo(kind="sink"))
        network = DinicNetwork(next_id)
        nb_drones = self.flight_map.nb_drones
        start = self.flight_map.start
        end = self.flight_map.end

        for zone_name in self.flight_map.zones:
            for time in range(horizon + 1):
                if time == 0:
                    capacity = nb_drones if zone_name == start else 0
                else:
                    capacity = self.flight_map.capacity(zone_name)
                network.add_edge(
                    node(zone_name, time, 0),
                    node(zone_name, time, 1),
                    capacity,
                )

        network.add_edge(source, node(start, 0, 0), nb_drones)
        for time in range(1, horizon + 1):
            network.add_edge(
                node(end, time, 1), sink, nb_drones
            )

        for zone_name in self.flight_map.zones:
            if zone_name == end:
                continue
            for time in range(horizon):
                capacity = self.flight_map.capacity(zone_name)
                if time == 0 and zone_name != start:
                    capacity = 0
                network.add_edge(
                    node(zone_name, time, 1),
                    node(zone_name, time + 1, 0),
                    capacity,
                )

        for connection in self.flight_map.connections:
            zone_a = self.flight_map.zone(connection.zone_a)
            zone_b = self.flight_map.zone(connection.zone_b)
            if zone_a.is_blocked or zone_b.is_blocked:
                continue
            cost_ab = zone_b.movement_cost
            cost_ba = zone_a.movement_cost
            for departure in range(1, horizon + 1):
                capacity_in = connection_node(
                    connection.name, departure, 0
                )
                capacity_out = connection_node(
                    connection.name, departure, 1
                )
                network.add_edge(
                    capacity_in,
                    capacity_out,
                    connection.max_link_capacity,
                )
                if connection.zone_a != end:
                    network.add_edge(
                        node(connection.zone_a, departure - 1, 1),
                        capacity_in,
                        connection.max_link_capacity,
                    )
                if connection.zone_b != end:
                    network.add_edge(
                        node(connection.zone_b, departure - 1, 1),
                        capacity_in,
                        connection.max_link_capacity,
                    )
                if connection.zone_a != end:
                    arrival_ab = departure - 1 + cost_ab
                    if arrival_ab <= horizon:
                        network.add_edge(
                            capacity_out,
                            node(connection.zone_b, arrival_ab, 0),
                            connection.max_link_capacity,
                        )
                if connection.zone_b != end:
                    arrival_ba = departure - 1 + cost_ba
                    if arrival_ba <= horizon:
                        network.add_edge(
                            capacity_out,
                            node(connection.zone_a, arrival_ba, 0),
                            connection.max_link_capacity,
                        )

        return network, source, sink, node_info

    def _build_trajectories(
        self,
        edge_paths: list[list[FlowEdge]],
        node_info: dict[int, _NodeInfo],
        source: int,
    ) -> list[Trajectory]:
        """Convert decomposed flow paths into drone trajectories."""
        raw: list[tuple[int, int, list[Move]]] = []
        for edges in edge_paths:
            moves: list[Move] = []
            current = source
            index = 0
            while index < len(edges):
                edge = edges[index]
                next_info = node_info.get(edge.to)
                if (
                    next_info is not None
                    and next_info.kind == "connection"
                    and next_info.side == 0
                ):
                    current_info = node_info.get(current)
                    if (
                        current_info is None
                        or current_info.kind != "zone"
                        or current_info.side != 1
                    ):
                        raise SchedulingError(
                            "internal error: invalid connection entry"
                        )
                    if index + 2 >= len(edges):
                        raise SchedulingError(
                            "internal error: truncated connection path"
                        )
                    capacity_edge = edges[index + 1]
                    exit_edge = edges[index + 2]
                    exit_info = node_info.get(capacity_edge.to)
                    destination_info = node_info.get(exit_edge.to)
                    if (
                        exit_info is None
                        or exit_info.kind != "connection"
                        or exit_info.side != 1
                        or destination_info is None
                        or destination_info.kind != "zone"
                        or destination_info.side != 0
                    ):
                        raise SchedulingError(
                            "internal error: invalid connection exit"
                        )
                    from_zone = current_info.zone
                    to_zone = destination_info.zone
                    if from_zone != to_zone:
                        self._append_movement(
                            moves,
                            from_zone,
                            to_zone,
                            next_info.departure,
                            destination_info.time,
                            next_info.connection_name,
                        )
                    current = exit_edge.to
                    index += 3
                    continue
                current = edge.to
                index += 1

            if not moves:
                raise SchedulingError(
                    "internal error: a drone has an empty trajectory"
                )
            moves.sort(
                key=lambda move: (
                    move.turn,
                    0 if move.is_transit else 1,
                )
            )
            first_turn = moves[0].turn
            arrival_turn = max(move.turn for move in moves)
            raw.append((first_turn, arrival_turn, moves))

        raw.sort(key=lambda item: (item[0], item[1]))
        trajectories: list[Trajectory] = []
        for drone_id, (_first, arrival_turn, moves) in enumerate(
            raw, start=1
        ):
            trajectories.append(
                Trajectory(
                    drone_id=drone_id,
                    moves=moves,
                    arrival_turn=arrival_turn,
                )
            )
        return trajectories

    def _append_movement(
        self,
        moves: list[Move],
        from_zone: Optional[str],
        to_zone: Optional[str],
        departure: int,
        arrival: int,
        connection_name: Optional[str],
    ) -> None:
        """Append the visible moves corresponding to one flow edge."""
        if from_zone is None or to_zone is None:
            raise SchedulingError(
                "internal error: incomplete movement metadata"
            )
        target = self.flight_map.zone(to_zone)
        cost = arrival - departure + 1
        if cost == 2:
            if connection_name is None:
                raise SchedulingError(
                    "internal error: missing connection name"
                )
            moves.append(
                Move(
                    turn=departure,
                    destination=connection_name,
                    connection=connection_name,
                    is_transit=True,
                    arrival_turn=arrival,
                    color=target.color,
                    target_zone=to_zone,
                )
            )
            moves.append(
                Move(
                    turn=arrival,
                    destination=to_zone,
                    connection=None,
                    is_transit=False,
                    arrival_turn=arrival,
                    color=target.color,
                    target_zone=to_zone,
                )
            )
            return
        if cost != 1:
            raise SchedulingError(
                f"internal error: unexpected movement cost {cost}"
            )
        moves.append(
            Move(
                turn=departure,
                destination=to_zone,
                connection=None,
                is_transit=False,
                arrival_turn=departure,
                color=target.color,
                target_zone=to_zone,
            )
        )
