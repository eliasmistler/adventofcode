from enum import Enum
from itertools import starmap

from toolz import pluck, thread_last

from aoc_common import get_file_content


class Figure(int, Enum):
    """Figure. int value is the score associated"""

    Rock = 1
    Paper = 2
    Scissors = 3


class Outcome(int, Enum):
    """Win/Lose/Draw scores"""

    Win = 6
    Draw = 3
    Lose = 0


elf_map = {
    "A": Figure.Rock,
    "B": Figure.Paper,
    "C": Figure.Scissors,
}

our_map = {
    "X": Figure.Rock,
    "Y": Figure.Paper,
    "Z": Figure.Scissors,
}

outcome_map = {
    "X": Outcome.Lose,
    "Y": Outcome.Draw,
    "Z": Outcome.Win,
}

win_pairs = [
    # left wins over right
    (Figure.Rock, Figure.Scissors),
    (Figure.Paper, Figure.Rock),
    (Figure.Scissors, Figure.Paper),
]


def get_outcome(elf_move: Figure, our_move: Figure) -> Outcome:
    if (our_move, elf_move) in win_pairs:
        return Outcome.Win
    elif our_move == elf_move:
        return Outcome.Draw
    else:
        return Outcome.Lose


def score_round(elf_move: Figure, our_move: Figure) -> int:
    return get_outcome(elf_move, our_move).value + our_move.value


def parse_inputs(mapping: dict) -> list[tuple[Figure, Figure]]:
    raw = get_file_content(2022, 2)
    return thread_last(
        raw.split("\n"),
        (map, lambda row: (elf_map[row[0]], mapping[row.strip()[-1]])),
        list,
    )


def score_game(moves: list[tuple[Figure, Figure]]) -> int:
    return sum(starmap(score_round, moves))


def score_game_with_moves() -> int:
    moves = parse_inputs(mapping=our_map)
    return score_game(moves)


def match_outcomes(elf_move: Figure, outcome: Outcome) -> Figure:
    if outcome is Outcome.Draw:
        return elf_move
    elif outcome is Outcome.Win:
        for our_move in Figure:
            if (our_move, elf_move) in win_pairs:
                return our_move
    else:
        for our_move in Figure:
            if elf_move != our_move and (our_move, elf_move) not in win_pairs:
                return our_move


def score_game_with_outcomes() -> int:
    strategy = parse_inputs(mapping=outcome_map)
    our_moves = list(starmap(match_outcomes, strategy))
    all_moves = list(zip(pluck(0, strategy), our_moves))
    return score_game(all_moves)


if __name__ == "__main__":
    print(score_game_with_moves())
    print(score_game_with_outcomes())
