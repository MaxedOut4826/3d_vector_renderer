from constants.my_types import Vector3

class RotationVector:
    pitch_down: Vector3 = [1, 0, 0]
    pitch_up: Vector3 = [-1, 0, 0]
    yaw_right: Vector3 = [0, 1, 0]
    yaw_left: Vector3 = [0, -1, 0]
    roll_clockwise: Vector3 = [0, 0, 1]
    roll_counter: Vector3 = [0, 0, -1]
