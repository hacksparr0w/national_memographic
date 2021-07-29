import textwrap

from wand.image import Image
from wand.drawing import Drawing

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

    def get_text_dims() -> Dims:
        metrics = drawing.get_font_metrics(
            image,
            wrapped_text,
            multiline=True
        )

        width = metrics.text_width
        height = metrics.text_height

        return width, height

    text_width = None
    text_height = None

    while drawing.font_size > 0:
        text_width, text_height = get_text_dims()

        if text_height > bounds.height:
            drawing.font_size -= 0.75
            wrapped_text = text
        elif text_width > bounds.width:
            columns = len(wrapped_text)

            while columns > 1:
                columns -= 1
                wrapped_text = "\n".join(textwrap.wrap(text, columns))
                text_width, _ = get_text_dims()

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

    drawing.text(x, y, wrapped_text)
    drawing.font_size = previous_font_size
