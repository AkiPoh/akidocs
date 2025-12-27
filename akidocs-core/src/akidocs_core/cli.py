import argparse
import os
import sys
from importlib.metadata import version
from pathlib import Path

from akidocs_core.opener import open_file
from akidocs_core.renderer import render_pdf
from akidocs_core.styles import STYLES
from akidocs_core.tokenizer import tokenize


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
        "-o",
        "--open",
        action="store_true",
        help="Open the PDF in default application after creation",
    )
    parser.add_argument(
        "-s",
        "--style",
        default="generic",
        choices=list(STYLES.keys()),
        help="Document style (default: generic)",
    )
    parser.add_argument(
        "-n",
        "--non-interactive",
        action="store_true",
        help="Never prompt; error if output file exists",
    )
    parser.add_argument("input", help="Input Markdown file")
    parser.add_argument("output", help="Output PDF file")

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    if output_path.exists():
        if args.non_interactive:
            print(f"Error: {output_path} already exists")
            sys.exit(1)
        else:
            response = input(f"{output_path} already exists. Overwrite? [y/N] ")
            if response.lower() != "y":
                print(f"Aborted: {output_path} already exists")
                sys.exit(1)

    style = STYLES[args.style]

    text = input_path.read_text(encoding="utf-8")
    tokens = tokenize(text)
    pdf_bytes = render_pdf(tokens, style)
    output_path.write_bytes(pdf_bytes)

    print(f"Written to {output_path}")
    if args.open:
        print(f"Opening {output_path}")
        if not os.environ.get("AKIDOCS_TEST_MODE"):
            open_file(output_path)
        else:
            print(
                f"Failed to open due to AKIDOCS_TEST_MODE being {os.environ.get('AKIDOCS_TEST_MODE')}"
            )


if __name__ == "__main__":
    main()
