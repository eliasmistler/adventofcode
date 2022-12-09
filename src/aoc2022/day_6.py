import toolz

from aoc_common import get_file_content


def detect_marker(message: str, marker_length: int) -> int:
    for n_win, window in enumerate(toolz.sliding_window(marker_length, message)):
        if len(set(window)) == marker_length:
            return n_win + marker_length


if __name__ == "__main__":
    raw = get_file_content(2022, 6)
    print(detect_marker(raw, 4))
    print(detect_marker(raw, 14))
