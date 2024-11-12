import time
from typing import Callable

from .condition import Condition
from .container import ResultContainer2


class Runner:
    def __init__(
        self, func: Callable, name: str, init_params: dict, condition: Condition
    ):
        self.func = func
        self.name = name
        self.init_params = init_params
        self.condition = condition

        self.result: ResultContainer2 = None

    def __call__(self):
        result: list[tuple[int, float, float]] = list()

        index = 1
        current_time = 0
        params = self.init_params

        while not self.condition(result):
            start_time = time.perf_counter()
            value, params = self.func(**params)
            current_time += time.perf_counter() - start_time
            result.append((index, current_time, value))
            index += 1

        self.result = ResultContainer2(self.name, result)

    def save(self, path: str):
        if self.result is None:
            raise ValueError("You need to run before saving.")
        self.result.save(path)
