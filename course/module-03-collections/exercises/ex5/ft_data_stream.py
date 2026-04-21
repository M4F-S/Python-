# Exercise 5 — ft_data_stream
# Authorized: next(), range(), len(), print(), typing.Generator,
#             import random, random.*
#
# gen_event()      -> endless generator yielding (name, action)
# consume_event(L) -> generator yielding+removing a random element each
#                     call until L is empty
#
# Main: loop 1000 events; build a list of 10 events; use consume_event
# in a for-loop, printing each event and the remaining list.

import random
from typing import Generator


NAMES: list[str] = ["alice", "bob", "charlie", "dylan"]
ACTIONS: list[str] = ["run", "eat", "sleep", "grab", "move",
                      "climb", "swim", "use", "release"]


def gen_event() -> Generator[tuple[str, str], None, None]:
    pass


def consume_event(
    events: list[tuple[str, str]]
) -> Generator[tuple[str, str], None, None]:
    pass


if __name__ == "__main__":
    pass
