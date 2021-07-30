import json

from typing import List, Sequence

from wand.drawing import Drawing
from wand.image import Image

from ._image import draw_bounded_text
from .data import (
    get_template_dir_path,
    get_template_path,
    read_template_from_json_file
)

from .template import Template


class InvalidCaptionLengthError(ValueError):
    def __init__(self, expected_length, actual_length):
        super().__init__(
            "Invalid number of captions was specified. This template only "
            f"accepts {expected_length}, {actual_length} specified."
        )


def load_template(uid: str) -> Template:
    path = get_template_path(uid)
    template = read_template_from_json_file(uid, path)

    return template


def load_templates() -> List[Template]:
    templates = []

    for path in get_template_dir_path().iterdir():
        template = read_template_from_json_file(path.stem, path)
        templates.append(template)

    return templates


def render(template: Template, captions: Sequence[str]) -> Image:
    text_area_length = len(template.text_areas)
    caption_length = len(captions)

    if caption_length != text_area_length:
        raise InvalidCaptionLengthError(text_area_length, caption_length)

    with Image(filename=template.image_path) as image:
        with Drawing() as drawing:
            for area, caption in zip(template.text_areas, captions):
                drawing.font = str(area.text.font_path)
                drawing.font_size = area.text.size

                draw_bounded_text(
                    drawing,
                    image,
                    caption,
                    area.text.align,
                    area.text.position,
                    area.bounds.pad(area.padding)
                )

            drawing.draw(image)

        return Image(image)
