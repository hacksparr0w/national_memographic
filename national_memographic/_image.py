"""
An internal module for advanced image manipulation using :mod:`wand`.
"""

import textwrap

from wand.image import Image  # type: ignore
from wand.drawing import Drawing  # type: ignore

from .common import Rect
from .template import (
    TextAlignment,
    TextPositionX,
    TextPositionY,
    TextStyle,
    TextTransformation
)


def draw_rect(drawing: Drawing, rect: Rect) -> None:
    """
    Draws a rectangle according to the suplied :class:`Rect` object.

    :param drawing: the drawing to be drawn on.
    :param rect: the :class:`Rect` object to be drawn.
    """

    drawing.rectangle(
        left=rect.x1,
        top=rect.y1,
        width=rect.width,
        height=rect.height
    )


def draw_bounded_text(  # pylint: disable=R0912,R0914,R0915
        drawing: Drawing,
        image: Image,
        bounds: Rect,
        style: TextStyle,
        text: str
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

    drawing.push()

    drawing.font = str(style.font_path)
    drawing.font_size = style.font_size
    drawing.fill_color = style.fill_color
    drawing.stroke_width = 0.0
    drawing.text_interline_spacing = style.interline_spacing

    transformed_text = text

    if style.transform == TextTransformation.UPPERCASE:
        transformed_text = text.upper()

    wrapped_text = transformed_text

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
            wrapped_text = transformed_text
        elif text_width > bounds.width:
            columns = len(wrapped_text)

            while columns > 1:
                columns -= 1
                wrapped_text = "\n".join(
                    textwrap.wrap(transformed_text, columns)
                )

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
                wrapped_text = transformed_text
        else:
            break

    x = bounds.x1
    y = bounds.y1

    if style.position.x == TextPositionX.CENTER:
        x += round((bounds.width - text_width) / 2)
    elif style.position.x == TextPositionX.RIGHT:
        x += round(bounds.width - text_width)

    if style.position.y == TextPositionY.BOTTOM:
        y += round(bounds.height - text_height)
    elif style.position.y == TextPositionY.CENTER:
        y += round((bounds.height - text_height) / 2)

    lines = wrapped_text.split("\n")

    for line in lines:
        y += round(ascender)

        metrics = drawing.get_font_metrics(image, line)
        line_width = metrics.text_width

        dx = 0

        if style.align == TextAlignment.CENTER:
            dx = round((text_width - line_width) / 2)
        elif style.align == TextAlignment.RIGHT:
            dx = round(text_width - line_width)

        if style.border_width:
            drawing.push()

            drawing.fill_color = style.border_color
            drawing.stroke_color = style.border_color
            drawing.stroke_width += style.border_width

            drawing.text(x + dx, y, line)

            drawing.pop()

        drawing.text(x + dx, y, line)

        y -= round(descender - drawing.text_interline_spacing)

    drawing.pop()
