"""
A module containing concepts common across the whole project.
"""


class Rect:
    """
    This class represents a rectangle defined by its upper-left and
    bottom-right point coordinates.
    """

    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.width = x2 - x1
        self.height = y2 - y1

    def pad(self, padding: int) -> "Rect":
        """
        Construct a new rectangle by applying a padding to this one.

        :param padding: the size of the padding to be applied.
        :return: A new :class:`Rect` instance with newly calculated
            coordinates.
        """

        return Rect(
            self.x1 + padding,
            self.y1 + padding,
            self.x2 - padding,
            self.y2 - padding
        )
