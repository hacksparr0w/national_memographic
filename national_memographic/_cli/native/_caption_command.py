"""
A module implementing a version of the caption command that is used in a
terminal.
"""

from typing import List

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
def caption(path: str, uid: str, captions: List[str]) -> None:
    """
    Makes a meme from a template with the passed UID using the given
    captions.
    """

    template = meme.load_template(uid)
    image = meme.caption(template, captions)

    image.save(filename=path)
