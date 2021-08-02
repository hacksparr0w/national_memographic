from io import BytesIO
from typing import List

import click

from ... import meme
from ..._twitter import media, tweet
from ..._twitter.session import Session
from .._error import handle_error
from ._pass_session import pass_session


@click.command()
@click.argument("uid")
@click.argument("captions", nargs=-1)
@pass_session
@handle_error
def generate(session: Session, uid: str, captions: List[str]) -> None:
    template = meme.load_template(uid)
    image = meme.render(template, captions)
    blob = image.make_blob()
    size = len(blob)
    stream = BytesIO(blob)

    media_id = media.upload(session, image.mimetype, size, stream)
    tweet.publish(session, "@hacksparr0w here you go!", media_ids=[media_id])

    click.echo("🔥")
