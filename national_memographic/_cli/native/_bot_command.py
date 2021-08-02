"""
A module implementing the bot command that is runnable only from a terminal.
"""

import click

from ..._bot.bot import run
from .._error import handle_error


@click.command()
@click.option("--api-key", required=True)
@click.option("--api-secret", required=True)
@click.option("--access-token", required=True)
@click.option("--access-secret", required=True)
@click.option("--bulk-apperception", type=int, default=10)
@handle_error
def bot(
        api_key: str,
        api_secret: str,
        access_token: str,
        access_secret: str,
        bulk_apperception: int
) -> None:
    """
    Runs the Twitter bot with the given parameters.
    """

    run(
        api_key,
        api_secret,
        access_token,
        access_secret,
        bulk_apperception=bulk_apperception
    )
