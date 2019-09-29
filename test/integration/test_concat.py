""" Test str processors on actual file contents """
import os
import sys
import config
from flynt.process import fstringify_concats

import pytest


int_test_dir = os.path.join(config.home, "test/integration/")

in_dir = os.path.join(int_test_dir, "samples_in_concat")
out_dir = os.path.join(int_test_dir, "actual_out_concat")
expected_dir = os.path.join(int_test_dir, "expected_out_concat")

os.makedirs(out_dir, exist_ok=True)


def read_in(name):
    filepath = os.path.join(in_dir, name)
    with open(filepath) as f:
        txt = f.read()

    return txt


def read_expected(name):
    filepath = os.path.join(expected_dir, name)
    with open(filepath) as f:
        txt = f.read()

    return txt


def write_output_file(name, txt):
    filepath = os.path.join(out_dir, name)
    with open(filepath, "w") as f:
        f.write(txt)


def try_on_file_string_concat(filename: str, multiline):
    """ Given a file name (something.py) find this file in test/integration/samples_in,
    run flint_str on its content, write result
    to test/integration/actual_out/something.py,
    and compare the result with test/integration/expected_out/something.py"""
    txt_in = read_in(filename)
    out, edits = fstringify_concats(txt_in, multiline=multiline, len_limit=None)

    write_output_file(filename, out)
    return out, read_expected(filename)


@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires python3.8 or higher")
def test_fstringify_concat(filename_concat):
    out, expected = try_on_file_string_concat(filename_concat, multiline=True)
    assert out == expected