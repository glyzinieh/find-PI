import math
import random
from math import factorial, sqrt

from .math_funcs import cos, sin, tan

from .__main__ import findPI


# @findPI.func("内接多角形", {"n": 3})
def incribed(params):
    n = params["n"]

    value = n / 2 * sqrt(2 - 2 * cos(360 / n))
    n += 1

    params["n"] = n
    return value, params


# @findPI.func("外接多角形", {"n": 3})
def outcribed(params):
    n = params["n"]

    value = n * tan(180 / n)
    n += 1

    params["n"] = n
    return value, params


@findPI.func("モンテカルロ法", {"n": 0, "in_circle": 0})
def montecarlo(params):
    n = params["n"]
    in_circle = params["in_circle"]

    x = random.random()
    y = random.random()
    if x**2 + y**2 <= 1:
        in_circle += 1
    n += 1
    value = 4 * in_circle / n

    params["n"] = n
    params["in_circle"] = in_circle
    return value, params


@findPI.func("ライプニッツ級数", {"n": 0, "s": 0})
def leibniz(params):
    n = params["n"]
    sum = params["s"]

    sum += (-1) ** n / (2 * n + 1)
    value = sum * 4
    n += 1

    params["n"] = n
    params["s"] = sum
    return value, params


@findPI.func("チュドノフスキーの公式", {"n": 0, "s": 0})
def chudnovsky(params):
    n = params["n"]
    s = params["s"]

    s += (
        ((-1) ** n * factorial(6 * n)) / ((factorial(3 * n)) * (factorial(n) ** 3))
    ) * ((13591409 + 545140134 * n) / (640320 ** (3 * n + 3 / 2)))
    value = 1 / (12 * s)
    n += 1

    params["n"] = n
    params["s"] = s
    return value, params


@findPI.func("区分求積法", {"n": 1})
def quadrature(params):
    n = params["n"]

    s = 0
    dx = 1 / n
    x = 1 / n / 2
    for _ in range(n):
        y = sqrt(1 - x**2)
        s += dx * y
        x += dx
    value = s * 4
    n += 1

    params["n"] = n
    return value, params


@findPI.func("二分法", {"x_1": 0, "x_2": 3})
def dichotomy(params):
    x_1 = params["x_1"]
    x_2 = params["x_2"]

    wj = (x_1 + x_2) / 2
    if math.tan(wj) < 1:
        x_1 = wj
    else:
        x_2 = wj
    value = wj * 4

    params["x_1"] = x_1
    params["x_2"] = x_2
    return value, params
