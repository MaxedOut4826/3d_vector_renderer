from typing import TypedDict, Callable
from utils.vector3 import Vector3

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
