from pathlib import Path


def get_file_path(day: int) -> Path:
    folder = Path(__file__).parent.parent.parent / 'inputs'
    return folder / f'day{day}.txt'


def get_file_content(day: int) -> str:
    with open(get_file_path(day)) as f:
        return f.read().strip('\n')
