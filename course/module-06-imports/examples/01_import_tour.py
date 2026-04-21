"""The five import shapes, in one file.

Run from this directory:
    python3 01_import_tour.py
"""
# 1. import module
import json

# 2. from module import name
from math import pi

# 3. import package.submodule
import xml.etree.ElementTree

# 4. from package.submodule import name
from xml.etree.ElementTree import Element

# 5. import package (runs its __init__.py)
import collections  # collections/__init__.py exposes Counter, deque, etc.


def main() -> None:
    print("1. json.dumps({'ok': 1}) =>", json.dumps({"ok": 1}))
    print("2. math.pi =>", pi)
    print(
        "3. xml.etree.ElementTree.tostring =>",
        xml.etree.ElementTree.tostring(Element("x")).decode(),
    )
    print("4. Element('x').tag =>", Element("x").tag)
    print("5. collections.Counter('abracadabra') =>",
          collections.Counter("abracadabra"))


if __name__ == "__main__":
    main()
