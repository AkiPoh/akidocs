import sys
from pathlib import Path

from akidocs_core.renderer import render_pdf
from akidocs_core.tokenizer import tokenize


def main():
    if len(sys.argv) < 3:
        print("Usage: aki <input.md> <output.pdf>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not input_path.exists():
        print(f"Error: Fine not found: {input_path}")
        sys.exit(1)
    text = input_path.read_text(encoding="utf-8")
    tokens = tokenize(text)
    pdf_bytes = render_pdf(tokens)
    output_path.write_bytes(pdf_bytes)

    print(f"Written to {output_path}")


if __name__ == "__main__":
    main()
