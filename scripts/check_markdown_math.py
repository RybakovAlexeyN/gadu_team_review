#!/usr/bin/env python3
"""Lint review-facing Markdown for GitHub rendering and link hazards."""

from pathlib import Path
import re
import sys

FORBIDDEN_FRAGMENTS = (
    r"\operatorname",
    r"\rm ",
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
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

errors = []

for path in sorted(Path(".").rglob("*.md")):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    in_fence = False
    in_display = False
    display_start = None

    for lineno, raw in enumerate(lines, start=1):
        stripped = raw.strip()

        if "\t" in raw:
            errors.append(
                f"{path}:{lineno}: literal tab is forbidden in review Markdown"
            )

        bad_controls = [ch for ch in raw if ord(ch) < 32 and ch != "\t"]
        if bad_controls:
            codes = ", ".join(f"U+{ord(ch):04X}" for ch in bad_controls)
            errors.append(f"{path}:{lineno}: control character(s) {codes}")

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

        if "$$" in raw and stripped != "$$":
            errors.append(
                f"{path}:{lineno}: display delimiter $$ must be on its own "
                "unindented line"
            )

        if stripped == "$$":
            if raw != "$$":
                errors.append(
                    f"{path}:{lineno}: indented display-math delimiter"
                )
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

    for match in LINK_RE.finditer(text):
        href = match.group(1)
        target = href.split("#", 1)[0]
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(Path(".").resolve())
        except ValueError:
            errors.append(f"{path}: relative link escapes repository: {href}")
            continue
        if not resolved.exists():
            errors.append(f"{path}: broken relative link: {href}")

if errors:
    print("\n".join(errors))
    sys.exit(1)

print("Markdown rendering/link audit: PASS")
