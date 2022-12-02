#!/usr/bin/env python3

import sys

ROCK = 1
PAPER = 2
SCISSOR = 3


def part1(input_txt: str) -> int:
    rounds = [round.split() for round in input_txt.splitlines()]

    score = 0
    for x, y in rounds:
        a = ord(x) - ord("A") + 1
        b = ord(y) - ord("X") + 1

        score += b

        if (a, b) in {(ROCK, PAPER), (PAPER, SCISSOR), (SCISSOR, ROCK)}:
            score += 6
        elif a == b:
            score += 3

    return score


def part2(input_txt: str) -> int:
    LOSE = 1
    DRAW = 2
    WIN = 3

    rounds = [round.split() for round in input_txt.splitlines()]

    score = 0
    for x, y in rounds:
        a = ord(x) - ord("A") + 1
        b = ord(y) - ord("X") + 1

        score += 0 if b == LOSE else 3 if b == DRAW else 6

        if b == LOSE:
            score += SCISSOR if a == ROCK else ROCK if a == PAPER else PAPER
        elif b == DRAW:
            score += a
        elif b == WIN:
            score += PAPER if a == ROCK else SCISSOR if a == PAPER else ROCK

    return score


def main():
    input_txt = sys.stdin.read()
    print(part1(input_txt))
    print(part2(input_txt))


if __name__ == "__main__":
    main()
