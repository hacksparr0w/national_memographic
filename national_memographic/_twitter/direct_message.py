"""
Simple interface for accessing Twitter's Standard v1.1 Direct Message API
methods.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Mapping

from .. import _url
from ._api import API_URL
from .session import Session


_URL = _url.join(API_URL, "/direct_messages")


@dataclass
class DirectMessage:
    """
    A simplified version of Twitter's Direct Message structure.
    """

    event_id: str
    recipient_id: str
    sender_id: str
    text: str
    created_at: datetime


def _deserialize_direct_message(data: Mapping[str, Any]) -> DirectMessage:
    event_id = data["id"]
    created_at = datetime.fromtimestamp(
        int(data["created_timestamp"]) / 1000.0
    )

    inner = data["message_create"]

    sender_id = inner["sender_id"]
    recipient_id = inner["target"]["recipient_id"]
    text = inner["message_data"]["text"]

    return DirectMessage(event_id, recipient_id, sender_id, text, created_at)


def _deserialize_direct_messages(
        data: Mapping[str, Any]
) -> List[DirectMessage]:
    return [_deserialize_direct_message(event) for event in data["events"]]


def _endpoint(path: str) -> str:
    return _url.join(_URL, path)


def send(session: Session, recipient_id: str, text: str) -> None:
    """
    Sends a message with the specified text to a target user identified by the
    passed recipient ID.

    :param session: the authenticated session to be used for the API request.
    :param recipient_id: a ID that identifies the desired message recipient.
    :param text: the text content of the message.
    """

    body = {
        "event": {
            "type": "message_create",
            "message_create": {
                "target": {"recipient_id": recipient_id},
                "message_data": {"text": text}
            }
        }
    }

    session.post(_endpoint("/events/new.json"), json=body)


def latest(session: Session) -> List[DirectMessage]:
    """
    Lists the latest inbound messages within the last 30 days, sorted in
    reverse-chronological order.

    :param session: The session to be used when fulfilling the request.
    """

    data = session.get(_endpoint("/events/list.json")).json()
    messages = _deserialize_direct_messages(data)

    return messages
