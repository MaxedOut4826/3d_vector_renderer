from typing import Self
from render_pipeline import ObjectParameters, Vector3, Vector3Math, Vertices
from objects.vertex_transformations import Vertex
from render_pipeline.camera import Camera


class Prefab:
    instances: list["ObjectInstance"] = []

    def __init__(self: Self, mesh: ObjectParameters):
        self.mesh = mesh

    def __call__(
        self: Self,
        position: Vector3 | None = None,
        rotation: Vector3 | None = None,
        size: Vector3 | None = None,
    ):
        return ObjectInstance(self, position, rotation, size)


class ObjectInstance:
    def __init__(
        self: Self,
        prefab: Prefab,
        position: Vector3 | None = None,
        rotation: Vector3 | None = None,
        size: Vector3 | None = None,
    ) -> None:
        self.prefab = prefab
        self.position = position if position else [0.0, 0.0, 0.0]
        self.rotation = rotation if rotation else [0.0, 0.0, 0.0]
        self.size = size if size else [1.0, 1.0, 1.0]

        Prefab.instances.append(self)

    """
    These methods are public to be used on the object instances for making transformations
    """

    def rotate_pitch(self: Self, angle: float) -> Self:
        self.rotation[0] += angle
        return self

    def rotate_yaw(self: Self, angle: float) -> Self:
        self.rotation[1] += angle
        return self

    def rotate_roll(self: Self, angle: float) -> Self:
        self.rotation[2] += angle
        return self

    # Shorthand for the other rotate methods
    def rotate(self: Self, rotation_vector: Vector3) -> Self:
        pitch, yaw, roll = rotation_vector

        self.rotate_yaw(yaw).rotate_pitch(pitch).rotate_roll(roll)

        return self

    def move(self: Self, offset: Vector3) -> Self:
        x0, y0, z0 = self.position
        x1, y1, z1 = offset

        self.position = [
            x0 + x1,
            y0 + y1,
            z0 + z1,
        ]

        return self

    def scale(self: Self, scalar: Vector3) -> Self:
        x0, y0, z0 = self.size
        x1, y1, z1 = scalar

        self.size = [
            x0 * x1,
            y0 * y1,
            z0 * z1,
        ]

        return self

    """
    These methods are private and for object updates only
    """

    def get_vertices(self: Self) -> Vertices:
        return self.prefab.mesh["vertices"]

    def get_transformed_vertices(self: Self) -> Vertices:
        camera_rotation_x, camera_rotation_y, camera_rotation_z = Camera.rotation
        inverted_camera_rotation = [
            -camera_rotation_x,
            -camera_rotation_y,
            -camera_rotation_z,
        ]

        position = self.position
        rotation = self.rotation
        scale = self.size

        vertices = self.get_vertices()
        transformed_vertices: Vertices = []

        for v in vertices:
            vertex = v

            vertex = Vertex.get_scaled(vertex, scale)
            vertex = Vertex.get_rotated(vertex, rotation)
            vertex = Vertex.get_translated(vertex, position)
            vertex = Vector3Math.subtract(vertex, Camera.position)
            vertex = Vertex.get_rotated(vertex, inverted_camera_rotation)

            transformed_vertices.append(vertex)

        return transformed_vertices


"""
* EXAMPLE SYNTAX
cube = Prefab({
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
! Prefab definitions may need a different naming scheme or something to clarify
"""
