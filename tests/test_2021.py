from aoc2021 import day_1, day_2


def test_day1():
    assert day_1.count_increases() == 7
    assert day_1.count_increases_w3() == 5


def test_day2():
    assert day_2.calc_new_position_int(day_2.follow_instructions_v1) == 150
    assert day_2.calc_new_position_int(day_2.follow_instructions_v2) == 900
