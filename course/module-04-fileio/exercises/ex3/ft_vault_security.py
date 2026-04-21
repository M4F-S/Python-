# Exercise 3 — ft_vault_security
# Authorized: open(), read(), write(), print()
#
# secure_archive(filename, action="read", content="") -> tuple[bool, str]
#   read  : (True, file_contents)                     or (False, err)
#   write : (True, "Content successfully written to file") or (False, err)
# Use `with open(...)` in both branches.


def secure_archive(
    filename: str,
    action: str = "read",
    content: str = "",
) -> tuple[bool, str]:
    pass


if __name__ == "__main__":
    pass
