from math import sqrt
from constants.my_types import Vector2, Vector3


class Vector:
    @staticmethod
    def add(vector1: Vector2 | Vector3, vector2: Vector2 | Vector3) -> Vector2 | Vector3:
        result: Vector2 | Vector3 = []

        for p0, p1 in zip(vector1, vector2):
            result.append(p0 + p1)

        return result

    @staticmethod
    def subtract(vector1: Vector2 | Vector3, vector2: Vector2 | Vector3) -> Vector2 | Vector3:
        result: Vector2 | Vector3 = []

        for p0, p1 in zip(vector1, vector2):
            result.append(p0 - p1)

        return result

    @staticmethod
    def multiply(vector: Vector2 | Vector3, scalar: float) -> Vector2 | Vector3:
        return [p * scalar for p in vector]

    @staticmethod
    def hadamard_product(vector: Vector2 | Vector3, scalar: Vector2 | Vector3) -> Vector2 | Vector3:
        return [p * s for p, s in zip(vector, scalar)]

    @staticmethod
    def normalise(vector: Vector2 | Vector3, scalar: float) -> Vector2 | Vector3:
        return [p / scalar for p in vector]

    @staticmethod
    # TODO Adapt to both 2d and 3d
    def distance_sqr(vector1: Vector3, vector2: Vector3) -> float:
        dx, dy, dz = Vector.subtract(vector1, vector2)
        return dx * dx + dy * dy + dz * dz

    @staticmethod
    def distance(vector1: Vector3, vector2: Vector3) -> float:
        return sqrt(Vector.distance_sqr(vector1, vector2))

    @staticmethod
    def lerp(vector1: Vector2 | Vector3, vector2: Vector2 | Vector3, t: float):
        return Vector.add(
            vector1,
            Vector.multiply(Vector.subtract(vector2, vector1), t),
        )

    @staticmethod
    def get_lowest_vector(vector1: Vector2 | Vector3, vector2: Vector2 | Vector3):
        result: Vector2 | Vector3 = []

        for p0, p1 in zip(vector1, vector2):
            result.append(min(p0, p1))

        return result

    @staticmethod
    def get_highest_vector(vector1: Vector2 | Vector3, vector2: Vector2 | Vector3):
        result: Vector2 | Vector3 = []

        for p0, p1 in zip(vector1, vector2):
            result.append(max(p0, p1))

        return result

    @staticmethod
    # TODO: add vector2 compatability and/or make separate Vector2 class to handle 2d vector math
    def to_string(vector: Vector3):
        return f"{vector[0]}, {vector[1]}, {vector[2]}"

    @staticmethod
    def round(vector: Vector2 | Vector3, precision: int):
        return [round(p, precision) for p in vector]
