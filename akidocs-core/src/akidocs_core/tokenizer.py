from akidocs_core.inline_tokenizer import tokenize_inline
from akidocs_core.tokens import Header, Paragraph, Token


def try_parse_header(block: str) -> Header | None:
    if not block.startswith("#"):
        return None

    stripped = block.lstrip("#")
    level = len(block) - len(stripped)

    if level > 6:
        return None

    if stripped and stripped[0] not in (" ", "\t"):
        return None

    if stripped.endswith("#"):
        new_stripped = stripped.rstrip("#")
        if new_stripped and new_stripped[-1] in (" ", "\t"):
            stripped = new_stripped

    return Header(level=level, content=tokenize_inline(stripped.strip()))


def tokenize(text: str) -> list[Token]:
    text = text.replace("\r\n", "\n")

    if text == "":
        return []

    lines = text.split("\n")
    tokens: list[Token] = []
    paragraph_lines: list[str] = []

    def flush_paragraph() -> None:
        if not paragraph_lines:
            return

        parts: list[str] = []
        for i, line in enumerate(paragraph_lines):
            stripped_line = line.rstrip(" ")
            trailing_spaces = len(line) - len(stripped_line)
            if i < len(paragraph_lines) - 1 and trailing_spaces >= 2:
                parts.append(stripped_line + "\n")
            elif i < len(paragraph_lines) - 1:
                parts.append(stripped_line + " ")
            else:
                parts.append(stripped_line)

        joined = "".join(parts).strip()
        if joined:
            tokens.append(Paragraph(content=tokenize_inline(joined)))
        paragraph_lines.clear()

    for line in lines:
        stripped = line.strip()

        if stripped == "":
            flush_paragraph()
            continue

        header = try_parse_header(stripped)
        if header:
            flush_paragraph()
            tokens.append(header)
            continue

        paragraph_lines.append(line)

    flush_paragraph()

    return tokens
