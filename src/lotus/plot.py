
"""
TODO
"""

import sys
import os
from os import path
import colorsys
from typing import List, Optional, Tuple, Union
import matplotlib as mpl
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from datetime import datetime
from lotus.dataset import DataSet

__author__ = "Maximilian Anzinger"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Maximilian Anzinger"]
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Maximilian Anzinger"
__email__ = "maximilian.anzinger@tum.de"
__status__ = "Development"

COLOR_TYPE = Union[str, Tuple[float, float, float]]


class LotusPlot:

    def __init__(self, datasets: List[DataSet], file_extension=".svg") -> None:
        self._datasets = datasets
        self._file_extension = file_extension
        self._outpath = os.getcwd()
        self._draw_title = False

        self.COLORS: Tuple[COLOR_TYPE, ...] = ("grey", "blue", "green",
                                               "red", "purple", "olive", "orange")

    def enableTitle(self):
        self._draw_title = True

    def _generate_field_plot_for_label(self, dataSet: DataSet, label: str, ax: Axes, color: COLOR_TYPE, field: str, marker: str, linestyle: str):
        """Helper method that adds plot for the specified data

        `dataSet`: DataSet
        `label`: str
            label for which the data should be added to the plot.
        `ax`: Axes
            Axes to add the new plot to.
        `color`: str or Tuple[float, float, float]
            color of points and linesegments.
        `field`: str in {'min', 'max', 'avg', 'var', 'mean', 'std'}
            field of simple data representation that should be plotted
        `marker`:
            marker styling of `matplotlib`
        `linestyle`:
            linesegment styling `matplotlib`
        """
        simpleData = dataSet.getSimpData(label)
        x = dataSet.Groups
        avg_y = [entry[field] for entry in simpleData]
        ax.plot(x, avg_y, label=label + " " + field,
                marker=marker, linestyle=linestyle, color=color)

    def _generate_min_plot_for_label(self, dataSet: DataSet, label: str, ax: Axes, color: COLOR_TYPE):
        self._generate_field_plot_for_label(
            dataSet, label, ax, color, 'min', 'o', 'dotted')

    def _generate_max_plot_for_label(self, dataSet: DataSet, label: str, ax: Axes, color: COLOR_TYPE):
        self._generate_field_plot_for_label(
            dataSet, label, ax, color, 'max', 'o', 'dotted')

    def _generate_avg_plot_for_label(self, dataSet: DataSet, label: str, ax: Axes, color: COLOR_TYPE):
        self._generate_field_plot_for_label(
            dataSet, label, ax, color, 'avg', '^', 'solid')

    def _generate_simp_plot_for_label(self, dataSet: DataSet, label: str, ax: Axes, color: COLOR_TYPE):
        self._generate_min_plot_for_label(dataSet, label, ax, color)
        self._generate_max_plot_for_label(dataSet, label, ax, color)
        self._generate_avg_plot_for_label(dataSet, label, ax, color)

    def _generate_min_plot_for_dataset(self, dataSet: DataSet, fig: Figure, ax: Axes, color=None):
        colors: Tuple[COLOR_TYPE, ...] = ()
        if color is None:
            colors = self.COLORS
        else:
            min_factor = 0.5
            max_factor = 1.5
            step = (max_factor - min_factor) / (dataSet.LabelCount - 1)
            colors = tuple(self._lightenColor(color, min_factor + i * step)
                           for i in range(len(dataSet.Labels)))
        for i, label in enumerate(dataSet.Labels):
            self._generate_avg_plot_for_label(dataSet, label, ax, colors[i])

    def _generate_simp_plot_for_dataset(self, dataSet: DataSet, fig: Figure, ax: Axes, color: Optional[COLOR_TYPE] = None):
        if color is None:
            colors = self.COLORS
        else:
            min_factor = 0.5
            max_factor = 1.5
            step = (max_factor - min_factor) / (dataSet.LabelCount - 1)
            colors = tuple(self._lightenColor(color, min_factor + i * step)
                           for i in range(len(dataSet.Labels)))
        for i, label in enumerate(dataSet.Labels):
            self._generate_simp_plot_for_label(dataSet, label, ax, colors[i])

    def _generate_min_plot_for_collection(self, collection: List[DataSet]):
        if (len(self.COLORS) < len(collection)):
            sys.exit("CRITICAL FAILURE: Too many datasets selected!")
        fig, ax = plt.subplots()
        for i, dataSet in enumerate(collection):
            self._generate_min_plot_for_dataset(
                dataSet, fig, ax, mpl.colors.ColorConverter.to_rgb(self.COLORS[i]))

    def _lightenColor(self, rgb, factor) -> COLOR_TYPE:
        h, l, s = colorsys.rgb_to_hls(*rgb)
        return colorsys.hls_to_rgb(h, min(1, l * factor), s=s)

    def _export_min_plot_for_dataset(self, dataset: DataSet):
        file = self._generate_filename(dataset.Title)
        fig, ax = plt.subplots()
        if self._draw_title:
            ax.set_title(dataset.Title)
        self._generate_min_plot_for_dataset(dataset, fig, ax)
        plt.legend(loc='best')
        plt.savefig(file)
        plt.close()

    def exportMinPlotPerDataset(self):
        for dataset in self._datasets:
            self._export_min_plot_for_dataset(dataset)

    def exportMinPlotForDatasets(self):
        file = self._generate_filename("MinPlot")
        fig, axs = plt.subplots(len(self._datasets), figsize=(
            5, 5 * len(self._datasets)), sharex=True)
        for i, dataset in enumerate(self._datasets):
            if self._draw_title:
                axs[i].set_title(dataset.Title)
            self._generate_min_plot_for_dataset(dataset, fig, axs[i])
            axs[i].legend(loc='best')
        plt.savefig(file)
        plt.close()

    def _export_simp_plot_for_dataset(self, dataset: DataSet):
        file = self._generate_filename(dataset.Title)
        fig, ax = plt.subplots()
        if self._draw_title:
            ax.set_title(dataset.Title)
        self._generate_simp_plot_for_dataset(dataset, fig, ax)
        plt.legend(loc='best')
        plt.savefig(file)
        plt.close()

    def exportSimpPlotPerDataset(self):
        for dataset in self._datasets:
            self._export_simp_plot_for_dataset(dataset)

    def exportSimpPlotForDatasets(self):
        pass

    def _generate_filename(self, name) -> str:
        filename = name + "_" + datetime.now().strftime("%d-%b-%Y(%H-%M-%S-%f)") + \
            self._file_extension
        return path.join(self._outpath, filename)
