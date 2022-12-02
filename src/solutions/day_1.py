from solutions.common import get_file_content


def sum_calories(elf_raw: str) -> int:
    return sum(map(int, elf_raw.strip().split('\n')))


def find_top_chunkiest_elves(top_n: int) -> list[int]:
    raw = get_file_content(day=1)
    all_elves = map(sum_calories, raw.split('\n\n'))
    return sorted(all_elves, reverse=True)[:top_n]


def sum_top_chunkiest_elves(top_n: int) -> int:
    return sum(find_top_chunkiest_elves(top_n))


if __name__ == "__main__":
    print(sum_top_chunkiest_elves(1))
    print(sum_top_chunkiest_elves(3))
