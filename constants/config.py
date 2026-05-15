CELL_VALUES: tuple[str, ...] = (" ", "▀", "▄", "█")

CELL_LOOKUP: dict[str, int] = {
    cell: i for i, cell in enumerate(CELL_VALUES)
}

TICKS_PER_SECOND: int = 30
TICK_LENGTH: float = 1 / TICKS_PER_SECOND

TARGET_FPS: float = 240

class Edge:
    inside: int = 0
    left: int = 1
    right: int = 2
    bottom: int = 4
    top: int = 8