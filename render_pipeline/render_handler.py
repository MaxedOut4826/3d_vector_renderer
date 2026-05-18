from sys import stdout
from os import name as os, system as run, get_terminal_size as screen_size  # type: ignore
from math import floor
from time import time
from render_pipeline.camera import Camera
from render_pipeline.objects import Object
from . import (
    CELL_VALUES,
    CELL_LOOKUP,
    TARGET_FPS,
    Edge,
    Vector3,
    Vector2,
    Vector,
)


class Renderer:
    screen_size: list[int] = []
    aspect_ratio: float = 0
    empty_frame_buffer: list[list[str]] = []

    frame_buffer: list[list[str]] = []
    frame: str = ""
    fps: float = TARGET_FPS
    delta_time: float = 1 / fps

    # queue: list[ObjectInstance] = Object.objects

    @staticmethod
    def draw_pixel(x: float, y: float) -> None:
        buffer = Renderer.frame_buffer

        y = int(y)
        data = 1 if (y & 1) == 0 else 2

        x = int(x)
        y >>= 1

        pixel = buffer[y][x]
        bit: str = CELL_VALUES[data | CELL_LOOKUP[pixel]]
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
        now: float = time()

        screen_project = Renderer.screen_project
        edge_clip = Renderer.edge_clip
        near_clip = Renderer.near_clip

        # pi * 0.1 * Renderer.delta_time

        for object in Object.objects:
            mesh = object.object
            vertices = mesh["vertices"]
            indices = mesh["indices"]

            for lines in indices:
                v0 = vertices[lines[0]]

                for index in (lines[1:] + lines[:1]) if len(lines) > 2 else lines[1:]:
                    v1 = vertices[index]

                    clipped = near_clip(v0, v1)

                    if not clipped:
                        v0 = v1
                        continue

                    c0_3d, c1_3d = clipped

                    clipping_points = edge_clip(
                        screen_project(c0_3d), screen_project(c1_3d)  # type: ignore
                    )

                    if clipping_points:
                        c0, c1 = clipping_points
                        Renderer.draw_line(c0[0], c0[1], c1[0], c1[1])

                    v0 = v1

        buffer = Renderer.frame_buffer

        Renderer.frame = "\n".join(map("".join, buffer))

        Renderer.clear_frame()

        stdout.write(f"\x1b[H{Renderer.frame}")

        # ? DEBUG
        delta_time = time() - now
        Renderer.delta_time = delta_time
        Renderer.fps = round(1 / delta_time)

        # Renderer.log_performance(delta_time)
        # stdout.write(f"\nDT: {delta_time}s   |   FPS: {Renderer.fps}")

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

        x0, y0 = p0
        x1, y1 = p1

        p0_clip = Renderer.point_is_clipping(p0)
        p1_clip = Renderer.point_is_clipping(p1)

        while True:
            # Check if neither points are out of bounds
            if not (p0_clip or p1_clip):
                return [int(x0), int(y0)], [int(x1), int(y1)]

            # Check if both points are out of bounds
            if p0_clip & p1_clip:
                return

            # Only one point is out of bounds; perform the algorithm
            x: float = 0
            y: float = 0

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

            if clipping_point is p0_clip:
                x0, y0 = [x, y]
                p0_clip = Renderer.point_is_clipping([x0, y0])
                continue

            x1, y1 = [x, y]
            p1_clip = Renderer.point_is_clipping([x1, y1])

    # 3D Modified version of the Cohen Sutherland Algorithm
    @staticmethod
    def near_clip(p0: Vector3, p1: Vector3) -> tuple[Vector3, Vector3] | None:
        NEAR_SCREEN_CUTOFF_THRESHOLD: float = 0.01

        dz0 = p0[2] - Camera.position[2]
        dz1 = p1[2] - Camera.position[2]

        inside0 = dz0 > NEAR_SCREEN_CUTOFF_THRESHOLD
        inside1 = dz1 > NEAR_SCREEN_CUTOFF_THRESHOLD

        if not inside0 and not inside1:
            return

        if inside0 and inside1:
            return p0, p1

        t = (NEAR_SCREEN_CUTOFF_THRESHOLD - dz0) / (dz1 - dz0)

        intersection = [
            p0[0] + (p1[0] - p0[0]) * t,
            p0[1] + (p1[1] - p0[1]) * t,
            p0[2] + (p1[2] - p0[2]) * t,
        ]

        if inside0:
            return p0, intersection

        return intersection, p1

    @staticmethod
    def screen_project(vertex: Vector3) -> Vector2 | None:
        offset_x, offset_y, offset_z = Vector.subtract(vertex, Camera.position)
        screen_x, screen_y = Renderer.screen_size

        return [
            floor(
                (((offset_x / offset_z) / Renderer.aspect_ratio + 1) * 0.5)
                * (screen_x - 1)
            ),
            floor(((1 - offset_y / offset_z) * 0.5) * (screen_y - 1)),
        ]

    @staticmethod
    def clear_frame() -> None:
        screen_x, screen_y = screen_size()
        screen_y <<= 1

        if Renderer.screen_size != [screen_x, screen_y]:
            Renderer.empty_frame_buffer = [
                [CELL_VALUES[0]] * screen_x for _ in range(screen_y >> 1)
            ]

            Renderer.screen_size = [screen_x, screen_y]
            Renderer.aspect_ratio = screen_x / screen_y

        Renderer.frame_buffer = [y.copy() for y in Renderer.empty_frame_buffer]

        # \x1b[2J   <-- CLEAR SCREEN ANSI

    @staticmethod
    def clear_all() -> None:
        if os == "nt":
            run("cls")
        else:
            run("clear")

        Renderer.clear_frame()

    # @staticmethod
    # def push_object_to_queue(object: ObjectParameters) -> None:  #! Object
    #     Renderer.queue.append(object)

    @staticmethod
    def log_performance(delta_time: float) -> None:  #! Move to util?
        with open("performance_log.txt", "r+") as rpt:
            rpt.write(f"\nDT: {delta_time}s   |   FPS: {Renderer.fps, 2}")


"""
TODO: store rotation per object
? Each object may be an instance of the class where the address gets pushed to a list as an iterable
"""
