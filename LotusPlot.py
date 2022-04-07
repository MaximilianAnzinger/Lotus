
"""
TODO
"""

import sys
import os
from os import path
import colorsys
import matplotlib as mpl
import matplotlib.pyplot as plt
from datetime import datetime
from DataSet import DataSet
from typing import List

__author__ = "Maximilian Anzinger"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Maximilian Anzinger"]
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Maximilian Anzinger"
__email__ = "maximilian.anzinger@tum.de"
__status__ = "Development"


class LotusPlot:

    def __init__(self, datasets: List[DataSet], file_extension=".svg") -> None:
        self._datasets = datasets
        self._file_extension = file_extension
        self._outpath = os.getcwd()

        self.COLORS = ("grey", "blue", "green",
                       "red", "purple", "olive", "orange")

    def _generate_field_plot_for_label(self, dataSet: DataSet, label: str, rgb_color, field: str, marker: str, linestyle: str):
        simpleData = dataSet.getSimpData(label)
        x = dataSet.Groups
        avg_y = [entry[field] for entry in simpleData]
        plt.plot(x, avg_y, label=label + " " + field,
                 marker=marker, linestyle=linestyle, color=rgb_color)

    def _generate_min_plot_for_label(self, dataSet: DataSet, label: str, rgb_color):
        self._generate_field_plot_for_label(
            dataSet, label, rgb_color, 'min', 'o', 'dotted')

    def _generate_max_plot_for_label(self, dataSet: DataSet, label: str, rgb_color):
        self._generate_field_plot_for_label(
            dataSet, label, rgb_color, 'max', 'o', 'dotted')

    def _generate_avg_plot_for_label(self, dataSet: DataSet, label: str, rgb_color):
        self._generate_field_plot_for_label(
            dataSet, label, rgb_color, 'avg', '^', 'solid')

    def _generate_simp_plot_for_label(self, dataSet: DataSet, label: str, rgb_color):
        self._generate_min_plot_for_label(dataSet, label, rgb_color)
        self._generate_max_plot_for_label(dataSet, label, rgb_color)
        self._generate_avg_plot_for_label(dataSet, label, rgb_color)

    def _generate_min_plot_for_dataset(self, dataSet: DataSet, rgb_color=None):
        if rgb_color is None:
            for i, label in enumerate(dataSet.Labels):
                self._generate_avg_plot_for_label(
                    dataSet, label, self.COLORS[i])
        else:
            min_factor = 0.5
            max_factor = 1.5
            step = (max_factor - min_factor) / (dataSet.LabelCount - 1)
            for i, label in enumerate(dataSet.Labels):
                self._generate_avg_plot_for_label(dataSet, label, self._lightenColor(
                    rgb_color, min_factor + i * step))

    def _generate_simp_plot_for_dataset(self, dataSet: DataSet, rgb_color=None):
        if rgb_color is None:
            for i, label in enumerate(dataSet.Labels):
                self._generate_simp_plot_for_label(
                    dataSet, label, self.COLORS[i])
        else:
            min_factor = 0.5
            max_factor = 1.5
            step = (max_factor - min_factor) / (dataSet.LabelCount - 1)
            for i, label in enumerate(dataSet.Labels):
                self._generate_simp_plot_for_label(dataSet, label, self._lightenColor(
                    rgb_color, min_factor + i * step))

    def _generate_min_plot_for_collection(self, collection: List[DataSet]):
        if (len(self.COLORS) < len(collection)):
            sys.exit("CRITICAL FAILURE: Too many datasets selected!")
        for i, dataSet in enumerate(collection):
            self._generate_min_plot_for_dataset(
                dataSet, mpl.colors.ColorConverter.to_rgb(self.COLORS[i]))

    def _lightenColor(self, rgb, factor):
        h, l, s = colorsys.rgb_to_hls(*rgb)
        return colorsys.hls_to_rgb(h, min(1, l * factor), s=s)

    def _export_min_plot_for_dataset(self, dataset: DataSet):
        file = self._generate_filename(dataset.Title)
        fig = plt.figure()
        self._generate_min_plot_for_dataset(dataset)
        plt.legend(loc='best')
        plt.savefig(file)
        plt.close()

    def exportMinPlotPerDataset(self):
        for dataset in self._datasets:
            self._export_min_plot_for_dataset(dataset)

    def _export_simp_plot_for_dataset(self, dataset: DataSet):
        file = self._generate_filename(dataset.Title)
        plt.figure()
        self._generate_simp_plot_for_dataset(dataset)
        plt.legend(loc='best')
        plt.savefig(file)
        plt.close()

    def exportSimpPlotPerDataset(self):
        for dataset in self._datasets:
            self._export_simp_plot_for_dataset(dataset)

    def _generate_filename(self, name) -> str:
        filename = name + "_" + datetime.now().strftime("%d-%b-%Y(%H-%M-%S-%f)") + \
            self._file_extension
        return path.join(self._outpath, filename)
