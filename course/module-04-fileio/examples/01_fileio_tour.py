"""File I/O tour. Creates and removes a scratch file as it runs."""

import sys
from typing import IO


SCRATCH = "/tmp/fileio_tour_scratch.txt"


def write_demo() -> None:
    f: IO[str] = open(SCRATCH, "w")
    f.write("line 1\n")
    f.write("line 2\n")
    f.close()


def read_demo() -> None:
    f = open(SCRATCH, "r")
    print(f.read(), end="")
    f.close()


def stderr_demo() -> None:
    print("this goes to stderr", file=sys.stderr)


def with_demo() -> None:
    with open(SCRATCH, "r") as f:
        for line in f:
            print("with:", line.rstrip("\n"))


if __name__ == "__main__":
    write_demo()
    read_demo()
    stderr_demo()
    with_demo()
