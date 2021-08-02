"""
Simple interface for accessing Twitter's Standard v1.1 Tweet API methods.
"""

from typing import List, Optional

from .. import _url
from ._api import API_URL
from .session import Session


_URL = _url.join(API_URL, "/statuses")


def _endpoint(path: str) -> str:
    return _url.join(_URL, path)


def publish(
        session: Session,
        text: str,
        media_ids: Optional[List[str]] = None
) -> None:
    """
    Publishes a new tweet comprised of specified text content and images
    identified by the passed media IDs.

    :param session: An authenticated session to be used.
    :param text: The textual content of the new tweet.
    :param media_ids: An optional list of media to be included in the tweet.
    """

    params = {
        "status": text,
        "media_ids": None if not media_ids else ",".join(media_ids)
    }

    session.post(_endpoint("/update.json"), params=params)
