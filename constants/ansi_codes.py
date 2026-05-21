class Ansi:
    clear_screen: str = "\x1b[2J"
    hide_cursor: str = "\x1b[?25l"
    cursor_home: str = "\x1b[H"