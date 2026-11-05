"""Parser for the Fly-in map format."""

from __future__ import annotations

import re
from collections.abc import Iterable
from typing import Optional

from .errors import ParseError
from .models import Connection, FlightMap, Zone, ZoneType

_METADATA_RE = re.compile(r"\[([^\]]*)\]\s*$")

_ZONE_KEYS = {"zone", "color", "max_drones"}
_CONNECTION_KEYS = {"max_link_capacity"}


class MapParser:
    """Turn a textual map into a :class:`FlightMap`."""

    def parse_file(self, path: str) -> FlightMap:
        """Read and parse *path*."""
        with open(path, "r", encoding="utf-8") as handle:
            return self.parse_lines(handle, path)

    def parse_lines(
        self, lines: Iterable[str], source: str = "<input>"
    ) -> FlightMap:
        """Parse an iterable of text lines."""
        nb_drones: Optional[int] = None
        zones: dict[str, Zone] = {}
        connections: list[Connection] = []
        connection_keys: set[tuple[str, str]] = set()
        start: Optional[str] = None
        end: Optional[str] = None
        end_line = 0
        last_line = 0

        for line_number, raw_line in enumerate(lines, 1):
            last_line = line_number
            line = raw_line.split("#", 1)[0].strip()
            if not line:
                continue

            if ":" not in line:
                raise ParseError(
                    line_number, "expected a 'key: value' declaration"
                )
            raw_key, remainder = line.split(":", 1)
            key = raw_key.strip()
            body = remainder.strip()

            if key == "nb_drones":
                if nb_drones is not None:
                    raise ParseError(
                        line_number, "nb_drones is declared more than once"
                    )
                if zones or connections:
                    raise ParseError(
                        line_number,
                        "nb_drones must be declared before zones and links",
                    )
                nb_drones = self._positive_int(
                    body, line_number, "nb_drones"
                )
                continue

            if key not in {"start_hub", "end_hub", "hub", "connection"}:
                raise ParseError(
                    line_number, f"unknown declaration {key!r}"
                )

            if nb_drones is None:
                raise ParseError(
                    line_number,
                    "nb_drones must be declared before this line",
                )

            if key == "connection":
                connection = self._parse_connection(
                    body, line_number, zones, connection_keys
                )
                connections.append(connection)
                connection_keys.add(connection.key)
                continue

            zone = self._parse_zone(body, line_number, key)
            if zone.name in zones:
                raise ParseError(
                    line_number, f"duplicate zone name {zone.name!r}"
                )
            zones[zone.name] = zone

            if key == "start_hub":
                if start is not None:
                    raise ParseError(
                        line_number, "more than one start_hub declared"
                    )
                start = zone.name
            elif key == "end_hub":
                if end is not None:
                    raise ParseError(
                        line_number, "more than one end_hub declared"
                    )
                end = zone.name
                end_line = line_number

        if nb_drones is None:
            raise ParseError(1, "missing nb_drones declaration")
        if start is None:
            raise ParseError(last_line + 1, "missing start_hub declaration")
        if end is None:
            raise ParseError(last_line + 1, "missing end_hub declaration")
        if start == end:
            raise ParseError(
                end_line, "start_hub and end_hub must be different zones"
            )

        return FlightMap(
            nb_drones=nb_drones,
            zones=zones,
            connections=connections,
            start=start,
            end=end,
        )

    def _parse_zone(
        self, body: str, line_number: int, key: str
    ) -> Zone:
        """Parse a start_hub, end_hub or hub line."""
        content, metadata = self._split_metadata(body, line_number)
        parts = content.split()
        if len(parts) != 3:
            raise ParseError(
                line_number,
                "zone declaration must be: <name> <x> <y> [metadata]",
            )
        name, raw_x, raw_y = parts
        self._validate_zone_name(name, line_number)
        x = self._integer(raw_x, line_number, "x coordinate")
        y = self._integer(raw_y, line_number, "y coordinate")

        self._validate_metadata_keys(metadata, _ZONE_KEYS, line_number)
        zone_type = self._zone_type(
            metadata.get("zone", "normal"), line_number
        )
        color = metadata.get("color")
        if color is not None and not color:
            raise ParseError(line_number, "color cannot be empty")
        max_drones = self._positive_int(
            metadata.get("max_drones", "1"),
            line_number,
            "max_drones",
        )

        return Zone(
            name=name,
            x=x,
            y=y,
            zone_type=zone_type,
            color=color,
            max_drones=max_drones,
            is_start=key == "start_hub",
            is_end=key == "end_hub",
        )

    def _parse_connection(
        self,
        body: str,
        line_number: int,
        zones: dict[str, Zone],
        connection_keys: set[tuple[str, str]],
    ) -> Connection:
        """Parse a connection declaration."""
        content, metadata = self._split_metadata(body, line_number)
        parts = content.split()
        if len(parts) != 1:
            raise ParseError(
                line_number,
                "connection declaration must be: <zone1>-<zone2> [metadata]",
            )
        token = parts[0]
        endpoints = token.split("-")
        if len(endpoints) != 2 or not all(endpoints):
            raise ParseError(
                line_number,
                "connection must contain exactly one '-' between two names",
            )
        zone_a, zone_b = endpoints
        self._validate_zone_name(zone_a, line_number)
        self._validate_zone_name(zone_b, line_number)
        if zone_a == zone_b:
            raise ParseError(
                line_number, "a connection cannot link a zone to itself"
            )
        if zone_a not in zones:
            raise ParseError(
                line_number, f"unknown zone {zone_a!r} in connection"
            )
        if zone_b not in zones:
            raise ParseError(
                line_number, f"unknown zone {zone_b!r} in connection"
            )

        self._validate_metadata_keys(
            metadata, _CONNECTION_KEYS, line_number
        )
        max_link_capacity = self._positive_int(
            metadata.get("max_link_capacity", "1"),
            line_number,
            "max_link_capacity",
        )
        connection = Connection(
            zone_a=zone_a,
            zone_b=zone_b,
            max_link_capacity=max_link_capacity,
        )
        if connection.key in connection_keys:
            raise ParseError(
                line_number,
                f"duplicate connection {zone_a!r}-{zone_b!r}",
            )
        return connection

    def _split_metadata(
        self, body: str, line_number: int
    ) -> tuple[str, dict[str, str]]:
        """Split a declaration body into its content and metadata tags."""
        match = _METADATA_RE.search(body)
        if match is None:
            if "[" in body or "]" in body:
                raise ParseError(
                    line_number, "malformed metadata block"
                )
            return body.strip(), {}

        content = body[: match.start()].strip()
        metadata_text = match.group(1).strip()
        metadata: dict[str, str] = {}
        if not metadata_text:
            return content, metadata

        for token in metadata_text.split():
            if "=" not in token:
                raise ParseError(
                    line_number,
                    f"metadata tag {token!r} must use key=value",
                )
            tag_key, tag_value = token.split("=", 1)
            if not tag_key or not tag_value:
                raise ParseError(
                    line_number,
                    f"metadata tag {token!r} must use key=value",
                )
            if tag_key in metadata:
                raise ParseError(
                    line_number,
                    f"duplicate metadata key {tag_key!r}",
                )
            metadata[tag_key] = tag_value
        return content, metadata

    def _validate_metadata_keys(
        self,
        metadata: dict[str, str],
        allowed: set[str],
        line_number: int,
    ) -> None:
        """Reject metadata keys that do not belong to the declaration."""
        for tag_key in metadata:
            if tag_key not in allowed:
                raise ParseError(
                    line_number, f"unknown metadata key {tag_key!r}"
                )

    def _zone_type(self, value: str, line_number: int) -> ZoneType:
        """Convert a textual zone type into the enum."""
        try:
            return ZoneType(value)
        except ValueError as exc:
            allowed = ", ".join(item.value for item in ZoneType)
            raise ParseError(
                line_number,
                f"invalid zone type {value!r} (allowed: {allowed})",
            ) from exc

    def _positive_int(
        self, value: str, line_number: int, field: str
    ) -> int:
        """Parse a strictly positive integer."""
        try:
            number = int(value)
        except ValueError as exc:
            raise ParseError(
                line_number, f"{field} must be an integer"
            ) from exc
        if number <= 0:
            raise ParseError(
                line_number, f"{field} must be a positive integer"
            )
        return number

    def _integer(self, value: str, line_number: int, field: str) -> int:
        """Parse an integer (coordinates may be negative)."""
        try:
            return int(value)
        except ValueError as exc:
            raise ParseError(
                line_number, f"{field} must be an integer"
            ) from exc

    def _validate_zone_name(self, name: str, line_number: int) -> None:
        """Check the naming rules for zones."""
        if not name:
            raise ParseError(line_number, "zone name cannot be empty")
        if "-" in name:
            raise ParseError(
                line_number, f"zone name {name!r} cannot contain '-'"
            )
        if any(character.isspace() for character in name):
            raise ParseError(
                line_number, f"zone name {name!r} cannot contain spaces"
            )
        if "[" in name or "]" in name:
            raise ParseError(
                line_number,
                f"zone name {name!r} cannot contain brackets",
            )
