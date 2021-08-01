from dataclasses import dataclass
from datetime import datetime
from typing import List, Mapping

from .. import _url
from ._api import API_URL
from .session import Session


_URL = _url.join(API_URL, "/direct_messages")


@dataclass
class DirectMessage:
    id: str
    recipient_id: str
    sender_id: str
    text: str
    created_at: datetime


def _deserialize_direct_message(data: Mapping) -> DirectMessage:
    id = data["id"]
    created_at = datetime.fromtimestamp(
        int(data["created_timestamp"]) / 1000.0
    )

    inner = data["message_create"]

    sender_id = inner["sender_id"]
    recipient_id = inner["target"]["recipient_id"]
    text = inner["message_data"]["text"]

    return DirectMessage(id, recipient_id, sender_id, text, created_at)


def _deserialize_direct_messages(data: Mapping) -> List[DirectMessage]:
    return [_deserialize_direct_message(event) for event in data["events"]]


def _endpoint(path: str) -> str:
    return _url.join(_URL, path)


def send(session: Session, recipient_id: str, text:str) -> None:
    body = {
        "event": {
            "type": "message_create",
            "message_create": {
                "target": {"recipient_id": recipient_id},
                "message_data": {"text": text }
            }
        }
    }

    session.post(_endpoint("/events/new.json"), json=body)


def latest(session: Session):
    data = session.get(_endpoint("/events/list.json")).json()
    messages = _deserialize_direct_messages(data)

    return messages
