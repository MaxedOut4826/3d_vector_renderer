from math import sqrt

Vector3 = list[float]


class Vector3Math(Vector3):
    def __new__(cls, x: float, y: float, z: float) -> Vector3:
        return [x, y, z]

    @staticmethod
    def add(vector1: Vector3, vector2: Vector3) -> Vector3:
        x0, y0, z0 = vector1
        x1, y1, z1 = vector2

        return [
            x0 + x1,
            y0 + y1,
            z0 + z1,
        ]

    @staticmethod
    def subtract(vector1: Vector3, vector2: Vector3) -> Vector3:
        x0, y0, z0 = vector1
        x1, y1, z1 = vector2

        return [
            x0 - x1,
            y0 - y1,
            z0 - z1,
        ]

    @staticmethod
    def multiply(vector: Vector3, scalar: float) -> Vector3:
        x, y, z = vector

        return [
            x * scalar,
            y * scalar,
            z * scalar,
        ]

    @staticmethod
    def hadamard_product(vector1: Vector3, vector2: Vector3) -> Vector3:
        x0, y0, z0 = vector1
        x1, y1, z1 = vector2

        return [
            x0 * x1,
            y0 * y1,
            z0 * z1,
        ]

    @staticmethod
    def normalise(vector: Vector3, scalar: float) -> Vector3:
        x0, y0, z0 = vector

        return [
            x0 / scalar,
            y0 / scalar,
            z0 / scalar,
        ]

    @staticmethod
    def distance_sqr(vector1: Vector3, vector2: Vector3) -> float:
        x0, y0, z0 = vector1
        x1, y1, z1 = vector2

        dx = x0 - x1
        dy = y0 - y1
        dz = z0 - z1

        return dx * dx + dy * dy + dz * dz

    @staticmethod
    def distance(vector1: Vector3, vector2: Vector3) -> float:
        x0, y0, z0 = vector1
        x1, y1, z1 = vector2

        dx = x0 - x1
        dy = y0 - y1
        dz = z0 - z1

        return sqrt(dx * dx + dy * dy + dz * dz)

    @staticmethod
    def lerp(vector1: Vector3, vector2: Vector3, t: float) -> Vector3:
        x0, y0, z0 = vector1
        x1, y1, z1 = vector2

        dx = x1 - x0
        dy = y1 - y0
        dz = z1 - z0

        return [
            dx * t + x0,
            dy * t + y0,
            dz * t + z0,
        ]

    @staticmethod
    def get_lowest_vector(vector1: Vector3, vector2: Vector3):
        x0, y0, z0 = vector1
        x1, y1, z1 = vector2

        return [
            min(x0, x1),
            min(y0, y1),
            min(z0, z1),
        ]

    @staticmethod
    def get_highest_vector(vector1: Vector3, vector2: Vector3):
        x0, y0, z0 = vector1
        x1, y1, z1 = vector2

        return [
            max(x0, x1),
            max(y0, y1),
            max(z0, z1),
        ]

    @staticmethod
    def to_string(vector: Vector3):
        x, y, z = vector

        return f"{x}, {y}, {z}"

    @staticmethod
    def round(vector: Vector3, precision: int):
        x, y, z = vector

        return [
            round(x, precision),
            round(y, precision),
            round(z, precision),
        ]
