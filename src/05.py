#!/usr/bin/env python3

import re
import sys


def parse_input(input_txt: str):
    stacks: dict[int, list[str]] = {}
    moves: list[tuple[int, int, int]] = []

    # parse drawing of the starting stacks of crates
    drawing = [line[1::4] for line in input_txt.splitlines() if line.startswith("[")]
    for layer in reversed(drawing):
        for i, crate in enumerate(layer, start=1):
            if crate != " ":
                if i not in stacks:
                    stacks[i] = []
                stacks[i].append(crate)

    # parse rearrangement procedure
    for line in input_txt.splitlines():
        match = re.search(r"move (\d+) from (\d+) to (\d+)", line)
        if match is not None:
            moves.append(tuple(int(x) for x in match.groups()))

    return stacks, moves


def part1(input_txt: str) -> str:
    stacks, moves = parse_input(input_txt)

    for n, src, dst in moves:
        for _ in range(n):
            stacks[dst].append(stacks[src].pop())

    return "".join(stacks[i][-1] for i in sorted(stacks.keys()))


def part2(input_txt: str) -> str:
    stacks, moves = parse_input(input_txt)

    for n, src, dst in moves:
        tmp: list[str] = []
        for _ in range(n):
            tmp.append(stacks[src].pop())
        for _ in range(n):
            stacks[dst].append(tmp.pop())

    return "".join(stacks[i][-1] for i in sorted(stacks.keys()))


def main():
    input_txt = sys.stdin.read()
    print(part1(input_txt))
    print(part2(input_txt))


if __name__ == "__main__":
    main()
