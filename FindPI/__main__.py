import math

from . import conditions
from .evaluate import Comparer

DIGITS = 10
THRESHOLD = 1e-10
CONDITION = conditions.DigitsAndDistance(digits=DIGITS, threshold=THRESHOLD)
TIMES = 5

findPI = Comparer(CONDITION, TIMES, hline=math.pi, hline_name="π")

if __name__ == "__main__":
    from . import funcs

    findPI.evaluate()
    findPI.plot()
