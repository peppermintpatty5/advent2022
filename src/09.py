#!/usr/bin/env python3

import sys


def part1(input_txt: str) -> int:
    head = (0, 0)
    tail = (0, 0)
    tail_visited = {tail}

    for line in input_txt.splitlines():
        move, steps = line.split()
        steps = int(steps)
        for _ in range(steps):
            if move == "U":
                dh = (0, 1)
            elif move == "D":
                dh = (0, -1)
            elif move == "L":
                dh = (-1, 0)
            elif move == "R":
                dh = (1, 0)
            else:
                dh = (0, 0)

            head = (head[0] + dh[0], head[1] + dh[1])

            hx, hy = head
            tx, ty = tail
            if abs(hx - tx) == 2:
                tx += dh[0]
                ty = hy
            if abs(hy - ty) == 2:
                ty += dh[1]
                tx = hx

            tail = tx, ty
            tail_visited.add(tail)

    return len(tail_visited)


def part2(input_txt: str) -> int:
    rope: list[tuple[int, int]] = [(0, 0) for _ in range(10)]
    tail_visited = {rope[-1]}

    for line in input_txt.splitlines():
        move, steps = line.split()
        steps = int(steps)
        for _ in range(steps):
            # just move front of rope, everything else follows
            if move == "U":
                dh = (0, 1)
            elif move == "D":
                dh = (0, -1)
            elif move == "L":
                dh = (-1, 0)
            elif move == "R":
                dh = (1, 0)
            else:
                dh = (0, 0)

            head = rope[0]
            head = (head[0] + dh[0], head[1] + dh[1])
            rope[0] = head

            # move following segments
            for i in range(1, len(rope)):
                head = rope[i - 1]
                tail = rope[i]

                hx, hy = head
                tx, ty = tail

                if abs(hx - tx) == 2 and abs(hy - ty) == 2:
                    tx += (hx - tx) // 2
                    ty += (hy - ty) // 2
                elif abs(hx - tx) == 2:
                    tx += (hx - tx) // 2
                    ty = hy
                elif abs(hy - ty) == 2:
                    ty += (hy - ty) // 2
                    tx = hx

                tail = tx, ty
                rope[i] = tail

            tail_visited.add(rope[-1])

    return len(tail_visited)


def main():
    input_txt = sys.stdin.read()
    print(part1(input_txt))
    print(part2(input_txt))


if __name__ == "__main__":
    main()
