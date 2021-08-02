"""
Simple interface for accessing Twitter's Standard v1.1 User API methods.
"""

from dataclasses import dataclass
from typing import Any, Mapping

from .. import _url
from ._api import API_URL
from .session import Session


_URL = _url.join(API_URL, "/users")


@dataclass
class User:
    """
    A simplified version of Twitter's User object.
    """

    user_id: str
    handle: str


def _deserialize_user(data: Mapping[str, Any]) -> User:
    user_id = data["id_str"]
    handle = data["screen_name"]

    return User(user_id, handle)


def _endpoint(path: str) -> str:
    return _url.join(_URL, path)


def get(session: Session, user_id: str) -> User:
    """
    Retrieves an :class:`User` object representing a user with the specified
    ID.

    :param session: an authenticated session to be used for this request.
    :param user_id: an ID of a user to retrieve information about.
    :return: A :class:`User` object with information about the user.
    """

    params = {
        "user_id": user_id
    }

    data = session.get(_endpoint("/show.json"), params=params).json()
    user = _deserialize_user(data)

    return user
