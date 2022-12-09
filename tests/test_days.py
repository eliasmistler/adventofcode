from pathlib import Path

from solutions import common, day_1, day_2, day_3, day_4, day_5, day_6, day_7, day_8, day_9


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


def test_day6():
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


def test_day7():
    root = day_7.parse_directory_structure()
    exp = day_7.Directory('/', {
        'a': day_7.Directory('a', {
            'e': day_7.Directory('e', {'i': day_7.File('i', 584)}),
            'f': day_7.File('f', 29116),
            'g': day_7.File('g', 2557),
            'h.lst': day_7.File('h.lst', 62596),
        }),
        'b.txt': day_7.File('b.txt', 14848514),
        'c.dat': day_7.File('c.dat', 8504156),
        'd': day_7.Directory('d', {
            'j': day_7.File('j', 4060174),
            'd.log': day_7.File('d.log', 8033020),
            'd.ext': day_7.File('d.ext', 5626152),
            'k': day_7.File('k', 7214296),
        })
    })

    assert root == exp

    assert root['a']['e'].size == 584
    assert root['a'].size == 94853
    assert root['d'].size == 24933642
    assert root.size == 48381165

    assert day_7.sum_of_small_folders(root) == 95437

    assert day_7.space_to_clean_up(root) == 8381165

    cleanup_dir = day_7.get_smallest_dir_for_cleanup(root)
    assert cleanup_dir.name == 'd'
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


def test_day9_alt(monkeypatch):
    def get_alt_test_file_path(day: int) -> Path:
        return Path(__file__).parent.parent / 'inputs' / f'day{day:d}_test_alt.txt'

    monkeypatch.setattr(common, 'get_file_path', get_alt_test_file_path)

    assert day_9.count_visited_positions(10) == 36
