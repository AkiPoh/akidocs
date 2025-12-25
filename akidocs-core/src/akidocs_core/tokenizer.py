from akidocs_core.tokens import Header, Paragraph, Token


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

        if block.startswith("#"):
            stripped = block.lstrip("#")
            level = min(len(block) - len(stripped), 6)
            content = stripped.strip()
            tokens.append(Header(level=level, content=content))
        else:
            tokens.append(Paragraph(content=block))

    return tokens
