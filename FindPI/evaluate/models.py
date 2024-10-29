import time
from typing import Callable


class Condition:
    def __init__(self, **settings):
        self.settings = settings

    def __call__(self, index: list[int], value: list[float]) -> bool:
        raise NotImplementedError


class Wrapper:
    def __init__(self, name: str, func: Callable, params: dict, condition: Callable):
        self.name: str = name
        self.func: Callable = func
        self.params: dict = params
        self.condition: Callable = condition

    def __call__(self):
        params = self.params.copy()
        index = 0
        index_list = list()
        value_list = list()
        time_list = list()

        start_time = time.perf_counter()

        while not self.condition(index_list, value_list):
            value, params = self.func(params)
            index_list.append(index)
            value_list.append(value)
            time_list.append(time.perf_counter() - start_time)
            index += 1

        self.index_list = index_list
        self.value_list = value_list
        self.time_list = time_list


class Comparer:
    def __init__(
        self,
        condition: Callable,
        times: int,
        funcs: list[Wrapper] = list(),
        hline: float = None,
        hline_name: str = None,
    ):
        self.condition: Callable = condition
        # self.times: int = times
        self.funcs: list[Wrapper] = funcs
        self.hline: float = hline
        self.hline_name: str = hline_name

        self.evaluated = False

    def func(self, name: str, params: dict):
        def _func(func: Callable):
            self.funcs.append(Wrapper(name, func, params, self.condition))

        return _func

    def evaluate(self):
        for func in self.funcs:
            func()
            print(
                f"【{func.name}】\n"
                f"時間: {func.time_list[-1]}\n"
                f"回数: {len(func.index_list)}\n"
                f"結果: {func.value_list[-1]}\n"
            )
        self.evaluated = True

    def plot(self):
        if not self.evaluated:
            raise Exception("You must evaluate before plotting.")

        from . import plot

        plot.index_value(self.funcs, self.hline, self.hline_name)
