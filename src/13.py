#!/usr/bin/env python3

import functools
import sys


Packet = list["Packet"] | int


def parse_input(input_txt: str):
    packet_pairs: list[tuple[Packet, Packet]] = []

    for section in input_txt.split("\n\n"):
        a, b = section.splitlines()
        pa = eval(a)  # FIXME: eval is dangerous
        pb = eval(b)
        packet_pairs.append((pa, pb))

    return packet_pairs


def compare(pa: Packet, pb: Packet) -> int:
    if isinstance(pa, int) and isinstance(pb, int):
        return pa - pb
    elif isinstance(pa, list) and isinstance(pb, list):
        for a, b in zip(pa, pb):
            c = compare(a, b)
            if c != 0:
                return c
        return len(pa) - len(pb)
    else:
        return compare([pa], pb) if isinstance(pa, int) else compare(pa, [pb])


def part1(input_txt: str) -> int:
    packet_pairs = parse_input(input_txt)

    return sum(
        i for i, (pa, pb) in enumerate(packet_pairs, start=1) if compare(pa, pb) < 0
    )


def part2(input_txt: str) -> int:
    packet_pairs = parse_input(input_txt)
    packets = [p for pair in packet_pairs for p in pair]

    packets.append([[2]])
    packets.append([[6]])
    packets.sort(key=functools.cmp_to_key(compare))

    return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)


def main():
    input_txt = sys.stdin.read()
    print(part1(input_txt))
    print(part2(input_txt))


if __name__ == "__main__":
    main()
