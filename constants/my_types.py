from typing import TypedDict, Callable

Vector3 = list[int | float]
Vector2 = list[int | float]


class IntervalParameters(TypedDict):
    callback: Callable[[], None]
    interval: float
    next: float


class ObjectParameters(TypedDict):
    vertices: list[Vector3]
    indices: list[list[int]]
