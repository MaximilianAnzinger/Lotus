"""
TODO
"""

import sys
from typing import List, Dict, Tuple
import numpy as np
from numpy.typing import ArrayLike

__author__ = "Maximilian Anzinger"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Maximilian Anzinger"]
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Maximilian Anzinger"
__email__ = "maximilian.anzinger@tum.de"
__status__ = "Development"


class DataSet:

    # groups: List[str]
    def __init__(self, title: str, groups: Tuple[str, ...], labels: List[str]):
        """Returns new DataSet object with specified title, groups and labels
        title: Arbitrary titel of the DataSet.
        groups: List of all labels of the groups of the DataSet.
        labels: List of all labels.
        """

        self._Title = title
        self._Groups = groups
        self._GroupCount = len(groups)
        self._Labels = labels
        self._LabelCount = len(labels)
        self._data: Dict[str, List[List[float]]] = {}
        for label in self._Labels:
            self._data[label] = [[] for group in groups]
        self._SimplifiedData: Dict[str, List[Dict[str, float]]] = {}

    @property
    def Title(self) -> str:
        return self._Title

    @Title.deleter
    def Title(self):
        del self._Title

    @property
    def Groups(self) -> Tuple[str, ...]:
        return self._Groups

    @property
    def GroupCount(self) -> int:
        return self._GroupCount

    @property
    def Labels(self) -> List[str]:
        return self._Labels

    @property
    def LabelCount(self) -> int:
        return self._LabelCount

    def addRow(self, row: List[float]):
        """Adds new row to the DataSet
        row: List of float values with matching length.
        Note: if length of the list doesn't match the specifications of the DataSet,
        the program will exit with an error message.
        """
        if len(row) != self.GroupCount * self.LabelCount:
            sys.exit("FATAL ERROR: Length of row doesn't match the dataset!")
        for i, label in enumerate(self.Labels):
            for j, group in enumerate(self.Groups):
                self._data[label][j].append(row[j * self.LabelCount + i])

    def getData(self, label: str) -> List[List[float]]:
        """Returns data corresponding to the specified label
        label: TODO
        Note: if the specified label is not contained by the DataSet, None will be returned.
        """
        if label in self.Labels:
            return self._data[label]
        return []

    def _generate_simplified_data(self, label: str):
        """
        Adds information for simplified representation of the data for the specified label.
        label: TODO
        """
        data = self.getData(label)
        simplifiedData = []
        for d in data:
            entry = {}
            entry['min'] = min(d)
            entry['max'] = max(d)
            nparr: ArrayLike = np.asarray(d)
            entry['avg'] = float(np.average(nparr))
            entry['var'] = np.var(nparr)
            entry['mean'] = np.mean(nparr)
            entry['std'] = np.std(nparr)
            simplifiedData.append(entry)

        self._SimplifiedData[label] = simplifiedData

    def getSimpData(self, label: str) -> List[Dict[str, float]]:
        if label not in self._SimplifiedData:
            self._generate_simplified_data(label)
        return self._SimplifiedData[label]

    def __str__(self):
        out = "DataSet: " + self.Title + "\n"
        out += str(self.Groups) + "\n"
        out += str(self.Labels) + "\n"
        for label in self.Labels:
            out += label + "->" + str(self._data[label]) + "\n"
        return out
