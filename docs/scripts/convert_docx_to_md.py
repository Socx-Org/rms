#!/usr/bin/env python3
"""Convert a .docx file to Markdown using mammoth + markdownify.

Usage:
  python3 scripts/convert_docx_to_md.py input.docx [output.md]
"""
import sys
import os

try:
    import mammoth
    from markdownify import markdownify as md
except Exception:
    print("Missing required packages. Install with: pip install mammoth markdownify", file=sys.stderr)
    sys.exit(2)


def convert(input_path, output_path=None):
    if not os.path.exists(input_path):
        raise FileNotFoundError(input_path)
    if output_path is None:
        base = os.path.splitext(input_path)[0]
        output_path = base + ".md"
    with open(input_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html = result.value

    markdown = md(html, heading_style="ATX")

    with open(output_path, "w", encoding="utf-8") as out:
        out.write(markdown)

    return output_path


def main():
    if len(sys.argv) < 2:
        print("Usage: convert_docx_to_md.py <input.docx> [output.md]")
        sys.exit(1)
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    try:
        outp = convert(inp, out)
        print(f"Wrote: {outp}")
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()
