import sys

import pytest
from lotus.dataset import DataSet
from lotus.parser import LotusParser


@pytest.fixture
def new_for_each_test():
    return DataSet("title1", (), ())  # yield if teardown code necessary


@pytest.fixture(scope="session")
def stays_for_all_tests():
    return DataSet("title1", (), ())  # yield if teardown code necessary


@pytest.fixture
def capture_stdout(monkeypatch):
    buffer = {"stdout": "", "write_calls": 0}

    def fake_write(s):
        buffer["stdout"] += s
        buffer["write_calls"] += 1

    monkeypatch.setattr(sys.stdout, "write", fake_write)
    return buffer


@pytest.fixture
def patch_stdin(monkeypatch, request):
    inputs = iter(request.param)
    monkeypatch.setattr("builtins.input", lambda: next(inputs))


@pytest.fixture
def mock_LotusParser_parse(monkeypatch):
    def mock_parse(self):
        pass

    monkeypatch.setattr(LotusParser, "parse", mock_parse)


@pytest.fixture
def mock_LotusParser_getDataSets(monkeypatch, request):
    def mock_getDataSets(self):
        return request.param[0]

    monkeypatch.setattr(LotusParser, "getDataSets", mock_getDataSets)
