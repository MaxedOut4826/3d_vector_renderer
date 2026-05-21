from . import Vector, Vector3


class Camera:
    position: Vector3 = [0, 0, -16]
    rotation: Vector3 = [0, 0, 0]

    movement_speed: float = 1
    sensitivity: float = 1

    @staticmethod
    def move(movement_vector: Vector3) -> None:
        Camera.position = Vector.round(
            Vector.add(
                Camera.position, Vector.multiply(movement_vector, Camera.movement_speed)
            ),
            4,
        )

    @staticmethod
    def rotate(rotation_vector: Vector3) -> None:
        Camera.rotation = Vector.round(
            Vector.add(
                Camera.rotation, Vector.multiply(rotation_vector, Camera.sensitivity)
            ),
            4,
        )
