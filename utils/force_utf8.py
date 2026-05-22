from os import system as run  # type: ignore
import ctypes
from ctypes import wintypes


def force_utf8() -> None:
    """
    AI solution for special ASCII characters not displaying to the terminal in pypy
    """

    # UTF-8 terminal
    run("chcp 65001 > nul")

    # Enable ANSI escape sequences
    kernel32 = ctypes.windll.kernel32

    STD_OUTPUT_HANDLE = -11
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004

    handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    mode = wintypes.DWORD()
    kernel32.GetConsoleMode(handle, ctypes.byref(mode))

    kernel32.SetConsoleMode(handle, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)
    # -- End of AI code
