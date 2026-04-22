"""Exercise 0 - detect whether we're inside a virtual environment.

Authorized: sys, os, site modules, print().

Required behaviour:
- Outside a venv: print the "still plugged in" report + creation instructions.
- Inside a venv: print the "welcome to the construct" report with the venv
  name, path, and site-packages directory.
"""
import os
import site
import sys


def _in_virtual_env() -> bool:
    # TODO: sys.prefix vs sys.base_prefix.
    raise NotImplementedError


def main() -> None:
    # TODO: branch on _in_virtual_env() and print the two reports.
    pass


if __name__ == "__main__":
    main()
