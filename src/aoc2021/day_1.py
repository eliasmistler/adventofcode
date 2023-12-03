import toolz

from aoc_common import get_file_content


def get_data():
    raw = get_file_content(2021, 1)
    return list(map(int, raw.split("\n")))


def count_increases() -> int:
    return sum(new > old for old, new in toolz.sliding_window(2, get_data()))


def count_increases_w3() -> int:
    data = get_data()
    return sum(
        sum(new) > sum(old)
        for old, new in zip(
            toolz.sliding_window(3, data),
            toolz.sliding_window(3, data[1:]),
        )
    )


if __name__ == "__main__":
    print(count_increases())
    print(count_increases_w3())
