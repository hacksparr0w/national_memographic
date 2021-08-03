"""
An internal module for advanced image manipulation using :mod:`wand`.
"""

import textwrap

from wand.image import Image  # type: ignore
from wand.drawing import Drawing  # type: ignore

from .common import Rect
from .template import TextAlign, TextPosition, TextPositionX, TextPositionY


def draw_bounded_text(
        drawing: Drawing,
        image: Image,
        text: str,
        align: TextAlign,
        position: TextPosition,
        bounds: Rect
) -> None:
    """
    Draws a text into an area defined by a :class:`Rect` object, resizing and
    wrapping the text as neccessary.

    :param drawing: the Wand :class:`Drawing` context to be used.
    :param image: the :class:`Image` object to draw on.
    :param text: the text to be drawn.
    :param align: the alignment of the text within the specified bounds.
    :param position: the position to snap the drawn text to.
    :param bounds: the area to fit the text into.
    """

    previous_font_size = drawing.font_size
    wrapped_text = text

    ascender: float
    descender: float
    text_width: float
    text_height: float

    while drawing.font_size > 0:
        metrics = drawing.get_font_metrics(
            image,
            wrapped_text,
            multiline=True
        )

        ascender = metrics.ascender
        descender = metrics.descender
        text_width = metrics.text_width
        text_height = metrics.text_height

        if text_height > bounds.height:
            drawing.font_size -= 0.75
            wrapped_text = text
        elif text_width > bounds.width:
            columns = len(wrapped_text)

            while columns > 1:
                columns -= 1
                wrapped_text = "\n".join(textwrap.wrap(text, columns))
                metrics = drawing.get_font_metrics(
                    image,
                    wrapped_text,
                    multiline=True
                )

                text_width = metrics.text_width

                if text_width <= bounds.width:
                    break

            if columns == 1:
                drawing.font_size -= 0.75
                wrapped_text = text
        else:
            break

    x = bounds.x1
    y = bounds.y1

    if position.x == TextPositionX.CENTER:
        x += round((bounds.width - text_width) / 2)
    elif position.x == TextPositionX.RIGHT:
        x += round(bounds.width - text_width)

    if position.y == TextPositionY.BOTTOM:
        y += round(bounds.height - text_height)
    elif position.y == TextPositionY.CENTER:
        y += round((bounds.height - text_height) / 2)

    lines = wrapped_text.split("\n")

    for line in lines:
        y += round(ascender)

        metrics = drawing.get_font_metrics(image, line)
        line_width = metrics.text_width

        dx = 0

        if align == TextAlign.CENTER:
            dx = round((text_width - line_width) / 2)
        elif align == TextAlign.RIGHT:
            dx = round(text_width - line_width)

        drawing.text(x + dx, y, line)

        y -= round(descender)

    drawing.font_size = previous_font_size
