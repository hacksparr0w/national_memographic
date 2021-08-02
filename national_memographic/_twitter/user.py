from dataclasses import dataclass
from typing import Mapping

from .. import _url
from ._api import API_URL
from .session import Session


_URL = _url.join(API_URL, "/users")


@dataclass
class User:
    id: str
    handle: str


def _deserialize_user(data: Mapping) -> User:
    id = data["id_str"]
    handle = data["screen_name"]

    return User(id, handle)


def _endpoint(path: str) -> str:
    return _url.join(_URL, path)


def get(session: Session, id: str) -> User:
    params = {
        "user_id": id
    }

    data = session.get(_endpoint("/show.json"), params=params).json()
    user = _deserialize_user(data)

    return user
