from intervals.intervals_manager import run_interval
from msvcrt import kbhit, getch
from . import TICK_LENGTH, KEY_BINDS


def input_handler() -> None:
    if not kbhit():
        return

    key: bytes = getch()

    if not key in KEY_BINDS:
        return

    KEY_BINDS[key]()


run_interval(input_handler, TICK_LENGTH)
