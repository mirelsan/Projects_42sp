import random
import typing


PLAYERS = ["alice", "bob", "charlie", "dylan"]
ACTIONS = ["run", "eat", "sleep", "grab", "move",
           "climb", "swim", "release", "use"]


def gen_event() -> typing.Generator[tuple[str, str], None, None]:
    while True:
        name = random.choice(PLAYERS)
        action = random.choice(ACTIONS)
        yield name, action


def consume_event(
        events: list[tuple[str, str]],
   ) -> typing.Generator[tuple[str, str], None, None]:
    while events:
        chosen = random.choice(events)
        events.remove(chosen)
        yield chosen


def main() -> None:
    print("=== Game Data Stream Processor ===")

    stream = gen_event()
    for i in range(1000):
        name, action = next(stream)
        print(f"Event {i}: Player {name} did action {action}")

    events = [next(stream) for _ in range(10)]
    print(f"Built list of 10 events: {events}")

    for event in consume_event(events):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {events}")


if __name__ == "__main__":
    main()
