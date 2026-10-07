#!/usr/bin/env python3
"""Lint review-facing Markdown for GitHub math rendering hazards."""

from pathlib import Path
import re
import sys

FORBIDDEN_FRAGMENTS = (
    r"\operatorname",
    r"\left(",
    r"\left[",
    r"\left\{",
    r"\left\lceil",
    r"\left\lfloor",
    r"\left|",
    r"\right)",
    r"\right]",
    r"\right\}",
    r"\right\rceil",
    r"\right\rfloor",
    r"\right|",
    r"\bigl(",
    r"\bigr)",
)
STANDALONE_MARKDOWN_TOKENS = {"=", "+", "-", ">", "<"}

errors = []

for path in sorted(Path(".").rglob("*.md")):
    lines = path.read_text(encoding="utf-8").splitlines()
    in_fence = False
    in_display = False
    display_start = None

    for lineno, raw in enumerate(lines, start=1):
        stripped = raw.strip()

        if stripped.startswith("~~~") or stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        line = re.sub(r"`[^`]*`", "", raw)

        for fragment in FORBIDDEN_FRAGMENTS:
            if fragment in line:
                errors.append(
                    f"{path}:{lineno}: GitHub-incompatible math fragment {fragment}"
                )

        if stripped == "$$":
            in_display = not in_display
            if in_display:
                display_start = lineno
            continue

        if in_display and stripped in STANDALONE_MARKDOWN_TOKENS:
            errors.append(
                f"{path}:{lineno}: standalone Markdown token "
                f"{stripped!r} inside display math"
            )

    if in_display:
        errors.append(
            f"{path}:{display_start}: unmatched display-math delimiter $$"
        )

if errors:
    print("\n".join(errors))
    sys.exit(1)

print("Markdown math compatibility check: PASS")
