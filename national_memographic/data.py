import json

from enum import Enum
from io import TextIOBase
from dataclasses import dataclass
from pathlib import Path
from typing import List, Mapping, Tuple

from wand.color import Color

from .common import Rect
from .template import Template, Text, TextAlign, TextArea, TextPosition


_TEMPLATE_DIR_PATH = Path("data/template")


class UnknownTemplateUidError(Exception):
    def __init__(self, uid):
        super().__init__(f"No template with UID '{uid}' found")

        self.uid = uid


def get_template_dir_path():
    return _TEMPLATE_DIR_PATH


def deserialize_text(data: Mapping) -> Text:
    align = TextAlign.of(data["align"])
    color = Color(data["color"])
    font_path = get_template_dir_path() / data["font_path"]
    line_height = data["line_height"]
    position = TextPosition.of(data["position"])
    size = data["size"]

    return Text(align, color, font_path, line_height, position, size)


def deserialize_text_area(data: Mapping) -> TextArea:
    bounds = Rect(*data["bounds"])
    padding = data["padding"]
    text = deserialize_text(data["text"])

    return TextArea(bounds, padding, text)


def deserialize_template(uid: str, data: Mapping) -> Template:
    image_path = get_template_dir_path() / data["image_path"]
    text_areas = tuple(
        deserialize_text_area(area) for area in data["text_areas"]
    )

    return Template(uid, image_path, text_areas)


def get_template_path(uid: str) -> Path:
    path = get_template_dir_path() / f"{uid}.json"

    if not path.is_file():
        raise UnknownTemplateUidError(uid)

    return path


def read_template_from_json_stream(uid: str, stream: TextIOBase) -> Template:
    return deserialize_template(uid, json.load(stream))


def read_template_from_json_file(uid: str, path: Path):
    with path.open("r", encoding="utf-8") as stream:
        return read_template_from_json_stream(uid, stream)
