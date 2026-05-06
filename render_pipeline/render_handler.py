from sys import stdout
from os import name as os, system as run, get_terminal_size as screen_size  # type: ignore
from math import floor, cos, sin, pi
from time import time
from render_pipeline.camera import Camera
from . import (
    CELL_VALUES,
    CELL_LOOKUP,
    indices,
    vertices,
    Vector3,
    Vector2,
    Vector,
)


class Renderer:
    screen_size: list[int] = []
    empty_frame_buffer: list[list[str]] = []

    frame_buffer: list[list[str]] = []
    frame: str = ""
    fps: int = 240

    angle: float = 5.5
    delta_time: float = 1 / fps
    
    cos_a: float = 0
    sin_a: float = 0
    
    @staticmethod
    def draw_pixel(x: float, y: float) -> None:
        LOCAL_CELL_VALUES = CELL_VALUES
        LOCAL_CELL_LOOKUP = CELL_LOOKUP
        buffer = Renderer.frame_buffer
        screen_size = Renderer.screen_size

        if 0 > x or 0 > y or x >= screen_size[0] or y >= screen_size[1]:
            return

        data = 1 if (y & 1) == 0 else 2
        x = int(x)
        y = int(y >> 1)
        pixel = buffer[y][x]

        bit: str = LOCAL_CELL_VALUES[data | LOCAL_CELL_LOOKUP[pixel]]

        buffer[y][x] = bit

    # Bresenham's Line Algorithm
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
        rotate_xy = Renderer.rotate_xy
        rotate_xz = Renderer.rotate_xz

        Renderer.angle += pi * Renderer.delta_time
        angle = Renderer.angle
        
        Renderer.cos_a = cos(angle)
        Renderer.sin_a = sin(angle)

        for lines in indices:
            for start, end in zip(lines, lines[1:] + lines[:1]):
                p0 = screen_project(
                    rotate_xy(
                        rotate_xz(vertices[start], angle),
                        angle,
                    )
                )

                p1 = screen_project(
                    rotate_xy(
                        rotate_xz(vertices[end], angle),
                        angle,
                    )
                )

                if not p0 or not p1:
                    continue

                Renderer.draw_line(p0[0], p0[1], p1[0], p1[1])

        buffer = Renderer.frame_buffer

        Renderer.frame = "\n".join(map("".join, buffer))

        Renderer.clear_frame()

        stdout.write(f"\x1b[H{Renderer.frame}")
        # stdout.flush()

        # * DEBUG
        delta_time = time() - now
        Renderer.delta_time = delta_time
        # Renderer.log_performance(delta_time)

    @staticmethod
    def screen_project(vertex: Vector3) -> Vector2 | None:
        offset_x, offset_y, offset_z = Vector.subtract(vertex, Camera.position)

        if offset_z <= 0.01:
            return

        screen_x, screen_y = Renderer.screen_size
        aspect_ratio = screen_x / screen_y

        return [
            floor((((offset_x / offset_z) / aspect_ratio + 1) * 0.5) * screen_x),
            floor(((1 - offset_y / offset_z) * 0.5) * screen_y),
        ]

    @staticmethod
    def rotate_xz(vertex: Vector3, angle: float) -> Vector3:
        x, y, z = vertex
        cos_a = Renderer.cos_a
        sin_a = Renderer.sin_a

        return [
            x * cos_a - z * sin_a,
            y,
            x * sin_a + z * cos_a,
        ]

    @staticmethod
    def rotate_xy(vertex: Vector3, angle: float) -> Vector3:
        x, y, z = vertex
        cos_a = Renderer.cos_a
        sin_a = Renderer.sin_a

        return [
            x * cos_a - y * sin_a,
            x * sin_a + y * cos_a,
            z,
        ]

    @staticmethod
    def clear_frame() -> None:
        screen_x, screen_y = screen_size()
        screen_y *= 2

        if Renderer.screen_size != [screen_x, screen_y]:
            Renderer.empty_frame_buffer = [[CELL_VALUES[0]] * screen_x for _ in range(screen_y // 2)]

            Renderer.screen_size = [screen_x, screen_y]

        Renderer.frame_buffer = [y.copy() for y in Renderer.empty_frame_buffer]
        
        # \x1b[2J   <-- CLEAR SCREEN ANSI

    @staticmethod
    def clear_all() -> None:
        if os == "nt":
            run("cls")
        else:
            run("clear")
            
        Renderer.clear_frame()

    @staticmethod
    def log_performance(delta_time: float) -> None:
        with open("performance_log.txt", "r+") as rpt:
            rpt.write(f"\nDT: {delta_time}s   |   FPS: {round(1 / delta_time, 2)}")


# TODO make proper delta time query
