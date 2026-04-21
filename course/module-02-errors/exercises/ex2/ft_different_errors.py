# Exercise 2 — ft_different_errors
# Authorized: print(), open(), int()
#
# garden_operations(n):
#   n == 0 -> ValueError         e.g. int("abc")
#   n == 1 -> ZeroDivisionError  e.g. 1/0
#   n == 2 -> FileNotFoundError  e.g. open("/non/existent/file")
#   n == 3 -> TypeError          e.g. "a" + 1 (needs `# type: ignore`)
#   other  -> return normally
#
# test_error_types() runs n=0..4, catching individually and then with a
# single multi-catch, showing the program keeps running.


def garden_operations(operation_number: int) -> None:
    pass


def test_error_types() -> None:
    pass


if __name__ == "__main__":
    pass
