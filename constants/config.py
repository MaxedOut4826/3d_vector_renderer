CELL_STATES: tuple[str, ...] = (" ", "▀", "▄", "█")

CELL_STATE_VALUE_LOOKUP: dict[str, int] = {
    cell: i for i, cell in enumerate(CELL_STATES)
}

TICKS_PER_SECOND: int = 30
TICK_LENGTH: float = 1 / TICKS_PER_SECOND

TARGET_FPS: int = 120
MAX_FPS: int = 1000


class Edge:
    inside: int = 0
    left: int = 1
    right: int = 2
    bottom: int = 4
    top: int = 8


class Ansi:
    clear_screen: str = "\x1b[2J"
    hide_cursor: str = "\x1b[?25l"
    cursor_home: str = "\x1b[H"
