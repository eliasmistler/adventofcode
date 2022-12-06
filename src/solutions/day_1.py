import toolz

from solutions.common import get_file_content


def sum_calories(elf_raw: str) -> int:
    return sum(map(int, elf_raw.strip().split('\n')))


def sum_top_chunkiest_elves(top_n: int) -> list[int]:
    raw = get_file_content(day=1)
    return toolz.thread_last(
        raw.split('\n\n'),
        (map, sum_calories),
        sorted,
        reversed,
        toolz.curried.take(top_n),
        sum
    )


if __name__ == "__main__":
    print(sum_top_chunkiest_elves(1))
    print(sum_top_chunkiest_elves(3))
