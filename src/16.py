#!/usr/bin/env python3

import re
import sys


def parse_input(input_txt: str):
    rates: dict[str, int] = {}
    tunnels: dict[str, set[str]] = {}
    for line in input_txt.splitlines():
        match = re.match(
            r"Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? (.*)", line
        )
        if match is not None:
            label, rate, children = match.groups()
            rate = int(rate)
            children = children.split(", ")
            rates[label] = rate
            tunnels[label] = set(children)
    return rates, tunnels


problem_cache = {}


def brute_force(
    rates: dict[str, int],
    tunnels: dict[str, set[str]],
    time_left: int,
    curr: str,
    open_valves: set[str],
) -> int:
    if time_left == 0:
        return 0

    hmm = tuple(sorted(open_valves))
    if (curr, time_left, hmm) in problem_cache:
        return problem_cache[curr, time_left, hmm]

    options: list[int] = []

    if curr not in open_valves and rates[curr] > 0:
        options.append(
            rates[curr] * (time_left - 1)
            + brute_force(rates, tunnels, time_left - 1, curr, open_valves | {curr})
        )

    for succ in tunnels[curr]:
        options.append(brute_force(rates, tunnels, time_left - 1, succ, open_valves))

    answer = max(options) if options else 0
    problem_cache[curr, time_left, hmm] = answer
    return answer


def part1(input_txt: str) -> int:
    rates, tunnels = parse_input(input_txt)

    return brute_force(rates, tunnels, 30, "AA", set())


def part2(input_txt: str) -> int:
    ...


def main():
    input_txt = sys.stdin.read()
    print(part1(input_txt))
    print(part2(input_txt))


if __name__ == "__main__":
    main()
