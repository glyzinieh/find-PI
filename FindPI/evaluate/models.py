import time
import tracemalloc
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
        self,
        index_list: list[int],
        value_list: list[float],
        time_list: list[float],
        memory_list: list[int],
    ):
        self.index_list = index_list
        self.value_list = value_list
        self.time_list = time_list
        self.memory_list = memory_list


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
            memory_list = list()

            current_time = 0
            params = self.params

            while not self.condition(index_list, value_list):
                tracemalloc.start()
                start_time = time.perf_counter()
                value, params = func(**params)
                current_time += time.perf_counter() - start_time
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                tracemalloc.clear_traces()
                index_list.append(index)
                value_list.append(value)
                time_list.append(current_time)
                memory_list.append(current)
                index += 1

            self.results.append(
                ResultContainer(index_list, value_list, time_list, memory_list)
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


class HLine:
    def __init__(self, value: float, name: str):
        self.value = value
        self.name = name


class Comparer:
    def __init__(self, times: int, funcs: list[Callable] = list()):
        self.times = times
        self.funcs = funcs
        self.evaluated = False

    def run(self):
        for func in tqdm(self.funcs):
            for _ in tqdm(range(self.times), leave=False):
                func()
        self.evaluated = True

    def plot(
        self, x_type: str, y_type: str, x_label: str, y_label: str, hline: HLine = None
    ):
        from . import plot

        if len(self.funcs) == 1:
            plot.plot_one_graph(self.funcs[0], x_type, y_type, x_label, y_label, hline)
        else:
            plot.plot_graphs(self.funcs, x_type, y_type, x_label, y_label, hline)
