from pathlib import Path

from pytest import fixture

from aoc_common import util


def get_test_file_path(year: int, day: int) -> Path:
    return Path(__file__).parent / f"data/{year:d}/day{day:d}_test.txt"


@fixture(autouse=True)
def use_test_files(monkeypatch):
    monkeypatch.setattr(util, "get_file_path", get_test_file_path)


@fixture
def alt_test_input(monkeypatch):
    def get_alt_test_file_path(year: int, day: int) -> Path:
        return Path(__file__).parent / f"data/{year:d}/day{day:d}_test_alt.txt"

    monkeypatch.setattr(util, "get_file_path", get_alt_test_file_path)
