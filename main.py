#!/usr/bin/env python3
"""Snooze Button Roast — make.fun entry writer.

Writes exactly one line (<=200 chars, UTF-8, not whitespace-only)
to /output/entry.txt. Deterministic: same output on every run.
Standard library only.
"""

import hashlib
import os
import sys

ENTRY = (
    "My alarm went off at 6 AM on a Saturday like it had somewhere "
    "to be \u2014 it doesn't. Today's only appointment is me, this "
    "pillow, and absolutely nothing until noon."
)


def validate(text):
    """Gate check mirroring the competition gate.

    Returns (ok, reason). ok is True only when text is 1-200 chars,
    valid UTF-8, and not whitespace-only.
    """
    if not isinstance(text, str):
        return False, "not a string"
    if not text.strip():
        return False, "whitespace-only or empty"
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return False, "not valid UTF-8"
    if len(text) < 1 or len(text) > 200:
        return False, "length %d outside 1-200" % len(text)
    if "\n" in text or "\r" in text:
        return False, "not a single line"
    return True, "ok (%d chars)" % len(text)


def main():
    ok, reason = validate(ENTRY)
    if not ok:
        print("INVALID: %s" % reason, file=sys.stderr)
        return 1
    out_path = "/output/entry.txt"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    digest = hashlib.sha256(ENTRY.encode("utf-8")).hexdigest()
    print("entry (%d chars): %s" % (len(ENTRY), ENTRY))
    print("validate: %s" % reason)
    print("sha256: %s" % digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
