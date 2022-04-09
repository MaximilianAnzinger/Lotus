"""
DOC STRING
"""

# built-in imports
import glob
# third-party modules

# own modules
from LotusParser import LotusParser
from LotusPlot import LotusPlot

__author__ = "Maximilian Anzinger"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Maximilian Anzinger"]
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Maximilian Anzinger"
__email__ = "maximilian.anzinger@tum.de"
__status__ = "Development"


def setup_parsing() -> str:
    print("SETUP: START -------------------------------------------\n")
    print("Enter file: (-h for help) ------------------------------")
    while (file_dir := input()) in ["-h", "h", "help"]:
        print("Possible candidates:")
        for file in glob.glob("**/***.csv", recursive=True):
            print(file)
        print("\nEnter file: (-h for help) ------------------------------")
    print("SETUP: COMPLETE ----------------------------------------\n")
    return file_dir


def parsing(file_dir: str):
    print("PARSER: START ------------------------------------------")
    parser = LotusParser(file_dir)
    parser.parse()
    print("PARSER: found " + str(len(parser.getDataSets())) + " valid DataSets")
    print("PARSER: COMPLETE ---------------------------------------\n")
    return parser.getDataSets()


def plot(datasets):
    print("PLOTTER: START -----------------------------------------\n")

    plotter = LotusPlot(datasets)

    title = None
    while title not in ["y", "yes", "n", "no"]:
        print("Print titles: (y/n) ------------------------------------")
        title = input()

    if title in ["y", "yes"]:
        plotter.enableTitle()

    method = None
    while title not in ["y", "yes", "n", "no"]:
        print("Print titles: (y/n) ------------------------------------")
        method = input()

    print(method)

    print("PLOTTER: COMPLETE --------------------------------------\n")


if __name__ == "__main__":
    """Main entry point to execute Lotus"""
    file_dir = setup_parsing()
    # datasets = parsing(file_dir)
    # plot(datasets)

    print("SETUP: -------------------------------------------------")
    print("Enter file:")
    fileDir = input()
    print("--------------------------------------------------------")

    print("PARSER: START ------------------------------------------")
    parser = LotusParser(fileDir)
    parser.parse()
    print("PARSER: found " + str(len(parser.getDataSets())) + " valid DataSets")
    print("PARSER: COMPLETE ---------------------------------------")

    print("PLOTTER: START -----------------------------------------")
    plotter = LotusPlot(parser.getDataSets())
    plotter.enableTitle()
    plotter.exportSimpPlotPerDataset()
    print("PLOTTER: COMPLETE --------------------------------------")
