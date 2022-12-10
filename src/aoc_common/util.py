from pathlib import Path
from typing import Iterable


def get_file_path(year: int, day: int) -> Path:
    return Path(__file__).parent.parent / f'aoc{year:d}/data/day{day:d}.txt'


def get_file_content(year: int, day: int) -> str:
    with open(get_file_path(year, day)) as f:
        return f.read().strip('\n')


def get_file_content_lazy(year: int, day: int) -> Iterable[str]:
    with open(get_file_path(year, day)) as f:
        for line in f:
            yield line.strip()
