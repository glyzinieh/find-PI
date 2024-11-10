import time
from functools import wraps
from typing import Callable

import gmpy2

from . import Condition, ResultContainer


class Runner:
    def __init__(
        self, name: str, params: dict, condition: Condition, true_value: float
    ):
        self.name = name
        self.params = params
        self.condition = condition
        self.true_value = gmpy2.mpfr(true_value)

        self.results: list[ResultContainer] = list()

    def __call__(self, func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            index = 1
            index_list = list()
            value_list = list()
            time_list = list()
            diff_list = list()

            current_time = 0
            params = self.params

            while not self.condition(index_list, value_list):
                start_time = time.perf_counter()
                value, params = func(**params)
                current_time += time.perf_counter() - start_time
                index_list.append(index)
                value_list.append(value)
                time_list.append(current_time)
                diff_list.append(abs(value - self.true_value))
                index += 1

            self.results.append(
                ResultContainer(index_list, value_list, time_list, diff_list)
            )

        return wrapper

    def average_time(self):
        return sum([result.time_list[-1] for result in self.results]) / len(
            self.results
        )

    def average_count(self):
        return sum([result.index_list[-1] for result in self.results]) / len(
            self.results
        )
