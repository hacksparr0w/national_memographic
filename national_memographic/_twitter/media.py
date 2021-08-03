"""
Simple interface for accessing Twitter's Standard v1.1 Media API methods.
"""

from io import BytesIO
from typing import Any, Mapping

from .. import _url
from ._api import UPLOAD_URL
from .session import Session


_SEGMENT_SIZE = 1000
_URL = _url.join(UPLOAD_URL, "/media")


def _endpoint(path: str) -> str:
    return _url.join(_URL, path)


def _initialize_upload(session: Session, media_type: str, size: int) -> str:
    params: Mapping[str, Any] = {
        "command": "INIT",
        "media_type": media_type,
        "total_bytes": size
    }

    data = session.post(_endpoint("/upload.json"), params=params).json()
    media_id: str = data["media_id_string"]

    return media_id


def _append_upload(
        session: Session,
        media_id: str,
        index: int,
        segment: bytes
) -> None:
    params: Mapping[str, Any] = {
        "command": "APPEND",
        "media_id": media_id,
        "segment_index": index
    }

    files = {
        "media": segment
    }

    session.post(_endpoint("/upload.json"), params=params, files=files)


def _finalize_upload(session: Session, media_id: str) -> bool:
    params = {
        "command": "FINALIZE",
        "media_id": media_id
    }

    data = session.post(_endpoint("/upload.json"), params=params).json()
    processing = "processing_info" in data

    return processing


def upload(
        session: Session,
        media_type: str,
        size: int,
        stream: BytesIO
) -> str:
    """
    Uploads the passed stream of bytes onto Twitter's media servers using the
    chunked upload end-point.

    :param session: the authenticated session to be used.
    :param media_type: the MIME type of the content.
    :param size: the total number of bytes the data is comprised of.
    :return: The ``media_id`` of the newly uploaded data.
    """

    media_id = _initialize_upload(session, media_type, size)

    index = 0

    while True:
        segment = stream.read(_SEGMENT_SIZE)

        if not segment:
            break

        _append_upload(session, media_id, index, segment)

        index += 1

    processing = _finalize_upload(session, media_id)

    if processing:
        raise NotImplementedError

    return media_id
