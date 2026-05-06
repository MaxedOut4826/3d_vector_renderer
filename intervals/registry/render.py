from ..intervals_manager import run_interval # type: ignore
from . import Renderer

run_interval(Renderer.draw_frame, 1 / Renderer.fps)