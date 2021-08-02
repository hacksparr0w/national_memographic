"""
A module that declares a command context with information about a user
the bot is currently processing a command from.
"""

from dataclasses import dataclass

import click

from ..._twitter.session import Session
from ..._twitter.user import User


@dataclass
class Context:
    """
    A context class that holds information about current user that is being
    served.
    """

    session: Session
    sender: User


pass_context = click.make_pass_decorator(Context)
