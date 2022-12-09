#!/usr/bin/env python3

import sys


class Directory:
    def __init__(self, name: str, parent: "Directory | None") -> None:
        self.name = name
        self.parent = parent
        self.subdirs: dict[str, "Directory"] = {}
        self.files: dict[str, int] = {}

    def path(self) -> str:
        """
        Get the absolute path of the directory.
        """
        parts: list[str] = []

        curr = self
        while curr is not None:
            parts.append(curr.name)
            curr = curr.parent

        return "/" + "/".join(parts)

    def get_all_sizes(self) -> dict[str, int]:
        """
        Calculate the total size of all directories using tabulation.

        Returns a dictionary that maps the path of each directory to its size.
        """
        sizes: dict[str, int] = {}
        self._get_all_sizes(sizes)
        return sizes

    def _get_all_sizes(self, sizes: dict[str, int]) -> None:
        """
        Helper method that does the work for `get_all_sizes()`.
        """
        # get sizes of subdirectories first
        for d in self.subdirs.values():
            d._get_all_sizes(sizes)

        sizes[self.path()] = sum(self.files.values()) + sum(
            sizes[d.path()] for d in self.subdirs.values()
        )


def parse_input(input_txt: str) -> Directory:
    """
    Recreate directory structure from terminal output.
    """
    lines = input_txt.splitlines()
    cwd = root = Directory("", None)

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("$"):
            if line.startswith("$ cd"):
                name = line.split()[-1]
                if name == "..":
                    # cannot go higher than root directory
                    cwd = cwd.parent or cwd
                else:
                    cwd = root if name == "/" else cwd.subdirs[name]
            elif line.startswith("$ ls"):
                while i + 1 < len(lines) and not lines[i + 1].startswith("$"):
                    i += 1
                    line = lines[i]
                    if line.startswith("dir"):
                        _, name = line.split()
                        cwd.subdirs[name] = Directory(name, cwd)
                    else:
                        size, name = line.split()
                        cwd.files[name] = int(size)
        i += 1

    return root


def part1(input_txt: str) -> int:
    root = parse_input(input_txt)
    sizes = root.get_all_sizes()

    return sum(size for size in sizes.values() if size <= 100000)


def part2(input_txt: str) -> int:
    root = parse_input(input_txt)
    sizes = root.get_all_sizes()

    used = sizes[root.path()]
    free = 70000000 - used

    return min(size for size in sizes.values() if free + size >= 30000000)


def main():
    input_txt = sys.stdin.read()
    print(part1(input_txt))
    print(part2(input_txt))


if __name__ == "__main__":
    main()
