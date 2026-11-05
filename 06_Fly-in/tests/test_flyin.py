"""Functional tests for the Fly-in project."""

from __future__ import annotations

from pathlib import Path

import pytest

from flyin.errors import ParseError, UnsolvableError
from flyin.parser import MapParser
from flyin.scheduler import FlowScheduler
from flyin.validator import ScheduleValidator

ROOT = Path(__file__).resolve().parent.parent
MAPS = ROOT / "maps"

EXPECTED_TURNS = {
    "01_linear_path.txt": 4,
    "02_simple_fork.txt": 4,
    "03_basic_capacity.txt": 4,
    "01_dead_end_trap.txt": 8,
    "02_circular_loop.txt": 10,
    "03_priority_puzzle.txt": 6,
    "01_maze_nightmare.txt": 13,
    "02_capacity_hell.txt": 16,
    "03_ultimate_challenge.txt": 26,
    "01_the_impossible_dream.txt": 43,
}


@pytest.mark.parametrize(
    ("map_path", "expected"),
    [
        (MAPS / "easy" / "01_linear_path.txt", 4),
        (MAPS / "easy" / "02_simple_fork.txt", 4),
        (MAPS / "easy" / "03_basic_capacity.txt", 4),
        (MAPS / "medium" / "01_dead_end_trap.txt", 8),
        (MAPS / "medium" / "02_circular_loop.txt", 10),
        (MAPS / "medium" / "03_priority_puzzle.txt", 6),
        (MAPS / "hard" / "01_maze_nightmare.txt", 13),
        (MAPS / "hard" / "02_capacity_hell.txt", 16),
        (MAPS / "hard" / "03_ultimate_challenge.txt", 26),
        (
            MAPS / "challenger" / "01_the_impossible_dream.txt",
            43,
        ),
    ],
)
def test_shipped_maps_reach_benchmark(
    map_path: Path, expected: int
) -> None:
    """Every shipped map is solved at its reference turn count."""
    flight_map = MapParser().parse_file(str(map_path))
    schedule = FlowScheduler(flight_map).solve()
    assert schedule.total_turns == expected
    assert not schedule.used_fallback
    ScheduleValidator(flight_map).validate(schedule)


def test_linear_path_output_format() -> None:
    """The simulation output follows the D<id>-<zone> format."""
    flight_map = MapParser().parse_file(
        str(MAPS / "easy" / "01_linear_path.txt")
    )
    schedule = FlowScheduler(flight_map).solve()
    lines = schedule.lines()
    assert lines[0] == "D1-waypoint1"
    assert lines[-1] == "D2-goal"


def test_restricted_connection_transit() -> None:
    """A restricted move is announced on the connection, then arrives."""
    flight_map = MapParser().parse_file(
        str(MAPS / "medium" / "02_circular_loop.txt")
    )
    schedule = FlowScheduler(flight_map).solve()
    lines = schedule.lines()
    transit_turn = next(
        index
        for index, line in enumerate(lines)
        if "D1-loop_b-exit_point" in line
    )
    assert "D1-exit_point" in lines[transit_turn + 1]


def test_parser_rejects_invalid_zone_type(tmp_path: Path) -> None:
    """An unknown zone type is a parsing error."""
    map_file = tmp_path / "bad.txt"
    map_file.write_text(
        "nb_drones: 1\n"
        "start_hub: start 0 0\n"
        "hub: middle 1 0 [zone=lava]\n"
        "end_hub: goal 2 0\n"
        "connection: start-middle\n"
        "connection: middle-goal\n",
        encoding="utf-8",
    )
    with pytest.raises(ParseError):
        MapParser().parse_file(str(map_file))


def test_parser_rejects_duplicate_connection(tmp_path: Path) -> None:
    """a-b and b-a are the same connection."""
    map_file = tmp_path / "duplicate.txt"
    map_file.write_text(
        "nb_drones: 1\n"
        "start_hub: start 0 0\n"
        "end_hub: goal 1 0\n"
        "connection: start-goal\n"
        "connection: goal-start\n",
        encoding="utf-8",
    )
    with pytest.raises(ParseError):
        MapParser().parse_file(str(map_file))


def test_parser_rejects_non_positive_capacity(
    tmp_path: Path,
) -> None:
    """Capacity metadata must be a positive integer."""
    map_file = tmp_path / "capacity.txt"
    map_file.write_text(
        "nb_drones: 1\n"
        "start_hub: start 0 0\n"
        "hub: middle 1 0 [max_drones=0]\n"
        "end_hub: goal 2 0\n"
        "connection: start-middle\n"
        "connection: middle-goal\n",
        encoding="utf-8",
    )
    with pytest.raises(ParseError):
        MapParser().parse_file(str(map_file))


def test_unsolvable_map_reports_clean_error(tmp_path: Path) -> None:
    """A disconnected graph raises UnsolvableError, not a crash."""
    map_file = tmp_path / "unsolvable.txt"
    map_file.write_text(
        "nb_drones: 2\n"
        "start_hub: start 0 0\n"
        "hub: island 5 5\n"
        "end_hub: goal 1 0\n"
        "connection: start-island\n",
        encoding="utf-8",
    )
    flight_map = MapParser().parse_file(str(map_file))
    with pytest.raises(UnsolvableError):
        FlowScheduler(flight_map).solve()


def test_blocked_zone_is_avoided(tmp_path: Path) -> None:
    """A blocked shortcut is never used."""
    map_file = tmp_path / "blocked.txt"
    map_file.write_text(
        "nb_drones: 1\n"
        "start_hub: start 0 0\n"
        "hub: blocked 1 0 [zone=blocked]\n"
        "hub: safe 1 1\n"
        "end_hub: goal 2 0\n"
        "connection: start-blocked\n"
        "connection: blocked-goal\n"
        "connection: start-safe\n"
        "connection: safe-goal\n",
        encoding="utf-8",
    )
    flight_map = MapParser().parse_file(str(map_file))
    schedule = FlowScheduler(flight_map).solve()
    assert schedule.total_turns == 2
    assert all("blocked" not in line for line in schedule.lines())


def test_metadata_order_is_irrelevant(tmp_path: Path) -> None:
    """Metadata tags can be written in any order."""
    map_file = tmp_path / "metadata.txt"
    map_file.write_text(
        "nb_drones: 1\n"
        "start_hub: start 0 0 [color=green]\n"
        "hub: middle 1 0 [max_drones=2 zone=priority color=blue]\n"
        "end_hub: goal 2 0\n"
        "connection: start-middle [max_link_capacity=2]\n"
        "connection: middle-goal\n",
        encoding="utf-8",
    )
    flight_map = MapParser().parse_file(str(map_file))
    middle = flight_map.zone("middle")
    assert middle.max_drones == 2
    assert middle.zone_type.value == "priority"
    assert middle.color == "blue"
    schedule = FlowScheduler(flight_map).solve()
    assert schedule.total_turns == 2
