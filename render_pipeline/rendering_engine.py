from sys import stdout
from os import name as os, system as run, get_terminal_size as screen_size  # type: ignore
from math import floor
from time import perf_counter
from render_pipeline.camera import Camera
from objects.objects_manager import Prefab
from . import (
    CELL_STATES,
    CELL_STATE_VALUE_LOOKUP,
    MAX_FPS,
    FrameBuffer,
    Edge,
    Ansi,
    Vector3,
    Vector2,
)


class Renderer:
    screen_size: Vector2 = []
    aspect_ratio: float = 0.0

    empty_frame_buffer: FrameBuffer = []
    frame_buffer: FrameBuffer = []
    frame: str = ""

    fps: float = MAX_FPS
    delta_time: float = 1 / fps
    last_frame_time: float = perf_counter()

    @staticmethod
    def draw_pixel(x: float, y: float) -> None:
        buffer = Renderer.frame_buffer

        y = int(y)
        # Bitmasking here with the first bit checks odd or even which is more performant than modulo by 2
        data = 1 if (y & 1) == 0 else 2

        x = int(x)
        # Shifting right one bit here is mathematically adjacent to dividing by two, but more performant
        y >>= 1

        pixel = buffer[y][x]
        bit: str = CELL_STATES[data | CELL_STATE_VALUE_LOOKUP[pixel]]
        buffer[y][x] = bit

    """
    Bresenham's Line Algorithm
    ? https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
    """

    @staticmethod
    def draw_line(x0: float, y0: float, x1: float, y1: float) -> None:
        draw_pixel = Renderer.draw_pixel

        dx: float = abs(x1 - x0)
        dy: float = abs(y1 - y0)

        sx: int = 1 if x0 < x1 else -1
        sy: int = 1 if y0 < y1 else -1

        err: float = dx - dy

        while True:
            draw_pixel(x0, y0)

            if x0 == x1 and y0 == y1:
                break

            e2 = 2 * err

            if e2 > -dy:
                err -= dy
                x0 += sx

            if e2 < dx:
                err += dx
                y0 += sy

    @staticmethod
    def draw_frame() -> None:
        # These functions and values are grabbed locally to prevent repeated external fetching for performance
        screen_project = Renderer.screen_project
        edge_clip = Renderer.edge_clip
        near_clip = Renderer.near_clip
        buffer = Renderer.frame_buffer

        total_edges = 0
        rendered_edges = 0

        for object in Prefab.instances:
            vertices = object.get_transformed_vertices()
            indices = object.prefab.mesh["indices"]

            for polygon in indices:
                p0 = vertices[polygon[0]]

                for index in (
                    (polygon[1:] + polygon[:1]) if len(polygon) > 2 else polygon[1:]
                ):
                    p1 = vertices[index]
                    total_edges += 1

                    any_clipped = near_clip(p0, p1)

                    if not any_clipped:
                        p0 = p1
                        continue

                    c0_3d, c1_3d = any_clipped

                    clipping_points = edge_clip(
                        screen_project(c0_3d), screen_project(c1_3d)
                    )

                    if clipping_points:
                        c0, c1 = clipping_points
                        Renderer.draw_line(c0[0], c0[1], c1[0], c1[1])

                        rendered_edges += 1

                    p0 = p1

        # unrendered_edges = total_edges - rendered_edges
        rendered_edges_percent = rendered_edges / total_edges * 100

        Renderer.frame = "\n".join(map("".join, buffer))
        Renderer.get_screen_size()
        Renderer.clear_frame()

        stdout.write(f"{Ansi.cursor_home}{Renderer.frame}")

        now = perf_counter()
        delta_time = now - Renderer.last_frame_time
        Renderer.delta_time = delta_time if delta_time > 0 else Renderer.delta_time
        Renderer.fps = min(floor(1 / Renderer.delta_time), MAX_FPS)
        Renderer.last_frame_time = now

        # ? DEBUG
        stdout.write(
            f"\nDT: {delta_time:.5f}s   |   FPS: {Renderer.fps:<3}|  Edges: {rendered_edges:,} / {total_edges:,} [{rendered_edges_percent:.1f}%]  |  {Camera.position}  |  {Camera.rotation}"
        )

    # Bitpacks the edges that the point overlaps to be masked later in the edge clip
    @staticmethod
    def point_is_clipping(vertex: Vector2) -> int:
        screen_x, screen_y = Renderer.screen_size
        x, y = vertex

        clip_edge: int = Edge.inside

        if x < 0:
            clip_edge |= Edge.left

        elif x >= screen_x:
            clip_edge |= Edge.right

        if y < 0:
            clip_edge |= Edge.bottom

        elif y >= screen_y:
            clip_edge |= Edge.top

        return clip_edge

    """
    Cohen Sutherland Algorithm
    ? https://en.wikipedia.org/wiki/Cohen%E2%80%93Sutherland_algorithm
    """

    @staticmethod
    def edge_clip(p0: Vector2, p1: Vector2) -> tuple[Vector2, Vector2] | None:
        screen_x, screen_y = Renderer.screen_size
        point_is_clipping = Renderer.point_is_clipping

        x0, y0 = p0
        x1, y1 = p1

        p0_clip = point_is_clipping(p0)
        p1_clip = point_is_clipping(p1)

        while True:
            # Check if neither points are out of bounds
            if not (p0_clip or p1_clip):
                return [int(x0), int(y0)], [int(x1), int(y1)]

            # Check if both points are out of bounds
            if p0_clip & p1_clip:
                return

            # Only one point is out of bounds; perform the algorithm
            x: float = 0.0
            y: float = 0.0

            # Explicit Type Annotating to stop it yapping
            x0: float
            y0: float
            x1: float
            y1: float

            clipping_point = p1_clip if p1_clip > p0_clip else p0_clip

            if clipping_point & Edge.top:
                x = x0 + (x1 - x0) * (screen_y - 1 - y0) / (y1 - y0)
                y = screen_y - 1

            elif clipping_point & Edge.bottom:
                x = x0 + (x1 - x0) * -y0 / (y1 - y0)
                y = 0

            elif clipping_point & Edge.right:
                y = y0 + (y1 - y0) * (screen_x - 1 - x0) / (x1 - x0)
                x = screen_x - 1

            elif clipping_point & Edge.left:
                y = y0 + (y1 - y0) * -x0 / (x1 - x0)
                x = 0

            if clipping_point == p0_clip:
                x0, y0 = [x, y]
                p0_clip = point_is_clipping([x0, y0])
                continue

            x1, y1 = [x, y]
            p1_clip = point_is_clipping([x1, y1])

    # 3D Modified version of the Cohen Sutherland Algorithm
    @staticmethod
    def near_clip(p0: Vector3, p1: Vector3) -> tuple[Vector3, Vector3] | None:
        NEAR_SCREEN_CUTOFF_THRESHOLD: float = 0.01

        camera_z = Camera.position[2]
        x0, y0, z0 = p0
        x1, y1, z1 = p1

        dz0 = z0 - camera_z
        dz1 = z1 - camera_z

        p0_inside = dz0 > NEAR_SCREEN_CUTOFF_THRESHOLD
        p1_inside = dz1 > NEAR_SCREEN_CUTOFF_THRESHOLD

        if not p0_inside and not p1_inside:
            return

        if p0_inside and p1_inside:
            return p0, p1

        t = (NEAR_SCREEN_CUTOFF_THRESHOLD - dz0) / (dz1 - dz0)

        intersection = [
            x0 + (x1 - x0) * t,
            y0 + (y1 - y0) * t,
            z0 + (z1 - z0) * t,
        ]

        if p0_inside:
            return p0, intersection

        return intersection, p1

    @staticmethod
    def screen_project(vertex: Vector3) -> Vector2:
        screen_x, screen_y = Renderer.screen_size

        x0, y0, z0 = vertex
        x1, y1, z1 = Camera.position

        offset_x = x0 - x1
        offset_y = y0 - y1
        offset_z = z0 - z1

        return [
            floor(
                (((offset_x / offset_z) / Renderer.aspect_ratio + 1) * 0.5)
                * (screen_x - 1)
            ),
            floor(((1 - offset_y / offset_z) * 0.5) * (screen_y - 1)),
        ]

    @staticmethod
    def get_screen_size() -> None:
        screen_x, screen_y_standard = screen_size()
        screen_y_standard -= (
            1  # Temporary fix for screen drifting when logging debug info
        )
        screen_y = screen_y_standard << 1
        """
        Shifting left one bit here is mathematically adjacent to multiplying by two, but more performant
        We do this because each character represents two pixels vertically to achieve a higher resolution
        """

        if Renderer.screen_size == [screen_x, screen_y]:
            return

        Renderer._build_empty_frame_buffer(screen_x, screen_y_standard)

        Renderer.screen_size = [screen_x, screen_y]
        Renderer.aspect_ratio = screen_x / screen_y

        Renderer.clear_all()

    @staticmethod
    def _build_empty_frame_buffer(screen_x: int, screen_y: int) -> None:
        Renderer.empty_frame_buffer = [
            [CELL_STATES[0]] * screen_x for _ in range(screen_y)
        ]

    @staticmethod
    def clear_frame() -> None:
        Renderer.frame_buffer = [y.copy() for y in Renderer.empty_frame_buffer]

    @staticmethod
    def clear_all() -> None:
        if os == "nt":
            run("cls")
        else:
            run("clear")

        Renderer.clear_frame()
