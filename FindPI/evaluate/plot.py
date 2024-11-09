from typing import Callable

import matplotlib.pyplot as plt
import matplotlib_fontja
from PIL import Image

from .models import HLine, Runner

matplotlib_fontja.japanize()


def plot_one_graph(
    func: Callable,
    x_type: str,
    y_type: str,
    x_label: str,
    y_label: str,
    hline: HLine,
    mode: str = "w",
):
    fig, ax = plt.subplots(figsize=(10, 5))

    if hline is not None:
        ax.axhline(hline.value, color="red", linestyle="--", label=hline.name)

    runner: Runner = func.__closure__[1].cell_contents
    time = runner.results[-1].time_list[-1]

    match x_type:
        case "index":
            x_list = runner.results[-1].index_list
        case "time":
            x_list = runner.results[-1].time_list
        case "value":
            x_list = runner.results[-1].value_list
        case "diff":
            x_list = runner.results[-1].diff_list

    match y_type:
        case "index":
            y_list = runner.results[-1].index_list
        case "time":
            y_list = runner.results[-1].time_list
        case "value":
            y_list = runner.results[-1].value_list
        case "diff":
            y_list = runner.results[-1].diff_list
        case "memory":
            y_list = runner.results[-1].memory_list

    ax.set_title(f"{runner.name}({len(x_list)}回/{time:.2e}秒)")

    ax.set_xlabel(x_label)
    ax.set_xscale("log")

    ax.set_ylabel(y_label)

    ax.plot(x_list, y_list)

    plt.tight_layout()

    match mode:
        case "w":
            plt.savefig(f"output/{x_label}_{y_label}_{runner.name}.png")
            plt.close()
        case "s":
            plt.show()


def plot_graphs(
    funcs: list[Callable],
    x_type: str,
    y_type: str,
    x_label: str,
    y_label: str,
    hline: HLine,
    mode: str = "w",
):
    fig, axes = plt.subplots(len(funcs), 1, figsize=(10, 5 * len(funcs)), sharex=True)

    for i, func in enumerate(funcs):
        ax: plt.Axes = axes[i]

        if hline is not None:
            ax.axhline(hline.value, color="red", linestyle="--", label=hline.name)

        runner: Runner = func.__closure__[1].cell_contents
        time = runner.results[-1].time_list[-1]

        match x_type:
            case "index":
                x_list = runner.results[-1].index_list
            case "time":
                x_list = runner.results[-1].time_list
            case "value":
                x_list = runner.results[-1].value_list
            case "diff":
                x_list = runner.results[-1].diff_list

        match y_type:
            case "index":
                y_list = runner.results[-1].index_list
            case "time":
                y_list = runner.results[-1].time_list
            case "value":
                y_list = runner.results[-1].value_list
            case "diff":
                y_list = runner.results[-1].diff_list
            case "memory":
                y_list = runner.results[-1].memory_list

        ax.set_title(f"{runner.name}({len(x_list)}回/{time:.2e}秒)")

        ax.set_xlabel(x_label)
        ax.set_xscale("log")
        ax.xaxis.set_tick_params(which="both", labelbottom=True)

        ax.set_ylabel(y_label)

        ax.plot(x_list, y_list)

    plt.tight_layout()

    match mode:
        case "w":
            plt.savefig(f"output/{x_label}_{y_label}_all.png")
            plt.close()

            im = Image.open(f"output/{x_label}_{y_label}_all.png")
            im_dpi = im.info["dpi"]

            for i, func in enumerate(funcs):
                runner: Runner = func.__closure__[1].cell_contents
                name = runner.name

                top = 5 * i
                bottom = 5 * (i + 1)
                im.crop((0, top * im_dpi[1], im.width, bottom * im_dpi[1])).save(
                    f"output/{x_label}_{y_label}_{name}.png"
                )
        case "s":
            plt.show()
