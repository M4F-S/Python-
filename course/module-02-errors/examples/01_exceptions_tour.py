"""Exception handling tour."""


def parse_int(s: str) -> int:
    return int(s)   # may raise ValueError


def div(a: int, b: int) -> int:
    return a // b   # may raise ZeroDivisionError


class MyError(Exception):
    DEFAULT = "custom boom"

    def __init__(self, msg: str = "") -> None:
        super().__init__(msg or self.DEFAULT)


def demo() -> None:
    for candidate in ("42", "abc"):
        try:
            print(parse_int(candidate))
        except ValueError as e:
            print("bad int:", e)

    for b in (2, 0):
        try:
            print(div(10, b))
        except ZeroDivisionError as e:
            print("div error:", e)

    try:
        raise MyError()            # default message
    except MyError as e:
        print("custom:", e)

    try:
        raise MyError("specific message here")
    except MyError as e:
        print("custom:", e)

    # catch multiple in one line
    for thing in (0, "abc", 3):
        try:
            n = int(thing) if isinstance(thing, str) else 10 // thing
            print("ok:", n)
        except (ValueError, ZeroDivisionError) as e:
            print("multi-catch:", type(e).__name__, e)


if __name__ == "__main__":
    demo()
