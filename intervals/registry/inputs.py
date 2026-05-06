from constants.my_types import Vector3
from ..intervals_manager import run_interval  # type: ignore
from . import Camera, TICK_LENGTH

run_interval(Camera.listen_for_input, TICK_LENGTH)
