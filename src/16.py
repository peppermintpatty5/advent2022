#!/usr/bin/env python3

import re
import sys
from typing import Generator, TypeVar

T = TypeVar("T")


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


def dijkstra(
    vertices: set[T], edges: dict[T, set[T]], costs: dict[tuple[T, T], int], start: T
) -> dict[T, tuple[T, int]]:
    # Thank you Wikipedia

    if start not in vertices:
        raise ValueError("invalid starting vertex")

    dist = {v: 999 for v in vertices}
    prev: dict[T, T | None] = {v: None for v in vertices}

    dist[start] = 0
    unvisited = {v for v in vertices}

    while unvisited:
        u = min(unvisited, key=lambda u: dist[u])
        unvisited.remove(u)

        for v in edges[u]:
            if v in unvisited:
                alt = dist[u] + costs[u, v]
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u

    return {v: (p, dist[v]) for v, p in prev.items() if p is not None}


def part2(input_txt: str) -> int:
    flow_rates, tunnels = parse_input(input_txt)

    vertices = {valve for valve in flow_rates.keys()}
    edges = {v1: tunnels[v1] for v1 in vertices}
    costs: dict[tuple[str, str], int] = {
        (v1, v2): 1 for v1, neighbors in edges.items() for v2 in neighbors
    }

    the_matrix = {
        (v1, v2): cost
        for v1 in vertices
        for v2, (_, cost) in dijkstra(vertices, edges, costs, v1).items()
        if (flow_rates[v1] > 0 or v1 == "AA") and flow_rates[v2] > 0
    }
    good_valves = {v for v in vertices if flow_rates[v] > 0}

    def get_possible_paths(
        valves: set[str], start: str, time_left: int, visited: set[str]
    ) -> Generator[list[str], None, None]:
        # create new set, do not update in-place!
        visited = visited | {start}

        reachable = {
            v
            for v in valves
            if v not in visited and (the_matrix[start, v] + 1) <= time_left
        }

        if reachable:
            for v in reachable:
                for path in get_possible_paths(
                    valves, v, time_left - (the_matrix[start, v] + 1), visited
                ):
                    yield [start] + path
        else:
            yield [start]

    def get_path_reward(path: list[str], time: int) -> int:
        total = 0
        for i in range(len(path) - 1):
            v1 = path[i]
            v2 = path[i + 1]
            time -= the_matrix[v1, v2] + 1
            total += flow_rates[v2] * time
        return total

    t = 26
    possible_paths = list(get_possible_paths(good_valves, "AA", t + 1, set()))

    # print(len(possible_paths))

    solution = 0
    for path1 in possible_paths:
        for path2 in possible_paths:
            a = set(path1[1:])
            b = set(path2[1:])
            if not a & b:
                print(a, b)
                solution = max(
                    solution, get_path_reward(path1, t) + get_path_reward(path2, t)
                )

    return solution


def main():
    input_txt = sys.stdin.read()
    # print(part1(input_txt))
    print(part2(input_txt))


if __name__ == "__main__":
    main()
