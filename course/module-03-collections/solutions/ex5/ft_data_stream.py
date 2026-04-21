import random
from typing import Generator


NAMES: list[str] = ["alice", "bob", "charlie", "dylan"]
ACTIONS: list[str] = ["run", "eat", "sleep", "grab", "move",
                      "climb", "swim", "use", "release"]


def gen_event() -> Generator[tuple[str, str], None, None]:
    while True:
        yield (random.choice(NAMES), random.choice(ACTIONS))


def consume_event(
    events: list[tuple[str, str]]
) -> Generator[tuple[str, str], None, None]:
    while len(events) > 0:
        idx = random.randint(0, len(events) - 1)
        item = events.pop(idx)
        yield item


if __name__ == "__main__":
    print("=== Game Data Stream Processor ===")

    stream = gen_event()
    for i in range(1000):
        name, action = next(stream)
        print(f"Event {i}: Player {name} did action {action}")

    events_list: list[tuple[str, str]] = []
    for _ in range(10):
        events_list.append(next(stream))
    print(f"Built list of 10 events: {events_list}")
    print()

    for ev in consume_event(events_list):
        print(f"Got event from list: {ev}")
        print(f"Remains in list: {events_list}")
        print()
