"""
A module implementing a version of the caption command that is used by the
bot for the Twitter CLI app.
"""

from io import BytesIO
from typing import List

import click

from ... import meme
from ..._twitter import media, tweet
from .._error import handle_error
from .context import Context, pass_context


@click.command()
@click.argument("uid")
@click.argument("captions", nargs=-1)
@pass_context
@handle_error
def caption(context: Context, uid: str, captions: List[str]) -> None:
    """
    Makes a meme from a template with the passed UID using the given
    captions.
    """

    sender = context.sender
    session = context.session
    template = meme.load_template(uid)
    image = meme.caption(template, captions)
    blob = image.make_blob()
    size = len(blob)
    stream = BytesIO(blob)

    media_id = media.upload(session, image.mimetype, size, stream)

    tweet.publish(
        session,
        f"@{sender.handle} here you go!",
        media_ids=[media_id]
    )

    click.echo("🔥")
