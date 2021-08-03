"""
A module that binds all of the commands for the Twitter CLI app together into
one command group.
"""

import click

from ._caption_command import caption
from ._ls_command import ls


@click.group()
def cli() -> None:
    """
    The main Twitter CLI command group.
    """


@cli.group()
def meme() -> None:
    """
    A helper command group that forces users to prepend all of their commands
    with "meme". This is not needed when dealing with native CLI apps.
    """


meme.add_command(caption)
meme.add_command(ls)
