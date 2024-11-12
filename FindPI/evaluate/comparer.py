import os
from typing import Callable

from tqdm import tqdm

from .runner import Runner


class Comparer:
    def __init__(self, condition: Callable):
        self.condition = condition

        self.funcs: list[Runner] = list()

        self.evaluated = False

    def func(self, name: str, init_params: dict):
        def decorator(func: Callable):
            self.funcs.append(Runner(func, name, init_params, self.condition))
            return func

        return decorator

    def run(self):
        for func in tqdm(self.funcs):
            func()
        self.evaluated = True

    def save(self, path: str):
        if not self.evaluated:
            raise ValueError("You need to run before saving.")
        for func in self.funcs:
            func.save(os.path.join(path, f"{func.name}.pkl2"))
