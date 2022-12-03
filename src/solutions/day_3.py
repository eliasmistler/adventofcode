from string import ascii_letters

import toolz

from solutions.common import get_file_content

priority_map = dict(zip(ascii_letters, range(1, 53)))


def split_compartments(rucksack: str) -> tuple[str, str]:
    mid = int(len(rucksack) / 2)
    return rucksack[:mid], rucksack[mid:]


def load_rucksacks():
    raw = get_file_content(day=3)
    return raw.split('\n')


def find_common_item(collections):
    return ''.join(set.intersection(*map(set, collections)))


def part1_find_common_items_between_compartments():
    return toolz.thread_last(
        load_rucksacks(),
        (map, split_compartments),
        (map, find_common_item),
        (map, priority_map.get),
        sum
    )


def part2_find_badges_in_elf_groups() -> list[tuple[str, str, str]]:
    return toolz.thread_last(
        load_rucksacks(),
        toolz.curried.partition(3),
        (map, find_common_item),
        (map, priority_map.get),
        sum
    )


if __name__ == "__main__":
    print(part1_find_common_items_between_compartments())
    print(part2_find_badges_in_elf_groups())
