"""
A module for manipulating resources, mainly meme templates.
"""

import os
import json

from pathlib import Path
from typing import Any, Dict, Mapping, Optional, TextIO

from wand.color import Color  # type: ignore

from .common import Rect
from .template import (
    Template,
    TextAlignment,
    TextArea,
    TextPosition,
    TextStyle,
    TextTransformation
)


_DATA_DIR_PATH = Path(os.path.abspath(__file__)).parent / "../data"
_TEMPLATE_DIR_PATH = _DATA_DIR_PATH / "template"


def get_template_dir_path() -> Path:
    """
    Returns a path to the internal template directory.

    :return: A :class:`Path` object pointing to the internal template
        directory.
    """

    return _TEMPLATE_DIR_PATH


def deserialize_text_style(data: Mapping[str, Any]) -> TextStyle:
    """
    Reconstructs a :class:`TextStyle` object from a mapping.

    :return: A :class:`TextStyle` object
    """

    kwargs = {}

    kwargs["font_path"] = get_template_dir_path() / data["font_path"]
    kwargs["font_size"] = data["font_size"]

    if "align" in data:
        kwargs["align"] = TextAlignment.of(data["align"])

    if "border_color" in data:
        kwargs["border_color"] = Color(data["border_color"])

    if "border_width" in data:
        kwargs["border_width"] = data["border_width"]

    if "fill_color" in data:
        kwargs["fill_color"] = Color(data["fill_color"])

    if "interline_spacing" in data:
        kwargs["interline_spacing"] = data["interline_spacing"]

    if "position" in data:
        kwargs["position"] = TextPosition.of(data["position"])

    if "transform" in data:
        kwargs["transform"] = TextTransformation.of(data["transform"])

    return TextStyle(**kwargs)


def deserialize_text_area(
    data: Mapping[str, Any],
    global_text_style: Optional[TextStyle]
) -> TextArea:
    """
    Reconstructs a :class:`TextArea` object from a mapping.

    :param data: a mapping to deserialize a text area from.
    :param global_text_style: a global definition of text style to be passed
        down to this :class:`TextArea` object.
    :return: A :class:`TextArea` object
    """

    kwargs: Dict[str, Any] = {}

    kwargs["bounds"] = Rect(*data["bounds"])

    if "padding" in data:
        kwargs["padding"] = data["padding"]

    if global_text_style:
        text_style = data.get("text_style")
        kwargs["text_style"] = (
            deserialize_text_style(text_style) if text_style
            else global_text_style
        )
    else:
        kwargs["text_style"] = data["text_style"]

    return TextArea(**kwargs)


def deserialize_template(uid: str, data: Mapping[str, Any]) -> Template:
    """
    Reconstructs a :class:`Template` object from a mapping.

    :return: A :class:`Template` object
    """

    image_path = get_template_dir_path() / data["image_path"]
    global_text_style = (
        deserialize_text_style(data["text_style"]) if "text_style" in data
        else None
    )

    text_areas = []

    for area in data["text_areas"]:
        text_area = deserialize_text_area(area, global_text_style)
        text_areas.append(text_area)

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
