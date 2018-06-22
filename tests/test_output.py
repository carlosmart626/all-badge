# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import pytest

from all_badge import __main__


@pytest.fixture
def cb(monkeypatch):
    """
    Return a monkey patched coverage_badge module that always returns a percentage of 79.
    """

    def get_fake_total():
        return "79"

    def get_fake_git_tag():
        return "0.1.3"

    monkeypatch.setattr(__main__, "get_total", get_fake_total)
    monkeypatch.setattr(__main__, "get_git_tag", get_fake_git_tag)
    return __main__


def test_version(cb, capsys):
    """
    Test the version output.
    """
    with pytest.raises(SystemExit) as se: # noqa
        cb.main(["--version"])
    out, _ = capsys.readouterr()
    assert out == "all-badge v%s\n" % __main__.__version__


def test_svg_output_git(cb, capsys):
    """
    Test the SVG output.
    """
    cb.main(["-git"])
    out, _ = capsys.readouterr()
    assert '>0.1.3</text>' in out


def test_svg_output_cov(cb, capsys):
    """
    Test the SVG output.
    """
    cb.main(["-cov"])
    out, _ = capsys.readouterr()
    assert '>79%</text>' in out


def test_color_ranges(cb, capsys):
    """
    Test color total value
    """
    for total, color in (
        ("97", "#4c1"),
        ("93", "#97CA00"),
        ("80", "#a4a61d"),
        ("65", "#dfb317"),
        ("45", "#fe7d37"),
        ("15", "#e05d44"),
        ("n/a", "#9f9f9f"),
    ):
        __main__.get_total = lambda: total
        cb.main(["-cov"])
        out, _ = capsys.readouterr()
        row = color
        assert row in out
        assert out.endswith("</svg>\n")
