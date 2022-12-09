from pathlib import Path

from pytest import fixture

import solutions.common


def get_test_file_path(day: int) -> Path:
    return Path(__file__).parent.parent / 'inputs' / f'day{day:d}_test.txt'


@fixture(autouse=True)
def use_test_files(monkeypatch):
    monkeypatch.setattr(solutions.common, 'get_file_path', get_test_file_path)
