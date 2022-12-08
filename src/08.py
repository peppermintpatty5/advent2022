#!/usr/bin/env python3

import sys


def part1(input_txt: str) -> int:
    grid = [[int(x) for x in row] for row in input_txt.splitlines()]
    count = 0
    for r, row in enumerate(grid):
        for c, tree in enumerate(row):

            if (
                all(grid[r][c2] < tree for c2 in range(0, c))
                or all(grid[r][c2] < tree for c2 in range(c + 1, len(row)))
                or all(grid[r2][c] < tree for r2 in range(0, r))
                or all(grid[r2][c] < tree for r2 in range(r + 1, len(grid)))
            ):
                count += 1
    return count


def part2(input_txt: str) -> int:
    grid = [[int(x) for x in row] for row in input_txt.splitlines()]
    max_score = 0
    for r, row in enumerate(grid):
        for c, tree in enumerate(row):
            ls = 0
            for c2 in range(c - 1, 0 - 1, -1):
                ls += 1
                if grid[r][c2] >= tree:
                    break

            rs = 0
            for c2 in range(c + 1, len(row)):
                rs += 1
                if grid[r][c2] >= tree:
                    break

            us = 0
            for r2 in range(r - 1, 0 - 1, -1):
                us += 1
                if grid[r2][c] >= tree:
                    break

            ds = 0
            for r2 in range(r + 1, len(grid)):
                ds += 1
                if grid[r2][c] >= tree:
                    break

            if (r, c) == (3, 2):
                print(ls, rs, us, ds)

            score = ls * rs * us * ds
            max_score = max(score, max_score)
    return max_score


def main():
    input_txt = sys.stdin.read()
    print(part1(input_txt))
    print(part2(input_txt))


if __name__ == "__main__":
    main()
