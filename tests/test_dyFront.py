#!/usr/bin/env pytest -vs
"""Tests for dyFront."""

# Standard Python Libraries
import os
import sys
from unittest.mock import patch

# Third-Party Libraries
import pytest

# cisagov Libraries
import dyFront

# define sources of version strings
RELEASE_TAG = os.getenv("RELEASE_TAG")
PROJECT_VERSION = dyFront.__version__


def test_stdout_version(capsys):
    """Verify that version string sent to stdout agrees with the module version."""
    with pytest.raises(SystemExit):
        with patch.object(sys, "argv", ["bogus", "--version"]):
            dyFront.dyFront.interactive()
    captured = capsys.readouterr()
    assert (
        captured.out == f"{PROJECT_VERSION}\n"
    ), "standard output by '--version' should agree with module.__version__"


@pytest.mark.skipif(
    RELEASE_TAG in [None, ""], reason="this is not a release (RELEASE_TAG not set)"
)
def test_release_version():
    """Verify that release tag version agrees with the module version."""
    assert (
        RELEASE_TAG == f"v{PROJECT_VERSION}"
    ), "RELEASE_TAG does not match the project version"


def test_list_working():
    """Working domain list to test with."""
    with patch.object(
        sys, "argv", ["bogus", "list", "google.com", "facebook.com", "login.gov"]
    ):
        return_code = dyFront.dyFront.interactive()
    assert return_code == 0, "interactive() should return successfully"


def test_list_working_double(capsys):
    """Working domain list to test -d with."""
    with patch.object(
        sys,
        "argv",
        ["bogus", "list", "google.com", "facebook.com", "login.gov", "-v", "-d"],
    ):
        return_code = dyFront.dyFront.interactive()
        captured = capsys.readouterr()
    assert return_code == 0, "interactive() should return successfully"
    assert "completed: 6" in captured.out


def test_list_working_verbose(capsys):
    """Working domain list to test -v with."""
    with patch.object(
        sys, "argv", ["bogus", "list", "google.com", "facebook.com", "login.gov", "-v"]
    ):
        return_code = dyFront.dyFront.interactive()
        captured = capsys.readouterr()
    assert return_code == 0, "interactive() should return successfully"
    assert "3 Domains Validated" in captured.out


def test_list_working_tcount(capsys):
    """Working domain list to test -t with."""
    with patch.object(
        sys,
        "argv",
        ["bogus", "list", "google.com", "facebook.com", "login.gov", "-t", "3"],
    ):
        return_code = dyFront.dyFront.interactive()
        captured = capsys.readouterr()
    assert return_code == 0, "interactive() should return successfully"
    assert "Using 3 threads" in captured.out


def test_list_broken():
    """Broken domain list to test with."""
    with patch.object(
        sys,
        "argv",
        ["bogus", "list", "google.com/searchtest", "facebook.com", "login.gov"],
    ):
        return_code = dyFront.dyFront.interactive()
    assert return_code == 1, "interactive() should return failure"


def test_file_working():
    """Working domain file to test with."""
    with patch.object(sys, "argv", ["./dyFront", "file", "tests/validTest.txt"]):
        return_code = dyFront.dyFront.interactive()
    assert return_code == 0, "interactive() should return successfully"


"""Test a broken domains passed in as a file"""


def test_file_broken():
    """Broken domain file to test with."""
    with patch.object(sys, "argv", ["bogus", "file", "tests/invalidTest.txt"]):
        return_code = dyFront.dyFront.interactive()
    assert return_code != 0, "interactive() should return failure"


def test_file_dne():
    """Working domain list to test with."""
    with patch.object(sys, "argv", ["./dyFront", "file", "nosuchfile.txt"]):
        return_code = dyFront.dyFront.interactive()
    assert return_code != 0, "interactive() should return successfully"


def test_file_write(tmpdir):
    """Test writing to a file."""
    file = tmpdir.join("outputtest.txt")
    with patch.object(
        sys, "argv", ["./dyFront", "list", "google.com", "-o", str(file)]
    ):
        dyFront.dyFront.interactive()
    assert "google.com" in file.read()
