from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from wand.color import Color

from .common import Rect


class UnknownTextAlignError(ValueError):
    def __init__(self, value: str) -> None:
        super().__init__(f"'{value}' is not a valid text alignment")


class UnknownTextPositionXError(ValueError):
    def __init__(self, value: str) -> None:
        super().__init__(f"'{value}' is not a valid X text position.")


class UnknownTextPositionYError(ValueError):
    def __init__(self, value: str) -> None:
        super().__init__(f"'{value}' is not a valid Y text position.")


class InvalidTextPositionError(ValueError):
    def __init__(self, value: str) -> None:
        super().__init__(f"'{value}' is not a valid text position.")


class TextAlign(Enum):
    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"

    @classmethod
    def of(cls, value: str) -> "TextAlign":
        for member in list(cls):
            if member.value == value:
                return member

        raise UnknownTextAlignError(value)


class TextPositionX(Enum):
    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"

    @classmethod
    def of(cls, value: str) -> "TextPositionX":
        for member in list(cls):
            if member.value == value:
                return member

        raise UnknownTextPositionXError(value)


class TextPositionY(Enum):
    BOTTOM = "bottom"
    CENTER = "center"
    TOP = "top"

    @classmethod
    def of(cls, value: str) -> "TextPositionY":
        for member in list(cls):
            if member.value == value:
                return member

        raise UnknownTextPositionYError(value)


@dataclass
class TextPosition:
    x: TextPositionX
    y: TextPositionY

    @classmethod
    def of(cls, value: str) -> "TextPosition":
        xy = value.split(" ")

        if len(xy) != 2:
            raise InvalidTextPositionError(value)

        x, y = xy

        return cls(TextPositionX.of(x), TextPositionY.of(y))


@dataclass
class Text:
    align: TextAlign
    color: Color
    font_path: str
    line_height: float
    position: TextPosition
    size: int


@dataclass
class TextArea:
    bounds: Rect
    padding: int
    text: Text


@dataclass
class Template:
    uid: str
    image_path: str
    text_areas: Tuple[TextArea]
