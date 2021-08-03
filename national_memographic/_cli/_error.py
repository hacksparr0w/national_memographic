"""
Common error handling capabilities shared by all CLI code.
"""

from functools import wraps
from typing import Any, Callable, TypeVar

import click

from .._bot.error import SecurityError
from ..meme import InvalidCaptionLengthError, UnknownTemplateUidError


# TODO: It may be more idiomatic to just define a base classes for these
# errors, but I'm currently too unimaginative to come up with new names...

_APP_ERRORS = (
    InvalidCaptionLengthError,
    SecurityError,
    UnknownTemplateUidError
)


F = TypeVar('F', bound=Callable[..., Any])


def handle_error(f: F) -> F:
    """
    Turns all application errors into :class:`click.UsageError`, causing them
    to be handled gracefully.

    :param f: a function to be wrapped with this decorator.
    :return: A modified version of the original function.
    """

    @wraps(f)
    def wrapped(*args, **kwargs):  # type: ignore
        try:
            return f(*args, **kwargs)
        except Exception as error:  # pylint: disable=W0703
            if isinstance(error, _APP_ERRORS):
                raise click.UsageError(error.args[0])

            raise error

    return wrapped  # type: ignore
