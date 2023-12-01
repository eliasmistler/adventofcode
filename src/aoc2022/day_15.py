import toolz
from parse import parse

from aoc_common import get_file_content

Point = tuple[int, int]


def parse_points() -> list[tuple[Point, Point]]:
    fmt = "Sensor at x={sx:d}, y={sy:d}: closest beacon is at x={bx:d}, y={by:d}"

    parsed = [
        parse(fmt, row).named
        for row in get_file_content(2022, 15).split('\n')
    ]

    return [
        ((p['sx'], p['sy']), (p['bx'], p['by']))
        for p in parsed
    ]


if __name__ == "__main__":
    points = parse_points()
    known_beacons = set(toolz.pluck(1, points))
