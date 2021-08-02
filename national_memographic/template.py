"""
A module concerned with defining the templating data model.
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Sequence

from wand.color import Color # type: ignore

from .common import Rect


class UnknownTextAlignError(ValueError):
    """
    Raised when an unknown value is provided for text alignment.
    """

    def __init__(self, value: str) -> None:
        super().__init__(f"'{value}' is not a valid text alignment")


class UnknownTextPositionXError(ValueError):
    """
    Raised when an unknown value is provided for X text position.
    """

    def __init__(self, value: str) -> None:
        super().__init__(f"'{value}' is not a valid X text position.")


class UnknownTextPositionYError(ValueError):
    """
    Raised when an unknown value is provided for Y text position.
    """

    def __init__(self, value: str) -> None:
        super().__init__(f"'{value}' is not a valid Y text position.")


class InvalidTextPositionError(ValueError):
    """
    Raised when an unknown value is provided for text position.
    """

    def __init__(self, value: str) -> None:
        super().__init__(f"'{value}' is not a valid text position.")


class TextAlign(Enum):
    """
    All possible text alignment options.
    """

    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"

    @classmethod
    def of(cls, value: str) -> "TextAlign":
        """
        Parses a member of :cls:`TextAlign` from its string value.

        :param value: a string value of text alignment.
        :return: A member of :cls:`TextAlign` enumeration.
        """

        members: List[TextAlign] = list(cls)

        for member in members:
            if member.value == value:
                return member

        raise UnknownTextAlignError(value)


class TextPositionX(Enum):
    """
    An enumeration of all possible text X-axis positionings.
    """

    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"

    @classmethod
    def of(cls, value: str) -> "TextPositionX":
        """
        Parses a member of :cls:`TextPositionX` from its string value.

        :param value: a string value representing text x-axis positioning.
        :return: A member of :cls:`TextPositionX` enumeration.
        """

        members: List[TextPositionX] = list(cls)

        for member in members:
            if member.value == value:
                return member

        raise UnknownTextPositionXError(value)


class TextPositionY(Enum):
    """
    An enumeration of all possible text Y-axis positionings.
    """

    BOTTOM = "bottom"
    CENTER = "center"
    TOP = "top"

    @classmethod
    def of(cls, value: str) -> "TextPositionY":
        """
        Parses a member of :cls:`TextPositionY` from its string value.

        :param value: a string value representing text y-axis positioning.
        :return: A member of :cls:`TextPositionY` enumeration.
        """

        members: List[TextPositionY] = list(cls)

        for member in members:
            if member.value == value:
                return member

        raise UnknownTextPositionYError(value)


@dataclass
class TextPosition:
    """
    A structure representing text positioning along the X and Y axes.
    """

    x: TextPositionX
    y: TextPositionY

    @classmethod
    def of(cls, value: str) -> "TextPosition":
        """
        Parses :class:`TextPosition` object from its string value.

        :param value: a string value representing text positioning.
        :return: The corresponding :class:`TextPosition` object.
        """

        xy = value.split(" ")

        if len(xy) != 2:
            raise InvalidTextPositionError(value)

        x, y = xy

        return cls(TextPositionX.of(x), TextPositionY.of(y))


@dataclass
class Text:
    """
    A structure of various properties of a text.
    """

    align: TextAlign
    color: Color
    font_path: Path
    position: TextPosition
    size: int


@dataclass
class TextArea:
    """
    A structure that defines text space boundaries and its visual properties.
    """

    bounds: Rect
    padding: int
    text: Text


@dataclass
class Template:
    """
    A structure that holds an image template with all possible text areas that
    can be filled with captions.
    """

    uid: str
    image_path: Path
    text_areas: Sequence[TextArea]
