"""
A module for manipulating resources, mainly meme templates.
"""

import json

from pathlib import Path
from typing import Any, Mapping, TextIO

from wand.color import Color # type: ignore

from .common import Rect
from .template import Template, Text, TextAlign, TextArea, TextPosition


_TEMPLATE_DIR_PATH = Path("data/template")



def get_template_dir_path() -> Path:
    """
    Returns a path to the internal template directory.

    :return: A :class:`Path` object pointing to the internal template
        directory.
    """

    return _TEMPLATE_DIR_PATH


def deserialize_text(data: Mapping[str, Any]) -> Text:
    """
    Reconstructs a :class:`Text` object from a mapping.

    :return: A :class:`Text` object
    """

    align = TextAlign.of(data["align"])
    color = Color(data["color"])
    font_path = get_template_dir_path() / data["font_path"]
    position = TextPosition.of(data["position"])
    size = data["size"]

    return Text(align, color, font_path, position, size)


def deserialize_text_area(data: Mapping[str, Any]) -> TextArea:
    """
    Reconstructs a :class:`TextArea` object from a mapping.

    :return: A :class:`TextArea` object
    """

    bounds = Rect(*data["bounds"])
    padding = data["padding"]
    text = deserialize_text(data["text"])

    return TextArea(bounds, padding, text)


def deserialize_template(uid: str, data: Mapping[str, Any]) -> Template:
    """
    Reconstructs a :class:`Template` object from a mapping.

    :return: A :class:`Template` object
    """

    image_path = get_template_dir_path() / data["image_path"]
    text_areas = [deserialize_text_area(area) for area in data["text_areas"]]

    return Template(uid, image_path, text_areas)


def get_template_path(uid: str) -> Path:
    """
    Builds a path of a template file with given UID. This operation does not
    raise any errors if no template with the passed UID exists.

    :param uid: a UID of a template
    :return: a :class:`Path` object pointing to a potential template location
    """

    path = get_template_dir_path() / f"{uid}.json"

    return path


def read_template_from_json_stream(uid: str, stream: TextIO) -> Template:
    """
    Reads a JSON serialized template from a stream and turns it into a new
    :class:`Template` object.

    :return: A new instance of :class:`Template` object, as deserialized from
        the JSON stream.
    """

    return deserialize_template(uid, json.load(stream))


def read_template_from_json_file(uid: str, path: Path) -> Template:
    """
    Reads a JSON serialized template from a file and turns it into a new
    :class:`Template` object.

    :return: A new instance of :class:`Template` object, as deserialized from
        the JSON file.
    """

    with path.open("r", encoding="utf-8") as stream:
        return read_template_from_json_stream(uid, stream)
