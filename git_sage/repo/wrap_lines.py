import textwrap


def wrap_lines(text: str) -> str:
    text = text.strip()
    accumulator = []
    for line in text.splitlines():
        line = '\n'.join(textwrap.wrap(line, 72))
        accumulator.append(line)
    return '\n'.join(accumulator)
