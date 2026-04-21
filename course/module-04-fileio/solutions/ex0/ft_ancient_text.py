import sys
from typing import IO


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file>")
        sys.exit(0)

    name = sys.argv[1]
    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file '{name}'")

    f: IO[str]
    try:
        f = open(name, "r")
    except OSError as e:
        print(f"Error opening file '{name}': {e}")
        sys.exit(0)

    try:
        contents = f.read()
        print("---")
        print()
        print(contents, end="")
        print()
        print("---")
    finally:
        f.close()
        print(f"File '{name}' closed.")
