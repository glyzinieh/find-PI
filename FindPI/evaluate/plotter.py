import os

import matplotlib.pyplot as plt
import matplotlib_fontja
from PIL import Image
from tqdm import tqdm

from .container import ResultContainer2

matplotlib_fontja.japanize()


class Axis:
    def __init__(self, type: str, label: str, scale: str = None):
        self.type = type
        self.label = label
        self.scale = scale


class HLine:
    def __init__(self, value: float, name: str):
        self.value = value
        self.name = name


class PlotSettings:
    def __init__(
        self,
        x_axis: Axis,
        y_axis: Axis,
        right_y_axis: Axis = None,
        hline: HLine = None,
        marker: bool = False,
    ):
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.right_y_axis = right_y_axis
        self.hline = hline
        self.marker = marker


class Plotter:
    def __init__(
        self, plot_settings: PlotSettings, results: list[ResultContainer2] = list()
    ):
        self.plot_settings = plot_settings
        self.results = results

    def add(self, result: ResultContainer2):
        self.results.append(result)

    def _plot_one_graph(self):
        result = self.results[0]
        settings = self.plot_settings

        fig, ax = plt.subplots(figsize=(10, 5))

        if settings.hline is not None:
            ax.axhline(
                settings.hline.value,
                color="red",
                linestyle="--",
                label=settings.hline.name,
            )

        x_list = result.get_column(settings.x_axis.type)
        y_list = result.get_column(settings.y_axis.type)

        ax.set_xlabel(settings.x_axis.label)
        if settings.x_axis.scale:
            ax.set_xscale(settings.x_axis.scale)

        ax.set_ylabel(settings.y_axis.label)
        if settings.y_axis.scale:
            ax.set_yscale(settings.y_axis.scale)

        if settings.marker:
            ax.plot(x_list, y_list, marker="o")
        else:
            ax.plot(x_list, y_list)

        if settings.right_y_axis is not None:
            right_ax = ax.twinx()
            right_y_list = result.get_column(settings.right_y_axis.type)
            right_ax.set_ylabel(settings.right_y_axis.label)
            if settings.right_y_axis.scale:
                right_ax.set_yscale(settings.right_y_axis.scale)
            if settings.marker:
                right_ax.plot(x_list, right_y_list, marker="o")
            else:
                right_ax.plot(x_list, right_y_list)

        time = result.df["time"].iloc[-1]
        ax.set_title(f"{result.name}({len(x_list)}回/{time:.2e}秒)")

        fig.tight_layout()
        return fig

    def _plot_graphs(self):
        settings = self.plot_settings
        fig, axes = plt.subplots(
            len(self.results), figsize=(10, 5 * len(self.results)), sharex=True
        )

        for i, result in tqdm(enumerate(self.results)):
            ax: plt.Axes = axes[i]

            if settings.hline is not None:
                ax.axhline(
                    settings.hline.value,
                    color="red",
                    linestyle="--",
                    label=settings.hline.name,
                )

            time = result.df["time"].iloc[-1]

            x_list = result.get_column(settings.x_axis.type)
            y_list = result.get_column(settings.y_axis.type)

            ax.set_title(f"{result.name}({len(x_list)}回/{time:.2e}秒)")
            ax.xaxis.set_tick_params(which="both", labelbottom=True)

            ax.set_xlabel(settings.x_axis.label)
            if settings.x_axis.scale:
                ax.set_xscale(settings.x_axis.scale)

            ax.set_ylabel(settings.y_axis.label)
            if settings.y_axis.scale:
                ax.set_yscale(settings.y_axis.scale)

            if settings.marker:
                ax.plot(x_list, y_list, marker="o")
            else:
                ax.plot(x_list, y_list)

            if settings.right_y_axis is not None:
                right_ax = ax.twinx()
                right_y_list = result.get_column(settings.right_y_axis.type)
                right_ax.set_ylabel(settings.right_y_axis.label)
                if settings.right_y_axis.scale:
                    right_ax.set_yscale(settings.right_y_axis.scale)
                if settings.marker:
                    right_ax.plot(x_list, right_y_list, marker="o")
                else:
                    right_ax.plot(x_list, right_y_list)

        fig.tight_layout()
        return fig

    def plot_one_graph(self):
        if not self.results:
            raise ValueError("You need to add results before plotting.")
        self.fig = self._plot_one_graph()

    def plot(self):
        if not self.results:
            raise ValueError("You need to add results before plotting.")
        if len(self.results) == 1:
            self.fig = self._plot_one_graph()
        else:
            self.fig = self._plot_graphs()

    def save(self, path: str):
        filename = f"{self.plot_settings.x_axis.label}_{self.plot_settings.y_axis.label}_{{}}.png"

        if not self.results:
            raise ValueError("You need to plot before saving.")

        if len(self.results) == 1:
            self.fig.savefig(
                os.path.join(
                    path,
                    filename.format(self.results[0].name),
                )
            )
        else:
            self.fig.savefig(
                os.path.join(
                    path,
                    filename.format("all"),
                )
            )

            im = Image.open(
                os.path.join(
                    path,
                    filename.format("all"),
                )
            )
            im_dpi = im.info["dpi"]

            for i, result in enumerate(self.results):
                top = 5 * i
                bottom = 5 * (i + 1)
                im.crop((0, top * im_dpi[1], im.width, bottom * im_dpi[1])).save(
                    os.path.join(
                        path,
                        filename.format(result.name),
                    )
                )
