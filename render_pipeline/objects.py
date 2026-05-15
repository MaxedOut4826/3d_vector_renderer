from math import cos, sin
from typing import Self
from . import ObjectParameters, Vector3


class Object:
    objects: list[ObjectParameters]

    def __init__(self: Self, mesh: ObjectParameters):
        self.mesh = mesh

    def __call__(self: Self, position: Vector3, rotation: Vector3):
        return ObjectInstance(self, position, rotation)


class ObjectInstance:
    def __init__(
        self: Self,
        object: Object,
        position: Vector3 = [0, 0, 0],
        rotation: Vector3 = [0, 0, 0],
        scale: Vector3 = [1, 1, 1],
    ) -> None:
        self.object = object
        self.position = position
        self.rotation = rotation
        self.scale = scale

    def rotate_xz(self: Self) -> None:  #! Object
        x, y, z = self.position
        rotation = self.rotation

        cos_a = cos(rotation)
        sin_a = cos(rotation)

        return [
            x * cos_a - z * sin_a,
            y,
            x * sin_a + z * cos_a,
        ]

    def rotate_xy(self) -> None:  #! Object
        x, y, z = self.position
        rotation = self.rotation

        cos_a = cos(rotation)
        sin_a = sin(rotation)

        return [
            x * cos_a - y * sin_a,
            x * sin_a + y * cos_a,
            z,
        ]

    def update_vertices(vertices: list[Vector3]) -> list[Vector3]:  #! Object
        return [Renderer.rotate_xy(Renderer.rotate_xz(vertex)) for vertex in vertices]

"""
* EXAMPLE SYNTAX
cube = Object(geometry)

cube_instance = cube([0, 0, 0], [0, 0, 0])

cube_instance.rotate_xy()
"""

"""
! Alternatively object definitions may take the geometry path and then load it instead of taking from pre-parsed file; parsing is pretty quick
! Object definitions may need a different naming scheme or something to clarify

TODO: Must fix all methods and references
"""