from enum import Enum
from functools import reduce
from operator import mul
from typing import Callable

import toolz

from aoc_common import get_file_content


class Direction(Enum):
    forward = (1, 0)
    down = (0, 1)
    up = (0, -1)


Instruction = tuple[Direction, int]
Position = tuple[int, int]


def parse_instructions() -> list[Instruction]:
    return [
        (Direction[row.split(" ")[0]], int(row.split(" ")[1]))
        for row in get_file_content(2021, 2).split("\n")
    ]


def follow_instructions_v1(instructions: list[Instruction]) -> Position:
    x, y = 0, 0
    for direction, distance in instructions:
        dx, dy = direction.value
        x = x + dx * distance
        y = y + dy * distance
    return x, y


def follow_instructions_v2(instructions: list[Instruction]):
    x, y, aim = 0, 0, 0
    for direction, multiplier in instructions:
        d_move, d_aim = direction.value
        aim += d_aim * multiplier
        x += d_move * multiplier
        y += aim * d_move * multiplier
    return x, y


def calc_new_position_int(fn_follow_instructions: Callable) -> int:
    return toolz.thread_last(
        parse_instructions(), fn_follow_instructions, (reduce, mul)
    )


if __name__ == "__main__":
    print(calc_new_position_int(follow_instructions_v1))
    print(calc_new_position_int(follow_instructions_v2))
