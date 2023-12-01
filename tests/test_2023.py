from aoc2023 import day_1


def test_day1():
    assert day_1.calibrate(parse_first=False) == 142


def test_day1_alt(alt_test_input):
    assert day_1.calibrate(parse_first=True) == 281
