#!/usr/bin/env python3

import sys


def lol_mkdir(filesystem, cwd, name):
    # print("lol_mkdir", filesystem, cwd, name)
    curr = filesystem
    for part in cwd:
        curr = curr[part]

    curr[name] = {}


def lol_creat(filesystem, cwd, name, size):
    curr = filesystem
    for part in cwd:
        curr = curr[part]

    curr[name] = size


def dir_size(directory):
    return sum(x if type(x) is int else dir_size(x) for x in directory.values())


def part1(input_txt: str) -> int:
    lines = input_txt.splitlines()
    cwd: list[str] = []
    filesystem = {"/": {}}

    all_dirs = [["/"]]

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("$"):
            if line.startswith("$ cd"):
                dir = line.split()[-1]
                if dir == "..":
                    cwd.pop()
                else:
                    cwd.append(dir)
            elif line.startswith("$ ls"):
                while i + 1 < len(lines) and not lines[i + 1].startswith("$"):
                    i += 1
                    line = lines[i]
                    if line.startswith("dir"):
                        name = line.split()[-1]
                        lol_mkdir(filesystem, cwd, name)
                        all_dirs.append(list(cwd) + [name])
                    else:
                        size, name = line.split()
                        size = int(size)
                        lol_creat(filesystem, cwd, name, size)
        i += 1

    dir_sizes = {}
    ouch = 0
    for dir in all_dirs:
        curr = filesystem
        for part in dir:
            curr = curr[part]

        size = dir_size(curr)
        # print(dir, size)
        if size <= 100000:
            ouch += size
        dir_sizes[size] = dir

    total = 70000000
    used = dir_size(filesystem)
    free = total - used
    goal = 30000000 - free

    for s in sorted(dir_sizes):
        if s > goal:
            print(s, dir_sizes[s])
            break

    return ouch


def part2(input_txt: str) -> int:
    ...


def main():
    input_txt = sys.stdin.read()
    print(part1(input_txt))
    print(part2(input_txt))


if __name__ == "__main__":
    main()
