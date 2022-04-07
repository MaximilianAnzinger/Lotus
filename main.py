"""
DOC STRING 
"""

# built-in imports

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

if __name__ == "__main__":
    """Main entry point to execute LotusPlot"""

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
    plotter.exportMinPlotPerDataset()
    print("PLOTTER: COMPLETE --------------------------------------")
