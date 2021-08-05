"""
The core API used for programmatic meme generation.
"""

from typing import List, Sequence

from wand.drawing import Drawing  # type: ignore
from wand.image import Image  # type: ignore

from ._image import draw_bounded_text
from .data import (
    get_template_dir_path,
    get_template_path,
    read_template_from_json_file
)

from .template import Template


class InvalidCaptionLengthError(ValueError):
    """
    An error raised uppon attempting to capture an image with different number
    of captions than specified in used template.
    """

    def __init__(self, expected_length: int, actual_length: int) -> None:
        super().__init__(
            "Invalid number of captions was specified. This template only "
            f"accepts {expected_length}, {actual_length} specified."
        )


class UnknownTemplateUidError(Exception):
    """
    Thrown when no template is found for given template UID.
    """

    def __init__(self, uid: str) -> None:
        super().__init__(f"No template with UID '{uid}' found")

        self.uid = uid


def load_template(uid: str) -> Template:
    """
    Loads a template by its UID.

    :param uid: a UID of a template.
    :return: A :class:`Template` object of the given UID.
    :raises UnknownTemplateUidError: if no template with the given UID exists.
    """

    path = get_template_path(uid)

    try:
        template = read_template_from_json_file(uid, path)
    except FileNotFoundError:
        raise UnknownTemplateUidError(uid)  # pylint: disable=W0707

    return template


def load_templates() -> List[Template]:
    """
    Loads all know templates.

    :return: A list of :class:`Template` objects
    """

    templates = []

    for path in get_template_dir_path().iterdir():
        template = read_template_from_json_file(path.stem, path)
        templates.append(template)

    return templates


def caption(template: Template, captions: Sequence[str]) -> Image:
    """
    Creates an :class:`Image` object by applying captions to a given
    template.

    :param template: a template to be used when generating the image.
    :param captions: a sequence of captions to be used.
    :return: A resultant :class:`Image` object
    """

    text_areas = template.text_areas
    text_area_length = len(text_areas)
    caption_length = len(captions)

    if text_area_length != caption_length:
        raise InvalidCaptionLengthError(text_area_length, caption_length)

    with Image(filename=template.image_path) as image:
        with Drawing() as drawing:
            for area, text in zip(text_areas, captions):
                draw_bounded_text(
                    drawing,
                    image,
                    area.bounds.pad(area.padding),
                    area.text_style,
                    text
                )

            drawing.draw(image)

        return Image(image)
