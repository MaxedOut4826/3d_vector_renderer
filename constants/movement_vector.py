from constants.my_types import Vector3

class MovementVector:
    forward: Vector3 = [0, 0, 1]
    backward: Vector3 = [0, 0, -1]
    right: Vector3 = [1, 0, 0]
    left: Vector3 = [-1, 0, 0]
    up: Vector3 = [0, 1, 0]
    down: Vector3 = [0, -1, 0]
