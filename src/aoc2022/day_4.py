from itertools import starmap

import toolz
from parse import parse

from aoc_common import get_file_content


def get_elf_ranges() -> list[tuple[set[int], set[int]]]:
    raw = get_file_content(2022, 4)

    def parse_line(line: str) -> tuple[set[int], set[int]]:
        parsed = parse('{elf1from:d}-{elf1to:d},{elf2from:d}-{elf2to:d}', line)
        return (
            set(range(parsed.named['elf1from'], parsed['elf1to'] + 1)),
            set(range(parsed.named['elf2from'], parsed['elf2to'] + 1))
        )

    return toolz.thread_last(
        raw.split('\n'),
        (map, parse_line),
        list
    )


def count_fully_contained():
    def fully_contained(left: set[int], right: set[int]) -> bool:
        return set.issubset(left, right) or set.issubset(right, left)

    return sum(starmap(fully_contained, get_elf_ranges()))


def count_overlapping():
    def fully_contained(left: set[int], right: set[int]) -> bool:
        return bool(set.intersection(left, right))

    return sum(starmap(fully_contained, get_elf_ranges()))


if __name__ == "__main__":
    print(count_fully_contained())
    print(count_overlapping())
