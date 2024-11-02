from typing import Callable

import matplotlib.pyplot as plt
import matplotlib_fontja
from PIL import Image

from .models import HLine, Runner

matplotlib_fontja.japanize()


def plot_value(
    funcs: list[Callable],
    x_label: str,
    y_label: str,
    hline: HLine,
    type: str = "index-value",
):
    funcs_length = len(funcs)
    axes_length = funcs_length

    fig, axes = plt.subplots(axes_length, 1, figsize=(10, 5 * axes_length), sharex=True)

    for i, func in enumerate(funcs):
        if hline is not None:
            axes[i].axhline(hline.value, color="red", linestyle="--", label=hline.name)

        runner: Runner = func.__closure__[1].cell_contents
        time = runner.results[-1].time_list[-1]

        match type:
            case "index-value":
                x_list = runner.results[-1].index_list
                y_list = runner.results[-1].value_list
            case "time-value":
                x_list = runner.results[-1].time_list
                y_list = runner.results[-1].value_list

        axes[i].set_title(f"{runner.name}({len(x_list)}回/{time:.2e}秒)")

        axes[i].set_xlabel(x_label)
        axes[i].set_xscale("log")
        axes[i].xaxis.set_tick_params(which="both", labelbottom=True)

        axes[i].set_ylabel(y_label)

        axes[i].plot(x_list, y_list)

    plt.tight_layout()
    filename = f"output/{x_label}_{y_label}_{{}}.png"
    plt.savefig(filename.format("all"))

    im = Image.open(filename.format("all"))
    im_dpi = im.info["dpi"]

    for i, func in enumerate(funcs):
        runner: Runner = func.__closure__[1].cell_contents
        name = runner.name

        top = 5 * i
        bottom = 5 * (i + 1)
        im.crop((0, top * im_dpi[1], im.width, bottom * im_dpi[1])).save(
            filename.format(name)
        )
