import sys


if __name__ == "__main__":
    print("=== Command Quest ===")
    print(f"Program name: {sys.argv[0]}")
    args = sys.argv[1:]
    if len(args) == 0:
        print("No arguments provided!")
    else:
        print(f"Arguments received: {len(args)}")
        for i in range(len(args)):
            print(f"Argument {i + 1}: {args[i]}")
    print(f"Total arguments: {len(sys.argv)}")
