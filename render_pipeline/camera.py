from constants.config import FLOATING_POINT_PRECISION
from objects.vertex_transformations import Vertex
from . import Vector3


class Camera:
    position: Vector3 = [0, 0, -16]
    rotation: Vector3 = [0, 0, 0]

    movement_speed: float = 1
    sensitivity: float = 10

    """
    This originally used Vector3Utils to calculate but i didnt like the extra abstraction
    This improves performance per action by about x6
    """

    @staticmethod
    def move(movement_vector: Vector3) -> None:
        precision = FLOATING_POINT_PRECISION
        speed = Camera.movement_speed

        position_x, position_y, position_z = Camera.position
        dx, dy, dz = Vertex.get_rotated(movement_vector, Camera.rotation)

        Camera.position = [
            round(position_x + dx * speed, precision),
            round(position_y + dy * speed, precision),
            round(position_z + dz * speed, precision),
        ]

    @staticmethod
    def rotate(rotation_vector: Vector3) -> None:
        precision = FLOATING_POINT_PRECISION
        sensitivity = Camera.sensitivity / 360

        rotation_x, rotation_y, rotation_z = Camera.rotation
        rotation_vector_x, rotation_vector_y, rotation_vector_z = rotation_vector

        Camera.rotation = [
            round(rotation_x + rotation_vector_x * sensitivity, precision),
            round(rotation_y + rotation_vector_y * sensitivity, precision),
            round(rotation_z + rotation_vector_z * sensitivity, precision),
        ]
