from dataclasses import dataclass
from typing import Mapping

from .. import _url
from ._api import API_URL
from .session import Session


_URL = _url.join(API_URL, "/account")


@dataclass
class Account:
    id: str
    screen_name: str


def _deserialize_account(data: Mapping) -> Account:
    id = data["id_str"]
    screen_name = data["screen_name"]

    return Account(id, screen_name)


def _endpoint(path: str) -> str:
    return _url.join(_URL, path)


def me(session: Session):
    data = session.get(_endpoint("/verify_credentials.json")).json()
    account = _deserialize_account(data)

    return account
