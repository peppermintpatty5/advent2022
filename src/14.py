#!/usr/bin/env python3

import sys


def parse_input(input_txt: str):
    rocks: set[tuple[int, int]] = set()
    for line in input_txt.splitlines():
        points = [
            (int(x), int(y))
            for x, y in (part.split(",") for part in line.split(" -> "))
        ]

        for (x1, y1), (x2, y2) in zip(points, points[1:]):
            if x1 == x2:
                if y1 < y2:
                    for y in range(y1, y2 + 1):
                        rocks.add((x1, y))
                else:
                    for y in range(y2, y1 + 1):
                        rocks.add((x1, y))
            elif y1 == y2:
                if x1 < x2:
                    for x in range(x1, x2 + 1):
                        rocks.add((x, y1))
                else:
                    for x in range(x2, x1 + 1):
                        rocks.add((x, y1))
            else:
                print("UH-OH")
    return rocks


def part1(input_txt: str) -> int:
    rocks = parse_input(input_txt)
    sand: set[tuple[int, int]] = set()

    abyss = max(y for _, y in rocks) + 1

    while True:
        x, y = 500, 0
        # keep moving down until hit sand or rock
        while y < abyss:
            if (x, y + 1) not in sand and (x, y + 1) not in rocks:
                y += 1
            elif (x - 1, y + 1) not in sand and (x - 1, y + 1) not in rocks:
                x -= 1
                y += 1
            elif (x + 1, y + 1) not in sand and (x + 1, y + 1) not in rocks:
                x += 1
                y += 1
            else:
                break
        # sand particle comes to rest
        sand.add((x, y))

        if y >= abyss:
            return len(sand) - 1


def part2(input_txt: str) -> int:
    rocks = parse_input(input_txt)
    sand: set[tuple[int, int]] = set()

    floor = max(y for _, y in rocks) + 2

    while True:
        x, y = 500, 0

        while y + 1 < floor:
            if (x, y + 1) not in sand and (x, y + 1) not in rocks:
                y += 1
            elif (x - 1, y + 1) not in sand and (x - 1, y + 1) not in rocks:
                x -= 1
                y += 1
            elif (x + 1, y + 1) not in sand and (x + 1, y + 1) not in rocks:
                x += 1
                y += 1
            else:
                break
        # sand particle comes to rest
        sand.add((x, y))

        if (x, y) == (500, 0):
            return len(sand)


def main():
    input_txt = sys.stdin.read()
    print(part1(input_txt))
    print(part2(input_txt))


if __name__ == "__main__":
    main()
