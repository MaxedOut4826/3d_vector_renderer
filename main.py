from sys import stdout
from os import system as run  # type: ignore
import objects.index  # type: ignore
import intervals.index  # type: ignore
from constants.ansi_codes import Ansi
from render_pipeline.render_handler import Renderer
from intervals.intervals_manager import schedule_intervals
from utils.force_utf8 import force_utf8


def main() -> None:
    """
    Forcing UTF-8 allows the special ASCII characters to show in the renderer for certain environments like pypy
    """
    force_utf8()

    stdout.write(f"{Ansi.hide_cursor}")

    Renderer.get_screen_size()
    Renderer.clear_all()

    schedule_intervals()


if __name__ == "__main__":
    main()
