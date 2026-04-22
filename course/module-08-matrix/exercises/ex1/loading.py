"""Exercise 1 - package management demo.

Authorized: pandas, requests, matplotlib, numpy, sys, importlib.

Required behaviour:
- Without deps: report each missing package and print pip / Poetry install
  commands, then exit non-zero.
- With deps: generate 1000 numpy data points, wrap them in a pandas
  DataFrame, and save a matplotlib plot to matrix_analysis.png.
"""
import importlib
import sys


# TODO: list of (module_name, description).

def _version(name):  # type: ignore[no-untyped-def]
    # TODO: import + return __version__ or None if missing.
    raise NotImplementedError


def main() -> None:
    # TODO: dependency check + analysis.
    pass


if __name__ == "__main__":
    main()
