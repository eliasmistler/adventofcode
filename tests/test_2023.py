from aoc2023 import day_1, day_2


def test_day1():
    assert day_1.calibrate(parse_first=False) == 142


def test_day1_pt2(alt_test_input):
    assert day_1.calibrate(parse_first=True) == 281


def test_day2():
    assert day_2.solve_cubes() == 8


def test_day2_pt2():
    assert day_2.get_total_power() == 2286
