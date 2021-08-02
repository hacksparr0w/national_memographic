import sys
import io
import logging
import time

from datetime import datetime, timedelta

import click

from .._args import parse
from .._cli.twitter.cli import cli
from .._twitter import account, direct_message
from .._twitter.direct_message import DirectMessage
from .._twitter.session import Session
from .error import SecurityError


_RESPONSE_TASK_RUN_PERIOD = timedelta(minutes=1)
_MESSAGE_PROCESSING_TIMEOUT = timedelta(minutes=5)


def _process_message(session: Session, message: DirectMessage) -> None:
    args = parse(message.text)

    old_stderr = sys.stderr
    old_stdout = sys.stdout

    buffer = io.BytesIO()
    output = io.TextIOWrapper(buffer, encoding="utf-8")

    sys.stderr = output
    sys.stdout = output

    try:
        cli(args=args, prog_name=" ", obj=session)
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
    bulk_apperception: int = 10
) -> None:
    if bulk_apperception > 20:
        raise SecurityError("A potential threat to humanity detected")

    session = Session(api_key, api_secret, access_token, access_secret)
    me = account.me(session)

    logging.info("Authenticated as @%s", me.screen_name)
    logging.info(
        "Running response task once in %s",
        str(_RESPONSE_TASK_RUN_PERIOD)
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

            if message.sender_id == me.id:
                processed[message.recipient_id] = True
                continue

            if message.recipient_id == me.id:
                if processed.get(message.sender_id):
                    continue

            _process_message(session, message)
            total += 1
            processed[message.sender_id] = True

        logging.info(
            "Processed total of %d message(s) during this period.",
            total
        )
