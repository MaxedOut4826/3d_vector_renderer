from time import sleep, time
from timeit import timeit
from typing import Callable
intervals = []

def run_interval(callback: Callable, interval: float ) -> None: # type: ignore
    intervals.append({ # type: ignore
        "callback": callback,
        "interval": interval,
        "next": time()
    })

def call_intervals() -> None:
    while True:
        now = time()
        
        for interval in intervals: # type: ignore
            if now < interval["next"]: continue
            
            interval["callback"]()
            interval["next"] += interval["interval"]
    
        sleep(0.001)
        
