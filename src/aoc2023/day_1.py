import string
from functools import partial

from toolz import first, last, thread_first

from aoc_common import get_file_lines

word_map = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def calibrate_line(line: str, parse_first: bool) -> int:
    if parse_first:
        line = thread_first(
            line,
            # {word}{digit}{word} is a bit silly, but it works in making sure that digit overlaps are considered
            *((str.replace, word, f"{word}{digit}{word}") for word, digit in word_map.items()),
        )
    digits = list(filter(string.digits.__contains__, line))
    return int(first(digits) + last(digits))


def calibrate(parse_first: bool):
    return sum(map(partial(calibrate_line, parse_first=parse_first),
                   get_file_lines(2023, 1)))


if __name__ == "__main__":
    print(calibrate(parse_first=False))
    print(calibrate(parse_first=True))
