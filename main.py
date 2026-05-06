from sys import stdout
import intervals.index # type: ignore
from intervals.intervals_manager import call_intervals
from render_pipeline.render_handler import Renderer

def main() -> None:
    stdout.write("\x1B[?25l")
    Renderer.clear_all()    
    call_intervals()

if __name__ == "__main__":
    main()
