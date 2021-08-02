"""
A module that binds all of the commands for the terminal CLI app together into
one command group.
"""

import click

from ._bot_command import bot
from ._generate_command import generate
from ._ls_command import ls


@click.group()
def cli() -> None:
    """
    The main terminal CLI command group.
    """


cli.add_command(bot)
cli.add_command(generate)
cli.add_command(ls)
