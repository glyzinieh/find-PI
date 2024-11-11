import time
from typing import Callable

from .condition import Condition
from .container import ResultContainer


class Runner:
    def __init__(
        self, func: Callable, name: str, init_params: dict, condition: Condition
    ):
        self.func = func
        self.name = name
        self.init_params = init_params
        self.condition = condition

        self.result: ResultContainer = None

    def __call__(self):
        index_list = list()
        time_list = list()
        value_list = list()

        index = 1
        current_time = 0
        params = self.init_params

        while not self.condition(index_list, time_list, value_list):
            start_time = time.perf_counter()
            value, params = self.func(**params)
            current_time += time.perf_counter() - start_time
            index_list.append(index)
            time_list.append(current_time)
            value_list.append(value)
            index += 1

        self.result = ResultContainer(self.name, index_list, time_list, value_list)

    def save(self, path: str):
        if self.result is None:
            raise ValueError("You need to run before saving.")
        self.result.save(path)
