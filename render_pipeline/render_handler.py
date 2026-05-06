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
    clear: list[list[str]] = []

    frame_buffer: list[list[str]] = []
    frame: str = ""
    fps: int = 240

    angle: float = 5.5
    delta_time: float = 1 / fps

    @staticmethod
    def draw_pixel(x: float, y: float) -> None:
        buffer = Renderer.frame_buffer
        screen_size = Renderer.screen_size

        if 0 > x or 0 > y or x >= screen_size[0] or y >= screen_size[1]:
            return

        data = 1 if (y & 1) == 0 else 2
        x = int(x)
        y = int(y >> 1)
        pixel = buffer[y][x]

        bit: str = CELL_VALUES[data | CELL_LOOKUP[pixel]]

        buffer[y][x] = bit

    # Bresenham's Line Algorithm
    @staticmethod
    def draw_line(x0: float, y0: float, x1: float, y1: float) -> None:
        dx: float = abs(x1 - x0)
        dy: float = abs(y1 - y0)

        sx: int = 1 if x0 < x1 else -1
        sy: int = 1 if y0 < y1 else -1

        err: float = dx - dy

        while True:
            Renderer.draw_pixel(x0, y0)

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

        for lines in indices:
            for start, end in zip(lines, lines[1:] + lines[:1]):
                p0 = screen_project(
                    rotate_xy(
                        rotate_xz(vertices[start], angle + 90),
                        angle,
                    )
                )

                p1 = screen_project(
                    rotate_xy(
                        rotate_xz(vertices[end], angle + 90),
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
        stdout.flush()
        
        #* DEBUG 
        delta_time = time() - now
        Renderer.delta_time = delta_time
        Renderer.performance_report(delta_time)

    @staticmethod
    def screen_project(vertex: Vector3) -> Vector2 | None:
        screen_x, screen_y = Renderer.screen_size
        offset_x, offset_y, offset_z = Vector.subtract(vertex, Camera.position)

        if offset_z <= 0.01:
            return

        aspect_ratio = screen_x / screen_y

        return [
            floor((((offset_x / offset_z) / aspect_ratio + 1) * 0.5) * screen_x),
            floor(((1 - offset_y / offset_z) * 0.5) * screen_y),
        ]

    @staticmethod
    def rotate_xz(vertex: Vector3, angle: float) -> Vector3:
        x, y, z = vertex
        cos_theta = cos(angle)
        sin_theta = sin(angle)

        return [
            x * cos_theta - z * sin_theta,
            y,
            x * sin_theta + z * cos_theta,
        ]

    @staticmethod
    def rotate_xy(vertex: Vector3, angle: float) -> Vector3:
        x, y, z = vertex
        cos_theta = cos(angle)
        sin_theta = sin(angle)

        return [
            x * cos_theta - y * sin_theta,
            x * sin_theta + y * cos_theta,
            z,
        ]

    @staticmethod
    def clear_frame() -> None:
        screen_x, screen_y = [screen_size()[0], screen_size()[1] * 2]
        
        if Renderer.screen_size != [screen_x, screen_y * 2]:
            Renderer.clear = [
                [CELL_VALUES[0]] * screen_x
                for _ in range(screen_y // 2)
            ]
            
            Renderer.screen_size = [screen_x, screen_y]
        
        Renderer.frame_buffer = Renderer.clear

        # if os == "nt":
        #     run("cls")
        # else:
        #     run("clear")

        # stdout.write("\x1b[2J")

    @staticmethod
    def performance_report(delta_time: float) -> None:
        with open("performance_report.txt", "r+") as rpt:
            rpt.write(f"\nDT: {delta_time}s   |   FPS: {(1 / delta_time):.2f}")
        

# TODO make proper delta time query
