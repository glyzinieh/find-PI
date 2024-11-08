import math
import random
from math import factorial

import gmpy2

from .__main__ import FindPIRunner
from .math_funcs import cos, sin, tan


@FindPIRunner("内接多角形", {"n": 3})
def incribed(n):
    value = gmpy2.mpfr(n) / 2 * gmpy2.mpfr(gmpy2.sqrt(2 - 2 * cos(gmpy2.mpfr(360) / n)))
    n += 1

    return value, {"n": n}


@FindPIRunner("外接多角形", {"n": 3})
def outcribed(n):
    value = gmpy2.mpfr(n) * gmpy2.mpfr(tan(gmpy2.mpfr(180) / n))
    n += 1

    return value, {"n": n}


@FindPIRunner("モンテカルロ法", {"n": 0, "in_circle": 0})
def montecarlo(n, in_circle):
    x = gmpy2.mpfr(random.random())
    y = gmpy2.mpfr(random.random())
    if x**2 + y**2 <= 1:
        in_circle += 1
    n += 1
    value = 4 * gmpy2.mpfr(in_circle) / n

    return value, {"n": n, "in_circle": in_circle}


@FindPIRunner("ライプニッツ級数", {"n": 0, "s": 0})
def leibniz(n, s):
    s += gmpy2.mpfr((-1) ** n) / (2 * n + 1)
    value = s * 4
    n += 1

    return value, {"n": n, "s": s}


@FindPIRunner("チュドノフスキーの公式", {"n": 0, "s": 0})
def chudnovsky(n, s):
    s += (
        (gmpy2.mpfr((-1) ** n) * gmpy2.mpfr(factorial(6 * n)))
        / (gmpy2.mpfr(factorial(3 * n)) * (gmpy2.mpfr(factorial(n)) ** 3))
    ) * (
        gmpy2.mpfr(13591409 + 545140134 * n)
        / (gmpy2.mpfr(640320) ** (3 * n + gmpy2.mpfr(3) / 2))
    )
    value = 1 / (12 * s)
    n += 1

    return value, {"n": n, "s": s}


@FindPIRunner("区分求積法", {"n": 1})
def quadrature(n):
    s = gmpy2.mpfr(0)
    dx = gmpy2.mpfr(1) / n
    x = gmpy2.mpfr(1) / n / 2
    for _ in range(n):
        y = gmpy2.mpfr(gmpy2.sqrt(1 - x**2))
        s += dx * y
        x += dx
    value = s * 4
    n += 1

    return value, {"n": n}


@FindPIRunner("二分法", {"x_1": 0, "x_2": 3})
def dichotomy(x_1, x_2):
    x_1 = gmpy2.mpfr(x_1)
    x_2 = gmpy2.mpfr(x_2)
    wj = (x_1 + x_2) / 2
    if gmpy2.mpfr(math.tan(wj)) < 1:
        x_1 = wj
    else:
        x_2 = wj
    value = wj * 4

    return value, {"x_1": x_1, "x_2": x_2}
