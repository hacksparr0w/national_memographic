from typing import List


def parse(text: str) -> List[str]:
    length = len(text)
    args = []
    buffer = []

    current_index = 0
    last_index = length - 1

    while current_index < length:
        char = text[current_index]

        if char == "\"" or char == "'":
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
