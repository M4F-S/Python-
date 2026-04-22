"""Exercise 2 - configuration from environment variables.

Authorized: os, sys, python-dotenv, file operations.

Required behaviour:
- Load .env if present (python-dotenv).
- Read MATRIX_MODE, DATABASE_URL, API_KEY, LOG_LEVEL, ZION_ENDPOINT.
- Print a "Configuration loaded" block and a security check block.
- CLI env vars (`FOO=bar python3 oracle.py`) must override .env values.
- Never print raw secrets - redact API_KEY.
"""
import os
import sys

# TODO: from dotenv import load_dotenv (with ImportError handling).


def main() -> None:
    # TODO
    pass


if __name__ == "__main__":
    main()
