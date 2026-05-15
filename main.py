from sys import stdout
import assets.index  # type: ignore
import intervals.index  # type: ignore
from intervals.intervals_manager import schedule_intervals
from render_pipeline.render_handler import Renderer


def main() -> None:
    stdout.write("\x1b[?25l")
    Renderer.clear_all()
    schedule_intervals()


if __name__ == "__main__":
    main()
