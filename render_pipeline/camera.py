from msvcrt import kbhit, getch
from . import inputs, Vector, Vector3


class Camera:
    position: Vector3 = [0, 0, -16]
    movement_speed: float = 1

    @staticmethod
    def listen_for_input() -> None:
        if not kbhit():
            return

        key: bytes = getch()

        if not key in inputs:
            return

        Camera.position = Vector.round(
            Vector.add(
                Camera.position, Vector.multiply(inputs[key], Camera.movement_speed)
            ),
            4,
        )
