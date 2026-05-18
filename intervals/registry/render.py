from ..intervals_manager import run_interval  # type: ignore
from . import Renderer, MAX_FPS

run_interval(Renderer.draw_frame, min(1 / Renderer.fps, MAX_FPS))
