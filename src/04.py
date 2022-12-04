#!/usr/bin/env python3

import sys


def part1(input_txt: str) -> int:
    count = 0
    for line in input_txt.splitlines():
        e1, e2 = line.split(",")
        a, b = map(int, e1.split("-"))
        c, d = map(int, e2.split("-"))
        r1 = set(range(a, b + 1))
        r2 = set(range(c, d + 1))

        if r1 <= r2 or r2 <= r1:
            count += 1
    return count


def part2(input_txt: str) -> int:
    count = 0
    for line in input_txt.splitlines():
        e1, e2 = line.split(",")
        a, b = map(int, e1.split("-"))
        c, d = map(int, e2.split("-"))
        r1 = set(range(a, b + 1))
        r2 = set(range(c, d + 1))

        if r1 & r2:
            count += 1
    return count


def main():
    input_txt = sys.stdin.read()
    print(part1(input_txt))
    print(part2(input_txt))


if __name__ == "__main__":
    main()
