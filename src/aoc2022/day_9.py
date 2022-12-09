from enum import Enum
from typing import Iterable

from parse import parse

from aoc_common import get_file_content


class Move(Enum):
    U = (-1, 0)
    D = (1, 0)
    L = (0, -1)
    R = (0, 1)


class Marker(int, Enum):
    empty = 0
    visited = 1
    start = -1
    head = 2
    tail = 3


def parse_moves() -> list[Move]:
    raw = get_file_content(2022, 9)
    parsed = (
        parse('{move} {steps:d}', row)
        for row in raw.split('\n')
    )
    return [
        getattr(Move, d.named['move'])
        for d in parsed
        for _ in range(d.named['steps'])
    ]


def get_head_positions(moves: list[Move]) -> Iterable[tuple[int, int]]:
    y, x = 0, 0
    for move in moves:
        y += move.value[0]
        x += move.value[1]
        yield y, x


def get_tail_positions(head_positions: Iterable[tuple[int, int]]) -> Iterable[tuple[int, int]]:
    y, x = 0, 0
    for head_y, head_x in head_positions:
        # straight move - vertical
        if y == head_y and abs(x - head_x) == 2:
            x = (x + head_x) // 2

        # straight move -- horizontal
        elif x == head_x and abs(y - head_y) == 2:
            y = (y + head_y) // 2

        # diagonal moves
        elif x != head_x and y != head_y:
            x_diff = head_x - x
            y_diff = head_y - y
            if max(abs(x_diff), abs(y_diff)) > 1:
                x = x + (x_diff // abs(x_diff))
                y = y + (y_diff // abs(y_diff))

        yield y, x


def count_visited_positions(rope_length: int) -> int:
    moves = parse_moves()
    head_positions = list(get_head_positions(moves))
    positions = head_positions
    for knot in range(rope_length - 1):
        positions = list(get_tail_positions(positions))
    return len(set(positions))


if __name__ == "__main__":
    print(count_visited_positions(2))
    print(count_visited_positions(10))
