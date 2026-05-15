from time import sleep, time
from typing import Callable
from constants.my_types import IntervalParameters

intervals: list[IntervalParameters] = []


def run_interval(callback: Callable, interval: float) -> None:  # type: ignore
    intervals.append(
        {"callback": callback, "interval": interval, "next": time()}  # type: ignore
    )


def schedule_intervals() -> None:
    while True:
        now = time()

        for interval in intervals:  # type: ignore
            if now < interval["next"]:
                continue

            interval["callback"]()
            interval["next"] += interval["interval"]

        sleep(0.001)
