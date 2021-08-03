from typing import List

import pytest

from national_memographic._args import parse


@pytest.mark.parametrize("text, args", [
    ("meme ls", ["meme", "ls"]),
    ("meme    ls", ["meme", "ls"]),
    ("meme 'ls'", ["meme", "ls"]),
    ("meme generate a \"b c\" 'd e'", ["meme", "generate", "a", "b c", "d e"])
])
def test_parse(text: str, args: List[str]) -> None:
    assert parse(text) == args
