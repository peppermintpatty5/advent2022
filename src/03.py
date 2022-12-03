#!/usr/bin/env python3

import sys


def part1(input_txt: str) -> int:
    sacks = input_txt.splitlines()

    sum = 0
    for s in sacks:
        a = s[: len(s) // 2]
        b = s[len(s) // 2 :]
        common = (set(a) & set(b)).pop()

        if common.islower():
            sum += ord(common) - ord("a") + 1
        else:
            sum += ord(common) - ord("A") + 27
    return sum


def part2(input_txt: str) -> int:
    sacks = input_txt.splitlines()

    sum = 0
    for i in range(0, len(sacks), 3):
        a, b, c = sacks[i : i + 3]
        common = (set(a) & set(b) & set(c)).pop()

        if common.islower():
            sum += ord(common) - ord("a") + 1
        else:
            sum += ord(common) - ord("A") + 27
    return sum


def main():
    input_txt = sys.stdin.read()
    print(part1(input_txt))
    print(part2(input_txt))


if __name__ == "__main__":
    main()
