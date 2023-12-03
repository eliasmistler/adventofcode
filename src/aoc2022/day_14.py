from itertools import chain

import numpy as np
import toolz

from aoc_common import get_file_content

AIR = 0
ROCK = 1
SAND = 2
SAND_START = -1

Position = tuple[int, int]


def parse_cave_map(with_floor: bool):
    """
    Parse the map of the cave.
    Implementation note: Uses original coordinates as the primary coordinate system, i.e.
                         (x,y) format with (500,0) as the start,
                         but creates a numpy array that doesn't fit that same coordinate system.
    """
    # parse the paths as list of coordinates
    paths = [
        [tuple(map(int, position.split(","))) for position in path.split(" -> ")]
        for path in get_file_content(2022, 14).split("\n")
    ]
    sand_start = (500, 0)

    # find edges of the relevant map area
    all_points = list(chain(*paths)) + [sand_start]
    x_min = min(toolz.pluck(0, all_points)) - 1
    x_max = max(toolz.pluck(0, all_points)) + 1
    y_min = min(toolz.pluck(1, all_points))
    y_max = max(toolz.pluck(1, all_points))

    # if there is a floor, adjust map size generously to accommodate for sand falling to either side
    if with_floor:
        y_max += 2
        height = y_max - y_min + 1
        x_min -= height
        x_max += height

    def draw(pos_a: Position, pos_b: Position, what: int):
        """draw a straight line from :pos_a to :pos_b into the cave_map"""
        # split points
        (x_from, y_from) = pos_a
        (x_to, y_to) = pos_b
        # sort coordinates for numpy
        (x_from, x_to) = min(x_from, x_to), max(x_from, x_to)
        (y_from, y_to) = min(y_from, y_to), max(y_from, y_to)
        # now draw into cave_map, adjusted by offsets
        cave_map[
            (y_from - y_min) : (y_to - y_min + 1), (x_from - x_min) : (x_to - x_min + 1)
        ] = what

    # create the cave_map as a numpy array, fill in rocks, start point and floor if required
    cave_map = np.zeros((y_max - y_min + 1, x_max - x_min + 1), dtype=int)
    [draw(p1, p2, ROCK) for path in paths for p1, p2 in toolz.sliding_window(2, path)]
    draw(sand_start, sand_start, SAND_START)
    if with_floor:
        draw((x_min, y_max), (x_max, y_max), ROCK)
    return cave_map


def simulate_sand(cave_map: np.array) -> np.array:
    """
    Simulate the trickling of sand down into the cave map.
    Implementation note: The coordinates in here have nothing to do with the original coordinates in the source file.
                         Instead, we use the numpy-style coordinates, i.e. (y, x), with (0,0) being the top left corner
    """
    start: Position = toolz.first(zip(*np.where(cave_map == SAND_START)))

    found_resting_place = True
    while found_resting_place:
        found_resting_place = False

        # for each sand, start at the start location
        (y, x) = start

        # keep going until sand gets to rest or leaves the map
        while y + 1 < cave_map.shape[0] and not found_resting_place:
            for target in [
                (y + 1, x),  # under
                (y + 1, x - 1),  # left diagonal
                (y + 1, x + 1),  # right diagonal
            ]:
                moved = False
                if cave_map[target] == AIR:
                    (y, x) = target
                    moved = True
                    break
            found_resting_place = not moved

            # end condition: sand found a resting place -> draw into map.
            if found_resting_place:
                cave_map[y, x] = SAND
                # make sure to stop if it blocks the starting point
                if (y, x) == start:
                    return cave_map

    return cave_map


def simulate_and_count(with_floor: bool = False) -> int:
    cave_map = toolz.pipe(parse_cave_map(with_floor=with_floor), simulate_sand)
    return int((cave_map == SAND).sum())


if __name__ == "__main__":
    print(simulate_and_count())
    print(simulate_and_count(with_floor=True))
