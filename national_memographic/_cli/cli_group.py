import click

from .bot_command import bot
from .generate_command import generate
from .ls_command import ls


@click.group()
def cli():
    pass


cli.add_command(bot)
cli.add_command(generate)
cli.add_command(ls)
