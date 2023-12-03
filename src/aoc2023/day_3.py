import operator
import re
from math import sqrt
from typing import Callable

from sympy import Point2D as Point, Polygon
from toolz import keyfilter, valfilter

from aoc_common import get_file_lines


def find_all(find_fn: Callable[[str], bool], raw: list[str]):
    for line_idx, line in enumerate(raw):
        for col_idx, char in enumerate(line):
            if find_fn(char):
                yield line_idx, col_idx


def parse() -> tuple[dict, dict]:
    raw = get_file_lines(2023, 3)

    engine_parts = {}
    other_parts = {}

    for line_idx, line in enumerate(raw):
        skip_num = False
        for col_idx, char in enumerate(line):
            if char in "0123456789":
                if not skip_num:
                    found = re.findall(r"\d+", line[col_idx:])[0]
                    rect = Polygon(
                        Point(line_idx, col_idx),
                        Point(line_idx, col_idx + len(found) - 1),
                    )
                    engine_parts[rect] = int(found)
                    skip_num = True
            elif char == ".":
                skip_num = False
            else:
                skip_num = False
                point = Point(line_idx, col_idx)
                other_parts[point] = char

    return engine_parts, other_parts


def get_parts_total() -> int:
    engine_parts, other_parts = parse()
    return sum(
        engine_number
        for engine_part, engine_number in engine_parts.items()
        if min(engine_part.distance(other_part) for other_part in other_parts.keys())
        <= sqrt(2)
    )


def get_gears_total() -> int:
    engine_parts, other_parts = parse()
    gears = valfilter("*".__eq__, other_parts)

    def gear_power(gear: Point) -> int:
        close_parts = keyfilter(
            lambda part: part.distance(gear) <= sqrt(2), engine_parts
        )
        return operator.mul(*close_parts.values()) if len(close_parts) == 2 else 0

    return sum(map(gear_power, gears.keys()))


if __name__ == "__main__":
    print(get_parts_total())
    print(get_gears_total())
