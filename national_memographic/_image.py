import textwrap

from wand.image import Image
from wand.drawing import Drawing, FontMetrics

from .common import Dims, Rect
from .template import TextPosition, TextPositionX, TextPositionY


def draw_bounded_text(
    drawing: Drawing,
    image: Image,
    text: str,
    bounds: Rect,
    position: TextPosition
) -> None:
    previous_font_size = drawing.font_size
    wrapped_text = text

    def get_text_metrics() -> FontMetrics:
        return drawing.get_font_metrics(
            image,
            wrapped_text,
            multiline=True
        )

    character_height = None
    text_width = None
    text_height = None

    while drawing.font_size > 0:
        metrics = get_text_metrics()
        character_height = metrics.character_height
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
                metrics = get_text_metrics()
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
        x += bounds.width - text_width

    if position.y == TextPositionY.BOTTOM:
        y += bounds.height - text_height
    elif position.y == TextPositionY.CENTER:
        y += round((bounds.height - text_height) / 2)

    y += round(character_height)

    drawing.text(x, y, wrapped_text)
    drawing.font_size = previous_font_size
