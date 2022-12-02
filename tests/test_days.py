from solutions import day_1, day_2


def test_day1():
    assert day_1.sum_top_chunkiest_elves(1) == 24000
    assert day_1.sum_top_chunkiest_elves(3) == 45000


def test_day2():
    assert day_2.score_round(day_2.Figure.Rock, day_2.Figure.Paper) == 8
    assert day_2.score_game_with_moves() == 15


def test_day2_part2():
    assert day_2.match_outcomes(day_2.Figure.Rock, day_2.Outcome.Win) == day_2.Figure.Paper
    assert day_2.score_game_with_outcomes() == 12
