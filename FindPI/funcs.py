import math
import random
from decimal import Decimal, getcontext
from math import factorial, sqrt

from .__main__ import FindPIRunner
from .math_funcs import cos, sin, tan

getcontext().prec = 1 + 1000 + 10  # 整数部 + 小数部 + 余分


@FindPIRunner("内接多角形", {"n": 3})
def incribed(n):
    value = Decimal(n) / 2 * Decimal(sqrt(2 - 2 * cos(Decimal(360) / n)))
    n += 1

    return value, {"n": n}


@FindPIRunner("外接多角形", {"n": 3})
def outcribed(n):
    value = Decimal(n) * Decimal(tan(Decimal(180) / n))
    n += 1

    return value, {"n": n}


@FindPIRunner("モンテカルロ法", {"n": 0, "in_circle": 0})
def montecarlo(n, in_circle):
    x = Decimal(random.random())
    y = Decimal(random.random())
    if x**2 + y**2 <= 1:
        in_circle += 1
    n += 1
    value = 4 * Decimal(in_circle) / n

    return value, {"n": n, "in_circle": in_circle}


@FindPIRunner("ライプニッツ級数", {"n": 0, "s": 0})
def leibniz(n, s):
    s += Decimal((-1) ** n) / (2 * n + 1)
    value = s * 4
    n += 1

    return value, {"n": n, "s": s}


@FindPIRunner("チュドノフスキーの公式", {"n": 0, "s": 0})
def chudnovsky(n, s):
    s += (
        (Decimal((-1) ** n) * Decimal(factorial(6 * n)))
        / (Decimal(factorial(3 * n)) * (Decimal(factorial(n)) ** 3))
    ) * (
        Decimal(13591409 + 545140134 * n)
        / (Decimal(640320) ** (3 * n + Decimal(3) / 2))
    )
    value = 1 / (12 * s)
    n += 1

    return value, {"n": n, "s": s}


@FindPIRunner("区分求積法", {"n": 1})
def quadrature(n):
    s = Decimal(0)
    dx = Decimal(1) / n
    x = Decimal(1) / n / 2
    for _ in range(n):
        y = Decimal(sqrt(1 - x**2))
        s += dx * y
        x += dx
    value = s * 4
    n += 1

    return value, {"n": n}


@FindPIRunner("二分法", {"x_1": 0, "x_2": 3})
def dichotomy(x_1, x_2):
    x_1 = Decimal(x_1)
    x_2 = Decimal(x_2)
    wj = (x_1 + x_2) / 2
    if Decimal(math.tan(wj)) < 1:
        x_1 = wj
    else:
        x_2 = wj
    value = wj * 4

    return value, {"x_1": x_1, "x_2": x_2}
