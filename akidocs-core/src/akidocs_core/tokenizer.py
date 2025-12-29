from akidocs_core.inline_tokenizer import tokenize_inline
from akidocs_core.tokens import Header, Paragraph, Token


def try_parse_header(block: str) -> Header | None:
    if not block.startswith("#"):
        return None

    stripped = block.lstrip("#")
    level = len(block) - len(stripped)

    if level > 6:
        return None

    if stripped != "" and stripped[0] not in (" ", "\t"):
        return None

    return Header(level=level, content=tokenize_inline(stripped.strip()))


def tokenize(text: str) -> list[Token]:
    text = text.replace("\r\n", "\n")

    if text == "":
        return []

    blocks = text.split("\n\n")
    tokens = []

    for block in blocks:
        block = block.strip()
        if block == "":
            continue

        header = try_parse_header(block)
        if header:
            tokens.append(header)
            continue

        tokens.append(Paragraph(content=tokenize_inline(block)))

    return tokens
