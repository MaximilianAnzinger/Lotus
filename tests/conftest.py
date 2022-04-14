import sys

import pytest
from lotus.dataset import DataSet


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
