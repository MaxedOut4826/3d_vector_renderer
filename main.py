import sys
from os import system
from io import TextIOWrapper

##########
# import assets.index  # type: ignore
import objects.index  # type: ignore
import intervals.index  # type: ignore
from constants.config import Ansi
from intervals.intervals_manager import schedule_intervals
from render_pipeline.render_handler import Renderer


def main() -> None:
    system("chcp 65001 > nul")

    sys.stdout = TextIOWrapper(
        sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True
    )

    sys.stdout.write(f"{Ansi.hide_cursor}")
    Renderer.clear_all()
    schedule_intervals()


if __name__ == "__main__":
    main()
