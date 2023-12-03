import operator
from typing import Callable

import numpy as np
from toolz import curried, valfilter

from aoc_common import get_file_lines
import gem

"""
This one is pretty ugly. I'd much rather avoid the tedious loops,
    or at least have only one version of it that is a bit more flexible (just like for find_all).

That is just a symptom of a different approach to this problem than I normally take though:
- Normally, I first load all the data in a format that represents the semantics of the data well
- Here I only interpreted the raw data when needing to apply the logic - which means multiple passes
    over the data, and having to repeatedly interpret it. 
    This would be much easier with a 2d math library like:
    - https://github.com/Pithikos/python-rectangles
    - https://www.sympy.org
    - https://pypi.org/project/shapely/
    
"""


def find_all(find_fn: Callable[[str], bool], raw: list[str]):
    for line_idx, line in enumerate(raw):
        for col_idx, char in enumerate(line):
            if find_fn(char):
                yield line_idx, col_idx


def get_parts_total() -> int:
    raw = get_file_lines(2023, 3)

    symbols = set(find_all(lambda char: char not in "0123456789.", raw))
    mask = np.zeros((len(raw), len(raw[0])))
    for line_idx, col_idx in symbols:
        mask[line_idx - 1 : line_idx + 2, col_idx - 1 : col_idx + 2] = 1

    # find part numbers
    part_numbers = []
    for line_idx, line in enumerate(raw):
        num = ""
        is_part_number = False
        # expand each line to make sure we always see the end of the number
        for col_idx, char in enumerate(line + "."):
            if char in "0123456789":
                num += char
                if mask[line_idx, col_idx] == 1:
                    is_part_number = True
            else:
                if num and is_part_number:
                    part_numbers.append(int(num))

                num = ""
                is_part_number = False

    return sum(part_numbers)


def get_gears_total() -> int:
    raw = get_file_lines(2023, 3)

    potential_gears = {pos: [] for pos in find_all('*'.__eq__, raw)}

    # find part numbers for each gear
    for line_idx, line in enumerate(raw):
        num = ""
        connected_gears = set()
        # expand each line to make sure we always see the end of the number
        for col_idx, char in enumerate(line + "."):
            if char in "0123456789":
                num += char
                for gear_line, gear_col in potential_gears.keys():
                    if (
                        gear_line - 1 <= line_idx <= gear_line + 1
                        and gear_col - 1 <= col_idx <= gear_col + 1
                    ):
                        connected_gears.add((gear_line, gear_col))
            else:
                if num:
                    for connected_gear in connected_gears:
                        potential_gears[connected_gear].append(int(num))

                num = ""
                connected_gears = set()

    gears = valfilter(lambda x: len(x) == 2, potential_gears)
    return sum(map(curried.reduce(operator.mul), gears.values()))


if __name__ == "__main__":
    print(get_parts_total())
    print(get_gears_total())
