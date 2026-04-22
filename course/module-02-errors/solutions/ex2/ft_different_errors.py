def garden_operations(operation_number: int) -> None:
    if operation_number == 0:
        int("abc")
    elif operation_number == 1:
        _ = 1 / 0
    elif operation_number == 2:
        open("/non/existent/file")
    elif operation_number == 3:
        _ = "a" + 1  # type: ignore[operator]
    else:
        return


def test_error_types() -> None:
    for n in range(5):
        print(f"Testing operation {n}...")
        try:
            garden_operations(n)
        except ValueError as e:
            print(f"Caught ValueError: {e}")
        except ZeroDivisionError as e:
            print(f"Caught ZeroDivisionError: {e}")
        except FileNotFoundError as e:
            print(f"Caught FileNotFoundError: {e}")
        except TypeError as e:
            print(f"Caught TypeError: {e}")
        else:
            print("Operation completed successfully")

    # bonus: single multi-catch demo
    print()
    print("Multi-catch demo:")
    for n in range(4):
        try:
            garden_operations(n)
        except (ValueError, ZeroDivisionError,
                FileNotFoundError, TypeError) as e:
            print(f"Caught {type(e).__name__}: {e}")


if __name__ == "__main__":
    print("=== Garden Error Types Demo ===")
    test_error_types()
    print()
    print("All error types tested successfully!")
