"""
Generate badges
"""
# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import os
import sys
import argparse
import pkg_resources

try:
    import coverage
except ImportError:
    coverage = None


__version__ = "0.1.4"


DEFAULT_STYLE = "flat"
STYLES = {"flat": 1, "flat-square": 1, "for-the-badge": 1.5}

DEFAULT_COLOR = "#a4a61d"
COLORS = {
    "brightgreen": "#4c1",
    "green": "#97CA00",
    "yellowgreen": "#a4a61d",
    "yellow": "#dfb317",
    "orange": "#fe7d37",
    "red": "#e05d44",
    "lightgrey": "#9f9f9f",
    "blue": "#007ec6",
}

COLOR_RANGES = [
    (95, "brightgreen"),
    (90, "green"),
    (75, "yellowgreen"),
    (60, "yellow"),
    (40, "orange"),
    (0, "red"),
]


class Devnull(object):
    """
    A file like object that does nothing.
    """

    def write(self, *args, **kwargs):
        pass


def get_total():
    """
    Return the rounded total as properly rounded string.
    """
    cov = coverage.Coverage()
    cov.load()
    total = cov.report(file=Devnull())
    return "{0:.0f}".format(total)


def get_git_tag():
    """
    Return current git tag.
    """
    return os.popen("git describe --tags --abbrev=0").read()


def get_color(total):
    """
    Return color for current coverage precent
    """
    try:
        xtotal = int(total)
    except ValueError:
        return COLORS["lightgrey"]
    for range_, color in COLOR_RANGES:
        if xtotal >= range_:
            return COLORS[color]


def get_badge(text, value, color=DEFAULT_COLOR, style=DEFAULT_STYLE):
    """
    Read the SVG template from the package, update total, return SVG as a
    string.
    """
    template_path = os.path.join("templates", "{}.svg".format(style))
    template = pkg_resources.resource_string(__name__, template_path).decode("utf8")
    value = value.strip()
    if style == "for-the-badge":
        text = text.upper()
        value = value.upper()

    return (
        template.replace("{{ value }}", value)
        .replace("{{ text }}", text)
        .replace("{{ color }}", color)
        .replace("{{ text_width }}", str(len(text) * 10 * STYLES[style]))
        .replace("{{ value_width }}", str(len(value) * 15 * STYLES[style]))
        .replace(
            "{{ total_width }}",
            str(len(text) * 10 * STYLES[style] + len(value) * 15 * STYLES[style]),
        )
        .replace("{{ value_text_width }}", str(len(value) * 80 * STYLES[style]))
        .replace("{{ user_text_width }}", str(len(text) * 60 * STYLES[style]))
        .replace("{{ user_text_margin }}", str((len(text) * 100 * STYLES[style]) / 2))
        .replace(
            "{{ value_text_margin }}",
            str(len(text) * 100 * STYLES[style] + len(value) * 150 * STYLES[style] / 2),
        )
    )


def parse_args(argv=None):
    """
    Parse the command line arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o", dest="filepath", help="Save the file to the specified path."
    )
    parser.add_argument(
        "-p",
        dest="plain_color",
        action="store_true",
        help="Plain color mode. Standard green badge.",
    )
    parser.add_argument(
        "-f",
        dest="force",
        action="store_true",
        help="Force overwrite image, use with -o key.",
    )
    parser.add_argument(
        "-q",
        dest="quiet",
        action="store_true",
        help="Don't output any non-error messages.",
    )
    parser.add_argument(
        "--version", dest="print_version", action="store_true", help="Show version."
    )
    parser.add_argument(
        "-git", dest="git", action="store_true", help="Build badge for git tag."
    )
    parser.add_argument(
        "-cov", dest="cov", action="store_true", help="Build badge for coverage."
    )
    parser.add_argument("-t", dest="text", help="Badge text.")
    parser.add_argument("-v", dest="value", help="Badge value.")
    parser.add_argument("-c", dest="color", help="Badge color.")
    parser.add_argument("-s", dest="style", help="Badge style.")

    # If arguments have been passed in, use them.
    if argv:
        return parser.parse_args(argv)

    # Otherwise, just use sys.argv directly.
    else:
        return parser.parse_args()


def save_badge(badge, filepath, force=False):
    """
    Save badge to the specified path.
    """
    # Validate path (part 1)
    if filepath.endswith("/"):
        print("Error: Filepath may not be a directory.")
        sys.exit(1)

    # Get absolute filepath
    path = os.path.abspath(filepath)
    if not path.lower().endswith(".svg"):
        path += ".svg"

    # Validate path (part 2)
    if not force and os.path.exists(path):
        print('Error: "{}" already exists.'.format(path))
        sys.exit(1)

    # Write file
    with open(path, "w") as f:
        f.write(badge)

    return path


def main(argv=None):
    """
    Console scripts entry point.
    """
    args = parse_args(argv)

    style = DEFAULT_STYLE

    # Validation
    if not args.git and not args.cov and not args.text and not args.value and not args.print_version:
        print("Not valid parameters. -git or -cov or -t and -v")
        sys.exit(1)

    if args.text and not args.value or not args.text and args.value:
        print("Not valid parameters. -t and -v required")
        sys.exit(1)

    # Print version
    if args.print_version:
        print("all-badge v{}".format(__version__))
        sys.exit(0)

    if args.color:
        if args.color not in COLORS.keys():
            print("Color not valid.")
            sys.exit(1)

    if args.style:
        if args.style not in STYLES:
            print("Style not valid.")
            sys.exit(1)
        else:
            style = args.style

    # Custom badge
    if args.text and args.value:
        color = args.color if args.color else "green"
        badge = get_badge(args.text, args.value, COLORS[color], style)

    # Git
    if args.git:
        # Get git last tag
        git_tag = get_git_tag()
        git_text = args.text if args.text else "version"
        color = args.color if args.color else "green"
        badge = get_badge(git_text, git_tag, COLORS[color], style)

    # Coverage
    if args.cov:
        # Check for coverage
        if coverage is None:
            print("Error: Python coverage module not installed.")
            sys.exit(1)

        # Generate badge
        try:
            total = get_total()
        except coverage.misc.CoverageException as e:
            print("Error: {} Did you run coverage first?".format(e))
            sys.exit(1)

        coverage_text = args.text if args.text else "coverage"
        color = DEFAULT_COLOR if args.plain_color else get_color(total)
        badge = get_badge(coverage_text, "{}%".format(total), color, style)

    # Show or save output
    if args.filepath:
        path = save_badge(badge, args.filepath, args.force)
        if not args.quiet:
            print("Saved badge to {}".format(path))
    else:
        print(badge, end="")


if __name__ == "__main__":
    main()
