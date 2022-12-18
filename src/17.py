#!/usr/bin/env python3

import itertools
import math
import sys
from dataclasses import dataclass
from typing import Iterable

rock_pattern_strings = [
    ["####"],
    [" # ", "###", " # "],
    ["  #", "  #", "###"],
    ["#", "#", "#", "#"],
    ["##", "##"],
]
rock_patterns = [
    {
        (x, y)
        for y, row in enumerate(reversed(pattern))
        for x, cell in enumerate(row)
        if cell == "#"
    }
    for pattern in rock_pattern_strings
]
CHAMBER_WIDTH = 7


def simulate_rockfall(winds: Iterable[str], n: int) -> int:
    """
    Simulate the falling rocks for `n` iterations and return the height.
    """
    fallen_rocks: set[tuple[int, int]] = set()

    pattern_cycle = itertools.cycle(rock_patterns)
    wind_cycle = itertools.cycle(winds)

    max_y = 0
    for _ in range(n):
        pattern = next(pattern_cycle)
        width = max(x for x, _ in pattern) - min(x for x, _ in pattern) + 1
        height = max(y for _, y in pattern) - min(y for _, y in pattern) + 1
        dx, dy = 2, max_y + 3

        while True:
            # wind pushes rock
            wind = next(wind_cycle)
            if wind == "<":
                if dx > 0:
                    dx -= 1
                    rock = {(x + dx, y + dy) for x, y in pattern}
                    if rock & fallen_rocks:
                        dx += 1
            if wind == ">":
                if dx < CHAMBER_WIDTH - width:
                    dx += 1
                    rock = {(x + dx, y + dy) for x, y in pattern}
                    if rock & fallen_rocks:
                        dx -= 1

            # rock falls down
            dy -= 1
            rock = {(x + dx, y + dy) for x, y in pattern}
            if rock & fallen_rocks or dy < 0:
                dy += 1
                max_y = max(max_y, dy + height)
                rock = {(x + dx, y + dy) for x, y in pattern}
                fallen_rocks.update(rock)
                break

    return max_y


def part1(input_txt: str) -> int:
    winds = input_txt.strip()

    return simulate_rockfall(winds, 2022)


def head(rocks: set[tuple[int, int]], max_y: int, n: int = 100) -> set[tuple[int, int]]:
    """
    Return the top `n` rows of the rock formation.
    """
    lines_removed = max(0, max_y - n)
    return {(x, y - lines_removed) for x, y in rocks if y >= lines_removed}


def rocks_str(rocks: set[tuple[int, int]]) -> str:
    max_y = max(y for _, y in rocks)

    return "".join(
        "#" if (x, y) in rocks else "."
        for x in range(CHAMBER_WIDTH)
        for y in range(max_y)
    )


@dataclass
class HistoryEntry:
    iteration: int
    pattern_num: int
    wind_num: int
    height: int


def part2(input_txt: str) -> int:
    winds = input_txt.strip()

    fallen_rocks: set[tuple[int, int]] = set()

    pattern_cycle = itertools.cycle(enumerate(rock_patterns))
    wind_cycle = itertools.cycle(enumerate(winds))

    max_y = 0
    lines_removed = 0

    # remember the rock formation (as a string) for each iteration
    history: dict[str, HistoryEntry] = {}

    for iteration in itertools.count():
        pattern_num, pattern = next(pattern_cycle)
        width = max(x for x, _ in pattern) - min(x for x, _ in pattern) + 1
        height = max(y for _, y in pattern) - min(y for _, y in pattern) + 1
        dx, dy = 2, max_y + 3

        while True:
            # wind pushes rock
            wind_num, wind = next(wind_cycle)
            if wind == "<":
                if dx > 0:
                    dx -= 1
                    rock = {(x + dx, y + dy) for x, y in pattern}
                    if rock & fallen_rocks:
                        dx += 1
            if wind == ">":
                if dx < CHAMBER_WIDTH - width:
                    dx += 1
                    rock = {(x + dx, y + dy) for x, y in pattern}
                    if rock & fallen_rocks:
                        dx -= 1

            # rock falls down
            dy -= 1
            rock = {(x + dx, y + dy) for x, y in pattern}
            if rock & fallen_rocks or dy < 0:
                dy += 1
                max_y = max(max_y, dy + height)
                rock = {(x + dx, y + dy) for x, y in pattern}
                fallen_rocks.update(rock)
                break

        # this solution is sketchy... may need bigger n to elminate false positives
        fallen_rocks = head(fallen_rocks, max_y, 100)
        lines_removed += max(0, max_y - 100)
        max_y -= max(0, max_y - 100)

        formation = rocks_str(fallen_rocks)
        curr = HistoryEntry(iteration, pattern_num, wind_num, max_y + lines_removed)
        if formation in history:
            prev = history[formation]
            if (curr.pattern_num, curr.wind_num) == (prev.pattern_num, prev.wind_num):
                # print("Fount a match!!!")
                # print("\t> ", iteration, pattern_num, wind_num)
                # print("\t< ", prev_iteration, prev_pattern_num, prev_wind_num)
                cycle_length = curr.iteration - prev.iteration
                height_diff = curr.height - prev.height
                return (1_000_000_000_000 // cycle_length * height_diff) + (
                    simulate_rockfall(winds, 1_000_000_000_000 % cycle_length)
                )
        else:
            history[formation] = curr

    return -1


def main():
    input_txt = sys.stdin.read()
    print(part1(input_txt))
    print(part2(input_txt))


if __name__ == "__main__":
    main()
