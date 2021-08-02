"""
A utility module for working with command-line arguments.
"""

from typing import List


def parse(text: str) -> List[str]:
    """
    Parse a textual arguments into a list of strings in Unix style.

    This function currently supports:
        * Splitting arguments by spaces, cleaning up redundant spaces
        * String literals using single and double quotes

    :param text: the text to parse the arguments from.
    :return: The parsed arguments as a list of string values.
    """

    length = len(text)
    args = []
    buffer = []

    current_index = 0
    last_index = length - 1

    while current_index < length:
        char = text[current_index]

        if char in ("\"", "'"):
            next_index = current_index + 1
            end_index = text.find(char, next_index)

            if end_index != -1:
                buffer.append(text[next_index:end_index])
                current_index = end_index
            else:
                buffer.append(char)
        elif char == " ":
            if buffer:
                args.append("".join(buffer))
                buffer = []
        else:
            buffer.append(char)

        if current_index == last_index and buffer:
            args.append("".join(buffer))

        current_index += 1

    return args
