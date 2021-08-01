import click

from ..._twitter.session import Session


pass_session = click.make_pass_decorator(Session)
