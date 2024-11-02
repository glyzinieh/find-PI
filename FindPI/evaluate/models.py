import time
from functools import wraps
from typing import Callable

from tqdm import tqdm


class Condition:
    def __init__(self, **settings):
        self.settings = settings

    def __call__(self, index: list[int], value: list[float]) -> bool:
        raise NotImplementedError


class ResultContainer:
    def __init__(
        self, index_list: list[int], value_list: list[float], time_list: list[float]
    ):
        self.index_list = index_list
        self.value_list = value_list
        self.time_list = time_list


class Runner:
    def __init__(self, name: str, params: dict, condition):
        self.name = name
        self.params = params
        self.condition = condition

        self.results: list[ResultContainer] = list()

    def __call__(self, func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            index = 1
            index_list = list()
            value_list = list()
            time_list = list()

            current_time = 0
            params = self.params

            while not self.condition(index_list, value_list):
                start_time = time.perf_counter()
                value, params = func(**params)
                current_time += time.perf_counter() - start_time
                index_list.append(index)
                value_list.append(value)
                time_list.append(current_time)
                index += 1

            self.results.append(ResultContainer(index_list, value_list, time_list))

        return wrapper

    def average_time(self):
        return sum([result.time_list[-1] for result in self.results]) / len(
            self.results
        )

    def average_count(self):
        return sum([result.index_list[-1] for result in self.results]) / len(
            self.results
        )


class HLine:
    def __init__(self, value: float, name: str):
        self.value = value
        self.name = name


class Comparer:
    def __init__(self, times: int, funcs: list[Callable] = list(), hline: HLine = None):
        self.times = times
        self.funcs = funcs
        self.hline_value = hline.value if hline else None
        self.hline_name = hline.name if hline else None
        self.evaluated = False

    def run(self):
        for func in tqdm(self.funcs):
            for _ in tqdm(range(self.times), leave=False):
                func()
        self.evaluated = True

    def plot(self, type="index-value"):
        from . import plot

        if self.hline_value is None:
            raise ValueError("HLine value is not set")

        match type:
            case "index-value":
                plot.plot_value(
                    self.funcs,
                    "試行回数",
                    "値",
                    HLine(self.hline_value, self.hline_name),
                    type,
                )
            case "time-value":
                plot.plot_value(
                    self.funcs,
                    "時間",
                    "値",
                    HLine(self.hline_value, self.hline_name),
                    type,
                )
