#!/usr/bin/env python3

import itertools
import sys


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


def debug_print(fallen_rocks: set[tuple[int, int]], max_y: int = 10):
    for y in range(max_y, -1, -1):
        print("".join("#" if (x, y) in fallen_rocks else "." for x in range(7)))
    print("-" * 7)


def part1(input_txt: str) -> int:
    winds = input_txt.strip()

    chamber_width = 7
    fallen_rocks: set[tuple[int, int]] = set()

    pattern_cycle = itertools.cycle(rock_patterns)
    wind_cycle = itertools.cycle(winds)

    max_y = 0
    for _ in range(2022):
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
                if dx < chamber_width - width:
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


def part2(input_txt: str) -> int:
    ...


def main():
    input_txt = sys.stdin.read()
    print(part1(input_txt))
    print(part2(input_txt))


if __name__ == "__main__":
    main()
