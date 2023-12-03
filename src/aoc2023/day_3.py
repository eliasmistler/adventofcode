import operator

import numpy as np
from toolz import curried, valfilter

from aoc_common import get_file_lines


def get_parts_total() -> int:
    raw = get_file_lines(2023, 3)
    mask = np.zeros((len(raw), len(raw[0])))

    # mask
    for line_idx, line in enumerate(raw):
        for col_idx, char in enumerate(line):
            if char not in "0123456789.":
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

    potential_gears = {}
    for line_idx, line in enumerate(raw):
        for col_idx, char in enumerate(line):
            if char == "*":
                potential_gears[(line_idx, col_idx)] = []

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
