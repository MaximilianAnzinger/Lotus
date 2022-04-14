import codecs

import lotus.util.cli as cli
import pytest
from tests.pytestregex import PytestRegex


parsing_regex = {
    "start-label": r"SETUP: START -*\n\n",
    "enter-file": r"Enter file: \(-h for help\) -*\n",
    "candidates": r"Possible candidates:\n(.*\.csv\n)*\n",
    "end-label": r"SETUP: COMPLETE -*\n\n",
}


def _setup_parsing_regex_generator(help_input=0):
    out = parsing_regex["start-label"]
    for i in range(help_input):
        out += parsing_regex["enter-file"] + parsing_regex["candidates"]
    out += parsing_regex["enter-file"] + r"\n"
    out += parsing_regex["end-label"]
    return out


@pytest.mark.parametrize(
    "capture_stdout, patch_stdin, expected",
    [
        ("capture_stdout", ("file_dir",), _setup_parsing_regex_generator(help_input=0)),
        (
            "capture_stdout",
            ("h", "file_dir"),
            _setup_parsing_regex_generator(help_input=1),
        ),
        (
            "capture_stdout",
            ("-h", "file_dir"),
            _setup_parsing_regex_generator(help_input=1),
        ),
        (
            "capture_stdout",
            ("help", "file_dir"),
            _setup_parsing_regex_generator(help_input=1),
        ),
        (
            "capture_stdout",
            ("h", "h", "file_dir"),
            _setup_parsing_regex_generator(help_input=2),
        ),
        (
            "capture_stdout",
            ("h", "-h", "file_dir"),
            _setup_parsing_regex_generator(help_input=2),
        ),
        (
            "capture_stdout",
            ("h", "h", "h", "file_dir"),
            _setup_parsing_regex_generator(help_input=3),
        ),
        (
            "capture_stdout",
            ("-h", "help", "h", "file_dir"),
            _setup_parsing_regex_generator(help_input=3),
        ),
    ],
    indirect=["patch_stdin", "capture_stdout"],
)
def test_setup_parsing_io(capture_stdout, patch_stdin, expected):
    cli._setup_parsing()
    assert capture_stdout["stdout"] == PytestRegex(expected), (
        "expected: <"
        + codecs.decode(expected, "unicode_escape")
        + "> but was: <"
        + capture_stdout["stdout"]
        + ">"
    )


@pytest.mark.parametrize(
    "patch_stdin,expected",
    [
        (("file_dir",), "file_dir"),
        (("h", "file_dir"), "file_dir"),
        (("h", "h", "file_dir"), "file_dir"),
        (("h", "h", "h", "file_dir"), "file_dir"),
    ],
    indirect=["patch_stdin"],
)
def test_setup_parsing_return(patch_stdin, expected):
    assert cli._setup_parsing() == expected


"""
TODO _parsing
"""

plot_regex = {
    "start-label": r"SETUP: START -*\n\n",
    "print-titles": r"Print titles: \(y/n\) -*\n",
    "select-plot": r"Select plot: -*\n",
    "option-label": r".*\n",
    "select-plot-invalid": r"Please select a number between 0 and ",
    "end-label": r"SETUP: COMPLETE -*\n\n",
}


def _setup_plot_regex_generator(invalid_titles=0, invalid_ids=0, max_id=0):
    out = plot_regex["start-label"]
    for i in range(invalid_titles + 1):
        out += plot_regex["print-titles"]
    out += r"\n"
    for i in range(invalid_ids + 1):
        out += plot_regex["select-plot"]
        for j in range(max_id + 1):
            out += str(j) + r" - " + plot_regex["option-label"]
        if i != invalid_ids:
            out += plot_regex["select-plot-invalid"] + str(max_id) + r"\n"

    out += plot_regex["end-label"]
    return out


def _setup_plot_io_args(invalid_titles=0, invalid_ids=0, max_id=0):
    print_title_valid = ["y", "yes", "n", "no"]
    print_title_invalid = ["0", "1", "-1", "invalid input"]
    id_invalid = ["-2", "-1", str(max_id + 1), "a"]

    tests = []

    # for each plot style test title on / off
    for valid in print_title_valid:
        for id in range(max_id + 1):
            tests.append(
                (
                    "capture_stdout",
                    (valid, str(id)),
                    _setup_plot_regex_generator(
                        invalid_titles=0, invalid_ids=0, max_id=max_id
                    ),
                )
            )

    for num_invalid_titles in range(invalid_titles + 1):
        for num_invalid_ids in range(invalid_ids + 1):
            title_input_seq = [
                print_title_invalid[i % len(print_title_invalid)]
                for i in range(num_invalid_titles)
            ]
            id_input_seq = [
                id_invalid[i % len(id_invalid)] for i in range(num_invalid_ids)
            ]
            tests.append(
                (
                    "capture_stdout",
                    tuple(title_input_seq + ["y"] + id_input_seq + [str(0)]),
                    _setup_plot_regex_generator(
                        invalid_titles=num_invalid_titles,
                        invalid_ids=num_invalid_ids,
                        max_id=max_id,
                    ),
                )
            )

    return tests


@pytest.mark.parametrize(
    "capture_stdout, patch_stdin, expected",
    _setup_plot_io_args(invalid_titles=3, invalid_ids=3, max_id=2),
    indirect=["patch_stdin", "capture_stdout"],
)
def test_setup_plot_io(capture_stdout, patch_stdin, expected):
    cli._setup_plot()
    assert capture_stdout["stdout"] == PytestRegex(expected), (
        "expected: <"
        + codecs.decode(expected, "unicode_escape")
        + "> but was: <"
        + capture_stdout["stdout"]
        + ">"
    )


# @pytest.mark.parametrize('patch_stdin,expected',
#                          [
#                              (("file_dir",), "file_dir"),
#                              (("h", "file_dir"), "file_dir"),
#                              (("h", "h", "file_dir"), "file_dir"),
#                              (("h", "h", "h", "file_dir"), "file_dir"),
#                          ], indirect=['patch_stdin'])
# def test_setup_plot_return(patch_stdin, expected):
#     assert cli._setup_parsing() == expected

"""
TODO _plot
"""
