CELL_VALUES: tuple[str, ...] = (" ", "▀", "▄", "█")

CELL_LOOKUP: dict[str, int] = {
    cell: i for i, cell in enumerate(CELL_VALUES)
}

TICKS_PER_SECOND = 30
TICK_LENGTH = 1 / TICKS_PER_SECOND