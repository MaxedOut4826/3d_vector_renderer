from typing import TypedDict, Callable

Vector3 = list[float]
Vector2 = list[float]

Vertices = list[Vector3]
Indices = list[list[int]]

FrameBuffer = list[list[str]]


class IntervalParameters(TypedDict):
    callback: Callable[[], None]
    interval: float
    next: float


class ObjectParameters(TypedDict):
    vertices: Vertices
    indices: Indices
