import pandas as pd


class Condition:
    def __init__(self, **settings):
        self.settings = settings

    def __call__(self, data: list[tuple[int, float, float]]) -> bool:
        raise NotImplementedError
