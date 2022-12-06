from solutions import day_1, day_2, day_3, day_4, day_5, day_6


def test_day1():
    assert day_1.sum_top_chunkiest_elves(1) == 24000
    assert day_1.sum_top_chunkiest_elves(3) == 45000


def test_day2():
    assert day_2.score_round(day_2.Figure.Rock, day_2.Figure.Paper) == 8
    assert day_2.score_game_with_moves() == 15

    assert day_2.match_outcomes(day_2.Figure.Rock, day_2.Outcome.Win) == day_2.Figure.Paper
    assert day_2.score_game_with_outcomes() == 12


def test_day3():
    assert day_3.part1_find_common_items_between_compartments() == 157

    assert day_3.part2_find_badges_in_elf_groups() == 70


def test_day4():
    assert day_4.count_fully_contained() == 2

    assert day_4.count_overlapping() == 4


def test_day5():
    stacks_before, instructions = day_5.parse_stacks_and_instructions()
    assert stacks_before == {
        1: ['Z', 'N'],
        2: ['M', 'C', 'D'],
        3: ['P'],
    }

    stacks_after_1 = day_5.apply_instruction(instructions[0], stacks_before, False)
    assert stacks_after_1 == {
        1: ['Z', 'N', 'D'],
        2: ['M', 'C'],
        3: ['P'],
    }

    stacks_final = day_5.apply_instructions(instructions, stacks_before, False)
    assert stacks_final == {
        1: ['C'],
        2: ['M'],
        3: ['P', 'D', 'N', 'Z'],
    }

    assert day_5.apply_and_check_top_crates(False) == 'CMZ'
    assert day_5.apply_and_check_top_crates(True) == 'MCD'


def test_day_6():
    assert day_6.detect_marker('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 4) == 7
    assert day_6.detect_marker('bvwbjplbgvbhsrlpgdmjqwftvncz', 4) == 5
    assert day_6.detect_marker('nppdvjthqldpwncqszvftbrmjlhg', 4) == 6
    assert day_6.detect_marker('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 4) == 10
    assert day_6.detect_marker('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 4) == 11

    assert day_6.detect_marker('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 14) == 19
    assert day_6.detect_marker('bvwbjplbgvbhsrlpgdmjqwftvncz', 14) == 23
    assert day_6.detect_marker('nppdvjthqldpwncqszvftbrmjlhg', 14) == 23
    assert day_6.detect_marker('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 14) == 29
    assert day_6.detect_marker('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 14) == 26
