from math import cos, sin
from typing import Self
from . import ObjectParameters, Vector3


class Object:
    objects: list[ObjectInstance]

    def __init__(self: Self, mesh: ObjectParameters):
        self.mesh = mesh

    def __call__(
        self: Self,
        position: Vector3 = [0, 0, 0],
        rotation: Vector3 = [0, 0, 0],
        scale: Vector3 = [1, 1, 1],
    ):
        return ObjectInstance(self.mesh, position, rotation, scale)


class ObjectInstance:
    def __init__(
        self: Self,
        object: ObjectParameters,
        position: Vector3 = [0, 0, 0],
        rotation: Vector3 = [0, 0, 0],
        scale: Vector3 = [1, 1, 1],
    ) -> None:
        self.object = object
        self.position = position
        self.rotation = rotation
        self.scale = scale
        
        Object.objects.append(self)

    def rotate_xz(self: Self, angle: float) -> None:
        self.rotation[0] += angle
        
        vertices = self.object["vertices"]
        xrot = self.rotation[0]

        cos_a = cos(xrot)
        sin_a = sin(xrot)

        for i, vertex in enumerate(vertices):
            x, y, z = vertex

            vertices[i] = [
                x * cos_a - y * sin_a,
                x * sin_a + y * cos_a,
                z
            ]

    def rotate_xy(self: Self, angle: float) -> None:
        self.rotation[1] += angle
        
        vertices = self.object["vertices"]
        yrot = self.rotation[1]

        cos_a = cos(yrot)
        sin_a = sin(yrot)

        for i, vertex in enumerate(vertices):
            x, y, z = vertex

            vertices[i] = [
                x * cos_a - y * sin_a,
                x * sin_a + y * cos_a,
                z
            ]


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