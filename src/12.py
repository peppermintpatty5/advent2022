#!/usr/bin/env python3

import sys
from collections import deque
from dataclasses import dataclass


@dataclass
class Node:
    location: tuple[int, int]
    prev: "Node | None"


def parse_input(input_txt: str):
    lines = input_txt.splitlines()
    grid = [
        [ord("a" if c == "S" else "z" if c == "E" else c) - ord("a") for c in row]
        for row in lines
    ]
    start: tuple[int, int] = (-1, -1)
    end: tuple[int, int] = (-1, -1)

    for r, row in enumerate(lines):
        for c, col in enumerate(row):
            if col == "S":
                start = (r, c)
            elif col == "E":
                end = (r, c)

    return grid, start, end


def find_path(
    grid: list[list[int]], start: tuple[int, int], end: tuple[int, int]
) -> list[Node] | None:
    rows, cols = len(grid), len(grid[0])

    queue = deque([Node(start, None)])
    visited = {start}
    while queue:
        node = queue.popleft()

        if node.location == end:
            path: list[Node] = []
            while node is not None:
                path.append(node)
                node = node.prev
            path.reverse()
            return path

        r, c = node.location
        for r2, c2 in [(r + 1, c), (r, c + 1), (r - 1, c), (r, c - 1)]:
            if 0 <= r2 < rows and 0 <= c2 < cols and grid[r2][c2] <= grid[r][c] + 1:
                if (r2, c2) not in visited:
                    queue.append(Node((r2, c2), node))
                    visited.add((r2, c2))
    return None


def part1(input_txt: str) -> int:
    grid, start, end = parse_input(input_txt)
    path = find_path(grid, start, end)

    return (len(path) if path is not None else 0) - 1


def part2(input_txt: str) -> int:
    grid, _, end = parse_input(input_txt)
    rows, cols = len(grid), len(grid[0])

    return min(
        len(path) - 1
        for path in (
            find_path(grid, (r, c), end)
            for r in range(rows)
            for c in range(cols)
            if grid[r][c] == 0
        )
        if path is not None
    )


def main():
    input_txt = sys.stdin.read()
    print(part1(input_txt))
    print(part2(input_txt))


if __name__ == "__main__":
    main()
