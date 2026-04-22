import sys


if __name__ == "__main__":
    print("=== Player Score Analytics ===")
    scores: list[int] = []
    for token in sys.argv[1:]:
        try:
            scores.append(int(token))
        except ValueError:
            print(f"Invalid parameter: '{token}'")

    if len(scores) == 0:
        print("No scores provided. Usage: python3 "
              "ft_score_analytics.py <score1> <score2> ...")
    else:
        total = sum(scores)
        avg = total / len(scores)
        high = max(scores)
        low = min(scores)
        print(f"Scores processed: {scores}")
        print(f"Total players: {len(scores)}")
        print(f"Total score: {total}")
        print(f"Average score: {avg}")
        print(f"High score: {high}")
        print(f"Low score: {low}")
        print(f"Score range: {high - low}")
