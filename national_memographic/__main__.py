"""
Python program entry point.
"""

from ._cli.native.cli import cli


def main() -> None:
    """
    Runs the main CLI code.
    """

    cli()


if __name__ == "__main__":
    main()
