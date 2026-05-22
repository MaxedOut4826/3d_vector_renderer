from constants.config import FLOATING_POINT_PRECISION
from . import Vector3


class Camera:
    position: Vector3 = [0, 0, -16]
    rotation: Vector3 = [0, 0, 0]

    movement_speed: float = 1
    sensitivity: float = 1

    """
    This originally used Vector3Math to calculate but i didnt like the extra abstraction
    This improves performance per action by about x6
    """

    @staticmethod
    def move(movement_vector: Vector3) -> None:

        precision = FLOATING_POINT_PRECISION
        speed = Camera.movement_speed

        position_x, position_y, position_z = Camera.position
        move_vector_x, move_vector_y, move_vector_z = movement_vector

        Camera.position = [
            round(position_x + move_vector_x * speed, precision),
            round(position_y + move_vector_y * speed, precision),
            round(position_z + move_vector_z * speed, precision),
        ]

    @staticmethod
    def rotate(rotation_vector: Vector3) -> None:
        precision = FLOATING_POINT_PRECISION
        sensitivity = Camera.sensitivity

        rotation_x, rotation_y, rotation_z = Camera.position
        rotation_vector_x, rotation_vector_y, rotation_vector_z = rotation_vector

        Camera.rotation = [
            round(rotation_x + rotation_vector_x * sensitivity, precision),
            round(rotation_y + rotation_vector_y * sensitivity, precision),
            round(rotation_z + rotation_vector_z * sensitivity, precision),
        ]
