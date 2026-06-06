from math import sqrt

Vector2 = list[float]


class Vector2Utils(Vector2):
    def __new__(cls, x: float, y: float) -> Vector2:
        return [x, y]

    @staticmethod
    def add(vector1: Vector2, vector2: Vector2) -> Vector2:
        x0, y0 = vector1
        x1, y1 = vector2

        return [
            x0 + x1,
            y0 + y1,
        ]

    @staticmethod
    def subtract(vector1: Vector2, vector2: Vector2) -> Vector2:
        x0, y0 = vector1
        x1, y1 = vector2

        return [
            x0 - x1,
            y0 - y1,
        ]

    @staticmethod
    def multiply(vector: Vector2, scalar: float) -> Vector2:
        x, y = vector

        return [
            x * scalar,
            y * scalar,
        ]

    @staticmethod
    def hadamard_product(
        vector1: Vector2, vector2: Vector2
    ) -> Vector2:
        x0, y0 = vector1
        x1, y1 = vector2

        return [
            x0 * x1,
            y0 * y1,
        ]

    @staticmethod
    def normalise(vector: Vector2, scalar: float) -> Vector2:
        x0, y0 = vector

        return [
            x0 / scalar,
            y0 / scalar,
        ]

    @staticmethod
    def distance_sqr(vector1: Vector2, vector2: Vector2) -> float:
        x0, y0 = vector1
        x1, y1 = vector2

        dx = x0 - x1
        dy = y0 - y1

        return dx * dx + dy * dy

    @staticmethod
    def distance(vector1: Vector2, vector2: Vector2) -> float:
        x0, y0 = vector1
        x1, y1 = vector2

        dx = x0 - x1
        dy = y0 - y1

        return sqrt(dx * dx + dy * dy)

    @staticmethod
    def lerp(
        vector1: Vector2, vector2: Vector2, t: float
    ) -> Vector2:
        x0, y0 = vector1
        x1, y1 = vector2

        dx = x1 - x0
        dy = y1 - y0

        return [
            dx * t + x0,
            dy * t + y0,
        ]

    @staticmethod
    def get_lowest_vector(vector1: Vector2, vector2: Vector2):
        x0, y0 = vector1
        x1, y1 = vector2

        return [
            min(x0, x1),
            min(y0, y1),
        ]

    @staticmethod
    def get_highest_vector(vector1: Vector2, vector2: Vector2):
        x0, y0 = vector1
        x1, y1 = vector2

        return [
            max(x0, x1),
            max(y0, y1),
        ]

    @staticmethod
    def to_string(vector: Vector2):
        x, y = vector

        return f"{x}, {y}"

    @staticmethod
    def round(vector: Vector2, precision: int):
        x, y = vector

        return [
            round(x, precision),
            round(y, precision),
        ]
