import operator as op
from functools import reduce

from toolz import get, merge_with, valfilter, valmap

from aoc_common import get_file_lines

AVAILABLE_CUBES = {"red": 12, "green": 13, "blue": 14}


def parse_games(raw_lines: list[str]) -> dict:
    return {
        int(raw_line.split(":")[0].split(" ")[1]): [
            {
                entry.strip(" ").split(" ")[1]: int(entry.strip(" ").split(" ")[0])
                for entry in round_.split(",")
            }
            for round_ in raw_line.split(":")[1].split(";")
        ]
        for raw_line in raw_lines
    }


def get_minimum_sets_per_game() -> dict[int, dict[str, int]]:
    raw_lines = get_file_lines(2023, 2)
    games = parse_games(raw_lines)
    return {game_id: merge_with(max, *rounds) for game_id, rounds in games.items()}


def is_game_possible(min_cubes: dict[str, int]) -> bool:
    remaining = merge_with(
        lambda args: (args[0] - get(1, args, 0)), AVAILABLE_CUBES, min_cubes
    )
    return all(map((0).__le__, remaining.values()))


def solve_cubes() -> int:
    return sum(valfilter(is_game_possible, get_minimum_sets_per_game()).keys())


def cube_set_power(min_cubes: dict[str, int]) -> int:
    return reduce(op.mul, min_cubes.values())


def get_total_power() -> int:
    return sum(valmap(cube_set_power, get_minimum_sets_per_game()).values())


if __name__ == "__main__":
    print(solve_cubes())
    print(get_total_power())
