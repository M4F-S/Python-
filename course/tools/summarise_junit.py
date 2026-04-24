"""Render a JUnit XML report as a Markdown summary for GitHub Actions.

Usage:
    python -m tools.summarise_junit <path-to-junit.xml>

Emits a heading plus a table per testsuite. Intended to be redirected
into $GITHUB_STEP_SUMMARY inside a workflow step.
"""
from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {argv[0]} <junit.xml>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print(f"# Grader\n\n`{path}` not produced.", flush=True)
        return 0

    tree = ET.parse(path)
    root = tree.getroot()
    suites = root.findall(".//testsuite") or [root]

    print("# Classroom grader results")
    for suite in suites:
        total = int(suite.get("tests", 0))
        failed = int(suite.get("failures", 0)) + int(suite.get("errors", 0))
        skipped = int(suite.get("skipped", 0))
        passed = total - failed - skipped
        print()
        print(f"## {suite.get('name', 'tests')}")
        print()
        print("| Status | Count |")
        print("|--------|------:|")
        print(f"| Passed  | {passed} |")
        print(f"| Failed  | {failed} |")
        print(f"| Skipped | {skipped} |")
        if failed:
            print()
            print("<details><summary>Failing cases</summary>\n")
            for case in suite.findall(".//testcase"):
                failure = case.find("failure") or case.find("error")
                if failure is None:
                    continue
                name = f"{case.get('classname', '')}::{case.get('name', '')}"
                print(f"- **{name}** — {failure.get('message', 'failed')}")
            print()
            print("</details>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
