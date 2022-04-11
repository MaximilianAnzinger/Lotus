"""
TODO
"""

__author__ = "Maximilian Anzinger"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Maximilian Anzinger"]
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Maximilian Anzinger"
__email__ = "maximilian.anzinger@tum.de"
__status__ = "Development"

import glob
from typing import Any, Callable, List, Tuple
from lotus.dataset import DataSet
from lotus.parser import LotusParser
from lotus.plot import LotusPlot


def _setup_parsing() -> str:
    print("SETUP: START -------------------------------------------\n")
    print("Enter file: (-h for help) ------------------------------")
    while (file_dir := input()) in ["-h", "h", "help"]:
        print("Possible candidates:")
        for file in glob.glob("**/***.csv", recursive=True):
            print(file)
        print("\nEnter file: (-h for help) ------------------------------")
    print("SETUP: COMPLETE ----------------------------------------\n")
    return file_dir


def _parsing(file_dir: str):
    print("PARSER: START ------------------------------------------")
    parser = LotusParser(file_dir)
    parser.parse()
    print("PARSER: found " + str(len(parser.getDataSets())) + " valid DataSets")
    print("PARSER: COMPLETE ---------------------------------------\n")
    return parser.getDataSets()


def _setup_plot() -> List[Tuple[Callable[[LotusPlot], Any], str]]:

    calls: List[Tuple[Callable[[LotusPlot], Any], str]] = []

    print("SETUP: START -------------------------------------------\n")

    title = None
    while title not in ["y", "yes", "n", "no"]:
        print("Print titles: (y/n) ------------------------------------")
        title = input()
    print()

    if title in ["y", "yes"]:
        calls.append((lambda plotter: plotter.enableTitle(), "Title enabled"))

    plot = -1
    options: Tuple[Tuple[str, Callable[[LotusPlot], Any]], ...] = (
        (
            "export min plot per dataset",
            lambda plotter: plotter.exportMinPlotPerDataset(),
        ),
        (
            "export min plot for datasets",
            lambda plotter: plotter.exportMinPlotForDatasets(),
        ),
        (
            "export simple plot per dataset",
            lambda plotter: plotter.exportSimpPlotPerDataset(),
        ),
    )
    while plot < 0 or len(options) <= plot:
        print("Select plot: -------------------------------------------")
        for (id, (label, method)) in enumerate(options):
            print(str(id) + " - " + label)
        i = input()
        try:
            plot = int(i)
            if plot < 0 or len(options) <= plot:
                print(
                    "Please select a number between "
                    + str(0)
                    + " and "
                    + str(len(options))
                )
        except ValueError:
            print(
                "Please select a number between " + str(0) + " and " + str(len(options))
            )

    calls.append((options[plot][1], "Running: " + options[plot][0]))

    print("SETUP: COMPLETE ----------------------------------------\n")
    return calls


def _plot(datasets: List[DataSet], calls: List[Tuple[Callable[[LotusPlot], Any], str]]):
    print("PLOTTER: START -----------------------------------------\n")

    plotter = LotusPlot(datasets)

    for call, msg in calls:
        print(msg)
        call(plotter)
    print()

    print("PLOTTER: COMPLETE --------------------------------------\n")


def cli():
    file_dir = _setup_parsing()
    datasets = _parsing(file_dir)
    calls = _setup_plot()
    _plot(datasets, calls)


if __name__ == "__main__":
    cli()
