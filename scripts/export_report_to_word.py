"""
Export the workshop report Markdown to a Word .docx file.

Usage (from repo root):
  python scripts/export_report_to_word.py

This script prefers system-installed Pandoc via pypandoc. If Pandoc isn't available,
it will download a local Pandoc copy via pypandoc (no admin required) and then convert.
"""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
INPUT_MD = ROOT / "VECTRI_Workshop_Report.md"
OUTPUT_DOCX = ROOT / "VECTRI_Workshop_Report.docx"


def main() -> int:
    if not INPUT_MD.exists():
        print(f"ERROR: Missing input file: {INPUT_MD}")
        return 2

    try:
        import pypandoc  # type: ignore
    except Exception:
        print("pypandoc is not installed.")
        print("Install it with:")
        print("  python -m pip install --user pypandoc")
        print("Then re-run:")
        print("  python scripts/export_report_to_word.py")
        return 3

    # Ensure pandoc is available; download locally if needed.
    try:
        _ = pypandoc.get_pandoc_path()
    except OSError:
        print("Pandoc not found. Downloading a local Pandoc copy via pypandoc...")
        try:
            pypandoc.download_pandoc()
        except Exception as e:
            print(f"ERROR: Failed to download Pandoc: {e}")
            print("Alternative: install Pandoc manually, then rerun this script.")
            return 4

    try:
        pypandoc.convert_file(
            str(INPUT_MD),
            to="docx",
            outputfile=str(OUTPUT_DOCX),
            extra_args=[
                "--from=gfm",
                "--metadata=title:VECTRI Workshop Report",
            ],
        )
    except Exception as e:
        print(f"ERROR: Conversion failed: {e}")
        return 5

    print(f"OK: Wrote {OUTPUT_DOCX}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


