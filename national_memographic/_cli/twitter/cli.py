import click

from ._generate_command import generate
from ._ls_command import ls


@click.group()
def cli():
    pass


@cli.group()
def meme():
    pass


meme.add_command(generate)
meme.add_command(ls)
