from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Union

import toolz

from solutions.common import get_file_content


@dataclass
class File:
    name: str
    size: int


@dataclass
class Directory:
    name: str
    contents: dict[str, Union['Directory', File]]

    @property
    def size(self) -> int:
        return sum(child.size for child in self.contents.values())

    def __getitem__(self, item):
        return self.contents[item]


def parse_ls_entry(entry: str) -> Union[File, Directory]:
    size, file_name = entry.split(' ')
    if size == 'dir':
        return Directory(file_name, {})
    else:
        return File(file_name, int(size))


def parse_directory_structure() -> Directory:
    raw = get_file_content(day=7)
    commands = raw.split('\n$ ')

    assert commands[0] == '$ cd /', commands[0]
    current_path = Path('/')

    paths = {}

    # collect all data from the commands
    for command in commands[1:]:
        if command.startswith('cd'):
            arg = command.split(' ', 1)[1]
            if arg == '..':
                current_path = current_path.parent
            else:
                current_path = current_path / arg
        elif command.startswith('ls'):
            results = command.split('\n')[1:]
            children = list(map(parse_ls_entry, results))
            paths[current_path] = {c.name: c for c in children}
        else:
            raise Exception(f'Unknown command: {command}')

    # nest the directories correctly
    for path, contents in sorted(paths.items(), key=lambda args: len(str(args[0])), reverse=True):
        if path == Path('/'):
            continue
        paths[path.parent][path.name].contents = contents

    return Directory('/', paths[Path('/')])


def _get_all_folders(root: Directory) -> Iterable[Directory]:
    yield root
    for f in root.contents.values():
        if isinstance(f, Directory):
            yield from _get_all_folders(f)


def sum_of_small_folders(root: Directory) -> int:
    return toolz.thread_last(
        root,
        _get_all_folders,
        (filter, lambda f: f.size < 100000),
        (map, lambda f: f.size),
        sum
    )


def space_to_clean_up(root: Directory, required: int = 30000000, total_filesystem: int = 70000000) -> int:
    return required + root.size - total_filesystem


def get_smallest_dir_for_cleanup(root: Directory, **kwargs) -> Directory:
    min_size = space_to_clean_up(root, **kwargs)
    return toolz.thread_last(
        root,
        _get_all_folders,
        (filter, lambda f: f.size >= min_size),
        toolz.curry(sorted, key=lambda f: f.size),
        toolz.first
    )


if __name__ == "__main__":
    root = parse_directory_structure()
    print(sum_of_small_folders(root))
    print(get_smallest_dir_for_cleanup(root).size)
