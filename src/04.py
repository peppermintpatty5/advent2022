#!/usr/bin/env python3

import re
import sys


def parse_input(input_txt: str):
    range_pairs: list[tuple[range, range]] = []

    for line in input_txt.splitlines():
        match = re.match(r"(\d+)-(\d+),(\d+)-(\d+)", line)
        if match is not None:
            a, b, c, d = tuple(int(x) for x in match.groups())
            range_pairs.append((range(a, b + 1), range(c, d + 1)))

    return range_pairs


def part1(input_txt: str) -> int:
    range_pairs = parse_input(input_txt)

    return sum(
        1
        for r1, r2 in range_pairs
        if all(x in r2 for x in r1) or all(x in r1 for x in r2)
    )


def part2(input_txt: str) -> int:
    range_pairs = parse_input(input_txt)

    return sum(1 for r1, r2 in range_pairs if any(x in r2 for x in r1))


def main():
    input_txt = sys.stdin.read()
    print(part1(input_txt))
    print(part2(input_txt))


if __name__ == "__main__":
    main()
