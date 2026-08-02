import sys


def parse_scores(args: list[str]) -> tuple[list[int], list[str]]:
    scores: list[int] = []
    invalid: list[str] = []
    for arg in args:
        try:
            scores.append(int(arg))
        except ValueError:
            invalid.append(arg)
    return scores, invalid


def print_stats(scores: list[int]) -> None:
    total = sum(scores)
    average = total / len(scores)
    highest = max(scores)
    lowest = min(scores)
    print(f"Scores processed: {scores}")
    print(f"Total players: {len(scores)}")
    print(f"Total score: {total}")
    print(f"Average score: {round(average, 1)}")
    print(f"High score: {highest}")
    print(f"Low score: {lowest}")
    print(f"Score range: {highest - lowest}")


def main() -> None:
    print("=== Player Score Analytics ===")
    args = sys.argv[1:]
    scores, invalid = parse_scores(args)

    for bad in invalid:
        print(f"Invalid parameter: '{bad}'")

    if not scores:
        print("No scores provided. Usage: "
              "python ft_score_analytics.py <score1> <score2> ...")
        return

    print_stats(scores)


if __name__ == "__main__":
    main()
