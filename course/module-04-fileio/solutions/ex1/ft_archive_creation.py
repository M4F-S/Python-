import sys
from typing import IO


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file>")
        sys.exit(0)

    name = sys.argv[1]
    print("=== Cyber Archives Recovery & Preservation ===")
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

    transformed = ""
    for line in contents.split("\n"):
        if line == "":
            transformed += "\n"
        else:
            transformed += line + "#\n"

    print()
    print("Transform data:")
    print("---")
    print()
    print(transformed, end="")
    print("---")

    dest = input("Enter new file name (or empty): ")
    if dest == "":
        print("Not saving data.")
        sys.exit(0)

    print(f"Saving data to '{dest}'")
    out: IO[str]
    try:
        out = open(dest, "w")
    except OSError as e:
        print(f"Error opening file '{dest}': {e}")
        print("Data not saved.")
        sys.exit(0)

    try:
        out.write(transformed)
    finally:
        out.close()
    print(f"Data saved in file '{dest}'.")
