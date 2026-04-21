"""Collections tour: list, tuple, set, dict, generator, comprehension."""

from typing import Generator


def tour_list() -> None:
    xs: list[int] = [1, 2, 3]
    xs.append(4)
    xs.insert(0, 0)
    print("list:", xs, "len:", len(xs), "sum:", sum(xs))


def tour_tuple() -> None:
    p = (1.0, 2.0, 3.0)
    x, y, z = p
    print("tuple:", p, "unpacked:", x, y, z)


def tour_set() -> None:
    a, b = {1, 2, 3}, {3, 4, 5}
    print("union:", a | b, "inter:", a & b, "diff a-b:", a - b)


def tour_dict() -> None:
    d = {"a": 1, "b": 2}
    d.update({"c": 3})
    for k, v in d.items():
        print(f"{k} -> {v}")


def count_up(n: int) -> Generator[int, None, None]:
    i = 0
    while i < n:
        yield i
        i += 1


def tour_generator() -> None:
    print("gen:", list(count_up(4)))


def tour_comprehension() -> None:
    squares = [x * x for x in range(5)]
    evens = {x for x in range(10) if x % 2 == 0}
    name_len = {w: len(w) for w in ["alpha", "beta", "gamma"]}
    print("list-comp:", squares)
    print("set-comp:", evens)
    print("dict-comp:", name_len)


if __name__ == "__main__":
    tour_list()
    tour_tuple()
    tour_set()
    tour_dict()
    tour_generator()
    tour_comprehension()
