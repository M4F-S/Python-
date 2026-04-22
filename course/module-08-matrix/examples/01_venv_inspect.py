"""Inspect the current Python environment.

Run without args:
    python3 01_venv_inspect.py
"""
import os
import site
import sys


def main() -> None:
    in_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    print(f"sys.executable        = {sys.executable}")
    print(f"sys.prefix            = {sys.prefix}")
    print(f"sys.base_prefix       = {getattr(sys, 'base_prefix', '<n/a>')}")
    print(f"in virtual env        = {in_venv}")
    print(f"VIRTUAL_ENV           = {os.environ.get('VIRTUAL_ENV', '<unset>')}")
    print(f"site.getsitepackages  = {site.getsitepackages()}")


if __name__ == "__main__":
    main()
