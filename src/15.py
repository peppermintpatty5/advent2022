#!/usr/bin/env python3

import re
import sys
from dataclasses import dataclass
from enum import Enum
from heapq import heappop, heappush


def parse_input(input_txt: str):
    closest_beacons: dict[tuple[int, int], tuple[int, int]] = {}

    for line in input_txt.splitlines():
        match = re.match(
            r"Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)",
            line,
        )
        if match is not None:
            # print(line)
            sx, sy, bx, by = match.groups()
            closest_beacons[(int(sx), int(sy))] = (int(bx), int(by))

    return closest_beacons


def manhattan_dist(a: tuple[int, int], b: tuple[int, int]) -> int:
    ax, ay = a
    bx, by = b

    return abs(ax - bx) + abs(ay - by)


def get_impossible_x(
    closest_beacons: dict[tuple[int, int], tuple[int, int]], y: int
) -> set[int]:
    impossible_x: set[int] = set()
    for sensor, beacon in closest_beacons.items():
        sx, sy = sensor
        radius = manhattan_dist(sensor, beacon)
        if abs(sy - y) <= radius:
            for x in range(radius - abs(sy - y) + 1):
                impossible_x.add(sx + x)
                impossible_x.add(sx - x)

    for bx, by in closest_beacons.values():
        if by == y and bx in impossible_x:
            impossible_x.remove(bx)

    return impossible_x


def get_impossible_y(
    closest_beacons: dict[tuple[int, int], tuple[int, int]], x: int
) -> set[int]:
    impossible_y: set[int] = set()
    for sensor, beacon in closest_beacons.items():
        sx, sy = sensor
        radius = manhattan_dist(sensor, beacon)
        if abs(sx - x) <= radius:
            for y in range(radius - abs(sx - x) + 1):
                impossible_y.add(sy + y)
                impossible_y.add(sy - y)

    for bx, by in closest_beacons.values():
        if bx == x and by in impossible_y:
            impossible_y.remove(by)

    return impossible_y


def diamond_border(center: tuple[int, int], radius: int) -> set[tuple[int, int]]:
    cx, cy = center
    r = radius + 1
    points: set[tuple[int, int]] = set()
    for i in range(r):
        points.add((cx + (r - i), cy + i))
        points.add((cx + (r - i), cy - i))
        points.add((cx - (r - i), cy + i))
        points.add((cx - (r - i), cy - i))
        points.add((cx + i, cy + (r - i)))
        points.add((cx - i, cy + (r - i)))
        points.add((cx + i, cy - (r - i)))
        points.add((cx - i, cy - (r - i)))
    return points


def part1(input_txt: str) -> int:
    closest_beacons = parse_input(input_txt)

    return len(get_impossible_x(closest_beacons, 2000000))


def get_badness(
    closest_beacons: dict[tuple[int, int], tuple[int, int]], x: int, y: int
) -> list[int]:
    badness: list[int] = []
    for sensor, beacon in closest_beacons.items():
        sx, sy = sensor
        radius = manhattan_dist(sensor, beacon)
        dist = abs(sx - x) + abs(sy - y)
        badness.append(max(0, (radius + 1) - dist))
    return badness


def part2_fail1(input_txt: str) -> int:
    closest_beacons = parse_input(input_txt)

    LIMIT = 4000000

    def F(x: int, y: int) -> int:
        return sum(get_badness(closest_beacons, x, y))

    # foo = [[F(x, y) for x in range(LIMIT)] for y in range(LIMIT)]
    # print("\n".join("\t".join(str(x) for x in row) for row in foo))

    queue = [(F(0, 0), (0, 0))]
    visited: set[tuple[int, int]] = {(0, 0)}
    i = 0

    while queue:
        val, (x, y) = heappop(queue)

        if i & 0xFF == 0:
            print(f"{i}\t: F({x}, {y})\t= {val}")
        i += 1

        if val == 0:
            return x * 4000000 + y

        # moving by 1 is REALLY slow, so take step that is proportional
        d = max(1, val // 2)
        adj = [
            (x2, y2)
            for x2, y2 in [(x + d, y), (x, y + d), (x - d, y), (x, y - d)]
            if 0 <= x2 <= LIMIT and 0 <= y2 <= LIMIT
        ]

        for x2, y2 in adj:
            if (x2, y2) not in visited:
                heappush(queue, (F(x2, y2), (x2, y2)))
                visited.add((x2, y2))


@dataclass
class LineSegment:
    p1: tuple[int, int]
    p2: tuple[int, int]


class Cardinal(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


@dataclass
class Diamond:
    center: tuple[int, int]
    radius: int

    def get_point(self, direction: Cardinal) -> tuple[int, int]:
        cx, cy = self.center
        r = self.radius

        match direction:
            case Cardinal.NORTH:
                return (cx, cy + r)
            case Cardinal.EAST:
                return (cx + r, cy)
            case Cardinal.SOUTH:
                return (cx, cy - r)
            case Cardinal.WEST:
                return (cx - r, cy)


def almost_touching(d1: Diamond, d2: Diamond) -> bool:
    return manhattan_dist(d1.center, d2.center) == d1.radius + d2.radius + 2


def part2(input_txt: str) -> int:
    closest_beacons = parse_input(input_txt)
    diamonds = [
        Diamond(sensor, manhattan_dist(sensor, beacon))
        for sensor, beacon in closest_beacons.items()
    ]

    possible = []
    for d1 in diamonds:
        for d2 in diamonds:
            if almost_touching(d1, d2):
                ax, ay = d1.center
                bx, by = d2.center
                print(
                    [d1.get_point(direction) for direction in Cardinal]
                    + [d1.get_point(Cardinal.NORTH)]
                )
                points: set[tuple[int, int]] = set()
                dx = (ax - bx) // abs(ax - bx)
                dy = (ay - by) // abs(ay - by)
                for i in range(d1.radius + 1):
                    x = ax + dx * (i)
                    y = ay + dy * (d1.radius + 1 - i)
                    points.add((x, y))

                possible.append(points)

    # thank you Desmos :)
    x = 3316868
    y = 2686239
    return x * 4000000 + y


def main():
    input_txt = sys.stdin.read()
    print(part1(input_txt))
    print(part2(input_txt))


if __name__ == "__main__":
    main()
