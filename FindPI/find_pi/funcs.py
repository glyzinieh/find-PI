import math
import random
from math import factorial, sqrt

from .utils import cos, sin, tan


# 内接多角形
def incribed(judge_func):
    index_list = list()
    value_list = list()
    index = 1
    n = 3
    while not judge_func(value_list):
        value = n / 2 * sqrt(2 - 2 * cos(360 / n))
        index_list.append(index)
        value_list.append(value)
        index += 1
        n += 1

    return index_list, value_list


# 外接多角形
def outcribed(judge_func):
    index_list = list()
    value_list = list()
    index = 1
    n = 3
    while not judge_func(value_list):
        value = n * tan(180 / n)
        index_list.append(index)
        value_list.append(value)
        index += 1
        n += 1

    return index_list, value_list


# モンテカルロ法
def monte_carlo(judge_func):
    index_list = list()
    value_list = list()
    index = 1
    n = 0
    in_circle = 0
    while not judge_func(value_list):
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1:
            in_circle += 1
        n += 1
        value = 4 * in_circle / n
        index_list.append(index)
        value_list.append(value)
        index += 1

    return index_list, value_list


# ライプニッツの公式
def leibniz(judge_func):
    index_list = list()
    value_list = list()
    index = 1
    value = 0
    n = 1
    while not judge_func(value_list):
        if index % 2 != 0:
            value += 1 / n
        else:
            value -= 1 / n
        index_list.append(index)
        value_list.append(value * 4)
        index += 1
        n += 2

    return index_list, value_list


# チュドノフスキーの公式
def chudnovsky(judge_func):
    index_list = list()
    value_list = list()
    index = 1
    n = 0
    s = 0
    while not judge_func(value_list):
        s += (
            ((-1) ** n * factorial(6 * n)) / ((factorial(3 * n)) * (factorial(n) ** 3))
        ) * ((13591409 + 545140134 * n) / (640320 ** (3 * n + 3 / 2)))
        value = 1 / (12 * s)
        index_list.append(index)
        value_list.append(value)
        index += 1
        n += 1

    return index_list, value_list


# 区分求積法
def quadrature(judge_func):
    index_list = list()
    value_list = list()
    n = 1
    while not judge_func(value_list):
        s = 0
        dx = 1 / n
        x = 1 / n / 2
        for _ in range(n):
            y = sqrt(1 - x**2)
            s += dx * y
            x += dx
        index_list.append(n)
        value_list.append(s * 4)
        n += 1

    return index_list, value_list


# 二分法
def dichotomy(judge_func):
    index_list = list()
    value_list = list()
    index = 1
    x_1 = 0
    x_2 = 3
    while not judge_func(value_list):
        wj = (x_1 + x_2) / 2
        if math.tan(wj) < 1:
            x_1 = wj
        else:
            x_2 = wj
        index_list.append(index)
        value_list.append(wj * 4)
        index += 1

    return index_list, value_list
