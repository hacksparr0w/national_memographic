from functools import wraps

import click

from .._bot.error import BotError
from ..meme import MemeError


def handle_error(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as error:
            if isinstance(error, (BotError, MemeError)):
                raise click.UsageError(error.args[0])
            else:
                raise error

    return wrapped
