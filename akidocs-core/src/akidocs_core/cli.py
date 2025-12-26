import argparse
import os
import subprocess
import sys
from importlib.metadata import version
from pathlib import Path

from akidocs_core.renderer import render_pdf
from akidocs_core.tokenizer import tokenize


def open_file(path):
    """Open file in default application."""
    try:
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.run(["open", path], check=True)
        elif sys.platform.startswith("linux"):
            subprocess.run(["xdg-open", path], check=True)
        else:
            print(f"Cannot open file: unsupported platform '{sys.platform}'")
            return False
    except OSError as e:
        print(f"Cannot open file: {e}")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Cannot open file: command failed with exit code {e.returncode}")
        return False


def main():
    pkg_version = version("akidocs-core")

    parser = argparse.ArgumentParser(
        prog="aki",
        description=f"Convert Markdown files to PDF - akidocs-core {pkg_version}",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"akidocs-core {pkg_version}",
    )
    parser.add_argument(
        "-O",
        "--open",
        action="store_true",
        help="Open the PDF in default application after creation",
    )
    parser.add_argument("input", help="Input Markdown file")
    parser.add_argument("output", help="Output PDF file")

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    text = input_path.read_text(encoding="utf-8")
    tokens = tokenize(text)
    pdf_bytes = render_pdf(tokens)
    output_path.write_bytes(pdf_bytes)

    print(f"Written to {output_path}")
    if args.open:
        print(f"Opening {output_path}")
        open_file(output_path)


if __name__ == "__main__":
    main()
