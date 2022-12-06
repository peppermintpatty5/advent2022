#!/usr/bin/env python3

import sys


def part1(input_txt: str) -> int:
    s = input_txt
    for i in range(len(s) - 4):
        if len(set(s[i : i + 4])) == 4:
            return i + 4
    return -1


def part2(input_txt: str) -> int:
    s = input_txt
    for i in range(len(s) - 14):
        if len(set(s[i : i + 14])) == 14:
            return i + 14
    return -1


def main():
    input_txt = sys.stdin.read()
    print(part1(input_txt))
    print(part2(input_txt))


if __name__ == "__main__":
    main()
