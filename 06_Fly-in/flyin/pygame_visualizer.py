"""Interactive Pygame visualisation of a completed schedule."""

from __future__ import annotations

import math

import pygame

from .models import FlightMap, Zone
from .schedule import Move, Schedule


class PygameVisualizer:
    """Replay a schedule in a Pygame window."""

    def __init__(self, width: int = 1100, height: int = 700) -> None:
        self.width = width
        self.height = height

    def render(self, schedule: Schedule) -> None:
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Fly-in replay")
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 24)
        small_font = pygame.font.Font(None, 18)

        flight_map = schedule.flight_map
        points = self._layout(flight_map.zones)
        positions = {
            drone: flight_map.start
            for drone in range(1, flight_map.nb_drones + 1)
        }
        transits: dict[int, tuple[str, str, int, int]] = {}
        delivered: set[int] = set()
        grouped = schedule.moves_by_turn()

        turn = 1
        playing = True
        turn_timer = 0.0
        turn_delay = 700
        running = True

        while running:
            delta = clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        playing = not playing
                    elif event.key in (pygame.K_RIGHT, pygame.K_n):
                        turn = min(turn + 1, schedule.total_turns + 1)
                        positions, transits, delivered = self._apply_turn(
                            turn, grouped, positions, transits, delivered,
                            flight_map.start, flight_map.end,
                        )
                    elif event.key == pygame.K_LEFT:
                        turn = max(1, turn - 1)
                        positions = {
                            drone: flight_map.start
                            for drone in range(1, flight_map.nb_drones + 1)
                        }
                        transits = {}
                        delivered = set()
                        for replay_turn in range(1, turn + 1):
                            positions, transits, delivered = self._apply_turn(
                                replay_turn, grouped, positions, transits,
                                delivered, flight_map.start, flight_map.end,
                            )

            if playing and turn <= schedule.total_turns:
                turn_timer += delta
                if turn_timer >= turn_delay:
                    positions, transits, delivered = self._apply_turn(
                        turn, grouped, positions, transits, delivered,
                        flight_map.start, flight_map.end,
                    )
                    turn += 1
                    turn_timer = 0.0

            screen.fill((8, 11, 18))
            for connection in flight_map.connections:
                pygame.draw.line(
                    screen, (70, 82, 104), points[connection.zone_a],
                    points[connection.zone_b], 3,
                )

            occupancy: dict[str, int] = {}
            for zone_name in positions.values():
                occupancy[zone_name] = occupancy.get(zone_name, 0) + 1

            for zone_name, zone in flight_map.zones.items():
                x, y = points[zone_name]
                color = self._zone_color(zone_name, flight_map)
                if zone.zone_type.value == "restricted":
                    pygame.draw.circle(screen, color, (x, y), 25, 4)
                else:
                    pygame.draw.circle(screen, color, (x, y), 25)
                pygame.draw.circle(screen, (235, 240, 250), (x, y), 25, 2)
                label = small_font.render(zone_name, True, (235, 240, 250))
                screen.blit(label, label.get_rect(center=(x, y + 40)))
                count = occupancy.get(zone_name, 0)
                if count:
                    badge = small_font.render(str(count), True, (10, 15, 24))
                    screen.blit(badge, badge.get_rect(center=(x, y)))

            for drone, zone_name in positions.items():
                x, y = points[zone_name]
                offset = occupancy.get(zone_name, 0)
                angle = drone * math.tau / max(flight_map.nb_drones, 1)
                radius = min(12 + offset * 2, 18)
                drone_x = int(x + math.cos(angle) * radius)
                drone_y = int(y + math.sin(angle) * radius)
                self._draw_drone(screen, font, drone, drone_x, drone_y)

            for drone, flight in transits.items():
                source, destination, departure, arrival = flight
                duration = max(arrival - departure, 1)
                progress = min(max((turn - departure) / duration, 0.0), 1.0)
                start_x, start_y = points[source]
                end_x, end_y = points[destination]
                drone_x = int(start_x + (end_x - start_x) * progress)
                drone_y = int(start_y + (end_y - start_y) * progress)
                self._draw_drone(screen, font, drone, drone_x, drone_y)

            shown_turn = min(max(turn - 1, 0), schedule.total_turns)
            status = "PLAYING" if playing else "PAUSED"
            header = font.render(
                f"Turn {shown_turn}/{schedule.total_turns}  {status}",
                True, (235, 240, 250),
            )
            screen.blit(header, (18, 16))
            controls = small_font.render(
                "SPACE play/pause   LEFT/RIGHT step", True, (160, 174, 198)
            )
            screen.blit(controls, (18, 48))

            pygame.display.flip()

        pygame.quit()

    def _apply_turn(
        self,
        turn: int,
        grouped: dict[int, list[tuple[int, Move]]],
        positions: dict[int, str],
        transits: dict[int, tuple[str, str, int, int]],
        delivered: set[int],
        start_zone: str,
        end_zone: str,
    ) -> tuple[dict[int, str], dict[int, tuple[str, str, int, int]], set[int]]:
        for drone, move in grouped.get(turn, []):
            if move.is_transit:
                source = positions.pop(drone, transits.get(drone, (start_zone, "", turn, turn))[0])
                transits[drone] = (
                    source,
                    move.target_zone or move.destination,
                    turn,
                    move.arrival_turn,
                )
                continue

            transits.pop(drone, None)
            if move.destination == end_zone:
                positions.pop(drone, None)
                delivered.add(drone)
            else:
                positions[drone] = move.destination

        return positions, transits, delivered

    def _layout(self, zones: dict[str, Zone]) -> dict[str, tuple[int, int]]:
        values = list(zones.values())
        if not values:
            return {}
        min_x = min(zone.x for zone in values)
        max_x = max(zone.x for zone in values)
        min_y = min(zone.y for zone in values)
        max_y = max(zone.y for zone in values)
        span_x = max(max_x - min_x, 1)
        span_y = max(max_y - min_y, 1)

        return {
            name: (
                round(90 + (zone.x - min_x) / span_x * (self.width - 180)),
                round(90 + (zone.y - min_y) / span_y * (self.height - 180)),
            )
            for name, zone in zones.items()
        }

    def _zone_color(
        self, zone_name: str, flight_map: FlightMap
    ) -> tuple[int, int, int]:
        zone = flight_map.zone(zone_name)
        named_colors = {
            "start_hub": (58, 170, 220),
            "end_hub": (40, 190, 130),
            "priority": (240, 170, 50),
            "restricted": (150, 110, 210),
            "blocked": (90, 96, 112),
        }
        zone_type = (
            "start_hub" if zone.is_start else
            "end_hub" if zone.is_end else
            zone.zone_type.value
        )
        return named_colors.get(zone_type, (75, 105, 145))

    def _draw_drone(
        self, screen: pygame.Surface, font: pygame.font.Font,
        drone: int, x: int, y: int,
    ) -> None:
        palette = (
            (168, 85, 247), (239, 93, 168), (85, 168, 255),
            (33, 199, 168), (246, 196, 83), (251, 113, 133),
        )
        color = palette[(drone - 1) % len(palette)]
        pygame.draw.circle(screen, color, (x, y), 10)
        pygame.draw.circle(screen, (8, 11, 18), (x, y), 10, 2)
        label = font.render(str(drone), True, (255, 255, 255))
        screen.blit(label, label.get_rect(center=(x, y)))
