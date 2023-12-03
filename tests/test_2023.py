from aoc2023 import day_1, day_2, day_3, day_4


def test_day1():
    assert day_1.calibrate(parse_first=False) == 142


def test_day1_pt2(alt_test_input):
    assert day_1.calibrate(parse_first=True) == 281


def test_day2():
    assert day_2.solve_cubes() == 8


def test_day2_pt2():
    assert day_2.get_total_power() == 2286


def test_day3():
    assert day_3.get_parts_total() == 4361


def test_day3_pt2():
    assert day_3.get_gears_total() == 467835


def test_day4():
    assert day_4.do_something() == ...
