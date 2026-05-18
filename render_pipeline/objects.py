from math import cos, sin
from copy import deepcopy
from typing import Self
from . import ObjectParameters, Vector3, Vector

"""
TODO: Move to objects package as "objects_handler"
"""


class Object:
    objects = []

    def __init__(self: Self, mesh: ObjectParameters):
        self.mesh = mesh

    def __call__(
        self: Self,
        position: Vector3 | None = None,
        rotation: Vector3 | None = None,
        size: Vector3 | None = None,
    ):
        return ObjectInstance(self.mesh, position, rotation, size)


class ObjectInstance:
    def __init__(
        self: Self,
        object: ObjectParameters,
        position: Vector3 | None = None,
        rotation: Vector3 | None = None,
        size: Vector3 | None = None,
    ) -> None:
        self.object = deepcopy(object)
        self.position = position if position else [0, 0, 0]
        self.rotation = rotation if rotation else [0, 0, 0]
        self.size = size if size else [1, 1, 1]

        Object.objects.append(self)

    def rotate_xz(self: Self, angle: float) -> Self:
        self.rotation[0] += angle

        object_x, _, object_z = self.position
        vertices = self.object["vertices"]

        cos_a = cos(angle)
        sin_a = sin(angle)

        for i, vertex in enumerate(vertices):
            x, y, z = vertex

            vertices[i] = [
                object_x + (x - object_x) * cos_a - (z - object_z) * sin_a,
                y,
                object_z + (x - object_x) * sin_a + (z - object_z) * cos_a,
            ]

        return self

    def rotate_xy(self: Self, angle: float) -> Self:
        self.rotation[1] += angle

        object_x, object_y, _ = self.position
        vertices = self.object["vertices"]

        cos_a = cos(angle)
        sin_a = sin(angle)

        for i, vertex in enumerate(vertices):
            x, y, z = vertex

            vertices[i] = [
                object_x + (x - object_x) * cos_a - (y - object_y) * sin_a,
                object_y + (x - object_x) * sin_a + (y - object_y) * cos_a,
                z,
            ]

        return self

    def move(self: Self, offset: Vector3) -> Self:
        self.position = Vector.add(self.position, offset)

        vertices = self.object["vertices"]

        for i, vertex in enumerate(vertices):
            vertices[i] = Vector.add(vertex, offset)

        return self

    def scale(self: Self, scalar: Vector3) -> Self:
        self.scale = Vector.hadamard_product(self.size, scalar)

        vertices = self.object["vertices"]

        for i, vertex in enumerate(vertices):
            vertices[i] = Vector.hadamard_product(vertex, scalar)

        return self


"""
* EXAMPLE SYNTAX
cube = Object({
    "vertices": [
        [0.25, 0.25, 0.25],
        [-0.25, 0.25, 0.25],
        [-0.25, -0.25, 0.25],
        [0.25, -0.25, 0.25],
        [0.25, 0.25, -0.25],
        [-0.25, 0.25, -0.25],
        [-0.25, -0.25, -0.25],
        [0.25, -0.25, -0.25],
    ],
    "indices": [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [0, 4],
        [1, 5],
        [2, 6],
        [3, 7],
    ],
})

cube_instance = cube()

cube_instance.rotate_xz()
"""

"""
! Alternatively object definitions may take the geometry path and then load it instead of taking from pre-parsed file; parsing is pretty quick
! Object definitions may need a different naming scheme or something to clarify
"""
