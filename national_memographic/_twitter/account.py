"""
Simple interface for accessing Twitter's Standard v1.1 Account API methods.
"""

from dataclasses import dataclass
from typing import Any, Mapping

from .. import _url
from ._api import API_URL
from .session import Session


_URL = _url.join(API_URL, "/account")


@dataclass
class Account:
    """
    A simplified Twitter Account structure.
    """

    user_id: str
    screen_name: str


def _deserialize_account(data: Mapping[str, Any]) -> Account:
    user_id = data["id_str"]
    screen_name = data["screen_name"]

    return Account(user_id, screen_name)


def _endpoint(path: str) -> str:
    return _url.join(_URL, path)


def me(session: Session) -> Account:
    """
    Retrieves the currently authenticated Twitter user's account information.

    :param session: the authenticated session to be used.
    :return: An :class:`Account` object representing the current user.
    """

    data = session.get(_endpoint("/verify_credentials.json")).json()
    account = _deserialize_account(data)

    return account
