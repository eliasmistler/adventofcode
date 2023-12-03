from enum import Enum
from functools import reduce

import numpy as np
from numpy import multiply

from aoc_common import get_file_content


def get_trees() -> np.array:
    raw = get_file_content(2022, 8)
    return np.array([np.fromiter(list(row), int) for row in raw.split("\n")])


class ScoreMode(Enum):
    is_visible = 1
    scenic_score = 2


def score_trees(trees: np.array, mode: ScoreMode) -> np.array:
    mode = ScoreMode(mode)

    scores = np.zeros_like(trees)

    if mode == ScoreMode.is_visible:
        # all edge trees are visible
        scores[:, 0] = 1
        scores[:, -1] = 1
        scores[0, :] = 1
        scores[-1, :] = 1
    # otherwise: all edge trees have score 0 -> nop;

    # now apply logic
    for y in range(1, trees.shape[0] - 1):
        for x in range(1, trees.shape[1] - 1):
            height = trees[y, x]
            view_ranges = [
                trees[y, :x][::-1],  # look left
                trees[y, x + 1 :],  # look right
                trees[:y, x][::-1],  # look up
                trees[y + 1 :, x],  # look down
            ]
            if mode == ScoreMode.is_visible:
                if any((height > view_range.max()) for view_range in view_ranges):
                    scores[y, x] = 1
            else:

                def score_range(r) -> int:
                    n = 0
                    for tree in r:
                        n += 1
                        if tree >= height:
                            break
                    return n

                scores[y, x] = reduce(multiply, map(score_range, view_ranges))

    return scores


def get_max_possible_score(trees: np.array) -> int:
    """
    find the best position, best case scenic score
    In the best case scenario we see all trees above, below, left and right
    from the positions, so the max score for a position is simply
    the product x * (n_cols - x - 1) * y * (n_rows - y - 1).

    We also know that a product of two numbers that add up to the same sum is
    always greater the closer the numbers are together -- e.g. 2*2 is greater than 3*1,
    i.e. the best possible view will always be the middle of the grid.
    """
    n_rows, n_cols = trees.shape
    x = n_cols // 2
    y = n_rows // 2
    return x * (n_cols - x - 1) * y * (n_rows - y - 1)


if __name__ == "__main__":
    trees = get_trees()
    mask = score_trees(trees, ScoreMode.is_visible)
    n_visible_trees = mask.sum()
    print(n_visible_trees)
    scores = score_trees(trees, ScoreMode.scenic_score)
    max_actual_score = scores.max()
    print(max_actual_score)

    # The exercise asks for the "maximum possible" score, so the
    # implementation below would imo create the correct answer to
    # that question.
    # The actual accepted answer was the highest scenic score of an
    # actual tree though.
    print(get_max_possible_score(trees))
