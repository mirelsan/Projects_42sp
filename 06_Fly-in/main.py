#!/usr/bin/env python3
"""Entry point for the Fly-in drone routing simulation."""

from __future__ import annotations

import argparse
import sys
from typing import Optional, Sequence, cast

from flyin.colors import ColorPalette
from flyin.errors import FlyInError
from flyin.parser import MapParser
from flyin.pygame_visualizer import PygameVisualizer
from flyin.scheduler import FlowScheduler
from flyin.visualizer import Visualizer


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="fly-in",
        description=(
            "Route a fleet of drones from the start hub to the end hub "
            "in the fewest possible simulation turns."
        ),
    )
    parser.add_argument(
        "map_file",
        help="path to a map file",
    )
    parser.add_argument(
        "--visual",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="show the coloured turn-by-turn view on stderr",
    )
    parser.add_argument(
        "--color",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="force or disable ANSI colours",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="print a short performance summary on stderr",
    )
    parser.add_argument(
        "--capacity-info",
        action="store_true",
        help="print zone and connection capacity usage on stderr",
    )
    parser.add_argument(
        "--pygame",
        action="store_true",
        help="show the interactive replay in a Pygame window",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="show the full traceback on unexpected errors",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Run the program and return a process exit status."""
    sys.setrecursionlimit(100_000)
    args = build_parser().parse_args(argv)
    map_file = cast(str, args.map_file)
    force_visual = cast(Optional[bool], args.visual)
    force_color = cast(Optional[bool], args.color)
    show_stats = cast(bool, args.stats)
    capacity_info = cast(bool, args.capacity_info)
    pygame_visual = cast(bool, args.pygame)
    debug = cast(bool, args.debug)

    visual = (
        False
        if pygame_visual
        else force_visual
        if force_visual is not None
        else sys.stderr.isatty()
    )
    color = (
        force_color if force_color is not None else sys.stdout.isatty()
    )
    palette = ColorPalette(enabled=color)

    try:
        flight_map = MapParser().parse_file(map_file)
        schedule = FlowScheduler(flight_map).solve()
    except FlyInError as error:
        print(f"Error: {map_file}: {error}", file=sys.stderr)
        return 1
    except OSError as error:
        print(f"Error: {map_file}: {error}", file=sys.stderr)
        return 1
    except Exception as error:  # noqa: BLE001
        if debug:
            raise
        print(
            f"Unexpected error while processing {map_file}: {error}",
            file=sys.stderr,
        )
        return 1

    lines = schedule.colored_lines(palette)
    for line in lines:
        print(line)
    sys.stdout.flush()

    if pygame_visual:
        PygameVisualizer().render(schedule)
    if visual:
        Visualizer(palette, sys.stderr).render(schedule)
    if capacity_info:
        Visualizer(palette, sys.stderr).render_capacity(schedule)
    if show_stats:
        print(schedule.summary(), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
