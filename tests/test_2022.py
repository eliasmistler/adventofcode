from collections import deque
from itertools import starmap
from pathlib import Path

from aoc2022 import (
    day_1,
    day_10,
    day_11,
    day_12,
    day_13,
    day_14,
    day_2,
    day_3,
    day_4,
    day_5,
    day_6,
    day_7,
    day_8,
    day_9,
)
from aoc_common import util


def test_day1():
    assert day_1.sum_top_chunkiest_elves(1) == 24000
    assert day_1.sum_top_chunkiest_elves(3) == 45000


def test_day2():
    assert day_2.score_round(day_2.Figure.Rock, day_2.Figure.Paper) == 8
    assert day_2.score_game_with_moves() == 15

    assert (
        day_2.match_outcomes(day_2.Figure.Rock, day_2.Outcome.Win) == day_2.Figure.Paper
    )
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
        1: ["Z", "N"],
        2: ["M", "C", "D"],
        3: ["P"],
    }

    stacks_after_1 = day_5.apply_instruction(instructions[0], stacks_before, False)
    assert stacks_after_1 == {
        1: ["Z", "N", "D"],
        2: ["M", "C"],
        3: ["P"],
    }

    stacks_final = day_5.apply_instructions(instructions, stacks_before, False)
    assert stacks_final == {
        1: ["C"],
        2: ["M"],
        3: ["P", "D", "N", "Z"],
    }

    assert day_5.apply_and_check_top_crates(False) == "CMZ"
    assert day_5.apply_and_check_top_crates(True) == "MCD"


def test_day6():
    assert day_6.detect_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 4) == 7
    assert day_6.detect_marker("bvwbjplbgvbhsrlpgdmjqwftvncz", 4) == 5
    assert day_6.detect_marker("nppdvjthqldpwncqszvftbrmjlhg", 4) == 6
    assert day_6.detect_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4) == 10
    assert day_6.detect_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4) == 11

    assert day_6.detect_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14) == 19
    assert day_6.detect_marker("bvwbjplbgvbhsrlpgdmjqwftvncz", 14) == 23
    assert day_6.detect_marker("nppdvjthqldpwncqszvftbrmjlhg", 14) == 23
    assert day_6.detect_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14) == 29
    assert day_6.detect_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14) == 26


def test_day7():
    root = day_7.parse_directory_structure()
    exp = day_7.Directory(
        "/",
        {
            "a": day_7.Directory(
                "a",
                {
                    "e": day_7.Directory("e", {"i": day_7.File("i", 584)}),
                    "f": day_7.File("f", 29116),
                    "g": day_7.File("g", 2557),
                    "h.lst": day_7.File("h.lst", 62596),
                },
            ),
            "b.txt": day_7.File("b.txt", 14848514),
            "c.dat": day_7.File("c.dat", 8504156),
            "d": day_7.Directory(
                "d",
                {
                    "j": day_7.File("j", 4060174),
                    "d.log": day_7.File("d.log", 8033020),
                    "d.ext": day_7.File("d.ext", 5626152),
                    "k": day_7.File("k", 7214296),
                },
            ),
        },
    )

    assert root == exp

    assert root["a"]["e"].size == 584
    assert root["a"].size == 94853
    assert root["d"].size == 24933642
    assert root.size == 48381165

    assert day_7.sum_of_small_folders(root) == 95437

    assert day_7.space_to_clean_up(root) == 8381165

    cleanup_dir = day_7.get_smallest_dir_for_cleanup(root)
    assert cleanup_dir.name == "d"
    assert cleanup_dir.size == 24933642


def test_day8():
    trees = day_8.get_trees()
    mask = day_8.score_trees(trees, day_8.ScoreMode.is_visible)
    exp_mask = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 0, 1],
        [1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1],
    ]
    assert (mask == exp_mask).all()

    scores = day_8.score_trees(trees, day_8.ScoreMode.scenic_score)
    exp_scores = [
        [0, 0, 0, 0, 0],
        [0, 1, 4, 1, 0],
        [0, 6, 1, 2, 0],
        [0, 1, 8, 3, 0],
        [0, 0, 0, 0, 0],
    ]
    assert (scores == exp_scores).all()

    assert day_8.get_max_possible_score(trees) == 16


def test_day9():
    assert day_9.count_visited_positions(2) == 13
    assert day_9.count_visited_positions(10) == 1


def test_day9_alt(alt_test_input):
    assert day_9.count_visited_positions(10) == 36


def test_day10():
    observations, screen = day_10.run_instructions()
    assert observations == [420, 1140, 1800, 2940, 2880, 3960]
    exp_screen = [
        "##..##..##..##..##..##..##..##..##..##..",
        "###...###...###...###...###...###...###.",
        "####....####....####....####....####....",
        "#####.....#####.....#####.....#####.....",
        "######......######......######......####",
        "#######.......#######.......#######.....",
    ]
    assert screen == exp_screen


def test_day11():
    monkeys = day_11.parse_monkeys()
    day_11.play(monkeys, 20, False)

    assert monkeys[0].items == deque([10, 12, 14, 26, 34])
    assert monkeys[1].items == deque([245, 93, 53, 199, 115])
    assert monkeys[2].items == deque([])
    assert monkeys[3].items == deque([])

    assert day_11.calculate_monkey_business(monkeys) == 10605

    # part 2
    monkeys = day_11.parse_monkeys()
    day_11.play(monkeys, 10000, True)
    assert day_11.calculate_monkey_business(monkeys) == 2713310158


def test_day12():
    heightmap, start, end = day_12.parse_heightmap()
    result = day_12.find_shortest_path(heightmap, start, end)
    assert result == 31

    pos, distance = day_12.find_best_starting_point(heightmap, start, end)
    assert pos == day_12.Coordinates(4, 0)
    assert distance == 29


def test_day13():
    inputs = day_13.parse_inputs()
    assert list(starmap(day_13.is_right_order, inputs)) == [
        True,
        True,
        False,
        True,
        False,
        True,
        False,
        False,
    ]
    assert day_13.sum_of_correct_order_indices(inputs) == 13

    assert day_13.get_decoder_key(inputs) == 140


def test_day14():
    assert day_14.simulate_and_count() == 24
    assert day_14.simulate_and_count(True) == 93
