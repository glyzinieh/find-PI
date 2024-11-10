import math

from .evaluate import Condition


class Times(Condition):
    def __call__(
        self, index_list: list[int], time_list: list[float], value_list: list[float]
    ) -> bool:
        return len(index_list) >= self.settings["times"]


class Digits(Condition):
    def __call__(
        self, index_list: list[int], time_list: list[float], value_list: list[float]
    ) -> bool:
        return (
            str(value_list[-1])[: self.settings["digits"] + 1]
            == str(math.pi)[: self.settings["digits"] + 1]
            if len(value_list) >= 1
            else False
        )


class Distance(Condition):
    def __call__(
        self, index_list: list[int], time_list: list[float], value_list: list[float]
    ) -> bool:
        return (
            abs(value_list[-1] - value_list[-2]) <= self.settings["threshold"]
            if len(value_list) >= 2
            else False
        )


class DigitsAndDistance(Condition):
    def __init__(self, **settings):
        self.digits = Digits(**settings)
        self.distance = Distance(**settings)

    def __call__(
        self, index_list: list[int], time_list: list[float], value_list: list[float]
    ) -> bool:
        return self.digits(index_list, time_list, value_list) and self.distance(
            index_list, time_list, value_list
        )
