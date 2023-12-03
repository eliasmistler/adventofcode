import json
from functools import cmp_to_key, reduce
from itertools import chain, starmap
from operator import mul

import toolz

from aoc_common import get_file_content


def parse_inputs():
    raw = get_file_content(2022, 13)
    return [
        tuple(map(json.loads, raw_pair.split("\n"))) for raw_pair in raw.split("\n\n")
    ]


def is_right_order(left: list | int, right: list | int) -> bool | None:
    if isinstance(left, int) and isinstance(right, list):
        return is_right_order([left], right)
    elif isinstance(left, list) and isinstance(right, int):
        return is_right_order(left, [right])

    elif isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
        else:
            return left < right

    else:
        assert isinstance(left, list) and isinstance(right, list)
        if len(left) == 0 and len(right) != 0:
            return True
        elif len(left) != 0 and len(right) == 0:
            return False
        elif len(left) == 0 and len(right) == 0:
            return None
        else:
            result = is_right_order(left[0], right[0])
            if result is not None:
                return result
            else:
                return is_right_order(left[1:], right[1:])


def sum_of_correct_order_indices(inputs) -> int:
    return toolz.thread_last(
        inputs,
        (starmap, is_right_order),
        enumerate,
        dict,
        (toolz.valfilter, bool),
        (map, (1).__add__),
        sum,
    )


def get_decoder_key(inputs) -> int:
    divider_signals = [[[2]], [[6]]]

    @cmp_to_key
    def cmp(left, right):
        if left == right:
            return 0
        elif is_right_order(left, right):
            return -1
        else:
            return 1

    all_signals = list(chain(*inputs)) + divider_signals
    correct_order = sorted(all_signals, key=cmp)
    return toolz.thread_last(
        divider_signals, (map, correct_order.index), (map, (1).__add__), (reduce, mul)
    )


if __name__ == "__main__":
    inputs = parse_inputs()
    print(sum_of_correct_order_indices(inputs))  # 5366
    print(get_decoder_key(inputs))  # 23391
