# GitHub math rendering policy

For review-facing Markdown:

- do not use `\operatorname`; use `\mathrm{...}` for named operators;
- do not indent display-math delimiters `$$` inside lists; use inline math there or move the display block out of the list;
- do not leave literal tabs or control characters in Markdown;
- do not use raw Markdown-significant lines such as `=` or `+` inside display math;
- run `python scripts/check_markdown_math.py` before merging.

These restrictions apply to GitHub Markdown only. LaTeX `.tex` files may use normal LaTeX constructs.
