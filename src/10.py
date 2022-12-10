#!/usr/bin/env python3

import sys


def part1(input_txt: str) -> int:
    hist = [1]
    x = 1
    for line in input_txt.splitlines():
        if line == "noop":
            hist.append(x)
        else:
            _, y = line.split()
            y = int(y)
            hist.append(x)
            hist.append(x)
            x += y
    return sum(hist[i] * i for i in [20, 60, 100, 140, 180, 220])


def part2(input_txt: str) -> str:
    hist = [1]
    x = 1
    for line in input_txt.splitlines():
        if line == "noop":
            hist.append(x)
        else:
            _, y = line.split()
            y = int(y)
            hist.append(x)
            hist.append(x)
            x += y

    i = 1
    grid = [["." for _ in range(40)] for _ in range(6)]
    for py in range(6):
        for px in range(40):
            x = hist[i]
            if px in (x - 1, x, x + 1):
                grid[py][px] = "#"
            i += 1
    return "\n".join("".join(row) for row in grid)


def main():
    input_txt = sys.stdin.read()
    print(part1(input_txt))
    print(part2(input_txt))


if __name__ == "__main__":
    main()
