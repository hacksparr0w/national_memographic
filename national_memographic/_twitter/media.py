from enum import Enum
from io import BytesIO

from .. import _url
from ._api import UPLOAD_URL
from .session import Session


_SEGMENT_SIZE = 1000
_URL = _url.join(UPLOAD_URL, "/media")


class MediaCategory(Enum):
    TWEET_IMAGE = "tweet_image"


def _endpoint(path: str) -> str:
    return _url.join(_URL, path)


def _initialize_upload(session: Session, media_type: str, size: int) -> str:
    params = {
        "command": "INIT",
        "media_type": media_type,
        "total_bytes": size
    }

    data = session.post(_endpoint("/upload.json"), params=params).json()
    id = data["media_id_string"]

    return id


def _append_upload(
    session: Session,
    id: str,
    index: int,
    segment: bytes
) -> None:
    params = {
        "command": "APPEND",
        "media_id": id,
        "segment_index": index
    }

    files = {
        "media": segment
    }

    session.post(_endpoint("/upload.json"), params=params, files=files)


def _finalize_upload(session: Session, id: str) -> bool:
    params = {
        "command": "FINALIZE",
        "media_id": id
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
    id = _initialize_upload(session, media_type, size)

    index = 0

    while True:
        segment = stream.read(_SEGMENT_SIZE)

        if not segment:
            break

        _append_upload(session, id, index, segment)

        index += 1

    processing = _finalize_upload(session, id)

    if processing:
        raise NotImplementedError

    return id
