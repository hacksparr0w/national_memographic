"""
A module containing the core bot logic.
"""

import sys
import io
import logging
import time

from datetime import datetime, timedelta

from .._args import parse
from .._cli.twitter.cli import cli
from .._cli.twitter.context import Context
from .._twitter import account, direct_message, user
from .._twitter.direct_message import DirectMessage
from .._twitter.session import Session
from .error import SecurityError


_RESPONSE_TASK_RUN_PERIOD = timedelta(minutes=1)
_MESSAGE_PROCESSING_TIMEOUT = timedelta(minutes=5)


def _process_message(session: Session, message: DirectMessage) -> None:
    args = parse(message.text)
    sender = user.get(session, message.sender_id)
    context = Context(session, sender)

    old_stderr = sys.stderr
    old_stdout = sys.stdout

    buffer = io.BytesIO()
    output = io.TextIOWrapper(buffer, encoding="utf-8")

    sys.stderr = output
    sys.stdout = output

    try:
        cli(args=args, prog_name=" ", obj=context)  # pylint: disable=E1123
    except SystemExit:
        pass
    finally:
        sys.stderr = old_stderr
        sys.stdout = old_stdout

    buffer.seek(0)
    response = buffer.read().decode("utf-8")

    if response:
        direct_message.send(session, message.sender_id, response)


def run(
        api_key: str,
        api_secret: str,
        access_token: str,
        access_secret: str,
        bulk_apperception: int
) -> None:
    """
    Runs the main bot request processing loop.

    :param api_key: Twitter API key
    :param api_secret: Twitter API secret
    :param access_token: Twitter user access token
    :param access_secret: Twitter user access secret
    :param bulk_apperception: a bot's overall intelligence
    """

    if bulk_apperception > 20:
        raise SecurityError("A potential threat to humanity detected")

    session = Session(api_key, api_secret, access_token, access_secret)
    me = account.me(session)

    logging.info("Authenticated as @%s", me.screen_name)
    logging.info(
        "Running response task once in %d seconds",
        _RESPONSE_TASK_RUN_PERIOD.total_seconds()
    )

    while True:
        time.sleep(_RESPONSE_TASK_RUN_PERIOD.total_seconds())

        now = datetime.now()
        messages = direct_message.latest(session)

        processed = {}
        total = 0

        for message in messages:
            if message.created_at < now - _MESSAGE_PROCESSING_TIMEOUT:
                break

            if message.sender_id == me.user_id:
                processed[message.recipient_id] = True
                continue

            if message.recipient_id == me.user_id:
                if processed.get(message.sender_id):
                    continue

            _process_message(session, message)
            total += 1
            processed[message.sender_id] = True

        logging.info(
            "Processed total of %d message(s) during this period",
            total
        )
