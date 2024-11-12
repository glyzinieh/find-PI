import pickle

import pandas as pd
from mpmath import log10


class ResultContainer:
    def __init__(
        self,
        name: str,
        index_list: list[int] = None,
        time_list: list[float] = None,
        value_list: list[float] = None,
        path: str = None,
    ):
        self.name = name
        if path is not None:
            self.load(path)
        else:
            self.index_list = index_list
            self.time_list = time_list
            self.value_list = value_list

    def set_target(self, target: float):
        self.target = target

    @property
    def diff_list(self):
        return [abs(value - self.target) for value in self.value_list]

    @property
    def digit_list(self):
        return [int(-log10(diff)) if diff != 0 else None for diff in self.diff_list]

    def save(self, path: str):
        d = zip(self.index_list, self.time_list, self.value_list)
        with open(path, "wb") as f:
            pickle.dump(d, f)

    def load(self, path: str):
        with open(path, "rb") as f:
            d = pickle.load(f)
        self.index_list, self.time_list, self.value_list = map(list, zip(*d))

    def container1to2(self):
        return ResultContainer2(
            self.name, list(zip(self.index_list, self.time_list, self.value_list))
        )


class ResultContainer2:
    def __init__(self, name: str, data: list[tuple[int, float, float]]):
        self.name = name
        self.df = pd.DataFrame(data, columns=["index", "time", "value"])

    def set_target(self, target: float):
        self.target = target

    def save(self, path: str):
        with open(path, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, path: str) -> "ResultContainer2":
        with open(path, "rb") as f:
            return pickle.load(f)

    def get_column(self, name: str):
        if name in self.df.columns:
            return self.df[name]
        match name:
            case "diff":
                return self.df["value"].diff().abs()
            case "digit":
                return self.df["value"].apply(
                    lambda x: int(-log10(abs(x - self.target))) if x != 0 else None
                )
