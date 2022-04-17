"""
TODO
"""
import abc
import csv
from typing import List
from typing import Tuple
from typing import TypeVar

from lotus.dataset import DataSet

__author__ = "Maximilian Anzinger"
__copyright__ = "Copyright 2022, Maximilian Anzinger"
__credits__ = ["Maximilian Anzinger"]
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Maximilian Anzinger"
__email__ = "maximilian.anzinger@tum.de"
__status__ = "Development"

TParser = TypeVar("TParser", bound="Parser")


class Parser(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "parse")
            and callable(subclass.parse)
            and hasattr(subclass, "getDataSets")
            and callable(subclass.getDataSets)
        )

    @abc.abstractmethod
    def __init__(self, fileDir, floatSep=".", delimiter=",", quotechar="|") -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def parse(self: TParser) -> TParser:
        raise NotImplementedError

    @abc.abstractmethod
    def getDataSets(self) -> List[DataSet]:
        raise NotImplementedError


class LotusParser(Parser):
    def __init__(self, fileDir, floatSep=".", delimiter=",", quotechar="|"):
        self.fileDir = fileDir

        self.floatSep = floatSep
        self.delimiter = delimiter
        self.quotechar = quotechar

        self._groups: Tuple[str, ...] = ()

        self.rawData: List[List[str]] = []
        self.dataSets: List[DataSet] = []

    def parse(self):
        self._import_data()
        self._parse_datasets()
        del self.rawData
        return self

    def _import_data(self) -> None:
        with open(self.fileDir, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=self.delimiter)
            self.rawData = []
            for row in reader:
                self.rawData.append(list(row))

    def _parse_dataset(self, base_offset: int) -> int:
        # generate labels
        labels = self.rawData[base_offset + 1]
        while labels[-1] == "":
            labels.pop()

        if len(labels) % len(self._groups) != 0:
            raise ValueError(
                f"Found invalid dataset: {self.rawData[base_offset][0]} - Number of columns must be a multiple of {len(self._groups)}."
            )
        col = len(labels) // len(self._groups)

        # structure values
        dataSet = DataSet(
            self.rawData[base_offset][0], self._groups, tuple(labels[0:col])
        )
        offset: int = 2
        while (
            base_offset + offset < len(self.rawData)
            and self.rawData[base_offset + offset][0] != ""
        ):
            raw_row = self.rawData[base_offset + offset]
            row = [self._str_to_float(i) for i in raw_row[: len(labels)]]
            dataSet.addRow(row)
            offset += 1

        self.dataSets.append(dataSet)
        return base_offset + offset

    def _parse_datasets(self) -> None:

        if len(self.rawData) == 0:
            raise ValueError(
                f"Invalid file: {self.fileDir} -  First row doen't match the specifications."
            )

        # generate groups
        self._groups = tuple(
            str(cell)
            for i, cell in enumerate(self.rawData[0])
            if not (cell == "" or i == 0)
        )

        # parse datasets
        offset = 1
        while offset < len(self.rawData):
            if self.rawData[offset][0] == "":
                offset += 1
            else:
                offset = self._parse_dataset(offset)

    def getDataSets(self):
        return self.dataSets

    def _str_to_float(self, str: str) -> float:
        if self.floatSep == ".":
            temp = str
        else:
            temp = str.replace(self.floatSep, ".")

        try:
            out = float(temp)
        except ValueError:
            raise ValueError(f"Found invalid dataset: Can not convert {str} to float.")
        finally:
            return out
