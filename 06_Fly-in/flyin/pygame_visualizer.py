"""Interactive Pygame visualisation of a completed schedule.

Supports pan (left-click drag) and zoom (mouse wheel) so that maps with
many zones (e.g. the "Impossible Dream" challenge map) can be inspected
without labels overlapping. Zone labels are truncated to fit their grid
cell and hidden entirely when zoomed out past legibility; hovering a
zone always shows its full name.

Drones glide continuously between zones (every schedule turn is animated
over ``TURN_DELAY_MS``) and leave a fading trail that shows the route they
have flown so far. Zone colours come from the map's ``color=`` attribute
when the model exposes it, softened into a consistent palette.
"""

from __future__ import annotations

import colorsys
import math
from dataclasses import dataclass, field

import pygame

from .models import FlightMap, Zone
from .schedule import Move, Schedule

RGB = tuple[int, int, int]
Point = tuple[float, float]

BACKGROUND = (8, 11, 18)
GRID_LINE = (70, 82, 104)
OUTLINE = (235, 240, 250)
TEXT_DIM = (160, 174, 198)
HOVER_RING = (255, 214, 10)
HOVER_TEXT = (255, 230, 120)
PRIORITY_RING = (251, 191, 36)

CELL = 100.0          # world-space pixels between adjacent grid coordinates
BASE_RADIUS = 25.0    # world-space node radius at zoom == 1
MIN_ZOOM = 0.15
MAX_ZOOM = 4.0
LABEL_ZOOM_THRESHOLD = 0.45  # below this zoom, per-node labels are hidden
MIN_FONT_PX = 10
ZOOM_STEP = 1.15

# --- Animation ------------------------------------------------------------
TURN_DELAY_MS = 700   # how long one schedule turn takes on screen
EASE_BLEND = 0.5      # 0 = constant speed, 1 = full smoothstep (stop & go)
DOCK_SHRINK_START = 0.6  # delivered drones shrink away after this progress

# --- Trails ---------------------------------------------------------------
TRAIL_ALPHA_MIN = 40    # oldest part of the trail (0-255)
TRAIL_ALPHA_MAX = 210   # part of the trail closest to the drone (0-255)
TRAIL_MAX_WAYPOINTS = 0  # 0 = keep the whole route, N = only the last N zones

# --- Glow -----------------------------------------------------------------
GLOW_SCALE = 1.8
GLOW_STEPS = 10
GLOW_CACHE_LIMIT = 400
ZONE_GLOW_ALPHA = 70
DRONE_GLOW_ALPHA = 95

ZONE_DEFAULTS: dict[str, RGB] = {
    "start_hub": (56, 189, 248),
    "end_hub": (52, 211, 153),
    "priority": (251, 191, 36),
    "restricted": (167, 139, 250),
    "blocked": (100, 116, 139),
    "normal": (96, 165, 250),
}

DRONE_COLORS: tuple[RGB, ...] = (
    (168, 85, 247), (239, 93, 168), (85, 168, 255), (33, 199, 168),
    (246, 196, 83), (251, 113, 133), (163, 230, 53), (251, 146, 60),
    (129, 140, 248), (34, 211, 238),
)


def _mix(a: RGB, b: RGB, amount: float) -> RGB:
    """Blend ``a`` towards ``b``; ``amount`` 0 gives ``a``, 1 gives ``b``."""
    amount = min(max(amount, 0.0), 1.0)
    return (
        round(a[0] + (b[0] - a[0]) * amount),
        round(a[1] + (b[1] - a[1]) * amount),
        round(a[2] + (b[2] - a[2]) * amount),
    )


@dataclass
class _Playback:
    """Logical state of the replay plus what the animation needs."""

    positions: dict[int, str] = field(default_factory=dict)
    transits: dict[int, tuple[str, str, int, int]] = field(
        default_factory=dict
    )
    delivered: set[int] = field(default_factory=set)
    # Drones that reached the end zone during the last applied turn.
    newly_delivered: set[int] = field(default_factory=set)
    # Drones whose trail got a new waypoint during the last applied turn.
    pending: set[int] = field(default_factory=set)
    # Zone centres each drone has visited, in order (world space).
    waypoints: dict[int, list[Point]] = field(default_factory=dict)
    # World-space point of every drone before / after the last applied turn.
    prev_points: dict[int, Point] = field(default_factory=dict)
    curr_points: dict[int, Point] = field(default_factory=dict)
    applied: int = 0


