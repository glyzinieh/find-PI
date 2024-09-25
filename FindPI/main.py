import math

import matplotlib.pyplot as plt
import matplotlib_fontja

from .evaluate import FindPIFunc
from .find_pi.utils import Judge

matplotlib_fontja.japanize()


def main(funcs, judge_func, digits, threshold, evaluate_times):
    funcs_length = len(funcs)
    fig, ax = plt.subplots(
        funcs_length, 1, sharex=True, figsize=(6.4, 4.8 * funcs_length)
    )

    for index, (func, name) in enumerate(funcs):
        judge = Judge(judge_func, digits, threshold).judge
        find_pi_func = FindPIFunc(func, judge)
        find_pi_func.evaluate(evaluate_times)

        running_time = find_pi_func.running_time
        n = find_pi_func.n
        value = find_pi_func.value
        count = len(n)

        ax[index].set_title(f"{name}({count}回/{running_time:.2e}秒)")
        ax[index].set_xscale("log")
        ax[index].xaxis.set_tick_params(which="both", labelbottom=True)
        ax[index].set_ylabel("求めたπの値")
        ax[index].axhline(math.pi, ls="--", color="r", label="π")
        ax[index].grid()
        ax[index].plot(n, value, "-", label=name)
        print(f"【{name}】")
        print(f"試行回数：{count}回")
        print(f"求めたπの値：{value[-1]}")
        print(f"実行時間：{running_time:.6f}秒")
        print()

    plt.savefig("result.png")


if __name__ == "__main__":
    from .find_pi.funcs import (
        chudnovsky,
        dichotomy,
        incribed,
        leibniz,
        monte_carlo,
        outcribed,
        quadrature,
    )
    from .find_pi.utils import judge_digits_and_distance

    FUNCS = [
        (incribed, "内接多角形"),
        (outcribed, "外接多角形"),
        (monte_carlo, "モンテカルロ法"),
        (leibniz, "ライプニッツの公式"),
        (chudnovsky, "チュドノフスキー法"),
        (quadrature, "区分求積法"),
        (dichotomy, "二分法"),
    ]
    JUDGE_FUNC = judge_digits_and_distance
    DIGITS = 5
    THRESHOLD = 0.00003
    EVALUATE_TIMES = 3

    main(FUNCS, JUDGE_FUNC, DIGITS, THRESHOLD, EVALUATE_TIMES)
