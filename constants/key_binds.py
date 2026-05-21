from typing import Callable  # type: ignore
from constants.movement_vector import MovementVector
from constants.rotation_vector import RotationVector
from render_pipeline.camera import Camera

KEY_BINDS: dict[bytes, Callable[[], None]] = {
    b"w": lambda: Camera.move(MovementVector.forward),
    b"s": lambda: Camera.move(MovementVector.backward),
    b"d": lambda: Camera.move(MovementVector.right),
    b"a": lambda: Camera.move(MovementVector.left),
    b" ": lambda: Camera.move(MovementVector.up),
    b"c": lambda: Camera.move(MovementVector.down),
    b"l": lambda: Camera.rotate(RotationVector.yaw_right),
    b"j": lambda: Camera.rotate(RotationVector.yaw_left),
    b"i": lambda: Camera.rotate(RotationVector.pitch_up),
    b"k": lambda: Camera.rotate(RotationVector.pitch_down),
}
