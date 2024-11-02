import math

from tqdm import tqdm

from . import conditions, funcs
from .evaluate import Comparer, HLine, Runner

# 条件
DIGITS = 5
THRESHOLD = 1e-5
CONDITION = conditions.DigitsAndDistance(digits=DIGITS, threshold=THRESHOLD)


class FindPIRunner(Runner):
    def __init__(self, name: str, params: dict):
        super().__init__(name, params, CONDITION)


if __name__ == "__main__":
    # 試行回数
    TIMES = 3

    # 関数
    FUNCS = [
        funcs.incribed,
        funcs.outcribed,
        funcs.montecarlo,
        funcs.leibniz,
        funcs.chudnovsky,
        funcs.quadrature,
        funcs.dichotomy,
    ]

    findPI = Comparer(TIMES, FUNCS, HLine(math.pi, "π"))
    findPI.run()
    findPI.plot(type="time-value")
