from dataclasses import dataclass

import click

from ..._twitter.session import Session
from ..._twitter.user import User


@dataclass
class Context:
    session: Session
    sender: User


pass_context = click.make_pass_decorator(Context)
