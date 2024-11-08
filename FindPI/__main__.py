import math

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

    # 実行
    findPI = Comparer(1, FUNCS)
    findPI.run()

    # プロット
    X_TYPE = "index"
    Y_TYPE = "value"
    HLINE = HLine(math.pi, "math.pi")

    findPI.plot(X_TYPE, Y_TYPE, "index", "value", HLINE)
