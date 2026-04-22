import os
import site
import sys


def _in_virtual_env() -> bool:
    return sys.prefix != getattr(sys, "base_prefix", sys.prefix)


def _env_name() -> str:
    explicit = os.environ.get("VIRTUAL_ENV")
    if explicit:
        return os.path.basename(explicit.rstrip(os.sep))
    return os.path.basename(sys.prefix.rstrip(os.sep))


def main() -> None:
    if _in_virtual_env():
        print("MATRIX STATUS: Welcome to the construct")
        print()
        print(f"Current Python: {sys.executable}")
        print(f"Virtual Environment: {_env_name()}")
        print(f"Environment Path: {sys.prefix}")
        print()
        print("SUCCESS: You're in an isolated environment!")
        print("Safe to install packages without affecting")
        print("the global system.")
        print()
        print("Package installation path:")
        site_paths = site.getsitepackages()
        # Prefer the one inside the venv prefix.
        preferred = next(
            (p for p in site_paths if p.startswith(sys.prefix)),
            site_paths[0] if site_paths else "<unknown>",
        )
        print(preferred)
    else:
        print("MATRIX STATUS: You're still plugged in")
        print()
        print(f"Current Python: {sys.executable}")
        print("Virtual Environment: None detected")
        print()
        print("WARNING: You're in the global environment!")
        print("The machines can see everything you install.")
        print()
        print("To enter the construct, run:")
        print("python -m venv matrix_env")
        print("source matrix_env/bin/activate  # On Unix")
        print("matrix_env\\Scripts\\activate   # On Windows")
        print()
        print("Then run this program again.")


if __name__ == "__main__":
    main()
