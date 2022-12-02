from pathlib import Path

from pytest import fixture

import solutions.common


def get_test_file_path(day: int) -> Path:
    folder = Path(__file__).parent.parent / 'inputs'
    return folder / f'day{day}_test.txt'


@fixture(autouse=True)
def use_test_files(monkeypatch):
    monkeypatch.setattr(solutions.common, 'get_file_path', get_test_file_path)
