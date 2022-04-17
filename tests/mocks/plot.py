from typing import List

from lotus.dataset import DataSet
from lotus.plot import Plotter


class CliPlotMock(Plotter):
    def __init__(self, datasets: List[DataSet], file_extension=".svg"):
        self.title_enabled = False
        self.export_min_plot_per_dataset = False
        self.export_min_plot_for_datasets = False
        self.export_simp_plot_per_dataset = False
        self.export_simp_plot_for_datasets = False

    def enableTitle(self) -> None:
        self.title_enabled = True

    def exportMinPlotPerDataset(self) -> None:
        self.export_min_plot_per_dataset = True

    def exportMinPlotForDatasets(self) -> None:
        self.export_min_plot_for_datasets = True

    def exportSimpPlotPerDataset(self) -> None:
        self.export_simp_plot_per_dataset = True

    def exportSimpPlotForDatasets(self) -> None:
        self.export_simp_plot_for_datasets = True
