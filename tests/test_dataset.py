from typing import List
from typing import Tuple

import pytest
from lotus.dataset import DataSet

init_args = (
    ("title1", (), ()),
    ("title2", ("group1"), ()),
    ("title3", ("group1", "group2"), ()),
    ("title4", (), ("label1")),
    ("title5", (), ("label1", "label2")),
    ("title6", ("group1", "group2"), ("label1", "label2", "label3")),
    ("title7", ("group1", "group2", "group3"), ("label1", "label2")),
)


@pytest.mark.parametrize("title,groups,labels", init_args)
def test_Title(title: str, groups: Tuple[str, ...], labels: List[str]):
    dataset = DataSet(title, groups, labels)
    assert dataset.Title is title


@pytest.mark.parametrize("title,groups,labels", init_args)
def test_Groups(title: str, groups: Tuple[str, ...], labels: List[str]):
    dataset = DataSet(title, groups, labels)
    assert dataset.Groups is groups


@pytest.mark.parametrize("title,groups,labels", init_args)
def test_GroupCount(title: str, groups: Tuple[str, ...], labels: List[str]):
    dataset = DataSet(title, groups, labels)
    assert dataset.GroupCount is len(groups)


@pytest.mark.parametrize("title,groups,labels", init_args)
def test_Labels(title: str, groups: Tuple[str, ...], labels: List[str]):
    dataset = DataSet(title, groups, labels)
    assert dataset.Labels is labels


@pytest.mark.parametrize("title,groups,labels", init_args)
def test_LabelCount(title: str, groups: Tuple[str, ...], labels: List[str]):
    dataset = DataSet(title, groups, labels)
    assert dataset.LabelCount is len(labels)


def test_addRow_invalid():
    pass


def test_addRow_success():
    pass


def test_getData():
    pass


def test_getSimpleData():
    pass


def test_str():
    pass
