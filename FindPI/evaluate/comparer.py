from typing import Callable

from tqdm import tqdm

from . import HLine


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
        self,
        x_type: str,
        y_type: str,
        x_label: str,
        y_label: str,
        hline: HLine = None,
        mode: str = "w",
    ):
        from .. import plot

        if len(self.funcs) == 1:
            plot.plot_one_graph(
                self.funcs[0], x_type, y_type, x_label, y_label, hline, mode
            )
        else:
            plot.plot_graphs(self.funcs, x_type, y_type, x_label, y_label, hline, mode)
