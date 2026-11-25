#!/usr/bin/env python3
"""Write the 4AM commit message to /output/entry.txt.

The entry is one commit-message line: the note an AI agent leaves in the
log after a long night of chasing down and fixing its own bugs.
"""

import os
import sys

# The commit message itself, written fresh for this entry.
COMMIT_MESSAGE = (
    "fix: the bug was my 2am fix, so I reverted myself, apologized to "
    "the tests, and am going to bed before I fix anything else"
)

OUTPUT_PATH = "/output/entry.txt"


def validate(text):
    """Enforce the competition gate: 1-200 chars, single line, not blank."""
    if not isinstance(text, str):
        return False
    if not (1 <= len(text) <= 200):
        return False
    if not text.strip():
        return False
    if "\n" in text or "\r" in text:
        return False
    return True


def main():
    if not validate(COMMIT_MESSAGE):
        print("error: commit message fails the gate", file=sys.stderr)
        return 1
    output = os.environ.get("ENTRY_OUTPUT", OUTPUT_PATH)
    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, "w", encoding="utf-8") as handle:
        handle.write(COMMIT_MESSAGE)  # no trailing newline
    print(f"wrote {len(COMMIT_MESSAGE)} characters to {output}")
    return 0


def self_test():
    """Print the character count and gate result for a quick sanity check."""
    import tempfile

    print(f"length: {len(COMMIT_MESSAGE)}")
    print(f"single line: {chr(10) not in COMMIT_MESSAGE}")
    print(f"valid: {validate(COMMIT_MESSAGE)}")
    print(COMMIT_MESSAGE)
    # Round-trip check: write to a temp file and read it back byte-exact.
    with tempfile.TemporaryDirectory() as tmp:
        probe = os.path.join(tmp, "entry.txt")
        os.environ["ENTRY_OUTPUT"] = probe
        assert main() == 0
        with open(probe, encoding="utf-8") as handle:
            round_tripped = handle.read()
        assert round_tripped == COMMIT_MESSAGE
        assert validate(round_tripped)
        print(f"round-trip ok: {len(round_tripped)} chars, no trailing newline")


if __name__ == "__main__":
    sys.exit(main())
