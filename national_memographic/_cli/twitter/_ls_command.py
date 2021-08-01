import click

from ... import meme


@click.command()
def ls():
    """
    Lists all available template UIDs with the number of captions they
    require.
    """

    templates = meme.load_templates()

    for template in templates:
        click.echo(f"{template.uid} ({len(template.text_areas)})")