class PygameVisualizer:
    """Replay a schedule in a Pygame window."""

    def __init__(self, width: int = 1100, height: int = 700) -> None:
        self.width = width
        self.height = height
        self.zoom = 1.0
        self.cam_x = 0.0
        self.cam_y = 0.0
        self._font_cache: dict[int, pygame.font.Font] = {}
        self._glow_cache: dict[tuple[RGB, int, int], pygame.Surface] = {}
        self._zone_colors: dict[str, RGB] = {}
        self._dragging = False
        self._drag_anchor: tuple[int, int] = (0, 0)
        self._drag_cam_anchor: tuple[float, float] = (0.0, 0.0)
        self._hovered: str | None = None
        self._show_trails = True

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
        self._glow_cache = {}
        header_font = self._get_font(24)
        hud_font = self._get_font(16)
        hover_font = self._get_font(20)

        flight_map = schedule.flight_map
        world_points = self._build_world_layout(flight_map.zones)
        self._fit_camera(world_points)
        self._zone_colors = {
            name: self._zone_color(name, flight_map)
            for name in flight_map.zones
        }
        grouped = schedule.moves_by_turn()

        playback = self._replay(0, grouped, flight_map, world_points)

        # ``turn`` is the next turn to apply; the state on screen is the
        # result of turns 1 .. turn-1, animated over TURN_DELAY_MS.
        turn = 1
        playing = True
        anim_ms = 0.0
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
                        if turn <= schedule.total_turns:
                            self._advance(
                                playback, turn, grouped, flight_map,
                                world_points,
                            )
                            turn += 1
                            anim_ms = 0.0
                    elif event.key == pygame.K_LEFT:
                        turn = max(1, turn - 1)
                        playback = self._replay(
                            turn - 1, grouped, flight_map, world_points
                        )
                        anim_ms = float(TURN_DELAY_MS)
                    elif event.key == pygame.K_t:
                        self._show_trails = not self._show_trails
                    elif event.key == pygame.K_r:
                        self._fit_camera(world_points)

                elif event.type == pygame.MOUSEWHEEL:
                    mouse_pos = pygame.mouse.get_pos()
                    world_under_mouse = self._screen_to_world(mouse_pos)
                    factor = ZOOM_STEP if event.y > 0 else (1 / ZOOM_STEP)
                    self.zoom = min(
                        MAX_ZOOM, max(MIN_ZOOM, self.zoom * factor)
                    )
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

            # The animation of the last applied turn always runs to the end,
            # even when paused. Pausing only stops *new* turns from starting.
            anim_ms = min(anim_ms + delta, float(TURN_DELAY_MS))
            if (
                playing
                and turn <= schedule.total_turns
                and anim_ms >= TURN_DELAY_MS
            ):
                self._advance(
                    playback, turn, grouped, flight_map, world_points
                )
                turn += 1
                anim_ms = 0.0

            progress = min(anim_ms / TURN_DELAY_MS, 1.0)
            eased = self._ease(progress)
            delivered_visible = len(playback.delivered) - (
                len(playback.newly_delivered) if progress < 1.0 else 0
            )

            self._hovered = self._find_hovered_zone(world_points)
            occupancy = self._occupancy(playback.positions)

            screen.fill(BACKGROUND)
            self._draw_connections(screen, flight_map, world_points)
            if self._show_trails:
                self._draw_trails(screen, playback, progress, eased)
            self._draw_zones(
                screen, flight_map, world_points, occupancy, delivered_visible,
            )
            self._draw_zone_labels(
                screen, flight_map, world_points, hover_font
            )
            self._draw_drones(screen, playback, progress, eased)
            self._draw_hud(
                screen, header_font, hud_font, schedule, turn, playing,
                delivered_visible,
            )

            pygame.display.flip()

        pygame.quit()

    # ------------------------------------------------------------------ #
    # Turn logic
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
    # Playback state / animation
    # ------------------------------------------------------------------ #

    def _new_playback(
        self, flight_map: FlightMap,
        world_points: dict[str, tuple[float, float]],
    ) -> _Playback:
        playback = _Playback(
            positions={
                drone: flight_map.start
                for drone in range(1, flight_map.nb_drones + 1)
            },
        )
        start_center = world_points[flight_map.start]
        for drone in playback.positions:
            playback.waypoints[drone] = [start_center]
        playback.curr_points = self._logical_points(
            flight_map, world_points, playback
        )
        playback.prev_points = dict(playback.curr_points)
        return playback

    def _replay(
        self, upto: int, grouped: dict[int, list[tuple[int, Move]]],
        flight_map: FlightMap, world_points: dict[str, tuple[float, float]],
    ) -> _Playback:
        """Rebuild the state after turns 1..upto, without any animation."""
        playback = self._new_playback(flight_map, world_points)
        for replay_turn in range(1, upto + 1):
            self._advance(
                playback, replay_turn, grouped, flight_map, world_points
            )
        playback.prev_points = dict(playback.curr_points)
        playback.newly_delivered = set()
        playback.pending = set()
        return playback

    def _advance(
        self, playback: _Playback, turn: int,
        grouped: dict[int, list[tuple[int, Move]]], flight_map: FlightMap,
        world_points: dict[str, tuple[float, float]],
    ) -> None:
        """Apply one turn and remember where every drone was and will be."""
        playback.prev_points = dict(playback.curr_points)
        before = set(playback.delivered)
        self._apply_turn(
            turn, grouped, playback.positions, playback.transits,
            playback.delivered, flight_map.start, flight_map.end,
        )
        playback.applied = turn
        playback.newly_delivered = playback.delivered - before
        playback.curr_points = self._logical_points(
            flight_map, world_points, playback
        )
        self._extend_trails(playback, flight_map, world_points)

    def _logical_points(
        self, flight_map: FlightMap,
        world_points: dict[str, tuple[float, float]], playback: _Playback,
    ) -> dict[int, Point]:
        """World-space point each drone occupies in the current state."""
        occupancy = self._occupancy(playback.positions)
        nb_drones = flight_map.nb_drones
        points: dict[int, Point] = {}
        for drone in range(1, nb_drones + 1):
            if drone in playback.positions:
                points[drone] = self._seat_point(
                    drone, playback.positions[drone], occupancy, nb_drones,
                    world_points,
                )
            elif drone in playback.transits:
                source, destination, departure, arrival = (
                    playback.transits[drone]
                )
                duration = max(arrival - departure, 1)
                fraction = (playback.applied - departure + 1) / (duration + 1)
                fraction = min(max(fraction, 0.0), 1.0)
                sx, sy = world_points[source]
                ex, ey = world_points[destination]
                points[drone] = (sx + (ex - sx) * fraction,
                                 sy + (ey - sy) * fraction)
            elif drone in playback.delivered:
                points[drone] = world_points[flight_map.end]
            else:
                points[drone] = world_points[flight_map.start]
        return points

    def _seat_point(
        self, drone: int, zone_name: str, occupancy: dict[str, int],
        nb_drones: int, world_points: dict[str, tuple[float, float]],
    ) -> Point:
        """Where a parked drone sits around its zone centre (world space)."""
        cx, cy = world_points[zone_name]
        angle = drone * math.tau / max(nb_drones, 1)
        orbit = min(12 + occupancy.get(zone_name, 0) * 2, 18)
        return cx + math.cos(angle) * orbit, cy + math.sin(angle) * orbit

    def _extend_trails(
        self, playback: _Playback, flight_map: FlightMap,
        world_points: dict[str, tuple[float, float]],
    ) -> None:
        """Add the zone each drone just reached to its trail."""
        playback.pending = set()
        end_center = world_points[flight_map.end]
        for drone, path in playback.waypoints.items():
            zone_name = playback.positions.get(drone)
            if zone_name is not None:
                center = world_points[zone_name]
            elif drone in playback.newly_delivered:
                center = end_center
            else:
                continue  # in transit, or already delivered
            if center == path[-1]:
                continue
            path.append(center)
            playback.pending.add(drone)
            if TRAIL_MAX_WAYPOINTS and len(path) > TRAIL_MAX_WAYPOINTS:
                del path[:-TRAIL_MAX_WAYPOINTS]

    @staticmethod
    def _ease(progress: float) -> float:
        """Mostly-linear motion with a gentle ease-in/ease-out."""
        progress = min(max(progress, 0.0), 1.0)
        smooth = progress * progress * (3.0 - 2.0 * progress)
        return progress + (smooth - progress) * EASE_BLEND

    @staticmethod
    def _display_point(playback: _Playback, drone: int, eased: float) -> Point:
        end = playback.curr_points[drone]
        start = playback.prev_points.get(drone, end)
        return (
            start[0] + (end[0] - start[0]) * eased,
            start[1] + (end[1] - start[1]) * eased,
        )

    # ------------------------------------------------------------------ #
    # Camera / layout
    # ------------------------------------------------------------------ #

    def _build_world_layout(
        self, zones: dict[str, Zone]
    ) -> dict[str, tuple[float, float]]:
        return {
            name: (zone.x * CELL, zone.y * CELL)
            for name, zone in zones.items()
        }

    def _fit_camera(
        self, world_points: dict[str, tuple[float, float]]
    ) -> None:
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

    def _get_font(self, size: float) -> pygame.font.Font:
        px = max(MIN_FONT_PX, round(size))
        font = self._font_cache.get(px)
        if font is None:
            font = pygame.font.Font(None, px)
            self._font_cache[px] = font
        return font

    def _fit_text(
        self, text: str, font: pygame.font.Font, max_width: int
    ) -> str:
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
        plate = pygame.Surface(
            (rect.width + pad * 2, rect.height + pad * 2),
            pygame.SRCALPHA,
        )
        plate.fill((*BACKGROUND, 185))
        screen.blit(plate, (rect.x - pad, rect.y - pad))
        screen.blit(label, rect)

    def _glow_sprite(
        self, color: RGB, radius: int, alpha: int
    ) -> pygame.Surface:
        """Soft round halo, cached because it is reused every frame."""
        radius = max(2, radius)
        key = (color, radius, alpha)
        sprite = self._glow_cache.get(key)
        if sprite is not None:
            return sprite
        if len(self._glow_cache) >= GLOW_CACHE_LIMIT:
            self._glow_cache.clear()
        sprite = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        # Biggest (faintest) circle first, each smaller one is more opaque.
        for step in range(GLOW_STEPS):
            ring_radius = max(1, round(radius * (1.0 - step / GLOW_STEPS)))
            strength = int(alpha * ((step + 1) / GLOW_STEPS) ** 2)
            pygame.draw.circle(
                sprite, (*color, strength), (radius, radius), ring_radius
            )
        self._glow_cache[key] = sprite
        return sprite

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

    def _draw_trails(
        self, screen: pygame.Surface, playback: _Playback,
        progress: float, eased: float,
    ) -> None:
        """Draw each drone's route so far, fading towards the oldest part."""
        width = max(2, round(4 * self.zoom))
        settled = progress >= 1.0
        for drone, waypoints in playback.waypoints.items():
            hidden = (
                drone in playback.delivered
                and drone not in playback.newly_delivered
            )
            docked = drone in playback.newly_delivered and settled
            path = list(waypoints)
            if not settled and drone in playback.pending:
                # The newest waypoint is where the drone is *heading*: the
                # line must stop at the drone, not run ahead of it.
                path = path[:-1]
            points = [self._world_to_screen(*p) for p in path]
            if not hidden and not docked:
                tip = self._display_point(playback, drone, eased)
                points.append(self._world_to_screen(*tip))
            if len(points) < 2:
                continue
            color = DRONE_COLORS[(drone - 1) % len(DRONE_COLORS)]
            self._draw_fading_path(screen, points, color, width)

    def _draw_fading_path(
        self, screen: pygame.Surface, points: list[tuple[int, int]],
        color: RGB, width: int,
    ) -> None:
        segments = len(points) - 1
        joint = max(1, width // 2)
        for index in range(segments):
            strength = TRAIL_ALPHA_MIN + (
                (TRAIL_ALPHA_MAX - TRAIL_ALPHA_MIN) * (index + 1) / segments
            )
            shade = _mix(BACKGROUND, color, strength / 255)
            pygame.draw.line(
                screen, shade, points[index], points[index + 1], width
            )
            pygame.draw.circle(screen, shade, points[index + 1], joint)

    def _draw_zones(
        self, screen: pygame.Surface, flight_map: FlightMap,
        world_points: dict[str, tuple[float, float]],
        occupancy: dict[str, int],
        delivered_visible: int,
    ) -> None:
        radius = max(3, round(BASE_RADIUS * self.zoom))
        ring_width = max(2, round(3 * self.zoom))
        outer_gap = max(3, round(6 * self.zoom))
        badge_font = self._get_font(18 * self.zoom)
        for zone_name, zone in flight_map.zones.items():
            x, y = self._world_to_screen(*world_points[zone_name])
            color = self._zone_colors.get(zone_name) or self._zone_color(
                zone_name, flight_map
            )
            kind = self._zone_kind(zone)

            if radius >= 8:
                glow = self._glow_sprite(
                    color, round(radius * GLOW_SCALE), ZONE_GLOW_ALPHA
                )
                screen.blit(glow, glow.get_rect(center=(x, y)))

            # Dark tinted body + bright ring: neon look, and drones stay
            # easy to see on top of it.
            pygame.draw.circle(
                screen, _mix(BACKGROUND, color, 0.22), (x, y), radius
            )
            if kind == "restricted" and radius >= 10:
                self._draw_dashed_ring(
                    screen, color, (x, y), radius, ring_width
                )
            else:
                pygame.draw.circle(screen, color, (x, y), radius, ring_width)

            if kind in ("start_hub", "end_hub"):
                pygame.draw.circle(
                    screen, color, (x, y), radius + outer_gap, 1
                )
            elif kind == "priority":
                pygame.draw.circle(
                    screen, PRIORITY_RING, (x, y), radius + outer_gap, 1
                )
            elif kind == "blocked":
                reach = round(radius * 0.45)
                pygame.draw.line(
                    screen,
                    color,
                    (x - reach, y - reach),
                    (x + reach, y + reach),
                    ring_width,
                )
                pygame.draw.line(
                    screen,
                    color,
                    (x - reach, y + reach),
                    (x + reach, y - reach),
                    ring_width,
                )

            if zone_name == self._hovered:
                pygame.draw.circle(
                    screen, HOVER_RING, (x, y), radius + outer_gap + 2, 3
                )

            count = (
                delivered_visible if kind == "end_hub"
                else occupancy.get(zone_name, 0)
            )
            if count:
                badge = badge_font.render(str(count), True, OUTLINE)
                screen.blit(badge, badge.get_rect(center=(x, y)))

    def _draw_dashed_ring(
        self, screen: pygame.Surface, color: RGB, center: tuple[int, int],
        radius: int, width: int,
    ) -> None:
        rect = pygame.Rect(0, 0, radius * 2, radius * 2)
        rect.center = center
        dashes = 14
        step = math.tau / dashes
        for index in range(dashes):
            start = index * step
            pygame.draw.arc(
                screen, color, rect, start, start + step * 0.6, width
            )

    def _draw_zone_labels(
        self, screen: pygame.Surface, flight_map: FlightMap,
        world_points: dict[str, tuple[float, float]],
        hover_font: pygame.font.Font,
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
        self, screen: pygame.Surface, playback: _Playback,
        progress: float, eased: float,
    ) -> None:
        drone_font = self._get_font(22 * self.zoom)
        for drone in sorted(playback.curr_points):
            if (
                drone in playback.delivered
                and drone not in playback.newly_delivered
            ):
                continue  # already home, nothing left to draw
            scale = 1.0
            if drone in playback.newly_delivered:
                # Docking: shrink away once the drone reaches the end zone.
                shrink = (
                    (progress - DOCK_SHRINK_START)
                    / (1.0 - DOCK_SHRINK_START)
                )
                scale = 1.0 - min(max(shrink, 0.0), 1.0)
                if scale <= 0.0:
                    continue
            wx, wy = self._display_point(playback, drone, eased)
            x, y = self._world_to_screen(wx, wy)
            self._draw_single_drone(screen, drone_font, drone, x, y, scale)

    def _draw_single_drone(
        self, screen: pygame.Surface, font: pygame.font.Font,
        drone: int, x: int, y: int, scale: float = 1.0,
    ) -> None:
        color = DRONE_COLORS[(drone - 1) % len(DRONE_COLORS)]
        radius = max(1, round(max(4, round(10 * self.zoom)) * scale))
        if radius >= 5:
            glow = self._glow_sprite(
                color, round(radius * 2.2), DRONE_GLOW_ALPHA
            )
            screen.blit(glow, glow.get_rect(center=(x, y)))
        pygame.draw.circle(screen, color, (x, y), radius)
        pygame.draw.circle(
            screen,
            BACKGROUND,
            (x, y),
            radius,
            max(1, round(2 * self.zoom)),
        )
        if self.zoom > 0.5 and scale > 0.8:
            label = font.render(str(drone), True, (255, 255, 255))
            screen.blit(label, label.get_rect(center=(x, y)))

    def _draw_hud(
        self, screen: pygame.Surface, header_font: pygame.font.Font,
        hud_font: pygame.font.Font,
        schedule: Schedule,
        turn: int,
        playing: bool,
        delivered: int,
    ) -> None:
        shown_turn = min(max(turn - 1, 0), schedule.total_turns)
        status = "PLAYING" if playing else "PAUSED"
        header = header_font.render(
            f"Turn {shown_turn}/{schedule.total_turns}  {status}",
            True,
            OUTLINE,
        )
        screen.blit(header, (18, 16))
        controls = hud_font.render(
            "SPACE play/pause   LEFT/RIGHT step   T trails   "
            "wheel=zoom   drag=pan   R=reset view",
            True, TEXT_DIM,
        )
        screen.blit(controls, (18, 48))
        arrived = hud_font.render(
            f"Delivered {delivered}/{schedule.flight_map.nb_drones}",
            True, TEXT_DIM,
        )
        screen.blit(arrived, (18, 72))
        if self._hovered:
            tip = hud_font.render(f"hover: {self._hovered}", True, HOVER_TEXT)
            screen.blit(tip, (18, 96))

    # ------------------------------------------------------------------ #
    # Colours
    # ------------------------------------------------------------------ #

    @staticmethod
    def _zone_kind(zone: Zone) -> str:
        if zone.is_start:
            return "start_hub"
        if zone.is_end:
            return "end_hub"
        return str(zone.zone_type.value)

    @staticmethod
    def _parse_color(value: object) -> RGB | None:
        """Turn a map colour name ("gold", "darkred", "#ffcc00") into RGB."""
        if not isinstance(value, str) or not value:
            return None
        try:
            parsed = pygame.Color(value)
        except (ValueError, TypeError):
            return None  # e.g. "rainbow" is not a real colour name
        return parsed.r, parsed.g, parsed.b

    @staticmethod
    def _soften(color: RGB) -> RGB:
        """Pull harsh CSS colours into one pleasant, consistent palette."""
        r, g, b = (channel / 255 for channel in color)
        hue, lightness, saturation = colorsys.rgb_to_hls(r, g, b)
        if saturation < 0.1:
            # black / gray / white: keep it neutral, with a slight cool tint
            hue, saturation = 0.62, 0.14
            lightness = min(max(lightness, 0.38), 0.72)
        else:
            saturation = min(max(saturation, 0.5), 0.85)
            lightness = min(max(lightness, 0.5), 0.66)
        red, green, blue = colorsys.hls_to_rgb(hue, lightness, saturation)
        return round(red * 255), round(green * 255), round(blue * 255)

    def _zone_color(
        self, zone_name: str, flight_map: FlightMap
    ) -> tuple[int, int, int]:
        zone = flight_map.zone(zone_name)
        custom = self._parse_color(getattr(zone, "color", None))
        if custom is not None:
            return self._soften(custom)
        return ZONE_DEFAULTS.get(
            self._zone_kind(zone), ZONE_DEFAULTS["normal"]
        )
