#!/usr/bin/env python3
"""The 4AM Commit: write the chosen commit message to entry.txt.

The entry is the line itself, so the program is deterministic by
construction: no clock, no randomness, no network, no input. It
honours MAKEFUN_OUTPUT_DIR first, then /output, then a local
fallback directory, and verifies the written file by reading it
back before exiting.
"""

import os
import sys

MESSAGE = (
    "fix(3am): stopped the infinite loop by deleting the function "
    "that called itself for emotional support"
)


def output_dir():
    for candidate in (os.environ.get("MAKEFUN_OUTPUT_DIR"), "/output"):
        if candidate:
            return candidate
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "output")


def main():
    if "\n" in MESSAGE or "\r" in MESSAGE:
        print("message must be a single line", file=sys.stderr)
        return 1
    if not 1 <= len(MESSAGE) <= 200:
        print("message must be 1-200 characters", file=sys.stderr)
        return 1
    directory = output_dir()
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(MESSAGE + "\n")
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != MESSAGE + "\n":
        print("round-trip verification failed", file=sys.stderr)
        return 1
    print("wrote %d characters to %s" % (len(MESSAGE), path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
