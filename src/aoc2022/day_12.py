import logging
import math
import string
from dataclasses import dataclass
from itertools import starmap

import numpy as np
import toolz

from aoc_common import get_file_content

height_conversion = dict(zip(string.ascii_lowercase, range(len(string.ascii_lowercase))))


@dataclass
class Coordinates:
    y: int
    x: int

    def __add__(self, other):
        if not isinstance(other, Coordinates):
            raise NotImplementedError()
        return Coordinates(y=self.y + other.y, x=self.x + other.x)

    def __sub__(self, other):
        if not isinstance(other, Coordinates):
            raise NotImplementedError()
        return Coordinates(y=self.y - other.y, x=self.x - other.x)

    def __iter__(self):
        yield self.y
        yield self.x

    def __hash__(self):
        return hash(tuple(self))

    def in_bounds(self, y: int, x: int) -> bool:
        return (
                0 <= self.y < y
                and
                0 <= self.x < x
        )

    def distance(self, other):
        """euclidean distance"""
        d = self - other
        return math.sqrt(d.y ** 2 + d.x ** 2)


def parse_heightmap() -> tuple[np.array, Coordinates, Coordinates]:
    raw = get_file_content(2022, 12).split('\n')
    heightmap = np.array(
        [
            list(map(height_conversion.get, row.replace('S', 'a').replace('E', 'z')))
            for row in raw
        ],
        int
    )

    def get_pos(letter: str) -> Coordinates:
        return [
            Coordinates(y, row.index(letter))
            for y, row in enumerate(raw)
            if letter in row
        ][0]

    start = get_pos('S')
    end = get_pos('E')
    return heightmap, start, end


NEIGHBOR_DIRECTIONS = [
    Coordinates(0, 1),
    Coordinates(0, -1),
    Coordinates(1, 0),
    Coordinates(-1, 0),
]


def get_distance_map(heightmap: np.array, start: Coordinates, end: Coordinates, inverted: bool = False) -> np.array:
    distances = np.zeros_like(heightmap) - 1
    distances[tuple(start)] = 0
    open_list = [start]
    while open_list:
        position = open_list.pop(0)
        distance = distances[tuple(position)]
        height = heightmap[tuple(position)]

        for direction in NEIGHBOR_DIRECTIONS:
            neighbor = position + direction
            if neighbor.in_bounds(*heightmap.shape):
                neighbor_height = heightmap[tuple(neighbor)]
                neighbor_distance = distances[tuple(neighbor)]

                # condition: can only go up vertically by max. 1 step (but down as far as we want)
                if inverted:
                    condition = (height - neighbor_height) <= 1
                else:
                    condition = (neighbor_height - height) <= 1

                if (
                        condition
                        # only replace if it's better than another path
                        and (neighbor_distance == -1 or (neighbor_distance > distance + 1))
                ):
                    distances[tuple(neighbor)] = distance + 1
                    open_list.append(neighbor)

        # sort to investigate most direct paths first
        # doesn't make much of a difference though as we need the optimal answer so can use a pruned/greedy approach
        open_list = sorted(open_list, key=lambda pos: end.distance(pos))

    return distances


def find_shortest_path(heightmap: np.array, start: Coordinates, end: Coordinates) -> int:
    distances = get_distance_map(heightmap, start, end)
    if distances[tuple(end)] != -1:
        return distances[tuple(end)]
    raise Exception('Failed to find a path!')


def find_best_starting_point(heightmap: np.array, start: Coordinates, end: Coordinates) -> tuple[Coordinates, int]:
    distance_from_end = get_distance_map(heightmap, end, start, inverted=True)

    candidates = {
        candidate: int(distance_from_end[tuple(candidate)])
        for candidate in starmap(Coordinates, np.argwhere(heightmap == 0))
    }
    candidates = toolz.valfilter((-1).__ne__, candidates)
    shortest_distance = min(candidates.values())
    candidates = toolz.valfilter(shortest_distance.__eq__, candidates)
    if len(candidates) > 1:
        logging.warning(f'{len(candidates)} starting points with the same distance.')
    return toolz.first(candidates), shortest_distance


if __name__ == "__main__":
    heightmap, start, end = parse_heightmap()
    result = find_shortest_path(heightmap, start, end)
    print(result)

    pos, distance = find_best_starting_point(heightmap, start, end)
    print(distance)
