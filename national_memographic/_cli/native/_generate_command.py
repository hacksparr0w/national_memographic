import click

from ... import meme
from .._error import handle_error


@click.command()
@click.option(
    "-o",
    "--out",
    "path",
    type=click.Path(),
    required=True,
    help="Path to the output file"
)
@click.argument("uid")
@click.argument("captions", nargs=-1)
@handle_error
def generate(path, uid, captions):
    template = meme.load_template(uid)
    image = meme.render(template, captions)

    image.save(filename=path)
