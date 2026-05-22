CELL_STATES: tuple[str, ...] = (" ", "▀", "▄", "█")

CELL_STATE_VALUE_LOOKUP: dict[str, int] = {
    cell: i for i, cell in enumerate(CELL_STATES)
}

TICKS_PER_SECOND: int = 30
TICK_LENGTH: float = 1 / TICKS_PER_SECOND

MAX_FPS: int = 60

FLOATING_POINT_PRECISION: int = 4
