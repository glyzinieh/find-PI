import mpmath
import pandas as pd

from .evaluate import Condition


class Times(Condition):
    def __call__(self, data: list[tuple[int, float, float]]) -> bool:
        return len(data) >= self.settings["times"]


class Digits(Condition):
    def __call__(self, data: list[tuple[int, float, float]]) -> bool:
        if len(data) < 1:
            return False
        target_digits = self.settings["digits"]
        digit = int(-mpmath.log10(abs(data[-1][2] - mpmath.pi())))
        return digit >= target_digits


class Distance(Condition):
    def __call__(self, data: list[tuple[int, float, float]]) -> bool:
        return (
            abs(data[-1][2] - data[-2][2])
            <= self.settings["threshold"]
            if len(data) >= 2
            else False
        )


class DigitsAndDistance(Condition):
    def __init__(self, **settings):
        self.digits = Digits(**settings)
        self.distance = Distance(**settings)

    def __call__(self, data: list[tuple[int, float, float]]) -> bool:
        return self.digits(data) and self.distance(data)
