#!/usr/bin/env python3

import sys


adj = {(1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1)}


def part1(input_txt: str) -> int:
    points = {tuple(map(int, line.split(","))) for line in input_txt.splitlines()}

    return sum(
        1
        for x, y, z in points
        for dx, dy, dz in adj
        if (x + dx, y + dy, z + dz) not in points
    )


def get_sides(point: tuple[int, int, int]) -> set[tuple[int, int, int]]:
    x, y, z = point
    return {(x + dx, y + dy, z + dz) for dx, dy, dz in adj}


def get_surface_area(cluster: set[tuple[int, int, int]]) -> int:
    return sum(
        1
        for x, y, z in cluster
        for dx, dy, dz in adj
        if (x + dx, y + dy, z + dz) not in cluster
    )


def part2(input_txt: str) -> int:
    lava = {tuple(map(int, line.split(","))) for line in input_txt.splitlines()}

    max_x = max(x for x, _, _ in lava) + 1
    max_y = max(y for _, y, _ in lava) + 1
    max_z = max(z for _, _, z in lava) + 1
    min_x = min(x for x, _, _ in lava) - 1
    min_y = min(y for _, y, _ in lava) - 1
    min_z = min(z for _, _, z in lava) - 1

    U = {
        (x, y, z)
        for x in range(min_x, max_x + 1)
        for y in range(min_y, max_y + 1)
        for z in range(min_z, max_z + 1)
    }
    air = U - lava
    air_copy = set(air)

    clusters = []
    while air_copy:
        cluster: set[tuple[int, int, int]] = {air_copy.pop()}

        while True:
            fringe = {s for point in cluster for s in get_sides(point) if s in air_copy}
            if fringe:
                cluster.update(fringe)
                air_copy -= fringe
            else:
                break
        clusters.append(cluster)

    return get_surface_area(lava) - sum(
        get_surface_area(cluster) for cluster in sorted(clusters, key=len)[:-1]
    )


def main():
    input_txt = sys.stdin.read()
    print(part1(input_txt))
    print(part2(input_txt))


if __name__ == "__main__":
    main()
