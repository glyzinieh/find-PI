import math

from .evaluate import Condition


class Times(Condition):
    def __call__(self, index: list[int], value: list[float]) -> bool:
        return len(index) >= self.settings["times"]


class Digits(Condition):
    def __call__(self, index: list[int], value: list[float]) -> bool:
        return (
            str(value[-1])[: self.settings["digits"] + 1]
            == str(math.pi)[: self.settings["digits"] + 1]
            if len(value) >= 1
            else False
        )


class Distance(Condition):
    def __call__(self, index: list[int], value: list[float]) -> bool:
        return (
            abs(value[-1] - value[-2]) <= self.settings["threshold"]
            if len(value) >= 2
            else False
        )


class DigitsAndDistance(Condition):
    def __init__(self, **settings):
        self.digits = Digits(**settings)
        self.distance = Distance(**settings)

    def __call__(self, index: list[int], value: list[float]) -> bool:
        return self.digits(index, value) and self.distance(index, value)
