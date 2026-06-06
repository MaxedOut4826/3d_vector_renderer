from time import sleep, time
from typing import Callable
from constants.my_types import IntervalParameters

intervals: list[IntervalParameters] = []


def run_interval(callback: Callable[[], None], interval: float) -> None:
    intervals.append(
        {"callback": callback, "interval": interval, "next": time()}
    )


def schedule_intervals() -> None:
    while True:
        now = time()

        for interval in intervals:
            if now < interval["next"]:
                continue

            interval["callback"]()
            interval["next"] += interval["interval"]

        sleep(0.005)
