#!/usr/bin/env python3

import sys


def part1(input_txt: str) -> int:
    groups = [sum(map(int, group.splitlines())) for group in input_txt.split("\n\n")]
    return max(groups)


def part2(input_txt: str) -> int:
    groups = [sum(map(int, group.splitlines())) for group in input_txt.split("\n\n")]
    return sum(sorted(groups)[-3:])


def main():
    input_txt = sys.stdin.read()
    print(part1(input_txt))
    print(part2(input_txt))


if __name__ == "__main__":
    main()
