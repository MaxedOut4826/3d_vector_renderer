from sys import stdout
import intervals.index # type: ignore
from intervals.intervals_manager import call_intervals
from render_pipeline.render_handler import Renderer

def main() -> None:
    stdout.write("\x1b[?25l\x1b[2J")
    
    Renderer.clear_frame()
    
    call_intervals()

if __name__ == "__main__":
    main()
