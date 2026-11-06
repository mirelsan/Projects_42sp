"""Interactive Pygame visualisation of a completed schedule.

Supports pan (left-click drag) and zoom (mouse wheel) so that maps with
many zones (e.g. the "Impossible Dream" challenge map) can be inspected
without labels overlapping. Zone labels are truncated to fit their grid
cell and hidden entirely when zoomed out past legibility; hovering a
zone always shows its full name.
"""

from __future__ import annotations

import math

import pygame

from .models import FlightMap, Zone
from .schedule import Move, Schedule

BACKGROUND = (8, 11, 18)
GRID_LINE = (70, 82, 104)
OUTLINE = (235, 240, 250)
TEXT_DIM = (160, 174, 198)
HOVER_RING = (255, 214, 10)
HOVER_TEXT = (255, 230, 120)

CELL = 100.0          # world-space pixels between adjacent grid coordinates
BASE_RADIUS = 25.0    # world-space node radius at zoom == 1
MIN_ZOOM = 0.15
MAX_ZOOM = 4.0
LABEL_ZOOM_THRESHOLD = 0.45  # below this zoom, per-node labels are hidden
MIN_FONT_PX = 10
ZOOM_STEP = 1.15


class PygameVisualizer:
    """Replay a schedule in a Pygame window."""

    def __init__(self, width: int = 1100, height: int = 700) -> None:
        self.width = width
        self.height = height
        self.zoom = 1.0
        self.cam_x = 0.0
        self.cam_y = 0.0
        self._font_cache: dict[int, pygame.font.Font] = {}
        self._dragging = False
        self._drag_anchor: tuple[int, int] = (0, 0)
        self._drag_cam_anchor: tuple[float, float] = (0.0, 0.0)
        self._hovered: str | None = None

    # ------------------------------------------------------------------ #
    # Main loop
    # ------------------------------------------------------------------ #

    def render(self, schedule: Schedule) -> None:
        pygame.init()
        screen = pygame.display.set_mode(
            (self.width, self.height), pygame.RESIZABLE
        )
        pygame.display.set_caption("Fly-in replay")
        clock = pygame.time.Clock()
        self._font_cache = {}
        header_font = self._get_font(24)
        hud_font = self._get_font(16)
        hover_font = self._get_font(20)

        flight_map = schedule.flight_map
        world_points = self._build_world_layout(flight_map.zones)
        self._fit_camera(world_points)

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

                elif event.type == pygame.VIDEORESIZE:
                    self.width, self.height = event.w, event.h
                    screen = pygame.display.set_mode(
                        (self.width, self.height), pygame.RESIZABLE
                    )

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
                    elif event.key == pygame.K_r:
                        self._fit_camera(world_points)

                elif event.type == pygame.MOUSEWHEEL:
                    mouse_pos = pygame.mouse.get_pos()
                    world_under_mouse = self._screen_to_world(mouse_pos)
                    factor = ZOOM_STEP if event.y > 0 else (1 / ZOOM_STEP)
                    self.zoom = min(MAX_ZOOM, max(MIN_ZOOM, self.zoom * factor))
                    self.cam_x = world_under_mouse[0] - (
                        mouse_pos[0] - self.width / 2
                    ) / self.zoom
                    self.cam_y = world_under_mouse[1] - (
                        mouse_pos[1] - self.height / 2
                    ) / self.zoom

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self._dragging = True
                        self._drag_anchor = event.pos
                        self._drag_cam_anchor = (self.cam_x, self.cam_y)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self._dragging = False

                elif event.type == pygame.MOUSEMOTION:
                    if self._dragging:
                        dx = event.pos[0] - self._drag_anchor[0]
                        dy = event.pos[1] - self._drag_anchor[1]
                        self.cam_x = self._drag_cam_anchor[0] - dx / self.zoom
                        self.cam_y = self._drag_cam_anchor[1] - dy / self.zoom

            if playing and turn <= schedule.total_turns:
                turn_timer += delta
                if turn_timer >= turn_delay:
                    positions, transits, delivered = self._apply_turn(
                        turn, grouped, positions, transits, delivered,
                        flight_map.start, flight_map.end,
                    )
                    turn += 1
                    turn_timer = 0.0

            self._hovered = self._find_hovered_zone(world_points)
            occupancy = self._occupancy(positions)

            screen.fill(BACKGROUND)
            self._draw_connections(screen, flight_map, world_points)
            self._draw_zones(screen, flight_map, world_points, occupancy)
            self._draw_zone_labels(screen, flight_map, world_points, hover_font)
            self._draw_drones(
                screen, flight_map, world_points, positions, transits,
                occupancy, turn,
            )
            self._draw_hud(screen, header_font, hud_font, schedule, turn, playing)

            pygame.display.flip()

        pygame.quit()

    # ------------------------------------------------------------------ #
    # Turn logic (unchanged)
    # ------------------------------------------------------------------ #

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
                source = positions.pop(
                    drone, transits.get(drone, (start_zone, "", turn, turn))[0]
                )
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

    def _occupancy(self, positions: dict[int, str]) -> dict[str, int]:
        occupancy: dict[str, int] = {}
        for zone_name in positions.values():
            occupancy[zone_name] = occupancy.get(zone_name, 0) + 1
        return occupancy

    # ------------------------------------------------------------------ #
    # Camera / layout
    # ------------------------------------------------------------------ #

    def _build_world_layout(
        self, zones: dict[str, Zone]
    ) -> dict[str, tuple[float, float]]:
        return {name: (zone.x * CELL, zone.y * CELL) for name, zone in zones.items()}

    def _fit_camera(self, world_points: dict[str, tuple[float, float]]) -> None:
        if not world_points:
            self.zoom = 1.0
            self.cam_x = self.cam_y = 0.0
            return
        xs = [p[0] for p in world_points.values()]
        ys = [p[1] for p in world_points.values()]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        span_x = max(max_x - min_x, 1.0)
        span_y = max(max_y - min_y, 1.0)
        margin = BASE_RADIUS * 2 + 60  # room for the circle plus its label
        zoom_x = (self.width - margin * 2) / span_x
        zoom_y = (self.height - margin * 2) / span_y
        self.zoom = min(MAX_ZOOM, max(MIN_ZOOM, min(zoom_x, zoom_y)))
        self.cam_x = (min_x + max_x) / 2
        self.cam_y = (min_y + max_y) / 2

    def _world_to_screen(self, wx: float, wy: float) -> tuple[int, int]:
        sx = (wx - self.cam_x) * self.zoom + self.width / 2
        sy = (wy - self.cam_y) * self.zoom + self.height / 2
        return int(round(sx)), int(round(sy))

    def _screen_to_world(self, pos: tuple[int, int]) -> tuple[float, float]:
        sx, sy = pos
        wx = (sx - self.width / 2) / self.zoom + self.cam_x
        wy = (sy - self.height / 2) / self.zoom + self.cam_y
        return wx, wy

    def _find_hovered_zone(
        self, world_points: dict[str, tuple[float, float]]
    ) -> str | None:
        mx, my = pygame.mouse.get_pos()
        radius = max(3, round(BASE_RADIUS * self.zoom))
        closest = None
        closest_dist = float(radius)
        for zone_name, world_pos in world_points.items():
            x, y = self._world_to_screen(*world_pos)
            dist = math.hypot(mx - x, my - y)
            if dist <= radius and dist <= closest_dist:
                closest_dist = dist
                closest = zone_name
        return closest

    # ------------------------------------------------------------------ #
    # Fonts / text helpers
    # ------------------------------------------------------------------ #

    def _get_font(self, size: int) -> pygame.font.Font:
        size = max(MIN_FONT_PX, round(size))
        font = self._font_cache.get(size)
        if font is None:
            font = pygame.font.Font(None, size)
            self._font_cache[size] = font
        return font

    def _fit_text(self, text: str, font: pygame.font.Font, max_width: int) -> str:
        if font.size(text)[0] <= max_width:
            return text
        truncated = text
        while truncated and font.size(truncated + "…")[0] > max_width:
            truncated = truncated[:-1]
        return f"{truncated}…" if truncated else text[:1]

    def _blit_with_plate(
        self, screen: pygame.Surface, label: pygame.Surface, rect: pygame.Rect,
        pad: int = 3,
    ) -> None:
        plate = pygame.Surface((rect.width + pad * 2, rect.height + pad * 2), pygame.SRCALPHA)
        plate.fill((*BACKGROUND, 185))
        screen.blit(plate, (rect.x - pad, rect.y - pad))
        screen.blit(label, rect)

    # ------------------------------------------------------------------ #
    # Drawing
    # ------------------------------------------------------------------ #

    def _draw_connections(
        self, screen: pygame.Surface, flight_map: FlightMap,
        world_points: dict[str, tuple[float, float]],
    ) -> None:
        width = max(1, round(3 * self.zoom))
        for connection in flight_map.connections:
            a = self._world_to_screen(*world_points[connection.zone_a])
            b = self._world_to_screen(*world_points[connection.zone_b])
            pygame.draw.line(screen, GRID_LINE, a, b, width)

    def _draw_zones(
        self, screen: pygame.Surface, flight_map: FlightMap,
        world_points: dict[str, tuple[float, float]], occupancy: dict[str, int],
    ) -> None:
        radius = max(3, round(BASE_RADIUS * self.zoom))
        badge_font = self._get_font(18 * self.zoom)
        for zone_name, zone in flight_map.zones.items():
            x, y = self._world_to_screen(*world_points[zone_name])
            color = self._zone_color(zone_name, flight_map)
            if zone.zone_type.value == "restricted":
                pygame.draw.circle(screen, color, (x, y), radius, max(2, round(4 * self.zoom)))
            else:
                pygame.draw.circle(screen, color, (x, y), radius)
            is_hovered = zone_name == self._hovered
            ring_color = HOVER_RING if is_hovered else OUTLINE
            ring_width = 3 if is_hovered else 2
            pygame.draw.circle(screen, ring_color, (x, y), radius, ring_width)
            count = occupancy.get(zone_name, 0)
            if count:
                badge = badge_font.render(str(count), True, (10, 15, 24))
                screen.blit(badge, badge.get_rect(center=(x, y)))

    def _draw_zone_labels(
        self, screen: pygame.Surface, flight_map: FlightMap,
        world_points: dict[str, tuple[float, float]], hover_font: pygame.font.Font,
    ) -> None:
        radius = max(3, round(BASE_RADIUS * self.zoom))

        if self.zoom >= LABEL_ZOOM_THRESHOLD:
            # Enough room on screen to show per-node labels. Cap each one to
            # (a bit less than) its own grid cell width so neighbouring
            # labels can never touch, regardless of how long the zone name is.
            label_font = self._get_font(16 * self.zoom)
            max_width = max(20, round(CELL * self.zoom * 0.92))
            for zone_name in flight_map.zones:
                x, y = self._world_to_screen(*world_points[zone_name])
                text = self._fit_text(zone_name, label_font, max_width)
                label = label_font.render(text, True, OUTLINE)
                rect = label.get_rect(center=(x, y + radius + 16))
                self._blit_with_plate(screen, label, rect)

        if self._hovered:
            # Always legible and never truncated, independent of zoom level.
            x, y = self._world_to_screen(*world_points[self._hovered])
            label = hover_font.render(self._hovered, True, HOVER_TEXT)
            rect = label.get_rect(midtop=(x, y + radius + 16))
            self._blit_with_plate(screen, label, rect, pad=4)

    def _draw_drones(
        self, screen: pygame.Surface, flight_map: FlightMap,
        world_points: dict[str, tuple[float, float]], positions: dict[int, str],
        transits: dict[int, tuple[str, str, int, int]], occupancy: dict[str, int],
        turn: int,
    ) -> None:
        drone_font = self._get_font(22 * self.zoom)
        for drone, zone_name in positions.items():
            x, y = self._world_to_screen(*world_points[zone_name])
            offset = occupancy.get(zone_name, 0)
            angle = drone * math.tau / max(flight_map.nb_drones, 1)
            orbit = min(12 + offset * 2, 18) * self.zoom
            drone_x = int(x + math.cos(angle) * orbit)
            drone_y = int(y + math.sin(angle) * orbit)
            self._draw_single_drone(screen, drone_font, drone, drone_x, drone_y)

        for drone, flight in transits.items():
            source, destination, departure, arrival = flight
            duration = max(arrival - departure, 1)
            progress = min(max((turn - departure) / duration, 0.0), 1.0)
            start_x, start_y = self._world_to_screen(*world_points[source])
            end_x, end_y = self._world_to_screen(*world_points[destination])
            drone_x = int(start_x + (end_x - start_x) * progress)
            drone_y = int(start_y + (end_y - start_y) * progress)
            self._draw_single_drone(screen, drone_font, drone, drone_x, drone_y)

    def _draw_single_drone(
        self, screen: pygame.Surface, font: pygame.font.Font,
        drone: int, x: int, y: int,
    ) -> None:
        palette = (
            (168, 85, 247), (239, 93, 168), (85, 168, 255),
            (33, 199, 168), (246, 196, 83), (251, 113, 133),
        )
        color = palette[(drone - 1) % len(palette)]
        radius = max(4, round(10 * self.zoom))
        pygame.draw.circle(screen, color, (x, y), radius)
        pygame.draw.circle(screen, BACKGROUND, (x, y), radius, max(1, round(2 * self.zoom)))
        if self.zoom > 0.5:
            label = font.render(str(drone), True, (255, 255, 255))
            screen.blit(label, label.get_rect(center=(x, y)))

    def _draw_hud(
        self, screen: pygame.Surface, header_font: pygame.font.Font,
        hud_font: pygame.font.Font, schedule: Schedule, turn: int, playing: bool,
    ) -> None:
        shown_turn = min(max(turn - 1, 0), schedule.total_turns)
        status = "PLAYING" if playing else "PAUSED"
        header = header_font.render(
            f"Turn {shown_turn}/{schedule.total_turns}  {status}", True, OUTLINE,
        )
        screen.blit(header, (18, 16))
        controls = hud_font.render(
            "SPACE play/pause   LEFT/RIGHT step   wheel=zoom   drag=pan   R=reset view",
            True, TEXT_DIM,
        )
        screen.blit(controls, (18, 48))
        if self._hovered:
            tip = hud_font.render(f"hover: {self._hovered}", True, HOVER_TEXT)
            screen.blit(tip, (18, 72))

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
