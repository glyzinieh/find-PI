import matplotlib.pyplot as plt
import matplotlib_fontja
from PIL import Image

from .models import Wrapper

matplotlib_fontja.japanize()


def plot_value(
    funcs: list[Wrapper],
    x_list_name: str,
    x_label: str,
    y_list_name: str,
    y_label: str,
    hline: float,
    hline_label: str,
):
    funcs_length = len(funcs)
    fig, axes = plt.subplots(funcs_length, 1, figsize=(10, 5 * funcs_length))

    for i, func in enumerate(funcs):
        if hline is not None:
            axes[i].axhline(hline, color="red", linestyle="--", label=hline_label)
        x_list = getattr(func, x_list_name)
        y_list = getattr(func, y_list_name)
        axes[i].plot(x_list, y_list)

        axes[i].set_title(
            f"{func.name}({len(func.index_list)}回/{func.time_list[-1]:.2e}秒)"
        )

        axes[i].set_xlabel(x_label)
        axes[i].set_xscale("log")
        axes[i].xaxis.set_tick_params(which="both")

        axes[i].set_ylabel(y_label)

    plt.tight_layout()
    filename = f"output/{x_label}_{y_label}_{{}}.png"
    plt.savefig(filename.format("all"))

    im = Image.open(filename.format("all"))
    im_dpi = im.info["dpi"]

    for i, func in enumerate(funcs):
        top = 5 * i
        bottom = 5 * (i + 1)
        im.crop((0, top * im_dpi[1], im.width, bottom * im_dpi[1])).save(
            filename.format(func.name)
        )


def index_value(funcs: list[Wrapper], hline: float, hline_name: str):
    plot_value(funcs, "index_list", "index", "value_list", "value", hline, hline_name)


def time_value(funcs: list[Wrapper], hline: float, hline_name: str):
    plot_value(funcs, "time_list", "time", "value_list", "value", hline, hline_name)
