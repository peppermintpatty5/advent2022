#!/usr/bin/env python3

import math
import re
import sys
from dataclasses import dataclass
from typing import Callable


@dataclass
class Monkey:
    items: list[int]
    operation: Callable[[int], int]
    divisor: int
    if_true: int
    if_false: int


def parse_input(input_txt: str):
    return [
        Monkey([75, 63], lambda x: x * 3, 11, 7, 2),
        Monkey([65, 79, 98, 77, 56, 54, 83, 94], lambda x: x + 3, 2, 2, 0),
        Monkey([66], lambda x: x + 5, 5, 7, 5),
        Monkey([51, 89, 90], lambda x: x * 19, 7, 6, 4),
        Monkey([75, 94, 66, 90, 77, 82, 61], lambda x: x + 1, 17, 6, 1),
        Monkey([53, 76, 59, 92, 95], lambda x: x + 2, 19, 4, 3),
        Monkey([81, 61, 75, 89, 70, 92], lambda x: x * x, 3, 0, 1),
        Monkey([81, 86, 62, 87], lambda x: x + 8, 13, 3, 5),
    ]


def part1(input_txt: str) -> int:
    monkeys = parse_input(input_txt)
    monkey_times = [0 for _ in range(len(monkeys))]

    for _ in range(20):
        for i, monkey in enumerate(monkeys):
            while monkey.items:
                item = monkey.items.pop(0)
                monkey_times[i] += 1
                new_item = monkey.operation(item) // 3
                dst_monkey = monkeys[
                    (
                        monkey.if_true
                        if new_item % monkey.divisor == 0
                        else monkey.if_false
                    )
                ]
                dst_monkey.items.append(new_item)
    a, b = sorted(monkey_times)[-2:]
    return a * b


def part2(input_txt: str) -> int:
    monkeys = parse_input(input_txt)
    monkey_times = [0 for _ in range(len(monkeys))]
    lcm = math.lcm(*(monkey.divisor for monkey in monkeys))

    for _ in range(10000):
        for i, monkey in enumerate(monkeys):
            while monkey.items:
                item = monkey.items.pop(0)
                monkey_times[i] += 1
                new_item = monkey.operation(item) % lcm
                dst_monkey = monkeys[
                    (
                        monkey.if_true
                        if new_item % monkey.divisor == 0
                        else monkey.if_false
                    )
                ]
                dst_monkey.items.append(new_item)
    a, b = sorted(monkey_times)[-2:]
    return a * b


def main():
    input_txt = sys.stdin.read()
    print(part1(input_txt))
    print(part2(input_txt))


if __name__ == "__main__":
    main()
