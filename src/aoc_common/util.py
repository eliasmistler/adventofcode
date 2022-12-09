from pathlib import Path


def get_file_path(year: int, day: int) -> Path:
    return Path(__file__).parent.parent / f'aoc{year:d}/data/day{day:d}.txt'


def get_file_content(year: int, day: int) -> str:
    with open(get_file_path(year, day)) as f:
        return f.read().strip('\n')
