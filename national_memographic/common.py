from typing import Tuple


Dims = Tuple[int, int]


class Rect:
    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.width = x2 - x1
        self.height = y2 - y1

    def pad(self, padding: int) -> "Rect":
        return Rect(
            self.x1 + padding,
            self.y1 + padding,
            self.x2 - padding,
            self.y2 - padding
        )
