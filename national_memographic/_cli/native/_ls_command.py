import click

from ... import meme
from .._error import handle_error


@click.command()
@handle_error
def ls():
    """
    Lists all available template UIDs with the number of captions they
    require.
    """

    templates = meme.load_templates()

    for template in templates:
        click.echo(f"{template.uid} ({len(template.text_areas)})")
