import click

from ._bot_command import bot
from ._generate_command import generate
from ._ls_command import ls


@click.group()
def cli():
    pass


cli.add_command(bot)
cli.add_command(generate)
cli.add_command(ls)
