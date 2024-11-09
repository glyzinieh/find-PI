import math

from . import conditions, funcs
from .evaluate import Comparer, HLine, Runner

# 条件
DIGITS = 5
THRESHOLD = 1e-5
# CONDITION = conditions.Times(times=200000)
CONDITION = conditions.Times(times=10000)
# CONDITION = conditions.DigitsAndDistance(digits=DIGITS, threshold=THRESHOLD)


class FindPIRunner(Runner):
    def __init__(self, name: str, params: dict):
        super().__init__(name, params, CONDITION, math.pi)


if __name__ == "__main__":
    # 関数
    FUNCS = [
        funcs.incribed,
        funcs.outcribed,
        funcs.montecarlo,
        funcs.leibniz,
        # funcs.chudnovsky,
        funcs.quadrature,
        funcs.dichotomy,
    ]

    # 実行
    findPI = Comparer(1, FUNCS)
    findPI.run()

    # プロット
    # HLINE = HLine(math.pi, "math.pi")
    HLINE = None

    findPI.plot("index", "memory", "index", "memory", HLINE)