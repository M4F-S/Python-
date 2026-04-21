def secure_archive(
    filename: str,
    action: str = "read",
    content: str = "",
) -> tuple[bool, str]:
    try:
        if action == "read":
            with open(filename, "r") as f:
                return (True, f.read())
        elif action == "write":
            with open(filename, "w") as f:
                f.write(content)
            return (True, "Content successfully written to file")
        else:
            return (False, f"Unknown action: {action!r}")
    except OSError as e:
        return (False, str(e))


if __name__ == "__main__":
    print("=== Cyber Archives Security ===")
    print()

    print("Using 'secure_archive' to read from a nonexistent file:")
    print(secure_archive("/not/existing/file"))
    print()

    print("Using 'secure_archive' to read from an inaccessible file:")
    print(secure_archive("/etc/shadow"))
    print()

    print("Using 'secure_archive' to read from a regular file:")
    ok, body = secure_archive("ancient_fragment.txt")
    print((ok, body))
    print()

    print("Using 'secure_archive' to write previous content to a new file:")
    print(secure_archive("/tmp/new_fragment.txt", "write", body))
